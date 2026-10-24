# Project Pluto VIDEO006 — Editor Bank V2 QC

## Result

The physical source bank is assembled against the locked 18:41.600 Arthur narration. The voice-synced plan contains **193 visual elements** across all **30 semantic beats** and ends exactly at **00:18:41:15 at 25 fps** (1121.600 seconds). There are no timeline gaps.

The plan uses **132 unique selected assets**:

- 34 direct Project Pluto/LASV-N1 motion clips.
- 20 period comparison clips from Atlas, Minuteman and B-52/Hound Dog films.
- 39 historical photographs: 3 Tory hardware photographs and 36 HAER Area 26 survey photographs.
- 26 original engineering-report figures.
- 13 rendered pages from official or period publications.

Another **20 context clips** remain in the physical reserve bank. They were retained for optional use but were not forced into the timeline because their relation to this narration is weaker.

## Technical QC

- Direct motion: 34/34 MP4 files pass `ffmpeg -v error -xerror` full decode; 737.375 seconds total; no detected black intervals of 0.40 seconds or longer.
- Selected context motion: 20/20 MP4 files pass full decode; 270.000 seconds total; no detected black intervals of 0.40 seconds or longer.
- Historical photos: 39/39 source hashes match `PHOTO_MASTER_INDEX.csv`; all source images opened successfully; 39 4K-long-edge JPEG proxies were generated for smoother DaVinci playback while the TIFF/JPEG originals remain preserved.
- Engineering figures: 26/26 PNG files opened successfully and have fresh SHA256 entries.
- Official documents: four downloaded PDFs have recorded SHA256 values; 13 relevant pages were rendered to PNG for editing.
- Package integrity: the 39-photo, 40-scene and primary editor-bank ZIP files pass complete ZIP CRC testing.
- Visual review: aggregate contact sheets were inspected for all 34 direct clips, all 20 selected comparison clips, and all 39 historical photographs. No unrelated modern stock, black frames or obvious duplicate filler was accepted into the locked plan.

## Editorial use rules

The 1963 LASV-N1 film is direct evidence of the Project Pluto development program. Its clips can show models, tunnel work, component fabrication, laboratory rigs, controls, telemetry and engineers. They do not show a 1964 Tory II-C hot run or a flying SLAM.

Atlas, Minuteman and B-52/Hound Dog footage is assigned only to narration that explicitly discusses competing or contemporary systems. Every such row carries `REAL_DIFFERENT_PROGRAM_CONTEXT` and requires the on-screen label `CONTEXT — DIFFERENT U.S. PROGRAM`.

HAER Area 26 photographs document the real facility after 1968. They may illustrate surviving infrastructure and spaces, but they must not be described as test-day photographs.

The plan leaves only three optional generated inserts: reactor-airflow explanation, tested-reactor versus unbuilt-vehicle comparison, and the May 20–July 1 decision timeline. They are explanatory graphics over real source evidence, not invented historical footage.

## Rights status

No blanket rights PASS is asserted. Federal reports and HAER materials retain source-specific citations. The recovered LASV-N1 mirror remains `HOLD_THIRD_PARTY_MIRROR_ITEM_REVIEW_REQUIRED` even though the underlying film is a U.S. government production. The 1964 Air Force Magazine article remains `RIGHTS_HOLD_EDITORIAL_QUOTE_REVIEW`. These holds are preserved in every manifest and timeline row.

## Primary files

- `VOICE_SYNCED_VISUAL_MAP_V2.csv`: edit order, audio timecodes, source IN/OUT, historical context, purpose, rights and script-bit mapping.
- `DIRECT_PLUTO_MOTION_MANIFEST_V2.csv`: fresh hashes and technical QC for 34 direct clips.
- `CONTEXT_MOTION_MANIFEST_V2.csv`: fresh hashes and QC for 20 selected comparison clips.
- `CONTEXT_ALL_40_INVENTORY_V2.csv`: the complete 40-clip reserve inventory.
- `HISTORICAL_PHOTO_MANIFEST_V2.csv`: source and proxy hashes for all 39 photos.
- `ENGINEERING_FIGURE_MANIFEST_V2.csv`: all 26 report figures.
- `OFFICIAL_DOCUMENT_PAGE_MANIFEST_V2.csv`: 13 rendered publication pages.
- `MINIMAL_GENERATION_GAPS_V2.csv`: the three limited graphic needs.

The original rejected R1 package is not treated as an approved edit. Individual recovered binaries were independently hashed, decoded and visually reviewed into this V2 bank.
