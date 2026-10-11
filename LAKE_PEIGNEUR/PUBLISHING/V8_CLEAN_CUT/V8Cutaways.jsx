import React from 'react';
import {AbsoluteFill,Img,staticFile} from 'remotion';

/**
 * V8 CLEAN CUT — only physically different approved original source images.
 * No zoom, pan, local radial darkness, spotlight, circular stroke, text cue,
 * arrow, graphic widgets or artificial motion.
 * The film's pre-existing Chapter/Fact and end screen are handled by V3.
 * This is a rough first-3min edit proof, not a final approved feature master.
 */
const CUTS=[
  // Actual short foreshadowing of workers and lake failure while Arthur states the stakes.
  {asset:'LP-REC-021',start:25.52,end:28.44,why:'52 underground; workers at mine' },
  {asset:'LP-REC-028',start:31.08,end:34.08,why:'future landscape collapse teaser, source-grounded reconstruction' },
  // Show actual drilling/mining geometry when narration introduces two industrial systems.
  {asset:'LP-GFX-012',start:59.04,end:62.28,why:'two industries on the same salt dome' },
  {asset:'LP-GFX-005',start:83.76,end:86.80,why:'mine workings within salt dome' },
  // Contrast mine grid image with 14-second mine-level plate, without moving the camera.
  {asset:'LP-GFX-016',start:122.00,end:125.08,why:'workers spread across working levels' }
];
// all chosen assets have 1 original locked exposure and are <=2 after this edit.
const FPS=25, FADE_FRAMES=10;
const smooth=v=>{const a=Math.max(0,Math.min(1,v));return a*a*(3-2*a)};
export const V8Cutaways=({frame})=>{
 const cut=CUTS.find(x=>frame>=Math.round(x.start*FPS)&&frame<Math.round(x.end*FPS));
 if(!cut)return null;
 const start=Math.round(cut.start*FPS),end=Math.round(cut.end*FPS);
 const opacity=Math.min(
   smooth((frame-start+1)/FADE_FRAMES),
   smooth((end-frame)/FADE_FRAMES)
 );
 return <AbsoluteFill style={{pointerEvents:'none',opacity,zIndex:9}}>
   <Img src={staticFile('assets/'+cut.asset+'.png')} style={{
     width:'100%',height:'100%',objectFit:'contain',objectPosition:'center',
     background:'#171A1C'
   }}/>
 </AbsoluteFill>;
};
export const V8CutMetadata={kind:'actual_cutaways_only',cuts:CUTS,fadeFrames:FADE_FRAMES,
  zooms:0,spotlights:0,circles:0,arrows:0,addedText:0,newPaidGeneration:0};
