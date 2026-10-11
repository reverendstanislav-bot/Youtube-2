import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';
import accents from '../public/v4_accents.json';

/**
 * Lake V7 — narration-locked, non-invasive visual retention proof.
 * NO subtitles, generated content, harsh zoom, lateral pan, outlined highlights,
 * white circles, fabricated maps, sound or end-screen changes.
 * Full-film rendering only after a 00:00–03:00 preview is QC/owner accepted.
 */
const FPS=25;
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
const smooth=(v)=>{const n=clamp(v);return n*n*(3-2*n)};
const active=accents.items.filter(x=>x.effect!=='HOLD'&&x.effect!=='QC_HOLD');
const getWindow=(assetId,frame)=>active.find(x=>x.asset_id===assetId && frame>=Number(x.slot_in_frame)&&frame<Number(x.slot_out_frame_exclusive));
export const v7Motion=(slot,frame)=>{
  if(!slot||getWindow(slot.assetId,frame)?.effect==='PUSH')return {};
  const a=Number(slot.a),b=Number(slot.b),duration=b-a;
  if(!Number.isFinite(duration)||duration<140||frame<a||frame>=b+18)return {};
  // Single continuous source-scale micro push; no X/Y translation or per-frame jitter.
  // <=1.018 maximum. A shot is ONE source exposure, not duplicated.
  const amount=duration>=225?.018:.011;
  const eased=smooth((Math.min(frame,b-1)-a)/Math.max(1,duration-1));
  return {transform:'scale('+(1+amount*eased).toFixed(5)+')',transformOrigin:'50% 50%'};
};
// Source-lock confirms both IDs have exactly 1 original timeline exposure.
// One additional teaser exposure each => 2 total, within rights/source reuse gate.
const inserts=[
  {id:'LP-REC-002',from:2.8,to:4.85}, // glimpse of drill crew on the rig during opening sentence
  {id:'LP-REC-003',from:7.65,to:10.0}, // water against salt as narration places people underground
];
export const V7Insert=({frame})=>{
  const t=frame/FPS,x=inserts.find(s=>t>=s.from&&t<s.to);
  if(!x)return null;
  const opacity=smooth((t-x.from)/.28)*smooth((x.to-t)/.28);
  return <AbsoluteFill style={{pointerEvents:'none',opacity,zIndex:9,overflow:'hidden',background:'#171A1C'}}>
    <Img src={staticFile('assets/'+x.id+'.png')} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(23,26,28,.04),transparent 55%,rgba(23,26,28,.18))'}}/>
  </AbsoluteFill>;
};
// Actual subject-based focal progression for hold-style exposition.
// Normalized ROI is editorial emphasis, NEVER supposed physical locations or arrows.
const focus=[
  {a:27,b:30,x:.82,y:.68}, {a:30,b:33.5,x:.81,y:.27},
  {a:75.5,b:81.0,x:.52,y:.59}, {a:81.0,b:87.5,x:.72,y:.42},
  {a:105,b:108.8,x:.55,y:.59}, {a:112.0,b:116.8,x:.41,y:.53},
  {a:119.5,b:125.0,x:.52,y:.34}, {a:125,b:131.2,x:.48,y:.73},
  {a:133,b:138.2,x:.43,y:.57}, {a:139,b:144.5,x:.31,y:.36},
  {a:159,b:163.3,x:.50,y:.67}, {a:167,b:171.7,x:.62,y:.52},
  {a:172.6,b:176.4,x:.37,y:.47}
];
export const V7Focus=({frame})=>{
  const t=frame/FPS,x=focus.find(x=>t>=x.a&&t<x.b);
  if(!x)return null;
  const p=smooth((t-x.a)/.56)*smooth((x.b-t)/.56);
  const cx=x.x*1920,cy=x.y*1080,d=(.135*p).toFixed(4);
  const bg='radial-gradient(ellipse 650px 365px at '+cx+'px '+cy+'px, rgba(23,26,28,0) 0%,rgba(23,26,28,.006) 44%,rgba(23,26,28,'+d+') 100%)';
  return <AbsoluteFill style={{pointerEvents:'none',zIndex:12,background:bg}}/>;
};
// These are editorial claim anchors, not subtitles or speech captions.
// The inherited Chapter/Fact typography always takes priority.
const cueEvents=[
 {a:40.8,b:44.9,label:'THE CANAL RAN BACKWARD'},
 {a:113.6,b:117.7,label:'PILLARS SUPPORT THE ROOF'},
 {a:137.7,b:142.4,label:'TWO INDUSTRIES. ONE SALT DOME.'},
 {a:166.7,b:171.1,label:'FRESH WATER DISSOLVES SALT'},
 {a:305.0,b:310.0,label:'ALL 52 GOT OUT'},
 {a:357.0,b:361.1,label:'THE PLATFORM WAS LOST'},
 {a:381.0,b:385.0,label:'ABOUT 68 ACRES OF LAND'},
 {a:561.0,b:566.0,label:'THE FLOW REVERSED'}
];
export const V7Cues=({frame,chapters=[],facts=[]})=>{
 const t=frame/FPS,q=cueEvents.find(e=>t>=e.a&&t<e.b);
 if(!q || chapters.some(c=>t>=c.s&&t<=c.e) || facts.some(f=>t>=f.s&&t<=f.e))return null;
 const a=smooth((t-q.a)/.34)*smooth((q.b-t)/.40);
 return <AbsoluteFill style={{pointerEvents:'none',zIndex:13}}>
    <div style={{position:'absolute',left:72,top:68,opacity:a,maxWidth:1050,
      fontFamily:'Arial,sans-serif',fontWeight:800,fontSize:29,letterSpacing:1.2,
      color:'#F3EBDD',textShadow:'0 2px 12px rgba(0,0,0,.85),0 0 30px #171A1C'}}>
      <div style={{width:62,height:3,background:'#A55235',marginBottom:13}}/>
      {q.label}
    </div>
 </AbsoluteFill>;
};
export const V7RetentionMeta={version:'V7_FIRST_180_SECOND_PROOF',inserts:inserts.length,
  focusWindows:focus.length,cueWindows:cueEvents.length,maxLocalImageScale:1.018,
  noLateralMovement:true,noCaptions:true};
