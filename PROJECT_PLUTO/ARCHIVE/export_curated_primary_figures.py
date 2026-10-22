#!/usr/bin/env python3
"""Export only 26 visually inspected, real Project Pluto engineering figures/pages.
Each source is an original official scan. No generative visuals or added invented labels.
"""
import pathlib,csv,hashlib,json,zipfile
import fitz
rows=list(csv.DictReader(open("PROJECT_PLUTO/ARCHIVE/TORY_CURATED_PRIMARY_FIGURES.csv",encoding="utf8",newline="")))
folder=pathlib.Path("PROJECT_PLUTO_DIRECT_REPORT_VISUALS")
folder.mkdir(exist_ok=True)
pages_dir=folder/"01_ORIGINAL_REPORT_PAGES";pages_dir.mkdir(exist_ok=True)
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for piece in iter(lambda:f.read(1048576),b""):h.update(piece)
 return h.hexdigest()
cached={};results=[]
for row in rows:
 did=row["id"]
 pdf=pathlib.Path("pluto_primary_reports")/(did+".pdf")
 if did not in cached: cached[did]=fitz.open(pdf)
 doc=cached[did]; page_num=int(row["pdf_page_1_based"])
 if not 1<=page_num<=len(doc):raise RuntimeError("Invalid page")
 page=doc.load_page(page_num-1)
 pix=page.get_pixmap(matrix=fitz.Matrix(2.6,2.6),alpha=False,colorspace=fitz.csRGB)
 out=pages_dir/(did+"__P"+f"{page_num:03}"+"__"+row["export_name"]+".png")
 pix.save(out)
 if pix.width<1250:raise RuntimeError("Too low pixels for "+str(out))
 results.append({**row,"export_file":str(out.relative_to(folder)), "width":pix.width,
 "height":pix.height,"file_bytes":out.stat().st_size,"sha256":sha(out),
 "source_report":"Project Pluto original government historic engineering report",
 "rights":"Original US government funded report; individual figures third-party reuse QC open",
 "page_verified":True})
 print("VERIFIED REPORT PAGE",did,page_num,row["export_name"],pix.width,pix.height,flush=True)
(folder/"FIGURES_SOURCE_MANIFEST.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
(folder/"FIGURES_SOURCE_MANIFEST.csv").write_text(open("PROJECT_PLUTO/ARCHIVE/TORY_CURATED_PRIMARY_FIGURES.csv",encoding="utf8").read())
(folder/"README.txt").write_text("Authentic primary-scanned Project Pluto/Tory reactor documents only; 26 visually selected official report pages at 2.6x output (~187 dpi). No AI images, no fake names, source PDF page as 1-based index. These are original DOC scans and technical diagrams, not 26 pieces of cinema. Exact editorial duration must follow script/VO timing.\\n".replace("\\n","\n"))
p=pathlib.Path("HIA_VIDEO006_26_GENUINE_TORY_ENGINEERING_FIGURES.zip")
with zipfile.ZipFile(p,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
 for file in sorted(folder.rglob("*")):
  if file.is_file():z.write(file,str(file))
print("DONE",len(results),"actual pages",p.stat().st_size,"bytes",flush=True)
