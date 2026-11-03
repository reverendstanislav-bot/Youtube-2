from pathlib import Path
import json,csv,re,time,hashlib
from faster_whisper import WhisperModel
L=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');Q=L/'AUDIO/R5_1_HARRISON_QUEUE';O=L/'AUDIO/R5_1_MASTER_QC/ASR';O.mkdir(exist_ok=True)
jobs=json.loads((Q/'08_VOICE_JOBS_R5_1.json').read_text(encoding='utf-8'))['jobs'];state=json.loads((Q/'QUEUE_STATE.json').read_text(encoding='utf-8'));byid={x['paragraph_id']:x for x in state['jobs']}
model=WhisperModel('medium.en',device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
def norm(s):return re.findall(r"[a-z0-9]+",s.lower().replace('?',"'"))
def distance(a,b):
 dp=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  nd=[i]+[0]*len(b)
  for j,y in enumerate(b,1):nd[j]=min(dp[j]+1,nd[j-1]+1,dp[j-1]+(x!=y))
  dp=nd
 return dp[-1]
results=[]
for i,j in enumerate(jobs,1):
 pid=j['paragraph_id'];f=Path(byid[pid]['output']);dest=O/(pid+'.json')
 if dest.exists():data=json.loads(dest.read_text(encoding='utf-8'))
 else:
  segments,info=model.transcribe(str(f),language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
  segments=[dict(start=s.start,end=s.end,text=s.text,words=[dict(word=w.word,start=w.start,end=w.end,probability=w.probability) for w in (s.words or [])]) for s in segments]
  text=' '.join(s['text'].strip() for s in segments);expected=j['payload']['text'];a,b=norm(expected),norm(text);ed=distance(a,b)
  data=dict(paragraph_id=pid,source=str(f),source_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),model='faster-whisper-medium.en CPUint8',expected=expected,text=text,segments=segments,raw_token_edit_distance=ed,reference_tokens=len(a),raw_recognition_error_rate=ed/max(1,len(a)),status='ASR_FLAG_REVIEW' if ed else 'ASR_TEXT_MATCH_NOT_LISTENING_PASS')
  dest.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 results.append({k:data[k] for k in ['paragraph_id','status','raw_token_edit_distance','reference_tokens','raw_recognition_error_rate','expected','text']})
 (O/'PROGRESS.json').write_text(json.dumps(dict(completed=i,total=len(jobs),status='RUNNING' if i<len(jobs) else 'COMPLETE_REVIEW_FLAGS',model='medium.en',elapsed_note='No TTS generation or retakes'),indent=2),encoding='utf-8')
 print(pid,data['status'],data['raw_token_edit_distance'],flush=True)
with (O/'ASR_DIFF_SUMMARY.csv').open('w',encoding='utf-8-sig',newline='') as h:w=csv.DictWriter(h,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
(O/'SUMMARY.json').write_text(json.dumps(dict(paragraphs=len(results),exact_token_matches=sum(x['status']=='ASR_TEXT_MATCH_NOT_LISTENING_PASS' for x in results),flagged=sum(x['status']=='ASR_FLAG_REVIEW' for x in results),full_listening=False,model='medium.en'),indent=2),encoding='utf-8')
