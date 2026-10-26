#!/usr/bin/env bash
# Codex Camp Century Stage06 R5; run from unpacked HIA_CAMP_CENTURY_STAGE06_CODEX toolkit.
# Actual original media and rights receipts are prerequisites to any scene PASS.
set -Eeuo pipefail
ROOT="${1:-$PWD/CAMP_CENTURY_ARCHIVE_QC}"
HERE=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ ! -f "$HERE/tools/stage06_real_footage.py" || ! -f "$HERE/tools/download_ia_originals.py" ]]; then
  echo "HANDOFF_ZIP_REQUIRED: download the conversation attachment HIA_CAMP_CENTURY_STAGE06_CODEX_HANDOFF_R5.zip, unpack it and run inside the folder containing tools/." >&2
  echo "The Github R2 baseline archive downloader is also available at CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh." >&2
  exit 3
fi
command -v ffmpeg >/dev/null || { echo "ffmpeg not installed" >&2;exit 2; }
command -v ffprobe >/dev/null || { echo "ffprobe not installed" >&2;exit 2; }
mkdir -p "$ROOT"
python3 "$HERE/tools/stage06_real_footage.py" init --root "$ROOT"
python3 "$HERE/tools/download_ia_originals.py" --root "$ROOT" || echo "DOWNLOAD_HOLD: original MPEG acquisition incomplete, inspect reports receipt."
python3 "$HERE/tools/stage06_real_footage.py" audit --root "$ROOT" --full-decode
python3 "$HERE/tools/stage06_real_footage.py" sheets --root "$ROOT" --sample-interval 20
echo 'NEXT MANUAL ACTION: Screen EACH original real Camp Century reel, fill rights_receipts/*.txt and approved_ranges.csv; only then cut, duplicates and finalize.'
echo 'Never mark archive as PASS until verified unique seconds by all eight V4 chapters are recorded.'
