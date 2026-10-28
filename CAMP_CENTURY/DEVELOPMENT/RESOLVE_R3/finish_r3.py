"""Wait for the real nine native exports; then make and QC a complete review."""
from pathlib import Path
import json,subprocess,sys,time,os,uuid,hashlib
ROOT=Path(__file__).resolve().parent
MOVIE=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R3\HIA_VIDEO007_CAMP_CENTURY_R3_PROXY_1080P25.mp4')
deadline=time.monotonic()+7200;last=-1
while True:
    try:rows=json.loads((ROOT/'CHAPTER_RENDER_RESULTS.json').read_text())
    except (FileNotFoundError,json.JSONDecodeError):rows=[]
    if len(rows)!=last:print('VERIFIED_NATIVE_PARTS',len(rows),flush=True);last=len(rows)
    if len(rows)==9 and sum(x['frames'] for x in rows)==27818:break
    if time.monotonic()>deadline:raise TimeoutError('Incomplete native parts; no full-file claim')
    time.sleep(10)
for name,args in [('mux_proxy.py',[]),('qc_proxy.py',[str(MOVIE)]),('qc_motion_samples.py',[str(MOVIE)])]:
    print('STAGE',name,flush=True);subprocess.run([sys.executable,str(ROOT/name),*args],check=True)
    if name=='qc_proxy.py':assert json.loads((ROOT/'QC/PROXY_QC.json').read_text())['technical_checks_pass']
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve');sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline()
assert p.GetName()=='YT2 Vid7' and t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS' and not p.IsRenderingInProgress()
plan=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text());v=t.GetItemListInTrack('video',1);a=t.GetItemListInTrack('audio',1)
assert len(v)==len(plan)==124 and len(a)==1 and t.GetStartFrame()==90000 and t.GetEndFrame()==117818
assert a[0].GetStart()==90000 and a[0].GetEnd()==117368 and t.GetIsTrackLocked('audio',1) and t.GetTrackCount('subtitle')==0
assert t.SetCurrentTimecode('01:00:00:00') and r.OpenPage('edit') and pm.SaveProject()
tmp=ROOT/('CHECKPOINT_'+uuid.uuid4().hex+'.drp');assert pm.ExportProject(p.GetName(),str(tmp),False)
dest=ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3.drp';tmp.replace(dest)
report=dict(project=p.GetName(),timeline=t.GetName(),fps=p.GetSetting('timelineFrameRate'),width=p.GetSetting('timelineResolutionWidth'),height=p.GetSetting('timelineResolutionHeight'),video_items=len(v),audio_items=len(a),timeline_start=90000,timeline_end_exclusive=117818,audio_start=90000,audio_end_exclusive=117368,audio_locked=True,subtitle_tracks=0,render_active=False,project_saved=True,drp_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
(ROOT/'NATIVE_FINAL_READBACK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
scan=ROOT/'QC/FULL_DECODE_AND_BLACK_SCAN.log'
if scan.exists():scan.write_text('\n'.join(s.rstrip() for s in scan.read_text().splitlines()).rstrip()+'\n',encoding='utf-8')
print('FULL_R3_TECHNICAL_QC_DONE_OWNER_REVIEW_PENDING',flush=True)
