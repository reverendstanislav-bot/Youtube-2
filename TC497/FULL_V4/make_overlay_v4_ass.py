import json, os
from pathlib import Path

PUB=Path(os.environ['V4_PUBLIC'])
OUT=Path(os.environ['ASS_OUT'])
CUT=82.6
shots=json.load(open(PUB/'shots.json',encoding='utf-8'))
caps=json.load(open(PUB/'captions.json',encoding='utf-8'))

def ts(t):
    h=int(t//3600); t-=h*3600; m=int(t//60); s=t-m*60
    return f'{h}:{m:02d}:{s:05.2f}'

def esc(s):
    return str(s).replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n','\\N')

def source_state(sh):
    code=sh['code']; ch=sh['chapter']
    if code.startswith('AR-OTTER') or code=='AR-PATENT':
        return 'DOCUMENT'
    if code.startswith('AR-'):
        return 'ARCHIVE'
    if ch=='NUCLEAR — RETENTION BEAT' and code in {'V4-NUKE','V2-NUKE'}:
        return 'CONCEPT'
    return 'RECONSTRUCTION'

head='''[Script Info]
ScriptType: v4.00+
PlayResX: 960
PlayResY: 540
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,31,&H00E6DDC8,&H00E6DDC8,&HDC171A1C,&H90171A1C,-1,0,0,0,100,100,0,0,1,2.5,0,2,56,56,36,1
Style: Chapter,DejaVu Sans,27,&H00F3EBDD,&H00F3EBDD,&HC0171A1C,&H90171A1C,-1,0,0,0,100,100,1.1,0,1,1.8,0,7,52,52,50,1
Style: Kicker,DejaVu Sans,12,&H00747D5F,&H00747D5F,&H00171A1C,&H70171A1C,-1,0,0,0,100,100,1.8,0,3,0,0,7,52,52,28,1
Style: Tag,DejaVu Sans,17,&H00F3EBDD,&H00F3EBDD,&H00171A1C,&H85171A1C,-1,0,0,0,100,100,.6,0,3,0,0,7,52,52,56,1
Style: Fact,DejaVu Sans,23,&H00F3EBDD,&H00F3EBDD,&HC0171A1C,&H90171A1C,-1,0,0,0,100,100,.7,0,1,2,0,7,56,56,86,1
Style: Source,DejaVu Sans,12,&H00E6DDC8,&H00E6DDC8,&H00171A1C,&H85171A1C,-1,0,0,0,100,100,1.2,0,3,0,0,9,34,34,28,1
Style: Document,DejaVu Sans,12,&H00171A1C,&H00171A1C,&H00E6DDC8,&H00E6DDC8,-1,0,0,0,100,100,1.2,0,3,0,0,9,34,34,28,1
Style: Concept,DejaVu Sans,12,&H00E6DDC8,&H00E6DDC8,&H003552A5,&H903552A5,-1,0,0,0,100,100,1.2,0,3,0,0,9,34,34,28,1
Style: End,DejaVu Sans,27,&H00171A1C,&H00171A1C,&H70F3EBDD,&H00E6DDC8,-1,0,0,0,100,100,.8,0,1,1,0,5,70,70,70,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''

ev=[]
for p in caps:
    if p['e']<=CUT: continue
    ev.append((90,max(CUT,p['s']),p['e'],'Cap',esc(p.get('text',''))))

chapter_titles={
 'WHEN THE ROAD ENDS':'WHEN THE ROAD ENDS','THE ELECTRIC WHEEL':'THE ELECTRIC WHEEL','BIGGER AND BIGGER':'BIGGER AND BIGGER',
 'THE 572-FOOT MACHINE':'THE 572-FOOT MACHINE','HOW DO YOU DRIVE 572 FEET?':'HOW DO YOU DRIVE 572 FEET?',
 'NUCLEAR — RETENTION BEAT':'THE NUCLEAR IDEA','YUMA':'YUMA','TEST RESULTS':'TEST RESULTS','IT WORKED':'IT WORKED',
 'DEFEATED BY THE SKY':'DEFEATED BY THE SKY','EPILOGUE — THE LAST CAR':'THE LAST CAR','ENDING / CTA':'AFTERMATH'
}
tag_text={
 'road_end':'ROAD ENDS HERE','road_gap':'NO PREPARED ROAD','solution':'ROADLESS FREIGHT','map_isolation':'DISTANCE • WEATHER • NO ROADS',
 'electric_powertrain':'GAS TURBINE  →  GENERATOR','electric_distribution':'ELECTRICAL POWER THROUGH THE TRAIN','wheel_motor':'POWER AT THE WHEEL',
 'scale_572':'572 FT  /  174 M','wheels_54':'54 DRIVEN WHEELS','human_scale':'PEOPLE FOR SCALE',
 'mechanical_detail':'ARTICULATION / POWER HARDWARE','scale_geometry':'572-FOOT GEOMETRY','crew_scale':'CREW / CONTROL ENVIRONMENT',
 'range_context':'RANGE IS A GEOGRAPHY PROBLEM','operation':'WORKING LOGISTICS','closer_follow':'REAR UNITS FOLLOW CLOSER TO THE LEAD PATH',
 'distributed_traction':'POWERED WHEELS ACROSS THE TRAIN','nuclear_concept':'1961 CONCEPT — NOT THE TC-497 POWERPLANT',
 'nuclear_distribution':'CENTRAL POWER • LONG ELECTRICAL DISTRIBUTION','nuclear_unbuilt':'PROPOSED — NEVER BUILT',
 'chapter_nuclear_actual':'ACTUAL TC-497 • GAS TURBINES','actual_gas_turbines':'ACTUAL TC-497 • GAS TURBINES',
 'yuma_test':'YUMA PROVING GROUND','dune_setup':'NATURAL DUNE TEST','dune_limit':'~12 FT SLIP FACE • 28°',
 'test_mechanics':'TRACTION UNDER TEST','evidence_crop':'PROJECT OTTER • EVIDENCE','metric_speed':'~20 MPH',
 'metric_range':'~400-MILE RANGE','metric_cargo':'~150 TONS OF CARGO','metric_crew':'6 CREW',
 'operational_motion':'POWERED WHEELS IN MOTION','sky_shift':'THE LOGISTICS ANSWER CHANGED',
 'sky_payoff':'GROUND MACHINE → AIRLIFT','heli_operation':'HEAVY-LIFT AIR MOBILITY','ground_context':'THE SAME DISTANCE — A DIFFERENT METHOD',
 'legacy_detail':'WHAT SURVIVED','legacy_interior':'SURVIVING CONTROL CAR INTERIOR','aftermath':'THE TEST RANGE AFTER THE MACHINE',
 'archive_survivor':'SURVIVING CONTROL CAR'
}

prev_source=None
for sh in shots:
    s,e=sh['s'],sh['e']
    if sh.get('chapter_start'):
        ce=min(e,s+2.45)
        ev.append((42,s+.08,ce,'Kicker','HIDDEN INDUSTRIAL AMERICA'))
        ev.append((43,s+.18,ce,'Chapter',esc(chapter_titles.get(sh['chapter'],sh['chapter']))))
    tag=sh.get('tag','')
    if tag in tag_text and tag_text[tag]:
        te=min(e,s+3.0)
        style='Fact' if tag.startswith('metric_') or tag in {'scale_572','wheels_54','dune_limit'} else 'Tag'
        ev.append((50,s+.18,te,style,esc(tag_text[tag])))

    state=source_state(sh)
    if state!=prev_source or sh.get('chapter_start'):
        style='Document' if state=='DOCUMENT' else ('Concept' if state=='CONCEPT' else 'Source')
        detail=state
        if state=='DOCUMENT':
            if sh['code'].startswith('AR-OTTER'):
                detail=f"DOCUMENT • PROJECT OTTER • P.{sh.get('page',1)}"
            elif sh['code']=='AR-PATENT':
                detail='DOCUMENT • U.S. PATENT'
        ev.append((40,s+.08,min(e,s+1.8),style,detail))
    prev_source=state

final=next((x for x in shots if x.get('tag')=='final_plate'),None)
if final:
    ev.append((60,final['s']+.35,final['e']-.20,'End','HIDDEN INDUSTRIAL AMERICA\\N{\\fs35\\b1}THE MACHINE WORKED.  THE WORLD MOVED ON.'))

lines=[]
for layer,s,e,style,text in sorted(ev,key=lambda x:(x[1],x[0])):
    lines.append(f'Dialogue: {layer},{ts(s)},{ts(e)},{style},,0,0,0,,{text}')

with open(OUT,'w',encoding='utf-8',newline='\n') as f:
    f.write(head)
    f.write('\n'.join(lines))
    f.write('\n')

physical=sum(1 for x in OUT.read_text(encoding='utf-8').splitlines() if x.startswith('Dialogue:'))
if physical!=len(lines):
    raise RuntimeError(f'ASS physical Dialogue lines mismatch: {physical} != {len(lines)}')
(Path(os.environ['V4_WORK'])/'ASS_QA.json').write_text(json.dumps({'events_expected':len(lines),'physical_dialogue_lines':physical},indent=2),encoding='utf-8')
print('V4_ASS_EVENTS',len(lines),'PHYSICAL',physical)
