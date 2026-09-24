# BIG MUSKIE — FINAL SOURCE REUSE AUDIT V1

Status: **PASS**

Rule: every visible R / C / D source asset may appear on screen no more than **2 times**.

Maximum observed reuse: **2**  
Violations: **0**

| Source | Uses | Beats | Rights / role | Result |
|---|---:|---|---|---|
| C01 | 2 | BM-B093, BM-B108 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C02 | 1 | BM-B059 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C07 | 1 | BM-B019 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C09 | 1 | BM-B054 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C10 | 2 | BM-B009, BM-B065 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C12 | 2 | BM-B023, BM-B110 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| C19 | 2 | BM-B017, BM-B060 | PUBLIC DOMAIN — U.S. EPA / NARA; Ohio regional context only | PASS |
| D03 | 2 | BM-B038, BM-B041 | DOCUMENT — US3531088A hoist patent; engineering lineage, not exact 4250-W blueprint | PASS |
| D04 | 2 | BM-B051, BM-B052 | DOCUMENT — US3375892A stepping/walking patent; engineering lineage, not exact 4250-W blueprint | PASS |
| D05 | 2 | BM-B066, BM-B069 | DOCUMENT — 1977 U.S. Bureau of Mines / Penn State study; exact cited pages/figures only | PASS |
| D06 | 2 | BM-B083, BM-B085 | DOCUMENT — U.S. EPA Title IV source; exact timing/context only | PASS |
| R01 | 2 | BM-B004, BM-B063 | PUBLIC DOMAIN — U.S. EPA / NARA | PASS |
| R02 | 2 | BM-B024, BM-B031 | PUBLIC DOMAIN — U.S. EPA / NARA | PASS |
| R03 | 2 | BM-B018, BM-B030 | PUBLIC DOMAIN — U.S. DOE | PASS |
| R05 | 2 | BM-B005, BM-B092 | CC BY-SA 3.0 — Brian M. Powell | PASS |
| R06 | 2 | BM-B002, BM-B116 | CC BY-SA 4.0 — Toni Leland | PASS |
| R07 | 2 | BM-B003, BM-B101 | CC BY-SA 3.0 — Eric Gunderson | PASS |
| R08 | 2 | BM-B032, BM-B098 | CC BY-SA 3.0 — Eric Gunderson; re-verified on Wikimedia Commons 2026-09-24 | PASS |
| R09 | 2 | BM-B102, BM-B104 | CC BY 2.0 — Charles Barilleaux | PASS |
| R10 | 2 | BM-B105, BM-B107 | CC BY 2.0 — Charles Barilleaux | PASS |
| R11 | 2 | BM-B109, BM-B112 | CC BY-SA 4.0 — Toni Leland | PASS |

Sequence note:
- exact same visible asset is never used more than twice;
- the only consecutive identical source ID is D04 across BM-B051/BM-B052, intentionally using two different patent crops;
- long GFX runs use different FX IDs and different locked compositions rather than repeating one image.
