# FanDuel alt-over ladders vs actuals, 2026 Weeks 8-9 — research only, not validated

Not a pick list. `projection_ready` stays false. No engine or weight changes. Rules were fixed in `../PREREG_BACKTEST.md`
(committed with the raw data, before the scoring commit). Refs NFL-75.

**Headline metric is flat 1u ROI, and the pre-registered decorrelated check is one rung per player-game.**
Unweighted margin (hit rate minus mean break-even) can have the **opposite sign** of ROI when prices vary, so a cell
is never described as beating the price when ROI is negative.

**Sample:** 29 games (all of Weeks 8-9), 5,206 FanDuel over rungs pulled, **5,138 graded** across **445 player-games**
(rush 1,531 rungs / 172 player-games; receiving 3,607 / 362). Excluded: 68 rungs void (8 players with 0 offensive snaps).
A name-matching bug fix graded 9 receiving rungs that were previously unmatched (FanDuel listed "Joshua Palmer" on
BAL@BUF; the weekly roster is "Josh Palmer"). All 9 were losses (0 rec yards, 7 offensive snaps). Pre-registered
grading rules are unchanged. Pinnacle has no alts, so break-even is FanDuel's own vig-included price (the strict bar).

**Confidence intervals:** one game settles a whole ladder, so rungs are not independent. Margin (hit − mean BE) and
ROI use a **cluster bootstrap over player-games** (and, as a sensitivity, over games): `numpy.random.default_rng`
seed **20261113**, **10,000** reps, percentile 95% (`nanquantile`, linear). Independent-rung Wilson 95% CIs on hit
rate are too narrow except on the one-rung table, where n already equals the number of player-games. Full column
layout is in `tables.md`.

## Headline: Rico-floor, one rung per player-game

For each gated player-game, the single floor rung closest to 75% of the player's trailing mean (prior weeks only).

| market | n (player-games) | hit | avg BE | margin (pts) | ROI | player-game cluster 95% CI (ROI) | player-game cluster 95% CI (margin, pts) |
|---|---|---|---|---|---|---|---|
| rush | 21 | 13/21 = 61.9% | 63.0% | -1.1 | -11.0% | [-41.4%, +18.6%] | [-19.0, +15.5] |
| rec | 99 | 62/99 = 62.6% | 65.8% | -3.2 | -5.8% | [-20.7%, +8.7%] | [-12.5, +5.8] |

Both point estimates are below break-even on ROI. Both player-game cluster CIs (and the game-clustered ones: rush
ROI [-35.8%, +13.9%], rec [-22.5%, +10.2%]) include zero, so this is not a tight loss — and it is not an edge.
Wilson hit-rate CIs, which are valid here because one observation equals one player-game, already include break-even
(rush 40.9–79.2% vs 63.0%; rec 52.8–71.5% vs 65.8%). The Joshua Palmer name-match did not change this table (he
failed the WR/TE 15% target-share gate, so he is not in the Rico-floor subset).

## Main takeaways

1. **Floor alt overs do not beat FanDuel's singles price as a point estimate.** The one-rung Rico-floor check is
   slightly under break-even (rush ROI -11.0%, rec -5.8%). All-rungs Rico-floor ROI is about -6% on both markets,
   even though all-rungs Rico-floor rush has an unweighted margin of **+1.1 pts**. That is not a plus-EV result:
   wins landed on short prices (mean BE 75.8%, mean decimal 1.39) and losses on longer ones (mean BE 47.1%, mean
   decimal 2.70). ROI for that cell is **-6.1%**, and its player-game cluster 95% CI is [-27.2%, +17.5%].
2. **The full ladder loses after clustering.** Overall rush 36.1% vs 41.9% BE, ROI **-20.8%**, player-game cluster
   95% **[-35.7%, -4.9%]**; receiving 37.6% vs 42.1% BE, ROI **-17.7%**, **[-28.1%, -6.9%]**. Game-clustered
   intervals also exclude zero (rush [-34.4%, -6.4%], rec [-28.4%, -5.8%]). FanDuel's alt-over prices carry roughly
   4–6 points of hold on average.
3. **Safer floors are the least-bad, not profitable.** Rungs at <=50% of the player's trailing mean: rush 77.0% vs
   82.7% BE, ROI -7.4%, player-game cluster 95% [-16.2%, +1.8%]; rec 76.3% vs 81.1% BE, ROI -6.0%, [-12.3%, +0.1%].
   Both intervals include or graze zero. Long rungs (>100% of trailing mean) are a clear loss (rush ROI -26.1%,
   [-46.7%, -4.0%]; rec -25.3%, [-40.5%, -9.2%]).
4. **Week split is consistent in sign.** Receiving Wk8 ROI -21.1% / Wk9 -14.4%; rush -18.8% / -22.7%. Tiny cells
   with a positive margin or ROI (Rico-floor rush Wk9: 9 player-games, ROI +6.9%, cluster CI [-20.8%, +37.7%];
   rush "no prior games": 2 player-games, ROI +24.8%) are too small to read as an edge. SGP (parlay) pricing was
   not tested; this is a singles-price result only.

## Overall (all rungs)

| market | rungs | player-games | hit | avg BE | margin (pts) | ROI | player-game cluster 95% CI (ROI) |
|---|---|---|---|---|---|---|---|
| rush | 1531 | 172 | 36.1% | 41.9% | -5.8 | -20.8% | [-35.7%, -4.9%] |
| rec | 3607 | 362 | 37.6% | 42.1% | -4.4 | -17.7% | [-28.1%, -6.9%] |

Independent-rung Wilson hit-rate CIs (too narrow): rush 33.8–38.6%; rec 36.1–39.2%.

## By rung / trailing mean (prior weeks only)

| market | band | rungs | player-games | hit | avg BE | margin (pts) | ROI | player-game cluster 95% CI (ROI) |
|---|---|---|---|---|---|---|---|---|
| rush | <=50% | 196 | 119 | 77.0% | 82.7% | -5.7 | -7.4% | [-16.2%, +1.8%] |
| rush | 50-75% | 193 | 123 | 61.7% | 71.6% | -10.0 | -16.1% | [-28.0%, -4.3%] |
| rush | 75-100% | 174 | 131 | 46.0% | 54.4% | -8.5 | -18.0% | [-35.7%, +0.5%] |
| rush | >100% | 945 | 169 | 20.2% | 25.0% | -4.8 | -26.1% | [-46.7%, -4.0%] |
| rec | <=50% | 653 | 312 | 76.3% | 81.1% | -4.8 | -6.0% | [-12.3%, +0.1%] |
| rec | 50-75% | 470 | 309 | 61.3% | 66.3% | -5.0 | -7.4% | [-16.1%, +1.1%] |
| rec | 75-100% | 376 | 304 | 47.1% | 51.3% | -4.2 | -7.3% | [-19.7%, +5.4%] |
| rec | >100% | 2089 | 360 | 18.6% | 22.8% | -4.3 | -25.3% | [-40.5%, -9.2%] |

(no-prior-games: rush 23 rungs / rec 19 rungs, 2 player-games each — too small. The rush cell's +24.8% ROI has a
player-game cluster 95% CI of [-64.0%, +162.9%].)

## Rico floor, all rungs (not the headline)

RB 60% carry gate / WR-TE 15% target-share gate, rung <= trailing mean. **Do not read the rush +1.1 pt margin as
beating the price**; ROI is -6.1%.

| market | band | rungs | player-games | hit | avg BE | margin (pts) | ROI | player-game cluster 95% CI (ROI) |
|---|---|---|---|---|---|---|---|---|
| rush | all (<=100%) | 117 | 21 | 67.5% | 66.4% | +1.1 | -6.1% | [-27.2%, +17.5%] |
| rush | <=50% | 30 | 15 | 83.3% | 83.6% | -0.2 | -2.9% | [-25.9%, +18.4%] |
| rush | 50-75% | 42 | 20 | 76.2% | 72.0% | +4.1 | -2.6% | [-25.2%, +18.3%] |
| rush | 75-100% | 45 | 21 | 48.9% | 49.8% | -0.9 | -11.6% | [-49.4%, +30.2%] |
| rec | all (<=100%) | 527 | 99 | 69.8% | 74.2% | -4.3 | -5.6% | [-16.6%, +5.4%] |
| rec | <=50% | 201 | 89 | 84.1% | 87.4% | -3.3 | -3.9% | [-13.6%, +4.7%] |
| rec | 50-75% | 184 | 99 | 67.9% | 73.8% | -5.9 | -7.9% | [-20.3%, +4.6%] |
| rec | 75-100% | 142 | 97 | 52.1% | 55.8% | -3.7 | -4.8% | [-25.1%, +15.3%] |

On the full rush ladder, rungs passing the 60% carry gate hit 48.2% (ROI -5.8%, 222 rungs) versus 34.1%
for rungs that fail it (ROI -23.3%, 1,309 rungs); both are negative-ROI. The gate does **not** lift hit rate on
RB floor rungs: Rico-floor rush is 67.5% versus 68.6% for RB floors that fail the gate, and both have ROI -6.1%.
On WR/TE floors the gate lifts hit rate (69.8% vs 64.8% for WR/TE floors that fail it) but also raises break-even
(74.2% vs 67.3%), and ROI is worse (-5.6% vs -3.8%). Prices already absorb any selection.

Absolute-yard bands, per-week splits, game-clustered intervals, and gated >100% rungs: see `tables.md`. Every row:
`graded_rungs.csv`.

## Notes and deviations

- **Name-matching bug fix (not a grading-rule change):** the matcher is exact on `full_name` or `football_name +
  last_name` after punctuation/`Jr` strip. It now falls back to a Joshua ↔ Josh first-name alias only when that
  exact match is empty, and still requires a unique `gsis_id`. The only alias hit was Joshua Palmer → Josh Palmer
  (`00-0036988`, BUF WR, BAL@BUF). Effect vs the pre-fix tables: +9 receiving rungs, all losses; graded sample
  5,129 → 5,138 rungs and 444 → 445 player-games. Overall receiving moved from 37.7% / ROI -17.5% to 37.6% /
  ROI -17.7%. Rico-floor and one-rung headline tables are unchanged (Palmer failed the 15% target-share gate).
- Void rule (pre-registered): 0 offensive snaps = void. Roschon Johnson (TB@CHI Wk9) had 0 offensive but 7
  special-teams snaps; FanDuel would likely settle his rungs as losses, not voids. Effect: a handful of rush/rec
  rungs; direction would make results slightly worse, not better.
- Actuals spot-checked against the committed ESPN box for BAL@BUF Wk8 (Henry 53, Cook 80, Bateman 22: match).
  Palmer's 0 rec yards / 7 offensive snaps also match that game's nflverse snap chart and pbp.
- Inputs: nflverse cache retrieved 2026-11-13 10:15:54 AM ET (`2026-11-13T15:15:54Z`). sha256 pins (also in
  `meta.json`): `play_by_play_2026.parquet` `d3a9d3e2873dffc4bf27ba482894d87a4d8324af14ae1d3fbfaa294a87f96fd2`;
  `roster_weekly_2026.parquet` `b5d7cbd68ec7280391010349f284364c1d6a27ee8683d481566fa962a2d3c77c`;
  `snap_counts_2026.parquet` `1d2e15675f9a3bc9eba04c1197a7650be7957b8f2fbb657c8df80d40c25e1f03`. Source URLs:
  `https://github.com/nflverse/nflverse-data/releases/download/{pbp,weekly_rosters,snap_counts}/...`. Week 9
  DAL@IND / JAX@BAL / BUF@MIN prices read from PR #41 (sha256 in `meta.json`). Reproduce:
  `python grade_alt_ladders.py --nflverse <dir> --wk9-pr41-raw <PR41 raw dir>`.
- Weeks 8-9 game outcomes were seen in earlier studies (see SPEC_FROZEN.md disclosure); these FanDuel alt prices
  were not. This is not a clean outcome holdout.
- The WR/TE 15% target-share gate was defined the day of the original scoring (before grading); no prior frozen
  WR/TE gate existed.
- Caveat: there is no sharp (Pinnacle) fair price per rung; cluster-aware CIs on the Rico-floor subset include
  zero; SGP pricing and profit boosts were not tested.
