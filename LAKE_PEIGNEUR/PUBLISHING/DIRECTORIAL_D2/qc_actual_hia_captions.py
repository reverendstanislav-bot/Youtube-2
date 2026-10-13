#!/usr/bin/env python3
"""Verify HIA word highlight in real MP4 frames; exclude the immutable endscreen."""
import json,pathlib,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
P=pathlib.Path(sys.argv[1]).resolve()
master=pathlib.Path(sys.argv[2]).resolve()
assert master.is_file()
cues=json.loads((P/'public/HIA_ARTHUR_CAPTIONS_LOCKED.json').read_text())
assert len(cues)>200
src=(P/'src/index.jsx').read_text()
assert 'function HiaWordCaptions({frame})' in src
assert src.count('HiaWordCaptions frame={frame}')==1
assert 'if(frame>=24211)return null' in src
assert src.count('approved_first_end_1080.png')==1
words=[w for c in cues for w in c['words']]
assert len(words)>1500
out=pathlib.Path('output/final_qc/captions');out.mkdir(parents=True,exist_ok=True)
frames=[];passes=0
for i in range(12):
 w=words[max(0,min(len(words)-1, (i*len(words)+len(words)//24)//12))]
 t=(w['s']+w['e'])/2
 path=out/('HIA_CAPTION_%02d.jpg'%(i+1))
 cmd=['ffmpeg','-nostdin','-v','error','-ss',str(round(t,3)),'-i',str(master),'-frames:v','1','-q:v','3','-y',str(path)]
 rr=subprocess.run(cmd,capture_output=True,text=True)
 assert rr.returncode==0,(t,rr.stderr[-800:])
 im=Image.open(path).convert('RGB')
 # Orange active-word pixels must appear in bottom subtitle-safe area.
 crop=im.crop((135,690,1785,1000)).resize((550,103))
 active=0
 for red,green,blue in crop.getdata():
  if red>=185 and 75<=green<=193 and blue<=150 and red>green*1.25 and green>blue*1.15:
   active+=1
 good=active>=15
 passes+=good
 frames.append({'timestamp':round(t,3),'word':w['w'],'orange_pixels_bottom_safe':active,'highlight_detected':good,'file':path.name})
page=Image.new('RGB',(3*540,4*325),'#171A1C')
draw=ImageDraw.Draw(page)
for i,x in enumerate(frames):
 px=i%3*540;py=i//3*325
 page.paste(Image.open(out/x['file']).resize((514,289)),(px+13,py+23))
 draw.text((px+13,py+5),('%.2fs  '%x['timestamp'])+x['word'],fill='#E6DDC8')
page.save(out/'CAPTIONS_ACTUAL_MP4_12_SAMPLES.jpg',quality=86)
report={'scope':'ACTUAL COMPLETED MP4: twelve Arthur-spoken samples checked for visible orange word-highlight','words':len(words),
'cues':len(cues),'actual_samples':frames,'highlight_passes':passes,'total_samples':12,
'endscreen_source_blocks_captions_after_frame':24211,
'verdict':'PASS' if passes==12 else 'HOLD: captions invisible or mismatched at one or more points'}
(out/'HIA_CAPTIONS_QC.json').write_text(json.dumps(report,indent=2)+'\n')
assert passes==12,report
print('HIA CAPTIONS ACTUAL FULL MP4: 12/12 colored word highlights PASS',len(words),'words',len(cues),'cues')
