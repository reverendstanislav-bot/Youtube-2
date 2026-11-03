from pathlib import Path
import csv,json,re,hashlib,shutil,datetime,collections
P=Path(__file__).resolve().parents[1];L=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');C=L/'CURATED_EDIT_R2';R=P/'SOURCE_FILES/PRODUCTION_PREP';E=L/'EDIT_PREP/R5_1';E.mkdir(parents=True,exist_ok=True);R.mkdir(exist_ok=True)
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,a):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(a[0]));w.writeheader();w.writerows(a)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
media=[]
for x in readcsv(C/'ASSET_MANIFEST.csv'):
 source=C/x['relative_path'];dest=E/'MEDIA_READY'/x['relative_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest);assert sha(dest)==x['sha256']
 kind=x['kind'];prov='MODERN CONTEXT' if kind=='modern_context_stock' else ('EDITORIAL BASE GEODATA' if kind=='geodata' else 'HISTORICAL SOURCE')
 media.append(dict(asset_id=x['id'],source_path=str(source),edit_package_path=str(dest),kind=kind,provenance_class=prov,sha256=sha(dest),rights_basis=x['rights_basis'],rights_evidence=str(C/x['rights_evidence']),credit=x['credit'],usage_limits=x['limitations'],import_policy='EXISTING_ACCEPTED_LIMITED_SCOPE_NO_RIGHTS_UPGRADE'))
for x in readcsv(L/'FREE_ONLY_R1/MANIFEST.csv'):
 source=L/'FREE_ONLY_R1'/x['relative_path'];dest=E/'MEDIA_READY/DOCUMENTS'/source.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest);assert sha(dest)==x['sha256']
 media.append(dict(asset_id=x['id'],source_path=str(source),edit_package_path=str(dest),kind='official_government_text_page',provenance_class='DOCUMENT',sha256=sha(dest),rights_basis=x['reuse_basis'],rights_evidence=str(L/'FREE_ONLY_R1'/x['rights_evidence']),credit=x['credit'],usage_limits=x['limitations'],import_policy='TWO_SELECTED_TEXT_PAGES_ONLY_NOT_ALL_PDF_ILLUSTRATIONS'))
for item in media:item['direct_editor_import']=item['kind']!='geodata'
writecsv(P/'12_MEDIA_READY_INDEX_R5_1.csv',media);writecsv(E/'MEDIA_READY_INDEX.csv',media)
(E/'IMPORT_ACCEPTED_MEDIA_ONLY.txt').write_text('\n'.join(x['edit_package_path'] for x in media if x['kind']!='geodata')+'\n',encoding='utf-8')
shutil.copytree(C/'RIGHTS',E/'RIGHTS_EVIDENCE/CURATED_R2',dirs_exist_ok=True);shutil.copy2(L/'FREE_ONLY_R1/RIGHTS/NLM_GOVERNMENT_TEXT_REVIEW.json',E/'RIGHTS_EVIDENCE/NLM_GOVERNMENT_TEXT_REVIEW.json')
held=[]
for x in readcsv(L/'SOURCE_CATALOG/ASSET_REGISTER.csv'):
 if x['id'] not in {m['asset_id'] for m in media}:
  held.append(dict(asset_id=x['id'],path=str(L/x['relative_path']),recorded_rights=x['rights_status'],quality=x['quality_status'],import_policy='REFERENCE_ONLY_NOT_IN_IMPORT_LIST',reason=x['note_ru']))
writecsv(E/'REFERENCE_NOT_FOR_IMPORT.csv',held)
# Reuse existing licensed Freesound previews as candidates;never reuse another episode's mixed master.
sfx=[]
for x in readcsv(Path(r'C:\YOUTUBE\Youtube 2\9\QC\DELIVERY_R9\FREESOUND_SOURCES.csv')):
 if x['id'] not in ['613918','871228']:continue
 f=Path(r'C:\YOUTUBE\Youtube 2\9\AUDIO\SFX\FREESOUND')/(x['id']+'.mp3');assert sha(f).lower()==x['sha256'].lower()
 dest=E/'SFX_CANDIDATES'/f.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(f,dest)
 sfx.append(dict(id=x['id'],title=x['title'],author=x['author'],license_recorded=x['license'],source=x['source'],file=str(dest),sha256=sha(dest),quality='Existing HQpreviewMP3,not originalWAV;no new listening/QC claim',use_policy='Short designed mechanical cue under explanation only;not authentic1939/1940sound,no continuous bed',status='CANDIDATE_NOT_MIXED'))
writecsv(E/'SFX_CANDIDATES.csv',sfx)
# Paragraph-specific source choices and reasons. No fixed-duration still slideshow.
mapping={
'A01-P01':('PH10;PH14','Broken ramp escape:unloading photo then actual ramp aftermath','C02;C04','Do not portray aftermath photo as impact footage.'),
'A01-P02':('PH09','Vehicle away from ship;poor progress follows arrival','C04','Movement is a still source;moving coverage rights/quality HOLD.'),
'A01-P03':('PH07','Scale and people;mobile-base functions','G01','Do not invent an interior cutaway from a crew portrait.'),
'A01-P04':('PH04','Named tyre/hub subject introduces support problem','G03','Graphic only when mechanism needs explanation;no defaultzoom.'),
'A01-P05':('PH03','Hatch and habitation express away-from-support stakes','','Do not recap later repairs.'),
'A01-P06':('LOC_BYRD','Byrd portrait leads to1934rescue','','Portrait is context,not a photograph of the rescue.'),
'A02-P01':('LOC_BYRD','1934winter rescue;tractor journey','NEED_1934_RESCUE_SOURCE','No1940Cruiserfilm pretending to be1934.'),
'A02-P07':('','Improvised searchlight and return trail lights','NEED_1934_RESCUE_SOURCE','No invented original lamp/film;source-informed explanation needs clear conceptclass.'),
'A02-P02':('PH07','Human requirements for transport','G01','Avoid another identical cut to same crew image.'),
'A02-P03':('','Traveling rooms,workshop and aircraft intent','G01;D03','No fake archived interior;design is intent.'),
'A02-P04':('PH02','Dogs as practical logistics;aircraft/route contrast','G01','Dogs haul a sparetyre,not the Cruiser.'),
'A02-P05':('','Armour/Pullman construction in1939','D03;NEED_FREE_CONSTRUCTION_PHOTO','Research page readable;image reproduction rights HOLD.'),
'A02-P06':('','Departure constrains testing sequence','NEED_FREE_CONSTRUCTION_PHOTO','No invented precise countdown.'),
'A03-P01':('','Welded body and field repair provision','G01;D03','Planned workshop,not proof of a specific onboard repair.'),
'A03-P03':('','Independent electric wheel drive and hydraulicmovement','G02;ENG40','Editable source-based diagram;no component inventory screen.'),
'A03-P04':('','Proposed body-as-bridge sequence','G02','Sequential load transfer,not a demonstrated Antarctic crossing.'),
'A03-P05':('','Proposed15ft gap and body role','G02','One dimension from ledger;do not invent surveyed crevasse.'),
'A03-P07':('','Controls ->need to reach ship','NEED_ROAD_ARCHIVE','Do not repeat finished mechanism explanation.'),
'A04-P10':('','Chicago controls and adjustments','NEED_ROAD_ARCHIVE','Road photographs must match city;OSU/BPLreuseHOLD.'),
'A04-P08':('','GrantParkdemonstration','NEED_GRANT_PARK_ARCHIVE','Do not label Bostoncrowd asChicago.'),
'A04-P01':('','Short sand trial','NEED_DUNE_ARCHIVE','Sand is not Antarctic snow.'),
'A04-P03':('','Public road journey','OSU_P01;BPL03','Reference-only,not imported.'),
'A04-P04':('','Indiana collision ->Ohio bridge accident','NEED_OHIO_CRASH_SOURCE','No unrelated crashphoto or exact crowd number.'),
'A04-P05':('','Hydraulic repair,jacks,reversing to road','NEED_OHIO_RECOVERY_SOURCE','No footage falsely presenting staged recovery as original.'),
'A04-P09':('','Workshop repair ->overheated climb ->tow','NEED_ROAD_REPAIR_SOURCE','Causal steps,not generic machines repeated.'),
'A04-P06':('','Boston removal of tail for loading','C01;BPL02','RightsHOLD;no implied cutting body inhalf.'),
'A04-P11':('','Tide aligns deck and dock;vehicle secured','C01','No precise loadingIN/OUTclaimedfrom sampled cues.'),
'A04-P07':('PH06','Voyage transition','C01','PH06is laterresupplycontext,not first departure;prefer cleared ship context.'),
'A05-P08':('PH07','Shipboard preparation','NEED_VOYAGE_WORK_SOURCE','Crew photois Antarctica1940context,not actual voyagework.'),
'A05-P09':('PH10','Hatch constraint,seaice,shelf approach','C02','Preserve seaice/iceshelf distinction.'),
'A05-P01':('PH14','Resume ramp incident with aftermath','C02;C04','Do not repeat opening as second fullclimax.'),
'A05-P03':('PH09','Inspection vs tyresinking','C04','Do not invent damage from ramp causing snowproblem.'),
'A05-P10':('PH04','Hot motors,rest,approach','C03','Torchphotoillustrates maintenance,not that exact rest stop.'),
'A05-P04':('','Planks under tyres and repeated shortapproaches','NEED_PLANK_SOURCE','No archival plank-operationfootage exists in acceptedpackage.'),
'A05-P05':('PH09','Single passable patch vs dependable route','','Avoid identical still fakecuts;coveragegap if source already exhausted.'),
'A05-P07':('PH07','Dependability becomes central question','','Use human consequence;no second mechanismrecap.'),
'A06-P01':('PH04','Tyre support vs grip','G03','Never derive measured contactpressurefrom tyre diameter.'),
'A06-P03':('','1955comparison3500vs17500lb perwheel','G03;D02','Retrospective date;not totalvehiclemass.'),
'A06-P05':('','Available tyre mold and schedule','G03;ENG40','No copyrightedpage facsimile silently cleared.'),
'A06-P06':('','Strongtyre vs weak snow support','G03','One visualpayoff,not repeated titlecard.'),
'A06-P07':('PH04','Heating during poorprogress','','Maintenance context,not a specific instrumentreading.'),
'A06-P08':('PH02','Two sparetyres become available intervention','G04','Dogs haul tyreonly.'),
'A07-P01':('','Dual fronts and rear chains','G04;FR86FIG5','600x350figureisreference-only;do notimport.'),
'A07-P02':('','Pressure/drive experiments','G04','No exactpressurefigure,no invented numericalgains.'),
'A07-P03':('PH09','Shortmovement not reliable expeditiontravel','','Not92mile reversejourney.'),
'A07-P04':('PH08','Try colder snow;wintertransition','','No exactdeparturedate or inventedprivateemotion.'),
'A07-P05':('PH11','Excavation ->climbs out ->brief improvement','CANDIDATE_SPRING_ARCHIVE','PH11contextonly,not proof ofthat exactspringtrial.'),
'A07-P06':('PH04;PH08','Blockage cleared ->wheelssink again','','No fabricatedalarm,injury or final-ever-movementclaim.'),
'A07-P07':('PH03','Stationaryshelter stilluseful','','Let consequence land;no promotionalCTA.'),
'A08-P02':('PH04;PH03;PH02','Realpeople and practicaljobs','','Photos have distinct roles;avoid repeating earlier framing just to filltime.'),
'A08-P03':('PH07','Winterwork restricted toWestBase','','Like+8sec for3sec;WarnerNOTidentified inPH07portrait.'),
'A08-P04':('','Icelaboratory snow samples;science onlocation','GL47;NEED_SCIENCE_SOURCE','LabfloorNOTCruiserfloor;no detached methodlecture.'),
'A08-P06':('PH08','War shortened expedition;vehicle left','','NoPearlHarborcausation afterevacuation.'),
'A08-P07':('','Visitors return yearslater','G05','Datechange,not genericicefloatstockpretendingtobehistorical.'),
'A09-P01':('DOC_HIGHJUMP_P347','1947unauthorized entry andvandalism','','Onegovernmentreport;textpageonly.'),
'A09-P02':('DOC_HIGHJUMP_P396','1947rooflevelwith snow','','No modernburialdepth extrapolation.'),
'A09-P03':('DOC_HIGHJUMP_P347;DOC_HIGHJUMP_P396','Observationdoesnotprove successfulrestart','','No ready-to-drivelegend.'),
'A09-P04':('','January1958excavation','G05;SC05','Original1958photo notacquired;no1958labelon1940image.'),
'A09-P05':('MAP_CIA_1956','Geographicorientation nearBayofWhales','G05','1956basemapcontextonly;not precise1958iceedge.'),
'A09-P06':('','Location reconstructed from datedvisits','G05','Originalhypothesismapnot recoveredwreckimage.'),
'A09-P07':('','Canstationaryvehicleleavewithice?','G05','Do notgive definitivefinalvehiclelocation.'),
'A10-P01':('','1957-1962regionalcalvinginference','G05;SC05','No exactdayofvehicledisappearance.'),
'A10-P02':('ST04_ICE_FLOES','Possible journeywithcalvedice','G05','ModernLarsenC2016contextlabel;notRoss1960footage.'),
'A10-P09':('','1963specificicebergclue','G05','Probablynotaboardthisberg;not a confirmedvehiclesighting.'),
'A10-P03':('','Possible seabedarea,unknownrestingplace','G05','No scannedcopyrightedpaperdiagram or fakewreck.'),
'A10-P04':('PH04;PH03','Return topeopleandwork','','Use only purposefulreturn,not randommontagerepeat.'),
'A10-P07':('','Researchleaves;machineleft;laterdigging','G05','1958evidenceattributed,noglobal-last-everclaim.'),
'A10-P08':('PH07','Humanworkvsunresolvedmachinefate','','FinishhistoricalemotionbeforeCampbridge.'),
'A10-CTA01':('','CampCenturytransition','EXISTING_APPROVED_ENDSCREEN_BACKGROUND','Do notgeneratebuttonorplaceholder;Subscribe+SpecificVideoaftervoice.')
}
paras=re.findall(r'^\[([^]]+)\] (.+)$',(P/'05_SCRIPT_R5_1_EN.md').read_text(encoding='utf-8'),re.M);assert set(mapping)=={k for k,t in paras}
tim={x['paragraph_id']:x for x in readcsv(P/'SOURCE_FILES/FINAL_SCRIPT_QC/PARAGRAPH_TIMING.csv')}
mi={x['asset_id']:x for x in media};sourcecross={x['paragraph_id']:x for x in readcsv(P/'SOURCE_FILES/FINAL_SCRIPT_QC/R5_1_SOURCE_CROSSWALK.csv')}
beats=[]
for k,t in paras:
 primary,reason,needs,limit=mapping[k];ready=[a for a in primary.split(';') if a in mi]
 needs=[a for a in needs.split(';') if a]
 status='SOURCE_GAP_OR_UNBUILT_GRAPHIC' if not ready else ('LIMITED_READY_PLUS_DEPENDENCY' if needs else 'LIMITED_READY_SOURCE_CONTEXT_ONLY')
 if k=='A10-CTA01':status='ENDSCREEN_BACKGROUND_CONFIRMATION_PENDING'
 beats.append(dict(paragraph_id=k,act=k[:3],narration=t,phrase_anchor=t.split('.')[0],primary_ready_asset_ids=';'.join(ready),primary_ready_paths=';'.join(mi[a]['edit_package_path'] for a in ready),required_graphic_or_held_source=';'.join(needs),purpose=reason,director_limit=limit,provenance=';'.join(mi[a]['provenance_class'] for a in ready),canonical_claim_ids=sourcecross[k]['canonical_claim_ids'],r4_source_change_ids=sourcecross[k]['r4_fact_change_ids'],transition='Clean cut on semantic phrase;time-shift dissolve only where justified',motion='Static by default;named subject inspection only if source pixels permit;no automatic zoom/drift/shake',estimated_start_at140=tim[k]['start_at140'],estimated_end_at140=tim[k]['end_at140'],actual_start_frame='',actual_end_frame='',audio_sync_status='HOLD_UNTIL_VOICE_ASR',coverage_status=status))
writecsv(P/'11_VISUAL_BEATS_R5_1.csv',beats);writecsv(E/'VISUAL_BEATS.csv',beats)
graphics=[
dict(id='G01',paragraphs='A01-P03;A02-P02;A02-P03;A03-P01',purpose='Mobile-base functions and intendedrooms',source='D03PDF20-21;C003/C007/C011/C012',build='Editable labelledschematicbasedonpublishedlayout;cleanink/charcoalvisualreference;accentsseparate',limits='No photoreal archivedinterior,no forgeddocument,no opaqueHUDcard',status='BRIEF_READY_ASSET_NOT_BUILT'),
dict(id='G02',paragraphs='A03-P03;A03-P04;A03-P05',purpose='Bodyasbridge and wheel-retractionsequence',source='D03PDF21;C014-C017',build='Nativeeditable3-phaseconceptdiagram;controlledloadtransferreveal',limits='Proposed15ftcapability,not successfulcrossing;no fakeasuredcrevasse',status='BRIEF_READY_ASSET_NOT_BUILT'),
dict(id='G03',paragraphs='A06-P01;A06-P03;A06-P05;A06-P06',purpose='Supportvsgrip;1955per-wheelloadcomparison',source='USACEPDF34/54;C029-C033',build='Two verifiedvalues3500/17500lbperwheel;schematiccontact/supportlogic;transparentlocallabels',limits='Do not calculatecontactpressurefromdiameter,sumvehiclemass,orclaimactualsnowtest;no giantwhitebackgroundcard',status='BRIEF_READY_ASSET_NOT_BUILT'),
dict(id='G04',paragraphs='A06-P08;A07-P01;A07-P02',purpose='What changed:frontspares,rearchains,pressureattempt',source='FR86Fig5reference;C035-C037;N15',build='Source-informedschematicaxlesandtyres;separatereveals;no bakedhighlights',limits='Exactcontact-area/pressuregainsunknown;Fig5originalrights/HDHOLD',status='BRIEF_READY_ASSET_NOT_BUILT'),
dict(id='G05',paragraphs='A08-P07;A09-P04;A09-P06;A10-P01;A10-P09;A10-P03',purpose='Datedvisitsvsregionalcalvinginferenceandunknownfate',source='HI47;SC05PDF8/14;C048-C055;N22',build='Nativeeditabletimeline/qualifiedgeographicorientation;modernearthbaseonlyascontext',limits='No inventedpreciseoldcoastline,wreckcoordinates,recoveredvehicleorcopiedpaperfigure',status='BRIEF_READY_ASSET_NOT_BUILT')
]
existing_graphics_path=P/'12_GRAPHICS_BUILD_BRIEFS_R5_1.csv'
existing_graphics={x['id']:x for x in readcsv(existing_graphics_path)} if existing_graphics_path.exists() else {}
for item in graphics:
 for key in ['reference_files','reference_sha256','reference_scope']:
  if key in existing_graphics.get(item['id'],{}):item[key]=existing_graphics[item['id']][key]
writecsv(P/'12_GRAPHICS_BUILD_BRIEFS_R5_1.csv',graphics);writecsv(E/'GRAPHICS_BUILD_BRIEFS.csv',graphics)
summary=dict(ready_source_assets=len(media),direct_media_import_files=sum(x['kind']!='geodata' for x in media),nonmedia_geodata_files=1,curated_existing_assets=19,official_text_pages=2,sfx_existing_cc0_candidates=len(sfx),paragraph_beats=len(beats),limited_ready_source_rows=sum(bool(x['primary_ready_asset_ids']) for x in beats),rows_without_ready_primary=sum(not x['primary_ready_asset_ids'] for x in beats),native_graphic_briefs=5,graphics_completed=0,approved_unique_historical_motion_seconds=0,all69_audio_sync='HOLD',full_edit_ready=False,media_files_hash_verified=True,no_held_asset_in_import_list=True,montage_started=False,source_package=str(E))
(R/'EDIT_PREP_VERIFICATION.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(E/'PACKAGE_STATE.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary))
