import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Sequence,Img,OffthreadVideo,staticFile,useCurrentFrame,interpolate} from 'remotion';
import timeline from '../public/timeline.json';
import captions from '../public/captions.json';

const FPS=30;
const C={charcoal:'#171A1C',paper:'#FFFFFF',ivory:'#F3EBDD',orange:'#F28A3A',rust:'#A55235',blue:'#5F747D'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const F=s=>Math.round(s*FPS);

function Still({item}){
  const f=useCurrentFrame();
  const n=Math.max(1,F(item.e-item.s)-1);
  const scale=item.motion==='push'?interpolate(f,[0,n],[1.002,1.014],CLAMP):1;
  return <AbsoluteFill style={{overflow:'hidden',background:C.charcoal}}>
    <Img src={staticFile(item.file)} style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${scale})`,transformOrigin:'50% 50%'}}/>
  </AbsoluteFill>;
}

function Picture(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <Sequence from={0} durationInFrames={F(timeline.cut)}>
      <OffthreadVideo src={staticFile('cold_picture_1080.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    </Sequence>
    {timeline.shots.map(s=><Sequence key={'s'+s.idx} from={F(s.s)} durationInFrames={Math.max(1,F(s.e)-F(s.s))} premountFor={8}>
      <Still item={s}/>
    </Sequence>)}
    {timeline.overrides.map(o=><Sequence key={'o'+o.i} from={F(o.s)} durationInFrames={Math.max(1,F(o.e)-F(o.s))} premountFor={8}>
      <Still item={o}/>
    </Sequence>)}
  </AbsoluteFill>;
}

const currentVisual=(t)=>{
  const ov=timeline.overrides.find(x=>t>=x.s&&t<x.e);
  if(ov)return {...ov,isOverride:true};
  const s=timeline.shots.find(x=>t>=x.s&&t<x.e);
  return s||null;
};

function Provenance(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<timeline.cut || t>=timeline.endScreen)return null;
  const v=currentVisual(t);
  if(!v||!v.provenance)return null;
  const start=v.s;
  const local=t-start;
  if(local>1.55)return null;
  const op=Math.min(interpolate(local,[0,.16],[0,1],CLAMP),interpolate(local,[1.18,1.55],[1,0],CLAMP));
  const accent=v.provenance==='HISTORICAL SOURCE'?C.orange:(v.provenance==='DOCUMENT'?C.ivory:(v.provenance==='CONCEPT'?C.rust:C.blue));
  return <div style={{position:'absolute',right:56,top:44,zIndex:40,opacity:op,fontFamily:'Arial,Helvetica,sans-serif',fontSize:20,fontWeight:700,letterSpacing:3.2,color:C.ivory,textShadow:'0 2px 6px rgba(0,0,0,.85)'}}>
    <span style={{display:'inline-block',width:36,height:4,background:accent,marginRight:14,verticalAlign:'middle'}}/>
    {v.provenance}
  </div>;
}

function Caption(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<timeline.cut||t>=timeline.endScreen)return null;
  const p=captions.find(x=>t>=x.s&&t<=x.e);
  if(!p)return null;
  const active=p.words.findIndex(w=>t>=w.s&&t<=Math.max(w.e,w.s+.06));
  return <div style={{position:'absolute',left:140,right:140,bottom:52,zIndex:50,textAlign:'center',fontFamily:'Arial,Helvetica,sans-serif',fontWeight:760,fontSize:58,lineHeight:1.16,color:C.paper,textShadow:'0 4px 7px rgba(23,26,28,.98),0 0 18px rgba(23,26,28,.72)'}}>
    {p.words.map((w,i)=><React.Fragment key={i}><span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<p.words.length-1?' ':''}</React.Fragment>)}
  </div>;
}

function Editorial(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<timeline.cut||t>=timeline.endScreen)return null;
  const s=timeline.shots.find(x=>t>=x.s&&t<x.e);
  if(!s)return null;
  const local=t-s.s;
  const showChapter=s.chapter_start && local<2.45;
  const showTag=!!s.tagText && local>=.15 && local<3.0;
  if(!showChapter&&!showTag)return null;
  const op=interpolate(local,[.05,.25],[0,1],CLAMP);
  return <div style={{position:'absolute',left:104,top:84,zIndex:30,opacity:op,color:C.ivory,textShadow:'0 3px 8px rgba(0,0,0,.86)'}}>
    {showChapter&&<>
      <div style={{fontFamily:'Arial,Helvetica,sans-serif',fontSize:20,fontWeight:700,letterSpacing:4,color:C.orange}}>HIDDEN INDUSTRIAL AMERICA</div>
      <div style={{marginTop:14,fontFamily:'Arial,Helvetica,sans-serif',fontSize:52,fontWeight:800,letterSpacing:1.2}}>{s.chapterTitle}</div>
    </>}
    {showTag&&!showChapter&&<div style={{fontFamily:'Arial,Helvetica,sans-serif',fontSize:38,fontWeight:760,letterSpacing:1.4}}>
      <span style={{display:'inline-block',width:50,height:4,background:C.rust,marginRight:16,verticalAlign:'middle'}}/>{s.tagText}
    </div>}
  </div>;
}

function EndScreen(){
  const t=useCurrentFrame()/FPS;
  if(t<timeline.endScreen)return null;
  return <AbsoluteFill style={{zIndex:80,background:C.charcoal}}>
    <Img src={staticFile('end_screen_1080.png')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  </AbsoluteFill>;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <Picture/>
    <Editorial/>
    <Provenance/>
    <Caption/>
    <EndScreen/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="TC497R14Reedit" component={Film} durationInFrames={37096} fps={30} width={1920} height={1080}/>);
