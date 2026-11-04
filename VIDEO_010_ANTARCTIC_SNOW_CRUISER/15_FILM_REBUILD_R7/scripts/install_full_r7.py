from pathlib import Path
import xml.etree.ElementTree as E,copy,json,sys,os,subprocess
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R7');P=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');L=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10');m=json.loads((P/'R6_1_MANIFEST.json').read_text());new={r['shot_id']:r for r in json.loads((D/'NEW_ARCHIVE_SELECTS_R7.json').read_text())};motion={r['shot_id']:r for r in json.loads((D/'MOTION_DESIGN_R7.json').read_text())};root=E.parse(P/'VIDEO010_R6_1_RESEARCH_RIGHTS_HOLD.xml');seq=root.getroot().find('sequence');name='VIDEO010_R7_DIRECTORS_FINAL_REVIEW';seq.find('name').text=name;clips=seq.findall('./media/video/track/clipitem');changes=[]
def setpath(c,path,duration,still=True,source_in=0,source_duration=None):
 path=Path(path);assert path.exists(),path;c.find('name').text=path.name;c.find('in').text=str(source_in);c.find('out').text=str(source_in+duration)
 flag=c.find('stillframe')
 if still and flag is None:E.SubElement(c,'stillframe').text='TRUE'
 if not still and flag is not None:c.remove(flag)
 c.find('rate/timebase').text='24';f=c.find('file');f.find('name').text=path.name;f.find('pathurl').text=path.as_uri();f.find('rate/timebase').text='24';d=86400 if still else source_duration or duration;f.find('duration').text=str(d);f.find('./media/video/duration').text=str(d)
for row,c in zip(m['shots'],clips):
 sid=row['shot_id'];n=row['e']-row['s'];path=Path(row['path']);kind=row['asset_type']
 if sid in new:path=Path(new[sid]['path']);kind='ACTUAL_ARCHIVE_RESEARCH_HOLD';row['archive_record']=new[sid]
 elif sid in motion:path=Path(motion[sid]['base']);kind='SOURCE_DRIVEN_NATIVE_SCENE';row['motion_record']=motion[sid]
 if sid in ['S192','S193']:
  path=D/'ASSETS/CAMP_PREVIOUS_STORY_MOVING_R7.mp4';setpath(c,path,n,False,0 if sid=='S192' else 88,178);kind='APPROVED_CAMP_MOVING_REFERENCE'
 else:setpath(c,path,n,path.suffix.lower() in ['.png','.jpg','.jpeg'])
 if str(path)!=row['path']:changes.append({'shot_id':sid,'old_path':row['path'],'new_path':str(path),'kind':kind})
 row['path']=str(path);row['asset_type']=kind
end=D/'ASSETS/VIDEO010_ENDSCREEN_CANON_20S_24FPS.mp4';setpath(clips[-1],end,480,False,0,480)
# Source/stems are retained for editing; the proper stereo printmaster is the only audible track.
au=seq.find('./media/audio');template=copy.deepcopy(au.findall('track')[0].find('clipitem'))
for t in list(au.findall('track')):au.remove(t)
def audio(path,duration,channels,idx):
 c=copy.deepcopy(template);c.set('id','r7_audio_'+str(idx));path=Path(path);c.find('name').text=path.name
 for key,val in [('duration',duration),('start',0),('end',duration),('in',0),('out',duration)]:c.find(key).text=str(val)
 f=c.find('file');f.set('id','r7_audio_file_'+str(idx));f.find('name').text=path.name;f.find('pathurl').text=path.as_uri();f.find('duration').text=str(duration);f.find('./media/audio/channelcount').text=str(channels);f.find('./media/audio/samplecharacteristics/samplerate').text='48000';tr=E.SubElement(au,'track');tr.append(c)
master=D/'MUSIC/VIDEO010_FILM_MIX_R7_48K_S24.wav';audio(master,21310,2,1);audio(L/'AUDIO/R5_1_MASTER_QC/VIDEO010_R5_1_HARRISON_MASTER_CANDIDATE_48K_S24.wav',20830,1,2);audio(D/'MUSIC/MUSIC_R7.wav',21310,2,3);audio(D/'MUSIC/FOLEY_R7.wav',21310,2,4)
xml=D/'VIDEO010_R7_FULL.xml';root.write(xml,encoding='utf-8',xml_declaration=True);m.update(name=name,owner_previous_version='R6.1 REJECTED',end_screen=str(end),end_screen_seconds=20,source_voice_unchanged=True,film_mix_processed=True,publication='HOLD_ARCHIVE_RIGHTS_AND_REVIEW',changes=changes);(D/'FILM_MANIFEST_R7.json').write_text(json.dumps(m,indent=2))
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json';from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();assert p.GetName()=='Yt2 Vid 10' and not p.IsRenderingInProgress();pool=p.GetMediaPool();tl=pool.ImportTimelineFromFile(str(xml),{'timelineName':name,'importSourceClips':True});assert tl and p.SetCurrentTimeline(tl);items=sorted(tl.GetItemListInTrack('video',1),key=lambda i:i.GetStart());assert len(items)==194;assert all(int(a.GetEnd())==int(b.GetStart()) for a,b in zip(items,items[1:]));assert int(tl.GetEndFrame())-int(tl.GetStartFrame())==21310
# Explicit stereo master track avoids a mono-track pan-law loss and prevents doubling with stems.
assert tl.DeleteTrack('audio',1);assert tl.AddTrack('audio','stereo');media=pool.ImportMedia([str(master)]);assert media;inserted=pool.AppendToTimeline([{'mediaPoolItem':media[0],'startFrame':0,'endFrame':21310,'recordFrame':int(tl.GetStartFrame()),'mediaType':2,'trackIndex':4}]);assert inserted and int(inserted[0].GetDuration())==21310
for n,label in [(1,'HARRISON / LOCKED SOURCE / MUTED STEM'),(2,'SCOTT BUCKLEY / MUSIC STEM / MUTED'),(3,'FREESOUND / SYNC FOLEY STEM / MUTED'),(4,'FILM MIX R7 / -16 LUFS / STEREO')]:
 tl.SetTrackName('audio',n,label);assert tl.SetTrackEnable('audio',n,n==4);assert tl.GetIsTrackEnabled('audio',n)==(n==4)
proof=['S044','S060','S105','S107','S154','S175'];loaded=[]
for sid in proof:
 if sid in motion and sid not in new:assert items[int(sid[1:])-1].ImportFusionComp(motion[sid]['comp']);loaded.append(sid)
assert r.GetProjectManager().SaveProject();(D/'INSTALL_R7.json').write_text(json.dumps({'timeline':name,'frames':21310,'picture_items':194,'printmaster_track':4,'only_master_enabled':True,'proof_scenes_imported':loaded,'all_native_scenes_pending':True,'end_screen':str(end),'archive_rights':'HOLD_RESEARCH_ONLY'},indent=2));assert p.SetCurrentRenderFormatAndCodec('mp4','H264');jobs=[]
for sid in proof:
 item=items[int(sid[1:])-1];n=int(item.GetDuration());
 for off in [5,min(n-4,48)]:
  frame=int(item.GetStart())+off;custom=f'R7_PROOF_{sid}_{off}';assert p.SetRenderSettings({'TargetDir':str(D),'CustomName':custom,'SelectAllFrames':False,'MarkIn':frame,'MarkOut':frame,'ExportVideo':True,'ExportAudio':False,'FormatWidth':1920,'FormatHeight':1080});job=p.AddRenderJob();assert job;jobs.append({'job':job,'name':custom})
for sid,frame in [('END',int(items[-1].GetStart())+120),('INTRO',int(tl.GetStartFrame())+48)]:
 assert p.SetRenderSettings({'TargetDir':str(D),'CustomName':'R7_PROOF_'+sid,'SelectAllFrames':False,'MarkIn':frame,'MarkOut':frame,'ExportVideo':True,'ExportAudio':False});job=p.AddRenderJob();jobs.append({'job':job,'name':'R7_PROOF_'+sid})
assert p.StartRendering([j['job'] for j in jobs]);(D/'PROOF_JOBS.json').write_text(json.dumps(jobs,indent=2));print(json.dumps({'timeline':name,'proof_jobs':len(jobs),'new_archive_clips':len(new),'native_scene_packages':len(motion),'end_screen':'REAL_CHANNEL_END_CARD'}),flush=True)
