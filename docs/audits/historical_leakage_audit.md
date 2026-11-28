# Historical model validation and calibration: leakage audit

- **Scope:** `GhostPapii21/nfl-matchup-database` at `main` @ `ef4cc690` (Nov 27 2026). Lightning was read from `GhostPapii21/sportsbook-odds-bridge` branch `experiment/nfl-lightning-opportunity-v1` @ `cb61d06`, read only.
- **Written:** Nov 27 2026, ET. This is a read-only audit. No model weights, model code, production code, fitted JSON or data files were changed. The only additions are this report and new test files under `evaluation/tests/` (all new filenames).
- **Not touched:** the missing sim_v6 entrypoint, which belongs to someone else. Nothing in this audit was blocked by it. The vendored `calibration/simv56/engines/cc_sim_v6*.py` files were imported read-only to test their as-of behaviour.
- **No calibration claim is made here.** The only legitimate prospective evidence in the repo is the following:
  - The pristine game-sim protocol: 14 games, Weeks 10-11, status `UNSCORABLE_INSUFFICIENT_COVERAGE` (minimum is 30 games across 3 weeks).
  - The frozen Week 9 Sunday prop boards: DraftKings Brier 0.289, which is worse than a 0.250 coin flip.
  - Neither one shows that any model is calibrated.

## 1. What "simv56", "Main" and "Lightning" mean here
| Name | What it is | Where |
|---|---|---|
| **simv56** | Rush-yards `p_model` = mean of three Monte Carlo engines (sim_v5, sim_v6, sim_v6_fix; each the mean of mc/bias/gr), opp 0.5, n=20,000, plus a QB / availability gate. Feeds the Phase 4 selective-edge study. | `calibration/simv56_pmodel.py`, `calibration/simv56/engines/*`, `calibration/selective_edge*.py`, `backtests/selective_under_alt_2026-11-12/` |
| **Main** | The current board / research model. In the Lightning comparison, "Main" = the frozen Week 9 boards (season_empirical; mean overlay late/SNF). Today's board chances come from the opportunity simulation in `dashboard/opportunity.py`, with its calibration layer, plus the 80-yard watch model. | `research/WEEK9_*`, `dashboard/opportunity.py`, `dashboard/calibration.json`, `dashboard/watch_model.json` |
| **Lightning** | PyTorch Lightning opportunity-count net (targets, rush attempts). Draft PR #32 in sportsbook-odds-bridge, shadow only. | `experiments/nfl_opportunity_lightning.py` (bridge branch); summarised in `data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md` |
| **Historical player-prop evaluations** | The opportunity-sim backtest (2024-26), the calibration-layer fit, the W8-9 FanDuel edge audit, the 80-yard watch-model holdouts, and the dispersion walk-forward. | `dashboard/backtest_opportunity.py`, `research/calibration_2026-11-22/fit.py`, `research/model_audit_2026-11-24/audit.py`, `research/shadow_2026-11-23/`, `market_calibration/backtest_dispersion_wk04_09.py` |

## 2. Leakage-risk report
Ratings: **HIGH** = can materially bias a reported calibration or edge number, or a "holdout" is contaminated. **MED** = look-ahead or survivorship that biases results but is bounded or disclosed. **LOW** = information loss, latent risk or hygiene.

| # | Risk | Rating | Evidence (file:line) | Test |
|---|---|---|---|---|
| R1 | **The board's calibration layer was switched on using its own "holdout".**<br>• Fit is on 2024-25. Each stat is kept or dropped by comparing 2026 Brier.<br>• 2026 is still reported as `holdout_2026`.<br>• 2026 was then reused for the W8-9 edge audit, so 2026 (and any Weeks 10+ rows in the cache at fit time) is a selection set, not a clean holdout, for board chances. | **HIGH** | `research/calibration_2026-11-22/fit.py:48`, `:56`<br>`dashboard/backtest_opportunity.py:219-220`<br>`dashboard/opportunity.py:124`<br>`research/model_audit_2026-11-24/audit.py:30-58` | `test_board_calibration_enable_decision_not_made_on_reported_holdout` (xfail) |
| R2 | **The sim_v6 / sim_v6_fix calibration multipliers are fitted only on players who appeared.**<br>• `backtest_rows` skips any universe player with no play in week W: inactive, DNP or active-but-zero-touch.<br>• simv56 refits its multipliers from those CSVs.<br>• Measured: **219** universe player-markets on teams that played in Weeks 4-7 are missing from `sim_v6_backtest.csv` (219 dropped vs 1,096 kept). | **HIGH** | `calibration/simv56/engines/cc_sim_v6.py:259-260`<br>`cc_sim_v6_fix.py:281`<br>`calibration/simv56_pmodel.py:127-129` | `test_backtest_universe_keeps_zero_stat_and_inactive_players` (xfail) |
| R3 | **Prop backtest filters on game-day active status.**<br>• Only players whose target-week roster status is `ACT` are projected and scored.<br>• Game-day inactives silently leave the population, and no counter records it.<br>• Changing only the target-week status changes who is projected (look-ahead selection, available at T-90 at best). | **MED** | `dashboard/backtest_opportunity.py:82-83`, `:107`, `:135` | `test_inactive_player_is_counted_not_silently_dropped`, `test_target_week_status_does_not_change_who_is_projected` (xfail) |
| R4 | **Position map comes from the whole season's roster.**<br>• Later rows win, so a later position change is applied to earlier weeks.<br>• This changes the league pools, catch-rate and YPR priors, and which rows exist. | **MED** | `dashboard/backtest_opportunity.py:77` | `test_position_map_is_point_in_time` (xfail) |
| R5 | **The 80-yard watch model ships weights fitted on 2022-2026.**<br>• Its `book_grade` (2026 W8-9) says "weights from 2022-2025 only".<br>• `star_record` covers 2025-26.<br>• The model+price blend was chosen on the W8-9 Brier.<br>• The reported numbers cannot be reproduced out-of-sample from the shipped weights. | **MED** | `dashboard/watch_model.json` (`fitted`, `book_grade`, `star_record`)<br>`research/watch_model_2026-11-16/grade_vs_books.py:5` | `test_watch_model_shipped_weights_exclude_its_reported_eval_window` (xfail) |
| R6 | **simv56's depth-chart gate defaults `as_of` to now.**<br>• A historical rerun without `--as-of` uses today's (post-game) depth chart to decide the QB starter. | **MED** | `calibration/simv56_pmodel.py:556`, `:253`, `:258` | `test_historical_run_defaults_as_of_to_kickoff_not_now` (xfail) |
| R7 | **Injury status cannot be verified as-of.**<br>• The committed nflverse injury file has no per-row publication time.<br>• The gates read the whole week's `report_status`.<br>• The opportunity backtest has no injury or teammate-out information at all, so the books knew who was out and the backtest did not (main cause of the W8-9 big-gap misses). | **MED** | `calibration/simv56_pmodel.py:246-248`<br>`calibration/opportunity_fit.py:169-182`<br>`dashboard/backtest_opportunity.py:10`<br>`research/model_audit_2026-11-24/REPORT.md` §1 | `test_injury_rows_carry_publication_timestamp` (xfail) |
| R8 | **Phase 4 training-period p_model is in-sample for the engine's own hyperparameters.**<br>• sim_v6_fix `BIAS_REG/BIAS_WIN/K_BIAS/BIAS_OPP` were tuned on wk4-7 LOWO.<br>• Phase 4 trains its selector on W4-7 using those p_model values.<br>• W4-9 outcomes were already seen and disclosed; p_model is reconstructed walk-forward, not archived pregame.<br>• OOS W8-9 stays clean for this item. | **MED** | `calibration/simv56/engines/cc_sim_v6_fix.py:10-14`<br>`calibration/selective_edge.py:45-47`<br>`backtests/selective_under_alt_2026-11-12/SPEC_FROZEN.md` ("Honest disclosure") | `test_engine_hyperparameters_not_tuned_on_selector_training_weeks`, `test_phase4_p_model_is_archived_pregame_not_reconstructed` (xfail) |
| R9 | **Lightning's validation is retrospective and survivor-only.**<br>• W8 test was seen during the pilot.<br>• W9 "matched props" were built after the games.<br>• Cohort = players in postgame stat records.<br>• Features are rebuilt, not archived.<br>• The loader's `data_as_of_utc < kickoff` check only validates a field the builder writes itself. | **MED** | `LIGHTNING_REPORT.md` §2 "Leakage / validity risks"<br>bridge `experiments/nfl_opportunity_lightning.py:104-106`, `:155-169` | `test_lightning_has_probability_calibration_evidence` (xfail; no probabilities to score) |
| R10 | **Zero-opportunity games are excluded from player histories and from the dispersion fit.**<br>• Engines build a player's volume only from games with a target or carry.<br>• The dispersion `p0` is conditional on at least 1 opportunity.<br>• This inflates volume means and hides zero outcomes. | **MED** | `cc_sim_v5.py:40`<br>`cc_sim_v6.py:64`<br>`cc_sim_v6_fix.py:75`<br>`market_calibration/fit_dispersion_nflverse.py:20-21` | `test_dispersion_player_games_include_zero_opportunity_games` (xfail); engine history: missing test M6 |
| R11 | **simv56 ensemble inner-joins the three engines.**<br>• A leg that errors in one engine silently leaves the population. | **LOW** | `calibration/simv56_pmodel.py:233` | `test_ensemble_inner_join_drops_legs_silently` (pass; documents behaviour) |
| R12 | **Receptions labels are jittered.**<br>• `uniform(-0.5, 0.5)` is added to every receptions *actual* stored in the backtest CSVs. | **LOW** | `cc_sim_v6.py:268`<br>`cc_sim_v6_fix.py:289` | `test_backtest_actuals_are_real_counts` (xfail) |
| R13 | **Player table snapshot (2026-11-02) post-dates the W4-8 cutoffs.**<br>• Used for name-to-gsis disambiguation (`latest_team`) and `position_group`. | **LOW** | `calibration/simv56_pmodel.py:51`<br>`cc_sim_v6.py:41`, `:52-55` | `test_player_table_snapshot_predates_cutoff` (xfail) |
| R14 | **W9 cutoff override drops the completed W8 Monday game.**<br>• Information loss, not leakage. The as-of rule is inconsistent across weeks. | **LOW** | `calibration/simv56_pmodel.py:58` | `test_cutoff_keeps_every_completed_prior_week_game` (xfail) |
| R15 | **`trailing_mean` depends on the caller's sort order.**<br>• Unsorted input makes `shift(1)` read future games. The caller does sort today. | **LOW** | `market_calibration/fit_dispersion_nflverse.py:92`, `:97-101` | `test_trailing_mean_is_order_independent` (xfail) |
| R16 | **Missing probability metrics.**<br>• Opportunity backtest: no log loss.<br>• Selective edge: only hit rate vs break-even; p_model is never scored with Brier or log loss.<br>• Lightning: no probabilities at all. | **LOW / MED** | `dashboard/backtest_opportunity.py:163-181`<br>`calibration/selective_edge*.py` | `test_log_loss_is_reported`, `test_selective_edge_scores_probabilities` (xfail) |

**Checked and found sound** (passing tests guard these):
- **simv56 engines:**
  - The engines see only plays strictly before the cutoff, which is at or before the first kickoff of the week (`cc_sim_v6.py:34`, `cc_sim_v5.py:11`, `simv56_pmodel.py:87-94`, `:560`).
  - Mutating every play on or after the cutoff leaves the simulated distributions, rolling-3 weights and opponent factors bit-identical.
  - The multiplier refit uses backtest weeks `< min(W, 8)` (`simv56_pmodel.py:128`).
  - The QB gate ignores depth snapshots after `as_of` (`:253`).
- **Opportunity backtest:**
  - Team, opponent and player windows use `week < g.week` only (`dashboard/backtest_opportunity.py:89-90`). Inflating future yards, or shutting down the opponent's future defence, does not move target-week projections.
  - Active zero-stat players are kept with actual 0 (`:122-123`).
- **Game backtest:**
  - The game backtest uses history weeks 1..W-1, with a runtime leak guard (`calibration/backtest.py:114`, `core/possession_engine_v0/simulate.py:1339-1340`).
  - Weeks 10 and later are refused (`calibration/backtest.py:217-218`).
  - Brier and log loss are computed correctly.
- **Selective edge:** train, eval and holdout weeks are disjoint and ordered: 4-7, 8-9, 10-12 (`calibration/selective_edge.py:45-47`).
- **Dispersion trailing mean and walk-forward mask:** these exclude the current game and the target week (`fit_dispersion_nflverse.py:101`, `:113-114`).
- **Shared shift-based features** in the research studies (`research/shadow_2026-11-23/study.py:38-44`) sort before `shift().expanding()`.
- **Pristine protocol:** future-only, `historical_pristine_claim=false`, `independently_calibrated=false` (`evaluation/EVALUATION.json`).

## 3. Answers to the eight questions
1. **Train / validation / holdout splits**
   - **simv56 / Phase 4:** train/select on 2026 W4-7, OOS W8-9, live holdout W10-12 (`calibration/selective_edge.py:45-47`; `backtests/selective_under_alt_2026-11-12/SPEC_FROZEN.md`).
     - The engine multipliers are fitted on W4-7 (`sim_v6_backtest.csv`; `sim_v6_fix_backtest.csv` also holds W8 rows, which the `min(W, 8)` rule never uses).
     - The engine hyperparameters were also tuned on W4-7 (R8).
   - **Game sim:** W4-9 is a disclosed "already-seen" backtest; W10+ is the reserved pristine holdout (`calibration/backtest.py:9-10`, `:35`).
   - **Opportunity board:**
     - Volume correction fitted on 2024-25 and checked on 2026 (`dashboard/opportunity.py:38-40`).
     - Calibration layer fitted on 2024-25, with on/off decided on 2026 (R1).
     - `SHARE_CV` is tunable via `--share-cv`; no record shows which seasons tuned it (`dashboard/backtest_opportunity.py:205`, `dashboard/opportunity.py:48`).
   - **Watch model:** fit 2022-24, checked 2025-26, then refit on 2022-26 for shipping (R5).
   - **Dispersion:** walk-forward per week, 2018..2025 plus 2026 W1..w-1.
   - **Lightning:** single week-grouped split, train ≤ W7 / val W8 / test W9; early stopping on val (bridge `:155-169`, `:236-248`).
2. **Game-week timestamps**
   - Respected at week or date granularity: `game_date < cutoff`, `week < W`, and `weeks_inclusive` < target, with a runtime guard in the game engine.
   - Exceptions: the W9 override (R14), and `as_of=now` in the simv56 gate (R6).
   - Opportunity-backtest scripts use the closing `spread_line`, which is only known at kickoff (fine for a kickoff-time projection, not for a T-90 one).
3. **Rolling averages**
   - The engines' `0.6*season + 0.4*last-3` uses only pre-cutoff games, sorted by date (`cc_sim_v6.py:57`, `:82`).
   - The opportunity backtest's last-8 / last-3 shares use `week < g.week`.
   - The dispersion trailing mean uses `shift(1)`.
   - No future leakage was found. Bias comes from excluding zero-opportunity games (R10).
4. **Opponent-adjusted stats**
   - Built only from pre-cutoff plays in the engines (`cc_sim_v6.py:42-51`) and from `dfn.week < g.week` in the opportunity backtest.
   - Verified by mutation tests. No future games are included.
5. **Injuries, depth charts and roles**
   - **Not reconstructed as of the game in the historical prop backtests.** The opportunity backtest has no injury data (R7), uses the game-day `ACT` status (R3) and a season-wide position map (R4).
   - simv56 uses depth snapshots ≤ `as_of` (good), but defaults `as_of` to now (R6). Its injury rows carry no timestamp (R7), and its player table is a Nov 2 snapshot (R13).
   - `opportunity_fit.py` states it uses the weekly report status and no game-day inactives (docstring lines 17-19).
   - Snap counts are not used anywhere point-in-time.
6. **Zero-stat games and inactive players**
   - **simv56 calibration backtest:** dropped (R2).
   - **Opportunity backtest:** active zero-stat players are kept; inactives are dropped (R3).
   - **Dispersion fit:** zero-opportunity games are dropped (R10).
   - **Lightning:** postgame-appearing players only (R9).
   - **Week 9 prospective scorer:** scores verified ACTIVE rows and reports INACTIVE / UNKNOWN separately (`research/evaluate_locked_week9.py:1-6`). This is the correct pattern.
7. **Calibration on actual vs reconstructed predictions**
   - **Actual archived pregame predictions:**
     - The pristine snapshot LOCKs (`evaluation/protocol.py`, `snapshots/score.py`).
     - The frozen W9 board lock (`research/WEEK9_PROSPECTIVE_EVAL_LOCK_20261108_0856ET.json`, `research/evaluate_locked_week9.py`).
     - The selective-edge live grader for W10-12 (`calibration/selective_edge_live.py`).
   - **Reconstructed after the fact:**
     - The Phase 4 W4-9 p_model.
     - Every `dashboard/backtest_opportunity.py` row.
     - The calibration-layer fit.
     - The W8-9 FanDuel edge audit (re-simulated with today's code and calibration).
     - The watch-model holdouts.
     - Lightning.
8. **Brier, log loss, reliability and hit rates**

   | Evaluation | Brier | Log loss | Reliability bins | Hit rate | ECE / CRPS |
   |---|---|---|---|---|---|
   | Pristine game protocol | yes | yes | — | — | CRPS |
   | Game backtest | yes | yes | — | — | — |
   | W9 prospective scorer | yes (3-way) | yes (3-way) | — | — | — |
   | Opportunity backtest | yes | **no** | yes | yes | — |
   | Calibration fit | yes | — | yes | — | — |
   | Dispersion backtest | yes | — | — | — | ECE |
   | Watch model / shadow | yes | yes | — | — | — |
   | Selective edge | **no** | **no** | — | vs break-even only | — |
   | Lightning | none (no probabilities); MAE/RMSE only | — | — | — | — |

## 4. Test results (new suite, run Nov 27 2026, ET)
Command (repo root): `python3 -m pytest -q -p no:cacheprovider evaluation/tests/test_hist_leakage_*.py -rA`

**35 passed, 18 xfailed, 0 failed, 0 errors** (about 11 s, offline, committed data only).
- With `--runxfail`, the 18 xfail tests fail on their real assertions (`18 failed, 35 passed`). That confirms each xfail is a live finding, not a broken test.
- Every xfail is `strict=True`, so a fix turns it into a visible XPASS failure until the marker is removed.

| File | Passed | Xfail (finding) |
|---|---|---|
| `evaluation/tests/test_hist_leakage_simv56.py` | 21 | 6 (R2, R6, R7, R12, R13, R14) |
| `evaluation/tests/test_hist_leakage_prop_backtest.py` | 4 | 4 (R3 x2, R4, R16 log loss) |
| `evaluation/tests/test_hist_leakage_calibration_provenance.py` | 6 | 6 (R1, R5, R8 x2, R16 selective edge, R9) |
| `evaluation/tests/test_hist_leakage_rolling_features.py` | 3 | 2 (R15, R10) |
| `evaluation/tests/hist_leakage_synth.py` | helper only (synthetic league builder) | — |

**Regression check:**
- `evaluation/tests calibration/tests dashboard/tests` together with the new suite gave **348 passed, 3 skipped, 18 xfailed, 1 failed**.
- The 1 failure was already there before this audit: `evaluation/tests/test_readiness.py::test_evidence_boundary_derived_live_from_repo` expects `w12_with_lock == []`, but Week 12 LOCKs for DEN@PIT and KC@BUF are now committed. It fails identically on untouched `main`, so it is a stale assertion, not caused by this audit.

## 5. Failing or missing tests (concrete list)
**Failing now** (xfail strict, real findings). See R1-R16 above for the 18 tests.

**Missing tests that should exist:**
- M1. **Population reconciliation for every historical prop evaluation.** For each (week, team) that played, the count of pregame-eligible players must equal scored + void(inactive) + excluded-with-reason. This applies to `backtest_opportunity`, `cc_sim_v6*.backtest_rows`, `selective_edge` and Lightning.
- M2. **Pregame-archive provenance test.** Every row used as calibration evidence carries a `created_utc` < kickoff and a content hash that matches a committed lock. Reconstructed rows must be labelled `reconstructed=true` and excluded from calibration claims. Today only the pristine protocol and the W9 lock do this.
- M3. **Holdout-use registry test.** A machine-readable ledger of which seasons and weeks each fitted artifact touched (fit, tuning, selection, reporting). Assert that no artifact reports a holdout it touched. This would catch R1, R5 and R8 automatically.
- M4. **Point-in-time roster / depth / injury join.** Given a kickoff time, the joined status must come from a snapshot with `published_utc ≤ kickoff - offset`. This needs timestamped injury and depth archives first (data gap R7).
- M5. **Season-boundary test for the opportunity backtest.** Weeks 1-4 are skipped (`week < 5`). Add a test that the first eligible week of a season never reads the current season's later weeks and that prior-season pools come only from `prev_season`.
- M6. **Engine zero-touch-game history test.** A player active with 0 targets and 0 carries should count as a game in his volume history (`cc_sim_v6.py:64`). This needs a weekly roster joined into the engine.
- M7. **Reliability and log-loss outputs for selective-edge p_model** on W8-9 and W10-12, and for the board calibration layer on prospective weeks only.
- M8. **Lightning** (in sportsbook-odds-bridge): a test that the feature builder's `data_as_of_utc` is the archive time of the inputs, not the builder's run time. Also a full pregame active-player cohort test.
- M9. **Closing-line timing:** tests that any projection labelled T-90 uses a line snapshot taken before T-90, not the closing `spread_line`.
- M10. **`SHARE_CV` / `VOLUME_CAL` tuning provenance:** record and test the seasons used to tune them.

## 6. What would count as legitimate evidence (and the current status)
- **Game sim:** 30 or more pristine LOCKs across 3 or more weeks, scored under the frozen protocol. Currently 14 games in W10-11. The readiness report's ceiling with W12 is 29, so W13 or later is needed.
- **Props:** a prospective, locked, timestamped board scored against verified outcomes, with inactives reported separately. The only one is W9 Sunday: Brier 0.289 (DraftKings), and the 60-80% confidence calls hit about 40%. That evidence points to miscalibration, not calibration.
- Everything else in Sections 2-3 is reconstructed, or contaminated by selection. It is useful for diagnostics but is not calibration evidence.

## 7. Limits of this audit
- `pregame/.cache` (nflverse 2022-25 PBP and weekly rosters used by `dashboard/backtest_opportunity.py` and the watch-model studies) is not committed. Those code paths were tested on a synthetic league rather than rerun on real data, and the exact 2026 weeks present when the calibration layer was fitted could not be verified.
- `statsmodels` is not installed on the audit machine, so `research/calibration_2026-11-22/fit.py` and `research/model_audit_2026-11-24/audit.py` were read, not executed.
- Lightning lives in a different repository. It was read at `cb61d06` and is documented here; no tests were added there.
