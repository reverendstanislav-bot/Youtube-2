import React from "react";
import {AbsoluteFill} from "remotion";
import map from "../public/v4_accents.json";

// HIA V4. Frame-accurate picture-only accents; NEVER affects Fact/Chapter/end screen.
const END=24211, FPS=25;
const blocked=new Set(map.conditional_ids_to_skip || []);
const active=map.items.filter(x=>x.effect!=="HOLD"&&x.effect!=="QC_HOLD").map(x=>({
  ...x,a:Number(x.accent_in_frame),b:Number(x.accent_out_frame_exclusive),
  fi:Number(x.fade_in_frames)||12,fo:Number(x.fade_out_frames)||12,
  x:Number(x.roi_x),y:Number(x.roi_y),w:Number(x.roi_w),h:Number(x.roi_h),
  strength:Number(x.strength)
}));
if(active.length!==36)throw Error("Expected 36 V4 accents");
const lookup=new Map();
for(const a of active){
  if(blocked.has(a.asset_id)||a.a>=a.b||a.b>END)throw Error("Unsafe V4 accent "+a.asset_id);
  for(let sec=Math.floor(a.a/FPS);sec<=Math.floor((a.b-1)/FPS);sec++){
    const arr=lookup.get(sec)||[];
    arr.push(a);lookup.set(sec,arr);
  }
}
const clamp=(x,l=0,h=1)=>Math.max(l,Math.min(h,x));
const smooth=x=>{const t=clamp(x);return t*t*(3-2*t);};
const at=f=>f>=END?null:(lookup.get(Math.floor(f/FPS))||[]).find(x=>f>=x.a&&f<x.b)||null;
const envelope=(a,f)=>smooth((f-a.a)/a.fi)*smooth((a.b-1-f)/a.fo);
export const V4Picture=({frame,children})=>{
  const a=at(frame);
  const push=a&&a.effect==="PUSH";
  const s=push?1+(a.strength-1)*envelope(a,frame):1;
  const origin=push?(100*a.x).toFixed(4)+"% "+(100*a.y).toFixed(4)+"%":"50% 50%";
  return <AbsoluteFill style={{transform:"scale("+s.toFixed(6)+")",transformOrigin:origin}}>{children}</AbsoluteFill>;
};
export const V4Overlay=({frame})=>{
  const a=at(frame);
  if(!a||a.effect==="PUSH")return null;
  const opacity=envelope(a,frame);
  if(opacity<0.001)return null;
  const cx=a.x*1920,cy=a.y*1080;
  const rx=Math.max(40,a.w*960),ry=Math.max(40,a.h*540);
  if(a.effect==="RING"){
    return <AbsoluteFill style={{pointerEvents:"none",opacity}}>
      <svg viewBox="0 0 1920 1080" width="100%" height="100%">
        <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke="#E6DDC8" strokeWidth="2" strokeOpacity="0.88"/>
      </svg>
    </AbsoluteFill>;
  }
  // PATH = soft source focus, NOT a fabricated line/arrow. Add traces only after waypoint QC.
  // DOCUMENT/DATA/SPOT use same restrained non-text spotlight, no new information.
  const dim=clamp(a.strength,0,.16)*opacity;
  const gradient="radial-gradient(ellipse "+(rx*2)+"px "+(ry*2)+"px at "+cx+"px "+cy+"px, rgba(23,26,28,0) 0%, rgba(23,26,28,0.006) 47%, rgba(23,26,28,"+dim.toFixed(4)+") 100%)";
  return <AbsoluteFill style={{pointerEvents:"none",background:gradient}}/>;
};
export const V4AccentMeta={sourceV3:map.source_v3_master_sha256,number:active.length,fps:FPS};
