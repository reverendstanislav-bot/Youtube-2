# CODEX TASK — HIA VIDEO007 CAMP CENTURY — STAGE05 ARCHIVE ACQUISITION / UNIQUE VIDEO QC R2

Repository: `reverendstanislav-bot/Youtube-2`, branch `main`. Follow actual repo ownership and commit rules. **Use Stage05 R2 sources, not R1 as the complete list.**

## Read before work
1. `CAMP_CENTURY/SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md`
2. `CAMP_CENTURY/SCRIPT/STAGE04_CAMP_CENTURY_BEATS_V4.csv`
3. `CAMP_CENTURY/ARCHIVE/STAGE05_VERIFIED_PUBLIC_ARCHIVE_LINKS_AND_RIGHTS_R2.md`
4. `CAMP_CENTURY/ARCHIVE/STAGE05_ASSET_ORIGIN_RIGHTS_SOURCE_REGISTER_R2.csv`
5. `CAMP_CENTURY/ARCHIVE/STAGE05_CODEX_DOWNLOAD_AND_RIGHTS_QC_RUNBOOK_R2.md`
6. `CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh`

## Mission
Download and visually verify **ORIGINAL U.S. GOVERNMENT** period media, **extract meaningful authentic 5–20s action clips** with exact source timecodes, distinguish duplicates between original color and B/W camp films, identify original creator/license and record metadata. Produce a proof-based, per-chapter visual coverage report against **LOCKED V4 narration**, without automatically spending on voice.

**Critical NEW independent film:**
https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv
https://www.dvidshub.net/download/popup/556111
It is a 23:07 distinct public-domain Army film, best listed copy **720×480 ~842 MB**; physically depicts 1964 PM-2A reactor dismantling, packing and transport, potentially excellent for CH07. Earlier Stage05 R1 file incorrectly listed shutdown/removal motion as unavailable; **R2 research identified original removal film**. Don't mark actual unique minutes until downloaded and inspected.

Original color construction film:
https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34
DoD mirror (same film): https://archive.org/details/gov.dod.dimoc.26064
B/W partially overlapping Army film: https://archive.org/details/gov.archives.arc.2569752
Use original-format MPEG2 from IA rather than 512kb previews. If a source requires authentication or blocks, log `DOWNLOAD_HOLD` with evidence; do not invent direct URLs.

Photo/report PD originals and excluded media are documented exactly in R2 archive pack. No generic snow stock, no commercial Getty/NatGeo, no University press-only photos/videos, no video generation, no AI historic reconstructions.

## Execute
- Run `bash CAMP_CENTURY/ARCHIVE/stage05_original_archive_probe_R2.sh /path/to/archive_storage` if network, ffmpeg and curl available.
- Download F01 official if possible and F04 DVIDS manually; validate sha256, native dimensions, actual duration, decoding and full playback.
- Contact sheets for each original film, choose action-bearing 5–20s shots. Do not cut tiny 2s fragments or inflate with duplicate frames.
- Preserve original-film and photo sources and archive license receipts; check details, physically view each included frame/shot.
- Map every excerpt to `STAGE04_CAMP_CENTURY_BEATS_V4.csv`, noting `source_in`, `source_out`, `actual_motion_secs`, `chapter`, `type`, `license`, `duplicate_of`.
- Colour and B/W same camera action = duplication, even if tint/resolution altered; **don't add 32+30 minutes**.
- R2 source list has **two physically separate long films with gross catalog runtimes 32:26 and 23:07**. Those 55:33 minutes are not proof of sufficient distinct footage. Include NARA B/W only for scene-by-scene new content.
- Pictures: original government 1965 engineering report, PM-2A 1961 report, 1969 59-page photo report, government Commons stills and original NASA radar. Motion must dominate wherever possible; visuals must match exact words and dates.

## MUST deliver in GitHub
1. `CAMP_CENTURY/ARCHIVE/STAGE05_DOWNLOADED_SOURCES_SHA256.csv`
2. `CAMP_CENTURY/ARCHIVE/STAGE05_ACTUAL_SHOT_LIST_V1.csv`
3. `CAMP_CENTURY/ARCHIVE/STAGE05_DUPLICATE_EXCLUSIONS_V1.csv`
4. `CAMP_CENTURY/ARCHIVE/STAGE05_CHAPTER_BY_CHAPTER_COVERAGE_V1.md`
5. rights metadata linked to source items, physical file list and scene eligibility state.
6. Produce actual excerpt binaries in archive/editing storage, not massive raw movie commits to regular Git.

At the end report **physically verified unique useful moving seconds**, per-chapter coverage, rights decisions, native video quality and exact shortfall, plus PASS/HOLD. If no downloads are accessible, log a reproducible blocker and DO NOT claim completion.

**DO NOT edit script V4 or Script Lock, DO NOT generate paid voice, DO NOT run paid Higgsfield, DO NOT send rights outreach or orders, NO captions/SRT/VTT**, consistent with HIA owner lock.
