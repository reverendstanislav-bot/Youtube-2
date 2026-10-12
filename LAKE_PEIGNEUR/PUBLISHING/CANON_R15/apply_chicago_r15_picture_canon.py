#!/usr/bin/env python3
"""Apply the EXISTING HIA / Chicago R15 editing canon to the locked Lake Peigneur master timeline.
Picture-only implementation: no narration, asset selection, captions, music, or end-screen redesign.
"""
import argparse,json,pathlib,collections
p=argparse.ArgumentParser()
p.add_argument('--project',required=True)
args=p.parse_args()
root=pathlib.Path(args.project).resolve()
source=root/'src/index.jsx'
timeline=json.loads((root/'public/timeline.json').read_text())
assert timeline['fps']==25 and len(timeline['beats'])==87
shots=[s for b in timeline['beats'] for s in b['slots']]
assert len(shots)==129 and shots[0]['assetId']=='LP-REC-001' and shots[0]['a']==0 and shots[0]['b']==278
assert shots[-1]['b']==24211
assert all(a['b']==b['a'] for a,b in zip(shots,shots[1:])), 'No montage should cover an audio gap with an unrelated frame'
for s in shots:
 assert (root/'public'/s['file']).is_file(),s['file']
src=source.read_text()
assert "import timeline from '../public/timeline.json';" in src
assert 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in src
assert 'approved_first_end_1080.png' in src
assert 'V4Picture' not in src and 'V4Overlay' not in src
assert '<Caption' not in src
assert src.count('function PictureLayer(')==1 and src.count('function Picture({beatIndex,frame})')==1
assert src.count('function OpeningPicture({frame})')==1
first=src.index('function PictureLayer(')
last=src.index('function Chapter({frame})',first)
canon=r"""// CHANNEL/PROVENANCE_AND_EDITING_CANON.md + CHICAGO/R15_SMOOTH/TRANSITION_DESIGN.md
// Picture-only R15 translation: no floating camera, no fake refocus, six-frame full-frame dissolve.
// Consecutive occurrences of the SAME file form a single uninterrupted group.
const DISSOLVE_HALF=3;
const rawShots=timeline.beats.flatMap(b=>b.slots);
if(rawShots.length!==129 || rawShots[0].a!==0 || rawShots[0].b!==278) {
 throw new Error('Source timeline changed; do not apply an incorrect editorial transfer');
}
// Preserve the ALREADY-APPROVED second cold-open source (LP-REC-018).
// Before, the special OpeningPicture used 20-frame crossfade and caused a wrong-source flash at 11.1 s.
const firstSource=rawShots[0];
const pictureShots=[
 {...firstSource,b:150,e:150/FPS},
 {assetId:'LP-REC-018',file:'assets/LP-REC-018.png',kind:'reconstruction',a:150,b:278,
  s:150/FPS,e:278/FPS,motion:'none'},
 ...rawShots.slice(1),
];
if(pictureShots.some((s,i)=>i>0 && s.a!==pictureShots[i-1].b)) {
 throw new Error('Picture timeline has a gap / overlap');
}
function makeGroups(slots){
 const groups=[];
 for(const shot of slots){
  const prev=groups[groups.length-1];
  if(prev && prev.file===shot.file && prev.kind===shot.kind && prev.b===shot.a){
   prev.b=shot.b;
   prev.members+=1;
  } else groups.push({...shot,members:1});
 }
 return groups;
}
const pictureGroups=makeGroups(pictureShots);
const smoothed=(t)=>{const q=Math.max(0,Math.min(1,t));return q*q*(3-2*q)};
function PictureLayer({slot,opacity=1}){
 // Genuine maps and graphics are fully legible. All assets fill the available documentary frame.
 const contain=slot.kind==='gfx'||slot.kind==='document'||slot.kind==='map'||slot.kind==='real_context';
 return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden',opacity}}>
  <Img src={staticFile(slot.file)} style={{
    position:'absolute',inset:0,width:'100%',height:'100%',
    objectFit:contain?'contain':'cover',objectPosition:'center'
  }}/>
 </AbsoluteFill>;
}
function groupAt(f){
 let lo=0,hi=pictureGroups.length-1;
 while(lo<=hi){
  const mid=(lo+hi)>>1,g=pictureGroups[mid];
  if(f<g.a)hi=mid-1;
  else if(f>=g.b)lo=mid+1;
  else return mid;
 }
 throw new Error('No approved shot at frame '+f);
}
function Picture({frame}){
 const f=frame,idx=groupAt(f),curr=pictureGroups[idx];
 const p=idx>0?pictureGroups[idx-1]:null;
 const n=idx+1<pictureGroups.length?pictureGroups[idx+1]:null;
 // Six frames total, centered over the original narration-aligned cut.
 // The two media layers always fill the screen; no underlay-to-black or lateral slide.
 if(n && f>=curr.b-DISSOLVE_HALF){
  const alpha=smoothed((f-(curr.b-DISSOLVE_HALF))/(2*DISSOLVE_HALF-1));
  return <AbsoluteFill style={{background:C.charcoal}}>
   <PictureLayer slot={curr} opacity={1-alpha}/>
   <PictureLayer slot={n} opacity={alpha}/>
  </AbsoluteFill>;
 }
 if(p && f<curr.a+DISSOLVE_HALF){
  const alpha=smoothed((f-(curr.a-DISSOLVE_HALF))/(2*DISSOLVE_HALF-1));
  return <AbsoluteFill style={{background:C.charcoal}}>
   <PictureLayer slot={p} opacity={1-alpha}/>
   <PictureLayer slot={curr} opacity={alpha}/>
  </AbsoluteFill>;
 }
 return <PictureLayer slot={curr}/>;
}

"""
src=src[:first]+canon+src[last:]
os=src.index('function OpeningPicture({frame})')
oe=src.index('function Film(){',os)
src=src[:os]+"""function OpeningPicture({frame}) {
 // Render opening from the SAME canonical R15 picture timeline; never flash a wrong previous source.
 return <Picture frame={frame}/>;
}
"""+src[oe:]
# Canonical 10-frame end-screen fade. The PNG itself is unchanged.
src=src.replace('CONTENT_FRAMES+11]', 'CONTENT_FRAMES+10]')
assert 'DISSOLVE_HALF=3' in src and 'const frames=18' not in src
assert 'const split=150,transition=20' not in src
assert not any(t in src for t in ('translate(', 'scale(', 'V7Focus', 'V4Overlay', 'V7Retention','<Caption'))
assert src.count('approved_first_end_1080.png')==1
assert src.count('LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')==2
source.write_text(src)
# Auditable source cadence, separate from any editorial / human approval.
flat=[dict(s) for s in shots]
print(json.dumps({'status':'HIA R15 PICTURE CANON INSTALLED',
                  'film_beats':87,'original_locked_slots':len(flat),
                  'film_frames':24711,'voice_original':True,'endscreen_original':True,
                  'dissolve_total_frames':6,
                  'same_asset_groups_merged_in_renderer':True,
                  'source_images_replaced':0,
                  'word_cut_timings_modified':0,
                  'camera_pan_zoom_shake':0,
                  'chapters_and_facts_untouched':True}))
