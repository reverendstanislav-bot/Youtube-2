#!/usr/bin/env python3
import argparse, re, subprocess
from pathlib import Path

END_START = 1221.948
TOTAL = 1236.533333

def sh(cmd):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(list(map(str, cmd)), check=True)

def ass_sec(s):
    h,m,ss=s.split(":")
    return int(h)*3600 + int(m)*60 + float(ss)

def sec_ass(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def build_end_ass(src, out):
    txt=Path(src).read_text(encoding="utf-8", errors="replace")
    before, sep, events = txt.partition("[Events]")
    if not sep:
        raise SystemExit("No [Events] section in source ASS")

    style_insert = """Style: V7Brand,DejaVu Sans,15,&H00171A1C,&H00171A1C,&H50F3EBDD,&H00000000,-1,0,0,0,100,100,1.7,0,1,0.8,0,7,66,66,52,1
Style: V7Hero,DejaVu Sans,43,&H00171A1C,&H00171A1C,&H40F3EBDD,&H00000000,-1,0,0,0,100,100,0.6,0,1,1.0,0,7,66,66,84,1
Style: V7Sub,DejaVu Sans,14,&H002E3234,&H002E3234,&H50F3EBDD,&H00000000,0,0,0,0,100,100,1.0,0,1,0.6,0,7,68,68,146,1
"""
    if "Style: V7Brand" not in before:
        before = before.replace("\n[Events]", "\n"+style_insert+"\n[Events]") if "[Events]" in before else before
        # partition removed [Events], so insert before the event marker explicitly.
        idx = before.rfind("\n")
        before = before[:idx+1] + style_insert + before[idx+1:]

    fmt="Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    kept=[]
    for line in events.splitlines():
        if line.startswith("Format:"):
            fmt=line
            continue
        if not line.startswith("Dialogue:"):
            continue
        p=line.split(",",9)
        if len(p)<10: continue
        s,e=ass_sec(p[1]),ass_sec(p[2])
        style=p[3]
        if style=="Cap" and e>END_START and s<TOTAL:
            p[1]=sec_ass(max(END_START,s))
            p[2]=sec_ass(min(TOTAL,e))
            kept.append(",".join(p))

    brand_start=1222.30
    kept += [
        f"Dialogue: 70,{sec_ass(brand_start)},{sec_ass(TOTAL)},V7Brand,,0,0,0,,{{\\fad(600,250)}}HIDDEN INDUSTRIAL AMERICA",
        f"Dialogue: 71,{sec_ass(1223.00)},{sec_ass(TOTAL)},V7Hero,,0,0,0,,{{\\fad(750,250)}}TC-497",
        f"Dialogue: 72,{sec_ass(1223.65)},{sec_ass(TOTAL)},V7Sub,,0,0,0,,{{\\fad(850,250)}}OVERLAND TRAIN",
        f"Dialogue: 72,{sec_ass(1225.00)},{sec_ass(TOTAL)},V7Sub,,0,0,0,,{{\\fad(900,250)}}FORGOTTEN MACHINES  /  HIDDEN SYSTEMS  /  ENGINEERING HISTORY",
    ]
    Path(out).write_text(before+"[Events]\n"+fmt+"\n"+"\n".join(kept)+"\n", encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--clean-end", required=True)
    ap.add_argument("--source-ass", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--work-dir", required=True)
    args=ap.parse_args()

    wd=Path(args.work_dir); wd.mkdir(parents=True, exist_ok=True)
    end_ass=wd/"v7_end.ass"
    build_end_ass(args.source_ass, end_ass)

    # The existing V6 frame is replaced only for the final plate. This removes
    # the baked centered slogan and old burned captions, then restores only the
    # final narration captions plus the new asymmetric brand lockup.
    fc = (
        f"[1:v]scale=960:540:force_original_aspect_ratio=increase,"
        f"crop=960:540,eq=brightness=0.015:contrast=1.025:saturation=0.92[clean];"
        f"[0:v][clean]overlay=0:0:enable='between(t,{END_START:.3f},{TOTAL:.3f})'[v1];"
        f"[v1]ass={end_ass}[vout];"
        f"[0:a]aresample=48000,asplit=2[base][sc];"
        f"[2:a]atrim=0:{TOTAL-1185.0:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=3.5,afade=t=out:st={TOTAL-1185.0-7.0:.3f}:d=7,"
        f"volume=0.42,adelay=1185000|1185000,apad=pad_dur={TOTAL:.3f},atrim=0:{TOTAL:.3f}[music];"
        f"[music][sc]sidechaincompress=threshold=0.028:ratio=9:attack=18:release=520:makeup=1[mduck];"
        f"[base][mduck]amix=inputs=2:weights='1 1':normalize=0,alimiter=limit=0.88[aout]"
    )
    sh([
        "ffmpeg","-y","-loglevel","error",
        "-i",args.input,"-loop","1","-framerate","30","-i",args.clean_end,"-i",args.music,
        "-filter_complex",fc,
        "-map","[vout]","-map","[aout]","-t",f"{TOTAL:.3f}",
        "-r","30","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-movflags","+faststart",args.output
    ])

if __name__=="__main__":
    main()
