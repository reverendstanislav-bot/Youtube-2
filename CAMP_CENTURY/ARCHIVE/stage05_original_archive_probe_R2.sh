#!/usr/bin/env bash
# HIA VIDEO007 CAMP CENTURY — R2 AUTHENTIC GOVERNMENT FILM DOWNLOAD + LOCAL QC
# Usage: bash CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh /path/to/output_dir
# No paid services. No synthetic video. Does NOT automatically clear footage legal provenance.
set -Eeuo pipefail
OUT="${1:-CAMP_CENTURY_ARCHIVE_QC}"
mkdir -p "$OUT"/{masters,reports,contact_sheets,clips,rights_receipts}
command -v python3 >/dev/null || { echo "ERROR: python3 not found"; exit 2; }
command -v curl >/dev/null || { echo "ERROR: curl not found"; exit 2; }
command -v ffprobe >/dev/null || { echo "ERROR: ffprobe not found"; exit 2; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg not found"; exit 2; }

# Archive.org item contains an authoritative list of ORIGINAL and DERIVATIVE filenames.
# Never guess a direct file name or pick a 512kb/s preview for the source-of-truth.
archive_metadata_to_url() {
  local item="$1" dest="$2"
  python3 - "$item" "$dest" <<'PY'
import json,sys,urllib.request,urllib.parse,pathlib
item,out=sys.argv[1:]
url='https://archive.org/metadata/'+urllib.parse.quote(item)
try:
    req=urllib.request.Request(url,headers={'User-Agent':'HIA-documentary-source-QC/1.0'})
    with urllib.request.urlopen(req,timeout=40) as resp:data=json.load(resp)
except Exception as ex:
    print("ARCHIVE_METADATA_HOLD",item,repr(ex),file=sys.stderr);sys.exit(3)
files=data.get('files',[])
candidates=[]
for f in files:
    name=f.get('name','')
    fmt=(f.get('format') or '').lower()
    ext=pathlib.Path(name).suffix.lower()
    if ext not in ('.mpeg','.mpg','.mp4','.mov'):continue
    if 'thumb' in name.lower() or 'sample' in name.lower():continue
    is_original=(f.get('source')=='original')
    high=('mpeg2' in fmt or 'mpeg-2' in fmt or ext in ('.mpeg','.mpg'))
    size=int(f.get('size') or '0')
    if size<100_000_000:continue
    candidates.append(((is_original, high, size),name,fmt,size))
if not candidates:
    print("NO_LARGE_ORIGINAL_FILM",item,"Inspect",url,file=sys.stderr)
    sys.exit(4)
candidates.sort(reverse=True)
best=candidates[0]
print(item,"SELECTED",best[1],"format",best[2],"bytes",best[3],file=sys.stderr)
download='https://archive.org/download/'+urllib.parse.quote(item)+'/'+urllib.parse.quote(best[1],safe='/')
pathlib.Path(out).write_text(download+'\n',encoding='utf-8')
PY
}

download_archive_original() {
  local item="$1" short="$2"
  local url_file="$OUT/reports/${short}_download_url.txt"
  if ! archive_metadata_to_url "$item" "$url_file"; then
    echo "DOWNLOAD_HOLD: $item: could not verify Archive file list" >&2
    return 0
  fi
  local url; url="$(head -1 "$url_file")"
  local ext="${url%%\?*}"; ext="${ext##*.}"
  local dest="$OUT/masters/${short}.${ext}"
  echo "$url" > "$OUT/rights_receipts/${short}_origin_url.txt"
  if ! curl --fail --location --retry 2 --connect-timeout 20 --continue-at - --output "$dest" "$url"; then
    echo "DOWNLOAD_HOLD: failed to obtain $item" >&2
    return 0
  fi
  [ -s "$dest" ] || { echo "DOWNLOAD_HOLD: zero-byte $dest" >&2; return 0; }
  echo "ACQUIRED_NOT_RIGHTS_LOCKED $dest"
}

download_archive_original 'gov.dod.dimoc.26064' 'CAMP_COLOR_IA'
download_archive_original 'gov.archives.arc.2569752' 'CAMP_BW_NARA'

echo "MANUAL AUTHENTIC PRIMARY SOURCES (NOT AUTO-DOWNLOADED):"
echo "  USACE COLOR ORIGINAL 32:26, item 35.mp4: https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34"
echo "  DVIDS PM2A 23:07 PD film, exact file specs UNVERIFIED, login may be required: https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv"
echo "  Save as CAMP_USACE_COLOR_ORIGINAL.mp4 / CAMP_PM2A_RELOCATION_DVIDS.mp4 in $OUT/masters if available."
echo "  Save screenshot of source rights statements to $OUT/rights_receipts."

find "$OUT/masters" -type f \( -iname '*.mp4' -o -iname '*.mpeg' -o -iname '*.mpg' -o -iname '*.mov' \) -size +100M -print0 |
while IFS= read -r -d '' src; do
  base="$(basename "$src")"
  echo "QC FILE: $src"
  sha256sum "$src" >> "$OUT/reports/source_sha256.txt"
  stat -c '%n,%s bytes' "$src" >> "$OUT/reports/source_sizes.txt"
  ffprobe -v error -show_format -show_streams -of json "$src" > "$OUT/reports/${base}.ffprobe.json" || { echo "FFPROBE_HOLD $src" >&2; continue; }
  if ! ffmpeg -nostdin -v error -i "$src" -map 0:v:0 -an -f null - </dev/null; then
    echo "DECODE_HOLD $src" >&2; continue
  fi
  # Review stills manually: each sheet is 5x5 thumbnails at ~20sec sampling.
  ffmpeg -nostdin -v error -i "$src" -map 0:v:0 \
    -vf 'fps=1/20,scale=320:-2,tile=5x5' -vsync vfr -y \
    "$OUT/contact_sheets/${base}_%03d.jpg" || echo "CONTACT_SHEET_HOLD $src" >&2
done
echo "NO AUTOMATIC FOOTAGE PASS. REQUIRED: inspect physical scenes and source rights; record exact IN/OUT and unique seconds per V4 beat."
echo "Do NOT add COLOR+BW total runtimes as unique footage. DVIDS removal film requires independent manual scene review."
