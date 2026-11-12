# P6 rush-over exception backtest (2026 Wk3–8). Analysis only, no rules changed
Generated 2026-11-01 (ET). Scripts: `bt_p6.py` (Wk3–8 from nflverse pbp, incl. CAR@GB), `bt_p6_wk8.py` (Wk8 Sunday graded from `playlogs/2026_wk8/*_box.json`). Every leg is in `p6_legs_all.csv`.

**Setup**
- **P6 proxy:** an RB rushing-yards OVER for an underdog team (team spread > 0), meaning the leg needs a trailing script. The universe is RBs with at least 2 prior games averaging 8+ carries who were active that week.
- **Walk-forward:** week W uses only plays before week W. The model is sim_v6 RAW: `calib=None`, because the calibration was fitted on Wk4–7 outcomes and would leak. It runs 100k sims for each of mc/bias/gr; p is the mean of the three P(X ≥ line).
- **Lines:** real book lines (from the Wk8 run manifests) for 9 legs. Everything else is a **stand-in**: floor(prior median) + 0.5.
- Wk1–2 can't be tested because there are fewer than 2 prior games.

## Buckets
| Bucket | n | W/L | Hit | 90% CI | ROI −110 | ROI −130 | ROI −160 |
|---|---|---|---|---|---|---|---|
| ALL P6 cuts | 90 | 41/90 | 45.6% | 37%-54% | -13.0% | -19.4% | -26.0% |
| p >= .60 | 28 | 14/28 | 50.0% | 35%-65% | -4.5% | -11.5% | -18.8% |
| p .55-.60 | 10 | 4/10 | 40.0% | 19%-65% | -23.6% | -29.2% | -35.0% |
| p < .55 | 52 | 23/52 | 44.2% | 33%-56% | -15.6% | -21.7% | -28.1% |
| VARIANT p >= .65 | 21 | 11/21 | 52.4% | 35%-69% | +0.0% | -7.3% | -14.9% |
| VARIANT p >= .60 + small dog (<=3.5) | 17 | 8/17 | 47.1% | 29%-66% | -10.2% | -16.7% | -23.5% |
| p >= .60 real lines only | 5 | 2/5 | 40.0% | 14%-73% | -23.6% | -29.2% | -35.0% |
| p >= .60 stand-ins only | 23 | 12/23 | 52.2% | 36%-68% | -0.4% | -7.7% | -15.2% |

## n per week × bucket
| week   |   .55-.60 |   <.55 |   >=.60 |   All |
|:-------|----------:|-------:|--------:|------:|
| 3      |         1 |     16 |       3 |    20 |
| 4      |         2 |      9 |       6 |    17 |
| 5      |         1 |      8 |       5 |    14 |
| 6      |         0 |      6 |       4 |    10 |
| 7      |         4 |      8 |       4 |    16 |
| 8      |         2 |      5 |       6 |    13 |
| All    |        10 |     52 |      28 |    90 |

## p ≥ .60 hits per week
|   week |   sum |   count |
|-------:|------:|--------:|
|      3 |     1 |       3 |
|      4 |     4 |       6 |
|      5 |     2 |       5 |
|      6 |     2 |       4 |
|      7 |     3 |       4 |
|      8 |     2 |       6 |

## Losers the exception would have let through (p ≥ .60): 14
- Wk3 Breece Hall (NYJ +7.0) O65.5 [standin] p 0.74 → 32
- Wk3 Ashton Jeanty (LV +3.5) O75.5 [standin] p 0.78 → 56
- Wk4 Cam Skattebo (NYG +2.5) O60.5 [standin] p 0.64 → 58
- Wk4 Jacory Croskey-Merritt (WAS +4.5) O43.5 [standin] p 0.83 → 15
- Wk5 Alvin Kamara (NO +2.5) O23.5 [standin] p 0.69 → 12
- Wk5 Omarion Hampton (LAC +3.5) O50.5 [standin] p 0.69 → 33
- Wk5 Ashton Jeanty (LV +3.5) O57.5 [standin] p 0.73 → 27
- Wk6 Bijan Robinson (ATL +1.5) O86.5 [standin] p 0.63 → 61
- Wk6 MarShawn Lloyd (GB +1.5) O20.5 [standin] p 0.70 → 10
- Wk7 Derrick Henry (BAL +3.0) O81.5 [standin] p 0.73 → 45
- Wk8 Jordan Mason (MIN +3.5) O49.5 [real] p 0.65 → 20
- Wk8 Jonathan Taylor (IND +10.5) O50.5 [real] p 0.65 → 23
- Wk8 Omarion Hampton (LAC +6.5) O31.5 [real] p 0.69 → 20
- Wk8 Jeremiyah Love (ARI +7.0) O41.5 [standin] p 0.77 → 23

## Read
- The postmortem's "2/2" counted only the two legs P6 actually cut on Wk8. Across every Wk8 P6-eligible leg on real lines, p ≥ .60 went **2/5**. Wk3–8 overall went **14/28 (50%)**, which is below break-even at every price.
- Raw sim_v6 is overconfident on underdog RB overs: legs priced at .60+ cashed 50%. P6 is doing real work as a filter.
- p ≥ .65 is 11/21, break-even at −110 only, with a CI of 35–69%. That isn't evidence of an edge.
- Small samples: every bucket has n < 50, real-line n = 5, and weekly n is 3–6.
- Caveats:
  - Stand-in lines are softer than book lines.
  - P6 here is a spread proxy: the clutch D/F grade isn't reconstructed.
  - Players active with 0 carries are dropped.
  - The Wk8 spreads come from game_scripts_2026.csv.

**Recommendation:** don't adopt the p ≥ .60 exception. Keep P6 as is and re-test after Wk12 with real lines and calibrated sim probabilities.
