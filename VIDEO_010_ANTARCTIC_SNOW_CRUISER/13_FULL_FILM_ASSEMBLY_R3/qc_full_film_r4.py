from pathlib import Path
import json,time,subprocess,hashlib,csv,re,math
import numpy as np
from PIL import Image,ImageOps,ImageDraw
W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');ROOT=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');out=W/'QC_FULL_FILM_R4';out.mkdir(exist_ok=True)
def run(args,binary=False):
 p=subprocess.run(args,capture_output=True,text=not binary);assert p.returncode==0,str(p.stderr)[-3000:];return p
while True:
 s=json.loads((W/'FULL_FILM_STATE.json').read_text())
 if s['stage']=='ERROR_REQUIRES_REPAIR':raise RuntimeError(s.get('error'))
 if s['stage']=='FULL_REVIEW_RENDER_READY':break
 time.sleep(30)
film=W/'RENDERS/VIDEO010_FULL_R4_HD_REVIEW.mp4';m=json.loads((W/'VIDEO010_FULL_R4_MANIFEST.json').read_text());rows=m['shots'];assert len(rows)==193
# Full decode and black-interval scan are technical checks, not an audiovisual listening pass.
p=run(['ffmpeg','-hide_banner','-i',str(film),'-vf','blackdetect=d=0.20:pix_th=0.10:pic_th=0.98','-f','null','-']);(out/'FULL_DECODE_AND_BLACK_SCAN.log').write_text(p.stderr,encoding='utf-8')
black=re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',p.stderr)
a=run(['ffmpeg','-v','error','-ss',str(20830/24),'-i',str(film),'-t','20','-map','0:a:0','-ac','1','-ar','48000','-f','f32le','pipe:1'],binary=True);samples=np.frombuffer(a.stdout,dtype='<f4');peak=float(np.max(np.abs(samples))) if len(samples) else None;rms=float(np.sqrt(np.mean(samples*samples))) if len(samples) else None
frames=[(x['s']+x['e'])//2 for x in rows]+[20834,21070,21305];expr='select='+('+'.join('eq(n\\,'+str(n)+')' for n in frames));dest=out/'FRAMES';dest.mkdir(exist_ok=True)
run(['ffmpeg','-v','error','-i',str(film),'-vf',expr,'-fps_mode','vfr','-q:v','3','-frames:v',str(len(frames)),str(dest/'FRAME_%03d.jpg')])
labels=[x['shot_id']+' '+x['asset_id']+' '+x['paragraph_id'] for x in rows]+['END +0.17s','END +10s','END LAST'];images=list(sorted(dest.glob('FRAME_*.jpg')));assert len(images)==len(frames),(len(images),len(frames))
for offset in range(0,len(images),20):
 group=images[offset:offset+20];sheet=Image.new('RGB',(1500,190*math.ceil(len(group)/5)),(238,236,227));draw=ImageDraw.Draw(sheet)
 for j,path in enumerate(group):
  thumb=ImageOps.contain(Image.open(path).convert('RGB'),(294,166));x=(j%5)*300;y=(j//5)*190;sheet.paste(thumb,(x+(300-thumb.width)//2,y));draw.text((x+4,y+168),labels[offset+j],fill=(20,30,40))
 sheet.save(out/f'ACTUAL_RENDER_{offset+1:03d}_{offset+len(group):03d}.jpg',quality=92)
with (out/'ACTUAL_FRAME_MAP.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.writer(f);writer.writerow(['image','frame','seconds','shot']);writer.writerows((str(p),n,n/24,label) for p,n,label in zip(images,frames,labels))
with (out/'USED_MEDIA_SHA256.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.writer(f);writer.writerow(['shot','paragraph','asset','path','sha256']);writer.writerows((x['shot_id'],x['paragraph_id'],x['asset_id'],x['path'],hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()) for x in rows)
report={'status':'TECHNICAL_COMPLETE_ACTUAL_FRAME_REVIEW_PENDING','film':str(film),'sha256':hashlib.sha256(film.read_bytes()).hexdigest(),'sampled_actual_render_frames':len(images),'narrative_shots':193,'possible_black_intervals':black,'end_audio_samples':len(samples),'end_audio_peak':peak,'end_audio_rms':rms,'end_audio_silence_technical_pass':peak is not None and peak<1e-4,'full_realtime_av_review':False,'human_listening':False,'owner_approval':False}
(out/'TECHNICAL_QC.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
