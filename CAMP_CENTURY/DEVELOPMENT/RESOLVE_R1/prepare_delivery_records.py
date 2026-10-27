"""Record existing assets and actual native edit provenance, without media changes."""
from pathlib import Path
import hashlib,json,csv
from PIL import Image
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
PEOPLE=REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_MOTION_PEOPLE_R2'
plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
results=json.loads((PEOPLE/'GENERATION_RESULTS.json').read_text(encoding='utf-8'))
manifest=[]
for r in results:
    path=Path(r['saved']); im=Image.open(path)
    aid=r['id']; base=aid.split('_')[0]
    used=[s for s in plan if s['asset_id']==base]
    rejected=aid=='M10_MILLER'
    alpha=im.getchannel('A').getextrema() if 'A' in im.getbands() else None
    manifest.append(dict(asset_id=aid,file=path.relative_to(REPO).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,width=im.width,height=im.height,mode=im.mode,alpha_extrema=alpha,status='REJECT_NOT_USED' if rejected else 'USED_ILLUSTRATIVE_R1',restriction='Incorrect machine form; not an authentic Peter miller' if rejected else 'Generated explanatory illustration; not archival evidence or a measured reconstruction',timeline_shots=[] if rejected else [s['shot_id'] for s in used],prompt_and_references='GENERATION_RESULTS.json',audio_changed=False))
(PEOPLE/'ASSET_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(PEOPLE/'README.md').write_text('''# Camp Century additional people and motion assets

Four backgrounds and two transparent object layers were generated from the registered Camp Century references. Full prompts and reference paths are in GENERATION_RESULTS.json; file hashes and native timeline use are in ASSET_MANIFEST.json.

M09: supply convoy and workers; the connected tractor/sled translates as one separate alpha layer. M10: workers in a snow excavation, used as an illustration only. The separate M10_MILLER object is REJECTED and is not on the timeline because its front assembly does not match the authentic Peter snow miller. M11: roof construction workers, restrained camera approach; no claim that the static roof part was animated. M12: anonymous modern researcher and sediment samples, local inspection lens; not a representation of an identified scientist or a documented 1960s event.

These assets are illustrative reconstructions, not original government documents, photographs, or moving archive. No generated video or voice job was run for these assets. Their provenance stays in the production records.
''',encoding='utf-8')
comps=[]
for p in sorted((ROOT/'COMPS').glob('*.comp')):
    comps.append(dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(ROOT/'COMPOSITION_SOURCE_HASHES.json').write_text(json.dumps(comps,indent=2),encoding='utf-8')
report=dict(timeline='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_25FPS',project='YT2 Vid7',duration_frames=27368,frame_rate=25,duration_seconds=1094.72,resolution=[1920,1080],shots=len(plan),fusion_compositions=len(comps),archive_shots=sum(s['kind']=='REAL_ARCHIVE_MOTION' for s in plan),audio_track_locked=True,subtitles=False,excluded=['G17','G18','C06 disputed rediscovery date','D07 unavailable GAO original','M10_MILLER'],alignment={'beat_boundaries':32,'subcue_fallback_shots':['S065','S089'],'note':'Beat boundaries use approved locked narration timing. Two internal visual cues use within-beat fallback timing; these are not claimed word-exact.'},render_scope='720p25 rough picture proxy, not final color/music/SFX',review={'representative_mask_stills':'Inspected actual DOC_MASK_CPU and CHART_MASK_CPU PNG outputs: local word fill and readable chart, no full-frame mask fill','additional_stills':'Inspected AIRCRAFT_CPU and REMOVAL_CPU; these sample a primary reference and buried-remains illustration, not the independently animated aircraft/module shots','full_real_time_av_review':'NOT_COMPLETED','owner_picture_approval':'PENDING','visual_coverage_pass':'NOT_CLAIMED'},historical_limitations=['Generated illustrations must not be treated as original footage or measured technical evidence','Source-bank independent real-time screening remains a separate gate','Archive motion gaps are covered by primary references and explanatory stills; no full archive-only coverage claim'])
(ROOT/'EDIT_PROVENANCE_AND_HOLDS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'people_assets':len(manifest),'compositions_hashed':len(comps),'shots':len(plan)}))
