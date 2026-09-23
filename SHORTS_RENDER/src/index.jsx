import React from 'react';
import {
  registerRoot,Composition,AbsoluteFill,Sequence,OffthreadVideo,Audio,staticFile,
  useCurrentFrame,interpolate
} from 'remotion';
import maps from '../public/maps.json';

const C={charcoal:'#171A1C',iron:'#30363A',paper:'#F3EBDD',orange:'#F28A3A',blue:'#5F747D',rust:'#A55235'};
const CLAMP={extrapolateLeft:'clamp',extrapolateRight:'clamp'};

const all=[...maps.chicago.shorts,...maps.tc497.shorts];

function canonicalProv(text=''){
  for(const x of ['HISTORICAL SOURCE','AI RECONSTRUCTION','DOCUMENT','CONCEPT']){
    if(text.includes(x)) return x;
  }
  return '';
}

function framing(beat){
  const s=(beat.visual+' '+beat.action+' '+beat.provenance).toLowerCase();
  if(/historical source|document|map|patent|publication|diagram|572|13 units|full-machine|long-profile|network scale|route|metrics|gauge|top-down/.test(s)) return 'contain';
  return 'cover';
}

function BackgroundVideo({src,startFrom}){
  return <OffthreadVideo
    src={staticFile(src)} startFrom={startFrom} muted
    style={{
      position:'absolute',inset:-90,width:'calc(100% + 180px)',height:'calc(100% + 180px)',
      objectFit:'cover',filter:'blur(34px) brightness(.34) saturate(.72)',transform:'scale(1.08)'
    }}
  />;
}

function VisualBeat({short,beat,index,nextStart}){
  const fps=short.source_fps;
  const frame=useCurrentFrame();
  const mode=framing(beat);
  const startFrom=Math.round(beat.source_in*fps);
  const durFrames=Math.max(1,Math.round((nextStart-beat.source_in)*fps));
  const prov=canonicalProv(beat.provenance);
  const p=interpolate(frame,[0,Math.max(1,durFrames-1)],[0,1],CLAMP);
  const tinyScale=1+0.008*p;

  return <AbsoluteFill style={{background:C.charcoal,overflow:'hidden'}}>
    <BackgroundVideo src={short.source_file} startFrom={startFrom}/>

    {mode==='contain' ? <>
      <div style={{
        position:'absolute',left:34,right:34,top:238,height:652,
        border:'2px solid rgba(243,235,221,.18)',boxShadow:'0 20px 55px rgba(0,0,0,.55)',
        background:C.charcoal,overflow:'hidden'
      }}>
        <OffthreadVideo
          src={staticFile(short.source_file)} startFrom={startFrom} muted
          style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${tinyScale})`,transformOrigin:'50% 45%'}}
        />
        {/* Cover the long-form caption strip while retaining the full-frame source/provenance area. */}
        <div style={{
          position:'absolute',left:0,right:0,bottom:0,height:138,
          background:'linear-gradient(180deg,rgba(23,26,28,0),rgba(23,26,28,.96) 34%,rgba(23,26,28,1))'
        }}/>
      </div>
    </> : <>
      <OffthreadVideo
        src={staticFile(short.source_file)} startFrom={startFrom} muted
        style={{
          position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',
          objectPosition:'50% 42%',transform:`scale(${tinyScale})`
        }}
      />
    </>}

    <div style={{
      position:'absolute',left:0,right:0,bottom:0,height:690,
      background:'linear-gradient(180deg,rgba(23,26,28,0),rgba(23,26,28,.78) 22%,rgba(23,26,28,.98) 52%,#171A1C 100%)',
      pointerEvents:'none'
    }}/>

    {prov && <div style={{
      position:'absolute',top:86,right:56,zIndex:8,
      fontFamily:'Arial,Helvetica,sans-serif',fontSize:24,fontWeight:800,letterSpacing:2.3,
      color:C.paper,textShadow:'0 2px 6px rgba(0,0,0,.92)',
      padding:'10px 14px',background:'rgba(23,26,28,.64)',borderLeft:`5px solid ${prov==='HISTORICAL SOURCE'?C.orange:prov==='AI RECONSTRUCTION'?C.blue:C.rust}`
    }}>{prov}</div>}

    <div style={{
      position:'absolute',left:54,top:72,zIndex:7,fontFamily:'Arial,Helvetica,sans-serif',
      fontSize:23,fontWeight:800,letterSpacing:4.4,color:C.paper,textShadow:'0 2px 6px rgba(0,0,0,.9)'
    }}>HIDDEN INDUSTRIAL AMERICA</div>
  </AbsoluteFill>;
}

function makeCaptionPhrases(words){
  const out=[]; let buf=[];
  const flush=()=>{if(buf.length){out.push(buf);buf=[];}};
  for(const w of words){
    if(buf.length && w.short_s-buf[buf.length-1].short_e>0.42) flush();
    buf.push(w);
    const chars=buf.reduce((a,x)=>a+x.w.length+1,0);
    const punct=/[.!?,;:]$/.test(w.w);
    if(buf.length>=6 || chars>=34 || (punct&&buf.length>=3)) flush();
  }
  flush();
  return out.map(x=>({s:x[0].short_s,e:x[x.length-1].short_e+0.08,words:x}));
}

function Captions({short}){
  const t=useCurrentFrame()/short.source_fps;
  const phrases=makeCaptionPhrases(short.source_words);
  const phrase=phrases.find(x=>t>=x.s&&t<=x.e);
  if(!phrase) return null;
  let active=-1;
  phrase.words.forEach((w,i)=>{if(t>=w.short_s&&t<=Math.max(w.short_e,w.short_s+.055)) active=i;});
  return <div style={{
    position:'absolute',left:82,right:82,bottom:330,zIndex:20,textAlign:'center',
    fontFamily:'Arial,Helvetica,sans-serif',fontSize:68,fontWeight:850,lineHeight:1.1,
    color:'#FFFFFF',WebkitTextStroke:'1.4px rgba(8,10,11,.95)',
    textShadow:'0 5px 10px rgba(0,0,0,.98),0 0 24px rgba(0,0,0,.8)'
  }}>
    {phrase.words.map((w,i)=><React.Fragment key={i}>
      <span style={{color:i===active?C.orange:'#FFFFFF'}}>{w.w}</span>{i<phrase.words.length-1?' ':''}
    </React.Fragment>)}
  </div>;
}

function Progress({short}){
  const frame=useCurrentFrame();
  const total=Math.max(1,Math.round(short.duration_sec*short.source_fps)-1);
  const w=interpolate(frame,[0,total],[0,100],CLAMP);
  return <div style={{position:'absolute',left:54,right:54,bottom:230,height:5,zIndex:25,background:'rgba(243,235,221,.16)'}}>
    <div style={{width:`${w}%`,height:'100%',background:C.orange}}/>
  </div>;
}

function ShortFilm({short}){
  const fps=short.source_fps;
  return <AbsoluteFill style={{background:C.charcoal}}>
    {short.montage.map((beat,i)=>{
      const next=i<short.montage.length-1?short.montage[i+1].source_in:short.source_out_sec;
      const from=Math.max(0,Math.round((beat.source_in-short.source_in_sec)*fps));
      const dur=Math.max(1,Math.round((next-beat.source_in)*fps));
      return <Sequence key={i} from={from} durationInFrames={dur} premountFor={6}>
        <VisualBeat short={short} beat={beat} index={i} nextStart={next}/>
      </Sequence>;
    })}
    <Audio src={staticFile(short.source_file)} startFrom={Math.round(short.source_in_sec*fps)} volume={1}/>
    <Captions short={short}/>
    <Progress short={short}/>
  </AbsoluteFill>;
}

const Root=()=> <>
  {all.map(short=><Composition
    key={short.id} id={short.id}
    component={ShortFilm} defaultProps={{short}}
    durationInFrames={Math.round(short.duration_sec*short.source_fps)}
    fps={short.source_fps} width={1080} height={1920}
  />)}
</>;

registerRoot(Root);
