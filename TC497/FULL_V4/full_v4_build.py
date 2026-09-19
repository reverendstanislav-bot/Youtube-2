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
EXTRA=Path(os.environ['V4_EXTRA'])
WORK=Path(os.environ['V4_WORK'])
PUB=Path(os.environ['V4_PUBLIC'])
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
 'V3-EMPTY':'V3_EMPTY_YUMA.png','V3-HELILOAD':'V3_HELI_LOAD.png',
 'V4-STEER-TRACKS':'V4_STEER_TRACKS.png','V4-STEER-JOINT':'V4_STEER_JOINT.png','V4-DRIVER':'V4_DRIVER.png',
 'V4-WHEEL':'V4_WHEEL_ALT.png','V4-ASSEMBLY':'V4_ASSEMBLY_ALT.png','V4-CARGO':'V4_CARGO_ALT.png',
 'V4-RANGE':'V4_RANGE_ALT.png','V4-NUKE':'V4_NUKE_TECH.png','V4-HELI':'V4_HELI_CARGO.png',
 'V4-SURVIVOR-INTERIOR':'V4_SURVIVOR_INTERIOR.png','V4-SURVIVOR-DETAIL':'V4_SURVIVOR_DETAIL.png',
 'V4-EMPTY-END':'V4_EMPTY_END.png'
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
    for _ in range(3):
        cur=Image.fromarray(arr)
        mask=_rust_rect_mask(cur)
        if not mask.max(): break
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
 ('WA-09','wide',6,'wheel_motor',1),('V2-TRAC','wide',5,'',1),('AR-PATENT','doc_mid',4,'patent_detail',1),('WA-10','wide',8,'',1),
 ('V2-EHERO','detail_left',5,'',1),('WA-09','detail',4,'wheel_motor',1),('V2-PWR','detail_right',5,'electric_powertrain',1)
]),
('BIGGER AND BIGGER',306.965,399.491,[
 ('V3-PRED','wide',6,'chapter_bigger',1),('AR-SNO','wide',5,'sno_once',1),('V4-ASSEMBLY','wide',6,'human_scale',1),
 ('V3-COUPLING','detail',5,'mechanical_detail',1),('V2-PRED2','wide',6,'recon',1),('V4-WHEEL','detail',5,'mechanical_detail',1),
 ('V2-PRED1','wide',6,'recon',1),('V4-CARGO','wide',6,'operation',1),('V3-CREW','wide',5,'crew_scale',1),
 ('V3-EMPTY','wide',5,'range_context',1),('V3-TOPDOWN','wide',6,'scale_geometry',1),('WB-L02','wide',6,'tc497_arrives',1),
 ('V4-ASSEMBLY','detail_left',5,'human_scale',1),('V4-CARGO','detail_right',5,'operation',1),('V4-WHEEL','detail_right',5,'mechanical_detail',1),
 ('V3-PRED','detail_left',5,'recon',1)
]),
('THE 572-FOOT MACHINE',399.491,525.453,[
 ('AR-A01','wide',5,'chapter_572',1),('ST-572','wide',6,'scale_572',1),('V3-TOPDOWN','detail',5,'scale_geometry',1),
 ('WB-L05','detail',5,'wheels_54',1),('V3-CREW','detail',4,'crew_scale',1),('V3-CARGOLOAD','wide',5,'cargo',1),
 ('V3-RANGE','wide',5,'range_context',1),('V3-ASSEMBLY','wide',5,'human_scale',1),('V3-WHEEL','detail',4,'mechanical_detail',1),
 ('V4-STEER-JOINT','detail_left',4,'mechanical_detail',1),('V2-CARGO','wide',5,'cargo',1),('WA-09','detail',4,'wheel_motor',1),
 ('V2-TRAC','wide',5,'distributed_traction',1),('WB-L02','detail_left',5,'full_machine',1),('V2-DIST','detail_right',5,'electric_distribution',1),
 ('V4-ASSEMBLY','detail_right',4,'human_scale',1),('V4-DRIVER','detail_left',4,'crew_scale',1),
 ('V3-CARGOLOAD','detail',4,'cargo',1),('V3-RANGE','detail',5,'range_context',1)
]),
('HOW DO YOU DRIVE 572 FEET?',525.453,663.014,[
 ('V4-STEER-TRACKS','wide',6,'chapter_steer',1),('AR-OTTER1','doc_mid',5,'otter',1),('V4-STEER-JOINT','detail',5,'mechanical_detail',1),
 ('V2-STEER','wide',6,'closer_follow',1),('V2-TRAC','detail_left',5,'distributed_traction',1),('V3-TOPDOWN','detail_right',5,'scale_geometry',1),
 ('V4-STEER-TRACKS','detail',5,'closer_follow',1),('AR-OTTER2','doc_upper',5,'otter',8),('V4-DRIVER','wide',5,'crew_scale',1),
 ('V2-STEER','detail_left',5,'closer_follow',1),('V3-YUMA','wide',6,'yuma_test',1),('V3-WHEEL','detail_left',4,'test_mechanics',1),
 ('V3-CREW','detail_right',4,'crew_scale',1),('V3-ASSEMBLY','detail_right',4,'human_scale',1),('AR-OTTER1','doc_lower',5,'otter',1),
 ('AR-OTTER2','doc_mid',5,'evidence_crop',8),('V3-COUPLING','detail_left',4,'mechanical_detail',1),('AR-OTTER1','doc_center',5,'evidence_crop',1),
 ('V4-RANGE','detail_right',5,'range_context',1)
]),
('NUCLEAR — RETENTION BEAT',663.014,750.184,[
 ('V2-PWR','wide',6,'chapter_nuclear_actual',1),('V4-NUKE','wide',7,'nuclear_concept',1),('WA-01','detail_left',5,'actual_gas_turbines',1),
 ('V4-NUKE','detail_right',6,'nuclear_concept',1),('V2-DIST','detail',6,'nuclear_distribution',1),('WA-02','detail_right',5,'actual_gas_turbines',1),
 ('V2-NUKE','wide',6,'nuclear_concept',1),('V2-EHERO','detail_right',5,'actual_gas_turbines',1),('WA-07R','detail',5,'actual_gas_turbines',1),
 ('V2-NUKE','detail_left',5,'nuclear_unbuilt',1),('WA-08','detail',5,'actual_gas_turbines',1),('WA-10','detail_left',5,'actual_gas_turbines',1)
]),
('YUMA',750.184,822.857,[
 ('AR-OTTER1','doc_upper',5,'chapter_yuma',1),('V3-YUMA','detail_right',6,'yuma_test',1),('V2-YUMA','wide',6,'yuma_test',1),
 ('AR-OTTER2','doc_center',5,'otter',26),('V3-DUNE','wide',6,'dune_setup',1),('V2-DUNE','detail_right',5,'dune_setup',1),
 ('V4-RANGE','wide',5,'range_context',1),('V2-CARGO','detail_left',5,'operation',1),('V2-YUMA','detail_right',5,'yuma_test',1)
]),
('TEST RESULTS',822.857,915.853,[
 ('AR-OTTER2','doc_upper',4,'chapter_tests',26),('AR-OTTER2','doc_mid',4,'evidence_crop',26),('V3-YUMA','detail_left',5,'yuma_test',1),
 ('WB-L05','detail_right',4,'test_mechanics',1),('AR-OTTER2','doc_mid',4,'otter_limit',47),('V3-DUNE','wide',5,'dune_limit',1),
 ('V2-DUNE','detail_right',4,'dune_limit',1),('V2-YUMA','wide',5,'yuma_test',1),('AR-OTTER2','doc_lower',4,'evidence_crop',26),
 ('V3-COUPLING','detail',4,'mechanical_detail',1),('V3-DUNE','detail_left',4,'dune_limit',1),('AR-OTTER2','doc_center',5,'evidence_crop',47),
 ('AR-OTTER2','doc_upper',4,'evidence_crop',47),('V4-STEER-JOINT','detail_left',4,'mechanical_detail',1),('V2-DUNE','wide',5,'dune_limit',1)
]),
('IT WORKED',915.853,1002.057,[
 ('V4-WHEEL','wide',5,'metric_speed',1),('V4-RANGE','wide',5,'metric_range',1),('V4-CARGO','wide',5,'metric_cargo',1),
 ('V4-DRIVER','detail_right',5,'metric_crew',1),('AR-OTTER2','doc_center',4,'evidence_crop',26),('ST-572','detail_left',5,'scale_geometry',1),
 ('V3-CARGOLOAD','detail_right',5,'cargo',1),('V3-RANGE','detail_left',5,'range_context',1),('V3-ASSEMBLY','detail_left',4,'human_scale',1),
 ('WB-L05','detail_left',4,'operational_motion',1),('V2-CARGO','detail',5,'cargo',1),('WA-10','detail_right',4,'distributed_traction',1)
]),
('DEFEATED BY THE SKY',1002.057,1115.376,[
 ('AR-CH54-1','wide',5,'chapter_sky',1),('V4-HELI','wide',6,'heli_operation',1),('WC-D02','wide',5,'',1),
 ('ST-SKY','wide',6,'sky_shift',1),('AR-CH54-2','wide',5,'archive_heli',1),('V4-HELI','detail_left',5,'heli_operation',1),
 ('WC-D04','wide',5,'',1),('AR-CH54-3','wide',5,'archive_heli',1),('WC-D02','detail_left',5,'ground_context',1),
 ('WC-D01','wide',5,'',1),('AR-CH54-2','detail',4,'archive_heli',1),('WC-D04','detail_right',4,'',1),
 ('AR-CH54-3','detail',4,'archive_heli',1),('WC-D01','right',5,'sky_payoff',1)
]),
('EPILOGUE — THE LAST CAR',1115.376,1173.420,[
 ('AR-A03','wide',5,'chapter_lastcar',1),('V3-LEGACY','wide',5,'legacy',1),('V4-SURVIVOR-DETAIL','wide',4,'legacy_detail',1),
 ('V4-SURVIVOR-INTERIOR','wide',5,'legacy_interior',1),('V3-LEGACYDETAIL','detail_right',4,'legacy_detail',1),
 ('V4-EMPTY-END','wide',5,'aftermath',1),('V4-SURVIVOR-DETAIL','detail_left',4,'legacy_detail',1),
 ('V4-SURVIVOR-INTERIOR','detail_left',4,'legacy_interior',1),('V3-EMPTY','detail',5,'aftermath',1)
]),
('ENDING / CTA',1173.420,1236.506,[
 ('V3-EMPTY','wide',5,'chapter_end',1),('V3-LEGACYDETAIL','wide',4,'legacy_detail',1),('AR-A03','detail',4,'archive_survivor',1),
 ('V4-SURVIVOR-INTERIOR','detail_right',4,'legacy_interior',1),('V4-EMPTY-END','detail_left',5,'aftermath',1),
 ('V3-LEGACY','detail_left',4,'legacy',1),('V4-SURVIVOR-DETAIL','detail_right',4,'legacy_detail',1),
 ('V4-EMPTY-END','wide',9,'final_plate',1)
])]

def make_state_image(code,variant,page,out):
    im=variant_image(code,variant,page)
    # Final cleanup must happen after grading because grading/JPEG can make baked
    # collage rectangles detectable again. Iterate on the final frame itself.
    if not code.startswith('AR-'):
        arr=np.asarray(im.convert('RGB')).copy()
        for _ in range(5):
            mask=_rust_rect_mask(Image.fromarray(arr))
            if not mask.max(): break
            arr=cv2.inpaint(arr,mask,9,cv2.INPAINT_TELEA)
        im=Image.fromarray(arr)
    im.save(out,quality=94,subsampling=0)

def render_segment(img,dur,out):
    frames=max(2,round(dur*FPS))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(img),'-vf','scale=960:540,format=yuv420p','-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(out)],check=True)


FULL_TC497={'AR-A01','ST-572','WB-L02','WB-L03','WB-L06','ST-STEER','WC-Y01','WD-T01','WD-T02','WD-T03','WD-W01','WD-W02','WD-W03','WC-D01','ST-LAST','WD-LC01','WD-LC02','WD-LC03'}
BLACKLISTED_LEGACY={'WA-03','WA-04R','WA-05','ST-STEER','WB-N01','WB-N03','WB-N04','AR-A04','V3-HELILOAD'}
def visual_category(code,variant,tag):
    if code.startswith('AR-OTTER') or code=='AR-PATENT': return 'document'
    if code.startswith('AR-'): return 'archive'
    if code in {'V4-ASSEMBLY','V3-ASSEMBLY','V3-CREW'}: return 'human'
    if code in {'V3-TOPDOWN','V4-STEER-TRACKS'}: return 'geometry'
    if code in {'V4-STEER-JOINT','V4-WHEEL','V3-COUPLING','V3-WHEEL','WB-L05','WA-09','V2-TRAC'} or str(variant).startswith('detail'): return 'mechanical_detail'
    if code in {'V4-RANGE','V4-EMPTY-END','V3-RANGE','V3-EMPTY','V3-DUNE','V2-DUNE'}: return 'environment'
    if code in {'V4-CARGO','V4-HELI','V3-CARGOLOAD','V2-CARGO'}: return 'operation'
    if code in FULL_TC497 and not str(variant).startswith('detail'): return 'full_tc497'
    if code=='V4-NUKE' or code=='V2-NUKE': return 'concept'
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

def _caption_normalize(text):
    fixes=[
      (r'Robert Gilmour\s+-?Lauterno', 'Robert Gilmour LeTourneau'),
      (r'\bturn\s*-o\b', 'LeTourneau'),
      (r'\bTC\s*-\s*497\b', 'TC-497'),
      (r'\bCH\s*-\s*54\b', 'CH-54'),
      (r'\bS\s*-\s*64\b', 'S-64'),
      (r'\bLCC\s*-\s*1\b', 'LCC-1'),
      (r'\bheavy\s*-\s*lift\b', 'heavy-lift'),
      (r'\bHeavy\s*-\s*lift\b', 'Heavy-lift'),
      (r'\bcross\s*-\s*country\b', 'cross-country'),
      (r'\belectrically\s*-\s*driven\b', 'electrically-driven'),
      (r'\blow\s*-\s*pressure\b', 'low-pressure'),
      (r'\bmulti\s*-\s*section\b', 'multi-section'),
      (r'\boff\s*-\s*road\b', 'off-road'),
      (r'\bsix\s*-\s*person\b', 'six-person'),
      (r'\btrain\s*-\s*sized\b', 'train-sized'),
      (r'\brubber\s*-\s*tired\b', 'rubber-tired'),
      (r'\bLeTourneau\s*-\s*train\b', 'LeTourneau train')
    ]
    for pat,repl in fixes:
        text=re.sub(pat,repl,text,flags=re.I if pat.startswith('\\bturn') else 0)
    text=re.sub(r'\b([A-Za-z]+)\s*-\s*([A-Za-z]+)\b',r'\1-\2',text)
    text=re.sub(r'\s+([,.;:!?])',r'\1',text)
    text=re.sub(r'\s{2,}',' ',text).strip()
    return text

def build_captions():
    path=next(TR.glob('TC497_VO_WORD_LEVEL.csv'))
    words=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            ss=float(r['start_sec']); ee=float(r['end_sec'])
            if ss>=END: break
            words.append({'s':ss,'e':min(ee,END),'w':r['word']})
    phrases=[]; buf=[]
    for w in words:
        buf.append(w)
        span=buf[-1]['e']-buf[0]['s']; chars=sum(len(x['w'])+1 for x in buf)
        punct=bool(re.search(r'[.!?;:]$',w['w'])); comma=bool(re.search(r',$',w['w']))
        if len(buf)>=7 or chars>=48 or span>=2.45 or (punct and len(buf)>=3) or (comma and len(buf)>=5):
            raw=' '.join(x['w'] for x in buf)
            phrases.append({'s':buf[0]['s'],'e':buf[-1]['e']+.08,'text':_caption_normalize(raw)})
            buf=[]
    if buf:
        phrases.append({'s':buf[0]['s'],'e':buf[-1]['e']+.08,'text':_caption_normalize(' '.join(x['w'] for x in buf))})
    (PUB/'captions.json').write_text(json.dumps(phrases,ensure_ascii=False),encoding='utf-8')
    suspicious=[p['text'] for p in phrases if re.search(r'(Lauterno|turn\s*-o|TC\s+-|CH\s+-|S\s+-|\w+\s+-\w+)',p['text'],re.I)]
    (WORK/'CAPTION_QA.json').write_text(json.dumps({'phrases':len(phrases),'suspicious_count':len(suspicious),'suspicious':suspicious[:30]},ensure_ascii=False,indent=2),encoding='utf-8')
    if suspicious:
        raise RuntimeError(f'caption normalization left suspicious phrases: {suspicious[:5]}')


def _slow_noise(rng,n,rate=32):
    if n<=1: return np.zeros(n,dtype=np.float32)
    points=max(3,int(n/48000*rate)+2)
    anchors=rng.normal(0,1,points).astype(np.float32)
    xi=np.linspace(0,points-1,n,dtype=np.float32)
    return np.interp(xi,np.arange(points,dtype=np.float32),anchors).astype(np.float32)

def build_score(shots):
    sr=48000
    rng=np.random.default_rng(4974)
    out=PUB/'rest_score.wav'
    roots={
      'WHEN THE ROAD ENDS':41.2,'THE ELECTRIC WHEEL':46.3,'BIGGER AND BIGGER':43.7,'THE 572-FOOT MACHINE':49.0,
      'HOW DO YOU DRIVE 572 FEET?':38.9,'NUCLEAR — RETENTION BEAT':51.9,'YUMA':43.7,'TEST RESULTS':46.3,
      'IT WORKED':49.0,'DEFEATED BY THE SKY':41.2,'EPILOGUE — THE LAST CAR':36.7,'ENDING / CTA':32.7
    }
    with wave.open(str(out),'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        for ci,(name,cs,ce,_) in enumerate(CHAPTERS):
            dur=ce-cs; n=max(1,int(round(dur*sr))); tt=np.arange(n,dtype=np.float32)/sr
            a=np.zeros(n,dtype=np.float32)
            root=roots[name]
            wind=_slow_noise(rng,n,24); micro=_slow_noise(rng,n,96)
            # Original underscore: root + fifth + octave, intentionally sparse.
            breath=.5+.5*np.sin(2*np.pi*(1/18.0)*tt + ci*.63)
            pad=(np.sin(2*np.pi*root*tt)+.42*np.sin(2*np.pi*(root*1.5)*tt+.4)+.18*np.sin(2*np.pi*(root*2)*tt+1.1))
            base_amp={
              'WHEN THE ROAD ENDS':.0045,'THE ELECTRIC WHEEL':.0060,'BIGGER AND BIGGER':.0046,'THE 572-FOOT MACHINE':.0052,
              'HOW DO YOU DRIVE 572 FEET?':.0048,'NUCLEAR — RETENTION BEAT':.0040,'YUMA':.0038,'TEST RESULTS':.0042,
              'IT WORKED':.0055,'DEFEATED BY THE SKY':.0042,'EPILOGUE — THE LAST CAR':.0018,'ENDING / CTA':.0007
            }[name]
            a += base_amp*pad*(.35+.65*breath)

            # Environmental texture by chapter.
            if name in {'WHEN THE ROAD ENDS','YUMA','TEST RESULTS'}:
                a += .0042*wind + .0017*micro
            if name in {'THE ELECTRIC WHEEL','THE 572-FOOT MACHINE','HOW DO YOU DRIVE 572 FEET?','IT WORKED'}:
                pulse=np.maximum(0,np.sin(2*np.pi*.52*tt))**7
                a += .0048*pulse*np.sin(2*np.pi*(root*.74)*tt) + .0018*micro
            if name=='DEFEATED BY THE SKY':
                rotor=np.maximum(0,np.sin(2*np.pi*6.15*tt))**6
                a += .0105*rotor*np.sin(2*np.pi*45*tt)+.0058*wind
            if name=='EPILOGUE — THE LAST CAR':
                a += .0013*wind
            if name=='ENDING / CTA':
                a += .00045*wind

            # Deliberate 1.2-2.0s dropouts every ~22s so the soundtrack breathes.
            pos=14.0 + (ci%3)*2.1
            while pos<dur-4:
                L=int((1.2 + .35*((ci+int(pos))%3))*sr)
                st=int(pos*sr); en=min(n,st+L)
                if en>st:
                    win=np.ones(en-st,dtype=np.float32)
                    edge=min(len(win)//2,int(.18*sr))
                    if edge>1:
                        win[:edge]=np.linspace(1,.08,edge); win[-edge:]=np.linspace(.08,1,edge)
                        if len(win)>2*edge: win[edge:-edge]=.08
                    a[st:en]*=win
                pos+=22.0

            # Sound events tied to editorial category.
            local=[x for x in shots if x['chapter']==name]
            for sh in local:
                p=max(0,int((sh['s']-cs)*sr))
                cat=sh['category']
                if cat=='document':
                    L=min(int(.20*sr),n-p)
                    if L>0:
                        noise=rng.normal(0,1,L).astype(np.float32)
                        env=np.exp(-np.arange(L,dtype=np.float32)/(sr*.055))
                        a[p:p+L]+=.0050*noise*env
                elif cat=='mechanical_detail':
                    L=min(int(.16*sr),n-p)
                    if L>0:
                        x=np.arange(L,dtype=np.float32)/sr
                        a[p:p+L]+=.0055*np.sin(2*np.pi*86*x)*np.exp(-x*22)
                elif cat=='operation':
                    L=min(int(.26*sr),n-p)
                    if L>0:
                        x=np.arange(L,dtype=np.float32)/sr
                        a[p:p+L]+=.0040*np.sin(2*np.pi*61*x)*np.exp(-x*12)

            # Chapter entry/exit dynamics.
            L=min(n,int(.45*sr))
            if ci>0 and L>0:
                x=np.arange(L,dtype=np.float32)/sr
                a[:L]+=.012*np.sin(2*np.pi*37*x)*np.exp(-x*10)
            F=min(n,int(.9*sr))
            if F>2:
                a[:F]*=np.linspace(0,1,F,dtype=np.float32)
                a[-F:]*=np.linspace(1,0,F,dtype=np.float32)
            pcm=(np.clip(a,-.38,.38)*32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())


def audit(shots):
    counts=Counter(x['code'] for x in shots)
    ds=[x['e']-x['s'] for x in shots]
    full_streak=0; max_full=0; cat_streak=0; max_cat=0; prev=None
    priority={'HOW DO YOU DRIVE 572 FEET?','NUCLEAR — RETENTION BEAT','TEST RESULTS','IT WORKED','DEFEATED BY THE SKY','EPILOGUE — THE LAST CAR','ENDING / CTA'}
    for x in shots:
        if x['category']=='full_tc497': full_streak+=1
        else: full_streak=0
        max_full=max(max_full,full_streak)
        if x['chapter'] in priority and x['category'] not in {'archive','document'}:
            if x['category']==prev: cat_streak+=1
            else: cat_streak=1; prev=x['category']
            max_cat=max(max_cat,cat_streak)
        else:
            cat_streak=0; prev=None

    orange_files=[]
    for p in IMG.glob('*.jpg'):
        if '_AR-' in p.name: continue
        if _rust_rect_mask(Image.open(p)).max(): orange_files.append(p.name)

    bad=[x for x in shots if x['code'] in BLACKLISTED_LEGACY]
    # Documents may use multiple distinct pages/crops; photographic stills are capped by source image.
    over={k:v for k,v in counts.items() if v>3 and not k.startswith('AR-OTTER') and k!='AR-PATENT'}
    caption_qa=json.loads((WORK/'CAPTION_QA.json').read_text())
    report={
      'shot_count_after_cold_open':len(shots),
      'min_shot_sec':min(ds),'max_shot_sec':max(ds),'median_shot_sec':float(np.median(ds)),
      'AR-SNO':counts['AR-SNO'],'AR-A01_after_cold_open':counts['AR-A01'],
      'max_consecutive_full_tc497':max_full,'max_consecutive_visual_category':max_cat,
      'orange_edge_blocks_after_cleanup':len(orange_files),'orange_flagged_files':orange_files,
      'blacklisted_legacy_uses':bad,'image_assets_over_3_uses':over,
      'caption_qa':caption_qa,
      'standalone_graphics':0,'generic_split_screens':0,
      'new_v4_asset_uses':sum(1 for x in shots if x['code'].startswith('V4-'))
    }
    (WORK/'V4_QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if counts['AR-SNO']>1: raise RuntimeError('AR-SNO reuse exceeds V4 rule')
    if counts['AR-A01']>2: raise RuntimeError('AR-A01 reuse exceeds V4 rule')
    if max_full>2: raise RuntimeError(f'full TC497 streak exceeds V4 rule: {max_full}')
    if max_cat>2: raise RuntimeError(f'visual-category streak exceeds V4 rule: {max_cat}')
    if orange_files: raise RuntimeError(f'baked orange/rust edge blocks remain: {orange_files[:5]}')
    if bad: raise RuntimeError(f'blacklisted misleading/legacy assets remain: {bad[:5]}')
    if over: raise RuntimeError(f'image asset reuse >3: {over}')
    if caption_qa.get('suspicious_count'): raise RuntimeError('caption QA failed')
    return report


if __name__=='__main__':
    shots=build_rest(); build_captions(); build_score(shots); qa=audit(shots)
    print('FULL_V4_PREP_DONE',qa)
