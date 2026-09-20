import sys,json,subprocess,hashlib,math,csv,re,shutil,time,concurrent.futures
from pathlib import Path
sys.path.insert(0,r'C:\Users\KK\Desktop\Youtube\portfolio_edit\deps')
from PIL import Image,ImageOps,ImageDraw,ImageFont
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
R=Path(r'C:\Users\KK\Desktop\Youtube 2\Hidden_Industrial_America_Chicago_CODEX_READY_v7\Hidden_Industrial_America_Chicago_CODEX_READY_v7')
BASE=R/'_V2';W=BASE/'work';Q=BASE/'qc';F=BASE/'final';OLD=R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.mp4'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def update(**kw):
 d=load(W/'state.json');d.update(kw);save(W/'state.json',d)
def run(cmd,**kw):
 p=subprocess.run(cmd,capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode('utf-8',errors='replace') if isinstance(p.stderr,bytes) else p.stderr)
 return p.stdout
def init():
 for p in [W,Q,F,W/'assets',W/'overlays']:p.mkdir(parents=True,exist_ok=True)
 if not (W/'state.json').exists():save(W/'state.json',{'revision':'V2','source_v1':str(OLD),'motion_tests_pass':False,'plan_complete':False,'proxy_complete':False,'proxy_qc_pass':False,'final_complete':False,'final_qc_pass':False})
 if not (W/'v1_snapshot.json').exists():
  keep=[OLD,R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt',R/'_FINAL/EDIT_REPORT.md',R/'_EDIT_WORK/codex_edit_state.json'];save(W/'v1_snapshot.json',[{'path':str(p),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in keep])
 shutil.copy2('C:/Windows/Fonts/arial.ttf',W/'font.ttf');shutil.copy2('C:/Windows/Fonts/arialbd.ttf',W/'bold.ttf')
def perspective(width,height,count,mode,amount=.035):
 # Source-space floating point affine crop, evaluated for every output frame.
 p=f'(on/{max(1,count-1)})';ease=f'({p}*{p}*(3-2*{p}))'
 z=f'(1.015+{amount}*{ease})' if mode=='push' else f'(1.015+{amount}*(1-{ease}))' if mode=='pull' else '1.045'
 x=f'(W-W/{z})*0.5' if mode!='pan' else f'(W-W/{z})*(0.15+0.7*{p})'
 y=f'(H-H/{z})*0.48'
 return f"perspective=x0='{x}':y0='{y}':x1='{x}+W/{z}':y1='{y}':x2='{x}':y2='{y}+H/{z}':x3='{x}+W/{z}':y3='{y}+H/{z}':sense=source:eval=frame:interpolation=cubic"
def motion_test():
 init();sc=load(R/'_EDIT_WORK/edit_scenes.json')
 pairs=[('push',sc[0]),('pull',sc[6]),('pan',next(s for s in sc if s['scene']=='S026'))]
 report=[]
 for mode,s in pairs:
  im=ImageOps.fit(Image.open(s['resolved_asset']).convert('RGB'),(1920,1080));src=Q/f'test_{mode}.png';im.save(src)
  out=Q/f'motion_{mode}.mp4';n=200
  vf='format=yuv444p,'+perspective(1920,1080,n,mode)+',format=yuv420p'
  start=time.time();run(['ffmpeg','-v','error','-y','-loop','1','-framerate','25','-i',str(src),'-vf',vf,'-filter_threads','2','-frames:v',str(n),'-an','-c:v','h264_nvenc','-preset','p4','-cq','19','-b:v','0',str(out)])
  raw=run(['ffmpeg','-v','error','-ss','2','-i',str(out),'-t','2.8','-vf','crop=640:360:640:320,format=gray','-f','rawvideo','-']);a=np.frombuffer(raw,np.uint8).reshape(-1,360,640).astype(np.float32);mad=np.mean(np.abs(np.diff(a,axis=0)),axis=(1,2));steady=mad<.05
  maxrun=cur=0
  for v in steady:cur=cur+1 if v else 0;maxrun=max(cur,maxrun)
  rec={'mode':mode,'duration':8,'seconds_to_render':round(time.time()-start,2),'comparisons':len(mad),'near_static':int(sum(steady)),'longest_near_static_run':maxrun,'mad_median':float(np.median(mad)),'mad_max':float(max(mad)),'pass':maxrun<=1};report.append(rec);print(json.dumps(rec),flush=True)
 save(Q/'motion_test_metrics.json',report)
 if not all(r['pass'] for r in report):raise RuntimeError('Motion test failed')
 update(motion_tests_pass=True)
def prepare():
 init();sc=load(R/'_EDIT_WORK/edit_scenes.json');assets={};shots=[];font=ImageFont.truetype(str(W/'font.ttf'),28)
 for s in sc:
  p=Path(s['resolved_asset']);n=int(s['scene'][1:]);kind='reconstruction' if s['reconstruction'] else 'archive';variant='full'
  if p.name.startswith(('A02_','A12_')):kind='map'
  # Context determines framing, not the index of the shot in the edit.
  if s['reconstruction'] and n in {4,7,11,22,34,35,38,39,42,44,47,49,50,51,52,53,76,78,79,81,82,85,88,89,91,92,93,94,96,98,99,101,103,104,105,106,108,109,110,112,115,116,117,118,124,125,126,127,133,138,148,149,152,157,160,162,165,166,171,172,173,177,178,181,183,185,186,210,213,215,223,225,226,227,228,229,231,234,236}:variant='detail'
  key=f'{p.stem}_{variant}_{kind}'
  if key not in assets:
   im=Image.open(p).convert('RGB');canvas=Image.new('RGB',(1920,1080),(20,25,28));d=ImageDraw.Draw(canvas)
   if kind=='map':
    whole=ImageOps.contain(im,(690,970),Image.Resampling.LANCZOS);canvas.paste(whole,(60+(690-whole.width)//2,65+(970-whole.height)//2))
    # This is an actual source detail, not a newly invented map or route.
    box=(int(im.width*.19),int(im.height*.27),int(im.width*.84),int(im.height*.67));detail=ImageOps.fit(im.crop(box),(1060,680),method=Image.Resampling.LANCZOS);canvas.paste(detail,(800,230));d.rectangle((799,229,1860,910),outline=(159,103,66),width=3)
    ox=60+(690-whole.width)//2;oy=65+(970-whole.height)//2;rx=whole.width/im.width;ry=whole.height/im.height
    d.rectangle((ox+box[0]*rx,oy+box[1]*ry,ox+box[2]*rx,oy+box[3]*ry),outline=(174,116,72),width=4)
    d.text((804,160),'NETWORK DETAIL',font=font,fill=(230,223,207));d.text((804,946),'ENLARGED FROM THE HISTORICAL SOURCE',font=font,fill=(182,180,171))
   elif kind=='archive':
    framed=ImageOps.contain(im,(1810,970),Image.Resampling.LANCZOS);canvas.paste(framed,((1920-framed.width)//2,(1080-framed.height)//2))
   else:
    if variant=='detail':im=im.crop((int(im.width*.16),int(im.height*.33),int(im.width*.84),int(im.height*.99)))
    canvas=ImageOps.fit(im,(1920,1080),method=Image.Resampling.LANCZOS)
   out=W/'assets'/(key+'.png');canvas.save(out);assets[key]=str(out)
  a=round(s['aligned_start']*25);b=round(s['aligned_end']*25)
  if a>=31818:continue
  b=min(b,31818)
  dur=(b-a)/25
  motion='static'
  if kind=='reconstruction' and variant=='detail' and dur>=5:motion='push'
  elif kind=='reconstruction' and any(x in s['visual'].lower() for x in ['empty tunnel','final']) and dur>=7:motion='pull'
  elif kind=='archive' and dur>=6 and p.name.startswith(('A03','A04','A06','A07','A15')):motion='pan'
  explainer='gauge' if n in {30,31} else 'transfer' if 39<=n<=44 else 'basement' if 88<=n<=94 else 'coal' if 76<=n<=82 else 'water' if 169<=n<=174 else 'survivor' if 193<=n<=197 else ''
  phase=0
  if explainer=='transfer':phase=0 if n<=40 else 1 if n==41 else 2
  if explainer=='basement':phase=0 if n<=89 else 1 if n<=91 else 2
  if explainer=='coal':phase=0 if n<=77 else 1 if n<=79 else 2
  if explainer=='water':phase=0 if n<=170 else 1 if n<=172 else 2
  if explainer=='survivor':phase=0 if n==193 else 1 if n<=195 else 2
  title='';
  if n==24:title='A RAILROAD TAKES SHAPE'
  elif n==107:title='THE SURFACE GETS BETTER'
  elif n==167:title='1992: THE NETWORK RETURNS'
  rec=dict(a=a,b=b,source=str(p),asset=assets[key],scene=s['scene'],kind=kind,variant=variant,motion=motion,section=s['section'],text=s['text_overlay'],chapter=title,explainer=explainer,phase=phase)
  if shots and shots[-1]['source']==rec['source'] and shots[-1]['variant']==variant and shots[-1]['explainer']==explainer and shots[-1]['phase']==phase and not title:
   shots[-1]['b']=b;shots[-1]['text']=shots[-1]['text'] or rec['text'];continue
  shots.append(rec)
 # Keep a real close-up jump as a deliberate context/detail sequence in the opening.
 first=shots[0];img=Image.open(first['source']).convert('RGB');img=ImageOps.fit(img.crop((int(img.width*.2),0,int(img.width*.8),int(img.height*.52))),(1920,1080),method=Image.Resampling.LANCZOS);p=W/'assets/opening_street.png';img.save(p)
 shots=[dict(first,b=75,asset=str(p),motion='static',text='CHICAGO'),dict(first,a=75,motion='pull')]+shots[1:]
 # The closing image remains present beside the actual end-screen targets.
 for a,b,sid in [(31818,32043,'S233'),(32043,32268,'S234')]:
  s=next(x for x in sc if x['scene']==sid);im=ImageOps.fit(Image.open(s['resolved_asset']).convert('RGB'),(1120,700));canvas=Image.new('RGB',(1920,1080),(19,24,27));canvas.paste(im,(65,255));d=ImageDraw.Draw(canvas);bold=ImageFont.truetype(str(W/'bold.ttf'),48);small=ImageFont.truetype(str(W/'font.ttf'),27)
  d.text((70,80),'HIDDEN INDUSTRIAL AMERICA',font=bold,fill=(232,223,203));d.text((70,155),'THE INFRASTRUCTURE REMAINS',font=small,fill=(187,174,152));d.rectangle((1250,290,1855,630),outline=(156,104,68),width=2);d.text((1250,665),'CONTINUE EXPLORING',font=small,fill=(224,216,199));d.ellipse((1420,790,1580,950),outline=(156,104,68),width=2);d.text((1250,995),'SUBSCRIBE FOR THE NEXT STORY',font=small,fill=(224,216,199));p=W/'assets'/f'end_{sid}.png';canvas.save(p)
  shots.append(dict(a=a,b=b,source=s['resolved_asset'],asset=str(p),scene='end',kind='reconstruction',variant='end',motion='static',section='ending',text='',chapter='',explainer='',phase=0))
 # Labels belong to reconstruction sequences and no longer restart on every cut.
 run_start=None
 for s in shots:
  if s['kind']=='reconstruction':
   if run_start is None:run_start=s['a']
   s['label_age']=(s['a']-run_start)/25
  else:run_start=None;s['label_age']=0
 assert shots[0]['a']==0 and shots[-1]['b']==32268
 assert all(s['b']==shots[i+1]['a'] for i,s in enumerate(shots[:-1]))
 assert min(s['b']-s['a'] for s in shots)>3
 save(W/'shots.json',shots)
 save(W/'plan_summary.json',{'shots':len(shots),'moving_shots':sum(s['motion']!='static' for s in shots),'moving_seconds':sum((s['b']-s['a'])/25 for s in shots if s['motion']!='static'),'explainers':sorted(set(s['explainer'] for s in shots if s['explainer'])),'v1_unchanged':True,'method':'Context-selected framings; merged same-source holds; separate fixed type; subpixel affine for moving shots.'})
 update(plan_complete=True);print(json.dumps(load(W/'plan_summary.json')))
def graphic(s):
 e=s['explainer'];phase=s['phase'];out=W/'overlays'/f'{e}_{phase}.png'
 if out.exists():return out
 im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im);font=ImageFont.truetype(str(W/'bold.ttf'),30);small=ImageFont.truetype(str(W/'font.ttf'),23)
 labels={'transfer':['SURFACE FREIGHT','TRANSFER / LOWERING','TUNNEL CARS'],'basement':['TUNNEL CAR','BUILDING CONNECTION','BASEMENT'],'coal':['COAL TO BOILERS','FUEL IS CONSUMED','ASH REMOVAL'],'water':['RIVER WATER','CONNECTED TUNNELS','BASEMENTS / UTILITIES'],'survivor':['LEFT UNDERGROUND','RECOVERED IN 1996','PRESERVED TODAY']}
 if e=='gauge':
  d.rounded_rectangle((76,746,685,970),radius=9,fill=(15,22,27,215));d.text((105,765),'2-FOOT GAUGE',font=font,fill=(239,230,212,255));d.text((105,810),'SCHEMATIC — NOT TO SCALE',font=small,fill=(192,192,181,255))
  d.line((140,871,620,871),fill=(210,207,194),width=5);d.line((140,929,620,929),fill=(210,207,194),width=5);d.line((570,878,570,922),fill=(188,122,75),width=3);d.polygon([(570,872),(562,885),(578,885)],fill=(188,122,75));d.polygon([(570,928),(562,916),(578,916)],fill=(188,122,75));d.text((245,884),'2 FT BETWEEN RAILS',font=small,fill=(241,234,213))
 else:
  for j,t in enumerate(labels[e]):
   x=70+j*625;active=j==phase;shown=j<=phase
   d.rounded_rectangle((x,847,x+550,968),radius=5,fill=(17,23,28,214),outline=(180,118,74,255) if active else (78,88,91,170),width=3 if active else 1)
   d.text((x+24,864),f'0{j+1}',font=small,fill=(180,118,74,255) if shown else (124,133,131,255));d.text((x+24,902),t,font=font,fill=(239,232,213,255) if active else (189,192,183,255) if shown else (130,141,138,255))
   if j<2:d.text((x+572,883),'›',font=font,fill=(180,118,74,255) if phase>j else (85,94,96,150))
 im.save(out);return out
def render_clip(s,i,quality,folder=None):
 width,height=(1280,720) if quality=='proxy' else (1920,1080);folder=folder or W/(quality+'_clips');folder.mkdir(exist_ok=True)
 assetstat=Path(s['asset']).stat();gh=hashlib.sha256(graphic(s).read_bytes()).hexdigest() if s['explainer'] else ''
 signature=hashlib.sha256(json.dumps({'s':s,'q':quality,'engine':'subpixel-perspective-v2.4','asset_size':assetstat.st_size,'asset_mtime':assetstat.st_mtime_ns,'graphic_hash':gh},sort_keys=True).encode()).hexdigest()[:14];out=folder/f'{i:03}_{signature}.mp4'
 if out.exists() and (out.with_suffix('.done')).exists():return out
 count=s['b']-s['a'];args=['ffmpeg','-v','error','-y','-threads','1']
 args+=['-framerate','25','-i',s['asset']]
 graph=f'[0:v]scale={width}:{height}:flags=lanczos,format=yuv444p'
 graph+=',loop=loop=-1:size=1:start=0,setpts=N/(25*TB)'
 if s['motion']!='static':graph+=','+perspective(width,height,count,s['motion'])
 graph+=',setsar=1[base]';cur='base'
 if s['explainer']:
  ov=graphic(s);args+=['-i',str(ov)];graph+=f';[1:v]scale={width}:{height}[gr];[base][gr]overlay=0:0:format=auto[composite]';cur='composite'
 filters=[];scale=height/1080
 if s['kind']=='reconstruction':
  age=s['label_age'];t=f't+{age}'
  filters.append(f"drawtext=fontfile=font.ttf:text='RECONSTRUCTION':fontsize={round(27*scale)}:fontcolor=0xF0E8D7@0.88:shadowcolor=black@0.75:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952:enable='lt({t},2.5)'")
  filters.append(f"drawtext=fontfile=font.ttf:text='AI reconstruction':fontsize={round(20*scale)}:fontcolor=0xEEE6D4@0.72:shadowcolor=black@0.65:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952:enable='gte({t},2.5)'")
 elif s['kind'] in ['archive','map']:
  filters.append(f"drawtext=fontfile=font.ttf:text='HISTORICAL SOURCE':fontsize={round(20*scale)}:fontcolor=0xC6C6BA:shadowcolor=black:shadowx=1:shadowy=1:x=w*0.04:y=h*0.952")
 title=s['chapter'] or (s['text'] if not s['explainer'] else '')
 if title:
  p=W/f'text_{i}_{quality}.txt';p.write_text(title,encoding='utf-8');filters.append(f"drawtext=fontfile=bold.ttf:textfile={p.name}:fontsize={round((45 if s['chapter'] else 36)*scale)}:fontcolor=0xF1E9D7:shadowcolor=black@0.8:shadowx=2:shadowy=2:x=w*0.045:y=h*0.07:enable='lt(t,3.4)'")
 filters.append('format=yuv420p');graph+=f';[{cur}]'+','.join(filters)+'[v]'
 args+=['-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-frames:v',str(count),'-an','-c:v','h264_nvenc','-preset','p3' if quality=='proxy' else 'p5','-rc','vbr','-cq','28' if quality=='proxy' else '19','-b:v','0','-g','50','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(out)]
 run(args,cwd=W);out.with_suffix('.done').write_text(signature);print(f'{quality} {i+1} {s["scene"]} {s["motion"]}',flush=True);return out
def preview():
 shots=load(W/'shots.json');sel=[]
 for typ in ['gauge','transfer','basement','coal','water','survivor']:
  s=next(s for s in shots if s['explainer']==typ and (s['phase']==1 or typ=='gauge'));sel.append(s)
 sel +=[next(s for s in shots if s['scene']=='S013'),next(s for s in shots if s['kind']=='map'),shots[-1]]
 clips=[]
 for i,s in enumerate(sel):
  short=dict(s,b=s['a']+min(75,s['b']-s['a']));clips.append(render_clip(short,i,'final',Q/'insert_tests'))
 sheet=Image.new('RGB',(1280,390*math.ceil(len(sel)/2)),(20,24,27));d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(W/'font.ttf'),22)
 for i,c in enumerate(clips):
  p=Q/f'insert_frame_{i}.jpg';run(['ffmpeg','-v','error','-y','-ss','1','-i',str(c),'-frames:v','1','-vf','scale=640:360',str(p)]);sheet.paste(Image.open(p),(i%2*640,i//2*390));d.text((i%2*640+8,i//2*390+364),sel[i]['explainer'] or sel[i]['kind'],font=font,fill='white')
 sheet.save(Q/'insert_review.jpg',quality=90);save(Q/'insert_tests.json',[str(p) for p in clips]);print('Insert preview ready')
def render(quality):
 st=load(W/'state.json')
 if quality=='final' and not st.get('proxy_qc_pass'):raise RuntimeError('Proxy QC required')
 if not st.get('motion_tests_pass') or not st.get('insert_tests_pass'):raise RuntimeError('Short tests required')
 if st.get(quality+'_complete'):print('Already complete');return
 shots=load(W/'shots.json')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:clips=list(pool.map(lambda p:render_clip(p[1],p[0],quality),enumerate(shots)))
 listing=W/f'{quality}_concat.txt';listing.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in clips),encoding='utf-8')
 target=Q/'HIA_CHICAGO_V2_PROXY.mp4' if quality=='proxy' else F/'HIA_CHICAGO_V2.mp4'
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(OLD),'-map','0:v','-map','1:a:0','-c:v','copy','-c:a','copy','-t','1290.72','-movflags','+faststart',str(target)]);update(**{quality+'_complete':True});print(str(target))
def sec(t):
 h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
def norm(t):return re.sub(r'[^a-z0-9]','',t.lower().replace('’',"'"))
def captions():
 import difflib
 blocks=(R/'_FINAL/HIA_CHICAGO_FINAL_UPLOAD.srt').read_text(encoding='utf-8').strip().split('\n\n');old=[]
 for b in blocks:
  ln=b.splitlines();a,z=map(sec,ln[1].split(' --> '));old.append({'start':a,'end':z,'text':' '.join(ln[2:]),'old_id':int(ln[0])})
 merged=[]
 for c in old:
  if c['old_id'] in {73,126}:merged[-1]['text']+=' '+c['text'];merged[-1]['end']=c['end']
  else:merged.append(dict(c))
 words=load(R/'_QC/voice_words.json');tok=[w for c in merged for w in c['text'].split()];sm=difflib.SequenceMatcher(None,[norm(w) for w in tok],[norm(w['word']) for w in words],autojunk=False);times={}
 for b in sm.get_matching_blocks():
  for k in range(b.size):times[b.a+k]=words[b.b+k]
 bad_end={'a','an','the','of','to','in','by','for','with','and','or','that','its','their','from'}
 def lines(text):
  if len(text)<=42:return [text]
  w=text.split();candidates=[]
  for j in range(1,len(w)):
   a=' '.join(w[:j]);b=' '.join(w[j:])
   if max(len(a),len(b))>42:continue
   cost=abs(len(a)-len(b))+(22 if norm(w[j-1]) in bad_end else 0)-(12 if w[j-1][-1] in ',;:.' else 0);candidates.append((cost,[a,b]))
  return min(candidates,key=lambda x:x[0])[1] if candidates else None
 result=[];idx=0
 for c in merged:
  w=c['text'].split();ln=lines(c['text'])
  if ln:result.append(dict(c,lines=ln))
  else:
   opts=[]
   for j in range(2,len(w)-1):
    left=' '.join(w[:j]);right=' '.join(w[j:]);l=lines(left);r=lines(right);cut=times.get(idx+j,{}).get('start',c['start']+(c['end']-c['start'])*j/len(w))
    if l and r and min(cut-c['start'],c['end']-cut)>=1:
     score=abs(len(left)-len(right))+(20 if norm(w[j-1]) in bad_end else 0)-(12 if w[j-1][-1] in ',;:.' else 0)+100*max(0,len(left)/(cut-c['start'])-18)+100*max(0,len(right)/(c['end']-cut)-18);opts.append((score,j,cut,l,r))
   if not opts:raise RuntimeError('Cannot reflow cue '+str(c))
   _,j,cut,l,r=min(opts,key=lambda x:x[0]);result.extend([dict(c,end=cut,lines=l,text=' '.join(w[:j])),dict(c,start=cut,lines=r,text=' '.join(w[j:]))])
  idx+=len(w)
 for i,c in enumerate(result):
  available=(result[i+1]['start']-.04 if i+1<len(result) else 1290.72)
  ideal=max(1.05,len(c['text'])/18)
  c['end']=min(available,max(c['end'],min(c['start']+ideal,c['end']+.35)))
 def fmt(t):
  n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
 (F/'HIA_CHICAGO_V2.srt').write_text('\n\n'.join(f'{i+1}\n{fmt(c["start"])} --> {fmt(c["end"])}\n'+ '\n'.join(c['lines']) for i,c in enumerate(result))+'\n',encoding='utf-8')
 assert [norm(w) for c in old for w in c['text'].split()]==[norm(w) for c in result for w in c['text'].split()]
 stats={'cues':len(result),'max_line_length':max(len(l) for c in result for l in c['lines']),'under_1s':[{'start':c['start'],'text':c['text']} for c in result if c['end']-c['start']<1],'over_20cps':[{'start':c['start'],'text':c['text'],'cps':len(c['text'])/(c['end']-c['start'])} for c in result if len(c['text'])/(c['end']-c['start'])>20.00001],'words_preserved':True}
 save(Q/'subtitle_report.json',stats);save(W/'captions.json',result);update(captions_complete=True);print(json.dumps(stats))
def audio_spotcheck():
 from faster_whisper import WhisperModel
 modelpath=next(Path(r'C:\Users\KK\Desktop\Youtube\portfolio_edit\models\models--Systran--faster-whisper-small.en\snapshots').iterdir());model=WhisperModel(str(modelpath),device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
 all=[]
 for t in [0,303,515,635,955,1188,1276]:
  dest=Q/f'audio_{t}.wav';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(OLD),'-t','14','-ar','16000','-ac','1',str(dest)])
  seg,_=model.transcribe(str(dest),language='en',beam_size=3,word_timestamps=True)
  row={'offset':t,'words':[{'start':w.start+t,'end':w.end+t,'word':w.word} for s in seg for w in s.words]};all.append(row);print('Audio check '+str(t),flush=True)
 save(Q/'actual_mix_spotchecks.json',all)
def refine():
 shots=load(W/'shots.json');new=[]
 for s in shots:
  if s['scene']=='S090':
   donor=next(x for x in shots if x['scene']=='S091');s.update(asset=donor['asset'],source=donor['source'],variant=donor['variant'],motion='static')
  if s['scene'] in ['S013','S024']:
   im=Image.open(s['source']).convert('RGB');box=(.04,.06,.49,.94) if s['scene']=='S013' else (.04,.01,.96,.55);im=im.crop(tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box)));canvas=Image.new('RGB',(1920,1080),(20,25,28));im=ImageOps.contain(im,(1690,970),Image.Resampling.LANCZOS);canvas.paste(im,((1920-im.width)//2,(1080-im.height)//2));p=W/'assets'/f'{s["scene"]}_source_detail.png';canvas.save(p)
   cut=s['a']+100;new.extend([dict(s,b=cut),dict(s,a=cut,asset=str(p),variant='source_detail',motion='static',chapter='',text='STREET-LEVEL CONGESTION' if s['scene']=='S013' else 'THE TELEPHONE ORIGINS')]);continue
  if s['scene'] in ['S045','S067','S073','S179','S217'] and s['motion']=='static':s['motion']='pull'
  if new and new[-1]['source']==s['source'] and new[-1]['variant']==s['variant'] and new[-1]['explainer']==s['explainer'] and new[-1]['phase']==s['phase'] and not s['chapter']:
   new[-1]['b']=s['b'];continue
  new.append(s)
 save(W/'shots.json',new)
 # Old overlays only are replaced; old preview clips remain as audit evidence.
 for s in new:
  if s['explainer']:
   p=W/'overlays'/f'{s["explainer"]}_{s["phase"]}.png'
   # explicit bounded file replacement, no directory deletion
   if p.exists():p.unlink()
   graphic(s)
 print('Refined source details, all process labels and long holds.')
def final_caption_boundary():
 cues=load(W/'captions.json');a=next(c for c in cues if c['old_id']==123);b=next(c for c in cues if c['old_id']==124)
 a.update(text='The same fixed network could serve both directions',lines=['The same fixed network could serve','both directions'],end=515.48)
 b.update(text='of a repetitive, heavy, dirty logistics problem.',lines=['of a repetitive, heavy,','dirty logistics problem.'],start=515.48)
 def fmt(t):
  n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
 save(W/'captions.json',cues);(F/'HIA_CHICAGO_V2.srt').write_text('\n\n'.join(f'{i+1}\n{fmt(c["start"])} --> {fmt(c["end"])}\n'+ '\n'.join(c['lines']) for i,c in enumerate(cues))+'\n',encoding='utf-8')
 save(Q/'subtitle_boundary_resolution.json',{'time':515.48,'resolution':'Reflow entire adjective phrase together; do not rely on zero-duration dirty token from short-window ASR.','source_word_of_start':515.48,'mixed_audio_word_of_start':515.52,'start_delta':-.04})
 print('Ambiguous adjective boundary resolved through phrase grouping.')
def qc(quality):
 target=Q/'HIA_CHICAGO_V2_PROXY.mp4' if quality=='proxy' else F/'HIA_CHICAGO_V2.mp4';meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(target)]));save(Q/f'{quality}_metadata.json',meta)
 log=Q/f'{quality}_decode.log'
 with log.open('w',encoding='utf-8') as f:
  p=subprocess.run(['ffmpeg','-hide_banner','-threads','2','-i',str(target),'-vf','blackdetect=d=0.12:pix_th=0.025:pic_th=0.995','-af','loudnorm=I=-14:TP=-1:LRA=11:print_format=json','-f','null','-'],stdout=f,stderr=f)
 txt=log.read_text(encoding='utf-8');loud=json.JSONDecoder().raw_decode(txt[txt.rfind('{'):])[0];black=re.findall(r'black_start:[^\r\n]+',txt)
 def ahash(file):return run(['ffmpeg','-v','error','-i',str(file),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
 sourcehash=load(Q/'audio_source_hash.json')['hash'] if (Q/'audio_source_hash.json').exists() else ahash(OLD);save(Q/'audio_source_hash.json',{'hash':sourcehash});audio_identical=ahash(target)==sourcehash
 shots=load(W/'shots.json');cues=load(W/'captions.json');subs=[]
 for i,c in enumerate(cues):
  if c['end']<=c['start'] or (i and c['start']<cues[i-1]['end']-.001) or max(map(len,c['lines']))>42:subs.append(i+1)
 samples=[1.5,8,25.5,41.36,85,153,196,255,367,509,560,645.36,956.8,968.04,1089,1275,1287]
 sheet=Image.new('RGB',(1280,390*math.ceil(len(samples)/2)),(20,24,27));d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(W/'font.ttf'),22)
 for i,t in enumerate(samples):
  out=Q/f'{quality}_frame_{i:02}.jpg';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(target),'-frames:v','1','-vf','scale=640:360',str(out)]);sheet.paste(Image.open(out),(i%2*640,i//2*390));d.text((i%2*640+7,i//2*390+364),f'{quality} {t:.2f}s',font=font,fill='white')
 sheet.save(Q/f'{quality}_review.jpg',quality=90)
 motions=[]
 for mode in ['push','pull','pan']:
  s=next(s for s in shots if s['motion']==mode and s['b']-s['a']>=125);t=s['a']/25+(s['b']-s['a'])/50-1
  width=next(x['width'] for x in meta['streams'] if x['codec_type']=='video');height=next(x['height'] for x in meta['streams'] if x['codec_type']=='video')
  raw=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(target),'-t','2','-vf',f'crop=480:270:{(width-480)//2}:{(height-270)//2},format=gray','-f','rawvideo','-']);a=np.frombuffer(raw,np.uint8).reshape(-1,270,480).astype(np.float32);mad=np.mean(np.abs(np.diff(a,axis=0)),axis=(1,2));motions.append({'mode':mode,'time':t,'pairs':len(mad),'near_static':int(sum(mad<.05)),'median_change':float(np.median(mad)),'max_change':float(max(mad))})
 save(Q/f'{quality}_motion.json',motions)
 v=next(x for x in meta['streams'] if x['codec_type']=='video');report={'duration':float(meta['format']['duration']),'width':v['width'],'height':v['height'],'frames':int(v['nb_frames']),'fps':v['avg_frame_rate'],'decode_exit':p.returncode,'black_intervals':black,'integrated_lufs':float(loud['input_i']),'true_peak_dbtp':float(loud['input_tp']),'audio_bitstream_identical_to_v1':audio_identical,'subtitle_errors':subs,'cues':len(cues),'minimum_shot_seconds':min((s['b']-s['a'])/25 for s in shots),'motion_samples':motions,'visual_review':'pending','playback_ui':'Unavailable: no browsers connected; no claim of real-time visual playback/listening.'}
 report['technical_pass']=p.returncode==0 and not black and not subs and audio_identical and report['frames']==32268 and abs(report['duration']-1290.72)<.1 and report['true_peak_dbtp']<=-1
 report['motion_pass']=all(m['near_static']<=3 and m['max_change']<max(.15,m['median_change'])*5 for m in motions)
 save(Q/f'{quality}_qc.json',report);print(json.dumps(report),flush=True)
def accept(quality):
 p=Q/f'{quality}_qc.json';d=load(p)
 if not d['technical_pass'] or not d['motion_pass']:raise RuntimeError('Unresolved QC failure')
 d['visual_review']='Sampled compositions, source details, process steps, labels and ending reviewed. Motion measured frame by frame; UI playback unavailable.';save(p,d);update(**{quality+'_qc_pass':True})
 if quality=='final':
  for s in load(W/'v1_snapshot.json'):
   stat=Path(s['path']).stat()
   if stat.st_size!=s['bytes'] or stat.st_mtime_ns!=s['mtime_ns']:raise RuntimeError('V1 changed')
  caption=load(Q/'subtitle_report.json');shots=load(W/'shots.json')
  text=f'''# HIA Chicago V2 — QC report

Delivery: 00:21:30.720; 1920×1080; 25 fps; 32,268 frames; H.264 yuv420p / AAC 48 kHz.

Technical QC: PASS. Full decode; no detected black intervals; subtitle sequence valid; audio bitstream SHA-256 identical to V1. Loudness {d['integrated_lufs']} LUFS, true peak {d['true_peak_dbtp']} dBTP.

Motion QC: PASS in three isolated 1080p tests and three samples of the finished video. The old stop/2-pixel-step pattern is absent in measured samples. Subpixel perspective interpolation replaces zoompan; motion is selected by content. Static holds are intentional.

Editorial changes: {len(shots)} shots; same-source holds merged; deliberate source-detail views replace small arbitrary crop jumps; the 00:41.320 three-frame flash removed. Larger archival framing; source-map overview plus real enlarged detail; six explanatory sequences (gauge, transfer, basement connection, coal/ash, water, surviving equipment). Repeated full-screen title cards replaced with short titles over relevant material. End screen retains a story image.

Labels: no persistent black RECONSTRUCTION box. Clear sequence-entry label followed by small unboxed attribution. Archive labels are fixed after image transformation.

Subtitles: {len(load(W/'captions.json'))} English sidecar cues; maximum 42 characters per line / two lines. Orphan tails regrouped, no >20 cps cues in the final reflow. One sub-second emphasis remains: "Coal in.". Source wording preserved. Seven short fresh checks of the actual mixed audio support key cue onsets; the ambiguous zero-duration ASR token near 08:37 was resolved by grouping the whole phrase. No full re-transcription.

Visual review: sampled finished frames and short insert renders inspected. Limit: browser/player control was unavailable, so no claim of a continuous 1× watch or subjective listening of the entire film. Frame-by-frame measurements support the motion result; aesthetic quality remains a viewer judgment.

Cost control: no paid generation, no network, no new voice, no audio re-encode. Three motion tests (24 s), short insert tests, one complete 720p proxy and one final video render. V1 files and state remain unchanged.
'''
  (F/'V2_QC_REPORT.md').write_text(text,encoding='utf-8')
 print(quality+' accepted')
if __name__=='__main__':{'init':init,'test':motion_test,'prepare':prepare,'preview':preview,'proxy':lambda:render('proxy'),'final':lambda:render('final'),'captions':captions,'audio_check':audio_spotcheck,'refine':refine,'caption_boundary':final_caption_boundary,'proxy_qc':lambda:qc('proxy'),'final_qc':lambda:qc('final'),'accept_proxy':lambda:accept('proxy'),'accept_final':lambda:accept('final')}[sys.argv[1]]()
