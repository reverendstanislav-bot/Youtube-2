#!/usr/bin/env python3
import argparse,json,re,statistics
from pathlib import Path
from collections import Counter,defaultdict

def st(fr): return fr/25.0
def fmt(s):
    m=int(s//60); return f"{m:02d}:{s-m*60:05.2f}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--shots',required=True)
    ap.add_argument('--out-json',required=True)
    ap.add_argument('--out-md',required=True)
    a=ap.parse_args()
    shots=json.loads(Path(a.shots).read_text(encoding='utf-8-sig',errors='replace'))
    rows=[]
    for i,s in enumerate(shots):
        r=dict(index=i,start=st(s['a']),end=st(s['b']),duration=(s['b']-s['a'])/25,
               scene=s.get('scene',''),source=s.get('source',''),asset=s.get('asset',''),
               variant=s.get('variant',''),motion=s.get('motion',''),kind=s.get('kind',''),
               explainer=s.get('explainer',''),phase=s.get('phase',0),
               section=s.get('section',''),chapter=s.get('chapter',''),text=s.get('text',''))
        rows.append(r)

    short=[r for r in rows if r['duration']<2.0]
    veryshort=[r for r in rows if r['duration']<1.5]
    same_adj=[]
    motion_flip=[]
    aba=[]
    quick_return=[]
    for i in range(len(rows)-1):
        x,y=rows[i],rows[i+1]
        if x['source']==y['source']:
            same_adj.append((i,i+1))
            if x['motion']!=y['motion'] or x['variant']!=y['variant']:
                motion_flip.append((i,i+1))
    for i in range(len(rows)-2):
        a1,b,a2=rows[i:i+3]
        if a1['source']==a2['source'] and a1['source']!=b['source']:
            aba.append((i,i+1,i+2))
    for i,r in enumerate(rows):
        for j in range(i+2,min(len(rows),i+7)):
            if rows[j]['source']==r['source']:
                quick_return.append((i,j))
                break

    # repeated scene/source density
    sources=Counter(r['source'] for r in rows)
    scenes=Counter(r['scene'] for r in rows)
    explainers=defaultdict(list)
    for r in rows:
        if r['explainer']:
            explainers[r['explainer']].append(r)

    # All intervals where lower overlays occupy subtitle-safe region.
    lower_overlay=[]
    for r in rows:
        reasons=[]
        if r['explainer']: reasons.append('explainer_cards_y847_968')
        if r['kind']=='reconstruction': reasons.append('reconstruction_label_y~1028')
        elif r['kind'] in ('archive','map'): reasons.append('historical_source_label_y~1028')
        if reasons:
            lower_overlay.append({'start':r['start'],'end':r['end'],'shot':r['index'],'scene':r['scene'],'reasons':reasons})

    data={
      'shot_count':len(rows),
      'duration':rows[-1]['end'] if rows else 0,
      'duration_median':statistics.median(r['duration'] for r in rows),
      'duration_min':min(r['duration'] for r in rows),
      'duration_max':max(r['duration'] for r in rows),
      'shots_under_2s':short,
      'shots_under_1_5s':veryshort,
      'adjacent_same_source':same_adj,
      'same_source_motion_or_variant_flip':motion_flip,
      'aba_returns':aba,
      'quick_source_returns_within_6_shots':quick_return,
      'most_repeated_sources':[{'source':k,'shots':v} for k,v in sources.most_common(30)],
      'most_repeated_scenes':scenes.most_common(30),
      'explainers':dict(explainers),
      'lower_overlay_intervals':lower_overlay,
      'shots':rows
    }
    Path(a.out_json).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

    md=['# Chicago V2 — full sequence / composition audit','',
        f'- Shots: **{len(rows)}**',
        f'- Duration: **{fmt(data["duration"])}**',
        f'- Median shot: **{data["duration_median"]:.2f}s**',
        f'- Minimum shot: **{data["duration_min"]:.2f}s**',
        f'- Shots <2s: **{len(short)}**; <1.5s: **{len(veryshort)}**',
        f'- Adjacent same-source boundaries: **{len(same_adj)}**',
        f'- Same-source motion/variant flips at adjacent boundaries: **{len(motion_flip)}**',
        f'- A→B→A source returns: **{len(aba)}**',
        f'- Source returns within 6 shots: **{len(quick_return)}**','',
        '## Confirmed subtitle-safe-area conflicts','',
        'V2 explainers draw three cards at source coordinates y=847..968 of 1080. At 540p review this becomes roughly y=424..484.',
        'The visible running subtitle style is bottom-aligned with MarginV=28 and can occupy roughly y=440..512 for two lines.',
        '**Therefore every explainer interval is a deterministic subtitle/graphic collision unless the caption is repositioned.**','',
        'Reconstruction/archive provenance labels are also drawn at y≈0.952*h (about 514px in the 540p review), inside the subtitle zone and need collision handling.','',
        '## Explainer intervals','']
    for name,xs in explainers.items():
        md.append(f'### {name}')
        for r in xs:
            md.append(f'- {fmt(r["start"])}–{fmt(r["end"])} | shot {r["index"]} | phase {r["phase"]} | {r["scene"]} | {r["motion"]}')
        md.append('')
    md += ['## Short shots (<2s)','']
    for r in short[:100]:
        md.append(f'- {fmt(r["start"])}–{fmt(r["end"])} ({r["duration"]:.2f}s) | {r["scene"]} | {r["variant"]} | {r["motion"]}')
    md += ['','## Adjacent same-source motion/variant flips','']
    for i,j in motion_flip[:100]:
        x,y=rows[i],rows[j]
        md.append(f'- {fmt(x["start"])}–{fmt(y["end"])} | {x["scene"]} {x["variant"]}/{x["motion"]} → {y["scene"]} {y["variant"]}/{y["motion"]}')
    md += ['','## A→B→A returns','']
    for i,j,k in aba[:100]:
        x,y,z=rows[i],rows[j],rows[k]
        md.append(f'- {fmt(x["start"])}–{fmt(z["end"])} | {x["scene"]} → {y["scene"]} → {z["scene"]}')
    Path(a.out_md).write_text('\n'.join(md)+'\n',encoding='utf-8')

if __name__=='__main__': main()
