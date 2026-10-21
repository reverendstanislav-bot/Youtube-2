#!/usr/bin/env python3
"""Download first-pass HIA Pluto Commons shortlist with Commons file metadata.

Install: pip install requests
Run from repo root:
 python PROJECT_PLUTO/ARCHIVE/fetch_public_domain_assets.py --out ./project_pluto_assets
Do not treat script output as clearance: individual rights and provenance still require human QC.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import re
import time
from urllib.parse import quote

import requests

API = "https://commons.wikimedia.org/w/api.php"
CATEGORY = "Category:Nevada Test Site Pluto Facility"
UA = "HIA-ProjectPluto-ArchiveResearch/1.0 (original archival source acquisition)"
BASE = pathlib.Path(__file__).resolve().parent

def api(sess, params):
    for attempt in range(4):
        try:
            r=sess.get(API, params={**params,"format":"json"},timeout=45)
            r.raise_for_status()
            obj=r.json()
            if "error" in obj:
                raise RuntimeError(str(obj["error"]))
            return obj
        except (requests.RequestException, ValueError) as e:
            if attempt == 3: raise
            time.sleep(2 ** attempt)
    raise RuntimeError("API unavailable")

def list_category(sess):
    out=[]
    cursor={}
    while True:
        v=api(sess, {"action":"query","list":"categorymembers",
                "cmtitle":CATEGORY,"cmlimit":"max","cmtype":"file",**cursor})
        out.extend(item["title"] for item in v["query"]["categorymembers"])
        if "continue" not in v: break
        cursor=v["continue"]
    return out

def fileinfo(sess,title):
    data=api(sess,{"action":"query","titles":title,"prop":"imageinfo",
       "iiprop":"url|size|mime|sha1|extmetadata"})
    p=next(iter(data["query"]["pages"].values()))
    if "imageinfo" not in p: raise ValueError(f"No media metadata: {title}")
    return p["imageinfo"][0]

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for ch in iter(lambda:f.read(1024*1024),b""): h.update(ch)
    return h.hexdigest()

def find_title(members, marker):
    if marker.startswith("HAER NEV,"):
        matches=[x for x in members if x.endswith(marker)]
    else:
        matches=[x for x in members if x=="File:"+marker]
    if len(matches)!=1: raise ValueError(f"Expected 1 match, got {len(matches)}: {marker}")
    return matches[0]

def download(sess,url,path):
    tmp=path.with_suffix(path.suffix+".part")
    with sess.get(url,stream=True,timeout=(20,120)) as r:
        r.raise_for_status()
        ctype=r.headers.get("Content-Type","").lower()
        if "text/html" in ctype or "application/json" in ctype:
            raise RuntimeError(f"unexpected download content-type {ctype}: {url}")
        with open(tmp,"wb") as f:
            for block in r.iter_content(chunk_size=1024*1024):
                if block: f.write(block)
    tmp.replace(path)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="project_pluto_assets")
    p.add_argument("--download-context-video",action="store_true")
    args=p.parse_args()
    dest=pathlib.Path(args.out); dest.mkdir(parents=True,exist_ok=True)
    sess=requests.Session()
    sess.headers.update({"User-Agent":UA})
    members=list_category(sess)
    selected=list(csv.DictReader(open(BASE/"PHOTO_SHORTLIST_V1.csv",encoding="utf-8",newline="")))
    video=list(csv.DictReader(open(BASE/"FILM_LEDGER_V1.csv",encoding="utf-8",newline="")))
    results=[]
    for item in selected:
        if item["priority"] in ("HOLD","REJECT"): continue
        marker=item["commons_file_or_haer_suffix"]
        try:
            # also query file outside the category (cross-section or reactor photos)
            if marker.startswith("HAER NEV,"):
                title=find_title(members,marker)
            else:
                title="File:"+marker
            info=fileinfo(sess,title)
            url=info["url"]; ext=pathlib.Path(marker).suffix.lower()
            if ext not in (".tif",".tiff",".jpg",".jpeg",".png"):
                raise ValueError(f"Unexpected extension: {ext}")
            target=dest/(item["asset_id"]+ext)
            if not target.exists():
                download(sess,url,target)
            results.append({**item,"title":title,"source_url":info.get("descriptionurl"),
                "original_url":url,"mime":info.get("mime"),"width":info.get("width"),
                "height":info.get("height"),"bytes":target.stat().st_size,
                "commons_sha1":info.get("sha1"),"sha256":sha256(target),"download":"OK",
                "rights_final_clearance":"MANUAL_QC_REQUIRED"})
            print(item["asset_id"], "OK", target, flush=True)
        except Exception as e:
            results.append({**item,"download":"ERROR","error":str(e)})
            print(item["asset_id"],"ERROR",e,flush=True)
    if args.download_context_video:
        for item in video:
            if item["status"]!="DOWNLOAD_CANDIDATE": continue
            name=item["source_page"].split("/wiki/File:")[-1]
            title="File:"+__import__("urllib.parse",fromlist=["unquote"]).unquote(name).replace("_"," ")
            try:
                info=fileinfo(sess,title)
                target=dest/(item["film_id"]+".webm")
                if not target.exists(): download(sess,info["url"],target)
                results.append({**item,"title":title,"original_url":info["url"],
                    "mime":info.get("mime"),"bytes":target.stat().st_size,
                    "sha256":sha256(target),"download":"OK","rights_final_clearance":"MANUAL_QC_REQUIRED"})
                print(item["film_id"],"OK",target,flush=True)
            except Exception as e:
                results.append({**item,"download":"ERROR","error":str(e)})
                print(item["film_id"],"ERROR",e,flush=True)
    (dest/"ACQUIRED_MANIFEST.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
    print("Done:",sum(x["download"]=="OK" for x in results),"of",len(results),"objects")
if __name__=="__main__": main()
