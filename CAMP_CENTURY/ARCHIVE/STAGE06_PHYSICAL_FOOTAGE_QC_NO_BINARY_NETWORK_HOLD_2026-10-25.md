# HIA VIDEO007 — STAGE06 ACTUAL CAMP CENTURY FOOTAGE ACQUISITION / QC STATUS — 2026-10-25

**Producer instruction:** Find extra UNIQUE real Camp Century frames in original NARA films; physically extract coherent 5–20s clips with true IN/OUT; source rights/native quality/site proof; exclude duplicates and other Greenland bases; sum actual moving minutes by all eight script chapters.

## What I actually executed this turn
1. Inspected the active model container at `/mnt/data`: it contains Project Pluto materials, **not one Camp Century original MPEG/MP4**. No usable site original was secretly available.
2. Checked direct source online catalog entries with actual NARA/DoD MPEG2 download links. Both content pages are public and specify authentic U.S. Army CC0-tagged movies:
   - `NARA 111-TV-514`: https://archive.org/details/gov.archives.arc.2569752 ; verified exact file URL https://archive.org/download/gov.archives.arc.2569752/gov.archives.arc.2569752.mpeg .
   - `DoD PIN26064`: https://archive.org/details/gov.dod.dimoc.26064 ; verified exact file URL https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064.mpeg .
3. Attempted container `curl -IL` to NARA/IA metadata URL, **FAILED: `curl: (6) Could not resolve host: archive.org`**. Attempted direct original source download via dedicated download tool, **FAILED**. Page-browser on each MPEG2 direct link encountered Archive.org redirects to `dn600304.us.archive.org` and `dn601204.us.archive.org`, also not accessible. This is network/redirect access, NOT evidence the archive originals were removed.
4. Verified DVIDS https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv : 23:07 distinct PM-2A Army movie, **PUBLIC DOMAIN** on official item; `Register/Login to Download` shown. No authenticated binary download performed. Do not invent best available file specs.
5. Verified additional NARA-original films via specialist catalog: `111-TV-543` https://campcentury.omeka.net/items/show/151 (Greenland 16:20 onward, real Camp Century entrance, **mixed** unrelated DEW/Lead Dog); and `111-TV-781` https://campcentury.omeka.net/items/show/161 (Greenland 12:23–17:19, **mostly reused earlier footage**). No binary was physically accessed, so none may be counted as UNIQUE moving seconds.
6. Authored, compiled, and ran an original FFmpeg/FFprobe-based physical media QC pipeline `stage06_real_footage.py` in local toolkit:
   - `init` creates strict blank candidate-approved IN/OUT CSV;
   - `audit` reads actual-source SHA256, fps/native resolution/codec/audio and optional full decode;
   - `sheets` creates source-screening contact sheets every 20s with approximate timestamps (not scene IN/OUT);
   - `cut` **requires editor-confirmed** original location, rights proof, true 5–20s in/out, correct V4 chapter, no duplicate; exports actual H.264 high-quality original-frame clip with SHA256;
   - `duplicates` gives multi-frame grayscale dHash duplicate **suggestions only**, not automatic copyrighted-item or film confirmation;
   - `report` separately sums `DIRECT_CAMP_CENTURY` and `SAME_PROJECT_SUPPLY_CHAIN` real motion seconds by all eight chapters.
   - Ran full tooling on a **temporary synthetic 16-second test video**, including full decode, sheet, 8s sample clip extraction, SHA and coverage. **Deleted the synthetic test** and its clips afterwards. This is a *technical test*, NOT real Camp Century footage.
7. Produced a truthful local archive QC toolkit ZIP for the producer with exact original direct URLs, Python pipeline, starter CSV, README and zero-footage coverage report. The ZIP is an attached downloadable ChatGPT conversation artifact `CAMP_CENTURY_STAGE06_ORIGINAL_FOOTAGE_QC_TOOLKIT.zip`. GitHub metadata here links to source and next Codex workstation operation, NOT an automatically uploaded Zip binary.

## Actual current source bank — numerical facts, not aspiration
| V4 chapter | VO | Original site verified cut seconds | Own Camp Century supply cut seconds | Physical QC |
|---|---|---:|---:|---|
| CH01 City losing space | actual base tunnels | 0 | 0 | DOWNLOAD_HOLD |
| CH02 138-mile convoy | actual site supply lines | 0 | 0 | DOWNLOAD_HOLD |
| CH03 Cut-and-cover | snow miller / roofs | 0 | 0 | DOWNLOAD_HOLD |
| CH04 Nuclear plant | PM-2A delivery/startup | 0 | 0 | DOWNLOAD_HOLD |
| CH05 Iceworm NEVER BUILT | no actual deployed arsenal film can exist | 0 | 0 | NO_DEPLOYMENT_FILM_POSSIBLE |
| CH06 Firn deformation | real Army maintenance | 0 | 0 | DOWNLOAD_HOLD |
| CH07 PM-2A removal | original separate 1964 Army movie | 0 | 0 | DVIDS_LOGIN_OR_BINARY_HOLD |
| CH08 Scientific aftermath | actual ice drilling/radar | 0 | 0 | TRUE_SITE_MOTION_UNKNOWN |

**Verified original site action footage in container: 0 seconds. Verified *own supply chain* action: 0 seconds. UNIQUE USABLE ACTUAL MOVING VIDEO: UNKNOWN** — no binary screened. Catalog gross runtime 32:26 + 23:07 does not represent 55 min unique scenes; color/BW sources have overlapping shots. There are **no actual extracted Camp Century clip MP4 files**, no actual frame-level IN/OUT, no verified duplicate exclusion data.

## Copyright / footage identity
Federal original U.S. Army productions and DVIDS item are identified as public-domain originals; this does NOT pre-clear any third-party musical inserts/rights or eliminate YouTube claims. For every accepted clip Codex must retain original agency license URL, file SHA, actual site/mission, source in/out, manual review; reject Third Party/CBS/Periscope/CriticalPast own added material. Never substitute Pluto files or Camp Tuto/Site II/Thule/Lead Dog as Camp Century.

## Exact networked editor/Codex action needed (not a promise)
1. On a machine that actually reaches `archive.org`, download NARA/DoD original MPEG2 using exact links above, obtain USACE official source if higher quality. DVIDS video requires possible registration.
2. Place real movie binaries under `masters/F01.mp4` / `masters/F01B.mpeg` / `masters/F02.mpeg` / `masters/F03.mp4`. Run toolkit `stage06_real_footage.py` as documented (or repo archive R2 downloader). Fully review frames in original movie.
3. Fill `approved_ranges.csv` with strictly genuine Camp Century or exact project convoy segments of 5–20 seconds; verify every source timecode, location and license before cutting. Finish dedup and per-chapter covered action totals. Publish manifests and report to this GitHub folder, keep raw MP4 outside normal Git.
4. Status stays **HOLD** until physical files and an actual shot list exist. No TTS expense authorized.

**STAGE05 Script V4 LOCK: PASS / no changes.**
**STAGE06 ORIGINALS DOWNLOADED: NO; VIDEO CLIPS: 0; VISUAL COVERAGE: NOT PROVEN — HOLD.**
