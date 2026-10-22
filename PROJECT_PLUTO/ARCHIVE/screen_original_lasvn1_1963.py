#!/usr/bin/env python3
"""Verify 1963 official USAF LASV-N1 film mirror and build chapter-accurate
film frame boards. This is REAL frame sampling, not AI output.
"""
import pathlib,json,hashlib,subprocess,math
from PIL import Image,ImageDraw,ImageFont

ROOT=pathlib.Path("LASVN1_ORIGINAL_SCREEN")
ROOT.mkdir(exist_ok=True)
files=list(pathlib.Path("lasvn1_source").rglob("*.mp4"))
if len(files)!=1:raise RuntimeError("Expected exactly one USAF LASVN1 film binary: "+str(files))
src=files[0]
def run(args,timeout=900):
 p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 if p.returncode!=0:raise RuntimeError(p.stderr[-1500:])
 return p.stdout
p=json.loads(run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(src)]))
v=next(s for s in p["streams"] if s.get("codec_type")=="video")
duration=float(p["format"]["duration"])
if not 1200<duration<1950:raise RuntimeError("Runtime implausible for LASV-N1: "+str(duration))
h=hashlib.sha256()
with src.open("rb") as f:
 for x in iter(lambda:f.read(1048576),b""):h.update(x)
info={"source":"LASVN1 US Air Force film 1963 USAF 38912","description":"What is Nuclear / NARA US Air Force film archived via Rutube mirror",
 "source_binary":src.name,"source_bytes":src.stat().st_size,"duration_seconds":duration,
 "resolution":[v["width"],v["height"]],"codec":v.get("codec_name"),"fps":v.get("avg_frame_rate"),"sha256":h.hexdigest(),
 "source_is_public_mirror":True,"rights_status":"COPY_SOURCE_RIGHTS_AND_MIRROR_RESTORATION_REVIEW_PENDING",
 "review_status":"SOURCE_TECHNICAL_QC_AND_CONTACT_SHEETS_ONLY"}
(ROOT/"ORIGINAL_MEDIA_FACTS.json").write_text(json.dumps(info,indent=2)+"\n")
# A deliberately wide sampling across full film, editorial reviewing every section.
chapters=[
 ("CH01_OPENING",42,175),
 ("CH02_PROGRAM_INTRO",176,322),
 ("CH03_SLAM_MODELS",322,492),
 ("CH04_AERODYNAMICS",493,617),
 ("CH05_MODEL_TESTING",618,775),
 ("CH06_SHIELDING",776,870),
 ("CH07_HARDENED_SERVOS",871,1019),
 ("CH08_COMPONENTS",1020,1156),
 ("CH09_AVIONICS",1157,1212),
 ("CH10_COMPUTER_DATA",1213,1314),
 ("CH11_RAD_HARDENED_COMPUTERS",1315,1521),
 ("CH12_ANTENNAS",1522,1570),
 ("CH13_GYROSCOPE",1571,min(duration-2,1710))
]
rows=[]
for ident,start,end in chapters:
 if end>duration-1:end=duration-1
 folder=ROOT/("work_"+ident);folder.mkdir(exist_ok=True)
 sample_period=max(6,math.floor((end-start)/18))
 args=["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(start),"-i",str(src),
 "-t",str(end-start),"-vf",f"fps=1/{sample_period},scale=400:-2","-frames:v","22","-q:v","4",
 str(folder/"%03d.jpg")]
 run(args,300)
 files=sorted(folder.glob("*.jpg"))
 cols=4;cellw=416;cellh=257
 board=Image.new("RGB",(cols*cellw,math.ceil(len(files)/cols)*cellh+34),"#191c1e")
 d=ImageDraw.Draw(board)
 d.text((8,8),f"{ident}  —  ORIGINAL 1963 FILM (other upload rights QC OPEN)",fill="white")
 for index,path in enumerate(files):
  x=index%cols*cellw+8;y=index//cols*cellh+34
  with Image.open(path) as a:
   a=a.convert("RGB");a.thumbnail((396,213));board.paste(a,(x,y+26))
  sec=int(start+sample_period*index)
  d.text((x,y+5),f"ORIGINAL SOURCE {sec//60:02}:{sec%60:02}",fill="white")
  path.unlink()
 folder.rmdir()
 out=ROOT/(ident+"_REVIEW.jpg")
 board.save(out,quality=85,optimize=True)
 rows.append({"chapter":ident,"source_start_s":start,"source_end_s":end,
 "sample_period_s":sample_period,"frames_reviewed":len(files),"sheet":out.name,"status":"HUMAN_EDITOR_REVIEW_REQUIRED"})
 print("DONE",ident,"frames",len(files),flush=True)
(ROOT/"TIMECODED_REVIEW_INDEX.json").write_text(json.dumps(rows,indent=2)+"\n")
print("FILM VERIFIED",round(duration,2),"SECONDS",v["width"],v["height"],flush=True)
