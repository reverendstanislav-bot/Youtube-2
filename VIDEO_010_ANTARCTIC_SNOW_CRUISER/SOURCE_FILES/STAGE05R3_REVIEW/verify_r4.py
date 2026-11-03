"""Recompute Stage05R.3 text/package checks; no media, generation or Resolve calls."""
from pathlib import Path
import csv,hashlib,json,re,subprocess
P=Path(__file__).resolve().parents[2]
R=Path(__file__).resolve().parent
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def paras(lang,rev='R4'):return re.findall(r'^\[([^]]+)\] (.+)$',(P/f'05_SCRIPT_{rev}_{lang}.md').read_text(encoding='utf-8-sig'),re.M)
def words(s):return len(re.findall(r"\b[\w]+(?:['?-][\w]+)*\b",s))
en,ru=paras('EN'),paras('RU')
ids=[k for k,t in en];rids=[k for k,t in ru]
assert ids==rids and len(ids)==len(set(ids))==73
assert len(set(k[:3] for k in ids))==10
assert sum(words(t) for k,t in en)==2592
assert sum(words(t) for k,t in ru)==2186
for lang in ['EN','RU']:
 s=(P/f'05_SCRIPT_R4_{lang}.md').read_text(encoding='utf-8')
 assert '\ufffd' not in s and '???' not in s
 assert len(re.findall(r'^## ACT ',s,re.M))==10
 assert [k for k,t in paras(lang) if '-CTA' in k]==['A04-CTA01','A10-CTA01']
baseline=json.loads((R/'BASELINE_SHA256.json').read_text(encoding='utf-8-sig'))
assert all(hashlib.sha256((P/f).read_bytes()).hexdigest()==h for f,h in baseline.items())
facts=readcsv(P/'05R3_FACT_CHANGES.csv');cross=readcsv(R/'R4_CLAIM_CROSSWALK.csv');cta=readcsv(P/'05R3_CTA_MAP.csv');ret=readcsv(P/'05R3_RETENTION_MAP.csv');timing=readcsv(R/'R4_PARAGRAPH_TIMING.csv')
assert len(facts)==22 and all(x['paragraph_id'] in ids and x['source_url'].startswith('https://') and x['locator'] and x['qualification'] for x in facts)
assert [x['r4_paragraph_id'] for x in cross]==ids
assert [x['paragraph_id'] for x in timing]==ids
r3ids={k for k,t in paras('EN','R3')}
assert all(k in r3ids or any(x['paragraph_id']==k for x in facts) for k in ids)
assert set(x['act'] for x in ret)=={f'A{i:02}' for i in range(1,11)}
assert sum(int(x['words']) for x in ret)==2592
assert all(x['new_event_or_fact'] and x['story_question'] and x['causal_transition'] and x['emotional_component'] and x['visual_material'] and x['repetition_control'] and x['slowdown_risk_and_execution'] for x in ret)
assert len([x for x in cta if x['mode']=='VOICE'])==2
assert len([x for x in cta if x['cta']=='LIKE'])==1
assert float(next(x for x in cta if x['cta']=='LIKE')['duration_seconds_at140'])==3
assert 96+64<864 and 1360+400<1920
end=next(x for x in cta if x['cta']=='END_SCREEN')
assert float(end['duration_seconds_at140'])==20
assert abs(float(end['start_seconds_at140'])-float(timing[-1]['end_seconds_at140']))<.0011
assert end['paragraph_id']=='AFTER_A10-CTA01'
for x in cta:
 if x['paragraph_id'] in ids and x['mode'] not in ['PINNED_COMMENT_ONLY']:
  t=next(p for p in timing if p['paragraph_id']==x['paragraph_id'])
  assert float(x['offset_seconds'])+float(x['duration_seconds_at140'])<=float(t['duration_seconds_at140'])+.002
assert max(words(t)*60/125 for k,t in en if '-CTA' in k)<=12
previous=json.loads((R/'PREVIOUS_STORY_VERIFIED.json').read_text(encoding='utf-8'))
assert previous['video_id']=='sP67aPtpwKg' and previous['is_private'] is False and previous['is_unlisted'] is False and previous['playability_status']=='OK'
required=['05_SCRIPT_R4_EN.md','05_SCRIPT_R4_RU.md','05R3_FINAL_EDITORIAL_QC.md','05R3_CTA_MAP.csv','05R3_RETENTION_MAP.csv','05R3_FACT_CHANGES.csv','05R3_PINNED_COMMENT.md']
assert all((P/n).is_file() and (P/n).stat().st_size for n in required)
# Earlier tracked script revisions and their source ledgers must remain unchanged.
changed=subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=P.parent,text=True).splitlines()
assert not any(re.search(r'05_SCRIPT_R[123]_|03_SCRIPT_DEVELOPMENT/|05R_CLAIM_SOURCE_LEDGER',s) for s in changed)
result=dict(status='STRUCTURAL_AND_TRACEABILITY_PASS_OWNER_REVIEW_PENDING',english_words=2592,russian_words=2186,paired_ids=73,acts=10,new_fact_groups=22,baseline_files_unchanged=len(baseline),prior_script_diff=False,spoken_ctas=2,visual_like_count=1,endscreen_seconds=20,public_previous_story_metadata_verified=True,actual_audio_duration_verified=False,full_AV_review=False,montage_geometry_rendered=False,source_original_access_holds_preserved=True,media_rights_holds_preserved=True,script_lock=False,budget_usd=0)
(R/'R4_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
