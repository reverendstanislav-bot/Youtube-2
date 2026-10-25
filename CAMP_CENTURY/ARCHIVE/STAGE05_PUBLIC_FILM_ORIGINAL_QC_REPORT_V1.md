# HIA VIDEO007 CAMP CENTURY — STAGE05 PUBLIC ORIGINAL FILM FORENSIC QC

**QC date:** 2026-10-25
**Current conclusion:** **SOURCE PROVENANCE / HISTORICAL CATALOGUE = PASS; PHYSICAL MOTION DEDUP + SHOT QC = HOLD**.
This is not an acquired video bank; **0 downloaded original MP4/MPEG bytes in the current running environment**; **0 source timecoded editorial extracts**; **0 verified distinct usable seconds**. Therefore no defensible assertion that a twenty-minute film is already visually covered.

## Tests genuinely carried out
1. Revisited original film's US Army / USACE ContentDM item https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34. Official description retained in Stage01 source records states **32:26 original, 439,061,611 bytes MP4 (catalogue)** and a U.S. federal public-domain copyright description. The interactive item is Javascript-dependent via the web text tool. Its video bytes were NOT physically acquired here.
2. Verified Internet Archive government-film record https://archive.org/details/gov.dod.dimoc.26064. Catalog identifies DoD progress report #6 and direct **MPEG2 and MPEG4 download options**, CC0 label. Its 1964 upload metadata conflicts with independent study's explicit Army 1963 on-film credits; this is likely source-date catalog inconsistency, not two independent films.
3. Verified Archive's NARA recording https://archive.org/details/gov.archives.arc.2569752 — **111-TV-514 / 1961–1962 US Army Big Picture**, with separately listed MPEG2 and 512kb MPEG4 files, CC0 label. This is **not** another guaranteed thirty minutes of new Camp Century activity.
4. Checked the specialist Iceworm/Camp Century research-film item https://campcentury.omeka.net/items/show/157 (US Army original). Historian's film description **explicitly says B/W Army Big Picture and color report #6 are very similar with only some differences**. Film description documents tracked-tractor convoys, heavy swing, actual Peter plow, prefab construction, reactor roof, plumbing, hatch, loading and startup of reactor, temporary snow buildings, crew lodging and tracked vehicles traveling underground. These are **catalogue indications, not source-frame verification**.
5. Attempted Linux container `curl -I` on archive.org and USACE site: network DNS error (cannot resolve external hosts), not source-file 404. Attempted direct-download via tool for the official Archive MPEG4 derivative: unsuccessful. Web's direct video download redirects to Archive hosts which the page browser could not access. **No video was ingested, probed with ffprobe, hash-checked, frame-reviewed or deduplicated.** Do not mark this as a media QC PASS.

## Intended sources (not to be added by raw runtime)
| ID | Reference | Grounded provenance | How to use |
|---|---|---|---|
| F01 | USACE official Army color movie, original 1963, 32:26 | U.S. Army / USACE original catalog, federal public-domain designation | **MAIN PRIMARY**. Prefer actual highest-quality original scan after physical retrieval |
| F02 | IA Department of Defense PIN26064 color report #6 | DoD film catalog, author identified, overlapping SAME WORK as F01 | **FALLBACK QUALITY OR ACCESS**, never additive independent footage |
| F03 | NARA Big Picture 111-TV-514, B/W | Army/NARA original; 1961–1962 edition | **UNIQUE DIFFERENCE ONLY**, not additive 30-minute source |
| F04 | Camp Tuto 1957 technique film on Omeka | Distinct Army installation | Only clearly labeled `CAMP_TUTO_CONTEXT` on technique, never passing it off as Camp Century |

## Documented original-film visual role coverage (NOT viewed clips)
See `STAGE05_ORIGINAL_FILM_SHOT_CANDIDATES_V1.csv`: 28 catalogue-grounded roles and explicit manuscript needs. Highest priority **real moving actions** (not yet verified or timecoded): transport convoy; heavy swing assembly; sleds crossing ice; Peter miller cutting trenches; roof and prefab assembly; escape hatch and plumbing installation; reactor component unloading, sled transport, installation and startup; tracked vehicle in underground corridor.
Non-cinematic catalogue sections include food, bunks, bathrooms, people, dog and haircut footage; they should NOT be padded just to fill twenty minutes.

## Known unsolved chapter visual issues
- CH01 shrinking tunnels: actual **Army1965 Figures28–29** show measured deformation. No period motion of actual tunnel closure verified. Do NOT invent video of ice crushing the buildings.
- CH02 logistics: strong primary original film candidates; unique duration unmeasured.
- CH03 industrial snow excavation and cut-cover: strong film candidates; duration/unspoiled native quality unmeasured.
- CH04 reactor arrival and operation: strong original-film candidates; unique duration unmeasured.
- CH05 Iceworm **only unbuilt proposal**, no film of an actual finished network. Use actual historical proposal documents/clearly PROPOSED diagram, not fabricated missile launch or recycled unrelated weapons stock.
- CH06 progressive closure and annual trimming: 1965 contemporaneous charts, original maintenance photo and contextual real period footage only; actual engineering-motion coverage **NOT CONFIRMED**.
- CH07 shutdown and left-behind waste: No original departure/PM2A dismantling footage authenticated. Use historical reports / correct narrative evidence and only matching authentic visuals.
- CH08 core rediscovery/NASA radar: science records and NASA original figure if licensed; historical Army film alone is insufficient.
**Hence** physical and semantic coverage of 8 chapters remains OPEN.

## NO-GO until actual binaries available
1. Download F01 highest-quality original via official USACE film interface or an accurate agency-origin derivative with traceable filename.
2. Preserve `SOURCE_ORIGIN_URL`, precise size in bytes, transport status, `SHA256`, `ffprobe` duration/fps/resolution/interlace/aspect/audio and playback decode check.
3. Download F03 independently in its highest native available quality; use F02 only if F01 unavailable/better.
4. Produce 20-second sampled contact sheets for human screening and a 5–10-second-per-sample hash-based duplicate suggestion across films. Mark match only after manual spot verification — color/B&W, cropping, old scan jitter complicate automatic detection.
5. For each accepted 5–20-second editor excerpt: exact source timecode, physically viewed subject/actual historical site, exact narration CH/beat, shot duration, release suitability, verified rights and native quality; only render genuinely meaningful action and preserve authenticity.
6. Sum actual `UNIQUE_REAL_ACTION_SECONDS` for approved clips after dedup; never count title frames/talking heads/unrelated films/doubled movements.
7. Compare coverage to locked 2931-word V4, specifically CH05–CH08 evidence. If scenes insufficient, expand genuine authorized original film research — NOT paid AI/video generation, anonymous winter stock, or loop padding.
8. Only then mark visual coverage PASS and obtain separate permission for paid TTS.

## Rights limitation
Original government-created films are identified as PD/CC0 in their official/archival catalogs; embedded third-party film/music/edited versions need separate attention. NASA publication is not original 1960s film. Others' edited YouTube documentaries are not source substitutes. YouTube Content ID is an enforcement process, not a guarantee of copyright status. `ARCHIVE/PUBLIC_FILM_ACQUISITION_GATE_V1.md` retains detailed originating URLs.

**STAGE05 SCRIPT LOCK: PASS** (see `SCRIPT/STAGE05_SCRIPT_LOCK_V4_2026-10-25.md`).
**ARCHIVE PHYSICAL QC: NO-GO/HOLD**; **DO NOT SPEND ON VOICE**.
