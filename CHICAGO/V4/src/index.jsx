import React from 'react';
import {
  registerRoot, Composition, AbsoluteFill, OffthreadVideo, staticFile,
  useCurrentFrame, interpolate, Easing, spring
} from 'remotion';
import captions from '../public/captions.json';
import overlays from '../public/overlays.json';

const FPS=25;
const F=(s)=>Math.round(s*FPS);
const C={
  charcoal:'#171A1C',
  iron:'#30363A',
  paper:'#E8E0D0',
  ivory:'#F5EFE4',
  orange:'#F28A3A',
  muted:'#A8AAA6',
  muted2:'#777E80'
};

const fade=(frame,s,e,edge=6)=>interpolate(
  frame,[F(s),F(s)+edge,F(e)-edge,F(e)],[0,1,1,0],
  {extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)}
);

const enter=(frame,s)=>{
  const local=Math.max(0,frame-F(s));
  return spring({fps:FPS,frame:local,config:{damping:18,stiffness:115,mass:.72}});
};

const activeWord=(cue,t)=>{
  let idx=-1;
  for(let i=0;i<cue.words.length;i++){
    const w=cue.words[i];
    if(t>=w.s && t<=Math.max(w.e,w.s+.06)){idx=i;break;}
  }
  return idx;
};

function Caption(){
  const frame=useCurrentFrame();
  const t=frame/FPS;
  const cue=captions.find(x=>t>=x.s&&t<=x.e);
  if(!cue)return null;
  const active=activeWord(cue,t);
  const endMode=t>=1270;
  return <div style={{
    position:'absolute',
    left:72,right:72,
    top:endMode?48:undefined,
    bottom:endMode?undefined:28,
    textAlign:'center',
    fontFamily:'Arial,Helvetica,sans-serif',
    fontWeight:700,
    fontSize:endMode?27:29,
    lineHeight:1.18,
    color:C.paper,
    textShadow:'0 2px 3px rgba(23,26,28,.95), 0 0 8px rgba(23,26,28,.70)',
    opacity:fade(frame,cue.s,cue.e,3),
    zIndex:20
  }}>
    {cue.words.map((w,i)=><React.Fragment key={i}>
      <span style={{color:i===active?C.orange:C.paper}}>{w.w}</span>{i<cue.words.length-1?' ':''}
    </React.Fragment>)}
  </div>;
}

function Provenance(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const p=overlays.provenance.find(x=>t>=x.s&&t<=x.e);
  if(!p)return null;
  const a=enter(frame,p.s);
  return <div style={{
    position:'absolute',right:28,top:22,
    opacity:fade(frame,p.s,p.e,4)*a,
    transform:`translateY(${(1-a)*-5}px)`,
    fontFamily:'Arial,Helvetica,sans-serif',
    fontSize:10,fontWeight:700,letterSpacing:1.5,
    color:C.paper,
    textShadow:'0 2px 5px rgba(23,26,28,.88)',
    zIndex:10
  }}>
    <span style={{display:'inline-block',width:18,height:1,background:C.orange,marginRight:7,verticalAlign:'middle'}}/>
    {p.label}
  </div>;
}

function InfoBeat(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const x=overlays.info.find(v=>t>=v.s&&t<=v.e);
  if(!x)return null;
  const a=enter(frame,x.s);
  const op=fade(frame,x.s,x.e,5);
  const chapter=x.type==='chapter';
  return <div style={{
    position:'absolute',left:54,top:chapter?78:82,
    maxWidth:690,
    opacity:op*a,
    transform:`translateY(${(1-a)*10}px)`,
    fontFamily:'Arial,Helvetica,sans-serif',
    color:C.ivory,
    textShadow:'0 2px 8px rgba(23,26,28,.78)',
    zIndex:11
  }}>
    <div style={{
      width:interpolate(a,[0,1],[0,chapter?44:30]),
      height:2,background:C.orange,marginBottom:chapter?11:8
    }}/>
    {chapter && <div style={{fontSize:11,letterSpacing:2.0,fontWeight:700,color:C.muted,marginBottom:7}}>CHAPTER</div>}
    <div style={{
      fontSize:chapter?34:22,
      lineHeight:1.02,
      fontWeight:chapter?800:760,
      letterSpacing:chapter?.7:1.0
    }}>{x.text}</div>
  </div>;
}

function Gauge(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const g=overlays.gauge;
  if(t<g.s||t>g.e)return null;
  const a=enter(frame,g.s+.12);
  const op=fade(frame,g.s,g.e,7);
  const line=interpolate(frame,[F(g.s+.45),F(g.s+1.25)],[0,1],{
    extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)
  });
  return <div style={{
    position:'absolute',left:58,top:70,width:520,
    opacity:op,
    fontFamily:'Arial,Helvetica,sans-serif',
    color:C.ivory,
    textShadow:'0 2px 7px rgba(23,26,28,.76)',
    zIndex:12
  }}>
    <div style={{display:'flex',alignItems:'center',gap:11,transform:`translateY(${(1-a)*8}px)`,opacity:a}}>
      <div style={{width:3,height:42,background:C.orange}}/>
      <div>
        <div style={{fontWeight:800,fontSize:27,letterSpacing:1.7}}>2-FOOT GAUGE</div>
        <div style={{fontSize:11.5,letterSpacing:1.65,color:C.muted,marginTop:4}}>SCHEMATIC — NOT TO SCALE</div>
      </div>
    </div>
    <div style={{marginTop:22,marginLeft:14,width:430,position:'relative',height:34}}>
      <div style={{position:'absolute',left:0,top:8,width:`${line*100}%`,height:1.5,background:C.paper,opacity:.92}}/>
      <div style={{position:'absolute',left:0,top:2,width:1.5,height:14,background:C.paper,opacity:line}}/>
      <div style={{position:'absolute',left:`calc(${line*100}% - 1px)`,top:0,width:2,height:18,background:C.orange,opacity:line}}/>
      <div style={{position:'absolute',left:188,top:15,fontSize:12,fontWeight:700,letterSpacing:1.5,color:C.paper,opacity:line}}>2 FT</div>
    </div>
  </div>;
}

const PLACEMENT={
  transfer:{left:56,top:68},
  coal:{right:52,top:70},
  basement:{left:56,top:68},
  water:{right:52,top:70},
  survivor:{left:56,top:68},
};

function Process(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const p=overlays.processes.find(x=>x.segments.some(s=>t>=s.s&&t<=s.e));
  if(!p)return null;
  const seg=p.segments.find(s=>t>=s.s&&t<=s.e);
  const wholeS=p.segments[0].s,wholeE=p.segments[p.segments.length-1].e;
  const a=enter(frame,wholeS+.05);
  const phaseA=enter(frame,seg.s);
  const op=fade(frame,wholeS,wholeE,6);
  const place=PLACEMENT[p.name]||{left:56,top:68};
  const title=p.labels[seg.phase];
  const railW=530;
  return <div style={{
    position:'absolute',width:railW,
    ...place,
    opacity:op,
    transform:`translateY(${(1-a)*10}px)`,
    fontFamily:'Arial,Helvetica,sans-serif',
    color:C.ivory,
    textShadow:'0 2px 7px rgba(23,26,28,.80)',
    zIndex:12
  }}>
    <div style={{display:'flex',alignItems:'center',gap:10,opacity:a}}>
      <div style={{width:interpolate(a,[0,1],[0,24]),height:2,background:C.orange}}/>
      <div style={{fontSize:10.5,fontWeight:700,letterSpacing:1.7,color:C.muted}}>
        PROCESS&nbsp;&nbsp;/&nbsp;&nbsp;STEP {seg.phase+1} / 3
      </div>
    </div>

    <div style={{
      marginTop:8,
      fontSize:28,fontWeight:800,letterSpacing:1.35,
      opacity:phaseA,
      transform:`translateY(${(1-phaseA)*6}px)`
    }}>{title}</div>

    <div style={{display:'flex',alignItems:'center',marginTop:17,width:'100%'}}>
      {p.labels.map((lab,i)=>{
        const done=i<seg.phase,current=i===seg.phase;
        return <React.Fragment key={lab}>
          <div style={{
            display:'flex',alignItems:'center',gap:7,
            opacity:current?1:done?.60:.36,
            color:current?C.ivory:C.muted
          }}>
            <div style={{
              width:current?10:8,height:current?10:8,borderRadius:'50%',
              background:current?C.orange:(done?C.muted:C.muted2),
              boxShadow:current?'0 0 0 2px rgba(242,138,58,.18)':'none'
            }}/>
            <span style={{fontSize:10.5,fontWeight:current?760:650,letterSpacing:.75,whiteSpace:'nowrap'}}>{lab}</span>
          </div>
          {i<p.labels.length-1 && <div style={{height:1,flex:1,minWidth:16,background:'rgba(232,224,208,.35)',margin:'0 10px'}}/>}
        </React.Fragment>;
      })}
    </div>
  </div>;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <OffthreadVideo src={staticFile('base.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    <Provenance/>
    <InfoBeat/>
    <Gauge/>
    <Process/>
    <Caption/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="ChicagoV4" component={Film} durationInFrames={32268} fps={25} width={960} height={540}/>);
