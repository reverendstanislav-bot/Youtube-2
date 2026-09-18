import json,re,os
from pathlib import Path

PUB=Path(os.environ["FULL_PUBLIC"])
OUT=Path(os.environ.get("ASS_OUT","/tmp/tc497full/overlay.ass"))
caps=json.loads((PUB/"captions.json").read_text(encoding="utf-8"))
events=json.loads((PUB/"events.json").read_text(encoding="utf-8"))

def ts(x):
    h=int(x//3600); x-=h*3600
    m=int(x//60); x-=m*60
    return f"{h}:{m:02d}:{x:05.2f}"

R="&H003552A5&" # rust in BGR
P="&H00C8DDE6&" # paper
keywords={"572","54","150","20","400","12-foot","12-ft","1963","1968","nuclear","helicopter","helicopters","worked","scrapped","sky","otter","yuma"}

def phrase_text(p):
    arr=[]
    for w in p["words"]:
        raw=w["w"]
        clean=re.sub(r'''[.,!?;:()"']''',"",raw).lower()
        if clean in keywords:
            arr.append(r"{\c"+R+"}"+raw+r"{\c"+P+"}")
        else:
            arr.append(raw)
    return " ".join(arr).replace("\n"," ")

with open(OUT,"w",encoding="utf-8") as f:
    f.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,DejaVu Sans,26,&H00C8DDE6,&H00C8DDE6,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,0,0,1,3,0,2,72,72,27,1
Style: Chapter,DejaVu Sans,28,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,3,0,7,46,46,38,1
Style: Kicker,DejaVu Sans,11,&H003552A5,&H003552A5,&H00171A1C,&H00000000,-1,0,0,0,100,100,2,0,1,1,0,7,46,46,66,1
Style: Bug,DejaVu Sans,11,&H00171A1C,&H00171A1C,&H00E6DDC8,&H80E6DDC8,-1,0,0,0,100,100,1,0,3,5,0,9,28,28,24,1
Style: Concept,DejaVu Sans,11,&H00EBF3F3,&H00EBF3F3,&H003552A5,&H803552A5,-1,0,0,0,100,100,1,0,3,5,0,9,28,28,24,1
Style: Hero,DejaVu Sans,40,&H00DDEBF3,&H00DDEBF3,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,55,55,0,1
Style: HeroRust,DejaVu Sans,40,&H003552A5,&H003552A5,&H00171A1C,&H50171A1C,-1,0,0,0,100,100,1,0,1,4,0,5,55,55,0,1
Style: End,DejaVu Sans,32,&H00171A1C,&H00171A1C,&H00E6DDC8,&H00E6DDC8,-1,0,0,0,100,100,1,0,1,1,0,7,55,430,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    # captions only after V14 boundary
    for p in caps:
        if p["e"]<=82.6: continue
        f.write(f"Dialogue: 10,{ts(max(82.6,p['s']))},{ts(p['e'])},Sub,,0,0,0,,{{\\fad(45,65)}}{phrase_text(p)}\n")
    for e in events["chapters"]:
        f.write(f"Dialogue: 20,{ts(e['s'])},{ts(e['e'])},Kicker,,0,0,0,,{{\\fad(100,160)}}HIDDEN INDUSTRIAL AMERICA\n")
        f.write(f"Dialogue: 20,{ts(e['s']+.08)},{ts(e['e'])},Chapter,,0,0,0,,{{\\fad(100,160)}}{e['text'].upper()}\n")
    for e in events["bugs"]:
        style="Concept" if e["text"]=="CONCEPT" else "Bug"
        f.write(f"Dialogue: 18,{ts(e['s'])},{ts(e['e'])},{style},,0,0,0,,{{\\fad(70,100)}}{e['text']}\n")

    f.write(f"Dialogue: 30,{ts(1088.4)},{ts(1092.0)},Hero,,0,0,0,,{{\\fad(180,120)}}IT WASN'T DEFEATED BY THE DESERT.\n")
    f.write(f"Dialogue: 31,{ts(1092.0)},{ts(1095.7)},HeroRust,,0,0,0,,{{\\fad(120,180)}}IT WAS DEFEATED BY THE SKY.\n")
    f.write(f"Dialogue: 30,{ts(1228.1)},{ts(1232.1)},End,,0,0,0,,{{\\pos(55,115)\\fad(160,100)}}HIDDEN INDUSTRIAL AMERICA\\NTHE MACHINE WORKED.\n")
    f.write(f"Dialogue: 31,{ts(1232.1)},{ts(1236.3)},End,,0,0,0,,{{\\pos(55,115)\\c&H003552A5&\\fad(100,220)}}HIDDEN INDUSTRIAL AMERICA\\NTHE WORLD MOVED ON.\n")

print(OUT)
