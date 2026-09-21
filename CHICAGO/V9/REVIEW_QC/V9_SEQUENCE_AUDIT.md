# Chicago V2 — full sequence / composition audit

- Shots: **207**
- Duration: **21:30.72**
- Median shot: **5.00s**
- Minimum shot: **1.36s**
- Shots <2s: **9**; <1.5s: **2**
- Adjacent same-source boundaries: **3**
- Same-source motion/variant flips at adjacent boundaries: **1**
- A→B→A source returns: **3**
- Source returns within 6 shots: **10**

## Confirmed subtitle-safe-area conflicts

V2 explainers draw three cards at source coordinates y=847..968 of 1080. At 540p review this becomes roughly y=424..484.
The visible running subtitle style is bottom-aligned with MarginV=28 and can occupy roughly y=440..512 for two lines.
**Therefore every explainer interval is a deterministic subtitle/graphic collision unless the caption is repositioned.**

Reconstruction/archive provenance labels are also drawn at y≈0.952*h (about 514px in the 540p review), inside the subtitle zone and need collision handling.

## Explainer intervals

### gauge
- 03:09.92–03:23.48 | shot 22 | phase 0 | S030 | static

### transfer
- 04:01.52–04:05.12 | shot 28 | phase 0 | S039 | static
- 04:05.12–04:13.52 | shot 29 | phase 0 | S040 | static
- 04:13.52–04:20.12 | shot 30 | phase 1 | S041 | static
- 04:20.12–04:24.40 | shot 31 | phase 2 | S042 | static
- 04:24.40–04:28.32 | shot 32 | phase 2 | S043 | static
- 04:28.32–04:33.08 | shot 33 | phase 2 | S044 | static

### coal
- 08:10.04–08:14.00 | shot 55 | phase 0 | S076 | static
- 08:14.00–08:22.20 | shot 56 | phase 0 | S077 | pan
- 08:22.20–08:26.56 | shot 57 | phase 1 | S078 | static
- 08:26.56–08:29.92 | shot 58 | phase 1 | S079 | static
- 08:29.92–08:32.12 | shot 59 | phase 2 | V3_COAL_MERGE | static
- 08:32.12–08:40.00 | shot 60 | phase 2 | S082 | push

### basement
- 09:06.12–09:07.88 | shot 65 | phase 0 | S088 | static
- 09:07.88–09:10.96 | shot 66 | phase 0 | S089 | static
- 09:10.96–09:29.28 | shot 67 | phase 1 | S090 | static
- 09:29.28–09:35.52 | shot 68 | phase 2 | S092 | push
- 09:35.52–09:38.72 | shot 69 | phase 2 | S093 | static
- 09:38.72–09:46.40 | shot 70 | phase 2 | S094 | push

### water
- 15:38.00–15:43.24 | shot 144 | phase 0 | S169 | static
- 15:43.24–15:47.40 | shot 145 | phase 0 | S170 | static
- 15:47.40–15:56.48 | shot 146 | phase 1 | S171 | push
- 15:56.48–16:00.88 | shot 147 | phase 1 | S172 | static
- 16:00.88–16:04.40 | shot 148 | phase 2 | S173 | static
- 16:04.40–16:06.60 | shot 149 | phase 2 | S174 | static

### survivor
- 17:56.40–18:06.92 | shot 167 | phase 0 | S193 | static
- 18:06.92–18:13.44 | shot 168 | phase 1 | S194 | static
- 18:13.44–18:15.84 | shot 169 | phase 1 | S195 | static
- 18:15.84–18:21.32 | shot 170 | phase 2 | S196 | static
- 18:21.32–18:27.04 | shot 171 | phase 2 | S197 | static

## Short shots (<2s)

- 00:11.80–00:13.40 (1.60s) | S002 | full | static
- 07:48.20–07:49.56 (1.36s) | S071 | full | static
- 07:49.56–07:51.44 (1.88s) | S072 | full | static
- 09:06.12–09:07.88 (1.76s) | S088 | detail | static
- 11:42.48–11:44.40 (1.92s) | S118 | detail | static
- 14:40.04–14:41.60 (1.56s) | S158 | full | static
- 20:13.28–20:15.20 (1.92s) | V3_LATE_15 | v3 | static
- 20:15.20–20:16.64 (1.44s) | V3_LATE_16 | v3 | static
- 20:16.64–20:18.40 (1.76s) | V3_LATE_17 | v3 | static

## Adjacent same-source motion/variant flips

- 02:33.68–02:47.44 | S024 full/static → S024 source_detail/static

## A→B→A returns

- 02:37.68–03:02.32 | S024 → S026 → S028
- 02:47.44–03:09.92 | S026 → S028 → S029
- 07:51.44–08:22.20 | S073 → S076 → S077
