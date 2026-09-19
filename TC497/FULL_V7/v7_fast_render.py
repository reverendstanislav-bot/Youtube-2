#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path

TAIL_START=1185.0
END_START=1222.300
TOTAL=1236.533333
TAIL_DUR=TOTAL-TAIL_START

def sh(cmd):
    print("+"," ".join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),check=True)

def ass_sec(s):
    h,m,ss=s.split(":")
    return int(h)*3600+int(m)*60+float(ss)

def sec_ass(t):
    t=max(0.0,float(t)); h=int(t//3600); t-=h*3600; m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def build_tail_ass(src,out):
    txt=Path(src).read_text(encoding="utf-8",errors="replace")
    before,sep,events=txt.partition("[Events]")
    if not sep: raise SystemExit("No [Events] in ASS")
    styles="""Style: V7Brand,DejaVu Sans,15,&H00171A1C,&H00171A1C,&H50F3EBDD,&H00000000,-1,0,0,0,100,100,1.7,0,1,0.8,0,7,66,66,52,1
Style: V7Hero,DejaVu Sans,43,&H00171A1C,&H00171A1C,&H40F3EBDD,&H00000000,-1,0,0,0,100,100,0.6,0,1,1.0,0,7,66,66,84,1
Style: V7Sub,DejaVu Sans,14,&H002E3234,&H002E3234,&H50F3EBDD,&H00000000,0,0,0,0,100,100,1.0,0,1,0.6,0,7,68,68,146,1
"""
    idx=before.rfind("\n")
    before=before[:idx+1]+styles+before[idx+1:]
    fmt="Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    keep=[]
    for line in events.splitlines():
        if line.startswith("Format:"): fmt=line; continue
        if not line.startswith("Dialogue:"): continue
        p=line.split(",",9)
        if len(p)<10: continue
        s,e=ass_sec(p[1]),ass_sec(p[2])
        if p[3]=="Cap" and e>END_START and s<TOTAL:
            p[1]=sec_ass(max(END_START,s)-TAIL_START)
            p[2]=sec_ass(min(TOTAL,e)-TAIL_START)
            keep.append(",".join(p))
    b=1222.30-TAIL_START
    keep += [
      f"Dialogue: 70,{sec_ass(b)},{sec_ass(TAIL_DUR)},V7Brand,,0,0,0,,{{\\fad(600,250)}}HIDDEN INDUSTRIAL AMERICA",
      f"Dialogue: 71,{sec_ass(1223.00-TAIL_START)},{sec_ass(TAIL_DUR)},V7Hero,,0,0,0,,{{\\fad(750,250)}}TC-497",
      f"Dialogue: 72,{sec_ass(1223.65-TAIL_START)},{sec_ass(TAIL_DUR)},V7Sub,,0,0,0,,{{\\fad(850,250)}}OVERLAND TRAIN",
    ]
    Path(out).write_text(before+"[Events]\n"+fmt+"\n"+"\n".join(keep)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--clean-end",required=True)
    ap.add_argument("--source-ass",required=True)
    ap.add_argument("--music",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--work-dir",required=True)
    args=ap.parse_args()
    wd=Path(args.work_dir); wd.mkdir(parents=True,exist_ok=True)
    ass=wd/"v7_tail.ass"; build_tail_ass(args.source_ass,ass)
    prefix=wd/"prefix.mp4"; tail=wd/"tail.mp4"; video=wd/"video_only.mp4"; audio=wd/"audio.m4a"
    sh(["ffmpeg","-y","-loglevel","error","-i",args.input,"-t",f"{TAIL_START:.3f}",
        "-map","0:v:0","-an","-c:v","copy","-avoid_negative_ts","make_zero",str(prefix)])
    rel=END_START-TAIL_START
    fc=(f"[1:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,"
        f"eq=brightness=0.015:contrast=1.025:saturation=0.92[clean];"
        f"[0:v][clean]overlay=0:0:enable='between(t,{rel:.3f},{TAIL_DUR:.3f})'[v1];"
        f"[v1]ass={ass}[vout]")
    sh(["ffmpeg","-y","-loglevel","error","-ss",f"{TAIL_START:.3f}","-i",args.input,
        "-loop","1","-framerate","30","-i",args.clean_end,
        "-filter_complex",fc,"-map","[vout]","-an","-t",f"{TAIL_DUR:.3f}","-r","30",
        "-c:v","libx264","-preset","ultrafast","-crf","19","-pix_fmt","yuv420p",
        "-g","60","-keyint_min","60","-sc_threshold","0",str(tail)])
    concat=wd/"concat.txt"
    concat.write_text(f"file '{prefix.resolve()}'\nfile '{tail.resolve()}'\n",encoding="utf-8")
    sh(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),
        "-c","copy","-movflags","+faststart",str(video)])
    af=(f"[0:a]aresample=48000,asplit=2[base][sc];"
        f"[1:a]atrim=0:{TAIL_DUR:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=3.5,afade=t=out:st={TAIL_DUR-7.0:.3f}:d=7,"
        f"volume=0.18,adelay=1185000|1185000,apad=pad_dur={TOTAL:.3f},atrim=0:{TOTAL:.3f}[music];"
        f"[music][sc]sidechaincompress=threshold=0.028:ratio=9:attack=18:release=520:makeup=1[mduck];"
        f"[base][mduck]amix=inputs=2:weights='1 1':normalize=0,alimiter=limit=0.794:level=false[aout]")
    sh(["ffmpeg","-y","-loglevel","error","-i",args.input,"-i",args.music,
        "-filter_complex",af,"-map","[aout]","-t",f"{TOTAL:.3f}",
        "-c:a","aac","-b:a","192k",str(audio)])
    sh(["ffmpeg","-y","-loglevel","error","-i",str(video),"-i",str(audio),
        "-map","0:v:0","-map","1:a:0","-c","copy","-t",f"{TOTAL:.3f}",
        "-movflags","+faststart",args.output])

if __name__=="__main__": main()
