#!/usr/bin/env python3
"""Recover existing Satsop picture sources from exact historical provenance.
This never creates/changes/generates images or voice. URLs are unverified
until bytes have been downloaded, decoded, and checked.
Use in network-enabled GitHub Actions runner.
"""
import hashlib
import json
import os
import pathlib
import time
import urllib.request
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[2]
SAT=ROOT/"SATSOP"
OUT=pathlib.Path(os.environ.get("SATSOP_RECOVER_OUT","/tmp/satsop-asset-recovery"))
ASSETS=OUT/"public"/"assets"
HEADERS={"User-Agent":"SatsopSourceRestore/1.0 (documentary provenance validation)"}

def load(p):
    return json.loads((SAT/p).read_text(encoding="utf-8-sig"))

TIMELINE=load("REMOTION_V1/public/timeline.json")["beats"]
REPL=load("STAGE_8_GENERATED_REPLACEMENTS/SATSOP_35_GENERATED_REPLACEMENTS.json")["items"]
REPL_JOBS=load("STAGE_8_GENERATED_REPLACEMENTS/HIGGSFIELD_RESULTS.json")
SOURCE=load("STAGE_7/SOURCES/STAGE7_SOURCE_MANIFEST.json")["commons"]
STAGES=[
 ("STAGE_6/FIX9_V6/FIX9_V6_HIGGSFIELD_SUBMISSIONS.json","fix9"),
 ("STAGE_6/FINAL28_V5/SATSOP_FINAL28_V5_JOBS.json","final28"),
 ("STAGE_6/REMAINING_V4/SATSOP_REMAINING_V4_JOBS.json","remainingV4"),
 ("STAGE_6/TEST20_V3/TEST20_V3_JOBS.json","testV3"),
 ("STAGE_6/TEST20_V2/TEST20_V2_JOBS.json","testV2"),
 ("STAGE_6/TEST20/TEST20_JOBS.json","testV1"),
]
by_repl={a["beat_id"]:REPL_JOBS[i] for i,a in enumerate(REPL)}
by_commons={c["source_title"]:c for c in SOURCE}
by_prompt={}
for f,stage in STAGES:
    d=load(f)
    for j in (d if isinstance(d,list) else d.get("jobs",[])):
        k=j.get("prompt_id","").replace("-V6","")
        url=j.get("result_url")
        if k and url:
            by_prompt.setdefault(k,[]).append({
                "url":url,"origin":stage,
                "job_id":j.get("job_id"),"sha256":j.get("sha256")
            })

def candidates(b):
    if b["beat"] in by_repl:
        v=by_repl[b["beat"]]
        return [{"url":v["result_url"],"origin":"stage8-replacement",
                 "job_id":v["job_id"],"sha256":None}]
    if b.get("kind")=="current":
        c=by_commons.get(b.get("sourceTitle"))
        return [] if c is None else [{"url":c["download_url"],"origin":"commons",
                      "license":c["license"],"sha256":c.get("sha256")}]
    return list(by_prompt.get(b.get("promptId"),[]))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def download(url,deadline=50):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=deadline) as r:
        payload=r.read(24000000)
        if len(payload)>23000000:raise ValueError("Suspicious asset size >23MB")
        return payload

def looks_image(payload):
    return payload.startswith(b"\x89PNG\r\n\x1a\n") or payload[:3]==b"\xff\xd8\xff"

def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    ledger=[]
    for n,b in enumerate(TIMELINE,1):
        p=ASSETS/pathlib.Path(b["file"]).name
        cs=candidates(b)
        rec={"beat":b["beat"],"local_path":str(p.relative_to(OUT)),
             "candidates":len(cs),"source":"", "status":"MISSING",
             "sha256":None,"bytes":0,"attempts":[]}
        for c in cs:
            try:
                payload=download(c["url"])
                if not looks_image(payload):
                    raise ValueError("Response is not recognized JPEG/PNG image")
                h=digest(payload)
                if c.get("sha256") and c["sha256"]!=h:
                    raise ValueError("Original file SHA256 mismatch "+h)
                # Binary header validation and size are mandatory before accepting.
                p.write_bytes(payload)
                rec.update({"source":c["origin"],"status":"DOWNLOADED_HEADER_CHECKED",
                            "sha256":h,"bytes":len(payload),"url":c["url"]})
                break
            except Exception as e:
                rec["attempts"].append({"origin":c.get("origin"),"error":str(e)[:240]})
        ledger.append(rec)
        print(f'{n:03d}/109 {b["beat"]}: {rec["status"]} {rec["source"]}',flush=True)
    recovered=sum(r["status"].startswith("DOWNLOADED") for r in ledger)
    report={"status":"CANDIDATE_MEDIA_RECOVERY_ONLY_NOT_FINAL_FILM",
        "recovered":recovered,"total":len(ledger),
        "missing":[r["beat"] for r in ledger if r["status"]=="MISSING"],
        "original_voiceover_available":False,
        "source_priority":"stage8 replacement; exact original stage6 job priority; commons originals",
        "warning":"Successful binary download is NOT proof of image acceptability or selected original version. Human visual QC required. No Arthur WAV.",
        "results":ledger}
    (OUT/"RECOVERY_RESULTS.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    with zipfile.ZipFile(OUT/"SATSOP_SOURCE_RECOVERY_CANDIDATES.zip","w",zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        z.write(OUT/"RECOVERY_RESULTS.json",arcname="RECOVERY_RESULTS.json")
        for r in ledger:
            p=OUT/r["local_path"]
            if p.is_file():z.write(p,arcname=r["local_path"])
    print(json.dumps({"recovered":recovered,"total":len(ledger),"missing":report["missing"],
                      "archive":str(OUT/"SATSOP_SOURCE_RECOVERY_CANDIDATES.zip")}))
    # A partial archive is useful for manual reconstruction. Don't report PASS.
    return 0

if __name__=="__main__":
    raise SystemExit(main())
