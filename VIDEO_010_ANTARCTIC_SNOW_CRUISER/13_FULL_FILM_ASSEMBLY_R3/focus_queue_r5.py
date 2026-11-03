from pathlib import Path
import json
R=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10\IMAGEGEN_FULL_FILM_R2');F=R/'GENERATION_QUEUE_ASSEMBLY_R4.json';q=json.loads(F.read_text());assert json.loads((R/'GENERATION_CONTROL.json').read_text())['run']==False
REF=R.parent/'IMAGEGEN_GAPS_R1/REFERENCES';STYLE=REF/'G07_REVISED_R2.png';STYLE_TEXT='One original landscape 16:9 Camp Century documentary drawing: hand-worked ink, charcoal and restrained watercolor, cream paper, muted olive clothing, blue-grey Antarctic light. Match the STYLE reference, not its subject or composition. Not a photograph, CGI or poster. No writing, numbers, captions, stamps, logos, graphic boxes, arrows or watermark. Keep key action out of the bottom 20%. All text and emphasis are later native Fusion layers.'
no_car={103,104,107,108,112,113,114,116,117,129,130,131,132,133,134,135,136,137,138,139,140,144,147,148,150}
macro={103,104,107,108,114,117,121,127,129,132,137,138,141,142}
extras={
103:'Tight hands-and-hydraulic-line repair. The pipe connection and tool fill the frame; no exterior vehicle body.',
104:'Macro gloved hand replacing a period fuse, with adjacent plain mechanical components. No exterior, no readable panel markings.',
107:'Close disconnected hydraulic line being inspected after a blockage. Do not invent a measured plug, pressure reading or detailed failure diagram.',
108:'Gloved hands cleaning the hydraulic line with ordinary period tools. No whole vehicle exterior.',
109:'Inside the cab: hands operating period drive controls. No exterior truck, no cutaway of the whole vehicle.',
110:'Extreme close-up of a front balloon tyre contact edge breaking through a thin crust into powder. A paired front spare may be partly visible. Do not show a whole truck.',
112:'Human-scale interior of the crew shelter: bunks, a cup, worn gloves, tired people. No entire vehicle cutaway.',
113:'Two period researchers preparing instruments at West Base. A small field-station hut supplies context, not a motor vehicle.',
114:'Close scientific instruments on a work table in a simple field-station room. Do not add a vehicle.',
116:'Inside the separate ice-laboratory hut, a floor opening into ice. This is a STATION BUILDING, not inside the Snow Cruiser. No motor vehicle or wheels.',
117:'Close cut blocks of layered snow and a period balance. No reading, labels, specimen numbers or motor vehicle.',
122:'Quiet cabin disarray only; no invented people vandalising the interior and no spectacular invented damage.',
123:'The roof is flush with surrounding snow. Do not expose the buried wheels or imply a measured burial depth.',
124:'Visitors approach the buried roof from the snow surface. No spectacular deep mine shaft or exposed wheels.',
126:'An ordinary unmeasured excavation toward a buried vehicle roof in 1958. No military base, crane or specific undocumented equipment.',
127:'Tight upper hatch, rough snow steps and a gloved hand. Do not expose the entire machine.',
129:'Hands comparing original editorial map sketches on a research table. No counterfeit historical document or readable invented record.',
130:'An original illustrative coastal ice edge. No vehicle, no surveyed coordinates, no claimed exact historical coastline.',
131:'Quiet ice cliff and dark seawater. Absolutely no vehicle, machinery, wreck or people.',
132:'A researcher comparing plain map sheets. These are editorial props, not reproduced historical evidence. No readable text.',
133:'A spare original watercolor geography study of an ice edge and open water; no exact old coastline, numbers, labels, grids or vehicle. Dates are later native overlays.',
134:'A broad tabular ice block separated in dark water. NO VEHICLE, cargo or wreck anywhere on the ice or underwater.',
135:'Quiet drifting tabular ice, shown as an interpretation of a possibility. No vehicle, cargo, wreck, tracks or eyewitness claim.',
136:'Wide tabular iceberg only, no ship, vehicle or invented recovered artifacts.',
137:'Close weathered station-timber fragments on ice. No vehicle parts, metal chassis, graves or bodies.',
138:'Researcher comparing plain unlabelled editorial sketches and timber notes. No readable forged record, no vehicle image.',
139:'Original conceptual ice-shelf section above dark water. NO vehicle, wreck, coordinate grid, discovery marker or exact seafloor survey.',
140:'Broad dark water and empty seafloor suggestion. NO vehicle, wreck silhouette, search target, coordinate or located artifact.',
141:'Tight gloved hands and a period torch at a wheel hub. Use the historical photo for the type of task, not its framing.',
142:'Human-scale view of a person emerging from a snow-surrounded upper hatch. No whole vehicle hero shot.',
143:'Scientific work in the immediate base area. The Cruiser is stationary context only; no successful inland travel.',
144:'People carrying packed instruments away from the base, cropped close around hands and crates. No invented specific ship, aircraft or vehicle.',
147:'Wide changing shelf edge, sea and empty ice. No visible Cruiser, wreck, floating cargo or claimed observed departure.',
148:'Quiet empty interior room with period bunks and work equipment. No whole vehicle exterior or dollhouse cutaway.',
149:'A stationary vehicle with nobody around. No death imagery, wreckage or recovered-machine claim.',
150:'An empty Antarctic meeting of ice and sea. NO vehicle, wreck, submarine, search target, coordinates, outlines or imagined final resting place.'}
fix={
59:('North Star sailing away from Boston in late1939. View from behind the stern toward open water; the foredeck cargo is OUT OF FRAME. A period expedition ship and wake dominate. NO Snow Cruiser, truck, road, workshop or snowfield in this image.',['PH10_1920px.jpg']),
64:('Cold rough seas during the southbound voyage. Close gloved hands securing lashings on an icy wooden ship deck, period railing and dark WAVES visible beyond. No snowy land, flat ice plain, whole truck or invented accident.',['PH10_1920px.jpg']),
68:('Tight view of a TEMPORARY WOODEN PLANK unloading ramp descending from an expedition ship deck onto SEA ICE. Timber beams and planks, not concrete, masonry, steel harbour walls or a warehouse. Only one partly cropped smooth balloon tyre may enter from the deck edge; no whole truck.',[next(z['existing_path'] for z in __import__('csv').DictReader((R/'SHOT_PLAN_193.csv').open(encoding='utf-8-sig')) if z['asset_id']=='PH14')]),
82:('Close gloved hand inspecting the INTACT smooth balloon-tyre sidewall and rim. NO rasp, file, knife, shaving, scraping, cutting grooves, tread removal or rubber modification. This illustrates tyre construction, not an invented workshop procedure.',['PH09_1920px.jpg'])}
changed=[]
for x in q:
 n=int(x['asset_id'][3:])
 if n not in fix and n<103:continue
 if n>=103 and x['status']=='GENERATED':continue
 old=x['prompt'];x['previous_prompt_before_focus_R5']=old
 if n in fix:
  scene,refs=fix[n];x['previous_receipt_before_focus_R5']={k:x.get(k) for k in ('status','sha256','source_generated_path','generated_prompt','generated_references')};x['status']='QUEUED_NOT_GENERATED';x['qc']='TARGETED_CONTENT_REGEN';focus=scene
 else:
  scene=x['visual_action'];focus=extras.get(n,scene)
  if n in no_car:focus+=' NO MOTOR VEHICLE, tyres, truck body or mechanical chassis in this composition.'
  elif n not in {109,121,122,127,141,142,148}:
   focus+=' Snow Cruiser continuity: two axle stations only; smooth balloon tyres. If the wheels are exposed after the Antarctic modification, paired FRONT tyres and chains on the REAR pair; never a third axle.'
  refs=[]
  if n in {105,118,119,120,123,124,125,126,127,145,146,149}:refs=['PH08_1920px.jpg' if n in {105,118,119,120} else 'PH11_1920px.jpg']
  elif n==141:refs=['PH04_1920px.jpg']
  elif n==142:refs=['PH03_1920px.jpg']
  elif n in {113,114,116,117,143}:refs=[str(R.parent/'IMAGEGEN_GAPS_R1/IMAGES/SCG21.png')]
  elif n in {130,131,133,134,135,136,147,150}:refs=[str(R.parent/'IMAGEGEN_GAPS_R1/IMAGES/SCG23.png')]
  elif n==137:refs=[str(R.parent/'IMAGEGEN_GAPS_R1/IMAGES/SCG24.png')]
  elif n in {139,140}:refs=[str(R.parent/'IMAGEGEN_GAPS_R1/IMAGES/SCG25.png')]
  elif n not in no_car:refs=[str(R.parent/'IMAGEGEN_GAPS_R1/IMAGES/SCG19.png')]
  elif n in {103,104,107,108,112,148}:refs=['D03_AUTO_PDF_PAGE_021_300DPI.png']
 prefix='EXTREME CLOSE / MATERIAL DETAIL. ' if n in macro or n in {64,68,82} else ''
 x['prompt']=prefix+focus+' '+STYLE_TEXT
 paths=[STYLE]+[Path(z) if Path(z).is_absolute() else REF/z for z in refs]
 for ii,z in enumerate(paths):
  if not z.exists() and z.name.startswith('PH'):
   aid=z.name.split('_')[0];matches=[a['existing_path'] for a in __import__('csv').DictReader((R/'SHOT_PLAN_193.csv').open(encoding='utf-8-sig')) if a['asset_id']==aid];assert matches,aid;paths[ii]=Path(matches[0])
 assert all(z.exists() for z in paths),[(str(z),z.exists()) for z in paths]
 x['references']=[{'role':'STYLE ONLY' if i==0 else 'CONTENT FACTS / CONTINUITY ONLY, NOT COMPOSITION','path':str(z)} for i,z in enumerate(paths)];x['prompt_version']='FOCUS_RECONCILED_R5';changed.append(x['asset_id'])
tmp=F.with_suffix('.tmp');tmp.write_text(json.dumps(q,indent=2));tmp.replace(F)
(R/'FOCUS_RECONCILIATION_R5.json').write_text(json.dumps({'reason':'Prevent whole-vehicle references overriding ship, hands, science and empty-ocean scenes','changed':changed,'targeted_regens':['SCN059','SCN064','SCN068','SCN082'],'script_changed':False},indent=2));print(json.dumps({'changed':len(changed),'ids':changed}))
