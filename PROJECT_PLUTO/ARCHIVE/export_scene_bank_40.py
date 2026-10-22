#!/usr/bin/env python3
"""40 distinct source-derived 5-20 second historical VIDEO scenes.
Source originals are unaltered. Source-sound removed from editorial clips.
This does not mean scenes were filmed during Project Pluto tests.
"""
import csv,pathlib,subprocess,hashlib,json,os
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/SCENE_BANK_40_SOURCE_IN_OUT.csv",newline="",encoding="utf8")))
srcdir=pathlib.Path("original_full_films")
dest=pathlib.Path("PROJECT_PLUTO_DELIVERY/02_SELECTED_SCENES")
dest.mkdir(parents=True,exist_ok=True)
def hashfile(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for v in iter(lambda:f.read(1024*1024),b""):h.update(v)
 return h.hexdigest()
qc=[]
for row in rows:
 fid=row["source_id"]
 src=srcdir/(fid+(".ogv" if fid=="F031" else ".webm"))
 if not src.exists():raise FileNotFoundError(src)
 start=float(row["start_seconds"]);end=float(row["end_seconds"]);duration=end-start
 if not 5<=duration<=20:raise ValueError("Scene outside 5-20 seconds:"+row["scene_id"])
 sub=dest/(fid);sub.mkdir(exist_ok=True)
 output=sub/(row["scene_id"]+"_"+fid+".mp4")
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
  "-ss",str(start),"-i",str(src),"-t",str(duration),"-map","0:v:0","-an","-sn","-dn",
  "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",
  "-movflags","+faststart",str(output)],check=True,timeout=400)
 pr=subprocess.run(["ffprobe","-v","error","-of","json","-show_streams","-show_format",str(output)],
  check=True,capture_output=True,text=True)
 d=json.loads(pr.stdout);v=next(x for x in d["streams"] if x.get("codec_type")=="video")
 if any(x.get("codec_type")=="audio" for x in d["streams"]):raise RuntimeError("Sound found in editorial clip")
 actual=float(d["format"]["duration"])
 if abs(actual-duration)>.25:raise RuntimeError("Duration failed verification")
 item={**row,"file":str(output),"verified_duration":actual,"bytes":output.stat().st_size,
 "width":v["width"],"height":v["height"],"fps":v.get("avg_frame_rate"),
 "sha256":hashfile(output),"technical":"PASS","rights_and_script_beat":"OPEN",
 "editorial_restriction":"CONTEXT_OTHER_PROJECT_NEVER_ACTUAL_TORY_TEST"}
 qc.append(item)
 print("QC",row["scene_id"],round(actual,3),flush=True)
out=pathlib.Path("PROJECT_PLUTO_DELIVERY/02_SELECTED_SCENES/SCENE_BANK_QC.json")
out.write_text(json.dumps(qc,indent=2,ensure_ascii=False)+"\n")
print("FINAL",len(qc),"total seconds",round(sum(r["verified_duration"] for r in qc),3))
