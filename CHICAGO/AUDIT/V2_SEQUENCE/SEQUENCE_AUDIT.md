# Chicago V2 — full sequence / composition audit

- Shots: **217**
- Duration: **21:30.72**
- Median shot: **4.84s**
- Minimum shot: **1.04s**
- Shots <2s: **13**; <1.5s: **4**
- Adjacent same-source boundaries: **4**
- Same-source motion/variant flips at adjacent boundaries: **2**
- A→B→A source returns: **5**
- Source returns within 6 shots: **23**

## Confirmed subtitle-safe-area conflicts

V2 explainers draw three cards at source coordinates y=847..968 of 1080. At 540p review this becomes roughly y=424..484.
The visible running subtitle style is bottom-aligned with MarginV=28 and can occupy roughly y=440..512 for two lines.
**Therefore every explainer interval is a deterministic subtitle/graphic collision unless the caption is repositioned.**

Reconstruction/archive provenance labels are also drawn at y≈0.952*h (about 514px in the 540p review), inside the subtitle zone and need collision handling.

## Explainer intervals

### gauge
- 03:09.92–03:23.48 | shot 29 | phase 0 | S030 | static

### transfer
- 04:01.52–04:05.12 | shot 35 | phase 0 | S039 | static
- 04:05.12–04:13.52 | shot 36 | phase 0 | S040 | static
- 04:13.52–04:20.12 | shot 37 | phase 1 | S041 | static
- 04:20.12–04:24.40 | shot 38 | phase 2 | S042 | static
- 04:24.40–04:28.32 | shot 39 | phase 2 | S043 | static
- 04:28.32–04:33.08 | shot 40 | phase 2 | S044 | static

### coal
- 08:10.04–08:14.00 | shot 63 | phase 0 | S076 | static
- 08:14.00–08:22.20 | shot 64 | phase 0 | S077 | pan
- 08:22.20–08:26.56 | shot 65 | phase 1 | S078 | static
- 08:26.56–08:29.92 | shot 66 | phase 1 | S079 | static
- 08:29.92–08:30.96 | shot 67 | phase 2 | S080 | static
- 08:30.96–08:32.12 | shot 68 | phase 2 | S081 | static
- 08:32.12–08:40.00 | shot 69 | phase 2 | S082 | push

### basement
- 09:06.12–09:07.88 | shot 74 | phase 0 | S088 | static
- 09:07.88–09:10.96 | shot 75 | phase 0 | S089 | static
- 09:10.96–09:29.28 | shot 76 | phase 1 | S090 | static
- 09:29.28–09:35.52 | shot 77 | phase 2 | S092 | push
- 09:35.52–09:38.72 | shot 78 | phase 2 | S093 | static
- 09:38.72–09:46.40 | shot 79 | phase 2 | S094 | push

### water
- 15:38.00–15:43.24 | shot 153 | phase 0 | S169 | static
- 15:43.24–15:47.40 | shot 154 | phase 0 | S170 | static
- 15:47.40–15:56.48 | shot 155 | phase 1 | S171 | push
- 15:56.48–16:00.88 | shot 156 | phase 1 | S172 | static
- 16:00.88–16:04.40 | shot 157 | phase 2 | S173 | static
- 16:04.40–16:06.60 | shot 158 | phase 2 | S174 | static

### survivor
- 17:56.40–18:06.92 | shot 176 | phase 0 | S193 | static
- 18:06.92–18:13.44 | shot 177 | phase 1 | S194 | static
- 18:13.44–18:15.84 | shot 178 | phase 1 | S195 | static
- 18:15.84–18:21.32 | shot 179 | phase 2 | S196 | static
- 18:21.32–18:27.04 | shot 180 | phase 2 | S197 | static

## Short shots (<2s)

- 00:11.80–00:13.40 (1.60s) | S002 | full | static
- 05:49.20–05:50.88 (1.68s) | S055 | full | static
- 07:48.20–07:49.56 (1.36s) | S071 | full | static
- 07:49.56–07:51.44 (1.88s) | S072 | full | static
- 08:29.92–08:30.96 (1.04s) | S080 | full | static
- 08:30.96–08:32.12 (1.16s) | S081 | detail | static
- 09:06.12–09:07.88 (1.76s) | S088 | detail | static
- 11:42.48–11:44.40 (1.92s) | S118 | detail | static
- 14:40.04–14:41.60 (1.56s) | S158 | full | static
- 19:21.84–19:23.64 (1.80s) | S208 | full | static
- 20:13.28–20:15.20 (1.92s) | S220 | full | static
- 20:15.20–20:16.64 (1.44s) | S221 | full | static
- 20:16.64–20:18.40 (1.76s) | S222 | full | static

## Adjacent same-source motion/variant flips

- 01:14.64–01:34.32 | S013 full/static → S013 source_detail/static
- 02:33.68–02:47.44 | S024 full/static → S024 source_detail/static

## A→B→A returns

- 02:37.68–03:02.32 | S024 → S026 → S028
- 02:47.44–03:09.92 | S026 → S028 → S029
- 05:49.20–06:17.36 | S055 → S056 → S057
- 05:59.48–06:59.24 | S057 → S061 → S062
- 07:51.44–08:22.20 | S073 → S076 → S077
