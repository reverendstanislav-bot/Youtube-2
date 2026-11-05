from pathlib import Path
import os,json,time
os.environ['HF_HUB_OFFLINE']='1'
from faster_whisper import WhisperModel
SRC=Path(r'C:\YOUTUBE\Youtube 2\Glomar Explorer\AUDIO\R1_2_VOICEBOX_QUEUE');OUT=SRC.parent/'R1_2_MASTER_ASR';dest=OUT/'ASR_MEDIUM_EN';dest.mkdir(exist_ok=True)
flags={d['paragraph_id'] for d in json.loads((OUT/'ASR_DIFF_BASE.json').read_text(encoding='utf-8')) if d['differences']}
cache=Path.home()/'.cache/huggingface/hub/models--Systran--faster-whisper-medium.en/snapshots';modeldir=next(p for p in cache.iterdir() if(p/'model.bin').exists());print('Loading cached medium.en CPU int8 for20 discrepant paragraphs',flush=True)
model=WhisperModel(str(modeldir),device='cpu',compute_type='int8',cpu_threads=6,num_workers=1,local_files_only=True)
q=json.loads((SRC/'QUEUE.json').read_text(encoding='utf-8'))
for i,j in enumerate([j for j in q['jobs'] if j['id'] in flags],1):
 p=dest/(j['id']+'.json')
 if p.exists():continue
 started=time.time();segs,info=model.transcribe(str(SRC/j['output_file']),language='en',beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,temperature=0)
 data=[]
 for s in segs:data.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in(s.words or [])]})
 p.write_text(json.dumps({'paragraph_id':j['id'],'model':'faster-whisper-medium.en CPU int8 VAD','expected':j['payload']['text'],'recognized':' '.join(s['text'].strip() for s in data),'segments':data,'initial_prompt':None},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'{i}/20 {j["id"]} {time.time()-started:.1f}s',flush=True)
print('Second-pass ASR complete.',flush=True)
