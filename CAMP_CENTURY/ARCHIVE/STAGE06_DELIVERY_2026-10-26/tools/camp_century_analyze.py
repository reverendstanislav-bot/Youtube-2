from pathlib import Path
import subprocess,json,hashlib,concurrent.futures,re,math,argparse,sys
from PIL import Image,ImageDraw,ImageFont
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for x in iter(lambda:f.read(8<<20),b''):h.update(x)
    return h.hexdigest()
def analyze(sid):
    files=[p for p in (R/'masters').glob(sid+'.*') if p.suffix in ['.mp4','.mpeg','.mov','.mpg']]
    if not files:print('NOT_YET_ACQUIRED',sid,flush=True);return
    p=files[0];out=R/'reports'/(sid+'_SOURCE_QC.json')
    if out.exists():
        previous=json.loads(out.read_text())
        if previous.get('status')=='FULL_DECODE_PASS' and previous.get('size_bytes')==p.stat().st_size:
            print('REUSE_FULL_DECODE',sid,flush=True);return
    meta=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]).stdout)
    v=next(x for x in meta['streams'] if x['codec_type']=='video');duration=float(meta['format']['duration'])
    decode=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-i',str(p),'-map','0:v:0','-map','0:a?','-f','null','-'],capture_output=True,text=True)
    (R/'reports'/(sid+'_FULL_DECODE.log')).write_text(decode.stderr,encoding='utf-8')
    all_stream_code=decode.returncode
    video_only_recheck=False
    if decode.returncode:
        # DVD audio mux timestamps can fail a null mux while every video frame decodes.
        # Archive clips are silent. Isolate and disclose audio instead of hiding warnings.
        video_only_recheck=True
        decode=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-i',str(p),'-map','0:v:0','-an','-f','null','-'],capture_output=True,text=True)
        (R/'reports'/(sid+'_VIDEO_ONLY_DECODE.log')).write_text(decode.stderr,encoding='utf-8')
    rec={'source_id':sid,'path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p),'status':'FULL_DECODE_PASS' if decode.returncode==0 else 'DECODE_FAILED','duration':duration,'width':v['width'],'height':v['height'],'fps':v.get('avg_frame_rate'),'r_frame_rate':v.get('r_frame_rate'),'pix_fmt':v.get('pix_fmt'),'field_order':v.get('field_order'),'sample_aspect_ratio':v.get('sample_aspect_ratio'),'display_aspect_ratio':v.get('display_aspect_ratio'),'video_codec':v['codec_name'],'audio_tracks':sum(x['codec_type']=='audio' for x in meta['streams']),'native_start_time':meta['format'].get('start_time'),'all_streams':meta['streams']}
    rec.update(all_stream_decode_exit_code=all_stream_code,video_only_recheck=video_only_recheck,source_audio_policy='Do not use source audio in editor clips; all exported clips silent')
    out.write_text(json.dumps(rec,indent=2));print('SOURCE_QC',sid,rec['status'],duration,v['width'],v['height'],rec['field_order'],flush=True)
    screen=R/'qc_sheets'/sid;screen.mkdir(parents=True,exist_ok=True)
    if (screen/'OVERVIEW_01.jpg').exists() and (R/'reports'/(sid+'_GRAY_1FPS_64x48.bin')).exists():
        print('REUSE_EXISTING_SCREENING_MEDIA',sid,flush=True);return
    # Screening sheets only; approximate sample times are never used as claimed shot boundaries.
    frames=screen/'frames';frames.mkdir(exist_ok=True)
    run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(p),'-an','-vf','fps=1/8:start_time=0,scale=320:240,setsar=1','-q:v','3',str(frames/'%05d.jpg')])
    fns=sorted(frames.glob('*.jpg'));font=ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf',16)
    for base in range(0,len(fns),40):
        batch=fns[base:base+40];image=Image.new('RGB',(1600,math.ceil(len(batch)/5)*268),(15,18,20));d=ImageDraw.Draw(image)
        for j,f in enumerate(batch):
            x=j%5*320;y=j//5*268
            with Image.open(f) as shot:image.paste(shot,(x,y))
            sec=(base+j)*8;d.text((x+4,y+242),f'{sid} ~{int(sec//60):02}:{sec%60:02} ({sec}s)',font=font,fill='white')
        image.save(screen/f'OVERVIEW_{base//40+1:02}.jpg',quality=90)
    run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(p),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(screen/(sid+'_RESEARCH_AUDIO.wav'))])
    # Per-second luminance fingerprints for cross-print duplicate alignment, not source authentication.
    feature=R/'reports'/(sid+'_GRAY_1FPS_64x48.bin')
    run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(p),'-an','-vf','fps=1:start_time=0,scale=64:48,format=gray','-f','rawvideo',str(feature)])
    print('OVERVIEW_READY',sid,len(fns),str(screen),flush=True)
parser=argparse.ArgumentParser();parser.add_argument('ids',nargs='*',default=['F01','F01B','F02','F03']);a=parser.parse_args()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(analyze,a.ids))
records=[]
for path in (R/'reports').glob('F0*_SOURCE_QC.json'):records.append(json.loads(path.read_text()))
(R/'reports/physical_originals.json').write_text(json.dumps(records,indent=2))
