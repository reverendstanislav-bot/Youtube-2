from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import hashlib, json, re, time

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'STAGE_7'/'SOURCES'
DOC=OUT/'DOCUMENTS'; CUR=OUT/'CURRENT_COMMONS'
DOC.mkdir(parents=True,exist_ok=True); CUR.mkdir(parents=True,exist_ok=True)
UA={'User-Agent':'HiddenIndustrialAmerica/1.0 source-acquisition'}

def get(url):
    with urlopen(Request(url,headers=UA),timeout=120) as r: return r.read(),dict(r.headers),r.geturl()

def safe(s): return re.sub(r'[^A-Za-z0-9._-]+','_',s).strip('_')
def record(path,extra):
    b=path.read_bytes(); return {**extra,'local_filename':path.name,'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

docs=[
('DOC-BPA-1994-ROD','https://www.bpa.gov/-/media/Aep/about/publications/records-of-decision/1994-rod/rod-19940513-wnp-1-and-3-study.pdf','U.S. federal agency work; inspect embedded elements','SAT-B045,SAT-B050,SAT-B051,SAT-B059,SAT-B085'),
('DOC-GAO-1982-106','https://www.gao.gov/assets/emd-82-106.pdf','U.S. federal government work','SAT-B009,SAT-B010,SAT-B020,SAT-B022'),
('DOC-GAO-1982-105','https://www.gao.gov/assets/emd-82-105.pdf','U.S. federal government work','finance and termination support'),
('DOC-WA-SSB5445','https://app.leg.wa.gov/documents/billdocs/1993-94/Pdf/Bill%20Reports/Senate/5445-S.SBR.pdf','Washington public record; quote/capture narrowly with attribution','SAT-B050'),
('DOC-NRC-1999-CPPR154','https://www.govinfo.gov/content/pkg/FR-1999-01-29/pdf/99-2133.pdf','U.S. federal government work','SAT-B089'),
('DOC-ENERGY-NW-2021-BUDGET','https://www.energy-northwest.com/whoweare/finance/Documents/2020%20Budget%20docs/Energy%20Northwest%20Fiscal%20Year%202021%20Budget%20Final.pdf','Official owner publication; document excerpt with attribution','SAT-B097')]

manifest={'downloaded_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'documents':[],'commons':[],'errors':[]}
for sid,url,rights,beats in docs:
    try:
        b,h,final=get(url); p=DOC/(sid+'.pdf'); p.write_bytes(b)
        if not b.startswith(b'%PDF'): raise ValueError('not PDF')
        manifest['documents'].append(record(p,{'source_id':sid,'source_url':url,'resolved_url':final,'rights_state':rights,'beats':beats,'mime':h.get('Content-Type','')}))
    except Exception as e: manifest['errors'].append({'source_id':sid,'url':url,'error':repr(e)})

titles=[
'File:Satsop Power Plant.jpg','File:Inside an Incomplete Satsop Cooling Tower - Mercator Projection.jpg',
'File:Satsop Development Park 07780.JPG','File:Satsop Development Park 07781.JPG',
'File:Satsop Nuclear Cooling Tower (22448062046).jpg','File:Satsop nuclear cooling tower east.jpg',
'File:Satsop Nuclear Plant.jpg','File:Satsop Nuclear Power Plant (3224050535).jpg',
'File:Satsop Nuclear Power Plant (3224056575).jpg','File:Satsop Nuclear Power Plant (3224059471).jpg',
'File:Gryphons soar into Satsop 141112-A-SF231-682.jpg','File:Satsop 141112-A-NC823-220.jpg']

allowed=('public domain','cc0','cc by','cc-by','pd-')
for n,title in enumerate(titles,1):
    try:
        q=urlencode({'action':'query','format':'json','prop':'imageinfo','iiprop':'url|extmetadata','titles':title})
        data,_,_=get('https://commons.wikimedia.org/w/api.php?'+q); page=next(iter(json.loads(data)['query']['pages'].values())); info=page['imageinfo'][0]; meta=info.get('extmetadata',{})
        val=lambda k: re.sub('<[^>]+>','',meta.get(k,{}).get('value',''))
        license_name=val('LicenseShortName'); usage=val('UsageTerms'); rights=(license_name+' '+usage).lower()
        if not any(x in rights for x in allowed): raise ValueError('license not allowlisted: '+license_name+' '+usage)
        b,h,final=get(info['url']); ext=Path(final.split('?')[0]).suffix or '.jpg'; p=CUR/(f'CUR-{n:02d}_'+safe(title[5:])[:80]+ext.lower()); p.write_bytes(b)
        if b[:2]!=b'\xff\xd8' and not b.startswith(b'\x89PNG'): raise ValueError('unexpected image magic')
        manifest['commons'].append(record(p,{'source_title':title,'description_url':info.get('descriptionurl'),'download_url':info['url'],'creator':val('Artist'),'date':val('DateTimeOriginal') or val('DateTime'),'license':license_name,'usage_terms':usage,'license_url':val('LicenseUrl'),'credit':val('Credit'),'intended_beats':'SAT-B001,SAT-B008,SAT-B041,SAT-B053,SAT-B056,SAT-B092,SAT-B100,SAT-B101,SAT-B104,SAT-B105,SAT-B108,SAT-B109'}))
    except Exception as e: manifest['errors'].append({'source_title':title,'error':repr(e)})

(OUT/'STAGE7_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'documents':len(manifest['documents']),'commons':len(manifest['commons']),'errors':manifest['errors']},indent=2,ensure_ascii=False))
