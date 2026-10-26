# CODEX JOB — CAMP CENTURY VIDEO007 — STAGE06 PHYSICAL NARA CUT BANK (2026-10-25)

## State of work and non-negotiable facts
Script V4 LOCKED, 2931 words / 8 chapters. REAL footage selection rule R4: `DIRECT_CAMP_CENTURY` / `SAME_PROJECT_SUPPLY_CHAIN` ONLY. No mixed Camp Tuto, Site I/II, Thule, old missile tests, generic Arctic footage, slideshows, AI-video or bought re-edits. User ordered source downloads, full 5-20sec cuts, scene-level rights check, B/W-vs-color duplication and real seconds/chapter.

Our assistant environment has **NO accessible original film bytes**. Original NARA/IA MPEG video downloads were actually attempted and failed due to Archive host DNS/redirect. Consequently zero original footage was screened or extracted, no source clip timestamps can be truthfully provided. Inspect `ARCHIVE/STAGE06_PHYSICAL_FOOTAGE_QC_NO_BINARY_NETWORK_HOLD_2026-10-25.md` and `ARCHIVE/STAGE06_ORIGINAL_MEDIA_PHYSICAL_ATTEMPT_LOG_2026-10-25.csv`.

## Source-first original downloads
1. ORIGINAL color Army construction movie F01 https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 ; official source filename `35.mp4`. Use official UI. Backup DoD ORIGINAL MPEG2 (same footage): `https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064.mpeg`.
2. ORIGINAL NARA 111-TV-514 black-and-white (dup compare against F01) `https://archive.org/download/gov.archives.arc.2569752/gov.archives.arc.2569752.mpeg`.
3. DISTINCT ORIGINAL U.S. Army PM-2A 1964 reactor removal film: https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv (DVIDS public-domain, 23:07). The DVIDS page displays `Register/Login to Download`; respect authentication. Exact MP4 size/resolution NOT independently known.
4. Additional genuine Camp Century film sections in NARA TV-543 `Top of the World` (https://campcentury.omeka.net/items/show/151), TV-520 and TV-781 only if frame-site authenticated and distinct. TV-781 Greenland section 12:23–17:19 is mostly recycled Army footage. No third party commercial scan downloads.

## Run command on a network-enabled workstation
Existing downloader `bash CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh /mnt/archive/CAMP_CENTURY` obtains NARA/DoD original movies if archive network accessible. Physically saved film must be inspected and full-decoded.

Also provided **ChatGPT conversation download ZIP**: `CAMP_CENTURY_STAGE06_ORIGINAL_FOOTAGE_QC_TOOLKIT.zip`. It contains an actual Python 3 + FFmpeg/FFprobe/OpenCV/Pillow script tested on a temporary synthetic clip *only* (deleted after test), **not Camp Century footage**. Download this ZIP from the preceding message attachment and provide to Codex / workstation, unzip, then follow `README.md`. The tool commands:
```bash
python stage06_real_footage.py init --root /mnt/archive/CAMP_CENTURY
# place F01.mp4 (official), F01B.mpeg (same work alternate), F02.mpeg (NARA B/W), F03.mp4 (DVIDS) under masters/
python stage06_real_footage.py audit --root /mnt/archive/CAMP_CENTURY --full-decode
python stage06_real_footage.py sheets --root /mnt/archive/CAMP_CENTURY --sample-interval 20
# Actually watch reels & sheets; sign exact original 5–20s scene ranges in approved_ranges.csv, with site, source, chapter/beat, rights_receipt, verified_by.
python stage06_real_footage.py cut --root /mnt/archive/CAMP_CENTURY
python stage06_real_footage.py duplicates --root /mnt/archive/CAMP_CENTURY
python stage06_real_footage.py report --root /mnt/archive/CAMP_CENTURY
```
The extraction tool uses CRF17 H.264 per short source excerpt and calculates SHA-256; it does not synthesize, stretch, upscale or replace historical source video. Computer hashes are duplicate **suggestions**; a human must verify overlap before counting as unique. A clip needs real-source manual sign-off (not an invented timecode) before the extractor allows it.

## Return EXACT deliverables, no placeholders passed as PASS
- `ARCHIVE/STAGE06_ACQUIRED_ORIGINALS_SHA256.csv`: real native file sizes, duration, video specs, original URL, original creator and rights receipt, actual SHA256.
- `ARCHIVE/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv`: clip export path in editing archive, parent original SHA, real video IN/OUT, 5–20sec physically viewed action, correct site, exact V4 chapter/beat, licensing receipt, no dup; reported runtime.
- `ARCHIVE/STAGE06_CONFIRMED_DUPLICATE_EXCLUSIONS.csv`: identical physical action across B/W, color, compilation; original timecodes on both.
- `ARCHIVE/STAGE06_REAL_CAMP_SECONDS_PER_CHAPTER.md`: 8 chapters, own Camp Century moving seconds, real project convoy seconds separately, unfilled time, no claims based on catalogue runtime.
- Actual 5–20sec MP4 files and source originals in editing storage (not large blobs in ordinary Git).
- GO/NO-GO: PASS only after genuinely viewed, rights-backed and deduplicated moving material. If source download blocked record HOLD with URL and error. No paid TTS without owner's explicit new approval.

**Do not revise V4 Script Lock or spend Higgsfield/voice credits.**
