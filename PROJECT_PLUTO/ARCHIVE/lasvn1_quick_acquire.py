#!/usr/bin/env python3
"""Single-fetch research only. NARA govt period film, Rutube mirror; rights HOLD."""
import pathlib,subprocess,json,hashlib
import imageio_ffmpeg
dest=pathlib.Path("LASVN1_RESEARCH_1963");dest.mkdir(exist_ok=True)
url="https://rutube.ru/video/7d865693ec753bcbed4d97c4277edcdb/"
subprocess.run(["yt-dlp","--no-playlist","-f","best[ext=mp4]/best",
 "--no-part","--no-write-auto-subs","-o",str(dest/"USAF38912_LASVN1_1963.%(ext)s"),url],
 check=True,timeout=1200)
files=[x for x in dest.iterdir() if x.suffix.lower() in (".mp4",".webm",".mkv")]
if len(files)!=1:raise RuntimeError("Exactly one film was expected: "+str(files))
media=files[0]
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
# Representative screens at genuine time positions; use accessible research source.
seconds=[0,240,335,385,500,610,765,875,920,1000,1060,1160,1240,1340,1430,1530,1590]
for s in seconds:
 out=dest/f"LASVN1_SEC_{s:04d}.jpg"
 subprocess.run([ffmpeg,"-hide_banner","-loglevel","error","-ss",str(s),"-i",str(media),"-frames:v","1","-q:v","3","-y",str(out)],check=True,timeout=120)
h=hashlib.sha256()
with media.open("rb") as f:
 for c in iter(lambda:f.read(1048576),b""):h.update(c)
data={"id":"USAF 38912 LASV-N1 1963 progress film","mirror":url,"original_archive":"NARA RG342 accession NN3-342-94-001","bytes":media.stat().st_size,"sha256":h.hexdigest(),
"file":media.name,"QC":"SOURCE_BINARY_DOWNLOAD_CHECKED_AND_SAMPLE_FRAMES_EXTRACTED",
"license":"PUBLIC US GOVERNMENT HISTORICAL SOURCE — THIRD PARTY MIRROR/RESTORATION LICENSE STILL HOLD",
"direct_1964_reactor_film":False}
(dest/"PROVENANCE_QC.json").write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps(data),flush=True)
