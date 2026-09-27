import React from 'react';
import {AbsoluteFill, Audio, Composition, Img, interpolate, registerRoot, staticFile, useCurrentFrame} from 'remotion';
import timeline from '../public/timeline.json';
import captions from '../public/captions.json';
import overlays from '../public/overlays.json';
import motion from '../public/motion.json';

const FPS=timeline.fps;
const CONTENT_END=Math.round(timeline.duration*FPS);
const END_SCREEN_FRAMES=20*FPS;
const TOTAL=CONTENT_END+END_SCREEN_FRAMES;
const C={charcoal:'#171A1C',paper:'#FFFFFF',ivory:'#F3EBDD',orange:'#F28A3A',blue:'#708996',rust:'#A55235'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const smooth=x=>{const v=Math.max(0,Math.min(1,x));return v*v*(3-2*v)};
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
  let scale=1.035,x=0,y=0,origin='50% 50%';
  if(style==='push')scale=1.012+0.052*p;
  if(style==='pull')scale=1.072-0.047*p;
  if(style==='pan_left'){scale=1.085;x=1.45-2.9*p;}
  if(style==='pan_right'){scale=1.085;x=-1.45+2.9*p;}
  if(style==='tilt_up'){scale=1.075;y=1.35-2.7*p;}
  if(style==='tilt_down'){scale=1.075;y=-1.35+2.7*p;}
  if(style==='push_left'){scale=1.018+0.055*p;origin='30% 50%';x=.45-.45*p;}
  if(style==='push_right'){scale=1.018+0.055*p;origin='70% 50%';x=-.45+.45*p;}
  if(style==='hold_then_push'){const q=smooth(interpolate(p,[.38,1],[0,1],CLAMP));scale=1.025+0.042*q;}
  return {style,transform:`translate(${x}%,${y}%) scale(${scale})`,origin};
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

function Caption({frame}){
  const t=frame/FPS,cue=captions.find(x=>t>=x.s&&t<=x.e+.08);
  if(!cue)return null;
  let active=-1;for(let i=0;i<cue.words.length;i++){const w=cue.words[i];if(t>=w.s&&t<=Math.max(w.e,w.s+.06)){active=i;break}}
  return <div style={{position:'absolute',left:150,right:150,bottom:54,zIndex:70,textAlign:'center',fontFamily:'Arial,Helvetica,sans-serif',fontWeight:850,fontSize:55,lineHeight:1.12,color:C.paper,WebkitTextStroke:'1.2px rgba(8,10,11,.95)',textShadow:'0 4px 9px rgba(0,0,0,.98),0 0 21px rgba(0,0,0,.8)'}}>{cue.words.map((w,i)=><React.Fragment key={i}><span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<cue.words.length-1?' ':''}</React.Fragment>)}</div>;
}

function Picture({frame,beat}){
  const index=beatIndexById[beat.beat];
  const spec=motionByBeat[beat.beat]||{};
  if(index>0&&spec.transition_in==='dissolve'){
    const frames=spec.dissolve_frames||8;
    const p=smooth(interpolate(frame,[beat.a,beat.a+frames],[0,1],CLAMP));
    const previous=timeline.beats[index-1];
    return <AbsoluteFill style={{background:C.charcoal}}>
      <ImageBeat beat={previous} frame={previous.b-1} opacity={1-p}/>
      <ImageBeat beat={beat} frame={frame} opacity={p}/>
    </AbsoluteFill>;
  }
  return <ImageBeat beat={beat} frame={frame}/>;
}

function EditorialCard({card,frame}){
  const t=frame/FPS,dur=card.e-card.s,local=t-card.s;
  const op=Math.min(interpolate(local,[0,.22],[0,1],CLAMP),interpolate(local,[Math.max(.45,dur-.30),dur],[1,0],CLAMP));
  const y=interpolate(local,[0,.28],[10,0],CLAMP);
  const titleSize=card.title.length>28?54:(card.title.length>20?61:70);
  return <div style={{position:'absolute',left:88,top:72,width:1120,zIndex:45,opacity:op,transform:`translateY(${y}px)`,fontFamily:'Arial,Helvetica,sans-serif',textShadow:'0 4px 12px rgba(0,0,0,.95)'}}>
    <div style={{display:'flex',alignItems:'center',gap:18}}>
      <div style={{width:64,height:5,background:C.orange}}/>
      <div style={{fontSize:20,fontWeight:760,letterSpacing:4.3,color:C.paper}}>{card.kicker}</div>
    </div>
    <div style={{marginTop:24,fontWeight:850,fontSize:titleSize,lineHeight:.95,color:C.ivory}}>{card.title}</div>
    <div style={{marginTop:18,fontSize:23,fontWeight:760,letterSpacing:3.0,color:C.orange}}>{card.subline}</div>
  </div>;
}

function Cards({frame}){
  const t=frame/FPS,card=overlays.cards.find(x=>t>=x.s&&t<=x.e);
  return card?<EditorialCard card={card} frame={frame}/>:null;
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
    <Provenance beat={beat} frame={frame}/><Cards frame={frame}/><Caption frame={frame}/></>}
    <Audio src={staticFile('SATSOP_VO_MASTER_V1.wav')}/>
    <EndScreen frame={frame}/>
  </AbsoluteFill>;
}

registerRoot(()=><Composition id="SatsopV1" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080}/>);
