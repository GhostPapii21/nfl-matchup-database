# DAL DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 DAL@NYG, wk2 WSH@DAL, wk3 BAL@DAL, wk4 DAL@HOU, wk5 TB@DAL, wk6 DAL@GB, wk7 DAL@PHI, wk8 ARI@DAL). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 21.3% / Zone 69.9% | MOF closed 60.2% / MOF open 35.7% | Blitz 23.0% | Light box 47.5% / Heavy box 21.0% | Sub package 67.0% | Sharp YPT allowed WR 9.0, TE 7.7, RB 4.5, Outside 7.4, Slot 11.8

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR2: 10.77 YPT on 31 tgts (league 8.2, +2.57), 6 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 42 | 34 | 213 | 3 | 0 | 5.07 | 5.20 | 26.60 | 5.61 | -0.54 |
| TE1 | 42 | 33 | 312 | 3 | 1 | 7.43 | 5.20 | 39 | 7.39 | 0.04 |
| TE2+ | 15 | 12 | 115 | 1 | 2 | 7.67 | 1.90 | 14.40 | 6.71 | 0.96 |
| WR1 | 71 | 46 | 566 | 5 | 12 | 7.97 | 8.90 | 70.80 | 8.16 | -0.19 |
| WR2 | 31 | 21 | 334 | 2 | 6 | 10.77 | 3.90 | 41.80 | 8.20 | 2.57 |
| WR3+ | 47 | 28 | 413 | 1 | 6 | 8.79 | 5.90 | 51.60 | 7.67 | 1.12 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 28 | 22 | 146 | 2 | 0 | 5.21 | 5.61 | -0.40 |
| TE1 | 27 | 20 | 182 | 1 | 0 | 6.74 | 7.39 | -0.65 |
| TE2+ | 6 | 3 | 15 | 0 | 0 | 2.50 | 6.71 | -4.21 |
| WR1 | 45 | 27 | 320 | 3 | 8 | 7.11 | 8.16 | -1.05 |
| WR2 | 13 | 7 | 130 | 0 | 3 | 10 | 8.20 | 1.80 |
| WR3+ | 20 | 13 | 190 | 0 | 1 | 9.50 | 7.67 | 1.83 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 44 | 38 | 188 | 3 | 0 | 4.27 | 4.58 | -0.31 |
| short_1-9 | 120 | 95 | 904 | 7 | 9 | 7.53 | 6.23 | 1.30 |
| inter_10-19 | 43 | 27 | 466 | 3 | 4 | 10.84 | 10.17 | 0.67 |
| deep_20+ | 41 | 14 | 395 | 2 | 14 | 9.63 | 12.32 | -2.69 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 22 | 8 | 218 | 0 | 6 | 9.91 | 11.28 | -1.37 |
| deep_middle | 8 | 5 | 145 | 0 | 4 | 18.12 | 14.90 | 3.22 |
| deep_right | 24 | 10 | 256 | 2 | 8 | 10.67 | 11.85 | -1.18 |
| short_left | 71 | 54 | 424 | 3 | 1 | 5.97 | 6.08 | -0.11 |
| short_middle | 41 | 32 | 364 | 4 | 3 | 8.88 | 7.43 | 1.45 |
| short_right | 82 | 65 | 546 | 6 | 5 | 6.66 | 5.95 | 0.71 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 48 | 24 | 393 | 2 | 7 | 8.19 | 8.94 | -0.75 |
| intermediate (aDOT 8-13) | 81 | 53 | 734 | 5 | 15 | 9.06 | 7.96 | 1.10 |
| short/YAC (aDOT <8) | 119 | 97 | 826 | 8 | 5 | 6.94 | 6.47 | 0.47 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'TE': 3, 'WR': 24} (27 total, 3.4/g)
- Pass 20+ by depth/direction: {'deep_left': 6, 'deep_middle': 4, 'deep_right': 8, 'short_left': 1, 'short_middle': 3, 'short_right': 5}
- Rush 15+ by position: {'QB': 6, 'RB': 6, 'WR': 2} (14 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 35 | 240 | 6 | 6.86 | 30 |
| RB | 194 | 924 | 6 | 4.76 | 115.50 |
| WR | 7 | 67 | 2 | 9.57 | 8.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DaRon Bland | CB | 7 | 97.40 | 22 | 3.10 | 16 | 210 | 30 | 9.55 | 0 | 4 | 6 | 0 | 0 |
| Shavon Revel Jr. | CB | 6 | 33.30 | 10 | 1.70 | 9 | 106 | 17.70 | 10.60 | 0 | 1 | 1 | 0 | 0 |
| Reddy Steward | CB | 3 | 46 | 9 | 3 | 9 | 92 | 30.70 | 10.22 | 0 | 2 | 0 | 0 | 0 |
| Ameer Speed | CB | 5 | 28 | 6 | 1.20 | 4 | 46 | 9.20 | 7.67 | 0 | 0 | 2 | 0 | 0 |
| Cobie Durant | CB | 4 | 56 | 7 | 1.80 | 5 | 31 | 7.80 | 4.43 | 0 | 0 | 2 | 0 | 0 |
| Joey Porter Jr. | CB | 3 | 53.50 | 6 | 2 | 3 | 19 | 6.30 | 3.17 | 0 | 0 | 3 | 0 | 0 |
| Dee Winters | LB | 6 | 61.20 | 13 | 2.20 | 12 | 112 | 18.70 | 8.62 | 0 | 1 | 0 | 1 | 0 |
| Shemar James | LB | 5 | 55 | 13 | 2.60 | 12 | 100 | 20 | 7.69 | 0 | 0 | 0 | 1 | 0 |
| DeMarvion Overshown | LB | 2 | 70.70 | 8 | 4 | 6 | 55 | 27.50 | 6.88 | 0 | 0 | 1 | 1 | 0 |
| Jaishawn Barham | LB | 5 | 59 | 6 | 1.20 | 6 | 7 | 1.40 | 1.17 | 0 | 0 | 0 | 0 | 0 |
| Caleb Downs | S | 6 | 92.60 | 21 | 3.50 | 20 | 242 | 40.30 | 11.52 | 0 | 3 | 1 | 0 | 0 |
| Malik Hooker | S | 6 | 61.20 | 15 | 2.50 | 13 | 234 | 39 | 15.60 | 0 | 3 | 2 | 0 | 0 |
| Markquese Bell | S | 5 | 45.60 | 14 | 2.80 | 13 | 198 | 39.60 | 14.14 | 0 | 5 | 1 | 0 | 0 |
| P.J. Locke | S | 3 | 43 | 6 | 2 | 6 | 79 | 26.30 | 13.17 | 0 | 1 | 0 | 0 | 0 |
| Jalen Thompson | S | 2 | 80.70 | 5 | 2.50 | 5 | 71 | 35.50 | 14.20 | 0 | 1 | 0 | 0 | 0 |
| Alijah Clark | S | 2 | 25 | 4 | 2 | 2 | 45 | 22.50 | 11.25 | 0 | 1 | 2 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **DaRon Bland** (CB): WR1:11t/105y, WR3+:4t/58y, WR2:3t/24y, RB:3t/18y, TE2+:1t/5y | 20+: wk4 J.Noel(WR3+) 52 deep_left; wk5 E.Egbuka(WR1) 21 deep_left; wk8 Mi.Wilson(WR1) 21 deep_right; wk8 Mi.Wilson(WR1) 27 deep_right
- **Shavon Revel Jr.** (CB): WR1:3t/52y, TE1:3t/33y, WR2:2t/13y, WR3+:2t/8y | 20+: wk6 M.Golden(WR1) 37 deep_left
- **Reddy Steward** (CB): WR1:5t/61y, WR2:2t/18y, WR3+:1t/9y, TE1:1t/4y | 20+: wk3 Z.Flowers(WR1) 27 deep_middle; wk4 X.Hutchinson(WR1) 26 short_middle
- **Ameer Speed** (CB): RB:1t/15y, WR3+:1t/14y, WR1:3t/9y, WR2:1t/8y
- **Cobie Durant** (CB): TE1:2t/13y, RB:1t/10y, WR1:3t/8y, WR3+:1t/0y
- **Joey Porter Jr.** (CB): WR1:3t/14y, TE1:1t/5y, WR2:1t/0y, WR3+:1t/0y
- **Dee Winters** (LB): TE1:4t/45y, WR2:2t/29y, RB:3t/14y, WR1:2t/14y, WR3+:2t/10y | 20+: wk4 D.Schultz(TE1) 21 short_right
- **Shemar James** (LB): RB:5t/40y, TE1:3t/34y, WR2:1t/14y, WR3+:3t/12y, TE2+:1t/0y
- **DeMarvion Overshown** (LB): RB:2t/22y, TE1:3t/13y, WR1:1t/9y, WR3+:1t/7y, TE2+:1t/4y
- **Jaishawn Barham** (LB): TE2+:1t/6y, WR2:1t/6y, RB:3t/1y, WR3+:1t/-6y
- **Caleb Downs** (S): WR3+:5t/72y, WR1:4t/54y, TE1:5t/50y, WR2:3t/42y, RB:3t/23y, TE2+:1t/1y | 20+: wk4 J.Noel(WR3+) 22 deep_right; wk6 C.Watson(WR2) 28 deep_middle; wk6 M.Golden(WR1) 21 deep_left
- **Malik Hooker** (S): WR3+:3t/94y, WR2:1t/45y, TE2+:2t/33y, RB:2t/31y, TE1:4t/18y, WR1:3t/13y | 20+: wk4 N.Collins(WR2) 45 deep_middle; wk4 C.Stover(TE2+) 20 short_right; wk5 T.Johnson(WR3+) 64 deep_right
- **Markquese Bell** (S): WR1:6t/83y, TE2+:3t/49y, WR3+:3t/42y, WR2:1t/19y, TE1:1t/5y | 20+: wk2 T.McLaurin(WR3+) 24 deep_right; wk3 Z.Flowers(WR1) 22 short_middle; wk3 M.Hibner(TE2+) 21 short_right; wk6 M.Golden(WR1) 21 short_right; wk7 M.Lemon(WR1) 21 short_left
- **P.J. Locke** (S): TE1:3t/37y, WR2:1t/29y, WR3+:1t/7y, TE2+:1t/6y | 20+: wk8 K.Bourne(WR2) 29 short_middle
- **Jalen Thompson** (S): WR3+:1t/26y, WR1:2t/23y, RB:1t/13y, TE2+:1t/9y | 20+: wk2 T.McLaurin(WR3+) 26 short_right
- **Alijah Clark** (S): WR2:1t/31y, WR1:1t/14y, TE2+:1t/0y, WR3+:1t/0y | 20+: wk3 R.Bateman(WR2) 31 deep_left

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DAL@NYG | Jalen Thompson | S | 3 | 3 | 35 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1, M.Nabersx1, D.Singletaryx1 |
| 1 | DAL@NYG | Dee Winters | LB | 3 | 3 | 33 | 0 | 0 | 0 | 0 | 0 | M.Fieldsx1, I.Likelyx1, D.Mooneyx1 |
| 1 | DAL@NYG | DaRon Bland | CB | 4 | 4 | 30 | 0 | 0 | 0 | 0 | 0 | M.Nabersx2, M.Fieldsx1, D.Singletaryx1 |
| 1 | DAL@NYG | Caleb Downs | S | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | M.Nabersx2, I.Likelyx1 |
| 1 | DAL@NYG | Shavon Revel Jr. | CB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | I.Likelyx1 |
| 1 | DAL@NYG | Malik Hooker | S | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | I.Likelyx1 |
| 1 | DAL@NYG | P.J. Locke | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | I.Likelyx1 |
| 1 | DAL@NYG | Cobie Durant | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | M.Nabersx1 |
| 1 | DAL@NYG | Jaishawn Barham | LB | 1 | 1 | -7 | 0 | 0 | 0 | 0 | 0 | D.Singletaryx1 |
| 2 | WSH@DAL | Markquese Bell | S | 2 | 2 | 38 | 0 | 1 | 0 | 0 | 0 | T.McLaurinx1, C.Yankoffx1 |
| 2 | WSH@DAL | Jalen Thompson | S | 2 | 2 | 36 | 0 | 1 | 0 | 0 | 0 | S.Diggsx1, T.McLaurinx1 |
| 2 | WSH@DAL | Caleb Downs | S | 4 | 3 | 32 | 0 | 0 | 1 | 0 | 0 | R.Whitex1, T.McLaurinx1, D.Brownx1, A.Williamsx1 |
| 2 | WSH@DAL | Dee Winters | LB | 4 | 4 | 30 | 0 | 0 | 0 | 0 | 0 | R.Whitex2, D.Brownx1, A.Williamsx1 |
| 2 | WSH@DAL | Shavon Revel Jr. | CB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | T.McLaurinx1, A.Williamsx1, D.Brownx1 |
| 2 | WSH@DAL | DaRon Bland | CB | 3 | 2 | 13 | 0 | 0 | 1 | 0 | 0 | S.Diggsx2, T.McLaurinx1 |
| 2 | WSH@DAL | Shemar James | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | R.Whitex1 |
| 2 | WSH@DAL | P.J. Locke | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | B.Sinnottx1 |
| 2 | WSH@DAL | Cobie Durant | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.McLaurinx1 |
| 2 | WSH@DAL | Jaishawn Barham | LB | 2 | 2 | -4 | 0 | 0 | 0 | 0 | 0 | R.Whitex1, D.Brownx1 |
| 3 | BAL@DAL | Markquese Bell | S | 4 | 4 | 62 | 0 | 2 | 0 | 0 | 0 | Z.Flowersx1, J.Cuevasx1, M.Hibnerx1, M.Andrewsx1 |
| 3 | BAL@DAL | Alijah Clark | S | 3 | 2 | 45 | 0 | 1 | 1 | 0 | 0 | D.Walkerx1, R.Batemanx1, Z.Flowersx1 |
| 3 | BAL@DAL | Reddy Steward | CB | 1 | 1 | 27 | 0 | 1 | 0 | 0 | 0 | Z.Flowersx1 |
| 3 | BAL@DAL | Dee Winters | LB | 2 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | M.Andrewsx1, Z.Flowersx1 |
| 3 | BAL@DAL | Shavon Revel Jr. | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx1 |
| 3 | BAL@DAL | Jaishawn Barham | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | R.Batemanx1 |
| 4 | DAL@HOU | Malik Hooker | S | 6 | 5 | 99 | 0 | 2 | 1 | 0 | 0 | X.Hutchinsonx2, N.Collinsx1, B.Jordanx1, C.Stoverx1, J.Noelx1 |
| 4 | DAL@HOU | DaRon Bland | CB | 3 | 3 | 76 | 0 | 1 | 0 | 0 | 0 | J.Noelx1, N.Collinsx1, K.Bouttex1 |
| 4 | DAL@HOU | Reddy Steward | CB | 4 | 4 | 53 | 0 | 1 | 0 | 0 | 0 | N.Collinsx2, X.Hutchinsonx1, K.Bouttex1 |
| 4 | DAL@HOU | Caleb Downs | S | 4 | 4 | 40 | 0 | 1 | 0 | 0 | 0 | D.Schultzx1, X.Hutchinsonx1, J.Noelx1, F.Moreaux1 |
| 4 | DAL@HOU | Dee Winters | LB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | D.Schultzx1 |
| 4 | DAL@HOU | Ameer Speed | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | N.Collinsx1 |
| 5 | TB@DAL | Malik Hooker | S | 2 | 2 | 67 | 0 | 1 | 0 | 0 | 0 | E.Egbukax1, T.Johnsonx1 |
| 5 | TB@DAL | DaRon Bland | CB | 4 | 3 | 32 | 0 | 1 | 1 | 0 | 0 | E.Egbukax3, P.Durhamx1 |
| 5 | TB@DAL | Shemar James | LB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | C.Godwinx1, C.Ottonx1 |
| 5 | TB@DAL | Markquese Bell | S | 2 | 1 | 19 | 0 | 0 | 1 | 0 | 0 | E.Egbukax1, C.Godwinx1 |
| 5 | TB@DAL | Ameer Speed | CB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | K.Gainwellx1 |
| 5 | TB@DAL | Reddy Steward | CB | 4 | 4 | 12 | 0 | 0 | 0 | 0 | 0 | E.Egbukax3, C.Ottonx1 |
| 5 | TB@DAL | Dee Winters | LB | 2 | 2 | 5 | 0 | 0 | 0 | 0 | 0 | C.Ottonx1, K.Gainwellx1 |
| 5 | TB@DAL | Shavon Revel Jr. | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | C.Godwinx1 |
| 6 | DAL@GB | Caleb Downs | S | 7 | 7 | 98 | 0 | 2 | 0 | 0 | 0 | C.Watsonx2, T.Kraftx2, S.Williamsx1, P.Strongx1, M.Goldenx1 |
| 6 | DAL@GB | Shavon Revel Jr. | CB | 3 | 3 | 51 | 0 | 1 | 0 | 0 | 0 | T.Kraftx2, M.Goldenx1 |
| 6 | DAL@GB | Markquese Bell | S | 3 | 3 | 32 | 0 | 1 | 0 | 0 | 0 | M.Goldenx2, S.Williamsx1 |
| 6 | DAL@GB | Shemar James | LB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | S.Williamsx2, P.Strongx1 |
| 6 | DAL@GB | Malik Hooker | S | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | P.Strongx1, T.Kraftx1 |
| 6 | DAL@GB | DaRon Bland | CB | 3 | 1 | 10 | 0 | 0 | 2 | 0 | 0 | P.Strongx1, C.Watsonx1, M.Goldenx1 |
| 6 | DAL@GB | Jaishawn Barham | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | P.Strongx1 |
| 6 | DAL@GB | Ameer Speed | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | M.Goldenx1 |
| 6 | DAL@GB | Dee Winters | LB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | M.Goldenx1 |
| 6 | DAL@GB | Joey Porter Jr. | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | C.Watsonx1, M.Goldenx1 |
| 7 | DAL@PHI | Markquese Bell | S | 3 | 3 | 47 | 0 | 1 | 0 | 0 | 0 | M.Lemonx2, M.Brownx1 |
| 7 | DAL@PHI | Shemar James | LB | 4 | 4 | 40 | 0 | 0 | 0 | 0 | 0 | D.Goedertx2, E.Moorex1, E.Mitchellx1 |
| 7 | DAL@PHI | DeMarvion Overshown | LB | 5 | 3 | 30 | 0 | 0 | 1 | 1 | 0 | D.Goedertx3, M.Lemonx1, E.Mitchellx1 |
| 7 | DAL@PHI | Caleb Downs | S | 2 | 2 | 29 | 0 | 0 | 0 | 0 | 0 | S.Barkleyx1, D.Cooperx1 |
| 7 | DAL@PHI | Malik Hooker | S | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | M.Brownx1 |
| 7 | DAL@PHI | Ameer Speed | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | E.Moorex1 |
| 7 | DAL@PHI | Joey Porter Jr. | CB | 3 | 2 | 10 | 0 | 0 | 1 | 0 | 0 | D.Goedertx1, M.Brownx1, M.Lemonx1 |
| 7 | DAL@PHI | Shavon Revel Jr. | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1 |
| 7 | DAL@PHI | Cobie Durant | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1 |
| 7 | DAL@PHI | DaRon Bland | CB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | D.Piercex1 |
| 7 | DAL@PHI | Alijah Clark | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | E.Stowersx1 |
| 8 | ARI@DAL | P.J. Locke | S | 4 | 4 | 61 | 0 | 1 | 0 | 0 | 0 | T.McBridex2, K.Bournex1, D.Duvernayx1 |
| 8 | ARI@DAL | DaRon Bland | CB | 4 | 2 | 48 | 0 | 2 | 2 | 0 | 0 | Mi.Wilsonx3, R.Virgilx1 |
| 8 | ARI@DAL | Cobie Durant | CB | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | T.McBridex2, Mi.Wilsonx1, Z.Knightx1 |
| 8 | ARI@DAL | DeMarvion Overshown | LB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | E.Higginsx1, T.Allgeierx1, D.Duvernayx1 |
| 8 | ARI@DAL | Malik Hooker | S | 3 | 2 | 22 | 0 | 0 | 1 | 0 | 0 | T.McBridex2, T.Allgeierx1 |
| 8 | ARI@DAL | Caleb Downs | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | T.McBridex1 |
| 8 | ARI@DAL | Ameer Speed | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | Mi.Wilsonx2 |
| 8 | ARI@DAL | Joey Porter Jr. | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | Mi.Wilsonx1 |
| 8 | ARI@DAL | Shemar James | LB | 3 | 2 | 8 | 0 | 0 | 0 | 1 | 0 | T.Allgeierx2, E.Higginsx1 |
| 8 | ARI@DAL | Jaishawn Barham | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | E.Higginsx1 |

## Who beat them each week

**Wk1 DAL@NYG** (vs NYG offense, 230 rec yds allowed; 31% of targets unattributed)
- Top receivers: I.Likely (TE1, short/YAC (aDOT <8)) 8/8 78y 2TD; M.Nabers (WR1, intermediate (aDOT 8-13)) 6/9 69y; D.Mooney (WR3+, deep (aDOT 13+)) 2/2 27y; M.Fields (WR2, deep (aDOT 13+)) 2/4 25y
- 15+ runs: J.Dart(QB) 22y rush left end; J.Dart(QB) 16y rush left end

**Wk2 WSH@DAL** (vs WSH offense, 207 rec yds allowed; 26% of targets unattributed)
- Top receivers: T.McLaurin (WR3+, intermediate (aDOT 8-13)) 2/9 50y; S.Diggs (WR1, intermediate (aDOT 8-13)) 5/6 47y 2TD; R.White (RB, short/YAC (aDOT <8)) 6/6 40y; A.Williams (WR2, intermediate (aDOT 8-13)) 3/3 24y
- 20+ catches: T.McLaurin(WR3+) 24y deep_right - M.Bell [tackler]; T.McLaurin(WR3+) 26y short_right - J.Thompson [tackler]; S.Diggs(WR1) 20y deep_right TD - no tackler named [unattributed]
- 15+ runs: J.Daniels(QB) 18y rush right end; J.Daniels(QB) 20y rush middle

**Wk3 BAL@DAL** (vs BAL offense, 186 rec yds allowed; 30% of targets unattributed)
- Top receivers: Z.Flowers (WR1, intermediate (aDOT 8-13)) 5/6 84y; R.Bateman (WR2, deep (aDOT 13+)) 2/3 37y; M.Andrews (TE1, short/YAC (aDOT <8)) 3/5 24y; M.Hibner (TE2+, short/YAC (aDOT <8)) 2/2 23y 1TD
- 20+ catches: Z.Flowers(WR1) 22y short_middle - M.Bell [tackler]; M.Hibner(TE2+) 21y short_right - M.Bell [tackler]; R.Bateman(WR2) 31y deep_left - A.Clark [tackler]; Z.Flowers(WR1) 27y deep_middle - R.Steward [tackler]
- 15+ runs: L.Jackson(QB) 21y rush right end; D.Henry(RB) 29y rush right tackle; Z.Flowers(WR) 20y rush left end; L.Jackson(QB) 17y rush right end

**Wk4 DAL@HOU** (vs HOU offense, 347 rec yds allowed; 27% of targets unattributed)
- Top receivers: N.Collins (WR2, intermediate (aDOT 8-13)) 7/8 118y 2TD; J.Noel (WR3+, intermediate (aDOT 8-13)) 3/3 85y; X.Hutchinson (WR1, intermediate (aDOT 8-13)) 3/5 46y; K.Boutte (WR3+, intermediate (aDOT 8-13)) 3/4 36y
- 20+ catches: N.Collins(WR2) 45y deep_middle - M.Hooker [tackler]; J.Noel(WR3+) 52y deep_left - D.Bland [tackler]; N.Collins(WR2) 22y deep_right TD - no tackler named [unattributed]; C.Stover(TE2+) 20y short_right - M.Hooker [tackler]; K.Boutte(WR3+) 21y deep_right - no tackler named [unattributed]; X.Hutchinson(WR1) 26y short_middle - R.Steward [tackler]; J.Noel(WR3+) 22y deep_right - C.Downs [tackler]; D.Schultz(TE1) 21y short_right - D.Winters [tackler]

**Wk5 TB@DAL** (vs TB offense, 189 rec yds allowed; 16% of targets unattributed)
- Top receivers: T.Johnson (WR3+, deep (aDOT 13+)) 1/1 64y; E.Egbuka (WR1, intermediate (aDOT 8-13)) 6/9 38y; C.Godwin (WR2, short/YAC (aDOT <8)) 3/3 37y; C.Otton (TE1, short/YAC (aDOT <8)) 3/4 25y
- 20+ catches: T.Johnson(WR3+) 64y deep_right - M.Hooker [tackler]; E.Egbuka(WR1) 21y deep_left - D.Bland [tackler]
- 15+ runs: B.Irving(RB) 72y rush left tackle; B.Irving(RB) 22y rush right tackle

**Wk6 DAL@GB** (vs GB offense, 276 rec yds allowed; 30% of targets unattributed)
- Top receivers: M.Golden (WR1, deep (aDOT 13+)) 6/13 104y 1TD; C.Watson (WR2, deep (aDOT 13+)) 3/8 64y; P.Strong (RB, short/YAC (aDOT <8)) 5/6 39y; T.Kraft (TE1, short/YAC (aDOT <8)) 5/8 37y
- 20+ catches: C.Watson(WR2) 27y deep_middle - no tackler named [unattributed]; M.Golden(WR1) 37y deep_left - S.Revel [tackler]; C.Watson(WR2) 28y deep_middle - C.Downs [tackler]; M.Golden(WR1) 21y deep_left - C.Downs [tackler]; M.Golden(WR1) 21y short_right - M.Bell [tackler]

**Wk7 DAL@PHI** (vs PHI offense, 211 rec yds allowed; 21% of targets unattributed)
- Top receivers: M.Lemon (WR1, short/YAC (aDOT <8)) 7/8 67y 1TD; D.Goedert (TE1, short/YAC (aDOT <8)) 5/7 48y; M.Brown (WR3+, deep (aDOT 13+)) 2/5 30y; E.Mitchell (RB, short/YAC (aDOT <8)) 3/4 23y
- 20+ catches: M.Lemon(WR1) 21y short_left - M.Bell [tackler]
- 15+ runs: S.Barkley(RB) 29y rush left tackle

**Wk8 ARI@DAL** (vs ARI offense, 307 rec yds allowed; 34% of targets unattributed)
- Top receivers: Mi.Wilson (WR1, intermediate (aDOT 8-13)) 8/15 111y 1TD; T.McBride (TE1, short/YAC (aDOT <8)) 7/8 72y 1TD; T.Allgeier (RB, short/YAC (aDOT <8)) 5/5 44y 1TD; K.Bourne (WR2, short/YAC (aDOT <8)) 1/2 29y
- 20+ catches: Mi.Wilson(WR1) 22y deep_left - no tackler named [unattributed]; K.Bourne(WR2) 29y short_middle - P.Locke [tackler]; Mi.Wilson(WR1) 21y deep_right - D.Bland [tackler]; Mi.Wilson(WR1) 27y deep_right - D.Bland [tackler]
- 15+ runs: T.Allgeier(RB) 63y rush middle; T.Allgeier(RB) 52y rush left end; Mi.Wilson(WR) 17y rush left end

## Seed notes from defenders/DAL_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 1:49 Michael Wilson (WR) rec 22 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q2 5:11 Kendrick Bourne (WR) rec 29 — Caleb Downs [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said DaRon Bland)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L18/S69/R13)
- Q3 0:57 Tyler Allgeier (RB) rush 63 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 14:20 Tyler Allgeier (RB) rush 52 — D.Bland [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 0:50 Michael Wilson (WR) rec 21 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q4 0:27 Michael Wilson (WR) rec 27 — Joey Porter Jr. [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Q5 5:43 Michael Wilson (WR) rush 17 — S.James [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L30/S18/R52)
- Joey Porter Jr. ← Michael Wilson: 15 tgt, 8 rec, 111 yds
- Caleb Downs ← Kendrick Bourne: 2 tgt, 1 rec, 29 yds

