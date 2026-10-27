from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
rows=[]
for f in sorted((ROOT/'preview').glob('*.mp4')):
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames','-of','json',str(f)],capture_output=True,text=True,check=True)
    probe=json.loads(p.stdout)
    expected=64 if f.name.startswith('CAMP_CENTURY_') else 8
    assert abs(float(probe['format']['duration'])-expected)<.001,(f,probe)
    assert len(probe['streams'])==1 and probe['streams'][0]['codec_type']=='video'
    rows.append(dict(file='preview/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,probe=probe))
assert len(rows)==9,len(rows)
combined=ROOT/'preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4'
p=subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(combined),'-f','null','-'],capture_output=True,text=True)
assert p.returncode==0,p.stderr
report=dict(actual_clips=8,actual_combined_seconds=64,full_combined_decode='PASS',decode_stderr=p.stderr,frame_rate_scope='25 fps DEMO ONLY; production fps unverified',audio='SILENT_TREATMENT_PREVIEW_NOT_VOICE_SYNCED',visual_review='Four sampled states per scene and representative full-size geometry checked. Full continuous human playback and owner motion approval pending.',style_status='Original illustration style accepted by owner; motion treatment pending owner review',resolve_modified=False,production_audio_timing='AUDIO_TIMING_HOLD',files=rows)
(ROOT/'QC_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
