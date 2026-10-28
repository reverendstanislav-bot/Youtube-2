"""Read-only render status. Never starts, cancels or modifies jobs."""
from pathlib import Path
import os, sys, json
ROOT=Path(__file__).resolve().parent
MCP=Path(r'C:\Users\KK\.codex\mcp\davinci-resolve')
sys.path.insert(0,str(MCP))
os.environ['DAVINCI_RESOLVE_BRIDGE_CONFIG']=str(MCP/'bridge-config.json')
from src.utils.resolve_bridge_client import connect
r=connect(require_enabled=False,timeout=45)
p=r.GetProjectManager().GetCurrentProject()
print('PROJECT',p.GetName(),flush=True)
print('RENDERING',p.IsRenderingInProgress(),flush=True)
jobs=p.GetRenderJobList() or []
for j in jobs[-3:]:
    jid=j.get('JobId') or j.get('JobID')
    print(json.dumps(dict(job=j,status=p.GetRenderJobStatus(jid) if jid else None),ensure_ascii=True),flush=True)
f=ROOT/'CHAPTER_RENDER_RESULTS.json'
if f.exists():
    rows=json.loads(f.read_text());print('VERIFIED_CHAPTERS',len(rows),'FRAMES',sum(x['frames'] for x in rows),flush=True)
