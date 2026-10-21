#!/usr/bin/env python3
"""Cut genuine, source-timestamped preselected historical b-roll; NOT generated media.
Do not label context video as actual Project Pluto. No subtitles and no audio.
"""
import csv,hashlib,json,pathlib,subprocess
src=pathlib.Path("project_pluto_media"); dst=pathlib.Path("project_pluto_clips")
dst.mkdir(exist_ok=True)
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/CLIP_SELECTION_V1.csv",newline="",encoding="utf-8")))
def cmd(args):
    return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout
def seconds(t):
    h,m,s=t.split(":")
    return int(h)*3600+int(m)*60+float(s)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
reports=[]
for r in rows:
    fid=r["original_film_id"]; stem=r["clip_id"]
    input=src/(fid+(".ogv" if fid=="F031" else ".webm"))
    if not input.exists(): raise FileNotFoundError(input)
    output=dst/(stem+".mp4")
    insec=seconds(r["source_in"]);endsec=seconds(r["source_out"]);duration=endsec-insec
    if duration<1 or duration>20: raise ValueError("Invalid interval: "+stem)
    cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(insec),"-i",str(input),
          "-t",str(duration),"-map","0:v:0","-an","-sn",
          "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",
          "-movflags","+faststart",str(output)])
    p=json.loads(cmd(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(output)]))
    v=next(x for x in p["streams"] if x["codec_type"]=="video")
    if any(x["codec_type"]=="audio" for x in p["streams"]):raise RuntimeError("Unexpected audio")
    report={"clip_id":stem,"source_film":fid,"source_in":r["source_in"],"source_out":r["source_out"],
        "desired_duration":round(duration,3),"actual_duration":float(p["format"]["duration"]),
        "width":v["width"],"height":v["height"],"fps":v["avg_frame_rate"],"codec":v["codec_name"],
        "file_bytes":output.stat().st_size,"sha256":sha(output),
        "status":"PHYSICAL_CLIP_EXPORTED; IN_FRAME_EDITOR_QC_PENDING"}
    reports.append(report)
    print("CUT",stem,report["actual_duration"],report["width"],report["height"],flush=True)
out=pathlib.Path("PROJECT_PLUTO/ARCHIVE/CLIP_DELIVERY_VERIFY.json")
out.write_text(json.dumps(reports,indent=2)+"\n")
