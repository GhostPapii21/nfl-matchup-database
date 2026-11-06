# Brainstorm — ≥40pp delivery anomaly guard (engineering)

Generated: 2026-11-06 07:19:47 ET
Skill: betting-game-brainstorm loaded; **no edge legs / no slip** (engineering detector only).

## Scenario (engineering)
Rico: never surface |raw_p − exact paired no-vig| ≥ 0.40 as a pick. Quarantine DIAGNOSTIC_ANOMALY; investigate identity/units/timestamp/calibration; preserve raw; no hide via anchor.

## Approaches considered
1. **Market-side delivery_guard only** (recommended) — owns surface/quarantine envelope; CORE keeps producer/contract. Avoids duplicate thresholds.
2. CORE adversarial gate only — overlaps; market already surfaces research edges via separate_outputs.
3. Soft shrink toward 50% — **rejected** (Rico no-shrink; hides anomalies).

## Design (approved by Rico t367u + phase5 prompt)
- `ANOMALY_EDGE_PP_THRESHOLD = 0.40`
- `guard_edge_delivery(raw_p, market_p, …)` → surfaceable | quarantined
- Reasons: ID_CHECK / UNITS_CHECK / PRICE_TIME_CHECK / CALIBRATION_CHECK / EDGE_GAP_GE_40PP
- Wire into `separate_outputs` enrichment; actionable NOLINE; Bias UNFITTED; edge_basis RAW_ONLY
- Tests: 39.9 not threshold-quarantine; 40.0/50 quarantine; units; identity; time; calib preserved

## Data check
Saved paired research MATCHED=60 from authorized CSVs; Pin Q2–Q4 spreads ABSENT→NOLINE; no fitted OOS calib rows → Bias stays UNIMPLEMENTED. Public method research informs; does not fabricate quotes.

## Pre-mortem
False quarantine of legitimate 39pp research diffs if float compare wrong; false pass if percent-scale 55 treated as 0.55 without UNITS_CHECK; silent mutation of raw — all covered by TDD cases.
