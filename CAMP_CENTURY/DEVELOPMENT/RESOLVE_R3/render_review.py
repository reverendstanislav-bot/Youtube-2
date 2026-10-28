from pathlib import Path
import sys,os,json,time,subprocess
ROOT=Path(__file__).resolve().parent;MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);p=r.GetProjectManager().GetCurrentProject();t=p.GetCurrentTimeline()
assert p.GetName()=='YT2 Vid7' and t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS' and not p.IsRenderingInProgress()
out=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R3\PROOFS');out.mkdir(parents=True,exist_ok=True)
assert p.LoadRenderPreset('H.264 Master') and p.SetCurrentRenderFormatAndCodec('mp4','H264') and p.SetCurrentRenderMode(1)
proofs=[('R3_REBUILT_OPENING_60S',0,1500),('R3_RESTORED_AIRCRAFT_8S',25178,200),('R3_PREVIOUS_VIDEO_ENDSCREEN',27368,100)]
if '--end-only' in sys.argv:proofs=[proofs[-1]]
records=[]
for name,start,n in proofs:
    assert p.SetRenderSettings(dict(TargetDir=str(out),CustomName=name,SelectAllFrames=False,MarkIn=90000+start,MarkOut=90000+start+n-1,FormatWidth=1920,FormatHeight=1080,FrameRate=25,ExportVideo=True,ExportAudio=True))
    job=p.AddRenderJob();assert job and p.StartRendering([job],False)
    print('RENDERING',name,flush=True);deadline=time.monotonic()+480
    while p.IsRenderingInProgress():
        if time.monotonic()>deadline:p.StopRendering();raise TimeoutError(name)
        time.sleep(3)
    status=p.GetRenderJobStatus(job);assert status['CompletionPercentage']==100,status
    file=out/(name+'.mp4');subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(file),'-f','null','-'],check=True)
    times=[.16,2,4,6.8] if 'AIRCRAFT' in name else ([1,5,10.8,17.5,24.8,28.5,38.1,44.1,52,59.5] if start==0 else [.2,2,3.8])
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(1600,246*((len(times)+3)//4)),'#eeefed');draw=ImageDraw.Draw(sheet)
    for j,at in enumerate(times):
        dst=ROOT/'QC'/f'{name}_{j}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(file),'-frames:v','1','-vf','scale=400:225',str(dst)],check=True)
        x=j%4*400;y=j//4*246;draw.text((x+3,y+2),name+' '+str(at),fill='#14232a');sheet.paste(Image.open(dst),(x,y+20))
    sheetpath=ROOT/'QC'/f'{name}_RENDERED_SEQUENCE.jpg';sheet.save(sheetpath,quality=95)
    records.append(dict(file=str(file),timeline_start_frame=start,frames=n,native_render_status=status,full_decode='PASS',sample_times=times,contact=str(sheetpath)))
    print('RENDERED_AND_DECODED',name,flush=True)
dest=ROOT/'REPRESENTATIVE_RENDER_PROOFS.json'
if '--end-only' in sys.argv and dest.exists():records=[x for x in json.loads(dest.read_text()) if 'ENDSCREEN' not in x['file']]+records
dest.write_text(json.dumps(records,indent=2),encoding='utf-8')
