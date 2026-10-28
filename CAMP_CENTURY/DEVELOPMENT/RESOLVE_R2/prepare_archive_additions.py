from pathlib import Path
import csv,json,hashlib,subprocess
from fractions import Fraction
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'CONFORMED_25FPS';OUT.mkdir(exist_ok=True)
Q=ROOT/'QC/ARCHIVE_ADDITIONS';Q.mkdir(parents=True,exist_ok=True)
bank=list(csv.DictReader(Path(r'C:\Users\KK\CAMP_CENTURY_VIDEO007_ARCHIVE\reports\STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv').open(encoding='utf-8-sig')))
plan=json.loads((ROOT.parent/'RESOLVE_R1/SHOT_PLAN_R1.json').read_text(encoding='utf-8'))
def call(args):return subprocess.run(args,capture_output=True,check=True)
def hashes(file,extra):
    p=call(['ffmpeg','-hide_banner','-v','error','-i',str(file),'-map','0:v:0','-an',*extra,'-f','framemd5','pipe:1'])
    return [line.split(',')[-1].strip() for line in p.stdout.decode().splitlines() if line and not line.startswith('#')]
rows=[]
for sid,cid in [('S050','CC07-C038'),('S130','CC07-C053')]:
    s=next(s for s in plan if s['shot_id']==sid);r=next(r for r in bank if r['scene_id']==cid);src=Path(r['cut_filename']);n=s['duration_frames'];assert n>=125 and float(r['cut_seconds'])>=n/25
    assert cid not in {s['asset_id'] for s in plan}
    assert hashlib.sha256(src.read_bytes()).hexdigest()==r['cut_sha256']
    original=hashes(src,[]);selected=hashes(src,['-vf','fps=25','-frames:v',str(n)])
    assert len(selected)==n
    mapping=[];ambiguous=0;fps=float(Fraction(r['source_fps']))
    for j,h in enumerate(selected):
        candidates=[i for i,x in enumerate(original) if x==h and (not mapping or i>=mapping[-1])]
        assert candidates
        ambiguous+=len(candidates)>1;mapping.append(min(candidates,key=lambda i:abs(i-j*fps/25)))
    dest=OUT/(cid+'_25FPS.mp4')
    call(['ffmpeg','-hide_banner','-v','error','-y','-i',str(src),'-an','-vf','fps=25','-frames:v',str(n),'-c:v','libx264','-preset','fast','-crf','12','-pix_fmt','yuv420p',str(dest)])
    call(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(dest),'-f','null','-'])
    pr=json.loads(call(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(dest)]).stdout)
    assert int(pr['streams'][0]['nb_frames'])==n and pr['streams'][0]['r_frame_rate']=='25/1'
    sheet=Image.new('RGB',(1440,764),'#efeeeb');draw=ImageDraw.Draw(sheet)
    for j in range(6):
        at=min(j,n/25-.08);png=Q/f'{cid}_{j}.jpg'
        call(['ffmpeg','-hide_banner','-v','error','-y','-ss',str(at),'-i',str(dest),'-frames:v','1','-vf','scale=480:360,setsar=1',str(png)])
        x=j%3*480;y=j//3*382;draw.text((x+3,y+3),f'{cid} / {at:.2f}s',fill='#17242b');sheet.paste(Image.open(png),(x,y+22))
    sheet.save(Q/(cid+'_MOTION_REVIEW.jpg'),quality=94)
    master0=int(r['start_frame']);used0=master0+mapping[0];used1=master0+mapping[-1]+1
    rows.append(dict(shot_id=sid,asset_id=cid,path=str(dest),kind='REAL_ARCHIVE_MOTION',title=r['actual_shot_description'],rights=r['rights_status'],source=r['source_url'],locator=f"Native master frames {used0}..{used1} exclusive at {r['source_fps']}; derivative frames 0..{n} exclusive at 25 fps",source_in_sec=used0/fps,source_out_sec=used1/fps,source_in_frame=used0,source_out_frame_exclusive=used1,source_fps=r['source_fps'],source_sha256=r['source_sha256'],original_selected_clip=str(src),original_selected_clip_sha256=r['cut_sha256'],conformed_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),duration_frames=n,site_class=r['site_class'],warning=r['editorial_warning'],frame_map= mapping,identical_frame_mapping_ambiguities=ambiguous,review_status='TECHNICAL_PASS_AWAITING_MOTION_STRIP_VISUAL_REVIEW'))
(ROOT/'ADDITIONAL_ARCHIVE_PLACEMENTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps([dict(shot=r['shot_id'],clip=r['asset_id'],frames=r['duration_frames'],mapping_ambiguities=r['identical_frame_mapping_ambiguities']) for r in rows]),flush=True)
