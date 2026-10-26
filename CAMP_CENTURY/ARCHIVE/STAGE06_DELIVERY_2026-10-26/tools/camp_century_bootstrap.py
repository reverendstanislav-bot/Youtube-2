from pathlib import Path
import zipfile,hashlib,subprocess,json,csv,io,urllib.request,re,concurrent.futures

REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
TOOLKIT=REPO/'CAMP_CENTURY/ARCHIVE/STAGE06_R5_TOOLKIT'
for p in [ROOT,ROOT/'masters',ROOT/'reports',ROOT/'rights_receipts',ROOT/'clips',ROOT/'records']:p.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(r'C:\Users\KK\Downloads\HIA_CAMP_CENTURY_STAGE06_CODEX_HANDOFF_R5.zip') as z:
    for entry in z.infolist():
        parts=Path(entry.filename).parts[1:]
        if not parts or entry.is_dir() or '__pycache__' in parts:continue
        target=TOOLKIT.joinpath(*parts)
        assert target.resolve().is_relative_to(TOOLKIT.resolve())
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():target.write_bytes(z.read(entry))
expected={'STAGE04_CAMP_CENTURY_FULL_NARRATION_V4_EN.md':'0006d5345bae22b77f3556dcb8090ce167f34292','STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt':'46fafe9914c1a061e9f219c344698f9857019973','STAGE04_CAMP_CENTURY_BEATS_V4.csv':'aea8122f66765b049effd61d6bc0eb4780250407'}
lock=[]
for name,want in expected.items():
    rel='CAMP_CENTURY/SCRIPT/'+name
    raw=subprocess.check_output(['git','-C',str(REPO),'show','HEAD:'+rel])
    got=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert got==want,(name,want,got)
    lock.append({'path':rel,'git_blob_sha':got,'sha256':hashlib.sha256(raw).hexdigest(),'status':'MATCH_LOCKED_V4'})
    if name.endswith('.csv'):beats=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if name.endswith('.txt'):wordcount=len(raw.decode('utf-8-sig').split())
assert len(beats)==32 and len({r['chapter'] for r in beats})==8 and wordcount==2931
(ROOT/'reports/SCRIPT_V4_IDENTITY.json').write_text(json.dumps({'files':lock,'words':wordcount,'beats':len(beats),'chapters':8},indent=2),encoding='utf-8')
print('SCRIPT LOCK MATCH: 2931 words / 32 beats / 8 chapters',flush=True)
targets={
 'F01_USACE_API':'https://usace.contentdm.oclc.org/digital/api/singleitem/collection/p16021coll1/id/34',
 'F01B_IA_METADATA':'https://archive.org/metadata/gov.dod.dimoc.26064',
 'F02_IA_METADATA':'https://archive.org/metadata/gov.archives.arc.2569752',
 'F03_DVIDS_ITEM':'https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv',
 'F03_DVIDS_POPUP':'https://www.dvidshub.net/download/popup/556111',
 'F03_DVIDS_PLAYER':'https://www.dvidshub.net/video/embed/556111',
 'F03_DVIDS_RIGHTS':'https://www.dvidshub.net/about/copyright',
}
def fetch(pair):
    name,url=pair;out=ROOT/'records'/(name+'.txt')
    try:
        rq=urllib.request.Request(url,headers={'User-Agent':'CampCenturyHistoricalSourceQC/1.0'})
        with urllib.request.urlopen(rq,timeout=45) as r:
            data=r.read();status=r.status;final=r.url
        out.write_bytes(data)
        record={'name':name,'url':url,'final_url':final,'status':status,'bytes':len(data),'saved':str(out)}
        text=data.decode('utf-8','replace')
        if name.endswith('METADATA'):
            m=json.loads(text);record['videos']=[{k:f.get(k) for k in ['name','size','source','format','md5','sha1']} for f in m.get('files',[]) if re.search(r'\.(mp4|mpeg|mov|mpg)$',f.get('name',''),re.I)]
        elif 'USACE' in name:record['metadata']=text[:14000]
        elif 'PLAYER' in name or 'POPUP' in name or 'ITEM' in name:record['media_lines']=[line.strip()[:2000] for line in text.splitlines() if re.search(r'\.mp4|m3u8|videofile|source src|sources:|jwplayer',line,re.I)][:15]
    except Exception as e:record={'name':name,'url':url,'error':repr(e)}
    print(json.dumps(record,ensure_ascii=True),flush=True)
    return record
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,targets.items()))
(ROOT/'reports/LIVE_SOURCE_ENDPOINT_PROBE.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
