from pathlib import Path
import json,wave,numpy as np
from faster_whisper import WhisperModel
p=Path(r"C:\YOUTUBE\Youtube 2\VIDEO 10\AUDIO\R5_1_MASTER_QC\ASR")
m=WhisperModel("base.en",device="cpu",compute_type="int8",cpu_threads=4,local_files_only=True)
results=[]
for f in sorted(p.glob("A*.json")):
 d=json.loads(f.read_text());initial=d["segments"][0]["text"].strip();flag=initial.lower().startswith("them.")
 if not flag:continue
 with wave.open(d["source"]) as h: sr=h.getframerate();a=np.frombuffer(h.readframes(int(sr*2.0)),dtype="<i2").astype(np.float32)/32768
 a=np.interp(np.arange(0,len(a),sr/16000),np.arange(len(a)),a).astype(np.float32)
 seg,_=m.transcribe(a,language="en",beam_size=5,condition_on_previous_text=False)
 text=" ".join(s.text.strip() for s in seg)
 results.append(dict(paragraph_id=d["paragraph_id"],medium_first=initial,base_start=text,status="PREFIX_REQUIRES_LISTENING_NO_AUDIO_CHANGED"))
 print(d["paragraph_id"],text,flush=True)
(p/"PREFIX_SECOND_MODEL_CHECK.json").write_text(json.dumps(results,indent=2))
