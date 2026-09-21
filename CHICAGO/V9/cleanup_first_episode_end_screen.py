#!/usr/bin/env python3
import argparse, cv2, numpy as np
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--input",required=True)
ap.add_argument("--output",required=True)
a=ap.parse_args()

im=cv2.imread(a.input,cv2.IMREAD_COLOR)
if im is None:
    raise SystemExit("cannot read input")
h,w=im.shape[:2]
if (w,h)!=(1920,1080):
    raise SystemExit(f"unexpected canonical end-screen size {(w,h)}")

# Canonical 06 End Screen geometry audit:
# recommendation slot approx x=1146 y=354 w=529 h=284.
# Remove ONLY its border by inpainting narrow strips.
x,y,rw,rh=1146,354,529,284
pad=16
mask=np.zeros((h,w),dtype=np.uint8)

# four narrow strips around recommendation rectangle
cv2.rectangle(mask,(x-pad,y-pad),(x+rw+pad,y+pad),255,-1)
cv2.rectangle(mask,(x-pad,y+rh-pad),(x+rw+pad,y+rh+pad),255,-1)
cv2.rectangle(mask,(x-pad,y-pad),(x+pad,y+rh+pad),255,-1)
cv2.rectangle(mask,(x+rw-pad,y-pad),(x+rw+pad,y+rh+pad),255,-1)

# Preserve subscribe/avatar circle region untouched.
circle_center=(957,704)
circle_r=170
yy,xx=np.ogrid[:h,:w]
circle=((xx-circle_center[0])**2+(yy-circle_center[1])**2)<=circle_r**2
mask[circle]=0

out=cv2.inpaint(im,mask,7,cv2.INPAINT_TELEA)
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
cv2.imwrite(a.output,out,[cv2.IMWRITE_PNG_COMPRESSION,6])

# QC metrics: border edge energy should fall substantially; circle area must remain bit-identical.
gray0=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
gray1=cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
e0=cv2.Canny(gray0,60,150)
e1=cv2.Canny(gray1,60,150)
border_mask=mask>0
before=float(e0[border_mask].mean()) if border_mask.any() else 0
after=float(e1[border_mask].mean()) if border_mask.any() else 0
circle_same=bool(np.array_equal(im[circle],out[circle]))
print(f"rectangle_border_edge_mean_before={before:.6f}")
print(f"rectangle_border_edge_mean_after={after:.6f}")
print(f"subscribe_circle_region_bit_identical={circle_same}")
if not circle_same:
    raise SystemExit("subscribe circle region changed")
