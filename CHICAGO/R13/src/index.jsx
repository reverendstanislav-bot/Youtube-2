import React from 'react';
import {
  registerRoot,Composition,AbsoluteFill,Sequence,Img,staticFile,useCurrentFrame,interpolate,Easing
} from 'remotion';
import manifest from '../public/timeline.json';
import captions from '../public/captions.json';
import overlays from '../public/overlays.json';

const FPS=25;
const END_START=1268.0;
const C={charcoal:'#171A1C',paper:'#F2ECE1',ivory:'#F6F1E8',orange:'#F28A3A',rust:'#A55235',blue:'#5F747D'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};

const activeWord=(cue,t)=>{
  for(let i=0;i<cue.words.length;i++){
    const w=cue.words[i];
    if(t>=w.s && t<=Math.max(w.e,w.s+.06)) return i;
  }
  return -1;
};

function Shot({shot}){
  const f=useCurrentFrame();
  const n=Math.max(1,shot.frames-1);
  let scale=1;
  if(shot.motion==='push'){
    scale=interpolate(f,[0,n],[1.002,1.016],CLAMP);
  }
  return <AbsoluteFill style={{overflow:'hidden',background:C.charcoal}}>
    <Img src={staticFile(shot.file)} style={{
      position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',
      transform:`scale(${scale})`,transformOrigin:'50% 50%'
    }}/>
  </AbsoluteFill>;
}

function Picture(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    {manifest.shots.map(s=><Sequence key={s.i} from={s.a} durationInFrames={s.frames} premountFor={10}>
      <Shot shot={s}/>
    </Sequence>)}
  </AbsoluteFill>;
}

function Provenance(){
  const frame=useCurrentFrame();
  const t=frame/FPS;
  if(t>=END_START)return null;
  const s=manifest.shots.find(x=>frame>=x.a&&frame<x.b);
  if(!s || !s.provenance)return null;
  const local=(frame-s.a)/FPS;
  if(local>Math.min(1.55,s.durationSec))return null;
  const a=interpolate(local,[0,.18],[0,1],CLAMP);
  const b=interpolate(local,[Math.max(.35,Math.min(1.22,s.durationSec-.30)),Math.min(1.55,s.durationSec)],[1,0],CLAMP);
  const op=Math.min(a,b);
  const accent=s.provenance==='HISTORICAL SOURCE'?C.orange:(s.provenance==='AI RECONSTRUCTION'?C.blue:C.rust);
  return <div style={{
    position:'absolute',right:28,top:22,opacity:op,zIndex:30,
    fontFamily:'Arial,Helvetica,sans-serif',fontSize:10,fontWeight:700,letterSpacing:1.7,
    color:C.paper,textShadow:'0 1px 3px rgba(0,0,0,.82)'
  }}>
    <span style={{display:'inline-block',width:18,height:2,background:accent,marginRight:8,verticalAlign:'middle'}}/>
    {s.provenance}
  </div>;
}

function Caption(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=END_START)return null;
  const cue=captions.find(x=>t>=x.s&&t<=x.e);
  if(!cue)return null;
  const active=activeWord(cue,t);
  return <div style={{
    position:'absolute',left:140,right:140,bottom:52,textAlign:'center',zIndex:40,
    fontFamily:'Arial,Helvetica,sans-serif',fontWeight:760,fontSize:58,lineHeight:1.16,
    color:C.paper,textShadow:'0 4px 6px rgba(15,16,17,.96),0 0 18px rgba(15,16,17,.72)'
  }}>
    {cue.words.map((w,i)=><React.Fragment key={i}>
      <span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<cue.words.length-1?' ':''}
    </React.Fragment>)}
  </div>;
}

const splitTitle=(title)=>{
  const words=title.trim().split(/\s+/);
  if(words.length<=2)return [title];
  let best=1,score=1e9;
  for(let i=1;i<words.length;i++){
    const a=words.slice(0,i).join(' '),b=words.slice(i).join(' ');
    const s=Math.abs(a.length-b.length);
    if(s<score){score=s;best=i;}
  }
  return [words.slice(0,best).join(' '),words.slice(best).join(' ')];
};

function EditorialCard({card}){
  const frame=useCurrentFrame(),t=frame/FPS;
  const local=t-card.s;
  const dur=card.e-card.s;
  const op=Math.min(
    interpolate(local,[0,.28],[0,1],CLAMP),
    interpolate(local,[Math.max(.4,dur-.35),dur],[1,0],CLAMP)
  );
  const lines=splitTitle(card.title).slice(0,2);
  return <div style={{position:'absolute',left:84,top:68,width:1120,zIndex:20,opacity:op}}>
    <div style={{display:'flex',alignItems:'center',gap:20}}>
      <div style={{width:68,height:5,background:C.orange}}/>
      <div style={{fontFamily:'Arial,Helvetica,sans-serif',fontSize:21,fontWeight:650,letterSpacing:5,color:C.paper,textShadow:'0 2px 5px #000'}}>{card.kicker}</div>
    </div>
    <div style={{marginTop:30,fontFamily:"Georgia,'Times New Roman',serif",fontWeight:700,fontSize:card.kind==='fact'?70:88,lineHeight:.92,color:C.ivory,textShadow:'0 4px 10px rgba(0,0,0,.86)',WebkitTextStroke:'1.5px rgba(15,16,17,.84)'}}>
      {lines.map((x,i)=><div key={i}>{x}</div>)}
    </div>
    {card.subline&&<div style={{marginTop:22,fontFamily:'Arial,Helvetica,sans-serif',fontSize:25,fontWeight:750,letterSpacing:4,color:C.orange,whiteSpace:'pre-line',textShadow:'0 2px 5px #000'}}>{card.subline}</div>}
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
  const op=interpolate(frame,[Math.round(END_START*FPS),Math.round(END_START*FPS)+8],[0,1],CLAMP);
  return <AbsoluteFill style={{zIndex:50,opacity:op,background:C.charcoal}}>
    <Img src={staticFile('end_screen_1080.png')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  </AbsoluteFill>;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <Picture/>
    <Cards/>
    <Provenance/>
    <Caption/>
    <EndScreen/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="ChicagoR13" component={Film} durationInFrames={32268} fps={25} width={1920} height={1080}/>);
