#!/usr/bin/env python3
"""Restore original photographic subtitle regions with geometrically aligned verified Commons images."""
import cv2,glob,json,os,pathlib,sys
import numpy as np
from PIL import Image,ImageDraw
WORK=pathlib.Path("/tmp/bigmuskie-commons-align")
HQ=pathlib.Path(os.getenv("BIGMUSKIE_HQ_MP4","/tmp/muskie_hq_source/BIG_MUSKIE_FINAL_UPLOAD_MASTER.mp4"))
OUT=WORK/"qc";OUT.mkdir(parents=True,exist_ok=True)
TARGET={2:(14.0,"R06"),3:(27.0,"R07"),101:(1240.0,"R07"),107:(1308.0,"R10")}
cap=cv2.VideoCapture(str(HQ))
assert cap.isOpened()
config=json.loads((WORK/"commons.json").read_text())
def source(name):
 fn=pathlib.Path(config[name]);img=cv2.imread(str(fn))
 if img is None:raise RuntimeError(f"missing input original photo {fn}")
 return img
def align(real,frame):
 gray_real=cv2.cvtColor(real,cv2.COLOR_BGR2GRAY)
 gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 mask=np.zeros(gray_frame.shape,np.uint8);mask[:860,:]=255
 sift=cv2.SIFT_create(nfeatures=6000,contrastThreshold=0.025)
 a,da=sift.detectAndCompute(gray_real,None)
 b,db=sift.detectAndCompute(gray_frame,mask)
 if da is None or db is None:raise RuntimeError("NO_SIFT_DESCRIPTORS")
 pairs=cv2.BFMatcher(cv2.NORM_L2).knnMatch(da,db,k=2)
 good=[m for m,n in pairs if m.distance<n.distance*.74]
 if len(good)<14:raise RuntimeError(f"insufficient matches {len(good)}")
 pa=np.float32([a[m.queryIdx].pt for m in good]).reshape(-1,1,2)
 pb=np.float32([b[m.trainIdx].pt for m in good]).reshape(-1,1,2)
 H,valid=cv2.findHomography(pa,pb,cv2.RANSAC,5.0)
 if H is None:raise RuntimeError("Cannot estimate homography")
 inliers=int(np.count_nonzero(valid))
 warped=cv2.warpPerspective(real,H,(1920,1080))
 opaque=cv2.warpPerspective(np.ones(real.shape[:2],np.uint8)*255,H,(1920,1080))
 # replace only original narration subtitle zone; feather edges
 out=frame.copy();roi=np.zeros((1080,1920),np.float32)
 roi[950:1041,260:1670]=1
 roi=cv2.GaussianBlur(roi,(0,0),5)
 roi*= (opaque>0).astype(np.float32)
 out[:]=(frame.astype(np.float32)*(1-roi[:,:,None])+warped.astype(np.float32)*roi[:,:,None]).astype(np.uint8)
 return out,H,len(good),inliers
rows=[]
for n,(t,ref) in TARGET.items():
 cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
 ok,frm=cap.read();assert ok
 photo=source(ref)
 try:
  fixed,H,matches,inliers=align(photo,frm)
  why=f"{ref}: matches={matches}, inliers={inliers}"
 except Exception as e:
  fixed=frm.copy();why="FAILED "+str(e)
 cv2.imwrite(str(OUT/f"B{n:03d}_BEFORE.jpg"),frm)
 cv2.imwrite(str(OUT/f"B{n:03d}_AFTER.jpg"),fixed)
 rows.append((n,why))
 print(n,why,flush=True)
canvas=Image.new("RGB",(1280,len(rows)*398),"#171a1c");draw=ImageDraw.Draw(canvas)
for i,(n,why) in enumerate(rows):
 y=i*398;draw.text((5,y+4),f"B{n:03d} {why}",fill="white")
 for j,stage in enumerate(["BEFORE","AFTER"]):
  im=Image.open(OUT/f"B{n:03d}_{stage}.jpg").resize((640,360))
  canvas.paste(im,(j*640,y+30))
canvas.save(OUT/"ALIGNMENT_CONTACT.jpg",quality=93)
(OUT/"RESULTS.json").write_text(json.dumps({str(n):why for n,why in rows},indent=2))
