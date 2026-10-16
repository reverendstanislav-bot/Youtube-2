#!/usr/bin/env python3
"""Build the full Satsop picture-only cut in GitHub Actions from 109 historic assets.

NO paid generation, NO new voice, NO subtitle layer.
The result is newly encoded and is NOT claimed byte-identical to local SHA88e8..
"""
import concurrent.futures,hashlib,json,os,pathlib,subprocess,time
from PIL import Image,ImageOps,ImageDraw,ImageFont

HERE=pathlib.Path(__file__).resolve().parent
SAT=HERE.parent
INPUT=pathlib.Path(os.environ["SATSOP_INPUT_ASSETS"])
WORK=pathlib.Path(os.environ.get("SATSOP_RENDER_WORK","/tmp/satsop-full-render"))
OUTPUT=pathlib.Path(os.environ.get("SATSOP_OUTPUT_MP4",str(WORK/"SATSOP_109_SCENE_PICTURE_ONLY_1080P30.mp4")))
PRE=WORK/"prepared";PAN=WORK/"panels";SEG=WORK/"segments"
for x in [PRE,PAN,SEG,OUTPUT.parent]:x.mkdir(parents=True,exist_ok=True)

timeline=json.loads((SAT/"REMOTION_V1/public/timeline.json").read_text())
overlays=json.loads((SAT/"REMOTION_V1/public/overlays.json").read_text())
BEATS=timeline["beats"]
assert timeline["fps"]==30 and len(BEATS)==109
assert BEATS[0]["a"]==0 and BEATS[-1]["b"]==34918
assert all(p["b"]==n["a"] for p,n in zip(BEATS,BEATS[1:]))
CARD={c["beat"]:c for c in overlays["cards"]}
FONTROOT=pathlib.Path("/usr/share/fonts/truetype/dejavu")
FREG=str(FONTROOT/"DejaVuSans.ttf");FBOLD=str(FONTROOT/"DejaVuSansCondensed-Bold.ttf");FMONO=str(FONTROOT/"DejaVuSansMono.ttf")
INK=(243,235,221,255);PAPER=(230,221,200,255);BLUE=(95,116,125,255);RUST=(165,82,53,255)
ACT={1,11,34,55,72,96}

def font(size,bold=False,mono=False):
 return ImageFont.truetype(FMONO if mono else FBOLD if bold else FREG,size)

def wrap(t,f,width,drawer):
 out=[];line=''
 for word in t.split():
  cand=(line+" "+word).strip()
  if line and drawer.textbbox((0,0),cand,font=f)[2]>width:out.append(line);line=word
  else:line=cand
 if line:out.append(line)
 return out[:4]

def panel(card,target):
 im=Image.new("RGBA",(1920,1080))
 d=ImageDraw.Draw(im)
 x0,y0,x1,y1=1302,165,1850,647
 d.rounded_rectangle((x0,y0,x1,y1),radius=4,fill=(23,26,28,237),outline=(95,116,125,160),width=2)
 d.rectangle((x0,y0,x0+4,y1),fill=BLUE)
 d.text((x0+38,y0+34),"HIA  /  PROJECT RECORD",font=font(18,mono=True),fill=PAPER)
 d.line((x0+38,y0+91,x1-28,y0+91),fill=BLUE,width=2)
 d.rectangle((x0+38,y0+116,x0+41,y0+145),fill=RUST)
 d.text((x0+58,y0+113),"REFERENCE",font=font(16,mono=True),fill=PAPER)
 y=y0+150
 for t in wrap(card["kicker"],font(24,bold=True),420,d):
  d.text((x0+58,y),t,font=font(24,bold=True),fill=INK);y+=31
 d.line((x0+38,y0+229,x1-28,y0+229),fill=BLUE,width=2)
 d.rectangle((x0+38,y0+250,x0+42,y0+310),fill=RUST)
 d.text((x0+58,y0+245),"EVIDENCE",font=font(16,mono=True),fill=PAPER)
 title=card["title"];f=font(33 if len(title)<28 else 26,bold=True)
 y=y0+284
 for t in wrap(title,f,435,d):
  d.text((x0+58,y),t,font=f,fill=INK);y+=41 if len(title)<28 else 32
 d.line((x0+38,y0+359,x1-28,y0+359),fill=BLUE,width=2)
 d.text((x0+58,y0+378),"CONTEXT",font=font(16,mono=True),fill=PAPER)
 y=y0+415
 for t in wrap(card["subline"],font(17,mono=True),434,d):
  d.text((x0+58,y),t,font=font(17,mono=True),fill=INK);y+=23
 im.save(target,optimize=True)

def intro(beat,target):
 im=Image.new("RGBA",(1920,1080));d=ImageDraw.Draw(im)
 d.rectangle((62,80,110,84),fill=RUST)
 d.text((122,65),"HIDDEN INDUSTRIAL AMERICA",font=font(20,mono=True),fill=INK)
 d.text((64,103),"SATSOP  /  WASHINGTON",font=font(17,mono=True),fill=PAPER)
 d.rectangle((64,990,101,994),fill=RUST)
 for idx,(start,tag) in enumerate([(1,"TWO TOWERS / TWO FAILURES"),(11,"FIVE PROJECTS / ONE SYSTEM"),(34,"COST TO COMPLETE"),(55,"THE COMPLETION QUESTION"),(72,"BONNEVILLE'S DECISION"),(96,"INFRASTRUCTURE REUSED")],1):
  if beat>=start:chosen=(idx,tag)
 d.text((113,974),"ACT  "+str(chosen[0]).zfill(2)+"  /  "+chosen[1],font=font(17,mono=True),fill=INK)
 im.save(target,optimize=True)

def prep(i,beat):
 path=INPUT/pathlib.Path(beat["file"]).name
 if not path.exists():raise RuntimeError(f"MISSING EXACT SOURCE {i}: {path}")
 out=PRE/f"{i:03d}.jpg"
 if not out.exists():
  with Image.open(path) as image:
   img=ImageOps.fit(image.convert("RGB"),(1980,1114),method=Image.Resampling.LANCZOS,centering=(.5,.46))
   img.save(out,quality=95,subsampling=0,optimize=True)
 if beat["beat"] in CARD:panel(CARD[beat["beat"]],PAN/f"{i:03d}.png")
 if i in ACT:intro(i,PAN/f"intro_{i:03d}.png")

def encode(i,beat):
 dur=int(beat["b"]-beat["a"])
 assert dur>0
 out=SEG/f"{i:03d}.mp4"
 if out.exists() and out.stat().st_size>40000:
  r=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=nb_frames","-of","default=nw=1:nk=1",str(out)],capture_output=True,text=True)
  if r.returncode==0 and r.stdout.strip()==str(dur):return i,out.stat().st_size
 mode=i%7
 poses=[("22+min(n*.025,23)","15"),("47-min(n*.025,23)","15"),("22","10+min(n*.021,13)"),("22","23-min(n*.021,13)"),("28+8*sin(n/120)","13+4*cos(n/120)"),("22","15"),("25+min(n*.018,15)","13")]
 x,y=poses[mode]
 filt=f"crop=1920:1080:x='{x}':y='{y}',format=yuv420p"
 if i in ACT and i!=1:filt+=",fade=t=in:st=0:d=0.40"
 elif i%11==0:filt+=",fade=t=in:st=0:d=0.22"
 cmd=["ffmpeg","-nostdin","-hide_banner","-v","error","-y","-loop","1","-framerate","30","-i",str(PRE/f"{i:03d}.jpg")]
 panelPath=PAN/f"{i:03d}.png" if beat["beat"] in CARD else PAN/f"intro_{i:03d}.png" if i in ACT else None
 if panelPath is not None:
  cmd+=["-loop","1","-framerate","30","-i",str(panelPath)]
  close=max(.5,dur/30-.34)
  layer=f"format=rgba,fade=t=in:st=0:d=0.42:alpha=1,fade=t=out:st={close:.3f}:d=0.28:alpha=1"
  cmd+=["-filter_complex",f"[0:v]{filt}[bg];[1:v]{layer}[panel];[bg][panel]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]","-map","[v]"]
 else:cmd+=["-vf",filt]
 cmd+=["-frames:v",str(dur),"-r","30","-fps_mode","cfr","-an","-c:v","libx264","-preset","ultrafast","-crf","14","-pix_fmt","yuv420p","-profile:v","high","-level","4.2","-g","90","-threads","2","-movflags","+faststart",str(out)]
 p=subprocess.run(cmd,capture_output=True,timeout=400)
 if p.returncode:raise RuntimeError(f"Scene {i}: "+p.stderr.decode(errors='replace')[-1200:])
 return i,out.stat().st_size

def main():
 a=time.time()
 print("Restored files",len(list(INPUT.glob("SAT-B*"))),flush=True)
 assert len(list(INPUT.glob("SAT-B*")))==109
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(prep,i,b) for i,b in enumerate(BEATS,1)]
  for x in concurrent.futures.as_completed(futures):x.result()
 print("Preparation ready; encoding 109 distinct sources",flush=True)
 result=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  jobs=[pool.submit(encode,i,b) for i,b in enumerate(BEATS,1)]
  for task in concurrent.futures.as_completed(jobs):
   result.append(task.result())
   if len(result)%10==0 or len(result)==109:
    print("Completed",len(result),"/109; MiB",sum(x[1] for x in result)//1048576,"time",round(time.time()-a),flush=True)
 manifest=WORK/"concat.txt"
 manifest.write_text("".join("file '"+str(SEG/f'{i:03d}.mp4')+"'\n" for i in range(1,110)))
 cmd=["ffmpeg","-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(manifest),"-map","0:v:0","-c:v","copy","-movflags","+faststart",str(OUTPUT)]
 subprocess.run(cmd,check=True,timeout=200)
 probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(OUTPUT)],text=True))
 vs=next(x for x in probe["streams"] if x["codec_type"]=="video")
 assert int(vs["nb_frames"])==34918 and (vs["width"],vs["height"])==(1920,1080) and vs["r_frame_rate"]=="30/1"
 assert len([x for x in probe["streams"] if x["codec_type"]=="audio"])==0
 print("Final FFmpeg full decode QC starts",flush=True)
 subprocess.run(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(OUTPUT),"-f","null","-"],check=True,timeout=1200)
 sha=hashlib.sha256()
 with OUTPUT.open("rb") as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b""):sha.update(chunk)
 metadata={"status":"FULL_PICTURE_ONLY_NO_ARTHUR_NO_ENDSCREEN","source_images":109,"frames":34918,"fps":30,"width":1920,"height":1080,"duration":34918/30,"bytes":OUTPUT.stat().st_size,"sha256":sha.hexdigest(),"original_local_master_sha256":"88e8f161138a53dedb473ad8e60a4eb704975470c8f462bc85a69e564fefafdd","same_bytes_as_original":sha.hexdigest()=="88e8f161138a53dedb473ad8e60a4eb704975470c8f462bc85a69e564fefafdd","audio":False,"original_end_screen":False,"generated_subtitles":False,"technical_qc":"PASS","editorial_approval":"NOT CLAIMED"}
 (OUTPUT.parent/"SATSOP_GITHUB_RELEASE_QC.json").write_text(json.dumps(metadata,indent=2))
 print("DONE",json.dumps(metadata),flush=True)
if __name__=="__main__":main()
