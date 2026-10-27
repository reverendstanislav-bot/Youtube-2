from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parent
OUT=Path(r'C:\Users\KK\Movies\HIA_VIDEO007_R1')
WAV=Path(r'C:\YOUTUBE\Youtube 2\VIDEO 7\AUDIO\VOICEBOX_ARTHUR_V1\HIA_VIDEO007_CAMP_CENTURY_ARTHUR_MASTER_48K_MONO_S24.wav')
ap=argparse.ArgumentParser();ap.add_argument('--chapters',type=int,default=8);args=ap.parse_args()
rows=json.loads((ROOT/'CHAPTER_RENDER_RESULTS.json').read_text())[:args.chapters]
assert len(rows)==args.chapters
frames=sum(r['frames'] for r in rows)
concat=OUT/f'CONCAT_{args.chapters}_CHAPTERS.txt'
concat.write_text(''.join("file '"+r['file'].replace('\\','/')+"'\n" for r in rows),encoding='utf-8')
name='HIA_VIDEO007_CAMP_CENTURY_R1_PROXY_720P25.mp4' if args.chapters==8 else f'HIA_VIDEO007_R1_FIRST_{args.chapters}_CHAPTERS_PARTIAL.mp4'
dest=OUT/name
subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(WAV),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','1','-t',str(frames/25),'-movflags','+faststart',str(dest)],check=True)
print(json.dumps(dict(file=str(dest),frames=frames,seconds=frames/25,scope='FULL_PROXY' if args.chapters==8 else 'PARTIAL_PREVIEW_NOT_FULL_FILM',video='Copied native Resolve-encoded chapter streams without re-encoding',audio='Complete locked master used from sample zero; AAC proxy encoding; source unchanged')))
