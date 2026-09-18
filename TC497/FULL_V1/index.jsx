import React from 'react';
import {registerRoot,Composition,AbsoluteFill,OffthreadVideo,Audio,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import captions from '../public/captions.json';
import events from '../public/events.json';

const FPS=30;
const CUT=82.6;
const END=1236.506;
const C={charcoal:'#171A1C',iron:'#30363A',paper:'#E6DDC8',ivory:'#F3EBDD',rust:'#A55235',blue:'#5F747D'};
const F=(s)=>Math.round(s*FPS);
const fade=(frame,s,e,edge=5)=>interpolate(frame,[F(s),F(s)+edge,F(e)-edge,F(e)],[0,1,1,0],{
  extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)
});

function findActive(arr,t){
  let lo=0,hi=arr.length-1;
  while(lo<=hi){
    const mid=(lo+hi)>>1, x=arr[mid];
    if(t<x.s) hi=mid-1;
    else if(t>x.e) lo=mid+1;
    else return x;
  }
  return null;
}

const keywordSet=new Set([
  '572','54','150','20','400','12-foot','12-ft','1963','1968','gas','turbines',
  'nuclear','helicopter','helicopters','worked','scrapped','sky','otter','yuma'
]);

function Caption(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<CUT)return null;
  const p=findActive(captions,t);
  if(!p)return null;
  return <div style={{
    position:'absolute',left:72,right:72,bottom:26,textAlign:'center',
    fontFamily:'Montserrat,Arial,sans-serif',fontWeight:700,fontSize:27,lineHeight:1.18,
    color:C.paper,textShadow:'0 2px 3px rgba(23,26,28,.96),0 0 9px rgba(23,26,28,.72)',
    opacity:fade(frame,p.s,p.e,3)
  }}>
    {p.words.map((w,i)=>{
      const clean=w.w.replace(/[.,!?;:()"']/g,'').toLowerCase();
      const hi=keywordSet.has(clean);
      return <React.Fragment key={i}><span style={{color:hi?C.rust:C.paper}}>{w.w}</span>{i<p.words.length-1?' ':''}</React.Fragment>;
    })}
  </div>;
}

function Chapter(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const e=findActive(events.chapters,t);
  if(!e)return null;
  return <div style={{
    position:'absolute',left:46,top:38,opacity:fade(frame,e.s,e.e,5),
    fontFamily:'Montserrat,Arial',textTransform:'uppercase'
  }}>
    <div style={{fontSize:12,fontWeight:750,letterSpacing:2.2,color:C.rust}}>HIDDEN INDUSTRIAL AMERICA</div>
    <div style={{marginTop:8,fontSize:29,fontWeight:800,letterSpacing:.5,color:C.ivory,
      textShadow:'0 3px 8px rgba(23,26,28,.78)'}}>{e.text}</div>
    <div style={{marginTop:9,width:126,height:3,background:C.blue}}/>
  </div>;
}

function SourceBug(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const e=findActive(events.bugs,t);
  if(!e)return null;
  const concept=e.text==='CONCEPT';
  return <div style={{
    position:'absolute',right:28,top:24,opacity:fade(frame,e.s,e.e,4),
    fontFamily:'Montserrat,Arial',fontSize:11,fontWeight:700,letterSpacing:1.2,
    color:concept?C.ivory:C.charcoal,
    background:concept?'rgba(165,82,53,.88)':'rgba(230,221,200,.90)',
    padding:'6px 9px 5px'
  }}>{e.text}</div>;
}

function Payoff(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=1088.4&&t<=1095.7){
    return <div style={{
      position:'absolute',left:70,right:70,top:165,textAlign:'center',
      opacity:fade(frame,1088.4,1095.7,8),
      fontFamily:'Montserrat,Arial',fontWeight:850,fontSize:43,lineHeight:1.04,
      letterSpacing:.6,color:C.ivory,textShadow:'0 3px 12px rgba(23,26,28,.82)'
    }}>
      <div>IT WASN'T DEFEATED BY THE DESERT.</div>
      <div style={{color:C.rust,marginTop:7}}>IT WAS DEFEATED BY THE SKY.</div>
    </div>;
  }
  if(t>=1228.1&&t<=1236.3){
    return <div style={{
      position:'absolute',left:55,top:105,width:420,opacity:fade(frame,1228.1,1236.3,8),
      fontFamily:'Montserrat,Arial',color:C.charcoal
    }}>
      <div style={{fontSize:12,fontWeight:800,letterSpacing:2.2,color:C.blue}}>HIDDEN INDUSTRIAL AMERICA</div>
      <div style={{fontSize:34,fontWeight:850,lineHeight:1.05,marginTop:13}}>THE MACHINE WORKED.</div>
      <div style={{fontSize:34,fontWeight:850,lineHeight:1.05,color:C.rust}}>THE WORLD MOVED ON.</div>
      <div style={{width:250,height:3,background:C.rust,marginTop:17}}/>
    </div>;
  }
  return null;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <OffthreadVideo src={staticFile('full_base.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    <Chapter/>
    <SourceBug/>
    <Payoff/>
    <Caption/>
    <Audio src={staticFile('full_mix.wav')} volume={1}/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="TC497FullV1" component={Film} durationInFrames={37095} fps={30} width={960} height={540}/>);
