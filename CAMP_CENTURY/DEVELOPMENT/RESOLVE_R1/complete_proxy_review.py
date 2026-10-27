"""Finish only after all eight actual native chapter exports exist."""
from pathlib import Path
import json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
deadline=time.monotonic()+1800
while True:
    try:
        rows=json.loads((ROOT/'CHAPTER_RENDER_RESULTS.json').read_text(encoding='utf-8'))
        ready=len(rows)==8 and sum(r['frames'] for r in rows)==27368
        ready=ready and all(Path(r['file']).is_file() for r in rows)
    except (OSError,ValueError):ready=False
    if ready:break
    if time.monotonic()>deadline:raise RuntimeError('All eight native chapters are not ready; no full proxy claim')
    time.sleep(5)
src=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R1\HIA_VIDEO007_CAMP_CENTURY_R1_PROXY_720P25.mp4')
for script,args in [('mux_proxy.py',[]),('qc_proxy.py',[str(src)]),('qc_motion_samples.py',[str(src)]),('finalize_native_checkpoint.py',[])]:
    print('RUNNING',script,flush=True)
    subprocess.run([sys.executable,str(ROOT/script),*args],check=True)
qc=json.loads((ROOT/'QC/PROXY_QC.json').read_text(encoding='utf-8'))
assert qc['technical_checks_pass'], 'Proxy exists but did not pass technical checks'
print('FULL_PROXY_TECHNICAL_CHECKS_COMPLETE',flush=True)
