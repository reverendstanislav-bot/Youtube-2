from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
out=ROOT/'CONFORMED_25FPS';out.mkdir(exist_ok=True)
plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text())
unique={s['asset_id']:s for s in plan if s['kind']=='REAL_ARCHIVE_MOTION'}
def run(pair):
    aid,s=pair;source=Path(s['path']);dest=out/(aid+'_25FPS.mp4')
    if not dest.exists():
        cmd=['ffmpeg','-hide_banner','-v','error','-xerror','-y','-i',str(source),'-vf','fps=25,setpts=PTS-STARTPTS','-an','-c:v','libx264','-preset','fast','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)]
        subprocess.run(cmd,check=True,capture_output=True)
    return aid,dict(file=str(dest),original=str(source),original_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),scope='Editorial 25fps derivative; full source and selected original preserved')
rows=dict(ThreadPoolExecutor(max_workers=4).map(run,unique.items()))
for s in plan:
    if s['kind']=='REAL_ARCHIVE_MOTION':s['original_selected_clip']=s['path'];s['path']=rows[s['asset_id']]['file'];s['native_fps']='25/1'
(ROOT/'CONFORMED_MEDIA_MANIFEST.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
(ROOT/'SHOT_PLAN_R1.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'conformed':len(rows),'shots':len(plan)}))
