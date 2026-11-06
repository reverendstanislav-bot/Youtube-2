"""Independent readback of the actual R2 media; does not regenerate or edit sources."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from collections import defaultdict
import csv,json,subprocess,hashlib,sys
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT.parent;PREP=PROJECT/'EDIT_PREP_R2'
QC=ROOT/'QC';QC.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((PREP/'EDIT_TIMELINE.csv').open(encoding='utf-8-sig')))
reg=json.loads((PREP/'ASSET_REGISTER.json').read_text(encoding='utf-8-sig'))
vid=[r for r in rows if r['visual_type']=='VIDEO']
def extract(job):
    i,shot,sample,fraction=job
    start=float(shot['source_in_seconds']);end=float(shot['source_out_seconds'])
    t=start+.08 if fraction==0 else end-.10 if fraction==1 else (start+end)/2
    target=QC/f'{shot["shot_id"]}_{sample}.jpg'
    p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',shot['asset_local'],'-frames:v','1','-q:v','2','-y',str(target)],capture_output=True)
    return {'shot_id':shot['shot_id'],'asset_id':shot['asset_id'],'source_time':round(t,6),'sample':sample,'path':str(target),'status':'PASS_EXTRACT' if p.returncode==0 and target.exists() else p.stderr.decode(errors='replace')[:200]}
jobs=[(i,s,n,f) for i,s in enumerate(vid) for n,f in [('start',0),('mid',.5),('end',1)]]
results=[]
with ThreadPoolExecutor(max_workers=4) as pool:
    for x in as_completed([pool.submit(extract,j) for j in jobs]):results.append(x.result())
(ROOT/'EXACT_FRAME_SAMPLES.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for page in range(3):
    group=vid[page*9:(page+1)*9];sheet=Image.new('RGB',(1110,len(group)*235),(25,25,25));draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(group):
        for j,sample in enumerate(['start','mid','end']):
            info=next(a for a in results if a['shot_id']==s['shot_id'] and a['sample']==sample)
            p=Path(info['path'])
            if not p.exists():continue
            im=Image.open(p).convert('RGB');im.thumbnail((366,205));x=j*370;y=i*235;sheet.paste(im,(x+(370-im.width)//2,y+27))
            draw.text((x+4,y+3),f'{s["shot_id"]} {s["asset_id"]} {sample} src {info["source_time"]:.3f}',fill='white')
    sheet.save(QC/f'VIDEO_CONTACT_{page+1:02d}.jpg',quality=92)
print(json.dumps({'selected_clips':len(vid),'exact_source_samples':len(results),'failed_samples':[r for r in results if r['status']!='PASS_EXTRACT'],'sheets':3},ensure_ascii=False))
