from pathlib import Path
import json,subprocess,sys
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');F=Path(json.loads((D/'FULL_RENDER_JOB.json').read_text())['output']);raw=F.with_name('VIDEO010_R7_RESOLVE_BEFORE_FINAL_FIXES.mp4');patches=[(json.loads((D/'FINISH_PATCH_JOB.json').read_text()),D/'S171_CLEAN_FINISH.mp4'),(json.loads((D/'CREW_PATCH_JOB.json').read_text()),D/'S021_CONTEXT_FINISH.mp4')];filters=[];last='0:v'
for k,(r,p) in enumerate(patches,1):
 start=r['source_start_frame']/24;end=(r['source_start_frame']+r['frames']-1)/24;filters.extend([f'[{k}:v]setpts=PTS-STARTPTS+{start}/TB[p{k}]',f"[{last}][p{k}]overlay=x=0:y=0:eof_action=pass:repeatlast=0:enable='between(t,{start},{end})'[v{k}]"]);last='v'+str(k)
cmd=['ffmpeg','-hide_banner','-loglevel','warning','-i',str(raw)]
for r,p in patches:cmd+=['-i',str(p)]
cmd+=['-filter_complex',';'.join(filters),'-map','['+last+']','-map','0:a:0','-c:v','h264_nvenc','-preset','p5','-tune','hq','-rc','vbr','-cq','18','-b:v','0','-pix_fmt','yuv420p','-frames:v','21310','-c:a','copy','-movflags','+faststart','-y',str(F)]
with (D/'FINAL_FINISH.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
(D/'FINISH_PASS.json').write_text(json.dumps({'raw_resolve_render_preserved':str(raw),'final':str(F),'native_resolve_patch_scenes':['S021','S171'],'source_flicker_repaired':True,'neutral_crew_caption':'EXPEDITION CREW / ARCHIVE','audio_bitstream_copied':True,'frames':21310,'source_voice_retimed':False},indent=2));print('FINAL_FINISH_COMPLETE',flush=True)
subprocess.run([sys.executable,'-X','utf8',str(D.parent/'qc_film_r7.py')],check=True)
