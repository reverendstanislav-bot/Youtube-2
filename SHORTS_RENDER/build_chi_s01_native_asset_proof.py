#!/usr/bin/env python3
import argparse, json, subprocess, hashlib, re
from pathlib import Path

FPS=25
W,H=1080,1920
START=11.800
END=46.680
DUR=END-START

SEGMENTS=[
    (0.000,0.650,'opening_street.png',0,'reconstruction'),
    (0.650,3.740,'S004_P003_detail_reconstruction.png',520,'reconstruction'),
    (3.740,7.700,'A03_ChicagoTunnelFieldsTrain_full_archive.png',600,'archive'),
    (7.700,12.380,'A04_TunnelCoalDelivery_full_archive.png',620,'archive'),
    (12.380,16.200,'S039_P015_detail_reconstruction.png',560,'reconstruction'),
    (16.200,20.720,'S041_P016_full_reconstruction.png',650,'reconstruction'),
    (20.720,24.800,'A02_IllinoisTunnelMap1910_full_map.png',220,'map'),
    (24.800,29.660,'A02_IllinoisTunnelMap1910_full_map.png',920,'map'),
    (29.660,32.500,'S006_P004_full_reconstruction.png',340,'reconstruction'),
    (32.500,34.880,'S007_P005_detail_reconstruction.png',680,'reconstruction'),
]

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:
        print(p.stdout)
        print(p.stderr[-12000:])
        raise subprocess.CalledProcessError(p.returncode,cmd)
    return p

def locate(root,name):
    hits=list(Path(root).rglob(name))
    if not hits:
        raise FileNotFoundError(name)
    return hits[0]

def ass_time(t):
    h=int(t//3600); t-=h*3600
    m=int(t//60); t-=m*60
    s=int(t); cs=int(round((t-s)*100))
    if cs>=100: s+=1; cs-=100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def build_caption_cues(words):
    cues=[]; buf=[]
    def flush():
        nonlocal buf
        if buf:
            cues.append(buf); buf=[]
    for w in words:
        if buf and w['s']-buf[-1]['e']>0.38:
            flush()
        buf.append(w)
        chars=sum(len(x['w'])+1 for x in buf)
        span=buf[-1]['e']-buf[0]['s']
        punct=bool(re.search(r'[.!?]$',buf[-1]['w']))
        if len(buf)>=6 or chars>=34 or span>=2.0 or (punct and len(buf)>=3):
            flush()
    flush()
    return cues

def build_ass(words_path,out_ass):
    raw=json.loads(Path(words_path).read_text(encoding='utf-8-sig'))
    words=[]
    for x in raw:
        s=float(x['start']); e=float(x['end']); w=str(x.get('word','')).strip()
        if not w or e<=START or s>=END: continue
        words.append({'w':w,'s':max(0,s-START),'e':min(DUR,e-START)})
    cues=build_caption_cues(words)
    head=r'''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,62,&H00FFFFFF,&H00FFFFFF,&H00110A05,&H00000000,-1,0,0,0,100,100,0,0,1,5,2,2,90,90,165,1
Style: Hist,DejaVu Sans,28,&H00DDE6F3,&H00DDE6F3,&H00110A05,&H00000000,-1,0,0,0,100,100,2,0,1,3,1,9,40,44,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events=[]
    for cue in cues:
        s=cue[0]['s']; e=max(cue[-1]['e'],s+0.08)
        for ai,a in enumerate(cue):
            ss=a['s']; ee=max(a['e'],ss+0.055)
            parts=[]
            for i,w in enumerate(cue):
                if i==ai:
                    parts.append(r'{\c&H003A8AF2&}'+w['w']+r'{\c&H00FFFFFF&}')
                else: parts.append(w['w'])
            text=' '.join(parts)
            events.append(f"Dialogue: 10,{ass_time(ss)},{ass_time(ee)},Cap,,0,0,0,,{text}")
    # Historical-source label only. No AI/CONCEPT/DOCUMENT plaques.
    hist=[
        (3.740,5.240),
        (7.700,9.200),
        (20.720,22.220),
    ]
    for s,e in hist:
        events.append(f"Dialogue: 20,{ass_time(s)},{ass_time(e)},Hist,,0,0,0,,— HISTORICAL SOURCE")
    out_ass.write_text(head+'\n'.join(events)+'\n',encoding='utf-8')
    return {'words':len(words),'cues':len(cues),'events':len(events)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assets',required=True)
    ap.add_argument('--v2',required=True)
    ap.add_argument('--words',required=True)
    ap.add_argument('--outdir',required=True)
    a=ap.parse_args()
    out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    ass=out/'captions.ass'
    capqc=build_ass(a.words,ass)

    inputs=[]
    filters=[]
    for i,(s,e,name,x,kind) in enumerate(SEGMENTS):
        p=locate(a.assets,name)
        dur=e-s
        inputs += ['-loop','1','-framerate',str(FPS),'-t',f'{dur:.3f}','-i',str(p)]
        # Normalize every clean long-form asset to 1920x1080 first, then static portrait crop.
        filters.append(
            f'[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,'
            f'crop=1920:1080,setsar=1,crop=608:1080:{x}:0,'
            f'scale=1080:1920:flags=lanczos,setsar=1,fps={FPS},format=yuv420p[v{i}]'
        )
    filters.append(''.join(f'[v{i}]' for i in range(len(SEGMENTS)))+f'concat=n={len(SEGMENTS)}:v=1:a=0[base]')
    # Soft bottom gradient is not a card; it only protects mobile captions.
    filters.append(
        "[base]drawbox=x=0:y=1450:w=1080:h=470:color=black@0.18:t=fill,"
        f"ass='{ass.as_posix()}':fontsdir='/usr/share/fonts/truetype/dejavu'[vout]"
    )
    fs=out/'filter.txt'; fs.write_text(';\n'.join(filters),encoding='utf-8')

    picture=out/'picture.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y']+inputs+[
        '-filter_complex_script',str(fs),'-map','[vout]',
        '-r',str(FPS),'-c:v','libx264','-preset','medium','-crf','17',
        '-profile:v','high','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)
    ])

    audio=out/'audio.m4a'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-ss',f'{START:.3f}','-t',f'{DUR:.3f}','-i',a.v2,
         '-vn','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',str(audio)])
    final=out/'CHI-S01_NATIVE_VERTICAL_ASSET_PROOF.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(picture),'-i',str(audio),
         '-map','0:v:0','-map','1:a:0','-c','copy','-shortest','-movflags','+faststart',str(final)])
    run(['ffmpeg','-v','error','-xerror','-i',str(final),'-f','null','-'])

    probe=json.loads(run(['ffprobe','-v','error','-show_entries',
        'stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels:format=duration,size',
        '-of','json',str(final)]).stdout)
    sha=hashlib.sha256(final.read_bytes()).hexdigest()
    qc={
      'source_audio_range':[START,END],
      'duration':DUR,
      'new_generation':False,
      'new_gfx':False,
      'ai_reconstruction_plaque':False,
      'visible_provenance_only':'HISTORICAL SOURCE',
      'transitions':'hard cuts only',
      'motion':'static reframes only',
      'segments':[{'s':s,'e':e,'asset':n,'x':x,'kind':k} for s,e,n,x,k in SEGMENTS],
      'caption_qc':capqc,
      'sha256':sha,
      'probe':probe,
    }
    (out/'QC.json').write_text(json.dumps(qc,indent=2),encoding='utf-8')

    # Contact sheet.
    stills=[]
    for i,t in enumerate([0.3,1.4,4.8,8.8,13.5,17.7,21.8,25.8,30.4,33.4],1):
        p=out/f'qc_{i:02d}.jpg'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(final),'-frames:v','1','-vf','scale=270:480',str(p)])
        stills.append(p)
    # ffmpeg tile from extracted qc stills.
    concat=out/'stills.txt'
    concat.write_text(''.join(f"file '{p.name}'\n" for p in stills),encoding='utf-8')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),
         '-vf','tile=5x2:padding=2:margin=2','-frames:v','1',str(out/'CONTACT.jpg')])
    print(json.dumps(qc,indent=2))

if __name__=='__main__':
    main()

# trigger native vertical proof
