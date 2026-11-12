# BUF DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 BUF@HOU, wk2 DET@BUF, wk3 LAC@BUF, wk4 NE@BUF, wk5 BUF@LAR, wk6 BUF@LV, wk8 BAL@BUF). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 16.8% / Zone 74.9% | MOF closed 45.8% / MOF open 49.2% | Blitz 27.5% | Light box 39.9% / Heavy box 33.1% | Sub package 61.0% | Sharp YPT allowed WR 8.1, TE 8.2, RB 5.6, Outside 7.7, Slot 10.0

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR3+: 9.67 YPT on 30 tgts (league 7.67, +2.0), 6 catches of 20+

Holds (-1.5 YPT or better): WR2: 6.7 YPT on 43 tgts (league 8.2, -1.5)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 62 | 42 | 311 | 3 | 2 | 5.02 | 8.90 | 44.40 | 5.61 | -0.59 |
| TE1 | 42 | 27 | 316 | 1 | 4 | 7.52 | 6 | 45.10 | 7.39 | 0.13 |
| TE2+ | 22 | 16 | 178 | 0 | 2 | 8.09 | 3.10 | 25.40 | 6.71 | 1.38 |
| WR1 | 65 | 42 | 500 | 5 | 10 | 7.69 | 9.30 | 71.40 | 8.16 | -0.47 |
| WR2 | 43 | 25 | 288 | 5 | 3 | 6.70 | 6.10 | 41.10 | 8.20 | -1.50 |
| WR3+ | 30 | 17 | 290 | 1 | 6 | 9.67 | 4.30 | 41.40 | 7.67 | 2 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 38 | 24 | 176 | 0 | 1 | 4.63 | 5.61 | -0.98 |
| TE1 | 24 | 17 | 229 | 0 | 4 | 9.54 | 7.39 | 2.15 |
| TE2+ | 18 | 12 | 149 | 0 | 2 | 8.28 | 6.71 | 1.57 |
| WR1 | 39 | 24 | 250 | 3 | 3 | 6.41 | 8.16 | -1.75 |
| WR2 | 23 | 13 | 140 | 4 | 1 | 6.09 | 8.20 | -2.11 |
| WR3+ | 14 | 7 | 112 | 1 | 2 | 8 | 7.67 | 0.33 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 47 | 35 | 182 | 1 | 0 | 3.87 | 4.58 | -0.71 |
| short_1-9 | 112 | 81 | 666 | 7 | 3 | 5.95 | 6.23 | -0.28 |
| inter_10-19 | 79 | 44 | 792 | 4 | 15 | 10.03 | 10.17 | -0.14 |
| deep_20+ | 25 | 9 | 243 | 3 | 9 | 9.72 | 12.32 | -2.60 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 17 | 8 | 196 | 0 | 5 | 11.53 | 11.28 | 0.25 |
| deep_middle | 13 | 5 | 146 | 2 | 5 | 11.23 | 14.90 | -3.67 |
| deep_right | 25 | 11 | 254 | 1 | 9 | 10.16 | 11.85 | -1.69 |
| short_left | 75 | 50 | 446 | 4 | 2 | 5.95 | 6.08 | -0.13 |
| short_middle | 50 | 34 | 352 | 4 | 3 | 7.04 | 7.43 | -0.39 |
| short_right | 83 | 61 | 489 | 4 | 3 | 5.89 | 5.95 | -0.06 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 45 | 28 | 386 | 6 | 5 | 8.58 | 8.94 | -0.36 |
| intermediate (aDOT 8-13) | 79 | 45 | 633 | 3 | 14 | 8.01 | 7.96 | 0.05 |
| short/YAC (aDOT <8) | 140 | 96 | 864 | 6 | 8 | 6.17 | 6.47 | -0.30 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 6, 'WR': 19} (27 total, 3.9/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 5, 'deep_right': 9, 'short_left': 2, 'short_middle': 3, 'short_right': 3}
- Rush 15+ by position: {'QB': 3, 'RB': 4} (7 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 17 | 99 | 3 | 5.82 | 14.10 |
| RB | 154 | 570 | 4 | 3.70 | 81.40 |
| WR | 3 | 16 | 0 | 5.33 | 2.30 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Christian Benford | CB | 6 | 92 | 25 | 4.20 | 19 | 191 | 31.80 | 7.64 | 0 | 3 | 6 | 0 | 0 |
| Davison Igbinosun | CB | 7 | 58.60 | 22 | 3.10 | 14 | 167 | 23.90 | 7.59 | 0 | 2 | 7 | 1 | 0 |
| Maxwell Hairston | CB | 7 | 61.10 | 11 | 1.60 | 9 | 109 | 15.60 | 9.91 | 0 | 1 | 2 | 0 | 0 |
| Jordan Hancock | CB | 1 | 20 | 5 | 5 | 5 | 63 | 63 | 12.60 | 0 | 1 | 0 | 0 | 0 |
| Dee Alford | CB | 4 | 53.60 | 5 | 1.20 | 3 | 38 | 9.50 | 7.60 | 0 | 0 | 1 | 1 | 0 |
| Te'Cory Couch | CB | 1 | 71 | 2 | 2 | 2 | 7 | 7 | 3.50 | 0 | 0 | 0 | 0 | 0 |
| Anthony Kendall | CB | 1 | 38 | 1 | 1 | 1 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| Terrel Bernard | LB | 7 | 90.90 | 19 | 2.70 | 18 | 179 | 25.60 | 9.42 | 0 | 2 | 1 | 0 | 0 |
| Dorian Williams | LB | 6 | 65.40 | 17 | 2.80 | 15 | 107 | 17.80 | 6.29 | 0 | 0 | 1 | 1 | 0 |
| Kaleb Elarms-Orr | LB | 5 | 18.70 | 7 | 1.40 | 6 | 83 | 16.60 | 11.86 | 0 | 2 | 1 | 0 | 0 |
| Greg Rousseau | OLB | 5 | 75.70 | 9 | 1.80 | 2 | 7 | 1.40 | 0.78 | 0 | 0 | 7 | 0 | 0 |
| Cole Bishop | S | 7 | 97 | 25 | 3.60 | 23 | 279 | 39.90 | 11.16 | 0 | 3 | 2 | 0 | 0 |
| C.J. Gardner-Johnson | S | 5 | 89.30 | 17 | 3.40 | 15 | 250 | 50 | 14.71 | 0 | 7 | 1 | 1 | 0 |
| Damar Hamlin | S | 5 | 44.30 | 11 | 2.20 | 10 | 141 | 28.20 | 12.82 | 0 | 3 | 1 | 0 | 0 |
| Geno Stone | S | 1 | 37 | 2 | 2 | 2 | 7 | 7 | 3.50 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Christian Benford** (CB): WR1:10t/91y, WR2:5t/36y, WR3+:3t/32y, TE1:5t/29y, TE2+:1t/3y, RB:1t/0y | 20+: wk2 A.St. Brown(WR1) 21 deep_right; wk2 I.TeSlaa(WR3+) 20 deep_left; wk3 T.Harris(WR1) 29 deep_right
- **Davison Igbinosun** (CB): WR1:10t/87y, WR3+:4t/53y, WR2:4t/13y, TE2+:1t/9y, RB:3t/5y | 20+: wk2 A.St. Brown(WR1) 34 deep_left; wk4 M.Hollins(WR3+) 26 deep_right
- **Maxwell Hairston** (CB): WR3+:4t/43y, WR2:3t/31y, WR1:1t/20y, TE2+:1t/16y, RB:2t/-1y | 20+: wk1 X.Hutchinson(WR1) 20 short_middle
- **Jordan Hancock** (CB): TE1:2t/30y, WR1:2t/27y, WR3+:1t/6y | 20+: wk2 A.St. Brown(WR1) 22 short_right
- **Dee Alford** (CB): TE1:2t/18y, WR1:1t/11y, WR2:2t/9y
- **Te'Cory Couch** (CB): RB:1t/7y, TE1:1t/0y
- **Anthony Kendall** (CB): RB:1t/3y
- **Terrel Bernard** (LB): RB:7t/44y, WR1:2t/31y, WR3+:2t/29y, TE1:3t/27y, WR2:2t/26y, TE2+:3t/22y | 20+: wk3 T.Harris(WR1) 23 deep_right; wk3 L.McConkey(WR3+) 29 deep_right
- **Dorian Williams** (LB): RB:7t/57y, TE1:3t/24y, WR1:5t/17y, TE2+:2t/9y
- **Kaleb Elarms-Orr** (LB): RB:2t/34y, TE2+:1t/28y, WR1:3t/12y, TE1:1t/9y | 20+: wk3 A.Ingold(RB) 25 short_right; wk6 M.Mayer(TE2+) 28 deep_middle
- **Greg Rousseau** (OLB): RB:3t/7y, TE1:2t/0y, WR1:2t/0y, WR2:1t/0y, WR3+:1t/0y
- **Cole Bishop** (S): TE1:5t/87y, RB:6t/59y, WR1:3t/41y, WR2:4t/41y, TE2+:5t/40y, WR3+:2t/11y | 20+: wk5 T.Higbee(TE1) 28 deep_left; wk5 T.Higbee(TE1) 30 deep_left; wk5 P.Nacua(WR1) 21 deep_right
- **C.J. Gardner-Johnson** (S): WR3+:4t/74y, RB:3t/53y, WR1:4t/42y, WR2:3t/37y, TE2+:2t/24y, TE1:1t/20y | 20+: wk1 N.Collins(WR2) 25 deep_right; wk1 J.Noel(WR3+) 35 short_middle; wk1 K.Boutte(WR3+) 21 short_middle; wk4 H.Henry(TE1) 20 short_left; wk5 B.Corum(RB) 34 short_left; wk5 D.Allen(TE2+) 21 deep_middle; wk6 T.Tucker(WR1) 26 deep_middle
- **Damar Hamlin** (S): TE1:3t/55y, WR2:2t/43y, RB:4t/27y, WR1:2t/16y | 20+: wk3 Q.Johnston(WR2) 21 short_right; wk6 B.Bowers(TE1) 29 deep_left; wk8 R.Bateman(WR2) 22 deep_right
- **Geno Stone** (S): TE1:1t/8y, RB:1t/-1y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BUF@HOU | C.J. Gardner-Johnson | S | 6 | 6 | 114 | 0 | 3 | 0 | 0 | 0 | N.Collinsx2, J.Noelx2, X.Hutchinsonx1, K.Bouttex1 |
| 1 | BUF@HOU | Maxwell Hairston | CB | 2 | 2 | 36 | 0 | 1 | 0 | 0 | 0 | M.Kleinx1, X.Hutchinsonx1 |
| 1 | BUF@HOU | Christian Benford | CB | 4 | 4 | 29 | 0 | 0 | 0 | 0 | 0 | N.Collinsx2, X.Hutchinsonx1, J.Waynex1 |
| 1 | BUF@HOU | Dee Alford | CB | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1 |
| 1 | BUF@HOU | Cole Bishop | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | F.Moreaux1, N.Collinsx1 |
| 1 | BUF@HOU | Dorian Williams | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | D.Montgomeryx2 |
| 1 | BUF@HOU | Davison Igbinosun | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | X.Hutchinsonx1, F.Moreaux1 |
| 1 | BUF@HOU | Kaleb Elarms-Orr | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1 |
| 1 | BUF@HOU | Damar Hamlin | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1 |
| 1 | BUF@HOU | Terrel Bernard | LB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | N.Collinsx1, C.Stoverx1 |
| 1 | BUF@HOU | Greg Rousseau | OLB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Schultzx1 |
| 2 | DET@BUF | Jordan Hancock | CB | 5 | 5 | 63 | 0 | 1 | 0 | 0 | 0 | S.LaPortax2, A.St. Brownx2, I.TeSlaax1 |
| 2 | DET@BUF | Davison Igbinosun | CB | 2 | 2 | 45 | 0 | 1 | 0 | 0 | 0 | A.St. Brownx2 |
| 2 | DET@BUF | Christian Benford | CB | 4 | 2 | 41 | 0 | 2 | 2 | 0 | 0 | A.St. Brownx2, I.TeSlaax2 |
| 2 | DET@BUF | Terrel Bernard | LB | 4 | 3 | 38 | 0 | 0 | 1 | 0 | 0 | S.LaPortax1, I.TeSlaax1, J.Gibbsx1, J.Williamsx1 |
| 2 | DET@BUF | Cole Bishop | S | 4 | 4 | 36 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx2, A.St. Brownx1, S.LaPortax1 |
| 2 | DET@BUF | Dorian Williams | LB | 4 | 3 | 27 | 0 | 0 | 1 | 0 | 0 | S.LaPortax1, J.Gibbsx1, S.Vakix1, A.St. Brownx1 |
| 2 | DET@BUF | Maxwell Hairston | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | J.Williamsx1 |
| 2 | DET@BUF | Dee Alford | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1 |
| 2 | DET@BUF | Kaleb Elarms-Orr | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx1 |
| 3 | LAC@BUF | Terrel Bernard | LB | 2 | 2 | 52 | 0 | 2 | 0 | 0 | 0 | T.Harrisx1, L.McConkeyx1 |
| 3 | LAC@BUF | Christian Benford | CB | 3 | 2 | 42 | 0 | 1 | 1 | 0 | 0 | T.Harrisx2, Q.Johnstonx1 |
| 3 | LAC@BUF | C.J. Gardner-Johnson | S | 5 | 3 | 27 | 0 | 0 | 1 | 1 | 0 | A.Ingoldx1, Q.Johnstonx1, T.Harrisx1, M.Valdes-Scantlingx1, K.Vidalx1 |
| 3 | LAC@BUF | Kaleb Elarms-Orr | LB | 1 | 1 | 25 | 0 | 1 | 0 | 0 | 0 | A.Ingoldx1 |
| 3 | LAC@BUF | Damar Hamlin | S | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | Q.Johnstonx1 |
| 3 | LAC@BUF | Cole Bishop | S | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | Q.Johnstonx1, L.McConkeyx1 |
| 3 | LAC@BUF | Davison Igbinosun | CB | 4 | 3 | 16 | 0 | 0 | 1 | 0 | 0 | T.Harrisx2, Q.Johnstonx1, K.Mitchellx1 |
| 3 | LAC@BUF | Maxwell Hairston | CB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | A.Ingoldx1, L.McConkeyx1 |
| 3 | LAC@BUF | Dorian Williams | LB | 2 | 2 | 5 | 0 | 0 | 0 | 0 | 0 | T.Harrisx1, A.Ingoldx1 |
| 3 | LAC@BUF | Greg Rousseau | OLB | 1 | 1 | -6 | 0 | 0 | 0 | 0 | 0 | K.Mitchellx1 |
| 4 | NE@BUF | Davison Igbinosun | CB | 4 | 3 | 53 | 0 | 1 | 1 | 0 | 0 | M.Hollinsx3, R.Stevensonx1 |
| 4 | NE@BUF | Cole Bishop | S | 3 | 3 | 36 | 0 | 0 | 0 | 0 | 0 | E.Raridonx1, R.Doubsx1, H.Henryx1 |
| 4 | NE@BUF | Maxwell Hairston | CB | 3 | 2 | 34 | 0 | 0 | 1 | 0 | 0 | R.Doubsx2, E.Chismx1 |
| 4 | NE@BUF | Dorian Williams | LB | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | H.Henryx2, R.Stevensonx1 |
| 4 | NE@BUF | C.J. Gardner-Johnson | S | 2 | 2 | 25 | 0 | 1 | 0 | 0 | 0 | H.Henryx1, D.Douglasx1 |
| 4 | NE@BUF | Greg Rousseau | OLB | 3 | 1 | 13 | 0 | 0 | 2 | 0 | 0 | E.Chismx1, R.Doubsx1, R.Stevensonx1 |
| 4 | NE@BUF | Terrel Bernard | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | R.Stevensonx1 |
| 4 | NE@BUF | Dee Alford | CB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | R.Doubsx1 |
| 5 | BUF@LAR | Cole Bishop | S | 7 | 7 | 124 | 0 | 3 | 0 | 0 | 0 | T.Higbeex3, P.Nacuax2, B.Corumx1, D.Adamsx1 |
| 5 | BUF@LAR | C.J. Gardner-Johnson | S | 3 | 3 | 58 | 0 | 2 | 0 | 0 | 0 | D.Allenx2, B.Corumx1 |
| 5 | BUF@LAR | Christian Benford | CB | 9 | 9 | 56 | 0 | 0 | 0 | 0 | 0 | P.Nacuax5, C.Parkinsonx1, K.Williamsx1, T.Higbeex1, D.Adamsx1 |
| 5 | BUF@LAR | Davison Igbinosun | CB | 5 | 4 | 33 | 0 | 0 | 1 | 0 | 0 | P.Nacuax3, D.Adamsx1, K.Williamsx1 |
| 5 | BUF@LAR | Terrel Bernard | LB | 4 | 4 | 32 | 0 | 0 | 0 | 0 | 0 | T.Higbeex1, B.Corumx1, P.Nacuax1, K.Williamsx1 |
| 5 | BUF@LAR | Damar Hamlin | S | 3 | 3 | 29 | 0 | 0 | 0 | 0 | 0 | K.Williamsx2, P.Nacuax1 |
| 5 | BUF@LAR | Dorian Williams | LB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | P.Nacuax3 |
| 5 | BUF@LAR | Kaleb Elarms-Orr | LB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | P.Nacuax2 |
| 5 | BUF@LAR | Maxwell Hairston | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | T.Atwellx1 |
| 5 | BUF@LAR | Anthony Kendall | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | K.Williamsx1 |
| 6 | BUF@LV | Damar Hamlin | S | 2 | 2 | 47 | 0 | 1 | 0 | 0 | 0 | B.Bowersx2 |
| 6 | BUF@LV | Cole Bishop | S | 6 | 4 | 36 | 0 | 0 | 2 | 0 | 0 | A.Jeantyx3, M.Mayerx2, C.Whitex1 |
| 6 | BUF@LV | Kaleb Elarms-Orr | LB | 2 | 2 | 33 | 0 | 1 | 0 | 0 | 0 | T.Tuckerx1, M.Mayerx1 |
| 6 | BUF@LV | Terrel Bernard | LB | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | M.Mayerx2, A.Jeantyx1 |
| 6 | BUF@LV | C.J. Gardner-Johnson | S | 1 | 1 | 26 | 0 | 1 | 0 | 0 | 0 | T.Tuckerx1 |
| 6 | BUF@LV | Christian Benford | CB | 4 | 2 | 23 | 0 | 0 | 2 | 0 | 0 | B.Bowersx4 |
| 6 | BUF@LV | Dorian Williams | LB | 3 | 2 | 16 | 0 | 0 | 0 | 1 | 0 | M.Mayerx2, M.Washingtonx1 |
| 6 | BUF@LV | Davison Igbinosun | CB | 4 | 1 | 11 | 0 | 0 | 3 | 0 | 0 | J.Nailorx2, C.Whitex1, T.Tuckerx1 |
| 6 | BUF@LV | Dee Alford | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | J.Nailorx1, B.Bowersx1 |
| 6 | BUF@LV | Greg Rousseau | OLB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | A.Jeantyx1, B.Bowersx1 |
| 6 | BUF@LV | Maxwell Hairston | CB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | 0 | D.Laubex1 |
| 8 | BAL@BUF | Damar Hamlin | S | 4 | 3 | 36 | 0 | 1 | 1 | 0 | 0 | J.Hillx2, R.Batemanx1, Z.Flowersx1 |
| 8 | BAL@BUF | Cole Bishop | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | J.Cuevasx1 |
| 8 | BAL@BUF | Terrel Bernard | LB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | D.Henryx2, M.Andrewsx1 |
| 8 | BAL@BUF | Maxwell Hairston | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | J.Lanex1 |
| 8 | BAL@BUF | Geno Stone | S | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | J.Hillx1, M.Andrewsx1 |
| 8 | BAL@BUF | Te'Cory Couch | CB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | J.Hillx1, M.Andrewsx1 |
| 8 | BAL@BUF | Greg Rousseau | OLB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | Z.Flowersx2 |
| 8 | BAL@BUF | Christian Benford | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | R.Batemanx1 |
| 8 | BAL@BUF | Davison Igbinosun | CB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Z.Flowersx1 |

## Who beat them each week

**Wk1 BUF@HOU** (vs HOU offense, 274 rec yds allowed; 30% of targets unattributed)
- Top receivers: N.Collins (WR2, intermediate (aDOT 8-13)) 7/10 75y 1TD; J.Noel (WR3+, intermediate (aDOT 8-13)) 2/2 53y; D.Schultz (TE1, short/YAC (aDOT <8)) 4/8 35y; X.Hutchinson (WR1, intermediate (aDOT 8-13)) 3/6 32y
- 20+ catches: N.Collins(WR2) 25y deep_right - C.Gardner-Johnson [tackler]; J.Noel(WR3+) 35y short_middle - C.Gardner-Johnson [tackler]; K.Boutte(WR3+) 21y short_middle - C.Gardner-Johnson [tackler]; X.Hutchinson(WR1) 20y short_middle - M.Hairston [tackler]
- 15+ runs: C.Stroud(QB) 15y rush middle; D.Montgomery(RB) 18y rush middle

**Wk2 DET@BUF** (vs DET offense, 327 rec yds allowed; 24% of targets unattributed)
- Top receivers: A.St. Brown (WR1, intermediate (aDOT 8-13)) 9/13 142y 2TD; J.Gibbs (RB, short/YAC (aDOT <8)) 6/8 61y 1TD; S.LaPorta (TE1, short/YAC (aDOT <8)) 6/7 52y 1TD; J.Williams (WR2, deep (aDOT 13+)) 2/4 33y
- 20+ catches: A.St. Brown(WR1) 22y short_right - J.Hancock [tackler]; A.St. Brown(WR1) 21y deep_right - C.Benford [tackler]; A.St. Brown(WR1) 34y deep_left - D.Igbinosun [tackler]; I.TeSlaa(WR3+) 20y deep_left - C.Benford [tackler]; A.St. Brown(WR1) 27y deep_middle TD - no tackler named [unattributed]
- 15+ runs: J.Gibbs(RB) 16y rush right tackle

**Wk3 LAC@BUF** (vs LAC offense, 226 rec yds allowed; 24% of targets unattributed)
- Top receivers: T.Harris (WR1, intermediate (aDOT 8-13)) 6/7 76y; L.McConkey (WR3+, intermediate (aDOT 8-13)) 4/5 66y; Q.Johnston (WR2, deep (aDOT 13+)) 3/6 40y; A.Ingold (RB, intermediate (aDOT 8-13)) 3/4 35y
- 20+ catches: A.Ingold(RB) 25y short_right - K.Elarms-Orr [tackler]; Q.Johnston(WR2) 21y short_right - D.Hamlin [tackler]; T.Harris(WR1) 29y deep_right - C.Benford [tackler]; T.Harris(WR1) 23y deep_right - T.Bernard [tackler]; L.McConkey(WR3+) 29y deep_right - T.Bernard [tackler]
- 15+ runs: K.Mitchell(RB) 17y rush left end

**Wk4 NE@BUF** (vs NE offense, 269 rec yds allowed; 41% of targets unattributed)
- Top receivers: H.Henry (TE1, short/YAC (aDOT <8)) 5/5 62y; R.Doubs (WR2, deep (aDOT 13+)) 6/9 58y 2TD; M.Hollins (WR3+, deep (aDOT 13+)) 3/4 53y; E.Chism (WR3+, short/YAC (aDOT <8)) 2/4 42y 1TD
- 20+ catches: H.Henry(TE1) 20y short_left - C.Gardner-Johnson [tackler]; M.Hollins(WR3+) 26y deep_right - D.Igbinosun [tackler]; E.Chism(WR3+) 23y deep_right TD - no tackler named [unattributed]
- 15+ runs: D.Maye(QB) 15y rush left guard; D.Maye(QB) 26y rush left end

**Wk5 BUF@LAR** (vs LAR offense, 383 rec yds allowed; 30% of targets unattributed)
- Top receivers: P.Nacua (WR1, short/YAC (aDOT <8)) 17/24 138y 1TD; T.Higbee (TE1, short/YAC (aDOT <8)) 5/6 83y; B.Corum (RB, short/YAC (aDOT <8)) 3/4 53y; D.Adams (WR2, deep (aDOT 13+)) 5/7 51y 2TD
- 20+ catches: T.Higbee(TE1) 28y deep_left - C.Bishop [tackler]; B.Corum(RB) 34y short_left - C.Gardner-Johnson [tackler]; T.Higbee(TE1) 30y deep_left - C.Bishop [tackler]; D.Allen(TE2+) 21y deep_middle - C.Gardner-Johnson [tackler]; P.Nacua(WR1) 21y deep_right - C.Bishop [tackler]

**Wk6 BUF@LV** (vs LV offense, 313 rec yds allowed; 18% of targets unattributed)
- Top receivers: T.Tucker (WR1, deep (aDOT 13+)) 5/7 97y 2TD; M.Mayer (TE2+, short/YAC (aDOT <8)) 7/9 95y; B.Bowers (TE1, intermediate (aDOT 8-13)) 4/9 70y; A.Jeanty (RB, short/YAC (aDOT <8)) 4/6 36y
- 20+ catches: T.Tucker(WR1) 26y deep_middle - C.Gardner-Johnson [tackler]; M.Mayer(TE2+) 28y deep_middle - K.Elarms-Orr [tackler]; B.Bowers(TE1) 29y deep_left - D.Hamlin [tackler]; T.Tucker(WR1) 44y deep_middle TD - no tackler named [unattributed]
- 15+ runs: M.Washington(RB) 18y rush middle

**Wk8 BAL@BUF** (vs BAL offense, 91 rec yds allowed; 31% of targets unattributed)
- Top receivers: R.Bateman (WR2, deep (aDOT 13+)) 1/3 22y; J.Hill (RB, short/YAC (aDOT <8)) 4/8 20y; J.Cuevas (TE2+, short/YAC (aDOT <8)) 1/2 15y; M.Andrews (TE1, short/YAC (aDOT <8)) 3/4 14y
- 20+ catches: R.Bateman(WR2) 22y deep_right - D.Hamlin [tackler]

## Seed notes from defenders/BUF_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q3 14:06 Rashod Bateman (WR) rec 22 — Davison Igbinosun [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Maxwell Hairston)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L31/S32/R37)
- Davison Igbinosun ← Rashod Bateman: 3 tgt, 1 rec, 22 yds
- Christian Benford ← Ja'Kobi Lane: 1 tgt, 1 rec, 13 yds
- Dee Alford ← Zay Flowers: 4 tgt, 0 rec, 0 yds — limited his man

