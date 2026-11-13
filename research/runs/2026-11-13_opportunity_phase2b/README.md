# NFL-75 Phase 2b: RB/WR/TE depth signal, M grid past 5000, opt-in engine INT pooling

Depends on PR #38 (Phase 2 opportunity model). This branch starts from the #38 head, 0b4ba62. Research only. projection_ready stays false. No W10-12 actuals were read. Zero Odds API credits were spent and no network was used for fitting or the backtest.

## What changed
1. **Depth signal (`calibration/opportunity_fit.py`).**
   - Source: `base_shares(..., dp)` reads `data/historical/nflverse/derived_pit/depth_skill_snapshots_2025_2026.csv.gz` (sha256 943a55ac…).
     - The file was derived from the nflverse depth charts retrieved 2026-11-13T08:01:05Z (03:01 AM ET): depth_charts_2025.parquet sha 14f74185…, depth_charts_2026.parquet sha 288f3dbb….
     - Each game uses the latest RB/WR/TE/FB snapshot before 04:00 UTC on game day.
   - Weighting: a kept player's weight is multiplied by exp(-br·(rank-1)) if he is on the chart, and by exp(-bo) if he is not.
   - Optional force-keep of stale charted players: off / top (RB2, WR3, TE1) / all.
   - Fitting (`fit_slot_depth`): a staged DM-likelihood search starting from the frozen #38 fit for the same week, in the order depth → (lam, K, gamma) → depth → alpha.
   - The gamma grid was extended down to 0.4. 2024 games have no dated chart, so they are unaffected.
2. **EB M grid** extended to 10000, 20000, 50000, 100000 and 1e9 (pure position prior).
3. **Opt-in engine INT pooling (`core/possession_engine_v0/int_pool.py`, kwarg `simulate_games(int_pool=...)`).**
   - Each team's per-attempt INT rate in its own row pool is pooled toward the league rate: p* = (k + m·p_league)/(n + m).
   - Each sampled pass attempt gets one draw from its own RNG (SeedSequence([seed, 75003])). It is converted INT ↔ incompletion so the team rate equals p* in expectation.
   - Runs and sacks never draw.
   - p_league is the 2026 weeks < w rate. m is fitted by binomial log likelihood over 2024-25 W4-18 plus 2026 W4..w-1 (`calibration/opportunity_intcap.py`). m = 1200 for every eval week, which is not at the grid edge.
4. **Guards.**
   - Default `int_pool=None` makes no draws and is bit-identical to main (golden digests).
   - `int_pool` is refused from a config, refused above n = 20,000, and refused by `snapshots/lock.run_sim`. It does not appear in `pipeline/sim100k.py`.
5. **Freeze.**
   - The holdout manifest now freezes the 2b model (`holdout_freeze_manifest.json`). It covers the code, the 2b W10 params and the W10 INT-pool spec.
   - It was first frozen at 7a0d45b (pre-rebase; 94b4c26 after the rebase onto main 7364335, same tree).
   - It was re-frozen at **f63daba** after review: only two harness files changed, opportunity_backtest.py (no-INT-pool variant) and opportunity_report_2b.py. All model code, params and the INT-pool spec hashes are unchanged. Both freezes are recorded in the manifest.
   - The #38 manifest (`../2026-11-13_opportunity_phase2/holdout_freeze_manifest.json`, model b6e955c) is marked `SUPERSEDED`. It would now refuse, because simulate.py, opportunity_fit.py and opportunity_backtest.py changed.

## Fitted depth parameters (W4-W10, every week)
| slot | force | br | bo | lam | gamma | K |
|---|---|---|---|---|---|---|
| carry | off | 0.25 | 2.0 | 0.8–0.9 | 0.75 | 0 |
| target | off | 0.1 | 2.0 | 0.8 | 0.75 | 0 |

- No parameter is at a grid edge except K = 0, which is a natural bound.
- Train DM log likelihood gain over the #38 fit:
  - W10: +62 (carry) and +137 (target)
  - W4: +37 and +107

## McLaurin / Croskey-Merritt: NOT fixed, and the data says why (`depth_force_sensitivity.md`)
- The point-in-time WAS chart before Nov 12 lists McLaurin at **WR7** and Croskey-Merritt at **RB4**.
- Forcing stale charted players back in lowers the training likelihood in every case:
  - carry: −82 (top) and −608 (all)
  - target: −475 (top) and −2641 (all)
- So the fitted rule keeps them out.
- Under force = all (not fitted, sensitivity only), McLaurin would get a 0.051 target share and Croskey-Merritt a 0.226 carry share.
- A real fix needs a signal the committed data does not have, such as an IR-return / practice-report flag. It is left unknown, not guessed.

## Results: see metrics.md (walk-forward W4-9, n=2000, 88 games, same seed as #38)

## Depth effect alone (review item 4)
- `noint/backtest_raw_noint.json`: Phase 2b params with the engine WITHOUT INT pooling. Same 88 games, n=2000, seed 20261113. Section D of metrics.md has the tables.
- The name-locked lines are byte-identical to the #38 run, so the engine stream is unchanged.
- Vs #38:

  | Measure | Change |
  |---|---|
  | RB carries MAE | −0.256 [−0.398, −0.124] |
  | WR targets MAE | −0.111 [−0.143, −0.079] |
  | TE targets MAE | −0.029 [−0.061, +0.003] |
  | QB attempts MAE | +0.021 [−0.017, +0.058] |
  | RB targets MAE | +0.020 [−0.019, +0.059] |
  | Brier, 21 thresholds | 6 fully below 0, 0 above |
  | INT | unchanged (19 zero-P games; Brier 0.302 vs main 0.298) |

- So the INT improvement in the full 2b run comes entirely from INT pooling. The opportunity gains come from the depth signal and grids.

## Zero-INT QB-games left in 2b
- These are QBs the model did not list as candidates. They are not all backups: some started.
- Actual attempts in our PBP count (non-sack pass plays): Kaliakmanis 33 (W4), Bagent 34, McKee 45, Milton 33, Lock 28, Wentz 24, Fagnano 21, Minshew 20, Keenum 19.

## Commit map after the rebase onto main 7364335 (#38 squash; trees identical)
| pre-rebase | after rebase |
|---|---|
| 6de940f | 23d9d84 |
| 2218448 | e2ba0ac |
| 7a0d45b | 94b4c26 |
| 98d3f47 | a9dd394 |
| cbd1450 | 125f64a |
| 2bf54a6 | 3390cd3 |

The backtest_raw.json engine head 2218448 is pre-rebase, so read it through this map.
