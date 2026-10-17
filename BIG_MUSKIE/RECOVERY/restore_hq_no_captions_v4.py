#!/usr/bin/env python3
"""Big Muskie V4: source-matched REAL frames + LaMa restored GFX subtitle bands.

Input is exact physical 1.527GB master; audio AAC copied from input untouched.
No subtitles are generated. Full-frame 1920x1080 and timeline preserved.
Cleaned synthetic-inpaint areas are subject to human editorial QC.
"""
import importlib.util,pathlib,sys,numpy as np,cv2
from PIL import Image,ImageDraw
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("bm_v3",(HERE/"restore_hq_no_captions_v3.py"))
v3=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v3;spec.loader.exec_module(v3)
from simple_lama_inpainting import SimpleLama
import torch
_orig_torch_load=torch.jit.load
def _force_cpu(*args,**kwargs):
 kwargs['map_location']=torch.device('cpu')
 return _orig_torch_load(*args,**kwargs)
torch.jit.load=_force_cpu
torch.set_num_threads(3)
lama=SimpleLama(device=torch.device('cpu'))
BAD_GFX={14,16,28,46,71,76,88,94,95,106}
# Mask only the narration caption baseline and its drop-shadow.
# For B095, extend upward to remove the fragments observed in V3.
MASK_TOP={95:880,94:904,88:915,71:915,76:915,106:910}
SAMPLED=[]
def repair_ref(ref,out):
 n=int(ref.stem)
 if n not in BAD_GFX:
  return v3.draw_patch(ref,out)
 img=cv2.imread(str(ref))
 if img is None:raise RuntimeError(f'Missing actual V4 source beat reference {n}')
 y0=MASK_TOP.get(n,905)
 top=max(875,y0);bottom=1050
 pil=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
 m=Image.new('L',pil.size,0);d=ImageDraw.Draw(m);d.rectangle((210,top,1715,bottom),fill=255)
 clean=lama(pil,m)
 cleaned=cv2.cvtColor(np.asarray(clean.convert('RGB')),cv2.COLOR_RGB2BGR)
 im=cleaned[v3.bm.Y0:v3.bm.Y1,v3.bm.X0:v3.bm.X1]
 rgba=cv2.cvtColor(im,cv2.COLOR_BGR2BGRA)
 H,W=im.shape[:2]
 a=np.ones((H,W),np.float32)
 for i in range(H):
  edge=min(i,H-i-1);a[i,:]*=min(1.0,edge/13)
 for j in range(W):
  edge=min(j,W-j-1);a[:,j]*=min(1.0,edge/19)
 rgba[:,:,3]=(a*255).astype(np.uint8)
 if not cv2.imwrite(str(out),rgba,[cv2.IMWRITE_PNG_COMPRESSION,4]):
  raise RuntimeError(f"Couldn't save cleaned original 1920x1080 GFX beat {n}")
 qc=out.parent.parent/"v4_reference_qc"
 qc.mkdir(exist_ok=True,parents=True)
 cv2.imwrite(str(qc/f"B{n:03d}_LAMA_1080P.jpg"),cleaned,[cv2.IMWRITE_JPEG_QUALITY,93])
 SAMPLED.append(n)
 print('V4_LAMA_CLEAN_REF',n,'region',210,top,1715,bottom,flush=True)
v3.bm.draw_patch=repair_ref
if __name__=='__main__':
 v3.bm.main()
 print('V4_LAMA_BEATS_DONE',sorted(SAMPLED),flush=True)
