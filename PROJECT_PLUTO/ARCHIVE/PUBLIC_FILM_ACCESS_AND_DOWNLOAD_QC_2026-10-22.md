# Project Pluto — PUBLiC-ONLY film sources: acquisition attempt 2026-10-22

**Owner lock:** use only films already accessible to everyone online, with no requests, no archive contact, no NARA orders, no paid rights clearance, no subscription resources. All preceding unsent NARA/DOE letter drafts were NOT SENT and the three new drafts from the immediately preceding work were REMOVED FROM MAIN.

## Actual public source research
- U.S. DOE's official public [Atomic Energy Commission film index](https://www.energy.gov/lm/atomic-energy-commission-films-available-online) explicitly links digitally available NARA media and publicly watchable official YouTube mirrors.
- High-relevance context-only: **Project Rover (1963)**, NARA 88229; **ML-1 Mobile Nuclear Power Plant (1963)**, NARA 88191; **EBR-I Core Disassembly After Melt Down (1958)**, NARA 88380; **EBR-II Fuel Cycle Development**, NARA 88381.
- **Additional public** Argonne AEC **The EBR-II Fuel Facility (1964)**, NARA 88139, published via Argonne video https://www.youtube.com/watch?v=xt3qSZCQAIs, indexed at https://whatisnuclear.com/old-videos.html . This is not the DOE EBR-II film 88381 and not Tory material.
- All are **DIFFERENT REACTOR / ROCKET PROGRAMS** and can only be context footage when genuinely required. None is filmed Tory II-C operation. Do not simply add their whole runtime to the montage.
- Existing seven previously downloaded historical context original-source movies remain separately on actual [GitHub Releases](../FINAL_VERIFIED_MEDIA_MANIFEST_20261021.md), but are not counted as newly acquired.

## Actual technical retrieval
- GitHub Action [run 39838874465](https://github.com/reverendstanislav-bot/Youtube-2/actions/runs/39838874465) failed at first due to Python Path composition bug, no media produced.
- Fixed workflow, rerun **[39839095490](https://github.com/reverendstanislav-bot/Youtube-2/actions/runs/39839095490)** completed technical collection. Four public video retrievals were attempted from the DOE's embed links using `yt-dlp` and FFmpeg/ffprobe. **0/4 MP4 downloaded**; all four links returned YouTube's `Sign in to confirm you're not a bot` blocker on GitHub public runner. No anti-bot circumvention or private cookies used.
- Full JSON per-video acquisition evidence is preserved as Actions artifact `HIA_Pluto_Public_Government_Films_CONTEXT_ONLY_Rights_HOLD`, size 6,792 bytes (metadata only) from run 39839095490. No media MP4 inside. Do not claim success simply because overall GitHub workflow shows green.
- No other public film binary acquired or cut in this run. R5 stays 34 clips / 15:33 total, of which 13:44 high-action 1963 film.

## Legal interpretation
- DOE [Web Policies](https://www.energy.gov/web-policies) say federal agency-made DOE material is generally public domain in the U.S., with attribution requested, but web pages can incorporate privately owned film/graphics.
- NARA [Special Media copyright notice](https://www.archives.gov/research/motion-pictures/permissions) says federal-employee produced items generally US PD, but archives hold privately-owned embedded content, contracts, donors, performances. NARA cannot certify every film or absolve Content ID.
- Thus accessibility to watch != US commercial use cleared; distinguish `PUBLIC_URL_PASS` from `RIGHTS_HOLD`. Contractor-produced and remastered materials can have extra rights.

**Status:** Updated public URL source list PASS; 0 new physical MP4; expanded editor footage count **UNCHANGED**, genuine Tory II-A/II-C test film still 0 confirmed, rights HOLD. No requests/letters/orders/paid credits.
