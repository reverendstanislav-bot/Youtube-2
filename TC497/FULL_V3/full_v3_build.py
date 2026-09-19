import csv, json, os, re, subprocess, wave
from pathlib import Path
from collections import Counter
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import cv2

FPS=30
W,H=960,540
CUT=82.6
END=1236.506

PKG=Path(os.environ['PKG_ROOT'])
GEN=Path(os.environ['GEN_DIR'])
ARC=PKG/'04_DOWNLOADS'/'ARCHIVE_GREEN'
TR=Path(os.environ['TRANSCRIPT_DIR'])
EXTRA=Path(os.environ['V3_EXTRA'])
WORK=Path(os.environ['V3_WORK'])
PUB=Path(os.environ['V3_PUBLIC'])
IMG=WORK/'state_images'; SEG=WORK/'segments'; PDF=WORK/'pdf_pages'
for p in [WORK,PUB,IMG,SEG,PDF]: p.mkdir(parents=True,exist_ok=True)

C={'charcoal':(23,26,28),'paper':(230,221,200),'matte':(188,179,160)}

ARCHIVE_MAP={
 'AR-A01':'AR-A01__*','AR-A03':'AR-A03__*','AR-A04':'AR-A04__*',
 'AR-CH54-1':'AR-CH54-1__*','AR-CH54-2':'AR-CH54-2__*','AR-CH54-3':'AR-CH54-3__*',
 'AR-DEW-BARTER':'AR-DEW-BARTER__*','AR-DEW-MAP':'AR-DEW-MAP__*','AR-DEW-RADAR':'AR-DEW-RADAR__*',
 'AR-SNO':'AR-SNO__*','AR-OTTER1':'AR-OTTER1__*','AR-OTTER2':'AR-OTTER2__*','AR-PATENT':'AR-PATENT__*'
}
NEW_ASSETS={
 'V2-PWR':'V2_POWERTRAIN.png','V2-DIST':'V2_DISTRIBUTION.png','V2-PRED1':'V2_PREDECESSOR_EARLY.png',
 'V2-PRED2':'V2_PREDECESSOR_MIL.png','V2-STEER':'V2_STEER_FOLLOW.png','V2-TRAC':'V2_TRACTION.png',
 'V2-YUMA':'V2_YUMA_OBSERVERS.png','V2-DUNE':'V2_DUNE.png','V2-CARGO':'V2_CARGO.png','V2-LEGACY':'V2_LEGACY.png',
 'V2-EHERO':'V2_ELECTRIC_HERO.png','V2-NUKE':'V2_NUCLEAR_CONCEPT.png','V2-INTERIOR':'V2_CONTROL_INTERIOR.png',
 'V3-PRED':'V3_PREDECESSOR.png','V3-YUMA':'V3_YUMA_TEST.png','V3-DUNE':'V3_DUNE_LIMIT.png','V3-LEGACY':'V3_LEGACY.png',
 'V3-ASSEMBLY':'V3_ASSEMBLY.png','V3-COUPLING':'V3_COUPLING.png','V3-TOPDOWN':'V3_TOPDOWN.png','V3-CARGOLOAD':'V3_CARGOLOAD.png',
 'V3-CREW':'V3_CREW.png','V3-WHEEL':'V3_WHEEL_MOTION.png','V3-RANGE':'V3_RANGE.png','V3-LEGACYDETAIL':'V3_LEGACY_DETAIL.png',
 'V3-EMPTY':'V3_EMPTY_YUMA.png','V3-HELILOAD':'V3_HELI_LOAD.png'
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
    if code in NEW_ASSETS:
        p=EXTRA/NEW_ASSETS[code]
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


def _rust_rect_mask(im):
    arr=np.asarray(im.convert('RGB'))
    hsv=cv2.cvtColor(arr,cv2.COLOR_RGB2HSV)
    raw=cv2.inRange(hsv,np.array([0,75,45],dtype=np.uint8),np.array([23,255,235],dtype=np.uint8))
    n,labels,stats,_=cv2.connectedComponentsWithStats(raw,8)
    out=np.zeros(raw.shape,dtype=np.uint8)
    hh,ww=raw.shape
    for i in range(1,n):
        x,y,w,h,area=[int(v) for v in stats[i]]
        if area<650 or w<22 or h<18: continue
        fill=area/max(1,w*h)
        near_edge=(x<ww*.18 or y<hh*.18 or x+w>ww*.82 or y+h>hh*.82)
        not_huge=(w<ww*.42 and h<hh*.48)
        if fill<.76 or not near_edge or not not_huge: continue
        pix=arr[labels==i]
        if len(pix)==0 or float(np.std(pix))>36: continue
        comp=np.uint8(labels==i)*255
        contours,_=cv2.findContours(comp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if not contours: continue
        cnt=max(contours,key=cv2.contourArea)
        peri=cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,.035*peri,True)
        if len(approx)!=4: continue
        out[labels==i]=255
    if out.max():
        out=cv2.dilate(out,np.ones((9,9),np.uint8),iterations=1)
    return out

def clean_baked_rust_blocks(im):
    arr=np.asarray(im.convert('RGB')).copy()
    mask=_rust_rect_mask(im)
    if mask.max():
        arr=cv2.inpaint(arr,mask,7,cv2.INPAINT_TELEA)
    return Image.fromarray(arr)

def doc_evidence(im,variant):
    im=im.convert('RGB')
    w,h=im.size
    bands={
      'doc_upper':(.07,.08,.93,.42),
      'doc_mid':(.07,.27,.93,.63),
      'doc_lower':(.07,.50,.93,.88),
      'doc_center':(.10,.18,.90,.78)
    }
    a,b,c,d=bands.get(variant,bands['doc_center'])
    crop=im.crop((int(w*a),int(h*b),int(w*c),int(h*d)))
    crop=fit_cover(crop,(W,H),(.5,.5),1.0)
    return grade(crop,'document')

def variant_image(code,variant='wide',page=1):
    p,kind=src_path(code,page)
    im=Image.open(p)
    if kind=='document':
        if str(variant).startswith('doc_'):
            return doc_evidence(im,variant)
        return grade(fit_inside(im,pad=24),kind)
    if variant=='inside':
        return grade(fit_inside(im,pad=24),kind)
    anchors={'left':(.30,.50),'right':(.70,.50),'top':(.50,.34),'bottom':(.50,.68),'wide':(.50,.50),
             'detail':(.50,.52),'detail_left':(.35,.52),'detail_right':(.65,.52)}
    if variant.startswith('detail'):
        zoom=1.16
    elif kind=='generated':
        zoom=1.035 if code in NEW_ASSETS else 1.105
    else:
        zoom=1.0
    out=fit_cover(im,anchor=anchors.get(variant,(.5,.5)),zoom=zoom)
    # Legacy reconstructions are the source of baked orange collage blocks.
    # Clean every used legacy generated frame, then crop/grade.
    if kind=='generated':
        out=clean_baked_rust_blocks(out)
    return grade(out,kind)

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
 ('V3-PRED','wide',5,'chapter_bigger',1),('AR-SNO','wide',5,'sno_once',1),('V3-ASSEMBLY','wide',5,'human_scale',1),
 ('V3-COUPLING','detail',4,'mechanical_detail',1),('V2-PRED2','wide',5,'recon',1),('V3-WHEEL','detail',4,'mechanical_detail',1),
 ('V3-PRED','detail_left',4,'recon',1),('V3-ASSEMBLY','detail_right',4,'human_scale',1),('V2-PRED1','wide',5,'recon',1),
 ('V3-COUPLING','detail_right',4,'mechanical_detail',1),('V3-CARGOLOAD','wide',5,'operation',1),('V3-WHEEL','detail_left',4,'mechanical_detail',1),
 ('WB-L02','wide',5,'tc497_arrives',1),('V3-ASSEMBLY','wide',4,'human_scale',1),('V3-TOPDOWN','wide',5,'scale_geometry',1)
]),
('THE 572-FOOT MACHINE',399.491,525.453,[
 ('AR-A01','wide',5,'chapter_572',1),('V3-TOPDOWN','wide',6,'scale_572',1),('V3-ASSEMBLY','wide',5,'human_scale',1),
 ('V3-WHEEL','detail',4,'wheels_54',1),('V3-COUPLING','detail',4,'mechanical_detail',1),('V3-CARGOLOAD','wide',5,'cargo',1),
 ('ST-572','wide',5,'scale_572',1),('V3-CREW','wide',4,'crew_scale',1),('V3-WHEEL','detail_right',4,'mechanical_detail',1),
 ('V3-RANGE','wide',5,'range_context',1),('V3-ASSEMBLY','detail_left',4,'human_scale',1),('V3-TOPDOWN','detail',5,'scale_geometry',1),
 ('V3-CARGOLOAD','detail_right',4,'cargo',1),('V3-COUPLING','detail_left',4,'mechanical_detail',1),('V3-CREW','detail_left',4,'crew_scale',1),
 ('WB-L05','detail',4,'wheels_54',1),('WB-L02','wide',5,'full_machine',1),('V3-TOPDOWN','wide',5,'scale_geometry',1),
 ('V3-ASSEMBLY','wide',4,'human_scale',1),('V3-RANGE','wide',5,'range_context',1),('V3-CARGOLOAD','wide',5,'cargo',1),
 ('V3-WHEEL','detail',4,'mechanical_detail',1)
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
 ('AR-OTTER2','doc_upper',4,'chapter_tests',26),('AR-OTTER2','doc_mid',4,'evidence_crop',26),('V3-YUMA','wide',5,'yuma_test',1),
 ('V3-WHEEL','detail',4,'test_mechanics',1),('AR-OTTER2','doc_mid',4,'otter_limit',47),('V3-DUNE','wide',5,'dune_limit',1),
 ('V2-DUNE','detail_right',4,'dune_limit',1),('V3-YUMA','detail_left',4,'yuma_test',1),('AR-OTTER2','doc_lower',4,'evidence_crop',26),
 ('V3-WHEEL','detail_right',4,'test_mechanics',1),('V3-DUNE','detail_left',4,'dune_limit',1),('V2-YUMA','wide',5,'yuma_test',1),
 ('AR-OTTER2','doc_upper',4,'evidence_crop',47),('V3-COUPLING','detail',4,'mechanical_detail',1),('V3-DUNE','wide',5,'dune_limit',1),
 ('V3-YUMA','detail_right',4,'yuma_test',1)
]),
('IT WORKED',915.853,1002.057,[
 ('V3-WHEEL','wide',5,'metric_speed',1),('V3-RANGE','wide',5,'metric_range',1),('V3-CARGOLOAD','wide',5,'metric_cargo',1),
 ('V3-CREW','wide',5,'metric_crew',1),('AR-OTTER2','doc_mid',4,'evidence_crop',26),('V3-WHEEL','detail',4,'operational_motion',1),
 ('V3-CARGOLOAD','detail_right',5,'cargo',1),('V3-RANGE','detail_left',5,'range_context',1),('V3-CREW','detail_left',4,'crew_scale',1),
 ('V3-TOPDOWN','wide',5,'scale_geometry',1),('V3-ASSEMBLY','wide',4,'human_scale',1),('V3-COUPLING','detail',4,'mechanical_detail',1),
 ('V3-WHEEL','detail_right',4,'operational_motion',1),('V3-CARGOLOAD','wide',5,'cargo',1)
]),
('DEFEATED BY THE SKY',1002.057,1115.376,[
 ('AR-CH54-1','wide',5,'chapter_sky',1),('V3-HELILOAD','wide',6,'heli_operation',1),('WC-D02','wide',5,'',1),
 ('ST-SKY','wide',6,'sky_shift',1),('AR-CH54-2','wide',5,'archive_heli',1),('V3-HELILOAD','detail_left',5,'heli_operation',1),
 ('WC-D04','wide',5,'',1),('AR-CH54-3','wide',5,'archive_heli',1),('V3-RANGE','wide',5,'ground_context',1),
 ('WC-D01','wide',5,'',1),('AR-CH54-2','detail',4,'archive_heli',1),('V3-HELILOAD','detail_right',5,'heli_operation',1),
 ('WC-D04','detail_right',4,'',1),('AR-CH54-3','detail',4,'archive_heli',1),('WC-D01','right',5,'sky_payoff',1)
]),
('EPILOGUE — THE LAST CAR',1115.376,1173.420,[
 ('AR-A03','wide',5,'chapter_lastcar',1),('V3-LEGACY','wide',5,'legacy',1),('V3-LEGACYDETAIL','wide',4,'legacy_detail',1),
 ('V2-INTERIOR','wide',5,'legacy_interior',1),('AR-A04','wide',4,'archive_interior',1),('V3-LEGACYDETAIL','detail_right',4,'legacy_detail',1),
 ('V3-EMPTY','wide',5,'aftermath',1),('V3-LEGACY','detail_left',4,'legacy',1),('V2-INTERIOR','detail_left',4,'legacy_interior',1),
 ('V3-EMPTY','detail',5,'aftermath',1)
]),
('ENDING / CTA',1173.420,1236.506,[
 ('V3-EMPTY','wide',5,'chapter_end',1),('V3-LEGACYDETAIL','wide',4,'legacy_detail',1),('AR-A03','detail',4,'archive_survivor',1),
 ('V2-INTERIOR','detail',4,'legacy_interior',1),('V3-EMPTY','wide',5,'aftermath',1),('V3-LEGACY','wide',5,'legacy',1),
 ('V3-LEGACYDETAIL','detail_left',4,'legacy_detail',1),('V3-EMPTY','detail_right',5,'aftermath',1),('AR-A04','detail',4,'archive_interior',1),
 ('V3-EMPTY','wide',8,'final_plate',1)
])]

def make_state_image(code,variant,page,out):
    im=variant_image(code,variant,page)
    im.save(out,quality=94,subsampling=0)

def render_segment(img,dur,out):
    frames=max(2,round(dur*FPS))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(img),'-vf','scale=960:540,format=yuv420p','-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(out)],check=True)


FULL_TC497={'AR-A01','ST-572','WB-L02','WB-L03','WB-L06','ST-STEER','WC-Y01','WD-T01','WD-T02','WD-T03','WD-W01','WD-W02','WD-W03','WC-D01','ST-LAST','WD-LC01','WD-LC02','WD-LC03'}
def visual_category(code,variant,tag):
    if code.startswith('AR-OTTER') or code=='AR-PATENT': return 'document'
    if code.startswith('AR-'): return 'archive'
    if code in {'V3-ASSEMBLY','V3-CREW'}: return 'human'
    if code in {'V3-COUPLING','V3-WHEEL','WB-L05','WA-09','V2-TRAC'} or str(variant).startswith('detail'): return 'mechanical_detail'
    if code in {'V3-RANGE','V3-EMPTY','V3-DUNE','V2-DUNE'}: return 'environment'
    if code in {'V3-CARGOLOAD','V2-CARGO','V3-HELILOAD'}: return 'operation'
    if code in FULL_TC497 and not str(variant).startswith('detail'): return 'full_tc497'
    if code=='V3-TOPDOWN' and variant=='wide': return 'full_tc497'
    return 'reconstruction'

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
            shots.append({'idx':idx,'s':round(cursor,3),'e':round(end,3),'chapter':cname,'code':code,'variant':variant,'tag':tag,'page':page,'chapter_start':j==0,'category':visual_category(code,variant,tag)})
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


def _slow_noise(rng,n,rate=32):
    if n<=1: return np.zeros(n,dtype=np.float32)
    points=max(3,int(n/48000*rate)+2)
    anchors=rng.normal(0,1,points).astype(np.float32)
    xi=np.linspace(0,points-1,n,dtype=np.float32)
    return np.interp(xi,np.arange(points,dtype=np.float32),anchors).astype(np.float32)

def build_score(shots):
    sr=48000
    rng=np.random.default_rng(497)
    out=PUB/'rest_score.wav'
    with wave.open(str(out),'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        for ci,(name,cs,ce,_) in enumerate(CHAPTERS):
            dur=ce-cs; n=max(1,int(round(dur*sr))); tt=np.arange(n,dtype=np.float32)/sr
            a=np.zeros(n,dtype=np.float32)
            # Environment, not music.
            wind=_slow_noise(rng,n,28)
            micro=_slow_noise(rng,n,120)
            if name in {'WHEN THE ROAD ENDS','YUMA','TEST RESULTS'}:
                a += .0065*wind + .0022*micro
            elif name in {'THE ELECTRIC WHEEL','THE 572-FOOT MACHINE','HOW DO YOU DRIVE 572 FEET?','IT WORKED'}:
                f={'THE ELECTRIC WHEEL':58,'THE 572-FOOT MACHINE':44,'HOW DO YOU DRIVE 572 FEET?':40,'IT WORKED':48}[name]
                rum=.72*np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*f*2.03*tt+.4)
                pulse=(.55+.45*np.sin(2*np.pi*.72*tt))
                a += .0075*rum*pulse + .0028*wind
            elif name=='BIGGER AND BIGGER':
                a += .0048*np.sin(2*np.pi*42*tt)+.0040*wind
            elif name=='NUCLEAR — RETENTION BEAT':
                a += .0030*np.sin(2*np.pi*52*tt)+.0018*wind
            elif name=='DEFEATED BY THE SKY':
                # Heavy-lift rotor thump + air wash.
                rotor_env=(np.maximum(0,np.sin(2*np.pi*6.2*tt))**5)
                a += .0100*rotor_env*np.sin(2*np.pi*46*tt)+.0055*wind+.0020*micro
            elif name=='EPILOGUE — THE LAST CAR':
                a += .0018*wind
            elif name=='ENDING / CTA':
                # Intentional near-silence.
                a += .0008*wind

            # Short chapter-entry low impact, no musical sting.
            L=min(n,int(.34*sr))
            if ci>0 and L>0:
                xt=np.arange(L,dtype=np.float32)/sr
                a[:L]+=.014*np.sin(2*np.pi*38*xt)*np.exp(-xt*11)

            # Paper/document rustles and mechanical ticks tied to actual shot starts.
            local=[x for x in shots if x['chapter']==name]
            for sh in local:
                pos=int(max(0,(sh['s']-cs))*sr)
                if sh['category']=='document':
                    L=min(int(.18*sr),n-pos)
                    if L>0:
                        noise=rng.normal(0,1,L).astype(np.float32)
                        env=np.linspace(1,0,L,dtype=np.float32)**2
                        a[pos:pos+L]+=.0045*noise*env
                elif sh['category']=='mechanical_detail':
                    L=min(int(.10*sr),n-pos)
                    if L>0:
                        xt=np.arange(L,dtype=np.float32)/sr
                        a[pos:pos+L]+=.0040*np.sin(2*np.pi*92*xt)*np.exp(-xt*35)

            # soft chapter edges
            F=min(n,int(.75*sr))
            if F>2:
                a[:F]*=np.linspace(0,1,F,dtype=np.float32)
                a[-F:]*=np.linspace(1,0,F,dtype=np.float32)
            pcm=(np.clip(a,-.35,.35)*32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())


def audit(shots):
    counts=Counter(x['code'] for x in shots)
    ds=[x['e']-x['s'] for x in shots]
    streak=0; max_streak=0
    for x in shots:
        if x['category']=='full_tc497': streak+=1
        else: streak=0
        max_streak=max(max_streak,streak)

    # Re-scan all rendered state images for flat rust/orange rectangles near frame edges.
    orange_left=0
    for p in IMG.glob('*.jpg'):
        if _rust_rect_mask(Image.open(p)).max(): orange_left+=1

    report={
      'shot_count_after_cold_open':len(shots),
      'min_shot_sec':min(ds),'max_shot_sec':max(ds),'median_shot_sec':float(np.median(ds)),
      'AR-SNO':counts['AR-SNO'],'AR-A01_after_cold_open':counts['AR-A01'],
      'max_consecutive_full_tc497':max_streak,
      'orange_edge_blocks_after_cleanup':orange_left,
      'standalone_graphics':0,'generic_split_screens':0,
      'new_clean_asset_uses':sum(1 for x in shots if x['code'] in NEW_ASSETS)
    }
    (WORK/'V3_QA.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    if counts['AR-SNO']>1: raise RuntimeError('AR-SNO reuse exceeds V3 rule')
    if counts['AR-A01']>2: raise RuntimeError('AR-A01 reuse exceeds V3 rule')
    if max_streak>2: raise RuntimeError(f'full TC497 streak exceeds V3 rule: {max_streak}')
    if orange_left>0: raise RuntimeError(f'baked orange/rust edge blocks remain: {orange_left}')
    return report

if __name__=='__main__':
    shots=build_rest(); build_captions(); build_score(shots); qa=audit(shots)
    print('FULL_V3_PREP_DONE',qa)
