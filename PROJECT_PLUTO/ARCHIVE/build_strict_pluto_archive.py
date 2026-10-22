#!/usr/bin/env python3
"""Strict source-derived edit package: true Tory/Pluto photos; only chapter-justified comparison video.
No generative footage, fake historic labels, upscaling, decorative B-roll or slides.
"""
import csv,json,zipfile,pathlib,hashlib,subprocess,io
from PIL import Image,ImageDraw,ImageFont

ROOT=pathlib.Path("HIA_VIDEO006_STRICT_EDITORIAL")
V=ROOT/"02_COMPARISON_VIDEO_NOT_PLUTO";P=ROOT/"01_ACTUAL_PLUTO_HISTORICAL_STILLS";Q=ROOT/"03_PROVENANCE"
for d in (V,P,Q):d.mkdir(parents=True,exist_ok=True)
CLIPS=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/STRICT_CUT_SOURCE_SELECTION.csv",encoding="utf8",newline="")))
STILLS=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/STRICT_REAL_PLUTO_PHOTOS.csv",encoding="utf8",newline="")))
def sha(b):return hashlib.sha256(b).hexdigest()
def source_seconds(name):
 row=next((x for x in old_index if x["scene_id"]==name),None)
 if row is None:raise RuntimeError("Source scene not found: "+name)
 return float(row["start_seconds"]),float(row["end_seconds"]),row["source_id"]
def run(command):
 return subprocess.run(command,capture_output=True,text=True,check=True,timeout=450).stdout

vzip=pathlib.Path("PROJECT_PLUTO_40_REAL_CONTEXT_SCENES.zip")
film_manifest=[]
with zipfile.ZipFile(vzip) as arc:
 old_index=list(csv.DictReader(io.StringIO(arc.read("PROJECT_PLUTO_DELIVERY/02_SELECTED_SCENES/SCENE_BANK_40_SOURCE_IN_OUT.csv").decode("utf-8"))))
 for entry in CLIPS:
  id=entry["previous_clip_id"];film=entry["source_film_id"]
  old_in,old_out,old_film=source_seconds(id)
  start=float(entry["absolute_in_seconds"]); end=float(entry["absolute_out_seconds"])
  if old_film!=film or start<old_in or end>old_out or end-start<4:raise RuntimeError("Bad source interval for "+id)
  seek=start-old_in;duration=end-start
  archived="PROJECT_PLUTO_DELIVERY/02_SELECTED_SCENES/"+film+"/"+id+"_"+film+".mp4"
  with arc.open(archived) as f:
   tmp=pathlib.Path("_input_"+id+".mp4");tmp.write_bytes(f.read())
  out=V/(id+"_SELECTED_"+film+".mp4")
  run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(seek),"-i",str(tmp),
      "-t",str(duration),"-map","0:v:0","-an","-sn",
      "-c:v","libx264","-crf","17","-preset","medium","-pix_fmt","yuv420p",
      "-movflags","+faststart",str(out)])
  tmp.unlink()
  data=json.loads(run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(out)]))
  video=next(s for s in data["streams"] if s.get("codec_type")=="video")
  actual=float(data["format"]["duration"])
  if abs(actual-duration)>.3 or any(s.get("codec_type")=="audio" for s in data["streams"]):
   raise RuntimeError("QC mismatch "+id)
  record={**entry,"path":str(out.relative_to(ROOT)),"actual_duration":round(actual,3),
    "width":video["width"],"height":video["height"],
    "sha256":sha(out.read_bytes()),"bytes":out.stat().st_size,
    "type":"CONTEXT_COMPARISON_ONLY_NOT_PROJECT_PLUTO","rights_and_script_final_qc":"OPEN"}
  film_manifest.append(record)
  print("PASS VIDEO",id,round(actual,3),flush=True)

pzip=pathlib.Path("PROJECT_PLUTO_REAL_HISTORICAL_PHOTOS_39_FILES.zip")
photo_manifest=[]
with zipfile.ZipFile(pzip) as arc:
 ref=list(csv.DictReader(io.StringIO(arc.read("PROJECT_PLUTO_HIA_PHOTO_ARCHIVE/PHOTO_MASTER_INDEX.csv").decode("utf8"))))
 for row in STILLS:
  name=row["source_filename"]
  base="01_ACTUAL_TORY_ENGINE_PHOTOS" if name.startswith("P00") else "02_PLUTO_FACILITY_HAER_AFTER_1968"
  path="PROJECT_PLUTO_HIA_PHOTO_ARCHIVE/"+base+"/"+name
  content=arc.read(path)
  original=next((x for x in ref if pathlib.PurePosixPath(x["file"]).name==name),None)
  if not original or sha(content)!=original["sha256"]:
   raise RuntimeError("Original photo hash mismatch "+name)
  with Image.open(io.BytesIO(content)) as img:
   dims=(img.width,img.height)
   img.thumbnail((3500,3500),Image.Resampling.LANCZOS)
   resized=img.convert("RGB")
  out=P/(row["delivery_filename"]+".jpg")
  resized.save(out,quality=94,subsampling=0,optimize=True)
  photo_manifest.append({**row,"original_image_pixels":dims,
    "derivative_pixels":[resized.width,resized.height],
    "original_sha256":sha(content),"edited_source_sha256":sha(out.read_bytes()),
    "bytes":out.stat().st_size,"path":str(out.relative_to(ROOT)),
    "source_kind":"GENUINE_1960s_TORY_STILL" if base.startswith("01") else "GENUINE_LATER_HAER_SITE_SURVEY",
    "rights_final_lock":"OPEN"})
  print("PASS HISTORICAL PHOTO",name,dims,flush=True)

if len(film_manifest)!=9 or len(photo_manifest)!=13:raise RuntimeError("Final item count differs")
(Q/"STRICT_SOURCE_LOG.json").write_text(json.dumps({"videos":film_manifest,
"photos":photo_manifest,"direct_Plutotest_video_count":0,
"editorial_lock":"OPEN","historical_rights":"PER_ASSET_REVIEW_OPEN",
"warning":"Other missile footage not to be shown as the nuclear Tory test"},indent=2,ensure_ascii=False)+"\n")
(Q/"SOURCE_IN_OUT.csv").write_text(open("PROJECT_PLUTO/ARCHIVE/STRICT_CUT_SOURCE_SELECTION.csv",encoding="utf8").read())
(Q/"PHOTO_SOURCES.csv").write_text(open("PROJECT_PLUTO/ARCHIVE/STRICT_REAL_PLUTO_PHOTOS.csv",encoding="utf8").read())
(ROOT/"README.txt").write_text(
"VIDEO 006 PROJECT PLUTO strict historical source cutouts.\n"
"01_ACTUAL_PLUTO_HISTORICAL_STILLS = 13 real source-derived photos; 10 are later HAER site surveys, not test-day photographs.\n"
"02_COMPARISON_VIDEO_NOT_PLUTO = 9 real archival MP4 cutouts from DIFFERENT programs, for explicit narrative comparisons only.\n"
"03_PROVENANCE = original documentary source/timecode and hashes.\n"
"No authentic operating Tory engine film has been acquired.\n"
"No music, new captions or fabricated history. Rights, script, and motion-editor approval still open.\n")
filename=pathlib.Path("HIA_VIDEO006_PROJECT_PLUTO_CLEAN_CUTS.zip")
with zipfile.ZipFile(filename,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=2) as z:
 for f in sorted(ROOT.rglob("*")):
  if f.is_file():z.write(f,str(f))
print("FINAL",len(film_manifest),"video",round(sum(x["actual_duration"] for x in film_manifest),2),"seconds,",
len(photo_manifest),"actual project photos, ZIP bytes",filename.stat().st_size,flush=True)
