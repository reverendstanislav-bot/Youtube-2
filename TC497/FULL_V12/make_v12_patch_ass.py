#!/usr/bin/env python3
import argparse
from pathlib import Path

PATCHES = [
    (261.771,269.100,'RECONSTRUCTION',''),
    (295.972,300.858,'DOCUMENT • U.S. PATENT',''),
    (474.502,480.163,'ARCHIVE • TC-497',''),
    (716.900,724.500,'RECONSTRUCTION','ACTUAL TC-497 • GAS TURBINES'),
]

def ass_to_sec(x):
    h,m,s=x.split(':')
    return int(h)*3600+int(m)*60+float(s)

def sec_to_ass(t):
    t=max(0.0,float(t))
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-ass',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    txt=Path(args.source_ass).read_text(encoding='utf-8',errors='replace')
    head,sep,events=txt.partition('[Events]')
    if not sep:
        raise SystemExit('ASS has no [Events]')

    fmt='Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text'
    parsed=[]
    for line in events.splitlines():
        if line.startswith('Format:'):
            fmt=line
        elif line.startswith('Dialogue:'):
            p=line.split(',',9)
            if len(p)==10:
                parsed.append(p)

    out=[]
    for ps,pe,label,tag in PATCHES:
        for p in parsed:
            if p[3] != 'Cap':
                continue
            s=ass_to_sec(p[1]); e=ass_to_sec(p[2])
            a=max(s,ps); b=min(e,pe)
            if b<=a:
                continue
            q=p.copy()
            q[1]=sec_to_ass(a)
            q[2]=sec_to_ass(b)
            out.append(','.join(q))

        style='Document' if label.startswith('DOCUMENT') else 'Source'
        out.append(f"Dialogue: 45,{sec_to_ass(ps+0.15)},{sec_to_ass(min(pe,ps+2.35))},{style},,0,0,0,,{label}")
        if tag:
            out.append(f"Dialogue: 50,{sec_to_ass(ps+0.30)},{sec_to_ass(min(pe,ps+3.10))},Tag,,0,0,0,,{tag}")

    Path(args.output).write_text(
        head+'[Events]\n'+fmt+'\n'+'\n'.join(out)+'\n',
        encoding='utf-8'
    )
    print('events',len(out))

if __name__=='__main__':
    main()
