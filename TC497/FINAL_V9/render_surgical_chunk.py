#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path

FPS=30.0
END_START=1222.300
CTA_CUT=1225.450
TOTAL=1236.533333

PATCHES=[
    {"start":215.356,"end":221.464,"image":"electric_human_v6.png","crop":0.0,"label":"RECONSTRUCTION"},
    {"start":230.014,"end":237.342,"image":"electric_wheel_v6.png","crop":0.0,"label":"RECONSTRUCTION"},
    {"start":766.838,"end":775.922,"image":"WC-Y01.png","crop":0.12,"label":"RECONSTRUCTION"},
    {"start":815.287,"end":822.857,"image":"WD-T03.png","crop":0.12,"label":"RECONSTRUCTION"},
    {"start":1020.122,"end":1028.334,"image":"WC-D03.png","crop":0.12,"label":"RECONSTRUCTION"},
    {"start":1054.611,"end":1062.822,"image":"WC-D05.png","crop":0.12,"label":"RECONSTRUCTION"},
]

def sh(cmd):
    print("+"," ".join(map(str,cmd)),flush=True)
    subprocess.run(list(map(str,cmd)),check=True)

def ass_to_sec(x):
    h,m,s=x.split(":")
    return int(h)*3600+int(m)*60+float(s)

def sec_to_ass(t):
    t=max(0.0,float(t)); h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def build_ass(source, start, end, active, tail, out):
    txt=Path(source).read_text(encoding="utf-8",errors="replace")
    head,sep,events=txt.partition("[Events]")
    if not sep:
        raise SystemExit("ASS has no [Events]")

    styles="""Style: V8Brand,DejaVu Sans,15,&H00171A1C,&H00171A1C,&H50F3EBDD,&H00000000,-1,0,0,0,100,100,1.7,0,1,0.8,0,7,66,66,52,1
Style: V8Hero,DejaVu Sans,43,&H00171A1C,&H00171A1C,&H40F3EBDD,&H00000000,-1,0,0,0,100,100,0.6,0,1,1.0,0,7,66,66,84,1
Style: V8Sub,DejaVu Sans,14,&H002E3234,&H002E3234,&H50F3EBDD,&H00000000,0,0,0,0,100,100,1.0,0,1,0.6,0,7,68,68,146,1
"""
    idx=head.rfind("\n")
    head=head[:idx+1]+styles+head[idx+1:]

    fmt="Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    parsed=[]
    for line in events.splitlines():
        if line.startswith("Format:"):
            fmt=line; continue
        if not line.startswith("Dialogue:"):
            continue
        p=line.split(",",9)
        if len(p)<10:
            continue
        parsed.append((p,ass_to_sec(p[1]),ass_to_sec(p[2])))

    rendered=[]
    for p,s,e in parsed:
        for patch in active:
            a=max(s,patch["start"],start); b=min(e,patch["end"],end)
            if b<=a:
                continue
            q=p.copy(); q[1]=sec_to_ass(a-start); q[2]=sec_to_ass(b-start)
            rendered.append(",".join(q))

    for patch in active:
        a=max(patch["start"],start)
        b=min(patch["end"],patch["start"]+2.2,end)
        if b>a:
            rendered.append(
                f"Dialogue: 0,{sec_to_ass(a-start)},{sec_to_ass(b-start)},Source,,0,0,0,,{patch['label']}"
            )

    if tail:
        for p,s,e in parsed:
            if p[3]=="Cap" and e>END_START and s<CTA_CUT:
                a=max(s,END_START,start); b=min(e,CTA_CUT,end)
                if b>a:
                    q=p.copy(); q[1]=sec_to_ass(a-start); q[2]=sec_to_ass(b-start)
                    rendered.append(",".join(q))
        if end>END_START:
            final_rel=end-start
            rendered += [
                f"Dialogue: 70,{sec_to_ass(max(END_START,start)-start)},{sec_to_ass(final_rel)},V8Brand,,0,0,0,,{{\\fad(600,350)}}HIDDEN INDUSTRIAL AMERICA",
                f"Dialogue: 71,{sec_to_ass(max(1223.00,start)-start)},{sec_to_ass(final_rel)},V8Hero,,0,0,0,,{{\\fad(750,350)}}TC-497",
                f"Dialogue: 72,{sec_to_ass(max(1223.65,start)-start)},{sec_to_ass(final_rel)},V8Sub,,0,0,0,,{{\\fad(850,350)}}OVERLAND TRAIN",
            ]

    Path(out).write_text(
        head+"[Events]\n"+fmt+"\n"+"\n".join(rendered)+("\n" if rendered else ""),
        encoding="utf-8"
    )
    return len(rendered)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--source-ass",required=True)
    ap.add_argument("--asset-dir",required=True)
    ap.add_argument("--start",type=float,required=True)
    ap.add_argument("--end",type=float,required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--clean-end")
    args=ap.parse_args()

    start=round(args.start*FPS)/FPS
    end=round(args.end*FPS)/FPS
    duration=end-start
    if duration<=0:
        raise SystemExit("bad range")

    active=[p for p in PATCHES if p["end"]>start and p["start"]<end]
    tail=bool(args.clean_end) and end>END_START
    ass=Path(args.output).with_suffix(".ass")
    count=build_ass(args.source_ass,start,end,active,tail,ass)
    print(f"chunk {start:.6f}-{end:.6f} active={len(active)} tail={tail} ass={count}",flush=True)

    cmd=["ffmpeg","-y","-loglevel","error","-ss",f"{start:.6f}","-i",args.input]
    overlays=[]
    for p in active:
        path=(Path(args.asset_dir)/p["image"]).resolve()
        if not path.is_file():
            raise SystemExit(f"missing {path}")
        overlays.append((p,path))
        cmd += ["-loop","1","-framerate","30","-i",str(path)]

    clean_index=None
    if tail:
        clean=Path(args.clean_end).resolve()
        if not clean.is_file():
            raise SystemExit(f"missing {clean}")
        clean_index=1+len(overlays)
        cmd += ["-loop","1","-framerate","30","-i",str(clean)]

    fc=["[0:v]setpts=PTS-STARTPTS[v0]"]
    prev="[v0]"
    for idx,(p,path) in enumerate(overlays,start=1):
        ps=max(start,p["start"])-start
        pe=min(end,p["end"])-start
        tag=f"p{idx}"; nxt=f"v{idx}"
        if p["crop"]>0:
            c=p["crop"]; keep=1-2*c
            prep=(f"[{idx}:v]crop=iw*{keep:.6f}:ih*{keep:.6f}:iw*{c:.6f}:ih*{c:.6f},"
                  f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS[{tag}]")
        else:
            prep=(f"[{idx}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                  f"setpts=PTS-STARTPTS[{tag}]")
        fc.append(prep)
        fc.append(f"{prev}[{tag}]overlay=0:0:eof_action=pass:enable='between(t,{ps:.6f},{pe:.6f})'[{nxt}]")
        prev=f"[{nxt}]"

    if tail:
        rel=max(0.0,END_START-start)
        tag="clean"
        fc.append(
            f"[{clean_index}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            f"eq=brightness=0.015:contrast=1.025:saturation=0.92,setpts=PTS-STARTPTS[{tag}]"
        )
        fc.append(f"{prev}[{tag}]overlay=0:0:eof_action=pass:enable='gte(t,{rel:.6f})'[vend]")
        prev="[vend]"

    if count:
        fc.append(f"{prev}ass={ass},format=yuv420p[vout]")
        prev="[vout]"

    cmd += [
        "-filter_complex",";".join(fc),"-map",prev,"-an","-t",f"{duration:.6f}","-r","30",
        "-c:v","libx264","-preset","fast","-crf","17","-profile:v","high","-level","4.1",
        "-pix_fmt","yuv420p","-movflags","+faststart",args.output
    ]
    sh(cmd)

if __name__=="__main__":
    main()
