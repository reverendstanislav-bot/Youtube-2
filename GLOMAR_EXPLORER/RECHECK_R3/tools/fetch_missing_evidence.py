from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import urllib.request,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'EVIDENCE';OUT.mkdir(exist_ok=True)
urls={
'D07_OCR_COORDINATES.xml':'https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.xml',
'SEC2015_ORIGINAL.html':'https://www.sec.gov/Archives/edgar/data/1451505/000145150515000116/form10_q2q2015.htm',
}
def fetch(item):
 name,url=item
 row={'file':name,'source_url':url}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HIA-Documentary-Research/1.0 (source verification)'}),timeout=25) as response:data=response.read();row['http_status']=response.status
  (OUT/name).write_bytes(data);row.update({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':'DOWNLOADED'})
 except Exception as exc:row.update({'status':'FAILED','error':str(exc)})
 return row
results=[]
with ThreadPoolExecutor(max_workers=2) as pool:
 for f in as_completed([pool.submit(fetch,item) for item in urls.items()]):
  row=f.result();results.append(row);print(json.dumps(row),flush=True)
(OUT/'FETCH_RECEIPT.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
