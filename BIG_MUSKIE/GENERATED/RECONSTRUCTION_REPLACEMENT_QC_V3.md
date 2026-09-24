# BIG MUSKIE — RECONSTRUCTION REPLACEMENT QC V3

Status: **10 PASS / 2 HOLD / 3 REJECT — NOT YET ASSET-LOCKED**

Date: 2026-09-24

Scope: the 15 replacement reconstruction slots from `RECONSTRUCTION_REPLACEMENT_PROMPT_PACK_V2.md`.

Important physical-file finding:
- 15 replacement slots were requested;
- **14 unique replacement files are physically present** in the current conversation workspace;
- one cycle output was overwritten because two generated images resolved to the same filename;
- therefore the package cannot be called 15/15 complete even before content QC.

## Per-slot QC

| GEN | Status | Current file / role | Finding |
|---|---|---|---|
| GEN05 | **HOLD** | `massive_dragline_bucket_in_open_pit_mine.png` | Strong loaded-overburden bucket and plausible 4250-W background. Critical bucket occupies the lower-right subtitle-safe band; salvage by reframe/mask before accepting. |
| GEN06 | **PASS** | `colossal_dragline_over_the_open_pit_mine.png` | Whole-machine relationship reads, circular tub/base visible, no crawler chassis, good negative-space floor. |
| GEN07 | **PASS** | `giant_dragline_excavator_at_work.png` | Bucket is on the ground in broken overburden with taut drag geometry; correct drag-start beat. |
| GEN08 | **PASS** | `giant_dragline_over_open_pit_mine.png` | Loaded bucket is airborne and 4250-W circular-tub identity reads. Some loose material falls, but hoist phase remains legible. |
| GEN09 | **REJECT** | no production-distinct swing frame | Available operating frames are near-duplicates and read as hoist/dump rather than a distinct loaded swing toward spoil. One unique GEN09 frame is still required. |
| GEN10 | **REJECT** | `rusty_dragline_over_the_open_pit.png` / duplicate-family operating frame | Bucket is still visibly dumping/loaded; required empty-or-nearly-empty post-dump return phase is not shown. Composition is also too close to adjacent operating frames. |
| GEN12 | **REJECT** | `giant_dragline_and_trailing_cable.png` | Foreground “cable” reads as a huge rigid/segmented industrial pipe or hose, not a believable flexible high-voltage trailing cable. Misleading for BM-B047. |
| GEN13 | **PASS** | `big_muskie_overlook_in_the_open_pit.png` | Circular tub/base is unmistakable and dominant; strong stability beat. |
| GEN14 | **HOLD** | `monumental_dragline_in_the_open_pit_mine.png` | No tracks/wheels and shoe-like supports are present, but a specific mid-step walking state is not clearly readable. Test with D04/editorial motion overlay; otherwise replace. |
| GEN16 | **PASS** | `rusty_dragline_maintenance_crew.png` | Human-scale maintenance/workplace scene works; lower base does not introduce crawler geometry. |
| GEN18 | **PASS** | `vintage_dragline_in_an_open_pit_mine.png` | One solitary intact machine, bucket down, no second spare, good empty-space dependency composition. |
| GEN19 | **PASS** | `massive_dragline_maintenance_crew.png` | Open service access + mechanics clearly reads as troubleshooting/repair, not catastrophe. |
| GEN20 | **PASS** | `abandoned_dragline_in_the_quarry.png` | Intact idle machine, subdued post-operation mood, no dismantling. |
| GEN21 | **PASS** | `abandoned_giant_excavator_in_open_pit_mine.png` | Distinct closer post-shutdown infrastructure-burden composition; circular tub identity readable. |
| GEN22 | **PASS** | `dragline_demolition_at_dusk.png` | Controlled dismantling clearly underway with cranes and a separated structural section; no explosion/fantasy. |

## Totals

- **PASS: 10**
- **HOLD: 2** — GEN05, GEN14
- **REJECT: 3** — GEN09, GEN10, GEN12

## Exact remaining work

### Zero-cost salvage first
1. **GEN05** — create a subtitle-safe reframe/mask; keep the same image if the bucket can be moved clear of the lower caption band.
2. **GEN14** — test D04-derived walking-step overlay / crop to make the shoe-transfer state explicit without asserting false exact geometry.

### Regenerate
1. **GEN09** — unique loaded swing frame; materially different camera angle from GEN08/GEN10.
2. **GEN10** — empty/nearly-empty bucket immediately after dump, beginning return.
3. **GEN12** — believable flexible trailing electrical cable; no pipe/hose appearance.

After GEN05/14 salvage and GEN09/10/12 replacement:
- repeat 15/15 reconstruction QC;
- only then combine with the 7 previously retained/salvaged reconstruction frames;
- final target = **22/22 reconstruction PASS**;
- then build FINAL 116-BEAT ASSET LOCK.

No claim of 22/22 completion is permitted yet.
