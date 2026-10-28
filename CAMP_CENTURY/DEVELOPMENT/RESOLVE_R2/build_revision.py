"""Build the owner-directed R2 without R1's generic cards or direct source scans."""
from pathlib import Path
import csv,json,sys,importlib.util,hashlib,re
from PIL import Image
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'RESOLVE_R1';G=ROOT.parents[1]/'GRAPHICS'
spec=importlib.util.spec_from_file_location('fusion_helpers',OLD/'build_fusion.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
def safe_ease(a,b):
    # Parenthesize negative offsets: time--82 is a Lua comment, not subtraction.
    q=f'min(1,max(0,(time-({a}))/({max(1,b-a)})))'
    return f'({q}*{q}*(3-2*{q}))'
f.ease=safe_ease
MAP={'C04':'Q02','R07_ESTIMATE':'Q01','R01_COVER':'Q04','C05':'Q09','R32_GREENLAND_ONLY':'Q05','C01':'Q05','C02A':'Q03','C02B':'Q03','R03_ARCH':'Q04','R25_PREMATURE_FORMS':'G14','R26_UTILITY_LINES':'G15','C16':'G13','C03':'Q07','C15':'Q06','R27_WATER_WELL':'G05','R28_SEWAGE_PROFILE':'G05','R10_SUMP':'Q17','C08':'Q07','C05_QUALIFIER':'Q09','C05_AREA':'Q18','C09':'G15','C10':'Q05','C11':'Q10','R11_DISTRESS':'Q19','R06_PROFILES':'Q02','R29_MAIN_HEIGHT_TABLE':'Q11','R30_SIDE_HEIGHT_TABLE':'Q11','R08_CHAINSAW':'Q01','R12_SHUTDOWN':'Q12','R33_FIRN_FORECAST':'Q13','C13':'Q13','R15_DRILL_1966':'G08','R24_FROZEN_ARCHIVE':'Q14','R13_CORE_2021':'Q14','R14_RADAR_2024':'Q15','C14':'Q15','M06':'G10','M09':'Q16'}
SHOT={'S012':'Q08','S026':'G03','S032':'G02','S050':'G15','S058':'G05','S062':'G03','S069':'Q08','S073':'Q05','S078':'G20','S094':'G14','S097':'G15','S066':'Q08','S077':'Q08','S110':'Q13','S013':'G03','S015':'G11','S021':'Q08','S041':'G03','S064':'Q04','S091':'G02','S132':'G03','S056':'Q17','S084':'Q02','S114':'Q14','S123':'G10'}
TITLES={j['id']:j['title'] for j in json.loads((G/'STAGE07_CORRECTIONS_R3/GENERATION_JOBS.json').read_text(encoding='utf-8'))}
gm={x['asset_id']:x for x in json.loads((G/'STAGE07_GENERATED_R1/GENERATION_MANIFEST.json').read_text(encoding='utf-8'))}
plan=json.loads((OLD/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
for s in plan:
    old=s['asset_id'];new=SHOT.get(s['shot_id'],MAP.get(old,old))
    s['r1_asset_id']=old;s['asset_id']=new
    if new!=old or new.startswith('Q'):
        s['primary_evidence_source']=s.get('source','');s['primary_evidence_locator']=s.get('locator','')
        if new.startswith('Q'):
            path=G/'STAGE07_CORRECTIONS_R3/assets'/f'{new}.png'
            clean_ids=['Q02','Q06','Q07','Q09','Q14','Q15','Q17','Q18']
            if new in clean_ids:path=path.with_name(new+'_CLEAN.png')
            record=new+'_CLEAN' if new in clean_ids else new
            recpath=G/'STAGE07_CORRECTIONS_R3'/f'{record}_GENERATION.json'
            title=json.loads(recpath.read_text(encoding='utf-8')).get('title',TITLES[new]) if recpath.exists() else TITLES[new]
            s.update(path=str(path),kind='GENERATED_DOCUMENT' if new!='Q16' else 'GENERATED_CONCEPT',title=title,rights='Authored generated explanatory artwork; not an original archival document',source='STAGE07_CORRECTIONS_R3/'+record+'_GENERATION.json',locator='Owner-directed clean generation, grounded in V4 and primary references',motion='NATIVE_R2_FOCUS')
        else:
            g=gm[new];s.update(path=str(G/'STAGE07_GENERATED_R1'/g['file']),kind='GENERATED_CONCEPT',title=g['title'],rights='Approved generated explanatory illustration; not archival evidence',source=g.get('references',''),locator='Approved complete artwork restored',motion='NATIVE_R2_FOCUS')
        s.pop('lines',None)
    s['edit_reason']=s.get('voice_cue') or s['beat_id']+' / narrative opening'
    s['scope']='R2 owner correction; preserve locked narration and beat bounds'
additions_path=ROOT/'ADDITIONAL_ARCHIVE_PLACEMENTS.json'
if additions_path.exists():
    additions={x['shot_id']:x for x in json.loads(additions_path.read_text(encoding='utf-8'))}
    for s in plan:
        if s['shot_id'] in additions:
            extra=additions[s['shot_id']]
            for key in ['asset_id','path','kind','title','rights','source','locator','source_in_sec','source_out_sec','source_in_frame','source_out_frame_exclusive','source_fps','source_sha256','original_selected_clip','site_class','warning']:s[key]=extra[key]
            s['native_fps']='25/1';s['motion']='GENUINE_ARCHIVE_PICTURE';s['edit_reason']='Actual Camp Century assembly/work crew footage matches the spoken action; no reused clip'
assert all(s['kind'] not in ['PRIMARY_REFERENCE','FACTUAL_NATIVE_GRAPHIC'] for s in plan)
assert len(plan)==132 and plan[-1]['end_frame']==27368
for a,b in zip(plan,plan[1:]):assert a['end_frame']==b['start_frame']
# Continuous motion across adjacent holds of one page; no zoom reset at a split.
i=0
while i<len(plan):
    j=i+1
    while j<len(plan) and plan[j]['asset_id']==plan[i]['asset_id']:j+=1
    length=sum(s['duration_frames'] for s in plan[i:j]);offset=0
    for s in plan[i:j]:s['motion_group_frames']=length;s['motion_group_offset']=offset;s['motion_group_start_frame']=plan[i]['start_frame'];offset+=s['duration_frames']
    i=j
(ROOT/'SHOT_PLAN_R2.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
cols=['shot_id','beat_id','chapter','asset_id','r1_asset_id','kind','start_frame','end_frame','duration_frames','voice_cue','alignment_basis','alignment_score','edit_reason','path','title','rights','source','locator','primary_evidence_source','primary_evidence_locator']
with (ROOT/'SHOT_PLAN_R2.csv').open('w',encoding='utf-8-sig',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(plan)
highlights=json.loads((ROOT/'LOCAL_HIGHLIGHT_TARGETS.json').read_text(encoding='utf-8')) if (ROOT/'LOCAL_HIGHLIGHT_TARGETS.json').exists() else {}
asr_path=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1\ASR_QC\CAMP_CENTURY_MASTER_WORDS_SMALL_EN.json')
words=json.loads(asr_path.read_text(encoding='utf-8-sig'))
timings=[]
def tokens(text):
    text=re.sub(r'(?<=\d),(?=\d)','',text.lower())
    return re.findall(r'[a-z0-9]+',text)
def sync_target(target,s):
    begin=s['motion_group_start_frame']/25;finish=begin+s['motion_group_frames']/25
    available=[]
    for word in words:
        if begin-.08<=float(word['start'])<finish:
            available.extend((token,float(word['start'])) for token in tokens(word['text']))
    for phrase in target.get('cue_phrases',[target['text']]):
        wanted=tokens(phrase)
        for k in range(len(available)-len(wanted)+1):
            if [token for token,_ in available[k:k+len(wanted)]]==wanted:
                at=available[k][1];start=round((at-begin)*25)
                if start+17>s['motion_group_frames']:continue
                return start,at,phrase
    return None
only=set(sys.argv[sys.argv.index('--only')+1].split(',')) if '--only' in sys.argv else None
out=ROOT/'COMPS';out.mkdir(exist_ok=True);manifest=[];graphs={}
soft_changes={'S006','S016','S022','S051','S060','S065','S076','S086','S089','S100','S111','S120','S121','S132'}
for idx,s in enumerate(plan):
    if s['kind']=='REAL_ARCHIVE_MOTION' or (only is not None and s['shot_id'] not in only):continue
    path=Path(s['path']);assert path.is_file(),str(path)
    n=s['duration_frames'];end=n-1;aid=s['asset_id'];tools=[f.background('Paper')]
    im=Image.open(path);w,h=im.size;k=min(1920/w,1080/h)*(.92 if aid=='Q07' else 1);fw,fh=round(w*k),round(h*k)
    tools.extend([f.loader('ApprovedArtwork',path,end),f.resize('ArtworkFit','ApprovedArtwork',fw,fh),f.merge('ArtworkOnPaper','Paper','ArtworkFit')]);last='ArtworkOnPaper';features=[]
    # Accents are distinct native nodes, never baked into generated artwork.
    for hi,target in enumerate(highlights.get(aid,[])):
        matched=sync_target(target,s)
        if matched is None:
            timings.append(dict(shot=s['shot_id'],asset=aid,text=target['text'],status='OMITTED_NO_EXACT_WITHIN_SCENE_ASR_CUE'));continue
        x0,y0,x1,y1=target['box'];left=(1920-fw)/2+x0*fw;right=(1920-fw)/2+x1*fw;top=(1080-fh)/2+y0*fh;bottom=(1080-fh)/2+y1*fh
        start=matched[0]-s['motion_group_offset'];p=f.ease(start,start+17)
        timings.append(dict(shot=s['shot_id'],asset=aid,text=target['text'],status='ASR_EXACT_PHRASE',audio_start_seconds=matched[1],matched_phrase=matched[2]))
        mask=f'LocalMarkerMask{hi}';color=f'LocalMarkerColor{hi}';merge=f'LocalMarkerMerge{hi}'
        tools.extend([f.rectangle(mask,f'{left/1920}+{(right-left)/1920}*.5*{p}',1-(top+bottom)/2160,f'{(right-left)/1920}*{p}',(bottom-top)/1080),f.background(color,(1,.84,.20),.32,mask),f.merge(merge,last,color,'1',mode='Multiply')]);last=merge;features.append('Native 0.68-second full-height marker sweep: '+target['text'])
    if aid in ['M01','M02','M03','M04','M05','M07']:
        overlay=G/f'STAGE07_MOTION_READY_R1/overlays/{aid}_ACCENTS_ENDSTATE.png'
        off=s['motion_group_offset'];p=f.ease(15-off,30-off)
        tools.extend([f.loader('ExplanatoryAccents',overlay,end),f.resize('AccentsHD','ExplanatoryAccents',1920,1080)])
        mask=None
        if aid=='M03':tools.append(f.rectangle('RoofAccentsOnly',.5,.60,1,.80));mask='RoofAccentsOnly'
        tools.append(f.merge('AccentsAppear',last,'AccentsHD',p,mask=mask));last='AccentsAppear'
        features.append('Separate transparent explanatory annotations; complete labels fade in without clipping individual letters')
    if aid=='M08':
        p=f.ease(n*.08,n*.65);hook=f'(.75+.12*{p}+277/2160)'
        tools.extend([f.rectangle('CableMask',.5,f'(1+{hook})/2',.0008,f'1-{hook}'),f.background('Cable',(.12,.18,.21),.85,'CableMask'),f.merge('CableOverScene',last,'Cable'),f.loader('LiftedModule',G/'STAGE07_MOTION_READY_R1/assets/M08_MODULE.png',end),f.resize('ModuleSize','LiftedModule',300,277),f.merge('ModuleLift','CableOverScene','ModuleSize','1',center=f'Point(.50,.75+.12*{p})')]);last='ModuleLift'
        features.append('Retained approved independent module hoist with attached cable; no vehicle sliding')
    if aid=='Q07':
        # Exact data, not the approximate bar discarded from the generated base.
        fraction=5.7/7.92;left=(1920-fw)/3840+.6274*fw/1920;width=.3471*fw/1920;cy=1-((1080-fh)/2+(.6780+.0861/2)*fh)/1080;height=.0861*fh/1080
        cue=sync_target({'text':'PM-2A cost','cue_phrases':['five point seven million','5 7 million','5.7 million','five million seven hundred thousand']},s)
        p=f.ease(cue[0]-s['motion_group_offset'],cue[0]-s['motion_group_offset']+20) if cue else '1'
        tools.extend([f.rectangle('CostTotalMask',left+width/2,cy,width,height),f.background('CostTotal',(.30,.34,.36),.22,'CostTotalMask'),f.merge('TotalOnLedger',last,'CostTotal')]);last='TotalOnLedger'
        tools.extend([f.rectangle('CostPartMask',f'{left}+{width*fraction}*.5*{p}',cy,f'{width*fraction}*{p}',height),f.background('CostPart',(.16,.40,.57),.82,'CostPartMask'),f.merge('CostAllocation','TotalOnLedger','CostPart')]);last='CostAllocation'
        features.append('Native exact cost-allocation ratio 5.70 / 7.92; generated approximate bar removed')
    # Zooms target named content; integrated vehicles never translate over ground.
    focus={'Q16':(.36,.62,.038),'G10':(.52,.48,.025),'Q01':(.48,.70,.020),'Q02':(.5,.64,.022),'Q03':(.5,.48,.030),'Q05':(.46,.49,.035),'Q06':(.47,.47,.025),'Q07':(.75,.47,.025),'Q10':(.70,.55,.020),'Q11':(.42,.60,.025),'Q14':(.60,.58,.035),'G03':(.38,.60,.025),'G15':(.65,.42,.025),'G16':(.43,.56,.025),'M11':(.50,.43,.025),'M12':(.70,.67,.035)}.get(aid,(.5,.5,0))
    tx,ty,amount=focus;off=s['motion_group_offset'];length=s['motion_group_frames'];p=f.ease(length*.08-off,length*.90-off);z=f'(1+{amount}*{p})'
    center=f'Point(.5+{.5-tx}*({z}-1),.5+{.5-ty}*({z}-1))'
    if s['shot_id']=='S001':
        e=f.ease(15,75);ceiling=sync_target({'text':'ceiling','cue_phrases':['ceiling']},s)
        anchor=ceiling[0] if ceiling else 250;pan=f.ease(anchor-20,min(anchor+40,n-10))
        z=f'(1+.08*{e})';cx=f'(.5-.03*{e}+.06*{pan})';center=f'Point(.5+(.5-{cx})*{z},.5)'
        features.append('Opening approach to initial section, then motivated pan toward reduced opening at the spoken ceiling cue')
    if s['shot_id'] in ['S083','S084','S085']:
        p83=next(x for x in plan if x['shot_id']=='S083');p84=next(x for x in plan if x['shot_id']=='S084')
        n83=p83['duration_frames'];n84=p84['duration_frames']
        phases=[('Main',.30,.70,f'{f.ease(10-off,25-off)}*(1-{f.ease(n83-18-off,n83-3-off)})'),('Side',.74,.66,f'{f.ease(n83+5-off,n83+20-off)}*(1-{f.ease(n83+n84-25-off,n83+n84-10-off)})')]
        for name,x,y,blend in phases:
            outer=name+'LensOuter';inner=name+'LensInner';canvas=name+'LensAlpha';ring=name+'LensInk';rim=name+'LensRim';zoom=name+'DetailZoom';detail=name+'LensSurface';merged=name+'Inspection'
            for mask_name,width in [(outer,.172),(inner,.168)]:
                tools.append(mask_name+' = EllipseMask { Inputs = { MaskWidth='+f.inp(1920)+',MaskHeight='+f.inp(1080)+',Center='+f.point(x,y)+',Width='+f.inp(width)+',Height='+f.inp(width)+',SoftEdge='+f.inp(.001)+' } }')
            tools.extend([f.background(canvas,(0,0,0),0),f.background(ring,(.12,.16,.18),.9,outer),f.merge(rim,canvas,ring)])
            tools.append(zoom+' = Transform { Inputs = { Input='+f.link('ArtworkOnPaper')+',Size='+f.inp(1.7)+',Center='+f.point(x-1.7*(x-.5),y-1.7*(y-.5))+' } }')
            tools.extend([f.merge(detail,rim,zoom,'1',mask=inner),f.merge(merged,last,detail,blend)]);last=merged
        z='1';center='Point(.5,.5)'
        features.append('Two native local contour inspections; full document stays in frame and captions remain intact')
    tools.append('MotivatedFocus = Transform { Inputs = { Input='+f.link(last)+',Size='+f.expr(z)+',Center='+f.expr(center)+' } }');last='MotivatedFocus'
    features.append('Coherent eased camera focus on named subject; same transform for artwork and native highlights' if amount else 'Stable complete illustration; no automatic camera drift')
    if aid=='G10':features.append('Owner-approved original aircraft and wide sensing wedge restored; no replacement aircraft or thin ray')
    if aid=='Q16':features.append('Vehicle and snow route are one coherent scene; independent tractor translation removed')
    graphs[s['shot_id']]=(list(tools),last,end)
    if s['shot_id'] in soft_changes and idx and plan[idx-1]['asset_id']!=aid and plan[idx-1]['shot_id'] in graphs:
        previous,prevlast,prevend=graphs[plan[idx-1]['shot_id']]
        names=[re.match(r'(\w+)\s*=',node).group(1) for node in previous]
        def freeze(node):
            for name in sorted(names,key=len,reverse=True):node=re.sub(r'\b'+re.escape(name)+r'\b','Previous_'+name,node)
            return re.sub(r'\btime\b',str(prevend),node)
        tools.extend([freeze(node) for node in previous])
        tools.append(f.merge('MotivatedDissolve','Previous_'+prevlast,last,f.ease(0,10)));last='MotivatedDissolve'
        features.append('Native 10-frame dissolve from exact previous generated-frame treatment for a report/location/time change')
    tools.append('MediaOut1 = MediaOut { Inputs = { Input='+f.link(last)+' } }')
    dest=out/f"{s['shot_id']}_{aid}.comp";f.write_comp(dest,tools,end)
    assert 'time--' not in dest.read_text(encoding='utf-8'),s['shot_id']
    manifest.append(dict(shot_id=s['shot_id'],item_index=idx,asset_id=aid,comp=str(dest),features=features,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
target=ROOT/('FUSION_IMPORT_MANIFEST_PROOFS.json' if only else 'FUSION_IMPORT_MANIFEST.json')
target.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(ROOT/'NATIVE_HIGHLIGHT_AUDIO_ALIGNMENT.json').write_text(json.dumps(timings,indent=2),encoding='utf-8')
print(json.dumps({'shots':len(plan),'built_native_comps':len(manifest),'direct_scans':0,'generic_text_cards':0,'picture_duration_frames':27368}))
