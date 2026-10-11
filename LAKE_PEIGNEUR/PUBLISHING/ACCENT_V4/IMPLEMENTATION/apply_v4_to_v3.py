#!/usr/bin/env python3
"""Non-destructively apply Lake Peigneur V4 to recovered Remotion V3 assets."""
import argparse, json, pathlib, shutil, sys
D=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument("--project",required=True)
parser.add_argument("--dry-run",action="store_true")
args=parser.parse_args()
P=pathlib.Path(args.project).expanduser().resolve()
index=P/"src/index.jsx"
timeline=P/"public/timeline.json"
facts=P/"public/facts.json"
end=P/"public/approved_first_end_1080.png"
m=json.loads((D/"HIA_LAKE_PEIGNEUR_V4_ACCENT_MAP_MACHINE.json").read_text())
assert index.is_file() and timeline.is_file() and facts.is_file() and end.is_file(), "Missing V3 files or APPROVED first endscreen"
j=json.loads(timeline.read_text())
assert j["fps"]==25 and len(j["beats"])==87 and sum(len(b["slots"]) for b in j["beats"])==99
assert len(m["items"])==100 and m.get("source_v3_master_sha256", m.get("base_v3_sha256",m.get("base_v3_sha")))=="fbc8efae5ec482b1fd6719e359cd7d50d21ed3ea9b45e0fe7608c399e700b40d"
active=[x for x in m["items"] if x["effect"] not in ("HOLD","QC_HOLD")]
assert len(active)==36
for x in active:
 assert x["asset_id"] not in m.get("conditional_ids_to_skip",m.get("blocked_conditional_assets",["LP-REC-005","LP-REC-008","LP-REC-010","LP-REC-012","LP-REC-038","LP-REC-041"]))
 assert int(x["slot_in_frame"])<=int(x["accent_in_frame"])<int(x["accent_out_frame_exclusive"])<=int(x["slot_out_frame_exclusive"])<=24211
for b in j["beats"]:
 for s in b["slots"]:
  assert s["file"].endswith(".png") and (P/"public"/s["file"]).is_file(),s["file"]
src=index.read_text()
assert "approved_first_end_1080.png" in src and "function OpeningPicture" in src
assert "<Caption" not in src and "CleanEndScreen" not in src
anchor="{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}<Chapter"
replacement="<V4Picture frame={frame}>{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}</V4Picture><V4Overlay frame={frame}/><Chapter"
if "V4Picture" in src:
 assert "V4Overlay" in src and "AccentV4" in src
else:
 assert src.count(anchor)==1,"V3 render anchor mismatch; refuse to patch unknown source"
 src='import {V4Picture,V4Overlay} from "./AccentV4";\n'+src.replace(anchor,replacement)
data=json.loads(facts.read_text())
changed=[]
for f in data:
 if f.get("title")=="65 ACRES":
  f["title"]="~68 ACRES";changed.append("65→~68 ACRES")
 if "52 MINERS" in f.get("title",""):
  f["title"]="52 PEOPLE UNDERGROUND"
  f["subline"]="7 DRILL WORKERS • ZERO FATALITIES"
  changed.append("52 MINERS corrected")
assert len(changed) in (0,2)
assert "65 ACRES" not in json.dumps(data) and "52 MINERS" not in json.dumps(data)
print("PREFLIGHT PASS: 87 beats / 99 timeline slots / 100 exposures / 36 accents")
print("FACT CORRECTIONS",changed)
if args.dry_run:
 print("DRY RUN: no writes");sys.exit(0)
if not (P/"src/index_v3_pre_v4.jsx").exists():shutil.copy2(index,P/"src/index_v3_pre_v4.jsx")
if not (P/"public/facts_v3_pre_v4.json").exists():shutil.copy2(facts,P/"public/facts_v3_pre_v4.json")
index.write_text(src)
(P/"src/AccentV4.jsx").write_text((D/"AccentV4.jsx").read_text())
(P/"public/v4_accents.json").write_text(json.dumps(m,indent=2)+"\n")
facts.write_text(json.dumps(data,indent=2)+"\n")
print("PATCHED. Run compositions and review scenes BEFORE final render. Do NOT run prepare_timeline.py")
