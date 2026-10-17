#!/usr/bin/env python3
"""Big Muskie HQ master: reconstruct burned narration subtitle pixels without cropping.

INPUT must be the canonical 1.527GB GitHub Release master.
The visible picture outside the centered lower caption zone stays unaltered
in geometry; Arthur audio copied exactly at final mux.
This is NOT restoration of lost original source bytes and requires review.
"""
import argparse,csv,hashlib,json,math,os,pathlib,re,subprocess,time
import cv2,numpy as np
from concurrent.futures import ThreadPoolExecutor,as_completed

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
EXPECTED_SHA="b78ee1a746a92ccb83eafd1a0be7114bcf862db62c2792c1167dc0d4dff93bbf"
FPS=25
TOTAL=35660
Y0,Y1=935,1049
X0,X1=100,1820
SS=(Y0,Y1,X0,X1)

def sh(*args,timeout=None):
 return subprocess.run(list(args),check=True,timeout=timeout)

def sec(s):
 z=s.split(":");return round((int(z[0])*3600+int(z[1])*60+float(z[2]))*FPS)

def items_from_csv(csv_file):
 with open(csv_file,newline="") as f: rows=list(csv.DictReader(f))
 assert len(rows)==116, len(rows)
 beats=[]
 for idx,r in enumerate(rows):
  start=sec(r["start"]); end=sec(r["end"])
  beats.append(dict(beat=r["beat"],start=start,end=end))
 for i,b in enumerate(beats):
  b["from"]=b["start"] if i==0 else math.floor((beats[i-1]["end"]+b["start"])/2)
  b["to"]=TOTAL if i==len(beats)-1 else math.floor((b["end"]+beats[i+1]["start"])/2)
 assert beats[0]["from"]==0 and beats[-1]["to"]==TOTAL
 assert all(beats[i]["to"]==beats[i+1]["from"] for i in range(len(beats)-1))
 return beats

def score(frame):
 a=frame[955:1030,260:1660]
 b,g,r=cv2.split(a)
 # Caption glyphs are opaque light ivory with occasional warm-orange highlight.
 minc=cv2.min(cv2.min(b,g),r)
 maxc=cv2.max(cv2.max(b,g),r)
 white=(minc>155)&((maxc.astype(np.int16)-minc.astype(np.int16))<43)
 orange=(r>150)&(r.astype(np.float32)>g.astype(np.float32)*1.2)&(g.astype(np.float32)>b.astype(np.float32)*1.18)
 return int(np.count_nonzero(white|orange))

def source_sha(path):
 v=hashlib.sha256()
 with open(path,"rb") as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b""): v.update(chunk)
 return v.hexdigest()

def probe(path):
 return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]).decode())

def preflight(source,beats,work):
 refs=work/"refs";refs.mkdir(exist_ok=True,parents=True)
 info=probe(source)
 v=next(x for x in info["streams"] if x["codec_type"]=="video")
 a=[x for x in info["streams"] if x["codec_type"]=="audio"]
 assert int(v["nb_frames"])==TOTAL and int(v["width"])==1920 and int(v["height"])==1080 and v["r_frame_rate"]=="25/1"
 assert a and a[0]["codec_name"]=="aac"
 cap=cv2.VideoCapture(str(source))
 assert cap.isOpened()
 clock=time.time();idx=0;best=[None for _ in beats]
 # Decode stream in order; evaluate roughly 5 fps in every beat excluding transition boundaries.
 for fi in range(TOTAL):
  ok=cap.grab()
  if not ok:raise RuntimeError(f"Decode stopped at video frame {fi}")
  while idx<len(beats)-1 and fi>=beats[idx]["to"]:idx+=1
  beat=beats[idx]
  if fi%5!=0 or fi<beat["start"]+10 or fi>=beat["end"]-8:continue
  ok,frame=cap.retrieve()
  if not ok:raise RuntimeError(f"Failed to retrieve {fi}")
  n=score(frame)
  if best[idx] is None or n<best[idx][0]:
   best[idx]=(n,fi)
   cv2.imwrite(str(refs/f"{idx+1:03}.png"),frame,[cv2.IMWRITE_PNG_COMPRESSION,3])
  if fi%3000==0:print("Scan frame",fi,"/",TOTAL,"elapsed",round(time.time()-clock),flush=True)
 cap.release()
 problems=[]
 for i,(beat,b) in enumerate(zip(beats,best)):
  if b is None:raise RuntimeError("No clean candidate in "+beat["beat"])
  beat.update({"best_score":b[0],"candidate_frame":b[1],"candidate_seconds":round(b[1]/FPS,3)})
  if b[0]>3500:problems.append({"beat":beat["beat"],"score":b[0],"time":b[1]/FPS})
 print("PREVIEW SCAN DONE", "problematic",len(problems), "worst",sorted(problems,key=lambda x:-x["score"])[:20],flush=True)
 (work/"PREVIEW_SCAN_QC.json").write_text(json.dumps({"input_master_sha256":EXPECTED_SHA,"size":source.stat().st_size,"fps":FPS,"frames":TOTAL,"beats":beats,"problematic":problems},indent=2))
 return problems

def draw_patch(ref,output):
 img=cv2.imread(str(ref))
 if img is None: raise RuntimeError("Missing source reference "+str(ref))
 cut=img[Y0:Y1,X0:X1]
 a=np.full(cut.shape[:2],255,dtype=np.uint8)
 # Soft alpha at patch boundary, but fully replace original caption-bearing center.
 h,w=a.shape
 for row in range(h):
  edge=min(row,h-1-row)
  mul=min(1,edge/13)
  a[row,:]=(a[row,:]*mul).astype(np.uint8)
 for col in range(w):
  edge=min(col,w-1-col)
  mul=min(1,edge/20)
  a[:,col]=(a[:,col]*mul).astype(np.uint8)
 rgba=cv2.cvtColor(cut,cv2.COLOR_BGR2BGRA)
 rgba[:,:,3]=a
 cv2.imwrite(str(output),rgba,[cv2.IMWRITE_PNG_COMPRESSION,6])

def preview(source,beats,work,probe_times):
 patches=work/"patches";patches.mkdir(exist_ok=True,parents=True)
 shots=work/"preview";shots.mkdir(exist_ok=True,parents=True)
 for i in range(len(beats)):
  draw_patch(work/"refs"/f"{i+1:03}.png",patches/f"{i+1:03}.png")
 cap=cv2.VideoCapture(str(source))
 for t in probe_times:
  fi=min(TOTAL-1,int(round(t*FPS)))
  cap.set(cv2.CAP_PROP_POS_FRAMES,fi);ok,f=cap.read()
  if not ok:continue
  bi=next(i for i,b in enumerate(beats) if b["from"]<=fi<b["to"])
  mask=cv2.imread(str(patches/f"{bi+1:03}.png"),cv2.IMREAD_UNCHANGED)
  rgba=mask[:,:,:3].astype(np.float32);alpha=(mask[:,:,3:4].astype(np.float32)/255)
  old=f[Y0:Y1,X0:X1].astype(np.float32)
  new=(old*(1-alpha)+rgba*alpha).astype(np.uint8)
  clean=f.copy();clean[Y0:Y1,X0:X1]=new
  label=f"{t:06.1f}_B{bi+1:03d}"
  cv2.imwrite(str(shots/(label+"_BEFORE.jpg")),f,[cv2.IMWRITE_JPEG_QUALITY,94])
  cv2.imwrite(str(shots/(label+"_AFTER.jpg")),clean,[cv2.IMWRITE_JPEG_QUALITY,94])
  print("PREVIEW",label,"candidate_score",beats[bi]["best_score"],flush=True)
 cap.release()

def segment(source,beats,work,i):
 b=beats[i];n=b["to"]-b["from"]
 clip=work/"segments"/f"{i+1:03d}.mp4"
 patch=work/"patches"/f"{i+1:03d}.png"
 if clip.exists():
  info=probe(clip);v=next(x for x in info["streams"] if x["codec_type"]=="video")
  if int(v.get("nb_frames",0))==n:return i,clip.stat().st_size
 cmd=[
 "ffmpeg","-nostdin","-hide_banner","-loglevel","error","-y",
 "-ss",f'{b["from"]/FPS:.3f}',"-i",str(source),
 "-loop","1","-framerate","25","-i",str(patch),
 "-filter_complex",f"[0:v][1:v]overlay={X0}:{Y0}:format=auto:shortest=1,format=yuv420p[v]",
 "-map","[v]","-frames:v",str(n),"-fps_mode","cfr","-r","25",
 "-c:v","libx264","-preset","fast","-crf","15","-pix_fmt","yuv420p",
 "-profile:v","high","-level","4.2","-g","100","-threads","2",
 "-an","-movflags","+faststart",str(clip)]
 p=subprocess.run(cmd,capture_output=True,timeout=750)
 if p.returncode!=0:raise RuntimeError(f"Segment {i+1}: "+p.stderr.decode(errors="replace")[-1000:])
 return i,clip.stat().st_size

def render(source,beats,work):
 seg=work/"segments";seg.mkdir(exist_ok=True,parents=True)
 output=work/"BIG_MUSKIE_FULL_HQ_NO_BURNED_CAPTIONS_1080P25.mp4"
 clock=time.time();sizes=0
 with ThreadPoolExecutor(max_workers=3) as pool:
  jobs=[pool.submit(segment,source,beats,work,i) for i in range(len(beats))]
  for ni,job in enumerate(as_completed(jobs),1):
   index,num=job.result();sizes+=num
   if ni%10==0 or ni==116:print("ENCODE",ni,"/",len(beats),"intermediate MiB",sizes//1048576,"elapsed",round(time.time()-clock),flush=True)
 manifest=work/"concat.txt"
 manifest.write_text("".join(f"file '{seg/f'{i+1:03d}.mp4'}'\n" for i in range(len(beats))))
 silent=work/"picture_only.mp4"
 sh("ffmpeg","-nostdin","-v","error","-y","-f","concat","-safe","0","-i",str(manifest),"-c:v","copy","-movflags","+faststart",str(silent),timeout=500)
 sh("ffmpeg","-nostdin","-v","error","-y","-i",str(silent),"-i",str(source),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy","-t",f"{TOTAL/FPS:.3f}","-movflags","+faststart",str(output),timeout=500)
 info=probe(output)
 v=next(s for s in info["streams"] if s["codec_type"]=="video")
 audio=[s for s in info["streams"] if s["codec_type"]=="audio"]
 assert int(v["nb_frames"])==TOTAL and v["width"]==1920 and v["height"]==1080 and v["r_frame_rate"]=="25/1",v
 assert len(audio)==1 and audio[0]["codec_name"]=="aac"
 print("FULL FILE DECODE QC RUNNING",flush=True)
 sh("ffmpeg","-nostdin","-v","error","-xerror","-i",str(output),"-f","null","-",timeout=1400)
 sha=source_sha(output)
 meta={"status":"HQ_SOURCE_SUBTITLE_REMOVAL_TECHNICAL_QC_PASS_EDITORIAL_REVIEW_REQUIRED","source_sha256":EXPECTED_SHA,"output_sha256":sha,"output_bytes":output.stat().st_size,"fps":25,"frames":35660,"duration_seconds":1426.4,"resolution":"1920x1080","original_aac_stream_copied":True,"no_crop_or_upscale":True,"subject_region_static_ref_patches":True,"source_license":"Creator-owned production","source":str(source),"caption_zone":[X0,Y0,X1,Y1],"warn":"Reconstructs subtitle-covered source pixels from clean frames, not original pixel files. Subtle lower-region static/fade patches may be visible and require editorial QC. No credit-based generation."}
 (work/"FINAL_QC.json").write_text(json.dumps(meta,indent=2))
 print("FINAL QC",json.dumps(meta),flush=True)

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--source",type=pathlib.Path,required=True)
 p.add_argument("--work",type=pathlib.Path,required=True)
 p.add_argument("--mode",choices=["preview","render"],default="preview")
 a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 assert a.source.exists(),a.source
 assert a.source.stat().st_size==1527013934,a.source.stat().st_size
 print("Canonical HQ SHA256 verifying",flush=True)
 assert source_sha(a.source)==EXPECTED_SHA
 beats=items_from_csv(ROOT/"FINAL_ASSET_LOCK/FINAL_116_BEAT_ASSET_LOCK_V1.csv")
 if not (a.work/"PREVIEW_SCAN_QC.json").exists():preflight(a.source,beats,a.work)
 else:
  qc=json.loads((a.work/"PREVIEW_SCAN_QC.json").read_text())
  beats=qc["beats"]
 preview(a.source,beats,a.work,[5,80,250,480,750,1020,1360,1419])
 if a.mode=="render":
  render(a.source,beats,a.work)
if __name__=="__main__":main()
