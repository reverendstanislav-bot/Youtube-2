#!/usr/bin/env python3
import argparse, difflib, json, re
from pathlib import Path

def norm(s):
    return ''.join(ch.lower() for ch in s.replace("’","'") if ch.isalnum())

def parse_time(s):
    h,m,rest=s.replace(".",",").split(":"); sec,ms=rest.split(",")
    return int(h)*3600+int(m)*60+int(sec)+int(ms[:3].ljust(3,"0"))/1000

def parse_srt(path):
    text=Path(path).read_text(encoding="utf-8-sig",errors="replace").strip()
    cues=[]
    for block in re.split(r"\n\s*\n",text):
        lines=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(lines)<3 or "-->" not in lines[1]: continue
        a,b=[x.strip() for x in lines[1].split("-->",1)]
        words=[]
        for li,line in enumerate(lines[2:]):
            for tok in re.findall(r"\S+",line):
                words.append({"w":tok,"n":norm(tok)})
        cues.append({"s":parse_time(a),"e":parse_time(b),"words":words})
    return cues

def load_voice(path):
    raw=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return [{"w":str(x.get("word","")).strip(),"n":norm(str(x.get("word",""))),"s":float(x["start"]),"e":float(x["end"])} for x in raw if norm(str(x.get("word","")))]

def captions(srt,voice):
    cues=parse_srt(srt); flat=[]; refs=[]
    for ci,c in enumerate(cues):
        for wi,w in enumerate(c["words"]):
            flat.append(w["n"]); refs.append((ci,wi))
    sm=difflib.SequenceMatcher(None,flat,[x["n"] for x in voice],autojunk=False)
    mp={}
    for a,b,n in sm.get_matching_blocks():
        for k in range(n): mp[a+k]=b+k
    for fi,(ci,wi) in enumerate(refs):
        c=cues[ci]; w=c["words"][wi]
        if fi in mp:
            vw=voice[mp[fi]]; w["s"]=vw["s"]; w["e"]=vw["e"]
        else:
            prev=[x for x in range(fi-1,-1,-1) if x in mp]
            nxt=[x for x in range(fi+1,len(flat)) if x in mp]
            lo=voice[mp[prev[0]]]["e"] if prev else c["s"]
            hi=voice[mp[nxt[0]]]["s"] if nxt else c["e"]
            w["s"]=max(c["s"],lo); w["e"]=min(c["e"],max(lo+.08,hi))
    return cues, len(mp)/max(1,len(flat))

def build_overlays(plan):
    info=[]; provenance=[]; processes={}
    label_map={
      "transfer":["SURFACE FREIGHT","TRANSFER / LOWERING","TUNNEL CARS"],
      "coal":["COAL DELIVERY","BOILERS / USE","ASH REMOVAL"],
      "basement":["TUNNEL CAR","BUILDING CONNECTION","BASEMENT"],
      "water":["RIVER WATER","TUNNEL NETWORK","BASEMENTS / UTILITIES"],
      "survivor":["LEFT UNDERGROUND","RECOVERED","PRESERVED TODAY"],
    }
    for s in plan:
        st=s["a"]/25; en=s["b"]/25
        if s.get("chapter"):
            info.append({"s":st,"e":min(en,st+4.0),"text":s["chapter"],"type":"chapter"})
        elif s.get("text") and not s.get("explainer"):
            info.append({"s":st,"e":min(en,st+3.2),"text":s["text"],"type":"info"})
        kind=s.get("kind")
        if kind in ("archive","map","reconstruction"):
            provenance.append({"s":st,"e":min(en,st+1.8),"label":"AI RECONSTRUCTION" if kind=="reconstruction" else "HISTORICAL SOURCE"})
        ex=s.get("explainer")
        if ex and ex!="gauge":
            processes.setdefault(ex,[]).append({"s":st,"e":en,"phase":int(s.get("phase",0))})
    return {
      "info":info,
      "provenance":provenance,
      "gauge":{"s":189.92,"e":203.48},
      "processes":[{"name":name,"labels":label_map[name],"segments":segs} for name,segs in processes.items() if name in label_map]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--srt",required=True); ap.add_argument("--words",required=True)
    ap.add_argument("--plan",required=True); ap.add_argument("--captions-out",required=True)
    ap.add_argument("--overlays-out",required=True); ap.add_argument("--report",required=True)
    a=ap.parse_args()
    cues,ratio=captions(a.srt,load_voice(a.words))
    plan=json.loads(Path(a.plan).read_text(encoding="utf-8"))
    ov=build_overlays(plan)
    Path(a.captions_out).write_text(json.dumps(cues,ensure_ascii=False),encoding="utf-8")
    Path(a.overlays_out).write_text(json.dumps(ov,ensure_ascii=False),encoding="utf-8")
    Path(a.report).write_text(json.dumps({"caption_cues":len(cues),"token_match_ratio":ratio,"info_overlays":len(ov["info"]),"provenance_overlays":len(ov["provenance"]),"processes":[x["name"] for x in ov["processes"]]},indent=2),encoding="utf-8")
    if ratio<0.95: raise SystemExit("caption token match below 95%")

if __name__=="__main__": main()
