#!/usr/bin/env python3
import argparse
from pathlib import Path

END_START = 1222.300
CTA_CUT = 1225.450
TOTAL = 1236.533333

PATCHES = [
    (215.356, 221.464, "RECONSTRUCTION"),
    (230.014, 237.342, "RECONSTRUCTION"),
    (766.838, 775.922, "RECONSTRUCTION"),
    (815.287, 822.857, "RECONSTRUCTION"),
    (1020.122, 1028.334, "RECONSTRUCTION"),
    (1054.611, 1062.822, "RECONSTRUCTION"),
]

def ass_to_sec(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def sec_to_ass(t):
    t=max(0.0,float(t))
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def clipped_dialogue(parts, a, b):
    q=parts.copy()
    q[1]=sec_to_ass(a)
    q[2]=sec_to_ass(b)
    return ",".join(q)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-ass", required=True)
    ap.add_argument("--output-ass", required=True)
    args=ap.parse_args()

    txt=Path(args.source_ass).read_text(encoding="utf-8", errors="replace")
    head, sep, events = txt.partition("[Events]")
    if not sep:
        raise SystemExit("ASS has no [Events] section")

    styles = """Style: V8Brand,DejaVu Sans,15,&H00171A1C,&H00171A1C,&H50F3EBDD,&H00000000,-1,0,0,0,100,100,1.7,0,1,0.8,0,7,66,66,52,1
Style: V8Hero,DejaVu Sans,43,&H00171A1C,&H00171A1C,&H40F3EBDD,&H00000000,-1,0,0,0,100,100,0.6,0,1,1.0,0,7,66,66,84,1
Style: V8Sub,DejaVu Sans,14,&H002E3234,&H002E3234,&H50F3EBDD,&H00000000,0,0,0,0,100,100,1.0,0,1,0.6,0,7,68,68,146,1
"""
    idx=head.rfind("\n")
    head=head[:idx+1]+styles+head[idx+1:]

    fmt="Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"
    parsed=[]
    for line in events.splitlines():
        if line.startswith("Format:"):
            fmt=line
            continue
        if not line.startswith("Dialogue:"):
            continue
        p=line.split(",",9)
        if len(p)<10:
            continue
        parsed.append((p,ass_to_sec(p[1]),ass_to_sec(p[2])))

    out=[]

    # The native 1080 source already has the V4 ASS baked in.
    # Re-burn only events hidden by the six replacement stills.
    for p,s,e in parsed:
        for ps,pe,_ in PATCHES:
            a=max(s,ps); b=min(e,pe)
            if b>a:
                out.append(clipped_dialogue(p,a,b))

    # Explicit provenance on all V6/V9 replacement stills.
    for start,end,label in PATCHES:
        out.append(
            f"Dialogue: 0,{sec_to_ass(start)},{sec_to_ass(min(end,start+2.2))},Source,,0,0,0,,{label}"
        )

    # Clean V8 ending covers the previously baked end-card and CTA captions.
    # Restore only the final documentary sentence, then the approved identity.
    for p,s,e in parsed:
        if p[3]=="Cap" and e>END_START and s<CTA_CUT:
            a=max(END_START,s); b=min(CTA_CUT,e)
            if b>a:
                out.append(clipped_dialogue(p,a,b))

    out += [
        f"Dialogue: 70,{sec_to_ass(1222.30)},{sec_to_ass(TOTAL)},V8Brand,,0,0,0,,{{\\fad(600,350)}}HIDDEN INDUSTRIAL AMERICA",
        f"Dialogue: 71,{sec_to_ass(1223.00)},{sec_to_ass(TOTAL)},V8Hero,,0,0,0,,{{\\fad(750,350)}}TC-497",
        f"Dialogue: 72,{sec_to_ass(1223.65)},{sec_to_ass(TOTAL)},V8Sub,,0,0,0,,{{\\fad(850,350)}}OVERLAND TRAIN",
    ]

    Path(args.output_ass).write_text(
        head+"[Events]\n"+fmt+"\n"+"\n".join(out)+"\n",
        encoding="utf-8"
    )
    print(f"FINAL_PATCH_ASS_READY events={len(out)} output={args.output_ass}")

if __name__=="__main__":
    main()
