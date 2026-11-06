from pathlib import Path
import urllib.request,urllib.parse,json,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]
url='https://www.youtube.com/oembed?'+urllib.parse.urlencode({'url':'https://www.youtube.com/watch?v=sP67aPtpwKg','format':'json'})
row={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'video_id':'sP67aPtpwKg','source_url':url,'catalog_evidence':'CHANNEL/RESEARCH/2026-11-02/VIDEO_METRICS.csv: published 2026-10-28','public_listing_currently_verified':False}
try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HIA-Documentary-Research/1.0'}),timeout=20) as response:
        row['http_status']=response.status;row['oembed']=json.loads(response.read())
    row['embed_available_now']=True
except Exception as exc:row['error']=str(exc);row['embed_available_now']=False
(root/'EVIDENCE/ENDSCREEN_TARGET_READBACK.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(row,ensure_ascii=False,indent=2))
