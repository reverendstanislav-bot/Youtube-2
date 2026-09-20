#!/usr/bin/env python3
import argparse, difflib, json, math, re, statistics
from pathlib import Path

TOKEN_RE=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?")

def toks(s):
    return [x.lower().replace("’","'").replace("'","") for x in TOKEN_RE.findall(s)]

def parse_time(s):
    h,m,rest=s.replace(".",",").split(":")
    sec,ms=rest.split(",")
    return int(h)*3600+int(m)*60+int(sec)+int(ms[:3].ljust(3,"0"))/1000

def parse_srt(path):
    text=Path(path).read_text(encoding="utf-8-sig",errors="replace").strip()
    cues=[]
    for block in re.split(r"\n\s*\n",text):
        lines=[x.rstrip() for x in block.splitlines() if x.strip()]
        if len(lines)<2: continue
        ti=1 if re.fullmatch(r"\d+",lines[0].strip()) else 0
        if ti>=len(lines) or "-->" not in lines[ti]: continue
        a,b=[x.strip() for x in lines[ti].split("-->",1)]
        cue_text=" ".join(lines[ti+1:])
        cues.append({"start":parse_time(a),"end":parse_time(b),"text":cue_text,"tokens":toks(cue_text)})
    return cues

def percentile(vals,p):
    if not vals: return None
    xs=sorted(vals)
    if len(xs)==1: return xs[0]
    pos=(len(xs)-1)*p
    lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi:return xs[lo]
    return xs[lo]*(hi-pos)+xs[hi]*(pos-lo)

def slope(xs,ys):
    if len(xs)<2:return 0.0
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    den=sum((x-mx)**2 for x in xs)
    return 0.0 if den==0 else sum((x-mx)*(y-my) for x,y in zip(xs,ys))/den

def analyze(srt_path, words_path):
    cues=parse_srt(srt_path)
    raw=json.loads(Path(words_path).read_text(encoding="utf-8-sig",errors="replace"))
    voice=[]
    for w in raw:
        ts=toks(str(w.get("word","")))
        for t in ts:
            voice.append({"token":t,"start":float(w["start"]),"end":float(w["end"])})
    flat=[]; cue_ranges=[]
    for ci,c in enumerate(cues):
        st=len(flat); flat.extend(c["tokens"]); cue_ranges.append((st,len(flat)))
    sm=difflib.SequenceMatcher(None,flat,[w["token"] for w in voice],autojunk=False)
    mapping={}
    matched=0
    for a,b,n in sm.get_matching_blocks():
        for k in range(n):
            mapping[a+k]=b+k
            matched+=1
    rows=[]
    for ci,c in enumerate(cues):
        a,b=cue_ranges[ci]
        vis=[mapping[i] for i in range(a,b) if i in mapping]
        if not vis: continue
        starts=[voice[j]["start"] for j in vis]; ends=[voice[j]["end"] for j in vis]
        actual_start=min(starts); actual_end=max(ends)
        rows.append({
          "cue":ci+1,"srt_start":c["start"],"srt_end":c["end"],
          "voice_start":actual_start,"voice_end":actual_end,
          "start_offset_sec":c["start"]-actual_start,
          "end_offset_sec":c["end"]-actual_end,
          "text":c["text"][:180],
          "mapped_tokens":len(vis),"cue_tokens":max(1,b-a)
        })
    offs=[r["start_offset_sec"] for r in rows]
    xs=[r["voice_start"] for r in rows]
    dur=max(xs) if xs else 0
    sl=slope(xs,offs)
    spread=(percentile(offs,.95)-percentile(offs,.05)) if offs else None
    samples=[]
    if rows:
        for q in [0,.1,.25,.5,.75,.9,1]:
            target=dur*q
            r=min(rows,key=lambda z:abs(z["voice_start"]-target))
            samples.append(r)
    return {
      "srt":str(srt_path),
      "cue_count":len(cues),
      "voice_token_count":len(voice),
      "srt_token_count":len(flat),
      "matched_token_ratio": matched/max(1,len(flat)),
      "aligned_cues":len(rows),
      "start_offset_sec":{
        "median":statistics.median(offs) if offs else None,
        "p05":percentile(offs,.05),"p95":percentile(offs,.95),
        "min":min(offs) if offs else None,"max":max(offs) if offs else None,
        "spread_p05_p95":spread
      },
      "offset_slope_sec_per_sec":sl,
      "estimated_offset_change_over_runtime_sec":sl*dur,
      "samples":samples,
      "rows":rows
    }

def verdict(d):
    o=d["start_offset_sec"]; drift=abs(d["estimated_offset_change_over_runtime_sec"] or 0)
    med=abs(o["median"] or 0); spread=abs(o["spread_p05_p95"] or 0)
    issues=[]
    if drift>0.5: issues.append(f"progressive drift ~{drift:.2f}s across runtime")
    if med>0.5: issues.append(f"global median offset {o['median']:.2f}s")
    if spread>1.0: issues.append(f"variable offset spread {spread:.2f}s")
    if d["matched_token_ratio"]<0.9: issues.append(f"low text match {d['matched_token_ratio']:.1%}")
    return "PASS" if not issues else "FAIL: "+"; ".join(issues)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--words",required=True)
    ap.add_argument("--srt",action="append",required=True)
    ap.add_argument("--out-json",required=True)
    ap.add_argument("--out-md",required=True)
    a=ap.parse_args()
    results=[analyze(p,a.words) for p in a.srt]
    for d in results:d["verdict"]=verdict(d)
    Path(a.out_json).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Chicago independent subtitle ↔ VO timing audit","",
           "Offsets are measured as **SRT cue start minus matched spoken-word start**. Positive = subtitle starts late.",""]
    for d in results:
        o=d["start_offset_sec"]
        lines += [f"## {Path(d['srt']).name}",
          f"- Verdict: **{d['verdict']}**",
          f"- Cues: {d['cue_count']}; aligned: {d['aligned_cues']}",
          f"- Text-token match: {d['matched_token_ratio']:.2%}",
          f"- Median start offset: {o['median']:.3f} s",
          f"- P05 / P95: {o['p05']:.3f} / {o['p95']:.3f} s",
          f"- Offset spread P05→P95: {o['spread_p05_p95']:.3f} s",
          f"- Estimated offset change over runtime: {d['estimated_offset_change_over_runtime_sec']:.3f} s","",
          "| Cue | Voice t | SRT t | Offset | Text |","|---:|---:|---:|---:|---|"]
        for r in d["samples"]:
            lines.append(f"| {r['cue']} | {r['voice_start']:.2f} | {r['srt_start']:.2f} | {r['start_offset_sec']:+.2f} | {r['text'].replace('|','/')} |")
        lines.append("")
    Path(a.out_md).write_text("\n".join(lines)+"\n",encoding="utf-8")
if __name__=="__main__":main()
