# Project Pluto — Generated Explanatory Frames R1 QC

Date: 2026-10-24  
Scope: the three gaps recorded in `MINIMAL_GENERATION_GAPS_V2.csv` only.

## Result

Three 3840x2160 PNG masters were created and imported into the open DaVinci Resolve project `Pluto`, Media Pool bin `PROJECT_PLUTO_GENERATED_EXPLAINERS_R1`.

| Asset | Script beat | Intended use | QC |
|---|---|---|---|
| GEN-01 | PLUTO-CH02-B01 | Explain intake air passing through the Tory core and exiting heated | PASS |
| GEN-02 | PLUTO-CH06-B03 | Distinguish tested Tory hardware from the unbuilt flight vehicle | PASS |
| GEN-03 | PLUTO-CH07-B01 | Connect the May 20 full-power test to the July 1 termination decision | PASS |

## Evidence safeguards

- GEN-01 is marked as an explanatory graphic and must not be described as a literal recovered Project Pluto drawing.
- GEN-02 preserves the exact source photograph on the left. The right-side vehicle is expressly labeled as a modern explanatory wireframe and `CONCEPT ONLY // NEVER BUILT`.
- GEN-03 uses ImageGen only for the design treatment. Both displayed document pages were re-composited from the exact source PNGs after generation, so no generated text is relied upon as evidence.
- No generated image represents a real Tory test, launch, flight, accident, or weapon deployment.

## Editorial placement

- GEN-01: 00:01:51:21 to approximately 00:02:01:21 at 25 fps.
- GEN-02: 00:13:07:00 to approximately 00:13:15:00 at 25 fps.
- GEN-03: 00:14:00:22 to 00:14:08:15 at 25 fps.

Placement is a recommendation tied to the locked narration map. The stills were imported but were not inserted into a timeline because the currently open `Pluto` project has no timeline or existing media assembly.

## Motion treatment for Resolve

- Hold each master long enough to read; use a 6–10 frame opacity/ease reveal rather than a hard cut.
- Animate only the information path: airflow left-to-right for GEN-01; left evidence then right concept for GEN-02; first node then second node for GEN-03.
- Keep scale movement within 100–103 percent. Avoid fast pans, bounce easing, and generic slideshow transitions.
- Preserve the 8 percent safe margin and the on-screen provenance/disclosure lines.

## Technical checks

- All three files decode through Pillow and report 3840x2160 RGB PNG.
- SHA-256 values are recorded in `GENERATED_EXPLANATORY_FRAMES_R1_MANIFEST.csv`.
- Visual review completed at full-frame scale: no clipped titles, random callout points, opaque gray cards, or generated microtext used as evidence.
