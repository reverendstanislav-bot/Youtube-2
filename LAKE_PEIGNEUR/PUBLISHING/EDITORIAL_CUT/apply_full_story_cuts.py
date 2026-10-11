#!/usr/bin/env python3
"""Implement ONLY individually justified Arthur word-level scene cuts from Git source of truth."""
import argparse,collections,csv,hashlib,json,pathlib,re,shutil
D=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--project',required=True)
parser.add_argument('--dry-run',action='store_true')
parser.add_argument('--report',default=None)
args=parser.parse_args()
P=pathlib.Path(args.project).resolve()
timeline=P/'public/timeline.json'
srcfile=P/'src/index.jsx'
m=json.loads((P/'public/v4_accents.json').read_text())
plan=json.loads((D/'FULL_STORY_SOURCE_CUT_PLAN.json').read_text())
j=json.loads(timeline.read_text())
src=srcfile.read_text()
assert len(j['beats'])==87 and sum(len(x['slots']) for x in j['beats'])==106
assert len(plan['cuts'])==23,('Expected 23 actual additional edit decisions',len(plan['cuts']))
assert 'V4Picture' not in src and 'V4Overlay' not in src and 'V7Retention' not in src
assert 'approved_first_end_1080.png' in src and 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in src
rejected={'LP-GFX-002','LP-GFX-022','LP-GFX-026','LP-REC-005','LP-REC-008','LP-REC-010','LP-REC-012','LP-REC-038','LP-REC-041'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for z in iter(lambda:f.read(1048576),b''):h.update(z)
 return h.hexdigest()
assert sha(P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')=='1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13'
assert sha(P/'public/approved_first_end_1080.png')=='b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575'
# EXACT canonical word-start match from all four original Stage 7 timing CSV chunks
base=D.parents[1]/'STAGE_7'
words=[]
for i in range(1,5):
 fn=base/f'WORD_TIMING_V1_CHUNK_0{i}.csv'
 assert fn.is_file(),fn
 with fn.open(newline='',encoding='utf-8-sig') as f:
  words.extend(list(csv.DictReader(f)))
def norm(w): return re.sub('[^a-z0-9]','',w.lower())
def aligned(c,beat):
 terms=[norm(w) for w in c['spoken'].split() if norm(w)]
 assert len(terms)>=2,c
 seq=[norm(w['canonical_word']) for w in words]
 found=[]
 for k in range(len(seq)-len(terms)+1):
  if seq[k:k+len(terms)]!=terms:continue
  t=float(words[k]['start_sec'])
  if beat['a']/25<=t<beat['b']/25:
   found.append(t)
 assert len(found)==1,(c['beat'],c['spoken'],found)
 delta=abs(found[0]-c['frame']/25)
 assert delta<=.055,(c['beat'],c['spoken'],found[0],c['frame']/25,delta)
 return found[0]
before_slot_total=sum(len(x['slots']) for x in j['beats'])
add_counts=collections.Counter()
full_cues=[]
for cut in plan['cuts']:
 beat=next((b for b in j['beats'] if b['beat']==cut['beat']),None)
 assert beat is not None,cut
 assert len(beat['slots'])==1,(cut['beat'],'Cannot split multishot beat without a shot-by-shot review')
 old=beat['slots'][0]
 frame=cut['frame']
 assert old['a']+45<frame<old['b']-45,(beat['beat'],frame,old['a'],old['b'])
 assert cut['asset']!=old['assetId'] and cut['asset'] not in rejected,cut
 source=P/'public/assets'/(cut['asset']+'.png')
 assert source.is_file(),cut['asset']
 alignment=aligned(cut,beat)
 kind='gfx' if cut['asset'].startswith('LP-GFX-') else ('real_context' if cut['asset'].startswith('LP-PD-') else 'reconstruction')
 first=dict(old)
 first.update(b=frame,e=frame/25,motion='none')
 second=dict(old)
 second.update(assetId=cut['asset'],file='assets/'+cut['asset']+'.png',kind=kind,
               a=frame,b=old['b'],s=frame/25,e=old['b']/25,motion='none')
 beat['slots']=[first,second]
 add_counts[cut['asset']]+=1
 full_cues.append({'beat':cut['beat'],'original':old['assetId'],'inserted':cut['asset'],'frame':frame,
                   'at':round(frame/25,3),'word_start':alignment,'narration_phrase':cut['spoken']})
original_count=collections.Counter(x['asset_id'] for x in m['items'])
# +7 original preview cut-ins are already in timeline but omitted by the 100-row V4 accent map
early=json.loads((D/'FIRST_180S_SCRIPT_LOCK.json').read_text())
for c in early['changes']:
 for seg in c['segments']:
  if seg['asset']!=c['replace_original']:original_count[seg['asset']]+=1
original_count.update(add_counts)
assert max(original_count.values())<=2,original_count.most_common(10)
assert len(add_counts)==23 and sum(add_counts.values())==23
assert sum(len(x['slots']) for x in j['beats'])==129
assert len([b for b in j['beats'] if b['a']>=24211])==0
assert not any(s['assetId'] in rejected for b in j['beats'] for s in b['slots'])
report={'verdict':'FULL STORY EDIT PREFLIGHT PASS. EDITORIAL AND OWNER VISUAL APPROVAL OPEN.',
 'locked_canonical_beats':87,
 'original_picture_slots':99,
 'first_180s_source_cuts':7,
 'rest_of_film_source_cuts':23,
 'total_new_meaningful_source_cuts':30,
 'physical_picture_slots_after_reedit':129,
 'including_special_opening_exposure':130,
 'source_max_reuse':max(original_count.values()),
 'script_and_arthur_audio':'UNCHANGED',
 'original_chicago_r15_endscreen':'UNCHANGED',
 'no_v4_v7_zoom_or_highlight_effects':True,
 'word_level_source':'STAGE_7/WORD_TIMING_V1_CHUNK_01..04.csv',
 'timestamped_cuts':full_cues}
print(json.dumps(report,indent=2))
if args.report:pathlib.Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
if args.dry_run:raise SystemExit(0)
shutil.copy2(timeline,P/'public/timeline_FIRST3_BEFORE_FULL_EDIT.json')
timeline.write_text(json.dumps(j,indent=2)+'\n')
