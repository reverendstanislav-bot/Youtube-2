#!/usr/bin/env python3
"""V3: Big Muskie clean-source HQ restoration: preserve true full frame and original Arthur.

More reliable correction to V1: expands patch capture zone to y=875-1050,
uses actual authenticated Wikimedia source pixels matched by SIFT homography
where available; otherwise title-specific constrained OpenCV inpaint only for
visually REJECTED scenes. No AI credit spending.
Editorial QC is required before labeling any generated MP4 final.
"""
import cv2,json,sys,importlib.util,pathlib,os
import numpy as np

BASEFILE=pathlib.Path(__file__).resolve().parent/"restore_burned_captions_without_crop.py"
spec=importlib.util.spec_from_file_location("bm_base",str(BASEFILE))
bm=importlib.util.module_from_spec(spec);sys.modules[spec.name]=bm;spec.loader.exec_module(bm)
bm.Y0=875
bm.Y1=1050
bm.X0=100
bm.X1=1820
W=pathlib.Path(os.getenv("BIG_MUSKIE_COMMONS_DIR","/tmp/bigmuskie-commons-align"))
CONFIG=W/"commons.json"
BADS=set([2,3,14,16,18,28,30,46,71,76,88,93,94,95,101,106,107])
PHOTO_MAP={2:"R06",3:"R07",18:"R03",30:"R03",93:"C01",101:"R07",106:"R10",107:"R10"}
FLATBACK=set([14,16,46,71,76,88,94,95,106])
texture_cache={}

def homography_photo(src,ref,n):
 kp_ref_src=src
 gray=cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
 s=cv2.SIFT_create(nfeatures=5500,contrastThreshold=.024)
 ks,ds=s.detectAndCompute(cv2.cvtColor(src,cv2.COLOR_BGR2GRAY),None)
 mask=np.zeros(gray.shape,np.uint8);mask[:865,:]=255
 kr,dr=s.detectAndCompute(gray,mask)
 if ds is None or dr is None:raise ValueError("SIFT descriptors absent")
 matches=cv2.BFMatcher(cv2.NORM_L2).knnMatch(ds,dr,k=2)
 good=[x for x,y in matches if x.distance<y.distance*.76]
 if len(good)<18:raise ValueError("Not enough SIFT matches "+str(len(good)))
 psrc=np.float32([ks[k.queryIdx].pt for k in good]).reshape(-1,1,2)
 pdst=np.float32([kr[k.trainIdx].pt for k in good]).reshape(-1,1,2)
 H,valid=cv2.findHomography(psrc,pdst,cv2.RANSAC,5.)
 ins=int(np.count_nonzero(valid))
 if ins<15:raise ValueError("SIFT inliers="+str(ins))
 warped=cv2.warpPerspective(src,H,(ref.shape[1],ref.shape[0]))
 alpha=cv2.warpPerspective(np.ones(src.shape[:2],np.uint8)*255,H,(ref.shape[1],ref.shape[0]))
 print(f"AUTHENTIC PHOTO B{n:03d} matches={len(good)} inliers={ins}",flush=True)
 return warped,alpha

def repair_source_fullframe(img,n):
 # For exact authentic-photo matches, recover captioned pixel content from original
 # photograph and preserve on-screen graphic source pixels outside the narrative captions.
 if n in PHOTO_MAP and CONFIG.exists():
  cfg=json.loads(CONFIG.read_text())
  orig=cv2.imread(str(cfg[PHOTO_MAP[n]]))
  if orig is not None:
   try:
    clean,valid=homography_photo(orig,img,n)
    # Recover full central caption band (caption y varies by source).
    alpha=np.zeros(img.shape[:2],np.float32)
    alpha[885:1045,240:1715]=1
    alpha=cv2.GaussianBlur(alpha,(0,0),4.)
    alpha*= (valid>0).astype(np.float32)
    return (img.astype(np.float32)*(1-alpha[:,:,None])+clean.astype(np.float32)*alpha[:,:,None]).astype(np.uint8),"SOURCE_MATCH"
   except Exception as e:print(f"AUTHENTIC SOURCE ALIGN B{n:03d} FAILED:",str(e),flush=True)
 if n in BADS:
  # Unmatched synthetic GFX scene: localized content-aware pixel restoration,
  # no resize/crop. Heavy background restoration stays limited to caption area.
  mask=np.zeros(img.shape[:2],np.uint8)
  if n in [71,76,93,94,95,107]:
   y0,y1=889,1044
  elif n in [14,16,18,28,30,46,88,106]:
   y0,y1=918,1044
  else:
   y0,y1=945,1044
  mask[y0:y1,275:1670]=255
  if n in FLATBACK:
   radius=17
  else:radius=12
  print(f"CONTENT REPAIR B{n:03d} region y={y0}:{y1}",flush=True)
  return cv2.inpaint(img,mask,radius,cv2.INPAINT_TELEA),"INPAINT"
 return img,"CLEAN_STILL_REFERENCE"

def draw_patch(ref,output):
 n=int(ref.stem)
 img=cv2.imread(str(ref))
 if img is None:raise RuntimeError("No video reference still "+str(ref))
 fixed,method=repair_source_fullframe(img,n)
 clip=fixed[bm.Y0:bm.Y1,bm.X0:bm.X1]
 rgba=cv2.cvtColor(clip,cv2.COLOR_BGR2BGRA)
 hh,ww=clip.shape[:2]
 a=np.ones((hh,ww),np.float32)
 for idx in range(hh):
  ed=min(idx,hh-idx-1)
  a[idx,:]*=min(1,ed/13)
 for idx in range(ww):
  ed=min(idx,ww-idx-1)
  a[:,idx]*=min(1,ed/19)
 rgba[:,:,3]=(a*255).astype(np.uint8)
 cv2.imwrite(str(output),rgba,[cv2.IMWRITE_PNG_COMPRESSION,5])
 # image of the exact reconstructed reference, for independent visual QC.
 diag=output.parent.parent/"reference_plate_qc"
 diag.mkdir(exist_ok=True,parents=True)
 if n in BADS or n%10==0:
  cv2.imwrite(str(diag/f"B{n:03d}_{method}.jpg"),fixed,[cv2.IMWRITE_JPEG_QUALITY,90])

bm.draw_patch=draw_patch
if __name__=="__main__":
 bm.main()
