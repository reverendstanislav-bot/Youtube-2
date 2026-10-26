import json,subprocess,io
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
def frame(sid,t):
 p=next(p for p in (ROOT/'masters').glob(sid+'.*') if p.suffix in ['.mp4','.mpeg'])
 r=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=320:240','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True,check=True)
 return Image.open(io.BytesIO(r.stdout)).convert('RGB')
out=[]
for sid in ['F01','F02','F04','F06']:
 data=json.loads((ROOT/'reports'/f'{sid}_ALIGNMENT_TO_F01B.json').read_text())['candidate_five_second_matches']
 if not data:continue
 raw=np.fromfile(ROOT/'reports'/f'{sid}_GRAY_1FPS_64x48.bin',dtype=np.uint8).reshape(-1,3072).astype(float)
 def score(r):
  t=int(r['source_start_sec']);motion=np.abs(raw[t+1:t+5]-raw[t:t+4]).mean()
  return r['minimum_correlation']+min(motion,10)*0.005
 choice=sorted(data,key=score,reverse=True)[0]
 st=choice['source_start_sec'];ct=choice['canonical_start_sec']
 canvas=Image.new('RGB',(960,540),'#111');d=ImageDraw.Draw(canvas)
 for j,off in enumerate([0.4,2.4,4.4]):
  canvas.paste(frame(sid,st+off),(j*320,0));canvas.paste(frame('F01B',ct+off),(j*320,270))
 d.text((4,244),f'{sid} {st:.3f}-{st+5:.3f}',fill='white');d.text((4,514),f'F01B {ct:.3f}-{ct+5:.3f}',fill='white')
 path=ROOT/'qc_sheets'/f'DUPLICATE_{sid}_F01B.jpg';canvas.save(path,quality=90)
 out.append({'source_id':sid,'source_start_sec':st,'source_end_sec':st+5,'canonical_source_id':'F01B','canonical_start_sec':ct,'canonical_end_sec':ct+5,'correlation':choice['minimum_correlation'],'proof_path':str(path),'status':'VISUAL_CONFIRMATION_PENDING'})
(ROOT/'reports/DUPLICATE_PROOF_CANDIDATES.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
