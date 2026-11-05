from pathlib import Path
import json,wave,hashlib,subprocess,csv,datetime,re
import numpy as np
SRC=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_VOICEBOX_QUEUE');OUT=SRC.parent/'R1_2_MASTER_ASR';OUT.mkdir(exist_ok=True)
q=json.loads((SRC/'QUEUE.json').read_text(encoding='utf-8'));assert len(q['jobs'])==50 and all(j['status']=='COMPLETED' for j in q['jobs'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC/'05_SCRIPT_R1_2_EN.md')==q['source_sha256']
rows=[];pcm=[];params=None;cursor=0;peak=0
for j in q['jobs']:
 p=SRC/j['output_file'];assert sha(p)==j['audio_sha256'],j['id']
 assert (SRC/(j['id']+'.txt')).read_text(encoding='utf-8')==j['payload']['text']
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,capture_output=True)
 with wave.open(str(p),'rb') as w:
  fmt=(w.getnchannels(),w.getsampwidth(),w.getframerate());frames=w.getnframes();data=w.readframes(frames)
 if params is None:params=fmt
 assert fmt==params and fmt[1]==2,fmt
 pcm.append(data);samples=np.frombuffer(data,dtype='<i2');pk=int(np.abs(samples.astype(np.int32)).max());peak=max(peak,pk)
 rows.append({'index':j['index'],'paragraph_id':j['id'],'file':p.name,'start_sample':cursor,'sample_count':frames,'start_seconds':cursor/fmt[2],'duration_seconds':frames/fmt[2],'end_seconds':(cursor+frames)/fmt[2],'peak_dbfs':round(20*np.log10(max(pk,1)/32768),3),'sha256':sha(p),'generation_id':j['generation_id']});cursor+=frames
master=OUT/'GLOMAR_R1_2_ARTHUR_MASTER_NATIVE_24K_PCM16.wav'
with wave.open(str(master),'wb') as w:w.setnchannels(params[0]);w.setsampwidth(params[1]);w.setframerate(params[2]);w.writeframes(b''.join(pcm))
with wave.open(str(master),'rb') as w:assert w.readframes(w.getnframes())==b''.join(pcm)
delivery=OUT/'GLOMAR_R1_2_ARTHUR_MASTER_48K_PCM24.wav'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(master),'-ar','48000','-c:a','pcm_s24le',str(delivery)],check=True)
for p in [master,delivery]:subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,capture_output=True)
with(OUT/'PARAGRAPH_TIMING.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Boundary measurements are diagnostic only; no silence, trimming, fades or gain changes applied.
boundaries=[]
for i in range(len(pcm)-1):
 a=np.frombuffer(pcm[i],dtype='<i2');b=np.frombuffer(pcm[i+1],dtype='<i2');jump=abs(int(a[-1])-int(b[0]))/32768
 boundaries.append({'from':rows[i]['paragraph_id'],'to':rows[i+1]['paragraph_id'],'time_seconds':rows[i]['end_seconds'],'sample_jump_fraction':jump,'listening_status':'NOT_LISTENED','action':'Diagnostic only; original joins preserved'})
with(OUT/'JOIN_DIAGNOSTICS.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(boundaries[0]));w.writeheader();w.writerows(boundaries)
metrics=subprocess.run(['ffmpeg','-hide_banner','-i',str(delivery),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True);(OUT/'LOUDNESS_MEASUREMENT.txt').write_text(metrics.stderr[-2500:],encoding='utf-8')
report={'status':'MASTER_TECHNICAL_PASS_ASR_PENDING_LISTENING_PENDING','source_clips':50,'decode_pass':50,'order':'QUEUE.json indices, including A03-CTA01','native_format':params,'samples':cursor,'duration_seconds':cursor/params[2],'duration_mmss':f'{int(cursor/params[2])//60}:{int(cursor/params[2])%60:02d}','source_pcm_concat_exact':True,'inserted_silence_seconds':0,'source_gain_changes':False,'time_stretch':False,'native_master_sha256':sha(master),'delivery_master_sha256':sha(delivery),'delivery_format':'48000Hz 24-bit PCM; resampled from24kHz original, not new captured detail','peak_dbfs':round(20*np.log10(max(peak,1)/32768),3),'listening':'NOT_PERFORMED','asr':'PENDING'}
(OUT/'MASTER_TECHNICAL_QC.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)
