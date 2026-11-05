from pathlib import Path
import json,time,urllib.request,urllib.parse,hashlib,os,sys
ROOT=Path(__file__).resolve().parent;FILE=ROOT/'QUEUE.json';BASE='http://127.0.0.1:17493';LOCK=ROOT/'worker.lock'
def api(path,payload=None,timeout=30):
 req=urllib.request.Request(BASE+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)
def save(q):
 tmp=FILE.with_suffix('.tmp');tmp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(tmp,FILE)
def log(s):
 with(ROOT/'worker.log').open('a',encoding='utf-8')as f:f.write(time.strftime('%Y-%m-%d %H:%M:%S ')+s+'\n')
try:
 fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
except FileExistsError:sys.exit('Worker lock exists; verify existing worker before restart.')
q=json.loads(FILE.read_text(encoding='utf-8'))
try:
 assert hashlib.sha256((ROOT/'05_SCRIPT_R1_2_EN.md').read_bytes()).hexdigest()==q['source_sha256']
 profile=api('/profiles/'+q['profile_id']);assert profile['name']==q['profile_name'] and profile['default_engine']=='qwen'
 q['worker_pid']=os.getpid();q['status']='RUNNING';save(q);log('Started durable sequential queue; no text rewriting; local engine only.')
 for job in q['jobs']:
  if job['status']=='COMPLETED':continue
  assert hashlib.sha256(job['payload']['text'].encode()).hexdigest()==job['text_sha256']
  if not job.get('generation_id'):
   history=api('/history?'+urllib.parse.urlencode({'profile_id':q['profile_id'],'limit':50,'offset':0,'search':job['payload']['text'][:80]}))
   if isinstance(history,dict):history=history.get('items',history.get('generations',history.get('history',[])))
   matches=[h for h in history if h.get('text')==job['payload']['text'] and h.get('seed')==job['payload']['seed']]
   if len(matches)>1:raise RuntimeError('Multiple matching jobs; manual reconciliation required: '+job['id'])
   if matches:job['generation_id']=matches[0]['id'];log('Recovered existing '+job['id'])
   else:
    if job['status'] in ['SUBMITTING','SUBMISSION_UNCERTAIN']:raise RuntimeError('Previous submission uncertain; do not automatically resubmit '+job['id'])
    job['status']='SUBMITTING';save(q)
    try:response=api('/generate',job['payload'],timeout=60)
    except Exception:
     job['status']='SUBMISSION_UNCERTAIN';save(q);raise
    gid=response.get('id') or response.get('generation_id')
    if not gid:job['status']='SUBMISSION_UNCERTAIN';job['response']=response;save(q);raise RuntimeError('No generation ID')
    job['generation_id']=gid;job['submission_response']=response
   job['status']='SUBMITTED';save(q);log(job['id']+' accepted '+job['generation_id'])
  while True:
   status=api('/generate/'+job['generation_id']+'/status');job['last_status']=status;save(q)
   phase=str(status.get('status','')).lower()
   if phase in ['completed','complete','done','success','succeeded']:break
   if phase in ['failed','error','cancelled','canceled']:job['status']='FAILED';save(q);raise RuntimeError(job['id']+' '+str(status))
   time.sleep(15)
  wav=ROOT/(job['id']+'.wav');temp=wav.with_suffix('.download')
  with urllib.request.urlopen(BASE+'/audio/'+job['generation_id'],timeout=120) as r:temp.write_bytes(r.read())
  assert temp.stat().st_size>44,'Empty audio';os.replace(temp,wav)
  job['output_file']=wav.name;job['audio_sha256']=hashlib.sha256(wav.read_bytes()).hexdigest();job['status']='COMPLETED';save(q);log(job['id']+' downloaded; listening/ASR not performed')
 q['status']='GENERATED_AWAITING_QC';save(q);log('Queue complete. No master/ASR/listening claimed.')
except Exception as e:
 q['status']='HOLD_WORKER_ERROR';q['error']=repr(e);save(q);log('HOLD '+repr(e));raise
finally:LOCK.unlink(missing_ok=True)

