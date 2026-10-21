#!/usr/bin/env python3
"""Acquire independent 1950s-1960s US government-film context originals.
Single movie per matrix job. Frames sampled for editorial review, NOT approved shots.
"""
import argparse,hashlib,json,math,pathlib,subprocess,time,requests
from PIL import Image,ImageDraw,ImageFont

FILMS={
 "F011":("On Target, The Atlas ICBM 1958.webm","1958 Atlas ICBM / strategic program contrast"),
 "F013":("Minutemen Missile And Mission 1962.webm","1962 Minuteman / alternatives to SLAM"),
 "F015":("Operation Bluenose AGM-28 Hound Dog Missile B-52 Launch 1960.webm","1960 Hound Dog air-launched missile / contrast"),
 "F018":("U.S. Army Ordnance Missile Command 1958.webm","1958 missile research facilities / context"),
 "F024":("Boeing Aircraft Wichita Bomber Maintenance & Development 1956.webm","1956 industrial aerospace manufacturing / context"),
}
p=argparse.ArgumentParser();p.add_argument("--id",required=True,choices=list(FILMS));args=p.parse_args()
fid=args.id
title,role=FILMS[fid]
root=pathlib.Path("pluto_batch2")/fid
root.mkdir(parents=True,exist_ok=True)
session=requests.Session()
session.headers["User-Agent"]="HIA-Archive-SourceQC/1.1 (archival-source-verification)"
def query():
    for attempt in range(4):
        try:
            resp=session.get("https://commons.wikimedia.org/w/api.php",
              params={"action":"query","format":"json","prop":"imageinfo","iiprop":"url|size|mime|sha1|extmetadata","titles":"File:"+title},
              timeout=40)
            resp.raise_for_status()
            obj=resp.json()
            page=next(iter(obj["query"]["pages"].values()))
            return page["imageinfo"][0]
        except Exception:
            if attempt==3:raise
            time.sleep(2*(attempt+1))
def download(info,path):
    size=info.get("size",0)
    if size>470*1024*1024: raise RuntimeError("Media >470MiB; split acquisition before retry")
    with session.get(info["url"],stream=True,timeout=(30,180)) as resp:
        resp.raise_for_status()
        mime=resp.headers.get("Content-Type","")
        if not any(x in mime for x in ["video/","application/octet-stream"]):
            raise RuntimeError("Unexpected source mime: "+mime)
        with path.open("wb") as out:
            for chunk in resp.iter_content(chunk_size=2*1024*1024):
                if chunk:out.write(chunk)
    if size and path.stat().st_size!=size:raise RuntimeError(f"Bad size {path.stat().st_size} vs {size}")
def checksum(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def call(a):
    proc=subprocess.run(a,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True,timeout=900)
    return proc.stdout
info=query()
path=root/(fid+".webm")
download(info,path)
probe=json.loads(call(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(path)]))
v=next(x for x in probe["streams"] if x.get("codec_type")=="video")
duration=float(probe["format"]["duration"])
interval=max(12,math.floor(duration/42))
thumbs=root/"_temporary_samples";thumbs.mkdir(exist_ok=True)
call(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(path),
"-vf",f"fps=1/{interval},scale=320:-2", "-frames:v","50","-q:v","5",str(thumbs/"%03d.jpg")])
images=sorted(thumbs.glob("*.jpg"))
font=ImageFont.load_default()
pages=[]
for page_i in range(math.ceil(len(images)/20)):
    group=images[page_i*20:(page_i+1)*20]
    tile=Image.new("RGB",(5*332,4*226+35),"#202124")
    draw=ImageDraw.Draw(tile)
    draw.text((6,10),fid+" SOURCE PHOTO FRAMES — NOT SHOT APPROVAL",fill="white",font=font)
    for cell_i,item in enumerate(group):
        absolute=page_i*20+cell_i
        sec=int(absolute*interval)
        x=(cell_i%5)*332+6; y=(cell_i//5)*226+35
        with Image.open(item) as frame:
            frame=frame.convert("RGB");frame.thumbnail((320,190))
            tile.paste(frame,(x,y+21))
        draw.text((x,y+3),f"{sec//60:02}:{sec%60:02} SOURCE",fill="white",font=font)
    name=f"{fid}_CONTACT_{page_i+1:02}.jpg"
    tile.save(root/name,quality=83,optimize=True)
    pages.append(name)
for item in images:item.unlink()
thumbs.rmdir()
metadata={"film_id":fid,"source_title":title,"editorial_class":"CONTEXT_ONLY_NOT_PLUTO",
"source_role":role,"source_file_url":info["url"],"source_page":info.get("descriptionurl"),
"source_sha1":info.get("sha1"),"sha256":checksum(path),"file_bytes":path.stat().st_size,
"duration_seconds":duration,"native_width":v["width"],"native_height":v["height"],
"video_codec":v.get("codec_name"),"fps":v.get("avg_frame_rate"),
"source_digital_edit_warning":"Commons derivative may contain AI upscaling; NOT film scan proof",
"snapshot_interval_sec":interval,"contact_sheet_pages":pages,
"rights_status":"ITEM_REVIEW_OPEN","editorial_status":"REVIEW_OPEN"}
(root/"FILE_QC.json").write_text(json.dumps(metadata,indent=2)+"\n")
print(json.dumps(metadata,indent=2))
