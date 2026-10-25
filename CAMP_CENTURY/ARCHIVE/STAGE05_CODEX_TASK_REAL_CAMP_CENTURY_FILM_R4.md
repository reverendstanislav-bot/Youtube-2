# CODEX — VIDEO007 CAMP CENTURY — HARD REQUIREMENT: ACTUAL HISTORIC MOTION, NOT STOCK / STILLS

**Owner corrected scope:** `Нужны именно фактические кадры` — only real film footage of **Camp Century itself**, supplemented solely by identified transport operations moving *that exact camp's* equipment.
**Script:** V4 8 chapters, 2931 spoken words, source `CAMP_CENTURY/SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md` LOCKED. No script edits and no paid voice.

## READ FIRST (supersedes permissive R3 for video selection)
- `CAMP_CENTURY/ARCHIVE/STAGE05_ACTUAL_SITE_MOVING_FOOTAGE_ONLY_R4.md`
- `CAMP_CENTURY/ARCHIVE/STAGE05_ACTUAL_CAMP_CENTURY_FILM_ONLY_R4.csv`
- `CAMP_CENTURY/ARCHIVE/STAGE05_REAL_MOVING_SHOT_SEARCH_MAP_R4.csv` (28 target real actions, NOT 28 visually confirmed unique clips)
- `CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv`
- `CAMP_CENTURY/ARCHIVE/STAGE05_CODEX_DOWNLOAD_AND_RIGHTS_QC_RUNBOOK_R2.md`
- `CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh` for available Internet Archive source downloads.

## Acquisition order (do real work, not new research list)
1. FIRST obtain U.S. Army ORIGINAL Camp Century 1963 government film https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 ; catalog file `35.mp4`, 32:26, 439061611 bytes. Official page explicitly PUBLIC DOMAIN. If direct official item UI fails, fetch original MPEG2 from SAME film IA https://archive.org/details/gov.dod.dimoc.26064 after checking the official metadata file name. Don't claim alternative mirror adds runtime.
2. SECOND independent original Army 1964 PM2A reactor removal film https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv DVIDS explicitly PUBLIC DOMAIN, 23:07. It may require user-facing registration/login; **do not attempt to bypass authorization**. Exact encoded file size/quality are unknown. If access unavailable, log precise blocker rather than claim asset acquired.
3. THIRD NARA Army black-and-white actual film 111-TV-514 https://archive.org/details/gov.archives.arc.2569752 . Manual compare same views to color before accepting any second; no automatic additional 30-minute film count.
4. FOURTH NARA Army `Top of the World` TV-543 https://campcentury.omeka.net/items/show/151 . Seek NARA 111-TV-543 original; expert archive confirms genuine Camp Century entrance, labs and construction BUT also Rollagon/DEW-line elsewhere; discard all non-Camp Century sections. Obtain original federal copy not Vimeo commercial modifications.
5. THEN only verified original filmed-Camp sequences TV-520 https://campcentury.omeka.net/items/show/144 and TV-781 https://campcentury.omeka.net/items/show/161 ; latter Greenland 12:23–17:19 largely duplicates earlier original films.
6. **DO NOT ACQUIRE FOR EDIT** CBS Cronkite original (copyright, https://campcentury.omeka.net/items/show/147), Periscope Film commercial raw scan (https://stock.periscopefilm.com/xd95155-greenland-camp-century-1959-project-iceworm-meteorological-station-silent/) or CriticalPast repackaged scans. They may identify original government camera footage not yet found; catalog descriptions are research clues, not permission to use their copies.

## Rejected as user's footage
- Generic 1950s Greenland / Arctic military film, Site I, Site II, Camp Tuto, Thule/base construction, Operation Blue Jay, Operation Lead Dog, another nuclear power station or missile tests, even if government PUBLIC DOMAIN. The actual Camp Century *specific cargo* passing through Tuto/Thule may count ONLY as `SAME_PROJECT_SUPPLY_CHAIN` when precisely verified, NEVER as shot at Camp Century.
- Slideshows, report photographs, PDF figures, maps, AI images/videos, simulations and borrowed modern documentary graphics DO NOT count as genuine moving footage. Don't pad film with stills.
- No fake Project Iceworm operational rockets/silos or fabricated tunnel-collapse films.

## Physical QC and actual deliverable
For each original downloaded: source URL + rights receipt, SHA256, bytes, duration, native width/height, frame rate, PAR, field order, audio, full decode QC, 20sec thumbnail sheets. Inspect each sequence at normal playback and with source-accurate original in/out.
For each selected original action: duration 5–20sec if movement supports it, preserve full action, exact source IN/OUT, true historical location (`DIRECT_CAMP_CENTURY` or `SAME_PROJECT_SUPPLY_CHAIN`), V4 chapter/beat, visual fact basis, duplication mark, actual file / parent SHA. Don't count titles/old narration as moving history.
Produce in GitHub:
- `ARCHIVE/STAGE05_R4_ACQUIRED_FILM_SHA256.csv` (real binaries, not placeholders)
- `ARCHIVE/STAGE05_R4_VERIFIED_MOVING_SHOTS.csv` (actually seen and extracted)
- `ARCHIVE/STAGE05_R4_FILM_DUPLICATES_EXCLUDED.csv`
- `ARCHIVE/STAGE05_R4_REAL_SITE_SECONDS_BY_CHAPTER.md` with 2 separate tallies `DIRECT_CAMP_CENTURY_SEC` and `OWN_PROJECT_SUPPLY_CHAIN_SEC`, plus `UNKNOWN/RIGHTS_HOLD`.
Keep original reels, meaningfully extracted 5–20sec movie files and film QC sheets in authorized editing storage, not standard Git blobs.
Declare `MOVING_FILM_PASS` only after honest unique footage verified; else `HOLD` with exact unsatisfied chapter beats. Do not claim 55 minutes available because two reels run 32:26+23:07 in catalogs.
**No TTS or other paid generation without new user approval.**
