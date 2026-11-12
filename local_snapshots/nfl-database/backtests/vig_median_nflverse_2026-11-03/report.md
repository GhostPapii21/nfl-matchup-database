# Vig / median / nflverse backtest — 2026-11-03 (backtest only; for Ghost6 to vet before Rico)
Pre-registered in PREREG.md (commit 21e1815, sha256 152206a4…ab43) before any result. Fit = 2026 Wk3-6, holdout = Wk7-8. CIs = 95% bootstrap resampling games.
Cost: **$0 Grok, 0 Odds API credits** (saved prices only). Nothing live, no merges, no skill edits, no held files touched (sim engines imported read-only; outputs only in this folder).

## Summary
| Test | Verdict | Key number (holdout Wk7-8) |
|---|---|---|
| T1 power vs multiplicative de-vig | **INSUFFICIENT** (no detectable difference) | Brier .24634 vs .24651, diff −.00017 [−.00043, +.00012], n=947 |
| T2 median vs mean projections | **FAIL** (all rules) | best: median rule ROI −5.6% vs rush-under +4.0%, diff −9.6 pts [−24.4, +5.4] |
| T2 skew explains rush unders | **NOT SUPPORTED** per leg | slope +0.009 [−0.089, +0.117]; terciles 52.6% / 61.0% / 53.5% (not rising) |
| T3a FTN + snap-count features over market | **INSUFFICIENT** (not better than market with confidence) | Brier .24546 vs .24641, diff −.00095 [−.00830, +.00686] |
| T3a C2 fields (coverage shell, area, alignment) | **DATA GAP** | not published for 2026 by nflverse |
| T3b Platt on closing lines 2018-25 | **FAIL / no gain** in all 3 markets | ML diff −.00014 [−.00047, +.00021]; spread +.00024; total +.00019 |

Plain words: none of the three ideas beats the market or the rush-under baseline. The rush-under baseline (517 legs, 288-229, +4.77%) is still the best result on this data (reproduced exactly from the review-branch replay universe: legs_with_probs.csv Wk3-8 rushyds).

## T1 — power vs multiplicative no-vig (t1_devig.csv)
Single-book two-sided saved prices, 2,382 legs (fit 1,435 / holdout 947). Average book hold ~6.2%. Power shifts p by <0.1 pt on average because most props are near −110/−110, where both methods agree.
| set | market | n | Brier mult | Brier power | diff [95% CI] | logloss diff [CI] |
|---|---|---|---|---|---|---|
| holdout | ALL | 947 | .24651 | .24634 | −.00017 [−.00043, +.00012] | −.00036 [−.00092, +.00024] |
| holdout | rec | 322 | .24051 | .24007 | −.00044 [−.00118, +.00033] | −.00093 [−.00249, +.00065] |
| holdout | rushyds | 163 | .24815 | .24800 | −.00015 [−.00039, +.00006] | −.00033 [−.00087, +.00011] |
| holdout | recyds | 326 | .25010 | .25012 | +.00001 [−.00005, +.00008] | |
| holdout | rushrec | 82 | .25024 | .25027 | +.00002 [−.00005, +.00010] | |
| holdout | passyds | 54 | .24996 | .24996 | .00000 | |
| fit | ALL | 1435 | .24938 | .24940 | +.00002 [−.00014, +.00019] | |
| all Wk3-8 | ALL | 2382 | .24824 | .24819 | −.00005 [−.00020, +.00010] | |
Direction favors power on the holdout (matches the Chanchani study, https://shaanchanchani.github.io/articles/sportsbook-props, 15,456 props), but the gain is ~0.0002 Brier and not distinguishable from zero here. Switching is harmless but not shown to help. Note: the replay's `nv_over` is not the single-book multiplicative number (max gap .041; it appears to be a cross-book no-vig), so T1 compares both methods on the same single book.

## T2 — median vs mean (t2_rules.csv, t2_skew_*.csv)
Sims rerun (3 engines, opp 0.5, same leak-free cutoffs) to save means; rerun probabilities match the saved ones exactly (median abs diff 0.0). 2,380 / 2,382 legs have sims.
| rule (side = projection vs line) | margin (chosen on fit) | holdout W-L | holdout ROI | vs rush-under holdout (+4.0%) [CI] | Wk3-8 W-L, ROI |
|---|---|---|---|---|---|
| mean | 5% | 399-387 | −6.3% | −10.3 pts [−26.5, +6.1] | 1039-1002, −5.2% |
| median | 0 | 485-462 | −5.6% | −9.6 pts [−24.4, +5.4] | 1225-1155, −4.3% |
| skew-adj median (fit-set bias corrected) | 0 | 470-477 | −6.5% | −10.5 pts [−23.9, +3.1] | 1221-1159, −3.3% |
By market, Wk3-8 (median rule): rushyds 273-244 −0.4%, rec 275-219 −1.3%, recyds 511-519 −6.4%, rushrec −8.1%, passyds −7.5%. Median beats mean (−4.3% vs −6.0% at margin 0), but nothing beats simply betting every rush under.
**Skew:** In rush yards the line sits between the median and the mean: our sim median is below the line in 62% of legs, the sim mean in only 39%; actual results land median −1.5 yds vs the line, mean +3.6 yds. So the market-level story fits (books hang lines above the median of a right-skewed stat, unders cash 55.7%). But per leg, more skew does NOT mean more unders: slope CI includes 0, terciles 52.6% / 61.0% / 53.5%. Verdict per prereg: NOT SUPPORTED as a leg-level selector.

## T3a — nflverse/FTN features over market (t3a_features.csv)
Features from prior weeks only: opponent blitz rate, pass rushers, box count, play-action and motion faced (FTN charting 2026 Wk1-8), player last-2 snap share and trend (snap counts 2026). Offset-logit on market p, fit Wk3-6 per group (rush/rec/pass), L2=1.
Holdout ALL n=947: Brier .24546 vs market .24641, diff −.00095 [−.00830, +.00686]; logloss .68482 vs .68585. By market: rushyds −.0042 [−.0194, +.0129], rushrec −.0047 [−.0329, +.0251], recyds −.0018 [−.0079, +.0045], rec +.0017, passyds +.0034. Small improvements, none certain. Largest fitted weight: rush legs vs heavier box → lower over p (−0.32 per SD).
**Data gap:** coverage shell, man/zone, routes (pbp_participation) are published only through 2025; NGS only through 2024 in releases. The C2 fields cannot be filled for 2026 from nflverse; they stay flags.

## T3b — Platt on closing lines (t3b_closing_platt.csv)
nfldata games.csv has closing odds from 2006 (not 1999). Train 2006-2017, test 2018-2025.
| market | n train / test | Platt a, b | Brier raw | Brier Platt | diff [CI] |
|---|---|---|---|---|---|
| home ML win | 3062 / 2219 | −0.041, 1.015 | .21075 | .21061 | −.00014 [−.00047, +.00021] |
| home spread cover | 2987 / 2175 | −0.046, −0.094 | .24969 | .24993 | +.00024 [−.00060, +.00107] |
| total over | 3011 / 2205 | +0.018, −0.247 | .24998 | .25017 | +.00019 [−.00035, +.00075] |
Closing lines are already calibrated (ML slope ≈1.0); recalibrating doesn't help out of sample. Supports keeping the market price as the anchor.

## Licenses (LICENSES.md)
nflverse data CC-BY-4.0 (credit nflverse). FTN charting is **CC-BY-SA 4.0**, attribution "FTN Data via nflverse"; any derived file we share (t3a_leg_features.csv) must carry the same license. nfldata has **no license**: used as data for analysis only, no code copied, raw file not committed (.gitignore).

## Files
PREREG.md/.sha256, LICENSES.md, common.py, t1_devig.py/.csv, run_sims_meanmed.py + sims/, t2_median.py, t2_rules.csv, t2_skew_slope.csv, t2_skew_terciles.csv, t2_legs_meanmed.csv, t3a_features.py/.csv, t3a_leg_features.csv, t3b_closing_platt.py/.csv, logs.

## Vet notes (Ghost6 vet passed, Nov 3, 2026; edits added after the vet)
1. **Fit window:** the sim engines calibrate walk-forward, so Week 8 legs use calibration that includes Week 7 results. Everything is still pre-kick, but this is not strictly "fit on Weeks 3-6 only."
2. **T2 resampling:** the T2 rule CIs used 5,000 bootstrap reps, not the 10,000 registered in PREREG.md.
3. **T3a market price:** T3a used nv_over (the cross-book no-vig) instead of the single-book price. That moves Brier by about 0.0001 and doesn't change the verdict.
4. **Rush skew slope:** the slope is fragile because of outliers. 51 legs have lines under 5 yards, and 25 have a sim median of 0.5 or less.
5. **T3b spreads and totals:** neither shows a calibration signal (slopes of about -0.09 for spreads and -0.25 for totals). Only the moneyline slope is near 1.0.
