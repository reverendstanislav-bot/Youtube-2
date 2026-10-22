#!/usr/bin/env python3
"""Acquire a 1963 Project Pluto/LASV-N1 PRIMARY HISTORIC FILM for source review.
Courtesy NARA according to What Is Nuclear YouTube description. Public source upload
is NOT proof of third-party restoration rights; final reuse subject to rights review.
"""
import pathlib,subprocess,json,hashlib,math
from PIL import Image,ImageDraw,ImageFont
url="https://www.youtube.com/watch?v=8qMuS5kaDBI"
dest=pathlib.Path("pluto_primary_film_F061");dest.mkdir(exist_ok=True)
def cmd(a,timeout=1200):
 p=subprocess.run(a,text=True,capture_output=True,timeout=timeout)
 if p.returncode!=0:raise RuntimeError(p.stderr[-2000:])
 return p.stdout
info=json.loads(cmd(["yt-dlp","-J","--no-playlist",url],180))
meta={k:info.get(k) for k in ("id","title","uploader","upload_date","duration","description","license","webpage_url")}
(dest/"SOURCE_DESCRIPTION.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n")
try:
 cmd(["yt-dlp","--no-playlist","--no-part","-f","bv*[height<=1080]+ba/b[height<=1080]",
 "-S","res:1080,codec:h264","--merge-output-format","mp4","-o",str(dest/"F061_LASV_N1_1963.%(ext)s"),url],1500)
except Exception:
 # One attempt only; preserve exact metadata and error for reproduction.
 raise
candidates=list(dest.glob("F061_LASV_N1_1963.*"))
films=[c for c in candidates if c.suffix.lower() in (".mp4",".webm",".mkv")]
if len(films)!=1:raise RuntimeError("Expected one original source, got "+str(candidates))
source=films[0]
pr=json.loads(cmd(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(source)]))
v=next(x for x in pr["streams"] if x.get("codec_type")=="video")
dur=float(pr["format"]["duration"])
if not 24*60<dur<32*60:raise RuntimeError("Unexpected runtime for LASV-N1 film "+str(dur))
interval=22
temps=dest/"_temp";temps.mkdir(exist_ok=True)
cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",f"fps=1/{interval},scale=340:-2","-q:v","5",str(temps/"%04d.jpg")],500)
imgs=sorted(temps.glob("*.jpg"))
for sheet in range(math.ceil(len(imgs)/20)):
 group=imgs[sheet*20:(sheet+1)*20]
 c=Image.new("RGB",(4*356,5*222+32),"#222426")
 draw=ImageDraw.Draw(c)
 draw.text((8,8),f"LASV-N1 — ORIGINAL NARA FILM UPLOAD — PAGE {sheet+1} / SOURCED 1963",fill="white")
 for k,img in enumerate(group):
  x=k%4*356+7;y=k//4*222+32
  with Image.open(img) as p:
   p=p.convert("RGB");p.thumbnail((340,183));c.paste(p,(x,y+24))
  n=(sheet*20+k)*interval
  draw.text((x,y+6),f"{n//60:02}:{n%60:02} SOURCE",fill="white")
 c.save(dest/f"F061_CONTACT_{sheet+1:02}.jpg",quality=85)
for x in imgs:x.unlink()
temps.rmdir()
h=hashlib.sha256()
with source.open("rb") as f:
 for c in iter(lambda:f.read(1024*1024),b""):h.update(c)
result={"filmid":"USAF 38912","date_of_original_film":1963,"video_title":meta["title"],
"source_page":url,"downloaded_file":source.name,"duration_sec":dur,
"width":v["width"],"height":v["height"],"codec":v["codec_name"],"bytes":source.stat().st_size,
"sha256":h.hexdigest(),"thumbnail_interval_sec":interval,"thumb_pages":math.ceil(len(imgs)/20),
"origin_claim":"US National Archives per YouTube uploader; need verify original NARA catalog link",
"rights":"US GOVERNMENT ORIGINAL MAY BE PUBLIC DOMAIN; MODERN UPLOAD/RESTORATION RIGHTS QC OPEN",
"editorial_role":"PRIMARY DIRECT PROGRAM ARCHIVE — LASV-N1 progress, NOT footage of flying SLAM or assured May 1964 engine run"}
(dest/"MEDIA_QC.json").write_text(json.dumps(result,indent=2)+"\n")
print("SUCCESS LASV_N1",json.dumps(result),flush=True)
