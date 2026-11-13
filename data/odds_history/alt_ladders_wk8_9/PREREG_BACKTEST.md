# Pre-registration: FanDuel alt-ladder (over) backtest, 2026 Weeks 8-9

Written 2026-11-13 ~11:17 AM ET, **before any Week 8-9 rung was graded**, and committed in the same commit as the raw pull
(the scoring script lands in a later commit). Research only, not validated, not a pick list. `projection_ready` stays false.
No engine, weight or production change. Refs NFL-75.

## Data
- Prices: FanDuel `player_rush_yds_alternate`, `player_reception_yds_alternate`, Odds API historical snapshot ~T-90 min
  (this folder `raw/` for 26 games + PR #41 `data/odds_history/alt_test_week9/raw/` for DAL@IND, JAX@BAL, BUF@MIN).
  FanDuel posts **over rungs only** (no alt unders). Pinnacle posts no alts, so there is no sharp fair price per rung.
- Actuals and history: nflverse 2026 play-by-play / roster_weekly / snap_counts (box cache retrieved 2026-11-13 15:15Z).
  Yards = rushing_yards (+ lateral_rushing_yards) and receiving_yards (+ lateral_receiving_yards), two-point tries excluded.

## Grading
- Win if actual >= rung (rungs are x.5, no pushes). Break-even = 1/decimal price (vig included; no no-vig possible one-sided).
- Flat 1u stake; ROI = profit / plays. Player with 0 offensive snaps in the game -> void (excluded, counted).
  Player name not matched to the roster of either team -> unknown (excluded, counted). No invented numbers.
- Hit-rate CI: Wilson 95%. Rungs per player-game are highly correlated (one game decides the whole ladder), so every
  table also reports the number of distinct player-games, and n is NOT the number of independent observations.

## Bands
- Relative: rung / trailing mean, trailing mean = player's 2026 per-game average of that stat over games played
  (offense snaps > 0) in weeks **before** the graded week. Bands: <=50%, 50-75%, 75-100%, >100%, no prior games.
- Absolute (yards): rush <=9.5, 10-24.5, 25-49.5, 50-74.5, 75-99.5, >=100; receiving <=19.5, 20-39.5, 40-59.5,
  60-79.5, 80-99.5, >=100.

## "Rico floor" subset (gates from prior weeks only, fixed here, not tuned on Weeks 8-9)
- Rush: RB (roster position) passing the frozen G-RB rule from `backtests/selective_under_alt_2026-11-12/SPEC_FROZEN.md`:
  team carry share >= 60% in >= 3 of the player's last 4 games played (prior weeks only; <3 prior games = fail),
  AND rung <= trailing mean.
- Receiving: WR/TE with "stable target share" = team target share >= 15% in >= 3 of the last 4 games played (prior weeks
  only; <3 prior games = fail), AND rung <= trailing mean.
  **Disclosure:** no frozen WR/TE target-share gate existed before today; this 15%-in-3-of-4 rule is defined now, mirroring
  the RB rule's structure, before grading, and will not be changed after seeing results.
- Weeks 8-9 are not a clean holdout for game outcomes (they were used in earlier studies; see SPEC_FROZEN.md disclosure),
  but no alt-ladder prices from FanDuel were ever graded before this study.
