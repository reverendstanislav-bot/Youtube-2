from pathlib import Path
import sys,os,json,time,subprocess,hashlib,shutil,traceback
W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');ROOT=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10')
def state(stage,**kw):
 x={'stage':stage,'updated':time.strftime('%Y-%m-%dT%H:%M:%S'),**kw};(W/'FULL_FILM_STATE.json').write_text(json.dumps(x,indent=2));print(json.dumps(x),flush=True)
try:
 sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
 from src.utils.resolve_bridge_client import connect
 r=connect(require_enabled=False,timeout=20);pm=r.GetProjectManager();p=pm.GetCurrentProject();assert p.GetName()=='Yt2 Vid 10';assert not p.IsRenderingInProgress();tl=p.GetCurrentTimeline();assert tl.GetName()=='VIDEO010_R5_1_FULL_R4_HD_REVIEW';assert int(tl.GetEndFrame())-int(tl.GetStartFrame())==21310
 item=tl.GetItemListInTrack('video',1)[164];c=item.GetFusionCompByIndex(1)
 for t in c.GetToolList(False).values():
  if t.GetAttrs().get('TOOLS_RegID')=='TextPlus':t.SetInput('Center',[.65,.90])
 rec=json.loads((W/'NATIVE_LAYER_RECEIPTS.json').read_text())
 for x in rec:
  if x['shot_id']=='S165':x['labels']=[['1956 MAP / REGIONAL CONTEXT',.65,.90,.027,0]]
 (W/'NATIVE_LAYER_RECEIPTS_R4.json').write_text(json.dumps(rec,indent=2));assert pm.SaveProject();drp=W/'VIDEO010_FULL_R4_HD_REVIEW.drp';assert pm.ExportProject(p.GetName(),str(drp))
 assert p.SetCurrentRenderFormatAndCodec('mp4','H264');assert p.SetRenderSettings({'TargetDir':str(W/'RENDERS'),'CustomName':'VIDEO010_FULL_R4_HD_REVIEW','SelectAllFrames':True,'ExportVideo':True,'ExportAudio':True,'FormatWidth':1920,'FormatHeight':1080});j=p.AddRenderJob();assert j;assert p.StartRendering(j);(W/'FULL_RENDER_JOB_R4.json').write_text(json.dumps({'job':j,'timeline':tl.GetName()}));state('RENDERING_FULL_R4',job=j,seconds=21310/24)
 failures=0
 while True:
  try:
   active=p.IsRenderingInProgress();failures=0
   if not active:break
  except Exception:
   failures+=1
   if failures>=3:raise
  time.sleep(10)
 status=p.GetRenderJobStatus(j);assert int(status.get('CompletionPercentage',0))==100,status
 film=W/'RENDERS/VIDEO010_FULL_R4_HD_REVIEW.mp4';assert film.is_file() and film.stat().st_size>1000000
 state('TECHNICAL_QC_FULL_R4',path=str(film))
 def run(args):
  x=subprocess.run(args,capture_output=True,text=True);assert x.returncode==0,x.stderr[-2500:];return x.stdout
 probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(film)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');assert v['codec_name']=='h264' and (v['width'],v['height'])==(1920,1080) and v['r_frame_rate']=='24/1';assert abs(float(probe['format']['duration'])-21310/24)<.2;assert a['sample_rate']=='48000'
 run(['ffmpeg','-v','error','-i',str(film),'-f','null','-'])
 delivery=ROOT/'DELIVERY/FULL_FILM_R4_REVIEW';delivery.mkdir(parents=True,exist_ok=True)
 for src in [film,drp,W/'VIDEO010_FULL_R4_MANIFEST.json',W/'NATIVE_LAYER_RECEIPTS_R4.json',W/'NATIVE_CLOCK_FIX_R4.json',W/'HD_MAP_PROXY_R4.json',W/'REFRAME_RECEIPTS.json']:shutil.copy2(src,delivery/src.name)
 report={'status':'FULL_REVIEW_RENDER_TECHNICAL_PASS_VISUAL_LISTENING_OWNER_HOLD','output':str(delivery/film.name),'duration_seconds':float(probe['format']['duration']),'fps':'24/1','resolution':[1920,1080],'audio_sample_rate':a['sample_rate'],'sha256':hashlib.sha256(film.read_bytes()).hexdigest(),'narrative_shots':193,'endscreen_seconds':20,'native_comps':22,'new_images_saved':147,'additional_generation_stopped_by_owner':True,'not_verified':['Full real-time audiovisual review','Human listening and ASR prefix flags','Owner acceptance'],'source_script':'R5.1 unchanged','publication':False}
 (delivery/'QC_STATUS.json').write_text(json.dumps(report,indent=2));(W/'QC_STATUS_R4.json').write_text(json.dumps(report,indent=2));state('FULL_REVIEW_RENDER_READY',**report)
except Exception:
 state('ERROR_REQUIRES_REPAIR',error=traceback.format_exc());raise
