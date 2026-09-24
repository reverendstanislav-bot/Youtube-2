# SUPERSEDED / REJECTED

This document describes the rejected HIA V10 semantic-rebuild Shorts system. It is retained only as historical QC evidence. **DO NOT USE IT AS A PRODUCTION REFERENCE.** Active Shorts canon: `CHANNEL/SHORTS_PRODUCTION_CANON.md` (Youtube-1 direct-cut model).

# HIA Shorts V10 — Wave 2 hard QC — 2026-09-24

## Scope

This report covers the seven V10 Wave-2 review Shorts only:

- CHI-S02
- CHI-S03
- CHI-S04
- CHI-S05
- TC497-S03
- TC497-S04
- TC497-S05

Big Muskie and long-form publication masters were not changed.

## Final build

- GitHub Actions run: `36017934649`
- Head commit: `d0223420ad6b8b49039dd6fe8571ea5110ae2eaf`
- Combined review artifact: `hia-v10-wave2-patch1-review`
- Artifact id: `10815054356`
- Artifact digest: `sha256:e51d1bfa305c21448f6d631f46994b8c3647481cda837958a0be524788941a92`
- Cost of this repair pass: **0 generation credits**. Existing assets + editor-native GFX only.

## Repair pass completed

- fixed the global ASS phrase-overlap bug;
- clamped every subtitle event to the next event / Short duration;
- removed legacy `100,100)}` contamination;
- display-normalized `Kinsey` → `Kinzie` in Chicago captions;
- display-normalized `Aircrafts` → `Aircraft` in TC497-S05 captions;
- added auto-fit for long metric labels so they cannot overflow the vertical safe width;
- editor-native GFX no longer receive a duplicate metric overlay unless explicitly enabled;
- CHI-S02 received origin / uncertainty / two-foot-gauge explanatory GFX;
- CHI-S03 received a clean obsolescence comparison beat and verified street archive;
- CHI-S04 received a clean network-flood explanatory payoff and corrected Kinzie display text;
- CHI-S05 received restrained legal-record cards separating allegation from final finding;
- TC497-S03 received an ordinary-road-truck vs roadless-TC-497 comparison;
- TC497-S04 now shows a verified January 1961 U.S. Army R&D publication excerpt before concept imagery;
- TC497-S05 separates terrain obstacles, verified CH-54 archive, vertical-lift explanation, and legacy payoff.

## Machine QC

| Short | Tech | Resolution / FPS | Audio | Decode | Subtitle overlaps | Forbidden strings |
|---|---|---|---|---|---:|---|
| CHI-S02 | PASS | 1080x1920 / 25 | 48 kHz stereo | PASS | 0 | none |
| CHI-S03 | PASS | 1080x1920 / 25 | 48 kHz stereo | PASS | 0 | none |
| CHI-S04 | PASS | 1080x1920 / 25 | 48 kHz stereo | PASS | 0 | none |
| CHI-S05 | PASS | 1080x1920 / 25 | 48 kHz stereo | PASS | 0 | none |
| TC497-S03 | PASS | 1080x1920 / 30 | 48 kHz stereo | PASS | 0 | none |
| TC497-S04 | PASS | 1080x1920 / 30 | 48 kHz stereo | PASS | 0 | none |
| TC497-S05 | PASS | 1080x1920 / 30 | 48 kHz stereo | PASS | 0 | none |

Forbidden-string scan includes `100,100)}`, `Kinsey`, and `Aircrafts` in the rendered ASS review subtitles.

## Final MP4 SHA256

- CHI-S02: `f7c3e7be08c30fee1b1f5ac4381fd748b5837d8f3e8c86a01ab187538175c81a`
- CHI-S03: `416e03c5624640ba725bd932fb35682f4f299fcd562d0548efa125a693f30661`
- CHI-S04: `88705e40509b73e672c487933610622cdb125535ec48ea9243da0ac6c0991099`
- CHI-S05: `1442c3f14ac4efb16904022b86e934ed3d8095e72179445e4b6cede878a3ed3c`
- TC497-S03: `9961f17ddfd737f8e06f4631a35a124cff47e7892c112a61de64de1afe020d55`
- TC497-S04: `67e868b5e5136df478e951c25b86a31225749392484e8babe7ef5f9b70085c28`
- TC497-S05: `24d2eb12ff18e8b6f96d2a5db897d66cf36ccdc8378c4314b3af62ff6e238794`

## Source / fact notes

- Chicago source script and source subtitles use **Kinzie Street**. The Wave-2 extraction map contained the transcript token `Kinsey`; V10 display captions are normalized back to the source-script spelling.
- TC497-S04 Army evidence card uses the verified article heading **“Nuclear Power Planned For Overland Train”** and a short excerpt from the January 1961 U.S. Army Research and Development Newsmagazine. The visual is deliberately an editor-native DOCUMENT EXCERPT card, not a fake archival scan.
- TC497-S05 uses the public-domain CH-54 archive already present in the canonical TC497 package. Generated helicopter imagery is not labeled as historical proof.

## Human visual QC verdict

No hard visual blocker remains in the seven review Shorts after the final cleanup:
- no duplicated visible panel system;
- no horizontal shake / aggressive side-to-side scan;
- captions stay in the vertical safe area;
- editor-native GFX no longer collide with service labels;
- provenance labels are readable and truthful for the shown asset type;
- map/document/legal beats are readable in 9:16;
- the previously failing TC497-S04 and TC497-S05 now have evidence-led visual logic.

## State

**Wave 2 review gate: PASS.**

Per `CHANNEL/SHORTS_PRODUCTION_CANON.md`, these remain `RENDER_REVIEW`, not `APPROVED`, until explicit user visual approval.
