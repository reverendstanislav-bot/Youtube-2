import React from 'react';
import {AbsoluteFill, Audio, Composition, Img, interpolate, registerRoot, staticFile, useCurrentFrame} from 'remotion';
import timeline from '../public/timeline.json';
import overlays from '../public/overlays.json';
import motion from '../public/motion.json';
import {HiaEstablishingSlug,HiaEditorialPanel} from './HiaMotionCanon';
import transitionPlan from '../public/hia_transition_plan.json';

const FPS=timeline.fps;
const CONTENT_END=Math.round(timeline.duration*FPS);
const END_SCREEN_FRAMES=20*FPS;
const TOTAL=CONTENT_END+END_SCREEN_FRAMES;
const C={charcoal:'#171A1C',paper:'#FFFFFF',ivory:'#F3EBDD',orange:'#F28A3A',blue:'#708996',rust:'#A55235'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const smooth=x=>{const v=Math.max(0,Math.min(1,x));return v*v*(3-2*v)};
const transitionByBeat=Object.fromEntries(transitionPlan.items.map(x=>[x.beat,x]));
const motionByBeat=Object.fromEntries(motion.items.map(x=>[x.beat,x]));
const beatIndexById=Object.fromEntries(timeline.beats.map((x,i)=>[x.beat,i]));

function currentBeat(frame){
  let lo=0,hi=timeline.beats.length-1;
  while(lo<=hi){const m=(lo+hi)>>1,b=timeline.beats[m];if(frame<b.a)hi=m-1;else if(frame>=b.b)lo=m+1;else return b;}
  return timeline.beats[Math.max(0,Math.min(timeline.beats.length-1,lo))];
}

function motionTransform(beat,frame){
  const p=smooth(interpolate(frame,[beat.a,Math.max(beat.a+1,beat.b-1)],[0,1],CLAMP));
  const style=(motionByBeat[beat.beat]||{}).style||'hold';
  let scale=1.007,x=0,y=0,origin='50% 50%';
  if(style==='push')scale=1.005+.012*p;
  if(style==='pull')scale=1.017-.012*p;
  if(style==='pan_left'){scale=1.018;x=.20-.40*p;}
  if(style==='pan_right'){scale=1.018;x=-.20+.40*p;}
  if(style==='tilt_up'){scale=1.018;y=.20-.40*p;}
  if(style==='tilt_down'){scale=1.018;y=-.20+.40*p;}
  if(style==='push_left'){scale=1.005+.012*p;origin='30% 50%';}
  if(style==='push_right'){scale=1.005+.012*p;origin='70% 50%';}
  if(style==='hold_then_push'){const q=smooth(interpolate(p,[.4,1],[0,1],CLAMP));scale=1.007+.010*q;}
  return {style,transform:'translate('+x+'%,'+y+'%) scale('+scale+')',origin};
}

function ImageBeat({beat,frame,opacity=1}){
  const isGfx=beat.kind==='gfx';
  const m=motionTransform(beat,frame);
  return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden',opacity}}>
    <Img src={staticFile(beat.file)} style={{width:'100%',height:isGfx?'900px':'100%',objectFit:isGfx?'contain':'cover',objectPosition:beat.objectPosition||'center top',transform:isGfx?'none':m.transform,transformOrigin:m.origin}}/>
    {isGfx&&<div style={{position:'absolute',left:0,right:0,bottom:0,height:180,background:C.charcoal,borderTop:'1px solid rgba(243,235,221,.12)'}}/>}
    {!isGfx&&<AbsoluteFill style={{background:'linear-gradient(180deg,rgba(8,10,11,.08),rgba(8,10,11,.02) 58%,rgba(8,10,11,.48))'}}/>}
  </AbsoluteFill>;
}

function DocumentBeat({beat,frame}){
  const local=(frame-beat.a)/FPS,dur=(beat.b-beat.a)/FPS;
  const op=Math.min(interpolate(local,[0,.25],[0,1],CLAMP),interpolate(local,[Math.max(.5,dur-.35),dur],[1,0],CLAMP));
  return <AbsoluteFill style={{background:C.charcoal,justifyContent:'center',alignItems:'center',opacity:op}}>
    <div style={{width:1420,minHeight:650,padding:'72px 84px',boxSizing:'border-box',background:C.ivory,boxShadow:'0 28px 80px rgba(0,0,0,.52)',color:C.charcoal,fontFamily:'Arial,Helvetica,sans-serif'}}>
      <div style={{fontSize:20,fontWeight:850,letterSpacing:5,color:C.rust}}>OFFICIAL DOCUMENT</div>
      <div style={{width:110,height:7,background:C.orange,margin:'26px 0 42px'}}/>
      <div style={{fontFamily:'Georgia,serif',fontWeight:700,fontSize:58,lineHeight:1.06,maxWidth:1220}}>{beat.narration}</div>
      <div style={{marginTop:50,fontSize:25,fontWeight:750,color:'#536067'}}>{beat.documentName}</div>
      <div style={{marginTop:10,fontSize:19,letterSpacing:1.5,color:'#68757b'}}>{beat.sourceTitle}</div>
    </div>
  </AbsoluteFill>;
}

function Provenance({beat,frame}){
  if(beat.kind!=='document')return null;
  const local=(frame-beat.a)/FPS,dur=(beat.b-beat.a)/FPS;
  if(local>Math.min(2.4,dur))return null;
  const op=Math.min(interpolate(local,[0,.18],[0,1],CLAMP),interpolate(local,[Math.min(1.85,dur-.25),Math.min(2.4,dur)],[1,0],CLAMP));
  return <div style={{position:'absolute',right:50,top:38,zIndex:40,opacity:op,fontFamily:'Arial,Helvetica,sans-serif',fontSize:23,fontWeight:850,letterSpacing:3,color:C.ivory,textShadow:'0 2px 8px #000'}}><span style={{display:'inline-block',width:40,height:5,background:C.rust,marginRight:13,verticalAlign:'middle'}}/>DOCUMENT</div>;
}

function Picture({frame,beat}){
  const index=beatIndexById[beat.beat];
  const edge=transitionByBeat[beat.beat]||{kind:'hard_cut',frames:0};
  if(index===0||edge.frames===0||edge.kind==='hard_cut'||edge.kind==='evidence_cut'){
    return <ImageBeat beat={beat} frame={frame}/>;
  }
  const previous=timeline.beats[index-1];
  const p=smooth(interpolate(frame,[beat.a,beat.a+edge.frames],[0,1],CLAMP));
  // Every transition blends original full-resolution scene pixels.
  // Editorial-only motion: no same-image pan wipe and no invented video footage.
  if(edge.kind==='chapter_dip'){
    const oldOpacity=Math.max(0,Math.min(1,(.57-p)/.57));
    const newOpacity=Math.max(0,Math.min(1,(p-.38)/.62));
    return <AbsoluteFill style={{background:C.charcoal}}>
      {oldOpacity>0&&<ImageBeat beat={previous} frame={previous.b-1} opacity={oldOpacity}/>}
      {newOpacity>0&&<ImageBeat beat={beat} frame={frame} opacity={newOpacity}/>}
    </AbsoluteFill>;
  }
  if(edge.kind==='focus_dissolve'){
    // A tiny perceived focus settle, NOT a Ken Burns slide/zoom jump.
    return <AbsoluteFill style={{background:C.charcoal}}>
      <ImageBeat beat={previous} frame={previous.b-1} opacity={1-p}/>
      <AbsoluteFill style={{opacity:p,transform:'scale('+(1.003-.003*p)+')'}}>
        <ImageBeat beat={beat} frame={frame}/>
      </AbsoluteFill>
    </AbsoluteFill>;
  }
  // Film vs match dissolve differ in duration & editorial selection.
  return <AbsoluteFill style={{background:C.charcoal}}>
    <ImageBeat beat={previous} frame={previous.b-1} opacity={1-p}/>
    <ImageBeat beat={beat} frame={frame} opacity={p}/>
  </AbsoluteFill>;
}

function Cards({frame}){
  const t=frame/FPS,card=overlays.cards.find(x=>t>=x.s&&t<=x.e);
  return card?<HiaEditorialPanel card={card} frame={frame} fps={FPS}/>:null;
}

function EndScreen({frame}){
  if(frame<CONTENT_END)return null;
  const opacity=interpolate(frame,[CONTENT_END,CONTENT_END+8],[0,1],CLAMP);
  return <AbsoluteFill style={{zIndex:100,background:C.charcoal,opacity}}>
    <Img src={staticFile('end_screen_1080.png')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  </AbsoluteFill>;
}

function Film(){
  const frame=useCurrentFrame(),beat=currentBeat(frame);
  return <AbsoluteFill style={{background:C.charcoal}}>
    {frame<CONTENT_END&&<>{beat.kind==='document'?<DocumentBeat beat={beat} frame={frame}/>:<Picture beat={beat} frame={frame}/>}
    <Provenance beat={beat} frame={frame}/><HiaEstablishingSlug frame={frame} beat={beat}/><Cards frame={frame}/></>}
    <Audio src={staticFile('SATSOP_VO_MASTER_V1.wav')}/>
    <EndScreen frame={frame}/>
  </AbsoluteFill>;
}

registerRoot(()=><Composition id="SatsopV1" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080}/>);
