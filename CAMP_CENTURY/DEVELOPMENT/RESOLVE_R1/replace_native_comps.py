"""Replace owned draft comps from corrected native Fusion files after checkpoint.
Uses the installed, authenticated bridge client and the public Resolve API.
"""
from pathlib import Path
import json,os,sys
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=15)
p=r.GetProjectManager().GetCurrentProject()
assert p.GetName()=='YT2 Vid7'
assert not p.IsRenderingInProgress()
assert (ROOT/'HIA_VIDEO007_NATIVE_R1_CHECKPOINT.drp').stat().st_size>1000
jobs=json.loads((ROOT/'FUSION_IMPORT_MANIFEST.json').read_text(encoding='utf-8'))
log=[]
for j in jobs:
    p=r.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline()
    assert t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS'
    item=t.GetItemListInTrack('video',1)[j['item_index']]
    old_names=list(item.GetFusionCompNameList() or [])
    comp=item.ImportFusionComp(j['comp'])
    assert comp,j['shot_id']
    new_names=[n for n in (item.GetFusionCompNameList() or []) if n not in old_names]
    if len(new_names)==1:
        item.LoadFusionCompByName(new_names[0])
        for name in old_names:
            assert item.DeleteFusionCompByName(name),(j['shot_id'],name)
    else:
        assert item.GetFusionCompCount()==1,(j['shot_id'],new_names)
    assert item.GetFusionCompCount()==1,j['shot_id']
    gpu_values=[]
    for node in (comp.GetToolList(False) or {}).values():
        value=node.GetInput('UseGPU')
        if value is not None:
            if value!=0:node.SetInput('UseGPU',0)
            actual=node.GetInput('UseGPU')
            assert actual==0,(j['shot_id'],'UseGPU',actual)
            gpu_values.append(actual)
    log.append(dict(shot_id=j['shot_id'],comp=j['comp'],native_comp_count=1,use_gpu_values=gpu_values))
    if len(log)%10==0:print('REPLACED',len(log),'/',len(jobs),flush=True)
(ROOT/'NATIVE_COMP_REPLACEMENT_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
assert r.GetProjectManager().SaveProject()
p=r.GetProjectManager().GetCurrentProject()
dest=ROOT/'HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_CPU_FIXED.drp'
assert r.GetProjectManager().ExportProject(p.GetName(),str(dest),False)
print(json.dumps(dict(native_comps=len(log),saved=True,exported=str(dest))))
