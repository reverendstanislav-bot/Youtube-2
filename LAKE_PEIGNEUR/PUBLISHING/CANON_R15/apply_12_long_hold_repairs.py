#!/usr/bin/env python3
"""Perform the 12 already identified long-hold repairs ONCE, on the locked 129-slot timeline."""
import argparse,collections,csv,hashlib,json,pathlib,re,shutil
D=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--project',required=True)
p.add_argument('--dry-run',action='store_true')
p.add_argument('--report',default=None)
args=p.parse_args()
P=pathlib.Path(args.project).resolve()
timeline=P/'public/timeline.json'
j=json.loads(timeline.read_text())
plan=json.loads((D/'LONG_HOLD_REPAIR_12.json').read_text())
assert j['fps']==25 and len(j['beats'])==87
assert sum(len(b['slots']) for b in j['beats'])==129
assert len(plan['cuts'])==12
all_old=[s for b in j['beats'] for s in b['slots']]
assert all(x['b']==y['a'] for x,y in zip(all_old,all_old[1:]))
assert all_old[0]['a']==0 and all_old[-1]['b']==24211
src=(P/'src/index.jsx').read_text()
assert 'approved_first_end_1080.png' in src and 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in src
assert 'DISSOLVE_HALF=3' not in src, 'Canonical Remotion compositing must run AFTER these 12 source edits'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for part in iter(lambda:f.read(1048576),b''):h.update(part)
 return h.hexdigest()
assert sha(P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')==plan['hard_limits']['preserve_arthur_sha256']
assert sha(P/'public/approved_first_end_1080.png')==plan['hard_limits']['preserve_endscreen_sha256']
rows=[]
stage=D.parents[1]/'STAGE_7'
for i in range(1,5):
 with (stage/f'WORD_TIMING_V1_CHUNK_0{i}.csv').open(newline='',encoding='utf-8-sig') as f:
  rows.extend(list(csv.DictReader(f)))
def norm(w):return re.sub('[^a-z0-9]','',w.lower())
seq=[norm(r['canonical_word']) for r in rows]
def get_frame(phrase,lo,hi):
 words=[norm(t) for t in phrase.split() if norm(t)]
 found=[]
 for k in range(len(seq)-len(words)+1):
  if seq[k:k+len(words)]==words:
   t=float(rows[k]['start_sec'])
   if lo/25<t<hi/25:found.append(t)
 assert len(found)==1,(phrase,found,lo,hi)
 return round(found[0]*25),found[0]
exposures=collections.Counter(s['assetId'] for s in all_old)
assert max(exposures.values())<=2,exposures.most_common(8)
rejected={'LP-GFX-002','LP-GFX-022','LP-GFX-026','LP-REC-005','LP-REC-008','LP-REC-010','LP-REC-012','LP-REC-038','LP-REC-041'}
result=[]
for cut in plan['cuts']:
 beat=next((b for b in j['beats'] if b['beat']==cut['beat']),None)
 assert beat and len(beat['slots'])==1,cut
 old=beat['slots'][0]
 assert old['assetId']==cut['old'],(cut['beat'],old['assetId'],cut['old'])
 assert cut['new'] not in rejected and cut['new']!=cut['old']
 assert (P/'public/assets'/(cut['new']+'.png')).is_file(),cut['new']
 frame,t=get_frame(cut['phrase'],old['a'],old['b'])
 assert old['a']+65<=frame<=old['b']-60,(cut['beat'],old['a'],frame,old['b'])
 first=dict(old);second=dict(old)
 first.update(b=frame,e=frame/25,motion='none')
 second.update(a=frame,s=frame/25,motion='none')
 mode=cut.get('mode','replace_second')
 fresh_asset=cut['new']
 if mode=='replace_second':
  second.update(assetId=fresh_asset,file='assets/'+fresh_asset+'.png',kind='gfx')
 elif mode=='replace_first':
  first.update(assetId=fresh_asset,file='assets/'+fresh_asset+'.png',kind='gfx')
 else:raise AssertionError(mode)
 assert exposures[fresh_asset]<2,(cut['beat'],fresh_asset,exposures[fresh_asset])
 exposures[fresh_asset]+=1
 beat['slots']=[first,second]
 result.append({'beat':cut['beat'],'old':cut['old'],'added':fresh_asset,'cut_frame':frame,'second':round(frame/25,3),
                'arthur_word_time':t,'original_hold_seconds':round((old['b']-old['a'])/25,2),
                'new_segments_seconds':[round((frame-old['a'])/25,2),round((old['b']-frame)/25,2)],
                'spoken_onset':cut['phrase'],'why':cut['why'],'mode':mode})
all_new=[s for b in j['beats'] for s in b['slots']]
actual=collections.Counter(s['assetId'] for s in all_new)
assert len(all_new)==141
assert max(actual.values())<=2,actual.most_common(8)
assert all(x['b']==y['a'] for x,y in zip(all_new,all_new[1:]))
assert all(x['a']<x['b'] for x in all_new)
assert all(x['assetId'] not in rejected for x in all_new)
assert all(r['new_segments_seconds'][0]<=12 and r['new_segments_seconds'][1]<=12 for r in result)
assert all((r['new_segments_seconds'][0]>=2.6 and r['new_segments_seconds'][1]>=2.4) for r in result)
assert all(r['beat'] in [b['beat'] for b in j['beats']] for r in result)
assert (all_old[0]['a'],all_old[-1]['b'])==(all_new[0]['a'],all_new[-1]['b'])
qc={'verdict':'12 ORIGINAL LONG-HOLD EDITS LOCKED, FRAME-EXACT',
    'new_assets_created':0,'new_asset_jobs':0,'new_script_audio':0,
    'story_beats':87,'original_picture_slots':129,'repaired_picture_slots':141,
    'previously_over12sec_hold_count':12,'repaired_too_long_count':0,
    'source_max_reuse':max(actual.values()),
    'original_arthur_sha256':sha(P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3'),
    'approved_endscreen_sha256':sha(P/'public/approved_first_end_1080.png'),
    'cuts':result}
print(json.dumps(qc,indent=2))
if args.report:pathlib.Path(args.report).write_text(json.dumps(qc,indent=2)+'\n')
if args.dry_run:raise SystemExit(0)
shutil.copy2(timeline,P/'public/timeline_BEFORE_12_HOLD_FIX.json')
timeline.write_text(json.dumps(j,indent=2)+'\n')
