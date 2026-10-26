#!/usr/bin/env python3
"""Download original large U.S. Army movie files using live Internet Archive item metadata.
No non-IA site auth bypass; fails/holds rather than inventing URLs or claiming a verified clip.
"""
import argparse,csv,hashlib,json,pathlib,sys,urllib.parse,urllib.request,urllib.error,time
SOURCES={"F01B":"gov.dod.dimoc.26064","F02":"gov.archives.arc.2569752"}
HEADERS=["source_id","archive_item","original_item_url","selected_filename","original_download_url","saved_local_path","bytes","sha256","status","error"]

def get_json(item):
    url='https://archive.org/metadata/'+urllib.parse.quote(item)
    request=urllib.request.Request(url,headers={'User-Agent':'CampCenturySourceQC/1.0 (original government archive acquisition)'})
    with urllib.request.urlopen(request,timeout=45) as res:return json.load(res)

def choose(item,metadata):
    choices=[]
    for f in metadata.get('files',[]):
        n=f.get('name','');ext=pathlib.Path(n).suffix.lower();fmt=f.get('format','').lower()
        if ext not in {'.mp4','.mpeg','.mpg','.mov'}:continue
        if any(z in n.lower() for z in ['_512kb','_256kb','_thumb','sample','.ia.mp4']):continue
        size=int(f.get('size') or 0)
        if size<90_000_000:continue
        # Actual IA SOURCE file is ranked above derivative; we also prefer large MPEG2 over a thin web preview.
        score=(f.get('source')=='original',('mpeg2' in fmt or 'mpeg-2' in fmt or ext in {'.mpeg','.mpg'}),size)
        choices.append((score,n,size))
    if not choices:raise ValueError('No verified large video file in metadata; use item download UI')
    choices.sort(reverse=True)
    return choices[0][1],choices[0][2]

def grab(url,out):
    tmp=out.with_suffix(out.suffix+'.part')
    start=tmp.stat().st_size if tmp.exists() else 0
    headers={'User-Agent':'CampCenturySourceQC/1.0'}
    if start:headers['Range']=f'bytes={start}-'
    rq=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(rq,timeout=90) as resp:
        status=resp.status
        mode='ab' if start and status==206 else 'wb'
        with tmp.open(mode) as w:
            while True:
                chunk=resp.read(4*1024*1024)
                if not chunk:break
                w.write(chunk)
    tmp.replace(out)

def sha256(path):
    d=hashlib.sha256()
    with path.open('rb') as f:
        while (part:=f.read(4*1024*1024)):d.update(part)
    return d.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True)
    p.add_argument('--ids',nargs='*',choices=list(SOURCES),default=['F01B','F02'])
    a=p.parse_args()
    root=pathlib.Path(a.root);(root/'masters').mkdir(parents=True,exist_ok=True);(root/'reports').mkdir(parents=True,exist_ok=True)
    logs=[]
    for sid in a.ids:
        item=SOURCES[sid];record=dict.fromkeys(HEADERS,'');record.update(source_id=sid,archive_item=item,original_item_url='https://archive.org/details/'+item,status='DOWNLOAD_HOLD')
        try:
            n,expected=choose(item,get_json(item)); url='https://archive.org/download/'+urllib.parse.quote(item)+'/'+urllib.parse.quote(n,safe='/')
            output=root/'masters'/(sid+pathlib.Path(n).suffix.lower())
            record.update(selected_filename=n,original_download_url=url,saved_local_path=str(output))
            if not output.exists():grab(url,output)
            if output.stat().st_size!=expected:raise ValueError(f'Size mismatch actual={output.stat().st_size}, metadata={expected}')
            record.update(bytes=str(output.stat().st_size),sha256=sha256(output),status='BINARY_ACQUIRED_NOT_YET_DECODED_OR_RIGHTS_CLEARED')
            print('ACQUIRED',sid,output,record['bytes'])
        except Exception as e:
            record['error']=type(e).__name__+': '+str(e)
            print('DOWNLOAD_HOLD',sid,record['error'],file=sys.stderr)
        logs.append(record)
    manifest=root/'reports'/'internet_archive_download_receipts.csv'
    with manifest.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=HEADERS);w.writeheader();w.writerows(logs)
    print('SOURCE_DOWNLOAD_LOG',manifest)
    if any(a['status']=='DOWNLOAD_HOLD' for a in logs):sys.exit(3)
if __name__=='__main__':main()
