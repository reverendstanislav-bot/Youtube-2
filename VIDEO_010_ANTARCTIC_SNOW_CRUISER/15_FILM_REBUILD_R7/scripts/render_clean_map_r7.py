import sys,os,json
from pathlib import Path
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline();assert not p.IsRenderingInProgress();items=sorted(t.GetItemListInTrack('video',1),key=lambda i:i.GetStart());it=items[170]
print(it.GetFusionCompNameList(),flush=True)
assert it.ImportFusionComp(str(D/'COMPS/S171_FINAL.comp'));assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R7_DIRECTORS_FINAL_REVIEW.drp'),False)
assert p.SetCurrentRenderFormatAndCodec('mp4','H264');assert p.SetRenderSettings({'TargetDir':str(D),'CustomName':'S171_CLEAN_FINISH','SelectAllFrames':False,'MarkIn':int(it.GetStart()),'MarkOut':int(it.GetEnd())-1,'ExportVideo':True,'ExportAudio':False,'FormatWidth':1920,'FormatHeight':1080});j=p.AddRenderJob();assert j and p.StartRendering(j);(D/'FINISH_PATCH_JOB.json').write_text(json.dumps({'job':j,'source_start_frame':int(it.GetStart())-int(t.GetStartFrame()),'frames':int(it.GetDuration())}));print('PATCH_RENDER',j)

