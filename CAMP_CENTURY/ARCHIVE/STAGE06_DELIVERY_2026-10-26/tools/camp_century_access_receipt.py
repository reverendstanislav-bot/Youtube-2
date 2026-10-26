import json,requests,datetime
from pathlib import Path
p=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\reports\F03_OFFICIAL_ORIGINAL_ACCESS_CHECK.json')
url='https://www.dvidshub.net/download/videofile/4604847'
result={'url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'anonymous GET, stream=True; no login bypass, no credentials, response body not downloaded'}
try:
 with requests.get(url,stream=True,timeout=(15,20)) as r:
  result.update(http_status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),status='AVAILABLE_REQUIRES_REVIEW' if r.status_code==200 else 'OFFICIAL_ORIGINAL_ACCESS_HOLD')
except requests.RequestException as e:result.update(status='NETWORK_ACCESS_HOLD',error_type=type(e).__name__,error=str(e))
p.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
