"""Read public catalogues and save evidence. No paid services or messages."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, urllib.request, urllib.parse, hashlib, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'EVIDENCE'
EVIDENCE.mkdir(parents=True, exist_ok=True)
queries = {
    'IA_GLOMAR_MOVIES': 'glomar AND mediatype:movies',
    'IA_AZORIAN_MOVIES': 'azorian AND mediatype:movies',
    'IA_OCEAN_MINING': 'title:(ocean mining) AND mediatype:movies',
    'IA_SUN_SHIP': '("Sun Shipbuilding" OR "Sun Ship") AND mediatype:movies',
    'IA_COLBY': 'title:(Colby) AND mediatype:movies',
}
jobs = {}
for key, query in queries.items():
    qs = urllib.parse.urlencode({'q':query,'output':'json','rows':100,'fl[]':['identifier','title','description','creator','licenseurl','date','collection']}, doseq=True)
    jobs[key] = 'https://archive.org/advancedsearch.php?' + qs
jobs['COMMONS_GLOMAR'] = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action':'query','generator':'search','gsrsearch':'Glomar Explorer filetype:video','gsrnamespace':6,'gsrlimit':50,'prop':'imageinfo','iiprop':'url|size|extmetadata','format':'json'})
jobs['COMMONS_HISTORIC'] = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action':'query','generator':'search','gsrsearch':'Glomar Explorer 1974','gsrnamespace':6,'gsrlimit':50,'prop':'imageinfo','iiprop':'url|size|extmetadata','format':'json'})
jobs['CIA_GLOMAR_VIDEO'] = 'https://www.cia.gov/legacy/museum/artifact/flag-that-flew-above-the-glomar-explorer/'
jobs['CIA_COPYRIGHT'] = 'https://www.cia.gov/site-policies/'

def fetch(item):
    key,url=item
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'HIA-Documentary-Research/1.0 (public archive verification)'})
        with urllib.request.urlopen(req,timeout=30) as resp:
            data=resp.read(); status=resp.status
        suffix='.json' if data.lstrip().startswith(b'{') else '.html'
        path=EVIDENCE/(key+suffix); path.write_bytes(data)
        result={'id':key,'url':url,'http_status':status,'bytes':len(data),'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest()}
        if key.startswith('IA_'):
            obj=json.loads(data); result['total']=obj.get('response',{}).get('numFound'); result['items']=obj.get('response',{}).get('docs',[])
        elif key.startswith('COMMONS_'):
            obj=json.loads(data); result['items']=list(obj.get('query',{}).get('pages',{}).values())
        return result
    except Exception as exc:
        return {'id':key,'url':url,'error':str(exc)}

results=[]
with ThreadPoolExecutor(max_workers=5) as executor:
    for future in as_completed([executor.submit(fetch,item) for item in jobs.items()]):
        row=future.result(); results.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='items'},ensure_ascii=False),flush=True)
(EVIDENCE/'PUBLIC_CATALOG_RESULTS.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
for row in results:
    if 'items' in row:
        print(row['id'],'items saved:',len(row['items']),flush=True)
