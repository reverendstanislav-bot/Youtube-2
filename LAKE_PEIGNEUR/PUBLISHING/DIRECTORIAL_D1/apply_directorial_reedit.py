#!/usr/bin/env python3
"""Lake Peigneur D1: frame-locked HIA picture directorial reedit; original Arthur & endcard."""
import argparse,collections,copy,hashlib,json,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--project',required=True)
p.add_argument('--dry-run',action='store_true')
p.add_argument('--report',default=None)
args=p.parse_args()
P=pathlib.Path(args.project).resolve()
manifest=json.loads((D/'DIRECTORIAL_REEDIT_PLAN.json').read_text())
timeline=P/'public/timeline.json'; source=P/'src/index.jsx'
j=json.loads(timeline.read_text()); src=source.read_text()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
assert sha(P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')=='1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13'
assert sha(P/'public/approved_first_end_1080.png')=='b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575'
assert len(j['beats'])==87 and j['fps']==25
assert sum(len(b['slots']) for b in j['beats'])==141
assert 'const DISSOLVE_HALF=3' in src
assert 'DIRECTORIAL_D1' not in src
assert src.count('function PictureLayer(')==1 and src.count('function Picture({frame})')==1
before=collections.Counter(s['assetId'] for b in j['beats'] for s in b['slots'])
assert max(before.values())<=2
edited=copy.deepcopy(j)
changes=[]
for c in manifest['editorialReplacements']:
 b=next(b for b in edited['beats'] if b['beat']==c['beat'])
 slots=[s for s in b['slots'] if s['assetId']==c['old']]
 assert len(slots)==1,c
 s=slots[0]; name=c['asset']
 assert (P/'public/assets'/(name+'.png')).is_file(),name
 s['assetId']=name;s['file']='assets/'+name+'.png'
 s['kind']='gfx' if name.startswith('LP-GFX-') else 'reconstruction'
 s['motion']='none'
 changes.append({'beat':b['beat'],'old':c['old'],'new':name,'start':s['a'],'end':s['b'],'why':c['why']})
shots=[s for b in edited['beats'] for s in b['slots']]
assert len(shots)==141 and all(x['b']==y['a'] for x,y in zip(shots,shots[1:]))
assert shots[0]['a']==0 and shots[-1]['b']==24211
count=collections.Counter(s['assetId'] for s in shots)
assert max(count.values())<=2,count.most_common(12)
rejected={'LP-GFX-002','LP-GFX-022','LP-GFX-026','LP-REC-005','LP-REC-008','LP-REC-010','LP-REC-012','LP-REC-038','LP-REC-041'}
assert not (set(count)&rejected)
assert len(changes)==5 and len(manifest['semanticAttention'])==16 and len(manifest['microBreath'])==6
for category in ['semanticAttention','microBreath']:
 for cue in manifest[category]:
  b=next(b for b in edited['beats'] if b['beat']==cue['beat'])
  assert sum(s['assetId']==cue['asset'] for s in b['slots'])==1,cue
for cue in manifest['semanticAttention']:
 assert 1<=len(cue['points'])<=4
 assert all(8<=x<=90 and 15<=y<=82 for x,y in cue['points'])
hardcuts={int(round(t*25)) for t in manifest['hardCutSeconds']}
assert len(hardcuts)==11 and hardcuts<={s['a'] for s in shots}
# Existing R15 renderer: add beat identity without altering locked timestamps.
needle='const rawShots=timeline.beats.flatMap(b=>b.slots);'
assert src.count(needle)==1
src=src.replace(needle,'const rawShots=timeline.beats.flatMap(b=>b.slots.map(s=>({...s,beat:b.beat})));')
needle=" {assetId:'LP-REC-018',file:'assets/LP-REC-018.png',kind:'reconstruction',a:150,b:278,"
assert src.count(needle)==1
src=src.replace(needle," {beat:'LP-B001',assetId:'LP-REC-018',file:'assets/LP-REC-018.png',kind:'reconstruction',a:150,b:278,")
focus=[{'beat':x['beat'],'asset':x['asset'],'points':x['points']} for x in manifest['semanticAttention']]
breath=[{'beat':x['beat'],'asset':x['asset']} for x in manifest['microBreath']]
directors="""// DIRECTORIAL_D1: a select original image detail is clarified only where the script needs it.
const DIRECTOR_FOCUS="""+json.dumps(focus,separators=(',',':'))+""";
const DIRECTOR_BREATH="""+json.dumps(breath,separators=(',',':'))+""";
const DIRECTOR_HARD_CUTS=new Set("""+json.dumps(sorted(hardcuts))+""");
function d1Attention(slot,frame){
 const cue=DIRECTOR_FOCUS.find(x=>x.beat===slot.beat&&x.asset===slot.assetId);
 if(!cue||frame<slot.a||frame>=slot.b)return null;
 const stages=cue.points.length;
 const position=Math.min(stages-.000001,(frame-slot.a)/(slot.b-slot.a)*stages);
 const idx=Math.floor(position),phase=position-idx;
 const fadeIn=smoothed(Math.min(1,phase/.17));
 const fadeOut=smoothed(Math.min(1,(1-phase)/.17));
 const edge=smoothed(Math.min(1,(frame-slot.a)/9))*smoothed(Math.min(1,(slot.b-1-frame)/9));
 return {x:cue.points[idx][0],y:cue.points[idx][1],opacity:Math.max(0,Math.min(1,fadeIn*fadeOut*edge))};
}
function d1Breath(slot,frame){
 if(!DIRECTOR_BREATH.some(x=>x.beat===slot.beat&&x.asset===slot.assetId))return 1;
 const t=Math.max(0,Math.min(1,(frame-slot.a)/(slot.b-slot.a)));
 return 1+0.0036*smoothed(t);
}
"""
at=src.index('const pictureGroups=makeGroups(pictureShots);')
src=src[:at]+directors+src[at:]
start=src.index('function PictureLayer(')
end=src.index('function groupAt(f){',start)
layer=r"""function PictureLayer({slot,opacity=1,frame=0}){
 const contain=slot.kind==='gfx'||slot.kind==='document'||slot.kind==='map'||slot.kind==='real_context';
 const focus=d1Attention(slot,frame),scale=d1Breath(slot,frame);
 const imStyle={position:'absolute',inset:0,width:'100%',height:'100%',
                objectFit:contain?'contain':'cover',objectPosition:'center',
                transform:scale===1?undefined:'scale('+scale+')',transformOrigin:'50% 50%'};
 const mask=focus?'radial-gradient(ellipse 32% 35% at '+focus.x+'% '+focus.y+'%,black 0%,rgba(0,0,0,.99) 36%,transparent 100%)':null;
 return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden',opacity}}>
  <Img src={staticFile(slot.file)} style={{
   ...imStyle,filter:focus?'brightness(.89) saturate(.965)':undefined
  }}/>
  {focus&&<Img src={staticFile(slot.file)} style={{
   ...imStyle,opacity:focus.opacity,filter:'brightness(1.065) contrast(1.035)',
   maskImage:mask,WebkitMaskImage:mask
  }}/>}
 </AbsoluteFill>;
}
"""
src=src[:start]+layer+src[end:]
start=src.index('function Picture({frame}){')
end=src.index('function Chapter({frame})',start)
picture=r"""function Picture({frame}){
 const f=frame,idx=groupAt(f),curr=pictureGroups[idx];
 const p=idx>0?pictureGroups[idx-1]:null;
 const n=idx+1<pictureGroups.length?pictureGroups[idx+1]:null;
 // Eleven hard cuts reserved for crisis/actions; other changes keep Chicago 6-frame dissolves.
 if(n&&!DIRECTOR_HARD_CUTS.has(curr.b)&&f>=curr.b-DISSOLVE_HALF){
  const alpha=smoothed((f-(curr.b-DISSOLVE_HALF))/(2*DISSOLVE_HALF-1));
  return <AbsoluteFill style={{background:C.charcoal}}>
   <PictureLayer slot={curr} frame={f}/>
   <PictureLayer slot={n} frame={f} opacity={alpha}/>
  </AbsoluteFill>;
 }
 if(p&&!DIRECTOR_HARD_CUTS.has(curr.a)&&f<curr.a+DISSOLVE_HALF){
  const alpha=smoothed((f-(curr.a-DISSOLVE_HALF))/(2*DISSOLVE_HALF-1));
  return <AbsoluteFill style={{background:C.charcoal}}>
   <PictureLayer slot={p} frame={f}/>
   <PictureLayer slot={curr} frame={f} opacity={alpha}/>
  </AbsoluteFill>;
 }
 return <PictureLayer slot={curr} frame={f}/>;
}
"""
src=src[:start]+picture+src[end:]
assert src.count('function PictureLayer(')==1 and src.count('function Picture({frame})')==1
assert src.count('const DIRECTOR_FOCUS=')==1 and src.count('const DIRECTOR_BREATH=')==1
assert 'opacity={1-alpha}' not in src
assert src.count('approved_first_end_1080.png')==1
assert src.count('LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')==2
assert not any(x in src for x in ('V4Picture','V4Overlay','V7Retention','v7Motion','<Caption'))
report={'status':'D1 DIRECTORIAL SOURCE PREFLIGHT PASS; OWNER EDITORIAL REVIEW OPEN',
 'beats':87,'slots':141,'full_frames':24711,'audio_and_endscreen_unchanged':True,
 'asset_swaps':changes,'semantic_detail_emphasis':focus,
 'hero_breath':breath,'hard_cut_frames':sorted(hardcuts),
 'max_source_reuse':max(count.values()),'no_new_assets':True,
 'original_arthur_sha256':sha(P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3'),
 'original_endscreen_sha256':sha(P/'public/approved_first_end_1080.png')}
print(json.dumps({'status':report['status'],'replacements':len(changes),'semantic_cues':len(focus),
                 'breath_cues':len(breath),'hardcuts':len(hardcuts),
                 'max_source_reuse':max(count.values())},indent=2),flush=True)
if args.report:pathlib.Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
if args.dry_run:raise SystemExit(0)
shutil.copy2(timeline,P/'public/timeline_BEFORE_DIRECTORIAL_D1.json')
shutil.copy2(source,P/'src/index_BEFORE_DIRECTORIAL_D1.jsx')
timeline.write_text(json.dumps(edited,indent=2)+'\n')
source.write_text(src)
