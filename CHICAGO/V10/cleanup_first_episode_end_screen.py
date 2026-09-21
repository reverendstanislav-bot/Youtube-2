#!/usr/bin/env python3
import argparse, cv2, numpy as np
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--input",required=True)
ap.add_argument("--output",required=True)
ap.add_argument("--report",required=True)
a=ap.parse_args()

src=cv2.imread(a.input,cv2.IMREAD_COLOR)
if src is None:
    raise SystemExit("cannot read input")
h,w=src.shape[:2]
if (w,h)!=(1920,1080):
    raise SystemExit(f"unexpected canonical end-screen size {(w,h)}")

# Canonical HIA 06 End Screen has TWO video placeholder slots.
# Episode 1 must keep neither. Subscribe/avatar circle must remain untouched.
# Coordinates verified against the canonical 1920x1080 asset and V9 review.
slots=[
    # left video slot, including border/accent
    (205,325,825,660),
    # right video slot, including border/accent
    (1085,325,1695,660),
]

mask=np.zeros((h,w),dtype=np.uint8)
for x1,y1,x2,y2 in slots:
    cv2.rectangle(mask,(x1,y1),(x2,y2),255,-1)

# Protect the canonical Subscribe/avatar circle plus safety ring.
circle_center=(957,704)
circle_r=190
yy,xx=np.ogrid[:h,:w]
circle=((xx-circle_center[0])**2+(yy-circle_center[1])**2)<=circle_r**2
mask[circle]=0

# Content-aware deterministic reconstruction from the surrounding canonical artwork.
# Two-stage fill gives smoother large-area propagation than border-only V9 cleanup.
telea=cv2.inpaint(src,mask,17,cv2.INPAINT_TELEA)
ns=cv2.inpaint(src,mask,11,cv2.INPAINT_NS)
filled=cv2.addWeighted(telea,0.68,ns,0.32,0)

# Feather only the mask perimeter into untouched canonical art.
soft=cv2.GaussianBlur(mask,(0,0),sigmaX=9,sigmaY=9).astype(np.float32)/255.0
soft=np.clip(soft[...,None],0,1)
out=(src.astype(np.float32)*(1-soft)+filled.astype(np.float32)*soft).astype(np.uint8)

# Hard guarantee: Subscribe circle region remains bit-identical to canonical source.
out[circle]=src[circle]

Path(a.output).parent.mkdir(parents=True,exist_ok=True)
cv2.imwrite(a.output,out,[cv2.IMWRITE_PNG_COMPRESSION,6])

# QC.
circle_same=bool(np.array_equal(src[circle],out[circle]))

# Edge energy inside former slot-border bands before/after.
gray0=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
gray1=cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
e0=cv2.Canny(gray0,60,150)
e1=cv2.Canny(gray1,60,150)

slot_reports=[]
for n,(x1,y1,x2,y2) in enumerate(slots,1):
    band=np.zeros((h,w),np.uint8)
    t=24
    cv2.rectangle(band,(x1,y1),(x2,y2),255,t)
    before=float(e0[band>0].mean())
    after=float(e1[band>0].mean())
    slot_reports.append({
        "slot":n,
        "coords":[x1,y1,x2,y2],
        "edge_mean_before":before,
        "edge_mean_after":after,
        "reduction_ratio":(after/before if before else 0.0),
    })

# Detect residual large rectangular contours in the former slot zone.
edges=cv2.Canny(gray1,60,150)
contours,_=cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
residual=[]
for cnt in contours:
    peri=cv2.arcLength(cnt,True)
    approx=cv2.approxPolyDP(cnt,0.02*peri,True)
    if len(approx)!=4:
        continue
    x,y,rw,rh=cv2.boundingRect(approx)
    area=rw*rh
    if area<35000 or rw<220 or rh<120:
        continue
    # only flag rectangles intersecting either old slot area substantially
    for si,(x1,y1,x2,y2) in enumerate(slots,1):
        ix=max(0,min(x+rw,x2)-max(x,x1))
        iy=max(0,min(y+rh,y2)-max(y,y1))
        if ix*iy > area*0.25:
            residual.append({"slot":si,"x":x,"y":y,"w":rw,"h":rh,"area":area})
            break

import json
report={
    "source_size":[w,h],
    "slots_removed":slots,
    "subscribe_circle_center":circle_center,
    "subscribe_circle_protect_radius":circle_r,
    "subscribe_circle_region_bit_identical":circle_same,
    "slot_edge_reports":slot_reports,
    "residual_large_rectangle_candidates":residual[:30],
}
Path(a.report).write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))

if not circle_same:
    raise SystemExit("Subscribe circle was modified")
for r in slot_reports:
    if r["reduction_ratio"]>0.75:
        raise SystemExit(f"slot {r['slot']} edge reduction insufficient")
