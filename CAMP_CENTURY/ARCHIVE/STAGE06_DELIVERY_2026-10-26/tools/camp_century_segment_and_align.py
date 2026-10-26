from pathlib import Path
import numpy as np,json,subprocess,re,concurrent.futures
from PIL import Image
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
def shots(sid):
    file=next(p for p in (R/'masters').glob(sid+'.*') if p.suffix in ['.mpeg','.mp4'])
    log=R/'reports'/(sid+'_SCENE_CUTS.json')
    if log.exists():return
    p=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-v','info','-i',str(file),'-an','-vf',"setpts=PTS-STARTPTS,select='gt(scene,0.28)',showinfo",'-fps_mode','vfr','-f','null','-'],capture_output=True,text=True,check=True)
    pts=[float(n) for n in re.findall(r'\bpts_time:([\d.]+)',p.stderr)]
    log.write_text(json.dumps({'source_id':sid,'threshold':.28,'purpose':'Scene-boundary hints only; not automatic approval','times':pts},indent=2))
    print('SCENE_BOUNDARIES',sid,len(pts),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(shots,['F01B','F02','F03','F05']))

def features(sid):
    raw=np.fromfile(R/'reports'/(sid+'_GRAY_1FPS_64x48.bin'),np.uint8).reshape(-1,48,64)
    small=np.stack([np.asarray(Image.fromarray(f[4:-4,5:-5]).resize((24,18),Image.Resampling.BILINEAR)) for f in raw]).astype(np.float32).reshape(len(raw),-1)
    small-=small.mean(axis=1,keepdims=True)
    small/=np.maximum(1,np.linalg.norm(small,axis=1,keepdims=True))
    return small
canonical=features('F01B');alignments=[]
for sid in ['F01','F02','F03','F04','F05','F06']:
    other=features(sid);best=[]
    for start in range(0,len(other),256):
        matrix=other[start:start+256]@canonical.T;idx=matrix.argmax(axis=1);score=matrix[np.arange(len(idx)),idx]
        best.extend([{'source_sec':start+i,'canonical_F01B_sec':int(j),'correlation':round(float(s),5)} for i,(j,s) in enumerate(zip(idx,score))])
    candidates=[]
    for i in range(0,len(best)-4):
        block=best[i:i+5]
        if min(b['correlation'] for b in block)<.89:continue
        offsets=[b['canonical_F01B_sec']-b['source_sec'] for b in block]
        if max(offsets)-min(offsets)<=2:
            candidates.append({'source_start_sec':i,'source_end_sec':i+5,'canonical_start_sec':block[0]['canonical_F01B_sec'],'minimum_correlation':min(b['correlation'] for b in block),'verdict':'CANDIDATE_REQUIRES_PICTURE_CONFIRMATION'})
    (R/'reports'/(sid+'_ALIGNMENT_TO_F01B.json')).write_text(json.dumps({'source_id':sid,'per_second_best':best,'candidate_five_second_matches':candidates},indent=2))
    print('CROSS_PRINT_CANDIDATES',sid,len(candidates),flush=True)
