from pathlib import Path
import json,subprocess,hashlib,sys,os
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');m=json.loads((D/'FILM_MANIFEST_R7.json').read_text());row=next(r for r in m['shots'] if r['shot_id']=='S021');old=Path(row['path']);fixed=old.with_name('S021_ARCHIVE_R7_DEFLICKER.mp4');a,b=2121-row['s'],2153-row['s'];expr=f'not(between(n,{a},{a+2})+between(n,{b},{b+3}))'
subprocess.run(['ffmpeg','-v','error','-i',str(old),'-vf',"select='"+expr+"',fps=24",'-frames:v',str(row['e']-row['s']),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-y',str(fixed)],check=True)
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json';from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();assert not p.IsRenderingInProgress();t=p.GetCurrentTimeline();items=sorted(t.GetItemListInTrack('video',1),key=lambda i:i.GetStart());assert items[20].GetMediaPoolItem().ReplaceClip(str(fixed));assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R7_DIRECTORS_FINAL_REVIEW.drp'),False)
row['path']=str(fixed);row['source_flicker_repair']='7 source black frames replaced by adjacent exposure; duration and narration unchanged';(D/'FILM_MANIFEST_R7.json').write_text(json.dumps(m,indent=2))
patch=json.loads((D/'FINISH_PATCH_JOB.json').read_text());F=Path(json.loads((D/'FULL_RENDER_JOB.json').read_text())['output']);raw=F.with_name('VIDEO010_R7_RESOLVE_BEFORE_FINAL_FIXES.mp4')
if not raw.exists():F.rename(raw)
start=patch['source_start_frame']/24;end=(patch['source_start_frame']+patch['frames']-1)/24
fc=f"[1:v]setpts=PTS-STARTPTS+{start}/TB[patch];[0:v][patch]overlay=x=0:y=0:eof_action=pass:repeatlast=0:enable='between(t,{start},{end})'[base];[base]select='not(between(n,2121,2123)+between(n,2153,2156))',fps=24[v]"
cmd=['ffmpeg','-hide_banner','-loglevel','warning','-i',str(raw),'-i',str(D/'S171_CLEAN_FINISH.mp4'),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','18','-b:v','0','-pix_fmt','yuv420p','-frames:v','21310','-c:a','copy','-movflags','+faststart','-y',str(F)]
with (D/'FINISH_PASS.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
(D/'FINISH_PASS.json').write_text(json.dumps({'full_resolve_render_preserved':str(raw),'final':str(F),'map_patch_frames':patch,'source_flicker_global_frames':[[2121,2123],[2153,2156]],'audio_bitstream_copied':True,'fps_duration_preserved':True},indent=2));print('FINISH_PASS_COMPLETE',flush=True)
subprocess.run([sys.executable,'-X','utf8',str(D.parent/'qc_film_r7.py')],check=True)
