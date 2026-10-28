from pathlib import Path
import json,subprocess,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;src=Path(sys.argv[1]);q=ROOT/'QC/motion';q.mkdir(parents=True,exist_ok=True)
p=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text());records=[]
for s in p:
    if s['kind']!='EXISTING_REFERENCE_MOTION':continue
    times=[(s['start_frame']+s['duration_frames']*f)/25 for f in [.02,.25,.50,.85]]
    sheet=Image.new('RGB',(1600,246),'#eeefed');draw=ImageDraw.Draw(sheet)
    for j,at in enumerate(times):
        file=q/f"{s['shot_id']}_{j}.jpg";subprocess.run(['ffmpeg','-v','error','-y','-ss',str(at),'-i',str(src),'-frames:v','1','-vf','scale=400:225',str(file)],check=True)
        draw.text((j*400+3,2),s['shot_id']+' '+s['asset_id']+' '+str(round(at,2)),fill='#14232a');sheet.paste(Image.open(file),(j*400,20))
    dest=q/f"{s['shot_id']}_{s['asset_id']}_RENDERED_SEQUENCE.jpg";sheet.save(dest,quality=95)
    records.append(dict(shot=s['shot_id'],motion=s['asset_id'],source=s['path'],rendered_times=times,sequence=str(dest),scope='Four-point samples from actual full Resolve render, not continuous real-time AV review'))
(ROOT/'QC/MOTION_SAMPLE_INDEX.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('R3_ACTUAL_MOTION_SEQUENCES',len(records),flush=True)
