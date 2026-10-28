"""Build an isolated native Resolve R3, preserving the accepted WAV and R2."""
from pathlib import Path
import sys,os,json,hashlib
ROOT=Path(__file__).resolve().parent;MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();assert p.GetName()=='YT2 Vid7' and not p.IsRenderingInProgress()
name='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS'
names=[p.GetTimelineByIndex(i).GetName() for i in range(1,p.GetTimelineCount()+1)]
assert name not in names,'R3 exists: inspect readback instead of overwriting it'
old=next(p.GetTimelineByIndex(i) for i in range(1,p.GetTimelineCount()+1) if p.GetTimelineByIndex(i).GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS')
assert pm.SaveProject();t=old.DuplicateTimeline(name);assert t and p.SetCurrentTimeline(t)
assert t.GetIsTrackLocked('audio',1) and t.GetTrackCount('subtitle')==0
audio=t.GetItemListInTrack('audio',1);assert len(audio)==1 and audio[0].GetStart()==90000 and audio[0].GetEnd()==117368
audio_path=audio[0].GetMediaPoolItem().GetClipProperty('File Path')
assert hashlib.sha256(Path(audio_path).read_bytes()).hexdigest()=='c6a5df8cff089418f4f2300551fd4ba6cb057dcd3012b84fa8143e02976d0480'
assert t.GetTrackCount('video')==1
assert t.DeleteClips(t.GetItemListInTrack('video',1),False)
plan=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text());mp=p.GetMediaPool()
carrier=str(ROOT.parent/'RESOLVE_R1/FUSION_CARRIER_60S_25FPS.mp4')
paths=list(dict.fromkeys([carrier]+[s['path'] for s in plan if 'comp' not in s]))
clips={}
for path in paths:
    imported=mp.ImportMedia([path]);assert imported and len(imported)==1,path;clips[path]=imported[0]
args=[dict(mediaPoolItem=clips[carrier if 'comp' in s else s['path']],startFrame=0,endFrame=s['duration_frames'],recordFrame=90000+s['start_frame'],trackIndex=1,mediaType=1) for s in plan]
added=mp.AppendToTimeline(args);assert len(added)==len(plan),(len(added),len(plan))
items={int(x.GetStart()):x for x in t.GetItemListInTrack('video',1)};records=[]
for j,s in enumerate(plan):
    item=items[90000+s['start_frame']];assert item.GetDuration()==s['duration_frames'],s['shot_id']
    if 'comp' in s:
        comp=item.ImportFusionComp(s['comp']);assert comp and item.GetFusionCompCount()==1
        for node in (comp.GetToolList(False) or {}).values():
            value=node.GetInput('UseGPU')
            if value is not None:
                if value!=0:node.SetInput('UseGPU',0)
                assert node.GetInput('UseGPU')==0
    records.append(dict(shot=s['shot_id'],asset=s['asset_id'],kind=s['kind'],start=item.GetStart(),end_exclusive=item.GetEnd(),frames=item.GetDuration(),native_comp_count=item.GetFusionCompCount(),actual_source=item.GetMediaPoolItem().GetClipProperty('File Path')))
    if (j+1)%25==0:print('R3_NATIVE_ITEMS_VERIFIED',j+1,flush=True)
assert t.GetStartFrame()==90000 and t.GetEndFrame()==117818 and len(t.GetItemListInTrack('audio',1))==1 and t.GetIsTrackLocked('audio',1)
assert audio[0].GetStart()==90000 and audio[0].GetEnd()==117368
assert t.SetCurrentTimecode('01:00:00:00') and r.OpenPage('edit') and pm.SaveProject()
drp=ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3.drp';assert pm.ExportProject(p.GetName(),str(drp),False)
(ROOT/'NATIVE_INSTALL_READBACK.json').write_text(json.dumps(dict(project=p.GetName(),timeline=t.GetName(),fps=p.GetSetting('timelineFrameRate'),width=p.GetSetting('timelineResolutionWidth'),height=p.GetSetting('timelineResolutionHeight'),timeline_start=90000,timeline_end_exclusive=117818,locked_audio_start=90000,locked_audio_end_exclusive=117368,audio_locked=True,subtitle_tracks=0,items=records,project_saved=True,checkpoint_sha256=hashlib.sha256(drp.read_bytes()).hexdigest()),indent=2),encoding='utf-8')
print('R3_INSTALLED',len(records),'FULL_NARRATION_PLUS_18_SECOND_ENDSCREEN',flush=True)
