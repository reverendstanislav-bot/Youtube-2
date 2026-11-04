from pathlib import Path
import json,importlib.util,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');P=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');A=D/'ASSETS';C=D/'COMPS';C.mkdir(exist_ok=True);m=json.loads((P/'R6_1_MANIFEST.json').read_text());rows={r['shot_id']:r for r in m['shots']}
spec=importlib.util.spec_from_file_location('f',r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007\CAMP_CENTURY\DEVELOPMENT\RESOLVE_R1\build_fusion.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
# Explicit source replacements, not arbitrary new pictures.
replace={'S007':'ORIGINAL_1939_SIDE','S023':'ORIGINAL_1939_PLAN','S027':'ORIGINAL_1939_PLAN','S028':'ORIGINAL_1939_SIDE','S031':'ORIGINAL_1939_SIDE','S033':'ORIGINAL_1939_SIDE','S035':'ORIGINAL_1939_PLAN','S060':'ROAD_GEOGRAPHY','S105':'USACE_1955_FIVEFOLD','S108':'USACE_1955_WHEEL_LOAD','S160':'PH13_TRUE_ARCHIVE','S165':'SCAMBOS_FIG5_COASTLINES','S166':'SCAMBOS_FIG5_COASTLINES','S167':'SCAMBOS_FIG5_COASTLINES','S168':'SCAMBOS_FIG5_COASTLINES','S171':'SCAMBOS_FIG5_COASTLINES','S170':'SCAMBOS_FIG5_COASTLINES','S172':'SCAMBOS_FIG5_COASTLINES','S174':'SCAMBOS_FIG5_COASTLINES','S175':'SCAMBOS_FIG6_1963_ICEBERG','S176':'SCAMBOS_FIG6_B_REMAINS','S177':'SCAMBOS_FIG6_C_POLE','S178':'SCAMBOS_CONCLUSION','S179':'SCAMBOS_FIG8_SEARCH_CONTEXT','S186':'PH12_TRUE_ARCHIVE','S188':'PH13_TRUE_ARCHIVE','S152':'PH12_TRUE_ARCHIVE','S189':None,'S191':'SCAMBOS_FIG8_SEARCH_CONTEXT'}
replace['S189']=str(W/'MEDIA/PH07_1920px.jpg')
# Annotation coordinates reference the real 1920x1080 scene, and stay above the lower20%.
# Each path identifies the exact mechanism, never a rectangle around the whole frame.
plans={
'S007':{'labels':[('A BASE THAT COULD TRAVEL',.50,.91,.044,0)],'paths':[[[720,700],[720,520],[1010,520]]]},
'S020':{'labels':[('IMPROVISED SEARCHLIGHT',.50,.91,.044,8)],'paths':[[[780,560],[1160,740],[1550,790]]]},
'S023':{'labels':[('LIVING QUARTERS',.50,.91,.044,12)],'paths':[[[760,520],[990,520],[1150,520]]]},
'S024':{'labels':[('REPAIRS WITHOUT RETURNING TO BASE',.50,.91,.039,10)],'paths':[[[430,700],[850,700],[1120,650]]]},
'S026':{'labels':[('SCIENCE ON THE GROUND ROUTE',.50,.91,.040,8)],'paths':[[[300,650],[780,650]]]},
'S027':{'labels':[('SLEEP INSIDE THE TRANSPORT',.50,.91,.041,8)],'paths':[[[750,420],[1020,420]]]},
'S028':{'labels':[('ONBOARD WELDING GENERATOR',.50,.91,.042,8)],'paths':[[[1350,610],[1490,610],[1490,710]]]},
'S031':{'labels':[('AIRCRAFT EXTENDS THE SURVEY',.50,.91,.040,8)],'paths':[[[560,280],[1080,280]]]},
'S040':{'labels':[('DIESEL → GENERATOR',.50,.91,.046,4)],'paths':[[[420,540],[740,540],[1050,590]]]},
'S041':{'labels':[('GENERATOR → WHEEL MOTOR',.50,.91,.044,8)],'paths':[[[1530,520],[1130,520],[560,600]]],'reverse':True},
'S042':{'labels':[('HYDRAULIC WHEEL POSITIONING',.50,.91,.042,8)],'paths':[[[1190,350],[1220,530],[1220,720]]],'vertical':True},
'S044':{'labels':[('FRONT WHEELS RETRACT',.50,.91,.047,4),('PROPOSED CROSSING METHOD',.50,.85,.030,4)],'paths':[[[1690,730],[1690,510]]],'vertical':True},
'S045':{'labels':[('REAR WHEELS RETRACT',.50,.91,.047,4),('PROPOSED CROSSING METHOD',.50,.85,.030,4)],'paths':[[[450,730],[450,510]]],'vertical':True},
'S047':{'labels':[('15 FT / PROPOSED GAP',.50,.91,.046,4),('NOT AN ANTARCTIC DEMONSTRATION',.50,.85,.030,4)],'paths':[[[650,825],[1250,825]]]},
'S052':{'labels':[('STEER',.24,.91,.045,4),('DRIVE',.50,.91,.045,25),('BRAKE',.76,.91,.045,46)],'paths':[[[400,720],[710,650]],[[940,730],[1100,560]]]},
'S055':{'labels':[('STEERING AT THE WHEELS',.50,.91,.044,8)],'paths':[[[460,700],[810,570],[1210,700]]]},
'S056':{'labels':[('BODY HEIGHT CONTROL',.50,.91,.044,8)],'paths':[[[1190,760],[1190,480]]],'vertical':True},
'S060':{'labels':[('CHICAGO → BOSTON',.50,.91,.046,0),('SCHEMATIC ROUTE',.50,.85,.029,0)],'route':True},
'S064':{'labels':[('GOMER, OHIO / 1939',.50,.91,.044,0)],'paths':[]},
'S066':{'labels':[('REPAIR → LEVEL → REVERSE',.50,.91,.043,4)],'paths':[[[600,730],[600,560]],[[900,760],[1380,760]]]},
'S070':{'labels':[('TOWED UP THE CLIMBS',.50,.91,.044,8)],'paths':[[[550,750],[1170,650]]]},
'S072':{'labels':[('REAR CARGO SECTION REMOVED',.50,.91,.043,8)],'paths':[[[310,700],[610,700]]]},
'S081':{'labels':[('PREPARING THE SPARE TIRES',.50,.91,.043,8)],'paths':[[[540,740],[1040,740]]]},
'S097':{'labels':[('A TEMPORARY SURFACE',.50,.91,.046,8)],'paths':[[[340,780],[1230,780]]]},
'S098':{'labels':[('PLANKS SUPPORT THIS STRETCH',.50,.91,.041,8)],'paths':[[[540,785],[1250,785]]]},
'S103':{'labels':[('GRIP',.50,.91,.052,6)],'paths':[[[620,790],[1130,790]]],'blue':True},
'S104':{'labels':[('SUPPORT',.50,.91,.052,6)],'paths':[[[590,350],[590,730]],[[1320,350],[1320,730]]],'vertical':True},
'S105':{'labels':[('U.S. ARMY CORPS OF ENGINEERS / 1955',.50,.92,.035,0)],'paths':[[[35,628],[760,628]]],'document':True},
'S107':{'labels':[('GULF MARSH BUGGY',.27,.92,.035,0),('3,500 LB / WHEEL',.27,.855,.044,10),('SNOW CRUISER',.73,.92,.035,0),('17,500 LB / WHEEL',.73,.855,.044,28)],'load_bars':True},
'S108':{'labels':[('FIVE TIMES THE LOAD PER WHEEL',.50,.92,.041,4)],'paths':[],'document':True},
'S109':{'labels':[('THE SNOW MUST CARRY THE TIRE',.50,.91,.041,6)],'paths':[[[620,360],[620,720]],[[960,790],[1410,790]]]},
'S112':{'labels':[('STRONGER TIRE CONSTRUCTION',.50,.91,.043,8)],'paths':[[[640,720],[620,520],[730,350],[970,280],[1200,350]]]},
'S113':{'labels':[('TIRE STRENGTH ≠ SNOW SUPPORT',.50,.91,.040,6)],'paths':[[[630,780],[1170,780]]],'blue':True},
'S118':{'labels':[('FRONT: EXTRA TIRES',.73,.92,.036,4),('REAR: CHAINS',.26,.92,.036,32)],'paths':[[[1180,770],[1450,770]],[[260,650],[500,650]]]},
'S120':{'labels':[('LOWER PRESSURE',.50,.92,.047,6),('NO VERIFIED PRESSURE FIGURE',.50,.855,.031,6)],'paths':[[[660,740],[860,790],[1010,740]]],'blue':True},
'S133':{'labels':[('BLOCKED HYDRAULIC LINE',.50,.91,.044,8)],'paths':[[[820,600],[1080,600]]]},
'S134':{'labels':[('CLEAR THE BLOCKAGE',.50,.91,.045,8)],'paths':[[[650,630],[1200,630]]]},
'S136':{'labels':[('THIN CRUST',.30,.91,.044,6),('LOOSE POWDER BELOW',.72,.91,.039,35)],'paths':[[[390,730],[1250,730]],[[780,750],[780,840]]],'blue':True},
'S147':{'labels':[('THE ICE LAB / NOT THE CRUISER',.50,.91,.039,6)],'paths':[[[580,730],[1000,730]]]},
'S148':{'labels':[('CUT → WEIGH → COMPARE',.50,.91,.044,6)],'paths':[[[500,620],[850,620],[1210,570]]]},
'S154':{'labels':[('WAR DEPARTMENT REPORT / 1947',.50,.92,.035,0)],'paths':[[[350,681],[850,681]]],'document':True},
'S157':{'labels':[('ROOF LEVEL WITH THE SNOW',.50,.92,.040,0)],'paths':[[[350,462],[1550,462]],[[350,534],[800,534]]],'document':True},
'S162':{'labels':[('JANUARY 1958',.50,.91,.047,4)],'paths':[]},
'S165':{'labels':[('RECONSTRUCTING THE COAST',.50,.92,.040,0)],'paths':[]},
'S167':{'labels':[('HISTORICAL MAPS + LATER IMAGERY',.50,.92,.037,0)],'paths':[]},
'S168':{'labels':[('BAY OF WHALES',.30,.92,.044,0)],'paths':[],'lens':True},
'S170':{'labels':[('SCAMBOS & NOVAK / 2005',.50,.92,.037,0)],'paths':[]},
'S171':{'labels':[('1957–1962',.50,.92,.052,0),('INFERRED CALVING INTERVAL',.50,.85,.032,0)],'paths':[],'coastlines':True},
'S172':{'labels':[('POSSIBLE FINAL JOURNEY',.50,.92,.044,0)],'paths':[]},
'S175':{'labels':[('1963 / STATION REMAINS',.50,.92,.039,0)],'paths':[]},
'S176':{'labels':[('NOT A VERIFIED CRUISER SIGHTING',.50,.92,.038,4)],'paths':[]},
'S178':{'labels':[('PROBABLY NOT ABOARD',.50,.92,.046,0)],'paths':[]},
'S179':{'labels':[('POSSIBLE SEARCH AREA',.50,.92,.044,0),('NO RECOVERED VEHICLE',.50,.85,.032,0)],'paths':[]},
'S191':{'labels':[('EXACT LOCATION UNKNOWN',.50,.92,.046,0)],'paths':[]}}
# Final semantic anchor corrections after contact-sheet review.
for sid,paths in {
'S007':[[[760,700],[760,620],[1060,620]]], 'S020':[[[1100,140],[1100,210],[1020,280]]],
'S028':[[[1450,200],[1650,520],[1650,750]]],
'S040':[[[650,455],[480,455],[300,510]],[[1470,455],[1320,455],[1130,510]]],
'S042':[[[1330,180],[1460,240],[1460,450]]], 'S052':[],
'S055':[[[400,780],[450,735],[520,710]]], 'S056':[[[1100,700],[1100,450]]],
'S066':[], 'S070':[], 'S072':[[[850,180],[700,270],[600,420]]],
'S081':[[[1270,180],[1200,380],[1120,650]]],
'S097':[[[1180,835],[1450,835]]], 'S098':[[[540,835],[1250,835]]],
'S109':[[[620,360],[620,690]],[[360,845],[900,845]]],
'S112':[[[950,610],[1000,480],[1090,380],[1240,330]]],
'S113':[], 'S118':[], 'S120':[], 'S136':[[[230,850],[610,850]]]
}.items():plans[sid]['paths']=paths
replace['S052']=rows['S049']['path']
replace['S047']=rows['S044']['path']
plans['S047']['labels']=plans['S047']['labels'][:1]
plans['S066']['labels']=[('REPAIR',.23,.91,.044,4),('LEVEL',.50,.91,.044,28),('REVERSE',.77,.91,.044,52)]
plans['S118']['labels']=[('EXTRA TIRES + CHAINS',.50,.92,.042,4)]

plans['S171']['coastlines']=False
# Keep every new archive insert free of unrelated engineering labels.
new={r['shot_id']:r for r in json.loads((D/'NEW_ARCHIVE_SELECTS_R7.json').read_text())}
for sid in list(plans):
 if sid in new:plans.pop(sid)
# The route needs its own actual geometry instead of a decorative line.
route=json.loads((A/'GEOGRAPHY_ROUTE_POINTS.json').read_text());plans['S060']['paths']=[[route['Chicago'],route['Gomer'],route['Boston']]]
for city in ['Chicago','Gomer','Boston']:
 x,y=route[city];plans['S060']['labels'].append((city.upper() if city!='Gomer' else 'GOMER, OHIO',x/1920,1-(y+(60 if city=='Gomer' else -65))/1080,.033,12))
font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',48);receipts=[]
for sid in sorted(set(plans)|set(replace)):
 row=rows[sid];n=row['e']-row['s'];end=n-1;source=Path(row['path']);v=replace.get(sid)
 if v:source=Path(v) if ':' in v else A/(v+'.png')
 if source.suffix.lower() not in ['.png','.jpg','.jpeg']:continue
 im=Image.open(source).convert('RGB');im=ImageOps.contain(im,(1920,1080),Image.Resampling.LANCZOS);base=Image.new('RGB',(1920,1080),(245,243,234) if sid in replace and sid not in ['S160','S186','S188','S189'] else (8,12,14));base.paste(im,((1920-im.width)//2,(1080-im.height)//2));
 if sid in ['S154','S157']:
  im=ImageOps.contain(Image.open(source).convert('RGB'),(1790,690),Image.Resampling.LANCZOS);base=Image.new('RGB',(1920,1080),(245,243,234));base.paste(im,((1920-im.width)//2,175+(690-im.height)//2))
 if sid in ['S165','S166','S167','S170','S171','S172','S174','S175','S176','S177','S178','S179','S191']:
  im=ImageOps.contain(Image.open(source).convert('RGB'),(1780,875),Image.Resampling.LANCZOS);base=Image.new('RGB',(1920,1080),(245,243,234));base.paste(im,((1920-im.width)//2,165+(875-im.height)//2))
 basepath=A/(sid+'_BASE_HD_FINAL.png');base.save(basepath)
 tools=[f.loader('Source',basepath,end)];last='Source';plan=plans.get(sid,{'labels':[],'paths':[]});features=[]
 if sid in ['S105','S108','S154','S157']:
  import numpy as np
  aa=np.asarray(base.convert('L'));ys=np.where((aa<115).sum(axis=1)>28)[0];bands=[]
  for yy in ys:
   if not bands or yy-bands[-1][-1]>9:bands.append([int(yy)])
   else:bands[-1].append(int(yy))
  bands=[b for b in bands if len(b)>3]
  if sid=='S105' and len(bands)>=4:plan['paths']=[[[35,bands[3][-1]+11],[760,bands[3][-1]+11]]]
  if sid=='S108' and len(bands)>=2:plan['paths']=[[[500,bands[-1][-1]+11],[920,bands[-1][-1]+11]]]
  if sid=='S154' and len(bands)>=8:plan['paths']=[[[350,bands[7][-1]+12],[850,bands[7][-1]+12]]]
  if sid=='S157' and len(bands)>=5:plan['paths']=[[[350,bands[3][-1]+12],[1550,bands[3][-1]+12]],[[350,bands[4][-1]+12],[800,bands[4][-1]+12]]]
 for j,path in enumerate(plan.get('paths',[])):
  overlay=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(overlay);color=(51,111,143) if plan.get('blue') else (192,137,48);pts=[tuple(p) for p in path];draw.line(pts,fill=(*color,65),width=24,joint='curve');draw.line(pts,fill=(*color,240),width=4,joint='curve');x,y=pts[-1];r=6;draw.ellipse((x-r,y-r,x+r,y+r),fill=(*color,230))
  if len(pts)==2 and math.dist(pts[0],pts[1])>150 and not plan.get('document'):
   a,b=pts[-2:];angle=math.atan2(b[1]-a[1],b[0]-a[0]);arrow=[(b[0]-19*math.cos(angle-.45),b[1]-19*math.sin(angle-.45)),b,(b[0]-19*math.cos(angle+.45),b[1]-19*math.sin(angle+.45))];draw.line(arrow,fill=(*color,235),width=5)
  op=A/f'{sid}_PATH_FINAL_{j}.png';overlay.save(op);on=f'Path{j}';mask=f'Mask{j}';tools.append(f.loader(on,op,end));t=f.ease(9+j*19,min(end-12,42+j*19));reverse=pts[0][0]>pts[-1][0];vertical=plan.get('vertical',False)
  if vertical:tools.append(f.rectangle(mask,.5,f'.5*{t}' if pts[0][1]>pts[-1][1] else f'1-.5*{t}',1,t))
  else:tools.append(f.rectangle(mask,f'1-.5*{t}' if reverse else f'.5*{t}',.5,t,1))
  merge=f'PathMerge{j}';tools.append(f.merge(merge,last,on,'1',mask=mask));last=merge;features.append('local source-targeted write-on path')
 if plan.get('load_bars'):
  for j,(left,width,delay) in enumerate([(.09,.12,8),(.57,.60,29)]):
   # Same scale 1:5; fit each bar in its half by scaling both equally.
   width=[.06,.30][j];t=f.ease(delay,min(end-8,delay+30));mask=f'LoadMask{j}';tools.append(f.rectangle(mask,f'{left}+.5*{width}*{t}',.79,f'{width}*{t}',.012));bg=f'LoadInk{j}';tools.append(f.background(bg,(.72,.48,.16),.92,mask));merge=f'LoadMerge{j}';tools.append(f.merge(merge,last,bg));last=merge
  features.append('native load bars on a shared exact1:5 scale')
 if plan.get('lens'):
  tools.append('DetailZoom = Transform { Inputs = { Input='+f.link('Source')+',Size='+f.inp(2.2)+',Center='+f.point(.798,.788)+' } }')
  tools.append('LensMask = EllipseMask { Inputs = { MaskWidth='+f.inp(1920)+',MaskHeight='+f.inp(1080)+',Center='+f.point(.78,.48)+',Width='+f.inp(.30)+',Height='+f.inp(.5333)+',SoftEdge='+f.inp(.004)+' } }')
  tools.append(f.merge('LocalDetailLens',last,'DetailZoom',f.ease(12,33),mask='LensMask'));last='LocalDetailLens';features.append('native local source lens on Bay of Whales; no full-frame zoom')
 if plan.get('coastlines'):
  import numpy as np
  rgb=np.asarray(base).astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
  masks=[(gg>rr*1.055)&(gg>bb*1.025)&((rgb.max(2)-rgb.min(2))>22),(bb>rr*1.07)&(bb>gg*1.015)&((rgb.max(2)-rgb.min(2))>22)]
  for k,mm in enumerate(masks):
   mm[:165]=False;alpha=Image.fromarray((mm*220).astype('uint8')).filter(__import__('PIL.ImageFilter',fromlist=['MaxFilter']).MaxFilter(3));ov=Image.new('RGBA',(1920,1080),(43,126,72,0) if k==0 else (53,91,163,0));ov.putalpha(alpha);op=A/(sid+'_COASTLINE_'+str(k)+'.png');ov.save(op);nm='Coastline'+str(k);tools.append(f.loader(nm,op,end));merge='CoastlineMerge'+str(k);blend=f.ease(7+k*38,25+k*38);tools.append(f.merge(merge,last,nm,blend));last=merge
  features.append('sequential emphasis of pixels from published1957/1962 map traces; no invented coast geometry')
 for j,(text,x,y,size,delay) in enumerate(plan.get('labels',[])):
  # Fixed bounds are checked before render; halo guarantees readability across source changes.
  text=text.replace('→',' / ').replace('≠',' IS NOT ').replace('–','-');px=round(size*1080);ft=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',px);bbox=ft.getbbox(text);width=bbox[2]-bbox[0]
  while width>1740 and size>.028:size-=.001;px=round(size*1080);ft=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',px);bbox=ft.getbbox(text);width=bbox[2]-bbox[0]
  assert x*1920-width/2>=64 and x*1920+width/2<=1856,(sid,text,width,x)
  region=base.crop((max(0,int(x*1920-width/2)),max(0,int((1-y)*1080-32)),min(1920,int(x*1920+width/2)),min(1080,int((1-y)*1080+32)))).convert('L');import PIL.ImageStat
  light=PIL.ImageStat.Stat(region).mean[0]>135;ink=(.10,.16,.19) if light else (.98,.97,.91);halo=(.98,.98,.95) if light else (.02,.03,.035)
  txt=f'Text{j}';node=f.text(txt,text,y,size,ink,x).replace('Style=Input { Value = "Regular" }','Style=Input { Value = "Bold" }');fields=f'Enabled2={f.inp(1)},Type2={f.inp(1)},Thickness2={f.inp(.035)},Red2={f.inp(halo[0])},Green2={f.inp(halo[1])},Blue2={f.inp(halo[2])},Alpha2={f.inp(.95)},GlobalOut={f.inp(1000000)},';node=node.replace('Inputs = {','Inputs = { '+fields,1);tools.append(node);merge=f'TextMerge{j}';tools.append(f.merge(merge,last,txt,f.ease(delay,min(end-8,delay+8))));last=merge;features.append('large high-contrast native Text+ with opposite-tone outline')
 if plan.get('route'):
  for city,(x,y) in [(c,route[c]) for c in ['Chicago','Gomer','Boston']]:
   dot=f'Dot{city}';tools.append(f.rectangle(dot,x/1920,1-y/1080,.007,.012));bg=f'DotInk{city}';tools.append(f.background(bg,(.15,.23,.25),1,dot));merge=f'DotMerge{city}';tools.append(f.merge(merge,last,bg));last=merge
 tools.append('MediaOut1 = MediaOut { Inputs = { Input='+f.link(last)+' } }');dest=C/(sid+'_FINAL.comp');f.write_comp(dest,tools,end);receipts.append({'shot_id':sid,'source':str(source),'base':str(basepath),'comp':str(dest),'frames':n,'features':features,'labels':[p[0] for p in plan.get('labels',[])],'status':'NATIVE_RENDER_PROOF_REQUIRED'})
(D/'MOTION_DESIGN_R7.json').write_text(json.dumps(receipts,indent=2));(D/'SOURCE_REPLACEMENTS_R7.json').write_text(json.dumps(replace,indent=2));print(json.dumps({'native_scenes':len(receipts),'motion_explanations':sum(bool(r['features']) for r in receipts),'new_ai_generation':0}),flush=True)
