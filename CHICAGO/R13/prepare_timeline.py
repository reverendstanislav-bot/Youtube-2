#!/usr/bin/env python3
import argparse, importlib.util, json, shutil
from pathlib import Path
from collections import Counter

FPS=25

def load_module(path):
    spec=importlib.util.spec_from_file_location("v3builder",path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def provenance(kind):
    k=(kind or "").lower()
    if k in {"archive","map"}:
        return "HISTORICAL SOURCE"
    if k=="document":
        return "DOCUMENT"
    if k=="concept":
        return "CONCEPT"
    if k=="reconstruction":
        return "AI RECONSTRUCTION"
    return ""

def edit_motion(shot, dur):
    kind=(shot.get("kind") or "").lower()
    variant=(shot.get("variant") or "").lower()
    if kind in {"archive","map","document"}:
        return "static"
    if kind in {"concept","reconstruction"} and dur>=4.6 and "detail" not in variant:
        return "push"
    return "static"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--v3-builder",required=True)
    ap.add_argument("--shots",required=True)
    ap.add_argument("--assets-root",required=True)
    ap.add_argument("--work",required=True)
    ap.add_argument("--public-dir",required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--plan-out",required=True)
    ap.add_argument("--report",required=True)
    a=ap.parse_args()

    work=Path(a.work); work.mkdir(parents=True,exist_ok=True)
    pub=Path(a.public_dir); shotdir=pub/"shots"; shotdir.mkdir(parents=True,exist_ok=True)
    gen=work/"generated"; gen.mkdir(parents=True,exist_ok=True)

    v3=load_module(a.v3_builder)
    assets=v3.resolve_assets(Path(a.assets_root))
    orig=json.loads(Path(a.shots).read_text(encoding="utf-8-sig"))
    plan=v3.patch_plan(orig,assets,gen)
    Path(a.plan_out).write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")

    # Merge contiguous identical picture sources so fake cuts / transform resets cannot occur.
    visual=[]
    for s in plan:
        row=dict(s)
        row["_src"]=str(Path(s["asset"]).resolve())
        if visual and visual[-1]["b"]==row["a"] and visual[-1]["_src"]==row["_src"] and visual[-1].get("kind")==row.get("kind"):
            visual[-1]["b"]=row["b"]
            visual[-1]["motion"]="static"
            continue
        visual.append(row)

    out=[]
    prev_section=None
    for i,s in enumerate(visual):
        src=Path(s["_src"])
        ext=src.suffix.lower() if src.suffix else ".png"
        if ext not in {".png",".jpg",".jpeg",".webp"}:
            ext=".png"
        dst=shotdir/f"{i:03d}{ext}"
        shutil.copy2(src,dst)
        dur=(s["b"]-s["a"])/FPS
        label=provenance(s.get("kind"))
        out.append({
            "i":i,
            "a":int(s["a"]),
            "b":int(s["b"]),
            "frames":int(s["b"]-s["a"]),
            "file":f"shots/{dst.name}",
            "scene":s.get("scene",""),
            "kind":s.get("kind",""),
            "variant":s.get("variant",""),
            "section":s.get("section",""),
            "sectionStart":s.get("section","")!=prev_section,
            "motion":edit_motion(s,dur),
            "provenance":label,
            "durationSec":round(dur,3)
        })
        prev_section=s.get("section","")

    # Hard provenance audit.
    bad=[]
    for x in out:
        if x["provenance"]=="HISTORICAL SOURCE" and x["kind"] not in {"archive","map"}:
            bad.append(x)
        if x["kind"]=="reconstruction" and x["provenance"]!="AI RECONSTRUCTION":
            bad.append(x)
    if bad:
        raise RuntimeError(f"PROVENANCE AUDIT FAILED: {bad[:5]}")

    # Coverage must be exact and continuous.
    if out[0]["a"]!=0 or out[-1]["b"]!=32268:
        raise RuntimeError(f"bad coverage endpoints {out[0]['a']}..{out[-1]['b']}")
    for x,y in zip(out,out[1:]):
        if x["b"]!=y["a"]:
            raise RuntimeError(f"gap/overlap {x['i']}->{y['i']}: {x['b']} != {y['a']}")

    counts=Counter(x["provenance"] or "NONE" for x in out)
    report={
        "visualBeats":len(out),
        "originalPlanBeats":len(plan),
        "mergedDuplicateVisualCuts":len(plan)-len(out),
        "provenanceCounts":dict(counts),
        "historicalOnNonHistorical":0,
        "reconstructionWithoutAIReconstruction":0,
        "archiveMotionNonStatic":sum(1 for x in out if x["kind"] in {"archive","map"} and x["motion"]!="static"),
        "status":"PASS"
    }
    Path(a.manifest).write_text(json.dumps({"fps":FPS,"shots":out},ensure_ascii=False,indent=2),encoding="utf-8")
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
