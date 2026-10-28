"""Reuse the proven native Resolve route with new names, sources and HD output."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'RESOLVE_R1'
for name in ['render_chapters.py','mux_proxy.py','qc_proxy.py','qc_motion_samples.py','finalize_native_checkpoint.py']:
    text=(OLD/name).read_text(encoding='utf-8')
    text=text.replace('HIA_VIDEO007_R1','HIA_VIDEO007_R2').replace('CAMP_CENTURY_R1','CAMP_CENTURY_R2').replace('VISUAL_R1_25FPS','VISUAL_R2_25FPS').replace('SHOT_PLAN_R1','SHOT_PLAN_R2').replace('720P25','1080P25')
    if name=='render_chapters.py':
        text=text.replace('FormatWidth=1280,FormatHeight=720','FormatWidth=1920,FormatHeight=1080')
        text=text.replace('import json,os,sys,time,subprocess','import json,os,sys,time,subprocess,hashlib')
        text=text.replace('log=[]',"log=[]\nsource_hash=hashlib.sha256((ROOT/'SHOT_PLAN_R2.json').read_bytes()+b''.join(p.read_bytes() for p in sorted((ROOT/'COMPS').glob('*.comp')))).hexdigest()")
        text=text.replace("if path.exists() and path.stat().st_size>10000:","sidecar=path.with_suffix('.source_sha256')\n    if path.exists() and path.stat().st_size>10000 and sidecar.exists() and sidecar.read_text().strip()==source_hash:")
        text=text.replace("print('COMPLETE',c['chapter'],path.stat().st_size,flush=True)","sidecar.write_text(source_hash+'\\n',encoding='ascii')\n    print('COMPLETE',c['chapter'],path.stat().st_size,flush=True)")
    elif name=='qc_proxy.py':text=text.replace("v[0]['width']==1280 and v[0]['height']==720","v[0]['width']==1920 and v[0]['height']==1080")
    elif name=='qc_motion_samples.py':text=text.replace("['M01','M03','M06','M08','M09','M11','M12','R07']","['Q01','Q02','Q03','Q07','Q11','G10','Q16','M08','M11','M12']")
    elif name=='finalize_native_checkpoint.py':text=text.replace('HIA_VIDEO007_CAMP_CENTURY_VISUAL_R1_CPU_FIXED.drp','HIA_VIDEO007_CAMP_CENTURY_VISUAL_R2.drp')
    (ROOT/name).write_text(text,encoding='utf-8')
(ROOT/'BEATS_AUDIO_LOCKED.json').write_bytes((OLD/'BEATS_AUDIO_LOCKED.json').read_bytes())
print(json.dumps({'route':'native Resolve chapter renders -> video copy concat + full locked WAV -> QC','output':'1920x1080 / 25 fps','audio':'unchanged','generated_video':False}))
