# Handoff: edge research (for Codex / ChatGPT / Grok)

You are extending an NFL player-prop model in this repo (`GhostPapii21/nfl-matchup-database`). Do the four tasks below
**in order**, on a new branch `codex/edge-research`, and open a pull request to `main`. Do not edit any existing file outside
`research/edge_2026/` except where a task says so. Python 3.12, pandas, numpy, scipy, statsmodels only.

## What we already know (do not redo)
- Our 80+ yard model (`dashboard/watch.py`, weights `dashboard/watch_model.json`, fit `research/watch_model_2026-11-16/fit.py`)
  is calibrated but only **as accurate as the book**: Brier 0.1136 model vs 0.1136 FanDuel; a logit-average blend 0.1118
  (`research/watch_model_2026-11-16/book_grade.json`). About 55% of 80+ games are not predictable from public data.
- Not predictive (tested): defense explosive rate, yards allowed to lead WRs, individual CB records, missed/broken tackles.
- Predictive: target/yard averages, implied team total, alpha tier (8+ tgt and 70+ ypg), RB yards allowed by defense.

## Data you have
| What | Where | Notes |
|---|---|---|
| Book lines, one file per game | `pregame/direct_lines/<season>_<week>_<AWAY>_<HOME>.json` | `rows`: `{book, event, market, player, side, line, american, break_even}` |
| Pull status per book | `pregame/direct_lines/latest.json` | books: fanduel, pinnacle, draftkings*, betmgm, betrivers, bovada, betonlineag, fanatics (*via StartWho) |
| **Line history** | `git log -p -- pregame/direct_lines/` | Files are overwritten every pull (hourly on game days). Rebuild history by reading each commit's version (`git log --format=%H --` then `git show <sha>:<path>`), timestamp = commit time. |
| Markets | `receptions, receiving_yards, rushing_yards, rush_rec_yards, alt_receiving_yards, alt_rushing_yards, alt_rush_rec_yards, spread, total, moneyline` | alt rows: `line` 79.5 = "80+" |
| Play-by-play, rosters, snaps, Next Gen Stats, participation | nflverse releases (`https://github.com/nflverse/nflverse-data/releases`) | Fit on 2022-2024, test on 2025-2026. No future data in any feature. |
| Results to grade against | nflverse `player_stats` weekly | |

Existing code to reuse: `research/edge_2026/fair_price.py` (`implied`, `devig`, `norm_name`, `game_edges`).

Do **not** scrape DraftKings or Caesars directly or work around their blocks. Use only the files above and nflverse.

## Task 1 - Pinnacle fair price and cross-book edges (`research/edge_2026/fair_price.py`) - DONE
Already built and tested (see `research/edge_2026/README.md`): same-line prices show no 2+ point edge. **Start at Task 3**, then add
the line shift to `fair_price.py` with the Task 3 distribution so the 1,218 different-line prices can be compared.

For each (game, player, market, line) Pinnacle posts both sides of:
```
q_over = 1/dec(over), q_under = 1/dec(under)          # dec = decimal odds from american
p_fair_over = q_over / (q_over + q_under)               # remove the vig (multiplicative)
edge(book, side) = p_fair(side) - break_even(book, side)  # same player, market AND same line only
```
When another book's line differs from Pinnacle's, shift Pinnacle's fair probability with the Task 3 distribution, and flag those rows `line_shifted: true`.
Output `research/edge_2026/edges_latest.json`: list of `{game_id, player, market, book, side, line, american, p_fair, edge, line_shifted}` with edge >= 0.02, sorted by edge.

## Task 2 - Closing line value tracker (`research/edge_2026/clv.py`)
From the line history, for every (book, player, market, side, line) find the first price seen and the last price before
kickoff (kickoff from the nflverse schedule). `clv = break_even(close) - break_even(open)` (positive = the price got worse, so
betting at open beat the close). Also grade every Task 1 edge row against the Pinnacle close: did Pinnacle move toward us?
Output `research/edge_2026/clv.json` with per-row values and a summary: n, mean CLV, share > 0, 95% CI.

## Task 3 - Alt ladder vs main line consistency (`research/edge_2026/ladder.py`)
For each player with a FanDuel main line (receiving or rushing or rush_rec yards) and its alt ladder:
1. Fit a distribution to the main line: yards ~ zero-inflated gamma (or negative binomial on yards/5) with the median =
   main line and the shape fit by position from 2022-2024 history (`shape` = by position and aDOT band).
2. Price each alt rung: `p_dist(rung)`. Compare with the vig-removed ladder price (use the ladder's average overround).
3. Backtest on the weeks we have: Brier of ladder price vs `p_dist` vs average of both.
Output `research/edge_2026/ladder.json`: per rung `{player, market, rung, p_book, p_dist, gap}` plus the backtest.

## Task 4 - Residual model on top of the book (`research/edge_2026/residual.py`)
Logistic regression where the book is an offset (we only fit what the book misses):
```
logit(P_hit) = logit(p_fair_book) + b1*teammate_out_share + b2*(tprr_l4 - tprr_season)
             + b3*route_share_change + b4*explosive_rate_l6 + b5*(our_mean - line)/sd
```
`tprr` = targets per route run (participation data), `route_share` = routes / team dropbacks, `explosive_rate` = share of
targets gaining 20+. Use statsmodels GLM Binomial with `offset=`. Report each b with SE, out-of-sample Brier vs book alone,
and the ROI of "bet when model - break_even >= 0.03" with a bootstrap 95% CI. If no b is significant, say so; that result
is useful too.
Output `research/edge_2026/residual.json` and write the fitted coefficients to `research/edge_2026/residual_model.json`
in the form `{"coef": {...}, "fit_seasons": [...], "test": {...}}`.

## Return format (so it plugs back in)
- All code and JSON under `research/edge_2026/`, plus `research/edge_2026/README.md` with each result in plain words:
  what was tested, the number, and whether it is significant.
- Tests in `research/edge_2026/test_edge.py` (pytest): de-vig math, open/close selection, no future data in features.
- Do not change `dashboard/` or `.github/`; the board wiring will be done afterwards from your JSON outputs.

---

# Phase 2 (start Monday, after Week 11's games are final)

Phase 1 status (merged in #62 and #65): Task 1 works on same-line prices. Task 3's distribution scored **worse than the book**,
so line-shifted edges (`line_shifted: true`) are not trusted. Task 2 had no closed games (n=0). Task 4 was not fit (no
graded props, no route data). Phase 2 fixes those, in this order.

**Rules (same as before, plus one):** branch `codex/edge-research-2`, change only `research/edge_2026/`, and **never commit
`pregame/direct_lines/`** (a bot updates it hourly; old copies overwrite newer data). Before opening the PR, run
`git diff --stat origin/main...HEAD` and confirm every path starts with `research/edge_2026/`. Fit on past seasons, test on
2025-2026, no future data in any feature. If a result is not significant, say so plainly.

## Step A - Grade the saved lines (`research/edge_2026/grade_lines.py`)
1. Rebuild every pregame snapshot of `pregame/direct_lines/*.json` from git history (`git log --format=%H%x09%cI --
   pregame/direct_lines/<file>`, then `git show <sha>:<file>`); keep only snapshots before kickoff (nflverse schedule).
2. Final results: nflverse weekly `player_stats` for 2026 (receptions, receiving_yards, rushing_yards; rush_rec_yards =
   rushing + receiving). Match players by name with `fair_price.norm_name`, plus team, and report the unmatched count.
3. For every (game, book, player, market, line, side) take the **last pregame price** and grade it: win / loss / push
   (whole-number lines).
4. Output `research/edge_2026/graded_lines.parquet` (or .csv) with columns `game_id, book, player, market, line, side,
   american, break_even, first_seen, last_seen, result, actual`; and `graded_summary.json`: hit rate vs average
   break-even by book and market, n, and a 95% CI.
5. Re-run `clv.py` now that games have closed and report n, mean CLV and its CI. Grade the Phase 1 candidates in
   `edges_latest.json` (same-line and line-shifted separately): did they win, and did they beat the close?

## Step B - Fix the yards distribution (`research/edge_2026/ladder.py`)
1. Add the missing 2023 season (`play_by_play_2023.parquet` from nflverse releases). Fit seasons 2022-2024.
2. Calibrate the shape to the books, not only to history: for each FanDuel alt ladder with a matching main line, find
   the shape (per position and aDOT band) that best reproduces the vig-removed ladder probabilities. Compare three
   versions: history-only, book-calibrated, and a blend.
3. Backtest every version on graded results from Step A (Brier and log loss vs the book's own price, with bootstrap CIs).
   Only a version that scores **no worse than the book** may be used for line shifting. Write the chosen one to
   `research/edge_2026/dist_params.json` and make `fair_price.py` read it; with no qualifying version, turn line
   shifting off (`line_shifted` rows excluded) and say so.

## Step C - Model on top of the book price (`research/edge_2026/residual.py`)
1. Training labels: the graded lines from Step A (2026), plus any historical prop odds already in the repo (search
   `research/` and `pregame/` for archived odds; list what was used).
2. Features, all known before kickoff: `teammate_out_share`, `tprr_l4 - tprr_season` and `route_share_change` (nflverse
   participation data; when routes are missing use snap share from nflverse `snap_counts` and say which was used),
   `explosive_rate_l6`, and `(our_mean - line)/sd` from `dashboard/data/*.json` where it exists.
3. Fit the GLM with `offset=logit(p_fair_book)` as specified in Task 4. Report each coefficient with its SE, the
   out-of-sample Brier vs the book alone, and the ROI of "bet when model - break_even >= 0.03" with a bootstrap 95% CI.
   With fewer than 300 graded rows, still fit it, but label the result **too small to judge** and give the n.

## Return
PR to `main` with a plain-words README section per step: what was tested, the number, the CI, significant or not, and
what is ready to show on the board (likely nothing yet; that's fine). Tests in `test_edge.py` for the grading (win,
loss, push), snapshot-before-kickoff selection, and the "no worse than book" gate.

---

# Phase 3 (from the Week 10 model review, `docs/MODEL_REVIEW_2026_W10.md`)

Same rules as Phase 2: branch `codex/model-fixes-3`, never commit `pregame/direct_lines/`, fit on past seasons and test on
2026, say plainly when something is not significant, and confirm with `git diff --stat origin/main...HEAD` that only the
paths named below changed. Run `python -m pytest -q pregame/tests pipeline/tests dashboard/tests grading/tests` before the PR.

## A - Calibration layer for the yardage simulation - DONE (`research/calibration_2026-11-22/README.md`)
The backtest (`dashboard/results/opportunity_backtest.md`, script `dashboard/backtest_opportunity.py`) shows the simulation
low in the middle of the range (12+ carries: said 45-55%, happened 59-67%; WR 40+ yards in 2026: said 30%, happened 34%)
and high at the top for 100+ yards (said 34-44%, happened 22-26%).
1. For each (stat, threshold) in the backtest, fit an isotonic or Platt calibration of simulated probability -> actual
   hit rate on 2024-2025 only. Save as `dashboard/calibration.json`.
2. Apply it to every threshold probability the board shows (`opportunity.py` outputs and `watch.py` p80/p100).
3. Re-run the backtest on 2026 with and without calibration; report Brier and the calibration table for both. Keep the
   layer only if 2026 Brier improves; otherwise leave the file in place but switched off, and say so.

## B - Use the new advanced data - DONE, not wired in (`research/advanced_inputs_2026/README.md`); labels fixed
`pregame/sources.py` now downloads NGS receiving/rushing/passing and PFR weekly receiving/rushing.
1. Build per-player features as of before each game (no future weeks): NGS average separation, cushion, YAC over
   expected, share of team intended air yards; PFR drops, broken tackles, yards after contact per attempt; NGS rush
   yards over expected per attempt.
2. Test each as a multiplier on top of the current projection, the same way as
   `research/context_effects_2026-11-22/test_context.py` (Poisson GLM with offset log(projection), fit 2022-2024, test
   2025-2026). Report multiplier, CI and test deviance.
3. Wire into `opportunity.py` only the features that are significant and improve 2025-2026 deviance.
4. Also replace the "Hard Rock Bet / Caesars" bettable-book labels in `pregame/render.py` and `pregame/odds.py` text with
   the gate's required books (`pipeline.hooks.REQUIRED_BOOKS`).

## C - Losing-streak factor (research only until it holds up) - scheduled re-test after Week 14
`research/context_effects_2026-11-22` found receivers on teams with 2+ straight losses gain about 5% fewer yards than
projected (CI 0.912-0.988). Re-test after Week 14 with 2026 Weeks 11-14 as the test set. Add it to the projection only
if it is still significant on that new data.
