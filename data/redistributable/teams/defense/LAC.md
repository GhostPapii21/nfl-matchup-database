# LAC DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 ARI@LAC, wk2 LV@LAC, wk3 LAC@BUF, wk4 LAC@SEA, wk5 DEN@LAC, wk6 LAC@KC, wk8 LAC@LAR). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 10.6% / Zone 58.0% | MOF closed 33.9% / MOF open 40.7% | Blitz 21.7% | Light box 37.6% / Heavy box 21.3% | Sub package 57.0% | Sharp YPT allowed WR 8.9, TE 9.1, RB 4.5, Outside 10.2, Slot 7.4

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE1: 8.9 YPT on 30 tgts (league 7.39, +1.51), 4 catches of 20+
- type TE2+: 8.33 YPT on 12 tgts (league 6.71, +1.62), 1 catches of 20+
- depth deep_20+: 17.56 YPT on 16 tgts (league 12.32, +5.24), 8 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 36 | 24 | 157 | 1 | 2 | 4.36 | 5.10 | 22.40 | 5.61 | -1.25 |
| TE1 | 30 | 21 | 267 | 1 | 4 | 8.90 | 4.30 | 38.10 | 7.39 | 1.51 |
| TE2+ | 12 | 10 | 100 | 0 | 1 | 8.33 | 1.70 | 14.30 | 6.71 | 1.62 |
| WR1 | 47 | 36 | 429 | 2 | 4 | 9.13 | 6.70 | 61.30 | 8.16 | 0.97 |
| WR2 | 19 | 13 | 159 | 1 | 2 | 8.37 | 2.70 | 22.70 | 8.20 | 0.17 |
| WR3+ | 43 | 26 | 341 | 3 | 5 | 7.93 | 6.10 | 48.70 | 7.67 | 0.26 |
| other | 1 | 1 | 1 | 0 | 0 | 1 | 0.10 | 0.10 | 2.86 | -1.86 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 17 | 12 | 74 | 1 | 1 | 4.35 | 5.61 | -1.26 |
| TE1 | 14 | 10 | 134 | 0 | 2 | 9.57 | 7.39 | 2.18 |
| TE2+ | 5 | 5 | 61 | 0 | 1 | 12.20 | 6.71 | 5.49 |
| WR1 | 30 | 25 | 248 | 1 | 2 | 8.27 | 8.16 | 0.11 |
| WR2 | 6 | 3 | 38 | 1 | 1 | 6.33 | 8.20 | -1.87 |
| WR3+ | 24 | 14 | 165 | 1 | 2 | 6.88 | 7.67 | -0.79 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 39 | 33 | 167 | 2 | 1 | 4.28 | 4.58 | -0.30 |
| short_1-9 | 89 | 64 | 608 | 3 | 3 | 6.83 | 6.23 | 0.60 |
| inter_10-19 | 44 | 26 | 398 | 2 | 6 | 9.05 | 10.17 | -1.12 |
| deep_20+ | 16 | 8 | 281 | 1 | 8 | 17.56 | 12.32 | 5.24 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 11 | 5 | 189 | 1 | 5 | 17.18 | 11.28 | 5.90 |
| deep_middle | 3 | 1 | 23 | 0 | 1 | 7.67 | 14.90 | -7.23 |
| deep_right | 7 | 5 | 129 | 0 | 4 | 18.43 | 11.85 | 6.58 |
| short_left | 58 | 42 | 380 | 3 | 3 | 6.55 | 6.08 | 0.47 |
| short_middle | 40 | 27 | 296 | 0 | 2 | 7.40 | 7.43 | -0.03 |
| short_right | 69 | 51 | 437 | 4 | 3 | 6.33 | 5.95 | 0.38 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 32 | 17 | 324 | 1 | 5 | 10.12 | 8.94 | 1.18 |
| intermediate (aDOT 8-13) | 47 | 34 | 431 | 4 | 7 | 9.17 | 7.96 | 1.21 |
| short/YAC (aDOT <8) | 109 | 80 | 699 | 3 | 6 | 6.41 | 6.47 | -0.06 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 5, 'WR': 11} (18 total, 2.6/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 1, 'deep_right': 4, 'short_left': 3, 'short_middle': 2, 'short_right': 3}
- Rush 15+ by position: {'RB': 9, 'WR': 1} (10 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 19 | 81 | 0 | 4.26 | 11.60 |
| RB | 177 | 758 | 9 | 4.28 | 108.30 |
| TE | 1 | 0 | 0 | 0 | 0 |
| WR | 4 | 45 | 1 | 11.25 | 6.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cam Hart | CB | 6 | 91.40 | 19 | 3.20 | 13 | 199 | 33.20 | 10.47 | 0 | 3 | 4 | 2 | 0 |
| Tarheeb Still | CB | 7 | 93.40 | 16 | 2.30 | 12 | 176 | 25.10 | 11 | 0 | 3 | 3 | 1 | 0 |
| Rodney Shelley | CB | 2 | 12.30 | 3 | 1.50 | 3 | 73 | 36.50 | 24.33 | 0 | 2 | 0 | 0 | 0 |
| Donte Jackson | CB | 4 | 41.50 | 7 | 1.80 | 5 | 57 | 14.20 | 8.14 | 0 | 1 | 2 | 0 | 0 |
| Deane Leonard | CB | 2 | 32 | 4 | 2 | 4 | 43 | 21.50 | 10.75 | 0 | 0 | 0 | 0 | 0 |
| Isas Waxter | CB | 1 | 37 | 5 | 5 | 5 | 16 | 16 | 3.20 | 0 | 0 | 0 | 0 | 0 |
| Daiyan Henley | LB | 6 | 86.90 | 15 | 2.50 | 14 | 137 | 22.80 | 9.13 | 0 | 1 | 1 | 0 | 0 |
| Del'Shawn Phillips | LB | 5 | 66 | 7 | 1.40 | 7 | 45 | 9 | 6.43 | 0 | 0 | 0 | 0 | 0 |
| Troy Dye | LB | 4 | 18.30 | 7 | 1.80 | 6 | 41 | 10.20 | 5.86 | 0 | 0 | 1 | 0 | 0 |
| Elijah Molden | S | 5 | 74.40 | 10 | 2 | 10 | 138 | 27.60 | 13.80 | 0 | 2 | 0 | 0 | 0 |
| Genesis Smith | S | 5 | 47.60 | 10 | 2 | 7 | 98 | 19.60 | 9.80 | 0 | 2 | 1 | 2 | 0 |
| Tony Jefferson | S | 6 | 68.10 | 12 | 2 | 10 | 96 | 16 | 8 | 0 | 0 | 2 | 0 | 0 |
| Derwin James | S | 3 | 94.30 | 9 | 3 | 8 | 65 | 21.70 | 7.22 | 0 | 0 | 1 | 0 | 0 |
| R.J. Mickens | S | 4 | 38.20 | 5 | 1.20 | 5 | 32 | 8 | 6.40 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Cam Hart** (CB): WR1:9t/99y, WR3+:3t/38y, TE1:2t/34y, WR2:4t/28y, TE2+:1t/0y | 20+: wk1 M.Harrison(WR3+) 33 deep_left; wk2 T.Tucker(WR1) 42 deep_left; wk5 E.Engram(TE1) 34 deep_left
- **Tarheeb Still** (CB): WR3+:10t/111y, WR1:4t/32y, TE1:1t/24y, WR2:1t/9y | 20+: wk2 D.Young(WR3+) 27 short_left; wk3 D.Kincaid(TE1) 24 short_middle; wk8 T.Atwell(WR3+) 40 deep_left
- **Rodney Shelley** (CB): WR2:2t/57y, WR3+:1t/16y | 20+: wk3 K.Coleman(WR2) 37 deep_right; wk4 R.Shaheed(WR2) 20 deep_right
- **Donte Jackson** (CB): WR1:5t/37y, WR3+:1t/20y, WR2:1t/0y | 20+: wk2 J.Bech(WR3+) 20 short_left
- **Deane Leonard** (CB): WR1:2t/19y, WR3+:1t/13y, TE1:1t/11y
- **Isas Waxter** (CB): WR3+:1t/12y, TE2+:1t/2y, WR1:3t/2y
- **Daiyan Henley** (LB): TE1:5t/64y, WR1:4t/48y, WR3+:2t/14y, RB:4t/11y | 20+: wk4 J.Smith-Njigba(WR1) 20 short_right
- **Del'Shawn Phillips** (LB): TE2+:3t/26y, WR2:1t/13y, RB:3t/6y
- **Troy Dye** (LB): WR1:3t/21y, RB:3t/15y, TE2+:1t/5y
- **Elijah Molden** (S): TE1:3t/45y, TE2+:3t/43y, WR1:1t/19y, WR3+:1t/13y, WR2:1t/12y, RB:1t/6y | 20+: wk1 T.McBride(TE1) 27 deep_right; wk6 N.Gray(TE2+) 31 short_right
- **Genesis Smith** (S): WR3+:4t/35y, WR1:2t/28y, RB:1t/16y, WR2:2t/14y, TE1:1t/5y | 20+: wk4 J.Smith-Njigba(WR1) 28 deep_right; wk6 C.Allen(WR3+) 23 deep_middle
- **Tony Jefferson** (S): WR1:4t/52y, WR3+:2t/18y, TE2+:1t/16y, RB:2t/9y, TE1:3t/1y
- **Derwin James** (S): TE1:4t/26y, WR2:2t/21y, RB:2t/10y, WR3+:1t/8y
- **R.J. Mickens** (S): TE1:1t/14y, WR3+:1t/8y, WR1:1t/6y, RB:2t/4y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ARI@LAC | Cam Hart | CB | 7 | 6 | 81 | 0 | 1 | 1 | 0 | 0 | K.Bournex3, Mi.Wilsonx3, M.Harrisonx1 |
| 1 | ARI@LAC | Derwin James | S | 7 | 6 | 52 | 0 | 0 | 1 | 0 | 0 | T.McBridex4, K.Bournex2, J.Lovex1 |
| 1 | ARI@LAC | Elijah Molden | S | 2 | 2 | 39 | 0 | 1 | 0 | 0 | 0 | T.McBridex1, K.Bournex1 |
| 1 | ARI@LAC | Daiyan Henley | LB | 4 | 4 | 39 | 0 | 0 | 0 | 0 | 0 | T.McBridex3, T.Allgeierx1 |
| 1 | ARI@LAC | Tarheeb Still | CB | 2 | 2 | 26 | 0 | 0 | 0 | 0 | 0 | K.Bournex1, Mi.Wilsonx1 |
| 1 | ARI@LAC | Donte Jackson | CB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | Mi.Wilsonx2 |
| 1 | ARI@LAC | Genesis Smith | S | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | T.McBridex1, K.Bournex1 |
| 1 | ARI@LAC | Tony Jefferson | S | 2 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | T.Allgeierx1, T.McBridex1 |
| 1 | ARI@LAC | Troy Dye | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | J.Lovex1 |
| 2 | LV@LAC | Cam Hart | CB | 5 | 3 | 60 | 0 | 1 | 1 | 1 | 0 | T.Tuckerx3, J.Bechx1, M.Mayerx1 |
| 2 | LV@LAC | Donte Jackson | CB | 3 | 2 | 29 | 0 | 1 | 1 | 0 | 0 | J.Bechx1, T.Tuckerx1, J.Nailorx1 |
| 2 | LV@LAC | Tarheeb Still | CB | 1 | 1 | 27 | 0 | 1 | 0 | 0 | 0 | D.Youngx1 |
| 2 | LV@LAC | Del'Shawn Phillips | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1, A.Jeantyx1, I.Thomasx1 |
| 2 | LV@LAC | Tony Jefferson | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | T.Tuckerx1 |
| 2 | LV@LAC | Troy Dye | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1, A.Jeantyx1 |
| 2 | LV@LAC | Genesis Smith | S | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | T.Tuckerx1, J.Nailorx1 |
| 2 | LV@LAC | Derwin James | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1 |
| 2 | LV@LAC | R.J. Mickens | S | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1 |
| 3 | LAC@BUF | Rodney Shelley | CB | 2 | 2 | 53 | 0 | 1 | 0 | 0 | 0 | K.Colemanx1, D.Moorex1 |
| 3 | LAC@BUF | Tarheeb Still | CB | 2 | 2 | 34 | 0 | 1 | 0 | 0 | 0 | D.Moorex1, D.Kincaidx1 |
| 3 | LAC@BUF | Daiyan Henley | LB | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | D.Kincaidx1, T.Johnsonx1, D.Moorex1 |
| 3 | LAC@BUF | Genesis Smith | S | 4 | 2 | 28 | 0 | 0 | 0 | 2 | 0 | D.Moorex3, T.Johnsonx1 |
| 3 | LAC@BUF | R.J. Mickens | S | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | D.Moorex1, T.Johnsonx1 |
| 3 | LAC@BUF | Derwin James | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | D.Moorex1 |
| 3 | LAC@BUF | Troy Dye | LB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | K.Shakirx2 |
| 3 | LAC@BUF | Del'Shawn Phillips | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | D.Knoxx1 |
| 3 | LAC@BUF | Tony Jefferson | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Kincaidx1 |
| 3 | LAC@BUF | Donte Jackson | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | K.Shakirx1 |
| 4 | LAC@SEA | Daiyan Henley | LB | 2 | 2 | 33 | 0 | 1 | 0 | 0 | 0 | J.Smith-Njigbax2 |
| 4 | LAC@SEA | Genesis Smith | S | 1 | 1 | 28 | 0 | 1 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 4 | LAC@SEA | Elijah Molden | S | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | A.Barnerx1, C.Kuppx1 |
| 4 | LAC@SEA | Rodney Shelley | CB | 1 | 1 | 20 | 0 | 1 | 0 | 0 | 0 | R.Shaheedx1 |
| 4 | LAC@SEA | Donte Jackson | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 4 | LAC@SEA | R.J. Mickens | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 4 | LAC@SEA | Del'Shawn Phillips | LB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | G.Holanix1 |
| 4 | LAC@SEA | Tarheeb Still | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | C.Kuppx1, J.Smith-Njigbax1 |
| 4 | LAC@SEA | Cam Hart | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | A.Barnerx1 |
| 5 | DEN@LAC | Cam Hart | CB | 2 | 1 | 34 | 0 | 1 | 1 | 0 | 0 | E.Engramx1, C.Suttonx1 |
| 5 | DEN@LAC | Deane Leonard | CB | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | J.Waddlex2, E.Engramx1 |
| 5 | DEN@LAC | Del'Shawn Phillips | LB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 5 | DEN@LAC | Tony Jefferson | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | T.Franklinx1 |
| 5 | DEN@LAC | Tarheeb Still | CB | 3 | 2 | 12 | 0 | 0 | 1 | 0 | 0 | L.Humphreyx2, T.Franklinx1 |
| 5 | DEN@LAC | Elijah Molden | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | E.Engramx1 |
| 5 | DEN@LAC | Daiyan Henley | LB | 3 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | M.Mimsx1, R.Harveyx1, J.Dobbinsx1 |
| 6 | LAC@KC | Elijah Molden | S | 4 | 4 | 62 | 0 | 1 | 0 | 0 | 0 | N.Grayx2, K.Walkerx1, X.Worthyx1 |
| 6 | LAC@KC | Tarheeb Still | CB | 4 | 4 | 37 | 0 | 0 | 0 | 0 | 0 | X.Worthyx2, C.Allenx1, J.Royalsx1 |
| 6 | LAC@KC | Tony Jefferson | S | 4 | 4 | 28 | 0 | 0 | 0 | 0 | 0 | N.Grayx1, J.Royalsx1, T.Kelcex1, K.Walkerx1 |
| 6 | LAC@KC | Genesis Smith | S | 1 | 1 | 23 | 0 | 1 | 0 | 0 | 0 | C.Allenx1 |
| 6 | LAC@KC | Troy Dye | LB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | X.Worthyx1, E.Johnsonx1 |
| 6 | LAC@KC | Cam Hart | CB | 3 | 2 | 19 | 0 | 0 | 0 | 1 | 0 | X.Worthyx2, A.Armstrongx1 |
| 6 | LAC@KC | Daiyan Henley | LB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | T.Kelcex1 |
| 6 | LAC@KC | Deane Leonard | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | A.Armstrongx1 |
| 8 | LAC@LAR | Tarheeb Still | CB | 2 | 1 | 40 | 0 | 1 | 0 | 1 | 0 | K.Mumpfieldx1, T.Atwellx1 |
| 8 | LAC@LAR | Tony Jefferson | S | 3 | 3 | 37 | 0 | 0 | 0 | 0 | 0 | P.Nacuax3 |
| 8 | LAC@LAR | Isas Waxter | CB | 5 | 5 | 16 | 0 | 0 | 0 | 0 | 0 | P.Nacuax3, D.Allenx1, T.Atwellx1 |
| 8 | LAC@LAR | Daiyan Henley | LB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | P.Nacuax2 |
| 8 | LAC@LAR | R.J. Mickens | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | T.Higbeex1 |
| 8 | LAC@LAR | Elijah Molden | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | D.Allenx1 |
| 8 | LAC@LAR | Cam Hart | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | P.Nacuax1 |
| 8 | LAC@LAR | Del'Shawn Phillips | LB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | K.Williamsx1 |

## Who beat them each week

**Wk1 ARI@LAC** (vs ARI offense, 277 rec yds allowed; 19% of targets unattributed)
- Top receivers: T.McBride (TE1, short/YAC (aDOT <8)) 9/13 95y 1TD; K.Bourne (WR2, short/YAC (aDOT <8)) 8/8 75y; Mi.Wilson (WR1, intermediate (aDOT 8-13)) 5/7 56y; M.Harrison (WR3+, deep (aDOT 13+)) 1/3 33y
- 20+ catches: T.McBride(TE1) 27y deep_right - E.Molden [tackler]; M.Harrison(WR3+) 33y deep_left - C.Hart [tackler]
- 15+ runs: J.Love(RB) 18y rush right end

**Wk2 LV@LAC** (vs LV offense, 253 rec yds allowed; 31% of targets unattributed)
- Top receivers: T.Tucker (WR1, deep (aDOT 13+)) 5/7 119y 1TD; D.Young (WR3+, intermediate (aDOT 8-13)) 1/1 27y; J.Bech (WR3+, intermediate (aDOT 8-13)) 2/2 25y; C.White (WR3+, intermediate (aDOT 8-13)) 2/2 24y 2TD
- 20+ catches: J.Bech(WR3+) 20y short_left - D.Jackson [tackler]; T.Tucker(WR1) 40y deep_left TD - no tackler named [unattributed]; T.Tucker(WR1) 42y deep_left - C.Hart [tackler]; D.Young(WR3+) 27y short_left - T.Still [tackler]

**Wk3 LAC@BUF** (vs BUF offense, 204 rec yds allowed; 23% of targets unattributed)
- Top receivers: D.Moore (WR3+, deep (aDOT 13+)) 6/10 67y; T.Johnson (RB, short/YAC (aDOT <8)) 4/4 50y; D.Kincaid (TE1, intermediate (aDOT 8-13)) 2/3 38y; K.Coleman (WR2, deep (aDOT 13+)) 1/2 37y
- 20+ catches: K.Coleman(WR2) 37y deep_right - R.Shelley [tackler]; D.Kincaid(TE1) 24y short_middle - T.Still [tackler]; T.Johnson(RB) 29y short_left - no tackler named [unattributed]
- 15+ runs: J.Cook(RB) 15y rush middle; J.Cook(RB) 15y rush left tackle; J.Cook(RB) 23y rush right guard

**Wk4 LAC@SEA** (vs SEA offense, 168 rec yds allowed; 25% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 5/6 76y; E.Wilson (RB, short/YAC (aDOT <8)) 3/4 39y 1TD; R.Shaheed (WR2, intermediate (aDOT 8-13)) 1/3 20y; C.Kupp (WR3+, intermediate (aDOT 8-13)) 1/2 13y
- 20+ catches: E.Wilson(RB) 23y short_right TD - no tackler named [unattributed]; R.Shaheed(WR2) 20y deep_right - R.Shelley [tackler]; J.Smith-Njigba(WR1) 28y deep_right - G.Smith [tackler]; J.Smith-Njigba(WR1) 20y short_right - D.Henley [tackler]
- 15+ runs: E.Wilson(RB) 15y rush left tackle; R.Shaheed(WR) 28y rush left end; E.Wilson(RB) 15y rush left end

**Wk5 DEN@LAC** (vs DEN offense, 123 rec yds allowed; 14% of targets unattributed)
- Top receivers: E.Engram (TE1, short/YAC (aDOT <8)) 4/4 55y; J.Waddle (WR1, intermediate (aDOT 8-13)) 2/5 19y; C.Sutton (WR2, intermediate (aDOT 8-13)) 2/3 18y 1TD; T.Franklin (WR3+, deep (aDOT 13+)) 2/2 16y
- 20+ catches: E.Engram(TE1) 34y deep_left - C.Hart [tackler]

**Wk6 LAC@KC** (vs KC offense, 272 rec yds allowed; 24% of targets unattributed)
- Top receivers: X.Worthy (WR1, intermediate (aDOT 8-13)) 7/7 73y; N.Gray (TE2+, short/YAC (aDOT <8)) 3/3 53y; T.Kelce (TE1, short/YAC (aDOT <8)) 4/5 53y; C.Allen (WR3+, intermediate (aDOT 8-13)) 2/2 27y
- 20+ catches: T.Kelce(TE1) 24y short_middle - K.Mack [tackler]; N.Gray(TE2+) 31y short_right - E.Molden [tackler]; C.Allen(WR3+) 23y deep_middle - G.Smith [tackler]
- 15+ runs: K.Walker(RB) 33y rush middle; K.Walker(RB) 16y rush middle

**Wk8 LAC@LAR** (vs LAR offense, 157 rec yds allowed; 32% of targets unattributed)
- Top receivers: P.Nacua (WR1, short/YAC (aDOT <8)) 11/12 80y 1TD; T.Atwell (WR3+, deep (aDOT 13+)) 2/4 52y; T.Higbee (TE1, short/YAC (aDOT <8)) 1/2 14y; D.Allen (TE2+, short/YAC (aDOT <8)) 2/2 8y
- 20+ catches: T.Atwell(WR3+) 40y deep_left - T.Still [tackler]
- 15+ runs: B.Corum(RB) 23y rush middle

## Seed notes from defenders/LAC_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 1:29 Tutu Atwell (WR) rec 40 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q3 10:42 Blake Corum (RB) rush 23 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Donte Jackson ← Puka Nacua: 12 tgt, 11 rec, 80 yds

