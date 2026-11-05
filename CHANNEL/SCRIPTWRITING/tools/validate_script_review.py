#!/usr/bin/env python3
"""Check review-record integrity; never judge narrative quality or grant Script Lock."""
import argparse
import json
import re
from pathlib import Path
IDS = {f'QC{i:02d}' for i in range(1, 21)}
CRITICAL = {'QC01','QC02','QC03','QC05','QC07','QC08','QC09','QC11','QC13','QC16','QC17','QC18','QC20'}

def validate(record):
    errors = []
    if not isinstance(record, dict):
        return {'valid':False,'readiness':'HOLD','errors':['Record must be object'],'script_lock_granted':False}
    if record.get('schema') != 'HIA_SCRIPT_REVIEW_V1': errors.append('Wrong schema')
    items = record.get('items')
    if not isinstance(items, list):
        return {'valid':False,'readiness':'HOLD','errors':['items must be list'],'script_lock_granted':False}
    ids = [x.get('id') for x in items if isinstance(x, dict)]
    if len(items)!=20 or len(ids)!=20 or any(not isinstance(x,str) for x in ids) or set(str(x) for x in ids)!=IDS:
        errors.append('Exactly one row each QC01-QC20 required')
    for x in items:
        if not isinstance(x,dict):
            errors.append('Each item must be object');continue
        key=x.get('id');status=x.get('status')
        if status not in ('PASS','HOLD','REJECT'):errors.append(f'{key}: invalid status')
        if type(x.get('critical')) is not bool or x.get('critical')!=(str(key) in CRITICAL):errors.append(f'{key}: critical flag differs from canon')
        evidence=x.get('evidence')
        if not isinstance(evidence,list) or any(not isinstance(v,str) or not v.strip() for v in evidence):errors.append(f'{key}: evidence must be nonempty-string list')
        if status=='PASS' and not evidence:errors.append(f'{key}: PASS requires specific evidence')
        if status in ('HOLD','REJECT') and not str(x.get('action','')).strip():errors.append(f'{key}: corrective action required')
    all_pass=len(items)==20 and all(isinstance(x,dict) and x.get('status')=='PASS' for x in items)
    approval=record.get('owner_approval')
    if not isinstance(approval,dict) or type(approval.get('approved')) is not bool:
        errors.append('owner_approval.approved must be boolean');approval={}
    if approval.get('approved') and (not isinstance(approval.get('evidence'),str) or not approval['evidence'].strip() or not all_pass):errors.append('Owner approval requires evidence and all rows resolved')
    if all_pass:
        for key in ['script_path','reviewer','review_date']:
            if not str(record.get(key,'')).strip() or str(record[key]).startswith('REPLACE_'):errors.append(f'Completed review needs {key}')
        if not re.fullmatch(r'[0-9a-fA-F]{64}',str(record.get('script_sha256',''))):errors.append('Completed review needs actual script SHA256')
    rejected=any(isinstance(x,dict) and x.get('status')=='REJECT' for x in items)
    return {'valid':not errors,'errors':errors,'readiness':'REJECT' if rejected else 'READY_FOR_OWNER_REVIEW' if all_pass and not errors else 'HOLD','owner_approval_recorded':approval.get('approved',False),'script_lock_granted':False,'semantic_verification':'NOT_PERFORMED_BY_THIS_TOOL'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('review',type=Path);a=parser.parse_args()
    try:result=validate(json.loads(a.review.read_text(encoding='utf-8-sig')))
    except (OSError,ValueError,TypeError) as e:result={'valid':False,'errors':[str(e)],'readiness':'HOLD','script_lock_granted':False}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result.get('valid') else 2
if __name__=='__main__':raise SystemExit(main())
