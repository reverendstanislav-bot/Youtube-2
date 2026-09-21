#!/usr/bin/env python3
import argparse,csv,json
from collections import Counter
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("--fact-map",required=True)
ap.add_argument("--license-manifest",required=True)
ap.add_argument("--music-downloads",required=True)
ap.add_argument("--sfx-downloads",required=True)
ap.add_argument("--music-attribution",required=True)
ap.add_argument("--out-json",required=True)
ap.add_argument("--out-md",required=True)
a=ap.parse_args()

def rows(path):
    with open(path,encoding="utf-8-sig",errors="replace",newline="") as f:
        return list(csv.DictReader(f,delimiter=";"))

facts=rows(a.fact_map)
lic=rows(a.license_manifest)
music=rows(a.music_downloads)
sfx=rows(a.sfx_downloads)
attr=Path(a.music_attribution).read_text(encoding="utf-8-sig",errors="replace")

fact_headers=list(facts[0].keys()) if facts else []
lic_headers=list(lic[0].keys()) if lic else []

def pick(row,*names):
    lower={k.lower().strip():v for k,v in row.items() if k is not None}
    for n in names:
        if n in lower: return (lower[n] or "").strip()
    return ""

# Generic last-column/status discovery as protection against historical header naming.
status_vals=[]
conf_vals=[]
source_urls=[]
for r in facts:
    st=pick(r,"status","lock","state","fact_status","verification","verified")
    if not st and r:
        vals=[(v or "").strip() for v in r.values()]
        for v in reversed(vals):
            if v.upper() in {"LOCKED","PASS","VERIFIED","APPROVED","OPEN","REVIEW"}:
                st=v; break
    status_vals.append(st)
    cf=pick(r,"confidence","quality","strength")
    if not cf:
        for v in r.values():
            if (v or "").strip().lower() in {"high","medium","low"}:
                cf=(v or "").strip(); break
    conf_vals.append(cf)
    url=pick(r,"url","source_url","source_page","link")
    if not url:
        for v in r.values():
            if isinstance(v,str) and v.startswith(("http://","https://")):
                url=v; break
    source_urls.append(url)

license_risk=[]
license_values=[]
missing_license=[]
for i,r in enumerate(lic):
    risk=pick(r,"risk")
    if risk: license_risk.append(risk)
    lv=pick(r,"license")
    if lv: license_values.append(lv)
    else: missing_license.append(i+1)

def url_count(rs):
    n=0
    for r in rs:
        if any(isinstance(v,str) and v.startswith(("http://","https://")) for v in r.values()):
            n+=1
    return n

data={
  "fact_map":{
    "headers":fact_headers,"rows":len(facts),
    "status_counts":dict(Counter(status_vals)),
    "confidence_counts":dict(Counter(conf_vals)),
    "rows_with_source_url":sum(bool(x) for x in source_urls),
    "rows_without_source_url":[i+1 for i,x in enumerate(source_urls) if not x],
  },
  "license_manifest":{
    "headers":lic_headers,"rows":len(lic),
    "risk_counts":dict(Counter(license_risk)),
    "missing_license_rows":missing_license,
    "unique_license_count":len(set(license_values)),
    "rows_with_url":url_count(lic),
  },
  "music":{
    "rows":len(music),"rows_with_url":url_count(music),
    "attribution_text_present":bool(attr.strip()),
    "attribution_chars":len(attr.strip())
  },
  "sfx":{"rows":len(sfx),"rows_with_url":url_count(sfx)}
}
Path(a.out_json).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")

lines=["# Chicago — fact / licensing / music / SFX pack audit","",
       "## Fact map",
       f"- Rows: **{len(facts)}**",
       f"- Headers: {fact_headers}",
       f"- Status counts: **{dict(Counter(status_vals))}**",
       f"- Confidence counts: **{dict(Counter(conf_vals))}**",
       f"- Rows with source URL: **{sum(bool(x) for x in source_urls)}/{len(facts)}**",
       f"- Rows without source URL: **{[i+1 for i,x in enumerate(source_urls) if not x]}**","",
       "## License manifest",
       f"- Rows: **{len(lic)}**",
       f"- Risk counts: **{dict(Counter(license_risk))}**",
       f"- Missing license rows: **{missing_license}**",
       f"- Rows with source/download URL: **{url_count(lic)}/{len(lic)}**","",
       "## Music",
       f"- Download rows: **{len(music)}**",
       f"- Rows with URL: **{url_count(music)}/{len(music)}**",
       f"- Attribution file present: **{bool(attr.strip())}** ({len(attr.strip())} chars)","",
       "## SFX",
       f"- Download rows: **{len(sfx)}**",
       f"- Rows with URL: **{url_count(sfx)}/{len(sfx)}**"]
Path(a.out_md).write_text("\n".join(lines)+"\n",encoding="utf-8")
