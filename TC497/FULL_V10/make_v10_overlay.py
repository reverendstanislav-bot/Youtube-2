#!/usr/bin/env python3
import re, argparse
from pathlib import Path

ACCENT='&H003552A5&'   # #A55235 rust, same family as V14 cold open
BASE='&H00DDEBF3&'     # #F3EBDD ivory
BLUE='&H00B6A89A&'
GOLD='&H008EC5E0&'
RECON='&H00708ED8&'
CONCEPT='&H009D9DE2&'

STOP=set('a an the and or but if then than that this these those it its is are was were be been being to of in on at for from by with as into over under across through after before when where who what why how one two three another some any all more most much very far no not did do does had has have having could would should can may might will just only already therefore'.split())

PHRASES=[
 'TC-497','TC 497','Overland Train','LeTourneau','Yuma Proving Ground','Yuma','Arizona','U.S. Army','Army',
 'gas turbines','gas turbine','turbines','turbine','generator','electric wheel','electricity','electric',
 'nuclear reactor','reactor','nuclear','helicopter','Skycrane','CH-54','terrain','desert','Arctic',
 'railroads','railroad','rails','roads','road','highway','cargo','wheels','wheel','fuel','power','engine',
 'prototype','testing','test','traction','survivor','survived','572 feet','572','54','150 tons','150'
]

def ass_to_sec(x):
    h,m,s=x.split(':')
    return int(h)*3600+int(m)*60+float(s)

def sec_to_ass(t):
    t=max(0.0,float(t))
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def esc(s):
    return s.replace('{','\\{').replace('}','\\}')

def colorize(text):
    plain=re.sub(r'\{[^}]*\}','',text)
    matches=[]
    for ph in sorted(PHRASES,key=len,reverse=True):
        for m in re.finditer(r'(?<![A-Za-z0-9])'+re.escape(ph)+r'(?![A-Za-z0-9])',plain,re.I):
            if not any(not (m.end()<=a or m.start()>=b) for a,b in matches):
                matches.append((m.start(),m.end()))
            if len(matches)>=2:
                break
        if len(matches)>=2:
            break
    if not matches:
        candidates=[]
        for m in re.finditer(r"[A-Za-z0-9][A-Za-z0-9'\-]*",plain):
            w=m.group(0).lower().strip("'-")
            if w in STOP or len(w)<6:
                continue
            candidates.append((len(w),m.start(),m.end()))
        if candidates:
            _,a,b=max(candidates)
            matches=[(a,b)]
    out=[]; pos=0
    for a,b in sorted(matches):
        out.extend([esc(plain[pos:a]),'{\\c'+ACCENT+'}',esc(plain[a:b]),'{\\c'+BASE+'}'])
        pos=b
    out.append(esc(plain[pos:]))
    return ''.join(out)

def label_text(style,text):
    t=re.sub(r'\{[^}]*\}','',text)
    up=t.upper()
    color=BASE
    if 'RECONSTRUCTION' in up: color=RECON
    elif 'DOCUMENT' in up: color=GOLD
    elif 'CONCEPT' in up: color=CONCEPT
    elif 'ARCHIVE' in up: color=BLUE
    elif style=='Tag': color=GOLD
    return '{\\c'+color+'}'+esc(t)+'{\\c'+BASE+'}'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-ass',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    txt=Path(args.source_ass).read_text(encoding='utf-8',errors='replace')
    _,sep,events=txt.partition('[Events]')
    if not sep:
        raise SystemExit('ASS has no [Events] section')

    lines=[]
    for line in events.splitlines():
        if not line.startswith('Dialogue:'):
            continue
        p=line.split(',',9)
        if len(p)<10:
            continue
        style=p[3]
        s,e=ass_to_sec(p[1]),ass_to_sec(p[2])

        if style=='Cap':
            if s>=1225.45:
                continue
            e=min(e,1225.45)
            if e<=s:
                continue
            lines.append(
                f"Dialogue: 90,{sec_to_ass(s)},{sec_to_ass(e)},CapV10,,0,0,0,,{colorize(p[9])}"
            )
        elif style in {'Source','Document','Concept'} and s<1222.30:
            lines.append(
                f"Dialogue: 110,{p[1]},{p[2]},SourceV10,,0,0,0,,{label_text(style,p[9])}"
            )
        elif style=='Tag' and s<1222.30:
            lines.append(
                f"Dialogue: 105,{p[1]},{p[2]},TagV10,,0,0,0,,{label_text(style,p[9])}"
            )

    # Reinforce provenance on corrected reconstruction intervals.
    for s,e in [
        (215.356,221.464),(230.014,237.342),(709.241,717.165),
        (717.165,723.769),(730.373,736.976),(766.838,775.922),
        (815.287,822.857),(1020.122,1028.334),(1054.611,1062.822),
        (1107.164,1115.376)
    ]:
        lines.append(
            f"Dialogue: 120,{sec_to_ass(s)},{sec_to_ass(min(e,s+2.2))},SourceV10,,0,0,0,,"
            f"{{\\c{RECON}}}RECONSTRUCTION{{\\c{BASE}}}"
        )

    # Explicitly identify the clean replacement after the nuclear-concept beat.
    lines.append(
        f"Dialogue: 121,{sec_to_ass(717.24)},{sec_to_ass(720.16)},TagV10,,0,0,0,,"
        f"{{\\c{GOLD}}}ACTUAL TC-497 • GAS TURBINES{{\\c{BASE}}}"
    )

    out=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: CapV10,DejaVu Sans,58,{BASE},{BASE},&H00171A1C,&H20171A1C,-1,0,0,0,100,100,0,0,3,18,0,2,170,170,110,1
Style: SourceV10,DejaVu Sans,25,{BASE},{BASE},&H00171A1C,&H20171A1C,-1,0,0,0,100,100,1.4,0,3,10,0,9,52,52,38,1
Style: TagV10,DejaVu Sans,29,{BASE},{BASE},&H00171A1C,&H28171A1C,-1,0,0,0,100,100,0.8,0,3,10,0,7,76,76,92,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""+"\n".join(lines)+"\n"

    Path(args.output).write_text(out,encoding='utf-8')
    print(f'V10 overlay events: {len(lines)}')

if __name__=='__main__':
    main()
