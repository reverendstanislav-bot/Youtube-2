# Chicago independent subtitle ↔ VO timing audit

Offsets are measured as **SRT cue start minus matched spoken-word start**. Positive = subtitle starts late.

## subtitles_en.srt
- Verdict: **FAIL: progressive drift ~9.60s across runtime; variable offset spread 14.72s**
- Cues: 293; aligned: 293
- Text-token match: 98.82%
- Median start offset: -0.360 s
- P05 / P95: -9.726 / 4.996 s
- Offset spread P05→P95: 14.722 s
- Estimated offset change over runtime: 9.597 s

| Cue | Voice t | SRT t | Offset | Text |
|---:|---:|---:|---:|---|
| 1 | 0.00 | 0.00 | +0.00 | Walk through downtown Chicago today, and almost nothing at street level tells you that another |
| 29 | 125.90 | 122.70 | -3.20 | That made the space beneath the streets valuable for a reason that had nothing to do with passengers. |
| 71 | 323.78 | 320.28 | -3.50 | The complexity only had to beat the alternative. |
| 141 | 642.30 | 638.21 | -4.09 | The system had solved Chicago’s street problem by becoming physically committed to one version of the |
| 219 | 966.60 | 969.36 | +2.76 | The U.S. |
| 261 | 1158.28 | 1161.12 | +2.84 | It was not a legend about a lost city beneath the city. |
| 293 | 1287.84 | 1287.51 | -0.33 | Sometimes long enough to matter all over again. |

## HIA_CHICAGO_FINAL_UPLOAD.srt
- Verdict: **PASS**
- Cues: 320; aligned: 320
- Text-token match: 98.82%
- Median start offset: 0.000 s
- P05 / P95: 0.000 / 0.000 s
- Offset spread P05→P95: 0.000 s
- Estimated offset change over runtime: 0.006 s

| Cue | Voice t | SRT t | Offset | Text |
|---:|---:|---:|---:|---|
| 1 | 0.00 | 0.00 | +0.00 | Walk through downtown Chicago today, and almost nothing at street level tells |
| 31 | 129.94 | 129.94 | +0.00 | had nothing to do with passengers. If some of the city’s repetitive |
| 76 | 320.70 | 320.70 | +0.00 | downtown to justify that complexity. |
| 154 | 642.30 | 642.30 | +0.00 | The system had solved Chicago’s street problem by becoming physically committed to |
| 240 | 966.60 | 966.60 | +0.00 | The U.S. Geological Survey later reported that utility services were lost in |
| 287 | 1158.28 | 1158.28 | +0.00 | It was not a legend about a lost city beneath the city. |
| 320 | 1287.84 | 1287.84 | +0.00 | Sometimes long enough to matter all over again. |

## HIA_CHICAGO_V2.srt
- Verdict: **PASS**
- Cues: 338; aligned: 338
- Text-token match: 98.82%
- Median start offset: 0.000 s
- P05 / P95: 0.000 / 0.000 s
- Offset spread P05→P95: 0.000 s
- Estimated offset change over runtime: 0.005 s

| Cue | Voice t | SRT t | Offset | Text |
|---:|---:|---:|---:|---|
| 1 | 0.00 | 0.00 | +0.00 | Walk through downtown Chicago today, and almost nothing at street level tells |
| 34 | 129.94 | 129.94 | +0.00 | had nothing to do with passengers. If some of the city’s repetitive |
| 81 | 320.70 | 320.70 | +0.00 | downtown to justify that complexity. |
| 162 | 644.10 | 644.10 | +0.00 | street problem by becoming physically committed to |
| 255 | 966.60 | 966.60 | +0.00 | The U.S. Geological Survey later reported that utility services were lost in |
| 302 | 1158.28 | 1158.28 | +0.00 | It was not a legend about a lost city beneath the city. |
| 338 | 1287.84 | 1287.84 | +0.00 | Sometimes long enough to matter all over again. |

