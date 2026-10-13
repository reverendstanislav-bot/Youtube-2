#!/usr/bin/env python3
"""Burn the canonical Arthur word alignment as HIA white/orange word-following captions.
No new speech, no synthetic ASR, no subtitles in the approved end-screen.
"""
import argparse,csv,json,pathlib
p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--report',required=True)
args=p.parse_args()
P=pathlib.Path(args.project).resolve()
stage=pathlib.Path(__file__).resolve().parents[2]/'STAGE_7'
words=[]
for i in range(1,5):
 with (stage/('WORD_TIMING_V1_CHUNK_%02d.csv'%i)).open(newline='',encoding='utf-8-sig') as f:
  for r in csv.DictReader(f):
   s=float(r['start_sec']);e=float(r['end_sec']);w=r['canonical_word'].strip()
   if w and s<968.44:words.append({'w':w,'s':round(s,3),'e':round(min(e,968.44),3)})
assert len(words)>1500,len(words)
assert all(0<=v['s']<=v['e']<=968.44 for v in words)
assert all(x['s']<=y['s'] for x,y in zip(words,words[1:]))
cues=[];g=[]
def flush():
 global g
 if not g:return
 cues.append({'s':g[0]['s'],'e':g[-1]['e'],'words':g})
 g=[]
for w in words:
 if g and (len(g)>=5 or (len(g)>=3 and g[-1]['w'].endswith(('.', '?', '!'))) or (w['s']-g[-1]['e']>.62)):
  flush()
 g.append(w)
flush()
assert len(cues)>200
assert all(len(c['words'])<=5 for c in cues)
assert all(a['s']<=b['s'] for a,b in zip(cues,cues[1:]))
dest=P/'public/HIA_ARTHUR_CAPTIONS_LOCKED.json'
dest.write_text(json.dumps(cues,separators=(',',':'))+'\n')
src=P/'src/index.jsx';s=src.read_text()
assert 'HiaWordCaptions' not in s
assert 'approved_first_end_1080.png' in s
assert 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in s
assert 'function Film(){' in s
imp="import hiaCaptionCues from '../public/HIA_ARTHUR_CAPTIONS_LOCKED.json';\n"
s=imp+s
layer="""// HIA CHANNEL CANON: white base, orange single spoken word; no black card.
function HiaWordCaptions({frame}){
 if(frame>=24211)return null; // unchanged approved end screen
 const t=frame/25;
 let lo=0,hi=hiaCaptionCues.length-1,idx=-1;
 while(lo<=hi){
  const m=(lo+hi)>>1,c=hiaCaptionCues[m];
  if(t<c.s)hi=m-1;else if(t>c.e)lo=m+1;else {idx=m;break;}
 }
 if(idx<0)return null;
 const c=hiaCaptionCues[idx];
 return <div style={{
  position:'absolute',zIndex:60,left:145,right:145,bottom:135,
  textAlign:'center',fontFamily:'Arial,Helvetica,sans-serif',
  fontWeight:850,fontSize:53,lineHeight:1.16,
  WebkitTextStroke:'1.1px rgba(10,12,13,.92)',
  textShadow:'0 3px 6px rgba(0,0,0,.94),0 0 15px rgba(0,0,0,.6)',
  pointerEvents:'none'
 }}>
 {c.words.map((w,i)=><span key={i}>
  <span style={{color:(t>=w.s && t<=w.e+.03)?'#F28A3A':'#FFFFFF'}}>{w.w}</span>{i<c.words.length-1?' ':''}
 </span>)}
 </div>;
}
"""
s=s.replace('function Film(){',layer+'\nfunction Film(){',1)
needle='<Chapter'
assert needle in s,'Cannot locate actual Remotion editorial layers'
# Word captions after chapter & facts, but they stay confined to the approved lower safe area.
last='function Film(){'
fpos=s.index(last)
ep=s.find('function ',fpos+len(last))
region=s[fpos:ep if ep>=0 else len(s)]
# Place overlay with sibling and do not touch locked end-screen (caption returns null at 24211).
anchor='</AbsoluteFill>;'
# Safest insertion: prepend one component beside Chapter in live Film tree.
h='<Chapter'
assert h in region, 'No chapter component in film root; halt'
region=region.replace(h,'<HiaWordCaptions frame={frame}/>'+h,1)
s=s[:fpos]+region+s[ep if ep>=0 else len(s):]
assert s.count('HiaWordCaptions frame={frame}')==1
assert 'function HiaWordCaptions({frame})' in s
assert s.count('approved_first_end_1080.png')==1
src.write_text(s)
report={'verdict':'HIA WORD-FOLLOWING CAPTIONS INSTALLED / RENDER QC OPEN',
 'words':len(words),'caption_cues':len(cues),'speaker':'original Arthur',
 'locked_word_alignment':'STAGE_7/WORD_TIMING_V1_CHUNK_01..04.csv',
 'visual':'white + orange active word, shadow, no black rectangles',
 'bottom_safe_px':135,'stop_at_frame':24211,'no_audio_modified':True}
pathlib.Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
