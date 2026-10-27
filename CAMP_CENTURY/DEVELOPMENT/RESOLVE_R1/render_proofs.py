from pathlib import Path
import os,sys,time,json,subprocess
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
OUT=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R1\PROOFS');OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=15);p=r.GetProjectManager().GetCurrentProject()
assert p.GetName()=='YT2 Vid7' and not p.IsRenderingInProgress()
assert p.LoadRenderPreset('H.264 Master')
assert p.SetCurrentRenderFormatAndCodec('mp4','H264')
assert p.SetCurrentRenderMode(1)
tests=[('DOC_MASK_CPU',53),('CHART_MASK_CPU',91.6),('AIRCRAFT_CPU',1015),('REMOVAL_CPU',870)]
rows=[]
for name,sec in tests:
    settings=dict(TargetDir=str(OUT),CustomName=name,SelectAllFrames=False,MarkIn=90000+round(sec*25),MarkOut=90000+round(sec*25)+49,FormatWidth=1280,FormatHeight=720,FrameRate=25,ExportVideo=True,ExportAudio=False)
    assert p.SetRenderSettings(settings)
    j=p.AddRenderJob();assert j and p.StartRendering([j],False)
    start=time.monotonic()
    while p.IsRenderingInProgress():
        assert time.monotonic()-start<90,'Proof render stalled'
        time.sleep(1)
    status=p.GetRenderJobStatus(j) or {};assert status.get('CompletionPercentage')==100,status
    file=OUT/(name+'.mp4');frame=OUT/(name+'.png')
    subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-ss','1','-i',str(file),'-frames:v','1',str(frame)],check=True)
    rows.append(dict(name=name,job=j,file=str(file),frame=str(frame),timeline_seconds=sec))
    print('PROOF_COMPLETE',name,flush=True)
(ROOT/'NATIVE_CPU_MASK_PROOFS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
