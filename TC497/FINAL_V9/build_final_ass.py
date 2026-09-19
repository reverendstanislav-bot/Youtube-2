#!/usr/bin/env python3
import argparse
from pathlib import Path

END_START = 1222.300
CTA_CUT = 1225.450
TOTAL = 1236.533333

SYNTHETIC_SOURCE_LABELS = [
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
    out=[]

    for line in events.splitlines():
        if line.startswith("Format:"):
            fmt=line
            continue
        if not line.startswith("Dialogue:"):
            continue
        p=line.split(",",9)
        if len(p)<10:
            continue
        s=ass_to_sec(p[1]); e=ass_to_sec(p[2])

        # Preserve the complete approved pre-ending caption/provenance grammar.
        if s < END_START:
            q=p.copy()
            q[2]=sec_to_ass(min(e, END_START))
            if ass_to_sec(q[2]) > ass_to_sec(q[1]):
                out.append(",".join(q))

        # On the clean end plate, retain only the final documentary caption.
        if p[3]=="Cap" and e>END_START and s<CTA_CUT:
            q=p.copy()
            q[1]=sec_to_ass(max(END_START,s))
            q[2]=sec_to_ass(min(CTA_CUT,e))
            if ass_to_sec(q[2]) > ass_to_sec(q[1]):
                out.append(",".join(q))

    # Reproduce V6/V9 synthetic provenance labels over replacement stills.
    for start, end, label in SYNTHETIC_SOURCE_LABELS:
        b=min(end, start+2.2)
        out.append(
            f"Dialogue: 0,{sec_to_ass(start)},{sec_to_ass(b)},Source,,0,0,0,,{label}"
        )

    # Approved V8 end-screen identity.
    out += [
        f"Dialogue: 70,{sec_to_ass(1222.30)},{sec_to_ass(TOTAL)},V8Brand,,0,0,0,,{{\\fad(600,350)}}HIDDEN INDUSTRIAL AMERICA",
        f"Dialogue: 71,{sec_to_ass(1223.00)},{sec_to_ass(TOTAL)},V8Hero,,0,0,0,,{{\\fad(750,350)}}TC-497",
        f"Dialogue: 72,{sec_to_ass(1223.65)},{sec_to_ass(TOTAL)},V8Sub,,0,0,0,,{{\\fad(850,350)}}OVERLAND TRAIN",
    ]

    Path(args.output_ass).write_text(
        head+"[Events]\n"+fmt+"\n"+"\n".join(out)+"\n",
        encoding="utf-8"
    )
    print(f"MASTER_ASS_READY events={len(out)} output={args.output_ass}")

if __name__=="__main__":
    main()
