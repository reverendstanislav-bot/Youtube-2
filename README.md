# Youtube-2

Production repository for **Hidden Industrial America**.

## Episodes

- `CHICAGO/` — Episode 1. Current active build: **R15 Smooth Remotion review**. Earlier masters remain withdrawn and must not be uploaded.
- `TC497/` — Episode 2. Current active build: **R14 Remotion re-edit review**. The earlier V13 textless 1080 master is withdrawn and must not be uploaded.
- `BIG_MUSKIE/` — Episode 3. Big Muskie / Bucyrus-Erie 4250-W. Picture V2 review build complete; technical QC passed; not RC/final.
- `SATSOP/` — Episode 4. Satsop Nuclear Plant / WNP-3 and WNP-5. Initial research and development.
- Episode 5 — Lake Peigneur.

## Active production workflows

Only two episode render workflows are active:
- `.github/workflows/build_chicago_r14_editorial_recut.yml`
- `.github/workflows/build_tc497_r14_remotion_reedit.yml`

Legacy build/review workflows were removed from the current tree. They remain available through Git history if ever needed for forensic recovery.

## Channel

Channel-level rules, scalable production structure, provenance rules, and approval conventions live under `CHANNEL/`.

## Source-of-truth rule

Never infer "final" from a filename. An episode becomes a publication/upload master only after:
1. explicit user approval;
2. editorial visual review;
3. technical QC;
4. subtitle/picture/audio QC;
5. canonical status update.

Large media belongs in GitHub Releases/Actions rather than the Git tree. The Git tree should keep only the current production code, essential recovery dependencies, manifests, source/QC records, and canonical status.

## Shorts

Canonical Shorts rules: `CHANNEL/SHORTS_PRODUCTION_CANON.md`.
Episode extraction maps currently exist for Chicago and TC497 under each episode's `SHORTS/` directory. Shorts remain extraction-first and are rendered only after long-form approval.
