#!/usr/bin/env python3
"""V8 narration-locked clean picture cuts. Remove ALL V4/V7 pseudo motion, do not touch audio."""
import argparse,collections,json,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('--project',required=True)
p.add_argument('--dry-run',action='store_true')
args=p.parse_args()
root=pathlib.Path(args.project).resolve()
index=root/'src/index.jsx'
assert index.is_file()
j=json.loads((root/'public/timeline.json').read_text())
m=json.loads((root/'public/v4_accents.json').read_text())
assert j['fps']==25 and len(j['beats'])==87 and sum(len(x['slots']) for x in j['beats'])==99
assert len(m['items'])==100
source=index.read_text()
assert '<Caption' not in source and 'approved_first_end_1080.png' in source
assert 'V7Retention' not in source, 'NEVER stack failed V7 motion'
assert 'V8Cutaways' not in source, 'Do not patch twice'
old='<V4Picture frame={frame}>{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}</V4Picture><V4Overlay frame={frame}/><Chapter'
new='{beatIndex===0?<OpeningPicture frame={frame}/>:<Picture beatIndex={beatIndex} frame={frame}/>}<V8Cutaways frame={frame}/><Chapter'
assert source.count(old)==1,'V4 anchor not unique; stop rather than silently leaving overlaid effect'
source=source.replace(old,new)
source=source.replace('import {V4Picture,V4Overlay} from "./AccentV4";\n','')
source='import {V8Cutaways} from "./V8Cutaways";\n'+source
# Hard preflight on every added exposure: NO third use of a recovered source.
src_assets=['LP-REC-021','LP-REC-031','LP-GFX-012','LP-GFX-005','LP-GFX-016']
counts=collections.Counter(x['asset_id'] for x in m['items'])
for asset in src_assets:
    assert counts[asset]==1,(asset,counts[asset])
    assert (root/'public/assets'/(asset+'.png')).is_file(),asset
    counts[asset]+=1
assert max(counts.values())<=2,counts.most_common(4)
cut_source=(D/'V8Cutaways.jsx').read_text()
assert 'zooms:0,spotlights:0,circles:0,arrows:0' in cut_source
assert not any(q in cut_source for q in ['transform:', 'scale(', 'radial-gradient', '<svg','<ellipse','V7Focus','v7Motion'])
assert len(src_assets)==5
assert 'V4Overlay' not in source and 'V4Picture' not in source, 'V4 effects still present'
assert 'V7Focus' not in source and 'v7Motion' not in source
assert 'Audio src={staticFile(' in source and 'approved_first_end_1080.png' in source, 'VO/end-screen changed'
if args.dry_run:
    print('V8 SOURCE PREFLIGHT PASS: five full-frame editorial cuts; no V4/V7 motion or spotlights; reuse<=2; 87 beats/99 slots; original Arthur/end screen')
    raise SystemExit()
shutil.copy2(index,root/'src/index_before_v8_clean_cut.jsx')
index.write_text(source)
(root/'src/V8Cutaways.jsx').write_text(cut_source)
print('V8 clean-cut patch installed — ZERO zoom, ZERO spotlight, ZERO rings; no new TTS/image jobs')
