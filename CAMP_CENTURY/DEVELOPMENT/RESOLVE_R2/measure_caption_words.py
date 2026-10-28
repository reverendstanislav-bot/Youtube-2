"""Measure clean generated caption ink, without OCR rewriting its contents."""
from pathlib import Path
from PIL import Image
import numpy as np,json
ROOT=Path(__file__).resolve().parent
image=ROOT.parents[1]/'GRAPHICS/STAGE07_CORRECTIONS_R3/assets/Q01.png'
a=np.asarray(Image.open(image).convert('RGB'));h,w=a.shape[:2]
ink=np.max(a,axis=2)<100
def runs(values,gap):
    pos=np.flatnonzero(values);out=[]
    if not len(pos):return out
    start=last=int(pos[0])
    for n in pos[1:]:
        if n-last>gap:out.append((start,last+1));start=int(n)
        last=int(n)
    out.append((start,last+1));return out
ys=runs((ink[:,int(.04*w):int(.94*w)].sum(axis=1)>8)&(np.arange(h)>.80*h),3)
rows=[]
for y0,y1 in ys:
    if y1-y0<10:continue
    cols=runs(ink[y0:y1].sum(axis=0)>0,9)
    rows.append(dict(y=[y0,y1],words=cols))
print(json.dumps(dict(size=[w,h],lines=rows),indent=2))
