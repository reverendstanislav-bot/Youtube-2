import os, glob, subprocess, csv, re
from pathlib import Path

ROOT=Path.cwd()
GEN=ROOT/'12_#U0413#U0435#U043d#U0435#U0440#U0430#U0446#U0438#U0438'/'FINAL_62'
ARC=ROOT/'04_DOWNLOADS'/'ARCHIVE_GREEN'
WORK=ROOT/'_EDIT_WORK'/'V3_PROOF'
SEG=WORK/'segments'
WORK.mkdir(parents=True,exist_ok=True)
SEG.mkdir(exist_ok=True)
VO=ROOT/'01_AUDIO'/'TC497_FINAL_VO.mp3'
TRANSCRIPT=Path(os.environ['TC497_TRANSCRIPT_DIR'])
DUR=90.792
W,H,FPS=960,540,30

def asset(code):
    p=GEN/f'{code}.png'
    if p.exists(): return p
    xs=glob.glob(str(ARC/f'{code}__*'))
    if xs: return Path(xs[0])
    raise FileNotFoundError(code)

shots=[
(0.000,2.920,'ST-COLD','static','Opening desert reveal'),
(2.920,6.340,'WB-C02','detail_left','Less like a truck'),
(6.900,10.040,'WB-C03','pan_r','Entire transportation system'),
(10.040,12.200,'WD-W01','static','Moving under own power'),
(12.940,15.340,'ST-572','static','572 feet'),
(15.340,17.360,'WB-L02','pan_r','13 units'),
(17.840,22.140,'WB-L06','pan_l','Control/cargo/power sections'),
(23.060,25.860,'WA-09','detail_center','54 driven wheels'),
(26.460,28.100,'WD-W02','detail_left','Crew of six'),
(28.100,32.000,'WD-W02','pan_r','150 tons cargo'),
(33.040,35.680,'AR-A01','static','Overland Train archive'),
(36.040,37.420,'AR-A01','detail_left','No railroad'),
(37.420,38.800,'AR-A01','detail_center','No rails'),
(38.800,40.500,'AR-A01','detail_right','No prepared highway'),
(41.300,47.300,'WB-C05','pan_l','Infrastructure ends'),
(48.060,53.880,'ST-COLD','static','TC-497 identification'),
(54.580,57.200,'WB-C03','pan_r','Army described it'),
(57.200,60.380,'ST-572','static','Longest rubber-tired vehicle'),
(61.080,63.840,'WB-C02','detail_center','But size is not strangest'),
(64.620,68.360,'WB-C04','pan_r','Army took it into desert'),
(68.760,71.480,'WD-T01','static','Testing setup'),
(71.480,74.260,'WC-Y01','detail_center','Disappearance question'),
(74.980,78.360,'WD-W01','pan_r','It actually worked'),
(78.920,80.840,'WD-E02','static_fade','Scrapped anyway'),
(80.840,82.600,'ST-COLD','static_title','Main title'),
(82.600,90.792,'AR-DEW-MAP','pan_r','When the road ends / map'),
]

def vf(mode,frames):
    base='scale=1440:810:force_original_aspect_ratio=increase,crop=1440:810'
    grade=',eq=saturation=0.88:contrast=1.03,format=yuv420p'
    if mode in ('static','static_title'):
        return base+',crop=960:540:240:135'+grade
    if mode=='static_fade':
        st=max(0,frames/FPS-.35)
        return base+f",crop=960:540:240:135,eq=saturation=0.82:contrast=1.03,fade=t=out:st={st:.3f}:d=.35,format=yuv420p"
    if mode=='detail_left':
        return base+',crop=960:540:70:135'+grade
    if mode=='detail_center':
        return base+',crop=960:540:240:135'+grade
    if mode=='detail_right':
        return base+',crop=960:540:410:135'+grade
    den=max(frames-1,1)
    x=f"70+340*n/{den}" if mode=='pan_r' else f"410-340*n/{den}"
    return base+f",crop=960:540:x='{x}':y=135"+grade

concat=WORK/'concat.txt'
with open(concat,'w') as lf:
    for i,(st,en,code,mode,note) in enumerate(shots,1):
        frames=max(1,round((en-st)*FPS))
        out=SEG/f'{i:02d}.mp4'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(asset(code)),
                        '-vf',vf(mode,frames),'-frames:v',str(frames),'-an',
                        '-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p',str(out)],check=True)
        lf.write(f"file '{out.resolve()}'\n")

silent=WORK/'silent.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(silent)],check=True)

src=(TRANSCRIPT/'TC497_VO_SUBTITLES.srt').read_text(encoding='utf-8-sig')
def sec(ts):
    h,m,s=ts.replace(',','.').split(':')
    return int(h)*3600+int(m)*60+float(s)
def at(t):
    h=int(t//3600); t-=h*3600; m=int(t//60); t-=m*60
    return f'{h}:{m:02d}:{t:05.2f}'

events=[]
for b in src.strip().split('\n\n'):
    lines=b.splitlines()
    if len(lines)<3 or '-->' not in lines[1]:
        continue
    a,z=lines[1].split(' --> ')
    s,e=sec(a),sec(z)
    if s>=DUR: break
    text=' '.join(x.strip() for x in lines[2:]).strip()
    for key in ['572','13 units','54 wheels','150 tons','no railroad','no rails','no prepared highway','actually work','scrapped it anyway']:
        text=re.sub(re.escape(key),r'{\\c&H3552A5&}'+key+r'{\\c&HC8DDE6&}',text,flags=re.I)
    events.append((s,min(e,DUR),text))

ass=WORK/'captions.ass'
with open(ass,'w',encoding='utf-8') as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 0
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,Montserrat SemiBold,28,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H90171A1C,-1,0,0,0,100,100,0,0,3,7,0,2,70,70,28,1
Style: Fact,Montserrat SemiBold,32,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H90171A1C,-1,0,0,0,100,100,0,0,3,6,0,7,36,36,36,1
Style: Title,Montserrat SemiBold,34,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H70171A1C,-1,0,0,0,100,100,1,0,3,10,0,5,60,60,0,1
Style: Chapter,Montserrat SemiBold,27,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H70171A1C,-1,0,0,0,100,100,1,0,3,7,0,7,38,38,38,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for s,e,t in events:
        f.write(f'Dialogue: 3,{at(s)},{at(e)},Sub,,0,0,0,,{t}\n')
    f.write(f'Dialogue: 2,{at(13.30)},{at(15.34)},Fact,,0,0,0,,572 FEET\n')
    f.write(f'Dialogue: 2,{at(16.00)},{at(17.36)},Fact,,0,0,0,,13 UNITS\n')
    f.write(f'Dialogue: 2,{at(23.06)},{at(25.86)},Fact,,0,0,0,,54 DRIVEN WHEELS\n')
    f.write(f'Dialogue: 2,{at(29.54)},{at(32.00)},Fact,,0,0,0,,~150 TONS\n')
    f.write(f'Dialogue: 4,{at(80.84)},{at(82.60)},Title,,0,0,0,,AMERICA BUILT A 572-FOOT TRAIN\\NTHAT NEEDED NO TRACKS\n')
    f.write(f'Dialogue: 4,{at(82.60)},{at(84.80)},Chapter,,0,0,0,,WHEN THE ROAD ENDS\n')

sfx=WORK/'sfx.wav'
fc=[f"anoisesrc=color=brown:duration={DUR}:amplitude=0.025,lowpass=f=120,highpass=f=28,volume=0.16[bed]"]
delays=[12940,23060,36040,74980,80840]
for j,d in enumerate(delays):
    fc.append(f"sine=frequency={58+j*3}:duration=.34,afade=t=out:st=.08:d=.26,volume=0.16,adelay={d}|{d}[i{j}]")
fc.append("anoisesrc=color=white:duration=.65:amplitude=.15,highpass=f=300,lowpass=f=2500,afade=t=in:d=.08,afade=t=out:st=.18:d=.47,volume=.10,adelay=80650|80650[w]")
inputs='[bed]'+''.join(f'[i{j}]' for j in range(len(delays)))+'[w]'
fc.append(f"{inputs}amix=inputs={len(delays)+2}:normalize=0,alimiter=limit=.35[sfx]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-filter_complex',';'.join(fc),'-map','[sfx]','-t',str(DUR),str(sfx)],check=True)

final=ROOT/'_V2'/'TC497_V3_COLD_OPEN_90S_PROOF.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(VO),'-i',str(sfx),
               '-filter_complex',f"[0:v]ass={ass}[v];[1:a]atrim=0:{DUR},asetpts=PTS-STARTPTS,volume=1.0[vo];[2:a]volume=.85[s];[vo][s]amix=inputs=2:normalize=0,alimiter=limit=.94[a]",
               '-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','160k',
               '-t',str(DUR),'-movflags','+faststart',str(final)],check=True)

with open(WORK/'shotlist.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['start','end','asset','treatment','editorial purpose'])
    w.writerows(shots)

print(final,final.stat().st_size)
