from pathlib import Path
import csv,json,hashlib,collections,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2];G=ROOT.parents[1]/'GRAPHICS';OUT=G/'STAGE07_CORRECTIONS_R3'
plan=json.loads((ROOT/'SHOT_PLAN_R2.json').read_text(encoding='utf-8'))
selected=[]
clean={'Q02','Q06','Q07','Q09','Q14','Q15','Q17','Q18'}
for i in range(1,20):
    aid=f'Q{i:02}';record_id=aid+'_CLEAN' if aid in clean else aid
    rec=json.loads((OUT/f'{record_id}_GENERATION.json').read_text(encoding='utf-8'))
    path=Path(rec['saved']);im=Image.open(path);used=[s['shot_id'] for s in plan if s['asset_id']==aid]
    assert used and path.is_file()
    rec.update(logical_asset_id=aid,file=path.relative_to(REPO).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),width=im.width,height=im.height,bytes=path.stat().st_size,used_in_shots=used,status='BASE_ARTWORK_VISUALLY_REVIEWED_FOR_R2',owner_approval='PENDING',provenance_class='GENERATED_EDITORIAL_ILLUSTRATION_NOT_ORIGINAL_RECORD',baked_text_highlighting=False)
    selected.append(rec)
(OUT/'SELECTED_GENERATION_RECORDS.json').write_text(json.dumps(selected,indent=2),encoding='utf-8')
fields=['logical_asset_id','title','file','sha256','width','height','bytes','provenance_class','baked_text_highlighting','owner_approval']
with (OUT/'ASSET_MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(selected)
sheet=Image.new('RGB',(1600,1230),'#eeefed');draw=ImageDraw.Draw(sheet)
for j,rec in enumerate(selected):
    im=Image.open(REPO/rec['file']);im.thumbnail((390,220));x=j%4*400;y=j//4*246
    draw.text((x+4,y+3),rec['logical_asset_id']+' / '+rec['title'][:47],fill='#17242b');sheet.paste(im,(x,y+20))
sheet.save(OUT/'SELECTED_BASES_CONTACT_SHEET.jpg',quality=94)
reason={'Q02':'unrelated aircraft in tunnel diagram','Q06':'thermal reactor rating visually associated with room heating','Q07':'approximate generated proportion bar removed for exact native chart','Q09':'invented stacked base; subsequent edit blocked by image generator; replaced with a different civil research notebook','Q14':'outdoor drilling and identifiable cereal-like material corrected using covered-trench source','Q15':'invented occupied surface scene in 2024 removed','Q17':'leaked authoring footer removed','Q18':'opaque beige annotation card removed'}
(OUT/'REJECTED_VARIANTS.json').write_text(json.dumps([dict(asset=k,file='assets/'+k+'.png',status='REJECTED_NOT_USED',reason=v) for k,v in reason.items()],indent=2),encoding='utf-8')
refs=[]
for name in ['G07_REVISED_R2.png','G01_DRAFT_R1.png','G12_DRAFT_R1.png','G10_REVISED_R2.png']:
    p=G/'STAGE07_GENERATED_R1/images'/name;refs.append(dict(file=p.relative_to(REPO).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(OUT/'LOCKED_STYLE_REFERENCE_HASHES.json').write_text(json.dumps(refs,indent=2),encoding='utf-8')
comps=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((ROOT/'COMPS').glob('*.comp'))]
(ROOT/'COMPOSITION_SOURCE_HASHES.json').write_text(json.dumps(comps,indent=2),encoding='utf-8')
summary=dict(project='YT2 Vid7',timeline='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2_25FPS',duration_frames=27368,duration_seconds=1094.72,fps=25,resolution=[1920,1080],shots=len(plan),native_fusion_comps=len(comps),selected_clean_new_assets=len(selected),generic_text_cards=0,direct_source_scans=0,archive_clips=sum(s['kind']=='REAL_ARCHIVE_MOTION' for s in plan),archive_timeline_seconds=sum(s['duration_frames']/25 for s in plan if s['kind']=='REAL_ARCHIVE_MOTION'),audio='Original locked WAV unchanged',subtitle_tracks=0,rejected_r1=True,full_continuous_av_review='NOT_COMPLETED',owner_picture_approval='PENDING',final_color_music_sfx='NOT_STARTED',visual_coverage_pass='NOT_CLAIMED',subcue_fallback_shots=['S065','S089'])
(ROOT/'EDIT_PROVENANCE_AND_HOLDS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(ROOT/'SOURCE_AND_RIGHTS_REGISTER.csv').write_bytes((ROOT/'SHOT_PLAN_R2.csv').read_bytes())
print(json.dumps(summary),flush=True)
