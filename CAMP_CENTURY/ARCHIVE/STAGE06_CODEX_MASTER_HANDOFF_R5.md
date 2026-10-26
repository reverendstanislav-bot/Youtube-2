# HIA VIDEO007 CAMP CENTURY — CODEX STAGE06 MASTER HANDOFF R5
**Date:** 2026-10-26
**Ready to hand off:** YES, acquisition/QC toolkit and exact source tasks.
**Ready-to-montage real clips present:** **NO** — *no original MPEG/MP4 was downloaded in the assistant runtime*, no original IN/OUT times physically verified. Do not announce a video-bank PASS.

## ONLY TASK / OWNER LOCK
Produce a real documentary cut bank from actual historical *moving* footage of Camp Century, not photos, CGI, generic Greenland, other sites or military videos. User requires:
1. Download authentic U.S. Army / NARA / DoD originals.
2. Physically screen actual frames, segment complete 5–20-second meaningful shots with exact genuine source IN and OUT.
3. Verify the shot depicts Camp Century itself or a transport convoy proven to carry that base's equipment (separate locations).
4. Check each original's federal-public-domain provenance and each included fragment for third-party components.
5. Deduplicate identical footage across color, B/W and later compilations.
6. Save full-length original master separately in editing storage, export only correct clips; record proven unique moving seconds **for each of eight V4 chapters**.
7. GitHub: manifests, hashes, reviewed scene list, confirmed duplicates, rights receipts, per-chapter coverage report, honest PASS/HOLD. Do not commit massive MPEG/MP4 to regular Git.

**NO paid TTS / no video generation / no paid archive orders or licenses / no speech captions/subtitles.** Audio spending requires separate producer authorization after footage-bank QC.

## IMMUTABLE SCRIPT REFERENCE — DO NOT MODIFY
- GitHub repo `reverendstanislav-bot/Youtube-2`, default branch main.
- Script lock `CAMP_CENTURY/SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md`.
- Narration `CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_VOICE_TEXT_V4_EN.txt` (2931 spoken words, 8 chapters).
- EXACT BEATS `CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv` (32 rows); native Git blob SHA `aea8122f66765b049effd61d6bc0eb4780250407`.
- Full locked markdown V4 in `CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_FULL_NARRATION_V4_EN.md`.
- Stage 05 visual rule `CAMP_CENTURY/ARCHIVE/STAGE05_ACTUAL_SITE_MOVING_FOOTAGE_ONLY_R4.md`, R4 film-source `STAGE05_ACTUAL_CAMP_CENTURY_FILM_ONLY_R4.csv`.
- R3 older 53-entry research list is **NOT an approved montage bank**.

## SOURCE INGEST — PRIORITY
**F01** 1963 USACE Army color original, official catalog says 32:26, `35.mp4`, https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 . Download actual agency file via its UI; **no guessed CDN path**. USACE marks original U.S.-government film public domain. Its content includes **Camp Tuto/Thule supply**, which must be separately marked from direct base footage.

**F01B** DoD PIN26064 Army color mirror of EXACT SAME FILM, alternate orig-format MPEG2:
https://archive.org/details/gov.dod.dimoc.26064
https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064.mpeg
Do not add film runtime to F01.

**F02** NARA 111-TV-514 B&W Army film (substantial color overlap):
https://archive.org/details/gov.archives.arc.2569752
https://archive.org/download/gov.archives.arc.2569752/gov.archives.arc.2569752.mpeg
Must review individual DIFFERENT shots; only those count as new motion.

**F03** SEPARATE genuine U.S. Army PM-2A reactor removal film, summer 1964, DVIDS item 556111, catalog 23:07:
https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv
Explicit DVIDS PUBLIC DOMAIN mark; **may require legitimate Register/Login to Download**. Original file size, resolution, codec **not verified**. Do not invent DVIDS CDN or bypass login. This is essential to CH07, different subject from F01.

**F04** U.S. Army `The Top of the World`, NARA 111-TV-543, actual Camp Century entrance but mixed non-Century Arctic tests: https://campcentury.omeka.net/items/show/151 . Acquire only actual original Army source (NARA catalog) and site-confirmed shots.

**F05** U.S. Army `U.S. Army and the Boy Scouts`, NARA 111-TV-520, authentic base claimed among other locations (catalog not independently fully accessible): https://campcentury.omeka.net/items/show/144 . HOLD individual site frames.

**F06** U.S. Army `Engineering for Tomorrow`, NARA 111-TV-781, Greenland 12:23–17:19 in expert catalog; mostly earlier footage reused: https://campcentury.omeka.net/items/show/161 . Use only unique original Century actions after checking.

Excluded: unrelated Site I/II, Camp Tuto, Thule, Operation Blue Jay/Lead Dog as supposed *Camp Century footage*. Exclude CBS Walter Cronkite commercial TV, licensed Periscope 16mm commercial scan and CriticalPast edits absent explicit original/master rights. No invented operational Project Iceworm system (it was never built). No maps/stills/archival photos counted as real moving seconds.

## ONE COMPLETE TOOLKIT — EXACT ATTACHMENT
**Attached to the ChatGPT conversation:** `HIA_CAMP_CENTURY_STAGE06_CODEX_HANDOFF_R5.zip`.
Transfer that ZIP to Codex and unpack `HIA_CAMP_CENTURY_STAGE06_CODEX/` on the networked workstation. It includes:
- `README_START_HERE.md`: exact platform steps;
- `CODEX_PROMPT_COPY_PASTE.txt`: ready-to-use brief;
- `SCRIPT_V4_LOCK.md`: blob hash identities;
- `tools/download_ia_originals.py`: reads **LIVE** IA item metadata, chooses original large file over stream previews, downloads atomically/resumes and SHA256 logs;
- `tools/stage06_real_footage.py`: tested auditer, **full decode gate**, contact sheets, manual rights receipts, exact timecode cut, duplicate suggestions, separate reviewed `finalize` stage, chapter count;
- `tools/run_workflow.sh`: first phase Linux/macOS runner; download access failures remain HOLD;
- `manifests/SOURCE_ORIGINAL_ACQUISITION.csv` (7 sources), `V4_BEAT_TO_REAL_FILM_COVERAGE.csv` (all 32 locked beat IDs, 2931 words), `CHAPTER_COVERAGE_NO_GO_BASELINE.csv` (all eight chapters NOT_MEASURED), blank `approved_ranges.csv` and `final_review.csv`;
- `rights/RIGHTS_RECEIPT_FORM.md`, `records/NO_FILM_BINARY_PRESENT.md`, `requirements.txt`.
The tool was tested on a TEMPORARY SYNTHETIC VIDEO ONLY and that file was removed; it is NOT proof that any archive content was downloaded, rights-cleared or edited.

## CODEX IMMEDIATE COMMANDS
```bash
# After unpacking attached ZIP:
cd HIA_CAMP_CENTURY_STAGE06_CODEX
python3 -m pip install -r requirements.txt
bash tools/run_workflow.sh /path/to/CAMP_CENTURY_ARCHIVE_QC
# Obtain real official F01 and F03 through legitimate sources/UI if they were not acquired automatically.
python3 tools/stage06_real_footage.py audit --root /path/to/CAMP_CENTURY_ARCHIVE_QC --full-decode
python3 tools/stage06_real_footage.py sheets --root /path/to/CAMP_CENTURY_ARCHIVE_QC --sample-interval 20
# Actually view all originals and sign the exact IN/OUT and rights receipts;
# copy manifests/approved_ranges.csv to archive root and fill with only real approved shots.
python3 tools/stage06_real_footage.py cut --root /path/to/CAMP_CENTURY_ARCHIVE_QC
python3 tools/stage06_real_footage.py duplicates --root /path/to/CAMP_CENTURY_ARCHIVE_QC
# Independently verify duplication and fill final_review.csv, then run:
python3 tools/stage06_real_footage.py finalize --root /path/to/CAMP_CENTURY_ARCHIVE_QC
python3 tools/stage06_real_footage.py report --root /path/to/CAMP_CENTURY_ARCHIVE_QC
```
Full original decode and a non-empty source-specific local rights receipt are required before this tool will export an approved scene; it refuses an invented source timecode, an invalid locked beat ID prefix, clips outside 5–20 seconds, different-site candidates or missing original SHA.

## REQUIRED GITHUB DELIVERY (actual files only, no fake numbers)
- `CAMP_CENTURY/ARCHIVE/STAGE06_ACQUIRED_ORIGINALS_SHA256.csv`: original file path/size/native resolution/fps/codec/ratio/hash/source rights URL;
- `CAMP_CENTURY/ARCHIVE/STAGE06_VERIFIED_REAL_5_20_SECOND_CLIPS.csv`: each actual watched excerpt's true IN/OUT, beat, real location, license receipt and SHA;
- `CAMP_CENTURY/ARCHIVE/STAGE06_CONFIRMED_DUPLICATE_EXCLUSIONS.csv`: manually confirmed identical footage between sources;
- `CAMP_CENTURY/ARCHIVE/STAGE06_REAL_CAMP_SECONDS_PER_CHAPTER.md`: 8 chapters actual `DIRECT_CAMP_CENTURY_SEC` and `OWN_PROJECT_SUPPLY_CHAIN_SEC` separately, % of true moving coverage vs narration, gaps and HOLD/PASS;
- `CAMP_CENTURY/ARCHIVE/STAGE06_EDITORIAL_LICENSE_RECEIPTS.csv`: exact source URLs and evaluated federal/third-party insert rights decisions.
- All original MPEG/MP4 and output clip binaries MUST exist in durable editing/archive storage and be addressable by manifest; do not claim physical media file in GitHub just because metadata exists.

## PASS CRITERION
**PASS** only after originals physically downloaded and fully decoded, real footage reviewed shot-by-shot, actual site and rights confirmed, 5–20s clips exported, overlap removed and V4 beats covered sufficiently without slideshow/repeat padding.
If F01/F03/Archive inaccessible, report precise blocking link/error, honest zero verified clips, **HOLD**. No TTS paid credits or purchases.

**Current factual status:** original film acquisition blocked in assistant runtime by Archive DNS/redirect; no genuine physical footage yet. Production tool is prepared and tested on synthetic disposable material only.
