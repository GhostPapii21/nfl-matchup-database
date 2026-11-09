# Week 9 Sunday forecast scorecard and calibration review · November 8, 2026 ET

This is a prospective audit of the frozen Madrid and 1 p.m. boards, using CBS player boxes for games marked final by the score feed. [All forecast rows and outcomes](WEEK9_SUNDAY_FORECAST_GRADES_20261108.csv) · [Sunday results board](WEEK9_SUNDAY_PROJECTION_RESULTS_BOARD_20261108.md) · [Frozen Madrid simulation](week9_930/simulation_100k_20261108_0908ET.csv) · [Frozen 1 p.m. simulation](week9_1pm_live/WEEK9_1PM_100K_SIMULATIONS.csv).

## Results

A model call is the side with the larger frozen raw over/under probability at that exact book line. Equal probabilities abstain; exact-line outcomes push. Games with unresolved scoring scope and unmatched players stay out of denominators. These are directional grades of board forecasts, not a bet slip, closing-line value or ROI. Report each book and model separately; their forecasts overlap. DraftKings is the headline reference so the same props are not counted twice across books.

| Window | Book | Model | Hits | Misses | Hit rate | Raw Brier |
|---|---|---|---:|---:|---:|---:|
| 1PM | DraftKings | season_empirical | 87 | 94 | 48.1% | 0.295 |
| 1PM | DraftKings | rolling5_empirical | 85 | 96 | 47.0% | 0.322 |
| 1PM | DraftKings | opponent_shrunk_rolling5 | 80 | 101 | 44.2% | 0.326 |
| 1PM | FanDuel | season_empirical | 86 | 94 | 47.8% | 0.296 |
| 1PM | FanDuel | rolling5_empirical | 83 | 97 | 46.1% | 0.326 |
| 1PM | FanDuel | opponent_shrunk_rolling5 | 80 | 100 | 44.4% | 0.330 |
| Madrid | DraftKings | season_empirical | 17 | 14 | 54.8% | 0.257 |
| Madrid | DraftKings | rolling5_empirical | 15 | 16 | 48.4% | 0.302 |
| Madrid | DraftKings | opponent_shrunk_rolling5 | 14 | 17 | 45.2% | 0.318 |
| Madrid | FanDuel | season_empirical | 13 | 17 | 43.3% | 0.280 |
| Madrid | FanDuel | rolling5_empirical | 13 | 17 | 43.3% | 0.314 |
| Madrid | FanDuel | opponent_shrunk_rolling5 | 13 | 17 | 43.3% | 0.324 |
| Combined | DraftKings | season_empirical | 104 | 108 | 49.1% | 0.289 |
| Combined | DraftKings | rolling5_empirical | 100 | 112 | 47.2% | 0.319 |
| Combined | DraftKings | opponent_shrunk_rolling5 | 94 | 118 | 44.3% | 0.325 |
| Combined | FanDuel | season_empirical | 99 | 111 | 47.1% | 0.294 |
| Combined | FanDuel | rolling5_empirical | 96 | 114 | 45.7% | 0.325 |
| Combined | FanDuel | opponent_shrunk_rolling5 | 93 | 117 | 44.3% | 0.330 |

The CSV contains 1,482 model/book rows. The combined DraftKings baseline grades 212, with 28 Cleveland–New Orleans rows held for regulation vs. overtime and eight outcomes unmatched. The combined FanDuel baseline grades 210 with the same hold counts. Late games and Sunday night are not in these denominators; late boxes and pregame probability data still need reconciliation. No ticket settlement is inferred.

## Reliability and board decision

Season empirical led both alternatives on hit rate and Brier on both books. On the matched DraftKings observations where the already frozen historical correction was applied (100 baseline rows), Brier improved from 0.297 to 0.274. On the parallel FanDuel subset (99 rows), it improved from 0.291 to 0.269. Both are above the 0.250 Brier from assigning 50% to every binary outcome. Books share outcomes and these comparisons do not supply independent replication. Historical diagnostics used fixed present-day thresholds, so the correction stays research-only.

| DraftKings baseline call confidence | Calls | Hits | Average stated confidence | Actual hit rate |
|---|---:|---:|---:|---:|
| 50–<60% | 91 | 50 | 54.7% | 54.9% |
| 60–<70% | 48 | 19 | 64.4% | 39.6% |
| 70–<80% | 47 | 19 | 73.1% | 40.4% |
| 80–100% | 26 | 16 | 90.3% | 61.5% |

Use season empirical as the comparison baseline in this report. Keep rolling five and opponent adjustment as challengers, and raw confidence labeled uncalibrated. A new correction fitted to this slate cannot be evaluated on the same outcomes. Require historical timestamped book thresholds, regulation/OT reconciliation, and a later untouched slate before promoting a new calibration.

## Equation verification

Recomputed the marginal Madrid equations from the locked Weeks 1–8 input and compared the resulting means with the matched official-score game box. Receiving uses targets per game × Jeffreys-smoothed catch rate × yards per reception. Passing uses attempts per game × completion rate × yards per completion. Rushing uses carries per game × yards per carry. The pregame equation artifact was a separate decomposition. The 1 p.m. run used historical outcome bootstraps and a capped team-level allowance factor for the opponent challenger. No evidence in the frozen 1 p.m. export that man/zone, shell, defender responsibility, pressure-at-decision or scramble triggers were used in those projections.

| Madrid market | Matched | Equation mean absolute error | Season bootstrap mean absolute error |
|---|---:|---:|---:|
| passing_yards | 2 | 41.40 | 41.61 |
| passing_tds | 2 | 0.32 | 0.32 |
| rushing_yards | 5 | 17.00 | 16.98 |
| pass_completions | 1 | 3.86 | 3.85 |
| receiving_yards | 10 | 27.72 | 27.74 |
| receptions | 10 | 1.20 | 1.19 |
| rushing_attempts | 1 | 0.25 | 0.26 |

Madrid examples: Burrow passing 302.1 projected vs. 271 actual, Chase receiving 70.0 vs. 155, Higgins receiving 103.2 vs. 32, and Robinson rushing 97.5 vs. 100. Similar aggregate errors are expected because the marginal products mostly reconstruct the historical average. The large Chase/Higgins reversal is a player-level allocation miss; it does not identify whether coverage, target share or per-target efficiency drove the shift without further charting. [Frozen equation inputs and audit](week9_930/CALIBRATION_EQUATION_AUDIT.md) · [Madrid CBS box](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_CIN%40ATL/).

The newer [Green Bay CBS snapshot](https://www.cbssports.com/nfl/gametracker/playbyplay/NFL_20261108_GB%40NE/) had Watson at 171 and Golden at 164 receiving yards. Those updated observations are separate from the scored sample and from the earlier 132/154 snapshot. Against the archived DraftKings means of 86.07 and 74.52, those are provisional errors of +84.93 and +89.48 yards respectively.
