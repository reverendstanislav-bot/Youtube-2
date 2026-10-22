#!/usr/bin/env python3
import subprocess,pathlib,json,hashlib,math
from PIL import Image,ImageDraw
URL="https://rutube.ru/video/7d865693ec753bcbed4d97c4277edcdb/"
OUT=pathlib.Path("pluto_LASVN1_NARA_reference")
OUT.mkdir(exist_ok=True)
def cmd(parts,timeout=900):
 p=subprocess.run(parts,capture_output=True,text=True,timeout=timeout)
 if p.returncode!=0:raise RuntimeError(p.stderr[-1500:])
 return p.stdout
meta=json.loads(cmd(["yt-dlp","-J","--no-playlist",URL],120))
(OUT/"METADATA.json").write_text(json.dumps({k:meta.get(k) for k in ("id","title","uploader","duration","webpage_url","description","license")},indent=2,ensure_ascii=False)+"\n")
cmd(["yt-dlp","--no-playlist","-S","res:1080","-f","bv*+ba/b","--merge-output-format","mp4","-o",str(OUT/"F061_LASVN1_1963.%(ext)s"),URL],1800)
movies=[p for p in OUT.glob("F061*") if p.suffix.lower() in (".mp4",".webm",".mkv")]
if len(movies)!=1:raise RuntimeError("Movie missing")
movie=movies[0]
p=json.loads(cmd(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(movie)]))
v=next(s for s in p["streams"] if s.get("codec_type")=="video")
seconds=float(p["format"]["duration"])
if not 1500<seconds<1800:raise RuntimeError("Unexpected duration")
tiles=OUT/"__sample";tiles.mkdir(exist_ok=True)
interval=20
cmd(["ffmpeg","-hide_banner","-loglevel","error","-i",str(movie),"-vf","fps=1/20,scale=310:-2","-q:v","5",str(tiles/"%04d.jpg")],600)
frames=sorted(tiles.glob("*.jpg"))
for num in range(math.ceil(len(frames)/16)):
 chunk=frames[num*16:(num+1)*16];sheet=Image.new("RGB",(4*328,4*225+30),"#171a1c");draw=ImageDraw.Draw(sheet)
 draw.text((8,8),f"LASVN1 PRIMARY PROGRAM 1963 / FRAME SCAN {num+1}",fill="white")
 for k,tile in enumerate(chunk):
  x=(k%4)*328+6;y=(k//4)*225+30
  with Image.open(tile) as i:
   i=i.convert("RGB");i.thumbnail((310,195));sheet.paste(i,(x,y+24))
  s=(num*16+k)*interval
  draw.text((x,y+5),f"{s//60:02}:{s%60:02}",fill="white")
 sheet.save(OUT/f"FILM_SCREEN_{num+1:02}.jpg",quality=84)
for t in frames:t.unlink()
tiles.rmdir()
sha=hashlib.sha256()
with movie.open("rb") as f:
 for c in iter(lambda:f.read(1048576),b""):sha.update(c)
(OUT/"QC.json").write_text(json.dumps({"title":"LASV-N1 Progress Report (1963)","filmid":"USAF 38912",
"source":URL,"original_claim":"US National Archives in original YouTube description",
"film_seconds":seconds,"pixels":[v["width"],v["height"]],"sha256":sha.hexdigest(),
"bytes":movie.stat().st_size,"source_is_mirror":True,
"rights_status":"REVIEW_ORIGINAL_NARA_AND_DIGITIZER_RIGHTS_BEFORE_PUBLICATION",
"not_film_of":"actual SLAM flight or Tory II-C 1964 test run"},indent=2)+"\n")
print("HISTORIC_SOURCE_ACQUIRED",movie.stat().st_size,seconds,v["width"],v["height"],flush=True)
