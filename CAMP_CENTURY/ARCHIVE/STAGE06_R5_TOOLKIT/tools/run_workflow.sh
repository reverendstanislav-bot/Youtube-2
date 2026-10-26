#!/usr/bin/env bash
set -Eeuo pipefail
ROOT=${1:-./CAMP_CENTURY_ARCHIVE_QC}
HERE=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
command -v ffmpeg >/dev/null || { echo 'Missing ffmpeg (system package)' >&2; exit 2; }
command -v ffprobe >/dev/null || { echo 'Missing ffprobe (system package)' >&2; exit 2; }
python3 "$HERE/stage06_real_footage.py" init --root "$ROOT"
# Network command logs DOWNLOAD_HOLD if archive is inaccessible: do not let it claim footage PASS.
python3 "$HERE/download_ia_originals.py" --root "$ROOT" || echo 'Source acquisition incomplete; see reports/internet_archive_download_receipts.csv'
python3 "$HERE/stage06_real_footage.py" audit --root "$ROOT" --full-decode
python3 "$HERE/stage06_real_footage.py" sheets --root "$ROOT" --sample-interval 20
printf '%s\n' 'STOP FOR HUMAN FILM REVIEW. Fill approved_ranges.csv from actual source playback; rights_receipts/; then manually run cut, duplicates and finalize.'
