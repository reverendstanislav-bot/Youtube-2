#!/usr/bin/env python3
import pathlib,csv,json,hashlib,subprocess
base=pathlib.Path("original_F020/F020.webm")
out=pathlib.Path("project_pluto_x15_extra_clips");out.mkdir(exist_ok=True)
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/X15_EXTRA_SELECTED_V3.csv",newline="",encoding="utf8")))
def s(t):
 m,n=t.split(":");return int(m)*60+int(n)
def hash(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
result=[]
for r in rows:
 beg=s(r["source_in"]);end=s(r["source_out"]);dur=end-beg
 assert 2<=dur<=11
 file=out/(r["clip_id"]+".mp4")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(beg),
  "-i",str(base),"-t",str(dur),"-map","0:v:0","-an","-sn","-c:v","libx264",
  "-preset","medium","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",str(file)],
  check=True,timeout=180)
 probe=subprocess.run(["ffprobe","-v","error","-of","json","-show_format","-show_streams",str(file)],
 check=True,capture_output=True,text=True)
 meta=json.loads(probe.stdout)
 track=next(x for x in meta["streams"] if x["codec_type"]=="video")
 length=float(meta["format"]["duration"])
 if abs(length-dur)>.2:raise RuntimeError("Duration mismatch")
 x={"clip":r["clip_id"],"film":"F020","source_in":r["source_in"],"source_out":r["source_out"],
 "duration":length,"width":track["width"],"height":track["height"],"file_bytes":file.stat().st_size,
 "sha256":hash(file),"context":"NASA X-15, NOT Pluto / Tory","review_status":"PRESELECTED_VISUAL_SOURCE_FRAMES; NEEDS_MOTION_QC"}
 result.append(x)
 print("CUT",r["clip_id"],length,flush=True)
p=pathlib.Path("PROJECT_PLUTO/ARCHIVE/X15_EXTRA_EXPORT_VERIFY_V3.json")
p.write_text(json.dumps(result,indent=2)+"\n")
print("TOTAL",len(result),round(sum(x["duration"] for x in result),4))
