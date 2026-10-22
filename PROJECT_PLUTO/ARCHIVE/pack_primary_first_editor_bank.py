#!/usr/bin/env python3
"""Combine independently verified delivered real Pluto stills, primary-report visuals,
and only story-warranted other-program MP4 comparisons into ONE flat organized zip.
No synthetic assets or fake 16–22 minute claim.
"""
import pathlib,zipfile,csv,json,hashlib,io,shutil
A=pathlib.Path("PROJECT_PLUTO_REAL_VISUAL_EDITOR_BANK")
folders={
 "photo":A/"01_PRIMARY_PLUTO_STILLS",
 "reports":A/"02_PRIMARY_ENGINEERING_REPORT_FIGURES",
 "context":A/"03_HISTORIC_COMPARISONS_ONLY",
 "meta":A/"04_SOURCE_MAP_AND_RIGHTS"
}
for p in folders.values():p.mkdir(exist_ok=True,parents=True)
sources=[
 ("01","HIA_VIDEO006_PROJECT_PLUTO_CLEAN_CUTS.zip"),
 ("02","HIA_VIDEO006_26_GENUINE_TORY_ENGINEERING_FIGURES.zip")
]
records=[]
with zipfile.ZipFile(sources[0][1]) as z:
 names=z.namelist()
 for name in names:
  f=pathlib.PurePosixPath(name)
  if name.endswith("/"):continue
  if f.suffix==".jpg" and "01_ACTUAL_PLUTO_HISTORICAL_STILLS" in f.parts:
   out=folders["photo"]/f.name;out.write_bytes(z.read(name))
   records.append({"asset":str(out.relative_to(A)),"class":"REAL_PROJECT_PLUTO_PHOTO",
       "sha256":hashlib.sha256(out.read_bytes()).hexdigest()})
  elif f.suffix==".mp4" and "02_COMPARISON_VIDEO_NOT_PLUTO" in f.parts:
   out=folders["context"]/f.name;out.write_bytes(z.read(name))
   records.append({"asset":str(out.relative_to(A)),"class":"OTHER_PROGRAM_HISTORIC_COMPARISON_VIDEO",
       "sha256":hashlib.sha256(out.read_bytes()).hexdigest()})
  elif f.name in ("STRICT_SOURCE_LOG.json","SOURCE_IN_OUT.csv","PHOTO_SOURCES.csv"):
   (folders["meta"]/f.name).write_bytes(z.read(name))
with zipfile.ZipFile(sources[1][1]) as z:
 for name in z.namelist():
  if name.endswith("/"):continue
  f=pathlib.PurePosixPath(name)
  if f.suffix==".png" and "01_ORIGINAL_REPORT_PAGES" in f.parts:
   out=folders["reports"]/f.name;out.write_bytes(z.read(name))
   records.append({"asset":str(out.relative_to(A)),"class":"AUTHENTIC_PRIMARY_TORY_REPORT_SCAN",
   "sha256":hashlib.sha256(out.read_bytes()).hexdigest()})
  elif f.name in ("FIGURES_SOURCE_MANIFEST.json","FIGURES_SOURCE_MANIFEST.csv"):
   (folders["meta"]/f.name).write_bytes(z.read(name))
nP=sum(x["class"]=="REAL_PROJECT_PLUTO_PHOTO" for x in records)
nF=sum(x["class"]=="AUTHENTIC_PRIMARY_TORY_REPORT_SCAN" for x in records)
nV=sum(x["class"]=="OTHER_PROGRAM_HISTORIC_COMPARISON_VIDEO" for x in records)
if (nP,nF,nV)!=(13,26,9):raise RuntimeError("Wrong verified source count "+str((nP,nF,nV)))
(folders["meta"]/"BEAT_VISUAL_MAP.csv").write_text(open("PROJECT_PLUTO/ARCHIVE/BEAT_VISUAL_MAP_V1.csv",encoding="utf8").read())
(A/"READ_ME_FIRST.txt").write_text(
 "HIA Project Pluto Real Media Documentary Bank — PRIMARY first.\\n"
 "This is a real-source library for an 8-chapter outline, NOT a 20-minute finished film.\\n"
 "01 Primary: 13 authentic Tory/Pluto photos (site photos are POST-1968).\\n"
 "02 Primary: 26 actual engineering report pages/figures, exact PDF source page given.\\n"
 "03 Secondary: only 9 videos of OTHER US military projects, 69.020s for explicit comparisons.\\n"
 "04 Metadata: accurate source page/timecode, SHA checksums, rights/QC pending.\\n"
 "REAL film of LASV-N1 1963 research is discovered and public on YouTube, but the media binary has not been successfully acquired/rights approved yet.\\n"
 "Real live footage of Tory II-C May 1964 is NOT obtained. DO NOT SUBSTITUTE ATLAS OR X15 TESTS.\\n"
 "User-approved script with exact VO timing does not exist; therefore stage is SOURCE_LIBRARY_READY, NOT EDITORIAL_COVERAGE_PASS.\\n".replace("\\n","\n"),encoding="utf8")
(folders["meta"]/"ALL_DELIVERED_FILES_QC.json").write_text(json.dumps(records,indent=2)+"\n")
archive=pathlib.Path("HIA_VIDEO006_PLUTO_PRIMARY_FIRST_EDITOR_BANK.zip")
with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as zipfile_writer:
 for item in sorted(A.rglob("*")):
  if item.is_file():zipfile_writer.write(item,str(item))
print("PACKAGE",nP,"TORY_PHOTOS",nF,"TORY_REPORT_PAGES",nV,"comparison movie files",archive.stat().st_size,"bytes",flush=True)
