import React from 'react';
import {AbsoluteFill, Audio, Composition, Img, interpolate, registerRoot, staticFile, useCurrentFrame} from 'remotion';
import timeline from '../public/timeline.json';
import captions from '../public/captions.json';

const FPS=timeline.fps;
const TOTAL=Math.round(timeline.duration*FPS);
const C={charcoal:'#171A1C',paper:'#FFFFFF',ivory:'#F3EBDD',orange:'#F28A3A',blue:'#708996',rust:'#A55235'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const smooth=x=>{const v=Math.max(0,Math.min(1,x));return v*v*(3-2*v)};

function currentBeat(frame){
  let lo=0,hi=timeline.beats.length-1;
  while(lo<=hi){const m=(lo+hi)>>1,b=timeline.beats[m];if(frame<b.a)hi=m-1;else if(frame>=b.b)lo=m+1;else return b;}
  return timeline.beats[Math.max(0,Math.min(timeline.beats.length-1,lo))];
}

function ImageBeat({beat,frame}){
  const p=smooth(interpolate(frame,[beat.a,Math.max(beat.a+1,beat.b-1)],[0,1],CLAMP));
  const isGfx=beat.kind==='gfx';
  const scale=isGfx?1:1.025+0.035*p;
  const x=isGfx?0:beat.direction*interpolate(p,[0,1],[-0.55,0.55]);
  const fade=Math.min(interpolate(frame,[beat.a,beat.a+6],[0,1],CLAMP),interpolate(frame,[beat.b-6,beat.b],[1,0],CLAMP));
  return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden',opacity:fade}}>
    <Img src={staticFile(beat.file)} style={{width:'100%',height:isGfx?'900px':'100%',objectFit:isGfx?'contain':'cover',objectPosition:'center top',transform:`translateX(${x}%) scale(${scale})`,transformOrigin:'50% 50%'}}/>
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
  if(beat.kind!=='generated'&&beat.kind!=='document')return null;
  const local=(frame-beat.a)/FPS,dur=(beat.b-beat.a)/FPS;
  if(local>Math.min(2.4,dur))return null;
  const op=Math.min(interpolate(local,[0,.18],[0,1],CLAMP),interpolate(local,[Math.min(1.85,dur-.25),Math.min(2.4,dur)],[1,0],CLAMP));
  const label=beat.kind==='generated'?'AI RECONSTRUCTION':'DOCUMENT';
  return <div style={{position:'absolute',right:50,top:38,zIndex:40,opacity:op,fontFamily:'Arial,Helvetica,sans-serif',fontSize:23,fontWeight:850,letterSpacing:3,color:C.ivory,textShadow:'0 2px 8px #000'}}><span style={{display:'inline-block',width:40,height:5,background:beat.kind==='generated'?C.blue:C.rust,marginRight:13,verticalAlign:'middle'}}/>{label}</div>;
}

function Caption({frame}){
  const t=frame/FPS,cue=captions.find(x=>t>=x.s&&t<=x.e+.08);
  if(!cue)return null;
  let active=-1;for(let i=0;i<cue.words.length;i++){const w=cue.words[i];if(t>=w.s&&t<=Math.max(w.e,w.s+.06)){active=i;break}}
  return <div style={{position:'absolute',left:150,right:150,bottom:54,zIndex:70,textAlign:'center',fontFamily:'Arial,Helvetica,sans-serif',fontWeight:850,fontSize:55,lineHeight:1.12,color:C.paper,WebkitTextStroke:'1.2px rgba(8,10,11,.95)',textShadow:'0 4px 9px rgba(0,0,0,.98),0 0 21px rgba(0,0,0,.8)'}}>{cue.words.map((w,i)=><React.Fragment key={i}><span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<cue.words.length-1?' ':''}</React.Fragment>)}</div>;
}

function Film(){
  const frame=useCurrentFrame(),beat=currentBeat(frame);
  return <AbsoluteFill style={{background:C.charcoal}}>
    {beat.kind==='document'?<DocumentBeat beat={beat} frame={frame}/>:<ImageBeat beat={beat} frame={frame}/>} 
    <Provenance beat={beat} frame={frame}/><Caption frame={frame}/>
    <Audio src={staticFile('SATSOP_VO_MASTER_V1.wav')}/>
  </AbsoluteFill>;
}

registerRoot(()=><Composition id="SatsopV1" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080}/>);
