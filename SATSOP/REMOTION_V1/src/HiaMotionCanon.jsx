import React from 'react';
import {interpolate} from 'remotion';
import {HiaVerifiedMetric} from './HiaEvidenceAnimations';

// HIA owner-selected right technical-panel system, all frame-based, no captions.
// All factual copy comes from the original public/overlays.json.
const C={charcoal:'#171A1C',iron:'#30363A',paper:'#E6DDC8',ivory:'#F3EBDD',rust:'#A55235',blueprint:'#5F747D'};
const ui='IBM Plex Sans,Arial,Helvetica,sans-serif';
const mono='IBM Plex Mono,Consolas,monospace';
const caps='IBM Plex Sans Condensed,Arial Narrow,Arial,sans-serif';
const CL={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const ease=(t)=>{const x=Math.max(0,Math.min(1,t));return 1-Math.pow(1-x,3)};
const fade=(frame,start,end)=>{
  const a=ease(interpolate(frame,[start,start+12],[0,1],CL));
  const b=interpolate(frame,[end-10,end],[1,0],CL);
  return Math.max(0,Math.min(a,b));
};

// A single establishing slug, not a persistent oversized channel logo.
export const HiaEstablishingSlug=({frame,beat})=>{
  if(beat.beat!=='SAT-B001')return null;
  const a=fade(frame,beat.a+6,beat.b-6);
  const shift=8*(1-ease(interpolate(frame,[beat.a+6,beat.a+18],[0,1],CL)));
  return <div style={{position:'absolute',left:64,top:54,zIndex:41,opacity:a,
    transform:'translateY('+shift+'px)',pointerEvents:'none',
    fontFamily:mono,color:C.ivory,textShadow:'0 2px 7px rgba(0,0,0,.75)'}}>
    <div style={{display:'flex',gap:15,alignItems:'center',fontSize:17,letterSpacing:2.8}}>
      <span style={{width:45,height:3,background:C.rust}}/>HIDDEN INDUSTRIAL AMERICA
    </div>
    <div style={{marginLeft:60,marginTop:18,fontSize:15,letterSpacing:2.4,color:C.paper}}>
      SATSOP, WASHINGTON
    </div>
  </div>;
};

// All 33 pre-existing data cards become a compact right-side evidence panel.
// Deterministic 0.4s entrance, row stagger, ~0.33s exit. Original timing unchanged.
export const HiaEditorialPanel=({card,frame,fps=30})=>{
  const start=Math.round(card.s*fps),end=Math.round(card.e*fps);
  const opacity=fade(frame,start,end);
  if(opacity<=0)return null;
  const e=ease(interpolate(frame,[start,start+13],[0,1],CL));
  const x=(1-e)*22;
  const val=card.title;
  const fs=val.length>26?28:val.length>20?34:41;
  const rows=[
    {label:'REFERENCE',value:card.kicker},
    {label:'EVIDENCE',value:val,featured:true},
    {label:'CONTEXT',value:card.subline}
  ];
  return <div style={{position:'absolute',right:60,top:165,zIndex:46,
    width:520,padding:'28px 31px 24px',boxSizing:'border-box',
    background:'rgba(23,26,28,.87)',
    borderLeft:'2px solid rgba(95,116,125,.75)',
    boxShadow:'-18px 12px 48px rgba(0,0,0,.2)',
    opacity,transform:'translateX('+x+'px)',pointerEvents:'none'}}>
    <div style={{fontFamily:mono,fontSize:14,letterSpacing:2.1,color:C.paper,marginBottom:12}}>
      HIA / PROJECT RECORD
    </div>
    {rows.map((row,i)=>{
      const z=ease(interpolate(frame,[start+3+i*5,start+15+i*5],[0,1],CL));
      return <div key={i} style={{
        borderTop:'1px solid rgba(230,221,200,.27)',
        padding:'16px 0 15px 12px',position:'relative',
        opacity:z,transform:'translateY('+((1-z)*6)+'px)'}}>
        <span style={{position:'absolute',left:0,top:17,width:3,
          height:row.featured?42:18,
          background:row.featured?C.rust:C.blueprint}}/>
        <div style={{fontFamily:mono,fontSize:14,lineHeight:1.2,
          letterSpacing:1.9,color:C.paper,marginBottom:row.featured?8:5}}>
          {row.label}
        </div>
        <div style={{fontFamily:row.featured?caps:mono,
          fontWeight:row.featured?700:400,
          fontSize:row.featured?fs:row.value.length>36?15:17,
          lineHeight:row.featured?1.03:1.22,
          letterSpacing:row.featured?1:1.1,
          color:row.featured?C.ivory:C.paper,overflowWrap:'break-word'}}>
          {row.value}
        </div>
      </div>;
    })}
    <HiaVerifiedMetric card={card} frame={frame} fps={fps}/>
    <div style={{height:1,background:'rgba(230,221,200,.3)',marginTop:4}}/>
    <div style={{display:'flex',gap:12,alignItems:'center',marginTop:13}}>
      <div style={{width:37,height:3,background:C.rust}}/>
      <div style={{height:1,flex:1,background:'rgba(95,116,125,.7)'}}/>
      <div style={{fontSize:13,letterSpacing:1.4,fontFamily:mono,color:C.paper}}>
        SATSOP
      </div>
    </div>
  </div>;
};

// No automatic callout endpoints: without actual source pixels, pointers could
// falsely identify tower parts. Per-frame annotations require manual verification.
