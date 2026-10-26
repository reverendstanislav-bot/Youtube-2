import pymupdf,json,re
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\GRAPHICS_PREP_R1')
manifest=[]
jobs={'ARMY65_TR174.pdf':{'printed30':'Wonder Arches being installed','printed31':'5, 700','printed32':'as it was actually constructed','printed33':'Figure 25.','plan26':'KITCHEN','printed37':'Table II.','printed39':'Figure 28.','printed40':'Figure 30.','printed41':'20,000','printed43':'Figure 33','printed44':'150 fee','printed47':'9 July 1963'},'SCI24.pdf':{'fig1':'Figure 1.','fig2':'Figure 2.','fig3':'Figure 3.','fig4':'Figure 4.'}}
for filename,queries in jobs.items():
 path=ROOT/'sources'/filename
 if not path.exists():continue
 doc=pymupdf.open(path)
 if filename.startswith('ARMY'):
  # Printed page numbering appears as a standalone header; record exact PDF index separately.
  chosen=[]
  for i,p in enumerate(doc):
   t=p.get_text()
   if any(q.lower() in t.lower() for q in queries.values()):chosen.append(i)
  # Main Camp Century report printed25 onward; early figures are predecessor sites, not actual Century.
  print('ARMY_PAGE_HEADERS',[(i+1,doc[i].get_text()[:100].replace('\n',' ')) for i in chosen],flush=True)
 else:
  chosen=[i for i,p in enumerate(doc) if any(q in p.get_text() for q in queries.values())]
 for i in chosen:
  p=doc[i];ref=('ARMY65' if filename.startswith('ARMY') else 'SCI24')+f'_PDFPAGE_{i+1:03d}'
  pix=p.get_pixmap(matrix=pymupdf.Matrix(2,2),alpha=False);out=ROOT/'references'/(ref+'.png');pix.save(out)
  manifest.append({'reference_id':ref,'source_pdf':filename,'pdf_page_1based':i+1,'path':str(out),'width':pix.width,'height':pix.height,'text_excerpt':p.get_text()[:160].replace('\n',' '),'visual_review':'PENDING'})
for name in ['NASA_RADAR.jpg','NASA_1966.jpg']:
 p=ROOT/'sources'/name
 if p.exists():
  im=Image.open(p);print(name,im.size,im.format,flush=True)
  manifest.append({'reference_id':p.stem,'path':str(p),'width':im.width,'height':im.height,'visual_review':'PENDING'})
# Overview sheets: evidence only, not generated film art.
for start in range(0,len(manifest),8):
 chunk=manifest[start:start+8];canvas=Image.new('RGB',(1280,1000),'#222');d=ImageDraw.Draw(canvas)
 for k,r in enumerate(chunk):
  im=Image.open(r['path']).convert('RGB');im.thumbnail((300,430));x=(k%4)*320;y=(k//4)*500
  canvas.paste(im,(x,y));d.text((x+4,y+444),r['reference_id'],fill='white')
 canvas.save(ROOT/'qc'/f'REFERENCES_OVERVIEW_{start//8+1:02d}.jpg',quality=90)
(ROOT/'qc/RENDERED_REFERENCES.json').write_text(json.dumps(manifest,indent=2));print('RENDERED',len(manifest),flush=True)
