# Week 9 probability calibration and equation audit

**As of:** 2026-11-08 09:24 ET. The 09:08 pregame forecast and its 100k simulation are unchanged. This separate update uses the same pregame Weeks 1–8 source extract and all recorded zero-opportunity rows as a sensitivity.

## What was calibrated

Historical prop lines are not in the repository. I therefore used each current DK line as a fixed threshold on earlier Weeks 5–8 outcomes, generating strictly prior-only probabilities for every test week. The correction was fitted on Weeks 5–6 and evaluated on untouched Weeks 7–8. It is pooled across the 31 DK player-market lines because per-market samples are too small. A correction is applied to the Week 9 estimate only if its slope remains positive and it improves both Brier score and log loss on W7–8.

This is a threshold-specific forward diagnostic, not a backtest of the historical sportsbook market. Today’s lines are being applied to past games. Player/week observations overlap, the evaluation spans only four weeks, and the current line does not reflect each past game’s true market line.

## Walk-forward scores (Week 7–8 untouched)

| Sample definition | Probability model | W5–6 fit n | W7–8 test n | Active-opportunity test n | Raw Brier | Calibrated Brier | Raw log loss | Calibrated log loss | Platt slope | Applied? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| all_recorded_games | season | 46 | 60 | 60 | 0.259 | 0.252 | 0.712 | 0.696 | 0.000 | No |
| all_recorded_games | recent5 | 46 | 60 | 60 | 0.271 | 0.252 | 0.739 | 0.696 | 0.000 | No |
| positive_opportunity_only | season | 44 | 60 | 60 | 0.260 | 0.250 | 0.713 | 0.694 | 0.000 | No |
| positive_opportunity_only | recent5 | 44 | 60 | 60 | 0.271 | 0.250 | 0.739 | 0.694 | 0.000 | No |

If the fitted slope is zero, the calibrator collapses to a single pool-level rate and cannot distinguish player props; the procedure refuses to apply it as a player-specific probability. See the score table and CSV rather than treating such a constant as a pick signal.

## Equations used

For receivers, the available marginal form is `E[receptions/game] = E[targets/game] × P(catch | target)` and `E[receiving yards/game] = E[targets/game] × P(catch | target) × E[yards | catch]`. The expected target count uses all recorded team-game rows, including zero-target rows; catch rate uses the Jeffreys Beta(0.5, 0.5) estimate. For quarterbacks, `E[completions] = E[attempts] × completion rate`, `E[passing yards] = E[attempts] × completion rate × yards/completion`, and `E[pass TD] = E[attempts] × TD/attempt`. For backs, `E[rush yards] = E[carries] × yards/carry`. Per-player factors and denominators are in `EQUATION_COMPONENTS_20261108_0924ET.csv`.

These are marginal accounting decompositions; the current data has no exhaustive coverage context c, routes per dropback, charted defender assignment, target depth, play-level explosive catches, pressure-at-decision label, or designed-run/scramble split. Therefore it cannot fit the full explosive-completion equation, coverage adjustment, or scramble-trigger equation. Yardage probabilities still use observed player-game joint outcomes; no catch-level explosiveness is fabricated.

## Probability files

`PROBABILITY_CALIBRATION_20261108_0924ET.csv` reports DK and FD line-specific Jeffreys-smoothed rates, 90% intervals, and both scopes: all recorded games (zero opportunities included) and positive-opportunity-only (conditional role sample). Today’s inactives were checked, but the historical input does not distinguish inactive games from an active player receiving zero opportunities. The two scopes bracket that uncertainty. Re-run with `python run_probability_calibration.py`.
