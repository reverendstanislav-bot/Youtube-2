"""Render only a separate 16s practice timeline; restore the production timeline."""
from pathlib import Path
import os,sys,json,time,subprocess,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45);pm=r.GetProjectManager();p=pm.GetCurrentProject();original=p.GetCurrentTimeline();page=r.GetCurrentPage()
assert p.GetName()=='YT2 Vid7' and not p.IsRenderingInProgress() and float(p.GetSetting('timelineFrameRate'))==25
def signature(t):
    return [(kind,track,int(x.GetStart()),int(x.GetEnd()),x.GetName()) for kind in ['video','audio'] for track in range(1,t.GetTrackCount(kind)+1) for x in (t.GetItemListInTrack(kind,track) or [])]
before=signature(original);name='HIA_NATIVE_MOTION_LIBRARY_TEST_V1'
assert name not in [p.GetTimelineByIndex(i).GetName() for i in range(1,p.GetTimelineCount()+1)],'Proof exists: review it instead of duplicating work'
out=Path(r'C:\Users\KK\Movies\HIA_MOTION_LIBRARY_V1');out.mkdir(exist_ok=True)
rows=json.loads((ROOT/'BUILD_MANIFEST.json').read_text());records=[]
try:
    mp=p.GetMediaPool();test=mp.CreateEmptyTimeline(name);assert test and p.SetCurrentTimeline(test)
    carrier=ROOT.parents[1]/'DEVELOPMENT/RESOLVE_R1/FUSION_CARRIER_60S_25FPS.mp4';clip=mp.ImportMedia([str(carrier)])[0]
    start=test.GetStartFrame();cursor=start
    for row in rows:
        added=mp.AppendToTimeline([dict(mediaPoolItem=clip,startFrame=0,endFrame=row['frames'],recordFrame=cursor,trackIndex=1,mediaType=1)]);assert len(added)==1
        item=added[0];assert item.GetDuration()==row['frames'];comp=item.ImportFusionComp(row['comp']);assert comp
        control=comp.FindTool('MotionControls');assert control
        actual=[control.GetInput('NumberIn'+str(i)) for i in range(1,9)];assert all(abs(float(a)-float(b))<.001 for a,b in zip(actual,row['native_controls']))
        gpu=[]
        for node in (comp.GetToolList(False) or {}).values():
            v=node.GetInput('UseGPU')
            if v is not None:assert v==0;gpu.append(v)
        records.append(dict(id=row['id'],frames=row['frames'],controls_native_readback=actual,use_gpu=gpu,timeline_start_frame=cursor))
        cursor+=row['frames']
    assert p.LoadRenderPreset('H.264 Master') and p.SetCurrentRenderFormatAndCodec('mp4','H264') and p.SetCurrentRenderMode(1)
    assert p.SetRenderSettings(dict(TargetDir=str(out),CustomName='HIA_NATIVE_AIRCRAFT_AND_HOIST_V1_16S',SelectAllFrames=False,MarkIn=start,MarkOut=cursor-1,FormatWidth=1920,FormatHeight=1080,FrameRate=25,ExportVideo=True,ExportAudio=False))
    job=p.AddRenderJob();assert job and p.StartRendering([job],False);print('RENDERING_SEPARATE_NATIVE_RIG_TEST_16S',flush=True)
    deadline=time.monotonic()+180
    while p.IsRenderingInProgress():
        if time.monotonic()>deadline:p.StopRendering();raise TimeoutError('Practice render stopped; production timeline will be restored')
        time.sleep(2)
    status=p.GetRenderJobStatus(job);assert status['CompletionPercentage']==100,status
    movie=out/'HIA_NATIVE_AIRCRAFT_AND_HOIST_V1_16S.mp4'
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
    sheet=Image.new('RGB',(1600,492),'#eef0ee');draw=ImageDraw.Draw(sheet)
    for j,at in enumerate([.2,2,4,6.8,8.2,10,12,14.8]):
        dst=out/f'SAMPLE_{j}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(movie),'-frames:v','1','-vf','scale=400:225',str(dst)],check=True)
        x=j%4*400;y=j//4*246;draw.text((x+4,y+2),('AIRCRAFT' if j<4 else 'HOIST')+' '+str(at)+'s',fill='#14242c');sheet.paste(Image.open(dst),(x,y+20))
    sheet.save(ROOT/'NATIVE_PROOF_SEQUENCE.jpg',quality=95)
    report=dict(native_render_complete=True,full_decode='PASS',frames=400,fps=25,seconds=16,movie=str(movie),movie_sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),rigs=records,visual_sample_review='PENDING',full_continuous_playback_review='NOT_COMPLETED')
finally:
    assert p.SetCurrentTimeline(original);assert signature(original)==before
    r.OpenPage(page or 'edit');pm.SaveProject()
    print('PRODUCTION_TIMELINE_RESTORED_UNCHANGED',original.GetName(),flush=True)
if 'report' in globals():
    report['production_timeline_restored_unchanged']=True
    (ROOT/'NATIVE_PROOF.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('TWO_NATIVE_RIGS_RENDERED_AND_DECODED',flush=True)
