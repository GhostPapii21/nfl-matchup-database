# CHI DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 CHI@CAR, wk2 MIN@CHI, wk3 PHI@CHI, wk4 NYJ@CHI, wk5 CHI@GB, wk6 CHI@ATL, wk7 NE@CHI, wk8 CHI@SEA). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 29.9% / Zone 65.8% | MOF closed 53.6% / MOF open 42.0% | Blitz 37.9% | Light box 31.1% / Heavy box 25.6% | Sub package 62.0% | Sharp YPT allowed WR 9.5, TE 8.6, RB 8.0, Outside 11.3, Slot 7.7

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE2+: 8.47 YPT on 17 tgts (league 6.71, +1.76), 2 catches of 20+
- type WR2: 12.97 YPT on 35 tgts (league 8.2, +4.77), 8 catches of 20+
- depth deep_20+: 21.21 YPT on 29 tgts (league 12.32, +8.89), 15 catches of 20+
- depth/direction deep_left: 13.79 YPT on 19 tgts (league 11.28, +2.51), 6 catches of 20+
- depth/direction deep_right: 16.79 YPT on 14 tgts (league 11.85, +4.94), 6 catches of 20+
- receiver archetype deep (aDOT 13+): 10.77 YPT on 44 tgts (league 8.94, +1.83), 7 catches of 20+
- receiver archetype intermediate (aDOT 8-13): 9.55 YPT on 78 tgts (league 7.96, +1.59), 10 catches of 20+

Holds (-1.5 YPT or better): WR3+: 5.37 YPT on 43 tgts (league 7.67, -2.3)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 40 | 31 | 261 | 2 | 3 | 6.52 | 5 | 32.60 | 5.61 | 0.91 |
| TE1 | 34 | 24 | 275 | 2 | 2 | 8.09 | 4.20 | 34.40 | 7.39 | 0.70 |
| TE2+ | 17 | 12 | 144 | 1 | 2 | 8.47 | 2.10 | 18 | 6.71 | 1.76 |
| WR1 | 56 | 33 | 512 | 1 | 7 | 9.14 | 7 | 64 | 8.16 | 0.98 |
| WR2 | 35 | 25 | 454 | 5 | 8 | 12.97 | 4.40 | 56.80 | 8.20 | 4.77 |
| WR3+ | 43 | 18 | 231 | 2 | 1 | 5.37 | 5.40 | 28.90 | 7.67 | -2.30 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 26 | 20 | 139 | 1 | 1 | 5.35 | 5.61 | -0.26 |
| TE1 | 24 | 19 | 218 | 2 | 2 | 9.08 | 7.39 | 1.69 |
| TE2+ | 5 | 4 | 62 | 1 | 1 | 12.40 | 6.71 | 5.69 |
| WR1 | 34 | 19 | 326 | 1 | 5 | 9.59 | 8.16 | 1.43 |
| WR2 | 13 | 9 | 230 | 3 | 5 | 17.69 | 8.20 | 9.49 |
| WR3+ | 30 | 14 | 126 | 1 | 0 | 4.20 | 7.67 | -3.47 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 43 | 33 | 129 | 0 | 1 | 3 | 4.58 | -1.58 |
| short_1-9 | 101 | 67 | 668 | 6 | 4 | 6.61 | 6.23 | 0.38 |
| inter_10-19 | 48 | 28 | 465 | 1 | 3 | 9.69 | 10.17 | -0.48 |
| deep_20+ | 29 | 15 | 615 | 6 | 15 | 21.21 | 12.32 | 8.89 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 19 | 7 | 262 | 3 | 6 | 13.79 | 11.28 | 2.51 |
| deep_middle | 8 | 6 | 231 | 2 | 5 | 28.88 | 14.90 | 13.98 |
| deep_right | 14 | 7 | 235 | 1 | 6 | 16.79 | 11.85 | 4.94 |
| short_left | 66 | 41 | 352 | 4 | 0 | 5.33 | 6.08 | -0.75 |
| short_middle | 40 | 29 | 277 | 0 | 1 | 6.92 | 7.43 | -0.51 |
| short_right | 74 | 53 | 520 | 3 | 5 | 7.03 | 5.95 | 1.08 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 44 | 25 | 474 | 3 | 7 | 10.77 | 8.94 | 1.83 |
| intermediate (aDOT 8-13) | 78 | 47 | 745 | 5 | 10 | 9.55 | 7.96 | 1.59 |
| short/YAC (aDOT <8) | 103 | 71 | 658 | 5 | 6 | 6.39 | 6.47 | -0.08 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 3, 'TE': 4, 'WR': 16} (23 total, 2.9/g)
- Pass 20+ by depth/direction: {'deep_left': 6, 'deep_middle': 5, 'deep_right': 6, 'short_middle': 1, 'short_right': 5}
- Rush 15+ by position: {'QB': 3, 'RB': 5} (8 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 18 | 118 | 3 | 6.56 | 14.80 |
| RB | 136 | 576 | 5 | 4.24 | 72 |
| TE | 1 | 2 | 0 | 2 | 0.20 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jaylon Johnson | CB | 7 | 97.20 | 20 | 2.90 | 18 | 308 | 44 | 15.40 | 0 | 5 | 2 | 0 | 0 |
| Tyrique Stevenson | CB | 6 | 68.40 | 18 | 3 | 14 | 206 | 34.30 | 11.44 | 0 | 2 | 4 | 0 | 0 |
| Malik Muhammad | CB | 7 | 74.70 | 17 | 2.40 | 12 | 172 | 24.60 | 10.12 | 0 | 1 | 4 | 1 | 0 |
| Josh Blackwell | CB | 1 | 16 | 3 | 3 | 2 | 33 | 33 | 11 | 0 | 1 | 1 | 0 | 0 |
| Clark Phillips III | CB | 1 | 20.70 | 1 | 1 | 1 | 33 | 33 | 33 | 0 | 1 | 0 | 0 | 0 |
| Kyler Gordon | CB | 2 | 50 | 3 | 1.50 | 2 | 5 | 2.50 | 1.67 | 0 | 0 | 1 | 0 | 0 |
| Devin Bush | LB | 7 | 94.60 | 14 | 2 | 13 | 106 | 15.10 | 7.57 | 0 | 0 | 1 | 0 | 0 |
| T.J. Edwards | OLB | 5 | 89.70 | 10 | 2 | 7 | 19 | 3.80 | 1.90 | 0 | 0 | 2 | 1 | 0 |
| Dillon Thieneman | S | 6 | 98 | 18 | 3 | 13 | 197 | 32.80 | 10.94 | 0 | 3 | 4 | 1 | 0 |
| Cam Lewis | S | 7 | 82.40 | 20 | 2.90 | 19 | 187 | 26.70 | 9.35 | 0 | 1 | 1 | 0 | 0 |
| Xavier Woods | S | 3 | 63.50 | 4 | 1.30 | 4 | 26 | 8.70 | 6.50 | 0 | 0 | 0 | 0 | 0 |
| Elijah Hicks | S | 2 | 15.40 | 3 | 1.50 | 3 | 23 | 11.50 | 7.67 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Jaylon Johnson** (CB): WR1:9t/135y, RB:2t/67y, WR2:4t/43y, WR3+:3t/35y, TE1:1t/19y, TE2+:1t/9y | 20+: wk1 J.Brooks(RB) 48 deep_right; wk1 T.McMillan(WR1) 21 deep_middle; wk3 D.Smith(WR2) 30 deep_right; wk5 M.Golden(WR1) 36 deep_right; wk5 M.Golden(WR1) 50 deep_middle
- **Tyrique Stevenson** (CB): WR1:5t/58y, WR3+:5t/44y, TE1:3t/38y, RB:1t/29y, TE2+:2t/20y, WR2:2t/17y | 20+: wk1 C.Hubbard(RB) 29 short_middle; wk2 J.Jefferson(WR1) 30 deep_left
- **Malik Muhammad** (CB): TE1:3t/69y, WR1:6t/41y, WR2:3t/23y, WR3+:3t/22y, RB:2t/17y | 20+: wk5 T.Kraft(TE1) 46 deep_right
- **Josh Blackwell** (CB): TE1:1t/29y, WR3+:1t/4y, WR1:1t/0y | 20+: wk6 K.Pitts(TE1) 29 short_right
- **Clark Phillips III** (CB): WR2:1t/33y | 20+: wk6 J.Dotson(WR2) 33 short_right
- **Kyler Gordon** (CB): RB:1t/6y, WR1:2t/-1y
- **Devin Bush** (LB): WR1:4t/53y, RB:4t/29y, TE2+:2t/17y, TE1:3t/7y, WR2:1t/0y
- **T.J. Edwards** (OLB): RB:7t/16y, TE1:1t/3y, TE2+:1t/0y, WR2:1t/0y
- **Dillon Thieneman** (S): WR2:2t/72y, TE2+:3t/35y, WR1:5t/34y, TE1:3t/27y, WR3+:4t/24y, RB:1t/5y | 20+: wk2 J.Oliver(TE2+) 24 short_right; wk5 C.Watson(WR2) 31 deep_middle; wk6 J.Dotson(WR2) 41 deep_left
- **Cam Lewis** (S): WR1:4t/52y, WR2:4t/48y, TE1:4t/43y, TE2+:3t/22y, WR3+:4t/18y, RB:1t/4y | 20+: wk8 J.Smith-Njigba(WR1) 21 short_right
- **Xavier Woods** (S): WR2:2t/13y, WR3+:1t/8y, RB:1t/5y
- **Elijah Hicks** (S): WR1:2t/19y, WR2:1t/4y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CHI@CAR | Jaylon Johnson | CB | 2 | 2 | 69 | 0 | 2 | 0 | 0 | 0 | J.Brooksx1, T.McMillanx1 |
| 1 | CHI@CAR | Tyrique Stevenson | CB | 4 | 4 | 66 | 0 | 1 | 0 | 0 | 0 | T.Tremblex1, J.Cokerx1, M.Evansx1, C.Hubbardx1 |
| 1 | CHI@CAR | Cam Lewis | S | 4 | 4 | 36 | 0 | 0 | 0 | 0 | 0 | J.Cokerx3, T.Tremblex1 |
| 1 | CHI@CAR | Malik Muhammad | CB | 4 | 2 | 35 | 0 | 0 | 1 | 1 | 0 | T.McMillanx2, J.Cokerx1, D.Wallerx1 |
| 1 | CHI@CAR | Dillon Thieneman | S | 4 | 3 | 27 | 0 | 0 | 1 | 0 | 0 | M.Evansx1, C.Hubbardx1, D.Wallerx1, T.Tremblex1 |
| 1 | CHI@CAR | Devin Bush | LB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | T.McMillanx2 |
| 2 | MIN@CHI | Cam Lewis | S | 2 | 2 | 31 | 0 | 0 | 0 | 0 | 0 | J.Jeffersonx1, J.Addisonx1 |
| 2 | MIN@CHI | Tyrique Stevenson | CB | 2 | 1 | 30 | 0 | 1 | 1 | 0 | 0 | J.Jeffersonx2 |
| 2 | MIN@CHI | Jaylon Johnson | CB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | J.Addisonx1, T.Hockensonx1 |
| 2 | MIN@CHI | Dillon Thieneman | S | 2 | 1 | 24 | 0 | 1 | 1 | 0 | 0 | J.Jeffersonx1, J.Oliverx1 |
| 2 | MIN@CHI | T.J. Edwards | OLB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | D.Claibornex1, D.Dallasx1, T.Hockensonx1 |
| 2 | MIN@CHI | Malik Muhammad | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Jeffersonx1 |
| 2 | MIN@CHI | Devin Bush | LB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | T.Hockensonx1, J.Addisonx1 |
| 3 | PHI@CHI | Jaylon Johnson | CB | 5 | 5 | 60 | 0 | 1 | 0 | 0 | 0 | D.Smithx2, Z.Ertzx1, M.Lemonx1, D.Wicksx1 |
| 3 | PHI@CHI | Malik Muhammad | CB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | D.Smithx1, W.Shipleyx1 |
| 3 | PHI@CHI | Dillon Thieneman | S | 2 | 1 | 19 | 0 | 0 | 0 | 1 | 0 | M.Lemonx1, D.Wicksx1 |
| 3 | PHI@CHI | Cam Lewis | S | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | J.Mundtx1, D.Wicksx1 |
| 3 | PHI@CHI | Elijah Hicks | S | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | D.Smithx1, M.Lemonx1 |
| 3 | PHI@CHI | Xavier Woods | S | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | D.Smithx2 |
| 3 | PHI@CHI | T.J. Edwards | OLB | 4 | 1 | -2 | 0 | 0 | 2 | 1 | 0 | S.Barkleyx1, Z.Ertzx1, W.Shipleyx1, D.Smithx1 |
| 4 | NYJ@CHI | Tyrique Stevenson | CB | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx2, I.Williamsx1 |
| 4 | NYJ@CHI | Malik Muhammad | CB | 2 | 1 | 14 | 0 | 0 | 1 | 0 | 0 | G.Wilsonx2 |
| 4 | NYJ@CHI | Devin Bush | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | J.Woodsx1 |
| 4 | NYJ@CHI | Xavier Woods | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | B.Allenx1 |
| 4 | NYJ@CHI | T.J. Edwards | OLB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | B.Allenx1 |
| 5 | CHI@GB | Jaylon Johnson | CB | 5 | 4 | 103 | 0 | 2 | 1 | 0 | 0 | M.Goldenx4, C.Watsonx1 |
| 5 | CHI@GB | Malik Muhammad | CB | 4 | 4 | 66 | 0 | 1 | 0 | 0 | 0 | T.Kraftx2, B.Meltonx1, C.Watsonx1 |
| 5 | CHI@GB | Dillon Thieneman | S | 5 | 4 | 59 | 0 | 1 | 1 | 0 | 0 | B.Meltonx2, T.Kraftx1, C.Watsonx1, M.Goldenx1 |
| 5 | CHI@GB | Cam Lewis | S | 4 | 4 | 19 | 0 | 0 | 0 | 0 | 0 | M.Goldenx2, P.Strongx1, S.Moorex1 |
| 5 | CHI@GB | Xavier Woods | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | B.Meltonx1 |
| 5 | CHI@GB | Tyrique Stevenson | CB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | T.Kraftx1, C.Watsonx1 |
| 5 | CHI@GB | Devin Bush | LB | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | M.Lloydx1, T.Kraftx1 |
| 5 | CHI@GB | T.J. Edwards | OLB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | 0 | P.Strongx1 |
| 6 | CHI@ATL | Dillon Thieneman | S | 2 | 1 | 41 | 0 | 1 | 1 | 0 | 0 | D.Londonx1, J.Dotsonx1 |
| 6 | CHI@ATL | Josh Blackwell | CB | 3 | 2 | 33 | 0 | 1 | 1 | 0 | 0 | Z.Branchx1, K.Pittsx1, D.Londonx1 |
| 6 | CHI@ATL | Clark Phillips III | CB | 1 | 1 | 33 | 0 | 1 | 0 | 0 | 0 | J.Dotsonx1 |
| 6 | CHI@ATL | Cam Lewis | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | Z.Branchx1, K.Pittsx1 |
| 6 | CHI@ATL | Devin Bush | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | K.Pittsx1, A.Hooperx1 |
| 6 | CHI@ATL | Elijah Hicks | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | D.Londonx1 |
| 6 | CHI@ATL | Jaylon Johnson | CB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | D.Londonx2 |
| 6 | CHI@ATL | Malik Muhammad | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Londonx1 |
| 7 | NE@CHI | Cam Lewis | S | 3 | 3 | 42 | 0 | 0 | 0 | 0 | 0 | H.Henryx2, E.Raridonx1 |
| 7 | NE@CHI | Devin Bush | LB | 3 | 3 | 33 | 0 | 0 | 0 | 0 | 0 | T.Hendersonx1, R.Stevensonx1, D.Douglasx1 |
| 7 | NE@CHI | Jaylon Johnson | CB | 2 | 2 | 33 | 0 | 0 | 0 | 0 | 0 | R.Stevensonx1, A.Brownx1 |
| 7 | NE@CHI | Tyrique Stevenson | CB | 3 | 2 | 32 | 0 | 0 | 1 | 0 | 0 | A.Brownx2, H.Henryx1 |
| 7 | NE@CHI | Dillon Thieneman | S | 3 | 3 | 27 | 0 | 0 | 0 | 0 | 0 | E.Chismx1, D.Douglasx1, H.Henryx1 |
| 7 | NE@CHI | Malik Muhammad | CB | 3 | 2 | 24 | 0 | 0 | 1 | 0 | 0 | A.Brownx2, T.Hendersonx1 |
| 7 | NE@CHI | Kyler Gordon | CB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | 0 | D.Douglasx1 |
| 8 | CHI@SEA | Tyrique Stevenson | CB | 4 | 3 | 45 | 0 | 0 | 1 | 0 | 0 | T.Hortonx2, A.Barnerx1, J.Smith-Njigbax1 |
| 8 | CHI@SEA | Cam Lewis | S | 3 | 2 | 27 | 0 | 1 | 1 | 0 | 0 | T.Hortonx1, J.Smith-Njigbax1, A.Barnerx1 |
| 8 | CHI@SEA | Devin Bush | LB | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1, Z.Charbonnetx1 |
| 8 | CHI@SEA | Jaylon Johnson | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1, T.Hortonx1 |
| 8 | CHI@SEA | Kyler Gordon | CB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | J.Smith-Njigbax1, Z.Charbonnetx1 |
| 8 | CHI@SEA | T.J. Edwards | OLB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | J.Pricex1 |

## Who beat them each week

**Wk1 CHI@CAR** (vs CAR offense, 361 rec yds allowed; 38% of targets unattributed)
- Top receivers: J.Coker (WR2, intermediate (aDOT 8-13)) 8/9 138y 2TD; T.McMillan (WR1, intermediate (aDOT 8-13)) 5/8 75y; J.Brooks (RB, intermediate (aDOT 8-13)) 1/2 48y; C.Hubbard (RB, short/YAC (aDOT <8)) 3/3 38y 1TD
- 20+ catches: J.Coker(WR2) 26y deep_right - no tackler named [unattributed]; J.Coker(WR2) 51y deep_left TD - no tackler named [unattributed]; J.Brooks(RB) 48y deep_right - J.Johnson [tackler]; T.McMillan(WR1) 21y deep_middle - J.Johnson [tackler]; C.Hubbard(RB) 29y short_middle - T.Stevenson [tackler]
- 15+ runs: K.Pickett(QB) 24y rush right end

**Wk2 MIN@CHI** (vs MIN offense, 143 rec yds allowed; 26% of targets unattributed)
- Top receivers: J.Jefferson (WR1, intermediate (aDOT 8-13)) 3/6 55y; T.Hockenson (TE1, short/YAC (aDOT <8)) 3/4 29y; J.Oliver (TE2+, short/YAC (aDOT <8)) 1/1 24y; J.Addison (WR2, deep (aDOT 13+)) 2/5 21y
- 20+ catches: J.Jefferson(WR1) 30y deep_left - T.Stevenson [tackler]; J.Oliver(TE2+) 24y short_right - D.Thieneman [tackler]
- 15+ runs: A.Jones(RB) 20y rush right tackle; A.Jones(RB) 15y rush left end

**Wk3 PHI@CHI** (vs PHI offense, 153 rec yds allowed; 20% of targets unattributed)
- Top receivers: D.Smith (WR2, intermediate (aDOT 8-13)) 6/8 65y; D.Wicks (WR3+, deep (aDOT 13+)) 2/5 32y; M.Lemon (WR1, short/YAC (aDOT <8)) 3/4 29y; W.Shipley (RB, short/YAC (aDOT <8)) 1/2 11y
- 20+ catches: D.Smith(WR2) 30y deep_right - J.Johnson [tackler]
- 15+ runs: S.Barkley(RB) 17y rush right end; J.Hurts(QB) 20y rush left tackle

**Wk4 NYJ@CHI** (vs NYJ offense, 119 rec yds allowed; 40% of targets unattributed)
- Top receivers: I.Williams (WR3+, intermediate (aDOT 8-13)) 2/3 73y 1TD; G.Wilson (WR1, intermediate (aDOT 8-13)) 3/4 27y; J.Woods (TE2+, short/YAC (aDOT <8)) 1/1 11y; B.Allen (RB, short/YAC (aDOT <8)) 2/2 8y
- 20+ catches: I.Williams(WR3+) 58y deep_middle TD - no tackler named [unattributed]

**Wk5 CHI@GB** (vs GB offense, 367 rec yds allowed; 16% of targets unattributed)
- Top receivers: C.Watson (WR2, deep (aDOT 13+)) 6/8 143y 2TD; M.Golden (WR1, deep (aDOT 13+)) 6/8 123y; T.Kraft (TE1, short/YAC (aDOT <8)) 5/5 64y; B.Melton (WR3+, deep (aDOT 13+)) 3/4 20y
- 20+ catches: C.Watson(WR2) 42y deep_left TD - no tackler named [unattributed]; C.Watson(WR2) 31y deep_middle - D.Thieneman [tackler]; C.Watson(WR2) 53y deep_middle TD - no tackler named [unattributed]; T.Kraft(TE1) 46y deep_right - M.Muhammad [tackler]; M.Golden(WR1) 36y deep_right - J.Johnson [tackler]; M.Golden(WR1) 50y deep_middle - J.Johnson [tackler]
- 15+ runs: K.Johnson(RB) 23y rush left tackle

**Wk6 CHI@ATL** (vs ATL offense, 225 rec yds allowed; 37% of targets unattributed)
- Top receivers: J.Dotson (WR2, deep (aDOT 13+)) 3/5 87y 1TD; D.London (WR1, intermediate (aDOT 8-13)) 4/11 62y; K.Pitts (TE1, short/YAC (aDOT <8)) 5/7 60y 2TD; Br.Robinson (RB, short/YAC (aDOT <8)) 2/2 9y
- 20+ catches: D.London(WR1) 39y deep_left - N.Sewell [tackler]; J.Dotson(WR2) 33y short_right - C.Phillips [tackler]; K.Pitts(TE1) 29y short_right - J.Blackwell [tackler]; J.Dotson(WR2) 41y deep_left - D.Thieneman [tackler]
- 15+ runs: Bi.Robinson(RB) 23y rush right guard

**Wk7 NE@CHI** (vs NE offense, 321 rec yds allowed; 20% of targets unattributed)
- Top receivers: R.Stevenson (RB, short/YAC (aDOT <8)) 5/5 93y 1TD; H.Henry (TE1, short/YAC (aDOT <8)) 7/7 71y; E.Raridon (TE2+, short/YAC (aDOT <8)) 3/4 56y 1TD; A.Brown (WR3+, deep (aDOT 13+)) 3/6 48y
- 20+ catches: R.Stevenson(RB) 48y short_right TD - no tackler named [unattributed]; E.Raridon(TE2+) 30y deep_right TD - no tackler named [unattributed]
- 15+ runs: D.Maye(QB) 15y rush right end

**Wk8 CHI@SEA** (vs SEA offense, 188 rec yds allowed; 49% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 6/11 118y 1TD; T.Horton (WR3+, intermediate (aDOT 8-13)) 3/7 26y; A.Barner (TE1, short/YAC (aDOT <8)) 2/5 23y; J.Price (RB, short/YAC (aDOT <8)) 2/4 8y
- 20+ catches: J.Smith-Njigba(WR1) 21y short_right - C.Lewis [tackler]; J.Smith-Njigba(WR1) 43y deep_left TD - no tackler named [unattributed]

## MNF CHI@SEA live log (runs/2026-11-02_CHI@SEA_r3/live/chi_defender_log.csv, ESPN text, tackler/PBU tag, not true coverage)

By target, depth x direction (tgt / catches / yds / tacklers / PBU):

- A.Barner short left: 2 tgt, 1 rec, 17 yds; tacklers: T.Stevenson; PBU: -
- A.Barner short middle: 1 tgt, 1 rec, 6 yds; tacklers: C.Lewis; PBU: -
- A.Barner short right: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- C.Kupp short left: 3 tgt, 1 rec, 7 yds; tacklers: -; PBU: -
- C.Kupp short right: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- G.Holani short right: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: M.Sweat
- J.Price short left: 2 tgt, 1 rec, 2 yds; tacklers: T.Edwards; PBU: M.Sweat
- J.Price short middle: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- J.Price short right: 1 tgt, 1 rec, 6 yds; tacklers: A.Booker; PBU: -
- J.Smith-Njigba deep left: 3 tgt, 1 rec, 43 yds; tacklers: -; PBU: -
- J.Smith-Njigba short left: 2 tgt, 2 rec, 26 yds; tacklers: D.Bush, T.Stevenson; PBU: -
- J.Smith-Njigba short middle: 2 tgt, 1 rec, 15 yds; tacklers: T.Stevenson; PBU: K.Gordon
- J.Smith-Njigba short right: 5 tgt, 3 rec, 44 yds; tacklers: C.Lewis, J.Johnson; PBU: -
- T.Horton short left: 4 tgt, 2 rec, 24 yds; tacklers: T.Stevenson; PBU: -
- T.Horton short middle: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- T.Horton short right: 1 tgt, 1 rec, 2 yds; tacklers: J.Johnson; PBU: -
- Z.Charbonnet short middle: 2 tgt, 1 rec, 6 yds; tacklers: D.Bush; PBU: -
- Z.Charbonnet short right: 2 tgt, 2 rec, 0 yds; tacklers: J.Simmons, K.Gordon; PBU: -

Tackler-after-catch totals: T.Stevenson 4 rec/55y (A.Barner, J.Smith-Njigba, T.Horton); C.Lewis 2 rec/27y (A.Barner, J.Smith-Njigba); D.Bush 2 rec/22y (J.Smith-Njigba, Z.Charbonnet); J.Johnson 2 rec/13y (J.Smith-Njigba, T.Horton); A.Booker 1 rec/6y (J.Price); K.Gordon 1 rec/6y (Z.Charbonnet); T.Edwards 1 rec/2y (J.Price); J.Simmons 1 rec/-6y (Z.Charbonnet)

