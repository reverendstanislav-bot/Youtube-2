#!/usr/bin/env python3
"""Independent integrity, decode and timeline audit for Project Pluto R6."""
from __future__ import annotations
import csv, hashlib, json, subprocess
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO=Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
SRC=REPO/"PROJECT_PLUTO"/"SOURCE_BANK_V2"
MAP=SRC/"VOICE_SYNCED_VISUAL_MAP_R6_MAX_VIDEO.csv"
OUT=SRC/"EDITOR_BANK_R6_TECH_AUDIT.json"
MANIFESTS=[
 ("direct_pluto",SRC/"DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv","clip_id"),
 ("context_v2",SRC/"CONTEXT_MOTION_MANIFEST_V2.csv","scene_id"),
 ("context_promoted",SRC/"CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv","scene_id"),
 ("context_f024",SRC/"F024_CONTEXT_MOTION_R6_MANIFEST.csv","clip_id"),
 ("context_f018",SRC/"F018_CONTEXT_MOTION_R6_MANIFEST.csv","clip_id"),
]
def read(p):
 with p.open("r",newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def verify(item):
 group,row,key=item;p=Path(row["file"]); errors=[]
 if not p.exists():return {"id":row[key],"group":group,"errors":["MISSING_FILE"]}
 if sha(p).lower()!=row["sha256"].lower():errors.append("SHA256_MISMATCH")
 q=subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(p),"-f","null","-"],capture_output=True)
 if q.returncode:errors.append("DECODE_FAIL")
 return {"id":row[key],"group":group,"errors":errors}
def main():
 all_rows=[]; summaries={}
 for group,path,key in MANIFESTS:
  rows=read(path);all_rows += [(group,r,key) for r in rows]
  summaries[group]={"clips":len(rows),"duration_sec":round(sum(float(r["duration_sec"]) for r in rows),3),"manifest_black_intervals":sum(bool(r.get("black_intervals")) for r in rows)}
 with ThreadPoolExecutor(max_workers=4) as ex: verified=list(ex.map(verify,all_rows))
 failures=[x for x in verified if x["errors"]]
 hashes=[r["sha256"].lower() for _,r,_ in all_rows]
 duplicates=[h for h,n in Counter(hashes).items() if n>1]
 rows=read(MAP); continuity=[]
 for a,b in zip(rows,rows[1:]):
  if abs(float(a["timeline_out_sec"])-float(b["timeline_in_sec"]))>0.001:continuity.append([a["scene_id"],b["scene_id"]])
 file_missing=[r["scene_id"] for r in rows if not Path(r["file"]).exists()]
 overruns=[]
 for r in rows:
  if r["local_clip_out_sec"]:
   p=Path(r["file"])
   probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(p)],capture_output=True,text=True)
   if probe.returncode or float(r["local_clip_out_sec"])>float(probe.stdout.strip())+0.04:overruns.append(r["scene_id"])
 motion=[r for r in rows if "MOTION" in r["media_type"]]
 result={
  "result":"PASS" if not failures and not duplicates and not continuity and not file_missing and not overruns else "FAIL",
  "motion_bank":summaries,
  "motion_bank_total_clips":len(all_rows),
  "motion_bank_total_duration_sec":round(sum(v["duration_sec"] for v in summaries.values()),3),
  "motion_unique_sha256":len(set(hashes)),"duplicate_motion_hashes":duplicates,
  "full_decode_and_hash_pass":len(all_rows)-len(failures),"full_decode_or_hash_failures":failures,
  "timeline_rows":len(rows),"timeline_unique_assets":len({r["asset_id"] for r in rows}),
  "timeline_unique_motion_assets":len({r["asset_id"] for r in motion}),
  "timeline_motion_sec":round(sum(float(r["timeline_out_sec"])-float(r["timeline_in_sec"]) for r in motion),3),
  "timeline_start_sec":float(rows[0]["timeline_in_sec"]),"timeline_end_sec":float(rows[-1]["timeline_out_sec"]),
  "timeline_beats":len({r["beat_id"] for r in rows}),"timeline_chapters":len({r["chapter"] for r in rows}),
  "continuity_errors":continuity,"timeline_missing_files":file_missing,"local_clip_overruns":overruns,
  "empty_rights_rows":sum(not r["rights_status"].strip() for r in rows),"empty_required_label_rows":sum(not r["required_screen_label"].strip() for r in motion),
  "media_type_counts":dict(Counter(r["media_type"] for r in rows)),
 }
 OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
 print(json.dumps(result,indent=2,ensure_ascii=False))
 if result["result"]!="PASS":raise SystemExit(1)
if __name__=="__main__":main()
