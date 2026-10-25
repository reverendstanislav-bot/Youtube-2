# HIA VIDEO007 CAMP CENTURY — R2A SHORT SOURCE / COPYRIGHT RECHECK
Reviewed: 2026-10-25, live source pages + GitHub file identities. **Not a physical film/clip QC.**

## Confirmed
- Script Lock V4: GitHub has an immutable blob-identified VO, 8 chapters, 2931 words. No re-authoring or payment in this source recheck.
- F01 official USACE color documentary original: https://usace.contentdm.oclc.org/digital/collection/p16021coll1/id/34 . Real U.S. Army-origin movie, catalog **32:26 / 439061611 bytes**, explicitly **U.S. federal public domain**.
- F02 DoD Internet Archive mirror (https://archive.org/details/gov.dod.dimoc.26064) same film subject as F01, **MPEG2 download option confirmed**, not a unique movie's worth of footage.
- F03 NARA 111-TV-514 B&W https://archive.org/details/gov.archives.arc.2569752 : government creator and **MPEG2 download option confirmed**, major source-shot overlap with original F01.
- F04 original US Army Pictorial Center https://www.dvidshub.net/video/556111/relocation-pm-2a-nuclear-power-plant-mf5-5118-mcmlxv : 23:07, video ID 556111, explicitly **PUBLIC DOMAIN** under DVIDS terms, subject confirmed as **summer 1964 reactor dismantling/crating/transport** by https://campcentury.omeka.net/items/show/145 .
- F06 TV543 expert catalog https://campcentury.omeka.net/items/show/151 confirms genuine additional Camp Century footage alongside other-site Arctic tests (don't label all shots Camp Century). F08 TV781 https://campcentury.omeka.net/items/show/161 confirms Greenland section 12:23–17:19 **mostly reused** earlier Army footage. F07 TV520 catalog https://campcentury.omeka.net/items/show/144 **intermittently times out**, still a candidate, not physically confirmed.
- USACE 1965 engineering technical report, 1961 PM2A engineering report, 1969 visit pictorial report: existing genuine original government PDF pages (Common 1969 PDF confirms **59 pages, 125.64MB, PD US federal**). Government-related Commons photos (trench, layout, reactor, actual drill, deformation diagram) have item-level federal PD labels in Commons. NASA original radar images under NASA media-use guidelines and accurate credit, no endorsement.

## Important corrections applied directly to GitHub R2
1. **Not eight independent Camp Century videos.** 8 entries F01–F08 = 1 color film, 1 duplicate color mirror, B&W with overlap, 1 real separate PM2A removal film, Camp Tuto at DIFFERENT SITE, and three other Army film candidates including later compilation largely recycled. **NO count of unique usable minutes established.**
2. DVIDS official listing confirms **23:07 and public-domain item**; prior claimed download size **842MB** and resolution **720×480** cannot be verified from accessible DVIDS pages and are now labeled **UNVERIFIED**. Download popup is not accessible to the web tool; official item offers `Register/Login to Download`, so Codex may need user-authenticated access. Do not invent direct cloud CDN URLs.
3. Government public-domain labels apply to **original U.S. agency-created work**. DVIDS page https://www.dvidshub.net/about/copyright additionally requires **non-endorsement** and cautions about third-party rights, trademarks/privacy. For documentary editing, identify actual original shots; preserve receipts and source links. **PD does NOT make YouTube Content ID impossible.**
4. Press-only University of Vermont photographs/videos: https://www.campcentury.org/press/photos explicitly says no commercial use without permission, and https://www.campcentury.org/press/videos authorizes press coverage with credit, not unconditional monetized use. Historical magazine/National Geographic/Boys Life media excluded pending independent permission. Do not mistake derivative CC BY-SA colorized layouts for pure federal PD originals.

## File integrity / executable workflow
Repo contains `ARCHIVE/STAGE05_VERIFIED_PUBLIC_ARCHIVE_LINKS_AND_RIGHTS_R2.md`, `ARCHIVE/STAGE05_ASSET_ORIGIN_RIGHTS_SOURCE_REGISTER_R2.csv` (25 records: **8 film leads, 12 report/photo/NASA leads, 5 restricted examples**), `ARCHIVE/stage05_original_archive_probe_R2.sh`, and the exact Codex runbook/task.
The script discovers Internet Archive film filenames from the site's live metadata, then requests originals, calculates local SHA256, ffprobes and produces sampled contact sheets **on a network-enabled machine**. DVIDS/USACE originals require manual page download or verified direct links. This archive script has NOT been shown to successfully download or finish a full decode in an actual networked production environment; treat it as a prepared runbook, not a tested ingest pipeline.

## Manufacturing GO/NO-GO
- **Script textual lock**: PASS.
- **Original film provenance / item rights page verification**: PASS for selected F01/F03/F04 and item-labeled original government images, **individual insert review still OPEN**.
- **Acquired original MP4/MPEG files in workspace**: **0 confirmed**.
- **Original frame-by-frame scene selection and B&W/color de-dup**: **NOT DONE**.
- **Actual source in/out timestamps and useful unique motion seconds**: **UNKNOWN**.
- **Coverage for 18–22 minute V4 narrative**: **NOT PROVEN — HOLD**.
- **Paid TTS/generation**: **NOT AUTHORIZED / ZERO SPEND**.

## One concrete next action
Network-enabled Codex workstation: acquire F01 and F04 first, verify sha/native specs/rights, screen and extract meaningful 5–20-second on-topic unique scenes, then F03 and F06 for genuinely distinct additions; record exact source IN/OUT and per-chapter actual seconds. If footage coverage is weak, report missing beats before paid narration. Avoid generic unrelated visuals.
