import React from 'react';
import {registerRoot,Composition,AbsoluteFill,OffthreadVideo,Audio,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import captions from '../public/captions.json';

const FPS=30;
const C={charcoal:'#171A1C',iron:'#30363A',paper:'#E6DDC8',ivory:'#F3EBDD',rust:'#A55235',blue:'#5F747D'};
const F=(s)=>Math.round(s*FPS);
const fade=(frame,s,e,edge=4)=>interpolate(frame,[F(s),F(s)+edge,F(e)-edge,F(e)],[0,1,1,0],{
  extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)
});

function Caption(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const p=captions.find(x=>t>=x.s&&t<=x.e);
  if(!p)return null;
  const words=p.words||[];
  let active=0;
  const timed=words.length&&words.every(w=>typeof w.s==='number'&&typeof w.e==='number');
  if(timed){
    const hit=words.findIndex(w=>t>=w.s&&t<=w.e);
    active=hit>=0?hit:Math.max(0,words.findIndex(w=>t<w.s)-1);
    if(active<0)active=words.length-1;
  }else if(words.length){
    const prog=Math.max(0,Math.min(.999,(t-p.s)/Math.max(.08,p.e-p.s)));
    active=Math.min(words.length-1,Math.floor(prog*words.length));
  }
  return <div style={{
    position:'absolute',left:66,right:66,bottom:27,textAlign:'center',
    fontFamily:'Montserrat,Arial,sans-serif',fontWeight:750,fontSize:27,lineHeight:1.18,
    color:C.paper,textShadow:'0 2px 3px rgba(23,26,28,.98),0 0 9px rgba(23,26,28,.82)',
    opacity:fade(frame,p.s,p.e,2)
  }}>
    {words.map((w,i)=><React.Fragment key={i}>
      <span style={{color:i===active?'#D97932':C.paper}}>{w.w}</span>{i<words.length-1?' ':''}
    </React.Fragment>)}
  </div>;
}

function ReconBug(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>1.95)return null;
  return <div style={{
    position:'absolute',right:28,top:22,opacity:fade(frame,.08,1.92,4),
    fontFamily:'Montserrat,Arial',fontSize:11,fontWeight:650,letterSpacing:1.3,
    color:C.paper,background:'rgba(23,26,28,.58)',padding:'5px 8px 4px'
  }}>RECONSTRUCTION</div>;
}

function Measurement(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<13.15||t>16.90)return null;
  const op=fade(frame,13.15,16.90,5);
  const grow=interpolate(frame,[F(13.30),F(13.82)],[0,1],{
    extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)
  });
  return <div style={{position:'absolute',left:108,right:108,top:112,opacity:op}}>
    <div style={{height:2,width:`${grow*100}%`,background:C.blue,opacity:.74,position:'relative'}}>
      {[0,25,50,75,100].map((x,i)=><span key={i} style={{position:'absolute',left:`${x}%`,top:-5,width:1,height:12,background:C.blue}}/>)}
    </div>
    <div style={{marginTop:11,fontFamily:'Montserrat,Arial',fontWeight:800,fontSize:53,letterSpacing:1.4,color:C.rust,textShadow:'0 3px 9px rgba(23,26,28,.72)'}}>572 FEET</div>
  </div>;
}

function WheelBeat(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<23.20||t>26.20)return null;
  return <div style={{position:'absolute',left:74,top:86,opacity:fade(frame,23.20,26.20,4),fontFamily:'Montserrat,Arial',color:C.ivory}}>
    <div style={{fontWeight:800,fontSize:24,letterSpacing:1.05}}>54 DRIVEN WHEELS</div>
    <div style={{marginTop:8,fontSize:12,letterSpacing:1.1,color:C.paper}}>
      <span style={{display:'inline-block',width:36,height:2,background:C.rust,marginRight:9,verticalAlign:'middle'}}/>
      ELECTRIC DRIVE • DISTRIBUTED POWER
    </div>
  </div>;
}

function ArchiveTag(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=33.04&&t<=35.70)return <div style={{
    position:'absolute',right:34,top:24,opacity:fade(frame,33.10,35.70,4),
    fontFamily:'Montserrat,Arial',fontWeight:650,fontSize:12,letterSpacing:1.15,
    color:C.iron,background:'rgba(191,179,155,.91)',padding:'6px 9px 5px'
  }}>ARCHIVE • U.S. ARMY / YUMA</div>;
  if(t>=53.88&&t<=57.05)return <div style={{
    position:'absolute',right:34,top:24,opacity:fade(frame,53.96,57.05,4),
    fontFamily:'Montserrat,Arial',fontWeight:650,fontSize:12,letterSpacing:1.10,
    color:C.iron,background:'rgba(179,167,143,.92)',padding:'6px 9px 5px'
  }}>PROJECT OTTER • TEST REPORT • 1963</div>;
  return null;
}

function InfoLabels(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const items=[
    {s:18.05,e:20.15,text:'13 UNITS'},
    {s:28.65,e:31.10,text:'~150 TONS OF CARGO'},
    {s:36.04,e:37.18,text:'NO RAILROAD'},
    {s:37.42,e:38.56,text:'NO RAILS'},
    {s:38.80,e:40.02,text:'NO PREPARED HIGHWAY'},
    {s:48.25,e:50.55,text:'TC-497 OVERLAND TRAIN • MARK II'},
    {s:57.35,e:59.75,text:'LONGEST RUBBER-TIRED VEHICLE'}
  ];
  const x=items.find(a=>t>=a.s&&t<=a.e);
  if(!x)return null;
  return <div style={{
    position:'absolute',left:58,top:84,opacity:fade(frame,x.s,x.e,4),
    fontFamily:'Montserrat,Arial',fontWeight:750,fontSize:20,letterSpacing:1,color:C.ivory,
    textShadow:'0 2px 7px rgba(23,26,28,.68)'
  }}><span style={{display:'inline-block',width:31,height:2,background:C.rust,marginRight:9,verticalAlign:'middle'}}/>{x.text}</div>;
}

function YumaBuild(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=68.95&&t<=70.85)return <div style={{
    position:'absolute',left:58,top:84,opacity:fade(frame,68.95,70.85,4),
    fontFamily:'Montserrat,Arial',color:C.ivory
  }}>
    <div style={{fontWeight:800,fontSize:21,letterSpacing:1}}>YUMA PROVING GROUND</div>
    <div style={{fontSize:12,letterSpacing:1.15,marginTop:6,color:C.paper}}>DESERT TEST • U.S. ARMY</div>
  </div>;
  if(t>=71.08&&t<=74.35)return <div style={{
    position:'absolute',left:58,top:84,opacity:fade(frame,71.08,74.35,4),
    fontFamily:'Montserrat,Arial',fontWeight:750,fontSize:19,letterSpacing:1,color:C.ivory
  }}><span style={{display:'inline-block',width:32,height:2,background:C.rust,marginRight:9,verticalAlign:'middle'}}/>TESTED OFF ROAD</div>;
  return null;
}

function Payoff(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t>=74.90&&t<=77.70)return <div style={{
    position:'absolute',left:65,right:65,top:158,textAlign:'center',opacity:fade(frame,74.90,77.70,5),
    fontFamily:'Montserrat,Arial',fontWeight:800,fontSize:50,letterSpacing:1.15,color:C.ivory,
    textShadow:'0 3px 10px rgba(23,26,28,.78)'
  }}>IT WORKED.</div>;
  if(t>=79.00&&t<=80.70)return <div style={{
    position:'absolute',left:65,right:65,top:158,textAlign:'center',opacity:fade(frame,79.00,80.70,5),
    fontFamily:'Montserrat,Arial',fontWeight:800,fontSize:46,letterSpacing:1.05,color:C.rust,
    textShadow:'0 3px 10px rgba(23,26,28,.80)'
  }}>SCRAPPED IT ANYWAY.</div>;
  return null;
}

function Mood(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<78.92||t>=80.84)return null;
  const o=interpolate(t,[78.92,80.84],[.035,.11],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <AbsoluteFill style={{backgroundColor:`rgba(23,26,28,${o})`}}/>;
}

function Title(){
  const frame=useCurrentFrame(),t=frame/FPS;
  if(t<80.90||t>82.58)return null;
  return <div style={{
    position:'absolute',left:54,right:54,top:92,textAlign:'center',opacity:fade(frame,80.90,82.58,5),
    fontFamily:'Montserrat,Arial',color:C.charcoal,
    textShadow:'0 1px 0 rgba(243,235,221,.28)'
  }}>
    <div style={{fontSize:12,fontWeight:750,letterSpacing:2.3,color:C.blue,marginBottom:12}}>HIDDEN INDUSTRIAL AMERICA</div>
    <div style={{fontWeight:850,fontSize:43,lineHeight:1.03,letterSpacing:.35}}>AMERICA BUILT A 572-FOOT TRAIN</div>
    <div style={{fontWeight:850,fontSize:43,lineHeight:1.03,letterSpacing:.35}}>THAT NEEDED NO TRACKS</div>
    <div style={{height:3,width:365,background:C.rust,margin:'17px auto 0'}}/>
  </div>;
}

const Film=()=> <AbsoluteFill style={{background:C.charcoal}}>
  <OffthreadVideo src={staticFile('base.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  <Mood/>
  <ReconBug/>
  <ArchiveTag/>
  <Measurement/>
  <WheelBeat/>
  <InfoLabels/>
  <YumaBuild/>
  <Payoff/>
  <Title/>
  <Caption/>
  <Audio src={staticFile('mix.wav')} volume={1}/>
</AbsoluteFill>;

registerRoot(()=> <Composition id="TC497V14" component={Film} durationInFrames={2478} fps={30} width={960} height={540}/>);
