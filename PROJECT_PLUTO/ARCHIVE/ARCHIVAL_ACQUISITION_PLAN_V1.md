# Project Pluto — ARCHIVAL SOURCE ACQUISITION V1

Updated 2026-10-21. **Discovery and shortlist; NOT a claim of binaries downloaded or media LOCK**.

## Search results and usable editorial differentiation
- Wikimedia Commons [Nevada Test Site Pluto Facility category](https://commons.wikimedia.org/wiki/Category:Nevada_Test_Site_Pluto_Facility): **56 pages**, including approximately **48 HAER documentary photographs/scans** from the Library of Congress and **8 additional category items**. Many are facility interiors taken for HAER **after 1968**, NOT 1961 or 1964 test-day exposures.
- Selected **28 photo/diagram leads** in PHOTO_SHORTLIST_V1.csv: **5 direct engine/period-diagram** core leads, 19 selected HAER view candidates (including alternates), 2 late-era demolition, 1 historical-dating HOLD and 1 modern-context REJECT. This is a curation pool, not 28 independent shots or 28 approved photographs.
- [Library of Congress, HAER NV-32](https://www.loc.gov/item/nv0255/) original Pluto facility (4 views) and [NV-32-A](https://www.loc.gov/item/nv0256/) disassembly building (40 views) plus related individual-site records. NPS employee source images generally US-public-domain; LOC caveat: rephotographed third-party items may require additional review.
- For motion picture: **four direct Pluto film discovery records**, but no verified open/public digital file or original downloaded. THREE NARA ARC pointers are based on a legacy catalog index, pending NARA re-verification. Plus **six directly accessible contextual historical films on Commons**, suitable ONLY with historical context distinction (no claims they show Pluto).
- Engine photo licensed summary: [Tory II-A](https://commons.wikimedia.org/wiki/File:Tory_II-A_nuclear_ramjet_engine.jpg) 1550x1100, [Tory II-C](https://commons.wikimedia.org/wiki/File:Tory_II-C_nuclear_ramjet_engine.jpg) 663x482; latter cannot become native high detail by fake upscaling. [Tory II-C cross section](https://commons.wikimedia.org/wiki/File:Schematic_cross-section_of_Tory_reactor.png) 2866x1575 1962 technical diagram from DOE report. Government-US PD status documented on their file pages.
- Source image titled 'Tory-IIC at Jackass flats' is falsely dated circa 1955; Pluto Tory II-C belongs to later program. Photo can be valid but **HOLD** the date/origin until independently verified.
- NNSA image NSO-1182 depicts later counterterrorism exercise, not historical reactor operation; **REJECT for Pluto direct footage**.
- Other footage of atomic detonations is documentary **context**, not actual Tory exhaust or a Project Pluto-related explosion. It must not be cut to imply the tests involved a detonation.
- Proprietary visualizations/modern YouTube explainers, even if compelling, are NOT license-cleared archival footage.
- Review individual item license/copyright and capture source URL, download timestamp, hash, true pixel dimensions, photographer and original caption before placing in Remotion.

## Top visual beats by story
1. 1964 Tory II-C real archival still (P002/P004), with technical identity accurate.
2. 1961 Tory II-A with technician scale (P001/P003).
3. 1962 actual cross-section (P005), explanatory schematic, not fabricated image.
4. Desert/rail approach (P006/P008).
5. Assembly bay vs control room (P010/P014/P015) — different spatial functions.
6. Cooling, support and hot-cell equipment (P007/P012/P013/P017).
7. Post-program late documentary facility and demolition (P025/P026) with actual era label.
8. Primary-document decision extracts (see RESEARCH/SOURCE_LEDGER.md) with visible provenance.
9. At most a few seconds of accurately labeled Cold War contextual film; use documents for exact 1964 decision.

## Technical source-quality and rights locks
- LOC HAER original is TIFF 5000-wide around 19MB. Retain lossless original; generate an editorial 3000–4000-wide JPEG derivative only after download and inspect contrast.
- On Commons file pages, hit **Original file**. Do not download thumbnails then claim source quality.
- Black-and-white and 4:3 period frames should be composed without routine aggressive crops to 16:9; preserve rail-engine and operator features.
- Once source is downloaded, record SHA256, actual pixels, and verified rights in asset manifest. No automated rights conclusion from category membership.
- Keep separate role labels: `DIRECT_PLUTO`, `POST_PROGRAM`, `CONTEXT_ONLY`, `DOCUMENT`, `CONCEPT`; never promote all to verified archive by class alone.
- Current environment has no working direct external-media binary download; acquisition was **not executed**. No ZIP of original photographs or films exists yet.
- To acquire originals on a connected Codex/VPS runner, use the checked-in `fetch_public_domain_assets.py` script after reviewing the shortlist.

## How to acquire via internet-enabled runner
From the repository root, with `requests` available:

```bash
python PROJECT_PLUTO/ARCHIVE/fetch_public_domain_assets.py --out ./project_pluto_assets
# Add accessible CONTEXT videos only if desired; may be very large:
python PROJECT_PLUTO/ARCHIVE/fetch_public_domain_assets.py --out ./project_pluto_assets --download-context-video
```

Script fetches the Wikimedia Commons authoritative API to resolve current original file URLs, downloads approved shortlist items, logs hashes and dimensions when provided by Commons. It does **not** infer PD for every page or automatically assert owner clearance. It intentionally ignores the HOLD/REJECT entries. Large binaries should live in GitHub Releases/Actions or a storage bucket, **not in Git tree**. Verify response MIME and hashes, then manually record license screen/source decisions and retain licensing provenance.

## Film digitization request to NARA
Use original IDs from FILM_LEDGER_V1.csv; ask whether each surviving reel is digitized, accessible to the public, available as high-resolution file, declassified, and if reuse restrictions apply. Index records alone do not establish actual footage availability. If reels are unavailable, do not use fake Pluto tests.

## Milestone status
Research candidates: collected and recorded. Binary download: **0 confirmed**. Visual QC: **not started**. Rights/permission final lock: **not started**. Film direct-source playable videos: **0 confirmed**. Next stage = actual bulk acquisition + per-asset QC.
