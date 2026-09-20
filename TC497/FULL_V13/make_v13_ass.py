#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

ORANGE_BASE='&H002E7AD7&'   # RGB D77A2E
ORANGE_ACTIVE='&H00389AF3&' # RGB F39A38
ORANGE_SOFT='&H005D92C8&'   # RGB C8925D
DARK='&H00171A1C&'

COLD_END=82.6
CTA_CUT=1225.45
TOTAL=1236.533333

def ass_to_sec(x):
    h,m,s=x.split(':')
    return int(h)*3600+int(m)*60+float(s)

def sec_to_ass(t):
    t=max(0.0,float(t))
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def strip_tags(text):
    return re.sub(r'\{[^}]*\}','',text).replace('\\N',' ')

def esc(text):
    return text.replace('{','\\{').replace('}','\\}')

def active_phrase(text, active_idx):
    words=text.split()
    out=[]
    for i,w in enumerate(words):
        color=ORANGE_ACTIVE if i==active_idx else ORANGE_BASE
        out.append('{\\c'+color+'}'+esc(w))
    return ' '.join(out)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-ass',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    src=Path(args.source_ass).read_text(encoding='utf-8',errors='replace')
    _,sep,events=src.partition('[Events]')
    if not sep:
        raise SystemExit('ASS missing [Events]')

    parsed=[]
    for line in events.splitlines():
        if not line.startswith('Dialogue:'):
            continue
        p=line.split(',',9)
        if len(p)<10:
            continue
        parsed.append(p)

    lines=[]

    # Global post-cold-open running orange captions.
    caps=[]
    for p in parsed:
        if p[3] != 'Cap':
            continue
        s=ass_to_sec(p[1]); e=ass_to_sec(p[2])
        if e <= COLD_END or s >= CTA_CUT:
            continue
        s=max(s,COLD_END); e=min(e,CTA_CUT)
        text=strip_tags(p[9]).strip()
        if not text or e<=s:
            continue
        caps.append((s,e,text))

    for s,e,text in caps:
        words=text.split()
        if not words:
            continue
        # Keep the whole phrase visible; move a brighter orange emphasis word-by-word.
        # Minimum 0.11s per state avoids unreadable flicker.
        dur=max(0.11,(e-s)/len(words))
        for i in range(len(words)):
            a=s+i*dur
            b=e if i==len(words)-1 else min(e,s+(i+1)*dur)
            if b-a < 0.06:
                continue
            lines.append(
                f"Dialogue: 100,{sec_to_ass(a)},{sec_to_ass(b)},RunV13,,0,0,0,,{active_phrase(text,i)}"
            )

    # Provenance / editor labels: one warm-orange family, no blue/cyan caption language.
    for p in parsed:
        style=p[3]
        if style not in {'Source','Document','Concept','Tag'}:
            continue
        s=ass_to_sec(p[1]); e=ass_to_sec(p[2])
        if e<=COLD_END or s>=1222.30:
            continue
        text=strip_tags(p[9]).strip()
        if not text:
            continue
        out_style='TagV13' if style=='Tag' else 'SourceV13'
        lines.append(
            f"Dialogue: 80,{sec_to_ass(max(COLD_END,s))},{sec_to_ass(min(1222.30,e))},{out_style},,0,0,0,,"
            f"{{\\c{ORANGE_SOFT}}}{esc(text)}"
        )

    # Explicit labels for later replacement windows.
    labels=[
      (261.771,264.10,'RECONSTRUCTION'),
      (295.972,298.30,'DOCUMENT • U.S. PATENT'),
      (474.502,476.90,'ARCHIVE • TC-497'),
      (709.241,711.50,'CONCEPT'),
      (716.900,719.20,'RECONSTRUCTION'),
      (716.900,719.95,'ACTUAL TC-497 • GAS TURBINES','tag'),
      (730.373,732.65,'CONCEPT'),
      (766.838,769.05,'RECONSTRUCTION'),
      (815.287,817.50,'RECONSTRUCTION'),
      (1020.122,1022.35,'RECONSTRUCTION'),
      (1054.611,1056.85,'RECONSTRUCTION'),
      (1079.245,1081.45,'RECONSTRUCTION'),
      (1107.164,1109.35,'RECONSTRUCTION'),
      (1209.007,1211.20,'RECONSTRUCTION'),
    ]
    for item in labels:
        s,e,text,*kind=item
        st='TagV13' if kind and kind[0]=='tag' else 'SourceV13'
        lines.append(
          f"Dialogue: 120,{sec_to_ass(s)},{sec_to_ass(e)},{st},,0,0,0,,{{\\c{ORANGE_SOFT}}}{esc(text)}"
        )

    # V8 restrained identity, but in the same warm-orange family.
    lines += [
      f"Dialogue: 70,{sec_to_ass(1222.30)},{sec_to_ass(TOTAL)},V13Brand,,0,0,0,,{{\\fad(600,350)}}HIDDEN INDUSTRIAL AMERICA",
      f"Dialogue: 71,{sec_to_ass(1223.00)},{sec_to_ass(TOTAL)},V13Hero,,0,0,0,,{{\\fad(750,350)}}TC-497",
      f"Dialogue: 72,{sec_to_ass(1223.65)},{sec_to_ass(TOTAL)},V13Sub,,0,0,0,,{{\\fad(850,350)}}OVERLAND TRAIN",
    ]

    header=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: RunV13,DejaVu Sans,31,{ORANGE_BASE},{ORANGE_ACTIVE},{DARK},&H00000000,-1,0,0,0,100,100,0,0,1,3.1,1.2,2,74,74,38,1
Style: SourceV13,DejaVu Sans,16,{ORANGE_SOFT},{ORANGE_SOFT},{DARK},&H00000000,-1,0,0,0,100,100,0.8,0,1,2.2,0.8,9,28,28,20,1
Style: TagV13,DejaVu Sans,17,{ORANGE_SOFT},{ORANGE_SOFT},{DARK},&H00000000,-1,0,0,0,100,100,0.4,0,1,2.4,0.8,7,38,38,46,1
Style: V13Brand,DejaVu Sans,15,{ORANGE_SOFT},{ORANGE_SOFT},{DARK},&H00000000,-1,0,0,0,100,100,1.7,0,1,1.0,0,7,66,66,52,1
Style: V13Hero,DejaVu Sans,43,{ORANGE_ACTIVE},{ORANGE_ACTIVE},{DARK},&H00000000,-1,0,0,0,100,100,0.6,0,1,1.2,0,7,66,66,84,1
Style: V13Sub,DejaVu Sans,14,{ORANGE_SOFT},{ORANGE_SOFT},{DARK},&H00000000,0,0,0,0,100,100,1.0,0,1,0.8,0,7,68,68,146,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    Path(args.output).write_text(header+'\n'.join(lines)+'\n',encoding='utf-8')
    print('V13 events',len(lines),'caption phrases',len(caps))

if __name__=='__main__':
    main()
