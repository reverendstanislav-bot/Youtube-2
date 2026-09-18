import os, csv, json, math, re, subprocess, textwrap, wave
from pathlib import Path
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from openpyxl import load_workbook
import numpy as np

PKG=Path(os.environ["PKG_ROOT"])
GEN=Path(os.environ["GEN_DIR"])
ARC=PKG/"04_DOWNLOADS"/"ARCHIVE_GREEN"
XLSX=PKG/"03_TIMELINE"/"TC497_FINAL_VISUAL_TIMELINE_CODEX_EDIT_MAP_v2.xlsx"
TR=Path(os.environ["TRANSCRIPT_DIR"])
WORK=Path(os.environ["FULL_WORK"])
PUB=Path(os.environ["FULL_PUBLIC"])
WORK.mkdir(parents=True,exist_ok=True)
PUB.mkdir(parents=True,exist_ok=True)
IMGDIR=WORK/"state_images"; IMGDIR.mkdir(exist_ok=True)
SEGDIR=WORK/"segments"; SEGDIR.mkdir(exist_ok=True)
PDFDIR=WORK/"pdf_pages"; PDFDIR.mkdir(exist_ok=True)
FPS=30
CUT_START=82.6
END=1236.506
W,H=960,540

C={
 "charcoal":(23,26,28),"iron":(48,54,58),"paper":(230,221,200),
 "ivory":(243,235,221),"rust":(165,82,53),"blue":(95,116,125),
 "matte":(191,179,155),"black":(14,16,17)
}
FONT_B="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fnt(sz,bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R,sz)

def sec(v):
    if hasattr(v,"total_seconds"): return float(v.total_seconds())
    return float(v)

def fit_cover(im,size=(W,H),anchor=(.5,.5)):
    im=im.convert("RGB")
    tw,th=size; iw,ih=im.size
    s=max(tw/iw,th/ih)
    nw,nh=round(iw*s),round(ih*s)
    im=im.resize((nw,nh),Image.Resampling.LANCZOS)
    x=max(0,min(nw-tw,round((nw-tw)*anchor[0])))
    y=max(0,min(nh-th,round((nh-th)*anchor[1])))
    return im.crop((x,y,x+tw,y+th))

def fit_inside(im,size=(W,H),pad=28,bg=None):
    bg=bg or C["matte"]
    out=Image.new("RGB",size,bg)
    tw,th=size[0]-2*pad,size[1]-2*pad
    im=im.convert("RGB")
    im.thumbnail((tw,th),Image.Resampling.LANCZOS)
    x=(size[0]-im.width)//2; y=(size[1]-im.height)//2
    out.paste(im,(x,y))
    return out

def grade(im,kind):
    im=im.convert("RGB")
    if kind=="generated":
        im=ImageEnhance.Brightness(im).enhance(1.035)
        im=ImageEnhance.Contrast(im).enhance(1.025)
        im=ImageEnhance.Color(im).enhance(.90)
    elif kind=="archive":
        im=ImageOps.grayscale(im).convert("RGB")
        warm=Image.new("RGB",im.size,C["paper"])
        im=Image.blend(im,warm,.12)
        im=ImageEnhance.Contrast(im).enhance(1.03)
        im=ImageEnhance.Brightness(im).enhance(.94)
    elif kind=="document":
        im=ImageEnhance.Color(im).enhance(.72)
        im=ImageEnhance.Brightness(im).enhance(.92)
        im=ImageEnhance.Contrast(im).enhance(1.00)
    return im

def gen_path(code):
    p=GEN/(code+".png")
    if not p.exists(): raise FileNotFoundError(code)
    return p

ARCHIVE_MAP={
 "AR-A01":"AR-A01__*","AR-A03":"AR-A03__*","AR-A04":"AR-A04__*",
 "AR-CH54-1":"AR-CH54-1__*","AR-CH54-2":"AR-CH54-2__*","AR-CH54-3":"AR-CH54-3__*",
 "AR-DEW-BARTER":"AR-DEW-BARTER__*","AR-DEW-MAP":"AR-DEW-MAP__*",
 "AR-DEW-RADAR":"AR-DEW-RADAR__*","AR-SNO":"AR-SNO__*",
 "AR-OTTER1":"AR-OTTER1__*","AR-OTTER2":"AR-OTTER2__*","AR-PATENT":"AR-PATENT__*"
}
def archive_path(code):
    xs=list(ARC.glob(ARCHIVE_MAP[code]))
    if not xs: raise FileNotFoundError(code)
    return xs[0]

PDF_PAGE_BY_ROW={
 23:1,59:1,71:8,82:1,87:8,89:8,93:26
}
def pdf_page(code,rownum,page=None):
    p=archive_path(code)
    if page is None: page=PDF_PAGE_BY_ROW.get(rownum,1)
    out=PDFDIR/(f"{code}_p{page}.png")
    if not out.exists():
        stem=out.with_suffix("")
        subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-singlefile","-png","-r","120",str(p),str(stem)],
                       check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return out

def source_image(code,typ,rownum=0,detail=False):
    if typ=="Generated":
        im=Image.open(gen_path(code))
        # purposeful detail crops only when timeline itself calls for detail.
        anchors={
            "WB-L05":(.46,.58),"WA-09":(.52,.56),"WB-L04":(.56,.52),
            "AR-A04":(.5,.5),"WD-LC02":(.42,.50)
        }
        return grade(fit_cover(im,anchor=anchors.get(code,(.5,.5))),"generated")
    if typ=="Archive":
        p=archive_path(code)
        if p.suffix.lower()==".pdf":
            im=Image.open(pdf_page(code,rownum))
            return grade(fit_inside(im,pad=24,bg=C["matte"]),"document")
        im=Image.open(p)
        if detail:
            return grade(fit_cover(im,anchor=(.5,.48)),"archive")
        return grade(fit_inside(im,pad=22,bg=C["matte"]),"archive")
    raise ValueError((code,typ))

def base_canvas():
    im=Image.new("RGB",(W,H),C["charcoal"])
    d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,H],fill=C["paper"])
    d.rectangle([0,0,W,7],fill=C["rust"])
    d.rectangle([0,H-5,W,H],fill=C["iron"])
    return im

def label(draw,xy,text,size=22,color=None,bold=True,anchor=None):
    draw.text(xy,text,font=fnt(size,bold),fill=color or C["charcoal"],anchor=anchor)

def line(draw,pts,fill=None,width=3):
    draw.line(pts,fill=fill or C["blue"],width=width)

def graphic(code):
    im=base_canvas(); d=ImageDraw.Draw(im)
    label(d,(50,45),code,14,C["blue"])
    if code=="GR-R01":
        label(d,(50,86),"WHEN THE ROAD ENDS",36)
        # rail
        line(d,[(70,190),(410,190)],C["iron"],5)
        line(d,[(70,214),(410,214)],C["iron"],5)
        for x in range(85,405,28): line(d,[(x,182),(x,222)],C["iron"],2)
        label(d,(70,238),"RAIL",16,C["iron"])
        # road
        line(d,[(70,340),(420,340)],C["blue"],12)
        for x in range(90,410,50): line(d,[(x,340),(x+24,340)],C["paper"],3)
        label(d,(70,365),"ROAD",16,C["blue"])
        # destination beyond
        line(d,[(420,202),(650,270)],C["rust"],3)
        line(d,[(420,340),(650,270)],C["rust"],3)
        d.ellipse([646,256,674,284],fill=C["rust"])
        label(d,(690,255),"DESTINATION",22,C["rust"])
        label(d,(690,288),"still beyond both networks",16,C["iron"],False)
    elif code=="GR-E01":
        label(d,(50,82),"ELECTRIC DRIVE",38)
        xs=[55,260,465,690]; names=["GAS TURBINE","GENERATOR","ELECTRICAL BUS","WHEEL MOTORS"]
        for i,(x,nm) in enumerate(zip(xs,names)):
            d.rounded_rectangle([x,205,x+165,305],14,fill=C["iron"] if i<3 else C["rust"])
            label(d,(x+82,255),nm,16,C["ivory"],True,"mm")
            if i<3:
                line(d,[(x+165,255),(xs[i+1],255)],C["blue"],6)
                d.polygon([(xs[i+1]-4,247),(xs[i+1]+8,255),(xs[i+1]-4,263)],fill=C["blue"])
        label(d,(55,350),"mechanical complexity becomes electrical distribution",18,C["iron"],False)
    elif code=="GR-E02":
        bg=source_image("WA-09","Generated")
        im=Image.blend(bg,Image.new("RGB",(W,H),C["charcoal"]),.28); d=ImageDraw.Draw(im)
        label(d,(50,54),"ELECTRIC WHEEL",32,C["ivory"])
        for y,txt in [(180,"HIGH-TORQUE DC MOTOR"),(270,"POWERED HUB"),(360,"10-FT TIRE")]:
            line(d,[(520,y),(730,y)],C["rust"],3); d.ellipse([512,y-5,522,y+5],fill=C["rust"])
            label(d,(745,y),txt,18,C["ivory"],True,"lm")
    elif code=="GR-B01":
        label(d,(50,80),"LETOURNEAU OVERLAND LINEAGE",30)
        names=["VC-12","TC-264","VC-22","LCC-1","TC-497"]
        xs=[75,245,415,585,755]
        line(d,[(75,270),(825,270)],C["blue"],5)
        for x,n in zip(xs,names):
            d.ellipse([x-10,260,x+10,280],fill=C["rust"] if n=="TC-497" else C["iron"])
            label(d,(x,220),n,20,C["rust"] if n=="TC-497" else C["iron"],True,"mm")
        label(d,(50,345),"Each generation pushed the same idea farther: more load, more length, more distributed power.",17,C["iron"],False)
    elif code=="GR-L01":
        label(d,(50,75),"572 FEET",54,C["rust"])
        label(d,(52,133),"174 METERS • FINAL DESCRIBED CONFIGURATION",17,C["iron"])
        line(d,[(70,300),(890,300)],C["iron"],5)
        for i in range(0,7):
            x=70+i*(820/6); line(d,[(x,287),(x,313)],C["blue"],3)
            if i<6: label(d,(x,335),str(i*100)+" ft",13,C["iron"],False,"mm")
        label(d,(480,402),"A transportation system the length of a city block — multiplied.",18,C["iron"],False,"mm")
    elif code=="GR-L02":
        label(d,(50,70),"13 UNITS • 54 DRIVEN WHEELS",34)
        x=55
        widths=[85]+[58]*12
        for i,w0 in enumerate(widths):
            fill=C["rust"] if i==0 else C["iron"]
            d.rounded_rectangle([x,235,x+w0,300],8,fill=fill)
            wheels=2 if i in (0,12) else 4
            for j in range(wheels):
                wx=x+(j+1)*w0/(wheels+1)
                d.ellipse([wx-7,294,wx+7,308],fill=C["blue"])
            x+=w0+7
        label(d,(55,355),"distributed traction across the consist",18,C["iron"],False)
    elif code=="GR-H01":
        label(d,(50,72),"OFF-TRACKING vs CLOSER-FOLLOW STEERING",29)
        # Conventional
        label(d,(70,145),"CONVENTIONAL TRAILERS",15,C["iron"])
        pts=[(70,240),(180,180),(300,180),(420,250)]
        line(d,pts,C["iron"],5)
        line(d,[(70,270),(180,230),(300,235),(420,290)],C["rust"],4)
        # coordinated
        label(d,(545,145),"TC-497 LOGIC",15,C["iron"])
        pts2=[(540,240),(650,180),(770,180),(885,250)]
        line(d,pts2,C["blue"],5)
        line(d,[(540,250),(650,192),(770,192),(885,260)],C["blue"],3)
        label(d,(480,380),"rear units follow closer to the lead path",18,C["iron"],False,"mm")
    elif code=="GR-H02":
        label(d,(50,75),"STEERING + DISTRIBUTED TRACTION",30)
        xs=[70,235,400,565,730]
        line(d,[(90,250),(820,250)],C["blue"],4)
        for i,x in enumerate(xs):
            d.rounded_rectangle([x,205,x+120,290],10,fill=C["iron"])
            label(d,(x+60,235),"MODULE",13,C["ivory"],True,"mm")
            for wx in (x+28,x+92):
                d.ellipse([wx-13,280,wx+13,306],fill=C["rust"])
        label(d,(70,350),"steering information propagates through articulated modules",17,C["iron"],False)
        label(d,(70,382),"traction is distributed instead of concentrated at the front",17,C["iron"],False)
    elif code=="GR-N01":
        label(d,(50,68),"DO NOT CONFUSE THE TWO",34)
        d.rounded_rectangle([60,155,445,420],18,fill=(210,198,174))
        d.rounded_rectangle([515,155,900,420],18,fill=C["iron"])
        label(d,(252,195),"1961 CONCEPT",20,C["rust"],True,"mm")
        label(d,(252,250),"NUCLEAR-POWERED",28,C["charcoal"],True,"mm")
        label(d,(252,290),"OVERLAND VEHICLE",28,C["charcoal"],True,"mm")
        label(d,(252,355),"proposal / concept",16,C["iron"],False,"mm")
        label(d,(707,195),"ACTUAL TC-497",20,C["paper"],True,"mm")
        label(d,(707,250),"GAS TURBINES",30,C["ivory"],True,"mm")
        label(d,(707,300),"+ ELECTRIC DRIVE",23,C["ivory"],True,"mm")
        label(d,(707,355),"built and tested",16,C["paper"],False,"mm")
    elif code=="GR-N02":
        label(d,(50,75),"THE CONCEPTUAL APPEAL",32)
        items=[("CENTRAL\nPOWER",65),("GENERATOR",285),("LONG ELECTRICAL\nDISTRIBUTION",505),("WHEEL\nMOTORS",755)]
        for idx,(nm,x) in enumerate(items):
            d.rounded_rectangle([x,205,x+150,315],14,fill=C["rust"] if idx==0 else C["iron"])
            label(d,(x+75,260),nm,16,C["ivory"],True,"mm")
            if idx<len(items)-1:
                line(d,[(x+150,260),(items[idx+1][1],260)],C["blue"],5)
        label(d,(65,370),"Concept only — not the powerplant used by TC-497.",18,C["rust"])
    elif code=="GR-Y01":
        label(d,(50,72),"YUMA / PROJECT OTTER",32)
        events=[("1962","YUMA TESTING"),("FEB 1963","FORMAL OTTER TESTS"),("JUN 1963","SECOND OTTER TEST SERIES")]
        ys=[175,275,375]
        line(d,[(190,160),(190,400)],C["blue"],5)
        for (date,txt),y in zip(events,ys):
            d.ellipse([179,y-11,201,y+11],fill=C["rust"])
            label(d,(145,y),date,18,C["iron"],True,"rm")
            label(d,(235,y),txt,21,C["charcoal"],True,"lm")
    elif code=="GR-T01":
        label(d,(50,68),"PROJECT OTTER — COURSE RESULTS",30)
        cards=[("COURSE 12","4 traverses","NO terrain-induced immobilization"),
               ("COURSE 1","4 traverses","NO delays or immobilizations")]
        for i,(a,b,c) in enumerate(cards):
            y=155+i*175
            d.rounded_rectangle([60,y,900,y+135],16,fill=(214,203,182))
            label(d,(90,y+32),a,24,C["rust"])
            label(d,(90,y+72),b,18,C["iron"],False)
            label(d,(390,y+67),c,18,C["charcoal"])
        label(d,(60,485),"Source: Project OTTER Test Report (1963)",13,C["blue"],False)
    elif code=="GR-T02":
        label(d,(50,65),"THE LIMIT",34,C["rust"])
        basey=410
        line(d,[(60,basey),(370,basey),(600,basey-190),(900,basey-190)],C["iron"],6)
        # slope annotation
        line(d,[(370,basey),(600,basey-190)],C["rust"],5)
        line(d,[(390,basey-10),(390,basey-190)],C["blue"],3)
        label(d,(410,310),"12 FT",25,C["rust"])
        label(d,(520,395),"28° SLOPE",18,C["iron"])
        label(d,(635,190),"DUNE SLIP FACE",18,C["iron"])
        label(d,(60,455),"Attempt unsuccessful — Project OTTER test report.",16,C["iron"],False)
    elif code=="GR-W01":
        label(d,(50,72),"IT WORKED",42,C["rust"])
        metrics=[("~20 MPH","speed range"),("~400 MI","official retrospective"),("~150 TONS","cargo capacity"),("6 CREW","crew")]
        for i,(a,b) in enumerate(metrics):
            x=55+(i%2)*455; y=165+(i//2)*155
            d.rounded_rectangle([x,y,x+405,y+115],16,fill=C["iron"])
            label(d,(x+25,y+32),a,30,C["ivory"])
            label(d,(x+25,y+77),b,15,C["paper"],False)
    else:
        label(d,(50,100),code,36,C["rust"])
    return im

def split_comp(left,right,title=None,ratio=.5):
    out=Image.new("RGB",(W,H),C["charcoal"])
    lw=int(W*ratio)
    l=fit_cover(left,(lw,H)); r=fit_cover(right,(W-lw,H))
    out.paste(l,(0,0)); out.paste(r,(lw,0))
    d=ImageDraw.Draw(out); d.rectangle([lw-2,0,lw+2,H],fill=C["paper"])
    if title:
        d.rectangle([0,0,W,62],fill=(23,26,28))
        label(d,(30,31),title,20,C["ivory"],True,"lm")
    return out

def composite(code,rownum):
    if code=="CP-R01":
        a=source_image("AR-DEW-MAP","Archive",rownum)
        b=source_image("AR-DEW-BARTER","Archive",rownum)
        out=split_comp(a,b,"DEW LINE • SUPPLY ROUTE")
        d=ImageDraw.Draw(out); line(d,[(85,390),(250,330),(430,290),(565,260),(785,210)],C["rust"],4)
        return out
    if code=="CP-R02":
        return split_comp(source_image("AR-SNO","Archive",rownum,True),source_image("WC-R03","Generated"),"FROM ROADLESS PROBLEM TO OVERLAND SOLUTION")
    if code=="CP-E01":
        return split_comp(source_image("AR-PATENT","Archive",rownum),source_image("WA-09","Generated"),"PATENT → PRACTICAL WHEEL MOTOR")
    if code=="CP-B01":
        return split_comp(source_image("AR-SNO","Archive",rownum),source_image("WC-B03","Generated"),"THE LINEAGE GETS BIGGER")
    if code=="CP-L01":
        return split_comp(source_image("AR-A01","Archive",rownum),source_image("WB-L02","Generated"),"EVIDENCE → FULL PROFILE")
    if code=="CP-L02":
        bg=source_image("WB-L02","Generated"); out=ImageEnhance.Brightness(bg).enhance(.78); d=ImageDraw.Draw(out)
        d.rectangle([35,35,925,155],fill=(23,26,28))
        label(d,(60,65),"572 FEET",34,C["rust"]); label(d,(290,65),"13 UNITS",26,C["ivory"]); label(d,(520,65),"54 DRIVEN WHEELS",26,C["ivory"])
        label(d,(60,115),"distributed electric drive across the consist",16,C["paper"],False)
        return out
    if code=="CP-H02":
        bg=source_image("WA-04R","Generated"); out=ImageEnhance.Brightness(bg).enhance(.82); d=ImageDraw.Draw(out)
        line(d,[(70,360),(230,300),(430,310),(650,275),(880,245)],C["blue"],5)
        line(d,[(70,390),(230,345),(430,350),(650,320),(880,300)],C["rust"],3)
        label(d,(55,55),"PATH TRACES",20,C["ivory"])
        return out
    if code=="CP-H01":
        return split_comp(source_image("AR-OTTER2","Archive",rownum),source_image("WA-12","Generated"),"DOCUMENTED TEST → STEERING EXPLANATION")
    if code=="CP-N01":
        a=graphic("GR-N01"); b=source_image("WB-N01","Generated")
        return split_comp(a,b,"1961 CONCEPT • NOT THE TC-497 POWERPLANT",.48)
    if code=="CP-N02":
        return split_comp(source_image("WB-N02","Generated"),source_image("AR-A01","Archive",rownum),"CONCEPT → ACTUAL GAS-TURBINE TC-497")
    if code=="CP-Y01":
        return split_comp(source_image("AR-OTTER1","Archive",rownum),source_image("WC-Y01","Generated"),"PROJECT OTTER → YUMA")
    if code=="CP-Y02":
        return split_comp(source_image("AR-OTTER1","Archive",rownum),source_image("WC-Y01","Generated"),"TEST RANGE • YUMA")
    if code=="CP-T01":
        left=grade(fit_inside(Image.open(pdf_page("AR-OTTER2",rownum,26)),pad=24,bg=C["matte"]),"document")
        return split_comp(left,source_image("WD-T01","Generated"),"REPORT RESULT → SUCCESSFUL TRAVERSAL")
    if code=="CP-T02":
        left=grade(fit_inside(Image.open(pdf_page("AR-OTTER2",rownum,47)),pad=24,bg=C["matte"]),"document")
        return split_comp(left,source_image("WC-Y02","Generated"),"12-FT DUNE SLIP FACE")
    if code=="CP-W01":
        left=grade(fit_inside(Image.open(pdf_page("AR-OTTER2",rownum,26)),pad=24,bg=C["matte"]),"document")
        out=split_comp(left,source_image("WD-W01","Generated"),"PROJECT OTTER • PERFORMANCE EVIDENCE")
        d=ImageDraw.Draw(out); label(d,(535,462),"Four traverses • no terrain-induced immobilization",14,C["ivory"],False)
        return out
    if code=="CP-W02":
        return split_comp(source_image("AR-A01","Archive",rownum),source_image("WD-W02","Generated"),"REAL MACHINE • REAL CARGO JOB")
    if code=="CP-D01":
        bg=source_image("WC-D01","Generated")
        heli=Image.open(archive_path("AR-CH54-1")).convert("RGB")
        # crop helicopter away from most ground, then key out near-white sky.
        crop=heli.crop((0,160,heli.width,760))
        crop.thumbnail((480,240),Image.Resampling.LANCZOS)
        gray=ImageOps.grayscale(crop)
        mask=gray.point(lambda p: 255 if p<205 else max(0,int((235-p)*8.5)))
        mask=mask.filter(ImageFilter.GaussianBlur(1.2))
        rgba=crop.convert("RGBA"); rgba.putalpha(mask)
        out=bg.convert("RGBA")
        out.alpha_composite(rgba,(450,70))
        d=ImageDraw.Draw(out)
        d.rectangle([28,28,305,86],fill=(23,26,28,220))
        label(d,(45,57),"REAL U.S. ARMY CH-54",16,C["ivory"],True,"lm")
        return out.convert("RGB")
    if code=="CP-D02":
        return split_comp(source_image("WC-D01","Generated"),source_image("AR-CH54-2","Archive",rownum),"THE LOGISTICS ANSWER CHANGED")
    return source_image("ST-COLD","Generated")

def load_timeline():
    wb=load_workbook(XLSX,data_only=True)
    ws=wb["VISUAL_TIMELINE"]
    headers=[c.value for c in ws[4]]
    out=[]
    for r in ws.iter_rows(min_row=5,values_only=True):
        if not r[0]: continue
        d=dict(zip(headers,r))
        d["Start"]=sec(d["Start"]); d["End"]=sec(d["End"]); d["Dur"]=sec(d["Dur"])
        out.append(d)
    return out

ROWS=load_timeline()

def state_image(row):
    n=int(row["#"]); typ=row["Source Type"]; code=row["Asset Code"]
    out=IMGDIR/f"{n:03d}_{code}.jpg"
    if out.exists(): return out
    detail=("detail" in str(row["VO / Visual Beat"]).lower() or "crop" in str(row["VO / Visual Beat"]).lower())
    if typ=="Generated": im=source_image(code,typ,n,detail)
    elif typ=="Archive": im=source_image(code,typ,n,detail)
    elif typ=="Graphic": im=graphic(code)
    elif typ=="Composite": im=composite(code,n)
    else: im=Image.new("RGB",(W,H),C["charcoal"])
    im.save(out,quality=94,subsampling=0)
    return out

def render_segment(row,start,end,out):
    dur=end-start
    frames=max(1,round(dur*FPS))
    img=state_image(row)
    typ=row["Source Type"]
    n=int(row["#"])
    # Motion is deliberately restrained. Archive/graphics/composites are mostly locked.
    motion=(typ=="Generated" and n%3!=0 and dur>=5)
    if motion:
        # One-direction micro push. No reversal.
        vf=("scale=1008:567:force_original_aspect_ratio=increase,crop=1008:567,"
            "zoompan=z='min(zoom+0.000055,1.018)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=960x540:fps=30,"
            "format=yuv420p")
    else:
        vf="scale=960:540,format=yuv420p"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-loop","1","-i",str(img),
                    "-vf",vf,"-frames:v",str(frames),"-an","-c:v","libx264","-preset","veryfast","-crf","19",
                    "-pix_fmt","yuv420p",str(out)],check=True)

def build_rest():
    selected=[]
    for row in ROWS:
        if row["End"]<=CUT_START: continue
        st=max(CUT_START,row["Start"]); en=min(END,row["End"])
        if en<=st: continue
        selected.append((row,st,en))
    paths=[]
    decisions=[]
    for i,(row,st,en) in enumerate(selected,1):
        p=SEGDIR/f"{i:03d}.mp4"
        render_segment(row,st,en,p)
        paths.append(p)
        decisions.append({
            "row":int(row["#"]),"start":st,"end":en,"chapter":row["Chapter"],
            "source_type":row["Source Type"],"asset":row["Asset Code"],
            "beat":row["VO / Visual Beat"],"instruction":row["Codex Edit Instruction"]
        })
    concat=WORK/"rest_concat.txt"
    concat.write_text("".join("file '"+str(p.resolve())+"'\\n" for p in paths))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),
                    "-c","copy",str(PUB/"rest_base.mp4")],check=True)
    (PUB/"timeline.json").write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding="utf-8")
    return decisions

def build_captions():
    path=TR/"TC497_VO_WORD_LEVEL.csv"
    words=[]
    with open(path,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            s=float(r["start_sec"]); e=float(r["end_sec"])
            if s>=END: break
            words.append((s,min(e,END),r["word"]))
    phrases=[]; buf=[]
    for w in words:
        buf.append(w)
        punct=bool(re.search(r"[.!?;:]$",w[2]))
        comma=bool(re.search(r",$",w[2]))
        span=buf[-1][1]-buf[0][0]
        char=sum(len(x[2])+1 for x in buf)
        if len(buf)>=7 or char>=48 or span>=2.45 or (punct and len(buf)>=3) or (comma and len(buf)>=5):
            phrases.append({"s":buf[0][0],"e":buf[-1][1]+.10,"words":[{"s":x[0],"e":x[1],"w":x[2]} for x in buf]})
            buf=[]
    if buf: phrases.append({"s":buf[0][0],"e":buf[-1][1]+.10,"words":[{"s":x[0],"e":x[1],"w":x[2]} for x in buf]})
    (PUB/"captions.json").write_text(json.dumps(phrases,ensure_ascii=False),encoding="utf-8")
    return phrases

def build_events():
    # Chapter events, archive/reconstruction/concept source bugs.
    ch=[]; bugs=[]
    last=None
    for row in ROWS:
        if row["End"]<=CUT_START: continue
        st=max(CUT_START,row["Start"])
        if row["Chapter"]!=last:
            ch.append({"s":st,"e":min(st+2.35,row["End"]),"text":row["Chapter"]})
            last=row["Chapter"]
        typ=row["Source Type"]; code=row["Asset Code"]
        if typ=="Generated":
            if str(row["Chapter"]).startswith("NUCLEAR"):
                bugs.append({"s":st+.12,"e":min(st+1.8,row["End"]),"text":"CONCEPT"})
            elif row["#"] in (15,24,34,45,57,85,91,100,110,121,126):
                bugs.append({"s":st+.12,"e":min(st+1.8,row["End"]),"text":"RECONSTRUCTION"})
        elif typ=="Archive" and row["#"] in (10,23,44,59,72,81,89,99,108,120):
            bugs.append({"s":st+.12,"e":min(st+1.8,row["End"]),"text":"ARCHIVE • PUBLIC DOMAIN"})
    (PUB/"events.json").write_text(json.dumps({"chapters":ch,"bugs":bugs},ensure_ascii=False),encoding="utf-8")

def build_score():
    # Score only for post-V14 portion; first 82.6 s preserves V14 mix.
    dur=END-CUT_START
    sr=48000
    n=int(dur*sr)
    score=WORK/"rest_score.wav"
    chapters=[
      (82.6,.020),(200.7,.026),(307.0,.030),(399.5,.035),(525.5,.028),
      (663.0,.024),(750.2,.030),(822.9,.034),(915.9,.041),(1002.1,.052),
      (1115.4,.029),(1173.4,.024),(1236.5,.000)
    ]
    # stream chunks to keep memory modest
    with wave.open(str(score),"wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        chunk=sr*10
        for i0 in range(0,n,chunk):
            m=min(chunk,n-i0)
            tt=(np.arange(m,dtype=np.float32)+i0)/sr + CUT_START
            xp=np.array([x for x,_ in chapters],dtype=np.float32)
            yp=np.array([y for _,y in chapters],dtype=np.float32)
            env=np.interp(tt,xp,yp).astype(np.float32)
            local=tt-CUT_START
            sig=(.55*np.sin(2*np.pi*46.25*local)+.22*np.sin(2*np.pi*69.375*local+.6)+
                 .08*np.sin(2*np.pi*92.5*local+1.2))*env
            # subtle slow modulation
            sig*=.88+.12*np.sin(2*np.pi*.035*local)
            # chapter impulses
            for tm,_ in chapters[1:-1]:
                rel=tt-tm
                mask=(rel>=0)&(rel<.34)
                if np.any(mask):
                    rr=rel[mask]
                    sig[mask]+=0.040*np.sin(2*np.pi*52*rr)*np.exp(-rr*9)
            pcm=(np.clip(np.tanh(sig*1.05),-.72,.72)*32767).astype(np.int16)
            stereo=np.column_stack([pcm,pcm]).ravel()
            wf.writeframes(stereo.tobytes())
    return score

if __name__=="__main__":
    decisions=build_rest()
    caps=build_captions()
    build_events()
    score=build_score()
    print("FULL_PREP_DONE",len(decisions),len(caps),score)
