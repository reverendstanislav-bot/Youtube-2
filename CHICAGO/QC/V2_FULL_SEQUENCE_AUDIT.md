# Chicago V2 — Full Sequence / Composition QC

## Status

**FAIL FOR PUBLICATION IN CURRENT VISIBLE-CAPTION FORM**

The underlying V2 MP4 remains technically valid, but the current visible-caption review exposed composition and continuity problems that require targeted picture/layout cleanup before a publication master is built.

This report supersedes any earlier generic "visual PASS" claim for V2.

## User-confirmed examples

The supplied review screenshots show the same systemic issue found by the sequence audit:

- **TRANSFER explainer** — `04:01.52–04:33.08`
  - three bottom process cards occupy the same vertical safe area as the running captions;
  - narration captions cover process-card copy such as `TRANSFER / LOWERING`;
  - the frame becomes a stack of competing text systems.

- **BASEMENT explainer** — `09:06.12–09:46.40`
  - the same three-card construction is repeated;
  - the lower graphic strip dominates the frame;
  - caption placement cannot remain at the normal bottom position here.

This is not a single-frame defect. The same layout logic is used by multiple explainer sequences.

## Objective sequence audit

- Runtime: **21:30.72**
- Shots: **217**
- Median shot: **4.84 s**
- Minimum shot: **1.04 s**
- Shots under 2 seconds: **13**
- Shots under 1.5 seconds: **4**
- Static-shot runtime: **864.64 s / 67.0%**
- Moving-shot runtime: **426.08 s / 33.0%**
- A→B→A source returns: **5**
- Source returns within 6 shots: **23**
- Adjacent same-source motion/variant flips: **2**
- Freeze detector events ≥3 seconds: **72** (many are intentional still-photo holds, but the density is editorially relevant)

## 1. Subtitle / lower-third collision — confirmed systemic defect

The V2 explainer graphic is drawn at source coordinates approximately `y=847..968` in a 1080 frame.

In the 540p review this occupies approximately `y=424..484`.

The running captions are bottom-aligned and can occupy approximately `y=440..512` for two lines.

Therefore the collision is deterministic.

Total explainer-card runtime affected: **174.60 seconds (~2:55)**.

Breakdown:

- gauge: **03:09.92–03:23.48** — 13.56 s
- transfer: **04:01.52–04:33.08** — 31.56 s
- coal: **08:10.04–08:40.00** — 29.96 s
- basement: **09:06.12–09:46.40** — 40.28 s
- water: **15:38.00–16:06.60** — 28.60 s
- survivor: **17:56.40–18:27.04** — 30.64 s

### Additional collision risk

V2 also draws `RECONSTRUCTION / AI reconstruction / HISTORICAL SOURCE` labels near the bottom edge (`y≈0.952*h`). The running-caption style uses the same lower safe area. Caption placement must therefore become scene-aware, not globally fixed.

## 2. Long static / map-heavy section — major pacing issue

The most obvious concentration is approximately **05:49–07:17**.

Key sequence:

- 05:49.20–05:50.88 — Chicago tunnel map
- 05:50.88–05:59.48 — reconstruction
- 05:59.48–06:17.36 — **same Chicago tunnel map, 17.88 s static**
- 06:17.36–06:34.08 — archive train image, slow pan
- 06:34.08–06:59.24 — **same Chicago tunnel map, 25.16 s static**
- 06:59.24–07:17.28 — another map, **18.04 s static**

This creates a long map → image → same map → another map rhythm. It is structurally coherent on paper but visually too repetitive for the channel standard.

Longest detected near-static intervals include:
- 06:37.48–06:59.24 — **21.76 s**
- 06:59.24–07:17.28 — **18.04 s**
- 09:12.96–09:29.28 — **16.32 s**
- 06:02.88–06:17.36 — **14.48 s**
- 03:09.92–03:23.48 — **13.56 s**

Do not solve this by adding arbitrary push/pull to every still. The fix should change visual evidence / framing / information progression rather than recreating the old zoom-in / zoom-out problem.

## 3. Repeated-source bouncing

The sequence still reuses several sources heavily:

- `A02_IllinoisTunnelMap1910.png` — 8 shots
- `A04_TunnelCoalDelivery.jpg` — 8 shots
- `A01_IllinoisTunnelIntersectionCloser.jpg` — 6 shots
- `A16_LOC_Illinois_Central_freight_1942.jpg` — 6 shots
- several State Street archive photos — 4+ shots each

There are **23 source returns within six shots**.

Important clusters:

### 01:10–02:34
Multiple State Street archive photos rotate and return repeatedly:
`A14 → A13 → A15 → A14 → A13 → A15 → A14 → A13 ...`

One source is also held as:
- 01:14.64–01:18.64 full
- 01:18.64–01:34.32 source-detail

This is exactly the kind of "same photo / crop / return / switch back" rhythm that previously felt like photo jitter rather than documentary progression.

### 02:33–03:10
Telephone ad and construction imagery return in A→B→A patterns.

### 05:49–06:59
The same 1910 map repeatedly leaves and returns.

### 07:51–08:22
Coal-delivery material returns around the transition into the coal explainer.

## 4. Very short cuts inside explanatory sequences

Potential visual flicker / unnecessary cadence breaks:

- 08:29.92–08:30.96 — **1.04 s**
- 08:30.96–08:32.12 — **1.16 s**
- 09:06.12–09:07.88 — 1.76 s
- 20:13.28–20:15.20 — 1.92 s
- 20:15.20–20:16.64 — **1.44 s**
- 20:16.64–20:18.40 — 1.76 s

The 08:29.92–08:32.12 pair is especially suspicious because it happens inside the coal process graphic. A process explanation should read as one controlled information progression, not two near-flash cuts.

## 5. Explainer design repetition

The same three-card grammar is reused for:

- transfer
- coal
- basement
- water
- survivor

The system is visually consistent but overused. Across nearly three minutes it starts to look like a template rather than episode-specific documentary direction.

Recommended treatment:
- retain the information;
- reduce card height / density;
- do not show all three full cards throughout every phase;
- reveal only the current step or use a compact horizontal progress rail;
- reserve a clear caption-safe zone.

## 6. Late-film slideshow density

Approximately **19:05–20:18** is dominated by static reconstruction images with several short successive cuts.

Examples:
- S205 appears, leaves, then returns as S209;
- multiple 1.4–4 s static reconstruction shots cluster near 19:18–20:18;
- only a small number of shots use meaningful motion.

This section should be checked for narrative reason per image. Repetition should be consolidated rather than animated indiscriminately.

## What is NOT broken

- V2 duration / frame rate / decode: PASS.
- Audio: preserve exactly; V1/V2 audio is bit-identical.
- Correct V2 SRT timing: PASS.
- Old broken `03_TIMELINE/subtitles_en.srt`: permanently rejected.
- Current problem is not subtitle timing; it is **caption composition + picture sequence/pacing**.

## Required repair plan

1. **Do not touch audio.**
2. Keep V2 as the base source.
3. Replace global bottom caption placement with scene-aware caption zones:
   - normal scenes: current lower caption zone;
   - explainer scenes: captions move above the graphic;
   - end screen: no narration captions over CTA elements unless required.
4. Redesign the five three-card explainers plus gauge for a caption-safe composition.
5. Fix the map-heavy **05:49–07:17** block by reducing repeated map returns and using meaningful detail/evidence changes.
6. Consolidate State Street photo bouncing in **01:10–02:34**.
7. Remove / merge the 1.04 s + 1.16 s coal cuts around **08:30**.
8. Review the static reconstruction run **19:05–20:18** and merge redundant images.
9. Build a new low-resolution review only after all fixes are applied.
10. Run another full sequence audit + user review before 1920×1080 publication master.

## Audit evidence

- `CHICAGO/AUDIT/V2_SEQUENCE/SEQUENCE_AUDIT.md`
- `CHICAGO/AUDIT/V2_SEQUENCE/SEQUENCE_AUDIT.json`
- `CHICAGO/AUDIT/V2_SEQUENCE/GLOBAL_SHEET_01.jpg ... GLOBAL_SHEET_09.jpg`
- `CHICAGO/AUDIT/V2_SEQUENCE/SPECIAL_SHEET_01.jpg ... SPECIAL_SHEET_04.jpg`
- `CHICAGO/AUDIT/V2_SEQUENCE/FREEZEDETECT_LOG.txt`
- `CHICAGO/AUDIT/V2_SEQUENCE/SCENE_CHANGE_LOG.txt`
- user-provided review screenshots
