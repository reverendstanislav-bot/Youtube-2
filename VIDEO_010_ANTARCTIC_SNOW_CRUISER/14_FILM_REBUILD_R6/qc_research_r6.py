from pathlib import Path
import json,subprocess,re,hashlib
from PIL import Image,ImageDraw
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');F=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3\RENDERS\VIDEO010_R6_RESEARCH_RIGHTS_HOLD.mp4');Q=D/'QC_COMPLETE_R6';Q.mkdir(exist_ok=True);frames=Q/'FRAMES';frames.mkdir(exist_ok=True);m=json.loads((D/'R6_1_MANIFEST.json').read_text());samples=[(r['shot_id'],r['s']+(r['e']-r['s'])//2) for r in m['shots']]+[('END_SCREEN',21070)]
def balanced(terms):
 if len(terms)==1:return terms[0]
 n=len(terms)//2;return '('+balanced(terms[:n])+'+'+balanced(terms[n:])+')'
expr=balanced([f'eq(n\\,{n})' for sid,n in samples]);log=Q/'DECODE_BLACK_LOUDNESS.log';args=['ffmpeg','-hide_banner','-loglevel','info','-i',str(F),'-map','0:v:0','-vf','blackdetect=d=0.1:pix_th=0.02,select='+expr+',scale=320:180','-fps_mode','vfr','-q:v','3','-an','-y',str(frames/'%03d.jpg'),'-map','0:a:0','-af','ebur128=peak=true','-vn','-f','null','-']
with log.open('w') as out:p=subprocess.run(args,stdout=out,stderr=subprocess.STDOUT)
assert p.returncode==0,log.read_text(errors='replace')[-2000:];images=sorted(frames.glob('*.jpg'));assert len(images)==len(samples),(len(images),len(samples))
for start in range(0,len(images),42):
 group=images[start:start+42];sheet=Image.new('RGB',(1920,1400),'#151515');dr=ImageDraw.Draw(sheet)
 for j,f in enumerate(group):
  im=Image.open(f);x=j%6*320;y=j//6*200;sheet.paste(im,(x,y));sid,n=samples[start+j];dr.text((x+4,y+181),sid+' / '+str(round(n/24,2))+'s',fill='white')
 sheet.save(Q/f'SEQUENCE_{start//42+1:02}.jpg')
h=log.read_text(errors='replace');integrated=re.findall(r'I:\s*(-?[\d.]+) LUFS',h);peaks=re.findall(r'Peak:\s*(-?[\d.]+) dBFS',h);black=re.findall(r'black_start:([^\r\n]+)',h);report={'status':'SAMPLED_SEQUENCE_AND_METRICS_ONLY_FULL_AV_HOLD','sampled_frames':len(images),'integrated_lufs':float(integrated[-1]) if integrated else None,'true_peak_dbfs':float(peaks[-1]) if peaks else None,'black_events':black,'visual_contact_sheets_generated':True,'full_real_time_av_review':'HOLD','human_listening':'HOLD','archive_rights':'HOLD_RESEARCH_ONLY'};(Q/'SEQUENCE_METRICS.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
