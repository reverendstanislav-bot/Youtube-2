# Chicago V3 — targeted visual/sequence QC

## Result

**READY FOR USER REVIEW. NOT A PUBLICATION MASTER YET.**

V3 was rebuilt from clean V2 work-assets rather than patched over the rejected V2 visible-caption review.

## Technical

- workflow run: `35544915218` — SUCCESS
- review: 960x540 / 25 fps / 21:30.720
- full decode: PASS
- review SHA-256:
  `4a88e004a416775ee98eaa385cf1067d41b55df4d1d2cc5ec4fc1c66cac21f07`
- AAC SHA-256:
  `a1e84ecb33a2060075b5681a086bf59b166396e16564b8e705a5b201dc4928ed`
- audio remains bit-identical to V1/V2 source AAC
- captions: 338 V2 cues / 98.665% word-level token mapping
- one running subtitle layer only
- white base + orange active word
- end-screen captions switch to top-safe placement from 21:10

## Sequence improvement vs V2

| Metric | V2 | V3 |
|---|---:|---:|
| shots | 217 | 207 |
| shots <1.5s | 4 | 2 |
| A→B→A source returns | 5 | 3 |
| source returns within 6 shots | 23 | 10 |

## Targeted fixes confirmed in build plan

- 01:10–02:34 State Street cluster rebuilt as one-way archival progression rather than repeated A/B/A returns.
- 05:49–07:17 map block rebuilt as overview → real detail → archival train evidence → different overview crop → later map.
- 08:29.92–08:32.12 coal flash pair merged into one 2.20-second shot.
- old large bottom explainer cards removed from gauge / transfer / coal / basement / water / survivor.
- explainers now use a compact upper-left process rail, leaving lower subtitle-safe area clear.
- provenance labels moved from the lower edge to the upper-right.
- late 19:05–20:18 sequence received semantic cleanup: the literal S205 return is replaced with a distinct detail, while short cuts matching the narration rhythm ("Some remained useful / altered / filled") are preserved.

## Short-clip scene analysis

Separate short-video analyses were run for the repaired areas to avoid relying only on a 21-minute global analysis.

- Transfer: 8 coherent narrative scenes; surface freight → transfer → underground railroad → building connection.
- Map block: 9 scenes; network overview → detail → train evidence → later map progression.
- Coal: 7 scenes; delivery → connection → consumption → ash removal → general freight.
- Basement: 10 scenes; building connection / last-hundred-feet logic remains coherent.
- Late sequence: 21 scenes; surviving locomotive → changing freight economy → decline → tunnels remain.
- End: 4 scenes; modern Chicago → old infrastructure → concluding CTA narrative.

These analyses are supplementary; final subjective approval remains the user's full playback review.

## Review release

Tag:
`chicago-v3-sequence-fix-review-20260920`

Direct review asset:
`HIA_CHICAGO_V3_SEQUENCE_FIX_REVIEW_960x540.mp4`
