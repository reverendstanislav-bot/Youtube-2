import csv, glob, subprocess, re, wave, os
from pathlib import Path
import numpy as np

ROOT=Path.cwd()
GEN=Path(os.environ["GEN_DIR"])
ARC=ROOT/"04_DOWNLOADS"/"ARCHIVE_GREEN"
VO=ROOT/"01_AUDIO"/"TC497_FINAL_VO.mp3"
TR=Path(os.environ["TC497_TRANSCRIPT_DIR"])
WORK=ROOT/"_EDIT_WORK"/"V9_COLD_OPEN"; SEG=WORK/"segments"
WORK.mkdir(parents=True,exist_ok=True); SEG.mkdir(exist_ok=True)
FPS=30; DUR=82.6

def asset(code):
    p=GEN/f"{code}.png"
    if p.exists(): return p
    xs=glob.glob(str(ARC/f"{code}__*"))
    if xs: return Path(xs[0])
    raise FileNotFoundError(code)

# V9: surgical fixes only. Base rhythm inherited from V8/V7.
SHOTS=[
(0.000,"ST-COLD","full","recon","","cut"),
(3.900,"WB-C02","left","recon","","dissolve"),
(7.800,"WB-C03","full","recon","","cut"),
(12.940,"ST-572","full","recon","572 FEET","dissolve"),
(17.840,"WB-L06","pan_r","recon","13 UNITS","cut"),
(23.060,"WB-L06","tight","recon","54 DRIVEN WHEELS","cut"),
(26.460,"WD-W02","center","recon","~150 TONS","dissolve"),
(33.040,"AR-A01","full","archive","","cut"),
(36.040,"AR-A01","left","archive","NO RAILROAD","cut"),
(37.420,"AR-A01","center","archive","NO RAILS","cut"),
(38.800,"AR-A01","right","archive","NO PREPARED HIGHWAY","dissolve"),
(40.500,"WB-C04","full","recon","","dissolve"),
(45.352,"WB-C01","full","recon","","cut"),
(48.060,"ST-COLD","full","recon","TC-497 OVERLAND TRAIN • MARK II","dissolve"),
(53.880,"AR-A01","center","archive","","dissolve"),
(57.200,"ST-572","full","recon","LONGEST RUBBER-TIRED VEHICLE","cut"),
(61.080,"WB-C02","tight","recon","","cut"),
(64.620,"WB-L06","tight","recon","","cut"),
(68.760,"WD-T01","full","recon","","cut"),
(71.480,"WC-Y02","center","recon","","cut"),
(74.980,"WD-W01","full","recon","IT WORKED","fadeblack"),
(78.920,"ST-LAST","full","last","SCRAPPED IT ANYWAY","fadeblack"),
(80.840,"ST-COLD","full","title","TITLE","cut"),
(82.600,"ST-COLD","full","title","END","cut")
]

# Only visual-language bridges get dissolves.
TD={2:(0.12,"fade"),4:(0.14,"fade"),7:(0.10,"fade"),11:(0.12,"fade"),
    12:(0.12,"fade"),14:(0.12,"fade"),15:(0.12,"fade"),21:(0.14,"fadeblack"),
    22:(0.12,"fadeblack")}

def vf(mode,kind):
    base="scale=1440:810:force_original_aspect_ratio=increase,crop=1440:810"
    if mode=="full": crop="crop=960:540:240:135"
    elif mode=="left": crop="crop=960:540:65:135"
    elif mode=="right": crop="crop=960:540:415:135"
    elif mode=="center": crop="crop=960:540:240:135"
    elif mode=="tight":
        return base+",scale=1728:972,crop=960:540:384:216,eq=saturation=0.82:contrast=1.04:brightness=-0.01"
    elif mode=="pan_r": crop="crop=960:540:x='120+240*n/150':y=135"
    else: crop="crop=960:540:240:135"
    if kind=="archive":
        # Deliberately archival, not disguised reconstruction: monochrome image on warm-paper matte.
        return base+","+crop+",hue=s=0.18,eq=contrast=1.09:brightness=-0.025:gamma=0.98,scale=900:506,pad=960:540:30:17:color=0xE6DDC8"
    if kind=="last": grade="eq=saturation=0.62:contrast=1.08:brightness=-0.06,vignette=PI/11"
    elif kind=="title": grade="eq=saturation=0.56:contrast=1.06:brightness=-0.15,vignette=PI/9"
    else: grade="eq=saturation=0.84:contrast=1.04:brightness=-0.012"
    return base+","+crop+","+grade

def render(code,mode,kind,dur,out):
    frames=max(2,round(dur*FPS))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-loop","1","-i",str(asset(code)),
                    "-vf",vf(mode,kind)+",format=yuv420p","-frames:v",str(frames),"-an",
                    "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",str(out)],check=True)

seq=[]; decisions=[]
for i,s in enumerate(SHOTS[:-1]):
    st,code,mode,kind,ov,tr=s; en=SHOTS[i+1][0]; n=i+1
    pin=TD.get(n-1,(0,""))[0] if n>1 else 0; pout=TD.get(n,(0,""))[0]
    body=max(.08,(en-st)-pin/2-pout/2)
    bo=SEG/f"{n:03d}_body.mp4"; render(code,mode,kind,body,bo); seq.append(bo)
    decisions.append([n,st,en,code,mode,kind,ov,TD.get(n,(0,"cut"))[1]])
    if n in TD and i+1<len(SHOTS)-1:
        td,tn=TD[n]; ns=SHOTS[i+1]
        a=SEG/f"{n:03d}_a.mp4"; b=SEG/f"{n:03d}_b.mp4"; x=SEG/f"{n:03d}_x.mp4"
        render(code,mode,kind,td,a); render(ns[1],ns[2],ns[3],td,b)
        fc=f"[0:v]settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]xfade=transition={tn}:duration={td}:offset=0[v]"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(a),"-i",str(b),"-filter_complex",fc,
                        "-map","[v]","-an","-t",str(td),"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",str(x)],check=True)
        seq.append(x)

concat=WORK/"concat.txt"
concat.write_text("".join(f"file '{p.resolve()}'\n" for p in seq))
picture=WORK/"picture.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(picture)],check=True)

# Calm phrase captions, with hero / rapid-spec windows protected from clutter.
words=[]
with open(TR/"TC497_VO_WORD_LEVEL.csv",encoding="utf-8-sig",newline="") as f:
    for r in csv.DictReader(f):
        s=float(r["start_sec"]); e=float(r["end_sec"])
        if s>=DUR: break
        words.append((s,min(e,DUR),r["word"]))
phr=[]; buf=[]
for w in words:
    buf.append(w); punct=bool(re.search(r"[.!?;:]$",w[2])); comma=bool(re.search(r",$",w[2]))
    if len(buf)>=7 or (punct and len(buf)>=3) or (comma and len(buf)>=5) or buf[-1][1]-buf[0][0]>=2.5:
        phr.append((buf[0][0],buf[-1][1]," ".join(x[2] for x in buf))); buf=[]
if buf: phr.append((buf[0][0],buf[-1][1]," ".join(x[2] for x in buf)))

def ts(x):
    h=int(x//3600); x-=h*3600; m=int(x//60); x-=m*60
    return f"{h}:{m:02d}:{x:05.2f}"
R="&H003552A5&"; P="&H00C8DDE6&"
def hi(txt):
    for k in ["572","54","150","actually work","scrapped"]:
        txt=re.sub(re.escape(k),lambda m:"{\\c"+R+"}"+m.group(0)+"{\\c"+P+"}",txt,flags=re.I)
    return txt

ass=WORK/"v9.ass"
with open(ass,"w",encoding="utf-8") as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,DejaVu Sans,26,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,0,0,1,3,0,2,74,74,30,1
Style: Metric,DejaVu Sans,28,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H30171A1C,-1,0,0,0,100,100,1,0,1,3,0,7,36,36,36,1
Style: Micro,DejaVu Sans,14,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H30171A1C,0,0,0,0,100,100,1,0,1,1,0,7,36,36,38,1
Style: Bug,DejaVu Sans,12,&H00363A30,&H00363A30,&H00E6DDC8,&H00000000,0,0,0,0,100,100,1,0,1,1,0,9,34,34,26,1
Style: Hero,DejaVu Sans,38,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H40171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,52,52,0,1
Style: HeroRust,DejaVu Sans,38,&H003552A5,&H003552A5,&H00171A1C,&H30171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,52,52,0,1
Style: Title,DejaVu Sans,34,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,60,60,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    blocked=[(12.9,15.7),(22.9,26.6),(35.9,40.6),(74.8,82.6)]
    for s,e,t in phr:
        if any(s<b and e>a for a,b in blocked): continue
        f.write(f"Dialogue: 5,{ts(s)},{ts(e+.12)},Sub,,0,0,0,,{{\\fad(55,75)}}{hi(t)}\n")
    # Intentional archive treatment + source label.
    for a,b in [(33.04,40.50),(53.88,57.20)]:
        f.write(f"Dialogue: 3,{ts(a+.12)},{ts(min(b,a+2.6))},Bug,,0,0,0,,{{\\fad(100,140)}}ARCHIVE • U.S. ARMY / YUMA\n")
    # Specs: hierarchy instead of spec-sheet parity.
    f.write(f"Dialogue: 7,{ts(13.28)},{ts(15.55)},HeroRust,,0,0,0,,{{\\fad(130,170)}}572 FEET\n")
    f.write(f"Dialogue: 4,{ts(18.15)},{ts(20.20)},Micro,,0,0,0,,{{\\fad(100,130)}}13 UNITS\n")
    f.write(f"Dialogue: 4,{ts(23.25)},{ts(25.60)},Micro,,0,0,0,,{{\\fad(100,130)}}54 DRIVEN WHEELS\n")
    f.write(f"Dialogue: 4,{ts(28.70)},{ts(31.10)},Metric,,0,0,0,,{{\\fad(100,140)}}~150 TONS\n")
    for st,txt in [(36.04,"NO RAILROAD"),(37.42,"NO RAILS"),(38.80,"NO PREPARED HIGHWAY")]:
        f.write(f"Dialogue: 4,{ts(st)},{ts(st+1.15)},Metric,,0,0,0,,{txt}\n")
    f.write(f"Dialogue: 4,{ts(48.25)},{ts(50.50)},Micro,,0,0,0,,{{\\fad(100,130)}}TC-497 OVERLAND TRAIN • MARK II\n")
    f.write(f"Dialogue: 4,{ts(57.35)},{ts(59.70)},Micro,,0,0,0,,{{\\fad(100,130)}}LONGEST RUBBER-TIRED VEHICLE\n")
    # Payoff hierarchy.
    f.write(f"Dialogue: 7,{ts(75.15)},{ts(77.60)},Hero,,0,0,0,,{{\\fad(130,220)}}IT WORKED.\n")
    f.write(f"Dialogue: 8,{ts(79.02)},{ts(80.66)},HeroRust,,0,0,0,,{{\\fad(120,170)}}SCRAPPED IT ANYWAY.\n")
    f.write(f"Dialogue: 9,{ts(80.94)},{ts(82.56)},Title,,0,0,0,,{{\\fad(120,180)}}AMERICA BUILT A 572-FOOT TRAIN\\NTHAT NEEDED NO TRACKS\n")

# Low procedural industrial bed. Payoff drops before returning for title.
SR=48000; N=int(DUR*SR); t=np.arange(N,dtype=np.float32)/SR
xp=np.array([0,6,13,23,33,40.5,48,57,64.6,68.8,71.5,74.8,75.4,77.6,78.9,80.5,80.84,82.6],np.float32)
yp=np.array([.012,.024,.038,.045,.032,.040,.050,.044,.050,.058,.068,.076,.026,.009,.007,.012,.065,.022],np.float32)
env=np.interp(t,xp,yp).astype(np.float32)
m=(.55*np.sin(2*np.pi*46.25*t)+.23*np.sin(2*np.pi*69.375*t+.4)+.08*np.sin(2*np.pi*92.5*t+1.1)).astype(np.float32)*env
for tm,amp,fq in [(12.94,.050,52),(23.06,.028,60),(74.98,.060,56),(78.92,.085,44),(80.84,.065,50)]:
    i=int(tm*SR); L=min(int(.34*SR),N-i); tt=np.arange(L,dtype=np.float32)/SR
    m[i:i+L]+=amp*np.sin(2*np.pi*fq*tt)*np.exp(-tt*10)
pcm=(np.clip(np.tanh(m*1.08),-.82,.82)*32767).astype(np.int16)
score=WORK/"score.wav"
with wave.open(str(score),"wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())

final=ROOT/"_V2"/"TC497_V9_COLD_OPEN_RETENTION_POLISH.mp4"
fc=f"[0:v]ass={ass}[v];[1:a]atrim=0:{DUR},asetpts=PTS-STARTPTS[vo];[2:a]highpass=f=35,lowpass=f=3200,volume=.32[mu];[vo][mu]amix=inputs=2:normalize=0,alimiter=limit=.94[a]"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(picture),"-i",str(VO),"-i",str(score),
                "-filter_complex",fc,"-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","20",
                "-c:a","aac","-b:a","192k","-t",str(DUR),"-movflags","+faststart",str(final)],check=True)

with open(WORK/"V9_EDIT_DECISIONS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["shot","start","end","asset","framing","treatment","overlay","transition"]); w.writerows(decisions)
(WORK/"V9_CHANGELOG.txt").write_text("""V9 SURGICAL RETENTION PASS
1) 12.94–32.00: spec hierarchy simplified. 572 FT is hero; 13 UNITS and 54 WHEELS are micro; only ~150 TONS remains metric weight.
2) 23.06–26.46: technical-card aesthetic removed. Same machine source is reframed tightly onto wheels.
3) 40.50–45.35: red variant removed; TC-497 desert plate substituted.
4) 64.62–74.98: buildup rebuilt as detail -> test evidence -> terrain/problem -> full-machine payoff.
5) 74.98–82.60: IT WORKED -> darker ST-LAST SCRAPPED beat -> dedicated title space.
Archive is intentionally archival via warm-paper matte and source bug; it is no longer disguised as reconstruction.
No new generations. No shake. No split-screen. Base V8 rhythm preserved.
""")
print(final, final.stat().st_size)
