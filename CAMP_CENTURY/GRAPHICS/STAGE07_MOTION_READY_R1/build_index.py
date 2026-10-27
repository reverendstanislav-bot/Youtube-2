from pathlib import Path
import html,json
p=Path(__file__).resolve().parent
rows=json.loads((p/'MOTION_PLAN.json').read_text())
cards=[]
for r in rows:
    cards.append(f'<article><h2>{r["id"]} / {html.escape(r["purpose"])}</h2><video controls preload="metadata" src="preview/{r["id"]}_MOTION_DEMO.mp4"></video><p>V4 cue: {html.escape(r["voice_cue_exact"])}</p></article>')
head='''<!doctype html><meta charset="utf-8"><title>Camp Century motion tests</title><style>body{font:16px system-ui;background:#edf1f3;color:#172a32;margin:24px}main{max-width:1200px;margin:auto}video{width:100%;background:#fff}article{margin:42px 0}h2{font-size:20px}</style><main><h1>Camp Century / 8 motion treatments</h1><p>64-second silent design test. Narration synchronization pending.</p><video controls preload="metadata" src="preview/CAMP_CENTURY_8_MOTION_TESTS_64S.mp4"></video>'''
(p/'INDEX.html').write_text(head+''.join(cards)+'</main>',encoding='utf-8')
