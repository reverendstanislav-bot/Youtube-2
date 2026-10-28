from pathlib import Path
import os,sys,json,hashlib,uuid
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject()
assert p.GetName()=='YT2 Vid7' and not p.IsRenderingInProgress()
t=p.GetCurrentTimeline();assert t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS'
v=t.GetItemListInTrack('video',1);a=t.GetItemListInTrack('audio',1)
assert len(v)==132 and len(a)==1
assert t.GetStartFrame()==90000 and t.GetEndFrame()==117368
assert t.GetTrackCount('subtitle')==0
assert t.GetIsTrackLocked('audio',1)
assert int(float(p.GetSetting('timelineFrameRate')))==25
assert a[0].GetStart()==90000 and a[0].GetEnd()==117368
assert t.SetCurrentTimecode('01:00:00:00')
assert r.OpenPage('edit')
assert pm.SaveProject()
dest=ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp'
temporary=ROOT/('CHECKPOINT_'+uuid.uuid4().hex+'.drp')
assert pm.ExportProject(p.GetName(),str(temporary),False)
assert temporary.stat().st_size>10000
temporary.replace(dest)
report=dict(project=p.GetName(),timeline=t.GetName(),timeline_start=t.GetStartFrame(),timeline_end_exclusive=t.GetEndFrame(),fps=p.GetSetting('timelineFrameRate'),width=p.GetSetting('timelineResolutionWidth'),height=p.GetSetting('timelineResolutionHeight'),video_items=len(v),audio_items=len(a),audio_locked=t.GetIsTrackLocked('audio',1),subtitle_tracks=t.GetTrackCount('subtitle'),project_saved=True,drp=str(dest),drp_bytes=dest.stat().st_size,drp_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),render_active=False)
(ROOT/'NATIVE_FINAL_READBACK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report),flush=True)
