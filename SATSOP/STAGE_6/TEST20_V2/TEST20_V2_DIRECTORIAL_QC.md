# SATSOP — V2 TEXT-ONLY 20-IMAGE TEST / DIRECTORIAL QC

Updated: 2026-09-25

Status: **IMPROVED BUT NOT READY FOR FULL SCALE — REFERENCES STILL REQUIRED**

## Test boundary

- submitted/completed: **20/20**;
- model: GPT Image 2 / low / 1k / 16:9;
- authorized and attributable test cost: **10.00 credits**;
- retries: **0**;
- provider failures: **0**;
- reference mode: **TEXT ONLY — NO R01–R07 MEDIA ATTACHED**;
- balance observed after completion: **1,196.57 credits**.

The balance moved by more than this test's locked 10.00-credit cost while the jobs were running. Only 10.00 credits are attributable to these 20 jobs from their verified 0.50-credit model profile; the additional workspace movement is not attributed to this batch without a provider usage ledger.

## Technical QC

- 20/20 PNG files decode;
- resolution: 1344 × 752;
- non-zero sizes and SHA-256 recorded for every file;
- no failed, canceled, NSFW, or IP-detected job.

## Directorial QC

| Prompt | Beat | Verdict | Finding |
|---|---|---|---|
| SAT-GEN001 | SAT-B002 | CONDITIONAL | Early-phase construction reads clearly, but it remains generic and cannot be authenticated as Project Five without R02/R03. |
| SAT-GEN002 | SAT-B003 | FAIL | Invents a domed reactor building and therefore cannot represent reference-controlled Project Three. |
| SAT-GEN003 | SAT-B004 | FAIL | Clean map layout, but fabricated rivers, roads and completed domes make it unusable as factual Satsop geography. |
| SAT-GEN006 | SAT-B011 | CONDITIONAL | Sparse early works are improved, but exact Project Five identity remains unverified. |
| SAT-GEN011 | SAT-B019 | PASS | Utility-node network is visually clear, distinct and usable as a non-factual graphic base. |
| SAT-GEN012 | SAT-B021 | PASS | Three-state payment-obligation triptych communicates the contract mechanism without relying on readable text. |
| SAT-GEN016 | SAT-B026 | FAIL | Again fabricates coastal geography and reactor geometry; real R02 is indispensable. |
| SAT-GEN020 | SAT-B032 | CONDITIONAL | Two technical silhouettes read clearly, but reactor/building geometry requires R04 validation. |
| SAT-GEN022 | SAT-B036 | CONDITIONAL | Reactor-to-turbine-to-cooling chain reads, but the generated engineering layout cannot be treated as exact. |
| SAT-GEN025 | SAT-B039 | PASS | Covered stored equipment and inspection-only activity correctly communicate preservation rather than construction. |
| SAT-GEN032 | SAT-B048 | PASS | Missing systems and unfinished interfaces now dominate over exterior concrete, matching the remaining-cost idea. |
| SAT-GEN036 | SAT-B058 | PASS | One large commitment versus five modular units reads instantly and leaves clean overlay space. |
| SAT-GEN044 | SAT-B070 | PASS | Low/base/high and combined-cycle comparison is finally expressed as a clean physical-model graphic. |
| SAT-GEN046 | SAT-B074 | CONDITIONAL | Large-versus-small capacity metaphor is legible but too abstract to carry 1,240 MW and 600 aMW without careful overlay. |
| SAT-GEN050 | SAT-B079 | CONDITIONAL | Sparse regional demand context is improved, but the site identity and comparison axis remain too implicit. |
| SAT-GEN057 | SAT-B088 | FAIL | Four strips do not distinguish the four chronology events; repeated landscapes cannot carry termination/default/suspension dates. |
| SAT-GEN058 | SAT-B090 | PASS | Permit, property, remediation and debt workstreams read as distinct physical objects for later labels. |
| SAT-GEN063 | SAT-B096 | PASS | Civic meeting around a reuse model fixes the false renewed-construction problem and fits the 1995 redevelopment beat. |
| SAT-GEN065 | SAT-B102 | CONDITIONAL | Industrial reuse reads well, but the interior is not reference-verified as the Satsop turbine building. |
| SAT-GEN068 | SAT-B107 | CONDITIONAL | Useful industrial afterlife is clearer, but exact present-day site identity still requires R01/R07. |

Totals: **8 PASS / 8 CONDITIONAL / 4 FAIL**.

## Comparison with first test

| Metric | V1 test | V2 test |
|---|---:|---:|
| Pass | 5/20 — 25% | 8/20 — 40% |
| Conditional | 7/20 — 35% | 8/20 — 40% |
| Fail | 8/20 — 40% | 4/20 — 20% |
| Immediate rejection | 40% | 20% |

V2 cuts the outright failure rate in half and materially improves visual diversity. It does not solve site identity by prose alone.

## Locked V2 passes

The following eight V2 outputs are accepted and must not be regenerated automatically:

- SAT-GEN011;
- SAT-GEN012;
- SAT-GEN025;
- SAT-GEN032;
- SAT-GEN036;
- SAT-GEN044;
- SAT-GEN058;
- SAT-GEN063.

Together with the five locked V1 passes, the project now has **13 accepted generated images**. The remaining corrected queue is **55 images**, maximum **27.50 credits** if later approved.

## Remaining errors

1. Real Satsop geography and architecture cannot be recovered from text-only prompts.
2. `MAP_BASE` must use authenticated R02 as an actual image input or be built entirely as deterministic vector GFX.
3. Technical cutaways need R04 engineering references and should remain interpretive until checked.
4. Chronology should be authored as native editorial GFX rather than generated landscape strips.
5. Present-day reuse frames require R01/R07 before being called Satsop-specific.

## Gate

Do not run the remaining 55 images as text-only jobs. Acquire and attach real references first. No retries or replacement jobs are authorized by this report.
