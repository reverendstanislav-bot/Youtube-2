#!/usr/bin/env python3
"""Targeted D1->D2 edit: repair 3 misleading shots and expose 16 real focal cues without new media."""
import argparse,collections,copy,hashlib,json,pathlib,shutil
PARSER=argparse.ArgumentParser()
PARSER.add_argument("--project",required=True)
PARSER.add_argument("--report",required=True)
args=PARSER.parse_args()
P=pathlib.Path(args.project).resolve()
D=pathlib.Path(__file__).resolve().parent
plan=json.loads((D/"DIRECTORIAL_D2_REPAIR_PLAN.json").read_text())
path=P/"public/timeline.json"
srcpath=P/"src/index.jsx"
data=json.loads(path.read_text())
src=srcpath.read_text()
assert len(data["beats"])==87 and sum(len(b["slots"]) for b in data["beats"])==141
assert src.count("const DIRECTOR_FOCUS=")==1 and "DIRECTORIAL_D1" in src
assert "DIRECTOR_HARD_CUTS" in src and "D2EditorialEmphasis" not in src
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""):h.update(block)
 return h.hexdigest()
assert sha(P/"public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3")=="1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13"
assert sha(P/"public/approved_first_end_1080.png")=="b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575"
for z in plan["swaps"]:
 beat=next((b for b in data["beats"] if b["beat"]==z["beat"]),None)
 assert beat,z
 cand=[s for s in beat["slots"] if s["assetId"]==z["old"]]
 assert len(cand)==1,(z,len(cand))
 s=cand[0]
 assert (P/"public/assets"/(z["new"]+".png")).is_file(),z["new"]
 s.update(assetId=z["new"],file="assets/"+z["new"]+".png",kind=z["kind"],motion="none")
# D1's 16-stage attention map refers to two GFX-036 source exposures now replaced.
m1='"beat":"LP-B048","asset":"LP-GFX-036"'
m2='"beat":"LP-B052","asset":"LP-GFX-036"'
assert src.count(m1)==1 and src.count(m2)==1
src=src.replace(m1,'"beat":"LP-B048","asset":"LP-REC-045"')
src=src.replace(m2,'"beat":"LP-B052","asset":"LP-GFX-037"')
# Gentle, visible soft-area emphasis: preserve all content; no circles, rings, panels or panning.
old={
 "0.0036*smoothed(t)":"0.009*smoothed(t)",
 "brightness(.89) saturate(.965)":"brightness(.86) saturate(.95)",
 "brightness(1.065) contrast(1.035)":"brightness(1.17) contrast(1.08)",
 "ellipse 32% 35%":"ellipse 36% 38%"
}
for a,b in old.items():
 assert src.count(a)==1,(a,src.count(a))
 src=src.replace(a,b)
# Strong invariants: 87 acts, 141 locked picture segments, no missing frames/repeated sources.
shots=[s for b in data["beats"] for s in b["slots"]]
assert len(shots)==141
assert shots[0]["a"]==0 and shots[-1]["b"]==24211
assert all(a["b"]==b["a"] for a,b in zip(shots,shots[1:]))
counts=collections.Counter(s["assetId"] for s in shots)
assert max(counts.values())<=2,counts.most_common(12)
rejected={"LP-GFX-002","LP-GFX-022","LP-GFX-026","LP-REC-005","LP-REC-008","LP-REC-010","LP-REC-012","LP-REC-038","LP-REC-041"}
assert not set(counts).intersection(rejected)
# Every D1 detail emphasis cue is still attached to a unique, on-screen source in its beat.
a=src.split("const DIRECTOR_FOCUS=",1)[1].split(";",1)[0]
focus=json.loads(a)
assert len(focus)==16
for e in focus:
 beat=next(x for x in data["beats"] if x["beat"]==e["beat"])
 assert sum(s["assetId"]==e["asset"] for s in beat["slots"])==1,e
assert len(plan["swaps"])==3
assert src.count("approved_first_end_1080.png")==1
assert src.count("LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3")==2
assert "0.009*smoothed(t)" in src and "DIRECTOR_HARD_CUTS" in src
assert not any(x in src for x in ["<Caption","V4Overlay","V7Focus","D2EditorialEmphasis"])
shutil.copy2(path,P/"public/timeline_BEFORE_D2_REPAIR.json")
shutil.copy2(srcpath,P/"src/index_BEFORE_D2_REPAIR.jsx")
path.write_text(json.dumps(data,indent=2)+"\n")
srcpath.write_text(src)
report={"status":"D2 SOURCE PREFLIGHT PASS (OWNER EDITORIAL REVIEW OPEN)",
 "changed_sources":plan["swaps"],
 "story_beats":87,"picture_slots":141,"source_reuse_max":max(counts.values()),
 "human_selected_semantic_cues":len(focus),"micro_motion_cues":6,
 "max_hero_scale":1.009,"motivated_hard_cuts":11,
 "original_audio_sha256":sha(P/"public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3"),
 "original_endscreen_sha256":sha(P/"public/approved_first_end_1080.png"),
 "new_generations":0,"V2_typographic_overlays_included":False}
pathlib.Path(args.report).write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
