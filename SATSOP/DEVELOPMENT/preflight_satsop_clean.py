#!/usr/bin/env python3
"""Hard preflight and (optional) physical QC for Satsop clean Remotion master.

Absolutely no spoken dialogue caption layer. Requires original locked source bytes.
No stand-ins, cropping, inpainting, or caption removal from compressed MP4.
"""
import argparse,hashlib,json,pathlib,subprocess,sys
p=argparse.ArgumentParser()
p.add_argument('--project',type=pathlib.Path,default=pathlib.Path('SATSOP/REMOTION_V1'))
p.add_argument('--video',type=pathlib.Path)
a=p.parse_args()
P=a.project.resolve()
src=(P/'src/index.jsx').read_text()
for forbidden in ("function Caption(","<Caption","captions.json","HiaWordCaptions","srt","assSubtitle"):
    if forbidden.lower() in src.lower():raise SystemExit(f'CAPTIONS_OWNER_REJECT: {forbidden}')
assert "function EndScreen(" in src and "end_screen_1080.png" in src
assert "function EditorialCard(" in src and "function Picture(" in src
tl=json.loads((P/'public/timeline.json').read_text())
assert tl['fps']==30 and len(tl['beats'])==109 and abs(tl['duration']-1163.92)<.0001
assert sum(int(x['b']-x['a']) for x in tl['beats'])==34918
assert all(int(b['b'])==int(n['a']) for b,n in zip(tl['beats'],tl['beats'][1:]))
missing=[x['file'] for x in tl['beats'] if x['kind']!='document' and not (P/'public'/x['file']).is_file()]
wav=P/'public/SATSOP_VO_MASTER_V1.wav'
end=P/'public/end_screen_1080.png'
if not end.exists():missing.append('public/end_screen_1080.png')
if not wav.exists(): missing.append('public/SATSOP_VO_MASTER_V1.wav')
if missing:
    print(json.dumps({'status':'BLOCKED_MISSING_LOCKED_MEDIA','missing_count':len(missing),'missing':missing},indent=2))
    raise SystemExit(2)
h=hashlib.sha256()
with wav.open('rb') as f:
 for c in iter(lambda:f.read(4*1024*1024),b''):h.update(c)
assert h.hexdigest()=='5e9afb2310f812cf39aff3f37a8d4500bbca2988ae57ba1633244ed65d9d070c','ORIGINAL_ARTHUR_WAV_SHA_MISMATCH'
print('SOURCE_PREFLIGHT_PASS: 109 source beats + immutable Arthur WAV + original endscreen; NO SPOKEN SUBTITLES')
if a.video:
    movie=a.video.resolve()
    assert movie.exists() and movie.stat().st_size>100000000,'CLEAN_MASTER_NOT_RENDERED'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)],text=True))
    vid=next(x for x in probe['streams'] if x['codec_type']=='video')
    aud=next(x for x in probe['streams'] if x['codec_type']=='audio')
    assert (vid['width'],vid['height'],vid['r_frame_rate'],int(vid['nb_frames']))==(1920,1080,'30/1',35518)
    assert aud['sample_rate']=='48000'
    assert not [x for x in probe['streams'] if x['codec_type']=='subtitle']
    assert abs(float(probe['format']['duration'])-1183.99)<.2
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
    digest=hashlib.sha256()
    with movie.open('rb') as f:
      for chunk in iter(lambda:f.read(4*1024*1024),b''):digest.update(chunk)
    print(json.dumps({'qc':'DECODE_AND_TECHNICAL_PASS; VISUAL_OWNER_QC_PENDING','master':movie.name,
                     'sha256':digest.hexdigest(),'size_bytes':movie.stat().st_size,
                     'frames':35518,'subtitle_streams':0},indent=2))
