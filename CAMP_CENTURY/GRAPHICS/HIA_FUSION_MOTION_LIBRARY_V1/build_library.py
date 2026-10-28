"""Build two reusable native Fusion rigs from existing owner-selected artwork.
No generation, background translation, AI video, or narration modification.
"""
from pathlib import Path
import json,hashlib,importlib.util,argparse
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;CAMP=ROOT.parents[1]
REF=CAMP/'GRAPHICS/STAGE07_MOTION_READY_R1'
spec=importlib.util.spec_from_file_location('fusion_helpers',CAMP/'DEVELOPMENT/RESOLVE_R1/build_fusion.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
def ease(a,b):
    q=f'min(1,max(0,(time-({a}))/max(1,({b})-({a}))))'
    return f'({q}*{q}*(3-2*{q}))'
def controls(values,frames):
    labels=['Move start frame','Move end frame','Start X','End X','Start top','End top','Object width px','Accent strength']
    inputs=','.join('NumberIn'+str(i)+'='+f.inp(v) for i,v in enumerate(values,1))
    ui=[]
    for i,(label,v) in enumerate(zip(labels,values),1):
        low,high=(0,frames-1) if i<=2 else ((10,1200) if i==7 else (-.5,1.5))
        ui.append(f'NumberIn{i} = {{ LINKS_Name={json.dumps(label)},LINKID_DataType="Number",INPID_InputControl="SliderControl",INP_Default={v},INP_MinScale={low},INP_MaxScale={high} }}')
    return 'MotionControls = CustomTool { Inputs = { '+inputs+' }, UserControls = ordered() { '+','.join(ui)+' } }'
def crop_alpha(src,dst):
    im=Image.open(src).convert('RGBA');bounds=im.getchannel('A').getbbox();assert bounds and im.getchannel('A').getextrema()[0]==0
    im.crop(bounds).save(dst);return im.crop(bounds).size,bounds
def build(config):
    name=config['id'];fps=config['fps'];n=round(config['seconds']*fps);end=n-1
    assets=ROOT/'assets';out=ROOT/'comps';assets.mkdir(exist_ok=True);out.mkdir(exist_ok=True)
    source=REF/'assets'/config['object'];obj=assets/(name+'_ALPHA_CROPPED.png');size,bbox=crop_alpha(source,obj)
    vals=[round(config['move_start_seconds']*fps),round(config['move_end_seconds']*fps),*config['start_xy_top'],*config['end_xy_top']]
    # Native ordering is start X, end X, start top, end top.
    values=[vals[0],vals[1],config['start_xy_top'][0],config['end_xy_top'][0],config['start_xy_top'][1],config['end_xy_top'][1],config['object_width_px'],1]
    tools=[controls(values,n),f.background('Canvas'),f.loader('BackgroundPlate',REF/'assets'/config['background'],end),f.resize('BackgroundHD','BackgroundPlate',1920,1080),f.merge('LockedBackground','Canvas','BackgroundHD')]
    p=ease('MotionControls.NumberIn1','MotionControls.NumberIn2')
    x=f'(MotionControls.NumberIn3+(MotionControls.NumberIn4-MotionControls.NumberIn3)*{p})'
    top=f'(MotionControls.NumberIn5+(MotionControls.NumberIn6-MotionControls.NumberIn5)*{p})'
    height=f'(MotionControls.NumberIn7*{size[1]/size[0]})'
    centre=f'Point({x},1-{top}-{height}/2160)';last='LockedBackground'
    if name=='AIRCRAFT_PASS':
        # Existing reference's broad conceptual sector, not invented radar data.
        beam=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(beam)
        pts=[((430+70)/1672*1920,143/940*1080),((430-50)/1672*1920,581/940*1080),((430+270)/1672*1920,581/940*1080)]
        d.polygon(pts,fill=(223,163,58,26));d.line([pts[1],pts[0],pts[2]],fill=(223,163,58,130),width=2)
        beamfile=assets/'AIRCRAFT_REFERENCE_SECTOR.png';beam.save(beamfile)
        tools.append(f.loader('SensorSector',beamfile,end))
        dx=f'({x}-{430/1672})'
        tools.append('FollowAircraftX = Transform { Inputs = { Input='+f.link('SensorSector')+',Center='+f.expr(f'Point(.5+{dx},.5)')+' } }')
        env=ease(f'MotionControls.NumberIn1+{.1*fps}',f'MotionControls.NumberIn1+{.55*fps}')+'*(1-'+ease('MotionControls.NumberIn2',f'MotionControls.NumberIn2+{.6*fps}')+')*MotionControls.NumberIn8'
        tools.append(f.merge('ConceptualSector',last,'FollowAircraftX',env));last='ConceptualSector'
    else:
        hook=f'(1-{top})';tools.extend([f.rectangle('CableMask',x,f'(1+{hook})/2',1.4/1920,f'max(0,1-{hook})'),f.background('CableInk',(.12,.18,.21),.70,'CableMask'),f.merge('AttachedCable',last,'CableInk','MotionControls.NumberIn8')]);last='AttachedCable'
    tools.append(f.loader('IndependentObject',obj,end))
    tools.append('ObjectSize = BetterResize { Inputs = { Width='+f.expr('MotionControls.NumberIn7')+',Height='+f.expr(height)+',KeepAspect='+f.inp(0)+',Input='+f.link('IndependentObject')+' } }')
    tools.extend([f.merge('IndependentMotion',last,'ObjectSize','1',center=centre),'MediaOut1 = MediaOut { Inputs = { Input='+f.link('IndependentMotion')+' } }'])
    path=out/(name+'.comp');f.write_comp(path,tools,end)
    return dict(id=name,comp=str(path),frames=n,fps=fps,background=str(REF/'assets'/config['background']),original_object=str(source),alpha_bbox=list(bbox),cropped_object=str(obj),native_controls=values,source_object_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),comp_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),state='BUILT_NATIVE_PROOF_REQUIRED')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,default=ROOT/'EXAMPLE_CONFIGS.json');a=ap.parse_args()
    rows=[build(c) for c in json.loads(a.config.read_text())]
    (ROOT/'BUILD_MANIFEST.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print('BUILT_NATIVE_FUSION_RIGS',len(rows),flush=True)
