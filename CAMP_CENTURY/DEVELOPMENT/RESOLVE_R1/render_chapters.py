"""Native Resolve chapter exports, guarded against stalled GPU sessions.
The full original locked WAV remains on A1; exported video-only chapter parts
will be joined and paired with the same complete master for a continuous proxy.
"""
from pathlib import Path
import json,os,sys,time,subprocess
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
OUT=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R1\CHAPTERS');OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(MCP));os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect, BridgeCallError

def read_status(call):
    # Rendering can occupy the application thread. Retrying reads is safe;
    # do not retry render-start or other mutations after an ambiguous timeout.
    for attempt in range(4):
        try:return call()
        except BridgeCallError as exc:
            if 'bridge_timeout' not in str(exc) or attempt==3:raise
            print('STATUS_READ_TIMEOUT_RETRY',attempt+1,flush=True)
            time.sleep(3)

def probe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,r_frame_rate,nb_frames,width,height','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

r=connect(require_enabled=False,timeout=45)
p=r.GetProjectManager().GetCurrentProject();assert p.GetName()=='YT2 Vid7'
while read_status(p.IsRenderingInProgress):
    print('WAITING_FOR_EXISTING_NATIVE_RENDER',flush=True)
    time.sleep(8)
t=p.GetCurrentTimeline();assert t.GetName()=='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS'
assert float(p.GetSetting('timelineFrameRate'))==25
plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
beats=json.loads((ROOT/'BEATS_AUDIO_LOCKED.json').read_text(encoding='utf-8'))
for b in beats:
    t.AddMarker(round(float(b['audio_start_sec'])*25),'Blue',b['beat_id'],b['chapter_title'],1,b['beat_id'])
assert r.GetProjectManager().SaveProject()
dest=ROOT/'HIA_VIDEO007_CAMP_CENTURY_R1_NATIVE.drp'
if not dest.exists():assert r.GetProjectManager().ExportProject(p.GetName(),str(dest),False)
chapters=[]
for s in plan:
    if not chapters or chapters[-1]['chapter']!=s['chapter']:
        chapters.append(dict(chapter=s['chapter'],start=s['start_frame'],end=s['end_frame']))
    else:chapters[-1]['end']=s['end_frame']
assert len(chapters)==8
assert p.LoadRenderPreset('H.264 Master')
assert p.SetCurrentRenderFormatAndCodec('mp4','H264')
assert p.SetCurrentRenderMode(1)
log=[]
debug=Path(r'C:\Users\KK\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\logs\ResolveDebug.txt')
offset=debug.stat().st_size if debug.exists() else 0
for c in chapters:
    name=c['chapter']+'_CAMP_CENTURY_R1_720P25'
    path=OUT/(name+'.mp4');n=c['end']-c['start']
    if path.exists() and path.stat().st_size>10000:
        try:
            pr=probe(path)
            if abs(float(pr['format']['duration'])-n/25)<.045:
                log.append(dict(**c,file=str(path),frames=n,probe=pr,reused_verified=True));continue
        except Exception:pass
    settings=dict(TargetDir=str(OUT),CustomName=name,SelectAllFrames=False,MarkIn=90000+c['start'],MarkOut=90000+c['end']-1,FormatWidth=1280,FormatHeight=720,FrameRate=25,ExportVideo=True,ExportAudio=False)
    assert p.SetRenderSettings(settings),settings
    job=p.AddRenderJob();assert job
    c['job_id']=job
    assert p.StartRendering([job],False)
    print('STARTED',c['chapter'],n,'frames',flush=True)
    last=-1;last_change=time.monotonic();last_print=-10
    while read_status(p.IsRenderingInProgress):
        status=read_status(lambda:p.GetRenderJobStatus(job)) or {};percent=status.get('CompletionPercentage',0)
        if percent!=last:last=percent;last_change=time.monotonic()
        if percent>=last_print+20:
            print(c['chapter'],str(percent)+'%',flush=True);last_print=percent
        if debug.exists():
            with debug.open('rb') as f:f.seek(offset);new=f.read()
            offset=debug.stat().st_size
            if b'cudaErrorIllegalAddress' in new or b'CUDA error 700' in new:
                p.StopRendering()
                (ROOT/'CHAPTER_RENDER_ERROR.log').write_bytes(new)
                raise RuntimeError('CUDA fault recurred; stopped immediately')
        if time.monotonic()-last_change>120:
            p.StopRendering();raise RuntimeError('Render made no progress for 120 seconds')
        time.sleep(2)
    status=read_status(lambda:p.GetRenderJobStatus(job)) or {}
    assert status.get('CompletionPercentage',0)==100,(c,status)
    pr=probe(path)
    assert abs(float(pr['format']['duration'])-n/25)<.045,(c,pr)
    assert pr['streams'][0]['r_frame_rate']=='25/1'
    log.append(dict(**c,file=str(path),frames=n,probe=pr,status=status))
    (ROOT/'CHAPTER_RENDER_RESULTS.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
    print('COMPLETE',c['chapter'],path.stat().st_size,flush=True)
(ROOT/'CHAPTER_RENDER_RESULTS.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
assert sum(x['frames'] for x in log)==27368
print('ALL_8_NATIVE_CHAPTERS_COMPLETE',flush=True)
