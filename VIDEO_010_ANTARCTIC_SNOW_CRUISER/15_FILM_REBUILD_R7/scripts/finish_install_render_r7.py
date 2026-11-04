from pathlib import Path
import sys,os,json,importlib.util
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7')
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline();assert t.GetName()=='VIDEO010_R7_DIRECTORS_FINAL_REVIEW';assert not p.IsRenderingInProgress()
items=sorted(t.GetItemListInTrack('video',1),key=lambda i:i.GetStart());motions=json.loads((D/'MOTION_DESIGN_R7.json').read_text());new={q['shot_id']:q for q in json.loads((D/'NEW_ARCHIVE_SELECTS_R7.json').read_text())};done=[]
for row in motions:
 sid=row['shot_id']
 if sid in new:continue
 item=items[int(sid[1:])-1]
 if sid not in ['S044','S060','S105','S107','S154','S175']:assert item.ImportFusionComp(row['comp']),sid
 done.append(sid)
print('native scenes installed',len(done),flush=True)
spec=importlib.util.spec_from_file_location('f',r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007\CAMP_CENTURY\DEVELOPMENT\RESOLVE_R1\build_fusion.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
caps=[]
for sid,row in new.items():
 words=row['caption']
 if not words:continue
 item=items[int(sid[1:])-1];end=int(item.GetDuration())-1
 node=f.text('SourceCaption',words,.935,.033,(.98,.97,.92)).replace('Value = "Regular"','Value = "Bold"').replace('Inputs = {','Inputs = { Enabled2=Input { Value=1 },Type2=Input { Value=1 },Thickness2=Input { Value=.045 },Red2=Input { Value=.015 },Green2=Input { Value=.02 },Blue2=Input { Value=.02 },Alpha2=Input { Value=1 },GlobalOut=Input { Value=1000000 },',1)
 tools=['MediaIn1 = MediaIn { Inputs = { GlobalIn = Input { Value = 0 }, GlobalOut=Input { Value='+str(end)+' }, MediaSource=Input { Value="MediaPool" } } }',node,f.merge('CaptionMerge','MediaIn1','SourceCaption',f.ease(3,10)),'MediaOut1 = MediaOut { Inputs = { Input='+f.link('CaptionMerge')+' } }']
 dest=D/'COMPS'/f'{sid}_ARCHIVE_CAPTION.comp';f.write_comp(dest,tools,end);assert item.ImportFusionComp(str(dest)),sid;caps.append(sid)
assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R7_DIRECTORS_FINAL_REVIEW.drp'),False)
(D/'FINAL_INSTALL.json').write_text(json.dumps({'timeline':t.GetName(),'native_scenes':done,'archive_context_captions':caps,'frames':21310,'raw_voice_preserved':True,'publication':'HOLD','full_listening':'HOLD'},indent=2))
assert p.SetCurrentRenderFormatAndCodec('mp4','H264');out=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3\RENDERS');out.mkdir(exist_ok=True)
assert p.SetRenderSettings({'TargetDir':str(out),'CustomName':'VIDEO010_R7_DIRECTORS_REVIEW','SelectAllFrames':True,'ExportVideo':True,'ExportAudio':True,'FormatWidth':1920,'FormatHeight':1080});job=p.AddRenderJob();assert job;assert p.StartRendering(job);(D/'FULL_RENDER_JOB.json').write_text(json.dumps({'job':job,'output':str(out/'VIDEO010_R7_DIRECTORS_REVIEW.mp4')},indent=2));print('FULL_RENDER_STARTED',job,flush=True)
