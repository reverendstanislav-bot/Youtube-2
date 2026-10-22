#!/usr/bin/env python3
"""Scout exact engineering diagrams in 1964 Project Pluto primary reports.
No OCR; uses PDF text, image blocks and real rendered pages. Selection still needs producer eye QC.
"""
import pathlib,fitz,re,math,json,statistics
from PIL import Image,ImageDraw
root=pathlib.Path("pluto_pdf_screening");root.mkdir(exist_ok=True)
DOCS=[("DOC-01","Tory II-C Tests 1964"),("DOC-02","Tory II-C Engineering"),("DOC-03","Tory II-C Engineering Study"),("DOC-04","Pluto Control Systems"),("DOC-05","Pluto Disassembly Site HAER")]
keywords=[("figure",3),("fig.",4),("schematic",8),("cross section",9),("cross-section",9),("reactor",2),("assembly",4),("rail",6),("pluto",2),("ceramic",4),("control",4),("drawing",4),("flow diagram",8),("air system",6),("test facility",6),("sl am",5),("airflow",4),("core",3)]
output=[]
for did,label in DOCS:
 pdf=pathlib.Path("pluto_primary_reports")/(did+".pdf")
 if not pdf.exists():continue
 document=fitz.open(pdf)
 scores=[]
 for i in range(len(document)):
  pg=document.load_page(i);txt=pg.get_text("text").lower()
  score=sum(weight*min(3,txt.count(word)) for word,weight in keywords)
  images=pg.get_images(full=True)
  draw=pg.get_drawings()
  # Favor visually rich schematic pages; scanned reports contain image-only pages.
  score+=5*bool(images) + min(5,len(draw)//20)
  if not txt.strip():score+=2
  if i<4:score-=6
  scores.append((score,i,txt[:120].replace("\n"," "),len(images),len(draw)))
 # diversified pages across document: top per 15-page bins, cap 40/doc
 winners=set()
 for start in range(0,len(document),15):
  group=sorted(scores[start:start+15],reverse=True)[:2]
  for row in group:
   if row[0]>=4:winners.add(row[1])
 top=sorted(scores,reverse=True)[:25]
 winners.update(i for score,i,*_ in top if score>=8)
 winners=sorted(winners)[:60]
 for i in winners:
  pg=document.load_page(i);p=pg.get_pixmap(matrix=fitz.Matrix(0.85,0.85),alpha=False)
  img=Image.frombytes("RGB",[p.width,p.height],p.samples)
  img.thumbnail((240,310))
  output.append({"doc":did,"label":label,"pdf_page_1based":i+1,"score":scores[i][0],"preview":f"{did}_P{i+1:03}.jpg",
                 "page_text_excerpt":scores[i][2][:160]})
  img.save(root/f"{did}_P{i+1:03}.jpg",quality=72)
 print("REPORT",did,"pages",len(document),"candidates",len(winners),flush=True)
# consolidated grouped source contact sheet, 5col x 4 row
for start in range(0,len(output),20):
 chunk=output[start:start+20]
 sheet=Image.new("RGB",(5*263,4*354+36),"#212427")
 draw=ImageDraw.Draw(sheet)
 draw.text((9,8),f"REAL TORY REPORT ORIGINAL PAGES — CONTACT {start//20+1}",fill="white")
 for j,row in enumerate(chunk):
  x=j%5*263+8;y=j//5*354+36
  with Image.open(root/row["preview"]) as src:
   src=src.convert("RGB");sheet.paste(src,(x,y+28))
  draw.text((x,y+5),f"{row['doc']} PDF P{row['pdf_page_1based']} SCORE {row['score']}",fill="white")
 sheet.save(root/f"REPORT_CONTACT_{start//20+1:02}.jpg",quality=79)
(root/"CANDIDATE_INDEX.json").write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n")
print("DONE candidate render",len(output),"contact sheets",math.ceil(len(output)/20),flush=True)
