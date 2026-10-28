"""Remove the previous film's baked intro dissolve, preserve its endscreen."""
from pathlib import Path
import json,hashlib,subprocess,sys,os,csv
ROOT=Path(__file__).resolve().parent
src=ROOT/'ASSETS/HIA_PREVIOUS_VIDEO_ENDSCREEN_18S.mp4'
dst=ROOT/'ASSETS/HIA_CLEAN_PREVIOUS_ENDSCREEN_18S.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(src),'-an','-vf','tpad=stop_mode=clone:stop_duration=2','-t','18','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],check=True)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve');sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline()
assert t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS' and not p.IsRenderingInProgress()
item=next(x for x in t.GetItemListInTrack('video',1) if x.GetStart()==117368)
assert item.GetDuration()==450 and t.GetIsTrackLocked('audio',1)
mp=p.GetMediaPool();clip=mp.ImportMedia([str(dst)])[0];assert t.DeleteClips([item],False)
added=mp.AppendToTimeline([dict(mediaPoolItem=clip,startFrame=0,endFrame=450,recordFrame=117368,trackIndex=1,mediaType=1)])
assert len(added)==1 and added[0].GetDuration()==450 and t.GetEndFrame()==117818
assert pm.SaveProject()
plan=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text());plan[-1].update(path=str(dst),source_trim='Previous endscreen source 2.00–18.00 seconds, then 2-second clean final-frame hold; excludes old Pluto crossfade',conformed_sha256=hashlib.sha256(dst.read_bytes()).hexdigest())
(ROOT/'SHOT_PLAN_R3.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (ROOT/'SHOT_PLAN_R3.csv').open(encoding='utf-8-sig') as fp:cols=next(csv.reader(fp))
with (ROOT/'SHOT_PLAN_R3.csv').open('w',encoding='utf-8-sig',newline='') as fp:w=csv.DictWriter(fp,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(plan)
(ROOT/'ENDSCREEN_CLEANUP_READBACK.json').write_text(json.dumps(dict(file=str(dst),frames=450,start=117368,end_exclusive=117818,source_trim=plan[-1]['source_trim'],sha256=plan[-1]['conformed_sha256'],source_plate_design_unchanged=True),indent=2),encoding='utf-8')
print('CLEAN_PREVIOUS_ENDSCREEN_INSTALLED_18_SECONDS')
