#!/usr/bin/env python3
"""Read-only V2 release QC on ACTUAL downloadable MP4; no Remotion render and no artistic PASS claims."""
import csv,hashlib,json,pathlib,subprocess,sys
from PIL import Image,ImageDraw
P=pathlib.Path("output");P.mkdir(exist_ok=True)
qc=P/"v2_qc";qc.mkdir(exist_ok=True)
movie=P/"HIA_LAKE_PEIGNEUR_DIRECTORIAL_V2_MASTER_1080P25.mp4"
prior=P/"HIA_LAKE_PEIGNEUR_V6_NO_RINGS_MASTER_1920x1080_25FPS.mp4"
assert movie.is_file() and prior.is_file()
def command(args,out=None):
 q=subprocess.run(args,text=True,capture_output=True)
 if out:pathlib.Path(out).write_text(q.stdout+"\n"+q.stderr)
 if q.returncode:raise AssertionError((args,q.returncode,q.stderr[-1500:]))
 return q.stdout+q.stderr
def digest(file):
 h=hashlib.sha256()
 with open(file,"rb") as f:
  for b in iter(lambda:f.read(4*1024*1024),b""):h.update(b)
 return h.hexdigest()
def audiohash(file):
 proc=subprocess.Popen(["ffmpeg","-nostdin","-v","error","-i",str(file),"-map","0:a:0","-c:a","copy","-f","adts","-"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 h=hashlib.sha256()
 while True:
  b=proc.stdout.read(4*1024*1024)
  if not b:break
  h.update(b)
 assert proc.wait()==0,proc.stderr.read()
 return h.hexdigest()
data=json.loads(command(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(movie)]))
v=next(s for s in data["streams"] if s["codec_type"]=="video")
a=next(s for s in data["streams"] if s["codec_type"]=="audio")
assert v["codec_name"]=="h264",(v["codec_name"])
assert [v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"])]==[1920,1080,"25/1",24711]
assert v.get("color_space")=="bt709"
assert a["codec_name"]=="aac" and a["sample_rate"]=="48000"
assert abs(float(data["format"]["duration"])-988.44)<.12
assert not [s for s in data["streams"] if s["codec_type"]=="subtitle"]
audio_main=audiohash(movie)
audio_prior=audiohash(prior)
assert audio_main==audio_prior,"Arthur AAC content differs from approved ancestor"
command(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(movie),"-f","null","-"],qc/"FULL_VIDEO_DECODE.log")
black=command(["ffmpeg","-nostdin","-hide_banner","-i",str(movie),"-vf","blackdetect=d=0.4:pix_th=0.10:pic_th=0.98","-an","-f","null","-"],qc/"BLACKDETECT.log")
assert "black_start:" not in black
accent=json.loads(pathlib.Path("LAKE_PEIGNEUR/PUBLISHING/DIRECTORIAL_V2/EMPHASIS_MAP_V1.json").read_text())
assert len(accent["overlays"])==13 and len(accent["focus"])==7
# Source planning is explicitly NOT proof of visually correct overlay or final editorial quality.
tm=json.loads(pathlib.Path("work/edition/FINAL_LOCKED_TIMELINE_141_SLOTS.json").read_text())
slots=[s for b in tm["beats"] for s in b["slots"]]
assert len(slots)==141 and len(tm["beats"])==87
idx=[]
shots=[]
for i,e in enumerate(accent["overlays"]):
 for mode,t in [("before",max(.1,e["start"]-.42)),("inside",min(e["end"]-.4,e["start"]+1.1)),("ending",max(e["start"]+.8,e["end"]-.42))]:
  out=qc/f"OVERLAY_{i+1:02d}_{mode}.jpg"
  command(["ffmpeg","-nostdin","-v","error","-ss",f"{t:.3f}","-i",str(movie),"-frames:v","1","-vf","scale=960:540","-q:v","3","-y",str(out)])
  idx.append({"cue":i+1,"wording":e["main"],"mode":mode,"time":round(t,3),"frame":round(t*25),"file":out.name})
  shots.append((e,mode,t,out))
for page in range((len(shots)+11)//12):
 block=shots[page*12:page*12+12]
 sheet=Image.new("RGB",(3*992,4*576),"#171A1C");d=ImageDraw.Draw(sheet)
 for i,(e,mode,t,path) in enumerate(block):
  xx=(i%3)*992;yy=(i//3)*576
  im=Image.open(path).convert("RGB");sheet.paste(im,(xx+14,yy+27))
  d.text((xx+14,yy+8),f"{t:.2f}s  {mode.upper()}  {e['main']}",fill="#E6DDC8")
  d.text((xx+14,yy+554),f"EXPECTED: {e['top']} / {e['sub']}",fill="#E6DDC8")
 sheet.save(qc/f"ACTUAL_DIRECTOR_V2_CUE_SHEET_{page+1:02d}.jpg",quality=85)
# A D1/V2 side-by-side choice requires creative judgement of actual visual content, not automatic PASS.
report={
 "status":"TECHNICAL_PASS; HUMAN_EDITORIAL_PASS_OPEN",
 "master":movie.name,"bytes":movie.stat().st_size,"sha256":digest(movie),
 "dimensions":"1920x1080","fps":25,"frames":24711,"duration_sec":float(data["format"]["duration"]),
 "audio_packet_sha256":audio_main,"original_audio_aac_packet_equal":True,
 "full_decode":"PASS","black_over_400ms":0,
 "story_beats":87,"base_picture_slots":141,
 "authored_emphasis_cues":len(accent["overlays"]),"authored_focal_windows":len(accent["focus"]),
 "visual_cues_extracted_from_actual_mp4":len(idx),
 "note":"A technically valid video and visibly rendered callouts do not certify the statements, typography, legibility, pacing or directorial approval.",
 "owner_editorial_approval":"OPEN","youtube_publication":"NOT DONE"
}
(qc/"QC_ACTUAL_V2_RELEASE.json").write_text(json.dumps(report,indent=2)+"\n")
(qc/"QC_ACTUAL_V2_CUES.json").write_text(json.dumps(idx,indent=2)+"\n")
print(json.dumps(report,indent=2))
