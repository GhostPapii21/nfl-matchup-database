# Rome Odunze, MNF CHI@SEA. pbp through Wk8, odds 7:26 AM ET (jsn_995/odds_m0726.csv). Fixed-model, copies only (jsn_995/raw_odunze.json). Script: odunze.py
|   week | opp   |   tgt |   rec |   yds |   td |   adot |   air |   rz |   lng |   mid |   share | qb         |
|-------:|:------|------:|------:|------:|-----:|-------:|------:|-----:|------:|------:|--------:|:-----------|
|      1 | CAR   |     3 |     2 |    52 |    0 |  30    |    90 |    0 |    47 |  0.33 |    0.1  | C.Williams |
|      2 | MIN   |     4 |     3 |    43 |    0 |  11.75 |    47 |    0 |    21 |  0.25 |    0.11 | C.Williams |
|      3 | PHI   |     6 |     3 |    44 |    0 |  14.5  |    87 |    2 |    22 |  0.17 |    0.18 | C.Keenum   |
|      4 | NYJ   |     7 |     6 |    94 |    0 |  11.57 |    81 |    0 |    37 |  0.43 |    0.21 | T.Bagent   |
|      5 | GB    |     9 |     3 |    40 |    0 |  11.22 |   101 |    2 |    20 |  0.44 |    0.22 | T.Bagent   |
|      6 | ATL   |     4 |     3 |    39 |    0 |   9.5  |    38 |    0 |    23 |  0.5  |    0.11 | C.Williams |
|      7 | NE    |     5 |     4 |    69 |    0 |  12.6  |    63 |    1 |    21 |  0    |    0.15 | C.Williams |
Caleb-game WR/TE targets {'L.Burden': 24, 'C.Loveland': 24, 'K.Raymond': 18, 'R.Odunze': 16, 'C.Kmet': 9, 'S.Roush': 3}
location all {'right': 16, 'middle': 12, 'left': 10}
|   week | posteam   | receiver_player_name   |   tgt |   rec |   yds |
|-------:|:----------|:-----------------------|------:|------:|------:|
|      1 | NE        | M.Hollins              |     5 |     4 |    51 |
|      3 | WAS       | S.Diggs                |     7 |     4 |    33 |
|      3 | WAS       | T.McLaurin             |     9 |     6 |    77 |
|      4 | LAC       | Q.Johnston             |     2 |     1 |    44 |
|      4 | LAC       | T.Harris               |     5 |     3 |    60 |
|      5 | SF        | M.Evans                |    11 |     7 |   113 |
SEA WR ypg 91.7 outside(L/R) ypg 76.1 middle ypg 15.6
Caleb games (1,2,6,7): rec 2,3,3,4 | yds 52,43,39,69 | tgt 3,4,4,5 (avg 4, 11.8% share). Backups (3-5): 22 tgt, 12-178, avg 7.3 tgt.
Alignment proxy (pass_location): right 16, middle 12, left 10. Mostly outside, with some middle in Wks 4-6.
Vs opponent season man rate (Sharp, season-level). Zone-heavy (CAR 11.6, MIN 5.3, PHI 15.1, GB 13.8): 44.8 yds/g. Man-heavier (NYJ 23.8, ATL 21.9, NE 30.8): 67.3 yds/g. Small sample. SEA is 90% zone, which does not favor him.
SEA vs WRs: 91.7 ypg (outside L/R 76.1, middle 15.6). The only 100-yard game was Evans 7-113. Next best: McLaurin 6-77, Harris 3-60, Hollins 4-51.
Injury: not on the latest injury report (no designation).
Rule check: with Caleb, WR targets go Burden 24, Raymond 18, Odunze 16, which makes Odunze CHI's WR3. That FAILS the no-#3/#4 WR rule.

| Rung | FD / nv | DK | MC / Bias / GR | Raw edge | Edge x0.7 | Shrink to 50 | Clear +3 (raw / x0.7 / to50) | §7 Caleb |
|---|---|---|---|---|---|---|---|---|
| Rec O1.5 | -600 / .801 | -539 | .838 / .880 / .810 | +3.8/+7.9/+0.9 | +2.6/+5.5/+0.6 | -6.4/-3.5/-8.4 | 2 / 1 / 0 | 4/4 |
| Rec O2.5 | -188 / .610 | -170 main | .638 / .707 / .626 | +2.8/+9.7/+1.6 | +1.9/+6.8/+1.1 | -1.4/+3.5/-2.2 | 1 / 1 / 1 | 3/4 |
| Yds O29.5 | -192 / .620 | -195 | .632 / .669 / .604 | +1.3/+5.0/-1.6 | +0.9/+3.5/-1.1 | -2.7/-0.1/-4.7 | 1 / 1 / 0 | 4/4 |
| Yds O38.5 (main) | -113 / .500 | -115 | .484 / .525 / .479 | -1.6/+2.5/-2.1 | -1.2/+1.8/-1.5 | same | 0 | 3/4 |
FD main rec 3.5 (+134/-180). Medians: 3 rec, 37-40 yds. No longest-reception market in our pull.
Verdicts: all rungs CUT. He is WR3 with Caleb (rule fail). Only Bias clears after any shrink, and Rec 1.5 is too thin to price at -600.
