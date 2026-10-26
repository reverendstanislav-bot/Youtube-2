from pathlib import Path
import urllib.request,urllib.parse,json,importlib.util
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
spec=importlib.util.spec_from_file_location('provided',r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007\CAMP_CENTURY\ARCHIVE\STAGE06_R5_TOOLKIT\tools\download_ia_originals.py')
provided=importlib.util.module_from_spec(spec);spec.loader.exec_module(provided)
jobs=[]
for sid,item in {'F04':'gov.archives.arc.2569778','F05':'gov.archives.arc.2569758','F06':'gov.dod.dimoc.30259'}.items():
    with urllib.request.urlopen('https://archive.org/metadata/'+item,timeout=30) as r:m=json.load(r)
    (R/'records'/(sid+'_IA_METADATA.txt')).write_text(json.dumps(m,indent=2))
    name,size=provided.choose(item,m);f=next(f for f in m['files'] if f['name']==name)
    jobs.append(dict(source_id=sid,url='https://archive.org/download/'+item+'/'+urllib.parse.quote(name),size=size,md5=f['md5'],ext=Path(name).suffix,origin_kind='IA_METADATA_ORIGINAL',source_page='https://archive.org/details/'+item))
    print(sid,m['metadata'].get('description'),flush=True)
(R/'records/EXTRA_JOBS.json').write_text(json.dumps(jobs,indent=2))
