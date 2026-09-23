#!/usr/bin/env python3
import argparse, importlib.util, json, math, shutil, hashlib
from pathlib import Path
from collections import Counter

FPS=25
TOTAL_FRAMES=32268
END_START=1268.0

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def norm_kind(kind):
    return (kind or "").strip().lower()

def provenance(kind):
    k=norm_kind(kind)
    if k in {"archive","map"}:
        return "HISTORICAL SOURCE"
    if k=="document":
        return "DOCUMENT"
    if k=="concept":
        return "CONCEPT"
    if k=="reconstruction":
        return "AI RECONSTRUCTION"
    return ""

def load_words(path):
    raw=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    out=[]
    for x in raw:
        word=str(x.get("word","")).strip()
        if not word:
            continue
        out.append({"w":word,"s":float(x["start"]),"e":float(x["end"])})
    return out

def nearest_word_end(words,target,lo,hi,window=1.15):
    c=[w["e"] for w in words if lo<=w["e"]<=hi and abs(w["e"]-target)<=window]
    if not c:
        c=[w["e"] for w in words if lo<=w["e"]<=hi]
    return min(c,key=lambda t:abs(t-target)) if c else target

def split_times(start,end,kind,words):
    dur=end-start
    k=norm_kind(kind)
    maxdur={"map":5.8,"archive":6.6,"reconstruction":6.8,"document":6.2,"concept":6.5}.get(k,7.0)
    if dur<=maxdur:
        return [start,end],0
    n=max(2,math.ceil(dur/maxdur))
    minseg=2.4
    cuts=[start]
    snapped=0
    for j in range(1,n):
        target=start+dur*j/n
        lo=cuts[-1]+minseg
        hi=end-minseg*(n-j)
        if hi<=lo:
            cut=target
        else:
            cut=nearest_word_end(words,target,lo,hi)
            cut=max(lo,min(hi,cut))
            # Count as narration-snapped if it exactly matches a word end to 20 ms.
            if any(abs(w["e"]-cut)<=0.020 for w in words):
                snapped+=1
        cuts.append(cut)
    cuts.append(end)
    return cuts,snapped

VIEW_CYCLES={
    "map":["map_wide","map_detail_left","map_detail_right","map_center"],
    "archive":["wide","detail_left","detail_right","center_detail"],
    "document":["wide","detail_left","detail_right"],
    "concept":["wide","center_detail","detail_right"],
    "reconstruction":["wide","detail_left","detail_right","center_detail"],
}

def view_for(kind,variant,sub,count):
    k=norm_kind(kind)
    cycle=VIEW_CYCLES.get(k,["wide"])
    if count<=1:
        if k=="map":
            return "map_wide"
        if "detail" in (variant or "").lower():
            return "center_detail"
        return "wide"
    return cycle[sub % len(cycle)]

def motion_for(kind,sub,count,dur):
    k=norm_kind(kind)
    # Archive/map/document use reframing cuts only; no constant Ken Burns.
    if k in {"archive","map","document"}:
        return "static"
    # Reconstruction/concept: subtle push only on selected longer sub-beats.
    if k in {"reconstruction","concept"} and dur>=4.0 and sub%2==1:
        return "push"
    return "static"

def copy_once(src,asset_dir,cache):
    p=Path(src).resolve()
    key=str(p)
    if key in cache:
        return cache[key]
    ext=p.suffix.lower() if p.suffix.lower() in {".png",".jpg",".jpeg",".webp"} else ".png"
    token=hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
    dst=asset_dir/f"{token}{ext}"
    shutil.copy2(p,dst)
    rel=f"assets/{dst.name}"
    cache[key]=rel
    return rel

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--v3-builder",required=True)
    ap.add_argument("--shots",required=True)
    ap.add_argument("--assets-root",required=True)
    ap.add_argument("--words",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--public-dir",required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--plan-out",required=True)
    ap.add_argument("--report",required=True)
    a=ap.parse_args()

    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    pub=Path(a.public_dir); asset_dir=pub/"assets"; asset_dir.mkdir(parents=True,exist_ok=True)
    gen=work/"generated"; gen.mkdir(parents=True,exist_ok=True)

    v3=load_module(a.v3_builder,"v3builder")
    assets=v3.resolve_assets(Path(a.assets_root))
    orig=json.loads(Path(a.shots).read_text(encoding="utf-8-sig"))
    base=v3.patch_plan(orig,assets,gen)
    Path(a.plan_out).write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding="utf-8")
    words=load_words(a.words)

    out=[]; cache={}; generated_cuts=0; snapped_cuts=0
    prev_asset=None; prev_kind=None
    for base_i,s in enumerate(base):
        start=s["a"]/FPS; end=s["b"]/FPS
        times,snapped=split_times(start,end,s.get("kind"),words)
        subcount=len(times)-1
        generated_cuts += max(0,subcount-1)
        snapped_cuts += snapped
        rel=copy_once(s["asset"],asset_dir,cache)
        for sub in range(subcount):
            ss=times[sub]; ee=times[sub+1]
            aa=round(ss*FPS); bb=round(ee*FPS)
            # Preserve exact base boundaries despite float snapping.
            if sub==0: aa=int(s["a"])
            if sub==subcount-1: bb=int(s["b"])
            if bb<=aa: continue
            dur=(bb-aa)/FPS
            kind=norm_kind(s.get("kind"))
            prov=provenance(kind)
            source_change=(str(s["asset"])!=prev_asset or kind!=prev_kind)
            row={
                "i":len(out),"baseIndex":base_i,"sub":sub,"subCount":subcount,
                "a":aa,"b":bb,"frames":bb-aa,
                "file":rel,"scene":s.get("scene",""),"kind":kind,
                "variant":s.get("variant",""),"section":s.get("section",""),
                "sectionStart":bool(s.get("section","") and (not out or s.get("section","")!=out[-1].get("section",""))),
                "view":view_for(kind,s.get("variant",""),sub,subcount),
                "motion":motion_for(kind,sub,subcount,dur),
                "provenance":prov,
                "showProvenance":bool(prov and (sub==0 or source_change)),
                "durationSec":round(dur,3),
                "splitFromLongBeat":subcount>1,
                "text":s.get("text",""),"chapter":s.get("chapter",""),
                "explainer":s.get("explainer",""),"phase":s.get("phase",0),
            }
            out.append(row)
            prev_asset=str(s["asset"]); prev_kind=kind

    if not out or out[0]["a"]!=0 or out[-1]["b"]!=TOTAL_FRAMES:
        raise RuntimeError(f"bad coverage endpoints: {out[0]['a'] if out else None}..{out[-1]['b'] if out else None}")
    for x,y in zip(out,out[1:]):
        if x["b"]!=y["a"]:
            raise RuntimeError(f"gap/overlap {x['i']}->{y['i']}: {x['b']} != {y['a']}")

    bad=[]
    for x in out:
        if x["provenance"]=="HISTORICAL SOURCE" and x["kind"] not in {"archive","map"}: bad.append(x)
        if x["kind"]=="reconstruction" and x["provenance"]!="AI RECONSTRUCTION": bad.append(x)
    if bad:
        raise RuntimeError(f"PROVENANCE AUDIT FAILED: {bad[:5]}")

    before_end=[x for x in out if x["a"]/FPS<END_START]
    long=[x for x in before_end if x["durationSec"]>7.05]
    counts=Counter(x["provenance"] or "NONE" for x in out)
    report={
        "baseBeats":len(base),
        "editorialBeats":len(out),
        "newInternalCuts":generated_cuts,
        "wordSnappedInternalCuts":snapped_cuts,
        "wordSnapRatio":round(snapped_cuts/max(1,generated_cuts),6),
        "maxBeatSecBeforeOutro":round(max(x["durationSec"] for x in before_end),3),
        "beatsOver7_05SecBeforeOutro":len(long),
        "provenanceCounts":dict(counts),
        "historicalOnNonHistorical":0,
        "reconstructionWithoutAIReconstruction":0,
        "archiveMapMotionNonStatic":sum(1 for x in out if x["kind"] in {"archive","map"} and x["motion"]!="static"),
        "status":"PASS" if not long else "FAIL"
    }
    Path(a.manifest).write_text(json.dumps({"fps":FPS,"endStart":END_START,"shots":out},ensure_ascii=False,indent=2),encoding="utf-8")
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    if long:
        raise SystemExit(f"R14 pacing audit failed: {len(long)} beats >7.05 sec")

if __name__=="__main__":
    main()
