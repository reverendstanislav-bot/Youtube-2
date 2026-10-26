"""Validate/unpack-relative ImageGen inputs and write call arguments. NEVER generates images.
Usage: python tools/prepare_imagegen_calls.py --verify-only
       python tools/prepare_imagegen_calls.py
"""
import argparse,json,hashlib
from pathlib import Path
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
 root=Path(__file__).resolve().parent.parent
 refs={r['reference_id']:r for r in json.loads((root/'REFERENCE_REGISTER.json').read_text(encoding='utf-8'))}
 assets=json.loads((root/'ASSET_PRODUCTION_QUEUE.json').read_text(encoding='utf-8'))
 calls=[]
 for a in assets:
  if a['production_route']!='IMAGEGEN_REFERENCED_ILLUSTRATION':continue
  assert a['status']=='PREPARATION_READY_REFERENCES_REVIEWED_OUTPUT_NOT_GENERATED',a['asset_id']
  paths=[]
  for rid in a['reference_ids']:
   r=refs[rid];p=(root/r['file']).resolve()
   assert root.resolve() in p.parents and p.is_file(),str(p)
   assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],rid
   assert 'RESEARCH_ONLY' not in str(p) and rid!='R09_AIR_WELL'
   paths.append(str(p))
  prompt=(root/a['prompt_file']).read_text(encoding='utf-8')
  assert paths and 'Primary request:' in prompt and 'Text (verbatim' in prompt
  calls.append({'asset_id':a['asset_id'],'call_status':'PREPARATION_ONLY_DO_NOT_EXECUTE','tool':'image_gen.imagegen','arguments':{'prompt':prompt,'referenced_image_paths':paths,'transparent_background':False},'output_intent':a['asset_id']+'_R1.png'})
 assert len(calls)==10
 if not args.verify_only:(root/'IMAGEGEN_CALLS_PREPARED_NOT_EXECUTED.json').write_text(json.dumps(calls,indent=2),encoding='utf-8')
 print('PREPARATION_INPUTS_VALID:10 jobs; all image files and SHA256 verified; NO generation executed.')
if __name__=='__main__':main()
