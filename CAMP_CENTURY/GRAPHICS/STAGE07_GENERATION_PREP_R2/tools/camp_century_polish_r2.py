import json,csv,hashlib,io,shutil
from pathlib import Path
from PIL import Image
import pymupdf
R=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007');P=R/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R2';B=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
def csvout(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
refs=json.loads((P/'REFERENCE_REGISTER.json').read_text());pdf=B/'sources/FIRN2021.pdf'
if pdf.exists():
 doc=pymupdf.open(pdf);page=doc[11];r=page.rect;norm=(.075,.438,.925,.662);clip=pymupdf.Rect(norm[0]*r.width,norm[1]*r.height,norm[2]*r.width,norm[3]*r.height)
 pix=page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=clip,alpha=False);im=Image.open(io.BytesIO(pix.tobytes('png')))
 p=P/'references/R33_FIRN_FORECAST.jpg';im.save(p,quality=96,subsampling=0)
 ref=next(r for r in refs if r['reference_id']=='R33_FIRN_FORECAST');ref.update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),width=im.width,height=im.height,source_url='https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.578978/pdf',source_locator='Original PDF page12, Fig10 and full caption; normalized crop'+str(norm)+'; original PDF SHA256'+hashlib.sha256(pdf.read_bytes()).hexdigest(),visual_review='ORIGINAL_PDF_FIGURE_UPGRADE_PENDING_FINAL_CROP_CHECK')
(P/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2));csvout(P/'REFERENCE_REGISTER.csv',refs)
maps=list(csv.DictReader((P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv').open(encoding='utf-8-sig',newline='')));bm={r['beat_id']:r for r in maps}
units=list(csv.DictReader((P/'V4_PARAGRAPH_VISUAL_UNITS.csv').open(encoding='utf-8-sig',newline='')))
for u in units:
 u['alternate_evidence_options']=bm[u['beat_id']]['alternate_evidence_options']
 u['unit_role']='Narration indexing/search only; NOT an individual cut instruction.'
csvout(P/'V4_PARAGRAPH_VISUAL_UNITS.csv',units)
# Replace inherited R1-only QC wording; the first four control points stay applicable.
q=json.loads((P/'qc/PREPARATION_QC.json').read_text());q['reference_quality_upgrade']='R33 rendered from actual author PDF Fig10 with full caption and different-scales note';q['comparison_to_R1']={'imagegen_jobs':'+14 (10 to24)','document_photo_treatments':'+10 (10 to20)','data_logic_diagrams':'+10 (6 to16)','total_asset_briefs':'+34 (26 to60)'}
(P/'qc/PREPARATION_QC.json').write_text(json.dumps(q,indent=2))
# A selection plan explains intended placement instead of turning the library into a card deck.
text='''# R2 editorial selection priority

This is a production library, not an instruction to show all60 assets. Every option has a literal V4 narration trigger;24 generation jobs are prepared, not executed. Several treatments of the same fact are intentional alternatives, not extra unique footage.

1. CH01: use genuine camp activity first; G01 is a short spatial explanation. Save the full measured-profile read for CH06. D02 can establish that the real base existed when the narration contrasts it with the unbuilt proposal.
2. CH02: retain varied real convoy actions. C01 identifies the138mile supply leg; C02 handles actual tonnage. G12/G13 are optional explanations of oversized loads and support burden. G11 makes the cuttable-material transition.
3. CH03: original excavation and framing remain the dominant pictures. G02 explains the construction order; choose D12 or G14 for premature form removal. D02 establishes actual layout. Choose D14 or G15 for overhead services, not both back-to-back by default.
4. CH04: show real module transport/install. D03/C03 handle cost; C15 separately distinguishes thermal power from electricity. Choose G05/D15 to explain water supply, then D16/G18 for the local wastewater problem. D17 is actual mechanical-performance evidence. D18/C08 clarify chronology, not a missile-funding theory.
5. CH05: public camp life first, followed by C05 proposal totals. C09 explains support burden; C10 gives sovereignty/political context. C11 closes the proposal without fabricated missile deployments or a fake cancellation document. No operational Iceworm imagery is generated.
6. CH06: the main evidence sequence is D04 followed by C04/C07 only as needed. Choose G19 for functional clearance, D06 or G07 for trimming work, G20 for drifting entrances. Do not multiply the same arch shot to fake variety.
7. CH07: actual1964 removal footage stays primary. C12/G21 distinguish removed plant from remaining structures. D19 is the actual2021 graph; C13 explains scenario versus observation without invented curves or a present spill. D07 GAO remains source-image HOLD.
8. CH08: genuine1966 drilling still and modern sample photographs anchor the story. G08/G24 explain depth/material origin; D20/G23 explain archive preservation without a hard rediscovery-year label. G10 can explain radar before the untouched actual NASA composite. End with selected real evidence, not a repeat of every graphic.

Exact seconds require the locked narration WAV. Current estimated speech length is20.21minutes at145wpm; this is not an actual final runtime. The13:18.7selected archival bank is not automatically13:18.7 of final matched timeline coverage.190paragraph units are an index, not190 cuts. No extra unique-motion minutes are credited to generated stills or document treatments.
'''
(P/'EDITORIAL_SELECTION_PRIORITY.md').write_text(text,encoding='utf-8')
shutil.copyfile(Path(__file__),P/'tools'/Path(__file__).name)
print('POLISHED_R2',len(refs),'references',len(units),'narration units')
