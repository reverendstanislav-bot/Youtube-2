from pathlib import Path
import urllib.request,urllib.parse,json,re,hashlib,concurrent.futures,time,importlib.util,sys
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
TOOL=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007\CAMP_CENTURY\ARCHIVE\STAGE06_R5_TOOLKIT\tools\download_ia_originals.py')
spec=importlib.util.spec_from_file_location('provided_ia_downloader',TOOL);provided=importlib.util.module_from_spec(spec);spec.loader.exec_module(provided)
UA={'User-Agent':'CampCenturyHistoricalSourceQC/1.0'}
def request(url,headers=None):return urllib.request.urlopen(urllib.request.Request(url,headers=UA|dict(headers or {})),timeout=45)
def hashfile(path,method='sha256'):
    h=hashlib.new(method)
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(8<<20),b''):h.update(chunk)
    return h.hexdigest()
jobs=[]
for sid,item in provided.SOURCES.items():
    meta=json.loads((R/'records'/(sid+'_IA_METADATA.txt')).read_text());name,size=provided.choose(item,meta)
    selected=next(f for f in meta['files'] if f['name']==name)
    jobs.append({'source_id':sid,'url':'https://archive.org/download/'+item+'/'+urllib.parse.quote(name),'size':size,'md5':selected['md5'],'ext':Path(name).suffix,'origin_kind':'IA_METADATA_ORIGINAL','source_page':'https://archive.org/details/'+item})
official=json.loads((R/'records/F01_USACE_API.txt').read_text())
jobs.append({'source_id':'F01','url':official['streamUri'],'size':439061611,'ext':'.mp4','origin_kind':'OFFICIAL_USACE_STREAM_FROM_ITEM_API','source_page':'https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34'})

events=[]
try:
    with request('https://www.dvidshub.net/download/videofile/4604847') as response:
        events.append({'source':'F03','requested_maximum_download':'https://www.dvidshub.net/download/videofile/4604847','status':response.status,'final_url':response.url,'content_type':response.headers.get('Content-Type')})
except Exception as e:events.append({'source':'F03','requested_maximum_download':'https://www.dvidshub.net/download/videofile/4604847','error':repr(e),'quality_status':'ORIGINAL_DOWNLOAD_AUTH_REQUIRED_NOT_BYPASSED'})
item=(R/'records/F03_DVIDS_ITEM.txt').read_text()
player=re.findall(r'<source\s+src="([^"]+\.mp4)"',item)[0]
with request(player,{'Range':'bytes=0-0'}) as response:
    total=int(response.headers.get('Content-Range','').split('/')[-1] or response.headers.get('Content-Length'))
jobs.insert(0,{'source_id':'F03','url':player,'size':total,'ext':'.mp4','origin_kind':'EXPLICIT_PUBLIC_PLAYER_RENDITION','source_page':'https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv','quality_hold':'720x480 original requires login; advertised anonymous 640x480 playback rendition acquired instead'})
(R/'reports/OFFICIAL_DOWNLOAD_LIMITS.json').write_text(json.dumps(events,indent=2))

def acquire(job):
    sid=job['source_id'];target=R/'masters'/(sid+job['ext']);rec=R/'reports'/(sid+'_DOWNLOAD_RECEIPT.json')
    if target.is_file() and target.stat().st_size==job['size']:
        h=hashfile(target)
        if rec.exists() and json.loads(rec.read_text()).get('sha256')==h:
            print('REUSE_VERIFIED',sid,target.stat().st_size,h,flush=True);return
    segments=R/'records'/('download_segments_'+sid);segments.mkdir(exist_ok=True)
    chunk=8*1024*1024;ranges=[(i,start,min(start+chunk,job['size'])-1) for i,start in enumerate(range(0,job['size'],chunk))]
    finished=0
    def part(row):
        i,start,end=row;out=segments/f'{i:05}.bin';want=end-start+1
        if out.exists() and out.stat().st_size==want:return out
        error=None
        for attempt in range(3):
            try:
                with request(job['url'],{'Range':f'bytes={start}-{end}'}) as res:
                    if res.status!=206:raise ValueError('Range unsupported: '+str(res.status))
                    cr=res.headers.get('Content-Range','')
                    if not cr.startswith(f'bytes {start}-{end}/'):raise ValueError('Unexpected Content-Range '+cr)
                    tmp=out.with_suffix('.part')
                    with tmp.open('wb') as w:
                        count=0
                        while count<want:
                            data=res.read(min(512*1024,want-count))
                            if not data:break
                            w.write(data);count+=len(data)
                    if count!=want:raise ValueError(f'Incomplete range {count}/{want}')
                tmp.replace(out);return out
            except Exception as e:error=e;time.sleep(min(5,attempt+1))
        raise RuntimeError(f'{sid} range {start}-{end}: {error}')
    print('START_RANGE_DOWNLOAD',sid,job['size'],len(ranges),'segments',flush=True)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4 if sid.startswith('F0') else 2) as pool:
            for future in concurrent.futures.as_completed([pool.submit(part,row) for row in ranges]):
                future.result();finished+=1
                if finished%8==0 or finished==len(ranges):print('PROGRESS',sid,finished,'/',len(ranges),flush=True)
        temp=target.with_suffix(target.suffix+'.verified_tmp')
        with temp.open('wb') as out:
            for i,_,_ in ranges:
                with (segments/f'{i:05}.bin').open('rb') as source:
                    while data:=source.read(4*1024*1024):out.write(data)
        assert temp.stat().st_size==job['size']
        if job.get('md5'):assert hashfile(temp,'md5')==job['md5'],'IA original MD5 mismatch'
        result=job|{'path':str(target),'sha256':hashfile(temp),'status':'ACQUIRED_HASH_VERIFIED_PENDING_FULL_DECODE'}
        temp.replace(target);rec.write_text(json.dumps(result,indent=2))
        print('ACQUIRED',sid,job['size'],result['sha256'],flush=True)
    except Exception as e:
        rec.write_text(json.dumps(job|{'status':'DOWNLOAD_HOLD','error':repr(e),'complete_segments':finished},indent=2))
        print('DOWNLOAD_HOLD',sid,repr(e),flush=True)

if len(sys.argv)>1:jobs=json.loads(Path(sys.argv[1]).read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(acquire,jobs))
