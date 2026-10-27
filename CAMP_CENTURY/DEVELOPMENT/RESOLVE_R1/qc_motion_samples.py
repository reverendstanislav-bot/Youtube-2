"""Three-point visual evidence from actual rendered motion treatments."""
from pathlib import Path
import json,subprocess,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
src=Path(sys.argv[1]);folder=ROOT/'QC'/'motion';folder.mkdir(parents=True,exist_ok=True)
plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
chosen=[]
for asset in ['M01','M03','M06','M08','M09','M11','M12','R07']:
    shots=[s for s in plan if s['asset_id']==asset]
    if shots:chosen.append(max(shots,key=lambda s:s['duration_frames']))
records=[]
for s in chosen:
    strip=Image.new('RGB',(1440,292),'#f0eeeb');draw=ImageDraw.Draw(strip)
    at=[]
    for j,fraction in enumerate([.08,.50,.92]):
        sec=(s['start_frame']+s['duration_frames']*fraction)/25
        dest=folder/f"{s['shot_id']}_{j}.jpg"
        subprocess.run(['ffmpeg','-hide_banner','-v','error','-threads','1','-y','-ss',str(sec),'-i',str(src),'-frames:v','1','-vf','scale=480:270',str(dest)],check=True)
        draw.text((j*480+5,3),f"{s['shot_id']} {s['asset_id']} {sec:.2f}s",fill='#15242d')
        strip.paste(Image.open(dest),(j*480,22));at.append(sec)
    out=folder/f"{s['asset_id']}_RENDERED_SEQUENCE.jpg";strip.save(out,quality=94)
    records.append(dict(shot=s['shot_id'],asset=s['asset_id'],sample_seconds=at,strip=str(out),review_scope='Three-point rendered sequence, not a claim of continuous playback review'))
(ROOT/'QC'/'MOTION_SAMPLE_INDEX.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('RENDERED_MOTION_STRIPS',len(records),flush=True)
