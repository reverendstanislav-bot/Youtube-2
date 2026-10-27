"""Deterministic frame-based motion compositor. No video AI and no Resolve control.
Pillow draws native animation masks/paths; illustration pixels come from ImageGen.
Run: python render_motion.py --stills, or python render_motion.py [--fps 25]
Frame rate here is a preview setting, not a claim about the production timeline.
"""
from pathlib import Path
import argparse, csv, hashlib, json, math, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
W,H=1672,940
DURATION=8.0
S=2
GOLD=(223,163,58)
BLUE=(43,112,153)
INK=(31,48,56)
FONT=Path('C:/Windows/Fonts/consola.ttf')
BASES={}
OBJECTS={}

def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def phase(t,start,dur): return ease((t-start)/dur)
def env(t,start,end): return phase(t,start,.45)*(1-phase(t,end,.6))
def pts(seq): return [(round(x*S),round(y*S)) for x,y in seq]
def smooth(seq,n=12):
    out=[];p=[seq[0],*seq,seq[-1]]
    for i in range(1,len(p)-2):
        a,b,c,e=p[i-1:i+3]
        for k in range(n):
            t=k/n
            out.append(tuple(.5*((2*b[j])+(-a[j]+c[j])*t+(2*a[j]-5*b[j]+4*c[j]-e[j])*t*t+(-a[j]+3*b[j]-3*c[j]+e[j])*t*t*t) for j in (0,1)))
    return out+[seq[-1]]
def partial(seq,f):
    if f<=0:return []
    lengths=[math.dist(a,b) for a,b in zip(seq,seq[1:])]
    remain=sum(lengths)*min(1,f);out=[seq[0]]
    for a,b,length in zip(seq,seq[1:],lengths):
        if remain>=length:out.append(b);remain-=length
        else:
            p=remain/max(length,.001);out.append((a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p));break
    return out
def trace(d,seq,p,color=GOLD,width=4,alpha=230):
    q=partial(seq,p)
    if len(q)>1:
        d.line(pts(q),fill=(*color,int(alpha)),width=round(width*S),joint='curve')
        x,y=q[-1];r=width*.55*S;d.ellipse((x*S-r,y*S-r,x*S+r,y*S+r),fill=(*color,int(alpha)))
def label(d,text,pos,opacity=1,size=28):
    if opacity<=0:return
    font=ImageFont.truetype(str(FONT),size*S)
    d.text((pos[0]*S,pos[1]*S),text,font=font,fill=(*INK,int(255*opacity)),stroke_width=2*S,stroke_fill=(249,249,240,int(170*opacity)))
def polygon(d,seq,alpha=30,color=GOLD): d.polygon(pts(seq),fill=(*color,int(alpha)))
def mark(d,seq,t,start,duration=1.4,width=16,color=GOLD):
    trace(d,seq,phase(t,start,duration),color,width,70)
    trace(d,seq,phase(t,start,duration),color,2.5,220)

def load_assets(plan):
    for shot in plan:
        im=Image.open(ROOT/shot['base']).convert('RGBA')
        if im.size!=(W,H+1) and im.size!=(W,H): raise ValueError((shot['id'],im.size))
        BASES[shot['id']]=im.crop((0,0,W,H))
    keys=[]
    if any(s['id']=='M06' for s in plan):keys.append('M06_AIRCRAFT')
    if any(s['id']=='M08' for s in plan):keys.append('M08_MODULE')
    for key in keys:
        im=Image.open(ROOT/'assets'/f'{key}.png').convert('RGBA')
        bounds=im.getchannel('A').getbbox()
        if not bounds or im.getchannel('A').getextrema()[0]==255: raise ValueError('Missing true alpha: '+key)
        OBJECTS[key]=im.crop(bounds)

def object_layer(frame,key,cx,top,width):
    im=OBJECTS[key];size=(round(width),round(width*im.height/im.width))
    obj=im.resize(size,Image.Resampling.LANCZOS)
    x=cx-width/2;xi=math.floor(x);yi=math.floor(top)
    padded=Image.new('RGBA',(size[0]+6,size[1]+6));padded.alpha_composite(obj,(3,3))
    padded=padded.transform(padded.size,Image.Transform.AFFINE,(1,0,-(x-xi),0,1,-(top-yi)),resample=Image.Resampling.BICUBIC)
    frame.alpha_composite(padded,(xi-3,yi-3))

def overlay_for(shot,t):
    layer=Image.new('RGBA',(W*S,H*S));d=ImageDraw.Draw(layer)
    sid=shot['id']
    if sid=='M01':
        seq=[(326,786),(326,584),(606,540)]
        polygon(d,[(325,590),(603,548),(607,782),(588,857),(329,785)],27*phase(t,1,1))
        trace(d,seq,phase(t,.7,2.2),GOLD,3.4)
        trace(d,[(366,148),(424,148),(562,292)],phase(t,3.8,1),INK,1.7,200)
        label(d,'PREFAB ROOMS',(1100,780),phase(t,2.1,.6))
        trace(d,[(1084,793),(1008,793),(845,729)],phase(t,2,1),INK,1.7,200)
        label(d,'SNOW-COVERED ARCH',(75,130),phase(t,4.4,.6),27)
    elif sid=='M02':
        # Under-label marker strokes stay in the paper margin, never blanket a drawing.
        for seq,start in [([(150,902),(308,902)],.7), ([(707,902),(968,902)],2.7), ([(1288,902),(1482,902)],4.7)]:
            trace(d,seq,phase(t,start,.8),GOLD,8,125)
        trace(d,[(178,615),(178,299)],phase(t,1,1.1),BLUE,4)
        # Keep original arch drawing unobscured; no approximate contour over it.
    elif sid=='M03':
        left=[(31,822),(33,637),(75,477),(123,349),(158,207),(199,135),(288,82),(406,49),(515,65),(624,117),(707,206),(734,350),(792,490),(829,816)]
        right=[(871,822),(900,664),(947,546),(1011,461),(1101,407),(1190,363),(1287,375),(1394,398),(1484,454),(1552,548),(1598,666),(1649,820)]
        # Do not invent a new hard outline over an irregular illustrative section.
        trace(d,[(241,901),(610,901)],phase(t,.7,1.3),BLUE,7,130)
        trace(d,[(1082,901),(1510,901)],phase(t,3,1.3),GOLD,7,145)
        trace(d,smooth([(1042,534),(1135,500),(1234,475),(1331,487),(1427,530)]),phase(t,3.2,1.9),GOLD,22,43)
        label(d,'INITIAL OPENING',(230,861),phase(t,1,.6),29)
        label(d,'REDUCED OPENING',(1090,861),phase(t,3.4,.6),29)
        # Three short downward cues emphasize intrusion; no numerical rate implied.
        for x,y in [(1090,427),(1240,396),(1400,436)]:
            p=phase(t,5.5,1);end=y+46*p
            trace(d,[(x,y),(x,end)],1,GOLD,3,200*p)
            if p>.05:d.line(pts([(x-7,end-8),(x,end),(x+7,end-8)]),fill=(*GOLD,int(200*p)),width=3*S)
    elif sid=='M04':
        # Two disconnected systems; cold water accent and warm waste cavity edge.
        trace(d,[(254,800),(254,280)],phase(t,.9,2.2),BLUE,5,220)
        waste=[(1460,290),(1458,412),(1437,445),(1361,454),(1271,480),(1250,545),(1272,627),(1352,675),(1445,688),(1553,665),(1610,593),(1604,491)]
        trace(d,smooth(waste),phase(t,3.8,2.3),GOLD,3,180)
        trace(d,[(375,820),(759,820)],phase(t,1.8,.8),BLUE,5,170)
        trace(d,[(1228,820),(1580,820)],phase(t,4.6,.8),GOLD,5,170)
    elif sid=='M05':
        # Split at the visible depth-break symbol; do not color across it.
        trace(d,[(940,200),(940,537)],phase(t,.8,1.7),BLUE,5,220)
        trace(d,[(940,584),(940,851)],phase(t,2.5,1.6),BLUE,5,220)
        sed=[(877,864),(913,850),(951,850),(990,861),(1035,854),(1070,846)]
        mark(d,sed,t,4.3,1.4,14)
        label(d,'1966 CORE',(1035,383),phase(t,1.8,.7))
        trace(d,[(1020,398),(982,398),(950,417)],phase(t,1.8,.7),INK,1.7,220)
        label(d,'BASAL SEDIMENT',(1120,812),phase(t,4.8,.7))
        trace(d,[(1104,829),(1070,829),(1000,862)],phase(t,4.7,.8),INK,1.7,210)
    elif sid=='M06':
        # Beam is a conceptual sensor illustration, not simulated radar data.
        cx=430+700*phase(t,.7,5.8)
        a=env(t,.8,6.5)
        polygon(d,[(cx+70,143),(cx-50,581),(cx+270,581)],26*a)
        trace(d,[(cx+70,143),(cx-50,581)],1,GOLD,1.5,130*a)
        trace(d,[(cx+70,143),(cx+270,581)],1,GOLD,1.5,130*a)
        if t>3:
            mark(d,[(650,584),(820,587),(995,582),(1173,591)],t,3,2.1,12)
        label(d,'BURIED STRUCTURES',(1030,685),phase(t,4.4,.7),27)
        trace(d,[(1020,698),(974,698),(925,598)],phase(t,4.3,.9),INK,1.7,210)
    elif sid=='M07':
        # Accent actual snow contact and falling blocks; workers themselves remain still.
        trace(d,[(96,304),(148,327),(199,350)],phase(t,.8,1),GOLD,8,120)
        trace(d,[(744,473),(800,503),(850,555)],phase(t,2.5,1.1),BLUE,5,180)
        for seq,start in [([(203,904),(352,904)],.9), ([(878,904),(1100,904)],2.9), ([(1335,904),(1557,904)],4.8)]:
            trace(d,seq,phase(t,start,.8),GOLD,7,150)
    elif sid=='M08':
        hook_y=120-125*phase(t,1,3.5)
        if hook_y>0:trace(d,[(830,0),(830,hook_y)],1,INK,1.2,180)
        trace(d,smooth([(170,638),(262,608),(356,610),(468,643),(584,648),(709,609),(801,611),(905,650),(1018,650),(1125,628),(1245,628),(1393,653),(1535,653)]),phase(t,3.4,2.3),GOLD,11,80)
        label(d,'PLANT REMOVED',(1055,125),phase(t,1.8,.7))
        label(d,'STRUCTURES REMAINED',(1000,770),phase(t,4.5,.7),27)
        trace(d,[(987,781),(927,781),(872,697)],phase(t,4.4,1),INK,1.7,210)
    return layer.resize((W,H),Image.Resampling.LANCZOS)

def compose(shot,t,overlay_only=False):
    overlay=overlay_for(shot,t)
    if overlay_only:return overlay
    im=BASES[shot['id']].copy()
    if shot['id']=='M06':
        cx=430+700*phase(t,.7,5.8)
        object_layer(im,'M06_AIRCRAFT',cx,62,370)
    if shot['id']=='M08':
        object_layer(im,'M08_MODULE',830,120-125*phase(t,1,3.5),130)
    im=Image.alpha_composite(im,overlay)
    # Only one motivated shallow push, directed at foreground prefab rooms.
    if shot['id']=='M01':
        z=1+.028*phase(t,.4,6.8);cx,cy=650,610
        left=cx*(1-1/z);top=cy*(1-1/z)
        im=im.transform((W,H),Image.Transform.AFFINE,(1/z,0,left,0,1/z,top),resample=Image.Resampling.BICUBIC)
    return im

def encode(shot,fps):
    target=ROOT/'preview'/f"{shot['id']}_MOTION_DEMO.mp4"
    cmd=['ffmpeg','-hide_banner','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for f in range(round(DURATION*fps)):
            p.stdin.write(compose(shot,f/fps).convert('RGB').tobytes())
        p.stdin.close();error=p.stderr.read().decode();rc=p.wait()
        if rc:raise RuntimeError(error)
    finally:
        if p.poll() is None:p.kill()
    print('RENDERED',shot['id'],flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stills',action='store_true');ap.add_argument('--fps',type=float,default=25);ap.add_argument('--only',default='');args=ap.parse_args()
    plan=json.loads((ROOT/'MOTION_PLAN.json').read_text(encoding='utf-8'))
    if args.only:plan=[s for s in plan if s['id'] in args.only.split(',')]
    load_assets(plan)
    for name in ['keyframes','overlays','preview']:(ROOT/name).mkdir(exist_ok=True)
    for shot in plan:
        for t in [0,2,4,6.8]:
            compose(shot,t).convert('RGB').save(ROOT/'keyframes'/f"{shot['id']}_{t:04.1f}s.jpg",quality=93)
        compose(shot,6.8,True).save(ROOT/'overlays'/f"{shot['id']}_ACCENTS_ENDSTATE.png")
        if not args.stills:encode(shot,args.fps)
    if not args.stills and not args.only:
        concat=ROOT/'preview/concat.txt'
        concat.write_text(''.join(f"file '{s['id']}_MOTION_DEMO.mp4'\n" for s in plan),encoding='utf-8')
        subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(ROOT/'preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4')],check=True)

if __name__=='__main__':main()
