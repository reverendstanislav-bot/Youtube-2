from pathlib import Path
import json
import re,math
from PIL import Image
ROOT=Path(__file__).resolve().parent
ROOT.mkdir(parents=True,exist_ok=True)
GRAPHICS=ROOT.parents[1]/'GRAPHICS'

def inp(v):
    if isinstance(v,str):return 'Input { Value = '+json.dumps(v,ensure_ascii=False)+' }'
    return 'Input { Value = '+str(v)+' }'
def link(name):return 'Input { SourceOp = "'+name+'", Source = "Output" }'
def masklink(name):return 'Input { SourceOp = "'+name+'", Source = "Mask" }'
def loader(name,path,end):
    return f'''{name} = Loader {{ Clips = {{ Clip {{ ID="Clip1", Filename={json.dumps(str(path).replace(chr(92),'/'))}, FormatID="PNGFormat", StartFrame=0, Length=1, Loop=1 }} }}, Inputs = {{ GlobalIn={inp(0)}, GlobalOut={inp(end)}, ["Clip1.ExtendFirst"]={inp(0)}, ["Clip1.ExtendLast"]={inp(end+1)}, ["Clip1.Loop"]={inp(1)} }} }}'''
def resize(name,source,w,h):return f'{name} = BetterResize {{ Inputs = {{ Width={inp(w)}, Height={inp(h)}, KeepAspect={inp(0)}, Input={link(source)} }} }}'
def write_comp(path,tools,end):
    body=',\n'.join(tools)
    body=re.sub(r'Inputs\s*=\s*\{','Inputs = { UseGPU = Input { Value = 0 },',body)
    path.write_text('{\nTools = ordered() {\n'+body+'\n},\nGlobalRange = { 0, '+str(end)+' }, RenderRange = { 0, '+str(end)+' }, CurrentTime = 0\n}\n',encoding='utf-8')

def expr(value):return 'Input { Expression = '+json.dumps(value)+' }'
def point(x,y):return f'Input {{ Value = {{{x},{y}}} }}'
def ease(a,b):
    q=f'min(1,max(0,(time-{a})/{max(1,b-a)}))'
    return f'({q}*{q}*(3-2*{q}))'
def merge(name,bg,fg,blend='1',center=None,mask=None,mode=None):
    fields=[f'Background={link(bg)}',f'Foreground={link(fg)}',f'Blend={expr(blend)}']
    if center:fields.append('Center='+expr(center))
    if mask:fields.append('EffectMask='+masklink(mask))
    if mode:fields.append('ApplyMode='+inp(mode))
    return name+' = Merge { Inputs = { '+','.join(fields)+' } }'
def background(name,color=(.972,.969,.948),alpha=1,mask=None):
    fields=[f'Width={inp(1920)}',f'Height={inp(1080)}',f'TopLeftRed={inp(color[0])}',f'TopLeftGreen={inp(color[1])}',f'TopLeftBlue={inp(color[2])}',f'TopLeftAlpha={inp(alpha)}']
    if mask:fields.append('EffectMask='+masklink(mask))
    return name+' = Background { Inputs = { '+','.join(fields)+' } }'
def rectangle(name,cx,cy,w,h):
    center=expr(f'Point({cx},{cy})')
    return f'{name} = RectangleMask {{ Inputs = {{ MaskWidth={inp(1920)},MaskHeight={inp(1080)}, Center={center}, Width={expr("max(0.0001,"+str(w)+")")}, Height={expr("max(0.0001,"+str(h)+")")}, SoftEdge={inp(.002)} }} }}'
def text(name,words,y,size=.043,color=(.12,.18,.21),x=.5):
    for a,b in [('≈','APPROX.'),('≠','IS NOT'),('→','/'),('—','/'),('²','2')]:words=words.replace(a,b)
    if len(words)>38:size=min(size,.040)
    return f'''{name} = TextPlus {{ Inputs = {{ Width={inp(1920)},Height={inp(1080)},UseFrameFormatSettings={inp(0)},Font={inp('Consolas')},Style={inp('Regular')},StyledText={inp(words)},Size={inp(size)},Center={point(x,y)},Red1={inp(color[0])},Green1={inp(color[1])},Blue1={inp(color[2])},HorizontalJustificationNew={inp(3)},VerticalJustificationNew={inp(3)} }} }}'''

def build_all():
    plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
    refs=json.loads((GRAPHICS/'STAGE07_GENERATION_PREP_R2/REFERENCE_REGISTER.json').read_text(encoding='utf-8-sig'))
    if isinstance(refs,dict):refs=refs.get('references',refs.get('items',[]))
    rmap={r['reference_id']:r for r in refs}
    focus=json.loads((GRAPHICS/'STAGE07_GENERATION_PREP_R2/data/DOCUMENT_FOCUS_TARGETS.json').read_text(encoding='utf-8-sig'))
    q=json.loads((GRAPHICS/'STAGE07_GENERATION_PREP_R2/ASSET_PRODUCTION_QUEUE.json').read_text(encoding='utf-8-sig'))
    drefs={}
    for r in q:
        if r['asset_id'].startswith('D'):
            for ref in r['reference_ids']:drefs.setdefault(ref,set()).add(r['asset_id'])
    folder=ROOT/'COMPS';folder.mkdir(exist_ok=True)
    manifest=[]
    for idx,s in enumerate(plan):
        if s['kind']=='REAL_ARCHIVE_MOTION':continue
        n=s['duration_frames'];end=n-1;aid=s['asset_id'];nodes=[background('Paper')];last='Paper';features=[]
        if s['kind']=='FACTUAL_NATIVE_GRAPHIC':
            for j,line in enumerate(s['lines']):
                tname=f'Text{j}';nodes.append(text(tname,line,[.71,.53,.36][j],[.035,.056,.028][j],(.12,.18,.21) if j!=1 else (.64,.34,.12)))
                # Qualifiers stay visible with their proposal numbers, never delayed.
                blend='1' if j==0 or aid.startswith('C05') else ease(j*7,min(j*7+20,max(j*7+5,n*.3)))
                mn=f'TextMerge{j}';nodes.append(merge(mn,last,tname,blend));last=mn
            p=ease(n*.2,n*.6);nodes.append(rectangle('AccentMask',f'.12+.38*{p}',.445,f'.76*{p}',.004));nodes.append(background('Accent',(.73,.40,.15),1,'AccentMask'));nodes.append(merge('AccentMerge',last,'Accent'));last='AccentMerge';features.append('native Text+ qualifiers and progressive accent')
        else:
            im=Image.open(s['path']);w,h=im.size
            margin=.92 if s['kind']=='PRIMARY_REFERENCE' else 1
            k=min(1920*margin/w,1080*margin/h);fw,fh=round(w*k),round(h*k)
            nodes.extend([loader('Base',s['path'],end),resize('BaseFit','Base',fw,fh),merge('BaseMerge','Paper','BaseFit')]);last='BaseMerge'
            if aid in ['M01','M02','M03','M04','M05','M07']:
                overlay=GRAPHICS/f'STAGE07_MOTION_READY_R1/overlays/{aid}_ACCENTS_ENDSTATE.png'
                nodes.extend([loader('Accents',overlay,end),resize('AccentsHD','Accents',1920,1080)])
                p=ease(n*.09,n*.75)
                if aid=='M05':nodes.append(rectangle('WriteOnMask',.5,f'1-.5*{p}',1,p))
                else:nodes.append(rectangle('WriteOnMask',f'.5*{p}',.5,p,1))
                nodes.append(merge('WriteOnMerge',last,'AccentsHD','1',mask='WriteOnMask'));last='WriteOnMerge';features.append('native animated write-on mask over local transparent accents')
            if aid in ['M06','M08','M09']:
                if aid=='M06':
                    f=GRAPHICS/'STAGE07_MOTION_READY_R1/assets/M06_AIRCRAFT.png';ow,oh=450,149
                    p=ease(n*.07,n*.85);center=f'Point(.24+.48*{p},.84)'
                elif aid=='M08':
                    f=GRAPHICS/'STAGE07_MOTION_READY_R1/assets/M08_MODULE.png';ow,oh=300,277
                    p=ease(n*.08,n*.65);center=f'Point(.50,.75+.12*{p})'
                    hook=f'(.75+.12*{p}+277/2160)'
                    nodes.append(rectangle('HoistCableMask',.5,f'(1+{hook})/2',.0008,f'1-{hook}'))
                    nodes.append(background('HoistCable',(.12,.18,.21),.85,'HoistCableMask'))
                    nodes.append(merge('HoistCableMerge',last,'HoistCable'));last='HoistCableMerge'
                else:
                    f=GRAPHICS/'STAGE07_MOTION_PEOPLE_R2/assets/M09_CONVOY.png';ow,oh=950,356
                    p=ease(n*.06,n*.93);center=f'Point(.36+.18*{p},.36)'
                nodes.extend([loader('MovingObject',f,end),resize('ObjectSize','MovingObject',ow,oh),merge('ObjectMerge',last,'ObjectSize','1',center=center)]);last='ObjectMerge';features.append('native independently moving transparent object')
                if aid=='M06':
                    nodes.append(rectangle('SensorMask',f'.28+.48*{p}',.585,.0016,.42))
                    nodes.append(background('Sensor',(.84,.60,.25),.32,'SensorMask'));nodes.append(merge('SensorMerge',last,'Sensor',ease(n*.12,n*.25)));last='SensorMerge';features.append('sensor ray tied to aircraft position')
            if aid=='M12':
                # Local lens magnifies the real illustration pixels; no invented microstructure.
                nodes.append('LensZoom = Transform { Inputs = { Input='+link('BaseMerge')+',Size='+inp(2.1)+',Center='+point(.444,1.129)+' } }')
                nodes.append('LensMask = EllipseMask { Inputs = { MaskWidth='+inp(1920)+',MaskHeight='+inp(1080)+',Center='+point(.78,.73)+',Width='+inp(.27)+',Height='+inp(.48)+',SoftEdge='+inp(.005)+' } }')
                lens_blend='1' if idx and plan[idx-1]['asset_id']==aid else ease(n*.18,n*.38)
                nodes.append(merge('LensMerge',last,'LensZoom',lens_blend,mask='LensMask'));last='LensMerge';features.append('native local magnifying lens on small sample fragments')
            if aid in ['G01','G04','G14','G15','G16','G19','G20','G22','G24','M11']:
                p=ease(n*.07,n*.9);z=f'1+.025*{p}'
                nodes.append('FocusPush = Transform { Inputs = { Input='+link(last)+',Size='+expr(z)+',Center='+point(.5,.5)+' } }');last='FocusPush';features.append('restrained continuous 2.5 percent subject push')
            if aid in rmap:
                ref=rmap[aid];loc=ref.get('source_locator','')
                boxmatch=re.search(r'crop[^\(]*\(([^)]+)\)',loc,re.I)
                page=re.search(r'PDF\s*page\s*(\d+)',loc,re.I)
                crop=None
                if boxmatch:
                    try:crop=[float(x.strip()) for x in boxmatch.group(1).split(',')]
                    except ValueError:pass
                hits=[]
                if crop and page:
                    for target in focus:
                        if target['asset_id'] not in drefs.get(aid,set()) or target.get('pdf_page_1based')!=int(page.group(1)):continue
                        for box in target.get('normalized_original_page_word_boxes',[]):hits.append((target['exact_search_text'],box))
                for hi,(words,box) in enumerate(hits[:5]):
                    # Full-height word boxes transformed through the actual registered source crop.
                    x0,y0,x1,y1=box;cx0,cy0,cx1,cy1=crop
                    left=(1920-fw)/2+(x0-cx0)/(cx1-cx0)*fw-2
                    right=(1920-fw)/2+(x1-cx0)/(cx1-cx0)*fw+2
                    top=(1080-fh)/2+(y0-cy0)/(cy1-cy0)*fh-2
                    bottom=(1080-fh)/2+(y1-cy0)/(cy1-cy0)*fh+2
                    if min(left,top)<0 or right>1920 or bottom>1080:continue
                    p=ease(n*.15+hi*13,n*.15+hi*13+18)
                    mask=f'WordMask{hi}';color=f'WordColor{hi}';mn=f'WordMerge{hi}'
                    nodes.append(rectangle(mask,f'{left/1920}+{(right-left)/1920}*.5*{p}',1-(top+bottom)/2/1080,f'{(right-left)/1920}*{p}',(bottom-top)/1080))
                    nodes.append(background(color,(1,.85,.24),.42,mask));nodes.append(merge(mn,last,color,'1',mode='Multiply'));last=mn
                    features.append('precise yellow full-height sweep: '+words)
        nodes.append('MediaOut1 = MediaOut { Inputs = { Input='+link(last)+' } }')
        path=folder/(s['shot_id']+'_'+aid+'.comp');write_comp(path,nodes,end)
        manifest.append(dict(shot_id=s['shot_id'],asset_id=aid,item_index=idx,start_frame=s['start_frame'],end_frame=s['end_frame'],comp=str(path),features=features or ['Source-led stable document or photo; no arbitrary motion']))
    (ROOT/'FUSION_IMPORT_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps({'native_comps':len(manifest),'timeline_shots':len(plan)}))

def canary():
    p=GRAPHICS/'STAGE07_MOTION_READY_R1/assets'
    tools=[loader('Base',p/'M06_BASE.png',198),resize('BaseHD','Base',1920,1080),loader('Plane',p/'M06_AIRCRAFT.png',198),resize('PlaneSmall','Plane',450,149),'''PlaneMerge = Merge { Inputs = { Background=Input { SourceOp="BaseHD", Source="Output" }, Foreground=Input { SourceOp="PlaneSmall", Source="Output" }, Center=Input { Value={0.4,0.84}, Expression="Point(0.22+0.50*min(1,max(0,time/198)),0.84)" } } }''','MediaOut1 = MediaOut { Inputs = { Input=Input { SourceOp="PlaneMerge",Source="Output" } } }']
    write_comp(ROOT/'NATIVE_FUSION_CANARY.comp',tools,198)

if __name__=='__main__':
    import sys
    build_all() if '--all' in sys.argv else canary()
