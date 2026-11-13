# FROZEN SPEC — selective under / alt signal backtest (NFL, 2026 Weeks 4-9)

Frozen: **2026-11-12 18:26 EST (2026-11-12T23:26Z)**, written before any flag in this study was scored against an outcome.
Research only, not validated. Not a pick list. Never sets `projection_ready`. Refs NFL-75.
Goal (Rico, Nov 12 6:21 / 6:23 PM ET): stop trying to beat the market on every line; judge the model by whether the plays it
FLAGS (strong unders, alt rungs) beat the break-even of their real price.

## Honest disclosure of prior exposure (not a clean holdout)
- Weeks 3-8 prop outcomes were already used in prior studies (vig_median_nflverse_2026-11-03: rush unders were the only edge,
  517 legs 288-229; calibration.md bins). Weeks 4-9 game outcomes were used in PR #21. Weeks 4-9 are therefore **already-seen**.
- While inventorying for this spec the author saw the PR #21 per-game aggregate (new_off arm mean sim total 44.9 vs mean actual 46.0).
- Weeks 10-12 are the only clean live holdout.

## Inputs (box-local; book prices are NOT committed to this public repo — only scripts, hashes and aggregates)
| id | file | sha256 | notes |
|---|---|---|---|
| PROPS | /workspace/nfl-database/backtests/confidence_check_2026-11-03/legs_with_probs.csv | 3a945f3c…69a2 | main-line player props, one single-book two-sided price per leg, snapshot ~34 min pre-kick, walk-forward sim probs (sim_v5/sim_v6/sim_v6_fix, opp 0.5/1.0), nflverse actuals |
| INV | /workspace/research/historical_nfl_odds_inventory_2026-11-07/sportsbook_observations.csv | d59d7cc9…0b65 | named-book observations Wk3-9; ONLY `pregame_status=verified_capture_before_start` and snapshot < kickoff used |
| GAMES | calibration/outputs/backtest_wk04_09_n2000_per_game.csv (this repo, PR #21) | in repo | walk-forward game sims (arm `new_off`): sim_total, sim_total_sd, sim_margin, sim_margin_sd, actuals |
| PBP | data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet (this repo) | in repo | carry shares, prior weeks only |
| BETLOG | /workspace/bet-log.csv | hashed at run time | Rico's actual NFL slips (slip comparison only) |
Odds API: **0 credits** (saved prices only).

## Universe
- Weeks 4-9 2026 REG. Week 3 excluded. **Passing yards excluded everywhere** (Rico rule).
- Prop markets: rushyds, recyds, rec (receptions; Wk6+ only), rushrec. Game markets: full-game totals, spreads; team totals
  (no saved main team-total lines / no team-points SD -> expected UNKNOWN, reported as such, not zero).
- Splits: TRAIN/SELECT = Weeks 4-7. OUT-OF-SAMPLE = Weeks 8-9 (never used for selection or tuning). LIVE = Weeks 10-12.

## Model probability (pre-chosen, no alternatives scored as primary)
- Props: `p_model_over` = mean of `sim_v5|0.5`, `sim_v6|0.5`, `sim_v6_fix|0.5` (each already the mean of mc/bias/gr modes).
  `p_model_under = 1 - p_model_over`. Alt rungs: the same three engines are re-run (same leak-free cutoffs, same code as
  confidence_check run_sims.py, read-only engine copies outside this repo) with `rungs=[main + alt rungs]`, P(X >= rung).
- Games: Normal(sim_total, sim_total_sd) and Normal(sim_margin, sim_margin_sd) from arm `new_off` (Normal approximation is an
  assumption, declared). Integer lines: P(push) = P(|X - L| < 0.5); win/lose probabilities exclude push.
- The core engine and its weights are not changed.

## Prices and no-vig
- Props main line: the leg's single book over/under price in PROPS. No-vig = multiplicative.
- Games main line: per book, latest verified pre-kick two-sided quote from INV (`spreads`/`totals`). Main line = modal line
  across books (ties -> line closest to the median). No-vig = mean across books of multiplicative no-vig at that line.
  Graded price = best price for the flagged side across books at that line. Weeks 4-5 have no named-book game quotes -> UNKNOWN.
- Alts (one-sided, real prices only): per book, latest verified pre-kick quote per player/market/rung from INV
  (`*_alternate`, `alternate_totals`, `alternate_spreads`, `alternate_team_totals`); graded price = best across books.
  Break-even = 1/decimal (with vig; no no-vig exists for a one-sided rung, so this is the stricter bar).
- Grading: win pays (decimal-1), loss -1, push 0 (refund). ROI = profit / plays.

## Flag rules (control). X grid pre-registered = {+3, +5, +8} percentage points. All three reported.
**U (strong under):** flag main-line UNDER if `p_model_under - p_nv_under >= X` and gates pass.
  Spreads: flag the side (either) whose `p_model_cover - p_nv_cover >= X` (spreads have no under; reported as "spread side").
**A (alt):** for a prop/game with main line L and alt rungs r (real price), EV_r = p_model(r)*dec_r - 1;
  EV_main = max EV of the two main sides. Flag the single best-EV rung if `EV_r > EV_main` AND `p_model(r) - 1/dec_r >= X`
  and gates pass. One alt flag per player-market (or game-market).
**Gates:**
  - G-RB 60% carry rule: rushyds/rushrec props on RBs require team carry share >= 60% in >= 3 of the player's last 4 games
    played (prior weeks only, from PBP). Fewer than 3 prior games -> fail (unknown is not a pass).
  - G-REC verified main defender: not available historically -> receiving flags are reported as **UNGATED (defender unknown)**,
    a separate line that cannot count toward readiness until verified live.
  - No passing yards.
Primary headline = X = +5 with gates. +3 and +8 reported alongside.

## Statistics
- Per market and side: n, wins-losses-pushes, hit rate, mean break-even of the graded price, margin (hit - BE), ROI,
  mean no-vig (where two-sided). 95% CI by bootstrap resampling games (game_id clusters), 10,000 reps, seed 0.
- **n < 30 is flagged "too small to trust"** in every table.
- Walk-forward only: every model input uses data before the game's week.

## "Strong markets" (selected on Weeks 4-7 ONLY, then frozen and scored on 8-9)
A market x side x rule (X=+5, gated) is "strong" if on Weeks 4-7: n >= 30, ROI > 0 and margin (hit - BE) > 0.
The list is written to `strong_markets_wk4_7.json` and committed BEFORE Weeks 8-9 are scored. No re-picking.

## Selector (trained layer, Rico 6:23 PM ET)
- Candidates: every main-line under (props, totals), every spread side, every alt rung with a real price, gates applied.
- Features: edge (p_model - p_nv, or - BE for alts), market one-hot, side, rung offset ((rung-main)/max(main,1)),
  model skew proxy (sim mean - median)/line where available, carry share (RB), team spread, price break-even.
  Weather: UNKNOWN for this study (not joined) — omitted, not zero.
- Model: L2 logistic regression (C = 0.5, standardized on train), target = win (pushes dropped from training).
  Train on Weeks 4-7 only. Select if `p_hat - BE >= 0.03` (fixed, not tuned). Frozen to `selector_frozen.json`
  (coefficients + scaler) and committed BEFORE scoring Weeks 8-9.
- Reported: selector vs control (X=+5 gated) on Weeks 8-9, per market, with in-sample Wk4-7 side by side.

## Slip study (scored on Weeks 8-9 ONLY)
- From Weeks 8-9 control flags (X=+5 gated) in strong markets only (as frozen above), per week build 2-, 3- and 4-leg
  cross-game slips: legs ranked by margin (p_model - BE), greedy, one leg per game, top-k. Price = product of decimals
  (cross-game; no SGP correlation pricing). Also all disjoint combinations reported as count only if feasible.
- Compare with Rico's actual NFL slips in BETLOG: ticket cash rate and ROI for Weeks 8-9 (primary) and Weeks 4-9 (reference),
  ticket stake/payout parsed from the log text; tickets with unparseable stake/odds are UNKNOWN and listed.

## Pass bar (for this study; not readiness)
Selective signal "beats its price" in a market only if OOS Weeks 8-9 margin > 0 with CI lower bound > 0 and n >= 30.
Otherwise: "not shown" (INSUFFICIENT or FAIL). Proposed NFL-75 criterion is written in REPORT.md and judged on Weeks 10-12.
