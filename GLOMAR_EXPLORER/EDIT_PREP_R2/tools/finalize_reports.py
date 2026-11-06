from pathlib import Path
from collections import defaultdict
import json,csv,hashlib,html,re,sys,subprocess
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parents[1];PROJECT=OUT.parent;EXP=PROJECT/'ARCHIVE_EXPANSION_R5'
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def writecsv(p,rows):
    if not rows:return
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
rows=readcsv(OUT/'EDIT_TIMELINE.csv');reg=json.loads((OUT/'ASSET_REGISTER.json').read_text(encoding='utf-8'))
summary=json.loads((OUT/'PLAN_SUMMARY.json').read_text(encoding='utf-8'))
acts=defaultdict(lambda:defaultdict(float))
for a in rows:acts[a['paragraph_id'].split('-')[0]][a['visual_type']]+=float(a['duration_seconds'])
writecsv(OUT/'ACT_COVERAGE.csv',[{'act':act,'video_seconds':round(v['VIDEO'],3),'photo_seconds':round(v['PHOTO']+v['PHOTO_DOCUMENT'],3),'document_seconds':round(v['DOCUMENT'],3),'archival_drawing_seconds':round(v['ARCHIVAL_DRAWING'],3),'full_frame_graphic_seconds':round(v['NATIVE_GRAPHIC'],3),'known_gap':('No free-cleared moving construction film; Sun Ship still permissions HOLD' if act=='A03' else 'No free-cleared January/West Coast trials film' if act=='A04' else 'V03/V04 motion rights remain HOLD' if v['VIDEO'] else '')} for act,v in acts.items() if act!='END_SCREEN'])
quality=[]
for aid in dict.fromkeys(a['asset_id'] for a in rows):
    obj=reg[aid];candidate=obj.get('staging_file') or obj.get('local_file','');p=Path(candidate) if candidate else None
    w=obj.get('width','');h=obj.get('height','')
    if p and p.is_file() and p.suffix.lower() in ['.jpg','.jpeg','.png']:
        with Image.open(p) as im:w,h=im.size
    display='SOURCE_REVIEW_REQUIRED'
    if isinstance(w,int) and w<700:display='LOW_NATIVE_RESOLUTION_NOT_FULL_HD; no full-frame enlargement; use legible bounded source detail or leave HOLD'
    elif w:display='NATIVE_PIXELS_RECORDED; inspect actual framing and no artificial detail restoration'
    if obj['kind']=='VIDEO':display='Original analog detail limit; 720p encode is not proof of HD. Preserve aspect ratio; no frame-over-frame filler'
    quality.append({'asset_id':aid,'kind':obj['kind'],'used_seconds':round(sum(float(a['duration_seconds']) for a in rows if a['asset_id']==aid),3),'local_file':obj.get('local_file',''),'staging_file':obj.get('staging_file',''),'physically_exists':bool(p and p.is_file()),'width':w,'height':h,'source':obj.get('source',''),'rights':obj.get('rights_status',''),'display_gate':display,'sha256':sha(p) if p and p.is_file() and obj['kind']!='VIDEO' else obj.get('sha256','')})
writecsv(OUT/'SOURCE_QUALITY_AND_GATES.csv',quality)
target_evidence=json.loads((EXP/'EVIDENCE/ENDSCREEN_TARGET_READBACK.json').read_text(encoding='utf-8'))
target={'previous_story_video_id':'sP67aPtpwKg','title':target_evidence.get('oembed',{}).get('title'),'channel':target_evidence.get('oembed',{}).get('author_name'),'url':'https://www.youtube.com/watch?v=sP67aPtpwKg','published_catalog_date':'2026-10-28','catalog':'CHANNEL/RESEARCH/2026-11-02/VIDEO_METRICS.csv','checked_utc':target_evidence['checked_utc'],'current_oembed_http':target_evidence.get('http_status'),'current_embed_available':target_evidence.get('embed_available_now'),'current_public_listing_visibility':'NOT_CHECKED; oEmbed alone does not establish public vs unlisted','decision':'Use Camp Century from published HIA catalogue; recheck end-screen element eligibility in Studio','slots':['Subscribe','Previous Story'],'start_seconds':816.96,'end_seconds':836.96,'duration_seconds':20,'spoken_cta_added':False,'artwork':'Existing layout is review-only, final artwork not yet produced'}
(OUT/'ENDSCREEN_TARGET.json').write_text(json.dumps(target,ensure_ascii=False,indent=2),encoding='utf-8')
validation=json.loads((OUT/'VALIDATION.json').read_text(encoding='utf-8'))
validation['end_screen_target']='CAMP_CENTURY_CATALOG_PUBLICATION_AND_CURRENT_OEMBED_CONFIRMED; STUDIO_ELIGIBILITY_PENDING'
validation['same_script_en_bytes']=sha(OUT/'SCRIPT_R1_2_EN.md')==sha(PROJECT/'EDIT_PREP_R1/SCRIPT_R1_2_EN.md')
validation['same_script_ru_bytes']=sha(OUT/'SCRIPT_R1_2_RU.md')==sha(PROJECT/'EDIT_PREP_R1/SCRIPT_R1_2_RU.md')
validation['same_paragraph_timing_bytes']=sha(OUT/'PARAGRAPH_TIMING.csv')==sha(PROJECT/'EDIT_PREP_R1/PARAGRAPH_TIMING.csv')
assert all(validation[k] for k in ['same_script_en_bytes','same_script_ru_bytes','same_paragraph_timing_bytes'])
# Probe all selected media against the actual binary, not solely an old manifest.
probe={};cuts=readcsv(OUT/'MOVING_ARCHIVE_CUTLIST.csv')
for aid in dict.fromkeys(a['asset_id'] for a in cuts):
    path=reg[aid]['local_file'];run=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,r_frame_rate,codec_name','-of','json',path],capture_output=True,text=True)
    assert run.returncode==0,(aid,run.stderr)
    obj=json.loads(run.stdout);probe[aid]={'file':path,'duration':float(obj['format']['duration']),'streams':obj.get('streams',[]),'sha256':sha(Path(path))}
for a in cuts:assert float(a['source_out_seconds'])<=probe[a['asset_id']]['duration']+.002,(a,probe[a['asset_id']])
validation['all_27_video_trim_bounds_probed']='PASS'
(OUT/'VIDEO_BINARY_READBACK.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')

state=json.loads((PROJECT/'PROJECT_STATE.json').read_text(encoding='utf-8'))
state.update({'status':'ARCHIVE_FIRST_R2_REVISED_FOOTAGE_AND_RIGHTS_HOLD','edit_prep':'EDIT_PREP_R2/README_RU.md','previous_edit_prep':'EDIT_PREP_R1/README_RU.md','archive_report':'ARCHIVE_EXPANSION_R5/README_RU.md','visual_timeline_rows':len(rows),'mandatory_image_generation_jobs':0,'deferred_image_jobs':7,'missing_image_prompts':0,'new_archival_motion_sources_acquired':0,'selected_moving_archive_plan_seconds':summary['planned_moving_archive_seconds'],'standalone_graphic_plan_seconds':summary['primary_visual_seconds']['NATIVE_GRAPHIC'],'owner_visual_rule':'Archive primary; stock rare; generation only unavoidable scene-specific gaps. Prior 40-second/graphics-majority plan rejected by owner on 2026-11-05.','end_screen_previous_story':'sP67aPtpwKg','end_screen_target_check':'PUBLISHED_CATALOG_AND_CURRENT_OEMBED_HIA_MATCH; STUDIO_CHECK_PENDING','picture_production_started':False})
(PROJECT/'PROJECT_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
for folder in [OUT,EXP]:
    hashes=[]
    for p in sorted(folder.rglob('*')):
        if p.is_file() and p.name not in ['SHA256.csv','SHA256_SYNC.csv']:hashes.append({'file':str(p.relative_to(folder)),'bytes':p.stat().st_size,'sha256':sha(p)})
    writecsv(folder/'SHA256.csv',hashes)
print(json.dumps({'quality_rows':len(quality),'video_sources_probed':len(probe),'selected_video_windows':len(cuts),'archive_plan_seconds':summary['planned_moving_archive_seconds'],'scripts_unchanged':True,'endscreen_target':target['title'],'status':state['status']},ensure_ascii=False,indent=2))
