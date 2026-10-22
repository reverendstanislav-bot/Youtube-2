#!/usr/bin/env python3
import argparse,pathlib,requests,time,json,hashlib
arg=argparse.ArgumentParser();arg.add_argument("--shard",type=int,required=True);a=arg.parse_args()
base=pathlib.Path("pluto_haer")/("batch_%02d"%a.shard);base.mkdir(parents=True,exist_ok=True)
photos=[("HAER-4A-%02d"%i,"HAER NEV,12-MERC.V,4A-"+str(i)+".tif","NV-32-A") for i in range(1,41)]
photos +=[("HAER-4-%02d"%i,"HAER NEV,12-MERC.V,4-"+str(i)+".tif","NV-32") for i in range(1,5)]
photos +=[("HAER-"+c+"-01","HAER NEV,12-MERC.V,"+c+"-1.tif","NV-32-"+c) for c in ("4B","4C","4D","4E")]
s=requests.Session();s.headers["User-Agent"]="HIA-ProjectPluto-Archive/1.0 source quality verification"
listing=s.get("https://commons.wikimedia.org/w/api.php",params={
 "action":"query","format":"json","list":"categorymembers",
 "cmtitle":"Category:Nevada Test Site Pluto Facility","cmlimit":"max","cmtype":"file"},timeout=50)
listing.raise_for_status()
members=[x["title"] for x in listing.json()["query"]["categorymembers"]]
print("REAL CATEGORY FILES",len(members),flush=True)
records=[]
for id,title,source in [v for i,v in enumerate(photos) if i%12==a.shard]:
 item={"id":id,"title":title,"source":source,"photo_date":"after 1968","source_class":"REAL_PLUTO_SITE_NOT_1964_TEST"}
 target=base/(id+".tif")
 try:
  matches=[name for name in members if name.endswith(title)]
  if len(matches)!=1:raise RuntimeError("No unique match for "+title+" "+str(matches))
  real_title=matches[0]
  r=s.get("https://commons.wikimedia.org/w/api.php",params={"action":"query","format":"json","prop":"imageinfo","iiprop":"url|size|mime|sha1","titles":real_title},timeout=50)
  r.raise_for_status()
  info=next(iter(r.json()["query"]["pages"].values()))["imageinfo"][0]
  if "tiff" not in info["mime"]:raise RuntimeError("Not original TIFF")
  with s.get(info["url"],stream=True,timeout=(40,150)) as resp:
   resp.raise_for_status()
   with target.open("wb") as f:
    for chunk in resp.iter_content(1024*1024):
     if chunk:f.write(chunk)
  if target.stat().st_size!=int(info["size"]):raise RuntimeError("Size mismatch")
  with target.open("rb") as f:
   if f.read(4) not in (bytes([73,73,42,0]),bytes([77,77,0,42])):raise RuntimeError("Not TIFF binary")
  h=hashlib.sha256()
  with target.open("rb") as f:
   for part in iter(lambda:f.read(1048576),b""):h.update(part)
  item.update({"actual_commons_title":real_title,"status":"DOWNLOADED_VERIFIED","bytes":target.stat().st_size,"sha256":h.hexdigest(),
    "url":info.get("url"),"width":info.get("width"),"height":info.get("height")})
  print("OK",id,flush=True)
 except Exception as exc:
  target.unlink(missing_ok=True)
  item.update({"status":"FAILED","error":str(exc)})
  print("FAIL",id,str(exc)[:130],flush=True)
 records.append(item)
 time.sleep(2)
(base/"SOURCE_MANIFEST.json").write_text(json.dumps(records,indent=2)+"\n")
print("VERIFIED",sum(x["status"]=="DOWNLOADED_VERIFIED" for x in records),"of",len(records))
