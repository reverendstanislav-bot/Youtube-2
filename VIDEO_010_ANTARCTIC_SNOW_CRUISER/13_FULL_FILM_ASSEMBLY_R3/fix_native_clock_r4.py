from pathlib import Path
import os,sys,json
from PIL import Image,ImageStat
W=Path(r'C:\Users\KK\Movies\HIA_VIDEO010_FULL_FILM_R3');WORK=Path(r'C:\Users\KK\VIDEO010_ASSEMBLY_WORK')
sys.path.insert(0,r'C:\Users\KK\.codex\mcp\davinci-resolve');os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=r'C:\Users\KK\.codex\mcp\davinci-resolve\bridge-config.json'
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=20);pm=r.GetProjectManager();p=pm.GetCurrentProject();assert p.GetName()=='Yt2 Vid 10';assert not p.IsRenderingInProgress();tl=p.GetCurrentTimeline();items=tl.GetItemListInTrack('video',1);assert len(items)==194
m=json.loads((W/'VIDEO010_R5_1_193SHOTS_R3_REVIEW_MANIFEST.json').read_text());m['shots'][164]['original_source_path']=m['shots'][164]['path'];m['shots'][164]['path']=str(W/'MEDIA/CIA_ANTARCTICA_1956_HD_WORKING_R4.png');m['name']=tl.GetName();receipts=json.loads((W/'NATIVE_LAYER_RECEIPTS.json').read_text());reframes=json.loads((WORK/'REFRAME_PLAN_R3.json').read_text());clocks=[]
for rec in receipts:
 idx=int(rec['shot_id'][1:])-1;row=m['shots'][idx];item=items[idx];c=item.GetFusionCompByIndex(1);base=int(item.GetLeftOffset());d=int(item.GetDuration());nodes=list(c.GetToolList(False).values());by={t.GetAttrs().get('TOOLS_Name'):t for t in nodes};c.SetAttrs({'COMPN_GlobalEnd':base+d-1,'COMPN_RenderStart':base,'COMPN_RenderEnd':base+d-1});crop=reframes.get(rec['shot_id']) or reframes.get(row['asset_id']);specs=rec['labels']
 if rec['shot_id']=='S165':specs=[['1956 MAP / REGIONAL CONTEXT',.72,.90,.027,0]]
 for j,(text,x,y,size,delay) in enumerate(specs):
  if crop:
   cx,cy=crop['center'];s=crop['size'];x=cx+(x-.5)*s;y=1-cy+(y-.5)*s;size*=s
  im=Image.open(row['path']).convert('RGB');ww,hh=im.size;box=(int(max(0,x-.15)*ww),int(max(0,1-y-.04)*hh),int(min(1,x+.15)*ww),int(min(1,1-y+.04)*hh));luma=sum(ImageStat.Stat(im.crop(box)).mean)/3;ink=(.94,.92,.86) if luma<110 else (.11,.15,.18)
  txt=by['HIA_'+rec['shot_id']+'_LABEL_'+str(j+1)]
  for key,value in {'GlobalIn':0,'GlobalOut':1000000,'StyledText':text,'Font':'Consolas','Style':'Regular','Size':size,'Center':[x,y],'Red1':ink[0],'Green1':ink[1],'Blue1':ink[2],'Alpha1':1}.items():txt.SetInput(key,value)
  merge=by['HIA_'+rec['shot_id']+'_REVEAL_'+str(j+1)];merge.ConnectInput('Blend',None);assert merge.AddModifier('Blend','BezierSpline');last=d-1;end=min(last,delay+72) if rec['shot_id']=='S146' else last;keys={0:0,delay:0,min(delay+6,end):1,max(delay+7,end-8):1,end:0,last:0}
  for f,v in sorted(keys.items()):merge.SetInput('Blend',v,base+f)
 for t in nodes:
  reg=t.GetAttrs().get('TOOLS_RegID');name=t.GetAttrs().get('TOOLS_Name','')
  if reg=='Background':t.SetInput('GlobalIn',0);t.SetInput('GlobalOut',1000000)
  if name in ('HIA_LOAD_BAR_MASK_1','HIA_LOAD_BAR_MASK_2'):
   j=int(name[-1])-1;width,delay=[(.08,10),(.40,25)][j];t.ConnectInput('Width',None);assert t.AddModifier('Width','BezierSpline');t.SetInput('Width',.001,base+delay);t.SetInput('Width',width,base+delay+20)
 assert item.ExportFusionComp(str(W/'FUSION'/(rec['shot_id']+'_CLOCK_FIXED_R4.comp')),1)
 clocks.append({'shot':rec['shot_id'],'source_clock_base':base,'duration':d,'generator_global_out':1000000,'keys_shifted':True});print(json.dumps(clocks[-1]),flush=True)
(W/'NATIVE_CLOCK_FIX_R4.json').write_text(json.dumps(clocks,indent=2));(W/'VIDEO010_FULL_R4_MANIFEST.json').write_text(json.dumps(m,indent=2));assert pm.SaveProject();assert pm.ExportProject(p.GetName(),str(W/'VIDEO010_FULL_R4_HD_REVIEW.drp'))
assert p.SetCurrentRenderFormatAndCodec('mp4','H264');jobs=[]
for sid in ['S107','S146','S165']:
 i=items[int(sid[1:])-1];f=int(i.GetStart())+min(48,int(i.GetDuration())//2);assert p.SetRenderSettings({'TargetDir':str(W/'RENDERS'),'CustomName':'QC_FINAL_'+sid+'_R4','SelectAllFrames':False,'MarkIn':f,'MarkOut':f,'ExportVideo':True,'ExportAudio':False});jobs.append(p.AddRenderJob())
assert all(jobs);assert p.StartRendering(jobs);(W/'QC_FINAL_NATIVE_JOBS_R4.json').write_text(json.dumps(jobs));print(json.dumps({'qc_jobs':jobs}),flush=True)
