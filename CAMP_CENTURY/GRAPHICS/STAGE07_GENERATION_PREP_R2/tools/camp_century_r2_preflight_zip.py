import csv,json,hashlib,zipfile,re,subprocess,shutil
from pathlib import Path
from html.parser import HTMLParser
R=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007');P=R/'CAMP_CENTURY/GRAPHICS/STAGE07_GENERATION_PREP_R2'
for md in P.rglob('*.md'):
 text=md.read_text(encoding='utf-8');clean=re.sub(r'[ \t]+(?=\n|$)','',text)
 if clean!=text:md.write_text(clean,encoding='utf-8')
def csvout(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
refs=json.loads((P/'REFERENCE_REGISTER.json').read_text());assets=json.loads((P/'ASSET_PRODUCTION_QUEUE.json').read_text());calls=json.loads((P/'IMAGEGEN_CALLS_PREPARED_NOT_EXECUTED.json').read_text())
assert len(refs)==37 and len(assets)==60 and len(calls)==24
assert len(list((P/'references').glob('*.jpg')))==37
for r in refs:
 p=P/r['file'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 if r['reference_id']=='R33_FIRN_FORECAST':r['visual_review']='CODEX_CHECKED_ORIGINAL_PDF_FIG10_CROP_LEGEND_BOTH_SCALES_FULL_CAPTION'
(P/'REFERENCE_REGISTER.json').write_text(json.dumps(refs,indent=2));csvout(P/'REFERENCE_REGISTER.csv',refs)
beats=list(csv.DictReader((R/'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv').open(encoding='utf-8-sig',newline='')));by={r['beat_id']:r for r in beats}
for a in assets:
 assert (P/a['prompt_file']).is_file()
 assert a['voice_cue_exact'] in by[a['primary_cue_beat']]['spoken_text_exact'],a['asset_id']
 assert a['voice_cue_exact'] in a['voice_context_exact']
 assert a['global_word_in_0based']<a['global_word_out_exclusive']<=2931
 if a['asset_id'].startswith('G'):assert a['provenance_class']=='CONCEPT' and a['reference_ids']
for c in calls:
 assert c['call_status']=='PREPARATION_ONLY_DO_NOT_EXECUTE'
 for s in c['arguments']['referenced_image_paths']:assert P.resolve() in Path(s).resolve().parents and Path(s).is_file()
units=list(csv.DictReader((P/'V4_PARAGRAPH_VISUAL_UNITS.csv').open(encoding='utf-8-sig',newline='')))
assert len(units)==190 and sum(int(u['word_count']) for u in units)==2931
maps=list(csv.DictReader((P/'V4_ALL_32_BEATS_ASSET_AND_MOTION_MAP.csv').open(encoding='utf-8-sig',newline='')))
assert len(maps)==32 and all(m['prepared_assets'] or m['real_motion_clip_ids'] or m['alternate_evidence_options'] for m in maps)
assert len(list(csv.DictReader((P/'ASSET_NARRATION_PLACEMENT_CUES.csv').open(encoding='utf-8-sig',newline=''))))==60
html=(P/'INDEX.html').read_text(encoding='utf-8');assert html.count('Exact narration cue:')==60
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['src','href'] and v and not v.startswith(('http:','https:','#')):assert (P/v).is_file(),v
Links().feed(html)
sourceh={'CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_FULL_NARRATION_V4_EN.md':'0006d5345bae22b77f3556dcb8090ce167f34292','CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt':'46fafe9914c1a061e9f219c344698f9857019973','CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv':'aea8122f66765b049effd61d6bc0eb4780250407'}
for f,v in sourceh.items():assert subprocess.check_output(['git','-c','safe.directory='+str(R).replace('\\','/'),'-C',str(R),'rev-parse','HEAD:'+f]).decode().strip()==v
q=json.loads((P/'qc/PREPARATION_QC.json').read_text());assert q['generation_outputs']==0 and q['paid_credits_spent']==0
q.update(preparation_integrity='PASS_WITH_DECLARED_SOURCE_HOLDS_NOT_VISUAL_OUTPUT_PASS',literal_cues_pass=60,word_text_integrity='2931unchanged across190paragraph units',source_v4_blobs_unchanged=True,graph_reference_quality='Actual original PDF Fig10 cropped with full caption; native vector/text source retained locally')
(P/'qc/PREPARATION_QC.json').write_text(json.dumps(q,indent=2))
shutil.copyfile(Path(__file__),P/'tools'/Path(__file__).name)
files=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  assert p.suffix.lower() not in ['.pdf','.mp4','.mpeg','.wav','.pyc']
  if p.name!='PACKAGE_FILES_SHA256.csv':files.append({'relative_path':str(p.relative_to(P)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
csvout(P/'PACKAGE_FILES_SHA256.csv',files)
z=Path(r'C:\Users\KK\Downloads\HIA_CAMP_CENTURY_STAGE07_GENERATION_PREP_R2.zip')
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for p in sorted(P.rglob('*')):
  if p.is_file():out.write(p,str(Path('HIA_CAMP_CENTURY_STAGE07_GENERATION_PREP_R2')/p.relative_to(P)))
with zipfile.ZipFile(z) as check:assert check.testzip() is None
print('R2_PREFLIGHT_PASS:60literal-cue-bound briefs;24referenced generation jobs;20document/photo treatments;16data/logic diagrams;37real references;32beat pools;190paragraph index entries;2931words unchanged;0generation calls.')
print('ZIP',str(z),'BYTES',z.stat().st_size,'SHA256',hashlib.sha256(z.read_bytes()).hexdigest())
