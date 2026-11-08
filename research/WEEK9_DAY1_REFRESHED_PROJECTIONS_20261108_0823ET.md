# Week 9 refreshed lines and projection overlay

**Captured:** 2026-11-08 8:23 a.m. ET (13:23:06Z), from Fieldwork’s scheduled Odds API board. **Scope:** 79 player-market rows from the saved model board; DraftKings and FanDuel current quotes where listed. Book quote timestamps are retained in the paired refresh CSV and vary by market.

## Projection method and limits

Forecast means and quantile bands below come from the already saved three-model 100,000-draw empirical run. They are unchanged by a sportsbook line move because the forecast is outcome-based. This is a fresh line-relative overlay, not a re-fit or fresh simulation. The saved simulation exports summary quantiles and probabilities but not draw-level outcomes or player-week samples, so a threshold-shifted hit probability cannot be recomputed honestly from that file. The overlay reports raw over frequencies only when the current book line exactly matches the saved simulation line; those frequencies are uncalibrated. No probability is promoted to calibrated or bet-approved.

Game-day conditions checked at 8:18 a.m. ET: only CIN–ATL inactives were posted; all other listed game-day inactive statuses remained pending. Key flags: Amon-Ra St. Brown Q (rib); George Pickens Q; Sam Darnold OUT and Rashid Shaheed OUT, with Seattle rain around kickoff; Emeka Egbuka Q; Hunter Henry Q. No injury or weather multipliers were inserted without a verified player-level adjustment. See `WEEK9_GAME_DAY_WEATHER_INACTIVES_20261108.md`.

## Same-threshold raw-frequency screen

All rows below match the saved simulation threshold exactly. Frequencies are uncalibrated bootstrap outputs, not hit probabilities verified by out-of-sample calibration. They can vary widely between candidate models and have only 5–8 eligible historical games. “Mean gap” compares the line with the range of the three model means; it is not a probability or expected profit.

| Player | Market / book | Current line (over price) | Mean range; gap vs line | Raw over frequency range | Games |
|---|---|---:|---:|---:|---:|
| Trey McBride | receptions / DraftKings (Over screen) | 6.5 (-136) | 7.6–8.2; +1.1 to +1.8 | 100.0%–100.0% | 8 |
| Ashton Jeanty | receiving_yards / FanDuel (Over screen) | 35.5 (-113) | 47.0–55.8; +11.5 to +20.3 | 87.6%–100.0% | 8 |
| Ashton Jeanty | receiving_yards / DraftKings (Over screen) | 35.5 (-113) | 47.0–55.7; +11.5 to +20.2 | 87.5%–100.0% | 8 |
| Ladd McConkey | receptions / DraftKings (Under screen) | 4.5 (+125) | 2.4–2.8; -2.1 to -1.7 | 0.0%–16.9% | 6 |
| Jaxon Smith-Njigba | receiving_yards / DraftKings (Over screen) | 93.5 (-114) | 116.1–123.2; +22.6 to +29.7 | 80.1%–87.5% | 8 |
| Jaxon Smith-Njigba | receiving_yards / FanDuel (Over screen) | 94.5 (-113) | 116.0–123.1; +21.5 to +28.6 | 79.9%–87.5% | 8 |
| Woody Marks | rushing_yards / DraftKings (Under screen) | 64.5 (-109) | 38.6–46.0; -25.9 to -18.5 | 14.2%–20.2% | 7 |
| Tre Tucker | receiving_yards / FanDuel (Over screen) | 34.5 (-113) | 56.4–59.2; +21.9 to +24.7 | 75.1%–80.0% | 8 |
| Tre Tucker | receiving_yards / DraftKings (Over screen) | 34.5 (-110) | 56.6–59.4; +22.1 to +24.9 | 75.1%–80.2% | 8 |
| AJ Barner | receiving_yards / DraftKings (Under screen) | 25.5 (-108) | 22.6–25.4; -2.9 to -0.1 | 19.9%–25.1% | 8 |
| AJ Barner | receiving_yards / FanDuel (Under screen) | 24.5 (-113) | 22.6–25.4; -1.9 to +0.9 | 20.0%–25.1% | 8 |
| Jahmyr Gibbs | rushing_yards / DraftKings (Over screen) | 96.5 (-114) | 110.7–113.1; +14.2 to +16.6 | 71.7%–80.2% | 7 |
| Amon-Ra St. Brown | receiving_yards / DraftKings (Under screen) | 77.5 (-110) | 72.4–81.3; -5.1 to +3.8 | 20.0%–28.3% | 7 |
| Dalton Schultz | receiving_yards / DraftKings (Under screen) | 36.5 (-109) | 28.6–46.1; -7.9 to +9.6 | 19.9%–28.7% | 7 |
| George Kittle | receiving_yards / FanDuel (Over screen) | 68.5 (-113) | 60.6–67.9; -7.9 to -0.6 | 71.2%–80.3% | 7 |
| Amon-Ra St. Brown | receiving_yards / FanDuel (Under screen) | 76.5 (-113) | 72.4–81.8; -4.1 to +5.3 | 20.0%–28.9% | 7 |
| Emeka Egbuka | receiving_yards / DraftKings (Under screen) | 50.5 (-114) | 35.3–39.9; -15.2 to -10.6 | 19.9%–33.2% | 6 |
| Quentin Johnston | receiving_yards / DraftKings (Over screen) | 29.5 (-115) | 33.7–37.9; +4.2 to +8.4 | 66.8%–79.9% | 6 |
| Tre Harris | receiving_yards / DraftKings (Over screen) | 29.5 (-110) | 42.7–49.0; +13.2 to +19.5 | 66.7%–80.1% | 6 |
| Quentin Johnston | receiving_yards / FanDuel (Over screen) | 31.5 (-113) | 33.7–38.0; +2.2 to +6.5 | 66.6%–79.9% | 6 |
| Emeka Egbuka | receiving_yards / FanDuel (Under screen) | 50.5 (-113) | 35.4–40.0; -15.1 to -10.5 | 20.0%–33.5% | 6 |
| Hunter Henry | receiving_yards / DraftKings (Over screen) | 37.5 (-110) | 40.8–51.1; +3.3 to +13.6 | 62.6%–80.3% | 8 |
| Cooper Kupp | receiving_yards / FanDuel (Under screen) | 25.5 (-113) | 20.9–25.7; -4.6 to +0.2 | 19.9%–37.5% | 8 |
| CeeDee Lamb | receiving_yards / DraftKings (Under screen) | 85.5 (-112) | 79.8–88.7; -5.7 to +3.2 | 20.0%–37.5% | 8 |
| Cooper Kupp | receiving_yards / DraftKings (Under screen) | 25.5 (-116) | 20.9–25.8; -4.6 to +0.3 | 19.8%–37.5% | 8 |
| George Pickens | receiving_yards / FanDuel (Over screen) | 54.5 (-113) | 66.6–76.7; +12.1 to +22.2 | 62.4%–80.2% | 8 |
| CeeDee Lamb | receiving_yards / FanDuel (Under screen) | 83.5 (-113) | 79.0–89.1; -4.5 to +5.6 | 19.5%–37.9% | 8 |
| Chris Olave | receptions / DraftKings (Over screen) | 5.5 (-124) | 5.8–7.0; +0.3 to +1.5 | 60.2%–71.4% | 7 |
| Rhamondre Stevenson | rushing_yards / FanDuel (Under screen) | 54.5 (-113) | 46.0–50.1; -8.5 to -4.4 | 25.1%–39.9% | 8 |
| Kenny Gainwell | rushing_yards / FanDuel (Under screen) | 21.5 (-113) | 36.2–53.5; +14.7 to +32.0 | 25.0%–39.9% | 8 |
| Caleb Williams | passing_yards / FanDuel (Over screen) | 243.5 (-113) | 246.9–253.5; +3.4 to +10.0 | 60.1%–80.0% | 5 |
| Xavier Hutchinson | receiving_yards / DraftKings (Over screen) | 21.5 (-112) | 36.8–37.8; +15.3 to +16.3 | 60.1%–71.5% | 7 |
| Trey McBride | receiving_yards / FanDuel (Over screen) | 59.5 (-113) | 62.7–68.0; +3.2 to +8.5 | 60.0%–62.6% | 8 |
| Jahmyr Gibbs | rushing_yards / FanDuel (Over screen) | 98.5 (-113) | 110.2–112.9; +11.7 to +14.4 | 60.0%–79.9% | 7 |
| Kenny Gainwell | rushing_yards / DraftKings (Under screen) | 22.5 (-112) | 35.9–53.6; +13.4 to +31.1 | 24.9%–40.0% | 8 |
| Luther Burden III | receiving_yards / DraftKings (Under screen) | 65.5 (-111) | 68.3–78.0; +2.8 to +12.5 | 24.9%–40.0% | 8 |

## Files

- `WEEK9_DAY1_DK_FD_REFRESH_20261108_0823ET.csv` — 79 market rows with per-book lines, prices, source and receipt times.
- `WEEK9_DAY1_REFRESHED_PROJECTION_OVERLAY_20261108_0823ET.csv` — per-book current line versus prior model mean/quantile range and probability reuse status.
- Existing 100,000-draw output: `WEEK9_DAY1_MODEL_SIMULATION_20261108.csv`; trial notes: `WEEK9_DAY1_MODEL_TRIALS_20261108.md`.
