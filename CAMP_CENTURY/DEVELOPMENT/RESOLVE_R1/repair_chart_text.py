from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def clean(s):
    for _ in range(3):
        try:
            fixed=s.encode('cp1252').decode('utf-8')
            if fixed==s:break
            s=fixed
        except (UnicodeEncodeError,UnicodeDecodeError):break
    for n,v in [(0x2248,'APPROX.'),(0x2260,'IS NOT'),(0x2192,'/'),(0x2014,'/'),(0xb2,'2')]:s=s.replace(chr(n),v)
    return s
p=ROOT/'SHOT_PLAN_R1.json'
rows=json.loads(p.read_text(encoding='utf-8'))
for row in rows:
    if row.get('lines'):row['lines']=[clean(s) for s in row['lines']]
p.write_text(json.dumps(rows,indent=2,ensure_ascii=True),encoding='utf-8')
print([r['lines'] for r in rows if r['asset_id']=='C05'][:1])
