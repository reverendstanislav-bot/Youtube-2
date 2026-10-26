"""Compare actual exported first/middle/last frame to full-decode source frame indices."""
import json,subprocess,numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
rows=json.loads((ROOT/'reports/FRAME_EXACT_CUT_RESULTS.json').read_text())
def extract(p,indices):
 def balanced(xs):
  if len(xs)==1:return xs[0]
  k=len(xs)//2
  return '('+balanced(xs[:k])+'+'+balanced(xs[k:])+')'
 expression=balanced([f'eq(n\\,{n})' for n in indices])
 r=subprocess.run(['ffmpeg','-nostdin','-v','error','-threads','2','-i',str(p),'-an','-vf',f'select={expression},scale=64:48,format=gray','-fps_mode','passthrough','-f','rawvideo','-'],capture_output=True)
 assert r.returncode==0,r.stderr[-500:]
 a=np.frombuffer(r.stdout,np.uint8).reshape(-1,3072).astype('float32');assert len(a)==len(indices),(p,len(a),len(indices))
 return a
sources={}
for sid in sorted({r['source_id'] for r in rows}):
 rr=[r for r in rows if r['source_id']==sid];inds=sorted({n for r in rr for n in [r['start_frame'],(r['start_frame']+r['end_frame_exclusive']-1)//2,r['end_frame_exclusive']-1]})
 a=extract(rr[0]['source_path'],inds);sources[sid]=dict(zip(inds,a));print('SOURCE_FRAME_REFERENCES',sid,len(inds),flush=True)
def check(r):
 n=r['end_frame_exclusive']-r['start_frame'];srcinds=[r['start_frame'],(r['start_frame']+r['end_frame_exclusive']-1)//2,r['end_frame_exclusive']-1]
 a=extract(r['cut_filename'],[0,(n-1)//2,n-1]);b=np.stack([sources[r['source_id']][k] for k in srcinds]);cor=[]
 for x,y in zip(a,b):cor.append(float(np.corrcoef(x,y)[0,1]))
 return {'scene_id':r['scene_id'],'source_reference_frames':srcinds,'output_reference_frames':[0,(n-1)//2,n-1],'first_middle_last_ncc':cor,'status':'SOURCE_FRAME_MATCH_PASS' if min(cor)>0.98 else 'SOURCE_FRAME_MATCH_HOLD'}
with ThreadPoolExecutor(max_workers=3) as pool:result=list(pool.map(check,rows))
(ROOT/'reports/EXPORTED_FRAME_SOURCE_CORRESPONDENCE.json').write_text(json.dumps(result,indent=2))
print('BOUNDARIES',len(result),'PASS',sum(r['status']=='SOURCE_FRAME_MATCH_PASS' for r in result),'MIN_NCC',min(min(r['first_middle_last_ncc']) for r in result),flush=True)
assert all(r['status']=='SOURCE_FRAME_MATCH_PASS' for r in result)
