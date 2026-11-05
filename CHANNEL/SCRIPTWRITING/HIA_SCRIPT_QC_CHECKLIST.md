# HIA script QC: PASS / HOLD / REJECT

Evaluate final spoken text under [canon](HIA_SCRIPTWRITING_CANON.md), [retention QC](HIA_RETENTION_QC.md) and [fact protocol](HIA_FACT_CHECK_PROTOCOL.md). Every row needs status, paragraph/source evidence, reason, corrective action, reviewer/date and retest. Initial status is HOLD.

PASS: criterion demonstrated by specific evidence. HOLD: missing/unverified evidence or incomplete work. REJECT: demonstrated falsehood, misleading approach or incompatible implementation. This does not reopen locked films; regression is descriptive compatibility review.

| ID | Criterion | PASS evidence / failure test | Critical |
|---|---|---|---|
| QC01 | First 15s hook | Verified action/anomaly in spoken text, no generic intro | yes |
| QC02 | First 60s retention | Hook, stakes, paradox and promise operate together | yes |
| QC03 | Central investigation | One consequential question answered with evidence | yes |
| QC04 | Relevant surprise/context | Origin/constraint changes understanding without history dump | no |
| QC05 | Revelations or justified alternative | Meaningful discoveries, no forced three-battle story | yes |
| QC06 | Increasing stakes | Real difficulty, cost, consequence or changed expectations | no |
| QC07 | Engineering mechanism | Actual decision, how it works, result and tradeoff | yes |
| QC08 | Factual source coverage | Final factual clauses traced, no unresolved critical error | yes |
| QC09 | No invented motives/quotes | No fabrication or unsupported first/largest/secret | yes |
| QC10 | No redundant explanation | Repeat only where new evidence changes meaning | no |
| QC11 | Causal progression | Consequences, not just dates, connect chapters | yes |
| QC12 | Mid CTA | Earned anchor,8–12s target or explicitly reviewed alternative | no |
| QC13 | Main payoff | Opening promise explained at final major turn; proportions flexible | yes |
| QC14 | Historical reassessment | Real legacy and known/unknown boundary | no |
| QC15 | Final CTA | Relevant question, natural subscribe, verified end-screen bridge | no |
| QC16 | Native en-US / translation | Spoken clarity; equivalent EN/RU IDs if required | yes |
| QC17 | Realistic duration | Spoken EN count, measured approved pace or honest timing HOLD | yes |
| QC18 | Feasible visual production | Specific files/pages/ranges, rights/quality gates and fallback | yes |
| QC19 | Shorts excluded | No Shorts scripts, extraction maps, generation or production planned under latest owner override | no |
| QC20 | HIA compatibility | Voice evidence, no subtitles/AI video, safe zones, locks and approval gates | yes |

A justified alternative is tested under its criterion, not penalized for lacking eight literal headings. No row silently disappears as N/A: document an applicable alternative. CTA omissions require rationale and review. VOICE/TIMING HOLD does not authorize generation of a sample. Critical failures cannot be averaged away.

## Automated gate integrity

Copy [review JSON template](templates/SCRIPT_REVIEW_TEMPLATE.json). Run:

    python CHANNEL/SCRIPTWRITING/tools/validate_script_review.py EPISODE/SCRIPT_REVIEW.json

Checks:20 unique IDs, allowed statuses, evidence for PASS, actions for HOLD/REJECT, correct critical flags and evidence for any owner-approval claim. This cannot judge facts, rights or drama. Structurally valid all-HOLD remains HOLD; all 20 PASS is READY_FOR_OWNER_REVIEW only. Owner approval is recorded separately. No automated Script Lock.

## Final package

Script path/hash/version, editorial QC, fact/legal QC, retention map, CTA map, timing report, explicit Shorts exclusion, outstanding issues and owner decision. Preserve previous versions and full diff for changes. Finishing a checklist never launches TTS/images/editing.
