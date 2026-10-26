"""Full clip decode/black/freeze scan and content fingerprints; no human playback claim."""
import json,csv,subprocess,hashlib,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import numpy as np
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
def run(args):return subprocess.run(args,capture_output=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4<<20),b''):h.update(b)
 return h.hexdigest()
def inspect(row):
 p=Path(row['cut_filename']);sid=row['scene_id']
 meta=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]).stdout)
 v=next(s for s in meta['streams'] if s['codec_type']=='video')
 scan=run(['ffmpeg','-nostdin','-hide_banner','-loglevel','info','-xerror','-i',str(p),'-map','0:v:0','-an','-vf','blackdetect=d=0.10:pix_th=0.10:pic_th=0.98,freezedetect=n=-55dB:d=1.0','-f','null','-'])
 log=scan.stderr.decode('utf-8','replace');(ROOT/'reports'/f'{sid}_FULL_CLIP_SCAN.log').write_text(log)
 frames=run(['ffmpeg','-v','error','-i',str(p),'-an','-vf','fps=5,scale=64:48,format=gray','-f','rawvideo','-'])
 a=np.frombuffer(frames.stdout,dtype=np.uint8).reshape(-1,48*64).astype('float32')
 z=a-a.mean(axis=1,keepdims=True);z/=np.maximum(np.linalg.norm(z,axis=1,keepdims=True),1e-8)
 np.save(ROOT/'reports'/f'{sid}_FINGERPRINT.npy',z)
 dif=np.abs(a[1:]-a[:-1]).mean(axis=1) if len(a)>1 else np.array([0])
 black=[m.group(0) for m in re.finditer(r'black_start:[^\r\n]+',log)]
 freeze=[m.group(0) for m in re.finditer(r'lavfi\.freezedetect\.[^\r\n]+',log)]
 result={'scene_id':sid,'sha256':sha(p),'size_bytes':p.stat().st_size,'full_decode_exit_code':scan.returncode,'fingerprint_exit_code':frames.returncode,'seconds':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'sar':v.get('sample_aspect_ratio'),'field_order':v.get('field_order'),'audio_tracks':sum(s['codec_type']=='audio' for s in meta['streams']),'black_events':black,'freeze_events':freeze,'mean_5fps_pixel_change':float(dif.mean()),'max_5fps_pixel_change':float(dif.max()),'qc_status':'TECHNICAL_PASS' if scan.returncode==0 and frames.returncode==0 and not black and not freeze else 'REVIEW_HOLD'}
 assert result['sha256']==row['cut_sha256'],sid
 print(sid,result['qc_status'],len(a),flush=True)
 return result
def main():
 rows=list(csv.DictReader((ROOT/'reports/extraction_results.csv').open(newline='',encoding='utf-8')))
 rows=[r for r in rows if r['status']=='PHYSICALLY_EXTRACTED_PENDING_DUP_QC']
 out=[]
 with ThreadPoolExecutor(max_workers=3) as pool:
  for f in as_completed([pool.submit(inspect,r) for r in rows]):out.append(f.result())
 out.sort(key=lambda x:x['scene_id']);(ROOT/'reports/CLIP_TECHNICAL_QC.json').write_text(json.dumps(out,indent=2))
 # Compare five-second sequences of 1fps fingerprints, not isolated similar snowy frames.
 arrays={r['scene_id']:np.load(ROOT/'reports'/f"{r['scene_id']}_FINGERPRINT.npy")[::5] for r in out}
 possible=[]
 for i,a in enumerate(out):
  for b in out[i+1:]:
   aa=arrays[a['scene_id']];bb=arrays[b['scene_id']];corr=aa@bb.T
   best=(-1,None,None)
   for x in range(max(0,len(aa)-4)):
    for y in range(max(0,len(bb)-4)):
     c=float(np.mean([corr[x+k,y+k] for k in range(5)]))
     if c>best[0]:best=(c,x,y)
   if best[0]>=0.955:possible.append({'scene_a':a['scene_id'],'scene_b':b['scene_id'],'mean_five_second_ncc':best[0],'a_offset_seconds':best[1],'b_offset_seconds':best[2],'decision':'CANDIDATE_VISUAL_REVIEW_REQUIRED_NOT_CONFIRMED'})
 (ROOT/'reports/SELECTED_CLIP_DUPLICATE_CANDIDATES.json').write_text(json.dumps(possible,indent=2))
 print('QC_COMPLETE',len(out),'HOLDS',sum(x['qc_status']!='TECHNICAL_PASS' for x in out),'DUPLICATE_CANDIDATES',len(possible),flush=True)
if __name__=='__main__':main()
