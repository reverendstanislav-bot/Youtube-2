#!/usr/bin/env python3
"""Sample the ACTUAL completed long MP4 at all 16 authored semantic focus scenes and six hero micro-motions."""
import json,os,pathlib,subprocess,sys,hashlib
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageStat
root=pathlib.Path('.').resolve()
project=pathlib.Path(sys.argv[1]).resolve()
master=pathlib.Path(sys.argv[2]).resolve()
plan=json.loads((root/'LAKE_PEIGNEUR/PUBLISHING/DIRECTORIAL_D1/DIRECTORIAL_REEDIT_PLAN.json').read_text())
for cue in plan['semanticAttention']:
 if cue['beat']=='LP-B048' and cue['asset']=='LP-GFX-036':cue['asset']='LP-GFX-038'
 if cue['beat']=='LP-B052' and cue['asset']=='LP-GFX-036':cue['asset']='LP-GFX-037'

timeline=json.loads((project/'public/timeline.json').read_text())
out=root/'output/final_qc/directorial'
out.mkdir(parents=True,exist_ok=True)
def shot(beat,asset):
 b=next(x for x in timeline['beats'] if x['beat']==beat)
 a=[s for s in b['slots'] if s['assetId']==asset]
 assert len(a)==1,(beat,asset)
 return a[0]
def extract(frame,name):
 sec=frame/25
 path=out/(name+'.jpg')
 proc=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(sec),'-i',str(master),
        '-frames:v','1','-vf','scale=640:360','-q:v','3','-y',str(path)],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 assert proc.returncode==0,(frame,proc.stderr.decode()[-700:])
 assert path.stat().st_size>1000
 return path
samples=[]
for i,cue in enumerate(plan['semanticAttention']):
 s=shot(cue['beat'],cue['asset'])
 n=len(cue['points'])
 for j in range(n):
  target=round(s['a']+(j+.5)*(s['b']-s['a'])/n)
  # This is inside the chosen source shot and at the middle of its own cue stage.
  assert s['a']+5<target<s['b']-5,(cue,target,s)
  img=extract(target,'F%02d_STEP%d'%(i+1,j+1))
  samples.append({'kind':'semantic','beat':cue['beat'],'asset':cue['asset'],'scene':i+1,'step':j+1,
                  'frame':target,'at_sec':round(target/25,2),'file':img.name,'why':cue['why']})
breaths=[]
for i,cue in enumerate(plan['microBreath']):
 s=shot(cue['beat'],cue['asset'])
 a=round(s['a']+.25*(s['b']-s['a']));b=round(s['a']+.75*(s['b']-s['a']))
 assert s['a']<a<b<s['b']
 x=extract(a,'B%02d_EARLY'%(i+1))
 y=extract(b,'B%02d_LATE'%(i+1))
 ix=Image.open(x).convert('RGB')
 iy=Image.open(y).convert('RGB')
 diff=ImageStat.Stat(ImageChops.difference(ix,iy)).mean
 breaths.append({'beat':cue['beat'],'asset':cue['asset'],'early_frame':a,'late_frame':b,
                 'early_image':x.name,'late_image':y.name,
                 'mean_channel_pixel_difference':round(sum(diff)/len(diff),4)})
# One contact sheet per <=12 screenshots. Never upscale individual source thumbnails.
for base in range(0,len(samples),12):
 items=samples[base:base+12]
 page=Image.new('RGB',(3*658,4*407),'#171A1C')
 draw=ImageDraw.Draw(page)
 for j,x in enumerate(items):
  left=(j%3)*658;top=(j//3)*407
  im=Image.open(out/x['file']).convert('RGB')
  page.paste(im,(left+7,top+26))
  draw.text((left+7,top+5),str(x['at_sec'])+'s | '+x['beat']+' '+x['asset']+' detail '+str(x['step']),fill='#F3EBDD')
 page.save(out/('D2_SEMANTIC_FOCUS_SHEET_%02d.jpg'%(base//12+1)),quality=86)
report={'scope':'Actual original-quality completed HIA D1 full master: all intentional authored semantic picture cues sampled',
        'semantic_story_cues':len(plan['semanticAttention']),
        'actual_semantic_frames_sampled':len(samples),'hero_micro_breath_cues':len(breaths),
        'hero_timing_pairs':breaths,
        'source_no_new_images':True,'individual_cues':samples,
        'notes':'Actual rendered frame evidence only. Cannot automatically certify creative quality, archive authenticity, or causal clarity.'}
(out/'D2_ACTUAL_ACCENT_QC.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'semantic_cues':report['semantic_story_cues'],
                 'actual_frames':report['actual_semantic_frames_sampled'],
                 'micro_breath_pairs':len(breaths),
                 'output':str(out)},indent=2),flush=True)
