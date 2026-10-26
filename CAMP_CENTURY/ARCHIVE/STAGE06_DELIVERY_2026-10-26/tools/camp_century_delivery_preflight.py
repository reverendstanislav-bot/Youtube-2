import csv,json,subprocess,hashlib
from pathlib import Path
R=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007');A=R/'CAMP_CENTURY/ARCHIVE';M=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+str(R).replace('\\','/'),'-C',str(R),*args])
identity=json.loads((M/'reports/SCRIPT_V4_IDENTITY.json').read_text())
for f in identity['files']:assert git('rev-parse','HEAD:'+f['path']).decode().strip()==f['git_blob_sha']
names=git('diff','--cached','--name-only','-z').decode().split('\0')
for n in filter(None,names):
 assert n.startswith('CAMP_CENTURY/ARCHIVE/STAGE06_'),n
 assert Path(n).suffix.lower() not in ['.mp4','.mpeg','.mpg','.wav','.part','.bin','.npy','.pyc'],n
 assert '__pycache__' not in n
rows=list(csv.DictReader((A/'STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig',newline='')))
assert len(rows)==78
q={r['scene_id']:r for r in json.loads((M/'reports/CLIP_TECHNICAL_QC.json').read_text())}
for r in rows:
 p=Path(r['cut_filename']);assert p.is_file() and p.stat().st_size==q[r['scene_id']]['size_bytes']
 assert r['cut_sha256']==q[r['scene_id']]['sha256'] and r['source_sha256']
 assert (A/r['rights_receipt']).is_file(),r['rights_receipt']
 assert r['audio_status']=='AUDIO_TIMING_HOLD' and not r['audio_start_sec'] and not r['audio_end_sec']
 assert 5<=float(r['cut_seconds'])<=20
total=sum(float(r['cut_seconds']) for r in rows)
assert abs(total-798.697902)<0.001
assert len(list((M/'clips').glob('*.mp4')))==78
report=json.loads((A/'STAGE06_DELIVERY_2026-10-26/STAGE06_FINAL_QC_REPORT.json').read_text())
assert report['clip_count']==78 and len(report['coverage'])==8 and report['coverage'][-1]['unique_minutes']==0
assert len(list(csv.DictReader((A/'STAGE06_DELIVERY_2026-10-26/STAGE06_ALL_32_V4_BEATS_COVERAGE.csv').open(encoding='utf-8-sig',newline=''))))==32
print('DELIVERY_PREFLIGHT_PASS:78 physical MP4;7 source records;8 chapters;32 beats;V4 unchanged;all rights receipt links resolve;no movie binaries staged;coverage honestly HOLD.')
