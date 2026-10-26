"""Frame-exact native-SD extraction. R5 source/location/rights/beat eligibility checks.
One full linear source decode per batch; trim by decoded frame index, never MPEG fast seek.
"""
import json,subprocess,csv,math,hashlib,shutil
from pathlib import Path
from fractions import Fraction
from concurrent.futures import ThreadPoolExecutor
import importlib.util
_spec=importlib.util.spec_from_file_location('ccprep',r'C:\Users\KK\camp_century_cut_reviewed.py')
prep=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(prep)
ROOT=prep.ROOT;r5=prep.r5
def extract_source(sid):
 allrows=json.loads((ROOT/'reports/REVIEWED_SCENES.json').read_text())
 rows=[r for r in allrows if r['source_id']==sid]
 audit={r['source_id']:r for r in json.loads((ROOT/'reports/physical_originals.json').read_text())}
 src=Path(rows[0]['source_path']);prior=audit[sid]
 assert prior['status']=='FULL_DECODE_PASS' and r5.digest(src)==prior['sha256']
 for r in rows:
  assert r['site_class'] in r5.ALLOW_LOC and r['beat'].startswith('CC07-S4-') and r['chapter'] in r5.CHAPTER_WORDS
  assert r['verified_by'] and r['actual_shot_description'] and r['status']=='APPROVED' and not r['duplicate_of']
  assert (ROOT/'rights_receipts'/r['rights_receipt']).stat().st_size>=30
  assert 5<=r['seconds']<=20 and r['end_sec']<=prior['duration']
  assert not (ROOT/'clips'/f"{r['scene_id']}.mp4").exists()
 # <=12 encoders per decode avoids excessive encoder queues; decode stays exact.
 for start in range(0,len(rows),12):
  batch=rows[start:start+12]
  filters=['[0:v:0]split='+str(len(batch))+''.join(f'[s{k}]' for k in range(len(batch)))]
  for k,r in enumerate(batch):filters.append(f"[s{k}]trim=start_frame={r['start_frame']}:end_frame={r['end_frame_exclusive']},setpts=PTS-STARTPTS[v{k}]")
  args=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-xerror','-threads','2','-i',str(src),'-filter_complex_threads','1','-filter_complex',';'.join(filters)]
  for k,r in enumerate(batch):
   args+=['-map',f'[v{k}]','-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-threads','1','-fps_mode','passthrough','-movflags','+faststart']
   if sid=='F05':args+=['-flags','+ilme+ildct','-x264-params','bff=1']
   args += [str(ROOT/'clips'/f"{r['scene_id']}.mp4")]
  result=subprocess.run(args,capture_output=True,text=True)
  (ROOT/'reports'/f'{sid}_EXACT_BATCH_{start:03d}.log').write_text(result.stderr)
  assert result.returncode==0,result.stderr[-3000:]
  for r in batch:
   dst=ROOT/'clips'/f"{r['scene_id']}.mp4";meta=r5.probe(dst);vi=r5.video_info(meta)
   v=next(x for x in meta['streams'] if x['codec_type']=='video')
   assert int(v['nb_frames'])==r['end_frame_exclusive']-r['start_frame'],r['scene_id']
   assert abs(vi['duration']-r['seconds'])<0.002,(r['scene_id'],vi['duration'],r['seconds'])
   assert vi['width']==prior['width'] and vi['height']==prior['height'] and vi['audio_tracks']==0
   r.update(cut_filename=str(dst),cut_sha256=r5.digest(dst),cut_seconds=f"{vi['duration']:.6f}",native_width=vi['width'],native_height=vi['height'],source_sha256=prior['sha256'],status='PHYSICALLY_EXTRACTED_PENDING_DUP_QC')
   print('EXACT_EXTRACTED',r['scene_id'],vi['duration'],flush=True)
  (ROOT/'reports'/f'{sid}_EXACT_EXTRACTION.json').write_text(json.dumps(rows,indent=2))
 return rows
if __name__=='__main__':
 quarantine=ROOT/'reports/REJECTED_FAST_SEEK';quarantine.mkdir(exist_ok=True)
 for p in (ROOT/'clips').glob('CC07-C*.mp4'):
  target=quarantine/p.name
  assert not target.exists()
  shutil.move(str(p),str(target))
 with ThreadPoolExecutor(max_workers=2) as pool:out=sum(list(pool.map(extract_source,['F01B','F03','F05'])),[])
 out.sort(key=lambda r:r['scene_id'])
 r5.write_rows(ROOT/'reports/extraction_results.csv',out,r5.HEADERS)
 (ROOT/'reports/FRAME_EXACT_CUT_RESULTS.json').write_text(json.dumps(out,indent=2))
 print('FRAME_EXACT_FINISHED',len(out),'seconds',sum(float(x['cut_seconds']) for x in out),flush=True)
