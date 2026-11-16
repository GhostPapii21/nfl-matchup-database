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
