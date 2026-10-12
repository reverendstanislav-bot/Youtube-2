#!/usr/bin/env python3
"""Enhance the existing final, director-locked Lake Peigneur 141-slot HIA/R15 source.

Not a picture shuffle: add selectively timed, story-led emphasis and extremely restrained
reconstruction depth only; never touch Arthur, factual PNGs, core timing, end screen.
"""
import argparse,json,pathlib,hashlib
p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--output',required=True)
a=p.parse_args();P=pathlib.Path(a.project).resolve()
D=pathlib.Path(__file__).resolve().parent
M=json.loads((D/'EMPHASIS_MAP_V1.json').read_text())
timeline=json.loads((P/'public/timeline.json').read_text())
assert len(timeline['beats'])==87 and sum(len(x['slots']) for x in timeline['beats'])==141
srcpath=P/'src/index.jsx'
src=srcpath.read_text()
assert 'const DISSOLVE_HALF=3;' in src and 'pictureGroups=makeGroups(pictureShots)' in src
assert src.count('function PictureLayer({slot,opacity=1})')==1
assert src.count('function Chapter({frame})')==1
assert 'approved_first_end_1080.png' in src and 'LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3' in src
assert '<Caption' not in src
assert 'D2EditorialEmphasis' not in src
assert len(M['overlays'])==13 and len(M['focus'])==7
all_assets={s['assetId'] for b in timeline['beats'] for s in b['slots']}
for z in M['focus']:
 assert z['asset'] in all_assets,z
 assert z['scale']<=1.012 and z['scale']>=1.0
 assert 0<=z['start']<z['end']<=968.44
for z in M['overlays']:
 assert 0<=z['start']<z['end']<=968.44
 assert len(z['main'])<=32 and len(z['sub'])<=75
assert all(x['end']<=y['start'] for x,y in zip(M['overlays'],M['overlays'][1:]))
# derive a fully immutable editorial cue map directly from the approved manifest
data=json.dumps(M,separators=(',',':'))
cue_code="""
const D2EditorMap=__D2_EDIT_MAP__;
const D2_LIMIT={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
function D2ease(p){const x=Math.max(0,Math.min(1,p));return x*x*(3-2*x)}
function D2EditorialEmphasis({frame}){
 const sec=frame/25;
 const e=D2EditorMap.overlays.find(c=>sec>=c.start && sec<c.end);
 if(!e)return null;
 const d=e.end-e.start;
 const local=sec-e.start;
 // An unobtrusive typographic hierarchy, not a panel, card, or animated collage.
 const fade=Math.min(D2ease(local/.25),D2ease((d-local)/.34));
 const rust=e.tone==='rust';
 return <div style={{
   position:'absolute',right:86,top:130,width:780,
   opacity:fade,zIndex:24,textAlign:'right',pointerEvents:'none',
   fontFamily:'Arial,Helvetica,sans-serif',
   filter:'drop-shadow(0px 3px 7px rgba(0,0,0,.83))'
 }}>
   <div style={{fontSize:23,letterSpacing:4.2,fontWeight:800,
     color:rust?'#CD6B48':'#E6DDC8'}}>{e.top}</div>
   <div style={{fontSize:56,lineHeight:1.04,fontWeight:900,letterSpacing:-1.5,
     color:'#F3EBDD',marginTop:10}}>{e.main}</div>
   <div style={{fontSize:23,fontWeight:650,color:'#F3EBDD',marginTop:10}}>{e.sub}</div>
 </div>
}
""".replace('__D2_EDIT_MAP__',data)
# Keep camera movement almost imperceptible and only on seven short verified story passages.
target="function PictureLayer({slot,opacity=1}){"
src=src.replace(target,"function PictureLayer({slot,opacity=1,frame=0}){\n const focus=D2EditorMap.focus.find(z=>z.asset===slot.assetId && frame/25>=z.start && frame/25<z.end);\n const progress=focus?D2ease((frame/25-focus.start)/(focus.end-focus.start)):0;\n const scale=focus?1+(focus.scale-1)*progress:1;\n",1)
old="objectFit:contain?'contain':'cover',objectPosition:'center'"
new="objectFit:contain?'contain':'cover',objectPosition:'center',\n    transform:scale!==1?('scale('+scale+')'):undefined,\n    transformOrigin:focus?focus.origin:'50% 50%'"
assert src.count(old)==1,src.count(old)
src=src.replace(old,new)
# Pass the actual composition frame into the existing three picture layers. No change to cut timing.
for x in ("curr","n","p"):
 if x=="curr":
  src=src.replace("<PictureLayer slot={curr} opacity={1-alpha}/>","<PictureLayer slot={curr} opacity={1-alpha} frame={f}/>")
  src=src.replace("<PictureLayer slot={curr} opacity={alpha}/>","<PictureLayer slot={curr} opacity={alpha} frame={f}/>")
  src=src.replace("<PictureLayer slot={curr}/>","<PictureLayer slot={curr} frame={f}/>")
 elif x=="n":src=src.replace("<PictureLayer slot={n} opacity={alpha}/>","<PictureLayer slot={n} opacity={alpha} frame={f}/>")
 elif x=="p":src=src.replace("<PictureLayer slot={p} opacity={1-alpha}/>","<PictureLayer slot={p} opacity={1-alpha} frame={f}/>")
assert src.count('frame={f}')>=5
at=src.index('function Chapter({frame})')
src=src[:at]+cue_code+"\n"+src[at:]
# Render the new layer before chapter/fact cards so historically verified display takes precedence.
needle="}<Chapter"
assert needle in src, 'Final film hook missing; refusing to guess where to place captions/graphics'
src=src.replace(needle,"}<D2EditorialEmphasis frame={frame}/><Chapter",1)
assert src.count("D2EditorialEmphasis frame={frame}") == 1
assert src.count("const D2EditorMap=")==1
assert 'approved_first_end_1080.png' in src
assert src.count('LAKE_PEIGNEUR_ARTHUR_MASTER_LOCKED.mp3')==2
srcpath.write_text(src)
report={"status":"DIRECTORIAL HIA EDIT LAYER INSTALLED; RENDER AND HUMAN QC REQUIRED",
 "beats":87,"slots":141,"word_locked_prior_cuts":42,
 "editorial_focus_windows":len(M['focus']),
 "editorial_text_windows":len(M['overlays']),
 "original_arthur_unchanged":True,"original_endscreen_unchanged":True,
 "new_media_generated":0,"global_zoom_applied":False,
 "source_manifest":'LAKE_PEIGNEUR/PUBLISHING/DIRECTORIAL_V2/EMPHASIS_MAP_V1.json'}
pathlib.Path(a.output).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
