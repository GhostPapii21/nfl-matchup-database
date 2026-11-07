# Source / Rights Manifest — NFL Week 9 Research Handoff

**Date:** 2026-11-07 ~17:08 ET
**Branch:** research/nfl-w9-source-verified-evidence-20261107
**Status:** RESEARCH_ONLY. Model NOT READY. No production writes.

## Files Delivered (PARTIAL where noted)

| File | Rows | Status | Rights / Restrictions |
|------|------|--------|-----------------------|
| WEEK1_8_PLAYER_USAGE_FULL.csv | 2 (sample) | PARTIAL | Public PFF summaries + independent aggregators. Full PFF raw restricted; no redistribution of licensed export. AJ Barner conflict flagged. |
| WEEK1_8_DEFENSE_COVERAGE_PRESSURE.csv | 1 (team note) | PARTIAL_RESTRICTED | PFR team aggregates public. Individual charted coverage / shell / defender responsibility restricted or incomplete. No inferences. |
| WEEK1_8_QUARTER_SCORE.csv | 2 (sample) | PARTIAL_VERIFIED | ESPN scoreboards + NFL.com finals. Full 121 verified in prior notes. OT separate. |
| WEEK1_8_QUARTER_MARKET_QUOTES.csv | 1 (note) | UNAVAILABLE | Odds API historical period markets exist but credit cost not checked / not spent. No top-up. |
| CALIBRATION_LEDGER.csv | 1 (note) | UNAVAILABLE | No archived pregame forecasts. Prospective only. |

## Conflict Resolutions

- **AJ Barner targets:** Prior Grok 51 vs PFF public 31 (and some aggregators 34). Flagged as conflict. Primary value 31 from PFF; excluded from model inputs until reconciled. Denominator: PFF targets on 233 routes.
- **Tyler Warren targets:** Verified 46 across PFF, Edgehalla, PerThirtySix, FTA. Matches prior verified history. Included.

## Injury / Availability

Confirmed active/inactive distinguished from questionable/projected/unknown. No shadow assignments inferred. No opportunity transfer to backups without official designation.

## Checksums (SHA of this commit will be recorded post-push)

All files source-auditable. Missing fields null with reason. No unsupported estimates.

**PR #2 remains research-only.**
