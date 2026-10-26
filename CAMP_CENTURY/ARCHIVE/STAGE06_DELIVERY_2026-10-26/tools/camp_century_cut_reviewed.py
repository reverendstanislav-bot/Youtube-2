"""Stage06 R5 extraction adapter: retains R5 eligibility gates, caches source hashes,
uses accurate input seeking, and documents Codex-only review rather than human signoff.
No narration, image generation, enhancement or frame-rate conversion.
"""
import json, math, csv, importlib.util, subprocess
from pathlib import Path
from fractions import Fraction
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
ROOT=Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE')
REPO=Path(r'C:\Users\KK\Youtube-2-CAMP-CENTURY-VIDEO007')
spec=importlib.util.spec_from_file_location('r5',REPO/'CAMP_CENTURY/ARCHIVE/STAGE06_R5_TOOLKIT/tools/stage06_real_footage.py')
r5=importlib.util.module_from_spec(spec);spec.loader.exec_module(r5)
notes=json.loads(Path(r'C:\Users\KK\camp_century_review_notes.json').read_text())
notes['reviewed_candidate_pages']=list(range(1,23))
notes['reject'].update({
 'CC07-C009':'Additional short tractor pass duplicates the visual function of stronger complete convoy actions; no need to pad logistics coverage.',
 'CC07-C076':'Very little discernible action in the selected machinery close-up; stronger removal actions retained.',
 'CC07-C079':'Long largely static transport-load view; reject rather than increase runtime.',
 'CC07-C087':'Interval mixes bakery, food insert and a brief corridor view; no meaningful 5-second corridor action.'})
notes['updates'].update({
 'CC07-C015':{'start_sec':614.0,'end_sec':620.0,'actual_shot_description':'Army construction sequence: steel trench arches and crew placing snow blocks beside the covered trench'},
 'CC07-C027':{'start_sec':1144.0,'actual_shot_description':'Construction supplies beside the camp workshop, followed by a tracked vehicle driving through the garage arch'},
 'CC07-C047':{'start_sec':1783.5,'end_sec':1790.2,'actual_shot_description':'Camp meal sequence: food serving, a loaded tray and personnel eating in the dining hall'},
 'CC07-C077':{'actual_shot_description':'Interior view into the opened circular PM-2A vessel housing during dismantling','editorial_warning':'Inside the plant, not a component emerging onto the surface; severely magenta public print. Not fuel-handling instruction.'},
 'CC07-C082':{'actual_shot_description':'Close view of the loaded tractor-sled followed by the departing 1964 removal convoy','site_class':'SAME_PROJECT_SUPPLY_CHAIN','editorial_warning':'1964 outgoing transport route; this interval is not the Camp Tuto loading ramp. Severely magenta print.'},
 'CC07-C086':{'actual_shot_description':'Army officer explains a PM-2A display to visiting scientific aides at Camp Century','editorial_warning':'Actual scientific-aide visit; not Iceworm disclosure or an operational missile installation. Original end dissolve retained.'}})
Path(r'C:\Users\KK\camp_century_review_notes.json').write_text(json.dumps(notes,indent=2),encoding='utf-8')
rows=json.loads((ROOT/'reports/CANDIDATE_SCENES.json').read_text())
accepted=[];rejected=[];changed=[]
for row in rows:
 sid=row['scene_id']
 if sid in notes['reject']:
  row.update(status='REJECTED_EDITORIAL',rejection_reason=notes['reject'][sid]);rejected.append(row);continue
 update=notes['updates'].get(sid,{})
 row.update(update)
 fps=float(Fraction(row['source_fps']))
 st=math.ceil(row['start_sec']*fps-0.0001);en=math.floor(row['end_sec']*fps+0.0001)
 row.update(start_frame=st,end_frame_exclusive=en,start_sec=st/fps,end_sec=en/fps,seconds=(en-st)/fps)
 assert 5<=row['seconds']<=20,(sid,row['seconds'])
 row.update(start_tc=f"{row['start_sec']:.9f}",end_tc=f"{row['end_sec']:.9f}",rights_receipt=f"{row['source_id']}_RIGHTS.md",verified_by='Codex: source-index plus eight-phase candidate review; not owner or independent human signoff',status='APPROVED',duplicate_of='')
 accepted.append(row)
 if 'start_sec' in update or 'end_sec' in update:changed.append(row)
for i,a in enumerate(accepted):
 for b in accepted[i+1:]:
  if a['source_id']==b['source_id']:
   assert min(a['end_sec'],b['end_sec'])<=max(a['start_sec'],b['start_sec'])+0.001,('OVERLAP',a['scene_id'],b['scene_id'])
(ROOT/'reports/REVIEWED_SCENES.json').write_text(json.dumps(accepted,indent=2))
(ROOT/'reports/REJECTED_CANDIDATES.json').write_text(json.dumps(rejected,indent=2))
r5.write_rows(ROOT/'approved_ranges.csv',accepted,r5.HEADERS)
rights={
 'F01B':'''# F01B selected Army picture: rights and limits
Item: https://archive.org/details/gov.dod.dimoc.26064
US Department of Defense PIN 26064 / US Army Research and Development Progress Report No.6, The Story of Camp Century.
IA metadata carries a CC0/public-domain dedication. USACE official matching work: https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 ; its API expressly states that the federal-agency video is public domain. Matching original-title and construction/plant sequences were visually compared; alternate print is not an additional film.
Selected intervals show Army project operations and facilities. No unrelated third-party painting, entertainment or commercial insert selected. Silent picture only; original narrator/music excluded. Government insignia do not imply endorsement. This is an evidence-based editorial rights determination, not legal advice or owner approval.
Local evidence: records/F01B_IA_METADATA.txt and records/F01_USACE_API.txt.
Quality: native SD 720x480, SAR8:9,29.97fps. Original audio has DTS/null-mux errors; video-only full decode passed. No original audio exported. F01 USACE copy has inferior color and is excluded as duplicate alternate print.
''',
 'F03':'''# F03 selected Army PM-2A removal picture: rights and limits
Official item: https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv
Official USACE ERDC / Army Pictorial Center release, marked PUBLIC DOMAIN on DVIDS.
Policy: https://www.dvidshub.net/about/copyright . US-government works generally public domain; third-party components and endorsement restrictions still require care.
Selected silent pictures show the actual 1964 Camp Century PM-2A dismantling and its identified supply route. Fort Belvoir training/mockup, unrelated intro reuse, original narrator and music excluded. Do not identify route, Tuto or Thule as inside Camp Century. Film issued1965, removal shownMarch-July1964. No endorsement implied.
Local primary receipts: records/F03_DVIDS_ITEM.txt, F03_DVIDS_RIGHTS.txt, F03_DVIDS_PLAYER.txt and F03_PUBLIC_HLS.txt.
Maximum anonymously accessible copy located:640x480 player MP4. Official720x480 download returned HTTP403, recorded separately. Strong magenta dye fading is in source; no restoration or HD claim. Future better-copy acquisition remains HOLD.
''',
 'F05':'''# F05 selected Army base pictures only: rights and limits
Item: https://archive.org/details/gov.archives.arc.2569758
NARA ARC2569758 /111-TV-520, US Army Big Picture: US Army and the Boy Scouts. IA item metadata public-domain/CC0 label and Army/NARA provenance support the selected Army base footage.
IMPORTANT: the film contains an explicit third-party copyright/permission slate for Norman Rockwell Boy Scout paintings belonging to Brown and Bigelow. The full film is NOT blanket-cleared. ALL painting/studio/entertainment and unrelated-location sequences excluded. Only reviewed Camp Century scientific-aide visit intervals near81-87 and139-147seconds selected. All clips silent; original narrator/music excluded. No endorsement implied.
Receipt: records/F05_IA_METADATA.txt; copyright slate visible near1680s in full-source QC sheet. Selected footage does not contain the paintings. Rights determination applies only to selected Army pictures.
Native720x48029.97, source bottom-field-first. H264 clip preserves BFF field coding; no invented upscaling or25fps conversion.
'''}
for sid,txt in rights.items():(ROOT/'rights_receipts'/f'{sid}_RIGHTS.md').write_text(txt,encoding='utf-8')
def preview(row):
 canvas=Image.new('RGB',(960,420),'#101010');d=ImageDraw.Draw(canvas)
 for k in range(8):
  t=row['start_sec']+(row['seconds']-0.08)*k/7
  p=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',row['source_path'],'-frames:v','1','-vf','scale=240:180','-f','image2pipe','-vcodec','mjpeg','-'],capture_output=True,check=True)
  import io
  canvas.paste(Image.open(io.BytesIO(p.stdout)),((k%4)*240,(k//4)*180))
 d.text((5,370),f"{row['scene_id']} revised {row['start_sec']:.3f}-{row['end_sec']:.3f} {row['seconds']:.3f}s",fill='white')
 canvas.save(ROOT/'qc_sheets/candidate_motion'/f"{row['scene_id']}_REVISED.jpg")
if __name__=='__main__':
 import sys
 if '--prepare' in sys.argv:
  with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(preview,changed))
  print('PREPARED',len(accepted),'seconds',sum(x['seconds'] for x in accepted),'rejected',len(rejected),'changed', [x['scene_id'] for x in changed]);raise SystemExit
 # Retain all R5 cut eligibility checks. Cache only unchanged files, using physical stat identity.
 original_digest=r5.digest;cache={}
 def cached_digest(p):
  s=p.stat();key=(str(p),s.st_size,s.st_mtime_ns)
  if key not in cache:cache[key]=original_digest(p)
  return cache[key]
 r5.digest=cached_digest
 original_process=r5.process
 def efficient_process(args,**kw):
  if args[0]=='ffmpeg' and '-c:v' in args and args[args.index('-c:v')+1]=='libx264':
   ix=args.index('-ss');ts=args[ix+1];del args[ix:ix+2]
   ix=args.index('-i');args[ix:ix]=['-ss',ts]
   args[-1:-1]=['-threads','2']
   if 'F05.mpeg' in str(args):args[-1:-1]=['-flags','+ilme+ildct','-x264-params','bff=1']
  return original_process(args,**kw)
 r5.process=efficient_process
 r5.extract(ROOT)
