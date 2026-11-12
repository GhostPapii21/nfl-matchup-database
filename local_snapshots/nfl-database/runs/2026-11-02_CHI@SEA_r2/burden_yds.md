# Burden receiving yards, MNF CHI@SEA. Odds at 7:29 AM ET (jsn_995/odds_m0729.csv). Fixed-model, copies only (jsn_995/raw_burden_yds.json). Script: /tmp/b.py
|   week | opp   |   tgt |   rec |   yds |   td |   adot |   air |   rz |   lng |   mid |   share | qb         |
|-------:|:------|------:|------:|------:|-----:|-------:|------:|-----:|------:|------:|--------:|:-----------|
|      1 | CAR   |     5 |     5 |    63 |    0 |   7.2  |    36 |    0 |    24 |  0.4  |    0.17 | C.Williams |
|      2 | MIN   |     7 |     3 |    32 |    0 |  12.43 |    87 |    2 |    18 |  0.29 |    0.2  | C.Williams |
|      3 | PHI   |    11 |     7 |    61 |    1 |   5.09 |    56 |    4 |    25 |  0.45 |    0.32 | C.Keenum   |
|      4 | NYJ   |     6 |     4 |    63 |    0 |   9.83 |    59 |    0 |    22 |  0.33 |    0.18 | T.Bagent   |
|      5 | GB    |     6 |     4 |    47 |    0 |  13    |    78 |    2 |    23 |  0.5  |    0.15 | T.Bagent   |
|      6 | ATL   |     8 |     8 |    95 |    0 |   5.75 |    46 |    1 |    25 |  0.12 |    0.22 | C.Williams |
|      7 | NE    |     4 |     4 |   130 |    1 |   9.5  |    38 |    0 |    58 |  0.25 |    0.12 | C.Williams |
Caleb-game WR/TE targets {'L.Burden': 24, 'C.Loveland': 24, 'K.Raymond': 18, 'R.Odunze': 16, 'C.Kmet': 9, 'S.Roush': 3}
YAC {1: 27.0, 2: 5.0, 3: 29.0, 4: 18.0, 5: 30.0, 6: 49.0, 7: 92.0} tot 250.0
loc {'right': 18, 'middle': 16, 'left': 13} yds by loc {'left': 148.0, 'middle': 165.0, 'right': 178.0}
Loveland rec by wk {1: 0.0, 2: 1.0, 3: 4.0, 4: 6.0, 5: 2.0, 6: 6.0, 7: 7.0}
Caleb games, yards: 63, 32, 95, 130 (avg 80, median 79). All 7 games: avg 70.1. Longest 58 (Wk 7). Season aDOT about 9. YAC 250 of 491 yards (51%). Wk 7 had 92 YAC.
Location proxy: targets right 18, middle 16, left 13. Yards: middle 165 (34%), right 178, left 148. SEA allows 15.6 WR ypg on middle throws, and Loeb says SEA allows the fewest slot catches (4.5/g). Both cut against his middle/YAC role.
Model medians: 48.5 / 46.6 / 47.1 yards, all below FD's main 51.5.

| Rung (FD price; DK) | no-vig | MC/Bias/GR | Raw Over | Over x0.7 | Over to50 | Clear Over (raw/x0.7/to50) | Clear Under (raw/x0.7) | §7 Over w/ Caleb |
|---|---|---|---|---|---|---|---|---|
| O29.5 (-420; -383) | .761 | .748/.725/.697 | -1.4/-3.6/-6.4 | -1.0/-2.5/-4.5 | -8.8/-10.4/-12.3 | 0/0/0 | 2/1 | 4/4 |
| O39.5 (-220; -208) | .648 | .610/.588/.579 | -3.7/-6.0/-6.9 | -2.6/-4.2/-4.8 | -7.1/-8.6/-9.3 | 0/0/0 | 3/2 | 3/4 |
| O49.5 (-130; -121) | .533 | .477/.457/.476 | -5.5/-7.6/-5.6 | -3.9/-5.3/-4.0 | -4.8/-6.3/-4.9 | 0/0/0 | 3/3 | 3/4 |
| O51.5 main (-113/-113; DK 50.5 -115) | .500 | .457/.426/.449 | -4.3/-7.4/-5.1 | -3.0/-5.2/-3.6 | same | 0/0/0 | 3/3 (MC exactly 3.0) | 3/4 (Under 1/4) |
No 34.5 rung is posted. Under edges on alt rungs are approximate (1 - alt no-vig). The Under fails §7 at 1/4 with Caleb.
Verdicts: O29.5 CUT (no model clears). O39.5 CUT (all models below book). O49.5 CUT (0/3, about -6pp). O51.5 CUT. Under 51.5: models 3/3 but §7 fails, so CUT.

## Loveland receptions O1.5
DK -1780 (no-vig .894, overround from the DK 4.5 main). FD lowest rung is 2.5 (-490). Models .865/.959/.806. Raw -3.0/+6.5/-8.9, x0.7 -2.1/+4.5/-6.2, to50 all negative. Clears 1/3 (Bias only). §7 with Caleb (0, 1, 6, 7 catches) = 2/4, FAIL. Medians 4/5/4. CUT, and the price is unplayable anyway.
