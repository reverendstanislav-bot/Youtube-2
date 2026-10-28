"""Local cached ASR only: recover the previously documented small.en gap."""
from pathlib import Path
import json,subprocess
from faster_whisper import WhisperModel
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'05_PROJECT_AND_QC';OUT.mkdir(exist_ok=True)
cache=Path.home()/'.cache/huggingface/hub/models--Systran--faster-whisper-medium.en/snapshots'
models=[p for p in cache.iterdir() if (p/'model.bin').is_file()];assert models,'No download is authorized or needed'
wav=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1\HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav')
temp=ROOT/'TIMING_SPOTCHECK_525_545.wav'
subprocess.run(['ffmpeg','-v','error','-y','-ss','525','-t','20','-i',str(wav),'-ar','16000','-ac','1',str(temp)],check=True)
model=WhisperModel(str(models[0]),device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
segments,info=model.transcribe(str(temp),language='en',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
records=[]
for seg in segments:
    for w in seg.words or []:records.append(dict(text=w.word.strip(),start=525+w.start,end=525+w.end,probability=w.probability))
assert 'iceworm' in ' '.join(w['text'] for w in records).lower()
(OUT/'MEDIUM_EN_525_545_WORD_TIMING.json').write_text(json.dumps(dict(model='cached faster-whisper-medium.en CPU int8',source_start=525,source_end=545,words=records,new_paid_jobs=0,source_wav_modified=False),indent=2),encoding='utf-8')
print(json.dumps([w for w in records if 532<w['start']<537.5]),flush=True)
