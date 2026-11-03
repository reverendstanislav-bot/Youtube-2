from pathlib import Path
import json,sys,os,time,subprocess,hashlib,traceback
from PIL import Image,ImageStat
ROOT=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 10'); Q=ROOT/'IMAGEGEN_FULL_FILM_R2'; W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3'); WORK=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK')
STATE=W/'FULL_FILM_STATE.json'
def state(stage,**kw):
 x={'stage':stage,'updated':time.strftime('%Y-%m-%dT%H:%M:%S'),**kw};STATE.write_text(json.dumps(x,indent=2));print(json.dumps(x),flush=True)
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,p.stderr[-3000:];return p.stdout

def native_layers(tl,manifest):
 items=tl.GetItemListInTrack('video',1);assert len(items)==194,len(items)
 rows=manifest['shots'];receipt=[];compdir=W/'FUSION';compdir.mkdir(exist_ok=True)
 reframes=json.loads((WORK/'REFRAME_PLAN_R3.json').read_text());crop_receipts=[]
 # These are local readable annotations, not opaque replacement cards.
 plan={
 'S001':[('ANTARCTICA / 1940',.19,.91,.030,0)],
 'S007':[('A MOVING RESEARCH BASE',.27,.92,.031,0)],
 'S017':[('ANTARCTIC WINTER / 1934',.27,.92,.031,0)],
 'S033':[('CHICAGO / 1939',.22,.92,.030,0)],
 'S044':[('PROPOSED CROSSING',.25,.92,.032,0),('FRONT WHEELS RETRACT',.25,.86,.026,10)],
 'S045':[('PROPOSED CROSSING',.25,.92,.032,0),('REAR WHEELS RETRACT',.25,.86,.026,10)],
 'S047':[('15 FT / PROPOSED DESIGN',.30,.92,.032,0),('NOT A DEMONSTRATED ANTARCTIC CROSSING',.34,.86,.023,10)],
 'S064':[('GOMER, OHIO / 1939',.25,.92,.030,0)],
 'S087':[('BAY OF WHALES / 1940',.29,.91,.030,0)],
 'S105':[('1955 ENGINEERING REPORT',.30,.92,.032,0),('RETROSPECTIVE ANALYSIS',.30,.86,.025,10)],
 'S107':[('GULF MARSH BUGGY',.28,.93,.027,0),('~3,500 LB / WHEEL',.28,.875,.033,8),('SNOW CRUISER',.73,.93,.027,0),('~17,500 LB / WHEEL',.73,.875,.033,20)],
 'S118':[('REAR: CHAINS',.24,.92,.030,0),('FRONT: SPARE TIRES',.75,.92,.030,16)],
 'S120':[('PRESSURE VALUE: UNCERTAIN',.31,.92,.030,0)],
 'S133':[('HYDRAULIC LINES BLOCKED',.32,.92,.030,0)],
 'S154':[('1947 / WAR DEPARTMENT REPORT',.35,.93,.028,0)],
 'S157':[('1947 / ROOF LEVEL WITH SNOW',.35,.93,.028,0)],
 'S160':[('NO VERIFIED RESTART',.29,.92,.031,0)],
 'S162':[('JANUARY 1958',.22,.92,.032,0)],
 'S171':[('1957-1962',.25,.92,.039,0),('INFERRED CALVING INTERVAL',.29,.855,.025,10)],
 'S172':[('INFERENCE / NOT A WITNESSED EVENT',.38,.92,.027,0)],
 'S180':[('EXACT RESTING PLACE UNKNOWN',.36,.92,.030,0)],
 'S192':[('PREVIOUS STORY / CAMP CENTURY',.34,.92,.028,0)]}
 # Keep the full three-second Like inside one shot: previous +8s would straddle a cut.
 plan['S146']=[('Like this story',.80,.90,.027,8)]
 plan['S165']=[('1956 MAP / REGIONAL CONTEXT',.35,.92,.027,0)]
 plan['S176']=[('1963 / STATION REMAINS',.29,.92,.029,0),('NO VERIFIED CRUISER SIGHTING',.34,.86,.024,10)]
 for sid in ('S154','S157','S160'):plan.pop(sid,None) # Never cover the original document prose.
 for i,row in enumerate(rows):
  sid=row['shot_id'];specs=plan.get(sid);item=items[i];crop=reframes.get(sid) or reframes.get(row['asset_id'])
  if crop:
   cx,cy=crop['center'];scale=crop['size'];z=1/scale;props={'ZoomX':z,'ZoomY':z,'Pan':(.5-cx)*1920*z,'Tilt':(cy-.5)*1080*z}
   for key,value in props.items():assert item.SetProperty(key,value),(sid,key)
   crop_receipts.append({'shot_id':sid,'asset_id':row['asset_id'],**crop,'properties':props})
  if not specs:continue
  duration=int(item.GetDuration());assert duration==row['e']-row['s'],sid
  assert item.GetFusionCompCount()==0,'Do not duplicate native comps: '+sid
  c=item.AddFusionComp();assert c,sid;nodes=c.GetToolList(False);nodes=list(nodes.values()) if isinstance(nodes,dict) else nodes
  base=next(n for n in nodes if (n.GetAttrs().get('TOOLS_RegID')=='MediaIn' or n.GetAttrs().get('TOOLS_Name','').startswith('MediaIn')));out=next(n for n in nodes if (n.GetAttrs().get('TOOLS_RegID')=='MediaOut' or n.GetAttrs().get('TOOLS_Name','').startswith('MediaOut')))
  for j,(text,x,y,size,delay) in enumerate(specs):
   if crop:
    x=cx+(x-.5)*scale;y=1-cy+(y-.5)*scale;size*=scale
   sample=Image.open(row['path']).convert('RGB');ww,hh=sample.size;box=(int(max(0,x-.15)*ww),int(max(0,1-y-.04)*hh),int(min(1,x+.15)*ww),int(min(1,1-y+.04)*hh));luma=sum(ImageStat.Stat(sample.crop(box)).mean)/3;ink=(.94,.92,.86) if luma<110 else (.11,.15,.18)
   txt=c.AddTool('TextPlus',j*2+1,2);txt.SetAttrs({'TOOLS_Name':'HIA_'+sid+'_LABEL_'+str(j+1)})
   for key,val in {'StyledText':text,'Font':'Consolas','Style':'Regular','Size':size,'Center':[x,y],'Red1':ink[0],'Green1':ink[1],'Blue1':ink[2],'Alpha1':1,'UseFrameFormatSettings':1}.items():txt.SetInput(key,val)
   merge=c.AddTool('Merge',j*2+2,1);merge.SetAttrs({'TOOLS_Name':'HIA_'+sid+'_REVEAL_'+str(j+1)});merge.ConnectInput('Background',base);merge.ConnectInput('Foreground',txt);merge.AddModifier('Blend','BezierSpline')
   last=duration-1;end=min(last,delay+72) if sid=='S146' else last
   keys={0:0,delay:0,min(delay+6,end):1,max(delay+7,end-8):1,end:0,last:0}
   for f,v in sorted(keys.items()):merge.SetInput('Blend',v,f)
   base=merge
  if sid=='S107':
   # Both bars use one scale: 3500 vs 17500 lb/wheel, exactly 1:5.
   for j,(start,width,delay) in enumerate(((.24,.08,10),(.53,.40,25))):
    mask=c.AddTool('RectangleMask',10+j,4);mask.SetAttrs({'TOOLS_Name':'HIA_LOAD_BAR_MASK_'+str(j+1)});mask.SetInput('Center',[start+width/2,.82]);mask.SetInput('Height',.005);mask.SetInput('Width',width);mask.AddModifier('Width','BezierSpline');mask.SetInput('Width',.001,delay);mask.SetInput('Width',width,delay+20)
    bg=c.AddTool('Background',10+j,3)
    for k,v in {'Width':1672,'Height':941,'TopLeftRed':.22,'TopLeftGreen':.29,'TopLeftBlue':.26,'TopLeftAlpha':1}.items():bg.SetInput(k,v)
    bg.ConnectInput('EffectMask',mask);merge=c.AddTool('Merge',10+j,1);merge.ConnectInput('Background',base);merge.ConnectInput('Foreground',bg);base=merge
  out.ConnectInput('Input',base);path=compdir/(sid+'.comp');assert item.ExportFusionComp(str(path),1),sid
  receipt.append({'shot_id':sid,'paragraph_id':row['paragraph_id'],'start_frame':row['s'],'duration':duration,'labels':specs,'comp':str(path),'status':'NATIVE_CREATED_RENDER_REVIEW_PENDING'})
 (W/'REFRAME_RECEIPTS.json').write_text(json.dumps(crop_receipts,indent=2));(W/'NATIVE_LAYER_RECEIPTS.json').write_text(json.dumps(receipt,indent=2));return receipt

try:
 q=json.loads((Q/'GENERATION_QUEUE_ASSEMBLY_R4.json').read_text());lookup={x['asset_id']:x for x in q};overrides=json.loads((WORK/'ASSEMBLY_ASSET_OVERRIDES_R4.json').read_text());import csv
 needed={x['asset_id'] for x in csv.DictReader((Q/'SHOT_PLAN_193.csv').open(encoding='utf-8-sig')) if x['asset_type']=='NEW_IMAGE' and x['asset_id'] not in overrides}
 missing=[a for a in needed if lookup[a]['status']!='GENERATED'];assert not missing,missing
 for a in needed:
  x=lookup[a];src=Q/x['output'];assert hashlib.sha256(src.read_bytes()).hexdigest()==x['sha256'],a
 for x in overrides.values():assert Path(x['path']).is_file(),x
 n=sum(x['status']=='GENERATED' for x in q)
 state('READY_FROM_AVAILABLE_ASSETS',generated=n,selected_new_assets=len(needed),reuse_overrides=len(overrides),owner_instruction='Stop extra generation; assemble whole film now')
 state('BUILDING_FULL_XML',generated=n)
 result=json.loads(run([sys.executable,str(WORK/'build_film_xml_r3.py')]))
 sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
 from src.utils.resolve_bridge_client import connect
 r=connect(require_enabled=False,timeout=30);pm=r.GetProjectManager();p=pm.GetCurrentProject();assert p and p.GetName()=='Yt2 Vid 10';assert not p.IsRenderingInProgress(),'Resolve is busy; preserve other renders'
 assert float(p.GetSetting('timelineFrameRate'))==24
 pool=p.GetMediaPool();folder=pool.AddSubFolder(pool.GetRootFolder(),'VIDEO010_FULL_193_R3');pool.SetCurrentFolder(folder)
 state('IMPORTING_FULL_TIMELINE',xml=result['xml'])
 tl=pool.ImportTimelineFromFile(result['xml'],{'timelineName':result['name'],'importSourceClips':True});assert tl;assert p.SetCurrentTimeline(tl)
 assert int(tl.GetEndFrame())-int(tl.GetStartFrame())==21310
 items=tl.GetItemListInTrack('video',1);assert len(items)==194
 assert all(int(a.GetEnd())==int(b.GetStart()) for a,b in zip(items,items[1:]))
 assert len(tl.GetItemListInTrack('audio',1))==1
 assert pm.SaveProject();manifest=json.loads((W/(result['name']+'_MANIFEST.json')).read_text())
 state('NATIVE_EXPLANATORY_LAYERS',timeline=tl.GetName(),video_items=len(items));layers=native_layers(tl,manifest)
 tl.SetTrackName('video',1,'PICTURE / 193 NARRATIVE SHOTS + 20S END');tl.SetTrackName('audio',1,'HARRISON / LOCKED ORDER');tl.SetTrackName('audio',2,'FREESOUND / SELECTIVE FOLEY')
 assert pm.SaveProject();drp=W/'VIDEO010_FULL_193SHOTS_R3_REVIEW.drp';assert pm.ExportProject(p.GetName(),str(drp))
 # Explicit real output directory and codec prevent the previous invalid-path modal / APV fallback.
 assert p.SetCurrentRenderFormatAndCodec('mp4','H264');target=W/'RENDERS';target.mkdir(exist_ok=True)
 settings={'TargetDir':str(target),'CustomName':'VIDEO010_FULL_193SHOTS_R3_REVIEW','SelectAllFrames':True,'ExportVideo':True,'ExportAudio':True,'FormatWidth':1920,'FormatHeight':1080}
 assert p.SetRenderSettings(settings);job=p.AddRenderJob();assert job
 (W/'FULL_RENDER_JOB.json').write_text(json.dumps({'job':job,'settings':settings,'timeline':tl.GetName()},indent=2));assert p.StartRendering(job)
 state('RENDERING_FULL_REVIEW',job=job,seconds=21310/24,native_comps=len(layers))
 while p.IsRenderingInProgress():time.sleep(15)
 status=p.GetRenderJobStatus(job);assert status.get('JobStatus')=='Complete',status
 output=target/'VIDEO010_FULL_193SHOTS_R3_REVIEW.mp4';assert output.exists()
 state('TECHNICAL_QC_FULL_REVIEW',path=str(output))
 probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(output)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');assert v['codec_name']=='h264';assert (v['width'],v['height'])==(1920,1080);assert v['r_frame_rate']=='24/1';assert abs(float(probe['format']['duration'])-21310/24)<.2
 run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
 delivery=ROOT/'DELIVERY'/'FULL_FILM_R3_REVIEW';delivery.mkdir(parents=True,exist_ok=True)
 import shutil
 for source in [output,drp,W/'NATIVE_LAYER_RECEIPTS.json',W/(result['name']+'_MANIFEST.json')]:shutil.copy2(source,delivery/source.name)
 digest=hashlib.sha256(output.read_bytes()).hexdigest();report={'status':'FULL_REVIEW_RENDER_TECHNICAL_PASS_VISUAL_LISTENING_OWNER_HOLD','duration_seconds':float(probe['format']['duration']),'shots':193,'endscreen_seconds':20,'native_comps':len(layers),'sha256':digest,'output':str(delivery/output.name),'source_script':'R5.1 unchanged','not_verified':['Full real-time audiovisual review','Human listening / prefix artifacts','All generated geometry and historical continuity','Owner acceptance'],'rights':'No held archive inserted; no blanket rights clearance','publication':False}
 (delivery/'QC_STATUS.json').write_text(json.dumps(report,indent=2));(W/'QC_STATUS.json').write_text(json.dumps(report,indent=2));state('FULL_REVIEW_RENDER_READY',**report)
except Exception:
 state('ERROR_REQUIRES_REPAIR',error=traceback.format_exc());raise
