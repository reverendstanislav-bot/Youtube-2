from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,math,subprocess,hashlib,pymupdf
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');A=D/'ASSETS';A.mkdir(exist_ok=True);W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');L=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');receipt=[]
def hd(src,name,box=None,paper=False):
 pdf=None;pg=None
 if src.name.startswith('LAYOUT_'):pdf=L/'DOCUMENTS/SOURCES/AUTOMOTIVE_INDUSTRIES_1939_09_15.pdf';pg=int(src.stem.split('P')[-1])-1
 elif src.name.startswith('LOAD_'):pdf=L/'DOCUMENTS/SOURCES/USACE_1955_TRAFFICABILITY_OF_SNOW_REPORT_1.pdf';pg=int(src.stem.split('P')[-1])-1
 elif src.name.startswith('FATE_'):pdf=L/'DOCUMENTS/SOURCES/SCAMBOS_2005.pdf';pg=int(src.stem.split('P')[-1])-1
 if pdf:
  doc=pymupdf.open(pdf);page=doc[pg];clip=pymupdf.Rect(box[0]*page.rect.width,box[1]*page.rect.height,box[2]*page.rect.width,box[3]*page.rect.height) if box else page.rect;pix=page.get_pixmap(matrix=pymupdf.Matrix(4,4),clip=clip);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);doc.close();box_applied=True
 else:im=Image.open(src).convert('RGB');box_applied=False
 if box and not box_applied:im=im.crop(tuple(round(v*(im.width if j%2==0 else im.height)) for j,v in enumerate(box)))
 
 if name.startswith('SCAMBOS_FIG6'):im=ImageOps.grayscale(im).convert('RGB')
 im=ImageOps.contain(im,(1920,1080),Image.Resampling.LANCZOS);out=Image.new('RGB',(1920,1080),(245,243,234) if paper else (10,13,14));out.paste(im,((1920-im.width)//2,(1080-im.height)//2));f=A/(name+'.png');out.save(f);receipt.append({'asset':name,'source':str(src),'crop':box,'output':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()});return f
hd(D/'LAYOUT_P021.jpg','ORIGINAL_1939_SIDE',(.07,.40,.91,.65),True);hd(D/'LAYOUT_P021.jpg','ORIGINAL_1939_PLAN',(.07,.66,.91,.89),True)
hd(D/'LOAD_P034.jpg','USACE_1955_FIVEFOLD',(.105,.425,.93,.565),True);hd(D/'LOAD_P054.jpg','USACE_1955_WHEEL_LOAD',(.105,.402,.93,.452),True)
hd(D/'FATE_P009.jpg','SCAMBOS_FIG5_COASTLINES',(.025,.045,.96,.465),True);hd(D/'FATE_P011.jpg','SCAMBOS_FIG6_1963_ICEBERG',(.057,.18,.915,.421),True)
hd(D/'FATE_P011.jpg','SCAMBOS_FIG6_B_REMAINS',(.054,.431,.496,.623),True)
hd(D/'FATE_P011.jpg','SCAMBOS_FIG6_C_POLE',(.513,.431,.913,.623),True)
hd(D/'FATE_P014.jpg','SCAMBOS_CONCLUSION',(.025,.255,.95,.315),True);hd(D/'FATE_P013.jpg','SCAMBOS_FIG8_SEARCH_CONTEXT',(.07,.055,.96,.29),True)
for pid in ['PH12','PH13']:
 hd(L/f'ARCHIVE/SOURCES/PHOTOS_SOURCE_MARKED_PD/{pid}_1920px.jpg',pid+'_TRUE_ARCHIVE')
# Geography from real Natural Earth geometry. Journey line is schematic, not a surveyed road track.
geo=json.loads((L/'CURATED_EDIT_R2/DATA/NATURAL_EARTH_50M_COUNTRIES.geojson').read_text());im=Image.new('RGB',(1920,1080),(239,236,222));dr=ImageDraw.Draw(im)
def xy(lon,lat):return ((lon+93)/25*1710+105,(48-lat)/13*780+190)
for ft in geo['features']:
 g=ft['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
 for poly in polys:
  coords=poly[0]
  if not any(-128<x<-64 and 21<y<53 for x,y,*_ in coords):continue
  pts=[xy(p[0],p[1]) for p in coords];dr.polygon(pts,fill=(213,216,205),outline=(90,107,106),width=2)
route=[xy(-87.6298,41.8781),xy(-84.19,40.85),xy(-71.0589,42.3601)];im.save(A/'ROAD_GEOGRAPHY.png')
(A/'GEOGRAPHY_ROUTE_POINTS.json').write_text(json.dumps({'Chicago':route[0],'Gomer':route[1],'Boston':route[2],'route_is_schematic':True},indent=2))
# The real channel end card, not unrelated stock ice. Convert cadence only; preserve approved geometry.
end=A/'VIDEO010_ENDSCREEN_CANON_20S_24FPS.mp4';subprocess.run(['ffmpeg','-v','error','-i',r'C:\YOUTUBE\Youtube 2\9\VISUAL\MASTERS\VIDEO009_ENDSCREEN_CANON_20S.mp4','-an','-vf','fps=24,scale=1920:1080,setsar=1','-frames:v','480','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-y',str(end)],check=True)
receipt.append({'asset':'ENDSCREEN','source':'Owner-approved VIDEO009_ENDSCREEN_CANON_20S.mp4','output':str(end),'frames':480,'sha256':hashlib.sha256(end.read_bytes()).hexdigest()});(D/'DESIGN_ASSET_RECEIPTS.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'assets':len(receipt),'end_screen_frames':480,'new_ai_generation':False}))
