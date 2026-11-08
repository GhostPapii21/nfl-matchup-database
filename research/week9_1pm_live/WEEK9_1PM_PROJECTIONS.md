# NFL Week 9 1 PM ET refreshed projections and simulations

Captured 2026-11-08T12:56:12-05:00 (board as-of 2026-11-08T17:56:11.028Z). Scope: the seven 1 PM ET games.

Source lines: current DraftKings and FanDuel quotes from Fieldwork's market API, with per-book source/receipt/expiry timestamps. The page states it aggregates DK, FD, BetMGM and BetRivers; it uses the median of eligible standard lines. It is not a direct sportsbook connection.

Quotes: 453; simulation rows: 1299; 100,000 draws per quote/model. Input SHA-256: `c768007d68abf564c8e445cfda380012b5cb0c65d20081659a7b912bc82c2720`; simulation SHA-256: `42080db294858418c7cd201a559635bc2d52c09654bab544b0be3613ac561684`.

## Calibration status

Calibration remains **false**. This run tests a pooled Platt correction on Weeks 5-6 and holds out Weeks 7-8, using today's prices as fixed thresholds because historical book lines are unavailable. It applies only to market/model pairs with at least 30 fit and 30 test events, positive slope, and improved Brier and log loss. Passing pairs receive a separate `calibration_probability`; other pairs retain the raw probability. These tests are diagnostics, not a true historical-line calibration backtest.

## Model definitions
*Diagnostic-adjusted values are shown only for market/model pairs that passed the fixed-threshold diagnostic; they are sensitivity outputs, not accepted calibrated hit probabilities.*

- Season empirical: bootstrap verified same-team Week 1-8 outcomes with positive opportunities, retaining zero-stat outcomes.
- Rolling five: same using the latest five eligible games.
- Opponent-shrunk rolling five: last-five outcomes multiplied by a capped opponent allowed-rate factor using existing team-level data; experimental only.

The chance columns are raw bootstrap frequencies. Calibration outputs are separately labeled and not promoted as calibrated hit probabilities.

## Current lines and projections

Values below summarize current DK/FD quotes by median line. These projections come from Weeks 1-8 recorded player-game outcomes; use the downloadable CSV for each book and the three separate model distributions.

| Player | Opp | Market | Current median line | Model | Mean | Raw over | Diagnostic-adjusted over* | Raw under | Eligible games |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| Amon-Ra St. Brown | MIA | receiving_yards | 78 | opponent_shrunk_rolling5 | 72.4 | 20.0% | — | 80.0% | 7 |
| Amon-Ra St. Brown | MIA | receiving_yards | 78 | rolling5_empirical | 72.6 | 20.2% | — | 79.8% | 7 |
| Amon-Ra St. Brown | MIA | receiving_yards | 78 | season_empirical | 81.5 | 28.6% | — | 71.4% | 7 |
| Amon-Ra St. Brown | MIA | receptions | 6.5 | opponent_shrunk_rolling5 | 6.8 | 59.9% | — | 40.1% | 7 |
| Amon-Ra St. Brown | MIA | receptions | 6.5 | rolling5_empirical | 6.8 | 60.0% | 58.3% | 40.0% | 7 |
| Amon-Ra St. Brown | MIA | receptions | 6.5 | season_empirical | 7.6 | 71.1% | 61.7% | 28.9% | 7 |
| CeeDee Lamb | IND | receiving_yards | 92.5 | opponent_shrunk_rolling5 | 79.9 | 20.1% | — | 79.9% | 8 |
| CeeDee Lamb | IND | receiving_yards | 92.5 | rolling5_empirical | 80.1 | 20.0% | — | 80.0% | 8 |
| CeeDee Lamb | IND | receiving_yards | 92.5 | season_empirical | 88.6 | 37.5% | — | 62.5% | 8 |
| CeeDee Lamb | IND | receptions | 7.5 | opponent_shrunk_rolling5 | 6.8 | 40.1% | — | 59.9% | 8 |
| CeeDee Lamb | IND | receptions | 7.5 | rolling5_empirical | 8.0 | 40.0% | 52.8% | 60.0% | 8 |
| CeeDee Lamb | IND | receptions | 7.5 | season_empirical | 7.5 | 37.8% | 52.1% | 62.2% | 8 |
| Chris Olave | CLE | receiving_yards | 75 | opponent_shrunk_rolling5 | 72.1 | 39.8% | — | 60.2% | 7 |
| Chris Olave | CLE | receiving_yards | 75 | rolling5_empirical | 73.7 | 40.0% | — | 60.0% | 7 |
| Chris Olave | CLE | receiving_yards | 75 | season_empirical | 90.8 | 57.2% | — | 42.8% | 7 |
| Chris Olave | CLE | receptions | 5.5 | opponent_shrunk_rolling5 | 5.8 | 60.2% | — | 39.8% | 7 |
| Chris Olave | CLE | receptions | 5.5 | rolling5_empirical | 6.2 | 59.9% | 58.3% | 40.1% | 7 |
| Chris Olave | CLE | receptions | 5.5 | season_empirical | 7.0 | 71.4% | 61.7% | 28.6% | 7 |
| Chuba Hubbard | DEN | receiving_yards | 18 | opponent_shrunk_rolling5 | 20.4 | 60.0% | — | 40.0% | 7 |
| Chuba Hubbard | DEN | receiving_yards | 18 | rolling5_empirical | 20.2 | 60.0% | — | 40.0% | 7 |
| Chuba Hubbard | DEN | receiving_yards | 18 | season_empirical | 21.4 | 57.0% | — | 43.0% | 7 |
| Chuba Hubbard | DEN | receptions | 2.5 | opponent_shrunk_rolling5 | 3.4 | 59.9% | — | 40.1% | 7 |
| Chuba Hubbard | DEN | receptions | 2.5 | rolling5_empirical | 3.4 | 60.0% | 58.3% | 40.0% | 7 |
| Chuba Hubbard | DEN | receptions | 2.5 | season_empirical | 3.1 | 57.1% | 57.5% | 42.9% | 7 |
| Chuba Hubbard | DEN | rushing_yards | 69 | opponent_shrunk_rolling5 | 92.2 | 80.0% | — | 20.0% | 7 |
| Chuba Hubbard | DEN | rushing_yards | 69 | rolling5_empirical | 87.6 | 79.9% | 63.6% | 20.1% | 7 |
| Chuba Hubbard | DEN | rushing_yards | 69 | season_empirical | 77.1 | 57.0% | 43.5% | 43.0% | 7 |
| Dak Prescott | IND | passing_yards | 263.5 | opponent_shrunk_rolling5 | 260.0 | 40.0% | — | 60.0% | 8 |
| Dak Prescott | IND | passing_yards | 263.5 | rolling5_empirical | 263.1 | 39.9% | — | 60.1% | 8 |
| Dak Prescott | IND | passing_yards | 263.5 | season_empirical | 255.7 | 50.1% | — | 49.9% | 8 |
| Dak Prescott | IND | rushing_yards | 6 | opponent_shrunk_rolling5 | 12.8 | 100.0% | — | 0.0% | 7 |
| Dak Prescott | IND | rushing_yards | 6 | rolling5_empirical | 12.2 | 100.0% | 100.0% | 0.0% | 7 |
| Dak Prescott | IND | rushing_yards | 6 | season_empirical | 14.4 | 100.0% | 100.0% | 0.0% | 7 |
| Dallas Goedert | NYG | receiving_yards | 36 | opponent_shrunk_rolling5 | 34.6 | 50.0% | — | 50.0% | 6 |
| Dallas Goedert | NYG | receiving_yards | 36 | rolling5_empirical | 36.2 | 59.9% | — | 40.1% | 6 |
| Dallas Goedert | NYG | receiving_yards | 36 | season_empirical | 43.0 | 66.7% | — | 33.3% | 6 |
| Dallas Goedert | NYG | receptions | 3.5 | opponent_shrunk_rolling5 | 4.4 | 80.1% | — | 19.9% | 6 |
| Dallas Goedert | NYG | receptions | 3.5 | rolling5_empirical | 4.4 | 79.9% | 64.8% | 20.1% | 6 |
| Dallas Goedert | NYG | receptions | 3.5 | season_empirical | 4.3 | 83.3% | 66.2% | 16.7% | 6 |
| Harold Fannin Jr. | NO | receiving_yards | 46 | opponent_shrunk_rolling5 | 58.1 | 39.9% | — | 60.1% | 8 |
| Harold Fannin Jr. | NO | receiving_yards | 46 | rolling5_empirical | 56.9 | 40.0% | — | 60.0% | 8 |
| Harold Fannin Jr. | NO | receiving_yards | 46 | season_empirical | 51.4 | 50.1% | — | 49.9% | 8 |
| Harold Fannin Jr. | NO | receptions | 4.5 | opponent_shrunk_rolling5 | 4.2 | 40.0% | — | 60.0% | 8 |
| Harold Fannin Jr. | NO | receptions | 4.5 | rolling5_empirical | 4.2 | 39.8% | 52.7% | 60.2% | 8 |
| Harold Fannin Jr. | NO | receptions | 4.5 | season_empirical | 4.4 | 50.0% | 55.6% | 50.0% | 8 |
| Jahmyr Gibbs | MIA | receiving_yards | 32.5 | opponent_shrunk_rolling5 | 38.8 | 40.1% | — | 59.9% | 7 |
| Jahmyr Gibbs | MIA | receiving_yards | 32.5 | rolling5_empirical | 38.8 | 40.1% | — | 59.9% | 7 |
| Jahmyr Gibbs | MIA | receiving_yards | 32.5 | season_empirical | 40.7 | 42.7% | — | 57.3% | 7 |
| Jahmyr Gibbs | MIA | receptions | 4.5 | opponent_shrunk_rolling5 | 4.6 | 59.9% | — | 40.1% | 7 |
| Jahmyr Gibbs | MIA | receptions | 4.5 | rolling5_empirical | 4.6 | 60.1% | 58.4% | 39.9% | 7 |
| Jahmyr Gibbs | MIA | receptions | 4.5 | season_empirical | 4.9 | 71.4% | 61.7% | 28.6% | 7 |
| Jahmyr Gibbs | MIA | rushing_yards | 98.5 | opponent_shrunk_rolling5 | 111.8 | 59.9% | — | 40.1% | 7 |
| Jahmyr Gibbs | MIA | rushing_yards | 98.5 | rolling5_empirical | 112.9 | 79.9% | 63.6% | 20.1% | 7 |
| Jahmyr Gibbs | MIA | rushing_yards | 98.5 | season_empirical | 110.4 | 71.3% | 55.1% | 28.7% | 7 |
| Jake Ferguson | IND | receiving_yards | 15.5 | opponent_shrunk_rolling5 | 13.2 | 39.9% | — | 60.1% | 7 |
| Jake Ferguson | IND | receiving_yards | 15.5 | rolling5_empirical | 13.2 | 39.9% | — | 60.1% | 7 |
| Jake Ferguson | IND | receiving_yards | 15.5 | season_empirical | 16.4 | 42.9% | — | 57.1% | 7 |
| Jake Ferguson | IND | receptions | 2.5 | opponent_shrunk_rolling5 | 2.2 | 60.0% | — | 40.0% | 7 |
| Jake Ferguson | IND | receptions | 2.5 | rolling5_empirical | 2.2 | 60.0% | 58.3% | 40.0% | 7 |
| Jake Ferguson | IND | receptions | 2.5 | season_empirical | 2.4 | 57.4% | 57.6% | 42.6% | 7 |
| Jared Goff | MIA | passing_yards | 260 | opponent_shrunk_rolling5 | 285.3 | 80.0% | — | 20.0% | 7 |
| Jared Goff | MIA | passing_yards | 260 | rolling5_empirical | 286.0 | 80.0% | — | 20.0% | 7 |
| Jared Goff | MIA | passing_yards | 260 | season_empirical | 280.5 | 71.4% | — | 28.6% | 7 |
| Javonte Williams | IND | receiving_yards | 8.5 | opponent_shrunk_rolling5 | 10.6 | 60.1% | — | 39.9% | 7 |
| Javonte Williams | IND | receiving_yards | 8.5 | rolling5_empirical | 10.6 | 59.9% | — | 40.1% | 7 |
| Javonte Williams | IND | receiving_yards | 8.5 | season_empirical | 14.8 | 71.4% | — | 28.6% | 7 |
| Javonte Williams | IND | receptions | 1.5 | opponent_shrunk_rolling5 | 2.2 | 80.0% | — | 20.0% | 7 |
| Javonte Williams | IND | receptions | 1.5 | rolling5_empirical | 2.4 | 80.0% | 64.8% | 20.0% | 7 |
| Javonte Williams | IND | receptions | 1.5 | season_empirical | 2.9 | 85.7% | 67.3% | 14.3% | 7 |
| Javonte Williams | IND | rushing_yards | 73.5 | opponent_shrunk_rolling5 | 76.8 | 20.0% | — | 80.0% | 8 |
| Javonte Williams | IND | rushing_yards | 73.5 | rolling5_empirical | 71.7 | 19.9% | 18.0% | 80.1% | 8 |
| Javonte Williams | IND | rushing_yards | 73.5 | season_empirical | 66.0 | 24.9% | 21.4% | 75.1% | 8 |
| Jonah Coleman | CAR | receiving_yards | 24.5 | opponent_shrunk_rolling5 | 32.0 | 33.4% | — | 66.6% | 3 |
| Jonah Coleman | CAR | receiving_yards | 24.5 | rolling5_empirical | 32.3 | 33.2% | — | 66.8% | 3 |
| Jonah Coleman | CAR | receiving_yards | 24.5 | season_empirical | 32.4 | 33.5% | — | 66.5% | 3 |
| Jonah Coleman | CAR | receptions | 3.5 | opponent_shrunk_rolling5 | 3.0 | 33.4% | — | 66.6% | 3 |
| Jonah Coleman | CAR | receptions | 3.5 | rolling5_empirical | 3.0 | 33.3% | 50.8% | 66.7% | 3 |
| Jonah Coleman | CAR | receptions | 3.5 | season_empirical | 3.0 | 33.3% | 50.8% | 66.7% | 3 |
| Jonah Coleman | CAR | rushing_yards | 56 | opponent_shrunk_rolling5 | 49.3 | 33.3% | — | 66.7% | 3 |
| Jonah Coleman | CAR | rushing_yards | 56 | rolling5_empirical | 44.7 | 0.0% | 0.0% | 100.0% | 3 |
| Jonah Coleman | CAR | rushing_yards | 56 | season_empirical | 44.7 | 0.0% | 0.0% | 100.0% | 3 |
| Jonathan Taylor | DAL | receiving_yards | 19.5 | opponent_shrunk_rolling5 | 27.2 | 59.9% | — | 40.1% | 8 |
| Jonathan Taylor | DAL | receiving_yards | 19.5 | rolling5_empirical | 27.0 | 59.9% | — | 40.1% | 8 |
| Jonathan Taylor | DAL | receiving_yards | 19.5 | season_empirical | 25.3 | 62.6% | — | 37.4% | 8 |
| Jonathan Taylor | DAL | receptions | 2.5 | opponent_shrunk_rolling5 | 2.4 | 39.8% | — | 60.2% | 8 |
| Jonathan Taylor | DAL | receptions | 2.5 | rolling5_empirical | 2.4 | 40.1% | 52.8% | 59.9% | 8 |
| Jonathan Taylor | DAL | receptions | 2.5 | season_empirical | 2.6 | 50.0% | 55.6% | 50.0% | 8 |
| Jonathan Taylor | DAL | rushing_yards | 70 | opponent_shrunk_rolling5 | 79.4 | 60.0% | — | 40.0% | 8 |
| Jonathan Taylor | DAL | rushing_yards | 70 | rolling5_empirical | 70.4 | 60.1% | 45.8% | 39.9% | 8 |
| Jonathan Taylor | DAL | rushing_yards | 70 | season_empirical | 76.3 | 62.5% | 47.7% | 37.5% | 8 |
| Kenneth Walker III | NYJ | receiving_yards | 18 | opponent_shrunk_rolling5 | 10.2 | 20.0% | — | 80.0% | 7 |
| Kenneth Walker III | NYJ | receiving_yards | 18 | rolling5_empirical | 10.4 | 20.0% | — | 80.0% | 7 |
| Kenneth Walker III | NYJ | receiving_yards | 18 | season_empirical | 18.7 | 35.7% | — | 64.3% | 7 |
| Kenneth Walker III | NYJ | receptions | 2.5 | opponent_shrunk_rolling5 | 2.6 | 40.0% | — | 60.0% | 7 |
| Kenneth Walker III | NYJ | receptions | 2.5 | rolling5_empirical | 2.6 | 40.1% | 52.8% | 59.9% | 7 |
| Kenneth Walker III | NYJ | receptions | 2.5 | season_empirical | 3.1 | 57.1% | 57.5% | 42.9% | 7 |
| Kenneth Walker III | NYJ | rushing_yards | 92.5 | opponent_shrunk_rolling5 | 99.2 | 40.0% | — | 60.0% | 7 |
| Kenneth Walker III | NYJ | rushing_yards | 92.5 | rolling5_empirical | 96.1 | 40.2% | 31.6% | 59.8% | 7 |
| Kenneth Walker III | NYJ | rushing_yards | 92.5 | season_empirical | 109.9 | 57.1% | 43.5% | 42.9% | 7 |
| Kyren Williams | WAS | receiving_yards | 21 | opponent_shrunk_rolling5 | 28.2 | 60.0% | — | 40.0% | 8 |
| Kyren Williams | WAS | receiving_yards | 21 | rolling5_empirical | 27.2 | 60.0% | — | 40.0% | 8 |
| Kyren Williams | WAS | receiving_yards | 21 | season_empirical | 30.3 | 62.7% | — | 37.3% | 8 |
| Kyren Williams | WAS | receptions | 2.5 | opponent_shrunk_rolling5 | 4.8 | 59.9% | — | 40.1% | 8 |
| Kyren Williams | WAS | receptions | 2.5 | rolling5_empirical | 4.4 | 59.8% | 58.3% | 40.2% | 8 |
| Kyren Williams | WAS | receptions | 2.5 | season_empirical | 4.1 | 62.5% | 59.0% | 37.5% | 8 |
| Kyren Williams | WAS | rushing_yards | 60.5 | opponent_shrunk_rolling5 | 61.9 | 39.8% | — | 60.2% | 8 |
| Kyren Williams | WAS | rushing_yards | 60.5 | rolling5_empirical | 66.8 | 40.1% | 31.5% | 59.9% | 8 |
| Kyren Williams | WAS | rushing_yards | 60.5 | season_empirical | 68.5 | 49.9% | 38.3% | 50.1% | 8 |
| Malik Nabers | PHI | receiving_yards | 73.5 | opponent_shrunk_rolling5 | 108.1 | 79.9% | — | 20.1% | 7 |
| Malik Nabers | PHI | receiving_yards | 73.5 | rolling5_empirical | 107.0 | 80.0% | — | 20.0% | 7 |
| Malik Nabers | PHI | receiving_yards | 73.5 | season_empirical | 86.6 | 57.3% | — | 42.7% | 7 |
| Malik Nabers | PHI | receptions | 5.5 | opponent_shrunk_rolling5 | 8.2 | 79.9% | — | 20.1% | 7 |
| Malik Nabers | PHI | receptions | 5.5 | rolling5_empirical | 8.2 | 80.0% | 64.8% | 20.0% | 7 |
| Malik Nabers | PHI | receptions | 5.5 | season_empirical | 6.9 | 71.4% | 61.7% | 28.6% | 7 |
| Matthew Stafford | WAS | passing_yards | 245.5 | opponent_shrunk_rolling5 | 269.9 | 39.7% | — | 60.3% | 8 |
| Matthew Stafford | WAS | passing_yards | 245.5 | rolling5_empirical | 254.9 | 40.1% | — | 59.9% | 8 |
| Matthew Stafford | WAS | passing_yards | 245.5 | season_empirical | 268.1 | 49.9% | — | 50.1% | 8 |
| Puka Nacua | WAS | receiving_yards | 93 | opponent_shrunk_rolling5 | 101.0 | 40.1% | — | 59.9% | 6 |
| Puka Nacua | WAS | receiving_yards | 93 | rolling5_empirical | 98.1 | 39.9% | — | 60.1% | 6 |
| Puka Nacua | WAS | receiving_yards | 93 | season_empirical | 94.2 | 33.3% | — | 66.7% | 6 |
| Puka Nacua | WAS | receptions | 8.5 | opponent_shrunk_rolling5 | 11.4 | 80.0% | — | 20.0% | 6 |
| Puka Nacua | WAS | receptions | 8.5 | rolling5_empirical | 10.2 | 60.1% | 58.4% | 39.9% | 6 |
| Puka Nacua | WAS | receptions | 8.5 | season_empirical | 9.3 | 50.0% | 55.6% | 50.0% | 6 |
| Rashee Rice | NYJ | receiving_yards | 55.5 | opponent_shrunk_rolling5 | 59.6 | 50.1% | — | 49.9% | 4 |
| Rashee Rice | NYJ | receiving_yards | 55.5 | rolling5_empirical | 60.8 | 50.0% | — | 50.0% | 4 |
| Rashee Rice | NYJ | receiving_yards | 55.5 | season_empirical | 60.7 | 50.0% | — | 50.0% | 4 |
| Rashee Rice | NYJ | receptions | 4.5 | opponent_shrunk_rolling5 | 4.5 | 50.0% | — | 50.0% | 4 |
| Rashee Rice | NYJ | receptions | 4.5 | rolling5_empirical | 5.0 | 49.9% | 55.6% | 50.1% | 4 |
| Rashee Rice | NYJ | receptions | 4.5 | season_empirical | 5.0 | 49.8% | 55.5% | 50.2% | 4 |
| Sam LaPorta | MIA | receiving_yards | 48.5 | opponent_shrunk_rolling5 | 53.5 | 40.1% | — | 59.9% | 7 |
| Sam LaPorta | MIA | receiving_yards | 48.5 | rolling5_empirical | 53.3 | 39.9% | — | 60.1% | 7 |
| Sam LaPorta | MIA | receiving_yards | 48.5 | season_empirical | 52.4 | 42.9% | — | 57.1% | 7 |
| Sam LaPorta | MIA | receptions | 4 | opponent_shrunk_rolling5 | 4.0 | 39.9% | — | 60.1% | 7 |
| Sam LaPorta | MIA | receptions | 4 | rolling5_empirical | 4.0 | 39.9% | 52.7% | 60.1% | 7 |
| Sam LaPorta | MIA | receptions | 4 | season_empirical | 4.4 | 57.0% | 57.5% | 43.0% | 7 |
| Saquon Barkley | NYG | receiving_yards | 9.5 | opponent_shrunk_rolling5 | 8.6 | 40.1% | — | 59.9% | 6 |
| Saquon Barkley | NYG | receiving_yards | 9.5 | rolling5_empirical | 8.8 | 40.0% | — | 60.0% | 6 |
| Saquon Barkley | NYG | receiving_yards | 9.5 | season_empirical | 6.8 | 33.3% | — | 66.7% | 6 |
| Saquon Barkley | NYG | receptions | 1.5 | opponent_shrunk_rolling5 | 1.2 | 20.0% | — | 80.0% | 6 |
| Saquon Barkley | NYG | receptions | 1.5 | rolling5_empirical | 1.2 | 20.0% | 46.0% | 80.0% | 6 |
| Saquon Barkley | NYG | receptions | 1.5 | season_empirical | 1.2 | 16.8% | 44.5% | 83.2% | 6 |
| Saquon Barkley | NYG | rushing_yards | 54 | opponent_shrunk_rolling5 | 40.1 | 40.0% | — | 60.0% | 6 |
| Saquon Barkley | NYG | rushing_yards | 54 | rolling5_empirical | 38.3 | 40.1% | 31.6% | 59.9% | 6 |
| Saquon Barkley | NYG | rushing_yards | 54 | season_empirical | 45.5 | 49.8% | 38.2% | 50.2% | 6 |
| Tetairoa McMillan | DEN | receiving_yards | 60.5 | opponent_shrunk_rolling5 | 79.6 | 39.9% | — | 60.1% | 7 |
| Tetairoa McMillan | DEN | receiving_yards | 60.5 | rolling5_empirical | 78.7 | 40.0% | — | 60.0% | 7 |
| Tetairoa McMillan | DEN | receiving_yards | 60.5 | season_empirical | 81.5 | 57.3% | — | 42.7% | 7 |
| Tetairoa McMillan | DEN | receptions | 5 | opponent_shrunk_rolling5 | 6.6 | 60.0% | — | 40.0% | 7 |
| Tetairoa McMillan | DEN | receptions | 5 | rolling5_empirical | 6.4 | 60.0% | 58.4% | 40.0% | 7 |
| Tetairoa McMillan | DEN | receptions | 5 | season_empirical | 6.0 | 57.2% | 57.7% | 42.8% | 7 |
| Travis Kelce | NYJ | receiving_yards | 46 | opponent_shrunk_rolling5 | 46.6 | 60.0% | — | 40.0% | 7 |
| Travis Kelce | NYJ | receiving_yards | 46 | rolling5_empirical | 47.6 | 59.9% | — | 40.1% | 7 |
| Travis Kelce | NYJ | receiving_yards | 46 | season_empirical | 58.6 | 71.7% | — | 28.3% | 7 |
| Travis Kelce | NYJ | receptions | 4.5 | opponent_shrunk_rolling5 | 3.2 | 0.0% | — | 100.0% | 7 |
| Travis Kelce | NYJ | receptions | 4.5 | rolling5_empirical | 3.4 | 20.0% | 46.0% | 80.0% | 7 |
| Travis Kelce | NYJ | receptions | 4.5 | season_empirical | 4.1 | 28.5% | 49.2% | 71.5% | 7 |

## Official inactive impact to apply

The NFL Week 9 official inactive report is the availability source. Material 1 PM names include DAL WR George Pickens and KaVontae Turpin; NYJ WR Garrett Wilson; DET RB Jacob Saylors; PHI WR DeVonta Smith and Dontayvion Wicks; NYG RB Cam Skattebo; CAR RB AJ Dillon; plus the other listed inactives. Offensive inactives are excluded from the simulation while their captured quotes remain in the line archive. Defensive inactives are matchup context and do not receive player offensive prop projections.

## Limits and gates

- Exact quote timestamps are per book and expire at the stored `validUntil`; recheck before any later decision.
- Historical input does not distinguish active zero opportunity from inactive or unavailable. A zero stat with positive opportunity remains in history; no-opportunity rows are omitted.
- Coverage, route participation, player assignment, pressure-at-decision, snap limits and weather are not included in these empirical distributions.
- `calibration=false` and `production_ready=false`; this new run does not change the 08:56 prospective lock or its baseline.

## Files

- Lines: `research/week9_1pm_live/WEEK9_1PM_DK_FD_LINES_20261108_175611.028Z.csv`
- 100k simulation: `research/week9_1pm_live/WEEK9_1PM_100K_SIMULATIONS.csv`
- Calibration diagnostic: `research/week9_1pm_live/WEEK9_1PM_CALIBRATION_DIAGNOSTIC.csv`
- Historical walk-forward events: `research/week9_1pm_live/WEEK9_1PM_WALK_FORWARD_EVENTS.csv`
- Metadata: `research/week9_1pm_live/WEEK9_1PM_RUN_METADATA.json`
