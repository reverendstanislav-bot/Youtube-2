#!/usr/bin/env python3
import argparse, json, re, difflib
from pathlib import Path

BASE='&H00FFFFFF&'
ORANGE='&H003A8AF2&'
DARK='&H00171A1C&'

TOKEN_RE=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?")

def norm(s):
    return ''.join(ch.lower() for ch in s.replace('’',"'") if ch.isalnum())

def sec_ass(t):
    t=max(0.0,float(t))
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def parse_srt_time(s):
    h,m,rest=s.replace('.',',').split(':')
    ss,ms=rest.split(',')
    return int(h)*3600+int(m)*60+int(ss)+int(ms[:3].ljust(3,'0'))/1000

def esc(s):
    return s.replace('\\','\\\\').replace('{','\\{').replace('}','\\}')

def load_srt(path):
    text=Path(path).read_text(encoding='utf-8-sig',errors='replace').strip()
    cues=[]
    for block in re.split(r'\n\s*\n',text):
        lines=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(lines)<3 or '-->' not in lines[1]:
            continue
        a,b=[x.strip() for x in lines[1].split('-->',1)]
        cue_lines=lines[2:]
        display=[]
        for li,line in enumerate(cue_lines):
            if li: display.append({'raw':'\\N','norm':'','newline':True})
            for tok in re.findall(r'\S+',line):
                display.append({'raw':tok,'norm':norm(tok),'newline':False})
        cues.append({'start':parse_srt_time(a),'end':parse_srt_time(b),'lines':cue_lines,'display':display})
    return cues

def load_words(path):
    raw=json.loads(Path(path).read_text(encoding='utf-8-sig',errors='replace'))
    out=[]
    for w in raw:
        token=norm(str(w.get('word','')))
        if token:
            out.append({'start':float(w['start']),'end':float(w['end']),'raw':str(w.get('word','')).strip(),'norm':token})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--srt',required=True)
    ap.add_argument('--words',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    cues=load_srt(args.srt)
    words=load_words(args.words)

    flat=[]
    refs=[]
    for ci,c in enumerate(cues):
        for di,d in enumerate(c['display']):
            if not d['newline'] and d['norm']:
                flat.append(d['norm']); refs.append((ci,di))

    sm=difflib.SequenceMatcher(None,flat,[w['norm'] for w in words],autojunk=False)
    mapping={}
    for a,b,n in sm.get_matching_blocks():
        for k in range(n):
            mapping[a+k]=b+k

    cue_wordmap=[{} for _ in cues]
    for fi,(ci,di) in enumerate(refs):
        if fi in mapping:
            cue_wordmap[ci][di]=mapping[fi]

    events=[]
    matched=0
    total=0
    for ci,c in enumerate(cues):
        mapped=cue_wordmap[ci]
        token_indices=[i for i,d in enumerate(c['display']) if not d['newline'] and d['norm']]
        total += len(token_indices)
        matched += sum(i in mapped for i in token_indices)

        active_candidates=[i for i in token_indices if i in mapped]
        if not active_candidates:
            txt=' '.join(c['lines'])
            events.append(f"Dialogue: 90,{sec_ass(c['start'])},{sec_ass(c['end'])},Run,,0,0,0,,{esc(txt)}")
            continue

        for pos,di in enumerate(active_candidates):
            wi=mapped[di]
            s=max(c['start'],words[wi]['start'])
            if pos+1<len(active_candidates):
                e=min(c['end'],words[mapped[active_candidates[pos+1]]]['start'])
            else:
                e=min(c['end'],max(words[wi]['end'],s+0.08))
            if e<=s:
                e=min(c['end'],s+0.08)
            if e<=s:
                continue

            parts=[]
            for j,d in enumerate(c['display']):
                if d['newline']:
                    parts.append('\\N')
                else:
                    tok=esc(d['raw'])
                    if j==di:
                        tok='{\\c'+ORANGE+'}'+tok+'{\\c'+BASE+'}'
                    parts.append(tok)
            line=''
            for p in parts:
                if p=='\\N':
                    line=line.rstrip()+'\\N'
                else:
                    if line and not line.endswith('\\N'):
                        line+=' '
                    line+=p
            events.append(f"Dialogue: 90,{sec_ass(s)},{sec_ass(e)},Run,,0,0,0,,{line}")

        first_di=active_candidates[0]
        first_w=words[mapped[first_di]]
        if c['start'] < first_w['start']-0.03:
            txt='\\N'.join(esc(x) for x in c['lines'])
            events.append(f"Dialogue: 89,{sec_ass(c['start'])},{sec_ass(min(c['end'],first_w['start']))},Run,,0,0,0,,{txt}")

    events.sort(key=lambda x: float(x.split(',')[1].split(':')[-1]) if False else 0)

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

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""+'\n'.join(events)+'\n'

    Path(args.output).write_text(out,encoding='utf-8')
    ratio=matched/max(1,total)
    print(json.dumps({'cues':len(cues),'voice_words':len(words),'mapped_display_tokens':matched,'display_tokens':total,'match_ratio':ratio,'events':len(events)},indent=2))
    if ratio<0.95:
        raise SystemExit('Token alignment ratio below 95%')

if __name__=='__main__':
    main()
