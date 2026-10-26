import json,csv,hashlib,shutil,zipfile,re,subprocess,sys
from pathlib import Path
import pymupdf
sys.stdout.reconfigure(encoding='utf-8')
REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
P=REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R1'
B=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
def csvout(p,rows):
 with p.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 # Explicit obsolete reference files; never leave the rejected water/air label in the pack.
 reject=B/'qc/REJECTED_REFERENCE_FILES';reject.mkdir(exist_ok=True)
 for name in ['R09_WELL.jpg','R19_PLANT.jpg']:
  src=P/'references'/name
  if src.exists():
   assert src.resolve().parent==(P/'references').resolve()
   dst=reject/name
   if dst.exists():dst=reject/('SUPERSEDED_'+name)
   shutil.move(str(src),str(dst))
 refs=json.loads((P/'REFERENCE_REGISTER.json').read_text())
 for r in refs:
  assert (P/r['file']).is_file() and sh(P/r['file'])==r['sha256']
  r['visual_review']='CODEX_REVIEWED_CURATED_SEQUENCE_AND_CORRECTED_CROPS_NOT_OWNER_APPROVAL'
 # Correct reference-purpose boundaries explicitly.
 for r in refs:
  if r['reference_id']=='R09_AIR_WELL':r['input_role']='SEWAGE_VENTILATION_ONLY_NOT_DRINKING_WATER_NO_GENERATION_JOB_USES_THIS_IMAGE'
 (P/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2));csvout(P/'REFERENCE_REGISTER.csv',refs)
 assets=json.loads((P/'ASSET_PRODUCTION_QUEUE.json').read_text())
 for a in assets:
  if a['asset_id']!='D07':a['status']='PREPARATION_READY_REFERENCES_REVIEWED_OUTPUT_NOT_GENERATED'
  a['provenance_class']=('CONCEPT' if a['asset_id'].startswith('G') else 'EDITORIAL_GRAPHIC_FROM_CITED_DATA' if a['asset_id'].startswith('C') else 'HISTORICAL_SOURCE' if a['asset_id']=='D09' else 'SCIENTIFIC_SOURCE' if a['asset_id'] in ['D08','D10'] else 'DOCUMENT')
  a['rendered_metadata_text']='NONE; keep job IDs/production notes/provenance-control metadata out of the frame; historical qualifiers are specified separately'
 (P/'ASSET_PRODUCTION_QUEUE.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
 for a in assets:
  if a['production_route']!='IMAGEGEN_REFERENCED_ILLUSTRATION':
   p=P/a['prompt_file'];text=p.read_text(encoding='utf-8');text=re.sub(r'Status: .*',f"Status: {a['status']}",text);p.write_text(text,encoding='utf-8')
 rowcsv=[{**a,'beat_ids':';'.join(a['beat_ids']),'reference_ids':';'.join(a['reference_ids']),'exact_screen_text':';'.join(a['exact_screen_text']),'claim_ids':';'.join(a['claim_ids'])} for a in assets]
 csvout(P/'ASSET_PRODUCTION_QUEUE.csv',rowcsv)
 page=P/'INDEX.html';page.write_text(page.read_text(encoding='utf-8').replace('PREPARED_PENDING_VISUAL_REFERENCE_QC','PREPARATION_READY_REFERENCES_REVIEWED_OUTPUT_NOT_GENERATED'),encoding='utf-8')
 # Exact short OCR word targets on original PDF pages, expressed in normalized page space.
 doc=pymupdf.open(B/'sources/ARMY65_TR174.pdf');targets=[]
 for aid,page,term,mode in [('D05',49,'20,000','HIGHLIGHT_WORD_BOX'),('D05',49,'estimated','HIGHLIGHT_WORD_BOX'),('D04',47,'12%','CAPTION_WORD_ONLY_NEVER_FILL_DRAWING'),('D04',47,'17%','CAPTION_WORD_ONLY_NEVER_FILL_DRAWING'),('D03',39,'PM-2A','ROW_FOCUS'),('C06',55,'9 July 1963','DATE_FOCUS')]:
  pg=doc[page-1];hits=pg.search_for(term)
  if aid=='D05' and term=='estimated' and hits:
   anchor=pg.search_for('20,000')
   if anchor:hits=[min(hits,key=lambda r:abs(r.y0-anchor[0].y0))]
  boxes=[[round(r.x0/pg.rect.width,6),round(r.y0/pg.rect.height,6),round(r.x1/pg.rect.width,6),round(r.y1/pg.rect.height,6)] for r in hits]
  targets.append({'asset_id':aid,'source_pdf':'ARMY65_TR174.pdf','pdf_page_1based':page,'exact_search_text':term,'normalized_original_page_word_boxes':boxes,'mode':mode,'status':'WORD_POSITION_FOUND_VERIFY_AFTER_FINAL_DOCUMENT_CROP' if boxes else 'OCR_TARGET_HOLD_DO_NOT_GUESS','animation':'0.5-0.8s left-to-right mask across full word-height translucent yellow multiply band; black letters remain visible; no underline/strike-through','coordinate_scope':'Original full PDF page, not cropped JPEG. Transform using reference normalized crop before animation. Pixel alignment must be checked on final document render.'})
 (P/'data/DOCUMENT_FOCUS_TARGETS.json').write_text(json.dumps(targets,indent=2))
 mapping=list(csv.DictReader((P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv').open(encoding='utf-8-sig',newline='')))
 secondary={'CC07-S4-CH01-B03':'D02: actual base plan only; withhold the full proposal-number graphic until CH05','CC07-S4-CH02-B04':'G02: transition into cut-and-cover construction','CC07-S4-CH05-B03':'G07: maintenance-labour concept as analogy only, not actual Iceworm system','CC07-S4-CH05-B04':'C05: PROPOSAL/NEVER DEPLOYED qualifier; no fabricated rejection memorandum','CC07-S4-CH06-B05':'D04/D02: actual measured limits versus constructed base; no working missile network','CC07-S4-CH07-B04':'D09/G08: bridge to actual1966 drilling evidence','CC07-S4-CH08-B04':'D02/D04/D10: closing evidence montage, use only assets not already overused'}
 for m in mapping:
  m['secondary_context_options']=secondary.get(m['beat_id'],'')
  m['secondary_option_counting_rule']='Alternative placement only; no added unique-footage seconds, no obligation to repeat the same asset.'
  if not m['prepared_assets'] and not m['real_motion_clip_ids'] and not m['secondary_context_options']:m['uncovered_or_context_only']='EDITORIAL_VISUAL_SELECTION_HOLD_NO_MATCHING_PRIMARY_ASSIGNMENT'
 csvout(P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv',mapping)
 # Locked V4 hash checks use Git raw blob identities, not Windows working-copy line endings.
 expected={'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_FULL_NARRATION_V4_EN.md':'0006d5345bae22b77f3556dcb8090ce167f34292','CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt':'46fafe9914c1a061e9f219c344698f9857019973','CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv':'aea8122f66765b049effd61d6bc0eb4780250407'}
 for file,h in expected.items():
  actual=subprocess.check_output(['git','-c','safe.directory='+str(REPO).replace('\\','/'),'-C',str(REPO),'rev-parse','HEAD:'+file]).decode().strip();assert actual==h
 q=json.loads((P/'qc/PREPARATION_QC.json').read_text());q.update(reference_visual_review='CODEX_REVIEWED_CURATED_SHEETS_PLUS_CORRECTED_SOURCE_CROPS',imagegen_referenced_payloads_validated=10,script_v4_hashes_unchanged=True,readiness='10_IMAGEGEN_JOBS_READY_FOR_FIRST_PROOF_NOT_GENERATED;D07_DOCUMENT_HOLD;CHARTS_DATA_LOCKED',document_word_targets_found=sum(bool(t['normalized_original_page_word_boxes']) for t in targets),document_word_target_count=len(targets))
 (P/'qc/PREPARATION_QC.json').write_text(json.dumps(q,indent=2))
 notes='''# Preparation editorial QC —2026-10-26

26 briefs prepared:10 ImageGen,10 authentic documents/photos,6 exact charts.19 physical curated image references visually inspected through three contact sheets, with full-page/source follow-up for the constructed plan, two measured profiles, chain-saw photo, cost table and scientific core panel.

Corrections made before readiness: use the actual October1965 title page, not the administrative distribution-change sheet; include the138mile/1000/4600short-ton paragraph in the crop; keep the roof-arch caption; identify Fig32 as an AIR ventilation well, not a drinking-water well; use actual water-production film context and water-well text for G05; include the9July1963 shutdown sentence in its crop; use only the modern2021 core-photo panel2d rather than historic/3D or private-log panels. Rejected old reference files were removed from this delivery and kept locally under a REJECTED folder.

Prepared ImageGen inputs are physical files with hashes and explicit roles. All ten prompts are subject-specific and source-informed. Final aesthetics and semantic correctness of generated images remain untested because no generation has run. This is preparation QC, not a visual PASS for nonexistent images or a newly owner-approved canon.

D07 original GAO Highlights PDF is unavailable locally: externally checked download returned HTTP403. Its verified web text is not a substitute document image. Do not generate a fake GAO page. Nielsen2014 and the private historical drilling log are excluded from generation inputs/public image assets.19 curated files are the only image inputs; source PDFs/private copies are not in this ZIP/Git pack.

All32 V4 beats mapped. Existing moving footage stays primary. No artificial voice timestamps; precise AUDIO_TIMING_HOLD remains. Document focus targets are original-page OCR coordinates, not final yellow overlays: confirm alignment after final cropping. No whole-diagram yellow fill or strike-through.

No generation, paid credits, TTS, video generation, Resolve edit or V4 change performed. Suggested execution starts with one G02 proof and one G05 proof, then visual/factual review before the rest. No automatic batch execution is authorized by this preparation file.
'''
 (P/'qc/EDITORIAL_PREPARATION_QC.md').write_text(notes,encoding='utf-8')
 (P/'CANON_COMPATIBILITY.md').write_text('''# Shared HIA provenance canon / this preparation task

Read source: CHANNEL/PROVENANCE_AND_EDITING_CANON.md on main, Git blob84e6c15506a86f42d322bace065d7fee2ef52996.

The important shared truth rule is retained: generated/explanatory imagery cannot be labelled HISTORICAL SOURCE. Each prepared asset now has an explicit provenance_class independent of its chapter. G01–G10 are CONCEPT, C01–C06 are editorial graphics from cited data, documents are DOCUMENT, the actual1966 photograph is HISTORICAL_SOURCE and modern scientific images remain SCIENTIFIC_SOURCE.

Production IDs/source-basis notes stay metadata. Do not create new on-screen administrative badges. Historical year, PROPOSAL and NEVER DEPLOYED are substantive factual qualifiers where specified. No timeline/render engine is selected or changed by this image-preparation task; no Resolve/Remotion project was touched. No captions or endscreen work is part of this pack.

The proposed off-white/ink/blue-grey/ochre treatment is derived from these source references, not a claim of newly approved HIA channel colours. Final appearance requires a first generated proof and owner review. This pack cannot mark nonexistent generated images visually PASS.
''',encoding='utf-8')
 chapter_lines=['# All eight V4 chapters — preparation allocation','', '|Chapter|Primary prepared options|Existing motion remains primary|','|---|---|---|']
 for ch in ['CH01','CH02','CH03','CH04','CH05','CH06','CH07','CH08']:
  ids=[a['asset_id'] for a in assets if a['chapter']==ch]
  chapter_lines.append(f"|{ch}|{', '.join(ids)}|See Stage06 real-clip registry and32-beat placement map|")
 chapter_lines += ['', 'The32-beat map includes exact narration word cues and alternate context placements. Alternatives are not extra unique footage and must not cause repetitive reuse. CH08 now has genuine still/scientific references and prepared concepts; its Stage06 real moving-footage count stays0. No generated illustration will be counted as recovered archival motion.', '', 'D07 is source-image HOLD. Two Fig28/29 caption-rate OCR targets were not found exactly; do not guess highlight coordinates. Original profiles can be shown unmodified; exact rates remain locked in C04. All final marker geometry needs a check after the document crop. AUDIO_TIMING_HOLD continues.']
 (P/'CHAPTER_PLACEMENT_AND_GAPS.md').write_text('\n'.join(chapter_lines)+'\n',encoding='utf-8')
 shutil.copyfile(Path(__file__),P/'tools'/Path(__file__).name)
 print(json.dumps(q,indent=2));print('DOCUMENT_TARGETS',[(r['exact_search_text'],len(r['normalized_original_page_word_boxes'])) for r in targets])
if __name__=='__main__':main()
