# HIA VIDEO007 — CAMP CENTURY | CODEX R2 ORIGINAL ARCHIVE DOWNLOAD + RIGHTS QC RUNBOOK

**Approved work:** Original public-domain / appropriately licensed HISTORICAL SOURCES search and archival video clip extraction for 2931-word LOCKED V4 narration.
**Not approved:** Paid voices, generative image/video, paid stock, contacting rights owners, importing other documentaries, exporting alleged finished master.

## 0. Mandatory reference files
1. `SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md` — exact Git blob identities and VO lock.
2. `SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv` — 32 semantic narrative beats (no audio exists).
3. `ARCHIVE/STAGE05_VERIFIED_PUBLIC_ARCHIVE_LINKS_AND_RIGHTS_R2.md` — authoritative research list and exclusions.
4. `ARCHIVE/STAGE05_ASSET_ORIGIN_RIGHTS_SOURCE_REGISTER_R2.csv` — 21 original source / still / exclusion entries with source URLs, license classes, relevant chapters.
5. `ARCHIVE/stage05_original_archive_probe_R2.sh` — safe source download and local media probe automation.
6. Earlier Stage05 R1 archival NO-GO report is superseded for source discovery by R2, because it MISSED **the separate PM-2A relocation film**. Its warning that no bytes/unique seconds were physically reviewed by the assistant remains accurate.

## 1. Exact FIRST downloads on machine with internet access
### A. Construction color, official U.S. Army film — original first
Open:
https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34
Agency catalog states **1963**, 32:26, 439061611-byte MP4, federal public domain. Document filename listed **35.mp4**. Use the official page's MP4/media download UI or a *tested URL resolved by that UI*. Do NOT fabricate a ContentDM getfile URL on spec. Put acquired movie in `masters/CAMP_USACE_COLOR_ORIGINAL.mp4`.
If no accessible original MP4, use Internet Archive original DoD copy:
https://archive.org/details/gov.dod.dimoc.26064
Select MPEG2 at actual Download Options — DO NOT pull a low-quality streaming preview as montage source if MPEG2 exists.

### B. New independent film: reactor removal, 1964 (published metadata 1965)
https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv
https://www.dvidshub.net/download/popup/556111
Select the best offered original-quality copy **after logging in if required**; **size, codec, and resolution remain unverified** until actual DVIDS download and ffprobe. Page identifies **23:07**, DVIDS video ID **556111**, asset **DOD_104928871**, federal-produced **PUBLIC DOMAIN**. It may require login/registration through DVIDS. Do not claim manual download was completed before reviewing the actual file. Save to `masters/CAMP_PM2A_RELOCATION_DVIDS.mp4`. Relevant to **CH07**: physical disassembly, packing/crating and transport. **This is NOT a duplicate of the color *construction* movie**; still scan for incidental stock shot overlaps when physically available.
Record official PD page: https://www.dvidshub.net/about/copyright

### C. Black-and-white edition, NARA *Big Picture 111-TV-514*
https://archive.org/details/gov.archives.arc.2569752
Use authentic MPEG2 from Download Options; same historical job and substantial construction action overlap with color. **NOT another 30 min unique**. Use only physically confirmed new angles/subjects missing from color film. Stage05 script `stage05_original_archive_probe_R2.sh` fetches this IA original if internet access works.

### D. Run automation for IA metadata-resolved original sources
```bash
bash CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh /mnt/archive/CAMP_CENTURY
```
It checks live IA metadata to find an actual large film filename, `curl` obtains it if accessible, records download URL, SHA-256, size, ffprobe output, decodes video and exports contact sheets. Failures stay **DOWNLOAD_HOLD**; don't claim acquired if only links exist. Local disk will need several GB free.

## 2. ORIGINAL stills/docs — highly specific to film, no stock wallpaper
From U.S. Army CRREL technical report:
https://usace.contentdm.oclc.org/digital/collection/p266001coll1/id/4529
Commons archived PDF:
https://commons.wikimedia.org/wiki/File:Camp_Century-_Evolution_of_concept_and_history_of_design,_construction,_and_performance_-_USACE-p266001coll1-4529.pdf
Extract only real figures: Peter miller, trench cross-section, wide reactor trench, built original street map, local deformation Fig28/29, snow saw trimming Fig33. Original federal report **PD**. Editors can apply clean restrained *editor-made* highlights of actual figure lines.

Deep PM-2A photo-rich engineering report (1961, 169p):
https://commons.wikimedia.org/wiki/File:Construction_of_the_Army_nuclear_power_plant_PM-2A_at_Camp_Century,_Greenland-_Final_report_-_USACE-p266001coll1-3968.pdf
Original site:
https://usace.contentdm.oclc.org/digital/collection/p266001coll1/id/3968
**PD Army-created**, choose real reactor assembly photos and plans.

1969 revisited Camp Century pictorial (published 1970; 59 pages):
https://commons.wikimedia.org/wiki/File:Camp_Century_revisited-_A_pictorial_view_-_June_1969_-_USACE-p266001coll1-3499.pdf
Original:
https://usace.contentdm.oclc.org/digital/collection/p266001coll1/id/3499
**PD Army-created**. Use selectively for actual later site conditions. Do not present stills as motion.

Exact PD individual Commons assets:
- Original trench construction: https://commons.wikimedia.org/wiki/File:Camp_Century_trench_construction.png
- Tunnel deformation real original: https://commons.wikimedia.org/wiki/File:Camp_Century_trench_deformation.png
- Camp physical layout black-white: https://commons.wikimedia.org/wiki/File:Camp_Century_layout_plan.png
- Actual Army PM-2A installation: https://commons.wikimedia.org/wiki/File:PM2Anuclearpowerplant.jpg
- Actual Camp Century thermal drilling: https://commons.wikimedia.org/wiki/File:Camp_Century_Drill-CRREL.jpg

NASA original (not behind an image search crop):
https://science.nasa.gov/earth/earth-observatory/new-view-of-the-city-under-the-ice-153616/
Download the original two JPEGs under `Downloads` on page: `April 2024` radar figure (**990.74 KB**) and `1966` National Archives Camp Century borehole photo (**1.85 MB**, NARA photo ID **404791598**). NASA's first-party imagery generally reusable with NASA credit. Cite image exactly as creator's page says, not `NASA discovered City for first time` (earlier surveys existed).

## 3. Rights ledger — what can actually enter the editor timeline
For each binary or extracted report still, record:
`source_id, file_path, original_item_url, catalog_title, originating_agency_or_copyright_owner, original_creation_year, film_period, exact_locator, law_or_license, rights_source_url, download_date, sha256, width, height, fps, interlace, actual_in, actual_out, actual_duration, scene_subject, geographical_location, script_chapter, semantic_beat, duplicate_group, manual_qc, inclusion_decision, credit_line`.

**Public domain is determined by ACTUAL ORIGINAL CREATOR/WORK**, not by whether it appears on a free site. 
- USACE original army film, federal reports/photos → PD-USGov as labeled on original catalog/item.
- DVIDS original army film → explicit PD mark on item; do not imply DoD endorsement.
- NASA-generated radar → NASA use guidelines, credit NASA and check page notices.
- Internet Archive CC0 label on derivative doesn't change fact that an embedded third-party insert can remain protected; verify original film.
- **DO NOT INCLUDE** National Geographic, Getty, HISTORY/A&E, Washington Post licensed media, commercial restoration audio/effects, Omeka third-party authors, or modern University of Vermont `press only` still/videos for an ad-supported standalone documentary.
- Photo group https://www.campcentury.org/press/photos expressly says **not for commercial use without permission**; separate government-origin credited 1960s originals are better sourced from USACE/Commons.
- Press-video page https://www.campcentury.org/press/videos only grants `press coverage with credit`: **not assumed safe for monetized HIA longform**.
- Any Commons CC BY-SA derivative may require attribution and share-alike; avoid when an authentic federal PD original is available.

## 4. Real footage-first shot detection plan (not invented source timecodes)
Prioritize physically present authentic actions:
- CH01: main actual tunnel vehicle movement and authentic measured deformation chart. Real time-lapse of actual closure likely absent — document, no fake kinetic shrinking B-roll.
- CH02: tracked Polecat tractor convoy, heavy swing constructing/loading/traversing ice, reactor/large cargo convoy.
- CH03: Peter snow miller cutting trench, arches going in, prefab modules, roofs, hatches, plumbing, roads under snow.
- CH04: PM-2A component transport, installation, real plant footage from original color master; original construction report photos.
- CH05: original documented *proposed* Iceworm defense plan, authentic modest rail experiment only if verified; no fake real missiles, no unrelated launch reels.
- CH06: 1965 original measured cross-section diagram Fig28/29 and snow-trimming figure; moving machines only if actual film shows correct work.
- CH07: **NEW 23:07 real PM-2A relocation movie** for genuine summer 1964 dismantling / crate / transport; 1969 revisit report for later building conditions. Not generic shut-down/empty hangar stock.
- CH08: actual 1966 core photo + NASA 2024 radar image; distinct original 1960s drilling image. University commercial images DO NOT enter without proper license.

## 5. Physical duplicate and quality QC, then STOP/GO
Do NOT rely on film runtime or pseudo-random scene counts. Create `ACTUAL_SHOT_LIST.csv` from real playback:
`source_sha256,source_name,scene_id,source_in_timecode,source_out_timecode,real_action,exact_site,script_ch,beat_id,motion_seconds,duplicate_of,license_receipt,visual_qc,editor_note`.
- Use 5–20-second self-contained shot excerpts **when the observed action permits**. No wasteful splitting into hundreds of short files.
- B/W and color showing identical action/camera angle is a DUPLICATE even if grade or scan differs; one source represents it. PM-2A 1964 removal footage is a separate event, but still evaluate at shot level.
- Take native frame resolution; old 4:3 sources can be framed/cropped responsibly in HIA 1920×1080/25fps without stretching people or unreadably enlarging a 480p source. Preserve good film grain.
- Each beat marked `ORIGINAL_VIDEO_PASS`, `LEGAL_DOCUMENT_STILL`, `EDITOR_FACTUAL_GFX`, or `GAP`. Real industrial motion dominates the movie when possible.
- Compute `unique_motion_sec` and overlap by actual clip. **Film lengths 32:26+23:07 do not imply 55:33 approved usable action.** NARA BW doesn't add time automatically.
- If material is still inadequate, produce real missing-action query/source plan. Do not fill with irrelevant generic snow stock/photos or video generation.

## Exact return for producer
Return in GitHub:
1. `ARCHIVE/STAGE05_DOWNLOADED_SOURCES_SHA256.csv` real acquired files only (no invented byte counts).
2. `ARCHIVE/STAGE05_ACTUAL_SHOT_LIST_V1.csv` actual in/out; scene matching locked V4 speech, unique seconds, rights status.
3. `ARCHIVE/STAGE05_DUPLICATE_EXCLUSIONS_V1.csv` color vs BW and others physically checked.
4. `ARCHIVE/STAGE05_COVERAGE_REPORT_V1.md`: per-chapter **usable moving minutes**, original film %, picture quality/rights, remaining gaps, verdict PASS/HOLD.
5. `ARCHIVE/RIGHTS_RECEIPTS/` small URL/license evidence notes/screenshots only; no unauthorized proprietary uploads.
6. Only meaningful verified 5–20sec scene files retained in editing storage `extracted_clips/`, not bloating Git with giant MPEGs.
7. Script Lock V4 remains untouched. No TTS/VO credit spending, no generative video, no dialogue subtitles, no claims of COMPLETE before verified QC.

## EXTRA FILM BANK — R2A expanded original Army studies
The consolidated `STAGE05_VERIFIED_PUBLIC_ARCHIVE_LINKS_AND_RIGHTS_R2.md` now contains **F06–F08**:
- **F06 `The Top of the World` TV-543 (1962)**: https://campcentury.omeka.net/items/show/151; specialist identifies genuine additional *Camp Century entrance and construction* footage from Greenland section starting ~16:20. Seek federal original by NARA ID **111-TV-543**; not unrelated Rollagon/DEW line scenes. Compare original shots to F01 color and F03 BW.
- **F07 `U.S. Army and the Boy Scouts` TV-520**, NARA **111-TV-520 / ARC2569758**: https://campcentury.omeka.net/items/show/144; genuine Camp Century visit but significant Camp Tuto/polar science footage. Screen location scene by scene.
- **F08 `Engineering for Tomorrow` TV-781 (1970)**: https://campcentury.omeka.net/items/show/161, Camp Century Greenland section **12:23–17:19** but **mostly REUSED original scenes**. Dedup heavily, only clearly distinct shots.
Add all three to local `ORIGINAL_FILM_CANDIDATES`, separate `SOURCE_QC` acquisition status `NOT_DOWNLOADED`. Never treat those catalog clips' runtime as unique V4 timeline. Search NARA identifiers, choose authoritative federal-origin copies, and preserve original movie sound provenance. R2 list now **8 candidate film-source records (including a duplicate mirror, reused compilations and Camp Tuto context) plus government photos and clear red exclusions**.
