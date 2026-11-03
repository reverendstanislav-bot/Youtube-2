from pathlib import Path
import json,xml.etree.ElementTree as E,copy,shutil,sys,os,time
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');m=json.loads((D/'R5_MANIFEST.json').read_text());rows={x['shot_id']:x for x in m['shots']};research=json.loads((D/'RESEARCH_SELECTS_RIGHTS_HOLD/RESEARCH_ARCHIVE_MANIFEST.json').read_text());exclude={'S135','S137','S151','S185'};research=[x for x in research if x['shot_id'] not in exclude];changes={x['shot_id']:x for x in research};root=E.parse(D/'VIDEO010_R5_REBUILD.xml');seq=root.getroot().find('sequence');name='VIDEO010_R6_FULL_RESEARCH_RIGHTS_HOLD';seq.find('name').text=name;seq.set('id','VIDEO010_R6_RIGHTS_HOLD');clips=seq.findall('./media/video/track/clipitem')
for row,c in zip(m['shots'],clips):
 sid=row['shot_id']
 if sid not in changes:continue
 x=changes[sid];path=Path(x['path']);row['path']=str(path);row['asset_type']='ARCHIVE_RESEARCH_RIGHTS_HOLD';row['rights']='HOLD';row['source_in_seconds']=x['source_in_seconds'];row['visual_action']=x['editorial_reason'];c.find('name').text=path.name
 still=c.find('stillframe')
 if still is not None:c.remove(still)
 f=c.find('file');f.find('name').text=path.name;f.find('pathurl').text=path.as_uri();f.find('duration').text=str(x['frames']);f.find('./media/video/duration').text=str(x['frames'])
# Fourth audio track is designed CC0 ambience. Existing voice, Foley, music remain separate.
au=seq.find('./media/audio');tr=copy.deepcopy(au.findall('track')[2]);au.append(tr);c=tr.find('clipitem');c.set('id','ambience_r6_clip');f=c.find('file');f.set('id','ambience_r6_file');src=D/'SFX/VIDEO010_DESIGNED_AMBIENCE_R6_48K_S24.wav';dest=W/'MEDIA'/src.name;shutil.copy2(src,dest);c.find('name').text=dest.name;f.find('name').text=dest.name;f.find('pathurl').text=dest.as_uri();xml=D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.xml';root.write(xml,encoding='utf-8',xml_declaration=True)
m.update(name=name,stage='RESEARCH_REVIEW_NOT_PUBLISHABLE',publication='BLOCKED_RIGHTS_AND_AV_LISTENING_HOLD',research_archive_shots=len(research),research_archive_seconds=sum(x['frames'] for x in research)/24);(D/'R6_MANIFEST.json').write_text(json.dumps(m,indent=2));(D/'RESEARCH_USED_SELECTS_R6.json').write_text(json.dumps(research,indent=2))
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();assert p.GetName()=='Yt2 Vid 10' and not p.IsRenderingInProgress();old=p.GetCurrentTimeline();assert old.GetName()=='VIDEO010_R5_REBUILD_ARCHIVE_MUSIC_V2';comps=D/'R5_NATIVE_BACKUP';comps.mkdir(exist_ok=True);backup=[];props={}
for i,item in enumerate(sorted(old.GetItemListInTrack('video',1),key=lambda a:a.GetStart())):
 sid=f'S{i+1:03}';pr=item.GetProperty();props[sid]={k:pr[k] for k in ['ZoomX','ZoomY','Pan','Tilt'] if k in pr}
 if item.GetFusionCompCount():
  path=comps/(sid+'.comp');assert item.ExportFusionComp(str(path),1);backup.append(sid)
assert r.GetProjectManager().SaveProject();pool=p.GetMediaPool();tl=pool.ImportTimelineFromFile(str(xml),{'timelineName':name,'importSourceClips':True});assert tl;assert p.SetCurrentTimeline(tl);items=sorted(tl.GetItemListInTrack('video',1),key=lambda a:a.GetStart());assert len(items)==194
newshots=set(changes)
for i,item in enumerate(items):
 sid=f'S{i+1:03}'
 if sid in newshots:continue
 if sid in backup:assert item.ImportFusionComp(str(comps/(sid+'.comp')))
 for k,v in props.get(sid,{}).items():assert item.SetProperty(k,v)
# Sparse source/date labels, editable, no permanent frames or backgrounds.
for sid,text in {'S001':'BAY OF WHALES / 1940','S030':'BYRD EXPEDITIONS / ARCHIVAL CONTEXT','S043':'EXPEDITION TERRAIN / 1939-1941','S071':'BOSTON / NOVEMBER 1939','S083':'BAY OF WHALES / 1940','S119':'SNOW CRUISER / EXPEDITION FOOTAGE','S124':'ARCHIVAL MOVEMENT / TRIAL DATE UNCONFIRMED','S165':'1956 MAP / REGIONAL CONTEXT'}.items():
 item=items[int(sid[1:])-1];assert item.GetFusionCompCount()==0,sid;c=item.AddFusionComp();c.SetPrefs({'Comp.FrameFormat.Width':1920,'Comp.FrameFormat.Height':1080});tools=list(c.GetToolList(False).values());base=next(t for t in tools if t.GetAttrs().get('TOOLS_RegID')=='MediaIn');out=next(t for t in tools if t.GetAttrs().get('TOOLS_RegID')=='MediaOut');t=c.AddTool('TextPlus');color=(.09,.14,.16) if sid=='S165' else (.96,.95,.91)
 for k,v in {'StyledText':text,'Font':'Consolas','Style':'Regular','Size':.025,'Center':[.5,.93],'Red1':color[0],'Green1':color[1],'Blue1':color[2],'GlobalOut':1000000,'UseFrameFormatSettings':1}.items():t.SetInput(k,v)
 merge=c.AddTool('Merge');merge.ConnectInput('Background',base);merge.ConnectInput('Foreground',t);out.ConnectInput('Input',merge)
for track,label in [(1,'HARRISON / LOCKED'),(2,'FOLEY / FREESOUND CC0'),(3,'MUSIC / 14 CUES / CC0'),(4,'DESIGNED AMBIENCE / CC0 / NOT ORIGINAL SOUND')]:tl.SetTrackName('audio',track,label)
assert all(int(a.GetEnd())==int(b.GetStart()) for a,b in zip(items,items[1:]));assert int(tl.GetEndFrame())-int(tl.GetStartFrame())==21310
for n in [1,3,4]:assert int(tl.GetItemListInTrack('audio',n)[0].GetDuration()) in ([20830] if n==1 else [21310]),n
assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.drp'))
(D/'R6_INSTALL_RECEIPT.json').write_text(json.dumps({'timeline':name,'video_items':194,'narrative_shots':193,'research_archive_shots':len(research),'research_archive_seconds':sum(x['frames'] for x in research)/24,'all_narrative_moving_shots':len(research)+5,'audio_tracks':4,'voice_source_unchanged':True,'end_screen_seconds':20,'rights':'HOLD_PRESERVED_NOT_A_RELEASE_MASTER','listening':'HOLD'},indent=2));print((D/'R6_INSTALL_RECEIPT.json').read_text(),flush=True)
