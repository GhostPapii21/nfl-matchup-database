# B3 QB under pressure, blitz and weather
Generated 2026-11-01 (ET), analysis only, nothing live, no rule changed. Scripts live in `backtests/rico_common/`.

**Method:**
- Data: leak-free sim_v6 RAW medians from `tools/sim_v6_backtest.csv`, Wk4–7, with each Engine cutoff set before week W and no calibration.
- Lines: **stand-in** lines of floor(prior median)+0.5, the same method as `p6_rush_exception`, `ol_dl_gap` and `rb_rec_script`.
- p: mean over mc/bias/gr of Normal(median, SD), with the SD taken walk-forward.
- Bet rule: over when p > .5238, the −110 break-even.
- Features: from weeks < W only.
- Not covered: Wk3 (under 2 priors) and Wk8 Sunday (no RAW medians).
- Stats: p-values are two-sided binomials vs break-even, and the bucket comparison uses a two-proportion z test. Every result is small-n.

| Bucket | n | W/L | Hit | 90% CI | ROI −110 | p vs BE |
|---|---|---|---|---|---|---|
| QB pass-yds overs, all | 27 | 15/27 | 55.6% | 40%-70% | +6.1% | 0.85 |
| QB: high-pressure D & weak-under-pressure QB | 5 | 3/5 | 60.0% | 27%-86% | +14.5% | 1.00 |
| QB: other | 22 | 12/22 | 54.5% | 38%-71% | +4.1% | 1.00 |
| WR/TE overs, all | 115 | 64/115 | 55.7% | 48%-63% | +6.2% | 0.51 |
| WR/TE: high-pressure D & weak-under-pressure QB | 19 | 12/19 | 63.2% | 44%-79% | +20.6% | 0.37 |
| WR/TE: other | 96 | 52/96 | 54.2% | 46%-62% | +3.4% | 0.76 |
| WR/TE: high-pressure D & STRONG-under-pressure QB | 21 | 15/21 | 71.4% | 54%-84% | +36.4% | 0.12 |

Weather slice: 11 bet legs in rain or wind ≥15 games, hit 54.5%. That n is too small to test, and the Phase 11 and forecast gates already cut these.



- Pressure = sack or QB hit per dropback, since nflverse pbp has no pressure or blitz column.
- QB-under-pressure composite = z(EPA/db) + z(cmp%) + z(YPA) − z(sack rate) − z(TO rate), on pressured dropbacks, QB n ≥ 15, weeks < W.
- High-pressure D = the top third of pressure rate.
- **Blitz:** no walk-forward blitz data exists, since `week9/model/defense_blitz_pressure` is a season-to-date snapshot and would leak. Blitz isn't tested.

## Recommendation
**Don't adopt.** The hypothesis predicts that a weak-under-pressure QB facing a high-pressure D should underperform, and it didn't. Those WR/TE legs hit 63.2% (12/19) vs 54.2% for the rest. QB pass-yds overs on the same split hit 3/5 vs 12/22. No split is significant, and weather has n=11. Keep the pressure inputs already required by the gate as context, and add no pass/fail rule. Rerun when weekly blitz snapshots exist; I suggest archiving `defense_blitz_pressure` weekly from now.
