from pathlib import Path
import json,csv,subprocess,concurrent.futures,math,re
from PIL import Image,ImageDraw,ImageFont
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
# These subject windows were chosen from the complete source-film indexes and narration.
# Scene cuts below constrain them; no evenly spaced bulk micro-cutting.
C=[]
def add(source,ch,beat,start,end,subject,site='DIRECT_CAMP_CENTURY',role='DIRECT_HISTORICAL_ACTION',warning=''):
    C.append(dict(source_id=source,chapter=f'CH{ch:02}',beat=f'CC07-S4-CH{ch:02}-B{beat:02}',requested_start=start,requested_end=end,actual_shot_description=subject,site_class=site,evidence_role=role,editorial_warning=warning))
SUP='SAME_PROJECT_SUPPLY_CHAIN'
CTX='CONTEXTUAL_ACTUAL_SITE_NOT_LITERAL_PROOF'
# Supply and construction: original 1959-60 Army construction film, best-colour print.
for a,b,desc in [(226,242,'Tractor and loaded material sleds at the Camp Century supply staging area'),(243,260,'Crane places a prefabricated load on a sled for the Camp Century convoy'),(272,284,'Crew secures the heavy swing load and sled fittings'),(286,303,'Heavy swing convoy begins its snow traverse'),(313,326,'Caterpillar tractor tracks and towing work'),(328,343,'Loaded sled train progresses across the ice cap'),(346,360,'Convoy crew works beside the towing vehicle'),(414,429,'Heavy swing passes across wind-packed snow'),(1120,1135,'Large fuel load brought in by the Camp Century construction supply convoy')]:add('F01B',2,2 if a<350 else 3,a,b,desc,SUP,warning='1959-60 Camp Century construction logistics. Staging/route footage is not footage inside the camp. Period film tonnage is not authority to change locked V4 figures.')
for a,b,beat,desc in [(529,543,1,'Peter snow miller advances while throwing a high stream of snow'),(544,557,1,'Snow milling machine cuts deeper into the camp trench'),(559,572,1,'Workers check and prepare the excavated trench'),(574,586,1,'Crew carries planks across the trench shoulders'),(587,598,1,'Worker levels the snow trench wall by hand'),(606,619,2,'Crew lowers a corrugated steel arch into the trench'),(621,637,2,'Workers cut and move snow blocks for the roof enclosure'),(653,670,3,'Worker cuts an opening through the snow wall between passages'),(677,691,3,'Crew places structural floor beams in the excavated trench'),(695,710,3,'Prefabricated timber building panels arrive inside the trench'),(711,724,3,'Workers assemble the floor structure inside the snow walls'),(735,749,3,'Worker raises a ceiling panel in a prefabricated room'),(750,762,3,'Insulated ceiling panel is fitted above the room'),(763,774,3,'Worker secures the insulated room door and wall panels'),(789,805,2,'Crew builds a snow-block closure at the tunnel opening')]:add('F01B',3,beat,a,b,desc,warning='Initial camp construction, not a later maintenance or creep measurement sequence.')
# Real working settlement used as context for the opening, not proof of a dated closure rate.
for a,b,desc in [(920,934,'Crew and tall structural framing inside the large reactor trench'),(1048,1064,'Worker opens a snow-covered emergency escape hatch'),(1139,1156,'Tracked vehicle moves into the camp workshop arch'),(1833,1845,'Tracked vehicle travels along the underground main passage'),(1847,1863,'Crew handles freight beside a vehicle inside the main communication tunnel')]:add('F01B',1,1,a,b,desc,role=CTX,warning='Real Camp Century activity. Does not itself document 1963 tunnel shrinkage or measured annual closure rates.')
# PM-2A transport and installation: support scenes kept separate from the underground site.
for a,b,desc in [(1168,1184,'Thule harbour handling of PM-2A plant components'),(1185,1200,'PM-2A vessel component on a heavy road transporter'),(1208,1223,'Large vapor-container section travels toward the snow-line transfer'),(1224,1239,'Crew checks the specially crated PM-2A shipment'),(1240,1256,'Crane transfers the round PM-2A component to an ice-traverse load'),(1260,1277,'Reactor supply convoy carries the heavy plant across snow')]:add('F01B',4,2,a,b,desc,SUP,warning='Actual inbound PM-2A supply chain, 1960. Harbour/road/snow-line scenes are not the Camp Century interior.')
for a,b,beat,desc in [(1338,1355,2,'Crane and crew unload PM-2A machinery at Camp Century'),(1357,1375,2,'Large plant assembly is eased into the underground reactor building'),(1382,1399,2,'Tractors and crew guide the heavy plant vessel toward the arched trench'),(1400,1414,2,'View along the large plant vessel inside the underground structure'),(1415,1431,2,'Workers complete mechanical fitting on the installed plant vessel'),(1475,1488,4,'Personnel attend the plant piping and machinery inside the reactor building'),(995,1011,3,'Crew works on the camp water-production apparatus'),(1014,1031,3,'Water is handled at the camp melting and pumping installation'),(1758,1771,3,'Kitchen equipment and cooking work in the occupied camp')]:add('F01B',4,beat,a,b,desc,warning='Historical plant/support activity only. Do not present a generic mechanical shot as the documented turbine failure or a particular waste-sump event.')
# Everyday life in the public Army film, to contrast with the unbuilt Iceworm proposal.
for a,b,desc in [(1698,1710,'Light and services inside the occupied camp passage'),(1713,1725,'Camp medical personnel and an occupied room'),(1778,1793,'Camp dining hall and meals in the underground settlement'),(1800,1811,'Personnel relax in a furnished camp living room'),(1813,1825,'Soldier reads while other personnel move in the living quarters')]:add('F01B',5,1,a,b,desc,role=CTX,warning='Actual occupied base, never an operational Iceworm railway, missile installation or weapons deployment.')
# Snow-work context: kept explicitly distinct from the numerical maintenance claims.
for a,b,beat,desc in [(832,847,3,'Peter miller throws excavated snow from the main trench'),(848,863,3,'Coordinated snow milling at different trench levels'),(865,881,4,'Snow-milling machinery clears a deep cut beside camp structures'),(891,905,4,'Crew works at the snow edge above the large camp trench')]:add('F01B',6,beat,a,b,desc,role=CTX,warning='1960 construction excavation illustrates the physical scale of snow work; not a filmed annual re-trimming tally, measured creep or the report Figure 33 chainsaw scene.')
# Research/legacy context: no substitution for the 1966 bedrock core or modern radar.
for a,b,desc in [(128,143,'1959 site-selection team examines the Camp Century snow surface'),(154,169,'Survey team gestures and marks the proposed camp location'),(1746,1757,'Camp personnel work and study together in an occupied room')]:add('F01B',8,4,a,b,desc,role=CTX,warning='Camp Century archival research/settlement context only. Not the 1966 deep core, plant-bearing basal sample, 2024 NASA radar or a modern laboratory.')
# Independent 1964 removal film. These are not scenes of the original construction convoy.
for a,b,desc in [(540,557,'1964 reopening team heavy swing travels to Camp Century'),(583,599,'Removal-team tractor reaches the camp and unloading begins'),(608,623,'Technicians prepare instruments and equipment in the reopened camp'),(630,646,'Crew disconnects and works on plant pipework'),(654,669,'Personnel work around the plant vessel and connected fittings'),(674,691,'Workers operate chain hoisting gear inside the reactor building'),(695,711,'Crew handles a removed mechanical assembly inside the plant space'),(718,734,'Tractor hauls a crated plant load up the camp access cut'),(739,756,'Personnel guide a large assembly through the plant doorway'),(765,783,'Crew opens snow cover above the reactor removal route'),(815,830,'Crane lifts a large shielded container at the Camp Century site'),(834,850,'Crew handles packing materials and equipment inside the plant area'),(855,870,'Plant hardware is secured and boxed by removal personnel'),(903,919,'Crane and snow excavation work above the reactor trench'),(946,964,'Machinery clears access through the snow structure for removal'),(965,982,'Heavy shielded equipment is raised from the camp opening'),(998,1014,'Crew prepares a large plant vessel for extraction'),(1018,1034,'Removal personnel work around the vessel and lifting gear'),(1041,1058,'Heavy plant load is moved through the opened trench'),(1064,1081,'Remaining industrial pipework and assemblies are dismantled'),(1124,1141,'Large PM-2A component emerges onto the camp surface'),(1147,1163,'Crew guides a heavy removed component into its transport position'),(1166,1182,'Removed plant assembly rests on the surface transport support'),(1185,1199,'Removal crew covers and packs equipment on the Camp Century surface')]:add('F03',7,1 if a<830 else 2,a,b,desc,warning='1964 PM-2A removal mission, not 1959 construction and not footage of the later abandoned buried site. Public 640x480 copy has severe magenta dye fade; use sparingly, source colour unaltered.')
for a,b,desc in [(1221,1238,'1964 return convoy carries crated PM-2A machinery away from camp'),(1240,1257,'Plant cargo is transferred at the Camp Tuto loading ramp'),(1263,1280,'Road transporter carries crated removed plant components'),(1292,1308,'Thule harbour crane handles the returned reactor cargo'),(1325,1343,'Ship loading of the removed PM-2A components at Thule')]:add('F03',7,2,a,b,desc,SUP,warning='Outbound 1964 removal logistics; Camp Tuto/Thule are separately identified, not Camp Century interiors. Strong magenta source-print fade.')
# New Camp Century visit shots in the Scout film; no Tuto weather station or copyrighted paintings.
for a,b,ch,beat,desc in [(77,87,5,1,'Scientific aides and personnel inside the occupied Camp Century settlement'),(121,132,3,3,'People move through the occupied Camp Century corridor'),(139,150,8,4,'Camp personnel demonstrate laboratory work during the scientific-aide visit'),(152,162,4,4,'Scientific aides observe machinery and instruments at Camp Century')]:add('F05',ch,beat,a,b,desc,role=CTX,warning='1960-61 scientific-aide visit. No claim this is the 1966 basal core. Excludes Camp Tuto introduction and Norman Rockwell paintings explicitly credited as copyrighted later in the reel.')

valid=[];rejected=[]
for i,row in enumerate(C,1):
    sid=row['source_id'];qc=json.loads((R/'reports'/(sid+'_SOURCE_QC.json')).read_text());assert qc['status']=='FULL_DECODE_PASS'
    a,b=row['requested_start'],row['requested_end'];cuts=json.loads((R/'reports'/(sid+'_SCENE_CUTS.json')).read_text())['times']
    limits=[0]+cuts+[qc['duration']];choices=[]
    for x,y in zip(limits,limits[1:]):
        st=max(a,x+.12);en=min(b,y-.12)
        if en-st>=5:choices.append((en-st,st,en))
    if not choices:
        # A proposed window may contain several useful short shots; do not assemble micro-fragments.
        row['rejection']='No continuous >=5-second interval inside proposed window';rejected.append(row);continue
    _,st,en=max(choices)
    fps=eval(qc['fps'],{'__builtins__':{}})
    fi=math.ceil(st*fps);fo=math.floor(en*fps)
    row.update(scene_id=f'CC07-C{i:03}',start_frame=fi,end_frame_exclusive=fo,start_sec=fi/fps,end_sec=fo/fps,seconds=(fo-fi)/fps,source_fps=qc['fps'],source_path=qc['path'],source_sha256=qc['sha256'],status='CANDIDATE_PENDING_DENSE_VISUAL_REVIEW')
    if (fo-fi)/fps<5:row['rejection']='Frame-aligned interval below 5 seconds';rejected.append(row);continue
    valid.append(row)
(R/'reports/CANDIDATE_SCENES.json').write_text(json.dumps(valid,indent=2));(R/'reports/REJECTED_SUBFIVE_CANDIDATES.json').write_text(json.dumps(rejected,indent=2))
print('SUBJECT_WINDOWS',len(C),'CONTINUOUS_CANDIDATES',len(valid),'SECONDS',sum(r['seconds'] for r in valid),flush=True)

def preview(row):
    folder=R/'qc_sheets'/'candidate_motion';folder.mkdir(exist_ok=True)
    file=folder/(row['scene_id']+'.jpg')
    if file.exists():return file
    # Eight sequential phases across the entire candidate; actual source times printed only in QC.
    w,h=240,180
    raw=subprocess.check_output(['ffmpeg','-hide_banner','-v','error','-ss',str(row['start_sec']),'-i',row['source_path'],'-t',str(row['seconds']),'-an','-vf',f"fps={8/row['seconds']}:start_time=0,scale={w}:{h},setsar=1",'-frames:v','8','-pix_fmt','rgb24','-f','rawvideo','-'])
    import numpy as np
    frames=np.frombuffer(raw,np.uint8).reshape(-1,h,w,3)
    out=Image.new('RGB',(w*4,h*2+55),(14,17,20));draw=ImageDraw.Draw(out)
    for j,fr in enumerate(frames):out.paste(Image.fromarray(fr),(j%4*w,j//4*h))
    draw.text((5,h*2+3),f"{row['scene_id']} {row['source_id']} {row['start_sec']:.3f}--{row['end_sec']:.3f}s {row['chapter']} {row['beat']}",fill='white')
    draw.text((5,h*2+22),row['actual_shot_description'][:130],fill='white')
    out.save(file,quality=91)
    return file
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(preview,valid))
for start in range(0,len(valid),4):
    page=Image.new('RGB',(960,415*len(valid[start:start+4])),(12,15,18))
    for j,row in enumerate(valid[start:start+4]):
        with Image.open(R/'qc_sheets/candidate_motion'/(row['scene_id']+'.jpg')) as shot:page.paste(shot,(0,j*415))
    page.save(R/'qc_sheets'/f'CANDIDATES_{start//4+1:02}.jpg',quality=90)
print('CANDIDATE_MOTION_REVIEW_PAGES_READY',len(valid),flush=True)
