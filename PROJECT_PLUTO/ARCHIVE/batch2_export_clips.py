#!/usr/bin/env python3
"""Export true-source historical context fragments, retaining native pixel size.
Caution: AI-upscaled Commons derivatives; these are NOT Pluto/Tory nuclear-engine tests.
"""
import csv,pathlib,subprocess,json,hashlib
INPUT=pathlib.Path("project_pluto_batch2_video")
OUT=pathlib.Path("pluto_batch2_clips")
OUT.mkdir(exist_ok=True,parents=True)
ROWS=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/BATCH2_SELECTED_21.csv",encoding="utf8",newline="")))
def ts(v):
 a,b=v.split(":");return int(a)*60+int(b)
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for part in iter(lambda:f.read(1048576),b""):h.update(part)
 return h.hexdigest()
manifest=[]
for r in ROWS:
 source=INPUT/(r["source_film_id"]+".webm")
 assert source.is_file(),source
 s=ts(r["source_in_mmss"]); e=ts(r["source_out_mmss"]); dur=e-s
 assert 1<dur<=11,(r["clip_id"],dur)
 out=OUT/(r["clip_id"]+".mp4")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(s),
  "-i",str(source),"-t",str(dur),"-map","0:v:0","-an","-sn","-c:v","libx264",
  "-crf","17","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],
  check=True,timeout=240)
 pr=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(out)],
  stdout=subprocess.PIPE,text=True,check=True)
 p=json.loads(pr.stdout)
 v=next(x for x in p["streams"] if x["codec_type"]=="video")
 if any(x["codec_type"]=="audio" for x in p["streams"]):raise RuntimeError("Unexpected audio")
 actual=float(p["format"]["duration"])
 if abs(actual-dur)>.2:raise RuntimeError("Duration mismatch")
 o={"clip_id":r["clip_id"],"source_film":r["source_film_id"],
    "source_in":r["source_in_mmss"],"source_out":r["source_out_mmss"],
    "duration_expected":dur,"duration_actual":actual,"source_subject":r["visually_screened_description"],
    "allowed_context":r["provenance_guard"],"file_bytes":out.stat().st_size,
    "width":v["width"],"height":v["height"],"source_format":"AI-UPSCALED_COMMONS_DERIVATIVE",
    "sha256":sha(out),"approval":"PRESELECTED_ONLY_NEEDS_MOTION_EDITOR_AND_RIGHTS_QC"}
 manifest.append(o)
 print("CUT",o["clip_id"],o["duration_actual"],o["width"],o["height"],flush=True)
QC=pathlib.Path("PROJECT_PLUTO/ARCHIVE/BATCH2_EXPORT_VERIFY.json")
QC.write_text(json.dumps(manifest,indent=2)+"\n")
print("FINAL",len(manifest),"total seconds",sum(x["duration_actual"] for x in manifest))
