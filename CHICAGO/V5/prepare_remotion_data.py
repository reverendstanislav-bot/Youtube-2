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
        for line in lines[2:]:
            for tok in re.findall(r"\S+",line):
                words.append({"w":tok,"n":norm(tok)})
        cues.append({"s":parse_time(a),"e":parse_time(b),"words":words})
    return cues

def load_voice(path):
    raw=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return [{"w":str(x.get("word","")).strip(),"n":norm(str(x.get("word",""))),"s":float(x["start"]),"e":float(x["end"])}
            for x in raw if norm(str(x.get("word","")))]

def align_captions(srt,voice):
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

PROCESS_COPY={
  "transfer":{
    0:("CHICAGO FREIGHT TUNNELS","SURFACE FREIGHT","MOVING CARGO INTO THE CITY","1 / 3"),
    1:("CHICAGO FREIGHT TUNNELS","TRANSFER / LOWERING","MOVING THE CITY BELOW GROUND","2 / 3"),
    2:("CHICAGO FREIGHT TUNNELS","TUNNEL CARS","DELIVERING FREIGHT BELOW GROUND","3 / 3"),
  },
  "coal":{
    0:("CHICAGO FREIGHT TUNNELS","COAL DELIVERY","FUEL MOVES BELOW THE CITY","1 / 3"),
    1:("CHICAGO FREIGHT TUNNELS","BOILERS / USE","POWERING THE BUILDINGS ABOVE","2 / 3"),
    2:("CHICAGO FREIGHT TUNNELS","ASH REMOVAL","THE RETURN LOAD","3 / 3"),
  },
  "basement":{
    0:("CHICAGO FREIGHT TUNNELS","TUNNEL CAR","THE LAST HUNDRED FEET","1 / 3"),
    1:("CHICAGO FREIGHT TUNNELS","BUILDING CONNECTION","FROM TUNNEL TO CUSTOMER","2 / 3"),
    2:("CHICAGO FREIGHT TUNNELS","BASEMENT","DELIVERY INSIDE THE BLOCK","3 / 3"),
  },
  "water":{
    0:("CHICAGO FREIGHT TUNNELS","RIVER WATER","WATER ENTERS THE NETWORK","1 / 3"),
    1:("CHICAGO FREIGHT TUNNELS","TUNNEL NETWORK","MOVING BENEATH THE STREETS","2 / 3"),
    2:("CHICAGO FREIGHT TUNNELS","BASEMENTS / UTILITIES","REACHING THE BUILDINGS ABOVE","3 / 3"),
  },
  "survivor":{
    0:("CHICAGO FREIGHT TUNNELS","LEFT UNDERGROUND","THE SYSTEM GOES QUIET","1 / 3"),
    1:("CHICAGO FREIGHT TUNNELS","RECOVERED","A MACHINE RETURNS TO LIGHT","2 / 3"),
    2:("CHICAGO FREIGHT TUNNELS","PRESERVED TODAY","THE SURVIVING EVIDENCE","3 / 3"),
  }
}

def add_card(cards,s,e,kicker,title,subline="",step="",kind="editorial",maxdur=4.8):
    if e<=s: return
    cards.append({
      "s":round(s,3),"e":round(min(e,s+maxdur),3),
      "kicker":kicker,"title":title,"subline":subline,"step":step,"kind":kind
    })

def build_cards(plan):
    cards=[]
    # Approved opening identity.
    add_card(cards,0.8,8.0,"A CHICAGO UNDERGROUND STORY","THE FREIGHT TUNNELS",
             "HIDDEN RAILS\nA DEEPER CHICAGO","1 / 4","hero",5.8)

    # Approved chapter treatment.
    add_card(cards,157.68,167.44,"CHAPTER 1","THE TELEPHONE ORIGINS",
             "2-FOOT GAUGE","","chapter",5.2)

    # Gauge gets a compact editorial technical beat later, not a gray schematic box.
    add_card(cards,189.92,203.48,"THE TELEPHONE ORIGINS","2-FOOT GAUGE",
             "NARROW-GAUGE RAILWAY","","fact",4.6)

    # One card at each phase boundary, not persistent UI for the whole sequence.
    grouped={}
    for s in plan:
        ex=s.get("explainer")
        if ex and ex!="gauge" and ex in PROCESS_COPY:
            grouped.setdefault(ex,{}).setdefault(int(s.get("phase",0)),[]).append(s)
    for ex,phases in grouped.items():
        for phase,segs in sorted(phases.items()):
            start=min(x["a"]/25 for x in segs); end=max(x["b"]/25 for x in segs)
            kicker,title,subline,step=PROCESS_COPY[ex][phase]
            add_card(cards,start,end,kicker,title,subline,step,"process",4.4)

    # Existing chapter / fact beats become restrained members of the same system,
    # excluding text already represented above.
    skip={"THE TELEPHONE ORIGINS","2-FOOT GAUGE","CHICAGO"}
    for s in plan:
        st=s["a"]/25; en=s["b"]/25
        if s.get("chapter") and s["chapter"] not in skip:
            add_card(cards,st,en,"CHAPTER",s["chapter"],"","","chapter",4.2)
        elif s.get("text") and not s.get("explainer") and s["text"] not in skip:
            txt=s["text"].strip()
            # Numeric/time/location facts stay compact but use the same visual language.
            add_card(cards,st,en,"CHICAGO FREIGHT TUNNELS",txt,"","","fact",3.4)

    cards.sort(key=lambda x:x["s"])
    return cards

def build_provenance(plan):
    out=[]
    for s in plan:
        kind=s.get("kind")
        if kind in ("archive","map","reconstruction"):
            st=s["a"]/25; en=s["b"]/25
            out.append({
              "s":st,"e":min(en,st+1.6),
              "label":"AI RECONSTRUCTION" if kind=="reconstruction" else "HISTORICAL SOURCE"
            })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--srt",required=True); ap.add_argument("--words",required=True)
    ap.add_argument("--plan",required=True); ap.add_argument("--captions-out",required=True)
    ap.add_argument("--overlays-out",required=True); ap.add_argument("--report",required=True)
    a=ap.parse_args()

    cues,ratio=align_captions(a.srt,load_voice(a.words))
    plan=json.loads(Path(a.plan).read_text(encoding="utf-8"))
    cards=build_cards(plan)
    data={"cards":cards,"provenance":build_provenance(plan)}

    Path(a.captions_out).write_text(json.dumps(cues,ensure_ascii=False),encoding="utf-8")
    Path(a.overlays_out).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    Path(a.report).write_text(json.dumps({
      "caption_cues":len(cues),
      "token_match_ratio":ratio,
      "editorial_cards":len(cards),
      "first_five":[x["title"] for x in cards[:5]]
    },ensure_ascii=False,indent=2),encoding="utf-8")
    if ratio<0.95: raise SystemExit("caption token match below 95%")

if __name__=="__main__": main()
