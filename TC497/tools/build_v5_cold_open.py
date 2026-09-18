import os, glob, subprocess, csv, re
from pathlib import Path

ROOT=Path.cwd()
GEN=ROOT/'12_#U0413#U0435#U043d#U0435#U0440#U0430#U0446#U0438#U0438'/'FINAL_62'
ARC=ROOT/'04_DOWNLOADS'/'ARCHIVE_GREEN'
VO=ROOT/'01_AUDIO'/'TC497_FINAL_VO.mp3'
TRANSCRIPT=Path(os.environ['TC497_TRANSCRIPT_DIR'])
WORK=ROOT/'_EDIT_WORK'/'V5_COLD_OPEN'
SEG=WORK/'segments'
WORK.mkdir(parents=True,exist_ok=True); SEG.mkdir(exist_ok=True)
W,H,FPS=960,540,30
DUR=82.600

def asset(code):
    p=GEN/f'{code}.png'
    if p.exists(): return p
    xs=glob.glob(str(ARC/f'{code}__*'))
    if xs: return Path(xs[0])
    raise FileNotFoundError(code)

# Balanced rhythm: 25 shots / 82.6s. Most holds 3–5s.
# transition belongs to the boundary AFTER this shot: cut or dissolve.
SHOTS=[
(0.000,'ST-COLD','full','','cut'),
(3.900,'WB-C02','left','','dissolve'),
(7.800,'WB-C03','full','','cut'),
(12.940,'ST-572','full','572 FEET','dissolve'),
(17.840,'WB-L06','pan_r','13 UNITS','cut'),
(23.060,'WA-09','tight','54 DRIVEN WHEELS','dissolve'),
(26.460,'WD-W02','center','6 CREW  •  ~150 TONS','cut'),
(33.040,'AR-A01','full','','dissolve'),
(36.040,'AR-A01','left','NO RAILROAD','cut'),
(37.420,'AR-A01','center','NO RAILS','cut'),
(38.800,'AR-A01','right','NO PREPARED HIGHWAY','cut'),
(40.500,'WB-C05','full','','dissolve'),
(45.352,'WB-C01','full','','cut'),
(48.060,'ST-COLD','full','TC-497 OVERLAND TRAIN • MARK II','dissolve'),
(53.880,'AR-A01','center','','cut'),
(57.200,'ST-572','full','LONGEST RUBBER-TIRED VEHICLE','dissolve'),
(61.080,'WB-C02','tight','','cut'),
(64.620,'WB-C04','full','','dissolve'),
(68.760,'WD-T01','full','','cut'),
(71.480,'WC-Y01','center','','cut'),
(74.980,'WD-W01','full','IT WORKED','dissolve'),
(78.920,'WD-E02','full','','cut'),
(80.840,'ST-COLD','full','TITLE','cut'),
(82.600,'ST-COLD','full','END','cut')
]

def crop_filter(mode):
    base="scale=1440:810:force_original_aspect_ratio=increase,crop=1440:810"
    grade=",eq=saturation=0.86:contrast=1.035:brightness=-0.01"
    if mode=='full': return base+",crop=960:540:240:135"+grade
    if mode=='left': return base+",crop=960:540:65:135"+grade
    if mode=='center': return base+",crop=960:540:240:135"+grade
    if mode=='right': return base+",crop=960:540:415:135"+grade
    if mode=='tight': return base+",scale=1728:972,crop=960:540:384:216"+grade
    if mode=='pan_r': return base+",crop=960:540:x='120+240*n/150':y=135"+grade
    return base+",crop=960:540:240:135"+grade

# Render source clips. Dissolve boundaries get 0.16s transition clips replacing
# 0.08s from each neighbor, so total duration stays unchanged.
TD=0.16
sequence=[]
rows=[]
for i,(st,code,mode,overlay,tr) in enumerate(SHOTS[:-1]):
    en=SHOTS[i+1][0]
    in_trim=TD/2 if i>0 and SHOTS[i-1][4]=='dissolve' else 0
    out_trim=TD/2 if tr=='dissolve' else 0
    body_st=st+in_trim
    body_en=en-out_trim
    body_d=max(0.05,body_en-body_st)
    out=SEG/f'{i+1:03d}_body.mp4'
    frames=max(1,round(body_d*FPS))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(asset(code)),
                    '-vf',crop_filter(mode)+",format=yuv420p",'-frames:v',str(frames),'-an',
                    '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(out)],check=True)
    sequence.append(out)
    rows.append([i+1,st,en,code,mode,overlay,tr])
    if tr=='dissolve':
        ncode=SHOTS[i+1][1]; nmode=SHOTS[i+1][2]
        a=SEG/f'{i+1:03d}_ta.mp4'; b=SEG/f'{i+1:03d}_tb.mp4'; x=SEG/f'{i+1:03d}_xfade.mp4'
        nframes=max(2,round(TD*FPS))
        for src,mo,dst in [(code,mode,a),(ncode,nmode,b)]:
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(asset(src)),
                            '-vf',crop_filter(mo)+",format=yuv420p",'-frames:v',str(nframes),'-an',
                            '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(dst)],check=True)
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(a),'-i',str(b),
                        '-filter_complex',f"[0:v]settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration={TD}:offset=0[v]",
                        '-map','[v]','-an','-t',str(TD),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(x)],check=True)
        sequence.append(x)

concat=WORK/'concat.txt'
with open(concat,'w') as f:
    for p in sequence:
        f.write(f"file '{p.resolve()}'\n")
picture=WORK/'picture.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(picture)],check=True)

# Calmer captions: 5–7 words, punctuation-aware, fewer visual updates.
word_csv=TRANSCRIPT/'TC497_VO_WORD_LEVEL.csv'
words=[]
with open(word_csv,encoding='utf-8-sig',newline='') as f:
    rd=csv.DictReader(f)
    for r in rd:
        s=float(r['start_sec']); e=float(r['end_sec'])
        if s>=DUR: break
        words.append((s,min(e,DUR),r['word']))

phrases=[]; buf=[]
for w in words:
    buf.append(w)
    punct=bool(re.search(r'[.!?;:]$',w[2]))
    comma=bool(re.search(r',$',w[2]))
    span=buf[-1][1]-buf[0][0]
    if len(buf)>=7 or (punct and len(buf)>=3) or (comma and len(buf)>=5) or span>=2.5:
        phrases.append((buf[0][0],buf[-1][1],' '.join(x[2] for x in buf)))
        buf=[]
if buf: phrases.append((buf[0][0],buf[-1][1],' '.join(x[2] for x in buf)))

def ats(t):
    h=int(t//3600); t-=h*3600; m=int(t//60); t-=m*60
    return f'{h}:{m:02d}:{t:05.2f}'

RUST='&H003552A5&'; PAPER='&H00C8DDE6&'
def highlight(text):
    out=text
    for k in ['572','13','54','150','no railroad','no rails','no prepared highway','actually work','scrapped']:
        out=re.sub(re.escape(k),r'{\\c'+RUST+r'}'+k+r'{\\c'+PAPER+r'}',out,flags=re.I)
    return out

ass=WORK/'v5.ass'
with open(ass,'w',encoding='utf-8') as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,DejaVu Sans,26,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,0,0,1,3,0,2,74,74,30,1
Style: Metric,DejaVu Sans,29,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H30171A1C,-1,0,0,0,100,100,1,0,1,3,0,7,36,36,36,1
Style: Bug,DejaVu Sans,12,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,0,0,0,0,100,100,1,0,1,2,0,9,24,24,22,1
Style: Title,DejaVu Sans,34,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,60,60,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for s,e,t in phrases:
        f.write(f"Dialogue: 4,{ats(s)},{ats(e+0.12)},Sub,,0,0,0,,{highlight(t)}\n")
    # Provenance only on first entry into each type sequence, not every shot.
    f.write(f"Dialogue: 2,{ats(0.0)},{ats(2.6)},Bug,,0,0,0,,RECONSTRUCTION\n")
    f.write(f"Dialogue: 2,{ats(33.04)},{ats(35.7)},Bug,,0,0,0,,ARCHIVE • U.S. ARMY / YUMA\n")
    f.write(f"Dialogue: 2,{ats(40.50)},{ats(43.1)},Bug,,0,0,0,,RECONSTRUCTION\n")
    f.write(f"Dialogue: 2,{ats(53.88)},{ats(56.5)},Bug,,0,0,0,,ARCHIVE • U.S. ARMY / YUMA\n")
    f.write(f"Dialogue: 2,{ats(57.20)},{ats(59.8)},Bug,,0,0,0,,RECONSTRUCTION\n")
    for i,(st,code,mode,overlay,tr) in enumerate(SHOTS[:-1]):
        en=SHOTS[i+1][0]
        if overlay in ('','TITLE'): continue
        f.write(f"Dialogue: 3,{ats(st)},{ats(min(en,st+2.4))},Metric,,0,0,0,,{overlay}\n")
    f.write(f"Dialogue: 6,{ats(80.840)},{ats(82.600)},Title,,0,0,0,,AMERICA BUILT A 572-FOOT TRAIN\\NTHAT NEEDED NO TRACKS\n")

# Fewer sound accents; no hit on every information beat.
SFX=WORK/'sfx.wav'
hits=[(12.94,52),(36.04,48),(74.98,55),(80.84,45)]
filters=[]
for j,(t,freq) in enumerate(hits):
    ms=int(t*1000)
    filters.append(f"sine=frequency={freq}:duration=0.24,volume=0.065,afade=t=out:st=0.03:d=0.21,adelay={ms}|{ms}[h{j}]")
mix=''.join(f'[h{i}]' for i in range(len(hits)))
filters.append(f"{mix}amix=inputs={len(hits)}:normalize=0,alimiter=limit=0.22[sfx]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-filter_complex',';'.join(filters),'-map','[sfx]','-t',str(DUR),str(SFX)],check=True)

FINAL=ROOT/'_V2'/'TC497_V5_COLD_OPEN_82S.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(picture),'-i',str(VO),'-i',str(SFX),
               '-filter_complex',f"[0:v]ass={ass}[v];[1:a]atrim=0:{DUR},asetpts=PTS-STARTPTS[vo];[2:a]volume=0.70[s];[vo][s]amix=inputs=2:normalize=0,alimiter=limit=0.94[a]",
               '-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k',
               '-t',str(DUR),'-movflags','+faststart',str(FINAL)],check=True)

with open(WORK/'V5_EDIT_DECISIONS.csv','w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['shot','start','end','asset','framing','overlay','out_transition']); w.writerows(rows)
print(FINAL)
print(FINAL.stat().st_size)
