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
  paper:'#F2ECE1',
  ivory:'#FBF7EF',
  orange:'#F27622',
  muted:'#D2CCC0'
};

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const fade=(frame,s,e,edge=7)=>interpolate(frame,[F(s),F(s)+edge,F(e)-edge,F(e)],[0,1,1,0],{
  ...clamp,easing:Easing.inOut(Easing.cubic)
});

const spr=(frame,s,delay=0)=>{
  const local=Math.max(0,frame-F(s)-delay);
  return spring({fps:FPS,frame:local,config:{damping:18,stiffness:105,mass:.68}});
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
  const frame=useCurrentFrame(),t=frame/FPS;
  const cue=captions.find(x=>t>=x.s&&t<=x.e);
  if(!cue)return null;
  const active=activeWord(cue,t);
  const endMode=t>=1270;
  return <div style={{
    position:'absolute',left:70,right:70,
    top:endMode?46:undefined,bottom:endMode?undefined:26,
    textAlign:'center',
    fontFamily:'Arial,Helvetica,sans-serif',
    fontWeight:760,fontSize:endMode?27:29,lineHeight:1.16,
    color:C.paper,
    textShadow:'0 2px 3px rgba(15,16,17,.96),0 0 9px rgba(15,16,17,.72)',
    opacity:fade(frame,cue.s,cue.e,3),
    zIndex:40
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
  const a=spr(frame,p.s);
  return <div style={{
    position:'absolute',right:24,top:18,
    opacity:fade(frame,p.s,p.e,4)*a,
    transform:`translateY(${(1-a)*-4}px)`,
    fontFamily:'Arial,Helvetica,sans-serif',
    fontSize:9.5,fontWeight:700,letterSpacing:1.7,
    color:C.paper,textShadow:'0 2px 5px rgba(0,0,0,.88)',zIndex:12
  }}>
    <span style={{display:'inline-block',width:18,height:2,background:C.orange,marginRight:7,verticalAlign:'middle'}}/>
    {p.label}
  </div>;
}

const splitTitle=(title)=>{
  const special={
    'THE FREIGHT TUNNELS':['THE','FREIGHT','TUNNELS'],
    'THE TELEPHONE ORIGINS':['THE','TELEPHONE','ORIGINS'],
    'SURFACE FREIGHT':['SURFACE','FREIGHT'],
    'TRANSFER / LOWERING':['TRANSFER /','LOWERING'],
    'TUNNEL CARS':['TUNNEL','CARS'],
    'COAL DELIVERY':['COAL','DELIVERY'],
    'BOILERS / USE':['BOILERS /','USE'],
    'ASH REMOVAL':['ASH','REMOVAL'],
    'BUILDING CONNECTION':['BUILDING','CONNECTION'],
    'BASEMENTS / UTILITIES':['BASEMENTS /','UTILITIES'],
    'LEFT UNDERGROUND':['LEFT','UNDERGROUND'],
    'PRESERVED TODAY':['PRESERVED','TODAY']
  };
  if(special[title])return special[title];
  const words=title.split(/\s+/);
  if(words.length<=2)return [title];
  const mid=Math.ceil(words.length/2);
  return [words.slice(0,mid).join(' '),words.slice(mid).join(' ')];
};

function EditorialCard({card}){
  const frame=useCurrentFrame();
  const op=fade(frame,card.s,card.e,8);
  const line=spr(frame,card.s,0);
  const kick=spr(frame,card.s,4);
  const titleA=spr(frame,card.s,7);
  const sub=spr(frame,card.s,13);
  const stepA=spr(frame,card.s,10);
  const lines=splitTitle(card.title);

  const isHero=card.kind==='hero';
  const isFact=card.kind==='fact';
  const isChapter=card.kind==='chapter';
  const baseSize=isHero?65:(isFact?48:(isChapter?57:58));
  const long=card.title.length>22;
  const fontSize=long?Math.max(41,baseSize-10):baseSize;
  const left=54;
  const top=isFact?70:48;
  const maxW=isFact?600:700;

  return <div style={{position:'absolute',inset:0,opacity:op,zIndex:20,pointerEvents:'none'}}>
    {/* Soft cinematic legibility field, never a box. Ends well above subtitle zone. */}
    <div style={{
      position:'absolute',left:0,top:0,width:'82%',height:'70%',
      background:'linear-gradient(90deg,rgba(10,11,12,.78) 0%,rgba(10,11,12,.55) 42%,rgba(10,11,12,.18) 68%,rgba(10,11,12,0) 100%)'
    }}/>

    <div style={{position:'absolute',left,top,width:maxW}}>
      <div style={{display:'flex',alignItems:'center',gap:14,height:21}}>
        <div style={{
          width:interpolate(line,[0,1],[0,44]),height:3,background:C.orange,
          boxShadow:'0 1px 4px rgba(242,118,34,.25)'
        }}/>
        <div style={{
          opacity:kick,transform:`translateY(${(1-kick)*5}px)`,
          fontFamily:'Arial,Helvetica,sans-serif',
          fontSize:12.5,fontWeight:500,letterSpacing:4.0,color:C.paper,
          textShadow:'0 2px 7px rgba(0,0,0,.9)',whiteSpace:'nowrap'
        }}>{card.kicker}</div>
      </div>

      <div style={{marginTop:10,position:'relative',display:'inline-flex',alignItems:'flex-start'}}>
        <div style={{
          clipPath:`inset(${(1-titleA)*100}% 0 0 0)`,
          transform:`translateY(${(1-titleA)*13}px)`,
          color:C.ivory,
          fontFamily:"Georgia,'Times New Roman',serif",
          fontWeight:700,
          fontSize,lineHeight:.86,letterSpacing:-2.0,
          textTransform:'uppercase',
          textShadow:'0 3px 10px rgba(0,0,0,.86)'
        }}>
          {lines.map((x,i)=><div key={i} style={{whiteSpace:'nowrap'}}>{x}</div>)}
        </div>

        {card.step && <div style={{
          marginLeft:18,marginTop:4,paddingLeft:15,
          borderLeft:'1px solid rgba(242,236,225,.72)',
          opacity:stepA,transform:`translateX(${(1-stepA)*8}px)`,
          fontFamily:'Arial,Helvetica,sans-serif',
          textShadow:'0 2px 7px rgba(0,0,0,.9)',
          minWidth:82
        }}>
          <div style={{fontSize:11.5,letterSpacing:2.5,color:C.paper}}>STEP</div>
          <div style={{marginTop:3,fontSize:22,fontWeight:700,letterSpacing:1.2,color:C.paper}}>
            <span style={{color:C.orange}}>{card.step.split('/')[0].trim()}</span>
            <span> / {card.step.split('/')[1].trim()}</span>
          </div>
        </div>}
      </div>

      {card.subline && <div style={{
        marginTop:isFact?10:12,
        opacity:sub,transform:`translateY(${(1-sub)*8}px)`,
        fontFamily:'Arial,Helvetica,sans-serif',
        fontSize:isFact?15:17,fontWeight:800,
        letterSpacing:isFact?2.4:3.2,lineHeight:1.12,
        color:C.orange,textTransform:'uppercase',
        textShadow:'0 2px 7px rgba(0,0,0,.9)',
        whiteSpace:'pre-line'
      }}>{card.subline}</div>}
    </div>
  </div>;
}

function Cards(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const card=overlays.cards.find(x=>t>=x.s&&t<=x.e);
  return card?<EditorialCard card={card}/>:null;
}

function Film(){
  return <AbsoluteFill style={{background:C.charcoal}}>
    <OffthreadVideo src={staticFile('base.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    <Provenance/>
    <Cards/>
    <Caption/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="ChicagoV5" component={Film} durationInFrames={32268} fps={25} width={960} height={540}/>);
