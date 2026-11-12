# B1 RB YPC floor: sim YPC vs the defense's opponent-adjusted YPC allowed
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
| All RB rush-yds overs the model would bet | 53 | 32/53 | 60.4% | 49%-71% | +15.3% | 0.27 |
| Pass floor (sim YPC ≤ def adj YPC allowed) | 31 | 19/31 | 61.3% | 47%-74% | +17.0% | 0.37 |
| FAIL floor → would be cut | 22 | 13/22 | 59.1% | 42%-74% | +12.8% | 0.67 |
| Variant: tolerance +0.3 | 39 | 23/39 | 59.0% | 46%-71% | +12.6% | 0.43 |
| Variant tol fails | 14 | 9/14 | 64.3% | 43%-81% | +22.7% | 0.43 |

floor ok vs fail p=0.87



- Sim YPC = mean sim median ÷ prior carries per game.
- Defense adjusted YPC = league YPC + the mean of (rush yds − the rusher's own prior YPC) on rushes against that defense, weeks < W.
- Legs in `rico_common/b1_legs.csv`.

## Recommendation
**Don't adopt the floor.** Legs that fail the floor hit 59.1% (13/22) and legs that pass hit 61.3% (19/31), with a difference p = 0.87. Cutting the fails would have removed winning legs. Walker 21-69 and J. Williams 24-56 are anecdotes the walk-forward data doesn't support. If anything, keep it as a non-live note in the checklist.
