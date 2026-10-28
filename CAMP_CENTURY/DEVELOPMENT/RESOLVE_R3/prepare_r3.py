"""Reuse the owner's named eight-motion reference. No image/video generation.
Existing silent motion tests are native Resolve media, not newly redesigned art.
"""
from pathlib import Path
import json,csv,hashlib,subprocess,re,copy,importlib.util,shutil
ROOT=Path(__file__).resolve().parent;PREV=ROOT.parent/'RESOLVE_R2'
G=ROOT.parents[1]/'GRAPHICS/STAGE07_MOTION_READY_R1'
for d in ['ASSETS','COMPS','QC']: (ROOT/d).mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('helpers',ROOT.parent/'RESOLVE_R1/build_fusion.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
old=json.loads((PREV/'SHOT_PLAN_R2.json').read_text());by={x['shot_id']:x for x in old}
bank={r['scene_id']:r for r in csv.DictReader(Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\reports\STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig'))}
def run(cmd):return subprocess.run(cmd,check=True,capture_output=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def archive(aid,start,end,origin='S001'):
    r=bank[aid];src=Path(r['cut_filename']);assert sha(src)==r['cut_sha256']
    dest=ROOT/'ASSETS'/f'{aid}_25FPS.mp4'
    if not dest.exists():run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-vf','fps=25,scale=640:480,setsar=1','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p',str(dest)])
    s=copy.deepcopy(by[origin]);s.update(asset_id=aid,path=str(dest),kind='REAL_ARCHIVE_MOTION',start_frame=start,end_frame=end,duration_frames=end-start,source=r['source_url'],locator=r['source_in_definition'],rights=r['rights_status'],title=r['actual_shot_description'],original_source=r,source_sha256=r['source_sha256'],selected_clip_sha256=r['cut_sha256'],conformed_sha256=sha(dest),source_trim_frames_25fps=[0,end-start],r2_origin=None)
    return s
def art(origin,start=None,end=None):
    s=copy.deepcopy(by[origin]);s['r2_origin']=origin
    if start is not None:s['start_frame']=start
    if end is not None:s['end_frame']=end
    s['duration_frames']=s['end_frame']-s['start_frame'];return s
def demo(mid,start,end,origin):
    s=art(origin,start,end);s.update(asset_id=mid,path=str(G/'preview'/f'{mid}_MOTION_DEMO.mp4'),kind='EXISTING_REFERENCE_MOTION',source=str(G/'preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4'),locator=mid+' original 8-second scene; existing deterministic motion, no new video generation',edit_reason='Restore the exact motion scene named by the owner, at the relevant narration')
    return s
# Real action opens the film. Reference M03 intrusion begins ~10.72s at "ceiling".
plan=[archive('CC07-C027',0,188),demo('M03',188,388,'S001'),demo('M01',388,588,'S003'),art('S051',588,664),art('S004',664,836),art('S005',836,1228),archive('CC07-C017',1228,1405),art('S006',1405,1556)]
for s in old:
    if s['start_frame']<1556:continue
    s=art(s['shot_id'])
    if s['shot_id']=='S032':s=demo('M02',s['start_frame'],s['start_frame']+200,'S032')
    elif s['shot_id']=='S033':s=art('S033',by['S032']['start_frame']+200)
    elif s['shot_id']=='S053':s=demo('M04',s['start_frame'],s['end_frame'],'S053')
    elif s['shot_id']=='S081':s=demo('M03',s['start_frame'],s['end_frame'],'S081')
    elif s['shot_id'] in ['S007','S090']:s=demo('M07',s['start_frame'],s['end_frame'],s['shot_id'])
    elif s['shot_id']=='S115':s=demo('M05',s['start_frame'],s['end_frame'],'S115')
    elif s['shot_id']=='S121':s=demo('M06',s['start_frame'],s['start_frame']+200,'S121')
    elif s['shot_id']=='S122':s=art('S122',by['S121']['start_frame']+200)
    elif s['shot_id']=='S123':
        replacement=art('S103',s['start_frame'],s['end_frame']);replacement['beat_id']=s['beat_id'];replacement['chapter']=s['chapter'];replacement['voice_cue']=s['voice_cue'];replacement['edit_reason']='Buried remains, not a second identical aircraft pass';s=replacement
    elif s['shot_id']=='S131':s=demo('M08',s['start_frame'],s['end_frame'],'S131')
    plan.append(s)
# Merge adjacent identical stills: one continuous explanatory view, no camera reset.
merged=[]
for s in plan:
    if merged and s['kind'].startswith('GENERATED') and merged[-1]['asset_id']==s['asset_id'] and merged[-1]['kind']==s['kind'] and merged[-1]['end_frame']==s['start_frame']:
        merged[-1]['end_frame']=s['end_frame'];merged[-1]['duration_frames']=merged[-1]['end_frame']-merged[-1]['start_frame'];merged[-1].setdefault('combined_r2_subcues',[]).append(s.get('r2_origin'));continue
    merged.append(s)
plan=merged
endsrc=Path(r'C:\Users\KK\Youtube-2-PROJECT_PLUTO-VIDEO006\PROJECT_PLUTO\RESOLVE_WORK\R23\R23_ENDSCREEN_18S_PREVIEW.mp4')
enddst=ROOT/'ASSETS/HIA_CLEAN_PREVIOUS_ENDSCREEN_18S.mp4'
if not enddst.exists():run(['ffmpeg','-v','error','-y','-ss','2','-i',str(endsrc),'-an','-vf','tpad=stop_mode=clone:stop_duration=2','-t','18','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',str(enddst)])
plan.append(dict(asset_id='HIA_PREVIOUS_ENDSCREEN',path=str(enddst),kind='CHANNEL_ENDSCREEN',start_frame=27368,end_frame=27818,duration_frames=450,chapter='ENDSCREEN',beat_id='AFTER_LOCKED_NARRATION',source=str(endsrc),rights='Channel-owned previous-video endscreen design reused unchanged',source_sha256=sha(endsrc),source_trim='2.00–18.00 sec plus 2-second clean final-frame hold; excludes old film dissolve',edit_reason='18-second existing channel endscreen after narration; locked WAV untouched'))
out=[];motion=[]
for s in plan:
    # Preserve actual reference playback cadence. Longer slots hold its final state,
    # never stretch 25fps motion into a low-frame-rate slow animation.
    if s['kind']=='EXISTING_REFERENCE_MOTION' and s['duration_frames']>200:
        tail=copy.deepcopy(s);tail['start_frame']+=200;tail['duration_frames']-=200
        s=copy.deepcopy(s);s['end_frame']=s['start_frame']+200;s['duration_frames']=200
        png=ROOT/'ASSETS'/f"{s['asset_id']}_REFERENCE_FINAL.png"
        if not png.exists():run(['ffmpeg','-v','error','-y','-i',s['path'],'-vf',r'select=eq(n\,199)','-frames:v','1',str(png)])
        tail.update(path=str(png),kind='REFERENCE_READING_HOLD',edit_reason='Hold the exact final animation frame for reading; no loop or replay')
        out.extend([s,tail])
    else:out.append(s)
plan=out
for s in plan:
    if s['start_frame']<1556:
        s['chapter']='CH01';s['beat_id']='CC07-S4-CH01-B01' if s['start_frame']<1228 else 'CC07-S4-CH01-B02'
        if s['asset_id']=='Q06':s['voice_cue']='nuclear power plant';s['edit_reason']='Brief plant cutaway at the spoken nuclear power plant; stable framing'
for i,s in enumerate(plan):
    s['shot_id']=f'R3-{i+1:03}';s['start_seconds']=s['start_frame']/25;s['end_seconds']=s['end_frame']/25
    if s['kind']=='EXISTING_REFERENCE_MOTION':motion.append(dict(shot=s['shot_id'],motion=s['asset_id'],timeline_in=s['start_seconds'],timeline_out=s['end_seconds'],source=s['path'],sha256=sha(s['path']),source_in_frame=0,source_out_exclusive=s['duration_frames'],cadence='Original 25fps, no retime or loop'))
    if s['kind'] in ['REAL_ARCHIVE_MOTION','EXISTING_REFERENCE_MOTION','CHANNEL_ENDSCREEN']:continue
    n=s['duration_frames'];dst=ROOT/'COMPS'/f"{s['shot_id']}_{s['asset_id']}.comp"
    if s['kind']=='REFERENCE_READING_HOLD':
        tools=[f.background('Paper'),f.loader('ReferenceFinal',Path(s['path']),n-1),f.resize('ReferenceHD','ReferenceFinal',1920,1080),f.merge('ReadingHold','Paper','ReferenceHD'),'MediaOut1 = MediaOut { Inputs = { Input='+f.link('ReadingHold')+' } }'];f.write_comp(dst,tools,n-1)
    else:
        origin=by[s['r2_origin']];src=PREV/'COMPS'/f"{origin['shot_id']}_{origin['asset_id']}.comp";txt=src.read_text(encoding='utf-8')
        # All generic camera pushes are removed; marker and loupe layers survive.
        lines=[]
        for line in txt.splitlines():
            if line.startswith('MotivatedFocus ='):
                input_node=re.search(r'Input=Input \{ SourceOp = "([^"]+)"',line).group(1)
                line='MotivatedFocus = Transform { Inputs = { UseGPU=Input { Value=0 }, Input='+f.link(input_node)+', Size=Input { Value=1 }, Center='+f.point(.5,.5)+' } },'
            lines.append(line)
        txt='\n'.join(lines)
        offset=s['start_frame']-origin['start_frame']
        txt=re.sub(r'\btime\b',f'(time+({offset}))',txt)
        txt=re.sub(r'GlobalOut=Input \{ Value = \d+ \}',f'GlobalOut=Input {{ Value = {n-1} }}',txt)
        txt=re.sub(r'\["Clip1.ExtendLast"\]=Input \{ Value = \d+ \}',f'["Clip1.ExtendLast"]=Input {{ Value = {n} }}',txt)
        txt=re.sub(r'(GlobalRange|RenderRange) = \{ 0, \d+ \}',lambda m:m.group(1)+f' = {{ 0, {n-1} }}',txt)
        # Do not flash the old previous shot at the new editorial boundaries.
        txt=txt.replace('SourceOp = "MotivatedDissolve"','SourceOp = "MotivatedFocus"')
        dst.write_text(txt,encoding='utf-8')
    s['comp']=str(dst)
assert plan[0]['start_frame']==0 and plan[-1]['end_frame']==27818
for a,b in zip(plan,plan[1:]):assert a['end_frame']==b['start_frame'],(a['shot_id'],b['shot_id'])
(ROOT/'SHOT_PLAN_R3.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
cols=['shot_id','chapter','beat_id','asset_id','kind','start_frame','end_frame','duration_frames','start_seconds','end_seconds','voice_cue','edit_reason','path','source','locator','rights','comp','r2_origin','source_sha256']
with (ROOT/'SHOT_PLAN_R3.csv').open('w',encoding='utf-8-sig',newline='') as fp:w=csv.DictWriter(fp,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(plan)
(ROOT/'RESTORED_REFERENCE_MOTION.json').write_text(json.dumps(motion,indent=2),encoding='utf-8')
(ROOT/'REFERENCE_SOURCE.json').write_text(json.dumps(dict(file=str(G/'preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4'),sha256=sha(G/'preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4'),treatment='Reuse original existing eight motion scenes in Resolve; no new generation',audio='Locked WAV unchanged; 18-second silent endscreen appended after narration',owner_approval='PENDING'),indent=2),encoding='utf-8')
print('R3_PLAN_READY',len(plan),'shots',len(motion),'motion placements','27818 frames / 1112.72 seconds',flush=True)
