"""Download source evidence for generation preparation only; no generative calls."""
import requests,json,hashlib,re,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin,urlparse
import pymupdf
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
for d in ['sources','references','prompts','data','qc']:(ROOT/d).mkdir(parents=True,exist_ok=True)
jobs=[
 ('ARMY65','https://icedrill.org/sites/default/files/477706.pdf','ARMY65_TR174.pdf','US federal Army report; inspect per-figure credits; not every photograph in report is Camp Century'),
 ('SCI24_PAGE','https://tc.copernicus.org/articles/18/4029/2024/','SCI24_PAGE.html','CC BY4 article; per-image credit inspection required'),
 ('NASA24_PAGE','https://science.nasa.gov/earth/earth-observatory/new-view-of-the-city-under-the-ice-153616/','NASA24_PAGE.html','NASA named-credit federal media; no endorsement; inspect historical photograph credit'),
 ('GAO24_PAGE','https://www.gao.gov/products/gao-24-104082','GAO24_PAGE.html','US federal report; no unrelated Marshall Islands or Spain images'),
 ('NIELSEN14_RESEARCH_ONLY','https://pure.au.dk/ws/files/81615219/City_under_the_Ice_2014.pdf','NIELSEN14_RESEARCH_ONLY.pdf','Copyright publisher: private research only; NOT a picture-generation input and NOT a public image asset'),
 ('NASA_POLICY','https://www.nasa.gov/nasa-brand-center/images-and-media/','NASA_MEDIA_POLICY.html','NASA media guidelines')]
def get(job):
 sid,url,name,rights=job;p=ROOT/'sources'/name
 try:
  if not p.exists():
   r=requests.get(url,timeout=(20,90));r.raise_for_status();p.write_bytes(r.content)
  content=p.read_bytes()
  result={'source_id':sid,'url':url,'path':str(p),'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'rights_note':rights,'status':'DOWNLOADED'}
  if name.endswith('.pdf'):
   doc=pymupdf.open(p);result['pages']=len(doc)
   (ROOT/'sources'/(sid+'_TEXT.txt')).write_text('\n'.join(f'\n=== PDF_PAGE_{i+1} ===\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf-8')
  print(sid,result['status'],len(content),flush=True);return result
 except Exception as e:return {'source_id':sid,'url':url,'status':'SOURCE_HOLD','error':str(e),'rights_note':rights}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out=list(pool.map(get,jobs))
extra=[]
for sid in ['SCI24','GAO24']:
 page=(ROOT/'sources'/(sid+'_PAGE.html'))
 if page.exists():
  urls=re.findall(r'(?:href|src)=["\']([^"\']+)["\']',page.read_text(encoding='utf-8'))
  candidates=[urljoin(next(j[1] for j in jobs if j[0]==sid+'_PAGE'),u) for u in urls if '.pdf' in u.lower()]
  target=next((u for u in candidates if ('tc-18-4029-2024.pdf' in u if sid=='SCI24' else 'gao-24-104082.pdf' in u.lower())),None)
  if target:extra.append((sid,target,sid+'.pdf','CC BY4 with per-figure credits' if sid=='SCI24' else 'US GAO federal report; selected Greenland section only'))
nasa=(ROOT/'sources/NASA24_PAGE.html').read_text(encoding='utf-8')
for sid,stem in [('NASA_RADAR','campcentury_aerial_radar_lrg.jpg'),('NASA_1966','campcentury_pho_1966_lrg.jpg')]:
 urls=re.findall(r'https?[^"\'<>\s]+',nasa)
 target=next((u.split('?')[0].replace('&amp;','&') for u in urls if stem in u),None)
 if target:extra.append((sid,target,sid+'.jpg','NASA credited radar composite' if sid=='NASA_RADAR' else 'Historical NARA photo404791598 courtesy National Archives; actual1966 Camp Century, not modern radar'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:out+=list(pool.map(get,extra))
(ROOT/'qc/SOURCE_DOWNLOAD_MANIFEST.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('REFERENCE_SOURCES',len(out),'HOLDS',sum(r['status']!='DOWNLOADED' for r in out),flush=True)
