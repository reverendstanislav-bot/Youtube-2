from pathlib import Path
import json,csv,hashlib,collections
ROOT=Path(__file__).resolve().parent
p=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text());beats=json.loads((ROOT/'BEATS_AUDIO_LOCKED.json').read_text())
chapters=[]
for b in beats:
    if not chapters or chapters[-1]['chapter']!=b['chapter']:chapters.append(dict(chapter=b['chapter'],title=b['chapter_title'],audio_start_seconds=float(b['audio_start_sec'])))
for i,c in enumerate(chapters):c['audio_end_seconds']=chapters[i+1]['audio_start_seconds'] if i+1<len(chapters) else 1094.72
(ROOT/'SCRIPT_CHAPTER_BOUNDARIES.json').write_text(json.dumps(chapters,indent=2),encoding='utf-8')
bank={s['scene_id']:s for s in csv.DictReader(Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\reports\STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig'))}
rights=[]
for s in p:
    row={k:s.get(k,'') for k in ['shot_id','chapter','beat_id','asset_id','kind','start_frame','end_frame','duration_frames','voice_cue','edit_reason','path','source','locator','rights']}
    if s['kind']=='REAL_ARCHIVE_MOTION':
        original=bank[s['asset_id']]
        row.update(original_verified_selection_in_frame=original['start_frame'],original_verified_selection_out_exclusive=original['end_frame_exclusive'],original_fps=original['source_fps'],original_master_sha256=original['source_sha256'],verified_selected_clip_sha256=original['cut_sha256'],native_derivative_in_frame=0,native_derivative_out_exclusive=s['duration_frames'],native_derivative_fps='25/1',rights_receipt=original['local_rights_receipt'],historical_context=original['historical_context'],warning=original['editorial_warning'],bound_definition='Original bounds identify the complete verified source selection; derivative bounds identify actual 25fps timeline use, not an assertion of frame-identical cadence')
    if s.get('r2_origin'):row['r2_origin']=s['r2_origin']
    rights.append(row)
cols=list(dict.fromkeys(k for r in rights for k in r))
with (ROOT/'SOURCE_AND_RIGHTS_REGISTER.csv').open('w',encoding='utf-8-sig',newline='') as fp:w=csv.DictWriter(fp,fieldnames=cols);w.writeheader();w.writerows(rights)
hashes=[]
for d in ['COMPS','ASSETS']:
    for f in sorted((ROOT/d).glob('*')):
        if f.is_file():hashes.append(dict(file=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
(ROOT/'REVISION_SOURCE_HASHES.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
summary=dict(project='YT2 Vid7',timeline='HIA_VIDEO007_CAMP_CENTURY_VISUAL_R3_25FPS',shots=len(p),frames=27818,seconds=1112.72,original_locked_audio_seconds=1094.72,endscreen_seconds=18,new_image_generation=0,new_video_generation=0,voice_generation=0,archive_downloads=0,real_archive_clips=sum(s['kind']=='REAL_ARCHIVE_MOTION' for s in p),real_archive_seconds=sum(s['duration_frames']/25 for s in p if s['kind']=='REAL_ARCHIVE_MOTION'),distinct_restored_motion_types=8,motion_placements=sum(s['kind']=='EXISTING_REFERENCE_MOTION' for s in p),original_audio_unchanged=True,subtitle_tracks=0,owner_picture_approval='PENDING',full_continuous_av_review='NOT_COMPLETED',final_color_music_sfx='NOT_STARTED',publication_approved=False,notes=['Existing eight motion clips reused as native media; do not claim all their internal graphics are editable Fusion strokes','Reference holds preserve 25fps cadence without loops','Some still illustrations recur or remain held for reading; not all repetition is removed','Legacy within-beat subcue fallbacks S065/S089 remain in carried-over R2 material'])
(ROOT/'EDIT_PROVENANCE_AND_HOLDS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
