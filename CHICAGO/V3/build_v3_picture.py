#!/usr/bin/env python3
import argparse, json, math, re, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

FPS=25
W1080,H1080=1920,1080

EXPLAINER_LABELS={
    'transfer':['SURFACE FREIGHT','TRANSFER / LOWERING','TUNNEL CARS'],
    'basement':['TUNNEL CAR','BUILDING CONNECTION','BASEMENT'],
    'coal':['COAL TO BOILERS','FUEL IS CONSUMED','ASH REMOVAL'],
    'water':['RIVER WATER','CONNECTED TUNNELS','BASEMENTS / UTILITIES'],
    'survivor':['LEFT UNDERGROUND','RECOVERED IN 1996','PRESERVED TODAY'],
}
ACCENT=(242,138,58,255)
PAPER=(239,232,213,255)
MUTED=(176,180,174,255)
DARK=(16,22,27,224)

def run(cmd, cwd=None):
    p=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-5000:])
    return p.stdout

def ass_time(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def resolve_assets(root):
    out={}
    for p in root.rglob('*'):
        if p.is_file():
            out.setdefault(p.name,p)
    return out

def crop_variant(src:Path,dst:Path,which='detail'):
    im=Image.open(src).convert('RGB')
    if which=='detail':
        box=(int(im.width*.12),int(im.height*.10),int(im.width*.88),int(im.height*.90))
    elif which=='map_detail':
        box=(int(im.width*.40),int(im.height*.12),int(im.width*.98),int(im.height*.90))
    elif which=='map_overview':
        box=(int(im.width*.01),int(im.height*.03),int(im.width*.56),int(im.height*.97))
    else:
        box=(0,0,im.width,im.height)
    crop=im.crop(box)
    crop=ImageOps.fit(crop,(1920,1080),method=Image.Resampling.LANCZOS)
    crop.save(dst,quality=95)
    return dst

def explainer_overlay(kind,phase,out,font_reg,font_bold):
    im=Image.new('RGBA',(1920,1080),(0,0,0,0))
    d=ImageDraw.Draw(im)
    if kind=='gauge':
        # Compact upper-left gauge card; leaves the entire lower third free.
        x,y,w,h=70,78,600,205
        d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=DARK,outline=(104,112,111,180),width=2)
        d.rectangle((x,y,x+7,y+h),fill=ACCENT)
        f1=ImageFont.truetype(str(font_bold),31)
        f2=ImageFont.truetype(str(font_reg),22)
        d.text((x+34,y+24),'2-FOOT GAUGE',font=f1,fill=PAPER)
        d.text((x+34,y+69),'SCHEMATIC — NOT TO SCALE',font=f2,fill=MUTED)
        yy=y+137
        d.line((x+50,yy,x+490,yy),fill=PAPER,width=4)
        d.line((x+50,yy+46,x+490,yy+46),fill=PAPER,width=4)
        d.line((x+455,yy+5,x+455,yy+41),fill=ACCENT,width=3)
        d.text((x+235,yy+10),'2 FT',font=f2,fill=PAPER)
    else:
        labels=EXPLAINER_LABELS[kind]
        x,y,w,h=70,78,690,215
        d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=DARK,outline=(86,96,98,175),width=2)
        d.rectangle((x,y,x+7,y+h),fill=ACCENT)
        small=ImageFont.truetype(str(font_reg),20)
        bold=ImageFont.truetype(str(font_bold),32)
        tiny=ImageFont.truetype(str(font_reg),18)
        d.text((x+35,y+22),f'PROCESS  •  STEP {phase+1} / 3',font=small,fill=ACCENT)
        d.text((x+35,y+62),labels[phase],font=bold,fill=PAPER)
        # compact progress rail, not three giant cards
        rail_y=y+145
        for j,t in enumerate(labels):
            px=x+37+j*205
            active=(j==phase)
            fill=ACCENT if active else ((166,170,164,230) if j<phase else (104,112,111,190))
            d.ellipse((px,rail_y,px+16,rail_y+16),fill=fill)
            short=t if len(t)<=18 else t[:16]+'…'
            d.text((px+24,rail_y-2),short,font=tiny,fill=PAPER if active else MUTED)
            if j<2:
                d.line((px+165,rail_y+8,px+195,rail_y+8),fill=(117,126,126,180),width=2)
    im.save(out)
    return out

def motion_filter(width,height,count,mode,amount=.025):
    p=f'(on/{max(1,count-1)})'
    ease=f'({p}*{p}*(3-2*{p}))'
    z=f'(1.012+{amount}*{ease})' if mode=='push' else f'(1.012+{amount}*(1-{ease}))' if mode=='pull' else '1.032'
    x=f'(W-W/{z})*0.5' if mode!='pan' else f'(W-W/{z})*(0.2+0.6*{p})'
    y=f'(H-H/{z})*0.48'
    return f"perspective=x0='{x}':y0='{y}':x1='{x}+W/{z}':y1='{y}':x2='{x}':y2='{y}+H/{z}':x3='{x}+W/{z}':y3='{y}+H/{z}':sense=source:eval=frame:interpolation=cubic"

def make_shot(a,b,asset,scene,kind='reconstruction',motion='static',text='',chapter='',explainer='',phase=0,variant='v3'):
    return {'a':round(a*FPS),'b':round(b*FPS),'asset':str(asset),'source':str(asset),'scene':scene,
            'kind':kind,'motion':motion,'text':text,'chapter':chapter,'explainer':explainer,'phase':phase,'variant':variant}

def patch_plan(orig, assets, gen):
    shots=[dict(s) for s in orig]
    for s in shots:
        name=s['asset'].replace('\\\\','/').split('/')[-1]
        if name not in assets:
            raise RuntimeError(f'Missing work asset {name}')
        s['asset']=str(assets[name])

    byscene={}
    for s in shots:
        byscene.setdefault(s['scene'],[]).append(s)

    # 01:10–02:34 — one-way archival progression: context -> detail for each source, no A/B/A bouncing.
    a14=assets['A14_LOC_State_Street_1905_full_archive.png']
    a13=assets['A13_LOC_State_Street_1903_full_archive.png']
    a15=assets['A15_LOC_Wabash_Avenue_c1900_full_archive.png']
    a14d=crop_variant(a14,gen/'street_1905_detail.jpg','detail')
    a13d=crop_variant(a13,gen/'street_1903_detail.jpg','detail')
    a15d=crop_variant(a15,gen/'wabash_detail.jpg','detail')
    street=[
      make_shot(70.32,82.04,a14,'V3_STREET_1','archive','pan'),
      make_shot(82.04,94.32,a14d,'V3_STREET_2','archive','static','STREET-LEVEL CONGESTION'),
      make_shot(94.32,108.00,a13,'V3_STREET_3','archive','pan'),
      make_shot(108.00,122.16,a13d,'V3_STREET_4','archive','static'),
      make_shot(122.16,137.00,a15,'V3_STREET_5','archive','pan'),
      make_shot(137.00,153.68,a15d,'V3_STREET_6','archive','static'),
    ]

    # 05:49–07:17 — deliberate map overview -> map detail -> archive evidence -> different map crop -> later map.
    a02=assets['A02_IllinoisTunnelMap1910_full_map.png']
    a12=assets['A12_1937_Chicago_Tunnel_Terminal_Company_full_map.png']
    a03=assets['A03_ChicagoTunnelFieldsTrain_full_archive.png']
    a02d=crop_variant(a02,gen/'map1910_detail.jpg','map_detail')
    a02o=crop_variant(a02,gen/'map1910_overview.jpg','map_overview')
    mapseq=[
      make_shot(349.20,363.00,a02,'V3_MAP_1','map','static'),
      make_shot(363.00,377.36,a02d,'V3_MAP_2','map','push','NETWORK DETAIL'),
      make_shot(377.36,394.08,a03,'V3_MAP_3','archive','pan'),
      make_shot(394.08,419.24,a02o,'V3_MAP_4','map','pan','~60 MILES'),
      make_shot(419.24,437.28,a12,'V3_MAP_5','map','pull'),
    ]

    # Coal: remove 1.04s + 1.16s flash pair by using one phase-2 visual.
    coal_merge=None
    s081=next(s for s in shots if s['scene']=='S081')
    coal_merge=make_shot(509.92,512.12,Path(s081['asset']),'V3_COAL_MERGE','reconstruction','static','', '', 'coal',2)

    # Late-film slideshow consolidation.
    s205=Path(next(s for s in shots if s['scene']=='S205')['asset'])
    s207=Path(next(s for s in shots if s['scene']=='S207')['asset'])
    s210=Path(next(s for s in shots if s['scene']=='S210')['asset'])
    a16=assets['A16_LOC_Illinois_Central_freight_1942_full_archive.png']
    a04=assets['A04_TunnelCoalDelivery_full_archive.png']
    s216=Path(next(s for s in shots if s['scene']=='S216')['asset'])
    s217=Path(next(s for s in shots if s['scene']=='S217')['asset'])
    s218=Path(next(s for s in shots if s['scene']=='S218')['asset'])
    s219=Path(next(s for s in shots if s['scene']=='S219')['asset'])
    s222=Path(next(s for s in shots if s['scene']=='S222')['asset'])
    late=[
      make_shot(1145.20,1158.28,s205,'V3_LATE_1','reconstruction','pull'),
      make_shot(1158.28,1167.68,s207,'V3_LATE_2','reconstruction','static'),
      make_shot(1167.68,1177.52,s210,'V3_LATE_3','reconstruction','push'),
      make_shot(1177.52,1181.52,a16,'V3_LATE_4','archive','static'),
      make_shot(1181.52,1185.52,a04,'V3_LATE_5','archive','static'),
      make_shot(1185.52,1192.44,s216,'V3_LATE_6','reconstruction','static'),
      make_shot(1192.44,1204.60,s217,'V3_LATE_7','reconstruction','pull'),
      make_shot(1204.60,1209.44,s218,'V3_LATE_8','reconstruction','static','JULY 1959'),
      make_shot(1209.44,1213.28,s219,'V3_LATE_9','reconstruction','static'),
      make_shot(1213.28,1218.40,s222,'V3_LATE_10','reconstruction','static'),
    ]

    out=[]
    for s in shots:
        a=s['a']/FPS; b=s['b']/FPS
        if b<=70.32 or a>=153.68:
            out.append(s)
    out=[s for s in out if not (s['b']/FPS>349.20 and s['a']/FPS<437.28)]
    out=[s for s in out if not (s['b']/FPS>509.92 and s['a']/FPS<512.12)]
    out=[s for s in out if not (s['b']/FPS>1145.20 and s['a']/FPS<1218.40)]
    out += street + mapseq + [coal_merge] + late
    out.sort(key=lambda s:s['a'])

    # Merge only truly identical adjacent V3 shots if produced by replacement.
    merged=[]
    for s in out:
        if merged and merged[-1]['b']==s['a'] and merged[-1]['asset']==s['asset'] and merged[-1]['motion']==s['motion'] and merged[-1].get('explainer')==s.get('explainer') and not s.get('text') and not s.get('chapter'):
            merged[-1]['b']=s['b']
        else:
            merged.append(s)

    if merged[0]['a']!=0 or merged[-1]['b']!=round(1290.72*FPS):
        raise RuntimeError(f'Coverage endpoints bad: {merged[0]["a"]}, {merged[-1]["b"]}')
    for i in range(len(merged)-1):
        if merged[i]['b']!=merged[i+1]['a']:
            raise RuntimeError(f'Gap/overlap at {i}: {merged[i]["b"]} != {merged[i+1]["a"]}')
    return merged

def render_shot(s,i,outdir,overlaydir,font_reg,font_bold):
    out=outdir/f'{i:03d}.mp4'
    width,height=960,540
    count=s['b']-s['a']
    args=['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','25','-loop','1','-i',s['asset']]
    graph=f'[0:v]scale={width}:{height}:flags=lanczos,format=yuv444p'
    if s.get('motion')!='static':
        graph+=','+motion_filter(width,height,count,s['motion'])
    graph+=',setsar=1[base]'
    cur='base'
    if s.get('explainer'):
        ov=overlaydir/f"{s['explainer']}_{s.get('phase',0)}.png"
        if not ov.exists():
            explainer_overlay(s['explainer'],int(s.get('phase',0)),ov,font_reg,font_bold)
        args += ['-i',str(ov)]
        graph += f';[1:v]scale={width}:{height}[ov];[base][ov]overlay=0:0:format=auto[cmp]'
        cur='cmp'

    filters=[]
    # provenance moved to upper-right, out of caption-safe area
    if s.get('scene')!='end':
        if s.get('kind')=='reconstruction':
            filters.append("drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='AI RECONSTRUCTION':fontsize=11:fontcolor=0xEEE6D4@0.80:shadowcolor=black@0.55:shadowx=1:shadowy=1:x=w-tw-22:y=18")
        elif s.get('kind') in ('archive','map'):
            filters.append("drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='HISTORICAL SOURCE':fontsize=10:fontcolor=0xD1D0C7@0.82:shadowcolor=black@0.65:shadowx=1:shadowy=1:x=w-tw-22:y=18")

    title=s.get('chapter') or (s.get('text') if not s.get('explainer') else '')
    if title:
        safe=title.replace("'","’").replace(':','\\:')
        filters.append(f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{safe}':fontsize=22:fontcolor=0xF1E9D7:shadowcolor=black@0.8:shadowx=1:shadowy=1:x=w*0.045:y=h*0.09:enable='lt(t,3.4)'")
    filters.append('format=yuv420p')
    graph += f';[{cur}]'+','.join(filters)+'[v]'
    args += ['-filter_complex',graph,'-map','[v]','-frames:v',str(count),'-an',
             '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','25','-g','50',
             '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(out)]
    run(args)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--shots',required=True)
    ap.add_argument('--assets-root',required=True)
    ap.add_argument('--work',required=True)
    ap.add_argument('--output-video',required=True)
    ap.add_argument('--plan-out',required=True)
    args=ap.parse_args()

    work=Path(args.work); work.mkdir(parents=True,exist_ok=True)
    gen=work/'generated'; gen.mkdir(exist_ok=True)
    clips=work/'clips'; clips.mkdir(exist_ok=True)
    overlays=work/'overlays'; overlays.mkdir(exist_ok=True)
    assets=resolve_assets(Path(args.assets_root))
    orig=json.loads(Path(args.shots).read_text(encoding='utf-8-sig'))
    plan=patch_plan(orig,assets,gen)
    Path(args.plan_out).write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')

    font_reg=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    font_bold=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
    rendered=[]
    for i,s in enumerate(plan):
        p=render_shot(s,i,clips,overlays,font_reg,font_bold)
        rendered.append(p)
        if i%20==0:
            print(f'rendered {i+1}/{len(plan)}',flush=True)

    listing=work/'concat.txt'
    listing.write_text('\n'.join("file '"+str(p.resolve()).replace("'","'\\''")+"'" for p in rendered)+'\n',encoding='utf-8')
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(listing),
         '-c','copy','-movflags','+faststart',args.output_video])
    print(json.dumps({'shots':len(plan),'video':args.output_video},indent=2))

if __name__=='__main__':
    main()
