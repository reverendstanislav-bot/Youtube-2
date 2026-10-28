"""Wait for all native chapters, then mux, QC and export checkpoint once.
Does not start renders or modify picture/audio media.
"""
from pathlib import Path
import json, time, subprocess, sys
ROOT=Path(__file__).resolve().parent
MOVIE=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R2\HIA_VIDEO007_CAMP_CENTURY_R2_PROXY_1080P25.mp4')
deadline=time.monotonic()+7200
last=-1
while True:
    f=ROOT/'CHAPTER_RENDER_RESULTS.json'
    try:rows=json.loads(f.read_text()) if f.exists() else []
    except json.JSONDecodeError:rows=[]
    if len(rows)!=last:
        print('VERIFIED_NATIVE_CHAPTERS',len(rows),flush=True);last=len(rows)
    if len(rows)==8 and sum(r['frames'] for r in rows)==27368:
        break
    if time.monotonic()>deadline:raise TimeoutError('Native chapters incomplete after two hours; no partial master delivered')
    time.sleep(10)
for name,args in [('mux_proxy.py',[]),('qc_proxy.py',[str(MOVIE)]),('qc_motion_samples.py',[str(MOVIE)]),('finalize_native_checkpoint.py',[])]:
    print('STAGE',name,flush=True)
    subprocess.run([sys.executable,str(ROOT/name),*args],check=True)
    if name=='qc_proxy.py':
        qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text())
        assert qc['technical_checks_pass'],qc
scan=ROOT/'QC/FULL_DECODE_AND_BLACK_SCAN.log'
if scan.exists():scan.write_text('\n'.join(x.rstrip() for x in scan.read_text().splitlines()).rstrip()+'\n',encoding='utf-8')
print('FULL_R2_TECHNICAL_QC_COMPLETE_OWNER_REVIEW_PENDING',flush=True)
