#!/usr/bin/env bash
set -euo pipefail

ROOT=/tmp/hia_shorts_youtube1_model
rm -rf "$ROOT"
mkdir -p "$ROOT"/{out,qc}
cd "$ROOT"

# Current Chicago picture master under review.
gh release download chicago-r14-editorial-recut-review-20260923 \
  --repo reverendstanislav-bot/Youtube-2 \
  --pattern 'HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4'

SRC=HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4
OUT=out/CHI-S01_YOUTUBE1_MODEL_PROOF.mp4
START=11.800
DUR=34.880

# Youtube-1 canonical model:
# one continuous direct cut from the long-form master,
# synchronized blurred same-frame background,
# protected centered foreground preserving ~93% source width,
# no Shorts-only graphics, captions, titles, pans or replacement shots.
ffmpeg -hide_banner -loglevel error -y \
  -ss "$START" -t "$DUR" -i "$SRC" \
  -filter_complex "
    [0:v]split=2[bgsrc][fgsrc];
    [bgsrc]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,
           crop=1080:1920,setsar=1,
           gblur=sigma=28,
           eq=brightness=-0.17:saturation=0.82[bg];
    [fgsrc]crop=1786:1080:67:0,
           scale=1080:654:flags=lanczos,
           setsar=1[fg];
    [bg][fg]overlay=x=0:y=633:shortest=1,setsar=1[vout]
  " \
  -map "[vout]" -map 0:a:0 \
  -r 25 \
  -c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -movflags +faststart \
  "$OUT"

# Technical QC.
ffmpeg -v error -xerror -i "$OUT" -f null - 2>qc/decode_errors.txt
test ! -s qc/decode_errors.txt

width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$OUT")
height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$OUT")
fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$OUT")
pix=$(ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of csv=p=0 "$OUT")
vcodec=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$OUT")
acodec=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$OUT")
sr=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$OUT")
ch=$(ffprobe -v error -select_streams a:0 -show_entries stream=channels -of csv=p=0 "$OUT")
duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")

test "$width" = 1080
test "$height" = 1920
test "$fps" = 25/1
test "$pix" = yuv420p
test "$vcodec" = h264
test "$acodec" = aac
test "$sr" = 48000
test "$ch" = 2

# PTS continuity.
ffprobe -v error -select_streams v:0 -show_entries frame=best_effort_timestamp_time -of csv=p=0 "$OUT" > qc/frame_pts.txt
python3 - <<'PY'
pts=[]
for line in open("qc/frame_pts.txt",encoding="utf-8"):
    s=line.strip().split(",")[0]
    try: pts.append(float(s))
    except ValueError: pass
bad=sum(1 for a,b in zip(pts,pts[1:]) if abs((b-a)-0.04)>0.0003)
if bad:
    raise SystemExit(f"PTS anomalies: {bad}")
print("PTS anomalies: 0")
PY

black=$(ffmpeg -hide_banner -loglevel info -i "$OUT" -vf "blackdetect=d=0.08:pix_th=0.02" -an -f null - 2>&1 | grep -c 'black_start' || true)
test "$black" = 0

# Contact sheet from the actual proof.
mkdir -p qc/stills
for spec in "01:1.0" "02:4.0" "03:8.0" "04:12.0" "05:17.0" "06:22.0" "07:27.0" "08:32.0"; do
  n="${spec%%:*}"; t="${spec##*:}"
  ffmpeg -hide_banner -loglevel error -y -ss "$t" -i "$OUT" -frames:v 1 "qc/stills/${n}.jpg"
done
python3 - <<'PY'
from PIL import Image,ImageDraw
from pathlib import Path
files=sorted(Path("qc/stills").glob("*.jpg"))
thumbs=[]
for p in files:
    im=Image.open(p).convert("RGB")
    im.thumbnail((360,640))
    thumbs.append((p.name,im.copy()))
canvas=Image.new("RGB",(1440,1280),(18,18,18))
d=ImageDraw.Draw(canvas)
for i,(name,im) in enumerate(thumbs):
    x=(i%4)*360; y=(i//4)*640
    canvas.paste(im,(x,y))
    d.rectangle((x,y,x+120,y+28),fill=(0,0,0))
    d.text((x+8,y+7),name,fill=(255,255,255))
canvas.save("qc/CHI-S01_YOUTUBE1_MODEL_CONTACT.jpg",quality=92)
PY

sha256sum "$OUT" > qc/SHA256SUMS.txt
cat > qc/PROOF_QC.txt <<EOF
HIA Shorts — Youtube-1 model proof
Short: CHI-S01
Source: HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4
Source range: 11.800 -> 46.680
Model: direct-cut master + synchronized blurred same-frame background + protected centered ~93% foreground
Shorts-only GFX: NONE
Shorts-only captions: NONE
Shorts-only titles: NONE
New generation: NONE
HIA vertical end-card: NOT APPENDED — no owner-locked HIA Shorts card exists
Resolution: $width x $height
FPS: $fps
Video: $vcodec / $pix
Audio: $acodec / $sr Hz / $ch channels
Duration: $duration
Black events introduced: $black
Decode: PASS
PTS continuity: PASS
EOF
cat qc/PROOF_QC.txt
