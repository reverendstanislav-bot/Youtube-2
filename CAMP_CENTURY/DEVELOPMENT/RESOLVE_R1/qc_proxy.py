from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,hashlib,json,math,subprocess
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
WAV=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1\HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav')
LOCK_SHA='c6a5df8cff089418f4f2300551fd4ba6cb057dcd3012b84fa8143e02976d0480'
def run(cmd):return subprocess.run(cmd,capture_output=True,check=True)
def audio(path):
    p=run(['ffmpeg','-hide_banner','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar','1000','-f','f32le','pipe:1'])
    return np.frombuffer(p.stdout,dtype='<f4').astype(np.float64)
def compare_audio(path):
    a,b=audio(WAV),audio(path)
    count=min(len(a),len(b));a=a[:count];b=b[:count]
    def score(lag,step=1):
        aa=a[max(lag,0):min(count+lag,count):step]
        bb=b[max(-lag,0):min(count-lag,count):step]
        return float(np.dot(aa,bb)/math.sqrt(np.dot(aa,aa)*np.dot(bb,bb)+1e-30))
    coarse=max(range(-150,151,10),key=lambda lag:score(lag,10))
    lag=max(range(coarse-9,coarse+10),key=score)
    aa=a[max(lag,0):min(count+lag,count)];bb=b[max(-lag,0):min(count-lag,count)]
    gain=float(np.dot(aa,bb)/max(np.dot(aa,aa),1e-30))
    return dict(correlation=score(lag),lag_ms=int(lag),gain_db=20*math.log10(max(abs(gain),1e-30)),locked_file_sha256=hashlib.sha256(WAV.read_bytes()).hexdigest(),reference_samples_1khz=len(a),rendered_samples_1khz=len(b),meaning='Proxy AAC signal comparison, not a bit-identical PCM claim')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('file');args=ap.parse_args();path=Path(args.file)
    q=ROOT/'QC';q.mkdir(exist_ok=True);frames=q/'frames';frames.mkdir(exist_ok=True)
    probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]).stdout)
    v=[s for s in probe['streams'] if s['codec_type']=='video'];a=[s for s in probe['streams'] if s['codec_type']=='audio'];subs=[s for s in probe['streams'] if s['codec_type']=='subtitle']
    run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(path),'-f','null','-'])
    scan=run(['ffmpeg','-hide_banner','-nostats','-v','info','-i',str(path),'-vf','blackdetect=d=0.12:pix_th=0.10','-an','-f','null','-']).stderr.decode(errors='replace')
    (q/'FULL_DECODE_AND_BLACK_SCAN.log').write_text(scan,encoding='utf-8')
    black=[l for l in scan.splitlines() if 'black_start:' in l]
    plan=json.loads((ROOT/'SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
    def sample(s):
        at=(s['start_frame']+s['duration_frames']*.52)/25
        dest=frames/(s['shot_id']+'_'+s['asset_id']+'.jpg')
        run(['ffmpeg','-hide_banner','-v','error','-y','-ss',str(at),'-i',str(path),'-frames:v','1','-vf','scale=640:-2',str(dest)])
        return dest
    files=list(ThreadPoolExecutor(max_workers=4).map(sample,plan))
    for start in range(0,len(files),20):
        tile=Image.new('RGB',(1600,1230),'#e9edef');d=ImageDraw.Draw(tile)
        for j,f in enumerate(files[start:start+20]):
            im=Image.open(f);im.thumbnail((390,220));x=(j%4)*400;y=(j//4)*246
            d.text((x+5,y+3),f.stem,fill='#15242d');tile.paste(im,(x,y+20))
        tile.save(q/f'RENDERED_CONTACT_{start//20+1:02}.jpg',quality=94)
    av=compare_audio(path)
    report=dict(file=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,duration_seconds=float(probe['format']['duration']),expected_seconds=1094.72,video_streams=v,audio_streams=a,subtitle_stream_count=len(subs),full_decode='PASS',black_events=black,narration_comparison=av,locked_wav_unchanged=av['locked_file_sha256']==LOCK_SHA,rendered_shot_samples=len(files),visual_review='Contact sheets and representative full-size frames require explicit review; decode does not prove editorial approval',final_color_music_sfx='NOT_STARTED')
    report['expected_frames']=27368
    report['encoded_video_frames']=int(v[0].get('nb_frames',0)) if v else 0
    report['technical_checks_pass']=len(v)==1 and len(a)==1 and not subs and not black and abs(report['duration_seconds']-1094.72)<.045 and v[0]['r_frame_rate']=='25/1' and report['encoded_video_frames']==27368 and v[0]['width']==1280 and v[0]['height']==720 and av['correlation']>.98 and abs(av['lag_ms'])<=40 and report['locked_wav_unchanged']
    (q/'PROXY_QC.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['video_streams','audio_streams']},indent=2))

if __name__=='__main__':main()
