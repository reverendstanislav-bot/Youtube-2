#!/usr/bin/env python3
import csv,math,pathlib,subprocess
from PIL import Image,ImageDraw,ImageFont
src=pathlib.Path("source_F020/F020.webm")
out=pathlib.Path("PROJECT_PLUTO/ARCHIVE/X15_MICRO_V3");out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/X15_EXTRA_CANDIDATES_V3.csv",newline="",encoding="utf8")))
font=ImageFont.load_default()
for row in rows:
    ident=row["candidate_id"];anchor=int(row["anchor_sec"]);start=max(0,anchor-5)
    frames=out/("_temp_"+ident);frames.mkdir(exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(start),"-i",str(src),
     "-t","12","-vf","fps=1,scale=320:-2","-q:v","4",str(frames/"%03d.jpg")]
    subprocess.run(cmd,check=True,timeout=180)
    images=sorted(frames.glob("*.jpg"))
    board=Image.new("RGB",(4*330,3*225+30),"#1e2123")
    d=ImageDraw.Draw(board)
    d.text((8,7),f"{ident} / TRUE 1962 NASA X-15 VIDEO / SOURCE TIME",fill="white",font=font)
    for i,file in enumerate(images[:12]):
       x=i%4*330+5;y=i//4*225+30
       with Image.open(file) as im:
          im=im.convert("RGB");im.thumbnail((320,196));board.paste(im,(x,y+18))
       n=start+i
       d.text((x,y),f"{n//60:02}:{n%60:02}",fill="white",font=font)
       file.unlink()
    for file in images[12:]:file.unlink()
    frames.rmdir()
    board.save(out/(ident+"_REVIEW.jpg"),quality=85,optimize=True)
    print("DONE",ident,flush=True)
