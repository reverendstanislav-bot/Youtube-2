#!/usr/bin/env bash
set -euo pipefail
ROOT=/tmp/chi_s01_crop_audit_fast
rm -rf "$ROOT"
mkdir -p "$ROOT/src" "$ROOT/audit"
cd "$ROOT/src"

gh release download chicago-r14-editorial-recut-review-20260923 \
  --repo reverendstanislav-bot/Youtube-2 \
  --pattern 'HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4'

SRC=HIA_CHICAGO_R14_EDITORIAL_RECUT_REVIEW_1920x1080.mp4
START=11.800

cat > "$ROOT/audit/samples.txt" <<'EOF'
0.70
2.10
4.30
7.20
10.20
13.50
17.20
21.20
24.80
28.00
31.20
33.70
EOF

i=0
while read -r t; do
  i=$((i+1))
  abs=$(python3 - "$START" "$t" <<'PY'
import sys
print(float(sys.argv[1])+float(sys.argv[2]))
PY
)
  src="$ROOT/audit/source_$(printf '%02d' $i).jpg"
  ffmpeg -hide_banner -loglevel error -y -ss "$abs" -i "$SRC" -frames:v 1 "$src"
  ffmpeg -hide_banner -loglevel error -y -i "$src" -filter_complex "
    [0:v]split=5[a][b][c][d][e];
    [a]crop=608:1080:0:0,scale=216:384[a1];
    [b]crop=608:1080:328:0,scale=216:384[b1];
    [c]crop=608:1080:656:0,scale=216:384[c1];
    [d]crop=608:1080:984:0,scale=216:384[d1];
    [e]crop=608:1080:1312:0,scale=216:384[e1];
    [a1][b1][c1][d1][e1]hstack=inputs=5[out]
  " -map "[out]" -frames:v 1 "$ROOT/audit/source_$(printf '%02d' $i)_candidates.jpg"
done < "$ROOT/audit/samples.txt"

ffmpeg -hide_banner -loglevel error -y \
  -framerate 1 -pattern_type glob -i "$ROOT/audit/source_??.jpg" \
  -vf "scale=320:180,tile=3x4:padding=2:margin=2" \
  -frames:v 1 "$ROOT/audit/SOURCE_OVERVIEW.jpg"

ffprobe -v error -show_entries stream=width,height,r_frame_rate,pix_fmt -of default=nw=1 "$SRC" > "$ROOT/audit/SOURCE_INFO.txt"
