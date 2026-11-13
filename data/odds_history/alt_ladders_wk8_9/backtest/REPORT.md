# FanDuel alt-over ladders vs actuals, 2026 Weeks 8-9 — research only, not validated

Not a pick list. `projection_ready` stays false. No engine or weight changes. Rules were fixed in `../PREREG_BACKTEST.md`
(committed with the raw data, before this scoring commit). Refs NFL-75.

**Sample:** 29 games (all of Weeks 8-9), 5,206 FanDuel over rungs pulled, **5,129 graded** across **444 player-games**
(rush 1,531 rungs / 172 player-games; receiving 3,598 / 361). Excluded: 68 rungs void (8 players with 0 offensive snaps),
9 rungs unknown (Joshua Palmer, BAL@BUF, no roster name match). Pinnacle has no alts, so break-even is FanDuel's own
vig-included price (the strict bar). Hit-rate CI = Wilson 95%.

**Correlation caveat:** each player-game decides its whole ladder, so rungs are NOT independent. Read `n_player_games`
as the real sample; Wilson CIs on rungs are too narrow. A one-rung-per-player-game check is included.

## Main takeaways
1. **Every band is below break-even.** Overall: rush hit 36.1% vs 41.9% break-even (ROI -20.8%), receiving 37.7% vs 42.1%
   (ROI -17.5%). FanDuel's alt-over prices carry roughly 4-6 points of hold at every rung distance.
2. **Floor rungs are the least-bad, not profitable.** Rungs at <=50% of the player's trailing mean hit 77.0% (rush) and
   76.5% (rec), but break-even there is 82.7% / 81.1% (ROI -7.4% / -5.7%). Long rungs (>100% of trailing mean, >=60 yds)
   are the worst (ROI -25% to -56%).
3. **"Rico floor" subset (RB 60% carry gate / WR-TE 15% target-share gate, rung <= trailing mean):** rush 67.5% vs 66.4%
   BE (+1.1 pts margin, ROI -6.1%, **only 21 player-games**); receiving 69.8% vs 74.2% (-4.3 pts, ROI -5.6%, 99 player-games).
   One rung per player-game (closest to 75% of trailing mean): rush 13/21 = 61.9% vs 63.0% BE; rec 62/99 = 62.6% vs 65.8%.
   The gate lifts hit rate but FanDuel prices that in. **No signal that alt-over floors beat their price.**
4. Week split is consistent (rec Wk8 -5.9 / Wk9 -2.9 pts; rush -5.5 / -6.1). The only positive cells are tiny
   (Rico-floor rush Wk9: 9 player-games; rush 50-75% band: 20 player-games) and are noise-level.

## Overall
| market | rungs | player-games | hit | 95% CI | avg BE | margin | ROI |
|---|---|---|---|---|---|---|---|
| rush | 1531 | 172 | 36.1% | 33.8-38.6 | 41.9% | -5.8 | -20.8% |
| rec | 3598 | 361 | 37.7% | 36.2-39.3 | 42.1% | -4.4 | -17.5% |

## By rung / trailing mean (prior weeks only)
| market | band | rungs | player-games | hit | 95% CI | avg BE | margin | ROI |
|---|---|---|---|---|---|---|---|---|
| rush | <=50% | 196 | 119 | 77.0% | 70.7-82.4 | 82.7% | -5.7 | -7.4% |
| rush | 50-75% | 193 | 123 | 61.7% | 54.6-68.2 | 71.6% | -10.0 | -16.1% |
| rush | 75-100% | 174 | 131 | 46.0% | 38.7-53.4 | 54.4% | -8.5 | -18.0% |
| rush | >100% | 945 | 169 | 20.2% | 17.8-22.9 | 25.0% | -4.8 | -26.1% |
| rec | <=50% | 651 | 311 | 76.5% | 73.1-79.6 | 81.1% | -4.6 | -5.7% |
| rec | 50-75% | 469 | 308 | 61.4% | 56.9-65.7 | 66.3% | -4.9 | -7.2% |
| rec | 75-100% | 375 | 303 | 47.2% | 42.2-52.3 | 51.3% | -4.1 | -7.1% |
| rec | >100% | 2084 | 359 | 18.6% | 17.0-20.3 | 22.9% | -4.2 | -25.1% |
(no-prior-games: rush 23 rungs / rec 19 rungs, 2 player-games each — too small.)

## Rico floor subset
| market | band | rungs | player-games | hit | 95% CI | avg BE | margin | ROI |
|---|---|---|---|---|---|---|---|---|
| rush | all (<=100%) | 117 | 21 | 67.5% | 58.6-75.3 | 66.4% | +1.1 | -6.1% |
| rush | <=50% | 30 | 15 | 83.3% | 66.4-92.7 | 83.6% | -0.2 | -2.9% |
| rush | 50-75% | 42 | 20 | 76.2% | 61.5-86.5 | 72.0% | +4.1 | -2.6% |
| rush | 75-100% | 45 | 21 | 48.9% | 35.0-63.0 | 49.8% | -0.9 | -11.6% |
| rec | all (<=100%) | 527 | 99 | 69.8% | 65.8-73.6 | 74.2% | -4.3 | -5.6% |
| rec | <=50% | 201 | 89 | 84.1% | 78.4-88.5 | 87.4% | -3.3 | -3.9% |
| rec | 50-75% | 184 | 99 | 67.9% | 60.9-74.3 | 73.8% | -5.9 | -7.9% |
| rec | 75-100% | 142 | 97 | 52.1% | 43.9-60.2 | 55.8% | -3.7 | -4.8% |

Absolute-yard bands, per-week splits and gated >100% rungs: see `tables.md`. Every row: `graded_rungs.csv`.

## Notes and deviations
- Void rule (pre-registered): 0 offensive snaps = void. Roschon Johnson (TB@CHI Wk9) had 0 offensive but 7 special-teams
  snaps; FanDuel would likely settle his rungs as losses, not voids. Effect: a handful of rush/rec rungs; direction would make
  results slightly worse, not better.
- Actuals spot-checked against the committed ESPN box for BAL@BUF Wk8 (Henry 53, Cook 80, Bateman 22: match).
- Inputs: nflverse box cache retrieved 2026-11-13 15:15Z; Week 9 DAL@IND/JAX@BAL/BUF@MIN prices read from PR #41
  branch (sha256 in `meta.json`). Reproduce: `python grade_alt_ladders.py --nflverse <dir> --wk9-pr41-raw <PR41 raw dir>`.
- Weeks 8-9 game outcomes were seen in earlier studies (see SPEC_FROZEN.md disclosure); these FanDuel alt prices were not.
- The WR/TE 15% target-share gate was defined today (before grading); no prior frozen WR/TE gate existed.
