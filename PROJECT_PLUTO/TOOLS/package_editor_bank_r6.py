#!/usr/bin/env python3
"""Create release-ready R6 motion and metadata packages without recompressing MP4s."""
from __future__ import annotations
import csv, hashlib, zipfile
from pathlib import Path

REPO=Path(r"C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006")
SRC=REPO/"PROJECT_PLUTO"/"SOURCE_BANK_V2"
OUT=Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_R6_RELEASE")
MOTION=[
 ("01_DIRECT_PLUTO_1963",SRC/"DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv","clip_id"),
 ("02_CONTEXT_ATLAS_MINUTEMAN_B52",SRC/"CONTEXT_MOTION_MANIFEST_V2.csv","scene_id"),
 ("03_CONTEXT_X15_FORT_BELVOIR",SRC/"CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv","scene_id"),
 ("04_CONTEXT_BOEING_WICHITA_1956",SRC/"F024_CONTEXT_MOTION_R6_MANIFEST.csv","clip_id"),
 ("05_CONTEXT_ARMY_ORDNANCE_1958",SRC/"F018_CONTEXT_MOTION_R6_MANIFEST.csv","clip_id"),
]
META=[
 "VOICE_SYNCED_VISUAL_MAP_R6_MAX_VIDEO.csv","DIRECT_PLUTO_MOTION_R6_MAX_MANIFEST.csv",
 "CONTEXT_MOTION_MANIFEST_V2.csv","CONTEXT_MOTION_PROMOTED_R6_MANIFEST.csv",
 "F024_CONTEXT_MOTION_R6_MANIFEST.csv","F018_CONTEXT_MOTION_R6_MANIFEST.csv",
 "HISTORICAL_PHOTO_MANIFEST_V2.csv","ENGINEERING_FIGURE_MANIFEST_V2.csv",
 "OFFICIAL_DOCUMENT_PAGE_MANIFEST_V2.csv","MINIMAL_GENERATION_GAPS_V2.csv",
 "ADDITIONAL_VIDEO_SOURCE_AUDIT_R6_2026-10-23.csv","EDITOR_BANK_R6_TECH_AUDIT.json",
 "EDITOR_BANK_R6_MAX_VIDEO_QC_REPORT_2026-10-23.md","SOURCE_BANK_R6_MAX_VIDEO_HANDOFF_2026-10-23.md",
]
def read(p):
 with p.open("r",newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 motion_zip=OUT/"HIA_VIDEO006_PROJECT_PLUTO_R6_MOTION_BANK_122_CLIPS.zip"
 seen=set(); count=0
 with zipfile.ZipFile(motion_zip,"w",compression=zipfile.ZIP_STORED,allowZip64=True) as z:
  for group,manifest,key in MOTION:
   for r in read(manifest):
    p=Path(r["file"]); ident=r[key]
    if ident in seen:raise SystemExit(f"duplicate id {ident}")
    seen.add(ident); z.write(p,f"{group}/{p.name}"); count+=1
 if count!=122:raise SystemExit(f"expected 122 clips, got {count}")
 meta_zip=OUT/"HIA_VIDEO006_PROJECT_PLUTO_R6_METADATA_QC.zip"
 with zipfile.ZipFile(meta_zip,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in META:z.write(SRC/name,name)
  for tool in sorted((REPO/"PROJECT_PLUTO"/"TOOLS").glob("*r6*.py")):z.write(tool,f"TOOLS/{tool.name}")
 checks=OUT/"SHA256SUMS.txt"
 checks.write_text("\n".join(f"{sha(p)}  {p.name}" for p in (motion_zip,meta_zip))+"\n",encoding="ascii")
 # Complete ZIP CRC test before release.
 for p in (motion_zip,meta_zip):
  with zipfile.ZipFile(p) as z:
   bad=z.testzip()
   if bad:raise SystemExit(f"CRC failure {p.name}: {bad}")
 print(f"clips={count}\nmotion_zip={motion_zip.stat().st_size}\nmetadata_zip={meta_zip.stat().st_size}")
if __name__=="__main__":main()
