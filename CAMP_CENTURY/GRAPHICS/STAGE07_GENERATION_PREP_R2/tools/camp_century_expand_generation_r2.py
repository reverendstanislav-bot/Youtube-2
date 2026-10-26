"""Expand Camp Century preparation by narration function. Does not generate any image."""
import json,csv,hashlib,shutil,subprocess,io,requests,sys,html,re
from pathlib import Path
from PIL import Image,ImageDraw
import pymupdf
sys.stdout.reconfigure(encoding='utf-8')
REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
OLD=REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R1'
P=REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R2'
B=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
if not P.exists():shutil.copytree(OLD,P)
refs=json.loads((OLD/'REFERENCE_REGISTER.json').read_text());assets=json.loads((OLD/'ASSET_PRODUCTION_QUEUE.json').read_text())
ARMY='https://icedrill.org/sites/default/files/477706.pdf';SCI='https://tc.copernicus.org/articles/18/4029/2024/';FIRN='https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.578978/full'
PD='Selected actual Camp Century US Army federal report image/text; preserve original locator and contextual caption'
CC='Bierman et al2024,The Cryosphere18,4029-4052,doi:10.5194/tc-18-4029-2024; CC BY4.0 https://creativecommons.org/licenses/by/4.0/ ; cropped; photo panels3c-g credited Andrew J.Christ; do not reuse private/historic panels'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(rid,im,title,url,loc,rights,role='FACT_AND_GEOMETRY'):
 path=P/'references'/(rid+'.jpg');im.convert('RGB').save(path,quality=94,subsampling=0)
 refs.append({'reference_id':rid,'file':'references/'+path.name,'sha256':h(path),'width':im.width,'height':im.height,'title':title,'source_url':url,'source_locator':loc,'rights':rights,'input_role':role,'visual_review':'NEW_REFERENCE_PENDING_SEQUENCE_REVIEW'})
def pdf(rid,file,n,box,title,rights=PD):
 doc=pymupdf.open(B/'sources'/file);page=doc[n-1];r=page.rect
 clip=pymupdf.Rect(box[0]*r.width,box[1]*r.height,box[2]*r.width,box[3]*r.height)
 pix=page.get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),clip=clip,alpha=False)
 ref(rid,Image.open(io.BytesIO(pix.tobytes('png'))),title,SCI if file.startswith('SCI') else ARMY,f'PDF page{n}; normalized source crop{box}',rights)
clips={r['scene_id']:r for r in csv.DictReader((REPO/'CAMP_CENTURY/ARCHIVE/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig',newline=''))}
for rid,cid,title in [('R20_SLED_LOAD','CC07-C004','Loaded sleds at Camp Century supply staging; NOT inside base'),('R21_HEAVY_SWING','CC07-C008','Actual Camp Century heavy-swing route; supply-chain location'),('R22_PM_MODULE','CC07-C031','Actual PM-2A vessel load on road transporter; supply chain'),('R23_CORRIDOR','CC07-C028','Actual vehicle in Camp Century main passage'),('R37_REMOVAL','CC07-C067','Actual1964 PM-2A removal lift; source print severely magenta')]:
 r=clips[cid];t=float(r['cut_seconds'])/2
 result=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',r['cut_filename'],'-frames:v','1','-vf','scale=640:480,setsar=1','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True,check=True)
 ref(rid,Image.open(io.BytesIO(result.stdout)),title,r['source_url'],f"{cid} output midpoint{t:.3f}s; source IN{r['start_tc']}; SHA256{r['cut_sha256']}",'Stage06 selected silent Army picture; source-specific rights receipt remains applicable','OBJECT_APPEARANCE_AND_VERIFIED_LOCATION_CONTEXT')
pdf('R24_FROZEN_ARCHIVE','SCI24.pdf',6,(.08,.43,.38,.605),'Fig3e modern photograph of Copenhagen archived samples; caption period is storage history, NOT photo date',CC)
pdf('R25_PREMATURE_FORMS','ARMY65_TR174.pdf',41,(.08,.07,.94,.51),'Actual Fig25: rapid deformation after forms removed too soon, printed33')
pdf('R26_UTILITY_LINES','ARMY65_TR174.pdf',54,(.08,.06,.94,.62),'Actual Fig36: communication trench overhead utility lines, printed46')
pdf('R27_WATER_WELL','ARMY65_TR174.pdf',53,(.08,.06,.94,.59),'Actual Fig35 water well looking down, printed45; NOT ventilation air well')
pdf('R28_SEWAGE_PROFILE','ARMY65_TR174.pdf',51,(.50,.49,.96,.765),'Actual Fig34: SEWAGE-contaminated snow near sump, printed43; not nuclear fallout')
pdf('R29_MAIN_HEIGHT_TABLE','ARMY65_TR174.pdf',45,(.07,.055,.95,.97),'Actual TableII main-trench measurements, printed37; height loss, not area percentage')
pdf('R30_SIDE_HEIGHT_TABLE','ARMY65_TR174.pdf',46,(.07,.055,.95,.96),'Actual TableII continued, printed38; retain headings and actual average rows')
pdf('R31_PLANT_PLANNING','ARMY65_TR174.pdf',39,(.08,.265,.95,.57),'Primary plant-planning chronology, printed31; precedes the formal Iceworm proposal')
pdf('R32_GREENLAND_ONLY','SCI24.pdf',3,(.08,.075,.498,.52),'Full modern author Fig1a geographic context ONLY; excludes Daugherty1963 Fig1b',CC)
pdf('R34_TURBINE_RECORD','ARMY65_TR174.pdf',57,(.07,.06,.95,.94),'Primary PM-2A service/performance record, printed49; mechanical troubles not a meltdown')
pdf('R35_DESIGN_CRITERIA','ARMY65_TR174.pdf',35,(.08,.06,.95,.76),'Original design criteria and intended facilities, printed27; distinguish planned from as-built')
pdf('R38_POWER_RATINGS','ARMY65_TR174.pdf',55,(.08,.645,.94,.715),'Original PM-2A characteristics: thermal power and net electrical rating, printed47; different quantities, not an efficiency calculation')
url='https://www.frontiersin.org/files/Articles/578978/xml-images/feart-09-578978-g010.webp'
source=B/'sources/FIRN2021_FIG10.webp';download={}
try:
 if not source.exists():
  r=requests.get(url,timeout=(15,40));r.raise_for_status();source.write_bytes(r.content)
 im=Image.open(source)
 ref('R33_FIRN_FORECAST',im,'Vandecrux et al2021 Fig10: modeled debris depth and meltwater penetration; different vertical scales',url,'Official author Fig10, simulation NOT observation','Vandecrux,Colgan,Solgaard,Steffensen,Karlsson2021,Front.EarthSci9:578978,Fig10,doi:10.3389/feart.2021.578978; CC BY https://creativecommons.org/licenses/by/4.0/ ; retain labels, scenarios and DIFFERENT VERTICAL SCALES','ACTUAL_PUBLISHED_SCIENTIFIC_GRAPH_NOT_IMAGEGEN_DATA_INVENTION')
 download={'source_id':'FIRN2021_FIG10','url':url,'local_source':str(source),'sha256':h(source),'bytes':source.stat().st_size,'status':'DOWNLOADED'}
except Exception as e:download={'source_id':'FIRN2021_FIG10','url':url,'status':'SOURCE_HOLD','error':str(e)}
R={r['reference_id']:r for r in refs}
def A(aid,ch,bs,title,rs,brief,labels,claims,limit,motion,priority='P0'):
 route='IMAGEGEN_REFERENCED_ILLUSTRATION' if aid.startswith('G') else 'AUTHENTIC_SOURCE_NO_IMAGEGEN' if aid.startswith('D') else 'DATA_LOCKED_CHART_NO_IMAGEGEN'
 row={'asset_id':aid,'production_route':route,'chapter':ch,'beat_ids':[f'CC07-S4-{ch}-B{n:02d}' for n in bs],'title':title,'reference_ids':rs,'brief':brief,'exact_screen_text':labels,'claim_ids':[f'CC07-S4-{n:03d}' for n in claims],'historical_limit':limit,'motion_after_approval':motion,'priority':priority,'audio_status':'AUDIO_TIMING_HOLD','timing':'Exact V4 phrase anchors; duration window is a design budget, not a voice timecode','status':'NEW_BRIEF_PENDING_REFERENCE_REVIEW','prompt_file':'','provenance_class':'CONCEPT' if aid.startswith('G') else 'EDITORIAL_GRAPHIC_FROM_CITED_DATA' if aid.startswith('C') else 'SCIENTIFIC_SOURCE' if aid in ['D19','D20'] else 'DOCUMENT','rendered_metadata_text':'NONE; production/source-control notes stay in metadata'};assets.append(row)
def G(n,ch,bs,title,rs,brief,labels,claims,limit,motion,priority='P0'):A(f'G{n:02d}',ch,bs,title,rs,brief,labels,claims,limit,motion,priority)
G(11,'CH02',[4],'The material they could cut',['R16_PETER','R25_PREMATURE_FORMS'],'One informative close cross-section of compacted snow/firn under an ordinary snow surface, with a shallow open trench and the actual Peter cutter. Contrast compacted snow with a small schematic bedrock swatch clearly separated as a material comparison, never as a real local geological section. No cave, TBM, blast, glacier crevasse or flowing-water cavern.',['SNOW AND FIRN','NOT BEDROCK'],[19,20],'Qualitative material comparison; not a claim of a measured bedrock depth at the camp.','4-6s reveal surface texture then the open cut; one stable camera.')
G(12,'CH02',[2],'Loads needed special sleds',['R20_SLED_LOAD','R21_HEAVY_SWING'],'A complete period engineering illustration of a long awkward construction load carried by a tractor-drawn sled train. Preserve the runners, cargo supports, load scale and equipment silhouette visible in the references. Indicate why a long prefabricated load needs support along its length, without giving fabrication dimensions, new mechanical designs or an invented load capacity.',['OVERSIZED LOAD','SLED TRANSPORT'],[13,14],'Camp Century supply chain, not footage inside the base; no invented measured sled blueprint.','6-8s follow the load from front support to rear support; no exploded-view fantasy.')
G(13,'CH02',[3],'The convoy had its own supply needs',['R21_HEAVY_SWING','R20_SLED_LOAD'],'An editorial logistics illustration of one actual-style tractor convoy carrying construction material plus ordinary fuel and spare-part cargo. Make the physical support burden legible with two small cargo details, not interface panels. No precise consumption, number of trips, breakdown event, calendar or invented cargo quantities.',['FUEL','SPARES','CONSTRUCTION CARGO'],[13,15,16],'Qualitative recurring supply burden; no guessed fuel-economy calculation.','5-7s move from tractor to support cargo, then back to the entire convoy.')
G(14,'CH03',[2,3],'Removing support too soon',['R25_PREMATURE_FORMS','R03_ARCH'],'A restrained cutaway explaining the role of temporary snow-arch forms. Show a supported snow arch and a separate, modestly deformed opening after early form removal. The visual direction follows the authentic Fig25. No total collapse, casualties, precise elapsed time or asserted dimensions; do not make all roof types the same.',['SUPPORT FORM','DEFORMED OPENING'],[21,23],'Mechanism illustration anchored in one documented form-removal problem, not a universal camp history.','6-8s reveal the support, then the changed opening; stable silhouettes, no wobble.')
G(15,'CH03',[3,4],'Services also occupied the trench',['R26_UTILITY_LINES','R18_ROOM'],'A clear period-report perspective into an ordinary communication trench showing a plain prefab room beside overhead utility lines, using the exact kinds of suspended lines visible in the reference. Separate the room envelope, walkway and services clearly; avoid dense fictional pipe networks, digital controls, wires through solid ice or invented electrical schematics.',['ROOM','PASSAGE','UTILITIES'],[24,26],'Appearance/space explanation only; not an installation or electrical-wiring plan.','5-7s focus once from room roof to overhead lines; keep geometry steady.')
G(16,'CH04',[2],'A power station arrived in pieces',['R22_PM_MODULE','R20_SLED_LOAD'],'A finished technical-report illustration of externally visible modular plant cargo moving on actual-style trailers and sleds. Use the large cylindrical enclosure and ordinary transport framing as appearance references. Explain modular transport without showing reactor internals, fuel, operating components or an invented assembly sequence. No exact package count unless separately verified.',['MODULAR LOAD','TRANSPORT'],[28,30],'Transport concept, not an operating-reactor design or an actual transport photograph.','5-7s follow an external module onto a loaded sled; no speculative exploded reactor.')
G(17,'CH04',[1,2],'One plant served many ordinary functions',['R02_PLAN','R22_PM_MODULE'],'A high-level editorial view of a small camp plant building connected by two simple qualitative paths to ordinary lit/heated prefab rooms. The paths stand for electricity and heat; no reactor internals, component circuit, temperatures, power-flow measurements, radiation beam or weapons imagery. Room functions and building outlines come from the actual plan.',['ELECTRICITY','HEAT','CAMP SERVICES'],[27,28],'Functional relationship only; no operating instructions, measured flow or claim that Iceworm financed it.','5-7s reveal the plant and two service relationships with restrained line masks.')
G(18,'CH04',[4],'The local foundation problem',['R28_SEWAGE_PROFILE','R10_SUMP','R02_PLAN'],'One local, qualitative cross-section around the wastewater sump and two neighboring prefab buildings. Indicate warmed supporting snow and modest localized settlement while the more distant camp remains intact. Keep sewage separate from drinking water and reactor components. No explosion, deaths, campwide sinkhole, molten reactor or radioactive river.',['WASTEWATER','LOCAL SETTLEMENT'],[34,36,37],'Specific local sewage/heat problem, not a recreation of an entire camp collapse; not to scale.','6-8s focus from sump influence to the two nearby supports; restrained change only.')
G(19,'CH06',[1,2],'Lost clearance has a practical cost',['R23_CORRIDOR','R06_PROFILES'],'A period technical illustration of a human and a small actual-style tracked vehicle inside an arched passage, showing why a reduced opening restricts usable headroom and passage. Keep people and machine proportions consistent with the corridor photograph. A thin comparison outline may indicate the former space, without dates, numerical scale or invented survey points.',['USABLE CLEARANCE'],[49,52,53],'Functional qualitative explanation, not a new measured profile or an accident.','5-7s move attention from arch crown to the vehicle clearance; no camera shake.')
G(20,'CH06',[4],'Snow could bury the entrance',['R23_CORRIDOR','R21_HEAVY_SWING'],'A surface access ramp entering a snow trench, with a restrained wind-blown accumulation building up at the ramp entrance. Use ordinary period tracks and the actual-style portal. Explain obstruction of access, not an avalanche, natural ice cave, sudden structural disaster, exact storm or measured snow depth.',['ACCESS RAMP','DRIFTING SNOW'],[56],'Qualitative documented access problem; weather field is illustrative, not a reconstruction of a dated event.','5-7s reveal shallow accumulation at the entrance with a stable view.')
G(21,'CH07',[2],'Removed plant, remaining infrastructure',['R37_REMOVAL','R02_PLAN'],'A clear high-level historical comparison: an external plant module being taken away above ground, while a simple cutaway retains ordinary buried building structures and waste areas. Follow the actual lift silhouette. Show no buried reactor core, nuclear warheads, leaking glowing barrels, detailed disposal layout or invented contaminated area.',['PLANT REMOVED','STRUCTURES REMAINED'],[59,62],'Explains the distinction in the narration; does not certify that every item of hardware or waste had the same fate.','6-8s follow the actual-shaped lifted module, then reveal only remaining non-operational infrastructure.')
G(22,'CH07',[2,3],'Burial is not disappearance',['R14_RADAR_2024','R15_DRILL_1966'],'A quiet snow/firn section showing abandoned structural remnants beneath accumulated snow. Add a simple unobtrusive comparison surface to explain continued burial qualitatively. No precise yearly depth curve, present-day liquid plume, exposed contaminated river or forecast catastrophe. No working rooms, lights or people under the modern surface.',['BURIED REMAINS'],[62,63,64],'Historical concept; not an observed present spill or a prediction of an exact exposure year.','5-7s reveal the surface and buried structures; no invented accelerated melt animation.')
G(23,'CH08',[2],'A sample survived in an archive',['R24_FROZEN_ARCHIVE','R13_CORE_2021'],'An informative modern editorial illustration of frozen sediment-bearing samples preserved in plain labelled containers and storage boxes. Use the authentic archive photograph for material, container shape and the modest scientific setting. Labels must be limited to the single permitted phrase; no invented accession number, government seal, discovery year, researcher identity or exact laboratory architecture.',['ARCHIVED SAMPLE'],[68,69],'Archive preservation concept; exact rediscovery date is source-conflicted and must not appear.','5-7s move from stored container to sample texture; do not fabricate a rediscovery reenactment.')
G(24,'CH08',[1,2],'The sample came from below the ice',['R13_CORE_2021','R15_DRILL_1966'],'A large, clear conceptual close-section of ice transitioning to frozen basal sediment at the ground interface. Grounded brown-grey granular material follows the actual core interior. Avoid recognizable plant species, invented fossil forms, numerical ages or a claim that the sample came from a camp room or meltwater.',['ICE','BASAL SEDIMENT'],[66,67,69],'Conceptual material origin; not a fabricated scientific specimen photograph or microscopy image.','5-7s reveal the interface and the sediment-bearing part of the sample.')
DOCS=[
 (11,'CH03',[3],'What the design called for',['R35_DESIGN_CRITERIA'],'Original design-criteria list. Show two or three relevant intended functions, with the DESIGN CRITERIA context intact. Do not present planned criteria as a verified as-built room inventory.',[24,25],'Authentic requirements, not generated meeting notes.'),
 (12,'CH03',[3],'The photographed early-form problem',['R25_PREMATURE_FORMS'],'Use actual Fig25 and its full caption. No synthetic collapse effect. Let the photograph explain the documented deformation after early form removal.',[23],'One documented problem; no universal failure or casualties.'),
 (13,'CH06',[2],'Actual vertical-clearance measurements',['R29_MAIN_HEIGHT_TABLE','R30_SIDE_HEIGHT_TABLE'],'Show the actual TableII headings, height measurement definition and average rows. Distinguish vertical closure from the area-profile percentages. Use a readable crop and sequential row focus.',[52,53],'Inches of height per year; not percentages of floor area or identical values for every trench.'),
 (14,'CH03',[3],'Utilities in the actual passage',['R26_UTILITY_LINES'],'Use the actual Fig36 overhead-line photograph with original caption. Focus on the services taking up space; do not generate wires over it.',[24,26],'A still, not newly recovered moving footage or a wiring diagram.'),
 (15,'CH04',[3],'The real water well',['R27_WATER_WELL'],'Use actual Fig35 looking down the water well; retain the caption and contrast with the separate wastewater discussion. Fig32 air well is not a drinking-water source.',[33],'Water supply picture, not an image of sewage or reactor fuel.'),
 (16,'CH04',[4],'A measured local sewage profile',['R28_SEWAGE_PROFILE'],'Use the authentic Fig34 sketch and its sewage-contaminated-snow caption. No full yellow diagram fill; a small focus on the original local profile only.',[34,36,37],'Sewage-contaminated snow; not a diagram of radioactive fallout or a reactor meltdown.'),
 (17,'CH04',[4],'The primary machinery-performance record',['R34_TURBINE_RECORD'],'Read the relevant turbine-generator service paragraph and retain its original documentary context. No invented repair log, explosion or plant-failure reenactment.',[38],'Mechanical service trouble, not a documented nuclear accident.'),
 (18,'CH04',[4],'Planning came before the missile proposal',['R31_PLANT_PLANNING'],'Use the primary October1958 ALCO design-study planning paragraph. This supports the sequence in V4; do not imply the later Iceworm proposal financed the original plant.',[39],'Actual plant planning record; no fake Iceworm authorization page.'),
 (19,'CH07',[3],'The actual2021 model result',['R33_FIRN_FORECAST'] if 'R33_FIRN_FORECAST' in R else [],'Use untouched published Fig10 with its modeled/scenario qualifiers, author credit and different vertical scales. Do not treat model curves as observations or compare the two panels as if they share a scale.',[64],'2021 modeled result under assumptions, not proof of zero future risk.'),
 (20,'CH08',[2],'Actual modern archive photograph',['R24_FROZEN_ARCHIVE'],'Use the modern Copenhagen sample-storage photograph, author credit and publication context. Do not label the photo1966 or attach an exact rediscovery date.',[68,69],'Storage history in the caption is not the photo capture date.')]
for n,ch,bs,title,rs,brief,cs,limit in DOCS:A(f'D{n:02d}',ch,bs,title,rs,brief,[],cs,limit,'6-10s readable original-source view; one motivated crop/focus; small text-span marker only when verified, no full-diagram fill.')
CHARTS=[
 (7,'CH06',[2],'Height loss, separately from area loss',['R29_MAIN_HEIGHT_TABLE','R30_SIDE_HEIGHT_TABLE'],['MAIN PASSAGE','SIDE TRENCHES','INCHES PER YEAR'],[52,53],'Zero-baseline bars16 and34; explicitly average vertical closure, not area percentages.'),
 (8,'CH04',[4],'Do not reverse the causal sequence',['R31_PLANT_PLANNING'],['PLANT PLANNING','LATER MISSILE PROPOSAL'],[39],'Sequence diagram, not an asserted financial link or a fabricated funding approval. Use no exact proposal year without separate evidence.'),
 (9,'CH05',[3],'A larger system meant more support',['R02_PLAN','R26_UTILITY_LINES'],['MAINTENANCE','POWER','COMMUNICATIONS','CREWS'],[41,47],'Qualitative support demands from V4; not a literal deployment map, engineered missile network or multiplied cost calculation.'),
 (10,'CH05',[3],'A research base was not political consent',['R32_GREENLAND_ONLY'],['GREENLAND','KINGDOM OF DENMARK','RESEARCH BASE'],[11,47],'Geographic/sovereignty context. No missile routes, targeting geometry, invented agreement or assertion that engineering demonstration granted weapons consent.'),
 (11,'CH05',[4],'The proposal ended without deployment',['R02_PLAN'],['PROPOSED','NEVER DEPLOYED'],[48,57],'Attribute1963 rejection to the later cited study; no fake cancellation memo or imagery of installed missiles.'),
 (12,'CH07',[2],'What was removed and what remained',['R37_REMOVAL','R02_PLAN'],['PLANT HARDWARE REMOVED','STRUCTURES AND WASTES REMAINED'],[59,62],'Categorical contrast only; no waste quantity estimate, buried operating reactor or complete item inventory.'),
 (13,'CH07',[2,3],'A scenario is not an observed spill',['R33_FIRN_FORECAST'] if 'R33_FIRN_FORECAST' in R else ['R14_RADAR_2024'],['MODELED SCENARIO','OBSERVATION'],[63,64],'Do not invent a common numeric axis, present-day spill, zero-risk guarantee or exact exposure year. Preserve assumptions and model/observation distinction.'),
 (14,'CH08',[1,3],'Two very different depth statements',['R14_RADAR_2024','R15_DRILL_1966'],['2024: AT LEAST30m','1966 CORE: MORE THAN1000m'],[67,73],'Different dates and different objects. Use inequality callouts with source context, NOT finite bars implying exact depths or a single measured simultaneous profile.'),
 (15,'CH04',[2],'Reactor heat is not delivered electricity',['R38_POWER_RATINGS'],['THERMAL POWER','NET ELECTRICAL RATING'],[31,32],'10MW thermal versus1.56MW net electrical rating (V4 narrates roughly1.5MW). Separate clearly identified quantities, not stacked parts, not net measured output, not an inferred efficiency or reactor-design diagram.'),
 (16,'CH04',[1,4],'Two kinds of power-supply burden',['R21_HEAVY_SWING','R04_BUDGET'],['FUEL DELIVERY','PLANT INVESTMENT','MAINTENANCE'],[27,29,30,38],'Qualitative engineering trade-off, not a life-cycle-cost model, fuel saving estimate, ROI or proof of a single motive.')]
for n,ch,bs,title,rs,labels,cs,limit in CHARTS:A(f'C{n:02d}',ch,bs,title,rs,'Build an editable restrained diagram from the exact narration categories or supplied data. Keep labels short, readable and geometrically stable; use physical/geographic context instead of dashboard cards.',labels,cs,limit,'4-7s ordered semantic reveal; no bouncing counters, decorative HUD, false intermediate values or automatic slide transitions.')
assert len(assets)==60
# Fix known date conflict in R1 context without altering the locked V4 script.
for a in assets:
 if a['asset_id']=='G10':a['beat_ids']=['CC07-S4-CH08-B02','CC07-S4-CH08-B03']
 if a['asset_id'] in ['G23','D20']:a['beat_ids']=['CC07-S4-CH08-B01']
 if a['asset_id']=='D16':a['beat_ids']=['CC07-S4-CH04-B03','CC07-S4-CH04-B04']
 if a['asset_id']=='D11':a['historical_limit']+=' The criteria page mentions a100-person year-round design criterion, not the later200-person capacity in V4. Crop/show the functional-facility list only; never use that100-person line as evidence for the200-person narration.'
 if a['asset_id']=='C06':
  a['historical_limit']+=' SOURCE_CONFLICT_HOLD for an exact rediscovery date: SCI24Fig3f labels2017 rediscovery and2019pilot analysis, while V4 narrates2019. Do not render an undisputed2019rediscovery event.'
 for rid in a['reference_ids']:assert rid in R,(a['asset_id'],rid)
 if not a['reference_ids']:a['status']='SOURCE_IMAGE_HOLD_DO_NOT_GENERATE'
 elif a['asset_id'] not in ['D07']:a['status']='PREPARATION_READY_PENDING_NEW_REFERENCE_VISUAL_REVIEW'
style=(OLD/'prompts/G01.txt').read_text(encoding='utf-8').split('Style/medium: ',1)[1].split('\nText (verbatim',1)[0]
payload=[]
for a in assets:
 if a['production_route']=='IMAGEGEN_REFERENCED_ILLUSTRATION':
  a['prompt_file']='prompts/'+a['asset_id']+'.txt'
  inputs='\n'.join(f'Image{k+1}: {rid}: {R[rid]["title"]}. Role: {R[rid]["input_role"]}.' for k,rid in enumerate(a['reference_ids']))
  prompt=f'Use case: scientific-educational\nAsset type: full-frame16:9 documentary explanatory illustration\nPrimary request: {a["brief"]}\nInput images:\n{inputs}\nStyle/medium: {style}\nText (verbatim, no other text): '+ '; '.join('"'+s+'"' for s in a['exact_screen_text'])+f'\nFactual boundary: {a["historical_limit"]}\nComplete composition, integrated labels, no empty containers or render/production metadata.\n'
  (P/a['prompt_file']).write_text(prompt,encoding='utf-8')
  payload.append({'asset_id':a['asset_id'],'call_status':'PREPARATION_ONLY_DO_NOT_EXECUTE','tool':'image_gen.imagegen','arguments':{'prompt':prompt,'referenced_image_paths':[str(P/R[rid]['file']) for rid in a['reference_ids']],'transparent_background':False},'output_intent':a['asset_id']+'_R2.png'})
 else:
  a['prompt_file']='prompts/'+a['asset_id']+'_PRODUCTION_BRIEF.md'
  (P/a['prompt_file']).write_text(f'# {a["asset_id"]} — {a["title"]}\n\nRoute: {a["production_route"]}\n\n{a["brief"]}\n\nReferences: '+(', '.join(a['reference_ids']) or 'SOURCE HOLD')+f'\n\nExact text: {"; ".join(a["exact_screen_text"])}\n\nFactual limit: {a["historical_limit"]}\n\nMotion: {a["motion_after_approval"]}\n\nStatus: {a["status"]}\n',encoding='utf-8')
def csvout(path,rows):
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def save():
 (P/'ASSET_PRODUCTION_QUEUE.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
 csvout(P/'ASSET_PRODUCTION_QUEUE.csv',[{**a,**{k:';'.join(a[k]) for k in ['beat_ids','reference_ids','exact_screen_text','claim_ids']}} for a in assets])
 (P/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2),encoding='utf-8');csvout(P/'REFERENCE_REGISTER.csv',refs)
save();(P/'IMAGEGEN_CALLS_PREPARED_NOT_EXECUTED.json').write_text(json.dumps(payload,indent=2))
data=list(csv.DictReader((OLD/'data/VERIFIED_CHART_DATA.csv').open(encoding='utf-8-sig',newline='')))
for row in data:
 if row['dataset']=='C06' and row['value']=='2019':row['kind']='SOURCE_DATE_CONFLICT_HOLD: V4 says2019; SCI24Fig3f distinguishes2017rediscovery and2019pilot analysis. Do not render before resolution.'
data += [{'dataset':'C07','item':'Main passage average vertical closure','value':'16','unit':'inches/year','kind':'approximate reported average HEIGHT loss, not area loss','source':ARMY,'locator':'TableII printed37-38/PDF45-46'}, {'dataset':'C07','item':'Side trench average vertical closure','value':'34','unit':'inches/year','kind':'approximate reported average HEIGHT loss, not area loss','source':ARMY,'locator':'TableII printed37-38/PDF45-46'}]
data += [{'dataset':'C15','item':'Gross thermal power','value':'10000','unit':'kW thermal','kind':'reported thermal rating, not electricity','source':ARMY,'locator':'PM-2A characteristics printed47/PDF55'}, {'dataset':'C15','item':'Net electrical power','value':'1560','unit':'kW electric rated','kind':'reported net electrical rating; V4 approximately1.5MW, not a heat/electric efficiency calculation','source':ARMY,'locator':'PM-2A characteristics printed47/PDF55'}]
for a in assets:
 if a['asset_id'].startswith('C') and int(a['asset_id'][1:])>=8 and a['asset_id']!='C15':
  for s in a['exact_screen_text']:data.append({'dataset':a['asset_id'],'item':s,'value':'','unit':'qualitative historical category / not numeric series','kind':a['historical_limit'],'source':';'.join(R[r]['source_url'] for r in a['reference_ids']),'locator':';'.join(a['claim_ids'])})
csvout(P/'data/VERIFIED_CHART_DATA.csv',data)
beats=list(csv.DictReader((REPO/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv').open(encoding='utf-8-sig',newline='')))
segments=[];placement=[]
for b in beats:
 # Paragraph-level narration units: exact text substrings, not made-up timecodes.
 paras=[t.strip() for t in re.split(r'\n\s*\n',b['spoken_text_exact']) if t.strip()]
 for i,t in enumerate(paras,1):
  opts=[a for a in assets if b['beat_id'] in a['beat_ids']]
  segments.append({'unit_id':b['beat_id']+f'-P{i:02d}','beat_id':b['beat_id'],'chapter':b['chapter'],'spoken_text_exact':t,'word_count':len(t.split()),'exact_in_words':' '.join(t.split()[:8]),'exact_out_words':' '.join(t.split()[-8:]),'eligible_asset_ids':';'.join(a['asset_id'] for a in opts),'real_motion_clip_ids':';'.join(r['scene_id'] for r in clips.values() if r['beat']==b['beat_id']),'selection_rule':'Eligible pool only. Pick by the asset-specific exact trigger; do not show every asset on every paragraph or repeat one clip.','audio_in_sec':'','audio_out_sec':'','timing_status':'AUDIO_TIMING_HOLD'})
 for a in assets:
  if b['beat_id'] in a['beat_ids']:placement.append({'asset_id':a['asset_id'],'chapter':b['chapter'],'beat_id':b['beat_id'],'narration_text_for_matching':b['spoken_text_exact'],'specific_cue_status':'NEEDS_ASSET_SPECIFIC_LITERAL_TRIGGER_BEFORE_USE','duration_budget_sec':'4-9; document6-12 if needed for reading','not_a_timeline':'Budget only; no audio timing invented','repeat_policy':'Select once; alternate placements are options, not additional unique images.'})
csvout(P/'V4_PARAGRAPH_VISUAL_UNITS.csv',segments);csvout(P/'ASSET_NARRATION_PLACEMENT_CUES.csv',placement)
outline=[]
for b in beats:
 aa=[a for a in assets if b['beat_id'] in a['beat_ids']]
 outline.append({'beat_id':b['beat_id'],'chapter':b['chapter'],'cue_in_exact_words':' '.join(b['spoken_text_exact'].split()[:10]),'cue_out_exact_words':' '.join(b['spoken_text_exact'].split()[-10:]),'prepared_assets':';'.join(a['asset_id'] for a in aa),'real_motion_clip_ids':';'.join(r['scene_id'] for r in clips.values() if r['beat']==b['beat_id']),'timing_status':'AUDIO_TIMING_HOLD','editorial_rule':'Real motion primary; choose the relevant explanation only. Preparation options do not equal coverage or added runtime.'})
csvout(P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv',outline)
page=['<!doctype html><meta charset="utf-8"><title>Camp Century R2 preparation</title><style>body{max-width:1400px;margin:32px auto;background:#eeeae1;color:#20282b;font:16px Arial;line-height:1.5}article{border-top:1px solid #8c9596;margin:24px 0;padding:20px}img{max-width:320px;max-height:300px;object-fit:contain;margin:8px;vertical-align:top}a{color:#24576b}.hold{color:#9e341e}</style><h1>Camp Century R2 — narration-led preparation</h1><p>60 briefs:24 referenced ImageGen illustrations,20 original document/photo treatments,16 data/logic diagrams. No generations. D07 source hold; exact core rediscovery date conflict held separately. The32beats/paragraph units have literal narration anchors; exact seconds remain AUDIO_TIMING_HOLD.</p>']
for ch in sorted({a['chapter'] for a in assets}):
 page.append(f'<h2>{ch}</h2>')
 for a in assets:
  if a['chapter']!=ch:continue
  page.append(f'<article><h3>{a["asset_id"]}: {html.escape(a["title"])}</h3><p>{a["production_route"]} · {a["status"]}</p><p>{html.escape(a["brief"])}</p>')
  for rid in a['reference_ids']:
   r=R[rid];page.append(f'<a href="{r["file"]}"><img src="{r["file"]}" title="{html.escape(r["title"])}"></a>')
  page.append(f'<p><b>Factual boundary:</b> {html.escape(a["historical_limit"])}</p><p><a href="{a["prompt_file"]}">Prompt / production brief</a></p></article>')
(P/'INDEX.html').write_text('\n'.join(page),encoding='utf-8')
new=[r for r in refs if r['reference_id'] not in {x['reference_id'] for x in json.loads((OLD/'REFERENCE_REGISTER.json').read_text())}]
for start in range(0,len(new),6):
 canvas=Image.new('RGB',(1200,1000),'#262626');draw=ImageDraw.Draw(canvas)
 for j,r in enumerate(new[start:start+6]):
  im=Image.open(P/r['file']);im.thumbnail((380,435));x=j%3*400;y=j//3*500;canvas.paste(im,(x,y));draw.text((x+4,y+450),r['reference_id'],fill='white')
 canvas.save(P/'qc'/f'R2_NEW_REFERENCES_{start//6+1:02d}.jpg',quality=92)
(P/'qc/R2_EXTRA_SOURCE_RECEIPT.json').write_text(json.dumps(download,indent=2))
q={'phase':'EXPANDED_PREPARATION_ONLY','asset_briefs':len(assets),'imagegen_jobs_prepared':len(payload),'document_photo_briefs':20,'data_and_logic_chart_briefs':16,'physical_reference_files':len(refs),'narration_beats':len(beats),'paragraph_visual_units':len(segments),'generation_outputs':0,'paid_credits_spent':0,'audio_timing':'HOLD','new_reference_review':'PENDING','source_image_holds':[a['asset_id'] for a in assets if not a['reference_ids']],'source_date_conflict':'C06 exact rediscovery year on hold; V4 unchanged; SCI24Fig3f says2017 vs2019pilot analyses'}
(P/'qc/PREPARATION_QC.json').write_text(json.dumps(q,indent=2))
shutil.copyfile(Path(__file__),P/'tools'/Path(__file__).name)
print(json.dumps(q,indent=2),flush=True)
