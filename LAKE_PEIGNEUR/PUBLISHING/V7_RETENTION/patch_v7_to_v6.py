#!/usr/bin/env python3
"""Add retention-only editorial picture treatment to completed V6 source. No TTS/art/video-generation."""
import argparse, collections, json, pathlib, shutil
p=argparse.ArgumentParser()
p.add_argument('--project',required=True)
p.add_argument('--dry-run',action='store_true')
a=p.parse_args()
root=pathlib.Path(a.project).resolve()
src=root/'src/index.jsx'
visual=root/'src/V7Retention.jsx'
j=json.loads((root/'public/timeline.json').read_text())
acc=json.loads((root/'public/v4_accents.json').read_text())
assert src.is_file() and not visual.exists(), 'Unexpected prior V7 patch'
assert len(j['beats'])==87 and sum(len(b['slots']) for b in j['beats'])==99
assert len(acc['items'])==100 and sum(x['effect'] not in ('HOLD','QC_HOLD') for x in acc['items'])==36
blocked={'LP-GFX-002','LP-GFX-022','LP-GFX-026','LP-REC-005','LP-REC-008','LP-REC-010','LP-REC-012','LP-REC-038','LP-REC-041'}
assert all(x['asset_id'] not in blocked for x in acc['items'])
source=src.read_text()
assert 'V4Picture' in source and 'V4Overlay' in source and 'approved_first_end_1080.png' in source
assert '<Caption' not in source and 'CleanEndScreen' not in source
current=(root/'src/AccentV4.jsx').read_text()
assert not any(z in current for z in ('<ellipse','<circle','<svg','strokeWidth=')),'V6 NO RINGS gate failed'
# Explicit additional teaser source exposures are counted, including original V5 repairs.
reps={'LP-REC-002':1,'LP-REC-003':1}
counts=collections.Counter(x['asset_id'] for x in acc['items'])
counts.update(reps)
assert max(counts.values())<=2,counts.most_common(8)
for s in reps: assert (root/'public/assets'/(s+'.png')).exists(),s
old="""<Img src={staticFile(slot.file)} style={{width:'100%',height:'100%',objectFit:gfx?'contain':'cover',objectPosition:'center',filter}}/>"""
new="""<Img src={staticFile(slot.file)} style={{width:'100%',height:'100%',objectFit:gfx?'contain':'cover',objectPosition:'center',filter,...v7Motion(slot,frame)}}/>"""
assert source.count(old)==1,'Exact V3 PictureLayer source anchor changed'
source=source.replace(old,new)
old2='<V4Overlay frame={frame}/><Chapter'
new2='<V4Overlay frame={frame}/><V7Insert frame={frame}/><V7Focus frame={frame}/><V7Cues frame={frame} chapters={chapters} facts={facts}/><Chapter'
assert source.count(old2)==1,'Exact V4 film integration anchor changed'
source=source.replace(old2,new2)
source='import {v7Motion,V7Insert,V7Focus,V7Cues} from "./V7Retention";\n'+source
data=pathlib.Path(__file__).with_name('V7Retention.jsx').read_text()
assert 'V7RetentionMeta' in data and 'noCaptions:true' in data
if a.dry_run:
 print('V7 EDITOR PREVIEW PREFLIGHT PASS: 87 beats, 99 slots, 36 preserved V6 accents, max reuse='+str(max(counts.values()))+', preview-first; no writes')
 exit(0)
shutil.copy2(src,root/'src/index_V6_pre_V7.jsx')
src.write_text(source)
visual.write_text(data)
print('V7 EDITORIAL PATCHED: 2 new source-locked early contextual cut-ins; 13 focus windows; 8 restrained non-caption cues; <=1.018 micro-motion on long non-PUSH image holds')
