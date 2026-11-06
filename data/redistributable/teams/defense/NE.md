# NE DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 NE@SEA, wk2 PIT@NE, wk3 NE@JAX, wk4 NE@BUF, wk5 LV@NE, wk6 NYJ@NE, wk7 NE@CHI, wk8 NE@MIA). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 30.8% / Zone 63.8% | MOF closed 51.0% / MOF open 45.4% | Blitz 40.2% | Light box 35.0% / Heavy box 29.6% | Sub package 76.0% | Sharp YPT allowed WR 8.8, TE 6.7, RB 6.5, Outside 8.4, Slot 10.5

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR1: 9.74 YPT on 54 tgts (league 8.16, +1.58), 8 catches of 20+
- depth deep_20+: 14.71 YPT on 24 tgts (league 12.32, +2.39), 12 catches of 20+
- depth/direction deep_left: 15.37 YPT on 19 tgts (league 11.28, +4.09), 8 catches of 20+
- depth/direction short_middle: 9.24 YPT on 41 tgts (league 7.43, +1.81), 3 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 40 | 31 | 248 | 0 | 2 | 6.20 | 5 | 31 | 5.61 | 0.59 |
| TE1 | 45 | 30 | 318 | 2 | 4 | 7.07 | 5.60 | 39.80 | 7.39 | -0.32 |
| TE2+ | 19 | 13 | 101 | 0 | 0 | 5.32 | 2.40 | 12.60 | 6.71 | -1.39 |
| WR1 | 54 | 39 | 526 | 4 | 8 | 9.74 | 6.80 | 65.80 | 8.16 | 1.58 |
| WR2 | 36 | 26 | 319 | 2 | 7 | 8.86 | 4.50 | 39.90 | 8.20 | 0.66 |
| WR3+ | 51 | 31 | 372 | 3 | 4 | 7.29 | 6.40 | 46.50 | 7.67 | -0.38 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 19 | 14 | 119 | 0 | 1 | 6.26 | 5.61 | 0.65 |
| TE1 | 31 | 20 | 234 | 2 | 3 | 7.55 | 7.39 | 0.16 |
| TE2+ | 14 | 10 | 81 | 0 | 0 | 5.79 | 6.71 | -0.92 |
| WR1 | 21 | 17 | 255 | 2 | 5 | 12.14 | 8.16 | 3.98 |
| WR2 | 10 | 8 | 100 | 0 | 3 | 10 | 8.20 | 1.80 |
| WR3+ | 31 | 19 | 273 | 2 | 3 | 8.81 | 7.67 | 1.14 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 51 | 43 | 258 | 1 | 2 | 5.06 | 4.58 | 0.48 |
| short_1-9 | 122 | 88 | 802 | 4 | 6 | 6.57 | 6.23 | 0.34 |
| inter_10-19 | 46 | 27 | 471 | 3 | 5 | 10.24 | 10.17 | 0.07 |
| deep_20+ | 24 | 12 | 353 | 3 | 12 | 14.71 | 12.32 | 2.39 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 19 | 10 | 292 | 3 | 8 | 15.37 | 11.28 | 4.09 |
| deep_middle | 8 | 5 | 147 | 1 | 4 | 18.38 | 14.90 | 3.48 |
| deep_right | 9 | 6 | 126 | 0 | 4 | 14 | 11.85 | 2.15 |
| short_left | 79 | 53 | 433 | 3 | 3 | 5.48 | 6.08 | -0.60 |
| short_middle | 41 | 33 | 379 | 2 | 3 | 9.24 | 7.43 | 1.81 |
| short_right | 87 | 63 | 507 | 2 | 3 | 5.83 | 5.95 | -0.12 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 42 | 29 | 351 | 2 | 8 | 8.36 | 8.94 | -0.58 |
| intermediate (aDOT 8-13) | 93 | 65 | 764 | 6 | 8 | 8.22 | 7.96 | 0.26 |
| short/YAC (aDOT <8) | 110 | 76 | 769 | 3 | 9 | 6.99 | 6.47 | 0.52 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 4, 'WR': 19} (25 total, 3.1/g)
- Pass 20+ by depth/direction: {'deep_left': 8, 'deep_middle': 4, 'deep_right': 4, 'short_left': 3, 'short_middle': 3, 'short_right': 3}
- Rush 15+ by position: {'QB': 1, 'RB': 4} (5 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 19 | 75 | 1 | 3.95 | 9.40 |
| RB | 164 | 658 | 4 | 4.01 | 82.20 |
| TE | 1 | 2 | 0 | 2 | 0.20 |
| WR | 6 | 9 | 0 | 1.50 | 1.10 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marcus Jones | CB | 8 | 80.50 | 26 | 3.20 | 20 | 239 | 29.90 | 9.19 | 0 | 5 | 5 | 1 | 0 |
| Christian Gonzalez | CB | 6 | 97.30 | 22 | 3.70 | 17 | 192 | 32 | 8.73 | 0 | 3 | 5 | 0 | 0 |
| Charles Woods | CB | 6 | 43.60 | 18 | 3 | 15 | 188 | 31.30 | 10.44 | 0 | 3 | 2 | 1 | 0 |
| Carlton Davis III | CB | 4 | 95.50 | 18 | 4.50 | 17 | 152 | 38 | 8.44 | 0 | 1 | 1 | 0 | 0 |
| Kindle Vildor | CB | 2 | 29.70 | 5 | 2.50 | 4 | 64 | 32 | 12.80 | 0 | 1 | 1 | 0 | 0 |
| Christian Elliss | LB | 8 | 96.60 | 23 | 2.90 | 22 | 137 | 17.10 | 5.96 | 0 | 0 | 1 | 0 | 0 |
| Robert Spillane | LB | 7 | 97.20 | 15 | 2.10 | 13 | 112 | 16 | 7.47 | 0 | 0 | 2 | 0 | 0 |
| Kevin Byard | S | 8 | 96.50 | 18 | 2.20 | 15 | 233 | 29.10 | 12.94 | 0 | 3 | 2 | 1 | 0 |
| Craig Woodson | S | 6 | 92.70 | 11 | 1.80 | 8 | 106 | 17.70 | 9.64 | 0 | 2 | 2 | 1 | 0 |
| Jaylen Reed | S | 3 | 33.80 | 4 | 1.30 | 4 | 35 | 11.70 | 8.75 | 0 | 1 | 0 | 0 | 0 |
| Mike Brown | S | 1 | 20.70 | 2 | 2 | 2 | 19 | 19 | 9.50 | 0 | 0 | 0 | 0 | 0 |
| Dell Pettus | S | 1 | 40 | 2 | 2 | 2 | 18 | 18 | 9 | 0 | 0 | 0 | 0 | 0 |
| Elliott Davison | S | 1 | 17 | 2 | 2 | 1 | 6 | 6 | 3 | 0 | 0 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Marcus Jones** (CB): TE1:6t/75y, WR3+:5t/74y, WR2:7t/60y, RB:4t/29y, WR1:3t/1y, TE2+:1t/0y | 20+: wk1 C.Kupp(WR3+) 24 deep_right; wk5 B.Bowers(TE1) 24 deep_left; wk5 B.Bowers(TE1) 27 short_middle; wk5 C.White(WR3+) 28 deep_left; wk7 R.Odunze(WR2) 21 deep_right
- **Christian Gonzalez** (CB): WR2:4t/59y, WR1:8t/57y, WR3+:4t/43y, TE2+:1t/14y, TE1:3t/13y, RB:2t/6y | 20+: wk7 R.Odunze(WR2) 21 deep_right; wk7 R.Odunze(WR2) 21 short_right; wk8 M.Washington(WR1) 23 deep_right
- **Charles Woods** (CB): WR1:2t/73y, RB:4t/42y, WR3+:6t/35y, WR2:2t/23y, TE2+:1t/9y, TE1:3t/6y | 20+: wk2 J.Warren(RB) 26 short_middle; wk4 K.Shakir(WR1) 51 deep_middle; wk7 L.Burden(WR1) 22 deep_middle
- **Carlton Davis III** (CB): TE1:5t/69y, WR3+:5t/44y, WR1:3t/19y, WR2:3t/13y, RB:2t/7y | 20+: wk3 B.Strange(TE1) 23 short_left
- **Kindle Vildor** (CB): WR1:2t/27y, WR2:1t/22y, TE1:2t/15y | 20+: wk4 K.Coleman(WR2) 22 deep_left
- **Christian Elliss** (LB): TE2+:7t/37y, TE1:4t/34y, WR2:2t/28y, RB:8t/26y, WR1:1t/6y, WR3+:1t/6y
- **Robert Spillane** (LB): RB:6t/55y, WR1:3t/29y, WR2:3t/15y, TE2+:1t/8y, WR3+:1t/5y, TE1:1t/0y
- **Kevin Byard** (S): WR1:6t/120y, RB:2t/42y, WR2:2t/27y, TE1:3t/18y, WR3+:3t/18y, TE2+:2t/8y | 20+: wk4 K.Coleman(WR2) 24 short_left; wk5 A.Jeanty(RB) 31 short_middle; wk7 L.Burden(WR1) 58 deep_left
- **Craig Woodson** (S): WR1:3t/50y, TE1:4t/30y, WR3+:2t/16y, RB:1t/10y, TE2+:1t/0y | 20+: wk1 J.Smith-Njigba(WR1) 21 deep_middle; wk7 L.Burden(WR1) 26 short_right
- **Jaylen Reed** (S): TE1:2t/24y, TE2+:1t/9y, WR3+:1t/2y | 20+: wk7 C.Loveland(TE1) 22 deep_left
- **Mike Brown** (S): RB:1t/11y, WR3+:1t/8y
- **Dell Pettus** (S): WR1:1t/11y, RB:1t/7y
- **Elliott Davison** (S): WR3+:2t/6y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NE@SEA | Robert Spillane | LB | 5 | 5 | 40 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax2, B.Russellx1, R.Shaheedx1, J.Pricex1 |
| 1 | NE@SEA | Marcus Jones | CB | 1 | 1 | 24 | 0 | 1 | 0 | 0 | 0 | C.Kuppx1 |
| 1 | NE@SEA | Craig Woodson | S | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 1 | NE@SEA | Christian Elliss | LB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1, J.Pricex1, A.Barnerx1 |
| 1 | NE@SEA | Dell Pettus | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | B.Russellx1, J.Smith-Njigbax1 |
| 1 | NE@SEA | Kevin Byard | S | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 1 | NE@SEA | Carlton Davis III | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | C.Kuppx1 |
| 1 | NE@SEA | Christian Gonzalez | CB | 3 | 1 | 4 | 0 | 0 | 2 | 0 | 0 | C.Kuppx1, A.Barnerx1, J.Smith-Njigbax1 |
| 2 | PIT@NE | Charles Woods | CB | 6 | 6 | 59 | 0 | 1 | 0 | 0 | 0 | R.Wilsonx3, R.Dowdlex1, G.Bernardx1, J.Warrenx1 |
| 2 | PIT@NE | Christian Elliss | LB | 5 | 5 | 48 | 0 | 0 | 0 | 0 | 0 | P.Freiermuthx2, D.Washingtonx1, G.Bernardx1, J.Warrenx1 |
| 2 | PIT@NE | Marcus Jones | CB | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | R.Dowdlex1, R.Wilsonx1 |
| 2 | PIT@NE | Christian Gonzalez | CB | 5 | 3 | 21 | 0 | 0 | 2 | 0 | 0 | D.Metcalfx3, P.Freiermuthx1, G.Bernardx1 |
| 2 | PIT@NE | Kevin Byard | S | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | G.Bernardx1, D.Metcalfx1 |
| 2 | PIT@NE | Craig Woodson | S | 3 | 2 | 12 | 0 | 0 | 1 | 0 | 0 | D.Metcalfx1, D.Washingtonx1, P.Freiermuthx1 |
| 2 | PIT@NE | Robert Spillane | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | R.Wilsonx1 |
| 2 | PIT@NE | Jaylen Reed | S | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | B.Skowronekx1 |
| 3 | NE@JAX | Carlton Davis III | CB | 8 | 7 | 63 | 0 | 1 | 1 | 0 | 0 | B.Strangex2, J.Meyersx2, Bri.Thomasx1, A.Abdullahx1, P.Washingtonx1, L.Allenx1 |
| 3 | NE@JAX | Robert Spillane | LB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1, B.Tutenx1 |
| 3 | NE@JAX | Kevin Byard | S | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | P.Washingtonx1 |
| 3 | NE@JAX | Christian Gonzalez | CB | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | L.Allenx1, B.Strangex1, J.Meyersx1 |
| 3 | NE@JAX | Charles Woods | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1 |
| 3 | NE@JAX | Marcus Jones | CB | 5 | 2 | 11 | 0 | 0 | 2 | 1 | 0 | B.Strangex2, J.Meyersx2, N.Boerkircherx1 |
| 3 | NE@JAX | Christian Elliss | LB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | B.Tutenx1 |
| 4 | NE@BUF | Charles Woods | CB | 2 | 2 | 54 | 0 | 1 | 0 | 0 | 0 | K.Shakirx1, J.Palmerx1 |
| 4 | NE@BUF | Kevin Byard | S | 3 | 2 | 30 | 0 | 1 | 1 | 0 | 0 | D.Kincaidx1, K.Shakirx1, K.Colemanx1 |
| 4 | NE@BUF | Kindle Vildor | CB | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | K.Colemanx1 |
| 4 | NE@BUF | Marcus Jones | CB | 5 | 4 | 20 | 0 | 0 | 1 | 0 | 0 | K.Colemanx2, K.Shakirx1, J.Cookx1, T.Johnsonx1 |
| 4 | NE@BUF | Carlton Davis III | CB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | D.Moorex1, K.Shakirx1, K.Colemanx1 |
| 4 | NE@BUF | Robert Spillane | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1, K.Shakirx1 |
| 4 | NE@BUF | Christian Elliss | LB | 3 | 3 | 15 | 0 | 0 | 0 | 0 | 0 | D.Knoxx2, J.Cookx1 |
| 4 | NE@BUF | Craig Woodson | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | J.Palmerx1 |
| 5 | LV@NE | Marcus Jones | CB | 4 | 4 | 97 | 0 | 3 | 0 | 0 | 0 | B.Bowersx3, C.Whitex1 |
| 5 | LV@NE | Kindle Vildor | CB | 4 | 3 | 42 | 0 | 0 | 1 | 0 | 0 | T.Tuckerx2, B.Bowersx2 |
| 5 | LV@NE | Kevin Byard | S | 1 | 1 | 31 | 0 | 1 | 0 | 0 | 0 | A.Jeantyx1 |
| 5 | LV@NE | Craig Woodson | S | 2 | 2 | 30 | 0 | 0 | 0 | 0 | 0 | C.Whitex1, B.Bowersx1 |
| 5 | LV@NE | Mike Brown | S | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, D.Thompkinsx1 |
| 5 | LV@NE | Christian Elliss | LB | 3 | 3 | 15 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1, A.Jeantyx1, M.Washingtonx1 |
| 5 | LV@NE | Elliott Davison | S | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | M.Bensonx2 |
| 5 | LV@NE | Charles Woods | CB | 4 | 2 | 4 | 0 | 0 | 2 | 0 | 0 | A.Jeantyx1, C.Whitex1, D.Laubex1, B.Bowersx1 |
| 6 | NYJ@NE | Christian Gonzalez | CB | 4 | 4 | 45 | 0 | 0 | 0 | 0 | 0 | O.Cooperx2, G.Wilsonx2 |
| 6 | NYJ@NE | Kevin Byard | S | 4 | 3 | 29 | 0 | 0 | 1 | 0 | 0 | M.Taylorx2, K.Sadiqx1, G.Wilsonx1 |
| 6 | NYJ@NE | Charles Woods | CB | 3 | 2 | 27 | 0 | 0 | 0 | 1 | 0 | M.Taylorx1, K.Sadiqx1, O.Cooperx1 |
| 6 | NYJ@NE | Robert Spillane | LB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | B.Allenx1 |
| 6 | NYJ@NE | Marcus Jones | CB | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | G.Wilsonx1, I.Davisx1, O.Cooperx1 |
| 6 | NYJ@NE | Christian Elliss | LB | 3 | 2 | 15 | 0 | 0 | 1 | 0 | 0 | O.Cooperx1, J.Woodsx1, M.Taylorx1 |
| 6 | NYJ@NE | Craig Woodson | S | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | B.Allenx1 |
| 6 | NYJ@NE | Jaylen Reed | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | M.Taylorx1 |
| 7 | NE@CHI | Kevin Byard | S | 3 | 3 | 75 | 0 | 1 | 0 | 0 | 0 | L.Burdenx1, D.Swiftx1, C.Lovelandx1 |
| 7 | NE@CHI | Christian Gonzalez | CB | 4 | 4 | 60 | 0 | 2 | 0 | 0 | 0 | R.Odunzex2, C.Kmetx1, D.Swiftx1 |
| 7 | NE@CHI | Craig Woodson | S | 3 | 2 | 33 | 0 | 1 | 1 | 0 | 0 | C.Lovelandx2, L.Burdenx1 |
| 7 | NE@CHI | Charles Woods | CB | 2 | 2 | 31 | 0 | 1 | 0 | 0 | 0 | L.Burdenx1, C.Lovelandx1 |
| 7 | NE@CHI | Jaylen Reed | S | 2 | 2 | 24 | 0 | 1 | 0 | 0 | 0 | C.Lovelandx2 |
| 7 | NE@CHI | Marcus Jones | CB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | R.Odunzex1 |
| 7 | NE@CHI | Robert Spillane | LB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | R.Odunzex1, C.Kmetx1 |
| 7 | NE@CHI | Christian Elliss | LB | 4 | 4 | 14 | 0 | 0 | 0 | 0 | 0 | D.Swiftx2, C.Lovelandx1, C.Kmetx1 |
| 8 | NE@MIA | Carlton Davis III | CB | 6 | 6 | 59 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx3, M.Washingtonx1, K.Colemanx1, J.Tolbertx1 |
| 8 | NE@MIA | Christian Gonzalez | CB | 3 | 3 | 46 | 0 | 1 | 0 | 0 | 0 | M.Washingtonx2, C.Douglasx1 |
| 8 | NE@MIA | Marcus Jones | CB | 5 | 4 | 28 | 0 | 0 | 1 | 0 | 0 | C.Bellx2, M.Washingtonx1, C.Douglasx1, G.Dulcichx1 |
| 8 | NE@MIA | Kevin Byard | S | 3 | 2 | 18 | 0 | 0 | 0 | 1 | 0 | C.Douglasx3 |
| 8 | NE@MIA | Christian Elliss | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | C.Bellx1 |
| 8 | NE@MIA | Robert Spillane | LB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | G.Dulcichx1, O.Gordonx1 |

## Who beat them each week

**Wk1 NE@SEA** (vs SEA offense, 200 rec yds allowed; 25% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 8/11 122y 1TD; C.Kupp (WR3+, intermediate (aDOT 8-13)) 2/3 35y; B.Russell (RB, short/YAC (aDOT <8)) 2/2 20y; A.Barner (TE1, short/YAC (aDOT <8)) 2/2 13y
- 20+ catches: J.Smith-Njigba(WR1) 21y deep_middle - C.Woodson [tackler]; C.Kupp(WR3+) 24y deep_right - M.Jones [tackler]; J.Smith-Njigba(WR1) 45y short_left TD - no tackler named [unattributed]

**Wk2 PIT@NE** (vs PIT offense, 187 rec yds allowed; 27% of targets unattributed)
- Top receivers: G.Bernard (WR2, short/YAC (aDOT <8)) 4/8 35y; J.Warren (RB, short/YAC (aDOT <8)) 2/4 34y; P.Freiermuth (TE1, intermediate (aDOT 8-13)) 4/5 32y; R.Wilson (WR3+, deep (aDOT 13+)) 5/6 28y
- 20+ catches: J.Warren(RB) 26y short_middle - C.Woods [tackler]

**Wk3 NE@JAX** (vs JAX offense, 182 rec yds allowed; 22% of targets unattributed)
- Top receivers: J.Meyers (WR2, intermediate (aDOT 8-13)) 7/8 64y 1TD; P.Washington (WR1, intermediate (aDOT 8-13)) 3/5 40y 1TD; B.Strange (TE1, short/YAC (aDOT <8)) 3/5 32y; B.Tuten (RB, short/YAC (aDOT <8)) 2/2 17y
- 20+ catches: B.Strange(TE1) 23y short_left - C.Davis [tackler]
- 15+ runs: T.Lawrence(QB) 15y rush left end

**Wk4 NE@BUF** (vs BUF offense, 253 rec yds allowed; 26% of targets unattributed)
- Top receivers: K.Coleman (WR2, deep (aDOT 13+)) 6/7 116y 1TD; K.Shakir (WR1, short/YAC (aDOT <8)) 7/8 82y; D.Knox (TE2+, short/YAC (aDOT <8)) 2/2 13y; D.Moore (WR3+, deep (aDOT 13+)) 1/2 11y
- 20+ catches: K.Shakir(WR1) 51y deep_middle - C.Woods [tackler]; K.Coleman(WR2) 22y deep_left - no tackler named [unattributed]; K.Coleman(WR2) 22y deep_left - K.Vildor [tackler]; K.Coleman(WR2) 24y short_left - K.Byard [tackler]; K.Coleman(WR2) 34y deep_middle TD - no tackler named [unattributed]
- 15+ runs: J.Cook(RB) 17y rush left end; J.Cook(RB) 16y rush left tackle

**Wk5 LV@NE** (vs LV offense, 291 rec yds allowed; 25% of targets unattributed)
- Top receivers: B.Bowers (TE1, intermediate (aDOT 8-13)) 8/10 110y 1TD; A.Jeanty (RB, short/YAC (aDOT <8)) 3/6 50y; C.White (WR3+, intermediate (aDOT 8-13)) 2/4 44y; T.Tucker (WR1, deep (aDOT 13+)) 4/5 41y
- 20+ catches: B.Bowers(TE1) 24y deep_left - M.Jones [tackler]; B.Bowers(TE1) 27y short_middle - M.Jones [tackler]; C.White(WR3+) 28y deep_left - M.Jones [tackler]; A.Jeanty(RB) 31y short_middle - K.Byard [tackler]

**Wk6 NYJ@NE** (vs NYJ offense, 252 rec yds allowed; 28% of targets unattributed)
- Top receivers: O.Cooper (WR3+, intermediate (aDOT 8-13)) 6/7 103y 1TD; G.Wilson (WR1, intermediate (aDOT 8-13)) 4/6 44y; M.Taylor (TE2+, intermediate (aDOT 8-13)) 4/6 33y; B.Allen (RB, short/YAC (aDOT <8)) 2/2 26y
- 20+ catches: O.Cooper(WR3+) 48y deep_left TD - no tackler named [unattributed]
- 15+ runs: B.Allen(RB) 16y rush left tackle

**Wk7 NE@CHI** (vs CHI offense, 308 rec yds allowed; 30% of targets unattributed)
- Top receivers: L.Burden (WR1, short/YAC (aDOT <8)) 4/4 130y 1TD; C.Loveland (TE1, short/YAC (aDOT <8)) 7/12 69y 1TD; R.Odunze (WR2, deep (aDOT 13+)) 4/5 69y; C.Kmet (TE2+, short/YAC (aDOT <8)) 3/3 28y
- 20+ catches: L.Burden(WR1) 26y short_right - C.Woodson [tackler]; L.Burden(WR1) 58y deep_left - K.Byard [tackler]; L.Burden(WR1) 22y deep_middle - C.Woods [tackler]; L.Burden(WR1) 24y short_right TD - no tackler named [unattributed]; C.Loveland(TE1) 22y deep_left - J.Reed [tackler]; R.Odunze(WR2) 21y deep_right - C.Gonzalez [tackler]; R.Odunze(WR2) 21y deep_right - M.Jones [tackler]; R.Odunze(WR2) 21y short_right - C.Gonzalez [tackler]

**Wk8 NE@MIA** (vs MIA offense, 211 rec yds allowed; 26% of targets unattributed)
- Top receivers: K.Coleman (WR3+, deep (aDOT 13+)) 3/3 46y 1TD; G.Dulcich (TE1, short/YAC (aDOT <8)) 4/6 43y; C.Douglas (WR3+, intermediate (aDOT 8-13)) 4/6 43y; M.Washington (WR1, intermediate (aDOT 8-13)) 5/6 40y 1TD
- 20+ catches: M.Washington(WR1) 23y deep_right - C.Gonzalez [tackler]; K.Coleman(WR3+) 35y deep_left TD - no tackler named [unattributed]
- 15+ runs: O.Gordon(RB) 16y rush middle

## Seed notes from defenders/NE_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 14:18 Malik Washington (WR) rec 23 — Marcus Jones [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Christian Gonzalez)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L25/S56/R18)
- Q2 0:34 Ollie Gordon II (RB) rush 15 — K.Byard [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 11:46 Ollie Gordon II (RB) rush 16 — C.Woodson [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Christian Gonzalez ← Caleb Douglas: 5 tgt, 4 rec, 43 yds
- Marcus Jones ← Malik Washington: 5 tgt, 4 rec, 39 yds
- Carlton Davis ← Kevin Coleman Jr.: 2 tgt, 2 rec, 11 yds

