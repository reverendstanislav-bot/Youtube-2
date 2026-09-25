#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'FINAL_ASSET_LOCK'/'FINAL_116_BEAT_ASSET_LOCK_V1.csv'
OUT=ROOT/'src'/'timeline.json'
FPS=25
END=1426.4

def sec(t):
    h,m,s=t.split(':')
    return int(h)*3600+int(m)*60+float(s)

rows=list(csv.DictReader(SOURCE.open(encoding='utf-8')))
timeline=[]
for i,r in enumerate(rows,1):
    start=sec(r['start'])
    end=sec(rows[i]['start']) if i<len(rows) else END
    timeline.append({
        'i':i,
        'beat':r['beat'].replace('BM-',''),
        'start':start,
        'end':end,
        'startFrame':round(start*FPS),
        'endFrame':round(end*FPS),
        'asset':r['asset_id'],
        'class':r['final_class'],
        'provenance':r['provenance'],
        'beatFile':f'beats/beat_{i:03d}.jpg',
    })
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(timeline,indent=2),encoding='utf-8')
assert len(timeline)==116
assert timeline[0]['startFrame']==0
assert timeline[-1]['endFrame']==35660
print(f'Wrote {OUT}: {len(timeline)} beats / {timeline[-1]["endFrame"]} frames')
