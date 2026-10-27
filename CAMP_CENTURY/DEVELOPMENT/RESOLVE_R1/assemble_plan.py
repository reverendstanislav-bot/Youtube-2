from pathlib import Path
import csv,json,re,math,difflib,subprocess,hashlib

ROOT=Path(__file__).resolve().parent
CAMP=ROOT.parents[1]
GFX=CAMP/'GRAPHICS'
ARCH=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
AUDIO=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1')
FPS=25;TOTAL=27368

# Existing 32-beat V4 route; exact spoken phrase anchors select the visual changes.
# R = authentic registered reference, G = approved concept, M = motion adaptation,
# C = factual native graphic, CC07-Cxxx = verified moving source selection.
ROUTES=[
 [('M03',''),('CC07-C026','This was Camp Century'),('M01','sleeping quarters'),('CC07-C028','Tracked vehicles'),('R06_PROFILES','measurements'),('C04','twelve percent')],
 [('R07_ESTIMATE',''),('M07','estimate not a record'),('CC07-C010','surviving film'),('R01_COVER','published engineering report'),('R03_ARCH','arches and rooms'),('CC07-C029','Everything looks finished')],
 [('C05',''),('R02_PLAN','The base was real'),('CC07-C021','clearly could'),('M09','first clue')],
 [('CC07-C054',''),('CC07-C055','no construction site'),('R32_GREENLAND_ONLY','Danish realm'),('M09','staging area')],
 [('C01',''),('CC07-C004','Tractors pull'),('G12','special sleds'),('CC07-C006','white horizon'),('CC07-C003','cargo tells'),('C02A','first season')],
 [('C02B',''),('G13','Spare parts'),('CC07-C007','conditions change'),('CC07-C008','hidden cost'),('CC07-C027','functioning camp')],
 [('G11',''),('CC07-C014','easier to cut')],
 [('CC07-C011',''),('M10','It cuts'),('M02','next step'),('CC07-C012','cut and cover'),('G04','pressure and temperature')],
 [('R03_ARCH',''),('M11','metal arches'),('CC07-C015','larger openings'),('CC07-C016','forty feet'),('R25_PREMATURE_FORMS','temporary roof forms')],
 [('R25_PREMATURE_FORMS',''),('G14','leave the support forms'),('CC07-C018','buildings were only'),('R02_PLAN','main street'),('R26_UTILITY_LINES','smaller passages'),('CC07-C022','operating settlement')],
 [('G01',''),('G04','Heat')],
 [('CC07-C043',''),('C16','diesel generators'),('G16','second idea'),('CC07-C039','electrical and heating'),('R04_BUDGET','seven point nine')],
 [('C03',''),('CC07-C031','reactor arrived'),('CC07-C036','assemble it'),('CC07-C040','reactor produced heat'),('C15','figures measure different')],
 [('CC07-C042',''),('M04','base required water'),('R27_WATER_WELL','recover usable water'),('R28_SEWAGE_PROFILE','disposal sumps'),('R10_SUMP','four feet')],
 [('R10_SUMP',''),('CC07-C041','turbine generator'),('R34_TURBINE_RECORD','mechanical troubles'),('G15','more there was to maintain'),('R31_PLANT_PLANNING','planned before'),('C08','extraordinary idea')],
 [('CC07-C044',''),('CC07-C047','comfortable rooms'),('CC07-C088','scientific work'),('CC07-C048','research connected'),('C05','Project Iceworm')],
 [('C05',''),('C05_QUALIFIER','Those numbers describe a proposal'),('C05_AREA','one hundred thirty five'),('R02_PLAN','experimental subsurface railway'),('C09','short experimental track')],
 [('R26_UTILITY_LINES',''),('CC07-C020','crews would all'),('C09','multiplied thousands'),('R32_GREENLAND_ONLY','Kingdom of Denmark'),('C10','political consent'),('C11','rival technologies')],
 [('C11',''),('R02_PLAN','never completed'),('G19','Keeping a vast network')],
 [('G19',''),('M03','roof settles'),('R11_DISTRESS','scale of what maintaining'),('R06_PROFILES','two diagrams')],
 [('R06_PROFILES',''),('C04','twelve percent'),('R29_MAIN_HEIGHT_TABLE','average annual vertical'),('R30_SIDE_HEIGHT_TABLE','thirty four inches'),('C07','clearance losses'),('R11_DISTRESS','continuing construction')],
 [('G19',''),('R07_ESTIMATE','twenty thousand'),('M07','maintenance estimate'),('CC07-C051','You build the city'),('M10','keep rebuilding')],
 [('G20',''),('CC07-C052','Warm air'),('R25_PREMATURE_FORMS','forms had been removed'),('R08_CHAINSAW','Figure thirty three'),('CC07-C050','ordinary maintenance task'),('G07','More snow')],
 [('G06',''),('R06_PROFILES','measurements showed'),('CC07-C053','what the experiment')],
 [('R12_SHUTDOWN',''),('CC07-C057','removed the following year'),('CC07-C059','Seasonal work continued'),('CC07-C060','Then Camp Century'),('CC07-C064','Army had proved')],
 [('CC07-C067',''),('M08','reactor hardware was taken out'),('G22','Materials structures and wastes'),('CC07-C081','snowfall would continue'),('R33_FIRN_FORECAST','One study')],
 [('C13',''),('R33_FIRN_FORECAST','twenty twenty one study'),('C13_2100','remain largely immobile'),('R32_GREENLAND_ONLY','Denmark established'),('G24','one last twist')],
 [('R15_DRILL_1966',''),('G08','researchers had drilled'),('G24','much older')],
 [('R15_DRILL_1966',''),('M05','more than a thousand'),('R13_CORE_2021','recovered frozen material'),('R24_FROZEN_ARCHIVE','samples were stored'),('M12','Copenhagen')],
 [('M12',''),('G09','ancient plants'),('R13_CORE_2021','far older landscape'),('M06','NASA aircraft'),('R14_RADAR_2024','instrument detected')],
 [('R14_RADAR_2024',''),('G22','Not an accessible city'),('C14','one hundred feet'),('CC07-C024','Army film shows'),('M06','radar shows'),('G24','scientific core')],
 [('CC07-C025',''),('G06','could not make'),('C11','never existed'),('R08_CHAINSAW','film of the men'),('R06_PROFILES','measurements showing'),('M08','structures and samples'),('G01','engineering warning')]
]

def norm(s):
    small=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens={20:'twenty',30:'thirty',40:'forty',50:'fifty',60:'sixty',70:'seventy',80:'eighty',90:'ninety'}
    def number(n):
        if n<20:return small[n]
        if n<100:return tens[n//10*10]+(' '+small[n%10] if n%10 else '')
        if n<1000:return number(n//100)+' hundred'+(' '+number(n%100) if n%100 else '')
        if 1900<=n<2000:return 'nineteen '+number(n%100)
        if 2000<=n<2100:return 'twenty '+number(n%100)
        if n==20000:return 'twenty thousand'
        return str(n)
    s=re.sub(r'(?<=\d),(?=\d)','',s.lower().replace('’',"'")).replace('%',' percent').replace('iceworm','ice worm')
    tokens=[]
    for token in re.findall(r'[a-z0-9]+',s):tokens.extend(number(int(token)).split() if token.isdigit() else [token])
    return tokens
def words():return json.loads((AUDIO/'ASR_QC/CAMP_CENTURY_MASTER_WORDS_SMALL_EN.json').read_text(encoding='utf-8-sig'))
def anchor(phrase,beat,allwords,frac):
    start=float(beat['audio_start_sec']);end=float(beat['audio_end_sec'])
    if not phrase:return start,1.,'BEAT_START'
    ws=[w for w in allwords if float(w['start'])>=start-.1 and float(w['start'])<end]
    tokens=[]
    for w in ws:
        tokens.extend((t,float(w['start'])) for t in norm(w['text']))
    target=norm(phrase);best=(0,None)
    for i in range(len(tokens)):
        for n in range(max(1,len(target)-2),len(target)+3):
            q=[t[0] for t in tokens[i:i+n]]
            score=difflib.SequenceMatcher(None,target,q).ratio()
            if score>best[0]:best=(score,tokens[i][1])
    if best[0]>=.68:return best[1],best[0],'ASR_PHRASE'
    return start+(end-start)*frac,best[0],'BEAT_BOUNDED_EDITORIAL_FALLBACK'

def registry():
    refrows=list(csv.DictReader((GFX/'STAGE07_GENERATION_PREP_R2/REFERENCE_REGISTER.csv').open(encoding='utf-8-sig')))
    refs={r['reference_id']:dict(path=str(GFX/'STAGE07_GENERATION_PREP_R2'/r['file']),kind='PRIMARY_REFERENCE',title=r['title'],rights=r['rights'],source=r['source_url'],locator=r['source_locator']) for r in refrows}
    gen=json.loads((GFX/'STAGE07_GENERATED_R1/GENERATION_MANIFEST.json').read_text())
    for r in gen:
        if r['asset_id'] in ['G17','G18']:continue
        refs[r['asset_id']]=dict(path=str(GFX/'STAGE07_GENERATED_R1'/r['file']),kind='GENERATED_CONCEPT',title=r['title'],rights='Generated illustration; retain reference provenance; not archival evidence',source=r['references'],locator='Concept, qualitative geometry')
    for r in json.loads((GFX/'STAGE07_MOTION_READY_R1/MOTION_PLAN.json').read_text()):
        refs[r['id']]=dict(refs[r['source_asset']],path=str(GFX/'STAGE07_MOTION_READY_R1'/r['base']),motion=r['id'])
    for mid,gid in [('M09','G12'),('M10','G02'),('M11','G14'),('M12','G23')]:refs[mid]=dict(refs[gid],path=str(GFX/'STAGE07_MOTION_PEOPLE_R2/assets'/f'{mid}_BASE.png'),motion=mid)
    clips=list(csv.DictReader((ARCH/'reports/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig')))
    for r in clips:
        refs[r['scene_id']]=dict(path=r['cut_filename'],kind='REAL_ARCHIVE_MOTION',title=r['actual_shot_description'],rights=r['rights_status'],source=r['source_url'],locator=f"{r['source_id']} source IN {r['start_tc']} OUT {r['end_tc']}",source_in_sec=float(r['start_tc']),source_out_sec=float(r['end_tc']),source_sha256=r['source_sha256'],native_fps=r['source_fps'],duration=float(r['cut_seconds']),site_class=r['site_class'],warning=r['editorial_warning'])
    chart_text={
    'C01':['CAMP TUTO → CAMP CENTURY','138 MILES','APPROXIMATE SUPPLY DISTANCE'],
    'C02A':['1959 CONSTRUCTION FREIGHT','≈ 1,000 SHORT TONS','REPORTED SEASONAL TOTAL'],
    'C02B':['1960 CONSTRUCTION FREIGHT','≈ 4,600 SHORT TONS','TWO SEASONS: ≈ 5,600 TOTAL'],
    'C03':['INITIAL CONSTRUCTION COST','PM-2A  $5.7 MILLION','TOTAL  $7.92 MILLION  //  PERIOD USD'],
    'C04':['MEASURED LOCAL CROSS-SECTIONS','MAIN  12%  //  SIDE  17%','AREA LOSS PER YEAR  //  TWO LOCAL EXAMPLES'],
    'C05':['PROJECT ICEWORM — PROPOSAL','≈ 600 MISSILES','NEVER DEPLOYED'],
    'C05_QUALIFIER':['PROJECT ICEWORM — PROPOSAL','OVER 2,000 POSSIBLE POSITIONS','NOT COMPLETED SILOS'],
    'C05_AREA':['PROJECT ICEWORM — PROPOSAL','≈ 135,000 km²','PROPOSED NETWORK  //  NEVER BUILT'],
    'C07':['AVERAGE VERTICAL CLOSURE','MAIN  ≈16 in/yr   SIDE  ≈34 in/yr','HEIGHT LOSS  //  DISTINCT FROM AREA LOSS'],
    'C08':['SEPARATE HISTORICAL EVENTS','PLANT PLANNING → LATER ICEWORM PROPOSAL','PLANT COST ≠ PROOF OF MISSILE-PROGRAM FUNDING'],
    'C09':['RESEARCH INSTALLATION ≠ DEPLOYED NETWORK','MAINTENANCE  /  POWER  /  CREWS','AN EXPERIMENTAL TRACK WAS BUILT'],
    'C10':['GREENLAND — DANISH REALM','RESEARCH BASE ≠ WEAPONS CONSENT','POLITICAL AUTHORIZATION WAS A SEPARATE QUESTION'],
    'C11':['PROJECT ICEWORM','REJECTED IN 1963','MISSILE NETWORK NEVER COMPLETED'],
    'C13':['LATER CLIMATE STUDIES','A SCENARIO ≠ AN OBSERVED SPILL','MODEL ASSUMPTIONS MATTER'],
    'C13_2100':['2021 STUDY — AS SUMMARIZED BY GAO','LARGELY IMMOBILE THROUGH 2100','A PROJECTION, NOT AN OBSERVED RELEASE'],
    'C14':['NASA — 2024 STRUCTURAL REMAINS','AT LEAST 100 FEET BELOW THE SURFACE','SEPARATE FROM THE DEEP 1966 ICE CORE'],
    'C15':['TWO DIFFERENT POWER QUANTITIES','≈10 MW THERMAL  //  ≈1.5 MW ELECTRIC','HEAT OUTPUT ≠ DELIVERED ELECTRICITY'],
    'C16':['SUPPLY BURDEN','DIESEL FUEL  /  REMOTE MAINTENANCE','THE CAMP NEEDED BOTH POWER AND HEAT']}
    for key,lines in chart_text.items():refs[key]=dict(path=str(ROOT/'FUSION_CARRIER_60S_25FPS.mp4'),kind='FACTUAL_NATIVE_GRAPHIC',title=lines[0],rights='Editorial graphic based on locked V4 and cited evidence ledger',source='STAGE04_CLAIM_BY_CLAIM_EVIDENCE_LEDGER_V1.csv + VERIFIED_CHART_DATA.csv',locator='No invented measurements, routes, weapon design or deployment geometry',lines=lines)
    return refs

def main():
    beats=list(csv.DictReader((AUDIO/'ASR_QC/STAGE08_CAMP_CENTURY_BEATS_AUDIO_ALIGNED_V1.csv').open(encoding='utf-8-sig')))
    assert len(beats)==len(ROUTES)==32
    assert hashlib.sha256((AUDIO/'HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav').read_bytes()).hexdigest()=='c6a5df8cff089418f4f2300551fd4ba6cb057dcd3012b84fa8143e02976d0480'
    refs=registry();aw=words();shots=[];used={};warnings=[]
    for bi,(beat,route) in enumerate(zip(beats,ROUTES)):
        bstart=round(float(beat['audio_start_sec'])*FPS)
        bend=round(float(beats[bi+1]['audio_start_sec'])*FPS) if bi+1<len(beats) else TOTAL
        events=[]
        for i,(asset,phrase) in enumerate(route):
            sec,score,basis=anchor(phrase,beat,aw,i/len(route))
            events.append(dict(asset=asset,start=max(bstart,min(bend-1,round(sec*FPS))),cue=phrase,score=score,basis=basis))
        # Keep the declared story order even when a noisy ASR phrase matches earlier.
        for i in range(1,len(events)):
            if events[i]['start']<=events[i-1]['start']:
                events[i]['start']=round(bstart+(bend-bstart)*i/len(events));events[i]['basis']='BEAT_BOUNDED_EDITORIAL_FALLBACK'
        events.sort(key=lambda e:e['start'])
        events[0]['start']=bstart
        # Short voice phrases share a shot; archival actions keep >=5 seconds.
        filtered=[events[0]]
        for ev in events[1:]:
            prev=filtered[-1];minimum=125 if refs[prev['asset']]['kind']=='REAL_ARCHIVE_MOTION' else 85
            if ev['start']-prev['start']<minimum:continue
            filtered.append(ev)
        if len(filtered)>1 and bend-filtered[-1]['start']<75:filtered.pop()
        for i,ev in enumerate(filtered):
            end=filtered[i+1]['start'] if i+1<len(filtered) else bend
            r=refs[ev['asset']];dur=end-ev['start']
            intervals=[(ev['asset'],ev['start'],end)]
            if r['kind']=='REAL_ARCHIVE_MOTION':
                # One bounded use of each original action; do not loop/stretch footage.
                available=math.floor(r['duration']*FPS)
                if ev['asset'] in used:
                    warnings.append(dict(beat=beat['beat_id'],asset=ev['asset'],warning='DUPLICATE_AVOIDED_REPLACED_WITH_PRIMARY_EVIDENCE'))
                    alt='R02_PLAN' if beat['chapter'] not in ['CH07','CH08'] else ('R12_SHUTDOWN' if beat['chapter']=='CH07' else 'R15_DRILL_1966')
                    intervals=[(alt,ev['start'],end)]
                elif dur>available:
                    if available>=125 and dur-available>=75:
                        alt='R02_PLAN' if beat['chapter'] not in ['CH07','CH08'] else ('G22' if beat['chapter']=='CH07' else 'R15_DRILL_1966')
                        intervals=[(ev['asset'],ev['start'],ev['start']+available),(alt,ev['start']+available,end)]
                    else:
                        alt='G01' if beat['chapter'] not in ['CH07','CH08'] else 'G22'
                        intervals=[(alt,ev['start'],end)]
            for aid,si,so in intervals:
                rr=refs[aid];used[aid]=used.get(aid,0)+1
                shots.append(dict(shot_id=f'S{len(shots)+1:03}',beat_id=beat['beat_id'],chapter=beat['chapter'],asset_id=aid,start_frame=si,end_frame=so,duration_frames=so-si,start_seconds=si/FPS,end_seconds=so/FPS,voice_cue=ev['cue'],alignment_basis=ev['basis'],alignment_score=round(ev['score'],3),**rr))
    assert shots[0]['start_frame']==0 and shots[-1]['end_frame']==TOTAL
    assert all(a['end_frame']==b['start_frame'] for a,b in zip(shots,shots[1:]))
    assert all(s['asset_id'] not in ['G17','G18','C06','D07'] for s in shots)
    missing=[s['path'] for s in shots if not Path(s['path']).is_file()]
    assert not missing,missing
    (ROOT/'SHOT_PLAN_R1.json').write_text(json.dumps(shots,indent=2,ensure_ascii=False),encoding='utf-8')
    fields=['shot_id','beat_id','chapter','asset_id','kind','start_frame','end_frame','duration_frames','voice_cue','alignment_basis','alignment_score','path','title','rights','source','locator']
    with (ROOT/'SHOT_PLAN_R1.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(shots)
    (ROOT/'BEATS_AUDIO_LOCKED.json').write_text(json.dumps(beats,indent=2),encoding='utf-8')
    (ROOT/'PLANNING_WARNINGS.json').write_text(json.dumps(warnings,indent=2),encoding='utf-8')
    summary=dict(shots=len(shots),beats=len(beats),duration=TOTAL/FPS,frame_rate=FPS,archive_seconds=sum(s['duration_frames']/FPS for s in shots if s['kind']=='REAL_ARCHIVE_MOTION'),native_graphics_seconds=sum(s['duration_frames']/FPS for s in shots if s['kind']=='FACTUAL_NATIVE_GRAPHIC'),fallback_alignments=sum(s['alignment_basis']=='BEAT_BOUNDED_EDITORIAL_FALLBACK' for s in shots),no_visual_gaps=True,excluded=['G17','G18','C06 disputed rediscovery date','D07 unavailable GAO PDF'])
    (ROOT/'ASSEMBLY_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))

if __name__=='__main__':main()
