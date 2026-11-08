# Week 9 CIN–ATL projection snapshot

**Frozen:** 2026-11-08 09:08 ET. Historical hit counts below compare W1–8 with today’s line; simulation probabilities are raw bootstrap frequencies, not calibrated probabilities. DraftKings lines shown where available. See README for full method, inputs, source caveats, and reproducibility.

| Player | Market / DK line | W1–8 hits | Model means (Season / Recent 5 / + opponent) | Raw P(over) (Season / Recent 5 / + opponent) |
|---|---:|---:|---:|---:|
| Joe Burrow | passing yards 278.5 | 4/7 | 302.5 / 330.5 / 335.0 | 57% / 80% / 80% |
| Joe Burrow | passing tds 2.5 | 4/7 | 2.9 / 3.4 / 3.4 | 57% / 80% / 80% |
| Ja'Marr Chase | receiving yards 76.5 | 3/7 | 69.8 / 81.0 / 81.3 | 42% / 60% / 60% |
| Ja'Marr Chase | receptions 6.5 | 3/7 | 6.2 / 6.8 / 7.6 | 43% / 40% / 60% |
| Tee Higgins | receiving yards 76.5 | 5/7 | 103.8 / 114.2 / 115.4 | 72% / 80% / 80% |
| Tee Higgins | receptions 5.5 | 4/7 | 6.1 / 7.0 / 7.8 | 57% / 80% / 80% |
| Mike Gesicki | receiving yards 27.5 | 4/6 | 40.1 / 32.7 / 32.7 | 67% / 60% / 60% |
| Mike Gesicki | receptions 2.5 | 4/6 | 2.8 / 2.4 / 2.4 | 67% / 60% / 60% |
| Chase Brown | rushing yards 49.5 | 4/7 | 48.5 / 40.7 / 41.2 | 57% / 40% / 40% |
| Chase Brown | receiving yards 23.5 | 2/7 | 26.9 / 33.1 / 32.9 | 28% / 40% / 40% |
| Michael Penix Jr. | passing yards 224.5 | 3/6 | 213.7 / 205.1 / 218.1 | 50% / 40% / 80% |
| Michael Penix Jr. | passing tds 1.5 | 2/6 | 1.5 / 1.6 / 1.6 | 33% / 40% / 40% |
| Drake London | receiving yards 77.5 | 3/8 | 77.7 / 69.9 / 72.2 | 37% / 40% / 40% |
| Drake London | receptions 5.5 | 3/8 | 4.9 / 4.8 / 4.8 | 38% / 40% / 40% |
| Kyle Pitts | receiving yards 42.5 | 2/8 | 24.6 / 35.5 / 36.4 | 25% / 40% / 60% |
| Bijan Robinson | rushing yards 97.5 | 2/8 | 97.6 / 86.3 / 88.7 | 25% / 20% / 20% |
| Bijan Robinson | rushing attempts 12.5 | 7/8 | 18.7 / 16.8 / 17.6 | 88% / 80% / 80% |

## First read

- Bengals passing props lean upward in the recent-five sample: Burrow clears 278.5 passing yards in 4/7 historical opportunity games; Higgins clears 76.5 receiving yards in 5/7. The season and recent samples agree directionally here, but samples are tiny and the models are not calibrated.
- Chase is much less clear at 76.5 yards (3/7 historical clears; model estimates 42–60%) and 6.5 receptions (3/7; 40–60%). His role has volume, but the yards/reception distribution is volatile.
- Atlanta side is mixed: Penix passing yards sits near 224.5 (3/6 clears; candidate probabilities range 40–80%); London is 3/8 at 77.5 receiving yards; Pitts is 2/8 at 42.5. Those are not reliable over signals.
- Bijan’s rushing yards line is high relative to his W1–8 hit count (2/8 over 97.5), while rushing attempts clears 12.5 in 7/8. His opportunity volume looks more supported than his yardage threshold. Atlanta’s Brian Robinson is on IR, but no extra carry share is mechanically added to Bijan’s historical results.
- Brown’s rushing output is volatile (4/7 over 49.5; recent five 2/5), while his receiving lines differ across books. Perine has sparse backup-volume history with a single large rushing game; do not treat his average as a stable workload estimate.

## Data/readiness status

The prospective artifact is frozen and reproducible for this game. Results from today’s game are not in the input and cannot be included before kickoff. This run does not establish calibrated hit probabilities. The full list of 31 book-line rows and all three 100,000-draw results is in the CSV. Coverage charting, likely individual matchups, current stadium roof/weather condition, and route/snap forecasts remain unavailable in this package.
