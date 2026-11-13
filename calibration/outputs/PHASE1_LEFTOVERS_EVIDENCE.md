# Phase 1 leftovers: residual snaps, goal-line TD over-count, punt rate, reconciliation (refs NFL-75)

Research only, not validated. BACKTEST on already-seen weeks 4-9 (not a clean holdout). Nothing fitted to scores or
lines, no weights changed, projection_ready untouched. **All three fixes are opt-in accounting keys; defaults are
unchanged** (golden hash d18e19271d666c3b, WAS@NYG n=30 seed 20261113, identical to main 3dad900). Tests were written
first (commit f48c2a3, 13 failing), then the engine change (05f5044, ca67748).

Repro tool: `python3 -m calibration.phase1_reconcile --weeks 4-9 --n 200 --workers 5 [--accounting JSON] --tag T`
(88 games, 17,600 sims per arm, seed 4949). It compares the sim with the same two teams' weeks 1..w-1 actual rates,
using the PBP the sim samples from (sha256 1028614b..., pulled 2026-11-12 11:16 AM ET). Outputs:
`phase1_reconcile_{main,round,round_v1,all}_n200.json`, all on a clean engine (cf16d9d / ca67748).

## (a) Residual excess snaps
- **Where:** `core/possession_engine_v0/simulate.py::_clock_cost`, which returns `int(max(3, rng.normal(mu, 4)))`.
- **Observed:** the sim charges less than the as-of mean on every clock event: pass 21.31 vs 21.85 s, run 33.82 vs
  34.34 s, punt 8.98 vs 9.36 s. Snaps per team-game are 63.73 vs 61.25 actual (+2.48).
- **Math:** `int()` truncates toward zero, so E[int(X)] = E[X] - ~0.5 for X ~ N(mu >= 10, 4). With ~140 clock
  events a game that is ~70 s, about 2.3 extra snaps a game. The 3 s floor biases the other way only for mu < ~8
  (FG 4.7 s: +0.5 s).
- **Fix (opt-in):** `accounting.clock_rounding = "round"` rounds to the nearest second. It uses the same single
  normal draw, so the RNG stream is identical.
- **Tests:** `test_truncate_default_is_half_second_short` (characterizes the bug), `test_round_is_unbiased` (|mean - mu|
  < 0.03 over 200k draws), `test_rounding_consumes_identical_rng_stream`, `test_round_keeps_three_second_floor`.
- **After:** pass 21.81 / run 34.31 / punt 9.45 s charged. Snaps 62.59 (+1.34) and drives 11.32 vs 10.53.
  **Remaining +1.3 snaps/team** includes 0.78 kneels per team-game that the sim excludes by design (NFL-49 B), so the
  like-for-like residual is about +0.5 snaps and +0.8 drives.

## (b) Goal-line TD over-count (inside the 3: Ghost6 audit 51.8% sim vs 46.5% actual)
- **Where:** `simulate.py::PlayCatalog.sample_snap`. The snap cell key is (team, down, distance, `empirical.yl_bucket`),
  and "RZ" spans yardline 1-20. A sparse cell falls back to `COARSE_SAME_DOWN`, which is the team's same-down rows
  from **any** field position.
- **Repro / observed** (game context, weeks 4-9): inside-3 TD share is 58.5% sim vs 48.2% actual. Split by the
  yardline the sampled row was actually run from:
  | Source row | Inside-3 snaps / team-game | TD share |
  |---|---|---|
  | run at yardline <= 3 | 0.265 | 42.4% |
  | 4-10 | 0.118 | 64.8% |
  | 11-20 | 0.168 | 59.9% |
  | beyond the 20 (COARSE_SAME_DOWN) | 0.572 | 64.2% |
  Rows really run inside the 3 score at about the actual rate, so **TD crediting is correct**. The over-count comes
  from gains drawn at deeper field positions and applied at the goal line. Example (unit test): NYG 2nd-and-goal at
  the 2 draws 97.7% of its rows from beyond the 5, up to its own 5. Rows resolved by WP2 censoring score 82% but are
  only 0.076 snaps per team-game.
- **Legit boundary vs wrong accounting:** gain capping, TD credit and possession change are correct (rows from <= 3
  match). The defect is pool width and coarsening: field position is dropped before distance. The WP2
  redistribution assumption (gain independent of field position) adds a smaller share.
- **Fix (opt-in):** `accounting.goal_line_pool = "local5"`. At yardline <= 5, draw from the offense's own rows run
  at yardline <= 5 (same down if >= min_n, else any down), otherwise use the unchanged v0 chain. GOAL_LINE_LOCAL_YL = 5
  is a structural boundary, not fitted.
- **Tests:** `test_v0_goal_line_draws_rows_from_deeper_field_positions` (characterizes the bug),
  `test_local5_goal_line_draws_only_goal_line_rows_and_is_deterministic`, `test_goal_line_pool_opt_in_only`, and
  accounting validation.
- **After (all three opt-ins):** inside-3 TD share 54.0% (from 58.5%; actual 48.2%), inside-10 34.8% (from 37.4%;
  actual 32.5%). Rows from beyond the 20 fall from 0.572 to 0.078 inside-3 snaps per team-game. **Remaining:** rows
  run at the 4-5 still score 66% when used at 1-3, and censored-resolved rows 77%. Not fixed here; a tighter local
  band trades off against sample size (min_n).

## (c) Punt rate (+16-18%)
- **Where:** `simulate.py::_fourth_down_decision`, whose cells come from `yl4_bucket`: fg_range <= 35, **mid 36-60**,
  own.
- **Observed:** sim punts 8.97 vs 7.58 actual per game (+18%). By band, the 36-45 decision mix is punt 0.652 / FG
  0.146 / go 0.202 vs actual 0.305 / 0.360 / 0.335. Every other band matches within ~0.05, except a 3% punt share in
  the FG-range bands (team-wide fallback).
- **Math:** one "mid" cell pools a 4th down at the opponent 38 with one at the own 45, so the opponent 36-45 draws the
  punt-heavy 46-60 mix. The rest of the excess comes from extra drives (see a).
- **Fix (opt-in):** `accounting.fourth_down_yl_buckets = "v1_fringe"` adds a 36-45 "fringe" cell (`yl4_bucket_v1`)
  with the same coarsening chain.
- **Tests:** `test_v1_bucket_boundaries`, `test_v0_mixes_own_side_punts_into_opponent_40`,
  `test_v1_fringe_cell_separates_opponent_40`, `test_v1_is_deterministic_for_fixed_seed`.
- **After:** the 36-45 mix is 0.438 / 0.302 / 0.260. Punts are 8.51 per game (+12%) and FGA 1.95 vs 2.06 per team.
  **Remaining:** the extra drives (+0.75/team) and the FG-range team-wide fallback punts.

## (d) Reconciliation, per team-game (sim main -> sim all opt-ins | actual)
| | main | all opt-ins | actual |
|---|---|---|---|
| Snaps (pass+run) | 63.73 | 62.47 | 61.25 (+0.78 kneels not simulated) |
| Possessions with a snap | 11.53 | 11.29 | 10.53 |
| Pass plays / targets | 36.87 / 32.96 | 35.91 / 32.11 | 35.28 / 31.58 |
| Carries | 26.87 | 26.57 | 25.97 |
| Sacks | 2.41 | 2.34 | 2.26 |
| No-play penalties | 5.82 | 5.71 | 5.43 |
| Turnovers | 1.20 | 1.17 | 1.26 |
| Offensive TDs (pass/run) | 2.50 | 2.40 | 2.48 |
| Punts | 4.48 | 4.26 | 3.79 |
| FG attempts | 1.85 | 1.95 | 2.06 |
| Points per game (both teams) | 45.90 | 44.99 | |
Clock budget (main): pass 1,571 + run 1,817 + punt 81 + FG 19 + kickoff 50 = 3,538 s a game via charged events, plus
~128 s of no-play fouls. The excess over 3,600 is the period-end overshoot, which the engine drops.

## Before / after backtest vs the close (weeks 4-9, 88 games, n=500 per game, seed base 20261112, h2h off)
`python3 -m calibration.backtest --n 500 --arms new_off,p1_all --workers 3 --tag phase1` (engine ca67748, clean;
lines ba83615 sha256 matches README). Outputs: `backtest_phase1_n500.json` and `_per_game.csv`.
| Metric | Before (new_off) | After (p1_all) | Close |
|---|---|---|---|
| Brier, home win | 0.2499 | 0.2492 | 0.2055 |
| Log loss | 0.7071 | 0.6993 | |
| Total MAE | 11.40 | 11.39 | 10.33 |
| Margin MAE | 10.60 | 10.76 | 8.98 |
| Total bias (sim - actual) | -0.11 | -0.97 | |
| Corr(sim total, close total) | 0.536 | 0.544 | |
| Corr(sim margin, close margin) | 0.552 | 0.543 | |
| PIT total quartiles | .284/.182/.284/.250 | .250/.216/.261/.273 | |
**Read:** the mechanics move toward the actual rates, but outcome accuracy against the close is unchanged within
noise. Brier and total MAE are slightly better, margin MAE slightly worse, and total bias moves to about -1 point
because there are fewer snaps and drives. The sim stays well behind the close. **Recommendation:** keep all three
opt-in and do not flip defaults until a weeks 10-12 holdout grades them. projection_ready stays false.

## Tests
`core/possession_engine_v0/tests/test_phase1_leftovers.py`: 20 tests. The full possession engine suite passes
(see the PR for the local and CI runs).
