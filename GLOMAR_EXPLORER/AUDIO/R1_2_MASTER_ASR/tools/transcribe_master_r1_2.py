from pathlib import Path
import json,re,csv,difflib,time,os
os.environ['HF_HUB_OFFLINE']='1'
from faster_whisper import WhisperModel
SRC=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_VOICEBOX_QUEUE');OUT=SRC.parent/'R1_2_MASTER_ASR';ASR=OUT/'ASR_BASE_EN';ASR.mkdir(exist_ok=True)
q=json.loads((SRC/'QUEUE.json').read_text(encoding='utf-8'));timing=list(csv.DictReader((OUT/'PARAGRAPH_TIMING.csv').read_text(encoding='utf-8').splitlines()));offset={r['paragraph_id']:float(r['start_seconds']) for r in timing}
cache=Path.home()/'.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots';modeldir=next(p for p in cache.iterdir() if(p/'model.bin').exists());print('Loading cached base.en CPU int8',flush=True)
model=WhisperModel(str(modeldir),device='cpu',compute_type='int8',cpu_threads=6,num_workers=1,local_files_only=True)
for i,j in enumerate(q['jobs'],1):
 dest=ASR/(j['id']+'.json')
 if dest.exists():continue
 started=time.time();segments,info=model.transcribe(str(SRC/j['output_file']),language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,temperature=0)
 data=[]
 for s in segments:
  data.append({'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in(s.words or [])]})
 result={'paragraph_id':j['id'],'model':'faster-whisper-base.en CPU int8','source_audio':j['output_file'],'expected':j['payload']['text'],'recognized':' '.join(s['text'].strip() for s in data),'master_offset_seconds':offset[j['id']],'segments':data,'initial_prompt':None,'condition_on_previous_text':False}
 dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'{i}/50 {j["id"]} {time.time()-started:.1f}s',flush=True)
print('ASR complete:50/50. Comparison follows separately.',flush=True)
