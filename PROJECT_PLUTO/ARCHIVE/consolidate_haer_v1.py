#!/usr/bin/env python3
"""Create a single documented source photo ZIP from genuinely downloaded files.
No fake images, edits, upscales, guessed items or unverified asset counts.
"""
import pathlib,json,hashlib,csv,zipfile
from PIL import Image
base=pathlib.Path("PROJECT_PLUTO_HIA_PHOTO_ARCHIVE")
src=pathlib.Path("haer_sources")
eng=pathlib.Path("engine_photos")
base.mkdir(exist_ok=True)
direct=base/"01_ACTUAL_TORY_ENGINE_PHOTOS";direct.mkdir(exist_ok=True)
site=base/"02_PLUTO_FACILITY_HAER_AFTER_1968";site.mkdir(exist_ok=True)
prov=base/"03_SOURCE_MANIFESTS";prov.mkdir(exist_ok=True)
def hashpath(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
 return h.hexdigest()
records=[]
for p in sorted(eng.glob("P00*.jpg")):
 target=direct/p.name;target.write_bytes(p.read_bytes())
 with Image.open(target) as i:dim=i.size
 records.append({"file":str(target.relative_to(base)),"bytes":target.stat().st_size,
   "width":dim[0],"height":dim[1],"sha256":hashpath(target),
   "class":"REAL_PROJECT_PLUTO_TORY_ENGINE_PHOTOGRAPH","date":"1961_OR_1964_BY_SOURCE_CAPTION",
   "rights":"USGov PD per Commons; inspect exact citation and third-party credit"})
manifests=[]
for batch in sorted(src.glob("batch_*")):
 mf=batch/"SOURCE_MANIFEST.json"
 if not mf.exists():raise RuntimeError("Missing batch manifest "+str(batch))
 entries=json.loads(mf.read_text())
 manifests.extend(entries)
 (prov/(batch.name+"_SOURCE_MANIFEST.json")).write_bytes(mf.read_bytes())
 for entry in entries:
  if entry.get("status")!="DOWNLOADED_VERIFIED":continue
  fromfile=batch/(entry["id"]+".tif")
  if not fromfile.exists():raise RuntimeError("Missing original "+str(fromfile))
  dest=site/fromfile.name;dest.write_bytes(fromfile.read_bytes())
  with Image.open(dest) as img:
   dim=img.size
   if dim[0]<1000 or dim[1]<1000:raise RuntimeError("Unexpected low-resolution TIFF")
  checksum=hashpath(dest)
  if checksum!=entry["sha256"]:raise RuntimeError("Source hash mismatch")
  records.append({"file":str(dest.relative_to(base)),"bytes":dest.stat().st_size,
      "width":dim[0],"height":dim[1],"sha256":checksum,
      "class":"REAL_PLUTO_FACILITY_HAER_SURVEY_NOT_TEST_DAY",
      "date":"AFTER_1968","rights":"LOC federal HAER, check per image"}
 )
if len([x for x in records if x["class"]=="REAL_PLUTO_FACILITY_HAER_SURVEY_NOT_TEST_DAY"])!=36:
 raise RuntimeError("Expected 36 verified new HAER originals")
if len([x for x in records if x["class"]=="REAL_PROJECT_PLUTO_TORY_ENGINE_PHOTOGRAPH"])!=3:
 raise RuntimeError("Expected 3 prior genuine Tory stills")
fields=["file","bytes","width","height","sha256","class","date","rights"]
with (base/"PHOTO_MASTER_INDEX.csv").open("w",newline="",encoding="utf8") as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
(base/"REVIEW_STATUS.json").write_text(json.dumps({
"master_photos_confirmed":len(records),"historical_tory_photos":3,"haer_facility_photos":36,
"haer_targeted":48,"haer_missing_or_failed":len(manifests)-36,
"status":"REAL_IMAGES_FILE_HASH_QC_PASS_EDITORIAL_RIGHTS_QC_OPEN",
"warning":"Facility photographs produced after 1968, not Tory II-C run in 1964",
"manifest":records},indent=2)+"\n")
(base/"README.txt").write_text(
 "Project Pluto actual source photo originals.\n"
 "01_ACTUAL_TORY_ENGINE_PHOTOS: 3 period historical photos (low resolution originally).\n"
 "02_PLUTO_FACILITY_HAER_AFTER_1968: 36 verified original high-resolution TIFF files.\n"
 "03_SOURCE_MANIFESTS: 12 download-attempt manifests, including failures.\n"
 "NO synthetically invented historical scenes. Not all file rights cleared.\n"
 "HAER photos are retrospective, not actual 1961 or 1964 test-day shots.\n")
out=pathlib.Path("PROJECT_PLUTO_REAL_HISTORICAL_PHOTOS_39_FILES.zip")
with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_STORED,allowZip64=True) as z:
 for f in sorted(base.rglob("*")):
  if f.is_file():z.write(f,str(f))
print("PHOTO_ARCHIVE",len(records),"BYTES",out.stat().st_size,flush=True)
