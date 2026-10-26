"""Prepare referenced image-generation jobs and authentic document/chart briefs. NO generation."""
import csv,json,hashlib,html,shutil,subprocess,io,zipfile,sys
from pathlib import Path
from PIL import Image,ImageDraw
import pymupdf
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
PACK=REPO/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R1'
for d in ['references','prompts','data','qc','tools']:(PACK/d).mkdir(parents=True,exist_ok=True)
URL_ARMY='https://icedrill.org/sites/default/files/477706.pdf'
URL_SCI='https://tc.copernicus.org/articles/18/4029/2024/'
URL_NASA='https://science.nasa.gov/earth/earth-observatory/new-view-of-the-city-under-the-ice-153616/'
URL_GAO='https://www.gao.gov/assets/gao-24-104082-highlights.pdf'
URL_NIELSEN='https://pure.au.dk/ws/files/81615219/City_under_the_Ice_2014.pdf'
refs=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def addref(rid,im,title,url,locator,rights,role='FACT_AND_GEOMETRY'):
 p=PACK/'references'/(rid+'.jpg');im.convert('RGB').save(p,quality=94,subsampling=0)
 r={'reference_id':rid,'file':'references/'+p.name,'sha256':sha(p),'width':im.width,'height':im.height,'title':title,'source_url':url,'source_locator':locator,'rights':rights,'input_role':role,'visual_review':'AWAITING_CURATED_CONTACT_SHEET_REVIEW'};refs.append(r)
def pdfref(rid,source,page,rect,title,url,rights):
 doc=pymupdf.open(BASE/'sources'/source);p=doc[page-1]
 clip=p.rect if rect is None else pymupdf.Rect(rect[0]*p.rect.width,rect[1]*p.rect.height,rect[2]*p.rect.width,rect[3]*p.rect.height)
 pix=p.get_pixmap(matrix=pymupdf.Matrix(2.5,2.5),clip=clip,alpha=False)
 addref(rid,Image.open(io.BytesIO(pix.tobytes('png'))),title,url,f'PDF page {page}, crop normalized {rect}',rights)
PD='US Army federal technical report; selected Army-origin figure/text; preserve caption and provenance'
pdfref('R01_COVER','ARMY65_TR174.pdf',2,None,'TR174 authentic October1965 report title cover; not the distribution-change sheet',URL_ARMY,PD)
pdfref('R02_PLAN','ARMY65_TR174.pdf',42,(.08,.07,.93,.83),'Fig26 constructed Camp Century layout, printed34',URL_ARMY,PD)
pdfref('R03_ARCH','ARMY65_TR174.pdf',38,(.09,.07,.91,.505),'Fig24 real reactor-trench roof arches, printed30',URL_ARMY,PD)
pdfref('R04_BUDGET','ARMY65_TR174.pdf',39,(.1,.065,.94,.285),'Cost table continuation: PM-2A and actual total, printed31',URL_ARMY,PD)
pdfref('R05_LOGISTICS','ARMY65_TR174.pdf',40,(.08,.61,.94,.73),'138mile route and1000/4600short-ton paragraph, printed32',URL_ARMY,PD)
pdfref('R06_PROFILES','ARMY65_TR174.pdf',47,(.035,.02,.985,.96),'Actual Fig28/29 dated measured cross sections, printed39',URL_ARMY,PD)
pdfref('R07_ESTIMATE','ARMY65_TR174.pdf',49,(.09,.525,.94,.705),'Snow trimming estimate paragraph, printed41',URL_ARMY,PD)
pdfref('R08_CHAINSAW','ARMY65_TR174.pdf',51,(.20,.072,.88,.49),'Fig33 actual electric-chain-saw trimming beside T5 eave, printed43',URL_ARMY,PD)
pdfref('R09_AIR_WELL','ARMY65_TR174.pdf',50,(.08,.07,.94,.63),'Fig32 AIR ventilation well for sewage odour; NOT drinking-water well, printed42',URL_ARMY,PD)
pdfref('R10_SUMP','ARMY65_TR174.pdf',52,(.08,.065,.94,.70),'Local sewage-sump heating and affected buildings, printed44',URL_ARMY,PD)
pdfref('R11_DISTRESS','ARMY65_TR174.pdf',48,(.09,.07,.94,.88),'Fig30 Wonder Arch distress at PM-2A building, printed40',URL_ARMY,PD)
pdfref('R12_SHUTDOWN','ARMY65_TR174.pdf',55,(.07,.55,.95,.64),'Historical service-period sentence including9July1963, printed47',URL_ARMY,PD)
pdfref('R13_CORE_2021','SCI24.pdf',4,(.505,.445,.785,.785),'Bierman et al2024 Fig2d ONLY: modern2021 archived core interiors',URL_SCI,'Bierman et al.,2024,The Cryosphere18,4029-4052,Fig2d,CC BY4.0; cropped; excludes historic panels a/b and derived 3D panel c')
for rid,name,title,rights in [
 ('R14_RADAR_2024','NASA_RADAR.jpg','Actual NASA April2024 airborne radar composite; published25Nov2024','NASA Earth Observatory/Michala Garrison and Jesse Allen; UAVSAR data Chad Greene NASA/JPL-Caltech; IceBridge UHF data Joseph MacGregor NASA/GSFC; NASA media guidelines, no endorsement'),
 ('R15_DRILL_1966','NASA_1966.jpg','NASA-published historical1966 drilling-trench photograph','National Archives photo404791598, via NASA Earth Observatory; preserve historical year; no NASA endorsement')]:
 addref(rid,Image.open(BASE/'sources'/name),title,URL_NASA,'NASA article named downloadable image',rights)
clips={r['scene_id']:r for r in csv.DictReader((REPO/'CAMP_CENTURY/ARCHIVE/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig',newline=''))}
for rid,cid,title in [('R16_PETER','CC07-C010','Actual Camp Century Peter miller'),('R17_FLOOR','CC07-C018','Actual prefab floor frame'),('R18_ROOM','CC07-C022','Actual prefab room under assembly'),('R19_WATER','CC07-C042','Actual Camp Century water-system film context; not the sewage air well')]:
 r=clips[cid];t=float(r['cut_seconds'])/2
 im=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',r['cut_filename'],'-frames:v','1','-vf','scale=640:480,setsar=1','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True,check=True)
 addref(rid,Image.open(io.BytesIO(im.stdout)),title,r['source_url'],f"{cid} output midpoint{t:.3f}s; source IN{r['start_tc']},clip SHA256{r['cut_sha256']}",'Selected silent US Army federal picture; Stage06 rights receipt applies','APPEARANCE_AND_CONSTRUCTION_CONTEXT')
gao=BASE/'references/GAO24_HIGHLIGHTS_PAGE001.png'
if gao.exists():addref('R20_GAO',Image.open(gao),'GAO2024 genuine highlights',URL_GAO,'Highlights1page','US GAO federal report; Greenland paragraph only')
R={r['reference_id']:r for r in refs}
STYLE='''Create a restrained, informative historical-documentary illustration for Hidden Industrial America, VIDEO007 CAMP CENTURY. Modern explanatory artwork informed by the attached authentic records; never impersonate a discovered archival photograph or an original government document. Period technical-report ink drawing with modest flat wash and natural drafting line variation. Neutral off-white paper, charcoal ink, muted blue-grey snow and sparse warm ochre emphasis; no burnt parchment, artificial damage, glossy 3D, neon, HUD, dossier panels, floating text boxes or decorative microtext. Full finished16:9 composition; the explanatory subject occupies roughly80% of the frame, with comfortable readable edge margins. No empty panels, placeholders, giant blank areas, authoring guides, crop marks, source IDs, job IDs, SOURCE BASIS, watermarks or extra text. Use only the short English labels explicitly listed. Keep each label readable; diagrams must explain one idea. Reference photos establish objects/appearance, not a request to invent photographic archival evidence. Never introduce Satsop, Pluto, Tory, cooling towers, weapons, modern labs into1960s scenes or unrelated Arctic bases. Do not invent dimensions, dates, data points, operational layouts or government stamps.'''
assets=[]
def asset(aid,kind,ch,beats,title,refids,brief,labels,claims,limit,motion,priority='P0'):
 row={'asset_id':aid,'production_route':kind,'chapter':ch,'beat_ids':beats,'title':title,'reference_ids':refids,'brief':brief,'exact_screen_text':labels,'claim_ids':claims,'historical_limit':limit,'motion_after_approval':motion,'priority':priority,'audio_status':'AUDIO_TIMING_HOLD','timing':'V4 word/beat cues only; no invented seconds','status':'BRIEF_READY_AWAITING_REFERENCE_QC'}
 assets.append(row)
def G(n,ch,beats,title,rs,brief,labels,claims,limit,motion,priority='P0'):asset(f'G{n:02d}','IMAGEGEN_REFERENCED_ILLUSTRATION',ch,beats,title,rs,brief,labels,claims,limit,motion,priority)
G(1,'CH01',['CC07-S4-CH01-B01'],'A working city in shallow firn',['R02_PLAN','R03_ARCH','R18_ROOM'],'One clear oblique cutaway through a compacted-snow trench. Show prefabricated occupied rooms beneath a corrugated arch, with a surface ramp. Match the actual ordinary rooms and arch proportions in the references. Show shallow buried construction, not a rock cavern, giant subterranean metropolis or natural ice cave. Explain material around the rooms, without drawing a complete invented site plan.',['COMPACTED SNOW','PREFAB ROOMS'],['CC07-S4-002','CC07-S4-003'],'Qualitative cutaway, not measured geometry or a literal historic view. No1963 deformation rate in this opening illustration.','4-6s gentle continuous reveal of surface then rooms, no shake; main evidence reveal later.')
G(2,'CH03',['CC07-S4-CH03-B01','CC07-S4-CH03-B02'],'Cut-and-cover method',['R16_PETER','R03_ARCH'],'A complete three-phase engineering illustration across one continuous snow section: excavated trench by a Peter miller, roof arch placed above a trench, the completed covered opening. Use consistent scale and camera across phases. The machines must look like the actual reference. No bedrock drilling, TBM, underground blast or tunnel-boring machine.',['CUT','COVER','BURY'],['CC07-S4-019','CC07-S4-020','CC07-S4-021'],'A method explanation, not three measured stages of a particular filmed trench.','6-8s: reveal each phase in action order with0.4-0.7s eased line/wash masks; no card slides.')
G(3,'CH03',['CC07-S4-CH03-B03'],'Prefab room inside the arch',['R17_FLOOR','R18_ROOM','R03_ARCH'],'One close technical cutaway showing timber floor framing supporting a plain prefabricated room within a snow trench. Preserve the visible materials and ordinary construction of the references. Distinguish room roof from the surrounding snow arch with clear drafting. No invented equipment or dimensions.',['SNOW ARCH','PREFAB ROOM'],['CC07-S4-024'],'Explains nesting of structures; does not assert measured clearances or prove a form-removal failure.','5-7s controlled focus from floor framing to room and enclosing arch; single motivated move.')
G(4,'CH03',['CC07-S4-CH03-B04'],'Heat changes the surrounding material',['R03_ARCH','R11_DISTRESS'],'A small heated room inside a snow arch in cross-section. Sparse muted warm wash around the room indicates local warming; charcoal snow contours remain clear. Show the material as snow/firn, not liquid oceans or melting blue caverns. No quantitative temperature scale, radiation glow or reactor cutaway.',['HEAT','SNOW AND FIRN'],['CC07-S4-026'],'Qualitative thermal influence only; no computed heat field or citywide collapse.','4-6s slow growth of restrained warm wash, stable camera.', 'P1')
G(5,'CH04',['CC07-S4-CH04-B03','CC07-S4-CH04-B04'],'Water supply and wastewater are different systems',['R19_WATER','R10_SUMP','R02_PLAN'],'Two clear separate subsurface systems within one finished cutaway: a meltwater well feeding a small water-supply building; a separate wastewater sump influencing nearby supporting snow locally. A thin physical separation makes the distinction obvious. The relative placement is conceptual, not a map. Do not connect drinking water to sewage or to a reactor coolant loop. Do not use the fan/air-well Fig32 as a drinking-water design. No plant internals, valves, operating parameters or radioactive visual symbols.',['WATER SUPPLY','WASTEWATER'],['CC07-S4-033','CC07-S4-034','CC07-S4-036'],'Not to scale; local sewage-related settlement, not reactor meltdown or all-camp failure.','6-9s first follow clean-water branch, then reveal the separate sump influence; no racing arrows.')
G(6,'CH06',['CC07-S4-CH06-B01','CC07-S4-CH06-B02'],'Why usable room disappears',['R06_PROFILES','R11_DISTRESS'],'A qualitative side-by-side interior snow-arch section, showing a plain room under an initially taller opening and a later reduced opening. Use the measured profile reference only to understand the direction and irregularity of deformation. No fabricated exact graph, time series, numeric axis or copied rate labels; exact data will use the authentic figure and separate verified chart.',['INITIAL OPENING','REDUCED OPENING'],['CC07-S4-049','CC07-S4-050','CC07-S4-051'],'Qualitative geometry, not a reconstruction of exact survey epochs.','6-8s stable dissolve/morph between approved endpoint contours; no elastic wobble or camera shake.')
G(7,'CH06',['CC07-S4-CH06-B03','CC07-S4-CH06-B04'],'The repeated maintenance job',['R08_CHAINSAW','R16_PETER'],'A readable three-action maintenance vignette: a worker trims encroaching snow beside a prefab eave with the small corded electric chain saw in the actual photograph; loose cut snow is gathered; a small load is removed. One continuous technical illustration, no boxed cards. Preserve ordinary period workwear and the tool silhouette. No chainsaw attacking steel beams, blast demolition or fictional disaster.',['TRIM','REMOVE','REPEAT'],['CC07-S4-054','CC07-S4-055'],'Illustrates recurring labour.20,000yd3 is an estimate, not footage of actual annual removal.','6-8s follow work in physical order; document Fig33 precedes it; no quantitative animation.')
G(8,'CH08',['CC07-S4-CH08-B01'],'Deep core versus the shallow base',['R15_DRILL_1966','R02_PLAN'],'A vertical explanatory section through Greenland snow and ice, with a small shallow camp near the top and a deep scientific core reaching the ice-sediment boundary far below. Include a clear scale-break convention; it is not to scale. Show plain drilling equipment informed by the authentic1966 drilling-trench photo. The basal sediment belongs below the ice sheet, not inside a barracks tunnel.',['1966 CORE','BASAL SEDIMENT'],['CC07-S4-066','CC07-S4-067'],'Do not invent a precise drilling depth or use the2024 minimum burial depth as a1966 camp depth.','6-9s track down the core path, pause at sediment; preserve the scale break.')
G(9,'CH08',['CC07-S4-CH08-B02'],'From frozen sample to scientific evidence',['R13_CORE_2021'],'An informative editorial drawing of a frozen sediment-bearing core cut face, a carefully held small sediment sample and a simple optical examination station, arranged in a clear visual progression. Follow the actual brown-grey archived core material; no gemstones or fantasy fossils. No identifiable plant species, numerical age, fake micrograph, invented data trace or historic government label. Use restrained report-style ink and flat wash, not glossy product photography.',['CORE','SEDIMENT','ANALYSIS'],['CC07-S4-068','CC07-S4-069'],'Conceptual modern analysis; not a photo of a specific laboratory, fossil or dated specimen.','5-7s one measured progression from core to sample; authentic sample photo remains the factual anchor.','P1')
G(10,'CH08',['CC07-S4-CH08-B03'],'What radar sees',['R14_RADAR_2024','R02_PLAN'],'A wide modern explanatory cutaway: a small airborne survey platform above the ice, a restrained broad side-looking radar sampling wedge, and buried structural traces below the surface. Use the actual NASA composite only to understand the kind of observation; never imitate or alter it into invented measurement data. No illuminated working underground city, people, accessible rooms, missile complex, fake heatmap or new radar returns.',['AIRBORNE RADAR','BURIED STRUCTURES'],['CC07-S4-070','CC07-S4-071','CC07-S4-073'],'Method illustration only; original NASA radar is D08. Do not interpret a distant bed reflection plotted above the camp as physically above it.','5-7s reveal survey geometry, then cut to the untouched actual radar composite.','P1')
DOCS=[
 (1,'CH01',['CC07-S4-CH01-B02'],'Authentic report identity',['R01_COVER'],'Use original cover. Brief readable hold, then source-led cut to the relevant page. Never generate report text.',['CC07-S4-001'],'No fake stamp, altered date or decorative declassification overlay.'),
 (2,'CH03',['CC07-S4-CH03-B03'],'Actual constructed base layout',['R02_PLAN'],'Use original Fig26. Focus on actual Main Street, living/service spaces and workshop; no all-page yellow box.',['CC07-S4-024'],'Dense original labels remain in scan; do not invent rooms or redraw the entire plan through ImageGen.'),
 (3,'CH04',['CC07-S4-CH04-B01','CC07-S4-CH04-B02'],'Actual cost accounting',['R04_BUDGET'],'Show the original PM-2A5,700,000 line and7,920,000 total with their table labels and actual-total footnote.',['CC07-S4-029','CC07-S4-030'],'Period dollars; no inflation-adjusted claim and no generated accounting sheet.'),
 (4,'CH06',['CC07-S4-CH06-B02'],'Actual measured profiles',['R06_PROFILES'],'Keep Fig28/29 contours, dates, station names and scale bars. Reveal original profiles, then the two local-rate captions.',['CC07-S4-050','CC07-S4-051'],'No yellow fill over the drawing, invented contour, extrapolation or whole-camp rate.'),
 (5,'CH06',['CC07-S4-CH06-B03'],'Annual trimming estimate',['R07_ESTIMATE'],'Focus precisely on estimated and20,000 cubic yards in the original paragraph; short translucent marker sweep behind text, not a line through it.',['CC07-S4-054'],'Keep the estimate qualifier attached to the quantity.'),
 (6,'CH06',['CC07-S4-CH06-B04'],'The actual electric-chain-saw photograph',['R08_CHAINSAW'],'Use the original Fig33 photograph and explanatory caption. Gentle focus on tool and eave; magnifier only if needed for readability.',['CC07-S4-055'],'A still photograph is not moving archive; do not generate a new worker and call it proof.'),
 (7,'CH07',['CC07-S4-CH07-B03'],'GAO assessment qualification',[],'Original Highlights Greenland paragraph required; local PDF acquisition returned403. Do not fake a GAO page. Use the source facts in editorial notes until genuine document image is acquired.',['CC07-S4-064','CC07-S4-065'],'DOCUMENT_BINARY_HOLD; web text verified, local source image missing.'),
 (8,'CH08',['CC07-S4-CH08-B03'],'Actual2024 radar composite',['R14_RADAR_2024'],'Use untouched actual NASA composite; retain meaningful context, original radar data and credit.',['CC07-S4-070','CC07-S4-071','CC07-S4-073'],'Published25Nov2024, acquiredApril2024; not first radar detection, not an interior photograph.'),
 (9,'CH08',['CC07-S4-CH08-B01'],'Actual1966 drilling-trench photograph',['R15_DRILL_1966'],'Use untouched NARA photograph from NASA as the historical drilling reference; identify1966 in context.',['CC07-S4-066'],'Still image, not motion; do not attribute an exact drilling moment absent a more specific caption.'),
 (10,'CH08',['CC07-S4-CH08-B02'],'Actual archived core interiors',['R13_CORE_2021'],'Use only Fig2d cropped modern2021 photographs with retained specimen scale and CC BY credit.',['CC07-S4-068','CC07-S4-069'],'Photographed2021, published2024. Not a1966 photo or an ancient-plant micrograph.')]
for n,ch,beats,title,rs,brief,claims,limit in DOCS:
 asset(f'D{n:02d}','AUTHENTIC_SOURCE_NO_IMAGEGEN',ch,beats,title,rs,brief,[],claims,limit,'6-10s source-led view; ease any zoom; marker sweep0.5-0.8s only behind a short verified text span; no shake or dashboard overlays.')
CHARTS=[
 (1,'CH02',['CC07-S4-CH02-B01','CC07-S4-CH02-B02'],'Supply distance',['R05_LOGISTICS'],['CAMP TUTO','138 MILES','CAMP CENTURY'],['CC07-S4-012'],'Two-node route-length diagram, NOT a geographic map. No invented coordinates, road, route shape or Thule distance.'),
 (2,'CH02',['CC07-S4-CH02-B02','CC07-S4-CH02-B03'],'Construction cargo',['R05_LOGISTICS'],['1959','1960','US SHORT TONS'],['CC07-S4-015','CC07-S4-016','CC07-S4-017'],'Zero-baseline bars1000 and4600; sum5600 identified as derived total. No invented quarterly time series.'),
 (3,'CH04',['CC07-S4-CH04-B02'],'Power plant share of initial cost',['R04_BUDGET'],['PM-2A','OTHER INITIAL COSTS','PERIOD DOLLARS'],['CC07-S4-029','CC07-S4-030'],'Total7,920,000, PM-2A5,700,000, derived remainder2,220,000. Shared baseline/proportional lengths; no modern dollars.'),
 (4,'CH06',['CC07-S4-CH06-B02'],'Two different measured local rates',['R06_PROFILES'],['MAIN TRENCH 6+00','TRENCH20 2+60','ANNUAL CROSS-SECTION AREA LOSS'],['CC07-S4-050','CC07-S4-051'],'12% and17% annual area loss at two specified sections; not vertical inches, universal closure or a recorded annual series.'),
 (5,'CH05',['CC07-S4-CH05-B02'],'Proposal versus actual deployment',['R02_PLAN'],['PROPOSAL','600 MISSILES','2,100 POSSIBLE LAUNCH POSITIONS','NEVER DEPLOYED'],['CC07-S4-043','CC07-S4-044','CC07-S4-057'],'High-level historical totals only. Facts from Nielsen2014p445; no missile or operational-network imagery, technical layouts or copyrighted article-page image.'),
 (6,'CH07',['CC07-S4-CH07-B01','CC07-S4-CH08-B01','CC07-S4-CH08-B02','CC07-S4-CH08-B03'],'Selected evidence chronology',['R12_SHUTDOWN','R15_DRILL_1966','R14_RADAR_2024'],['1963','1964','1966','2019','2024'],['CC07-S4-058','CC07-S4-059','CC07-S4-066','CC07-S4-068','CC07-S4-070'],'Show only the relevant2-3 dated events at each chapter transition. Do not invent a single uncontested end-of-occupation date; V4 discloses1966/1967 source differences.')]
for n,ch,beats,title,rs,labels,claims,limit in CHARTS:
 asset(f'C{n:02d}','DATA_LOCKED_CHART_NO_IMAGEGEN',ch,beats,title,rs,'Reconstruct in editable SVG/Fusion from the accompanying exact CSV, with thin axes, generous label margins and one restrained emphasis. Dense facts stay deterministic.',labels,claims,limit,'4-7s eased data reveal; axes/labels fixed; no bouncing numbers, abrupt wipes or fabricated intermediate observations.')
data=[
 {'dataset':'C01','item':'Camp Tuto to Camp Century','value':138,'unit':'miles','kind':'reported approximate distance','source':URL_ARMY,'locator':'printed32 / PDF40'},
 {'dataset':'C02','item':'1959','value':1000,'unit':'US short tons','kind':'approximately reported seasonal freight','source':URL_ARMY,'locator':'printed32 / PDF40'},
 {'dataset':'C02','item':'1960','value':4600,'unit':'US short tons','kind':'approximately reported seasonal freight','source':URL_ARMY,'locator':'printed32 / PDF40'},
 {'dataset':'C02','item':'combined','value':5600,'unit':'US short tons','kind':'derived sum1000+4600; NOT third independent bar','source':URL_ARMY,'locator':'printed32 / PDF40'},
 {'dataset':'C03','item':'total initial cost','value':7920000,'unit':'period USD','kind':'reported total; footnote actual held to this figure','source':URL_ARMY,'locator':'printed31 / PDF39'},
 {'dataset':'C03','item':'PM-2A','value':5700000,'unit':'period USD','kind':'reported allocation','source':URL_ARMY,'locator':'printed31 / PDF39'},
 {'dataset':'C03','item':'other initial costs','value':2220000,'unit':'period USD','kind':'derived remainder7920000-5700000','source':URL_ARMY,'locator':'printed31 / PDF39'},
 {'dataset':'C04','item':'Main Trench station6+00','value':12,'unit':'percent cross-section area loss per year','kind':'reported local example, not all trenches','source':URL_ARMY,'locator':'Fig28 printed39 / PDF47'},
 {'dataset':'C04','item':'Trench20 station2+60','value':17,'unit':'percent cross-section area loss per year','kind':'reported different local example','source':URL_ARMY,'locator':'Fig29 printed39 / PDF47'},
 {'dataset':'C05','item':'missiles','value':600,'unit':'proposed count','kind':'never deployed; historical proposal total only','source':URL_NIELSEN,'locator':'printed445 / PDF4; article is research-only, not visual input'},
 {'dataset':'C05','item':'possible launching positions','value':2100,'unit':'proposed count','kind':'never built/deployed; not completed silos','source':URL_NIELSEN,'locator':'printed445 / PDF4'},
 {'dataset':'D05','item':'annual snow trimming','value':20000,'unit':'cubic yards per year','kind':'engineering estimate needed to preserve original openings; not recorded removals','source':URL_ARMY,'locator':'printed41 / PDF49'}]
events=[('1963-07-09','PM-2A shut down',URL_ARMY,'printed47 / PDF55'),('1964','PM-2A removed',SOURCES if False else 'https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv','Actual removal film; released1965, events1964'),('1966','Basal material recovered',URL_SCI,'section2; avoid conflicting exact day/depth'),('2019','Archived material rediscovered',URL_SCI,'section2'),('2024-04','NASA UAVSAR acquisition',URL_NASA,'April2024 flight'),('2024-11-25','NASA imagery published',URL_NASA,'article date')]
for date,event,src,loc in events:data.append({'dataset':'C06','item':event,'value':date,'unit':'historical date','kind':'separate acquisition/publication events','source':src,'locator':loc})
def csvout(path,rows,fields=None):
 if fields is None:fields=list(dict.fromkeys(k for r in rows for k in r))
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
csvout(PACK/'data/VERIFIED_CHART_DATA.csv',data)
manifest_sources=json.loads((BASE/'qc/SOURCE_DOWNLOAD_MANIFEST.json').read_text())
for a in assets:
 if a['asset_id']=='D07' and 'R20_GAO' not in R:a['status']='DOCUMENT_BINARY_HOLD_HTTP403'
 else:a['status']='PREPARED_PENDING_VISUAL_REFERENCE_QC'
 if a['production_route'].startswith('IMAGEGEN'):
  roles='\n'.join(f"Image{k+1}: {rid}, {R[rid]['title']}; role {R[rid]['input_role']}." for k,rid in enumerate(a['reference_ids']))
  prompt=f"Use case: scientific-educational\nAsset type: full-frame16:9 documentary explanatory illustration\nPrimary request: {a['brief']}\nInput images:\n{roles}\nStyle/medium: {STYLE}\nText (verbatim; no other text): "+'; '.join('"'+t+'"' for t in a['exact_screen_text'])+f"\nFactual boundary: {a['historical_limit']}\nComposition: complete finished scene; no placeholder areas. Render labels as small integrated technical annotations, not a sidebar.\n"
  (PACK/'prompts'/(a['asset_id']+'.txt')).write_text(prompt,encoding='utf-8')
  a['prompt_file']='prompts/'+a['asset_id']+'.txt'
 else:
  (PACK/'prompts'/(a['asset_id']+'_PRODUCTION_BRIEF.md')).write_text(f"# {a['asset_id']} — {a['title']}\n\nRoute: {a['production_route']}\n\n{a['brief']}\n\nReferences: {', '.join(a['reference_ids'])}\n\nFactual limit: {a['historical_limit']}\n\nMotion: {a['motion_after_approval']}\n\nStatus: {a['status']}\n",encoding='utf-8')
  a['prompt_file']='prompts/'+a['asset_id']+'_PRODUCTION_BRIEF.md'
csvrows=[{**a,'beat_ids':';'.join(a['beat_ids']),'reference_ids':';'.join(a['reference_ids']),'exact_screen_text':';'.join(a['exact_screen_text']),'claim_ids':';'.join(a['claim_ids'])} for a in assets]
csvout(PACK/'ASSET_PRODUCTION_QUEUE.csv',csvrows)
(PACK/'ASSET_PRODUCTION_QUEUE.json').write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding='utf-8')
payloads=[]
for a in assets:
 if a['production_route'].startswith('IMAGEGEN'):
  payloads.append({'asset_id':a['asset_id'],'call_status':'PREPARATION_ONLY_DO_NOT_EXECUTE','tool':'image_gen.imagegen','arguments':{'prompt':(PACK/a['prompt_file']).read_text(encoding='utf-8'),'referenced_image_paths':[str(PACK/R[rid]['file']) for rid in a['reference_ids']],'transparent_background':False},'output_intent':a['asset_id']+'_R1.png'})
(PACK/'IMAGEGEN_CALLS_PREPARED_NOT_EXECUTED.json').write_text(json.dumps(payloads,indent=2),encoding='utf-8')
beats=list(csv.DictReader((REPO/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv').open(encoding='utf-8-sig',newline='')))
mapping=[]
for b in beats:
 aa=[a for a in assets if b['beat_id'] in a['beat_ids']];rr=[r for r in clips.values() if r['beat']==b['beat_id']];w=b['spoken_text_exact'].split()
 mapping.append({'beat_id':b['beat_id'],'chapter':b['chapter'],'cue_in_exact_words':' '.join(w[:10]),'cue_out_exact_words':' '.join(w[-10:]),'prepared_assets':';'.join(a['asset_id'] for a in aa),'real_motion_clip_ids':';'.join(r['scene_id'] for r in rr),'editorial_rule':'Use real motion first; choose at most one explanatory insert at a time. Assets are options, not mandatory cards per beat.','timing_status':'AUDIO_TIMING_HOLD','uncovered_or_context_only':('SOURCE_FOOTAGE_OR_EXISTING_PLAN_CONTEXT_ONLY_NO_NEW_ILLUSTRATION' if not aa else 'PREPARED_OPTION_NOT_A_FINISHED_TIMELINE')})
csvout(PACK/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv',mapping)
csvout(PACK/'REFERENCE_REGISTER.csv',refs)
(PACK/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2),encoding='utf-8')
(PACK/'qc/SOURCE_DOWNLOAD_MANIFEST.json').write_text(json.dumps(manifest_sources,indent=2),encoding='utf-8')
# Reference index for actual visual QC.
for start in range(0,len(refs),8):
 canvas=Image.new('RGB',(1280,960),'#252525');d=ImageDraw.Draw(canvas)
 for j,r in enumerate(refs[start:start+8]):
  im=Image.open(PACK/r['file']);im.thumbnail((300,415));x=j%4*320;y=j//4*480
  canvas.paste(im,(x,y));d.text((x+3,y+430),r['reference_id'],fill='white')
 canvas.save(PACK/'qc'/f'CURATED_REFERENCES_{start//8+1:02d}.jpg',quality=92)
style=f'''# HIA Camp Century — proposed generation style and factual contract

{STYLE}

This is a source-informed **proposed** treatment, not a newly owner-approved channel canon. No generated result exists yet and no visual style PASS is claimed.

- Genuine documents stay genuine scans. No fake letterhead, signature, classified/declassified stamp, invented table or replacement OCR text. ImageGen is never used to recreate a factual page.
- Charts use VERIFIED_CHART_DATA.csv and editable SVG/Fusion with fixed data. No sampled/imagined curve or false interpolation. Dates and labels are typed exactly.
- Generated illustrations explain only conceptual geometry. Sources establish object shape and context; they are explicitly distinct from primary evidence in metadata and descriptions. No operational missile installation, deployed arsenal or weapon-design details.
- Match source paper/ink texture gently; do not add orange/teal cinematic grades, black dashboard cards, oversized typography, unexplained UI or decorative clutter. Yellow is reserved for a short factual text emphasis; never paint over whole drawings.
- Documents: stabilize, crop to the relevant lines, give time to read. A translucent yellow marker follows actual word boxes left-to-right in0.5–0.8s, with its baseline behind the letters. No underline/strike-through. No reflow or rewritten scan. Magnify only genuinely unreadable details.
- Motion begins only after the still is accepted: motivated camera focus, restrained masks and stable geometry. No wiggle, noise, handheld shake, bounce, abrupt pushes or random transitions.
- Frame16:9, complete composition; no blank containers or authoring guides. Internal asset IDs and source-control notes never appear on screen. Historical qualifiers such as PROPOSAL,1966 or2024 remain when needed to prevent a false claim.
- Original dense scans may require a crop/zoom, not AI upscaling that rewrites evidence. Reference JPEGs are preparation assets; use original PDFs for final document exports.
'''
(PACK/'STYLE_AND_FACTUAL_CONTRACT.md').write_text(style,encoding='utf-8')
rights='''# Reference rights and source limitations

Army TR174: US federal Army report; use only reviewed Camp Century figures/pages and source text. Earlier report sections include other bases and methods; they are not Camp Century site evidence. Film stills are from already-verified Stage06 silent Army pictures.

NASA: https://www.nasa.gov/nasa-brand-center/images-and-media/ . Preserve credits and avoid endorsement. R14 credit: NASA Earth Observatory images by Michala Garrison and Jesse Allen, using UAVSAR data/imagery from Chad Greene (NASA/JPL-Caltech) and IceBridge UHF data from Joseph MacGregor (NASA/GSFC). R15 credit: National Archives photo404791598 via NASA Earth Observatory. R14 is2024 radar; R15 is1966 historical still; neither adds moving-video seconds to Stage06.

Bierman et al2024: https://doi.org/10.5194/tc-18-4029-2024 , CC BY4.0. R13 is Fig2d only, modern2021 new photographs; cropped, retain author/year/figure/DOI/license/change credit in upload credits. Historical Fig2a/b and the Daugherty1963 plan in Fig1b are not assumed cleared just because the article is open. The private drilling log in Fig4 is research-only pending specific underlying rights. None is an ImageGen input in this pack.

Nielsen et al2014: copyrighted publisher article. Downloaded locally for private fact research; full PDF/pages are NOT included in this public pack, NOT image-generation inputs and NOT cleared on-screen documents. Proposal totals are historical facts from p445 and remain labelled as unbuilt. No plan image or military deployment geometry is generated.

GAO Highlights: federal source web text verified. Local PDF requests returned403; D07 is HOLD, no fabricated substitute page. Acquisition errors include sandbox-only failures and the actual externally checked403; neither is hidden. Do not spend credits on reconstructing this page. Public original: https://www.gao.gov/assets/gao-24-104082-highlights.pdf

All local-source PDFs, raw HTML, original films and private research copies remain in the local archive, outside this Git image/prompt pack. This file records an editorial evidence assessment, not a legal guarantee.
'''
(PACK/'RIGHTS_AND_EXCLUSIONS.md').write_text(rights,encoding='utf-8')
readme='''# VIDEO007 CAMP CENTURY — complete reference and generation-preparation pack R1

**Preparation only. No image/video generation, paid TTS, credits or Resolve edits performed. V4 unchanged.**

-26 asset briefs:10 referenced ImageGen illustrations,10 authentic-source document/photo treatments,6 data-locked charts. D07 GAO source image is explicitly HOLD;25 other briefs have physical image references. No generated image or final style approval exists yet.
-Open INDEX.html for every brief, source image and prompt. REFERENCE_REGISTER contains physical-file hashes, page/caption, rights, date and input role. V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP covers all32 locked beats and links existing real moving clips.
-For ImageGen: read each attached local image first, then use IMAGEGEN_CALLS_PREPARED_NOT_EXECUTED.json. One built-in call per asset; references are mandatory. Rebase absolute reference paths if unpacked elsewhere. Never execute a bulk paid/API substitute. Suggested first proof:G02 (cut-and-cover), then G05 (water/waste distinction); review factual geometry/style before the remaining eight. This is an execution order, not permission to generate during preparation.
-Documents/charts: use the production brief and source/data. Authentic pages are not generative targets. Quantitative chart shapes and text stay editable and deterministic. A generated approximation is not a data source.
-Do not put26 inserts consecutively or everywhere. They are choices across the film; most visuals remain real Stage06 moving footage. Use one explanatory insert per relevant narration idea, usually4–9s; hold dense document evidence long enough to read. Exact timeline seconds remain AUDIO_TIMING_HOLD.
-No facsimile classified records, generic stock, Satsop/Pluto/Tory, working Iceworm missiles, fake scientific results, article-page regeneration, blank panels or metadata overlays.

Local source PDFs and source acquisition receipts: C:\\Users\\KK\\CAMP_CENTURY_VIDEO007_ARCHIVE\\GRAPHICS_PREP_R1. Large originals/private research PDFs are deliberately excluded from Git and this ZIP.
'''
(PACK/'README.md').write_text(readme,encoding='utf-8')
page=['<!doctype html><meta charset="utf-8"><title>Camp Century references and prompts</title><style>body{font:16px Arial;background:#eeeae1;color:#20282b;max-width:1350px;margin:30px auto;line-height:1.5}article{padding:24px;margin:25px 0;border-top:1px solid #9da2a0}img{max-width:380px;max-height:340px;object-fit:contain;vertical-align:top;margin:8px;background:white}pre{white-space:pre-wrap;background:#fff;padding:18px}a{color:#24566d}.hold{color:#9b3b21}</style><h1>Camp Century — references and generation preparation</h1><p>26 briefs:10 ImageGen illustrations,10 authentic documents/photos,6 exact charts. D07 source image HOLD. No generations executed, no final style approval. References and prompts follow V4; real motion remains primary.</p>']
for a in assets:
 page+=[f'<article><h2>{a["asset_id"]} · {html.escape(a["title"])}</h2><p>{a["chapter"]} · {a["production_route"]} · <b>{a["status"]}</b></p><p>{html.escape(a["brief"])}</p>']
 for rid in a['reference_ids']:
  r=R[rid];page.append(f'<a href="{r["file"]}"><img src="{r["file"]}" title="{html.escape(r["title"])}"></a>')
 page +=[f'<p><b>Limit:</b> {html.escape(a["historical_limit"])}</p><p><b>Motion:</b> {html.escape(a["motion_after_approval"])}</p><p><a href="{a["prompt_file"]}">Open prompt / production brief</a></p></article>']
(PACK/'INDEX.html').write_text('\n'.join(page),encoding='utf-8')
summary={'phase':'PREPARATION_ONLY_NOT_GENERATED','asset_briefs':len(assets),'imagegen_jobs_prepared':len(payloads),'document_photo_briefs':len(DOCS),'exact_chart_briefs':len(CHARTS),'physical_curated_reference_files':len(refs),'script_v4_beats_mapped':len(mapping),'paid_credits_spent':0,'generated_outputs':0,'resolve_changes':0,'hold_assets':['D07'],'reference_visual_review':'PENDING_CURATED_SHEETS','owner_style_approval':'NOT_CLAIMED','audio_timing':'HOLD'}
(PACK/'qc/PREPARATION_QC.json').write_text(json.dumps(summary,indent=2))
for src in ['camp_century_prepare_reference_sources.py','camp_century_render_reference_pages.py','camp_century_complete_references.py','camp_century_build_generation_pack.py']:
 shutil.copyfile(Path(r'C:\Users\KK')/src,PACK/'tools'/src)
print(json.dumps(summary,indent=2))
print('PACK',str(PACK),flush=True)
if __name__=='__main__':pass
