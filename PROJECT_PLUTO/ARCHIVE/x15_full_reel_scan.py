#!/usr/bin/env python3
"""Comprehensive source-accurate X-15 reel survey. Context only; not Project Pluto.
A frame every 9 sec; no shot is considered reviewed until human view + micro sampling.
"""
import pathlib,subprocess,math,json
from PIL import Image,ImageDraw,ImageFont
src=pathlib.Path("source_F020/F020.webm")
out=pathlib.Path("PROJECT_PLUTO/ARCHIVE/X15_FULL_REEL_REVIEW")
out.mkdir(parents=True,exist_ok=True)
frames=pathlib.Path("x15_tmp");frames.mkdir(exist_ok=True)
interval=9
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
 "-vf",f"fps=1/{interval},scale=310:-2","-q:v","5",str(frames/"%04d.jpg")],check=True,timeout=900)
imgs=sorted(frames.glob("*.jpg"))
font=ImageFont.load_default()
for page in range(math.ceil(len(imgs)/24)):
    group=imgs[page*24:(page+1)*24]
    canvas=Image.new("RGB",(4*320,6*206+30),"#171a1c")
    d=ImageDraw.Draw(canvas)
    d.text((8,7),f"F020 NASA X-15 1962 / PAGE {page+1} / SOURCE SECOND EVERY 9 SEC",font=font,fill="white")
    for cell,p in enumerate(group):
       x=cell%4*320+3;y=cell//4*206+30
       with Image.open(p) as im:
          im=im.convert("RGB");im.thumbnail((307,175))
          canvas.paste(im,(x,y+19))
       sec=(page*24+cell)*interval
       d.text((x,y),f"{sec//60:02}:{sec%60:02} SOURCE",font=font,fill="white")
    canvas.save(out/f"X15_FULL_{page+1:02}.jpg",quality=86,optimize=True)
for x in imgs:x.unlink()
frames.rmdir()
(out/"SCREENING_INFO.json").write_text(json.dumps({"film_id":"F020","date":1962,
"source_sha256_provenance":"See ARCHIVE/ACQUIRED_QC_V1/MEDIA_VERIFICATION.json",
"interval_sec":9,"sample_count":len(imgs),"pages":math.ceil(len(imgs)/24),
"rights_status":"USGov NASA sourced; upload license review remains open",
"scope":"CONTEXT_ONLY_X15_NOT_PLUTO", "qc":"SCREENING_CONTACTS_NOT_SHOTS_APPROVED"},indent=2)+"\n")
print("Screens",len(imgs),"pages",math.ceil(len(imgs)/24),flush=True)
