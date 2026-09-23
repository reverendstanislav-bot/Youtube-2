import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Sequence,Img,staticFile,useCurrentFrame,interpolate} from 'remotion';
import manifest from '../public/timeline.json';
import captions from '../public/captions.json';
import overlays from '../public/overlays.json';

const FPS=25;
const END_START=1268.0;
const C={charcoal:'#171A1C',paper:'#FFFFFF',ivory:'#F3EBDD',orange:'#F28A3A',rust:'#A55235',blue:'#5F747D'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};

function viewTransform(view,progress,motion){
  let scale=1,tx=0,ty=0;
  if(view==='detail_left'){scale=1.16;tx=5.0;}
  else if(view==='detail_right'){scale=1.16;tx=-5.0;}
  else if(view==='center_detail'){scale=1.12;}
  else if(view==='map_detail_left'){scale=1.22;tx=6.0;ty=1.5;}
  else if(view==='map_detail_right'){scale=1.22;tx=-6.0;ty=-1.0;}
  else if(view==='map_center'){scale=1.14;}
  else if(view==='map_wide'){scale=1.01;}
  if(motion==='push') scale += 0.015*progress;
  return `translate(${tx}%,${ty}%) scale(${scale})`;
}

function Shot({shot}){
  const f=useCurrentFrame();
  const p=interpolate(f,[0,Math.max(1,shot.frames-1)],[0,1],CLAMP);
  return <AbsoluteFill style={{overflow:'hidden',background:C.charcoal}}>
    <Img src={staticFile(shot.file)} style={{
      position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',
      transform:viewTransform(shot.view,p,shot.motion),transformOrigin:'50% 50%'
    }}/>
  </AbsoluteFill>;
}

function Picture(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    {manifest.shots.map(s=><Sequence key={s.i} from={s.a} durationInFrames={s.frames} premountFor={8}>
      <Shot shot={s}/>
    </Sequence>)}
  </AbsoluteFill>;
}

function Provenance(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=END_START)return null;
  const s=manifest.shots.find(x=>frame>=x.a&&frame<x.b);
  if(!s || !s.provenance || !s.showProvenance)return null;
  const local=(frame-s.a)/FPS;
  if(local>Math.min(1.9,s.durationSec))return null;
  const fadeOutStart=Math.max(.75,Math.min(1.45,s.durationSec-.30));
  const op=Math.min(
    interpolate(local,[0,.16],[0,1],CLAMP),
    interpolate(local,[fadeOutStart,Math.min(1.9,s.durationSec)],[1,0],CLAMP)
  );
  const accent=s.provenance==='HISTORICAL SOURCE'?C.orange:(s.provenance==='AI RECONSTRUCTION'?C.blue:C.rust);
  return <div style={{
    position:'absolute',right:48,top:34,zIndex:35,opacity:op,
    fontFamily:'Arial,Helvetica,sans-serif',fontSize:24,fontWeight:800,letterSpacing:2.5,
    color:C.ivory,textShadow:'0 2px 5px rgba(0,0,0,.95),0 0 10px rgba(0,0,0,.65)'
  }}>
    <span style={{display:'inline-block',width:38,height:4,background:accent,marginRight:12,verticalAlign:'middle'}}/>
    {s.provenance}
  </div>;
}

function Caption(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=END_START)return null;
  const cue=captions.find(x=>t>=x.s&&t<=x.e);
  if(!cue)return null;
  let active=-1;
  for(let i=0;i<cue.words.length;i++){
    const w=cue.words[i];
    if(t>=w.s&&t<=Math.max(w.e,w.s+.055)){active=i;break;}
  }
  return <div style={{
    position:'absolute',left:150,right:150,bottom:54,zIndex:50,textAlign:'center',
    fontFamily:'Arial,Helvetica,sans-serif',fontWeight:800,fontSize:58,lineHeight:1.13,
    color:C.paper,WebkitTextStroke:'1.25px rgba(10,12,13,.92)',
    textShadow:'0 4px 8px rgba(10,12,13,.98),0 0 20px rgba(10,12,13,.78)'
  }}>
    {cue.words.map((w,i)=><React.Fragment key={i}>
      <span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<cue.words.length-1?' ':''}
    </React.Fragment>)}
  </div>;
}

function EditorialCard({card}){
  const t=useCurrentFrame()/FPS,local=t-card.s,dur=card.e-card.s;
  const op=Math.min(
    interpolate(local,[0,.22],[0,1],CLAMP),
    interpolate(local,[Math.max(.45,dur-.30),dur],[1,0],CLAMP)
  );
  const words=card.title.trim().split(/\s+/);
  let lines=[card.title];
  if(words.length>3){
    let best=1,score=1e9;
    for(let i=1;i<words.length;i++){
      const a=words.slice(0,i).join(' '),b=words.slice(i).join(' ');
      const sc=Math.abs(a.length-b.length);
      if(sc<score){score=sc;best=i;}
    }
    lines=[words.slice(0,best).join(' '),words.slice(best).join(' ')];
  }
  return <div style={{position:'absolute',left:88,top:72,width:1100,zIndex:25,opacity:op}}>
    <div style={{display:'flex',alignItems:'center',gap:18}}>
      <div style={{width:64,height:5,background:C.orange}}/>
      <div style={{fontFamily:'Arial,Helvetica,sans-serif',fontSize:20,fontWeight:760,letterSpacing:4.3,color:C.paper,textShadow:'0 2px 6px #000'}}>{card.kicker}</div>
    </div>
    <div style={{marginTop:24,fontFamily:'Arial,Helvetica,sans-serif',fontWeight:850,fontSize:card.kind==='fact'?64:78,lineHeight:.95,color:C.ivory,textShadow:'0 4px 10px rgba(0,0,0,.9)'}}>
      {lines.slice(0,2).map((x,i)=><div key={i}>{x}</div>)}
    </div>
    {card.subline&&<div style={{marginTop:18,fontFamily:'Arial,Helvetica,sans-serif',fontSize:23,fontWeight:760,letterSpacing:3.2,color:C.orange,whiteSpace:'pre-line',textShadow:'0 2px 5px #000'}}>{card.subline}</div>}
  </div>;
}

function Cards(){
  const t=useCurrentFrame()/FPS;
  if(t>=END_START)return null;
  const c=overlays.cards.find(x=>t>=x.s&&t<=x.e);
  return c?<EditorialCard card={c}/>:null;
}

function EndScreen(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<END_START)return null;
  const op=interpolate(frame,[Math.round(END_START*FPS),Math.round(END_START*FPS)+6],[0,1],CLAMP);
  return <AbsoluteFill style={{zIndex:80,opacity:op,background:C.charcoal}}>
    <Img src={staticFile('end_screen_1080.png')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  </AbsoluteFill>;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <Picture/><Cards/><Provenance/><Caption/><EndScreen/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="ChicagoR14" component={Film} durationInFrames={32268} fps={25} width={1920} height={1080}/>);
