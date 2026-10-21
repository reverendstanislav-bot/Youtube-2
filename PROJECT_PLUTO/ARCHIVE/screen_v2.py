#!/usr/bin/env python3
"""Targeted 1-fps screenable sheets for real source footage; no AI images or footage generation.
Original film timestamps are video timeline timestamps, not HIA narration cutpoints.
"""
import csv, math, pathlib, subprocess, json
from PIL import Image, ImageDraw, ImageFont
OUT=pathlib.Path("PROJECT_PLUTO/ARCHIVE/SCREENING_V2");OUT.mkdir(parents=True,exist_ok=True)
SRC=pathlib.Path("project_pluto_media")
# 13 editorial search regions visually flagged from coarse overview sheets.
WINS=[
 ("X01","F020",621,"X-15 facility presenter with aerospace equipment","1950s/1960s engineering culture, not Pluto"),
 ("X02","F020",690,"X-15 aircraft equipment interior/technical engine","aircraft research laboratory context, NOT Tory"),
 ("X03","F020",759,"X-15 technicians at aerospace test shop","aerospace workshop only"),
 ("X04","F020",897,"X-15 hardware being worked in hangar","engineering test program context"),
 ("X05","F020",966,"NASA specialists at an aircraft system","aircraft instrumentation context"),
 ("X06","F020",1242,"X-15 aircraft in hangar with crew","research aircraft comparison"),
 ("X07","F020",1380,"NASA-era control equipment and dials","period test/measurement context"),
 ("P01","F026",301,"Atoms for Peace exposition technicians/machinery","US atomic exhibition (Tokyo) only"),
 ("P02","F026",473,"1955 atomic exhibition laboratory gauge","USIA expo, cannot portray Pluto facility"),
 ("P03","F026",559,"exhibition experimental apparatus/robots","atomic technology exhibition"),
 ("P04","F026",688,"exhibit of atomic-era industrial machine","Japan exhibition, not US Nevada"),
 ("B01","F031",7,"1957 Fort Belvoir reactor entry and vessel tour","other reactor at Fort Belvoir, not Tory"),
 ("B02","F031",20,"Fort Belvoir machinery/inside reactor building","other reactor technology, context only")
]
rows=[]
font=ImageFont.load_default()
for cid,fid,mid,desc,scope in WINS:
    ext=".ogv" if fid=="F031" else ".webm"
    source=SRC/(fid+ext)
    if not source.exists(): raise FileNotFoundError(source)
    start=max(0,mid-6)
    duration=12
    if fid=="F031" and start+duration>29.662: duration=29.662-start
    frames=OUT/("_frames_"+cid);frames.mkdir(exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-ss",str(start),"-i",str(source),"-t",str(duration),
         "-vf","fps=1,scale=320:-2","-q:v","4",str(frames/"f%03d.jpg")]
    subprocess.run(cmd,check=True,timeout=180)
    imgs=sorted(frames.glob("f*.jpg"))
    canvas=Image.new("RGB",(4*330,4*240+36),"#202124")
    pen=ImageDraw.Draw(canvas)
    pen.text((8,9),f"{cid} — {fid}: REVIEW EACH FRAME, 1 SECOND APART",fill="#ffffff",font=font)
    for n,p in enumerate(imgs[:16]):
        x=(n%4)*330;y=(n//4)*240+36
        with Image.open(p) as orig:
            im=orig.convert("RGB");im.thumbnail((320,207))
            canvas.paste(im,(x+5,y+23))
        sec=start+n
        pen.text((x+5,y+5),f"{int(sec)//60:02}:{int(sec)%60:02}  (source)",fill="white",font=font)
        p.unlink()
    for p in imgs[16:]: p.unlink()
    frames.rmdir()
    name=f"{cid}_{fid}_MICRO.jpg"
    canvas.save(OUT/name,quality=86,optimize=True)
    rows.append({"candidate":cid,"original_id":fid,"inspection_start_sec":start,
                 "inspection_end_sec":round(start+duration,3),"anchor_sec":mid,
                 "suggested_semantic_beat":desc,"only_allowed_context":scope,
                 "qc_contact_sheet":name,"manual_in_out_review":"OPEN"})
    print(cid,source.name,"sampled",len(imgs),"time",start,"to",start+duration,flush=True)
with (OUT/"SECOND_LEVEL_SHOT_REVIEW.csv").open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(OUT/"README.md").write_text(
 "# Project Pluto — Shot screening V2\\n\\n"
 "13 source windows were selected from actual screening contact sheets and"
 " subdivided into per-second frames. No montage clips have yet been locked."
 " Preview files are generated from actual captured video, not generative AI."
 " Views of NASA X-15, USIA Tokyo exposition, Fort Belvoir are context only."
 " We have NOT obtained original video of Tory tests.\\n".replace("\\n","\n"),encoding="utf-8")
