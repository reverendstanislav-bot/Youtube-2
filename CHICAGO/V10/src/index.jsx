import React from 'react';
import {
  registerRoot, Composition, AbsoluteFill, OffthreadVideo, Img, staticFile,
  useCurrentFrame, interpolate, Easing
} from 'remotion';
import captions from '../public/captions.json';
import overlays from '../public/overlays.json';

const FPS=25;
const F=(s)=>Math.round(s*FPS);
const C={
  charcoal:'#171A1C',
  paper:'#F2ECE1',
  ivory:'#F6F1E8',
  orange:'#F27622'
};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};

const fade=(frame,s,e,edge=8)=>interpolate(
  frame,[F(s),F(s)+edge,F(e)-edge,F(e)],[0,1,1,0],
  {...CLAMP,easing:Easing.inOut(Easing.cubic)}
);

const tween=(frame,startFrame,duration=8)=>interpolate(
  frame,[startFrame,startFrame+duration],[0,1],
  {...CLAMP,easing:Easing.out(Easing.cubic)}
);

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
  const endMode=t>=1272.72;
  return <div style={{
    position:'absolute',
    left:endMode?54:70,
    right:endMode?620:70,
    top:undefined,
    bottom:endMode?36:26,
    textAlign:endMode?'left':'center',
    fontFamily:'Arial,Helvetica,sans-serif',
    fontWeight:760,
    fontSize:endMode?22:29,
    lineHeight:1.16,
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
  const a=tween(frame,F(p.s),8);
  return <div style={{
    position:'absolute',right:24,top:18,
    opacity:fade(frame,p.s,p.e,4)*a,
    transform:`translateY(${(1-a)*-4}px)`,
    fontFamily:'Arial,Helvetica,sans-serif',
    fontSize:9,fontWeight:700,letterSpacing:1.6,
    color:C.paper,
    textShadow:'0 1px 3px rgba(0,0,0,.72)',WebkitTextStroke:'0.4px rgba(15,16,17,.86)',
    zIndex:12
  }}>
    <span style={{display:'inline-block',width:16,height:2,background:C.orange,marginRight:7,verticalAlign:'middle'}}/>
    {p.label}
  </div>;
}

const splitTitle=(title)=>{
  const map={
    'THE FREIGHT TUNNELS':['THE FREIGHT','TUNNELS'],
    'THE TELEPHONE ORIGINS':['THE TELEPHONE','ORIGINS'],
    'SURFACE FREIGHT':['SURFACE','FREIGHT'],
    'TRANSFER / LOWERING':['TRANSFER /','LOWERING'],
    'TUNNEL CARS':['TUNNEL','CARS'],
    'COAL DELIVERY':['COAL','DELIVERY'],
    'BOILERS / USE':['BOILERS /','USE'],
    'ASH REMOVAL':['ASH','REMOVAL'],
    'BUILDING CONNECTION':['BUILDING','CONNECTION'],
    'BASEMENTS / UTILITIES':['BASEMENTS /','UTILITIES'],
    'LEFT UNDERGROUND':['LEFT','UNDERGROUND'],
    'PRESERVED TODAY':['PRESERVED','TODAY'],
    'A RAILROAD TAKES SHAPE':['A RAILROAD','TAKES SHAPE'],
    'STREET-LEVEL CONGESTION':['STREET-LEVEL','CONGESTION'],
    '1906 - REGULAR FREIGHT SERVICE':['1906 — REGULAR','FREIGHT SERVICE']
  };
  if(map[title])return map[title];
  const words=title.trim().split(/\s+/);
  if(words.length<=2)return [title];
  let best=1,score=1e9;
  for(let i=1;i<words.length;i++){
    const a=words.slice(0,i).join(' ');
    const b=words.slice(i).join(' ');
    const s=Math.abs(a.length-b.length);
    if(s<score){score=s;best=i;}
  }
  return [words.slice(0,best).join(' '),words.slice(best).join(' ')];
};

function EditorialCard({card}){
  const frame=useCurrentFrame();
  const start=F(card.s);
  const op=fade(frame,card.s,card.e,9);

  const lineA=tween(frame,start,8);
  const kickerA=tween(frame,start+3,8);
  const titleA=tween(frame,start+5,10);
  const stepA=tween(frame,start+8,8);
  const subA=tween(frame,start+10,8);

  const isHero=card.kind==='hero';
  const isChapter=card.kind==='chapter';
  const isFact=card.kind==='fact';

  const lines=splitTitle(card.title).slice(0,2);
  const long=card.title.length>24;

  let fontSize=45;
  if(isHero)fontSize=52;
  else if(isChapter)fontSize=48;
  else if(isFact)fontSize=38;
  if(long)fontSize-=4;

  const left=42;
  const top=34;
  const titleTop=58;
  const titleWidth=isFact?500:560;
  const stepLeft=isFact?545:610;

  return <div style={{position:'absolute',inset:0,opacity:op,zIndex:20,pointerEvents:'none'}}>
    {/* V7: still NO background / gradient / panel. Readability comes from text stroke + shadow only. */}

    <div style={{position:'absolute',left,top,width:760,height:270}}>
      <div style={{position:'absolute',left:0,top:0,display:'flex',alignItems:'center',gap:12}}>
        <div style={{
          width:interpolate(lineA,[0,1],[0,34]),
          height:3,
          background:C.orange
        }}/>
        <div style={{
          opacity:kickerA,
          transform:`translateX(${(1-kickerA)*-10}px)`,
          fontFamily:'Arial,Helvetica,sans-serif',
          fontSize:11,
          fontWeight:600,
          letterSpacing:3.2,
          color:C.paper,
          whiteSpace:'nowrap',
          textShadow:'0 1px 3px rgba(0,0,0,.72)',WebkitTextStroke:'0.45px rgba(15,16,17,.88)'
        }}>{card.kicker}</div>
      </div>

      <div style={{
        position:'absolute',
        left:0,top:titleTop,
        width:titleWidth,
        opacity:titleA,
        transform:`translateX(${(1-titleA)*-10}px) translateY(${(1-titleA)*8}px)`,
        fontFamily:"Georgia,'Times New Roman',serif",
        fontWeight:700,
        fontSize,
        lineHeight:.90,
        letterSpacing:-1.2,
        textTransform:'uppercase',
        color:C.ivory,
        textShadow:'0 2px 5px rgba(0,0,0,.82),0 0 2px rgba(0,0,0,.72)',WebkitTextStroke:'1.15px rgba(15,16,17,.90)'
      }}>
        {lines.map((x,i)=><div key={i} style={{whiteSpace:'nowrap'}}>{x}</div>)}
      </div>

      {card.step && <div style={{
        position:'absolute',
        left:stepLeft,top:64,
        paddingLeft:13,
        borderLeft:'1px solid rgba(242,236,225,.65)',
        opacity:stepA,
        transform:`translateX(${(1-stepA)*8}px)`,
        fontFamily:'Arial,Helvetica,sans-serif',
        textShadow:'0 1px 3px rgba(0,0,0,.72)',WebkitTextStroke:'0.45px rgba(15,16,17,.88)'
      }}>
        <div style={{fontSize:10,letterSpacing:2,color:C.paper,fontWeight:600}}>STEP</div>
        <div style={{marginTop:3,fontSize:18,fontWeight:700,letterSpacing:1,color:C.paper}}>
          <span style={{color:C.orange}}>{card.step.split('/')[0].trim()}</span>
          <span> / {card.step.split('/')[1].trim()}</span>
        </div>
      </div>}

      {card.subline && <div style={{
        position:'absolute',
        left:0,
        top:lines.length===1?125:155,
        width:isFact?500:560,
        opacity:subA,
        transform:`translateX(${(1-subA)*-10}px) translateY(${(1-subA)*8}px)`,
        fontFamily:'Arial,Helvetica,sans-serif',
        fontSize:13,
        lineHeight:1.12,
        fontWeight:700,
        letterSpacing:2.6,
        textTransform:'uppercase',
        whiteSpace:'pre-line',
        color:C.orange,
        textShadow:'0 1px 3px rgba(0,0,0,.72)',WebkitTextStroke:'0.45px rgba(15,16,17,.88)'
      }}>{card.subline}</div>}
    </div>
  </div>;
}

function Cards(){
  const frame=useCurrentFrame(),t=frame/FPS;
  const card=overlays.cards.find(x=>t>=x.s&&t<=x.e);
  return card?<EditorialCard card={card}/>:null;
}

const END_START=1272.72;

function EndScreen(){
  const frame=useCurrentFrame();
  const t=frame/FPS;
  if(t<END_START)return null;
  const a=tween(frame,F(END_START),10);

  return <AbsoluteFill style={{
    zIndex:30,
    overflow:'hidden',
    background:C.charcoal,
    opacity:a
  }}>
    {/* Exact accepted brand-native Episode 1 proof, rendered deterministically
        from canonical HIA asset 07. No recommendation/video slots. */}
    <Img
      src={staticFile('end_screen_first_episode.png')}
      style={{
        position:'absolute',
        inset:0,
        width:'100%',
        height:'100%',
        objectFit:'cover'
      }}
    />
  </AbsoluteFill>;
}

function Film(){
  const frame=useCurrentFrame();
  const t=frame/FPS;
  return <AbsoluteFill style={{background:C.charcoal}}>
    <OffthreadVideo src={staticFile('base.mp4')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    {t<END_START && <Provenance/>}
    {t<END_START && <Cards/>}
    <EndScreen/>
    <Caption/>
  </AbsoluteFill>;
}

registerRoot(()=> <Composition id="ChicagoV10" component={Film} durationInFrames={32268} fps={25} width={960} height={540}/>);
