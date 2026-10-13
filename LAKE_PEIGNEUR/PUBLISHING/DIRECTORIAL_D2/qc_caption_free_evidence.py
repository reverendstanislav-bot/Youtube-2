#!/usr/bin/env python3
"""Owner No-Subtitles lock: produce visual evidence from actual final MP4.
No OCR or visual-only false PASS; source checks are mandatory.
"""
import json,pathlib,subprocess,sys
from PIL import Image,ImageDraw
P=pathlib.Path(sys.argv[1]).resolve()
f=pathlib.Path(sys.argv[2]).resolve()
s=(P/'src/index.jsx').read_text()
assert 'HiaWordCaptions' not in s and '<Caption' not in s and '<Subtitle' not in s
assert not (P/'public/HIA_ARTHUR_CAPTIONS_LOCKED.json').exists()
assert f.exists() and f.stat().st_size>100000000
out=pathlib.Path('output/final_qc/no_subtitles')
out.mkdir(parents=True,exist_ok=True)
times=[3.62,76.52,158.42,238.84,313.10,392.31,474.54,557.13,633.02,714.32,795.585,879.92,965.00,975.00]
data=[]
sheet=Image.new('RGB',(3*540,5*325),'#171A1C')
draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 p=out/('NO_CAPTION_ACTUAL_%02d.jpg'%(i+1))
 r=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(f),'-frames:v','1','-q:v','3','-y',str(p)],capture_output=True,text=True)
 assert r.returncode==0,(t,r.stderr[-1000:])
 image=Image.open(p).convert('RGB').resize((514,289))
 x=i%3*540+13;y=i//3*325+23
 sheet.paste(image,(x,y))
 draw.text((x,y-18),'%.3fs  SOURCE-NO-CAPTIONS'%t,fill='#E6DDC8')
 data.append({'sec':t,'image':p.name})
sheet.save(out/'NO_CAPTIONS_ACTUAL_MASTER_SHEET.jpg',quality=90)
report={'verdict':'CAPTION LAYER ABSENT FROM SOURCE; 14 ACTUAL VIDEO FRAMES PROVIDED FOR INDEPENDENT VISUAL REVIEW',
 'owner_lock':'CHANNEL/NO_SUBTITLES_OWNER_LOCK_2026-10-10.md',
 'source_caption_overlay_absent':True,'caption_cue_file_absent':True,
 'sampled_actual_movie_frames':len(data),'samples':data,
 'human_visual_review':'PENDING'}
(out/'NO_CAPTIONS_QC.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2))
