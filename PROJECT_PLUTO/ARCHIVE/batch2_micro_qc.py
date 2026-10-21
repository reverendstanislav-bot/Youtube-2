#!/usr/bin/env python3
"""Generate focused per-second shots from real full-length reel sources.
No fabricated video; this is an editor review worklist, not scene PASS.
"""
import csv,math,pathlib,subprocess
from PIL import Image,ImageDraw,ImageFont
ROOT=pathlib.Path("project_pluto_batch2_video")
OUT=pathlib.Path("PROJECT_PLUTO/ARCHIVE/BATCH2_MICRO_QC")
OUT.mkdir(parents=True,exist_ok=True)
sel=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/BATCH2_MICRO_CANDIDATES.csv",newline="",encoding="utf8")))
font=ImageFont.load_default()
for r in sel:
    fid=r["film_id"];id=r["id"]
    src=ROOT/(fid+".webm")
    assert src.is_file(),src
    t=float(r["anchor_sec"]);start=max(0,t-5)
    folder=OUT/("_temp_"+id);folder.mkdir(exist_ok=True)
    command=["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(start),"-i",str(src),
       "-t","12","-vf","fps=1,scale=320:-2","-frames:v","13","-q:v","4",
       str(folder/"%03d.jpg")]
    subprocess.run(command,check=True,timeout=300)
    frames=sorted(folder.glob("*.jpg"))
    board=Image.new("RGB",(4*326,math.ceil(len(frames)/4)*223+34),"#202124")
    painter=ImageDraw.Draw(board)
    painter.text((8,8),f"{id} / {fid} / SOURCED FILM — EDITORIAL REVIEW",fill="white",font=font)
    for k,p in enumerate(frames):
        x=(k%4)*326+4; y=(k//4)*223+34
        with Image.open(p) as f:
            im=f.convert("RGB");im.thumbnail((318,190))
            board.paste(im,(x,y+21))
        n=int(start+k)
        painter.text((x,y+4),f"{n//60:02}:{n%60:02}  SOURCE SECOND",fill="white",font=font)
        p.unlink()
    folder.rmdir()
    board.save(OUT/(id+"_"+fid+"_REVIEW.jpg"),quality=86,optimize=True)
    print(id,fid,"frames",len(frames),flush=True)
