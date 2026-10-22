#!/usr/bin/env python3
import csv,pathlib,requests,time,json,hashlib,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/PRIMARY_DOCS_CATALOG.csv",encoding="utf8",newline="")))
out=pathlib.Path("project_pluto_primary_documents");out.mkdir(exist_ok=True)
session=requests.Session()
session.headers.update({"User-Agent":"HIA-ProjectPluto-HistoricalSourceArchive/1.0 (documentary source verification)","Accept":"application/pdf,*/*"})
def sha256(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1048576),b""):h.update(c)
 return h.hexdigest()
records=[]
for r in rows:
 p=out/(r["id"]+".pdf")
 entry=dict(r)
 try:
  for attempt in range(2):
   try:
    with session.get(r["url"],stream=True,timeout=(25,120)) as resp:
     resp.raise_for_status()
     with p.open("wb") as f:
      for ch in resp.iter_content(1048576):
       if ch:f.write(ch)
    break
   except Exception:
    if attempt==1:raise
    time.sleep(3)
  with p.open("rb") as f:
   if f.read(5)!=b"%PDF-":raise RuntimeError("Not PDF source magic")
  info=subprocess.run(["pdfinfo",str(p)],capture_output=True,text=True,check=True).stdout
  pages=next((line.split(":")[1].strip() for line in info.splitlines() if line.startswith("Pages:")),"UNKNOWN")
  entry.update({"status":"ACQUIRED_PDF_BINARY","bytes":p.stat().st_size,"sha256":sha256(p),"pages":pages})
  print("OK",entry["id"],entry["pages"],entry["bytes"],flush=True)
 except Exception as exc:
  p.unlink(missing_ok=True)
  entry.update({"status":"UNAVAILABLE","reason":str(exc)})
  print("FAIL",entry["id"],str(exc)[:220],flush=True)
 records.append(entry)
(out/"DOCUMENT_MANIFEST.json").write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n")
if not any(r["status"]=="ACQUIRED_PDF_BINARY" for r in records):raise RuntimeError("No primary docs physically acquired")
