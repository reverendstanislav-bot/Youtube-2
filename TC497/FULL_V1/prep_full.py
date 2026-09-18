import csv, json, os, re, subprocess, sys, zipfile
from pathlib import Path
from openpyxl import load_workbook

FPS=30
W,H=1920,1080
TOTAL=1236.506
V14_END=82.600

PKG=Path(os.environ["PKG_ROOT"])
GEN=Path(os.environ["GEN_DIR"])
ARC=PKG/"04_DOWNLOADS"/"ARCHIVE_GREEN"
XLSX=PKG/"03_TIMELINE"/"TC497_FINAL_VISUAL_TIMELINE_CODEX_EDIT_MAP_v2.xlsx"
EXTRA=Path(os.environ["FULL_EXTRA"])
PUBLIC=Path(os.environ["FULL_PUBLIC"])
WORK=Path(os.environ["FULL_WORK"])
SEG=WORK/"segments"
DOCS=WORK/"docs"
for p in [EXTRA,PUBLIC,WORK,SEG,DOCS]: p.mkdir(parents=True,exist_ok=True)

# V14 cold-open grammar, reconstructed at 1080p.
V14=[
(0.000,"INTRO_DETAIL","Generated","INTRO_DETAIL","Mystery detail",""),
(2.120,"INTRO_OBSERVERS","Generated","INTRO_OBSERVERS","Human scale",""),
(6.900,"INTRO_REVEAL","Generated","INTRO_REVEAL","First full reveal",""),
(12.940,"ST-572","Generated","ST-572","572 feet",""),
(17.840,"WB-L06","Generated","WB-L06","13 units",""),
(23.060,"WB-L05","Generated","WB-L05","54 driven wheels",""),
(26.460,"WD-W02","Generated","WD-W02","~150 tons cargo",""),
(33.040,"AR-A01","Archive","AR-A01","Historical proof",""),
(40.500,"WC-R01","Generated","WC-R01","Road ends",""),
(45.352,"WC-R02","Generated","WC-R02","Roadless gap",""),
(48.060,"ST-COLD","Generated","ST-COLD","Named machine",""),
(53.880,"AR-OTTER2","Archive","AR-OTTER2","Project OTTER report","document"),
(57.200,"ST-572","Generated","ST-572","Longest rubber-tired vehicle",""),
(61.080,"WA-09","Generated","WA-09","Technical detail",""),
(64.620,"WB-L03","Generated","WB-L03","Machine buildup",""),
(68.760,"WD-T01","Generated","WD-T01","Yuma test evidence",""),
(71.000,"WC-Y02","Generated","WC-Y02","Dune limitation setup",""),
(74.650,"WD-W01","Generated","WD-W01","IT WORKED",""),
(78.920,"ST-LAST","Generated","ST-LAST","SCRAPPED IT ANYWAY",""),
(80.840,"WD-E05","Generated","WD-E05","Dedicated title plate",""),
(82.600,"END","","","","")
]

def tdsec(v):
    return float(v.total_seconds()) if hasattr(v,"total_seconds") else float(v)

def find_archive(code):
    xs=list(ARC.glob(f"{code}__*"))
    if not xs: raise FileNotFoundError(code)
    return xs[0]

def render_pdf_page(pdf:Path, code:str, page=1):
    out=DOCS/f"{code}_p{page}.png"
    if not out.exists():
        stem=DOCS/f"{code}_p{page}"
        subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-singlefile","-png","-r","150",str(pdf),str(stem)],check=True)
        made=Path(str(stem)+".png")
        if made != out: made.rename(out)
    return out

def source_for(code, source_type, note=""):
    if code.startswith("INTRO_"):
        return EXTRA/f"{code}.png"
    if source_type=="Generated":
        p=GEN/f"{code}.png"
        if p.exists(): return p
        # Some codes might be archived despite registry type mismatch.
        try: return find_archive(code)
        except: pass
    if source_type=="Archive":
        p=find_archive(code)
        if p.suffix.lower()==".pdf":
            page=1
            return render_pdf_page(p,code,page)
        return p
    raise FileNotFoundError(f"{source_type}:{code}")

def sanitize(s):
    return re.sub(r"[^A-Za-z0-9_-]+","_",str(s))[:80]

def vf_for(source_type, code, instruction, duration):
    # Scale with overscan so a single directed pan can be used without black borders.
    if source_type=="Archive":
        base=f"scale=2048:1152:force_original_aspect_ratio=increase,crop=2048:1152"
        grade="eq=saturation=.72:contrast=1.02:brightness=-.025:gamma=.985"
    elif source_type=="Generated":
        base=f"scale=2048:1152:force_original_aspect_ratio=increase,crop=2048:1152"
        grade="eq=saturation=.91:contrast=1.025:brightness=.012:gamma=1.025"
    else:
        base=f"scale=2048:1152:force_original_aspect_ratio=increase,crop=2048:1152"
        grade="eq=saturation=.84:contrast=1.02:brightness=.002:gamma=1.01"

    txt=(instruction or "").lower()
    frames=max(2,int(duration*FPS))
    # One directed movement only. Never wide->tight->wide.
    if any(k in txt for k in ["pan","lateral","crop"]) and source_type!="Archive":
        crop=f"crop={W}:{H}:x='64+64*n/{max(1,frames-1)}':y=36"
    elif any(k in txt for k in ["pan","lateral","crop"]):
        crop=f"crop={W}:{H}:x='96-64*n/{max(1,frames-1)}':y=36"
    else:
        crop=f"crop={W}:{H}:64:36"

    # Gentle paper matte only for documents/patents/reports.
    if code in {"AR-OTTER1","AR-OTTER2","AR-PATENT"}:
        return f"scale=1740:980:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0xB8AD96,eq=saturation=.62:contrast=.99:brightness=-.045:gamma=.96"
    return base+","+crop+","+grade

def render_still(src:Path, source_type, code, instr, dur, out:Path):
    frames=max(2,round(dur*FPS))
    subprocess.run([
        "ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-loop","1","-i",str(src),
        "-vf",vf_for(source_type,code,instr,dur)+",format=yuv420p",
        "-frames:v",str(frames),"-an","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",str(out)
    ],check=True)

def render_xfade(src1, typ1, code1, instr1, src2, typ2, code2, instr2, dur, out):
    # Purposeful two-source composite, not generic split-screen.
    d=max(.18,min(.45,dur*.08))
    half=max(.4,dur/2)
    a=out.with_name(out.stem+"_a.mp4"); b=out.with_name(out.stem+"_b.mp4")
    render_still(src1,typ1,code1,instr1,half+d,a)
    render_still(src2,typ2,code2,instr2,half+d,b)
    fc=f"[0:v]settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration={d:.3f}:offset={half:.3f}[v]"
    subprocess.run([
        "ffmpeg","-y","-loglevel","error","-i",str(a),"-i",str(b),"-filter_complex",fc,
        "-map","[v]","-an","-t",f"{dur:.3f}","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",str(out)
    ],check=True)

# Load canonical timeline.
wb=load_workbook(XLSX,data_only=True)
ws=wb["VISUAL_TIMELINE"]
rows=[]
for r in ws.iter_rows(min_row=5,values_only=True):
    if not r[0]: continue
    n,st,en,dur,chapter,beat,source_type,code,name,locator,rights,instr,overlay,qc=r
    s=tdsec(st); e=tdsec(en)
    rows.append({
        "n":int(n),"s":s,"e":e,"chapter":str(chapter),"beat":str(beat),
        "type":str(source_type),"code":str(code),"name":str(name),
        "locator":str(locator or ""),"rights":str(rights or ""),"instr":str(instr or ""),
        "overlay":str(overlay or "")
    })

# Build physical lookup for composites/graphics: nearest previous/next actual image.
physical=[i for i,x in enumerate(rows) if x["type"] in ("Generated","Archive")]
def nearest_phys(idx, direction):
    j=idx+direction
    while 0<=j<len(rows):
        if rows[j]["type"] in ("Generated","Archive"): return rows[j]
        j+=direction
    return None

states=[]
# Insert exact V14 visual states.
for i in range(len(V14)-1):
    s,code,typ,asset,beat,note=V14[i]
    e=V14[i+1][0]
    states.append({
        "s":s,"e":e,"chapter":"Cold Open","beat":beat,"type":typ,"code":asset,
        "name":beat,"instr":"V14 locked grammar","overlay":"","rights":"approved","timeline_n":0
    })

# Continue canonical map after V14_END, clipping first overlapping state.
for idx,x in enumerate(rows):
    if x["e"]<=V14_END: continue
    y=dict(x)
    y["s"]=max(V14_END,y["s"])
    states.append(y)

# Chapter start markers after Cold Open.
last=None
for st in states:
    st["chapter_start"] = st["chapter"]!=last
    last=st["chapter"]

# Create source-backed video segments.
concat=WORK/"concat.txt"
meta=[]
seq=[]
for i,st in enumerate(states):
    dur=st["e"]-st["s"]
    out=SEG/f"{i:03d}_{sanitize(st['code'])}.mp4"
    if st["type"] in ("Generated","Archive"):
        src=source_for(st["code"],st["type"])
        render_still(src,st["type"],st["code"],st.get("instr",""),dur,out)
        bg_code=st["code"]
    elif st["type"]=="Graphic":
        # Use a meaningful neighboring physical plate under restrained graphic overlay.
        # Prefer previous evidence unless the next plate is the graphic payoff.
        ridx=rows.index(next(r for r in rows if r.get("n")==st.get("n"))) if st.get("n") else None
        prev=nearest_phys(ridx,-1) if ridx is not None else None
        nxt=nearest_phys(ridx,1) if ridx is not None else None
        base=prev or nxt
        src=source_for(base["code"],base["type"])
        render_still(src,base["type"],base["code"],base.get("instr",""),dur,out)
        bg_code=base["code"]
    elif st["type"]=="Composite":
        ridx=rows.index(next(r for r in rows if r.get("n")==st.get("n")))
        prev=nearest_phys(ridx,-1); nxt=nearest_phys(ridx,1)
        if prev and nxt:
            s1=source_for(prev["code"],prev["type"]); s2=source_for(nxt["code"],nxt["type"])
            render_xfade(s1,prev["type"],prev["code"],prev.get("instr",""),s2,nxt["type"],nxt["code"],nxt.get("instr",""),dur,out)
            bg_code=prev["code"]+"→"+nxt["code"]
        else:
            base=prev or nxt
            src=source_for(base["code"],base["type"])
            render_still(src,base["type"],base["code"],base.get("instr",""),dur,out)
            bg_code=base["code"]
    else:
        raise RuntimeError(st)
    seq.append(out)
    mm=dict(st); mm["bg_code"]=bg_code
    meta.append(mm)

concat.write_text("".join(f"file '{p.resolve()}'\n" for p in seq))
subprocess.run([
    "ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),
    "-c","copy",str(PUBLIC/"base.mp4")
],check=True)

# State metadata for Remotion.
(PUBLIC/"states.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

# Full phrase captions from word-level CSV.
word_csv=Path(os.environ["WORD_CSV"])
words=[]
with open(word_csv,encoding="utf-8-sig",newline="") as f:
    for r in csv.DictReader(f):
        s=float(r["start_sec"]); e=float(r["end_sec"])
        if s>=TOTAL: break
        words.append({"s":s,"e":min(e,TOTAL),"w":r["word"]})
phr=[]; buf=[]
for w in words:
    buf.append(w)
    text=" ".join(x["w"] for x in buf)
    span=buf[-1]["e"]-buf[0]["s"]
    punct=bool(re.search(r"[.!?;:]$",w["w"]))
    comma=bool(re.search(r",$",w["w"]))
    if len(buf)>=8 or (punct and len(buf)>=3) or (comma and len(buf)>=5) or span>=2.7:
        phr.append({"s":buf[0]["s"],"e":buf[-1]["e"]+.08,"words":buf})
        buf=[]
if buf: phr.append({"s":buf[0]["s"],"e":buf[-1]["e"]+.08,"words":buf})
(PUBLIC/"captions.json").write_text(json.dumps(phr,ensure_ascii=False),encoding="utf-8")

# Build chapter-specific public-domain synthetic score. Silent during locked V14 audio.
import numpy as np, wave
SR=48000
N=int(TOTAL*SR)
t=np.arange(N,dtype=np.float32)/SR
score=np.zeros(N,dtype=np.float32)
chapters=[
(82.6,200.699,43.0,.013),(200.699,306.965,51.0,.016),(306.965,399.491,47.0,.015),
(399.491,525.453,45.0,.017),(525.453,663.014,49.0,.015),(663.014,750.184,38.0,.013),
(750.184,822.857,46.0,.014),(822.857,915.853,50.0,.016),(915.853,1002.057,54.0,.018),
(1002.057,1115.376,42.0,.020),(1115.376,1173.420,39.0,.011),(1173.420,TOTAL,44.0,.010)
]
for a,b,f,amp in chapters:
    m=(t>=a)&(t<b)
    tt=t[m]-a
    # Industrial low drone + subdued harmonic texture, never melodic foreground.
    env=np.ones_like(tt)
    fadeN=min(len(tt),int(1.2*SR))
    if fadeN>2:
        env[:fadeN]*=np.linspace(0,1,fadeN,dtype=np.float32)
        env[-fadeN:]*=np.linspace(1,0,fadeN,dtype=np.float32)
    sig=(.72*np.sin(2*np.pi*f*tt)+.20*np.sin(2*np.pi*(f*1.5)*tt+.7)+.08*np.sin(2*np.pi*(f*2.0)*tt+1.3))
    score[m]+=amp*env*sig.astype(np.float32)

# Sparse transition impacts at chapter boundaries only.
for a,_,f,_ in chapters[1:]:
    i=int(a*SR); L=min(int(.42*SR),N-i)
    tt=np.arange(L,dtype=np.float32)/SR
    score[i:i+L]+=0.030*np.sin(2*np.pi*(f*.72)*tt)*np.exp(-tt*8.5)

pcm=(np.clip(np.tanh(score*1.12),-.75,.75)*32767).astype(np.int16)
with wave.open(str(PUBLIC/"score.wav"),"wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())

# QA decision sheet.
with open(WORK/"FULL_EDIT_DECISIONS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["idx","start","end","chapter","source_type","asset_code","background","beat","instruction"])
    for i,x in enumerate(meta):
        w.writerow([i,f"{x['s']:.3f}",f"{x['e']:.3f}",x["chapter"],x["type"],x["code"],x["bg_code"],x["beat"],x.get("instr","")])

print("FULL_PREP_DONE",len(meta),meta[-1]["e"])
