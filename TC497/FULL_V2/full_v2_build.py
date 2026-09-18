import csv, json, os, re, subprocess, wave
from pathlib import Path
from collections import Counter
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

FPS=30
W,H=960,540
CUT=82.6
END=1236.506

PKG=Path(os.environ['PKG_ROOT'])
GEN=Path(os.environ['GEN_DIR'])
ARC=PKG/'04_DOWNLOADS'/'ARCHIVE_GREEN'
TR=Path(os.environ['TRANSCRIPT_DIR'])
EXTRA=Path(os.environ['V2_EXTRA'])
WORK=Path(os.environ['V2_WORK'])
PUB=Path(os.environ['V2_PUBLIC'])
IMG=WORK/'state_images'; SEG=WORK/'segments'; PDF=WORK/'pdf_pages'
for p in [WORK,PUB,IMG,SEG,PDF]: p.mkdir(parents=True,exist_ok=True)

C={'charcoal':(23,26,28),'paper':(230,221,200),'matte':(188,179,160)}

ARCHIVE_MAP={
 'AR-A01':'AR-A01__*','AR-A03':'AR-A03__*','AR-A04':'AR-A04__*',
 'AR-CH54-1':'AR-CH54-1__*','AR-CH54-2':'AR-CH54-2__*','AR-CH54-3':'AR-CH54-3__*',
 'AR-DEW-BARTER':'AR-DEW-BARTER__*','AR-DEW-MAP':'AR-DEW-MAP__*','AR-DEW-RADAR':'AR-DEW-RADAR__*',
 'AR-SNO':'AR-SNO__*','AR-OTTER1':'AR-OTTER1__*','AR-OTTER2':'AR-OTTER2__*','AR-PATENT':'AR-PATENT__*'
}
V2_NEW={
 'V2-PWR':'V2_POWERTRAIN.png','V2-DIST':'V2_DISTRIBUTION.png','V2-PRED1':'V2_PREDECESSOR_EARLY.png',
 'V2-PRED2':'V2_PREDECESSOR_MIL.png','V2-STEER':'V2_STEER_FOLLOW.png','V2-TRAC':'V2_TRACTION.png',
 'V2-YUMA':'V2_YUMA_OBSERVERS.png','V2-DUNE':'V2_DUNE.png','V2-CARGO':'V2_CARGO.png','V2-LEGACY':'V2_LEGACY.png',
 'V2-EHERO':'V2_ELECTRIC_HERO.png','V2-NUKE':'V2_NUCLEAR_CONCEPT.png'
}

def archive_path(code):
    xs=list(ARC.glob(ARCHIVE_MAP[code]))
    if not xs: raise FileNotFoundError(code)
    return xs[0]

def pdf_page(code,page=1):
    p=archive_path(code)
    out=PDF/f'{code}_p{page}.png'
    if not out.exists():
        stem=out.with_suffix('')
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-png','-r','150',str(p),str(stem)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return out

def src_path(code,page=1):
    if code in V2_NEW:
        p=EXTRA/V2_NEW[code]
        if not p.exists(): raise FileNotFoundError(p)
        return p,'generated'
    if code.startswith('AR-'):
        p=archive_path(code)
        if p.suffix.lower()=='.pdf': return pdf_page(code,page),'document'
        return p,'archive'
    p=GEN/f'{code}.png'
    if not p.exists(): raise FileNotFoundError(code)
    return p,'generated'

def fit_cover(im,size=(W,H),anchor=(.5,.5),zoom=1.0):
    im=im.convert('RGB')
    tw,th=size; iw,ih=im.size
    s=max(tw/iw,th/ih)*zoom
    nw,nh=max(tw,round(iw*s)),max(th,round(ih*s))
    im=im.resize((nw,nh),Image.Resampling.LANCZOS)
    x=max(0,min(nw-tw,round((nw-tw)*anchor[0])))
    y=max(0,min(nh-th,round((nh-th)*anchor[1])))
    return im.crop((x,y,x+tw,y+th))

def fit_inside(im,pad=22,bg=None):
    out=Image.new('RGB',(W,H),bg or C['matte'])
    im=im.convert('RGB'); im.thumbnail((W-2*pad,H-2*pad),Image.Resampling.LANCZOS)
    out.paste(im,((W-im.width)//2,(H-im.height)//2))
    return out

def grade(im,kind):
    if kind=='generated':
        im=ImageEnhance.Brightness(im).enhance(1.02)
        im=ImageEnhance.Contrast(im).enhance(1.025)
        im=ImageEnhance.Color(im).enhance(.90)
    elif kind=='archive':
        im=ImageEnhance.Contrast(im).enhance(1.02)
        im=ImageEnhance.Brightness(im).enhance(.98)
        im=ImageEnhance.Color(im).enhance(.52)
    elif kind=='document':
        im=ImageEnhance.Color(im).enhance(.68)
        im=ImageEnhance.Brightness(im).enhance(.91)
        im=ImageEnhance.Contrast(im).enhance(1.01)
    return im

def variant_image(code,variant='wide',page=1):
    p,kind=src_path(code,page)
    im=Image.open(p)
    if kind=='document' or variant=='inside':
        return grade(fit_inside(im,pad=24),kind)
    anchors={'left':(.30,.50),'right':(.70,.50),'top':(.50,.34),'bottom':(.50,.68),'wide':(.50,.50),'detail':(.50,.52),'detail_left':(.35,.52),'detail_right':(.65,.52)}
    zoom=1.16 if variant.startswith('detail') else 1.0
    return grade(fit_cover(im,anchor=anchors.get(variant,(.5,.5)),zoom=zoom),kind)

def ch54_composite():
    bg=variant_image('WC-D01','wide').convert('RGBA')
    heli=Image.open(archive_path('AR-CH54-1')).convert('RGB')
    crop=heli.crop((0,max(0,int(heli.height*.18)),heli.width,min(heli.height,int(heli.height*.82))))
    crop.thumbnail((460,250),Image.Resampling.LANCZOS)
    gray=ImageOps.grayscale(crop)
    mask=gray.point(lambda p: 255 if p<195 else max(0,min(255,int((232-p)*7.2)))).filter(ImageFilter.GaussianBlur(1.2))
    rgba=crop.convert('RGBA'); rgba.putalpha(mask)
    bg.alpha_composite(rgba,(455,64))
    return bg.convert('RGB')

CHAPTERS=[
('WHEN THE ROAD ENDS',82.600,200.699,[
 ('AR-DEW-MAP','inside',7,'chapter_road',1),('AR-DEW-BARTER','wide',7,'',1),('AR-DEW-RADAR','wide',7,'',1),
 ('WC-R01','wide',6,'road_end',1),('WC-R01','detail_right',4,'',1),('WC-R02','wide',8,'road_gap',1),
 ('WC-R02','detail_left',5,'',1),('V2-PRED1','wide',7,'recon',1),('WC-R03','wide',8,'solution',1),
 ('AR-DEW-MAP','detail',6,'map_isolation',1),('AR-DEW-BARTER','detail_left',5,'',1),('WC-R03','detail_right',5,'',1),
 ('AR-DEW-RADAR','detail',5,'',1),('WC-R01','left',5,'',1),('WC-R03','right',8,'',1),('AR-DEW-RADAR','wide',7,'',1)
]),
('THE ELECTRIC WHEEL',200.699,306.965,[
 ('AR-PATENT','inside',6,'chapter_electric',1),('WA-01','wide',6,'',1),('WA-07R','wide',5,'',1),('V2-PWR','wide',7,'electric_powertrain',1),
 ('WA-02','wide',6,'',1),('V2-EHERO','wide',8,'electric_distribution',1),('WA-08','wide',5,'',1),('V2-DIST','wide',7,'electric_distribution',1),
 ('WA-09','wide',6,'wheel_motor',1),('V2-TRAC','wide',5,'',1),('AR-PATENT','inside',4,'patent_detail',1),('WA-10','wide',8,'',1),
 ('V2-EHERO','detail_left',5,'',1),('WA-09','detail',4,'wheel_motor',1),('V2-PWR','detail_right',5,'electric_powertrain',1)
]),
('BIGGER AND BIGGER',306.965,399.491,[
 ('WC-B01','wide',7,'chapter_bigger',1),('V2-PRED1','wide',7,'recon',1),('WC-B02','wide',6,'',1),('AR-SNO','wide',7,'sno_once',1),
 ('V2-PRED2','wide',7,'recon',1),('WC-B03','wide',6,'',1),('WC-B04','wide',8,'',1),('V2-PRED1','detail_left',5,'',1),
 ('V2-PRED2','detail_right',5,'',1),('WC-B04','detail',8,'',1),('WB-L02','wide',7,'tc497_arrives',1)
]),
('THE 572-FOOT MACHINE',399.491,525.453,[
 ('AR-A01','wide',7,'chapter_572',1),('WB-L02','wide',8,'',1),('ST-572','wide',10,'scale_572',1),('WA-06','wide',7,'',1),
 ('WB-L03','wide',7,'units_13',1),('WB-L04','wide',5,'',1),('WB-L05','wide',5,'wheels_54',1),('WB-L06','wide',7,'',1),
 ('V2-CARGO','wide',7,'cargo',1),('ST-572','detail_left',5,'scale_572',1),('WB-L02','right',7,'',1),('WB-L03','detail',5,'',1),
 ('WB-L05','detail',4,'wheels_54',1),('WB-L06','detail_right',6,'',1),('V2-CARGO','detail_left',6,'cargo',1),('WB-L04','detail',5,'',1)
]),
('HOW DO YOU DRIVE 572 FEET?',525.453,663.014,[
 ('ST-STEER','wide',7,'chapter_steer',1),('WA-03','wide',6,'',1),('AR-OTTER1','inside',5,'otter',1),('WA-11R','wide',6,'offtrack',1),
 ('V2-STEER','wide',8,'closer_follow',1),('WA-04R','wide',6,'',1),('WA-12','wide',5,'',1),('V2-TRAC','wide',6,'distributed_traction',1),
 ('WA-05','wide',6,'',1),('WA-13R','wide',6,'distributed_traction',1),('WA-14','wide',7,'',1),('AR-OTTER2','inside',5,'otter',1),
 ('V2-STEER','detail_right',5,'closer_follow',1),('WA-04R','detail',5,'',1),('WA-13R','detail_left',5,'',1),('AR-OTTER2','inside',6,'otter',8),('ST-STEER','detail_left',6,'',1)
]),
('NUCLEAR — RETENTION BEAT',663.014,750.184,[
 ('V2-PWR','wide',6,'chapter_nuclear_actual',1),('WB-N01','wide',7,'nuclear_concept',1),('V2-NUKE','wide',8,'nuclear_concept',1),('WB-N03','wide',7,'nuclear_distribution',1),
 ('WB-N04','wide',8,'nuclear_unbuilt',1),('WB-N01','detail_left',5,'',1),('V2-NUKE','detail_right',6,'nuclear_concept',1),('WB-N03','detail',5,'nuclear_distribution',1),
 ('V2-PWR','detail_left',6,'actual_gas_turbines',1),('WB-N04','detail_right',7,'nuclear_unbuilt',1)
]),
('YUMA',750.184,822.857,[
 ('AR-OTTER1','inside',6,'chapter_yuma',1),('V2-YUMA','wide',8,'yuma_test',1),('WC-Y01','wide',7,'',1),('AR-OTTER2','inside',5,'otter',1),
 ('WC-Y01','detail_right',5,'',1),('V2-YUMA','detail_left',6,'yuma_test',1),('V2-DUNE','wide',7,'dune_setup',1),('WC-Y02','wide',7,'',1),
 ('AR-OTTER2','inside',4,'otter',8),('V2-DUNE','detail_right',6,'dune_setup',1)
]),
('TEST RESULTS',822.857,915.853,[
 ('AR-OTTER2','inside',5,'chapter_tests',26),('WD-T01','wide',7,'test_success',1),('V2-YUMA','wide',6,'yuma_test',1),('WD-T02','wide',6,'',1),
 ('AR-OTTER2','inside',5,'otter_limit',47),('V2-DUNE','wide',7,'dune_limit',1),('WD-T03','wide',6,'',1),('WC-Y02','wide',7,'',1),
 ('WD-T01','detail_left',5,'test_success',1),('V2-DUNE','detail_right',5,'dune_limit',1),('WD-T02','detail',5,'',1),('WC-Y02','detail_left',6,'',1),
 ('AR-OTTER2','inside',5,'otter',26)
]),
('IT WORKED',915.853,1002.057,[
 ('AR-A01','wide',6,'chapter_worked',1),('WD-W01','wide',8,'metric_speed',1),('V2-CARGO','wide',8,'metric_range',1),('WD-W02','wide',7,'metric_cargo',1),
 ('WD-W03','wide',7,'metric_crew',1),('AR-OTTER2','inside',5,'otter',26),('WD-W01','detail_left',5,'',1),('V2-CARGO','detail_right',7,'cargo',1),
 ('WD-W02','right',7,'',1),('WD-W03','detail_left',6,'',1)
]),
('DEFEATED BY THE SKY',1002.057,1115.376,[
 ('AR-CH54-1','wide',7,'chapter_sky',1),('AR-CH54-2','wide',7,'',1),('WC-D02','wide',6,'',1),('ST-SKY','wide',8,'sky_shift',1),
 ('WC-D03','wide',6,'',1),('AR-CH54-3','wide',7,'',1),('WC-D04','wide',7,'',1),('WC-D05','detail_left',7,'',1),
 ('WC-D05','wide',6,'',1),('WC-D01','wide',7,'',1),('AR-CH54-2','detail',5,'',1),('ST-SKY','detail_left',5,'',1),
 ('WC-D04','detail_right',6,'',1),('AR-CH54-3','detail',6,'',1),('WC-D01','right',7,'sky_payoff',1)
]),
('EPILOGUE — THE LAST CAR',1115.376,1173.420,[
 ('AR-A03','wide',7,'chapter_lastcar',1),('ST-LAST','wide',8,'',1),('WD-LC01','wide',7,'',1),('AR-A04','wide',6,'',1),
 ('WD-LC02','wide',7,'',1),('V2-LEGACY','wide',8,'legacy',1),('WD-LC03','wide',8,'',1)
]),
('ENDING / CTA',1173.420,1236.506,[
 ('WD-E01','wide',7,'chapter_end',1),('WD-E02','wide',8,'',1),('WD-E03','wide',8,'',1),('WD-E04','wide',8,'',1),
 ('AR-A03','detail',6,'legacy',1),('V2-LEGACY','detail_right',6,'legacy',1),('WD-E05','wide',14,'final_plate',1)
])]

def make_state_image(code,variant,page,out):
    im=variant_image(code,variant,page)
    im.save(out,quality=94,subsampling=0)

def render_segment(img,dur,out):
    frames=max(2,round(dur*FPS))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(img),'-vf','scale=960:540,format=yuv420p','-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(out)],check=True)

def build_rest():
    shots=[]; seq=[]; idx=0
    for cname,cs,ce,specs in CHAPTERS:
        total=sum(x[2] for x in specs); cursor=cs
        for j,(code,variant,weight,tag,page) in enumerate(specs):
            idx+=1
            dur=(ce-cs)*weight/total
            end=ce if j==len(specs)-1 else cursor+dur
            img=IMG/f'{idx:03d}_{code}_{variant}.jpg'
            if not img.exists(): make_state_image(code,variant,page,img)
            seg=SEG/f'{idx:03d}.mp4'
            render_segment(img,end-cursor,seg)
            seq.append(seg)
            shots.append({'idx':idx,'s':round(cursor,3),'e':round(end,3),'chapter':cname,'code':code,'variant':variant,'tag':tag,'page':page,'chapter_start':j==0})
            cursor=end
    concat=WORK/'rest_concat.txt'
    concat.write_text(''.join(f"file '{p.resolve()}'\n" for p in seq))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(PUB/'rest_base.mp4')],check=True)
    (PUB/'shots.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
    return shots

def build_captions():
    path=next(TR.glob('TC497_VO_WORD_LEVEL.csv'))
    words=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            s=float(r['start_sec']); e=float(r['end_sec'])
            if s>=END: break
            words.append({'s':s,'e':min(e,END),'w':r['word']})
    phrases=[]; buf=[]
    for w in words:
        buf.append(w)
        span=buf[-1]['e']-buf[0]['s']; chars=sum(len(x['w'])+1 for x in buf)
        punct=bool(re.search(r'[.!?;:]$',w['w'])); comma=bool(re.search(r',$',w['w']))
        if len(buf)>=7 or chars>=48 or span>=2.45 or (punct and len(buf)>=3) or (comma and len(buf)>=5):
            phrases.append({'s':buf[0]['s'],'e':buf[-1]['e']+.08,'words':buf}); buf=[]
    if buf: phrases.append({'s':buf[0]['s'],'e':buf[-1]['e']+.08,'words':buf})
    (PUB/'captions.json').write_text(json.dumps(phrases,ensure_ascii=False),encoding='utf-8')

def build_score():
    sr=48000; dur=END-CUT; n=int(dur*sr); t=np.arange(n,dtype=np.float32)/sr; a=np.zeros(n,dtype=np.float32)
    for ci,(name,cs,ce,_) in enumerate(CHAPTERS):
        s=max(0,cs-CUT); e=ce-CUT; m=(t>=s)&(t<e); tt=t[m]-s
        f=[42,47,44,39,45,38,46,43,50,41,37,40][ci%12]
        env=np.ones_like(tt); fadeN=min(len(tt),int(sr*.9))
        if fadeN>4:
            env[:fadeN]*=np.linspace(0,1,fadeN,dtype=np.float32)
            env[-fadeN:]*=np.linspace(1,0,fadeN,dtype=np.float32)
        sig=.78*np.sin(2*np.pi*f*tt)+.16*np.sin(2*np.pi*f*1.5*tt+.7)+.06*np.sin(2*np.pi*f*2*tt+1.3)
        a[m]+=.0105*env*sig
        if ci>0:
            ii=int(s*sr); L=min(int(.35*sr),n-ii); xt=np.arange(L,dtype=np.float32)/sr
            a[ii:ii+L]+=.018*np.sin(2*np.pi*f*.7*xt)*np.exp(-xt*10)
    pcm=(np.clip(a,-.6,.6)*32767).astype(np.int16)
    with wave.open(str(PUB/'rest_score.wav'),'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

def audit(shots):
    counts=Counter(x['code'] for x in shots)
    ds=[x['e']-x['s'] for x in shots]
    report={'shot_count_after_cold_open':len(shots),'min_shot_sec':min(ds),'max_shot_sec':max(ds),'median_shot_sec':float(np.median(ds)),
      'AR-SNO':counts['AR-SNO'],'AR-A01_after_cold_open':counts['AR-A01'],'standalone_graphics':0,'generic_split_screens':0,
      'new_v2_shot_uses':sum(1 for x in shots if x['code'] in V2_NEW)}
    (WORK/'V2_QA.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    if counts['AR-SNO']>1: raise RuntimeError('AR-SNO reuse exceeds V2 rule')
    if counts['AR-A01']>2: raise RuntimeError('AR-A01 reuse exceeds V2 post-cold-open rule')
    return report

if __name__=='__main__':
    shots=build_rest(); build_captions(); build_score(); qa=audit(shots)
    print('FULL_V2_PREP_DONE',qa)
