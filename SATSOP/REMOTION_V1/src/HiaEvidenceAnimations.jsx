import React from 'react';
import {interpolate} from 'remotion';

const ivory='#F3EBDD', paper='#E6DDC8', rust='#A55235', blue='#5F747D';
const cl={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const ease=(x)=>{const n=Math.max(0,Math.min(1,x));return n*n*(3-2*n)};
const mono='IBM Plex Mono,Consolas,monospace';

/**
 * Data-driven vector motion for verified values already present in
 * the locked Satsop overlays; no imported maps, no new figures.
 * This runs IN the hero shot (not a replacement graphic background).
 */
export function HiaVerifiedMetric({card,frame,fps=30}){
  const start=Math.round(card.s*fps);
  const p=ease(interpolate(frame,[start+19,start+36],[0,1],cl));
  let values=null;
  const whole=/^(\d{1,3})% COMPLETE$/.exec(card.title);
  if(whole){
    values=[{label:'PROJECT COMPLETION',ratio:Number(whole[1])/100,display:whole[1]+'%'}];
  }else if(card.title==='70% / 30%'){
    values=[
      {label:'PUBLIC NET BILLING',ratio:.7,display:'70%'},
      {label:'FOUR PRIVATE UTILITIES',ratio:.3,display:'30%'}
    ];
  }else if(card.title==='1,240 MW / 240 MW'){
    values=[
      {label:'NUCLEAR PROJECT',ratio:1240/1480,display:'1,240 MW'},
      {label:'COMBINED-CYCLE REFERENCE',ratio:240/1480,display:'240 MW'}
    ];
  }else if(card.title==='FIVE YEARS / THREE YEARS'){
    values=[
      {label:'PROJECT 3',ratio:1,display:'5 YEARS'},
      {label:'COMBINED CYCLE',ratio:.6,display:'3 YEARS'}
    ];
  }
  if(!values)return null;
  return <div style={{marginTop:16,paddingTop:17,borderTop:'1px solid rgba(230,221,200,.27)'}}>
    {values.map((item,i)=><div key={i} style={{marginBottom:i===values.length-1?0:17}}>
      <div style={{display:'flex',justifyContent:'space-between',
        gap:8,fontFamily:mono,fontSize:11,letterSpacing:.45,
        color:paper,marginBottom:7,whiteSpace:'nowrap'}}>
        <span>{item.label}</span><span>{item.display}</span>
      </div>
      <div style={{height:4,background:'rgba(95,116,125,.45)',width:'100%'}}>
        <div style={{height:'100%',width:(Math.max(0,Math.min(1,item.ratio))*p*100)+'%',
          background:i===0?rust:ivory}}/>
      </div>
    </div>)}
  </div>;
}
