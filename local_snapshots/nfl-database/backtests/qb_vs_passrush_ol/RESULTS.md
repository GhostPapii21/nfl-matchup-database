# B4 QB passing efficiency vs opponent pass rush: OL pass-block vs DL pass-rush
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
| QB pass-yds overs: OL-DL mismatch (top third: leaky OL + strong rush) | 11 | 9/11 | 81.8% | 57%-94% | +56.2% | 0.07 |
| QB: rest | 16 | 6/16 | 37.5% | 21%-58% | -28.4% | 0.32 |
| WR/TE overs: mismatch top third | 39 | 27/39 | 69.2% | 56%-80% | +32.2% | 0.04 |
| WR/TE: rest | 76 | 37/76 | 48.7% | 39%-58% | -7.1% | 0.57 |

Gap = (opp D pressure rate − lg) + (team OL pressure allowed − lg), using sack-or-hit per dropback from our pbp, weeks < W. Top-third cut = +0.011. ESPN PBWR/PRWR is published only as season-to-date with no weekly snapshots on hand, so it can't be used walk-forward for Wk4–7 without leaking. It's left out of the test, and an ESPN-only slice would be look-ahead.

This test is separate from the rejected run-blocking `ol_dl_gap` test. Legs are in `rico_common/b4_legs.csv`. Per-week top-third vs rest: W4 .88/.75, W5 .65/.28, W6 .77/.45, W7 .67/.48. The direction held all 4 weeks.

## Recommendation
**The opposite of the expected direction, and no rule now.** Overs in the biggest pass-rush-vs-OL mismatches *hit more*: WR/TE 69.2% (27/39, p vs BE 0.04) vs 48.7%, and QB 9/11 vs 6/16. The likeliest reason is that a leaky OL facing a strong rush leads to trailing and pass volume. This is one of several tests run, and multiple-testing p is about 0.2. So **don't** add a cut for 'bad OL vs good rush'. A pass-rush mismatch shouldn't be used to cut or soften a WR/TE over. Track it non-live as a possible PRESS context input, using ESPN PBWR/PRWR only once weekly snapshots are archived; ESPN data is season-to-date, which would leak.
