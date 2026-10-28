from pathlib import Path
import json,os,sys
ROOT=Path(__file__).resolve().parent;MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline()
assert p.GetName()=='YT2 Vid7' and t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS' and not p.IsRenderingInProgress()
assert t.GetIsTrackLocked('audio',1) and t.GetEndFrame()==117368
rows=json.loads((ROOT/'ADDITIONAL_ARCHIVE_PLACEMENTS.json').read_text(encoding='utf-8'))
plan={s['shot_id']:s for s in json.loads((ROOT.parent/'RESOLVE_R1/SHOT_PLAN_R1.json').read_text(encoding='utf-8'))}
assert pm.SaveProject()
names=[p.GetTimelineByIndex(i).GetName() for i in range(1,p.GetTimelineCount()+1)]
if 'R2_BEFORE_ADDITIONAL_ARCHIVE' not in names:
    backup=t.DuplicateTimeline('R2_BEFORE_ADDITIONAL_ARCHIVE');assert backup and p.SetCurrentTimeline(t)
assert p.GetCurrentTimeline().GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS'
mp=p.GetMediaPool();logs=[]
for row in rows:
    s=plan[row['shot_id']];start=90000+s['start_frame'];n=s['duration_frames']
    items={int(i.GetStart()):i for i in t.GetItemListInTrack('video',1)};old=items[start]
    existing=old.GetMediaPoolItem().GetClipProperty('File Path')
    if existing==row['path'] and old.GetDuration()==n:logs.append(dict(shot=row['shot_id'],already_installed=True));continue
    assert 'FUSION_CARRIER' in str(existing).upper() or existing==row['path'],existing
    clips=mp.ImportMedia([row['path']]);assert clips and len(clips)==1
    assert t.DeleteClips([old],False)
    added=mp.AppendToTimeline([dict(mediaPoolItem=clips[0],startFrame=0,endFrame=n,recordFrame=start,trackIndex=1,mediaType=1)])
    assert added and len(added)==1
    item=added[0];assert item.GetStart()==start and item.GetDuration()==n and item.GetEnd()==start+n
    assert item.GetFusionCompCount()==0
    assert len(t.GetItemListInTrack('video',1))==132 and t.GetEndFrame()==117368 and t.GetIsTrackLocked('audio',1)
    logs.append(dict(shot=row['shot_id'],clip=row['asset_id'],start_frame=start,end_frame_exclusive=start+n,frames=n,source_file=item.GetMediaPoolItem().GetClipProperty('File Path'),source_in_frame=row['source_in_frame'],source_out_frame_exclusive=row['source_out_frame_exclusive'],source_fps=row['source_fps']))
    print('INSTALLED_REAL_ARCHIVE',row['shot_id'],row['asset_id'],flush=True)
assert pm.SaveProject()
(ROOT/'ADDITIONAL_ARCHIVE_NATIVE_READBACK.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
