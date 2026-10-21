#!/usr/bin/env python3
"""Acquire three original public-domain or PD-labeled historical CONTEXT films for HIA Project Pluto.
All candidate timecodes are mechanical thumbnails, NOT a human shot approval.
"""
import csv, hashlib, json, math, os, pathlib, subprocess, time
import requests
from PIL import Image, ImageDraw, ImageFont

MEDIA = [
  ("F020", "Research Project X-15 - development of the X-15 rocket plane - 1962 NASA documentary.webm", "NASA X-15 research/engineering. NOT Project Pluto."),
  ("F026", "Power for Peace.webm", "USIA 1955 Atoms for Peace exhibition. NOT Project Pluto."),
  ("F031", "1957-07-04 Fort Belvoir Army Package Power Reactor.ogv", "Universal Newsreel Fort Belvoir SM-1 reactor. NOT Tory/Pluto.")
]
API="https://commons.wikimedia.org/w/api.php"
HEADERS={"User-Agent":"HIA-Youtube2-DocumentaryArchive/1.0 (Research and acquisition; noncommercial automated source access)"}
ROOT=pathlib.Path("project_pluto_media")
QC=pathlib.Path("PROJECT_PLUTO/ARCHIVE/ACQUIRED_QC_V1")
ROOT.mkdir(exist_ok=True,parents=True)
QC.mkdir(exist_ok=True,parents=True)
S=requests.Session(); S.headers.update(HEADERS)
records=[]; candidates=[]; problems=[]

def metadata(name):
    for try_no in range(4):
        try:
            r=S.get(API,params={"action":"query","format":"json","prop":"imageinfo","iiprop":"url|size|mime|sha1|extmetadata","titles":"File:"+name},timeout=35)
            r.raise_for_status()
            obj=r.json()
            p=next(iter(obj["query"]["pages"].values()))
            if "imageinfo" not in p: raise RuntimeError("Commons missing file: "+name)
            return p["imageinfo"][0]
        except Exception:
            if try_no==3: raise
            time.sleep(3*(try_no+1))

def download(url,out):
    temp=out.with_name(out.name+".part")
    if out.is_file() and out.stat().st_size>1024: return
    for try_no in range(3):
        try:
            with S.get(url,stream=True,timeout=(30,120)) as r:
                r.raise_for_status()
                content_type=r.headers.get("Content-Type","")
                if not any(x in content_type for x in ("video/","application/ogg","application/octet-stream","audio/ogg")):
                    raise RuntimeError("Not media Content-Type: "+content_type)
                with temp.open("wb") as handle:
                    for chunk in r.iter_content(chunk_size=2*1024*1024):
                        if chunk: handle.write(chunk)
            if temp.stat().st_size<4096: raise RuntimeError("Truncated")
            temp.replace(out); return
        except Exception:
            temp.unlink(missing_ok=True)
            if try_no==2: raise
            time.sleep(5*(try_no+1))

def sha256(out):
    h=hashlib.sha256()
    with out.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def cmd(*args):
    return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout

def probe(out):
    p=json.loads(cmd("ffprobe","-v","error","-show_format","-show_streams","-of","json",str(out)))
    v=next(s for s in p["streams"] if s.get("codec_type")=="video")
    duration=float(p["format"].get("duration") or v.get("duration") or 0)
    return {"duration":duration,"width":v.get("width"),"height":v.get("height"),
            "codec":v.get("codec_name"),"fps":v.get("avg_frame_rate"),"streams":len(p["streams"])}

def thumbsheet(fid,local,duration):
    interval=max(2,math.ceil(duration/24))
    frame_dir=QC/("thumbs_"+fid); frame_dir.mkdir(exist_ok=True)
    vf="fps=1/"+str(interval)+",scale=280:-2"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(local),
       "-vf",vf,"-frames:v","25","-q:v","5",str(frame_dir/("%03d.jpg"))],
       check=True,timeout=1200)
    thumbs=sorted(frame_dir.glob("*.jpg"))
    font=ImageFont.load_default()
    cellw,cellh=294,205
    canvas=Image.new("RGB",(6*cellw,math.ceil(len(thumbs)/6)*cellh+36),"#222222")
    d=ImageDraw.Draw(canvas)
    d.text((8,8),fid+"  AUTO SAMPLES — NOT HUMAN SHOT QC",fill="white",font=font)
    for index,path in enumerate(thumbs):
        x=(index%6)*cellw; y=(index//6)*cellh+36
        with Image.open(path) as raw:
            im=raw.convert("RGB")
            im.thumbnail((280,172))
            canvas.paste(im,(x+6,y+24))
        sec=int(index*interval)
        timestamp=f"{sec//60:02}:{sec%60:02}"
        d.text((x+7,y+5),f"{timestamp}  AUTO SAMPLE",fill="white",font=font)
        end=min(float(duration),sec+7)
        if end>sec:
            candidates.append({"id":fid,"sample_timestamp":timestamp,
                  "suggested_7s_in":sec,"suggested_7s_out":round(end,3),
                  "status":"AUTO_SAMPLE_REQUIRES_VISUAL_EDITOR_QC","description":"UNKNOWN; photo tile only, no human review"})
    out=QC/("CONTACT_"+fid+".jpg")
    canvas.save(out,quality=82,optimize=True)
    for image in thumbs: image.unlink()
    frame_dir.rmdir()
    return len(thumbs),str(out)

for fid,name,context in MEDIA:
    print("Starting",fid,name,flush=True)
    try:
        m=metadata(name)
        size=m.get("size")
        if size and size>280*1024*1024: raise RuntimeError("Original >280MB cap; must schedule separate batch")
        suffix=pathlib.Path(name).suffix
        out=ROOT/(fid+suffix)
        download(m["url"],out)
        if size and out.stat().st_size!=size:
            raise RuntimeError(f"Size mismatch actual={out.stat().st_size} expected={size}")
        tech=probe(out)
        count,contact=thumbsheet(fid,out,tech["duration"])
        row={"id":fid,"title":name,"file":out.name,"file_bytes":out.stat().st_size,
         "sha256":sha256(out),"commons_sha1":m.get("sha1"),"source_url":m.get("descriptionurl"),
         "direct_source":m.get("url"),"source_license_status":"PUBLIC_DOMAIN_REPORTED_ON_SOURCE_PAGE—PER_FRAME_QC_OPEN",
         "editorial_class":"CONTEXT_ONLY_NOT_PLUTO", "editorial_use":context,
         "contact_sheet":contact,"automated_sample_count":count,"status":"ACQUIRED_NEEDS_EDITOR_REVIEW",**tech}
        records.append(row);print("ACQUIRED",fid,tech["duration"],tech["width"],tech["height"],flush=True)
    except Exception as err:
        problems.append({"id":fid,"title":name,"status":"FAILED","reason":str(err)})
        print("FAILED",fid,repr(err),flush=True)
(QC/"MEDIA_VERIFICATION.json").write_text(json.dumps({"assets":records,"failed":problems},indent=2,ensure_ascii=False)+"\n")
with (QC/"AUTO_TIMECODE_CANDIDATES.csv").open("w",newline="",encoding="utf-8") as f:
    fields=["id","sample_timestamp","suggested_7s_in","suggested_7s_out","status","description"]
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(candidates)
lines=["# Project Pluto — video acquisition mechanical QC","",
 "WARNING: automated frame contact sheets only, NOT actual viewing/edit approval. ",
 "All files are CONTEXT_ONLY: do NOT represent any as Tory II-A/Tory II-C footage.",
 "",f"Acquired original files: **{len(records)}/3**; failed: **{len(problems)}**.",""]
for r in records:
    lines.append(f"- **{r['id']}** {r['title']} — {r['duration']:.3f}s, {r['width']}x{r['height']}, {r['codec']}, "+str(r["file_bytes"])+" bytes; SHA256 `"+r["sha256"]+"`; "+str(r["automated_sample_count"])+" timestamped sampled frames.")
for x in problems:lines.append("- **FAILED "+x["id"]+"** "+x["reason"])
lines.extend(["","Scene descriptions have not been reviewed. No in/out point has been approved.",
              "The original downloads are uploaded to workflow artifacts and/or a GitHub draft release.",
              "All licensing/provenance should be reviewed per film/shot before use."])
(QC/"README.md").write_text("\n".join(lines)+"\n")
print("FINAL",len(records),len(problems),flush=True)
if not records: raise RuntimeError("No original archival videos acquired")
