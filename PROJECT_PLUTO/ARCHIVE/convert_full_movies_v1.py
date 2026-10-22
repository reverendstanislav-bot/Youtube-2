#!/usr/bin/env python3
import argparse,csv,hashlib,json,pathlib,subprocess
parser=argparse.ArgumentParser();parser.add_argument("--id",required=True);args=parser.parse_args()
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/FULL_SOURCE_MASTER_CATALOG_V1.csv",encoding="utf8",newline="")))
r=next(r for r in rows if r["asset_id"]==args.id)
src=pathlib.Path("full_source_original")/r["source_filename"]
if src.stat().st_size!=int(r["known_source_bytes"]): raise RuntimeError("Original byte count mismatch")
dest=pathlib.Path("full_source_mp4");dest.mkdir(exist_ok=True)
out=dest/(r["asset_id"]+"_FULL_SOURCE.mp4")
def probe(p):
 s=subprocess.run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(p)],check=True,capture_output=True,text=True)
 return json.loads(s.stdout)
orig=probe(src);ov=next(x for x in orig["streams"] if x.get("codec_type")=="video")
audio=next((x for x in orig["streams"] if x.get("codec_type")=="audio"),None)
copy=ov.get("codec_name")=="h264" and (audio is None or audio.get("codec_name")=="aac")
flags=["-c:v","copy","-c:a","copy"] if copy else ["-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k"]
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
 "-map","0:v:0","-map","0:a?","-sn","-dn",*flags,"-movflags","+faststart",str(out)],check=True,timeout=4500)
mp=probe(out);mv=next(x for x in mp["streams"] if x.get("codec_type")=="video")
duration=float(orig["format"]["duration"]);actual=float(mp["format"]["duration"])
if abs(actual-duration)>1:raise RuntimeError("Full movie duration loss")
if (ov["width"],ov["height"])!=(mv["width"],mv["height"]):raise RuntimeError("Pixel resolution changed")
if ov.get("avg_frame_rate")!=mv.get("avg_frame_rate"):raise RuntimeError("FPS changed")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
data={"film_id":args.id,"film_subject":r["subject"],"class":r["source_class"],
"WARNING":r["provenance_guard"],"source_release":r["original_release_tag"],
"source_original":src.name,"original_sha256":sha(src),"original_bytes":src.stat().st_size,
"original_codec":ov.get("codec_name"),"source_duration_sec":duration,
"source_width":ov["width"],"source_height":ov["height"],"source_fps":ov.get("avg_frame_rate"),
"mp4":out.name,"mp4_sha256":sha(out),"mp4_bytes":out.stat().st_size,
"mp4_duration_sec":actual,"width":mv["width"],"height":mv["height"],"fps":mv.get("avg_frame_rate"),
"video_codec":mv.get("codec_name"),"conversion":"STREAM_COPY" if copy else "H264_CRF17_NATIVE_RESOLUTION",
"editorial_state":"FULL_LENGTH_FILE_VERIFIED_ONLY; SHOT_QC_AND_RIGHTS_OPEN"}
(dest/(args.id+"_FULL_SOURCE_TECH_QC.json")).write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps(data,indent=2),flush=True)
