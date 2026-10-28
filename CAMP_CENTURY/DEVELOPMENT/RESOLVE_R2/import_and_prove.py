from pathlib import Path
import json,os,sys,time,uuid,subprocess
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect,BridgeCallError
def read(call):
    for attempt in range(4):
        try:return call()
        except BridgeCallError as ex:
            if 'timeout' not in str(ex) or attempt==3:raise
            time.sleep(2)
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();t=p.GetCurrentTimeline()
assert p.GetName()=='YT2 Vid7' and t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS'
assert not read(p.IsRenderingInProgress)
proofs='--all' not in sys.argv;render_only='--render-only' in sys.argv
jobs=json.loads((ROOT/('FUSION_IMPORT_MANIFEST_PROOFS.json' if proofs and not render_only else 'FUSION_IMPORT_MANIFEST.json')).read_text(encoding='utf-8'))
if render_only:jobs=[j for j in jobs if j['shot_id'] in ['S083','S084']]
items=t.GetItemListInTrack('video',1);assert len(items)==132
plan_by_id={s['shot_id']:s for s in json.loads((ROOT/'SHOT_PLAN_R2.json').read_text(encoding='utf-8'))}
by_start={int(i.GetStart()):i for i in items}
records=[]
for j in jobs:
    if render_only:continue
    s=plan_by_id[j['shot_id']];item=by_start[90000+s['start_frame']]
    assert item.GetDuration()==s['duration_frames']
    comp=item.ImportFusionComp(j['comp']);assert comp and item.GetFusionCompCount()==1
    gpu=[]
    for node in (comp.GetToolList(False) or {}).values():
        v=node.GetInput('UseGPU')
        if v is not None:
            if v!=0:node.SetInput('UseGPU',0)
            actual=node.GetInput('UseGPU');assert actual==0;gpu.append(actual)
    records.append(dict(**j,native_comp_count=1,use_gpu=gpu))
    if len(records)%20==0:print('NATIVE_R2_IMPORTED',len(records),flush=True)
assert pm.SaveProject()
dest=ROOT/('HIA_VIDEO007_R2_PROOFS_'+uuid.uuid4().hex[:6]+'.drp' if proofs else 'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp')
if dest.exists():dest=ROOT/('HIA_VIDEO007_R2_CHECKPOINT_'+uuid.uuid4().hex[:6]+'.drp')
assert pm.ExportProject(p.GetName(),str(dest),False)
if not proofs:
    import shutil
    canonical=ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp'
    if dest!=canonical:shutil.copy2(dest,canonical)
(ROOT/('NATIVE_PROOF_IMPORT.json' if proofs else 'NATIVE_IMPORT_READBACK.json')).write_text(json.dumps(records,indent=2),encoding='utf-8')
print('R2_NATIVE_SAVED',len(records),flush=True)
if not proofs:sys.exit(0)
out=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R2\PROOFS');out.mkdir(parents=True,exist_ok=True)
assert p.LoadRenderPreset('H.264 Master') and p.SetCurrentRenderFormatAndCodec('mp4','H264') and p.SetCurrentRenderMode(1)
plan={s['shot_id']:s for s in json.loads((ROOT/'SHOT_PLAN_R2.json').read_text(encoding='utf-8'))};rendered=[]
for j in jobs:
    s=plan[j['shot_id']];length=min(s['duration_frames'],300 if s['asset_id'] in ['Q01','Q07','M03'] else 125);name=s['shot_id']+'_'+s['asset_id']+'_R2_CIRCULAR_HD_PROOF'
    settings=dict(TargetDir=str(out),CustomName=name,SelectAllFrames=False,MarkIn=90000+s['start_frame'],MarkOut=90000+s['start_frame']+length-1,FormatWidth=1920,FormatHeight=1080,FrameRate=25,ExportVideo=True,ExportAudio=True)
    assert p.SetRenderSettings(settings);job=p.AddRenderJob();assert job and p.StartRendering([job],False)
    start=time.monotonic()
    while read(p.IsRenderingInProgress):
        if time.monotonic()-start>150:p.StopRendering();raise RuntimeError('Representative render stalled')
        time.sleep(2)
    status=read(lambda:p.GetRenderJobStatus(job));assert status.get('CompletionPercentage')==100,status
    file=out/(name+'.mp4');png=out/(name+'.png')
    subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-ss',str(min(10.5 if s['asset_id'] in ['Q01','Q07'] else 3,length/25-.1)),'-i',str(file),'-frames:v','1',str(png)],check=True)
    rendered.append(dict(shot=s['shot_id'],asset=s['asset_id'],file=str(file),png=str(png),job=job,frames=length))
    print('R2_PROOF_RENDERED',s['shot_id'],flush=True)
(ROOT/'REPRESENTATIVE_RENDER_PROOFS.json').write_text(json.dumps(rendered,indent=2),encoding='utf-8')
