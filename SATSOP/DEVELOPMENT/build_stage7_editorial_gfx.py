from pathlib import Path
import hashlib,html,json,subprocess

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'STAGE_7'/'EDITORIAL_GFX'; OUT.mkdir(parents=True,exist_ok=True)
specs={
'SAT-B007':('PROJECT 4 / PROJECT 5','HANFORD  →  Satsop','Two sites. One financing warning.','MAP'),
'SAT-B009':('BONDS SOLD','$2.25 BILLION','Projects 4 + 5 combined','GFX'),
'SAT-B010':('COMPLETION ESTIMATE','$12B','~$8.5B above original combined estimate','GFX'),
'SAT-B013':('FEDERAL HYDRO SYSTEM','PACIFIC NORTHWEST','The region’s dominant mid-century supply','MAP'),
'SAT-B014':('1966 FORECAST','DEMAND > HYDRO PLAN','Regional thermal planning begins','MAP'),
'SAT-B018':('FIVE PROJECTS','ONLY PROJECT 2 OPERATED','Commercial service: December 1984','MAP'),
'SAT-B020':('TAKE OR PAY','PAYMENTS REMAIN DUE','Completed, operable, or operating: not required','GFX'),
'SAT-B022':('CONSTRUCTION ENDS','DEBT SERVICE CONTINUES','Cost without delivered power','GFX'),
'SAT-B028':('PROJECT 3','NET BILLING + BPA','Earlier financing structure','GFX'),
'SAT-B030':('PROJECT 3','70% NET-BILLED','Costs credited through wholesale power bills','GFX'),
'SAT-B033':('VISIBLE CONCRETE','INVISIBLE RISK','Who carries the next dollar?','GFX'),
'SAT-B034':('EACH SATSOP UNIT','REACTOR • AUXILIARY • TURBINE','Cooling • transmission • support systems','MAP'),
'SAT-B051':('FOUR DECISION TESTS','COMPETITIVENESS • NEED','Alternatives • risk','GFX'),
'SAT-B055':('COMPLETION COST ↑','CUSTOMER OPTIONS OPEN','No invented price series','GFX'),
'SAT-B057':('SUNK COST','$2.6B (1993 DOLLARS)','Past spending cannot answer future risk','GFX'),
'SAT-B063':('HYDRO VARIABILITY','FLEXIBLE DISPATCH','Water conditions + modular additions','MAP'),
'SAT-B064':('COMBINED CYCLE','MORE VARIABLE COST','More avoidable when not producing','GFX'),
'SAT-B065':('PROJECT 3','LARGER FIXED-COST SHARE','Obligation persists without output','GFX'),
'SAT-B072':('CAPITAL AT RISK','PROJECT 3 ≈ 3×','Base case vs combined-cycle alternative','GFX'),
'SAT-B073':('LOW PROJECT 3 CASE','2× CAPITAL AT RISK','Compared with combined cycle','GFX'),
'SAT-B075':('SURPLUS SALE CASE','≈ $200M / YEAR DEFICIT','Even at BPA Priority Firm rate','GFX'),
'SAT-B082':('RISK FIELD','8 UNCERTAINTIES','Cost • upgrades • operations • maintenance • waste • decommissioning • regulation • opposition','GFX'),
'SAT-B099':('RECOVERABLE INFRASTRUCTURE','ROADS • BUILDINGS • POWER','Water • wastewater • transmission • fiber','MAP')}

def svg(beat,title,value,note,kind):
    title,value,note=map(html.escape,(title,value,note))
    accent='#F28A3A'; bg='#151A1C'; white='#F2F2ED'; muted='#8D9A9C'; paper='#D2C9B2'
    if kind=='MAP':
        body=f'''<path d="M115 420 C300 250 480 520 665 360 S1010 220 1225 390" fill="none" stroke="{muted}" stroke-width="18"/><circle cx="260" cy="350" r="34" fill="{accent}"/><circle cx="1050" cy="310" r="34" fill="{paper}"/><path d="M260 350 L1050 310" stroke="{white}" stroke-width="4" stroke-dasharray="14 14"/>'''
    else:
        body=f'''<rect x="120" y="360" width="420" height="170" rx="18" fill="#30383A"/><rect x="804" y="280" width="420" height="250" rx="18" fill="#4C5557"/><path d="M575 405 H760" stroke="{accent}" stroke-width="12"/><path d="M735 380 L770 411 L735 442" fill="none" stroke="{accent}" stroke-width="12"/>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1344" height="752" viewBox="0 0 1344 752"><rect width="1344" height="752" fill="{bg}"/><g opacity=".25" stroke="#526063">{''.join(f'<path d="M0 {y} H1344"/>' for y in range(32,752,32))}</g><text x="80" y="82" fill="{accent}" font-family="Arial" font-weight="700" font-size="26">{beat} • EDITORIAL {kind}</text><text x="80" y="155" fill="{white}" font-family="Arial" font-weight="700" font-size="48">{title}</text><text x="80" y="225" fill="{paper}" font-family="Arial" font-weight="700" font-size="58">{value}</text>{body}<rect x="0" y="640" width="1344" height="112" fill="#101416"/><text x="80" y="700" fill="{white}" font-family="Arial" font-size="28">{note}</text></svg>'''

records=[]
for beat,args in specs.items():
    sp=OUT/f'{beat}.svg'; pp=OUT/f'{beat}.png'; sp.write_text(svg(beat,*args),encoding='utf-8')
    subprocess.run([r'C:\Program Files\Google\Chrome\Application\chrome.exe','--headless','--disable-gpu','--hide-scrollbars','--window-size=1344,752',f'--screenshot={pp.resolve()}',sp.resolve().as_uri()],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    records.append({'beat_id':beat,'class':args[3],'svg':sp.name,'png':pp.name,'size_bytes':pp.stat().st_size,'sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'source_basis':['BPA WNP-1 & -3 ROD (1994)','GAO EMD-82-106 (1982)','Stage 5 locked narration']})
(OUT/'STAGE7_EDITORIAL_GFX_MANIFEST.json').write_text(json.dumps({'status':'23/23 BUILT','count':len(records),'files':records},indent=2),encoding='utf-8')
print('built',len(records))
