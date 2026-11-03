from pathlib import Path
import json
p=Path(r"C:\YOUTUBE\Youtube 2\VIDEO 10\AUDIO\R5_1_HARRISON_QUEUE\QUEUE_STATE.json")
s=json.loads(p.read_text(encoding="utf-8"))
print(json.dumps({k:s.get(k) for k in ["queue_id","status","worker_pid","updated_utc","counts","last_error"]},indent=2))
print("No generation, retry, ASR or montage was launched by this check.")
