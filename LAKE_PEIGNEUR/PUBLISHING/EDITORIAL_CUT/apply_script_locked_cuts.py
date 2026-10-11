#!/usr/bin/env python3
"""Cut current approved timeline against exact Arthur beat-map. No invented keyframes."""
import argparse,collections,copy,hashlib,json,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--project',required=True)
parser.add_argument('--dry-run',action='store_true')
parser.add_argument('--report',default=None)
args=parser.parse_args()
P=pathlib.Path(args.project).resolve()
index=P/'src/index.jsx'
timeline=P/'public/timeline.json'
maps=P/'public/v4_accents.json'
facts=P/'public/facts.json'
voice=P/'public/LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3'
screen=P/'public/approved_first_end_1080.png'
plan=json.loads((D/'FIRST_180S_SCRIPT_LOCK.json').read_text())
m=json.loads(maps.read_text())
j=json.loads(timeline.read_text())
src=index.read_text()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert sha(voice)=='1ae5c97d85b9cf2c10c438a2834d024776ea851a932a02aab2490860fa4afd13','Arthur master drift'
assert sha(screen)=='b794e5582699e90812b25208ca1c5dd053df465825d1ce6e33a7a0c6ea53b575','Chicago R15 end screen drift'
assert j['fps']==25 and len(j['beats'])==87
assert sum(len(x['slots']) for x in j['beats'])==99
assert len(m['items'])==100 and sum(x['effect'] not in ('HOLD','QC_HOLD') for x in m['items'])==36
assert plan['film_fps']==25 and len(plan['changes'])==6
assert 'V7Retention' not in src and 'V8Cutaways' not in src
assert '<Caption' not in src and 'approved_first_end_1080.png' in src
assert 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in src
base_counts=collections.Counter(x['asset_id'] for x in m['items'])
used_extra=collections.Counter()
before_lengths={}
for change in plan['changes']:
 beat=next((x for x in j['beats'] if x['beat']==change['beat']),None)
 assert beat is not None,change['beat']
 assert len(beat['slots'])==1,(change['beat'],'Existing paired shots must not be scrambled')
 original=beat['slots'][0]
 assert original['assetId']==change['replace_original'],(change['beat'],original['assetId'],change['replace_original'])
 segs=change['segments']
 assert segs[0]['from']==original['a'] and segs[-1]['to']==original['b']
 for a,b in zip(segs,segs[1:]):assert a['to']==b['from'],change['beat']
 for segment in segs:
  assert segment['from']<segment['to']
  a=segment['asset']
  assert (P/'public/assets'/(a+'.png')).is_file(),a
  assert segment['kind'] in ('gfx','real_context','reconstruction')
  assert len(segment['spoken'])>15 and len(segment['editorial'])>15
  if a!=original['assetId']:used_extra[a]+=1
 beat['slots']=[{**original,'assetId':z['asset'],'file':'assets/'+z['asset']+'.png',
                 'kind':z['kind'],'a':z['from'],'b':z['to'],
                 's':z['from']/25,'e':z['to']/25,'motion':'none'} for z in segs]
 before_lengths[change['beat']]=len(segs)
base_counts.update(used_extra)
assert max(base_counts.values())<=2,base_counts.most_common(8)
assert len(used_extra)==7 and sum(used_extra.values())==7,used_extra
assert len(j['beats'])==87 and sum(len(b['slots']) for b in j['beats'])==106
assert 968.40 < j['duration'] < 968.46
# Remove all technical/decorative accents and leave native V3 18-frame shot dissolves, Chapter/Fact and unchanged audio/endscreen.
old='<V4Picture frame={frame}>{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}</V4Picture><V4Overlay frame={frame}/><Chapter'
replacement='{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}<Chapter'
assert src.count(old)==1,'Unrecognized source; refusing to render with leftover zoom/spotlight'
src=src.replace(old,replacement)
prefix='import {V4Picture,V4Overlay} from "./AccentV4";\n'
assert src.count(prefix)==1
src=src.replace(prefix,'')
assert not any(x in src for x in ['V4Picture','V4Overlay','V7Retention','V7Focus','V8Cutaways','v7Motion']), 'Decorative effects still enabled'
assert src.count('<Audio src={staticFile(\'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3\')}/>')==2
assert src.count('approved_first_end_1080.png')==1
report={'status':'EDITORIAL SCRIPT-LINKED PREVIEW PREFLIGHT, NOT FULL FILM PASS',
        'number_of_new_editorial_cuts':7,
        'beats':len(j['beats']),'original_slots':99,'new_slots':106,
        'full_video_seconds':j['duration'],'original_source_reuse_max':max(base_counts.values()),
        'voice_sha256':sha(voice),'approved_endscreen_sha256':sha(screen),
        'beat_changes':before_lengths,'every_cut_labelled_by_spoken_phrase':True,
        'no_motion_effects_in_film_source':True,'script_audio_unchanged':True,
        'preview_seconds':180,'no_new_generation':True}
print(json.dumps(report,indent=2))
if args.report:pathlib.Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
if args.dry_run:raise SystemExit(0)
shutil.copy2(index,P/'src/index_BEFORE_SCRIPT_CUT.jsx')
shutil.copy2(timeline,P/'public/timeline_BEFORE_SCRIPT_CUT.json')
index.write_text(src)
timeline.write_text(json.dumps(j,indent=2)+'\n')
