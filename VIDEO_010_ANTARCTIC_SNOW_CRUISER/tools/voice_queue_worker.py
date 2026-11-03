"""Durable serial Voicebox queue. Local Qwen only; no rewriting, no automatic retakes."""
import argparse,datetime,hashlib,json,os,sys,time,urllib.request,urllib.error,wave,msvcrt
from pathlib import Path
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic(path,obj):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,path)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--queue',required=True);ap.add_argument('--state-dir',required=True);ap.add_argument('--api',default='http://127.0.0.1:17493');args=ap.parse_args()
 if args.api!='http://127.0.0.1:17493':raise SystemExit('Only the verified local Voicebox endpoint is authorized.')
 qpath=Path(args.queue);out=Path(args.state_dir);out.mkdir(parents=True,exist_ok=True);(out/'RAW_WAV').mkdir(exist_ok=True)
 mutex=(out/'worker.lock').open('a+b');mutex.seek(0,2)
 if mutex.tell()==0:mutex.write(b'1');mutex.flush()
 mutex.seek(0)
 try:msvcrt.locking(mutex.fileno(),msvcrt.LK_NBLCK,1)
 except OSError:raise SystemExit('This queue already has a worker; no duplicate started.')
 queue=json.loads(qpath.read_text(encoding='utf-8-sig'));digest=sha(qpath.read_bytes());sp=out/'QUEUE_STATE.json'
 state=json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else dict(queue_id=queue['queue_id'],input_sha256=digest,created_utc=now(),jobs=[dict(paragraph_id=j['paragraph_id'],status='LOCAL_QUEUED',generation_id=None) for j in queue['jobs']])
 if state['input_sha256']!=digest:raise SystemExit('Frozen queue input changed; refusing submission.')
 def request(path,payload=None):
  data=json.dumps(payload,ensure_ascii=False).encode() if payload is not None else None
  req=urllib.request.Request(args.api+path,data=data,headers={'Content-Type':'application/json; charset=utf-8'} if data else {})
  with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
 def save(status,**extra):
  state.update(status=status,worker_pid=os.getpid(),updated_utc=now(),**extra)
  state['counts']={k:sum(j['status']==k for j in state['jobs']) for k in sorted({j['status'] for j in state['jobs']})};atomic(sp,state)
 def log(event,**kw):
  with (out/'EVENTS.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(time=now(),event=event,**kw))+'\n')
 save('WORKER_STARTED');log('WORKER_STARTED',pid=os.getpid())
 try:
  profile=request('/profiles/'+queue['profile']['id'])
  if profile['name']!='Harrison' or profile.get('default_engine')!='qwen':raise RuntimeError('Verified Harrison/Qwen profile changed.')
  for job,entry in zip(queue['jobs'],state['jobs']):
   text=job['payload']['text'];assert sha(text.encode())==job['text_sha256']
   if entry['status']=='GENERATED_TECHNICAL_UNREVIEWED':continue
   while True:
    if (out/'STOP_REQUESTED').exists():save('STOPPED_BY_OWNER_FILE');return
    try:
     if entry.get('generation_id'):
      info=request('/history/'+entry['generation_id']);status=info['status']
      if status in ['failed','error','cancelled','canceled']:
       entry.update(status='HOLD_GENERATION_FAILED',error=info.get('error'));save('HOLD_FAILED_NO_AUTO_RETRY');return
      if status!='completed':
       entry['status']='VOICEBOX_'+status.upper();save('WAIT_OWN_GENERATION');time.sleep(20);continue
      dest=out/'RAW_WAV'/(job['paragraph_id']+'.wav')
      if not dest.exists():
       with urllib.request.urlopen(args.api+'/audio/'+entry['generation_id'],timeout=180) as response:data=response.read()
       temp=dest.with_suffix('.part');temp.write_bytes(data)
       with wave.open(str(temp),'rb') as w:
        if w.getnframes()<=0:raise RuntimeError('Empty generated WAV')
        entry.update(duration_seconds=w.getnframes()/w.getframerate(),sample_rate=w.getframerate(),channels=w.getnchannels(),sample_width_bytes=w.getsampwidth())
       os.replace(temp,dest)
      entry.update(status='GENERATED_TECHNICAL_UNREVIEWED',output=str(dest),audio_sha256=sha(dest.read_bytes()),completed_utc=now(),listening_qc=False,asr_qc=False)
      save('GENERATING_SERIAL_QUEUE');log('DOWNLOADED_UNREVIEWED',paragraph_id=job['paragraph_id'],generation_id=entry['generation_id']);break
     history=request('/history?limit=50')['items']
     # Seed+exact text+profile identify ONLY this queue's submission.
     matches=[x for x in history if x.get('profile_id')==queue['profile']['id'] and x.get('seed')==job['payload']['seed'] and x.get('text')==text and x.get('engine')=='qwen']
     if matches:
      if len(matches)!=1:entry['status']='HOLD_DUPLICATE_MATCH';save('HOLD_AMBIGUOUS_EXISTING_GENERATION');return
      entry.update(generation_id=matches[0]['id'],status='ADOPTED_EXISTING_SUBMISSION');save('RESUMED');continue
     if entry['status'] in ['SUBMITTING','SUBMISSION_UNCERTAIN']:
      save('HOLD_UNCERTAIN_SUBMISSION_NO_BLIND_RETRY');return
     active=[dict(id=x['id'],status=x['status']) for x in history if x.get('status') in ['generating','pending','queued','processing']]
     if active:
      save('WAIT_EXISTING_VOICEBOX_JOBS',other_active_count=len(active),other_active_ids=[x['id'] for x in active],last_error=None);time.sleep(20);continue
     entry.update(status='SUBMITTING',submission_started_utc=now());save('SUBMITTING_ONE_JOB')
     try:reply=request('/generate',job['payload'])
     except Exception as e:
      entry.update(status='SUBMISSION_UNCERTAIN',error=str(e));save('HOLD_UNCERTAIN_SUBMISSION_NO_BLIND_RETRY');return
     if not reply.get('id'):entry['status']='SUBMISSION_UNCERTAIN';save('HOLD_MISSING_GENERATION_ID');return
     entry.update(generation_id=reply['id'],status='VOICEBOX_'+reply.get('status','pending').upper());save('SUBMITTED');log('SUBMITTED',paragraph_id=job['paragraph_id'],generation_id=reply['id']);time.sleep(20)
    except (urllib.error.URLError,TimeoutError,OSError) as e:
     save('WAIT_API_OR_DOWNLOAD',last_error=str(e));time.sleep(30)
  save('ALL_GENERATED_TECHNICAL_ONLY_ASR_AND_LISTENING_PENDING');log('QUEUE_DRAINED')
 except Exception as e:
  save('HOLD_WORKER_ERROR',last_error=str(e));raise
 finally:
  mutex.seek(0);msvcrt.locking(mutex.fileno(),msvcrt.LK_UNLCK,1);mutex.close()
if __name__=='__main__':main()
