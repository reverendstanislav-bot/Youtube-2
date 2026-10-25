# CAMP CENTURY VIDEO007 — Stage05 archive QC instructions for Codex / editing host

**Reason:** Stage05 script locked V4 but remote movie was not download-accessible from the assistant's runtime. Source QC cannot become PASS on catalogue metadata alone. This file gives immediate, non-paid, reproducible screening on a network-enabled editing machine.

## Film download — use ORIGINAL government films, not third-party video re-edits
- Preferred authentic U.S. Army color master: https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 (metadata 32:26 and 439061611 bytes; locate `35.mp4` through official download UI; if download not possible, do NOT invent URL).
- Backup for same original color government film: https://archive.org/details/gov.dod.dimoc.26064 , Original `gov.dod.dimoc.26064.mpeg`, or original site's 512kb MPEG4 derivative FOR SCREENING ONLY.
- Second black-and-white **overlapping** Army film: https://archive.org/details/gov.archives.arc.2569752 , NARA 111-TV-514, original `gov.archives.arc.2569752.mpeg`.
- Source provenance and content checklist: https://campcentury.omeka.net/items/show/157 (explicitly confirms many duplicate scenes between color/BW).

## Commands to run on a network-enabled editor workstation
```bash
mkdir -p CAMP_CENTURY_QC/masters CAMP_CENTURY_QC/reports CAMP_CENTURY_QC/sheets
# Substitute the official USACE master if it is available through the official collection.
curl -fL --retry 3 --continue-at - -o CAMP_CENTURY_QC/masters/CAMP_COLOR_ORIGINAL.mpeg \
  'https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064.mpeg'
curl -fL --retry 3 --continue-at - -o CAMP_CENTURY_QC/masters/CAMP_BW_ORIGINAL.mpeg \
  'https://archive.org/download/gov.archives.arc.2569752/gov.archives.arc.2569752.mpeg'

for file in CAMP_CENTURY_QC/masters/*; do
  [ -s "$file" ] || continue
  name=$(basename "$file")
  sha256sum "$file" >> CAMP_CENTURY_QC/reports/SOURCE_SHA256.txt
  ffprobe -v error -show_format -show_streams -of json "$file" > "CAMP_CENTURY_QC/reports/${name}.json"
  ffmpeg -nostdin -hide_banner -loglevel error -i "$file" \
    -vf "fps=1/20,scale=320:-2,tile=5x5" -frames:v 20 -y \
    "CAMP_CENTURY_QC/sheets/${name}_sheet_%03d.jpg"
done
```
Ensure `ffmpeg` / `ffprobe` actually finish with exit code 0 before a PASS. If `curl` errors due to Archive throttle or DNS, mark **DOWNLOAD_HOLD**, not missing film. Check native resolution, SAR, fps, interlace, sound type, actual runtime and full stream decode; never pretend source is native 1080p.

## Real scene QC: required deliverables
1. Manually review all contact sheets; refine relevant sections by source playback. Locate high-value actual motion matching rows 03-19 of `STAGE05_ORIGINAL_FILM_SHOT_CANDIDATES_V1.csv`.
2. Inspect original film at each chosen IN/OUT to note true action and remove extra titles, dogs, repeated corridor loops, irrelevant lifestyle, overlays, non-site films, or talking heads with no story value.
3. Compare BW with color visually shot-by-shot: same physical convoy/camera scene is DUPLICATE even if color grading, framing, speed, narrator, resolution or timecode differs.
4. Add `SOURCE_SHA256`, `source_in_sec`, `source_out_sec`, `unique_moving_sec`, `native_resolution`, `codec`, `date`, `rights_basis`, and `CH/beat` to source manifest.
5. Only retain clips **5–20 s long when the real action supports that duration**. No uniform microclips; don't artificially stretch.
6. Sum verified unique motion into a report: `REAL_ON_TOPIC_UNIQUE_SECONDS`, `DUPLICATE_SECONDS_EXCLUDED`, `UNKNOWN_SOURCE_SECONDS`, `CHAPTERS_WITHOUT_REAL_FILM`, `COVERAGE_SHORTFALL`.
7. Compare with final Script Lock `SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md`. Documentary must consist principally of relevant original moving industrial film, a little credited original documents, and restrained explanatory GFX. If actual real moving material is inadequate, do not mark film bank PASS, don't release TTS spending gate.
8. Source film local files, exported cuts, metadata and SHA records should be archived on your editor machine/appropriate storage. DO NOT commit multi-gigabyte raw MP4/MPEG blobs into regular Git; commit only manifests, shot ranges, evidence, screenshot contact sheets if legitimately licensed and sufficiently small.

**Do not download/use third-party YouTube creators' edits, music or proprietary restorations; source original Army material.** No Higgsfield or other paid credits.

## Script lock
Only current authoritative VO:
`CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt`
Source identity pinned in `SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md`.
