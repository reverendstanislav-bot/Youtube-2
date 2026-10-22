#!/usr/bin/env python3
"""Find independently hosted original AEC/NARA motion picture files.
Rights/source confirmation always required. Do not claim a local film without download.
"""
import requests,csv,json,pathlib,time,re,unicodedata
from urllib.parse import quote
root=pathlib.Path("aec_film_discovery");root.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/AEC_OFFICIAL_FILM_SOURCE_PRIORITY.csv",encoding="utf-8",newline="")))
sess=requests.Session();sess.headers["User-Agent"]="HIA-ProjectPluto-HistoricalFilms/1.0 documentary original source research"
def norm(s):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",str(s).lower())).strip()
def get(url,**kw):
 for retry in range(2):
  try:
   resp=sess.get(url,timeout=(12,38),**kw);resp.raise_for_status();return resp.json()
  except Exception:
   if retry:raise
   time.sleep(2)
results=[]
for film in rows:
 item={**film,"state":"CATALOG_LEAD_ONLY","matches":[],"rights":"UNCLEARED"}
 if film["id"]=="LASVN1":
  results.append(item);continue
 try:
  data=get("https://archive.org/advancedsearch.php",params={"q":'title:("'+film["title"]+'") AND mediatype:(movies)',"fl[]":["identifier","title","creator","mediatype","licenseurl"],"rows":8,"output":"json"})
  for hit in data.get("response",{}).get("docs",[]):
   if norm(hit.get("title",""))!=norm(film["title"]):continue
   ident=hit.get("identifier","")
   entry={"identifier":ident,"title":hit.get("title"),"creator":hit.get("creator"),"archive_page":"https://archive.org/details/"+ident}
   try:
    met=get("https://archive.org/metadata/"+quote(ident)).get("metadata",{})
    full=get("https://archive.org/metadata/"+quote(ident))
    mov=[x for x in full.get("files",[]) if str(x.get("name","")).lower().endswith((".mp4",".mpeg",".mpg",".mov")) and x.get("source")=="original" and 1000000<int(x.get("size",0))<700000000]
    entry["producer"]=met.get("creator");entry["rights_text"]=str(met.get("licenseurl",""));entry["candidate_files"]=[{"filename":x["name"],"size":int(x["size"]),"url":"https://archive.org/download/"+ident+"/"+quote(x["name"])} for x in mov[:3]]
   except Exception as e:entry["metadata_error"]=str(e)
   item["matches"].append(entry)
  item["state"]="DISCOVERY_COMPLETE_RIGHTS_UNVERIFIED"
 except Exception as e:item["state"]="DISCOVERY_FAILED";item["error"]=str(e)
 results.append(item)
 print(film["id"],item["state"],len(item["matches"]),flush=True)
(root/"SOURCE_DISCOVERY.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
