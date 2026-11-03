"""Final Script QC package checks. No generation,ASR,media editing or Resolve."""
from pathlib import Path
import csv,json,re,hashlib,difflib,subprocess
P=Path(__file__).resolve().parents[2];R=Path(__file__).resolve().parent
def csvread(f):
 with f.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
def parse(rev,lang):return re.findall(r'^\[([^]]+)\] (.+)$',(P/f'05_SCRIPT_{rev}_{lang}.md').read_text(encoding='utf-8'),re.M)
def wc(t):return len(re.findall(r"\b[\w]+(?:['?-][\w]+)*\b",t))
a,b=parse('R5_1','EN'),parse('R5_1','RU');ids=[k for k,t in a]
assert ids==[k for k,t in b] and len(ids)==len(set(ids))==69
assert sum(wc(t) for k,t in a)==2406 and sum(wc(t) for k,t in b)==2003
assert len(set(k[:3] for k in ids))==10
assert [k for k,t in a if '-CTA' in k]==['A10-CTA01']
assert not re.search(r'\b(subscribe|like this|comment below)\b',' '.join(t for k,t in a),re.I)
base=dict(parse('R5','EN'))
assert set(base)-set(ids)=={'A04-CTA01','A08-P08','A08-P09'}
assert {k for k,t in a if base[k]!=t}=={'A01-P05','A07-P06','A07-P07','A08-P04'}
assert sum(base[k]==t for k,t in a)==65
for lang in ['EN','RU']:
 old=(P/f'05_SCRIPT_R5_{lang}.md').read_text(encoding='utf-8');new=(P/f'05_SCRIPT_R5_1_{lang}.md').read_text(encoding='utf-8')
 assert '\ufffd' not in new and '???' not in new
 expected=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=f'05_SCRIPT_R5_{lang}.md',tofile=f'05_SCRIPT_R5_1_{lang}.md',n=0))
 assert expected==(R/f'R5_TO_R5_1_{lang}.diff').read_text(encoding='utf-8')
for n,h in json.loads((R/'BASELINE_SHA256.json').read_text(encoding='utf-8')).items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
audit=csvread(R/'EN_RU_LINE_AUDIT.csv');assert [x['paragraph_id'] for x in audit]==ids
assert [x['english'] for x in audit]==[t for k,t in a] and [x['russian'] for x in audit]==[t for k,t in b]
assert [x['paragraph_id'] for x in csvread(R/'R5_1_SOURCE_CROSSWALK.csv')]==ids
ret=csvread(P/'05_FINAL_RETENTION_MAP.csv');assert len(ret)==10 and sum(int(x['words']) for x in ret)==2406
ctas=csvread(P/'05_FINAL_CTA_PLACEMENT_MAP.csv');assert len([x for x in ctas if x['mode']=='VISUAL_ONLY'])==1
like=next(x for x in ctas if x['cta']=='LIKE');assert float(like['duration_seconds'])==3 and float(like['anchor_offset_seconds'])==8
tim=csvread(R/'PARAGRAPH_TIMING.csv');T={x['paragraph_id']:x for x in tim};assert float(T['A08-P03']['duration_at140'])>=11
assert abs(float(like['nominal_start_at140'])-float(T['A08-P03']['start_at140'])-8)<.002
end=next(x for x in ctas if x['cta']=='END_SCREEN');assert float(end['duration_seconds'])==20
assert float(end['nominal_start_at140'])==float(T['A10-CTA01']['end_at140'])
assert next(x for x in ctas if x['cta']=='PREVIOUS_STORY')['english']==dict(a)['A10-CTA01']
camp=json.loads((R/'CAMP_CENTURY_VERIFICATION.json').read_text(encoding='utf-8'))
assert camp['video_id']=='sP67aPtpwKg' and camp['author']=='Hidden Industrial America' and camp['is_private'] is False and camp['is_unlisted'] is False and camp['playability_status']=='OK'
claim=csvread(R/'CLAIM_STATUS_AUDIT.csv');assert len(claim)==64
assert len([x for x in claim if x['claim_id'].startswith('H') and x['final_disposition']=='EXCLUDED_HOLD_PRESERVED'])==8
rights=csvread(R/'ARCHIVE_RIGHTS_AUDIT.csv');assert len(rights)==72
rs=json.loads((R/'ARCHIVE_RIGHTS_SUMMARY.json').read_text(encoding='utf-8'));assert rs['missing_files']==[] and rs['approved_unique_moving_vehicle_seconds']==0 and rs['all_media_cleared'] is False
m=json.loads((R/'TIMING_METRICS.json').read_text(encoding='utf-8'));assert m['measured_harrison_wpm'] is None and m['actual_runtime_seconds'] is None
assert m['english_words']==2406
required=['05_SCRIPT_R5_1_EN.md','05_SCRIPT_R5_1_RU.md','05_FINAL_EDITORIAL_QC.md','05_FINAL_FACT_LEGAL_QC.md','05_FINAL_RETENTION_MAP.csv','05_FINAL_CTA_PLACEMENT_MAP.csv','05_FINAL_TIMING_REPORT.md','05_SCRIPT_LOCK_READINESS_REPORT.md','05_FINAL_PINNED_COMMENT_EN_RU.md']
assert all((P/n).is_file() and (P/n).stat().st_size>0 for n in required)
state=json.loads((P/'SOURCE_FILES/TOPIC_STATE_SNAPSHOT_2026-11-02.json').read_text(encoding='utf-8'))
assert state['script_lock'] is False and state['active_script_revision']=='R5.1' and state['script_draft']['owner_approved'] is False
changed=subprocess.check_output(['git','diff','--name-only','f0b9b7fb5ca6288dca5edfeda7a2d9b48f602d06'],cwd=P.parent,text=True)
assert not re.search(r'05_SCRIPT_R[2345]_(EN|RU)|05R_CLAIM_SOURCE_LEDGER',changed)
result=dict(status='PACKAGE_STRUCTURE_AND_TRACEABILITY_VERIFIED_OWNER_APPROVAL_HOLD',english_words=2406,russian_words=2003,paired_ids=69,unchanged_r5_paragraphs=65,rewritten_paragraphs=4,deleted_paragraphs=3,full_diff_verified=True,translation_matrix_matches_texts=True,canonical_ledger_unchanged=True,eight_exclusions_retained=True,archive_audit_rows=72,actual_harrison_rate_verified=False,full_film_AV_review=False,owner_approved=False,script_lock=False,production_started=False)
(R/'FINAL_PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(R/'DELIVERY_SHA256.json').write_text(json.dumps({n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in required},indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
