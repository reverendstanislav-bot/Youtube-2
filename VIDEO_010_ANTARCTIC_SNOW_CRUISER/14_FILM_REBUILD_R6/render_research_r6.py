from pathlib import Path
import sys,os,json,time,subprocess,hashlib,shutil
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');L=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');name='VIDEO010_R6_RESEARCH_RIGHTS_HOLD';state=D/'RENDER_R6_STATE.json'
def save(stage,**kwargs):state.write_text(json.dumps({'stage':stage,'updated':time.strftime('%Y-%m-%dT%H:%M:%S'),**kwargs},indent=2));print(stage,kwargs,flush=True)
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();assert p.GetName()=='Yt2 Vid 10';t=p.GetCurrentTimeline();assert t.GetName()=='VIDEO010_R6_1_FULL_RESEARCH_RIGHTS_HOLD';assert not p.IsRenderingInProgress();assert int(t.GetEndFrame())-int(t.GetStartFrame())==21310;assert r.GetProjectManager().SaveProject();assert p.SetCurrentRenderFormatAndCodec('mp4','H264');assert p.SetRenderSettings({'TargetDir':str(W/'RENDERS'),'CustomName':name,'SelectAllFrames':True,'ExportVideo':True,'ExportAudio':True,'FormatWidth':1920,'FormatHeight':1080});job=p.AddRenderJob();assert job;assert p.StartRendering(job);save('RENDERING_RESEARCH_REVIEW',job=job)
last=-1
while True:
 try:
  status=p.GetRenderJobStatus(job);active=p.IsRenderingInProgress()
 except Exception:
  p=r.GetProjectManager().GetCurrentProject();status=p.GetRenderJobStatus(job);active=p.IsRenderingInProgress()
 percent=int(status.get('CompletionPercentage',0))
 if percent!=last:save('RENDERING_RESEARCH_REVIEW',job=job,percent=percent);last=percent
 if not active:break
 time.sleep(10)
assert int(status.get('CompletionPercentage',0))==100,status
f=W/'RENDERS'/(name+'.mp4');assert f.stat().st_size>1000000
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');assert v['width']==1920 and v['height']==1080 and v['r_frame_rate']=='24/1';assert abs(float(probe['format']['duration'])-21310/24)<.2;assert a['sample_rate']=='48000'
save('FULL_DECODE_CHECK',job=job)
res=subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],capture_output=True,text=True);assert res.returncode==0,res.stderr[-1500:]
# This is a research review package, never a publishable master.
report={'status':'RESEARCH_REVIEW_TECHNICAL_PASS_RIGHTS_LISTENING_OWNER_HOLD','timeline':t.GetName(),'duration_seconds':float(probe['format']['duration']),'resolution':[1920,1080],'fps':24,'audio_tracks_in_project':4,'music_cues':14,'designed_ambience_cues':17,'new_images_generated':0,'voice_retimed_or_regenerated':False,'script_changed':False,'source_rights':'HOLD_PRIVATE_ARCHIVAL_COMPONENTS_NOT_CLEARED','publication':'BLOCKED','full_real_time_av_review':'HOLD','human_listening':'HOLD','owner_acceptance':'HOLD','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'technical_decode':'PASS'}
(D/'QC_R6.json').write_text(json.dumps(report,indent=2));delivery=L/'DELIVERY/RESEARCH_R6_RIGHTS_HOLD';delivery.mkdir(parents=True,exist_ok=True)
for src in [f,D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.drp',D/'QC_R6.json',D/'R6_INSTALL_RECEIPT.json',D/'RESEARCH_USED_SELECTS_R6.json']:shutil.copy2(src,delivery/src.name)
(delivery/'README_RU.txt').write_text('ИССЛЕДОВАТЕЛЬСКАЯ ВЕРСИЯ. НЕ ДЛЯ ПУБЛИКАЦИИ.\nХроника Snow Cruiser включена для проверки монтажа; права на частные компоненты остаются HOLD. Музыка и новые звуки Freesound CC0. Озвучка R5.1 сохранена. Требуется непрерывная A/V-проверка, прослушивание и решение по архивным правам.\n',encoding='utf-8')
old=L/'DELIVERY/FULL_FILM_R4_REVIEW/QC_STATUS.json'
if old.exists():
 x=json.loads(old.read_text());x.update(status='OWNER_REJECTED_SLIDESHOW_NO_ARCHIVE_NO_MUSIC',replaced_by_review=str(delivery/f.name),publication='BLOCKED');old.write_text(json.dumps(x,indent=2))
report['output']=str(delivery/f.name);save('RESEARCH_REVIEW_RENDER_READY_NOT_PUBLICATION_READY',**report);(W/'FULL_FILM_STATE.json').write_text(json.dumps(report,indent=2))
