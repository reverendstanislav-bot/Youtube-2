# Youtube-2

Production repository for **Hidden Industrial America**.

## Episodes

- CHICAGO/ — Episode 1. Chicago underground freight system. Historical/reference production tree; always read its canonical status before touching it.
- TC497/ — Episode 2. LeTourneau TC-497 Overland Train. User-approved FULL_V13 publication master and QC are tracked in that directory.
- BIG_MUSKIE/ — Episode 3. Big Muskie / Bucyrus-Erie 4250-W. Current status: research and preproduction.
- Episode 4 — Satsop Nuclear Plant.
- Episode 5 — Lake Peigneur.

## Channel

Channel-level rules, scalable production structure, and approval conventions live under CHANNEL/.

## Source-of-truth rule

Never infer "final" from a filename. An episode becomes a publication/upload master only after:
1. explicit user approval;
2. technical QC;
3. subtitle/picture/audio QC;
4. the canonical status file is updated.

Large media may live in GitHub Releases/Actions rather than the Git tree. The Git tree must contain manifests, hashes, provenance/state notes, rebuild/recovery tooling, and links/IDs needed to reproduce the current state.
