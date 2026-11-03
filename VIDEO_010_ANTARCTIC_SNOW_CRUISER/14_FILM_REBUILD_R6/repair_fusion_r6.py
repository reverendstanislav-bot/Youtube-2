from pathlib import Path
import json,sys,os,re
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');m=json.loads((D/'R6_MANIFEST.json').read_text());rows={x['shot_id']:x for x in m['shots']};sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline();assert t.GetName()=='VIDEO010_R6_FULL_RESEARCH_RIGHTS_HOLD' and not p.IsRenderingInProgress();items=sorted(t.GetItemListInTrack('video',1),key=lambda x:x.GetStart());rec=[]
for sid in ['S044','S045','S118','S120','S133']:
 i=items[int(sid[1:])-1];c=i.GetFusionCompByIndex(1);tools=list(c.GetToolList(False).values());merges=[x for x in tools if x.GetAttrs().get('TOOLS_RegID')=='Merge'];old=[x for x in merges if x.GetAttrs().get('TOOLS_Name','').startswith('HIA_'+sid+'_REVEAL_')];new=[x for x in merges if x.GetAttrs().get('TOOLS_Name','').startswith('Merge')];assert old and new,sid;base=max(old,key=lambda x:int(re.search(r'_REVEAL_(\d+)',x.GetAttrs()['TOOLS_Name']).group(1)));first=min(new,key=lambda x:int(re.search(r'Merge(\d+)',x.GetAttrs()['TOOLS_Name']).group(1)));assert first.ConnectInput('Background',base);rec.append({'shot':sid,'connected':first.GetAttrs()['TOOLS_Name'],'background':base.GetAttrs()['TOOLS_Name']});print(rec[-1],flush=True)
assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.drp'));(D/'FUSION_CONNECTION_REPAIR_R6.json').write_text(json.dumps(rec,indent=2));assert p.SetCurrentRenderFormatAndCodec('mp4','H264');jobs=[]
for sid in ['S044','S045','S118','S120','S133']:
 f=int(t.GetStartFrame())+rows[sid]['s']+48;assert p.SetRenderSettings({'TargetDir':str(D),'CustomName':'QC_REPAIRED_R6_'+sid,'SelectAllFrames':False,'MarkIn':f,'MarkOut':f,'ExportVideo':True,'ExportAudio':False});j=p.AddRenderJob();assert j;jobs.append(j)
assert p.StartRendering(jobs);(D/'REPAIRED_QC_JOBS.json').write_text(json.dumps(jobs));print('QC jobs started',flush=True)
