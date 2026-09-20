#!/usr/bin/env python3
import argparse,csv,re
from pathlib import Path

BASE='&H003D6FB9&'      # muted orange RGB #B96F3D
ORANGE='&H003A8AF2&'    # bright orange RGB #F28A3A
LABEL_BASE='&H00DDEBF3&' # warm ivory for non-dialogue labels only
DARK='&H00171A1C&'

PATCHES=[
    (215.356,221.464,'RECONSTRUCTION',''),
    (709.241,716.900,'RECONSTRUCTION',''),
    (716.900,724.500,'RECONSTRUCTION','ACTUAL TC-497 • GAS TURBINES'),
    (730.373,736.976,'CONCEPT • PROPOSED / UNBUILT',''),
    (766.838,775.922,'RECONSTRUCTION',''),
    (815.287,822.857,'RECONSTRUCTION',''),
    (1020.122,1028.334,'RECONSTRUCTION',''),
    (1054.611,1062.822,'RECONSTRUCTION',''),
    (1079.245,1087.457,'RECONSTRUCTION',''),
    (1107.164,1115.376,'RECONSTRUCTION',''),
    (1209.007,1215.477,'RECONSTRUCTION',''),
]
CAP_START=82.600
CTA_CUT=1225.450
END=1236.533333
END_PLATE=1222.300

def sec_ass(t):
    t=max(0.0,float(t)); h=int(t//3600); t-=h*3600; m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def ass_sec(s):
    h,m,ss=s.split(':')
    return int(h)*3600+int(m)*60+float(ss)

def clean_text(s):
    s=re.sub(r'\{[^}]*\}','',s)
    return s.replace('{','').replace('}','').strip()

def esc(s):
    return s.replace('\\','\\\\').replace('{','\\{').replace('}','\\}')

def normalize_word(s):
    fixes={
      'TC - 497':'TC-497','TC -497':'TC-497','TC- 497':'TC-497',
      'CH - 54':'CH-54','S - 64':'S-64'
    }
    for a,b in fixes.items(): s=s.replace(a,b)
    return s

def load_words(path):
    out=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            s=float(r['start_sec']); e=float(r['end_sec']); w=normalize_word(r['word'].strip())
            if e<=CAP_START or s>=CTA_CUT: continue
            out.append({'s':max(s,CAP_START),'e':min(e,CTA_CUT),'w':w})
    return out

def make_phrases(words):
    phrases=[]; buf=[]
    for w in words:
        if not buf:
            buf=[w]; continue
        candidate=buf+[w]
        span=candidate[-1]['e']-candidate[0]['s']
        chars=sum(len(x['w'])+1 for x in candidate)
        prev_punct=bool(re.search(r'[.!?;:]$',buf[-1]['w']))
        if len(candidate)>7 or chars>48 or span>2.75 or (prev_punct and len(buf)>=3):
            phrases.append(buf); buf=[w]
        else:
            buf.append(w)
    if buf: phrases.append(buf)
    return phrases

def active_line(words,idx):
    parts=[]
    for i,w in enumerate(words):
        token=esc(w['w'])
        if i==idx:
            token='{\\c'+ORANGE+'}'+token+'{\\c'+BASE+'}'
        parts.append(token)
    return ' '.join(parts)

def overlaps_any(s,e):
    for a,b,_,_ in PATCHES:
        if min(e,b)>max(s,a):
            return True
    return False

def prov_text(text):
    t=clean_text(text)
    m=re.match(r'^(ARCHIVE|DOCUMENT|RECONSTRUCTION|CONCEPT)\b(.*)$',t,re.I)
    if m:
        return '{\\c'+ORANGE+'}'+m.group(1).upper()+'{\\c'+LABEL_BASE+'}'+esc(m.group(2))
    return '{\\c'+LABEL_BASE+'}'+esc(t)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--words',required=True)
    ap.add_argument('--source-ass',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    words=load_words(args.words)
    phrases=make_phrases(words)

    events=[]
    for pi,ph in enumerate(phrases):
        next_phrase_s = phrases[pi+1][0]['s'] if pi+1 < len(phrases) else CTA_CUT
        phrase_end = min(CTA_CUT, ph[-1]['e'] + .04, next_phrase_s - .02)
        for i,w in enumerate(ph):
            s=max(w['s'],CAP_START)
            raw_e = ph[i+1]['s'] if i+1<len(ph) else phrase_end
            e=min(raw_e, phrase_end, CTA_CUT)
            if e<=s:
                continue
            events.append(
                f"Dialogue: 90,{sec_ass(s)},{sec_ass(e)},Run,,0,0,0,,{active_line(ph,i)}"
            )

    # Preserve provenance/editorial labels from the V4 overlay, but never its old captions.
    txt=Path(args.source_ass).read_text(encoding='utf-8',errors='replace')
    _,sep,ev=txt.partition('[Events]')
    if sep:
        for line in ev.splitlines():
            if not line.startswith('Dialogue:'): continue
            p=line.split(',',9)
            if len(p)<10: continue
            style=p[3]
            if style=='Cap': continue
            s=ass_sec(p[1]); e=ass_sec(p[2])
            if e<=CAP_START or s>=END_PLATE: continue
            s=max(s,CAP_START); e=min(e,END_PLATE)
            if e<=s or overlaps_any(s,e): continue
            outstyle='V13Tag' if style=='Tag' else 'V13Prov'
            events.append(
                f"Dialogue: 110,{sec_ass(s)},{sec_ass(e)},{outstyle},,0,0,0,,{prov_text(p[9])}"
            )

    for s,e,label,tag in PATCHES:
        le=min(e,s+2.25)
        events.append(
            f"Dialogue: 120,{sec_ass(s+.12)},{sec_ass(le)},V13Prov,,0,0,0,,{prov_text(label)}"
        )
        if tag:
            events.append(
                f"Dialogue: 121,{sec_ass(s+.28)},{sec_ass(min(e,s+3.0))},V13Tag,,0,0,0,,{{\\c{ORANGE}}}{esc(tag)}{{\\c{LABEL_BASE}}}"
            )

    # Restrained V8 end identity, no subscribe caption after CTA_CUT.
    events += [
      f"Dialogue: 70,{sec_ass(END_PLATE)},{sec_ass(END)},V13Brand,,0,0,0,,{{\\fad(600,350)}}HIDDEN INDUSTRIAL AMERICA",
      f"Dialogue: 71,{sec_ass(1223.00)},{sec_ass(END)},V13Hero,,0,0,0,,{{\\fad(750,350)}}TC-497",
      f"Dialogue: 72,{sec_ass(1223.65)},{sec_ass(END)},V13Sub,,0,0,0,,{{\\fad(850,350)}}OVERLAND TRAIN",
    ]

    events.sort(key=lambda line: ass_sec(line.split(',',3)[1]))

    out=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Run,DejaVu Sans,29,{BASE},{ORANGE},{DARK},&H00000000,-1,0,0,0,100,100,0,0,1,2.8,1.0,2,64,64,28,1
Style: V13Prov,DejaVu Sans,17,{LABEL_BASE},{LABEL_BASE},{DARK},&H00000000,-1,0,0,0,100,100,1.0,0,1,1.6,0.6,9,28,28,24,1
Style: V13Tag,DejaVu Sans,18,{LABEL_BASE},{LABEL_BASE},{DARK},&H00000000,-1,0,0,0,100,100,.6,0,1,1.6,.6,7,34,34,48,1
Style: V13Brand,DejaVu Sans,15,&H00171A1C,&H00171A1C,&H50F3EBDD,&H00000000,-1,0,0,0,100,100,1.7,0,1,.8,0,7,66,66,52,1
Style: V13Hero,DejaVu Sans,43,&H00171A1C,&H00171A1C,&H40F3EBDD,&H00000000,-1,0,0,0,100,100,.6,0,1,1.0,0,7,66,66,84,1
Style: V13Sub,DejaVu Sans,14,&H002E3234,&H002E3234,&H50F3EBDD,&H00000000,0,0,0,0,100,100,1.0,0,1,.6,0,7,68,68,146,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""+'\n'.join(events)+'\n'

    Path(args.output).write_text(out,encoding='utf-8')
    print('phrases',len(phrases),'events',len(events))

if __name__=='__main__':
    main()
