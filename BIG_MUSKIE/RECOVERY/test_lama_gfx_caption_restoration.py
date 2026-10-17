#!/usr/bin/env python3
"""One-shot free CPU LaMa inpainting diagnostic for Big Muskie narration captions in GFX beats.
Never treat output as historically authentic pixels or editorial QC approved.
"""
import pathlib,json,os,subprocess,time
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFilter
from simple_lama_inpainting import SimpleLama
WORK=pathlib.Path('/tmp/bigmuskie_lama_test');WORK.mkdir(exist_ok=True,parents=True)
SOURCE=pathlib.Path('/tmp/bm_master/BIG_MUSKIE_FINAL_UPLOAD_MASTER.mp4')
assert SOURCE.stat().st_size==1527013934
# Representative moments checked manually in current timeline from the worst 116-beat GFX scenes
TIMES={14:174.2,16:196.4,28:359.6,46:576.8,71:895.4,76:943.8,88:1092.8,94:1160.0,95:1167.4,106:1300.0}
# Inpainting only the exact caption baseline, not whole 175px wide previous smear band.
# Left and right 100px left untouched.
AREAS={14:(220,920,1715,1050),16:(220,920,1715,1050),28:(220,920,1715,1050),46:(220,920,1715,1050),71:(220,930,1715,1050),76:(220,920,1715,1050),88:(220,928,1715,1040),94:(220,920,1715,1050),95:(220,920,1715,1050),106:(220,920,1715,1050)}
import torch
lama=SimpleLama(device=torch.device('cpu'))
print('LAMA model ready',flush=True)
for n,t in TIMES.items():
 st=time.time()
 dst=WORK/f'B{n:03d}_ORIGINAL.jpg'
 subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y','-ss',str(t),'-i',str(SOURCE),'-frames:v','1',str(dst)],check=True)
 input_image=Image.open(dst).convert('RGB')
 mask=Image.new('L',input_image.size,0)
 d=ImageDraw.Draw(mask)
 area=AREAS[n]
 d.rectangle(area,fill=255)
 output=lama(input_image,mask)
 output.save(WORK/f'B{n:03d}_LAMA.jpg',quality=96)
 mask.save(WORK/f'B{n:03d}_MASK.png')
 w=960
 a=input_image.resize((960,540),Image.Resampling.LANCZOS)
 b=output.resize((960,540),Image.Resampling.LANCZOS)
 joint=Image.new('RGB',(1920,540),'#171a1c');joint.paste(a,(0,0));joint.paste(b,(960,0))
 joint.save(WORK/f'B{n:03d}_COMPARISON.jpg',quality=91)
 print('QC_SCENE',n,'TIME_SEC',t,'RUNTIME_SEC',round(time.time()-st,2),flush=True)
print('DONE; preview ready',flush=True)
