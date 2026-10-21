#!/usr/bin/env python3
"""Fetch 1969 DoD Space Age Railroad USGov source reel from Internet Archive;
hash and make timecoded whole-film screening sheets. CONTEXT ONLY not Pluto.
"""
import os,json,hashlib,math,pathlib,requests,subprocess,time
from PIL import Image,ImageDraw,ImageFont
root=pathlib.Path("archive_f060");root.mkdir(exist_ok=True)
session=requests.Session()
session.headers["User-Agent"]="HIA-ProjectPluto-ArchivalResearch/1.0 (official USGov motion picture lookup)"
identifier="gov.dod.dimoc.26555"
meta=session.get("https://archive.org/metadata/"+identifier,timeout=45)
meta.raise_for_status();md=meta.json()
files=md.get("files",[])
options=[f for f in files if f.get("format") in ("MPEG2","MPEG4","h.264","512Kb MPEG4","MPEG4") and f.get("name","").lower().endswith((".mpg",".mpeg",".mp4"))]
options.sort(key=lambda a:(0 if a.get("format")=="MPEG2" else 1,int(a.get("size") or "0")*-1))
chosen=next((f for f in options if 5000<int(f.get("size",0))<850*1024**2),None)
if not chosen:raise RuntimeError("No suitable source movie in IA metadata: "+str(options)[:1200])
from urllib.parse import quote
url="https://archive.org/download/"+identifier+"/"+quote(chosen["name"])
out=root/("F060"+pathlib.Path(chosen["name"]).suffix)
resp=session.get(url,stream=True,timeout=(35,180))
resp.raise_for_status()
ctype=resp.headers.get("Content-Type","")
if not ("video" in ctype or "octet-stream" in ctype or "mpeg" in ctype):
    raise RuntimeError("not media: "+ctype)
with out.open("wb") as f:
    for block in resp.iter_content(chunk_size=2*1024**2):
        if block:f.write(block)
assert out.stat().st_size==int(chosen["size"]),(out.stat().st_size,chosen["size"])
h=hashlib.sha256()
with out.open("rb") as f:
    for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
pr=subprocess.run(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(out)],capture_output=True,text=True,check=True)
probe=json.loads(pr.stdout)
v=next(t for t in probe["streams"] if t["codec_type"]=="video")
duration=float(probe["format"]["duration"])
frames=root/"frame_tmp";frames.mkdir(exist_ok=True)
interval=max(9,math.floor(duration/80))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(out),
  "-vf",f"fps=1/{interval},scale=320:-2","-frames:v","90","-q:v","5",str(frames/"%03d.jpg")],
check=True,timeout=1500)
imgs=sorted(frames.glob("*.jpg"))
font=ImageFont.load_default()
pages=[]
for n in range(math.ceil(len(imgs)/24)):
  subset=imgs[n*24:(n+1)*24]
  board=Image.new("RGB",(4*332,6*215+34),"#1b1c1e")
  d=ImageDraw.Draw(board)
  d.text((8,7),f"F060 DoD 1969 SPACE AGE RAILROAD / PAge {n+1} — CONTEXT NOT PLUTO",fill="white",font=font)
  for k,image in enumerate(subset):
    i=n*24+k
    x=k%4*332+5;y=k//4*215+34
    with Image.open(image) as z:
      z=z.convert("RGB");z.thumbnail((320,184));board.paste(z,(x,y+20))
    s=int(i*interval)
    d.text((x,y),f"{s//60:02}:{s%60:02} SOURCE",fill="white",font=font)
  p=root/f"F060_SCREEN_{n+1:02}.jpg"
  board.save(p,quality=84,optimize=True);pages.append(p.name)
for p in imgs:p.unlink()
frames.rmdir()
report={"id":"F060","archive_identifier":identifier,"title":"SPACE AGE RAILROAD",
"date":1969,"origin":"United States DoD - FedFlix, Public.Resource.Org",
"rights_note":"Archive item CC0 USGov; verify original material and downstream shot use",
"link":"https://archive.org/details/gov.dod.dimoc.26555",
"actual_source_url":url,"source_format":chosen.get("format"),"original_filename":chosen["name"],
"native_width":v["width"],"native_height":v["height"],"fps":v.get("avg_frame_rate"),
"codec":v.get("codec_name"),"duration_seconds":duration,"bytes":out.stat().st_size,
"sha256":h.hexdigest(),"screens":pages,
"editorial_class":"CONTEXT_RAIL_TEST_FACILITY_NOT_PROJECT_PLUTO",
"caution":"Holloman AFB NM, 1969 film depicting historical rocket sled, not Nevada Project Pluto test track"}
(root/"F060_QC.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2),flush=True)
