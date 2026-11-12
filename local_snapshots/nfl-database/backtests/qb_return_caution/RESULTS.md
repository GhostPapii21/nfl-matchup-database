# B2 QB-return caution for WR/TE legs
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
| All WR/TE overs bet | 152 | 87/152 | 57.2% | 51%-64% | +9.3% | 0.26 |
| No QB-change flag | 124 | 70/124 | 56.5% | 49%-64% | +7.8% | 0.37 |
| Flagged (QB return or model built on backup) | 28 | 17/28 | 60.7% | 45%-74% | +15.9% | 0.45 |
|   flagged: return | 28 | 17/28 | 60.7% | 45%-74% | +15.9% | 0.45 |
|   flagged: built-on-backup | 0 | 0/0 | nan% | nan%-nan% | +nan% | nan |

One-rung drop on the flagged legs (line −10 yds / −1 rec, priced −150, BE 60.0%): 24/28 = 85.7%, ROI +42.9%, p vs BE 0.01.



**Control:** the same one-rung drop on the *unflagged* legs went 88/124 = 71.0% at −150, ROI +18.3%. Flagged vs unflagged drop hit p = 0.11. Starter = the team's top passer that week. Flag = the starter missed 2+ of the team's prior games, or the previous game's starter was someone else (the model was built on the backup). The −150 price for the lower rung is an assumption, because no alt-rung price history exists.

## Recommendation
**Use a flag, not a forced rung drop.** Flagged WR/TE overs did *not* underperform (60.7%, n=28, vs 56.5% unflagged). The one-rung drop looks good on flagged legs (85.7%), but it looks good on every leg at an assumed −150, so the gain isn't specific to QB returns. Flowers 0-for-5 is real but n=1. My recommendation: add a non-live **QB-CHANGE** flag that forces a manual look at the §7 window (the last 4 games with the current QB). Don't make the rung drop automatic. Retest once real alt-rung prices are archived.
