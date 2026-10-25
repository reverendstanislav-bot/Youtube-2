# HIA VIDEO007 Camp Century — Public archival film gate V1

**Public sources only.** User has approved topic, not paid licenses, video generation or outside archive requests.

## Source A — authoritative color
Official U.S. Army Corps of Engineers library record:
https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34
- Title: *The Story of Camp Century, the City Under Ice — Research and Development Progress Report No. 6*
- Filmed/credited U.S. Army 1963; 32:26 / 439,061,611 bytes / source format MP4; USACE explicitly says PD federal creation. MP4 file catalog name `35.mp4`.
- Status: official catalog metadata verified; file bytes NOT downloaded or SHA checked in current production environment.
- Must verify original download URL using the site's publicly accessible official interface (do not manufacture ContentDM media API parameters).

## Source B — downloadable period mirror of likely same color film
Internet Archive DoD PIN 26064: https://archive.org/details/gov.dod.dimoc.26064
- MPEG original-associated file: https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064.mpeg
- Preview derivative 512kb MP4: https://archive.org/download/gov.dod.dimoc.26064/gov.dod.dimoc.26064_512kb.mp4
- Both direct filenames were exposed by actual Internet Archive download options, but binary transport success/codec/rights inserts still NOT independently tested.
- Mirror page labels 1964; U.S. Army/Camp Century historian Omeka catalog dates original film 1963. Treat film original date 1963 with conflicting metadata note; do not silently combine the dates.
- Likely DUPLICATE SOURCE A, never increase motion-coverage count by adding whole runtime.

## Source C — different black-and-white Army/NARA edition
Internet Archive original NARA Army The Big Picture 111-TV-514:
https://archive.org/details/gov.archives.arc.2569752
- Direct low-bitrate MP4:
https://archive.org/download/gov.archives.arc.2569752/gov.archives.arc.2569752_512kb.mp4
- Film overlap with Source A explicit per independent catalog:
https://campcentury.omeka.net/items/show/157
- Only add **new visual actions or alternative genuinely clearer shots** after timecode overlap audit.
- The 512kb original derivative is for screening/unique shot selection, not automatically high-quality final editorial use.

## Source D — historical Camp Tuto (DIFFERENT LOCATION)
https://campcentury.omeka.net/items/show/802
- Actual US Army ~1957 tunnel excavation; public-domain label; not Camp Century.
- Context ONLY when narrating related tunnel construction technology and named `CAMP_TUTO_CONTEXT`; otherwise exclude.

## Next verification before sourcing editor clips
1. Acquire at most one color version at highest faithfully available scan quality. Metadata/hashes in `FILM_SOURCE_VERIFY.csv`, ffprobe, decode, source duration and audio tracks, rights origin.
2. Generate contact sheets at broad increments then narrow inspection of interesting actions; exclude reels' intros, studio commentary, repeated shots, maps, talking heads unless essential.
3. Use real actions: tracked convoy / heavy sledge / snow excavation / arch assembly / reactor transport / actual living systems. Preserve real source IN/OUT.
4. Compare B&W to color with scene/hash and visual match; calculate DISTINCT NEW seconds, not two entire film runtimes.
5. Reject other research camps as Camp Century; avoid off-topic generic snow scenes. Do not pad timeline with archival photos.
6. Stage03 full script must exist before final timeline source count/coverage PASS; archive selection can be a validated source of construction scenes, never a made-up full film.
7. No contacts, orders, paid subscriptions or source video generation.

**Physical film source bank in repo: NOT YET. Scene QC: HOLD.**
