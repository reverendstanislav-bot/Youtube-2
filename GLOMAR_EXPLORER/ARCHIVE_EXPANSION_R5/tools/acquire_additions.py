"""Acquire originals with saved item-level attribution and license evidence."""
from pathlib import Path
import csv, sys, json, urllib.request, urllib.parse, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent
(ROOT/'ORIGINALS').mkdir(exist_ok=True)
(ROOT/'EVIDENCE').mkdir(exist_ok=True)
headers={'User-Agent':'HIA-Documentary-Research/1.0 (public collection verification)'}
def read(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=40) as r:return r.read()
rows=list(csv.DictReader((PROJECT/'ARCHIVE_R1/ASSET_REGISTER.csv').open(encoding='utf-8-sig')))
selected=[r for r in rows if r['asset_id'] in ['C05','C08','C10','C11']]
def acquire(row):
    aid=row['asset_id'];title=urllib.parse.unquote(row['source_page'].split('/wiki/')[-1])
    api='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata','format':'json'})
    try:
        raw=read(api);(ROOT/'EVIDENCE'/f'{aid}_COMMONS_ITEM.json').write_bytes(raw)
        page=next(iter(json.loads(raw)['query']['pages'].values()));info=page['imageinfo'][0];meta=info['extmetadata']
        url=info['url'].split('?')[0];data=read(url);target=ROOT/'ORIGINALS'/(aid+Path(urllib.parse.urlparse(url).path).suffix);target.write_bytes(data)
        return {'asset_id':aid,'title':page['title'],'source_page':row['source_page'],'download_url':url,'local_file':str(target.relative_to(ROOT)),'bytes':len(data),'width':info['width'],'height':info['height'],'sha256':hashlib.sha256(data).hexdigest(),'license':meta.get('LicenseShortName',{}).get('value'),'license_url':meta.get('LicenseUrl',{}).get('value'),'artist_html':meta.get('Artist',{}).get('value'),'date_html':meta.get('DateTimeOriginal',{}).get('value'),'source_html':meta.get('Credit',{}).get('value'),'description_html':meta.get('ImageDescription',{}).get('value'),'status':'DOWNLOADED_ITEM_EVIDENCE_SAVED'}
    except Exception as e:return {'asset_id':aid,'status':'ERROR','error':str(e)}
previous=ROOT/'ACQUISITION_RESULTS.json'
results=json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else []
for row in selected:
    x=acquire(row)
    results=[r for r in results if r['asset_id']!=x['asset_id']]
    results.append(x)
    print(json.dumps({k:v for k,v in x.items() if k not in ['description_html','source_html','artist_html']},ensure_ascii=False),flush=True)
(ROOT/'ACQUISITION_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
q='title:(Hughes) AND collection:universal_newsreels'
url='https://archive.org/advancedsearch.php?'+urllib.parse.urlencode({'q':q,'output':'json','rows':50,'fl[]':['identifier','title','licenseurl','description']},doseq=True)
try:
    raw=read(url);(ROOT/'EVIDENCE/IA_HUGHES_NEWSREEL.json').write_bytes(raw)
    for x in json.loads(raw)['response']['docs']: print('NEWSREEL',x.get('identifier'),x.get('title'),flush=True)
except Exception as e:print('NEWSREEL_ERROR',str(e),flush=True)
