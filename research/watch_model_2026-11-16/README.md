# 80-yard watch model (Nov 16, 2026)

`fit.py` fits one logistic model per player type on 2022 to 2026 games, with every factor in it so the data sets the
weights, and writes `dashboard/watch_model.json`. Weights are from all seasons; the calibration tables in the json come
from weights fitted on 2022-24 and tested on 2025-26.

| Receivers (8,070 games) | Odds of 80+ per standard deviation | z |
| --- | --- | --- |
| Targets (blend) | +123% | 7.0 |
| Yards a game | +118% | 6.3 |
| Team implied total | +16% | 3.5 |
| His team's pass volume | -10% | -2.6 |
| Defense's rate of 20+ yard completions allowed | +2% | 0.4 |
| 80+ games the defense has allowed to his position | +8% | 1.9 |

Held-out calibration (80+ by fifths): predicted 0.8 / 2.6 / 6.2 / 13.9 / 32.1%, happened 0.4 / 4.2 / 4.7 / 13.6 / 27.4%.
Ranking accuracy 0.802. For backs (1,855 games; carries, yards per carry, spread, team total, RB yards allowed; accuracy
0.65): predicted 12 / 20 / 27 / 34 / 48%, happened 18 / 20 / 27 / 37 / 47%.

Not in the weights, because they did not predict: the defense's big-play rate, yards allowed to other lead receivers,
missed and broken tackles, and individual cornerback records (see `coverage_db_2026-11-16` and `game_types_2026-11-16`).
The team's last-five passing form is shown as context; as a standalone factor it was weaker than implied total and volume.

## Track record of the stars (2025-26, weights fitted on 2022-24 only)

| Stars | Players a week | Predicted | Hit 80+ | Hit 100+ |
| --- | --- | --- | --- | --- |
| ★★★ (50%+) | 3.7 | 55.8% | 51.2% | 31.7% |
| ★★ (40-50%) | 5.6 | 43.9% | 43.1% | 29.3% |
| ★ (30-40%) | 11.3 | 34.3% | 34.5% | 19.3% |
| All stars | 20.6 | | 39.9% | |

The stars caught 45% of the 399 receiving and rushing 80-yard games in those 22 weeks. The other 55% came from players
rated under 30%, which is the ceiling of a pregame model with public data. Not graded against prices.

## Graded against FanDuel's real prices (`grade_vs_books.py`)

Data: the FanDuel alt-over ladders pulled 90 minutes before kickoff for 2026 weeks 8 and 9
(`data/odds_history/alt_ladders_wk8_9`, 5,138 graded rungs). The 79.5 and 99.5 rungs are the 80+ and 100+ yard markets.
Weights fitted on 2022-2025 only. 402 rungs matched a model row (receiving 80+: 172 of 192; 100+: 135 of 141; rushing
80+: 50 of 86; 100+: 45 of 68; the players with no row hit 0 to 3%).

| Rung | Rungs | Book break-even | Hit | Model | Brier: model / price |
| --- | --- | --- | --- | --- | --- |
| Receiving 80+ | 172 | 22.2% | 16.9% | 18.1% | 0.1209 / 0.1219 |
| Receiving 100+ | 135 | 15.9% | 9.6% | 11.5% | 0.0753 / 0.0761 |
| Rushing 80+ | 50 | 34.5% | 28.0% | 30.5% | 0.1605 / 0.1596 |
| Rushing 100+ | 45 | 23.1% | 22.2% | 19.2% | 0.1482 / 0.1429 |

- **The model is as accurate as FanDuel's price** (pooled Brier 0.1136 for both). Prices include the vig, so the book's
  break-even runs 3 to 6 points above how often these rungs hit.
- **Does the model add anything the price lacks?** Regressing the result on both: receiving model coefficient 0.16
  (z 0.3) against 0.97 for the price (z 1.8); rushing about 1.1 for each (z about 1). It does not, within noise.
- **Betting where the model beats the price by 3+ points lost:** 35 rungs, ROI -47%. The model's higher numbers there were
  not borne out, as they are mostly long shots.
- **Starred players (30%+ model chance):** 68 rungs, hit 50% against a 46.8% price, ROI +8.7%. Not distinguishable from
  zero at that sample (two weeks, clustered by game).
- **An even blend of the model and the de-vigged price** (leave-one-week-out) scored 0.1118 against 0.1136 for either
  alone: 1.6% better, within noise. `dashboard/watch.py: blend_with_book` implements it for use when a price exists.

Read: no edge over the book has been shown, and two weeks of ladders cannot show one. Weeks 10 and later need prices
pulled before kickoff (about 20 credits a game for the alt ladders).
