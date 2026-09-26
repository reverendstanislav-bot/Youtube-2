from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import hashlib,json,re,time

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'STAGE_7'/'SOURCES'; CUR=OUT/'CURRENT_COMMONS'
manifest=json.loads((OUT/'STAGE7_SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
existing={x['source_title'] for x in manifest['commons']}
titles=['File:Satsop Power Plant.jpg','File:Inside an Incomplete Satsop Cooling Tower - Mercator Projection.jpg','File:Satsop Development Park 07780.JPG','File:Satsop Development Park 07781.JPG','File:Satsop Nuclear Cooling Tower (22448062046).jpg','File:Satsop nuclear cooling tower east.jpg','File:Satsop Nuclear Plant.jpg','File:Satsop Nuclear Power Plant (3224050535).jpg','File:Satsop Nuclear Power Plant (3224056575).jpg','File:Satsop Nuclear Power Plant (3224059471).jpg','File:Gryphons soar into Satsop 141112-A-SF231-682.jpg','File:Satsop 141112-A-NC823-220.jpg']
missing=[x for x in titles if x not in existing]
ua={'User-Agent':'HiddenIndustrialAmerica/1.0 (documentary source acquisition)'}
q=urlencode({'action':'query','format':'json','prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':1920,'titles':'|'.join(missing)})
with urlopen(Request('https://commons.wikimedia.org/w/api.php?'+q,headers=ua),timeout=120) as r: pages=json.load(r)['query']['pages']
allowed=('public domain','cc0','cc by','cc-by','pd-')
for page in pages.values():
    title=page['title']; info=page['imageinfo'][0]; meta=info.get('extmetadata',{})
    val=lambda k: re.sub('<[^>]+>','',meta.get(k,{}).get('value',''))
    license_name=val('LicenseShortName'); usage=val('UsageTerms'); rights=(license_name+' '+usage).lower()
    if not any(x in rights for x in allowed): continue
    time.sleep(6)
    asset_url=info.get('thumburl',info['url'])
    with urlopen(Request(asset_url,headers=ua),timeout=180) as r: b=r.read(); final=r.geturl()
    ext=Path(final.split('?')[0]).suffix or '.jpg'; n=len(manifest['commons'])+1; name=f"CUR-{n:02d}_"+re.sub(r'[^A-Za-z0-9._-]+','_',title[5:]).strip('_')[:80]+ext.lower(); p=CUR/name; p.write_bytes(b)
    manifest['commons'].append({'source_title':title,'description_url':info.get('descriptionurl'),'download_url':asset_url,'original_url':info['url'],'creator':val('Artist'),'date':val('DateTimeOriginal') or val('DateTime'),'license':license_name,'usage_terms':usage,'license_url':val('LicenseUrl'),'credit':val('Credit'),'intended_beats':'SAT-B001,SAT-B008,SAT-B041,SAT-B053,SAT-B056,SAT-B092,SAT-B100,SAT-B101,SAT-B104,SAT-B105,SAT-B108,SAT-B109','local_filename':name,'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(OUT/'STAGE7_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print('commons',len(manifest['commons']))
