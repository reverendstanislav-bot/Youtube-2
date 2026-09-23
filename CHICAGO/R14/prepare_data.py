#!/usr/bin/env python3
import argparse, importlib.util, json, re
from pathlib import Path

END_START=1268.0

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def load_voice(path):
    raw=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    out=[]
    for x in raw:
        w=str(x.get("word","")).strip()
        if not w:
            continue
        s=float(x["start"]); e=float(x["end"])
        if s>=END_START:
            break
        out.append({"w":w,"s":s,"e":min(e,END_START)})
    return out

def build_captions(words):
    cues=[]; buf=[]
    def flush():
        nonlocal buf
        if not buf: return
        cues.append({"s":buf[0]["s"],"e":min(END_START,buf[-1]["e"]+0.08),"words":buf})
        buf=[]
    for i,w in enumerate(words):
        if buf:
            pause=w["s"]-buf[-1]["e"]
            if pause>0.42:
                flush()
        buf.append(dict(w))
        span=buf[-1]["e"]-buf[0]["s"]
        chars=sum(len(x["w"])+1 for x in buf)
        punct=bool(re.search(r'[.!?]$',w["w"]))
        comma=bool(re.search(r'[,;:]$',w["w"]))
        if len(buf)>=7 or chars>=42 or span>=2.35 or (punct and len(buf)>=3) or (comma and len(buf)>=5):
            flush()
    flush()
    return cues

def thin_cards(cards):
    # Keep the existing visual language but remove card spam: chapter/process beats
    # always stay, generic facts get at least 16 s separation.
    out=[]; last_fact=-999
    for c in sorted(cards,key=lambda x:x["s"]):
        kind=c.get("kind","editorial")
        if kind in {"hero","chapter","process"}:
            out.append(c); continue
        if c["s"]-last_fact>=16:
            out.append(c); last_fact=c["s"]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--words",required=True)
    ap.add_argument("--base-plan",required=True)
    ap.add_argument("--v12-script",required=True)
    ap.add_argument("--captions-out",required=True)
    ap.add_argument("--overlays-out",required=True)
    ap.add_argument("--report",required=True)
    a=ap.parse_args()

    words=load_voice(a.words)
    cues=build_captions(words)
    plan=json.loads(Path(a.base_plan).read_text(encoding="utf-8"))
    v12=load_module(a.v12_script,"v12data")
    cards=thin_cards(v12.build_cards(plan))

    Path(a.captions_out).write_text(json.dumps(cues,ensure_ascii=False),encoding="utf-8")
    Path(a.overlays_out).write_text(json.dumps({"cards":cards},ensure_ascii=False,indent=2),encoding="utf-8")
    timed_words=[w for c in cues for w in c["words"]]
    exact=(len(timed_words)==len(words) and all(abs(a["s"]-b["s"])<1e-6 and abs(a["e"]-b["e"])<0.081 for a,b in zip(timed_words,words)))
    report={
        "captionSource":"word-level transcript",
        "voiceWords":len(words),
        "captionWords":len(timed_words),
        "wordCoverageRatio":round(len(timed_words)/max(1,len(words)),6),
        "exactWordSequence":exact,
        "captionCues":len(cues),
        "editorialCards":len(cards),
        "status":"PASS" if exact and len(timed_words)==len(words) else "FAIL"
    }
    Path(a.report).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    if report["status"]!="PASS":
        raise SystemExit("caption word-level coverage failed")

if __name__=="__main__":
    main()
