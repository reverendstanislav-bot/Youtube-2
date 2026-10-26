"""Publish only physically verified Camp Century metadata and honest coverage HOLDs."""
import csv,json,hashlib,shutil,html,subprocess
from pathlib import Path
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
ARCH=REPO/'CAMP_CENTURY/ARCHIVE';DEST=ARCH/'STAGE06_DELIVERY_2026-10-26'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def writecsv(p,rows,fields=None):
 if fields is None:fields=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(4<<20),b''):h.update(x)
 return h.hexdigest()
SOURCES={
 'F01':('USACE Army Progress Report6 official alternate print','https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34'),
 'F01B':('DoD PIN26064 The Story of Camp Century color Army film','https://archive.org/details/gov.dod.dimoc.26064'),
 'F02':('NARA111-TV-514 City Under the Ice','https://archive.org/details/gov.archives.arc.2569752'),
 'F03':('USACE/Army PM-2A relocation film,1965 release/1964 events','https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv'),
 'F04':('NARA111-TV-543 Top of the World','https://archive.org/details/gov.archives.arc.2569778'),
 'F05':('NARA111-TV-520 US Army and the Boy Scouts','https://archive.org/details/gov.archives.arc.2569758'),
 'F06':('DoD PIN30259 ArmyTV781 Engineering for Tomorrow','https://archive.org/details/gov.dod.dimoc.30259')}
GAPS={
 'CH01':'1963 measured creep and the20,000yd3 annual estimate are not filmed here. Selected earlier camp views are context only; no operational Iceworm footage exists.',
 'CH02':'Actual construction supply actions available. Film tonnage/timing must not replace V4 figures. Route and Thule/Tuto remain separate from the base.',
 'CH03':'Actual excavation/arches/floor framing available. Footage does not itself prove measured deformation, annual upkeep or premature form removal.',
 'CH04':'Actual PM-2A transport/install/plant and water-system views available. No identified footage proves the quoted cost, wastewater destabilization or repeated turbine failures.',
 'CH05':'Only public-film camp life/research context. No actual Iceworm deployment: missiles and launching positions were proposals. Proposal/diplomacy/rejection beats need documentary evidence, not invented motion.',
 'CH06':'Only contextual construction/workshop actions, not verified annual re-trimming, cross-section closure measurements or Figure33 electric-chainsaw work. Those central beats remain uncovered by motion.',
 'CH07':'Real1964 dismantling and outward transport available, in severely magenta640x480 public print. No selected motion proves later contamination/climate projections. Higher-quality official720x480 requires legitimate access.',
 'CH08':'ZERO matching1966 deep-core drilling, ancient-plant analysis,2024 NASA radar flight or underground radar-city footage identified. Earlier1959 surveying and the scientific-aide visit are not relabelled as these events.'}
def main():
 DEST.mkdir(exist_ok=True);(DEST/'tools').mkdir(exist_ok=True);(DEST/'rights').mkdir(exist_ok=True);(DEST/'evidence').mkdir(exist_ok=True)
 scenes=read(ROOT/'reports/FRAME_EXACT_CUT_RESULTS.json');tech={r['scene_id']:r for r in read(ROOT/'reports/CLIP_TECHNICAL_QC.json')}
 selected=[]
 for r in scenes:
  sid=r['scene_id'];q=tech[sid]
  assert q['full_decode_exit_code']==0 and q['audio_tracks']==0 and q['sha256']==r['cut_sha256']
  assert not q['black_events'] and not q['freeze_events'],(sid,q)
  # Correct primary assignments instead of padding CH08 with unrelated-period context.
  if sid in ['CC07-C054','CC07-C055']:r.update(chapter='CH02',beat='CC07-S4-CH02-B01',evidence_role='1959_SITE_SELECTION_CONTEXT')
  if sid=='CC07-C088':r.update(chapter='CH05',beat='CC07-S4-CH05-B01',evidence_role='PERIOD_PUBLIC_RESEARCH_CONTEXT')
  if r['chapter'] in ['CH01','CH06']:r['evidence_role']='CONTEXT_ONLY_NOT_DIRECT_PROOF_OF_MEASURED_CREEP'
  if sid=='CC07-C041':r['evidence_role']='PLANT_CONTEXT_NOT_FILMED_TURBINE_FAILURE'
  r.update(status='PHYSICAL_FRAME_EXACT_CODEX_REVIEWED_NOT_OWNER_APPROVED',source_url=SOURCES[r['source_id']][1],rights_status='SELECTED_SILENT_ARMY_PICTURE_PD_BASIS_REVIEWED',rights_receipt='STAGE06_DELIVERY_2026-10-26/rights/'+r['rights_receipt'],historical_context=('March-July1964 PM-2A removal; film released1965' if r['source_id']=='F03' else '1959-early1960s Army Camp Century project, as identified by original film sequence'),audio_start_sec='',audio_end_sec='',audio_status='AUDIO_TIMING_HOLD',native_sar=q['sar'],native_field_order=q['field_order'],full_clip_decode_exit_code=q['full_decode_exit_code'],source_in_definition='Elapsed decoded source video frame index /30000*1001; zero-based, OUT exclusive; not SMPTE drop-frame',review_method='Full-source8s picture indexes + source narration research ASR + eight-phase per-candidate sequence inspection; every-frame technical decode; no full human1x screening claimed')
  r['local_rights_receipt']=str(ROOT/'rights_receipts'/f"{r['source_id']}_RIGHTS.md")
  selected.append(r)
 # Different ranges of one source may not overlap; alternate prints are not exported.
 for i,a in enumerate(selected):
  for b in selected[i+1:]:
   assert a['source_id']!=b['source_id'] or min(a['end_sec'],b['end_sec'])<=max(a['start_sec'],b['start_sec'])+0.0001
 assert len({r['cut_sha256'] for r in selected})==len(selected)
 fields=['scene_id','source_id','source_url','source_path','chapter','beat','site_class','actual_shot_description','historical_context','evidence_role','editorial_warning','start_tc','end_tc','start_frame','end_frame_exclusive','source_in_definition','seconds','cut_filename','cut_sha256','cut_seconds','source_sha256','source_fps','native_width','native_height','native_sar','native_field_order','rights_status','rights_receipt','local_rights_receipt','verified_by','review_method','status','audio_status','audio_start_sec','audio_end_sec']
 writecsv(ARCH/'STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv',selected,fields)
 writecsv(ROOT/'reports/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv',selected,fields)
 physical=read(ROOT/'reports/physical_originals.json');orig=[];lic=[]
 for r in sorted(physical,key=lambda r:r['source_id']):
  sid=r['source_id'];receipt=read(ROOT/'reports'/f'{sid}_DOWNLOAD_RECEIPT.json');n=sum(x['source_id']==sid for x in selected)
  caveat=''
  if sid=='F01':caveat='Same work asF01B; inferior faded official print;0clips to avoid double counting.'
  if sid=='F01B':caveat='Original audio DTS/null-mux errors; full VIDEO-only decode PASS; all clips silent.'
  if sid=='F03':caveat='PUBLIC_PLAYER_RENDITION, not the gated720x480 original; strong magenta fade; official videofile4604847 returned403.'
  if sid in ['F02','F04','F06']:caveat='No additional unique selected scenes after comparison; mixed-location content excluded. Does not mean every frame of the whole film is a duplicate.'
  if sid=='F05':caveat='Third-party Rockwell/Brown and Bigelow paintings and studio sections explicitly excluded; selected Army base pictures only.'
  orig.append({k:r.get(k,'') for k in ['source_id','path','size_bytes','sha256','duration','width','height','fps','video_codec','field_order','sample_aspect_ratio','display_aspect_ratio','status','all_stream_decode_exit_code','video_only_recheck']})
  orig[-1].update(title=SOURCES[sid][0],source_url=SOURCES[sid][1],download_url=receipt['url'],origin_kind=receipt.get('origin_kind',''),publisher_md5=receipt.get('md5',''),selected_clips=n,quality_and_exclusion_note=caveat)
  lic.append({'source_id':sid,'source_url':SOURCES[sid][1],'provenance':'US Army federal original / official Army record; IA mirror where applicable','rights_evidence':('USACE explicit federal public-domain statement' if sid in ['F01','F01B'] else 'DVIDS PUBLIC DOMAIN item and copyright policy' if sid=='F03' else 'IA item metadata CC0/public-domain and Army/NARA identifiers'),'selected_clips':n,'decision':'SELECTED_SILENT_PICTURE_ONLY' if n else 'NOT_USED_NO_RIGHTS_APPROVAL_OF_UNSELECTED_CONTENT','third_party_and_quality_limit':caveat,'receipt_file':f'STAGE06_DELIVERY_2026-10-26/rights/{sid}_RIGHTS.md' if n else 'STAGE06_DELIVERY_2026-10-26/evidence/'+sid+'_SOURCE_RECORD.json','endorsed_by_government':'NO'})
  record={'source_id':sid,'page':SOURCES[sid][1],'acquisition_receipt':receipt,'source_video_qc':r,'notes':caveat}
  (DEST/'evidence'/f'{sid}_SOURCE_RECORD.json').write_text(json.dumps(record,indent=2))
 writecsv(ARCH/'STAGE06_ACQUIRED_ORIGINALS_SHA256.csv',orig);writecsv(ARCH/'STAGE06_EDITORIAL_LICENSE_RECEIPTS.csv',lic)
 duplicates=read(ROOT/'reports/DUPLICATE_PROOF_CANDIDATES.json')
 desc={'F01':'Same Army film, alternate print; matching dining-room action','F02':'Same snow-block worker and dog action, B/W versus color','F04':'Same tractor driving through the garage arch, different compilation timing','F06':'Same Thule harbour shipment action, later color compilation'}
 for d in duplicates:
  d.update(status='CONFIRMED_SAME_UNDERLYING_PICTURE_SEQUENCE_EXCLUDED',reviewed_by='Codex three-phase paired picture inspection',action=desc[d['source_id']],time_alignment_limit='Intervals identify matching source sequences; print cut timing/crop may differ. Not a claim of frame-identical files.',scope='Only the documented window is confirmed here; no claim that entire compilation is duplicate',selected_duplicate_seconds_added=0)
  shutil.copyfile(Path(d['proof_path']),DEST/'evidence'/Path(d['proof_path']).name)
 writecsv(ARCH/'STAGE06_CONFIRMED_DUPLICATE_EXCLUSIONS.csv',duplicates)
 for p in (ROOT/'rights_receipts').glob('*.md'):shutil.copyfile(p,DEST/'rights'/p.name)
 beats=list(csv.DictReader((REPO/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv').open(encoding='utf-8-sig',newline='')))
 br=[]
 for b in beats:
  rr=[r for r in selected if r['beat']==b['beat_id']]
  br.append({'beat_id':b['beat_id'],'chapter':b['chapter'],'narration_words':b['words'],'estimated_seconds_145wpm':b['estimated_seconds_at_145wpm'],'scene_ids':';'.join(r['scene_id'] for r in rr),'unique_assigned_bank_seconds':round(sum(r['seconds'] for r in rr),6),'status':'CONTEXT_OR_ACTION_AVAILABLE_NOT_COMPLETE_NARRATIVE_COVERAGE' if rr else 'NO_MATCHING_SELECTED_MOTION_HOLD','chapter_limit':GAPS[b['chapter']],'audio_status':'AUDIO_TIMING_HOLD'})
 writecsv(DEST/'STAGE06_ALL_32_V4_BEATS_COVERAGE.csv',br)
 coverage=[]
 words={'CH01':297,'CH02':332,'CH03':336,'CH04':409,'CH05':368,'CH06':441,'CH07':333,'CH08':415}
 lines=['# Stage06 real moving-video bank — actual physical delivery','', 'Status: **VISUAL COVERAGE HOLD**. Acquisition and frame-exact clip extraction performed. This is not final owner/independent editorial approval.','', 'V4 remains locked:2931words,8chapters,32beats. AUDIO_TIMING_HOLD: no approved production narration was used;145wpm estimates below are planning figures only.','', '| Chapter | Clips | Direct site seconds | Own supply seconds | Unique total min | Bank sec / estimated speech sec |','|---|---:|---:|---:|---:|---:|']
 for ch,w in words.items():
  rr=[r for r in selected if r['chapter']==ch];direct=sum(r['seconds'] for r in rr if r['site_class']=='DIRECT_CAMP_CENTURY');supply=sum(r['seconds'] for r in rr if r['site_class']=='SAME_PROJECT_SUPPLY_CHAIN');total=direct+supply;vo=w*60/145
  coverage.append({'chapter':ch,'clips':len(rr),'DIRECT_CAMP_CENTURY_SEC':round(direct,6),'OWN_PROJECT_SUPPLY_CHAIN_SEC':round(supply,6),'unique_minutes':round(total/60,4),'estimated_speech_seconds_145wpm':round(vo,4),'bank_to_estimated_speech_percent':round(100*total/vo,2),'status':'HOLD','gap':GAPS[ch]})
  lines.append(f'|{ch}|{len(rr)}|{direct:.3f}|{supply:.3f}|{total/60:.3f}|{100*total/vo:.1f}%|')
 lines+=['','The percentage is **available bank duration divided by an estimated speech duration**, not percentage of a finished timeline covered. It can exceed100% while central beats remain missing. Context shots do not prove numerical claims. No repeated frame ranges are counted across chapters; each clip has one primary chapter. CH08 intentionally remains0 rather than relabelling earlier research as1966/2024.','']
 for ch in words:lines.append(f'- **{ch}:** {GAPS[ch]}')
 total=sum(r['seconds'] for r in selected);direct=sum(x['DIRECT_CAMP_CENTURY_SEC'] for x in coverage);supply=sum(x['OWN_PROJECT_SUPPLY_CHAIN_SEC'] for x in coverage)
 lines+=['',f'Physical delivery: **{len(selected)} MP4 clips, {total:.6f} seconds / {total/60:.4f} unique selected minutes**. Direct camp:{direct:.3f}s; own-project supply chain:{supply:.3f}s. All source intervals are5–20s. Sources represented:F01B,F03,F05; other print/source IDs do not add minutes.','',f'Editing archive: `{ROOT}`. Actual files are in `clips/`; originals in `masters/`. CSV paths address physical files. GitHub carries metadata, tools and rights/QC receipts, not multi-GB binaries.','', '## Verification and remaining gates','', '- All seven acquired video streams fully decoded; every delivered clip fully decoded and hashed. Frame-exact trim uses original decoded frame numbers; native resolution, SAR, fps and interlace order retained. No audio, upscaling, overlays, AI video or paid credits.','- Full-source8-second indexes, research-only source-narration ASR, scene-cut hints and eight sequential phases per candidate were inspected. This is **not a claim of continuous human1x screening**; independent complete playback/editorial signoff remains HOLD.','- Exact same-source range overlap and identical output hashes excluded. Cross-print paired pictures confirm reuse; a five-second sequence fingerprint screen additionally checks selected clips. Candidate matches require visual review and are not automatically called duplicates.','- F03 higher-quality720x480 download: HTTP403 at official videofile4604847. Anonymous public MP4/HLS ceiling640x480 acquired; source strongly magenta. Login-gated original not obtained or bypassed.','- F01B source audio has DTS/null-mux errors; video-only recheck passed; original sound not exported. F05 Rockwell paintings/third-party sequence excluded.','- Acquire actual rights-clear core-drilling/plant-research/radar motion for CH08, and documentary evidence for Iceworm/creep/annual-maintenance numerical beats; do not invent archival scenes. V4 unmodified.']
 (ARCH/'STAGE06_REAL_CAMP_SECONDS_PER_CHAPTER.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 writecsv(DEST/'STAGE06_UNIQUE_COVERAGE_BY_CHAPTER.csv',coverage)
 for name in ['SCRIPT_V4_IDENTITY.json','CLIP_TECHNICAL_QC.json','SELECTED_CLIP_DUPLICATE_CANDIDATES.json','REJECTED_CANDIDATES.json','EXPORTED_FRAME_SOURCE_CORRESPONDENCE.json','F03_OFFICIAL_ORIGINAL_ACCESS_CHECK.json']:
  shutil.copyfile(ROOT/'reports'/name,DEST/name)
 shutil.copyfile(Path(r'C:\Users\KK\camp_century_review_notes.json'),DEST/'CODEX_CANDIDATE_REVIEW_NOTES.json')
 for name in ['bootstrap','acquire_parallel','extra_jobs','analyze','asr','segment_and_align','candidates','cut_reviewed','frame_exact_cut','clip_qc','duplicate_proofs','verify_boundaries','access_receipt','deliver']:
  p=Path(r'C:\Users\KK')/f'camp_century_{name}.py'
  if p.exists():shutil.copyfile(p,DEST/'tools'/p.name)
 correspondence=read(ROOT/'reports/EXPORTED_FRAME_SOURCE_CORRESPONDENCE.json')
 assert len(correspondence)==len(selected) and all(r['status']=='SOURCE_FRAME_MATCH_PASS' for r in correspondence)
 qc={'status':'VISUAL_COVERAGE_HOLD','clip_count':len(selected),'unique_selected_seconds':total,'direct_camp_seconds':direct,'own_supply_seconds':supply,'acquired_source_files':len(physical),'acquired_bytes':sum(r['size_bytes'] for r in physical),'source_video_full_decode_pass':len(physical),'full_clip_decode_pass':len(tech),'source_first_middle_last_frame_match_pass':len(correspondence),'minimum_reference_frame_ncc':min(min(r['first_middle_last_ncc']) for r in correspondence),'black_events':sum(len(r['black_events']) for r in tech.values()),'freeze_events':sum(len(r['freeze_events']) for r in tech.values()),'independent_human_1x_screening':'NOT_PERFORMED_HOLD','owner_approval':'NOT_CLAIMED','audio_timing':'HOLD','paid_credits_spent':0,'script_changed':False,'coverage':coverage}
 (DEST/'STAGE06_FINAL_QC_REPORT.json').write_text(json.dumps(qc,indent=2))
 intro=f'''# CAMP CENTURY VIDEO007 — actual Stage06 editing archive

{len(selected)} silent native-SD MP4 excerpts, {total/60:.3f} unique selected minutes. This is an archival cut bank, not a finished film. Visual Coverage HOLD: see the eight-chapter report and32-beat table.

- Open `INDEX.html` for chapter-grouped local playback.
- `clips/`: actual montage files; `masters/`: seven downloaded prints/renditions. F01B/F01 are the same underlying work. F03 is the anonymously accessible640x480 copy, not the gated original.
- `reports/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv`: true source frame IN/OUT, primary chapter/beat, place, purpose, historical context, rights and source/clip hashes.
- No approved V4 voice timing used: AUDIO_TIMING_HOLD. Original archive sound excluded. No subtitles or generated video.
- Native4:3 SD is intentional. Do not stretch or relabel the magenta F03 print as restored HD. Route/Thule/Tuto shots are labelled separately from the camp.
- Full continuous independent human playback has not been claimed; retain this editorial gate before final montage approval.

Source receipts and QC metadata are also committed under `CAMP_CENTURY/ARCHIVE/` in reverendstanislav-bot/Youtube-2. Clip files are physical here; not Git placeholders.
'''
 (ROOT/'README.md').write_text(intro,encoding='utf-8');(DEST/'README.md').write_text(intro,encoding='utf-8')
 page=['<!doctype html><meta charset="utf-8"><title>Camp Century Stage06</title><style>body{background:#141719;color:#eee;font:16px Arial;max-width:1200px;margin:32px auto}video{width:320px;max-height:260px}article{display:inline-block;vertical-align:top;width:350px;margin:12px;padding:10px;background:#24292c}small{color:#c5c9cd}</style><h1>Camp Century — actual archival cut bank</h1><p>Visual Coverage HOLD. Native silent SD. Source IN/OUT and legal/context limits are in the CSV. No owner approval or continuous human1x screening claimed.</p>']
 for ch in words:
  page += [f'<h2>{ch}</h2><p>{html.escape(GAPS[ch])}</p>']
  for r in selected:
   if r['chapter']!=ch:continue
   sid=r['scene_id'];page.append(f'<article><video controls preload="none" src="clips/{sid}.mp4"></video><p>{sid} / {r["seconds"]:.2f}s</p><p>{html.escape(r["actual_shot_description"])}</p><small>{r["source_id"]} {r["start_tc"]}–{r["end_tc"]}<br>{r["site_class"]}<br>{html.escape(r.get("editorial_warning", ""))}</small></article>')
 (ROOT/'INDEX.html').write_text('\n'.join(page),encoding='utf-8')
 # Source and script originals stay unchanged. No film binaries, research WAVs, captions or caches staged.
 print(json.dumps(qc,indent=2))
if __name__=='__main__':main()
