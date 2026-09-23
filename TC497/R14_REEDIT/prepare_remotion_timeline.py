#!/usr/bin/env python3
import argparse, csv, json, shutil
from pathlib import Path
from collections import Counter

FPS=30
CUT=82.6
END_SCREEN=1222.3
TOTAL=1236.533333

TAG_TEXT={
 'road_end':'ROAD ENDS HERE','road_gap':'NO PREPARED ROAD','solution':'ROADLESS FREIGHT','map_isolation':'DISTANCE • WEATHER • NO ROADS',
 'electric_powertrain':'GAS TURBINE → GENERATOR','electric_distribution':'ELECTRICAL POWER THROUGH THE TRAIN','wheel_motor':'POWER AT THE WHEEL',
 'scale_572':'572 FT / 174 M','wheels_54':'54 DRIVEN WHEELS','human_scale':'PEOPLE FOR SCALE',
 'mechanical_detail':'ARTICULATION / POWER HARDWARE','scale_geometry':'572-FOOT GEOMETRY','crew_scale':'CREW / CONTROL ENVIRONMENT',
 'range_context':'RANGE IS A GEOGRAPHY PROBLEM','operation':'WORKING LOGISTICS','closer_follow':'REAR UNITS FOLLOW THE LEAD PATH',
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
CHAPTER_TITLES={
 'WHEN THE ROAD ENDS':'WHEN THE ROAD ENDS','THE ELECTRIC WHEEL':'THE ELECTRIC WHEEL','BIGGER AND BIGGER':'BIGGER AND BIGGER',
 'THE 572-FOOT MACHINE':'THE 572-FOOT MACHINE','HOW DO YOU DRIVE 572 FEET?':'HOW DO YOU DRIVE 572 FEET?',
 'NUCLEAR — RETENTION BEAT':'THE NUCLEAR IDEA','YUMA':'YUMA','TEST RESULTS':'TEST RESULTS','IT WORKED':'IT WORKED',
 'DEFEATED BY THE SKY':'DEFEATED BY THE SKY','EPILOGUE — THE LAST CAR':'THE LAST CAR','ENDING / CTA':'AFTERMATH'
}

def source_label(code, chapter):
    if code.startswith('AR-OTTER') or code=='AR-PATENT':
        return 'DOCUMENT'
    if code.startswith('AR-'):
        return 'HISTORICAL SOURCE'
    if chapter=='NUCLEAR — RETENTION BEAT' and code in {'V4-NUKE','V2-NUKE'}:
        return 'CONCEPT'
    return 'AI RECONSTRUCTION'

def motion_for(x):
    label=source_label(x['code'],x['chapter'])
    dur=x['e']-x['s']
    if label in {'HISTORICAL SOURCE','DOCUMENT','CONCEPT'}:
        return 'static'
    if dur>=4.8 and not str(x.get('variant','')).startswith('detail'):
        return 'push'
    return 'static'

def load_words(path):
    out=[]
    with open(path,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            out.append({'s':float(r['start_sec']),'e':float(r['end_sec']),'w':r['word']})
    return out

def snap_boundaries(shots, words, max_shift=.28):
    ends=[w['e'] for w in words if CUT<w['e']<END_SCREEN]
    snapped=0
    by_ch={}
    for x in shots:
        by_ch.setdefault(x['chapter'],[]).append(x)
    result=[]
    for ch,arr in by_ch.items():
        arr=sorted([dict(x) for x in arr],key=lambda x:x['s'])
        for i in range(len(arr)-1):
            b=arr[i]['e']
            cand=min(ends,key=lambda z:abs(z-b)) if ends else b
            if abs(cand-b)<=max_shift:
                left=cand-arr[i]['s']; right=arr[i+1]['e']-cand
                if left>=2.4 and right>=2.4:
                    arr[i]['e']=round(cand,3)
                    arr[i+1]['s']=round(cand,3)
                    snapped+=1
        result.extend(arr)
    result.sort(key=lambda x:x['s'])
    return result,snapped

def phrase_captions(words):
    use=[w for w in words if w['e']>CUT and w['s']<END_SCREEN]
    phrases=[]; buf=[]
    for w in use:
        z=dict(w); z['s']=max(z['s'],CUT); z['e']=min(z['e'],END_SCREEN)
        buf.append(z)
        span=buf[-1]['e']-buf[0]['s']
        chars=sum(len(x['w'])+1 for x in buf)
        punct=str(w['w']).rstrip().endswith(('.', '!', '?', ';', ':'))
        comma=str(w['w']).rstrip().endswith(',')
        if len(buf)>=7 or chars>=48 or span>=2.45 or (punct and len(buf)>=3) or (comma and len(buf)>=5):
            phrases.append({'s':buf[0]['s'],'e':min(END_SCREEN,buf[-1]['e']+.08),'words':buf})
            buf=[]
    if buf:
        phrases.append({'s':buf[0]['s'],'e':min(END_SCREEN,buf[-1]['e']+.08),'words':buf})
    return phrases

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--shots',required=True)
    ap.add_argument('--state-dir',required=True)
    ap.add_argument('--word-csv',required=True)
    ap.add_argument('--override-dir',required=True)
    ap.add_argument('--public-dir',required=True)
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--captions',required=True)
    ap.add_argument('--report',required=True)
    a=ap.parse_args()

    shots=json.loads(Path(a.shots).read_text(encoding='utf-8'))
    words=load_words(a.word_csv)
    shots,snapped=snap_boundaries(shots,words)

    pub=Path(a.public_dir); rest=pub/'rest'; over=pub/'overrides'
    rest.mkdir(parents=True,exist_ok=True); over.mkdir(parents=True,exist_ok=True)
    statedir=Path(a.state_dir)

    out=[]
    for x in shots:
        idx=int(x['idx'])
        matches=list(statedir.glob(f'{idx:03d}_*.jpg'))
        if len(matches)!=1:
            raise RuntimeError(f'state image mismatch for {idx}: {matches}')
        dst=rest/f'{idx:03d}.jpg'
        shutil.copy2(matches[0],dst)
        label=source_label(x['code'],x['chapter'])
        out.append({
            **x,
            'file':f'rest/{dst.name}',
            'provenance':label,
            'motion':motion_for(x),
            'chapterTitle':CHAPTER_TITLES.get(x['chapter'],x['chapter']),
            'tagText':TAG_TEXT.get(x.get('tag',''),'')
        })

    od=Path(a.override_dir)
    specs=[
      ('electric_human_v6.png',215.356,221.464,'AI RECONSTRUCTION','static'),
      ('nuclear_concept_clean.png',709.241,717.165,'CONCEPT','static'),
      ('nuclear_unbuilt_clean.png',730.373,736.976,'CONCEPT','static'),
      ('WC-Y01.png',766.838,775.922,'AI RECONSTRUCTION','static'),
      ('WD-T03.png',815.287,822.857,'AI RECONSTRUCTION','static'),
      ('WC-D03.png',1020.122,1028.334,'AI RECONSTRUCTION','static'),
      ('WC-D05.png',1054.611,1062.822,'AI RECONSTRUCTION','static'),
      ('heavy_lift_logistics_clean.png',1079.245,1087.457,'AI RECONSTRUCTION','static'),
      ('ground_vs_air_clean.png',1107.164,1115.376,'AI RECONSTRUCTION','static'),
      ('survivor_detail_clean.png',1209.007,1215.477,'AI RECONSTRUCTION','static'),
      ('WB-N04.png',716.900,724.500,'AI RECONSTRUCTION','static'),
    ]
    overrides=[]
    for i,(name,s,e,label,motion) in enumerate(specs):
        src=od/name
        if not src.exists():
            raise FileNotFoundError(src)
        dst=over/name
        shutil.copy2(src,dst)
        overrides.append({'i':i,'file':f'overrides/{name}','s':s,'e':e,'provenance':label,'motion':motion})

    bad=[x for x in out if x['provenance']=='HISTORICAL SOURCE' and not x['code'].startswith('AR-')]
    bad += [x for x in out if x['provenance']=='AI RECONSTRUCTION' and x['code'].startswith('AR-')]
    bad += [x for x in overrides if x['provenance']=='HISTORICAL SOURCE']
    if bad:
        raise RuntimeError(f'provenance audit failed: {bad[:5]}')

    caps=phrase_captions(words)
    Path(a.captions).write_text(json.dumps(caps,ensure_ascii=False),encoding='utf-8')
    Path(a.manifest).write_text(json.dumps({'fps':FPS,'cut':CUT,'endScreen':END_SCREEN,'total':TOTAL,'shots':out,'overrides':overrides},ensure_ascii=False,indent=2),encoding='utf-8')

    counts=Counter(x['provenance'] for x in out)
    report={
      'shots':len(out),
      'snappedCutsToWordEnds':snapped,
      'provenanceCounts':dict(counts),
      'overrideCount':len(overrides),
      'historicalOnGenerated':0,
      'archiveAsReconstruction':0,
      'captions':len(caps),
      'status':'PASS'
    }
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
