"""Literal narration binding and delivery QC for R2. No generative API calls."""
import csv,json,re,hashlib,shutil,subprocess,zipfile,sys,requests,io,html
from pathlib import Path
from PIL import Image
import pymupdf
sys.stdout.reconfigure(encoding='utf-8')
R=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007');P=R/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R2';B=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def main():
 assets=json.loads((P/'ASSET_PRODUCTION_QUEUE.json').read_text());refs=json.loads((P/'REFERENCE_REGISTER.json').read_text())
 # Discard an unused source crop that also contained unrelated water-cavity material.
 reject=B/'qc/R2_REJECTED_FILES';reject.mkdir(exist_ok=True)
 for rel in ['references/R36_CONCLUSIONS.jpg','tools/camp_century_build_generation_pack.py','tools/camp_century_complete_references.py','tools/camp_century_finalize_generation_pack.py','tools/camp_century_prepare_reference_sources.py','tools/camp_century_render_reference_pages.py']:
  src=P/rel
  if src.exists():
   assert P.resolve() in src.resolve().parents
   dest=reject/src.name
   if not dest.exists():shutil.move(str(src),str(dest))
 refs=[r for r in refs if r['reference_id']!='R36_CONCLUSIONS']
 # Keep the actual publisher figure, but also acquire the high-resolution source PDF if possible.
 pdf=B/'sources/FIRN2021.pdf';upgrade={'url':'https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.578978/pdf'}
 try:
  if not pdf.exists():
   rr=requests.get(upgrade['url'],timeout=(15,35));rr.raise_for_status();pdf.write_bytes(rr.content)
  doc=pymupdf.open(pdf);pages=[i for i,p in enumerate(doc) if re.search(r'FIGURE\s*10\s*\|',p.get_text())]
  assert pages
  n=pages[0];page=doc[n];pix=page.get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),alpha=False)
  # Full authentic article page is additional backing, not another unique figure.
  path=B/'references'/f'FIRN2021_PDFPAGE_{n+1:03d}.png';pix.save(path)
  upgrade.update(status='ORIGINAL_PDF_ACQUIRED',sha256=sha(pdf),bytes=pdf.stat().st_size,figure10_pdf_page_1based=n+1,backing_page_path=str(path),note='Existing R33 is the same figure, not an additional source. Use original PDF for final graph export.')
 except Exception as e:upgrade.update(status='PDF_QUALITY_UPGRADE_HOLD_OFFICIAL_FIGURE_ALREADY_PHYSICAL',error=str(e))
 (P/'qc/R2_FIRN_PDF_QUALITY_RECEIPT.json').write_text(json.dumps(upgrade,indent=2))
 # Bind every asset to actual wording, not a guessed clock or a generic chapter.
 cues={
 'G01':'working settlement','G02':'cuts a long trench','G03':'buildings were only the beginning','G04':'Heat.','G05':'base required water','G06':'walls creep inward','G07':'trimming and removing','G08':'reached the bottom','G09':'ancient plants','G10':'using radar to study',
 'G11':'easier to cut than rock','G12':'special sleds','G13':'Spare parts','G14':'support forms','G15':'network of smaller passages','G16':'reactor arrived','G17':'electrical and heating system','G18':'holding up part','G19':'shrinking of empty space','G20':'Blowing snow','G21':'reactor hardware was taken out','G22':'wastes remained in the ice sheet','G23':'samples were stored','G24':'ancient ground',
 'D01':'published engineering report','D02':'layout included a dining hall','D03':'five point seven million','D04':'same tunnel sections at different dates','D05':'twenty thousand','D06':'Figure thirty-three','D07':'Government Accountability Office','D08':'published the images','D09':'nineteen sixty-six','D10':'Later studies found traces',
 'D11':'a medical facility, workshops','D12':'openings began to deform','D13':'sixteen inches','D14':'network of smaller passages','D15':'base required water','D16':'two nearby buildings','D17':'repeated mechanical troubles','D18':'planned before Project Iceworm','D19':'twenty-one study','D20':'moved between institutions',
 'C01':'one hundred thirty-eight miles','C02':'four thousand six hundred','C03':'five point seven million','C04':'twelve percent','C05':'six hundred missiles','C06':'dismantled and removed','C07':'thirty-four inches','C08':'planned before Project Iceworm','C09':'Every passage would have to remain open','C10':'within the Kingdom of Denmark','C11':'rejected in nineteen sixty-three','C12':'reactor hardware was taken out','C13':'scenario, not an observation','C14':'at least one hundred feet','C15':'figures measure different things','C16':'diesel generators'}
 beats=list(csv.DictReader((R/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv').open(encoding='utf-8-sig',newline='')))
 bybeat={r['beat_id']:r for r in beats};offset={};word=0
 for b in beats:offset[b['beat_id']]=word;word+=len(b['spoken_text_exact'].split())
 assert word==2931 and len(beats)==32
 placements=[];bad=[]
 for a in assets:
  query=cues[a['asset_id']];pat=r'(?<!\w)'+r'\s+'.join(re.escape(x) for x in query.split())+r'(?!\w)';found=None
  for bid in a['beat_ids']:
   text=bybeat[bid]['spoken_text_exact'];m=re.search(pat,text,re.I)
   if m:found=(bid,text,m);break
  if not found:bad.append((a['asset_id'],query,a['beat_ids']));continue
  bid,text,m=found;literal=text[m.start():m.end()]
  before=text[:m.start()];paragraph_start=before.rfind('\n\n')+2 if '\n\n' in before else 0
  next_break=text.find('\n\n',m.end());paragraph_end=len(text) if next_break<0 else next_break
  paragraph=text[paragraph_start:paragraph_end].strip()
  anchor_start=offset[bid]+len(before.split());anchor_end=anchor_start+len(literal.split())
  a.update(primary_cue_beat=bid,voice_cue_exact=literal,voice_context_exact=paragraph,global_word_in_0based=anchor_start,global_word_out_exclusive=anchor_end)
  a['status']='SOURCE_IMAGE_HOLD_DO_NOT_GENERATE' if not a['reference_ids'] else 'PREPARATION_READY_REFERENCES_REVIEWED_OUTPUT_NOT_GENERATED'
  placements.append({'asset_id':a['asset_id'],'chapter':bybeat[bid]['chapter'],'primary_beat':bid,'exact_voice_trigger':literal,'exact_voice_context':paragraph,'global_word_in_0based':anchor_start,'global_word_out_exclusive':anchor_end,'visual_purpose':a['title'],'source_references':';'.join(a['reference_ids']),'duration_design_budget':'4-9s; original documents6-12s when needed','actual_audio_in_sec':'','actual_audio_out_sec':'','timing_status':'AUDIO_TIMING_HOLD','edit_rule':'A contextual option, not a mandatory card; do not show several treatments of the same fact consecutively.'})
 assert not bad,bad
 csvout(P/'ASSET_NARRATION_PLACEMENT_CUES.csv',placements)
 for r in refs:r['visual_review']='CODEX_REVIEWED_SOURCE_SEQUENCE_AND_CORRECTED_CROPS_NOT_OWNER_STYLE_APPROVAL'
 (P/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2));csvout(P/'REFERENCE_REGISTER.csv',refs)
 (P/'ASSET_PRODUCTION_QUEUE.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
 csvout(P/'ASSET_PRODUCTION_QUEUE.csv',[{**a,**{k:';'.join(a[k]) for k in ['beat_ids','reference_ids','exact_screen_text','claim_ids']}} for a in assets])
 # Endings and transitions use previously prepared evidence as alternate choices, not new counts.
 alternatives={'CC07-S4-CH01-B03':('D02','The base was real'),'CC07-S4-CH06-B05':('D04;D13','Camp Century demonstrated'),'CC07-S4-CH07-B04':('D09;G08','drilled out of the ground'),'CC07-S4-CH08-B04':('D02;D04;D10','lasting evidence')}
 maps=list(csv.DictReader((P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv').open(encoding='utf-8-sig',newline='')))
 for b in maps:
  b['alternate_evidence_options']=alternatives.get(b['beat_id'],('',''))[0]
  q=alternatives.get(b['beat_id'],('',''))[1]
  if q:
   m=re.search(r'\s+'.join(re.escape(x) for x in q.split()),bybeat[b['beat_id']]['spoken_text_exact'],re.I);assert m,(b['beat_id'],q)
   b['alternate_exact_cue']=m.group(0)
  else:b['alternate_exact_cue']=''
  b['alternate_counting_rule']='Choose a suitable placement once; no extra source/image/footage count. Avoid repeating the identical view.'
 csvout(P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv',maps)
 # Chapter priority is evidence availability: more concepts where real motion is genuinely missing.
 lines=['# R2 preparation against the locked V4 narration','', '60 source-led options, not60 mandatory inserts or proof that the final film is covered. All60 have a literal narration trigger and global word position. No approved WAV was found in the project; seconds remain AUDIO_TIMING_HOLD.','', '|Chapter|Words|Estimated speech @145wpm|ImageGen options|Document/photo treatments|Data/logic diagrams|','|---|---:|---:|---:|---:|---:|']
 for ch in sorted({b['chapter'] for b in beats}):
  words=sum(int(b['words']) for b in beats if b['chapter']==ch);aa=[a for a in assets if a['chapter']==ch]
  counts=[sum(a['asset_id'].startswith(prefix) for a in aa) for prefix in ['G','D','C']]
  lines.append(f'|{ch}|{words}|{words*60/145:.1f}s|{counts[0]}|{counts[1]}|{counts[2]}|')
 lines+=['', 'The190 paragraph units are exact narration index entries, **not190 cuts** and not a requirement to generate a picture for every paragraph. Existing78 real motion clips stay the foundation. A typical explanatory insert has a4-9s design budget; source documents need6-12s when reading. These are pacing budgets, never fabricated audio timestamps.','', 'Distinct measurement tasks: C04 area loss12%/17%; C07 vertical clearance16/34in/year; C15 thermal10MW versus net electric rating1.56MW (V4 approximately1.5MW). They are not the same quantity, not one stacked energy chart and not a claimed efficiency.','', 'Primary-cue bindings are in ASSET_NARRATION_PLACEMENT_CUES.csv. Several treatments of one fact are alternatives: choose original evidence OR a brief explanation, or sequence them only when it adds understanding. Do not turn the film into60 consecutive paper cards.','', 'HOLD: D07 GAO original image still returns403. C06 exact rediscovery-year graphic is held: SCI24Fig3f distinguishes2017rediscovery from2019pilot analysis, while V4 narrates a2019inventory. Script V4 is untouched; do not silently promote that date to an undisputed new graphic. Original Fig10 forecast remains a model under assumptions, with DIFFERENT vertical scales.','', 'The design-criteria source includes an earlier100-person year-round requirement. D11 uses only its facility-functions list, not that row against V4’s later up-to200capacity. Planned and as-built records remain separate.','', 'No image/video generation, paid credits, TTS, Resolve changes or fake historical documents. No generated result or new owner-approved style canon is claimed.']
 (P/'CHAPTER_PLACEMENT_AND_GAPS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 readme='''# VIDEO007 CAMP CENTURY — expanded preparation R2

**60 prepared tasks:24 referenced ImageGen illustrations,20 authentic document/photo treatments,16 data/logic diagrams.** R1 remains unchanged.

- Open INDEX.html. Every asset has a specific subject, source image(s), short permitted labels, factual limit, provenance class, motion treatment and literal V4 narration trigger.
- ASSET_NARRATION_PLACEMENT_CUES.csv binds all60 options to exact phrases and global word positions. The32-beat map includes real moving clips and evidence alternatives; the190paragraph entries are an index, not a190-cut edit.
- See CHAPTER_PLACEMENT_AND_GAPS.md for distribution. Real motion remains primary. Choose the relevant explanation; do not insert every option or repeat nearly identical views.
- For ImageGen: inspect the exact attached references, use the24 prepared built-in calls, one asset per call. Rebase local paths with tools/prepare_imagegen_calls.py if unpacked elsewhere. The script only prepares arguments and never generates.
- Documents remain authentic scans. Graph values/categorical claims stay in data/VERIFIED_CHART_DATA.csv and editable diagrams; no made-up curves, stamps or generated report pages.
- D07 original GAO image is HOLD. An exact rediscovery-date caption in C06 is separately held for source chronology reconciliation; V4 is not edited.
- No image/video generation, paid credits, narration generation or Resolve edit. AUDIO_TIMING_HOLD until a locked WAV is available. First generated proof is still needed to validate the actual look.

References are files/excerpts, not a claim of dozens of independent archives. Private copyrighted research PDFs and full source movies are excluded. Attribution and source limitations are in RIGHTS_AND_EXCLUSIONS.md.
'''
 (P/'README.md').write_text(readme,encoding='utf-8')
 rights=(P.parent/'STAGE07_GENERATION_PREP_R1/RIGHTS_AND_EXCLUSIONS.md').read_text(encoding='utf-8')
 rights+='''\n## R2 additions\n\nR24: Fig3e ONLY, modern Copenhagen archived-sample photograph credited Andrew J.Christ, in Bierman et al2024, doi:10.5194/tc-18-4029-2024, CC BY4.0 https://creativecommons.org/licenses/by/4.0/ ; cropped. Historical panels a/b and private log remain excluded. R32 is Fig1a modern geographic map only; Daugherty1963 Fig1b excluded.\n\nR33: Vandecrux B.,Colgan W.,Solgaard A.M.,Steffensen J.P.,Karlsson N.B.(2021), Firn Evolution at Camp Century, Greenland:1966–2100, Front.EarthSci9:578978, Fig10, doi:10.3389/feart.2021.578978. CC BY4.0 https://creativecommons.org/licenses/by/4.0/ . Actual published model, not observations. Retain attribution, scenario names, time axis and the different vertical scales. Do not digitize imagined values or generate substitute curves.\n\nR20–23 andR37 are selected silent federal Army film frames with original Stage06 scene IDs/clip SHA256 and site/supply-chain separation. Different excerpts from a film/report do not become independent sources or add moving minutes.\n'''
 (P/'RIGHTS_AND_EXCLUSIONS.md').write_text(rights,encoding='utf-8')
 canon=(P/'CANON_COMPATIBILITY.md').read_text(encoding='utf-8').replace('G01–G10','G01–G24').replace('C01–C06','C01–C16');(P/'CANON_COMPATIBILITY.md').write_text(canon,encoding='utf-8')
 htmlpath=P/'INDEX.html';s=htmlpath.read_text(encoding='utf-8').replace('PREPARATION_READY_PENDING_NEW_REFERENCE_VISUAL_REVIEW','PREPARATION_READY_REFERENCES_REVIEWED_OUTPUT_NOT_GENERATED')
 for a in assets:
  needle=f'<h3>{a["asset_id"]}: {html.escape(a["title"])}</h3>'
  s=s.replace(needle,needle+f'<p><b>Exact narration cue:</b> {html.escape(a["voice_cue_exact"])} · {a["primary_cue_beat"]}</p>')
 htmlpath.write_text(s,encoding='utf-8')
 q=json.loads((P/'qc/PREPARATION_QC.json').read_text());q.update(physical_reference_files=len(refs),new_reference_review='CODEX_VISUALLY_REVIEWED_ALL_NEW_REFERENCE_SHEETS_AND_CORRECTED_CROPS',literal_cue_bindings_verified=len(placements),spoken_words_unchanged=word,owner_style_approval='NOT_CLAIMED',generation_outputs=0,readiness='24REFERENCED_IMAGEGEN_JOBS_PREPARED_NOT_GENERATED;D07SOURCE_HOLD;C06EXACT_DATE_HOLD')
 (P/'qc/PREPARATION_QC.json').write_text(json.dumps(q,indent=2))
 (P/'qc/EDITORIAL_PREPARATION_QC.md').write_text('\n'.join(lines)+'\n\nAll37 current reference files inspected through base/new reference sheets; corrected full Greenland-map crop and power-ratings strip checked separately. No generated output has been reviewed because none exists. Exact V4 hashes are unchanged.\n',encoding='utf-8')
 # Prepare the portable call builder for24 jobs; it performs no generation.
 runner=P/'tools/prepare_imagegen_calls.py';t=runner.read_text(encoding='utf-8').replace('len(calls)==10','len(calls)==24').replace('VALID:10 jobs','VALID:24 jobs');runner.write_text(t,encoding='utf-8')
 shutil.copyfile(Path(__file__),P/'tools'/Path(__file__).name)
 print(json.dumps(q,indent=2));print('LITERAL_CUES_VERIFIED',len(placements));print('FIRN_SOURCE_PDF',upgrade['status'],upgrade.get('figure10_pdf_page_1based'))
if __name__=='__main__':main()
