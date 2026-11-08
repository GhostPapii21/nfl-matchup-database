# PIT DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 ATL@PIT, wk2 PIT@NE, wk3 CIN@PIT, wk4 PIT@CLE, wk5 IND@PIT, wk6 PIT@TB, wk7 PIT@NO, wk8 CLE@PIT). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 12.6% / Zone 82.2% | MOF closed 45.5% / MOF open 51.5% | Blitz 26.9% | Light box 45.9% / Heavy box 25.1% | Sub package 67.0% | Sharp YPT allowed WR 7.2, TE 7.3, RB 5.9, Outside 7.8, Slot 6.5

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- depth deep_20+: 14.88 YPT on 32 tgts (league 12.32, +2.56), 14 catches of 20+
- depth/direction deep_right: 16.81 YPT on 16 tgts (league 11.85, +4.96), 8 catches of 20+

Holds (-1.5 YPT or better): WR1: 6.43 YPT on 63 tgts (league 8.16, -1.73); WR3+: 5.88 YPT on 43 tgts (league 7.67, -1.79)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 59 | 46 | 375 | 1 | 3 | 6.36 | 7.40 | 46.90 | 5.61 | 0.75 |
| TE1 | 40 | 28 | 352 | 2 | 7 | 8.80 | 5 | 44 | 7.39 | 1.41 |
| TE2+ | 13 | 12 | 104 | 0 | 2 | 8 | 1.60 | 13 | 6.71 | 1.29 |
| WR1 | 63 | 35 | 405 | 2 | 4 | 6.43 | 7.90 | 50.60 | 8.16 | -1.73 |
| WR2 | 53 | 35 | 450 | 2 | 7 | 8.49 | 6.60 | 56.20 | 8.20 | 0.29 |
| WR3+ | 43 | 26 | 253 | 0 | 4 | 5.88 | 5.40 | 31.60 | 7.67 | -1.79 |
| other | 1 | 1 | -3 | 0 | 0 | -3 | 0.10 | -0.40 | 2.86 | -5.86 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 31 | 25 | 215 | 0 | 1 | 6.94 | 5.61 | 1.33 |
| TE1 | 26 | 19 | 248 | 0 | 5 | 9.54 | 7.39 | 2.15 |
| TE2+ | 8 | 8 | 61 | 0 | 1 | 7.62 | 6.71 | 0.91 |
| WR1 | 43 | 22 | 188 | 1 | 1 | 4.37 | 8.16 | -3.79 |
| WR2 | 26 | 17 | 173 | 1 | 2 | 6.65 | 8.20 | -1.55 |
| WR3+ | 27 | 13 | 153 | 0 | 3 | 5.67 | 7.67 | -2 |
| other | 1 | 1 | -3 | 0 | 0 | -3 | 2.86 | -5.86 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 68 | 50 | 313 | 1 | 5 | 4.60 | 4.58 | 0.02 |
| short_1-9 | 127 | 97 | 764 | 4 | 0 | 6.02 | 6.23 | -0.21 |
| inter_10-19 | 45 | 22 | 383 | 0 | 8 | 8.51 | 10.17 | -1.66 |
| deep_20+ | 32 | 14 | 476 | 2 | 14 | 14.88 | 12.32 | 2.56 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 22 | 10 | 276 | 0 | 9 | 12.55 | 11.28 | 1.27 |
| deep_middle | 7 | 3 | 91 | 1 | 2 | 13 | 14.90 | -1.90 |
| deep_right | 16 | 8 | 269 | 1 | 8 | 16.81 | 11.85 | 4.96 |
| short_left | 106 | 82 | 631 | 2 | 5 | 5.95 | 6.08 | -0.13 |
| short_middle | 42 | 31 | 298 | 0 | 1 | 7.10 | 7.43 | -0.33 |
| short_right | 79 | 49 | 371 | 3 | 2 | 4.70 | 5.95 | -1.25 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 50 | 30 | 429 | 1 | 6 | 8.58 | 8.94 | -0.36 |
| intermediate (aDOT 8-13) | 75 | 46 | 517 | 4 | 7 | 6.89 | 7.96 | -1.07 |
| short/YAC (aDOT <8) | 147 | 107 | 990 | 2 | 14 | 6.73 | 6.47 | 0.26 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 3, 'TE': 9, 'WR': 15} (27 total, 3.4/g)
- Pass 20+ by depth/direction: {'deep_left': 9, 'deep_middle': 2, 'deep_right': 8, 'short_left': 5, 'short_middle': 1, 'short_right': 2}
- Rush 15+ by position: {'QB': 2, 'RB': 6} (8 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 21 | 110 | 2 | 5.24 | 13.80 |
| RB | 157 | 560 | 6 | 3.57 | 70 |
| TE | 1 | 1 | 0 | 1 | 0.10 |
| WR | 1 | 6 | 0 | 6 | 0.80 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jalen Ramsey | CB | 8 | 99.80 | 26 | 3.20 | 24 | 255 | 31.90 | 9.81 | 0 | 6 | 2 | 0 | 0 |
| Asante Samuel Jr. | CB | 8 | 94.10 | 27 | 3.40 | 19 | 223 | 27.90 | 8.26 | 0 | 4 | 8 | 0 | 0 |
| Daylen Everette | CB | 5 | 33.90 | 17 | 3.40 | 12 | 211 | 42.20 | 12.41 | 0 | 4 | 4 | 1 | 0 |
| Jamel Dean | CB | 7 | 81.60 | 27 | 3.90 | 19 | 209 | 29.90 | 7.74 | 0 | 2 | 7 | 1 | 0 |
| Brandin Echols | CB | 1 | 6.60 | 1 | 1 | 1 | 7 | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| Patrick Queen | LB | 7 | 99.90 | 23 | 3.30 | 19 | 139 | 19.90 | 6.04 | 0 | 0 | 3 | 1 | 0 |
| Payton Wilson | LB | 8 | 85.90 | 23 | 2.90 | 20 | 134 | 16.80 | 5.83 | 0 | 1 | 2 | 1 | 0 |
| Jaquan Brisker | S | 8 | 99.80 | 29 | 3.60 | 26 | 327 | 40.90 | 11.28 | 0 | 5 | 2 | 1 | 0 |
| Rayshawn Jenkins | S | 3 | 54.50 | 8 | 2.70 | 8 | 132 | 44 | 16.50 | 0 | 1 | 0 | 0 | 0 |
| Robert Spears-Jennings | S | 4 | 45.30 | 11 | 2.80 | 9 | 91 | 22.80 | 8.27 | 0 | 0 | 1 | 1 | 0 |
| DeShon Elliott | S | 1 | 33.50 | 1 | 1 | 1 | 24 | 24 | 24 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Jalen Ramsey** (CB): TE1:7t/84y, RB:6t/70y, WR3+:6t/39y, TE2+:1t/21y, WR2:2t/21y, WR1:4t/20y | 20+: wk1 Bi.Robinson(RB) 24 short_left; wk2 H.Henry(TE1) 29 deep_left; wk3 D.Meyers(WR3+) 23 short_left; wk5 T.Warren(TE1) 20 short_middle; wk6 B.Sharp(TE2+) 21 deep_left; wk8 H.Fannin(TE1) 25 deep_right
- **Asante Samuel Jr.** (CB): WR2:7t/83y, WR1:9t/69y, WR3+:8t/58y, RB:2t/13y, TE1:1t/0y | 20+: wk1 D.London(WR1) 21 deep_left; wk2 R.Doubs(WR2) 29 deep_right; wk3 J.Chase(WR2) 21 deep_right; wk5 L.Treadwell(WR3+) 22 short_right
- **Daylen Everette** (CB): WR1:4t/85y, WR2:8t/83y, TE1:2t/31y, WR3+:3t/12y | 20+: wk4 D.Boston(WR1) 60 deep_left; wk4 K.Concepcion(WR2) 25 short_left; wk5 T.Warren(TE1) 29 deep_left; wk8 K.Concepcion(WR2) 24 deep_left
- **Jamel Dean** (CB): WR3+:7t/105y, WR1:15t/69y, WR2:3t/23y, TE1:1t/6y, TE2+:1t/6y | 20+: wk6 T.Hurst(WR3+) 22 deep_left; wk7 B.Brown(WR3+) 49 deep_middle
- **Brandin Echols** (CB): WR2:1t/7y
- **Patrick Queen** (LB): RB:10t/70y, WR2:4t/28y, TE1:4t/26y, WR1:2t/8y, TE2+:3t/7y
- **Payton Wilson** (LB): RB:10t/43y, TE2+:2t/34y, WR3+:4t/30y, TE1:3t/21y, WR1:3t/6y, WR2:1t/0y | 20+: wk2 E.Raridon(TE2+) 30 deep_left
- **Jaquan Brisker** (S): TE1:7t/112y, WR1:5t/73y, WR2:7t/68y, RB:7t/63y, TE2+:1t/9y, WR3+:2t/2y | 20+: wk4 K.Concepcion(WR2) 21 deep_left; wk5 J.Downs(WR1) 42 deep_right; wk5 J.Taylor(RB) 24 short_left; wk8 H.Fannin(TE1) 37 deep_right; wk8 H.Fannin(TE1) 27 short_left
- **Rayshawn Jenkins** (S): WR2:3t/89y, RB:2t/19y, WR3+:1t/10y, WR1:1t/8y, TE1:1t/6y | 20+: wk2 R.Doubs(WR2) 63 deep_right
- **Robert Spears-Jennings** (S): RB:3t/28y, TE1:2t/27y, WR1:3t/25y, WR2:2t/6y, TE2+:1t/5y
- **DeShon Elliott** (S): WR2:1t/24y | 20+: wk7 D.Vele(WR2) 24 deep_right

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ATL@PIT | Jalen Ramsey | CB | 2 | 1 | 24 | 0 | 1 | 1 | 0 | 0 | K.Pittsx1, Bi.Robinsonx1 |
| 1 | ATL@PIT | Jaquan Brisker | S | 4 | 3 | 22 | 0 | 0 | 0 | 1 | 0 | Bi.Robinsonx3, J.Dotsonx1 |
| 1 | ATL@PIT | Asante Samuel Jr. | CB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | D.Londonx1 |
| 1 | ATL@PIT | Jamel Dean | CB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | J.Dotsonx1 |
| 1 | ATL@PIT | Payton Wilson | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | Bi.Robinsonx1, O.Zaccheausx1 |
| 1 | ATL@PIT | Patrick Queen | LB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | D.Londonx1 |
| 1 | ATL@PIT | Rayshawn Jenkins | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | Bi.Robinsonx1 |
| 2 | PIT@NE | Rayshawn Jenkins | S | 2 | 2 | 73 | 0 | 1 | 0 | 0 | 0 | K.Williamsx1, R.Doubsx1 |
| 2 | PIT@NE | Asante Samuel Jr. | CB | 3 | 2 | 39 | 0 | 1 | 1 | 0 | 0 | M.Hollinsx1, R.Doubsx1, K.Williamsx1 |
| 2 | PIT@NE | Jalen Ramsey | CB | 2 | 2 | 38 | 0 | 1 | 0 | 0 | 0 | D.Douglasx1, H.Henryx1 |
| 2 | PIT@NE | Payton Wilson | LB | 1 | 1 | 30 | 0 | 1 | 0 | 0 | 0 | E.Raridonx1 |
| 2 | PIT@NE | Jamel Dean | CB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | R.Doubsx1, M.Hollinsx1 |
| 2 | PIT@NE | Jaquan Brisker | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | H.Henryx1 |
| 2 | PIT@NE | Patrick Queen | LB | 2 | 1 | 4 | 0 | 0 | 0 | 1 | 0 | H.Henryx1, R.Gilliamx1 |
| 3 | CIN@PIT | Rayshawn Jenkins | S | 5 | 5 | 52 | 0 | 0 | 0 | 0 | 0 | J.Chasex2, C.Brownx1, T.Higginsx1, M.Gesickix1 |
| 3 | CIN@PIT | Jalen Ramsey | CB | 5 | 5 | 41 | 0 | 1 | 0 | 0 | 0 | D.Meyersx3, J.Chasex1, S.Perinex1 |
| 3 | CIN@PIT | Jamel Dean | CB | 5 | 4 | 39 | 0 | 0 | 1 | 0 | 0 | T.Higginsx3, T.Hudsonx1, M.Gesickix1 |
| 3 | CIN@PIT | Jaquan Brisker | S | 4 | 4 | 38 | 0 | 0 | 0 | 0 | 0 | T.Higginsx2, C.Youngx1, J.Chasex1 |
| 3 | CIN@PIT | Asante Samuel Jr. | CB | 2 | 1 | 21 | 0 | 1 | 1 | 0 | 0 | J.Chasex2 |
| 3 | CIN@PIT | Patrick Queen | LB | 5 | 4 | 15 | 0 | 0 | 1 | 0 | 0 | D.Samplex2, J.Chasex1, T.Hudsonx1, C.Brownx1 |
| 3 | CIN@PIT | Daylen Everette | CB | 2 | 1 | 13 | 0 | 0 | 1 | 0 | 0 | D.Meyersx1, J.Chasex1 |
| 3 | CIN@PIT | Brandin Echols | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | J.Chasex1 |
| 3 | CIN@PIT | Payton Wilson | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | J.Chasex1 |
| 4 | PIT@CLE | Daylen Everette | CB | 4 | 3 | 94 | 0 | 2 | 1 | 0 | 0 | D.Bostonx2, K.Concepcionx2 |
| 4 | PIT@CLE | Jaquan Brisker | S | 5 | 5 | 51 | 0 | 1 | 0 | 0 | 0 | H.Fanninx2, Q.Judkinsx2, K.Concepcionx1 |
| 4 | PIT@CLE | Robert Spears-Jennings | S | 5 | 3 | 26 | 0 | 0 | 1 | 1 | 0 | K.Concepcionx2, D.Bostonx2, R.Sandersx1 |
| 4 | PIT@CLE | Asante Samuel Jr. | CB | 3 | 2 | 22 | 0 | 0 | 1 | 0 | 0 | D.Bostonx2, J.Jeudyx1 |
| 4 | PIT@CLE | Payton Wilson | LB | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | J.Jeudyx2, R.Sandersx1 |
| 4 | PIT@CLE | Patrick Queen | LB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1, Q.Judkinsx1 |
| 4 | PIT@CLE | Jalen Ramsey | CB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | I.Bondx1 |
| 4 | PIT@CLE | Jamel Dean | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Bostonx1 |
| 5 | IND@PIT | Jaquan Brisker | S | 6 | 4 | 84 | 0 | 2 | 2 | 0 | 0 | J.Downsx2, K.Allenx2, J.Taylorx1, L.Treadwellx1 |
| 5 | IND@PIT | Daylen Everette | CB | 5 | 3 | 45 | 0 | 1 | 2 | 0 | 0 | K.Allenx2, L.Treadwellx1, T.Warrenx1, D.Burksx1 |
| 5 | IND@PIT | Jalen Ramsey | CB | 6 | 5 | 44 | 0 | 1 | 1 | 0 | 0 | T.Warrenx4, J.Downsx1, K.Allenx1 |
| 5 | IND@PIT | Asante Samuel Jr. | CB | 7 | 3 | 36 | 0 | 1 | 4 | 0 | 0 | L.Treadwellx3, K.Allenx2, J.Downsx1, T.Warrenx1 |
| 5 | IND@PIT | Payton Wilson | LB | 7 | 6 | 32 | 0 | 0 | 1 | 0 | 0 | T.Warrenx2, J.Taylorx2, A.Ogletreex1, S.McGowanx1, J.Downsx1 |
| 5 | IND@PIT | Robert Spears-Jennings | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | T.Warrenx1 |
| 6 | PIT@TB | Jamel Dean | CB | 10 | 4 | 48 | 0 | 1 | 5 | 1 | 0 | E.Egbukax6, T.Hurstx2, C.Godwinx1, T.Johnsonx1 |
| 6 | PIT@TB | Daylen Everette | CB | 4 | 3 | 33 | 0 | 0 | 0 | 1 | 0 | C.Godwinx2, E.Egbukax2 |
| 6 | PIT@TB | Jalen Ramsey | CB | 2 | 2 | 26 | 0 | 1 | 0 | 0 | 0 | T.Hurstx1, B.Sharpx1 |
| 6 | PIT@TB | Asante Samuel Jr. | CB | 4 | 4 | 25 | 0 | 0 | 0 | 0 | 0 | E.Egbukax2, C.Godwinx1, T.Johnsonx1 |
| 6 | PIT@TB | Patrick Queen | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | C.Godwinx1 |
| 6 | PIT@TB | Payton Wilson | LB | 3 | 3 | 9 | 0 | 0 | 0 | 0 | 0 | B.Irvingx2, T.Johnsonx1 |
| 6 | PIT@TB | Jaquan Brisker | S | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | C.Ottonx1, E.Egbukax1 |
| 7 | PIT@NO | Jamel Dean | CB | 5 | 5 | 72 | 0 | 1 | 0 | 0 | 0 | C.Olavex2, B.Brownx2, B.Lancex1 |
| 7 | PIT@NO | Asante Samuel Jr. | CB | 6 | 6 | 59 | 0 | 0 | 0 | 0 | 0 | A.Kamarax2, C.Olavex2, B.Lancex1, D.Velex1 |
| 7 | PIT@NO | Jalen Ramsey | CB | 5 | 5 | 52 | 0 | 0 | 0 | 0 | 0 | A.Kamarax3, K.Millerx1, C.Olavex1 |
| 7 | PIT@NO | DeShon Elliott | S | 1 | 1 | 24 | 0 | 1 | 0 | 0 | 0 | D.Velex1 |
| 7 | PIT@NO | Patrick Queen | LB | 4 | 3 | 19 | 0 | 0 | 1 | 0 | 0 | C.Olavex1, D.Velex1, J.Johnsonx1, A.Kamarax1 |
| 7 | PIT@NO | Payton Wilson | LB | 4 | 3 | 15 | 0 | 0 | 0 | 1 | 0 | K.Millerx2, A.Kamarax1, C.Olavex1 |
| 7 | PIT@NO | Robert Spears-Jennings | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | C.Olavex1, N.Fantx1 |
| 7 | PIT@NO | Jaquan Brisker | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | D.Velex1 |
| 8 | CLE@PIT | Jaquan Brisker | S | 6 | 6 | 103 | 0 | 2 | 0 | 0 | 0 | H.Fanninx3, Q.Judkinsx1, K.Concepcionx1, B.Whiteheartx1 |
| 8 | CLE@PIT | Patrick Queen | LB | 8 | 7 | 70 | 0 | 0 | 1 | 0 | 0 | D.Sampsonx6, H.Fanninx2 |
| 8 | CLE@PIT | Robert Spears-Jennings | S | 3 | 3 | 38 | 0 | 0 | 0 | 0 | 0 | Q.Judkinsx1, H.Fanninx1, D.Sampsonx1 |
| 8 | CLE@PIT | Jalen Ramsey | CB | 3 | 3 | 28 | 0 | 1 | 0 | 0 | 0 | D.Bostonx1, T.Wallacex1, H.Fanninx1 |
| 8 | CLE@PIT | Daylen Everette | CB | 2 | 2 | 26 | 0 | 1 | 0 | 0 | 0 | H.Fanninx1, K.Concepcionx1 |
| 8 | CLE@PIT | Jamel Dean | CB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | D.Bostonx3 |
| 8 | CLE@PIT | Payton Wilson | LB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | H.Fanninx1, D.Bostonx1 |
| 8 | CLE@PIT | Asante Samuel Jr. | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Bostonx1 |

## Who beat them each week

**Wk1 ATL@PIT** (vs ATL offense, 143 rec yds allowed; 21% of targets unattributed)
- Top receivers: Bi.Robinson (RB, short/YAC (aDOT <8)) 8/10 90y 1TD; D.London (WR1, intermediate (aDOT 8-13)) 2/4 29y; J.Dotson (WR2, deep (aDOT 13+)) 1/3 19y; O.Zaccheaus (WR3+, short/YAC (aDOT <8)) 1/1 5y
- 20+ catches: Bi.Robinson(RB) 23y short_right TD - no tackler named [unattributed]; D.London(WR1) 21y deep_left - A.Samuel [tackler]; Bi.Robinson(RB) 24y short_left - J.Ramsey [tackler]
- 15+ runs: Bi.Robinson(RB) 20y rush right end; Bi.Robinson(RB) 15y rush right end

**Wk2 PIT@NE** (vs NE offense, 208 rec yds allowed; 14% of targets unattributed)
- Top receivers: R.Doubs (WR2, deep (aDOT 13+)) 3/4 96y; H.Henry (TE1, short/YAC (aDOT <8)) 3/5 40y; E.Raridon (TE2+, short/YAC (aDOT <8)) 1/1 30y; M.Hollins (WR3+, deep (aDOT 13+)) 2/2 18y
- 20+ catches: H.Henry(TE1) 29y deep_left - J.Ramsey [tackler]; E.Raridon(TE2+) 30y deep_left - P.Wilson [tackler]; R.Doubs(WR2) 29y deep_right - A.Samuel [tackler]; R.Doubs(WR2) 63y deep_right - R.Jenkins [tackler]
- 15+ runs: T.Henderson(RB) 39y rush left guard; R.Stevenson(RB) 24y rush middle

**Wk3 CIN@PIT** (vs CIN offense, 282 rec yds allowed; 19% of targets unattributed)
- Top receivers: J.Chase (WR2, intermediate (aDOT 8-13)) 9/12 98y 1TD; T.Higgins (WR1, deep (aDOT 13+)) 6/7 90y 1TD; M.Gesicki (TE1, intermediate (aDOT 8-13)) 3/3 37y 1TD; D.Meyers (WR3+, short/YAC (aDOT <8)) 3/5 29y
- 20+ catches: D.Meyers(WR3+) 23y short_left - J.Ramsey [tackler]; T.Higgins(WR1) 28y deep_right TD - no tackler named [unattributed]; J.Chase(WR2) 21y deep_right - A.Samuel [tackler]; M.Gesicki(TE1) 25y deep_middle TD - no tackler named [unattributed]

**Wk4 PIT@CLE** (vs CLE offense, 268 rec yds allowed; 12% of targets unattributed)
- Top receivers: D.Boston (WR1, deep (aDOT 13+)) 4/7 89y; K.Concepcion (WR2, short/YAC (aDOT <8)) 5/8 64y; Q.Judkins (RB, short/YAC (aDOT <8)) 6/7 43y; J.Jeudy (WR3+, intermediate (aDOT 8-13)) 3/3 36y
- 20+ catches: K.Concepcion(WR2) 21y deep_left - J.Brisker [tackler]; D.Boston(WR1) 60y deep_left - D.Everette [tackler]; K.Concepcion(WR2) 25y short_left - D.Everette [tackler]
- 15+ runs: J.McLaughlin(RB) 28y rush right end; D.Watson(QB) 21y rush left end

**Wk5 IND@PIT** (vs IND offense, 267 rec yds allowed; 21% of targets unattributed)
- Top receivers: T.Warren (TE1, short/YAC (aDOT <8)) 7/9 83y; J.Downs (WR1, intermediate (aDOT 8-13)) 3/6 47y; K.Allen (WR2, short/YAC (aDOT <8)) 5/9 45y; J.Taylor (RB, short/YAC (aDOT <8)) 3/4 37y
- 20+ catches: J.Downs(WR1) 42y deep_right - J.Brisker [tackler]; L.Treadwell(WR3+) 22y short_right - A.Samuel [tackler]; J.Taylor(RB) 24y short_left - J.Brisker [tackler]; T.Warren(TE1) 29y deep_left - D.Everette [tackler]; T.Warren(TE1) 20y short_middle - J.Ramsey [tackler]
- 15+ runs: J.Taylor(RB) 20y rush left tackle

**Wk6 PIT@TB** (vs TB offense, 164 rec yds allowed; 28% of targets unattributed)
- Top receivers: E.Egbuka (WR1, intermediate (aDOT 8-13)) 7/16 48y 1TD; T.Hurst (WR3+, deep (aDOT 13+)) 3/6 40y; C.Godwin (WR2, short/YAC (aDOT <8)) 4/8 37y; B.Sharp (TE2+, deep (aDOT 13+)) 1/1 21y
- 20+ catches: B.Sharp(TE2+) 21y deep_left - J.Ramsey [tackler]; T.Hurst(WR3+) 22y deep_left - J.Dean [tackler]
- 15+ runs: J.Daniels(QB) 17y rush middle

**Wk7 PIT@NO** (vs NO offense, 278 rec yds allowed; 11% of targets unattributed)
- Top receivers: A.Kamara (RB, short/YAC (aDOT <8)) 7/7 57y; B.Brown (WR3+, intermediate (aDOT 8-13)) 3/3 57y; C.Olave (WR1, intermediate (aDOT 8-13)) 6/10 56y; D.Vele (WR2, intermediate (aDOT 8-13)) 5/5 54y 1TD
- 20+ catches: B.Brown(WR3+) 49y deep_middle - J.Dean [tackler]; D.Vele(WR2) 24y deep_right - D.Elliott [tackler]

**Wk8 CLE@PIT** (vs CLE offense, 326 rec yds allowed; 18% of targets unattributed)
- Top receivers: H.Fannin (TE1, short/YAC (aDOT <8)) 10/12 154y; D.Sampson (RB, short/YAC (aDOT <8)) 6/8 62y; D.Boston (WR1, deep (aDOT 13+)) 6/11 37y; K.Concepcion (WR2, short/YAC (aDOT <8)) 3/4 37y
- 20+ catches: H.Fannin(TE1) 25y deep_right - J.Ramsey [tackler]; K.Concepcion(WR2) 24y deep_left - D.Everette [tackler]; H.Fannin(TE1) 37y deep_right - J.Brisker [tackler]; H.Fannin(TE1) 27y short_left - J.Brisker [tackler]

## Seed notes from defenders/PIT_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 11:21 Harold Fannin Jr. (TE) rec 25 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 2:00 KC Concepcion (WR) rec 24 — Jalen Ramsey [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jamel Dean)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L20/S59/R21)
- Q4 14:22 Harold Fannin Jr. (TE) rec 37 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 6:51 Harold Fannin Jr. (TE) rec 27 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Jamel Dean ← Denzel Boston: 10 tgt, 5 rec, 37 yds — limited his man
- Jalen Ramsey ← KC Concepcion: 4 tgt, 3 rec, 37 yds
- Asante Samuel Jr. ← Jerry Jeudy: 1 tgt, 0 rec, 0 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 CLE@PIT: Harold Fannin Jr. (TE-move/seam) 10/12tgt 154y 0TD | shell 13/82, MOFO 52 (two-high zone) | Trailing-script volume (Watson 39 att); PIT two-high zone (MOFO 52) leaves seams/underneath; pregame TE matchup S Spears-Jennings (inferred) — 10/12 for 154. [inferred]
- wk8 CLE@PIT: Dylan Sampson (RB-receiving/scat) 1-7 0TD; 6/8tgt 62y 0TD | shell 13/82, MOFO 52 (two-high zone) | Check-down valve vs PIT zone while trailing (6/8). [none (no explosive)]
- wk8 CLE@PIT: Deshaun Watson (QB-scrambler) 27/39 324y 0TD 0INT; 3-2 0TD | shell 13/82, MOFO 52 (two-high zone) | Trailing all game → 324y garbage volume vs PIT soft-zone; losing-QB-in-blowout pattern. [inferred]
- wk8 CLE@PIT: KC Concepcion (WR-X outside volume) 3/4tgt 37y 0TD | shell 13/82, MOFO 52 (two-high zone) | Script/volume; no specific matchup attribution — see explosives table. [inferred]
- wk8 CLE@PIT: Denzel Boston (WR-X outside volume) 6/11tgt 37y 0TD | shell 13/82, MOFO 52 (two-high zone) | Script/volume; no specific matchup attribution — see explosives table. [none (no explosive)]

