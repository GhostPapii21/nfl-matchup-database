# Calibration layer for the opportunity simulation (Phase 3, item A)

`fit.py` fits, per stat, `logit(p_cal) = const + lp*logit(p_sim) + lt*log(line)` on 2024-2025 backtest rows and tests on
2026 (`dashboard/backtest_opportunity.py` rows; every projection uses only earlier weeks). Kept only where 2026 Brier improved.

| Stat | 2026 Brier: simulation -> calibrated | Example | Used? |
|---|---|---|---|
| Carries | 0.1661 -> 0.1641 | 12+ carries: sim 38%, calibrated 43%, actual 42.6% | Yes (lines 12-15) |
| Rushing yards | 0.1427 -> 0.1418 | 50+: sim 35%, calibrated 37%, actual 39% | Yes (lines 50-90) |
| Receiving yards | 0.1017 -> 0.1016 | 40+: sim 30%, calibrated 33%, actual 34% | Yes (lines 40-100), small |
| Receptions | 0.13394 -> 0.13396 | no gain | No (switched off) |

Applied in `dashboard/opportunity.py` (`calibrate`, `chances`) to the board's chance tables, inside the fitted line range
only, and chances never rise as the line rises. Weights: `dashboard/calibration.json`. The 100+ yard overestimate is not
fixed by this form (2026: sim 5.3%, actual 4.7%); revisit with the full season.
