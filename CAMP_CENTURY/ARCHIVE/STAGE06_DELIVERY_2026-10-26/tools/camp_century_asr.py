from pathlib import Path
import json,sys,time
from faster_whisper import WhisperModel
R=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
model=WhisperModel('base',device='cuda',compute_type='int8_float16',local_files_only=True)
for sid in sys.argv[1:]:
    audio=R/'qc_sheets'/sid/(sid+'_RESEARCH_AUDIO.wav')
    out=R/'records'/(sid+'_ARCHIVE_NARRATION_ASR.json')
    if out.exists():print('REUSE_ASR',sid,flush=True);continue
    if not audio.exists():print('AUDIO_NOT_YET_READY',sid,flush=True);continue
    segments,info=model.transcribe(str(audio),language='en',beam_size=1,vad_filter=False)
    records=[]
    for seg in segments:
        records.append({'start':round(seg.start,3),'end':round(seg.end,3),'text':seg.text})
        if len(records)%60==0:print('ASR_PROGRESS',sid,round(seg.end),flush=True)
    out.write_text(json.dumps({'source_id':sid,'purpose':'Internal source-film narration research; NOT HIA voice generation or delivery captions','review_status':'AUTOMATIC_TRANSCRIPT_VERIFY_AGAINST_PICTURE','segments':records},indent=2))
    print('ASR_READY',sid,len(records),flush=True)
