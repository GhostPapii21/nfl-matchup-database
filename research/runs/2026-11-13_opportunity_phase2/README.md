# NFL-75 Phase 2: player opportunity model (opt-in, research only)

Rico's Nov 13 12:25 AM repair spec, Phase 2. This is research only and not validated. projection_ready stays false. No Odds API pulls and no paid credits were used. Weeks 10-12 were never read for scoring.

## What it is
- `core/possession_engine_v0/opportunity.py` is a second recorder. It only observes; it never changes the game. It runs on the same snaps as the name-locked `player_box` recorder from main (#36).
- It is opt-in through `simulate.simulate_games(..., opportunity_model=<frozen dict>)`. When that argument is left out, the output is byte-identical to main 6bc0c54. With it on, every block that already existed is still byte-identical, including games, the yard ledger and the name-locked box. The model only adds `player_box_opportunity`.
- It draws all its randomness from its own RNG stream (seed from the run seed plus SALT). It never touches the engine's RNG.
- Each sampled opportunity is re-attributed to the point-in-time roster in one of three slots:
  - **dropback:** pass attempts, sacks, QB scrambles and QB runs, kneels and spikes. Each trial draws one starter from a fitted starter mixture.
  - **carry:** every other run.
  - **target:** pass rows that had a receiver.
- Players marked Out on the weekly injury report get availability 0. Questionable and Doubtful players play with a fitted probability. The share of a player who sits is redistributed by the documented `redistribute(alpha)` rule, with alpha fitted. Game-to-game role noise is a Dirichlet draw with fitted kappa.
- Inside each slot, the player for a snap is drawn with probability proportional to pi_p × L_p(feature cell). L_p is the player's empirical-Bayes distribution over feature cells (zone × depth or yards bucket × result), shrunk toward his position prior with fitted strength m. Any listed player can therefore record an INT or TD; a player's own history no longer caps him.
- Team totals do not change. In every trial the opportunity team ledger equals the name-locked team ledger (check `team_ledger_eq_name_locked`, plus the #36 checks that don't refer to names).

## Fit, freeze, score (walk-forward)
- `calibration/opportunity_fit.py` fits on 2024 and 2025 regular seasons plus 2026 weeks before the eval week only. Guards and tests raise an error if the eval week or anything later is read. Parameters for each week are frozen in `params/params_2026_wNN.json` before scoring.
- `calibration/opportunity_backtest.py` covers 2026 Weeks 4-9: 88 games, n=2000 per game, h2h off, history weeks 1..w-1. One engine run per game feeds both recorders. Weeks 10 and later are refused.
- `calibration/opportunity_report.py` writes `metrics.md` / `metrics.json`. CIs are a game-cluster bootstrap with 2000 resamples.

Fitted parameters per eval week:

| eval wk | dropback (starter mixture) | carry | target | EB m (db/carry/tgt) | P(play) Q / D |
|---|---|---|---|---|---|
| 4 | lam 0.5, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.064 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.070 | lam 0.8, gamma 1.0, K 0, alpha 0.5, kappa 40.0, u 0.095 | 500/1000/500 | 0.66 (n=376) / 0.02 (n=58) |
| 5 | lam 0.5, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.063 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.070 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 20.0, u 0.094 | 1000/2000/200 | 0.66 (n=384) / 0.02 (n=58) |
| 6 | lam 0.35, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.062 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.070 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 20.0, u 0.095 | 200/5000/200 | 0.66 (n=400) / 0.02 (n=58) |
| 7 | lam 0.35, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.061 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.070 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 20.0, u 0.095 | 200/1000/200 | 0.67 (n=414) / 0.02 (n=58) |
| 8 | lam 0.35, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.059 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.072 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 20.0, u 0.095 | 1000/5000/1000 | 0.67 (n=421) / 0.02 (n=58) |
| 9 | lam 0.35, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.059 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.072 | lam 0.8, gamma 1.0, K 0, alpha 0.5, kappa 40.0, u 0.095 | 1000/5000/200 | 0.67 (n=431) / 0.02 (n=58) |
| 10 (WAS@NYG model only, never scored) | lam 0.35, K 0, gamma 1.0, beta_last 0.0, beta_dc 2.0, rho 0.975, u 0.060 | lam 0.8, gamma 0.75, K 0, alpha 0.5, kappa 5.0, u 0.072 | lam 0.8, gamma 1.0, K 0, alpha 0.5, kappa 40.0, u 0.096 | 1000/2000/200 | 0.66 (n=442) / 0.02 (n=59) |

Several values sit on a grid edge: K=0, beta_last=0, and m at 1000-5000 in some weeks. Each params file records its `at_grid_edge` flags.

## Data (sha256 is verified on every fit)
- **2026 PBP:** committed file `pbp_2026_w1_9_pulled_20261112T1116ET.parquet`, sha 1028614b...
- **2024 PBP:** committed file, sha 3fd2896b...
- **2025 PBP:** not committed. Read from /tmp/nflverse_pbp, sha c6ecedd6..., retrieved 2026-11-13T05:25:07Z.
- **Injuries:**
  - 2024 (new file under `data/historical/nflverse/injuries/`, sha 7ebabbba..., retrieved 2026-11-13T07:17:03Z)
  - 2025 (existing committed file, sha c7637c2f...)
  - 2026 (new file, sha a72cc1af..., retrieved 2026-11-13T05:26:36Z)
- **players.parquet:** not committed, sha 4f885ccf.... Only the position field is used.
- **Depth-chart QB1 snapshots 2025-2026:** a derived table, documented in `data/historical/nflverse/derived_pit/README.md`. It uses the latest snapshot before 04:00 UTC on game day.
- **Point in time:** availability is the weekly report status only. Game-day inactives are not used.
- **Snaps:** unknown. There is no snap model, and nflverse snap counts in the repo stop at Week 7.

## Holdout freeze (Weeks 10-12)
`holdout_freeze_manifest.json` records model commit b6e955c and the sha256 of the model code
(opportunity.py, player_box.py, simulate.py, state.py, opportunity_fit/backtest/report.py) and of the frozen params
for Weeks 10-12 (all = the Week-10 fit on data through 2026 Week 9). `calibration/opportunity_holdout_grade.py`
calls `opportunity_freeze.check_freeze(week)` before touching any actual and refuses if the manifest is absent or
any hash differs; any model change (e.g. the follow-up depth-signal PR) must be re-frozen and committed before
Week 10-12 actuals are read. Holdout grading itself is not implemented or run here. W10 TNF had already been played
at freeze time; its actuals were never read.

## Research guard
`opportunity_model` runs only through `simulate_games(opportunity_model=...)` with n <= 20,000; a config key
`opportunity_model`/`opportunity` is refused by simulate_games and by `snapshots/lock.run_sim` (the 100k path);
the output block is labelled UNACCEPTED_RESEARCH_ONLY.

## Provenance gaps (labelled, not fixed)
- `injuries_2026_pulled_20261113T0526Z.parquet` was retrieved 2026-11-13T05:26:36Z = **00:26 AM ET Nov 13, after the
  Nov 12 TNF kickoff**, and nflverse gives **no publication time** for its rows: publication time UNKNOWN. Its Week 10
  rows feed the WAS@NYG sanity model (WAS Out: C.Yankoff, and a non-skill player); pregame publication is assumed,
  not proven. For W4-9 the statuses are the weekly report; check (Ghost6 review, re-verified by me): 0 of 148 W4-9
  QB/RB/WR/TE Out rows and 0 of 5 Doubtful rows recorded any opportunity that week.
- Positions come from the **current** nflverse `players.parquet` (retrieved 2026-11-13), not a point-in-time
  roster; position changes during the season are not reflected.
- `games.csv` (game day only) is now sha-pinned: c606cb6cdf94d6a1c1e939e23ed524223dc7aeaa01a4e2982b0cb5db42bae017
  (committed d9779a1, 2026-11-11 10:07 AM ET; contains no W10+ scores).
- 2025 PBP and players.parquet are not committed (sha256-pinned, read from NFLVERSE_PBP_DIR).

## Results
See `metrics.md` (walk-forward Weeks 4-9) and `sanity_was_nyg_n20000.md` (WAS@NYG, projection only). Every figure in
`metrics.md` is produced by `python3 -m calibration.opportunity_report` from `backtest_raw.json` (including the
Brier summary and the zero-INT table).
- Brier: **10 of 21** thresholds have a 95% CI fully below 0, none fully above 0, all 21 point estimates <= 0
  (an earlier chat summary said 11; that was wrong, metrics.json `brier_summary` is the source).
- Zero-INT QB-games (178 with >= 10 actual attempts): 30 (main) -> 19 (opportunity); 9 of the 19 are QBs who were
  not candidates, 10 are starters whose team pool had no INT row before the eval week (engine-level cap).
  INT Brier is slightly worse (0.3016 vs 0.2982): do not price INT props from this model.

## Reproduce
```
python3 -m calibration.opportunity_backtest --weeks 4 5 6 7 8 9 --n 2000 --workers 6   # reuses frozen params/
python3 -m calibration.opportunity_report
python3 -m calibration.opportunity_fixtures
python3 research/runs/2026-11-13_opportunity_phase2/run_sanity_was_nyg.py
```
