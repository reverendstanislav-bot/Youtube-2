import os,re,zipfile,subprocess,glob,csv,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path.cwd(); W,H,FPS=960,540,30
GEN=ROOT/'12_#U0413#U0435#U043d#U0435#U0440#U0430#U0446#U0438#U0438'/'FINAL_62'
ARC=ROOT/'04_DOWNLOADS'/'ARCHIVE_GREEN'; WORK=ROOT/'_EDIT_WORK'; SEG=WORK/'segments_v2'; GFX=WORK/'gfx_v2'
for d in (SEG,GFX): d.mkdir(parents=True,exist_ok=True)
XLSX=ROOT/'03_TIMELINE'/'TC497_FINAL_VISUAL_TIMELINE_CODEX_EDIT_MAP_v2.xlsx'
VO=ROOT/'01_AUDIO'/'TC497_FINAL_VO.mp3'; V1=ROOT/'_EDIT_WORK'/'V1.mp4'

def rows():
 ns={'a':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 with zipfile.ZipFile(XLSX) as z:
  sh=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   x=ET.fromstring(z.read('xl/sharedStrings.xml'))
   for si in x.findall('a:si',ns): sh.append(''.join(t.text or '' for t in si.iter('{%s}t'%ns['a'])))
  x=ET.fromstring(z.read('xl/worksheets/sheet1.xml')); out=[]
  for row in x.findall('.//a:sheetData/a:row',ns)[4:]:
   v={}
   for c in row.findall('a:c',ns):
    m=re.match(r'[A-Z]+',c.attrib.get('r','')); col=m.group(0) if m else ''
    t=c.attrib.get('t'); q=c.find('a:v',ns)
    if t=='inlineStr':
     e=c.find('a:is',ns); val=''.join(y.text or '' for y in e.iter('{%s}t'%ns['a'])) if e is not None else ''
    elif q is None: val=''
    else: val=sh[int(q.text)] if t=='s' else q.text
    v[col]=val
   if v.get('A','').isdigit():
    v['start']=float(v['B'])*86400; v['end']=float(v['C'])*86400; out.append(v)
 return out

def raster_pdf(p,code):
 out=WORK/f'{code}.png'
 if not out.exists(): subprocess.run(['pdftoppm','-f','1','-singlefile','-png','-r','140',str(p),str(out.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 return out

def asset(code):
 p=GEN/f'{code}.png'
 if p.exists(): return p
 gs=glob.glob(str(ARC/f'{code}__*'))
 if gs:
  p=Path(gs[0]); return raster_pdf(p,code) if p.suffix.lower()=='.pdf' else p
 return None

CM={'CP-COLD01':('AR-A01','ST-COLD'),'CP-COLD02':('ST-COLD','WB-C01'),'CP-R01':('AR-DEW-MAP','AR-DEW-RADAR'),
'CP-R02':('AR-DEW-MAP','WC-R03'),'CP-E01':('AR-PATENT','WA-09'),'CP-B01':('AR-SNO','WC-B03'),
'CP-L01':('AR-A01','WB-L02'),'CP-L02':('WB-L04','WB-L06'),'CP-H02':('WA-04R','WA-11R'),
'CP-H01':('AR-OTTER2','WA-12'),'CP-N01':('WB-N01','WB-N02'),'CP-N02':('WB-N01','AR-A01'),
'CP-Y01':('AR-OTTER2','WC-Y01'),'CP-Y02':('AR-OTTER2','WC-Y01'),'CP-T01':('AR-OTTER2','WD-T01'),
'CP-T02':('AR-OTTER2','WC-Y02'),'CP-W01':('AR-A01','WD-W01'),'CP-W02':('AR-A01','WD-W02'),
'CP-D01':('WC-D01','AR-CH54-1'),'CP-D02':('AR-A01','AR-CH54-2')}

R=rows()
# preserve V1 graphics as clean frozen source frames
for r in R:
 if r.get('G')=='Graphic':
  out=GFX/f"{r['H']}.png"
  if not out.exists():
   t=(r['start']+r['end'])/2
   subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t:.3f}','-i',str(V1),'-frames:v','1',str(out)],check=True)

use={}
def mode(r):
 code=r.get('H',''); typ=r.get('G',''); inst=(r.get('L','') or '').lower()
 use[code]=use.get(code,0)+1; k=use[code]
 if typ=='Graphic': return 'STATIC'
 if 'hard cut' in inst or 'hold' in inst: return 'STATIC'
 if 'pan' in inst or 'route' in inst: return 'PAN_R' if k%2 else 'PAN_L'
 if 'push' in inst: return 'PUSH'
 if 'crop' in inst or 'detail' in inst: return 'DETAIL'
 if typ=='Archive': return ['STATIC','PAN_R','DETAIL','PAN_L'][(k-1)%4]
 if typ=='Generated': return ['PUSH','STATIC','PULL','DETAIL','PAN_R'][(k-1)%5]
 return 'STATIC'

def vf(m,n,gen=False):
 b="scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160"
 den=max(n-1,1)
 if m=='STATIC': c="scale=960:540"
 elif m=='PUSH': c=f"zoompan=z='1+0.035*on/{den}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=960x540:fps={FPS}"
 elif m=='PULL': c=f"zoompan=z='1.035-0.035*on/{den}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=960x540:fps={FPS}"
 elif m=='PAN_L': c=f"zoompan=z='1.07':x='(iw-iw/zoom)*(1-on/{den})':y='ih/2-(ih/zoom/2)':d={n}:s=960x540:fps={FPS}"
 elif m=='PAN_R': c=f"zoompan=z='1.07':x='(iw-iw/zoom)*(on/{den})':y='ih/2-(ih/zoom/2)':d={n}:s=960x540:fps={FPS}"
 else: c=f"zoompan=z='1.12':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=960x540:fps={FPS}"
 grade=",eq=saturation=0.82:contrast=1.02" if gen else ",eq=saturation=0.92:contrast=1.01"
 return f"{b},{c}{grade},format=yuv420p"

def one(src,out,n,m,gen=False):
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(src),'-vf',vf(m,n,gen),'-frames:v',str(n),'-an','-c:v','libx264','-preset','ultrafast','-crf','29','-pix_fmt','yuv420p',str(out)],check=True)

def composite(code,out,n):
 a,b=CM[code]; sa,sb=asset(a),asset(b); na=n//2+8; nb=n-na+16
 ta=WORK/'a.mp4'; tb=WORK/'b.mp4'; one(sa,ta,na,'STATIC',a.startswith(('ST-','W'))); one(sb,tb,nb,'PUSH' if b.startswith(('ST-','W')) else 'STATIC',b.startswith(('ST-','W')))
 dur=.30; off=max(.01,na/FPS-dur)
 fc=f"[0:v]fps={FPS},settb=AVTB,setpts=PTS-STARTPTS[a];[1:v]fps={FPS},settb=AVTB,setpts=PTS-STARTPTS[b];[a][b]xfade=transition=fade:duration={dur}:offset={off},trim=duration={n/FPS},setpts=PTS-STARTPTS[v]"
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(ta),'-i',str(tb),'-filter_complex',fc,'-map','[v]','-an','-c:v','libx264','-preset','ultrafast','-crf','29','-pix_fmt','yuv420p',str(out)],check=True)

def ts(s):
 h=int(s//3600); s-=h*3600; m=int(s//60); s-=m*60; return f'{h}:{m:02d}:{s:05.2f}'
ass=WORK/'labels_v2.ass'; seen=set()
with open(ass,'w',encoding='utf-8') as f:
 f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 960\nPlayResY: 540\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Chapter,DejaVu Sans,28,&H00EBF3F3,&H000000FF,&H00171A1C,&H65000000,-1,0,0,0,100,100,1,0,1,2,0,7,42,30,34,1\nStyle: Bug,DejaVu Sans,13,&H00DDE6E6,&H000000FF,&H00171A1C,&H80000000,0,0,0,0,100,100,1,0,1,1,0,3,20,24,20,1\nStyle: Title,DejaVu Sans,32,&H00EBF3F3,&H000000FF,&H00171A1C,&H65000000,-1,0,0,0,100,100,1,0,1,2,0,5,60,60,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
 for r in R:
  ch=r.get('E','')
  if ch and ch not in seen and ch!='Cold Open':
   seen.add(ch); f.write(f"Dialogue: 0,{ts(r['start'])},{ts(min(r['end'],r['start']+2))},Chapter,,0,0,0,,{ch.upper()}\n")
  if r.get('G') in ('Generated','Composite'):
   lab='CONCEPT' if 'Nuclear' in ch else ('RECONSTRUCTION' if 'RECONSTRUCTION' in (r.get('K','') or '') else '')
   if lab: f.write(f"Dialogue: 0,{ts(r['start']+.15)},{ts(max(r['start']+.3,r['end']-.15))},Bug,,0,0,0,,{lab}\n")
 f.write(f"Dialogue: 1,{ts(80.840)},{ts(82.600)},Title,,0,0,0,,AMERICA BUILT A 572-FOOT TRAIN\\NTHAT NEEDED NO TRACKS\n")

rep=[]; prev=None
with open(WORK/'concat_v2.txt','w') as lf:
 for r in R:
  i=int(r['A']); code=r.get('H',''); typ=r.get('G',''); n=max(1,round((r['end']-r['start'])*FPS)); out=SEG/f'{i:03d}.mp4'
  if typ=='Composite': composite(code,out,n); m='A_TO_B'
  else:
   src=GFX/f'{code}.png' if typ=='Graphic' else asset(code)
   if code=='AR-A03': src=asset('WD-LC01' if i<125 else 'WD-LC03')
   if not src: raise SystemExit(f'MISSING {i} {code}')
   m=mode(r)
   if code==prev and m=='STATIC': m='DETAIL'
   one(src,out,n,m,typ=='Generated')
  lf.write(f"file '{out.resolve()}'\n"); rep.append([i,r['start'],r['end'],typ,code,m]); prev=code
  if i%20==0: print('rendered',i,flush=True)
with open(WORK/'V2_EDIT_DECISIONS.csv','w',newline='') as f:
 w=csv.writer(f); w.writerow(['#','start','end','type','asset','motion']); w.writerows(rep)
silent=WORK/'silent_v2.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(WORK/'concat_v2.txt'),'-c','copy',str(silent)],check=True)
final=ROOT/'_V2'/'TC497_FIRST_CUT_PROXY_V2.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(silent),'-i',str(VO),'-vf',f'ass={ass}','-c:v','libx264','-preset','ultrafast','-crf','27','-c:a','aac','-b:a','128k','-t','1236.506122','-movflags','+faststart',str(final)],check=True)
print('FINAL',final,final.stat().st_size)
