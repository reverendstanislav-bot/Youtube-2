#!/usr/bin/env bash
set -euo pipefail
ROOT=/tmp/chi_s01_crop_audit
rm -rf "$ROOT"
mkdir -p "$ROOT/src" "$ROOT/audit"
cd "$ROOT/src"

gh release download chicago-r14-editorial-recut-review-20260923 \
  --repo reverendstanislav-bot/Youtube-2 \
  --pattern 'HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4'

SRC=HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4
START=11.800

python3 - <<'PY'
from pathlib import Path
samples=[0.70,2.10,4.30,7.20,10.20,13.50,17.20,21.20,24.80,28.00,31.20,33.70]
Path('/tmp/chi_s01_crop_audit/audit/samples.txt').write_text('\n'.join(str(x) for x in samples))
PY

i=0
while read -r t; do
  i=$((i+1))
  abs=$(python3 - "$START" "$t" <<'PY'
import sys
print(float(sys.argv[1])+float(sys.argv[2]))
PY
)
  ffmpeg -hide_banner -loglevel error -y -ss "$abs" -i "$SRC" -frames:v 1 "$ROOT/audit/source_$(printf '%02d' $i).jpg"
done < "$ROOT/audit/samples.txt"

python3 - <<'PY'
from PIL import Image, ImageDraw
from pathlib import Path
root=Path('/tmp/chi_s01_crop_audit/audit')
xs=[0,328,656,984,1312]
samples=sorted(root.glob('source_*.jpg'))
cellw,cellh=216,384
for p in samples:
    im=Image.open(p).convert('RGB')
    canvas=Image.new('RGB',(cellw*len(xs),cellh),(14,14,14))
    d=ImageDraw.Draw(canvas)
    for j,x in enumerate(xs):
        c=im.crop((x,0,x+608,1080)).resize((cellw,cellh),Image.Resampling.LANCZOS)
        canvas.paste(c,(j*cellw,0))
        d.rectangle((j*cellw,0,j*cellw+70,24),fill=(0,0,0))
        d.text((j*cellw+6,5),f'x={x}',fill=(255,255,255))
    canvas.save(root/f'{p.stem}_candidates.jpg',quality=92)

thumbw,thumbh=320,180
cols=3
rows=(len(samples)+cols-1)//cols
sheet=Image.new('RGB',(thumbw*cols,thumbh*rows),(12,12,12))
d=ImageDraw.Draw(sheet)
for i,p in enumerate(samples):
    im=Image.open(p).convert('RGB').resize((thumbw,thumbh),Image.Resampling.LANCZOS)
    x=(i%cols)*thumbw; y=(i//cols)*thumbh
    sheet.paste(im,(x,y))
    d.rectangle((x,y,x+100,y+22),fill=(0,0,0))
    d.text((x+5,y+4),p.stem,fill=(255,255,255))
sheet.save(root/'SOURCE_OVERVIEW.jpg',quality=92)
PY

ffprobe -v error -show_entries stream=width,height,r_frame_rate,pix_fmt -of default=nw=1 "$SRC" > "$ROOT/audit/SOURCE_INFO.txt"

# trigger crop audit
