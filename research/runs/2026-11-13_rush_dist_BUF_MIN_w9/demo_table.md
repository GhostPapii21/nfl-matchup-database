# Week 9 BUF@MIN rush-yards distribution demo (research only, n=20000)

Smoke test on ONE game; not a calibration result. PIT = P(X<actual)+0.5P(X=actual); a calibrated model puts PITs roughly uniform, ~80% inside [0.1, 0.9].

seed 713001691, chunks 4, runtime 189.6s, box reconciliation failures 0/20000; points mean MIN 22.5 BUF 28.2.

| Team | Player | Pos | Car mean | Rush yds mean | p10 / p50 / p90 | Actual | PIT | FD line | P(under) model | FD no-vig under | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BUF | J.Cook | RB | 21.7 | 115.0 | 70 / 112 / 164 | 107 | 0.447 | 84.5 | 0.211 | 0.500 | O |
| BUF | J.Allen | QB | 6.4 | 39.6 | 13 / 37 / 70 | 15 | 0.128 | 30.5 | 0.376 | 0.500 | U |
| BUF | R.Davis | RB | 1.6 | 6.8 | 0 / 6 / 15 | 2 | 0.234 | 5.5 | 0.464 | 0.515 | U |
| BUF | T.Johnson | RB | 0.8 | 1.5 | 0 / 0 / 4 | 1 | 0.541 |  |  |  |  |
| BUF | D.Moore | WR | 0.5 | 1.4 | 0 / 0 / 6 | 11 | 0.987 |  |  |  |  |
| MIN | A.Jones | RB | 16.6 | 69.0 | 39 / 67 / 102 | 16 | 0.004 | 30.5 | 0.043 | 0.500 | U |
| MIN | J.Mason | RB | 6.0 | 23.6 | 5 / 21 / 46 | 35 | 0.784 | 47.5 | 0.912 | 0.500 | U |
| MIN | K.Murray | QB | 3.1 | 28.2 | 6 / 24 / 56 |  |  |  |  |  |  |
| MIN | D.Claiborne | RB | 0.8 | 0.5 | -1 / 0 / 3 |  |  |  |  |  |  |
| MIN | D.Dallas | RB | 0.7 | 2.5 | 0 / 2 / 8 |  |  |  |  |  |  |
| MIN | C.Wentz | QB | 0.6 | 1.0 | 0 / 0 / 4 | 0 | 0.310 | 7.5 | 0.991 | 0.500 | U |

Players with an actual: 8; PIT inside [0.1, 0.9]: 75%; mean PIT 0.429 (0.5 = unbiased).

FD lines: draft PR #41 data/odds_history/alt_test_week9/raw (historical snapshot, 0 new credits).
