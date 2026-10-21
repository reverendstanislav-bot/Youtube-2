# PROJECT PLUTO — VIDEO ARCHIVE EXPANSION V2
Date: 2026-10-21.
Current state: link/source discovery only. NO videos downloaded in this conversation, NO shot-level QC, NO attribution/reuse final lock.

## Counts (non-overlapping inventory rows)
- 31 **playable Commons video-file leads** total: previous 6 contextual + **25 newly indexed**. Direct source pages show an original `WEBM/OGV` file; not asserting local downloads or YouTube clearances. The 25 are in `VIDEO_DOWNLOAD_PRIORITY_V2.csv`.
- 20 **U.S. Air Force film inventory leads** directly associated with Project Pluto, its predecessor propulsion program and SLAM (4 old + **16 new**): original catalogue entries/film numbers only, NO verified publicly downloadable movies. Earlier ARC/NARA IDs for three reels are index-derived; revalidate through archives.
- 5 **parts of copyrighted television documentary**: for RESEARCH ONLY, not cleared for reuse.
- **56 total film/video rows**, but only **31 public video-file leads**. Do not claim there are 56 usable footage sources or that any of them show Project Pluto tests.

## Source research
- [Nuclear aircraft and missile documentary film inventory, original Air Force film IDs](https://www.writing.upenn.edu/~afilreis/50s/govfilms.html) — original SECRET markings are HISTORICAL, do not assert today's classification without archival response.
- [Fourmilab Project Pluto article linking documentary playlist](https://www.fourmilab.ch/documents/pluto/) — embedded five-part television history with archival fragments. Publisher's page says the author's TEXT is public domain; **that does not clear the underlying Discovery TV documentary**. No reuse without permission.
- [NARA catalog](https://catalog.archives.gov/) — request original films by archival/USAF file numbers (especially 38914, 38921, 38922, 38912, 38925, 37491, 37492).
- [Commons NASA 1962 X-15 film](https://commons.wikimedia.org/wiki/File:Research_Project_X-15_-_development_of_the_X-15_rocket_plane_-_1962_NASA_documentary.webm) 720p.
- [Commons 'Power for Peace'](https://commons.wikimedia.org/wiki/File:Power_for_Peace.webm) 1080p, actually Atoms for Peace 1955 exhibition.
- [Commons Pershing 1964 documentary](https://commons.wikimedia.org/wiki/File:The_Pershing_Joins_the_Ranks_1964.webm) actual missile (not Pluto).
- [Commons Fort Belvoir reactor newsreel](https://commons.wikimedia.org/wiki/File:1957-07-04_Fort_Belvoir_Army_Package_Power_Reactor.ogv) real 1957 reactor facility but NOT Tory and NOT Pluto; original 30s.
- [Commons NASA Engines 2025 archival review](https://commons.wikimedia.org/wiki/File:Launching_the_Future_of_Flight-_Engines_%2820250220-AAV3553-NACA-Series-Engines-Glenn-v1%29.webm) includes genuine period ramjet/jet and nuclear aircraft research footage but production is 2025.
- Multiple Commons reels marked "**AI UPSCALED**": prefer original unmodified vintage masters from NARA/NASA/Prelinger; do not use AI-restored imagery as pristine original.

## Production priority and narrative fit
1. **Pluto real evidence first:** use genuinely Pluto-specific stills, diagrams, documents from photo ledger; 20 original Air Force film IDs pursued for direct-footage sourcing. Do not substitute a Minuteman launch.
2. **1950s military problem:** USAF tactical nuclear air strike, Boeing bomber industrial scenes, Tall Man Five Five SAC.
3. **Other strategic systems:** Hound Dog air-launched missile (closest major contrast), Atlas/Minuteman ballistic systems, Nike/Pershing as era comparison where justified.
4. **Research/testing environment:** X-15 high-speed aircraft work, US Army Ordnance and NASA NACA engines. These are SEPARATE programs, identified precisely.
5. **Nuclear science and public era:** Power for Peace, 1957 Fort Belvoir reactor newsreel, About Fallout. Never use these shots as if from Pluto or portray blast footage as Tory operation.
6. **No fake 1964 explosion:** Argus, Redwing, Plumbbob clips are NOT Project Pluto. Do not insert a mushroom cloud at Tory II-C full-power narration.

## Quality
Vintage film is often 4:3 / SD native. 1080p/4K wrapper around an SD restoration does not create original detail. Some large files (100-500+ MB) have only 678×442 pixels; 1080p uploads need editorial layout, not destructive crop.
Rights still need per-file inspection and any 3rd-party inserts/marks excluded; work-of-US-gov Commons PD statements are evidence for review, not blanket clearance for every derivative.
No music/SFX from these documentaries should be retained; HIA music and sound separate authorization/rights.
All films require shot-level timecoded selection and historical provenance before edit.
No captions anywhere in finished HIA video or shorts.

## Next actual acquisition
The **31 Commons items** have a player and a source file page, not a locally downloaded file. For each priority A item use original-file download, validate mime + duration + original hash, then owner-review. Large downloads should go to Release/Action artifacts rather than git tree. Existing acquisition workflow's optional `--download-context-video` currently targets entries with `DOWNLOAD_CANDIDATE` and may be very large; do NOT run entire catalogue in a single job. Use `VIDEO_DOWNLOAD_PRIORITY_V2.csv` to split download batches by file size or story section.

## Direct Pluto archive footage inquiries
NARA search for each original title + USAF film number. Ask the archive for:
1. Confirm holdings and archival identity; current classification/public access.
2. Is a **digitized master** available for download? Send exact media URL or transfer details.
3. What is the reel's original color/sound, running time, frame rate, and resolution.
4. Reproduction price if any, restrictions, attribution and YouTube commercial documentary permission.
5. Is there a separate film covering May 20, 1964 Tory II-C engine run or reactor handling.

Only after retrieved binary plus rights and QC can any film change from `CANDIDATE` to `LOCKED`.
