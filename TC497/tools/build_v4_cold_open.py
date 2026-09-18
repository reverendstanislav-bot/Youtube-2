import os, glob, subprocess, csv, re
from pathlib import Path

ROOT=Path.cwd()
GEN=ROOT/'12_#U0413#U0435#U043d#U0435#U0440#U0430#U0446#U0438#U0438'/'FINAL_62'
ARC=ROOT/'04_DOWNLOADS'/'ARCHIVE_GREEN'
VO=ROOT/'01_AUDIO'/'TC497_FINAL_VO.mp3'
TRANSCRIPT=Path(os.environ['TC497_TRANSCRIPT_DIR'])
WORK=ROOT/'_EDIT_WORK'/'V4_COLD_OPEN'
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

# Explicit editorial decision list. Start times follow VO meaning, not equal shot lengths.
# mode: full / left / center / right / pan_l / pan_r / tight
SHOTS=[
(0.000,'ST-COLD','full',''),
(1.860,'ST-COLD','left',''),
(2.920,'WB-C02','left',''),
(4.920,'WB-C02','right',''),
(6.900,'WB-C03','full',''),
(8.240,'WB-C03','right',''),
(10.040,'WB-C01','full',''),
(12.200,'WB-C01','left',''),
(12.940,'ST-572','full','572 FEET'),
(15.340,'WB-L02','pan_r',''),
(16.000,'WB-L02','full','13 UNITS'),
(17.840,'WB-L06','left',''),
(19.460,'WB-L06','center',''),
(21.260,'WB-L06','right',''),
(23.060,'WA-09','tight','54 DRIVEN WHEELS'),
(25.000,'WA-09','right',''),
(26.460,'WD-W02','left','6 CREW'),
(28.140,'WD-W02','center',''),
(29.540,'WD-W02','right','~150 TONS'),
(32.000,'WD-W03','full',''),
(33.040,'AR-A01','full','ARCHIVE'),
(34.480,'AR-A01','left',''),
(36.040,'AR-A01','tight','NO RAILROAD'),
(37.420,'AR-A01','center','NO RAILS'),
(38.800,'AR-A01','right','NO PREPARED HIGHWAY'),
(40.500,'WB-C05','full',''),
(41.300,'WB-C05','left',''),
(43.200,'WB-C05','right',''),
(45.352,'WB-C01','full',''),
(48.060,'ST-COLD','full','TC-497 OVERLAND TRAIN MARK II'),
(50.300,'ST-COLD','tight',''),
(53.880,'AR-A01','full','ARCHIVE'),
(54.580,'AR-A01','center',''),
(57.200,'ST-572','full','LONGEST RUBBER-TIRED VEHICLE'),
(60.380,'WB-C02','tight',''),
(61.080,'WB-C02','left',''),
(63.840,'WB-C04','full',''),
(64.620,'WB-C04','right',''),
(66.480,'WB-C04','left',''),
(68.760,'WD-T01','full',''),
(70.880,'WC-Y01','center',''),
(71.480,'WC-Y01','tight',''),
(74.260,'WD-W01','full',''),
(74.980,'WD-W01','center','IT WORKED'),
(78.360,'WD-E02','full',''),
(78.920,'WD-E02','tight',''),
(80.840,'ST-COLD','full','TITLE'),
(82.600,'ST-COLD','full','END')
]

def crop_filter(mode):
    # Fixed 1440x810 canvas; no zoompan. Pans move only a crop window and are used rarely.
    base="scale=1440:810:force_original_aspect_ratio=increase,crop=1440:810"
    grade=",eq=saturation=0.86:contrast=1.035:brightness=-0.01"
    if mode=='full': return base+",crop=960:540:240:135"+grade
    if mode=='left': return base+",crop=960:540:65:135"+grade
    if mode=='center': return base+",crop=960:540:240:135"+grade
    if mode=='right': return base+",crop=960:540:415:135"+grade
    if mode=='tight': return base+",scale=1728:972,crop=960:540:384:216"+grade
    return base+",crop=960:540:240:135"+grade

concat=WORK/'concat.txt'
rows=[]
with open(concat,'w') as lf:
    for i,(st,code,mode,overlay) in enumerate(SHOTS[:-1]):
        nxt=SHOTS[i+1][0]
        dur=nxt-st
        frames=max(1,round(dur*FPS))
        out=SEG/f'{i+1:03d}.mp4'
        vf=crop_filter(mode)+",format=yuv420p"
        subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-loop','1','-i',str(asset(code)),
                        '-vf',vf,'-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(out)],check=True)
        lf.write(f"file '{out.resolve()}'\n")
        rows.append([i+1,st,nxt,code,mode,overlay])

silent=WORK/'picture.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)],check=True)

# Phrase-level captions from word-level transcript: 3-5 words, punctuation-aware.
word_csv=TRANSCRIPT/'TC497_VO_WORD_LEVEL.csv'
words=[]
with open(word_csv,encoding='utf-8-sig',newline='') as f:
    rd=csv.DictReader(f)
    for r in rd:
        s=float(r['start_sec']); e=float(r['end_sec'])
        if s>=DUR: break
        words.append((s,min(e,DUR),r['word']))

phrases=[]
buf=[]
for w in words:
    buf.append(w)
    punct=bool(re.search(r'[,.!?;:]$',w[2]))
    span=buf[-1][1]-buf[0][0]
    if len(buf)>=4 or punct or span>=1.8:
        phrases.append((buf[0][0],buf[-1][1],' '.join(x[2] for x in buf)))
        buf=[]
if buf: phrases.append((buf[0][0],buf[-1][1],' '.join(x[2] for x in buf)))

def ats(t):
    h=int(t//3600); t-=h*3600; m=int(t//60); t-=m*60
    return f'{h}:{m:02d}:{t:05.2f}'

# Brand colors in ASS BGR.
RUST='&H003552A5&'
IVORY='&H00DDEBF3&'
PAPER='&H00C8DDE6&'

def highlight(text):
    keys=['572','13','54','150','no railroad','no rails','no prepared highway','actually work','scrapped']
    out=text
    for k in keys:
        out=re.sub(re.escape(k),r'{\\c'+RUST+r'}'+k+r'{\\c'+PAPER+r'}',out,flags=re.I)
    return out

ass=WORK/'v4.ass'
with open(ass,'w',encoding='utf-8') as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 0
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,DejaVu Sans,27,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,0,0,1,3,0,2,68,68,30,1
Style: Metric,DejaVu Sans,31,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H30171A1C,-1,0,0,0,100,100,1,0,1,3,0,7,36,36,36,1
Style: Bug,DejaVu Sans,13,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,0,0,0,0,100,100,1,0,1,2,0,9,24,24,22,1
Style: Title,DejaVu Sans,34,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,60,60,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    # captions
    for s,e,t in phrases:
        if e-s<0.22: e=s+0.22
        f.write(f"Dialogue: 4,{ats(s)},{ats(e+0.10)},Sub,,0,0,0,,{highlight(t)}\n")
    # reconstruction/archive provenance bugs by actual shot interval
    for i,(st,code,mode,overlay) in enumerate(SHOTS[:-1]):
        en=SHOTS[i+1][0]
        if code.startswith('AR-'):
            bug='ARCHIVE • U.S. ARMY / YUMA'
        else:
            bug='RECONSTRUCTION'
        f.write(f"Dialogue: 2,{ats(st)},{ats(en)},Bug,,0,0,0,,{bug}\n")
    # editorial fact beats; keep text short and on existing imagery
    for i,(st,code,mode,overlay) in enumerate(SHOTS[:-1]):
        en=SHOTS[i+1][0]
        if overlay in ('','ARCHIVE','TITLE'): continue
        txt=overlay.replace('TC-497 OVERLAND TRAIN MARK II','TC-497 OVERLAND TRAIN • MARK II')
        f.write(f"Dialogue: 3,{ats(st)},{ats(min(en,st+2.2))},Metric,,0,0,0,,{txt}\n")
    f.write(f"Dialogue: 6,{ats(80.840)},{ats(82.600)},Title,,0,0,0,,AMERICA BUILT A 572-FOOT TRAIN\\NTHAT NEEDED NO TRACKS\n")

# Minimal cut punctuation: 5 low hits only. No continuous synthetic bed.
SFX=WORK/'sfx.wav'
hits=[(12.94,52),(23.06,58),(36.04,48),(74.98,55),(80.84,45)]
filters=[]
for j,(t,freq) in enumerate(hits):
    ms=int(t*1000)
    filters.append(f"sine=frequency={freq}:duration=0.22,volume=0.08,afade=t=out:st=0.03:d=0.19,adelay={ms}|{ms}[h{j}]")
mix=''.join(f'[h{i}]' for i in range(len(hits)))
filters.append(f"{mix}amix=inputs={len(hits)}:normalize=0,alimiter=limit=0.25[sfx]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-filter_complex',';'.join(filters),'-map','[sfx]','-t',str(DUR),str(SFX)],check=True)

FINAL=ROOT/'_V2'/'TC497_V4_COLD_OPEN_82S.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(VO),'-i',str(SFX),
               '-filter_complex',f"[0:v]ass={ass}[v];[1:a]atrim=0:{DUR},asetpts=PTS-STARTPTS[vo];[2:a]volume=0.75[s];[vo][s]amix=inputs=2:normalize=0,alimiter=limit=0.94[a]",
               '-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k',
               '-t',str(DUR),'-movflags','+faststart',str(FINAL)],check=True)

with open(WORK/'V4_EDIT_DECISIONS.csv','w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['shot','start','end','asset','framing','overlay']); w.writerows(rows)
print(FINAL)
print(FINAL.stat().st_size)
