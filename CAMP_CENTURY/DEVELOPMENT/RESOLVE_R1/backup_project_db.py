from pathlib import Path
import sqlite3,hashlib,json
src=Path(r'C:\Users\KK\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Resolve Project Library\Resolve Projects\Users\guest\Projects\YT2 Vid7\Project.db')
out=Path(__file__).resolve().parent/'PROJECT_DB_CHECKPOINT'
out.mkdir(exist_ok=True)
dest=out/'Project.db'
a=sqlite3.connect(src.as_uri()+'?mode=ro',uri=True)
b=sqlite3.connect(dest)
a.backup(b)
result=b.execute('PRAGMA integrity_check').fetchone()[0]
b.close();a.close()
report=dict(original=str(src),backup=str(dest),sqlite_integrity=result,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),bytes=dest.stat().st_size,type='Native project database backup; not a DRP export')
(out/'BACKUP_MANIFEST.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
