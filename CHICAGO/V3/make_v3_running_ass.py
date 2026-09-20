#!/usr/bin/env python3
import argparse, json, re, difflib
from pathlib import Path

BASE='&H00FFFFFF&'
ORANGE='&H003A8AF2&'
DARK='&H00171A1C&'
END_TOP=1270.0

def norm(s):
    return ''.join(ch.lower() for ch in s.replace('’',"'") if ch.isalnum())

def sec_ass(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    return f"{h}:{m:02d}:{t:05.2f}"

def parse_time(s):
    h,m,rest=s.replace('.',',').split(':'); ss,ms=rest.split(',')
    return int(h)*3600+int(m)*60+int(ss)+int(ms[:3].ljust(3,'0'))/1000

def esc(s):
    return s.replace('\\','\\\\').replace('{','\\{').replace('}','\\}')

def load_srt(path):
    text=Path(path).read_text(encoding='utf-8-sig',errors='replace').strip()
    cues=[]
    for block in re.split(r'\n\s*\n',text):
        lines=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(lines)<3 or '-->' not in lines[1]: continue
        a,b=[x.strip() for x in lines[1].split('-->',1)]
        display=[]
        for li,line in enumerate(lines[2:]):
            if li: display.append({'raw':'\\N','norm':'','newline':True})
            for tok in re.findall(r'\S+',line):
                display.append({'raw':tok,'norm':norm(tok),'newline':False})
        cues.append({'start':parse_time(a),'end':parse_time(b),'lines':lines[2:],'display':display})
    return cues

def load_words(path):
    raw=json.loads(Path(path).read_text(encoding='utf-8-sig',errors='replace'))
    out=[]
    for w in raw:
        n=norm(str(w.get('word','')))
        if n: out.append({'start':float(w['start']),'end':float(w['end']),'norm':n})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--srt',required=True)
    ap.add_argument('--words',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    cues=load_srt(args.srt); words=load_words(args.words)
    flat=[]; refs=[]
    for ci,c in enumerate(cues):
        for di,d in enumerate(c['display']):
            if not d['newline'] and d['norm']:
                flat.append(d['norm']); refs.append((ci,di))
    sm=difflib.SequenceMatcher(None,flat,[w['norm'] for w in words],autojunk=False)
    mapping={}
    for a,b,n in sm.get_matching_blocks():
        for k in range(n): mapping[a+k]=b+k
    cue_map=[{} for _ in cues]
    for fi,(ci,di) in enumerate(refs):
        if fi in mapping: cue_map[ci][di]=mapping[fi]

    events=[]; mapped=0
    for ci,c in enumerate(cues):
        style='RunEnd' if c['start']>=END_TOP else 'Run'
        active=[di for di,d in enumerate(c['display']) if not d['newline'] and d['norm'] and di in cue_map[ci]]
        mapped += len(active)
        if not active:
            txt='\\N'.join(esc(x) for x in c['lines'])
            events.append((c['start'],f"Dialogue: 90,{sec_ass(c['start'])},{sec_ass(c['end'])},{style},,0,0,0,,{txt}"))
            continue
        first_word=words[cue_map[ci][active[0]]]
        if c['start'] < first_word['start']-.03:
            txt='\\N'.join(esc(x) for x in c['lines'])
            events.append((c['start'],f"Dialogue: 89,{sec_ass(c['start'])},{sec_ass(min(c['end'],first_word['start']))},{style},,0,0,0,,{txt}"))
        for pos,di in enumerate(active):
            wi=cue_map[ci][di]
            s=max(c['start'],words[wi]['start'])
            e=min(c['end'],words[cue_map[ci][active[pos+1]]]['start'] if pos+1<len(active) else max(words[wi]['end'],s+.08))
            if e<=s: continue
            parts=[]
            for j,d in enumerate(c['display']):
                if d['newline']: parts.append('\\N'); continue
                tok=esc(d['raw'])
                if j==di: tok='{\\c'+ORANGE+'}'+tok+'{\\c'+BASE+'}'
                parts.append(tok)
            line=''
            for p in parts:
                if p=='\\N': line=line.rstrip()+'\\N'
                else:
                    if line and not line.endswith('\\N'): line+=' '
                    line+=p
            events.append((s,f"Dialogue: 90,{sec_ass(s)},{sec_ass(e)},{style},,0,0,0,,{line}"))
    events.sort(key=lambda x:x[0])

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
Style: RunEnd,DejaVu Sans,27,{BASE},{ORANGE},{DARK},&H00000000,-1,0,0,0,100,100,0,0,1,2.8,1.0,8,72,72,105,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""+'\n'.join(x[1] for x in events)+'\n'
    Path(args.output).write_text(out,encoding='utf-8')
    print(json.dumps({'cues':len(cues),'mapped_tokens':mapped,'total_tokens':len(flat),'ratio':mapped/max(1,len(flat)),'events':len(events),'end_top_from':END_TOP},indent=2))

if __name__=='__main__': main()
