from pathlib import Path
import numpy as np,subprocess,json,hashlib,csv
W=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');M=W/'MUSIC';fps=24;N=21310;sr=48000
manifest=json.loads(Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3\VIDEO010_FULL_R4_MANIFEST.json').read_text());shots=manifest['shots'];act={i:(min(x['s'] for x in shots if x['paragraph_id'].startswith(f'A{i:02d}-')),max(x['e'] for x in shots if x['paragraph_id'].startswith(f'A{i:02d}-'))) for i in range(1,11)}
def decode(path):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar',str(sr),'-'],capture_output=True,check=True);return np.frombuffer(p.stdout,dtype=np.float32).reshape(-1,2).copy()
tracks={r['id']:decode(r['path']) for r in json.loads((M/'SOURCE_RECORDS.json').read_text())}
# Narrative cue groups with deliberate quiet at the scientific evidence and final emotional resolution.
cueplan=[(610070,0,59,'Opening: unloading danger and central question',-31),
(609657,70,118,'1934 rescue; human stakes',-34),(595385,123,211,'Mobile base ambition and design explanation',-34),
(610070,226,291,'Public trials and road accident',-32),(610070,299,342,'Recovery, loading, departure',-34),
(610070,352,437,'Arrival, failed traction, ramp to shelf',-32),(595385,464,512,'Tire support comparison, restrained analytical bed',-36),
(610070,530,577,'Chain and tire experiments',-34),(610070,586,622,'Final winter excavation and failed retry',-31),
(609657,639,657,'Change of purpose; people at work',-35),(609657,679,751,'Abandonment and later discoveries',-34),
(595385,762,811,'Changing coast and unresolved fate',-35),(609657,818,846,'Crew callback and separation',-34),
(595385,860,887.9166667,'Camp Century handoff and 20-second end screen',-32)]
voice=decode(manifest['voice']['derived_voice']);vmono=voice.mean(axis=1)
# 100ms RMS follower; gentle voice-aware ducking, not hard pumping.
block=4800;rv=np.sqrt(np.mean(np.pad(vmono,(0,(-len(vmono))%block)).reshape(-1,block)**2,axis=1));env=np.interp(np.arange(int(N/fps*sr))/sr,np.arange(len(rv))*.1,rv,right=0)
duck=1-.38*np.clip(env/.07,0,1);out=np.zeros((int(N/fps*sr),2),np.float32);receipts=[]
for sid,start,end,reason,db in cueplan:
 src=tracks[sid];length=int((end-start)*sr)
 # Longer cues repeat with a 4s equal-power crossfade at the source boundary.
 take=src.copy();cross=4*sr
 while len(take)<length:
  a=np.linspace(0,1,cross,dtype=np.float32)[:,None];blend=take[-cross:]*(1-a)+src[:cross]*a;take=np.concatenate([take[:-cross],blend,src[cross:]])
 take=take[:length].copy();rms=np.sqrt(np.mean(take**2));gain=10**(db/20)/max(float(rms),1e-6);take*=gain
 fi=min(3*sr,len(take)//3);fo=min(4*sr,len(take)//3);take[:fi]*=np.linspace(0,1,fi)[:,None];take[-fo:]*=np.linspace(1,0,fo)[:,None]
 s=int(start*sr);e=min(s+len(take),len(out));out[s:e]+=take[:e-s]*duck[s:e,None]
 receipts.append(dict(source_id=sid,start_seconds=start,end_seconds=end,reason=reason,target_cue_rms_dbfs=db,voice_ducking='up to -4.15dB',fade_in_seconds=fi/sr,fade_out_seconds=fo/sr))
raw=W/'SCORE_R5.f32';raw.write_bytes(out.tobytes());dest=M/'VIDEO010_SCORE_R5_48K_S24.wav';subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i',str(raw),'-c:a','pcm_s24le','-y',str(dest)],check=True);raw.unlink()
(M/'SCORE_CUE_MAP.json').write_text(json.dumps(receipts,indent=2));print(json.dumps({'score':str(dest),'cues':len(receipts),'peak_dbfs':float(20*np.log10(np.max(np.abs(out)))),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'listening':'HOLD_NO_HUMAN_LISTENING_CLAIM'}))
# Every act mapped before changes. No new generation, no locked voice changes.
beat=[]
for i,(s,e) in act.items():beat.append({'act':i,'start_frame':s,'end_frame':e,'purpose':['Failed task before specs','Rescue motivates mobile base','One mechanism per explanation','Trials / public failures / recovery','Arrival and escalating ground obstacles','Separate load capacity from snow bearing','Repairs restore motion but not mission','People continue after transport fails','Dated rediscovery, not restart','Map evidence, inference, unresolved fate'][i-1],'treatment':'Stable real source + selective local mechanism reveal; archive only after source gate','music':'See SCORE_CUE_MAP.json','archive_rights_gate':'preserve existing HOLD, never silently clear'})
(W/'FULL_FILM_BEAT_MAP_R5.json').write_text(json.dumps(beat,indent=2))
