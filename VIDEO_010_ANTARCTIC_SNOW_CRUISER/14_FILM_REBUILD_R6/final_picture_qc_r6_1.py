from pathlib import Path
import json,xml.etree.ElementTree as E,sys,os,shutil,subprocess
D=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK\REBUILD_R5');W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');m=json.loads((D/'R6_MANIFEST.json').read_text());rows={x['shot_id']:x for x in m['shots']};original=json.loads((W/'VIDEO010_FULL_R4_MANIFEST.json').read_text());orig={x['shot_id']:x for x in original['shots']};changes={'S011':orig['S011']['path'],'S132':orig['S132']['path'],'S134':orig['S134']['path'],'S186':orig['S186']['path'],'S190':str(W/'MEDIA/PH08_1920px.jpg')};root=E.parse(D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.xml');seq=root.getroot().find('sequence');name='VIDEO010_R6_1_FULL_RESEARCH_RIGHTS_HOLD';seq.find('name').text=name
for row,c in zip(m['shots'],seq.findall('./media/video/track/clipitem')):
 sid=row['shot_id']
 if sid not in changes:continue
 src=Path(changes[sid]);assert src.exists(),src;row['path']=str(src);row['asset_type']='EXISTING_ARCHIVE' if sid=='S190' else 'NEW_IMAGE';row['asset_id']='PH08' if sid=='S190' else orig[sid]['asset_id'];row['rights']='INHERITED_PD_SOURCE' if sid=='S190' else 'EXISTING_EDITORIAL_RECONSTRUCTION';row['visual_action']='Genuine buried Cruiser photo as emotional callback' if sid=='S190' else orig[sid]['visual_action'];c.find('name').text=src.name
 if c.find('stillframe') is None:E.SubElement(c,'stillframe').text='TRUE'
 f=c.find('file');f.find('name').text=src.name;f.find('pathurl').text=src.as_uri();f.find('duration').text='86400';f.find('./media/video/duration').text='86400'
xml=D/'VIDEO010_R6_1_RESEARCH_RIGHTS_HOLD.xml';root.write(xml,encoding='utf-8',xml_declaration=True);m.update(name=name,research_archive_shots=23,research_archive_seconds=sum(x['frames'] for x in json.loads((D/'RESEARCH_USED_SELECTS_R6.json').read_text()) if x['shot_id'] not in changes)/24);(D/'R6_1_MANIFEST.json').write_text(json.dumps(m,indent=2));(D/'FINAL_PICTURE_QC_FIXES_R6_1.json').write_text(json.dumps(changes,indent=2))
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=25);p=r.GetProjectManager().GetCurrentProject();old=p.GetCurrentTimeline();assert old.GetName()=='VIDEO010_R6_FULL_RESEARCH_RIGHTS_HOLD' and not p.IsRenderingInProgress();backup=D/'FINAL_NATIVE_R6';backup.mkdir(exist_ok=True);comps={};props={}
for j,item in enumerate(sorted(old.GetItemListInTrack('video',1),key=lambda i:i.GetStart())):
 sid=f'S{j+1:03}';pr=item.GetProperty();props[sid]={k:pr[k] for k in ['ZoomX','ZoomY','Pan','Tilt'] if k in pr}
 if item.GetFusionCompCount():
  dest=backup/(sid+'.comp');assert item.ExportFusionComp(str(dest),1);comps[sid]=dest
assert r.GetProjectManager().SaveProject();pool=p.GetMediaPool();tl=pool.ImportTimelineFromFile(str(xml),{'timelineName':name,'importSourceClips':True});assert tl and p.SetCurrentTimeline(tl);items=sorted(tl.GetItemListInTrack('video',1),key=lambda i:i.GetStart());assert len(items)==194
for j,item in enumerate(items):
 sid=f'S{j+1:03}'
 if sid in changes:continue
 if sid in comps:assert item.ImportFusionComp(str(comps[sid]))
 for k,v in props.get(sid,{}).items():assert item.SetProperty(k,v)
assert all(int(a.GetEnd())==int(b.GetStart()) for a,b in zip(items,items[1:]));assert int(tl.GetEndFrame())-int(tl.GetStartFrame())==21310
for n,label in [(1,'HARRISON / LOCKED'),(2,'FOLEY / CC0'),(3,'MUSIC / 14 CUES / CC0'),(4,'DESIGNED AMBIENCE / CC0')]:tl.SetTrackName('audio',n,label)
assert r.GetProjectManager().SaveProject();assert r.GetProjectManager().ExportProject(p.GetName(),str(D/'VIDEO010_R6_RESEARCH_RIGHTS_HOLD.drp'))
# Preserve prior research binary in staging; canonical output is replaced only after successful technical verification.
f=W/'RENDERS/VIDEO010_R6_RESEARCH_RIGHTS_HOLD.mp4';previous=W/'RENDERS/VIDEO010_R6_PRE_PICTURE_QC.mp4'
if f.exists() and not previous.exists():shutil.move(str(f),str(previous))
rec=json.loads((D/'R6_INSTALL_RECEIPT.json').read_text());rec.update(timeline=name,research_archive_shots=23,research_archive_seconds=m['research_archive_seconds'],all_narrative_moving_shots=28,picture_qc_fixes=list(changes));(D/'R6_INSTALL_RECEIPT.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec),flush=True)
