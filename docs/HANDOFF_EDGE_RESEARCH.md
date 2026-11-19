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

Do **not** scrape DraftKings or Caesars directly or work around their blocks. Use only the files above and nflverse.

## Task 1 - Pinnacle fair price and cross-book edges (`research/edge_2026/fair_price.py`)
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
