import React from 'react';
import {registerRoot,Composition,AbsoluteFill,Sequence,Img,staticFile,useCurrentFrame,interpolate} from 'remotion';
import timeline from './timeline.json';

const FPS=25;
const TOTAL=35660;
const C={charcoal:'#171A1C',iron:'#30363A',paper:'#E6DDC8',ivory:'#F3EBDD',rust:'#A55235',blue:'#5F747D',white:'#FFFFFF'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const REPL=new Set(['FX001','FX002','FX013','FX016','FX033','FX036','FX045','FX047','FX048','FX049']);
const NO_DISSOLVE=new Set(['B033','B034','B035','B036','B037','B038','B039','B040']);
const DENSE=new Set(['B010','B011','B012','B013','B014','B015','B016','B066','B067','B068','B069','B070','B071','B072','B073','B081','B082','B083','B084','B085','B086','B087','B088','B089','B113','B114','B115']);

const focusMap={
 B011:[[18,27,30,52],[55,27,30,52]],
 B013:[[1,18,24,64],[25,18,24,64],[50,18,24,64],[75,18,24,64]],
 B014:[[15,22,28,56],[57,22,28,56]],
 B015:[[2,20,23,62],[27,20,22,62],[51,20,22,62],[75,20,23,62]],
 B016:[[35,20,30,62]],
 B067:[[52,15,38,58]],
 B068:[[3,22,94,54]],
 B070:[[36,20,30,58]],
 B071:[[38,14,35,64]],
 B072:[[35,15,32,62]],
 B073:[[3,18,46,66],[51,18,46,66]],
 B081:[[2,12,96,46],[32,48,36,38]],
 B082:[[2,14,52,70],[58,14,40,70]],
 B084:[[1,10,45,80],[49,10,50,80]],
 B086:[[2,22,30,55],[35,22,30,55],[68,22,30,55]],
 B087:[[2,22,30,58],[35,22,30,58],[68,22,30,58]],
 B088:[[2,18,23,58],[27,18,22,58],[51,18,22,58],[75,18,23,58]],
 B089:[[2,14,96,72]],
 B113:[[15,10,70,75]],B114:[[12,10,76,75]],B115:[[12,10,76,75]]
};

const special={
 B033:{s0:1.025,s1:1.035,origin:'60% 52%'},
 B034:{s0:1.000,s1:1.008,origin:'50% 50%'},
 B036:{s0:1.030,s1:1.040,origin:'72% 66%'},
 B037:{s0:1.018,s1:1.030,origin:'64% 55%'},
 B039:{s0:1.030,s1:1.040,origin:'30% 52%'},
 B040:{s0:1.015,s1:1.025,origin:'67% 48%'},
 B038:{s0:2.65,s1:2.72,origin:'50% 48%',doc:'HOIST MECHANISM'},
 B041:{s0:2.55,s1:2.62,origin:'50% 54%',doc:'MAIN-MOTION ENGINEERING'},
 B051:{s0:2.45,s1:2.52,origin:'50% 48%',doc:'WALKING SHOE MECHANISM'},
 B052:{s0:2.45,s1:2.52,origin:'50% 52%',doc:'STEPPING PROPULSION'},
 B083:{s0:1.12,s1:1.15,origin:'50% 48%',doc:'1990 CLEAN AIR ACT AMENDMENTS'},
 B085:{s0:1.12,s1:1.15,origin:'50% 48%',doc:'PHASE I COMPLIANCE — 1995'},
 B102:{s0:1.00,s1:1.006,origin:'50% 50%'},
 B104:{s0:1.075,s1:1.085,origin:'66% 46%'},
 B105:{s0:1.00,s1:1.006,origin:'50% 50%'},
 B107:{s0:1.085,s1:1.095,origin:'35% 52%'},
 B109:{s0:1.00,s1:1.006,origin:'50% 50%'},
 B112:{s0:1.080,s1:1.090,origin:'70% 55%'},
 B116:{s0:1.000,s1:1.010,origin:'50% 50%'}
};

const transitionFrames=(item)=>NO_DISSOLVE.has(item.beat)?0:(DENSE.has(item.beat)?3:2);

function FocusOverlay({beat,duration}){
 const steps=focusMap[beat];
 const frame=useCurrentFrame();
 if(!steps||!steps.length)return null;
 const n=Math.max(1,duration);
 const idx=Math.min(steps.length-1,Math.floor((frame/n)*steps.length));
 const [x,y,w,h]=steps[idx];
 const phase=(frame/n)*steps.length-idx;
 const fade=Math.min(1,Math.min(phase*5,(1-phase)*5+0.15));
 return <AbsoluteFill style={{pointerEvents:'none',zIndex:10}}>
   <div style={{position:'absolute',left:`${x}%`,top:`${y}%`,width:`${w}%`,height:`${h}%`,
     boxShadow:'0 0 0 9999px rgba(23,26,28,.18)',border:'1px solid rgba(230,221,200,.14)',
     opacity:0.65*fade,borderRadius:4}}/>
 </AbsoluteFill>;
}

function DocumentTag({title}){
 return <div style={{position:'absolute',left:64,top:54,zIndex:15,fontFamily:'Arial Narrow,Arial,sans-serif',color:C.ivory,
   textShadow:'0 3px 10px rgba(0,0,0,.95)'}}>
   <div style={{fontSize:17,letterSpacing:4,fontWeight:800,color:C.blue}}>DOCUMENT — ENGINEERING LINEAGE</div>
   <div style={{marginTop:10,fontSize:38,letterSpacing:1.2,fontWeight:900}}>{title}</div>
 </div>;
}

function FailurePath(){
 const frame=useCurrentFrame();
 const p=interpolate(frame,[0,18],[0,1],CLAMP);
 const items=['COMPONENT FAULT','MACHINE UNAVAILABLE','STRIPPING SYSTEM AFFECTED'];
 return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden'}}>
   <Img src={staticFile('beats/beat_076.png')} style={{width:'100%',height:'100%',objectFit:'cover',filter:'grayscale(.45) brightness(.35)',transform:'scale(1.02)'}}/>
   <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(23,26,28,.92),rgba(23,26,28,.72),rgba(23,26,28,.88))'}}/>
   <div style={{position:'absolute',left:100,right:100,top:130,color:C.ivory,fontFamily:'Arial Narrow,Arial,sans-serif'}}>
    <div style={{fontSize:24,letterSpacing:5,color:C.rust,fontWeight:800,opacity:p}}>THE FAILURE PATH</div>
    <div style={{fontSize:72,fontWeight:900,marginTop:12,lineHeight:.96,opacity:p}}>ONE BREAK CAN BECOME<br/>A SYSTEM PROBLEM</div>
    <div style={{display:'flex',alignItems:'center',gap:24,marginTop:78}}>
     {items.map((x,i)=><React.Fragment key={x}>
       <div style={{flex:1,minHeight:150,borderTop:`5px solid ${i===0?C.rust:C.blue}`,padding:'24px 20px',background:'rgba(48,54,58,.62)',
         opacity:interpolate(frame,[10+i*10,22+i*10],[0,1],CLAMP)}}>
         <div style={{fontSize:22,letterSpacing:2,color:C.paper}}>0{i+1}</div>
         <div style={{fontSize:34,fontWeight:900,marginTop:16,lineHeight:1.0}}>{x}</div>
       </div>
       {i<2&&<div style={{fontSize:54,color:C.rust,opacity:interpolate(frame,[18+i*10,30+i*10],[0,1],CLAMP)}}>→</div>}
     </React.Fragment>)}
    </div>
   </div>
 </AbsoluteFill>;
}

function SurvivingParts(){
 const frame=useCurrentFrame();
 const p=interpolate(frame,[0,18],[0,1],CLAMP);
 return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden'}}>
   <Img src={staticFile('beats/beat_105.png')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',transform:'scale(1.035)',filter:'brightness(.48) saturate(.82)'}}/>
   <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(23,26,28,.22) 0%,rgba(23,26,28,.58) 48%,rgba(23,26,28,.94) 100%)'}}/>
   <div style={{position:'absolute',left:96,top:92,right:96,fontFamily:'Arial Narrow,Arial,sans-serif',color:C.ivory,opacity:p}}>
     <div style={{fontSize:22,letterSpacing:5,color:C.rust,fontWeight:800}}>WHAT SURVIVED</div>
     <div style={{fontSize:64,fontWeight:900,lineHeight:.98,marginTop:14}}>THE BUCKET WAS NOT<br/>THE ONLY MATERIAL LEFT</div>
   </div>
   <div style={{position:'absolute',right:110,top:420,width:620,fontFamily:'Arial Narrow,Arial,sans-serif',color:C.ivory}}>
     {['SECTIONS OF CABLE','CHAIN','A BUCKET TOOTH'].map((x,i)=><div key={x} style={{display:'flex',alignItems:'center',gap:22,padding:'20px 0',borderTop:'1px solid rgba(230,221,200,.28)',opacity:interpolate(frame,[10+i*9,24+i*9],[0,1],CLAMP)}}>
       <div style={{fontSize:18,letterSpacing:3,color:C.blue}}>0{i+1}</div><div style={{fontSize:34,fontWeight:900,letterSpacing:1.2}}>{x}</div>
     </div>)}
   </div>
 </AbsoluteFill>;
}

function Visual({item,duration}){
 const frame=useCurrentFrame();
 if(item.beat==='B076')return <FailurePath/>;
 if(item.beat==='B106')return <SurvivingParts/>;
 const sp=special[item.beat]||{};
 const isDoc=!!sp.doc;
 const defaultDrift=item.class==='RECONSTRUCTION'?0.010:(item.class==='GFX'?0.004:0.006);
 const s0=sp.s0??1.0, s1=sp.s1??(1+defaultDrift);
 const scale=interpolate(frame,[0,Math.max(1,duration-1)],[s0,s1],CLAMP);
 const src=REPL.has(item.asset)?`${item.asset}.png`:item.beatFile;
 return <AbsoluteFill style={{overflow:'hidden',background:C.charcoal}}>
   <Img src={staticFile(src)} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',
      transform:`scale(${scale})`,transformOrigin:sp.origin||'50% 50%'}}/>
   {isDoc&&<><AbsoluteFill style={{background:'linear-gradient(180deg,rgba(23,26,28,.18),transparent 28%,transparent 72%,rgba(23,26,28,.15))'}}/><DocumentTag title={sp.doc}/></>}
   <FocusOverlay beat={item.beat} duration={duration}/>
 </AbsoluteFill>;
}

function Beat({item,index}){
 const tf=transitionFrames(item);
 const first=index===0,last=index===timeline.length-1;
 const from=Math.max(0,item.startFrame-(first?0:tf));
 const to=Math.min(TOTAL,item.endFrame+(last?0:tf));
 const duration=Math.max(1,to-from);
 return <Sequence from={from} durationInFrames={duration} premountFor={4}>
   <BeatInner item={item} duration={duration} tf={tf} first={first} last={last}/>
 </Sequence>;
}

function BeatInner({item,duration,tf,first,last}){
 const f=useCurrentFrame();
 let opacity=1;
 if(tf>0&&!first) opacity=Math.min(opacity,interpolate(f,[0,tf*2],[0,1],CLAMP));
 if(tf>0&&!last) opacity=Math.min(opacity,interpolate(f,[Math.max(0,duration-tf*2),duration],[1,0],CLAMP));
 return <AbsoluteFill style={{opacity}}><Visual item={item} duration={duration}/></AbsoluteFill>;
}

function Film(){
 return <AbsoluteFill style={{background:C.charcoal}}>
   {timeline.map((item,i)=><Beat key={item.beat} item={item} index={i}/>)}
 </AbsoluteFill>;
}

registerRoot(()=> <Composition id="BigMuskieV3" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080}/>);