import csv,glob,os,subprocess
from pathlib import Path

PKG=Path(os.environ["PKG_ROOT"])
GEN=Path(os.environ["GEN_DIR"])
ARC=PKG/"04_DOWNLOADS"/"ARCHIVE_GREEN"
EXTRA=Path(os.environ["V14_EXTRA"])
PUB=Path(os.environ["V14_PUBLIC"])
WORK=Path(os.environ["V14_WORK"])
SEG=WORK/"segments"
PUB.mkdir(parents=True,exist_ok=True)
SEG.mkdir(parents=True,exist_ok=True)

FPS=30
DUR=82.6

# V14: semantic cuts, less repeated machine imagery, no crop oscillation.
SH=[
(0.000,"INTRO_DETAIL","full","generated"),
(2.120,"INTRO_OBSERVERS","full","generated"),
(6.900,"INTRO_REVEAL","full","generated"),
(12.940,"ST-572","full","recon"),
(17.840,"WB-L06","safe","recon"),
(23.060,"WB-L05","safe","recon"),
(26.460,"WD-W02","safe","recon"),
(33.040,"AR-A01","full","archive"),
(40.500,"WC-R01","safe","recon"),
(45.352,"WC-R02","safe","recon"),
(48.060,"ST-COLD","safe","recon"),
(53.880,"OTTER2_COVER","full","document"),
(57.200,"ST-572","full","recon"),
(61.080,"ST-ELECTRIC","safe","recon"),
(64.620,"WB-L03","safe","recon"),
(68.760,"WD-T01","safe","recon"),
(71.000,"WC-Y02","safe","recon"),
(74.650,"WD-W01","safe","recon"),
(78.920,"ST-LAST","safe","last"),
(80.840,"WD-E05","safe","titleplate"),
(82.600,"WD-E05","safe","titleplate")
]

# Only bridge actual visual-language changes.
TD={
  3:(.10,"fade"),          # reveal -> established plate
  7:(.10,"fade"),          # reconstruction -> archive evidence
  8:(.12,"fade"),          # archive -> terrain
  11:(.12,"fade"),         # named machine -> official document
  12:(.12,"fade"),         # document -> reconstruction
  17:(.10,"fade"),         # dune -> success
  18:(.12,"fadeblack"),    # success -> aftermath
  19:(.16,"fadeblack")     # aftermath -> dedicated title plate
}

def asset(code):
    if code.startswith("INTRO_"):
        return EXTRA/f"{code}.png"
    if code=="OTTER2_COVER":
        p=EXTRA/"OTTER2_COVER.png"
        if not p.exists():
            pdf=next(ARC.glob("AR-OTTER2__*.pdf"))
            stem=EXTRA/"otter2_cover"
            subprocess.run(["pdftoppm","-f","1","-singlefile","-png","-r","110",str(pdf),str(stem)],check=True)
            (EXTRA/"otter2_cover.png").rename(p)
        return p
    p=GEN/f"{code}.png"
    if p.exists():
        return p
    xs=glob.glob(str(ARC/f"{code}__*"))
    if xs:
        return Path(xs[0])
    raise FileNotFoundError(code)

def vf(mode,kind):
    if kind=="document":
        # Deliberately darker than V13 to avoid the 53.9s white flash.
        return "scale=900:506:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2:color=0xB3A78F,eq=saturation=.66:contrast=.99:brightness=-.055:gamma=.94"
    if mode=="safe":
        base="scale=1632:918:force_original_aspect_ratio=increase,crop=1632:918"
        crop="crop=960:540:336:189"
    else:
        base="scale=1440:810:force_original_aspect_ratio=increase,crop=1440:810"
        crop="crop=960:540:240:135"

    if kind=="archive":
        return base+","+crop+",hue=s=.08,eq=saturation=.70:contrast=1.015:brightness=-.050:gamma=.96,colorbalance=rs=.012:gs=.003:bs=-.010,scale=900:506,pad=960:540:30:17:color=0xBFB39B"
    if kind=="generated":
        return base+","+crop+",eq=saturation=.92:contrast=1.02:brightness=.014:gamma=1.025,colorbalance=rs=.014:gs=.003:bs=-.010"
    if kind=="last":
        return base+","+crop+",eq=saturation=.83:contrast=1.035:brightness=-.005:gamma=1.00,colorbalance=rs=.012:gs=.002:bs=-.012"
    if kind=="titleplate":
        return base+","+crop+",eq=saturation=.74:contrast=1.00:brightness=-.020:gamma=.98,colorbalance=rs=.010:gs=.002:bs=-.010"
    return base+","+crop+",eq=saturation=.90:contrast=1.025:brightness=.015:gamma=1.035,colorbalance=rs=.018:gs=.004:bs=-.014"

def render(code,mode,kind,dur,out):
    frames=max(2,round(dur*FPS))
    subprocess.run([
        "ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-loop","1","-i",str(asset(code)),
        "-vf",vf(mode,kind)+",format=yuv420p","-frames:v",str(frames),"-an",
        "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",str(out)
    ],check=True)

seq=[]
decisions=[]
for i,s in enumerate(SH[:-1]):
    st,code,mode,kind=s
    en=SH[i+1][0]
    n=i+1
    pin=TD.get(n-1,(0,""))[0] if n>1 else 0
    pout=TD.get(n,(0,""))[0]
    body=max(.08,(en-st)-pin/2-pout/2)
    bo=SEG/f"{n:03d}_body.mp4"
    render(code,mode,kind,body,bo)
    seq.append(bo)
    decisions.append([n,st,en,code,mode,kind,TD.get(n,(0,"cut"))[1]])
    if n in TD and i+1<len(SH)-1:
        d,tr=TD[n]
        ns=SH[i+1]
        a=SEG/f"{n:03d}_a.mp4"
        b=SEG/f"{n:03d}_b.mp4"
        x=SEG/f"{n:03d}_x.mp4"
        render(code,mode,kind,d,a)
        render(ns[1],ns[2],ns[3],d,b)
        fc=f"[0:v]settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]xfade=transition={tr}:duration={d}:offset=0[v]"
        subprocess.run([
            "ffmpeg","-y","-loglevel","error","-i",str(a),"-i",str(b),"-filter_complex",fc,
            "-map","[v]","-an","-t",str(d),"-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",str(x)
        ],check=True)
        seq.append(x)

concat=WORK/"concat.txt"
concat.write_text("".join(f"file '{p.resolve()}'\n" for p in seq))
subprocess.run([
    "ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),
    "-c","copy",str(PUB/"base.mp4")
],check=True)

with open(WORK/"V14_EDIT_DECISIONS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["shot","start","end","asset","framing","treatment","transition"])
    w.writerows(decisions)

print("V14_PREP_DONE", len(decisions))
