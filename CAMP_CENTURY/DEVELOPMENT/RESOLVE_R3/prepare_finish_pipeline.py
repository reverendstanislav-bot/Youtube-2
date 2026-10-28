"""Adapt the proven native renderer/QC to R3. Does not change picture sources."""
from pathlib import Path
import json,csv,shutil
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'RESOLVE_R2'
p=json.loads((ROOT/'SHOT_PLAN_R3.json').read_text())
for s in p:
    if s['start_frame']<1556:
        s['chapter']='CH01';s['beat_id']='CC07-S4-CH01-B01' if s['start_frame']<1228 else 'CC07-S4-CH01-B02'
        if s['asset_id']=='Q06':s['voice_cue']='nuclear power plant';s['edit_reason']='Brief plant cutaway at the spoken nuclear power plant; stable framing'
(ROOT/'SHOT_PLAN_R3.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
with (ROOT/'SHOT_PLAN_R3.csv').open(encoding='utf-8-sig') as fp:cols=next(csv.reader(fp))
with (ROOT/'SHOT_PLAN_R3.csv').open('w',encoding='utf-8-sig',newline='') as fp:w=csv.DictWriter(fp,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(p)
shutil.copy2(OLD/'BEATS_AUDIO_LOCKED.json',ROOT/'BEATS_AUDIO_LOCKED.json')
for name in ['render_chapters.py','mux_proxy.py','qc_proxy.py']:
    txt=(OLD/name).read_text(encoding='utf-8').replace('RESOLVE_R2','RESOLVE_R3').replace('R2','R3').replace('27368','27818').replace('1094.72','1112.72')
    if name=='render_chapters.py':
        txt=txt.replace('assert len(chapters)==8','assert len(chapters)==9').replace('ALL_8_NATIVE_CHAPTERS_COMPLETE','ALL_9_NATIVE_CHAPTERS_COMPLETE')
    elif name=='mux_proxy.py':
        txt=txt.replace('default=8','default=9').replace('args.chapters==8','args.chapters==9').replace("'-ac','1','-t'","'-ac','1','-af','apad','-t'")
    else:
        # Compare only the entire original narration; appended silence is endscreen.
        txt=txt.replace("meaning='Proxy AAC signal comparison, not a bit-identical PCM claim'","meaning='Full original narration compared; 18-second endscreen silence excluded from comparison; no bit-identical AAC claim'")
        txt=txt.replace("final_color_music_sfx='NOT_STARTED'","final_color_music_sfx='NOT_STARTED',endscreen_seconds=18,original_locked_audio_seconds=1094.72")
    (ROOT/name).write_text(txt,encoding='utf-8')
print('R3_NATIVE_9_PART_RENDER_AND_QC_PIPELINE_READY')
