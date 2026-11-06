# LAR DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 SF@LAR, wk2 NYG@LAR, wk3 LAR@DEN, wk4 LAR@PHI, wk5 BUF@LAR, wk6 ARI@LAR, wk7 LAR@LV, wk8 LAC@LAR). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 22.7% / Zone 68.7% | MOF closed 38.7% / MOF open 55.6% | Blitz 26.6% | Light box 50.7% / Heavy box 20.1% | Sub package 67.0% | Sharp YPT allowed WR 6.7, TE 5.0, RB 6.7, Outside 6.2, Slot 7.7

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- nothing flagged

Holds (-1.5 YPT or better): TE1: 5.35 YPT on 43 tgts (league 7.39, -2.04); TE2+: 5.15 YPT on 26 tgts (league 6.71, -1.56); WR1: 6.66 YPT on 50 tgts (league 8.16, -1.5); WR2: 5.72 YPT on 40 tgts (league 8.2, -2.48)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 55 | 44 | 346 | 1 | 4 | 6.29 | 6.90 | 43.20 | 5.61 | 0.68 |
| TE1 | 43 | 26 | 230 | 0 | 1 | 5.35 | 5.40 | 28.80 | 7.39 | -2.04 |
| TE2+ | 26 | 14 | 134 | 1 | 1 | 5.15 | 3.20 | 16.80 | 6.71 | -1.56 |
| WR1 | 50 | 27 | 333 | 2 | 3 | 6.66 | 6.20 | 41.60 | 8.16 | -1.50 |
| WR2 | 40 | 23 | 229 | 2 | 2 | 5.72 | 5 | 28.60 | 8.20 | -2.48 |
| WR3+ | 37 | 20 | 334 | 4 | 7 | 9.03 | 4.60 | 41.80 | 7.67 | 1.36 |
| other | 1 | 1 | 2 | 0 | 0 | 2 | 0.10 | 0.20 | 2.86 | -0.86 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 28 | 25 | 243 | 1 | 4 | 8.68 | 5.61 | 3.07 |
| TE1 | 26 | 19 | 185 | 0 | 1 | 7.12 | 7.39 | -0.27 |
| TE2+ | 14 | 9 | 94 | 0 | 1 | 6.71 | 6.71 | 0 |
| WR1 | 25 | 15 | 246 | 1 | 3 | 9.84 | 8.16 | 1.68 |
| WR2 | 20 | 12 | 105 | 1 | 1 | 5.25 | 8.20 | -2.95 |
| WR3+ | 15 | 7 | 120 | 0 | 3 | 8 | 7.67 | 0.33 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 66 | 52 | 285 | 0 | 2 | 4.32 | 4.58 | -0.26 |
| short_1-9 | 109 | 71 | 675 | 4 | 4 | 6.19 | 6.23 | -0.04 |
| inter_10-19 | 50 | 26 | 464 | 5 | 6 | 9.28 | 10.17 | -0.89 |
| deep_20+ | 22 | 6 | 184 | 1 | 6 | 8.36 | 12.32 | -3.96 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 9 | 3 | 97 | 1 | 3 | 10.78 | 11.28 | -0.50 |
| deep_middle | 10 | 4 | 98 | 1 | 3 | 9.80 | 14.90 | -5.10 |
| deep_right | 16 | 3 | 94 | 1 | 2 | 5.88 | 11.85 | -5.97 |
| short_left | 90 | 58 | 522 | 1 | 3 | 5.80 | 6.08 | -0.28 |
| short_middle | 42 | 27 | 293 | 1 | 2 | 6.98 | 7.43 | -0.45 |
| short_right | 80 | 60 | 504 | 5 | 5 | 6.30 | 5.95 | 0.35 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 46 | 26 | 343 | 3 | 6 | 7.46 | 8.94 | -1.48 |
| intermediate (aDOT 8-13) | 72 | 34 | 406 | 3 | 4 | 5.64 | 7.96 | -2.32 |
| short/YAC (aDOT <8) | 134 | 95 | 859 | 4 | 8 | 6.41 | 6.47 | -0.06 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 4, 'TE': 2, 'WR': 12} (18 total, 2.2/g)
- Pass 20+ by depth/direction: {'deep_left': 3, 'deep_middle': 3, 'deep_right': 2, 'short_left': 3, 'short_middle': 2, 'short_right': 5}
- Rush 15+ by position: {'QB': 5, 'RB': 7} (12 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 35 | 199 | 5 | 5.69 | 24.90 |
| RB | 180 | 649 | 7 | 3.61 | 81.10 |
| WR | 2 | 26 | 0 | 13 | 3.20 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Josh Wallace | CB | 7 | 72.50 | 24 | 3.40 | 19 | 176 | 25.10 | 7.33 | 0 | 2 | 4 | 1 | 0 |
| Jaylen Watson | CB | 7 | 84 | 23 | 3.30 | 14 | 162 | 23.10 | 7.04 | 0 | 1 | 8 | 1 | 0 |
| Trent McDuffie | CB | 5 | 96.50 | 20 | 4 | 12 | 65 | 13 | 3.25 | 0 | 1 | 6 | 2 | 0 |
| Emmanuel Forbes | CB | 4 | 32.80 | 6 | 1.50 | 4 | 21 | 5.20 | 3.50 | 0 | 0 | 2 | 0 | 0 |
| Nate Landman | LB | 7 | 88.60 | 13 | 1.90 | 12 | 70 | 10 | 5.38 | 0 | 0 | 1 | 0 | 0 |
| Omar Speights | LB | 6 | 45 | 9 | 1.50 | 7 | 43 | 7.20 | 4.78 | 0 | 1 | 2 | 0 | 0 |
| Kam Curl | S | 8 | 93 | 18 | 2.20 | 16 | 246 | 30.80 | 13.67 | 0 | 5 | 2 | 0 | 0 |
| Quentin Lake | S | 7 | 100 | 35 | 5 | 24 | 228 | 32.60 | 6.51 | 0 | 2 | 8 | 3 | 0 |
| Kamren Kinchens | S | 6 | 68.20 | 13 | 2.20 | 12 | 191 | 31.80 | 14.69 | 0 | 1 | 1 | 0 | 0 |
| Jaylen McCollough | S | 3 | 35.90 | 4 | 1.30 | 4 | 33 | 11 | 8.25 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Josh Wallace** (CB): WR1:7t/73y, WR3+:2t/36y, TE1:6t/28y, WR2:4t/15y, TE2+:2t/14y, RB:3t/10y | 20+: wk6 J.Brooks(WR3+) 21 deep_middle; wk7 T.Tucker(WR1) 41 short_right
- **Jaylen Watson** (CB): WR3+:4t/67y, WR1:10t/42y, WR2:4t/30y, RB:1t/10y, TE1:3t/9y, TE2+:1t/4y | 20+: wk8 L.McConkey(WR3+) 54 deep_right
- **Trent McDuffie** (CB): WR3+:4t/29y, WR2:3t/16y, WR1:6t/14y, TE1:3t/5y, RB:3t/1y, TE2+:1t/0y | 20+: wk3 T.Franklin(WR3+) 21 short_right
- **Emmanuel Forbes** (CB): WR1:2t/12y, WR2:3t/9y, WR3+:1t/0y
- **Nate Landman** (LB): TE2+:2t/25y, WR3+:2t/13y, TE1:1t/12y, RB:5t/9y, WR1:1t/6y, WR2:1t/3y, other:1t/2y
- **Omar Speights** (LB): WR2:2t/26y, RB:4t/12y, TE2+:2t/6y, WR3+:1t/-1y | 20+: wk8 Q.Johnston(WR2) 21 deep_middle
- **Kam Curl** (S): RB:9t/87y, WR3+:2t/72y, TE1:3t/54y, TE2+:4t/33y | 20+: wk2 D.Mooney(WR3+) 33 deep_left; wk3 P.Bryant(WR3+) 39 short_right; wk5 T.Johnson(RB) 26 short_left; wk6 T.McBride(TE1) 26 short_middle; wk8 C.Kolar(TE2+) 20 short_right
- **Quentin Lake** (S): RB:7t/64y, TE1:12t/43y, WR3+:3t/41y, WR2:5t/41y, WR1:4t/27y, TE2+:4t/12y | 20+: wk5 R.Davis(RB) 31 short_left; wk8 L.McConkey(WR3+) 30 short_left
- **Kamren Kinchens** (S): WR1:5t/101y, TE1:3t/48y, TE2+:3t/32y, WR2:1t/10y, RB:1t/0y | 20+: wk5 K.Shakir(WR1) 57 short_middle
- **Jaylen McCollough** (S): TE1:2t/19y, RB:2t/14y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SF@LAR | Quentin Lake | S | 9 | 6 | 52 | 0 | 0 | 2 | 1 | 0 | G.Kittlex2, M.Evansx2, C.McCaffreyx2, L.Farrellx1, D.Robinsonx1, D.Samuelx1 |
| 1 | SF@LAR | Jaylen Watson | CB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | M.Evansx2, G.Kittlex1 |
| 1 | SF@LAR | Trent McDuffie | CB | 6 | 4 | 23 | 0 | 0 | 2 | 0 | 0 | D.Samuelx2, G.Kittlex1, D.Robinsonx1, M.Evansx1, C.McCaffreyx1 |
| 1 | SF@LAR | Kamren Kinchens | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | L.Farrellx1 |
| 1 | SF@LAR | Kam Curl | S | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | K.Blackx1, C.McCaffreyx1 |
| 1 | SF@LAR | Nate Landman | LB | 3 | 2 | 5 | 0 | 0 | 1 | 0 | 0 | J.Brendelx1, C.McCaffreyx1, D.Samuelx1 |
| 1 | SF@LAR | Omar Speights | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | C.McCaffreyx1 |
| 2 | NYG@LAR | Kam Curl | S | 4 | 3 | 48 | 0 | 1 | 1 | 0 | 0 | C.Skattebox1, T.Johnsonx1, D.Mooneyx1, I.Likelyx1 |
| 2 | NYG@LAR | Jaylen Watson | CB | 4 | 3 | 35 | 0 | 0 | 1 | 0 | 0 | M.Fieldsx3, I.Likelyx1 |
| 2 | NYG@LAR | Quentin Lake | S | 7 | 4 | 29 | 0 | 0 | 3 | 0 | 0 | I.Likelyx4, C.Skattebox2, T.Johnsonx1 |
| 2 | NYG@LAR | Josh Wallace | CB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | M.Nabersx1, D.Mooneyx1 |
| 2 | NYG@LAR | Trent McDuffie | CB | 5 | 1 | 5 | 0 | 0 | 3 | 1 | 0 | M.Nabersx3, I.Likelyx2 |
| 2 | NYG@LAR | Emmanuel Forbes | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | M.Fieldsx1 |
| 2 | NYG@LAR | Nate Landman | LB | 1 | 1 | -2 | 0 | 0 | 0 | 0 | 0 | C.Skattebox1 |
| 3 | LAR@DEN | Kam Curl | S | 3 | 3 | 70 | 0 | 1 | 0 | 0 | 0 | R.Harveyx1, T.Badiex1, P.Bryantx1 |
| 3 | LAR@DEN | Trent McDuffie | CB | 3 | 2 | 22 | 0 | 1 | 1 | 0 | 0 | J.Waddlex2, T.Franklinx1 |
| 3 | LAR@DEN | Quentin Lake | S | 4 | 3 | 16 | 0 | 0 | 1 | 0 | 0 | R.Harveyx2, C.Suttonx2 |
| 3 | LAR@DEN | Omar Speights | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | J.Dobbinsx1 |
| 3 | LAR@DEN | Nate Landman | LB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | R.Harveyx1 |
| 3 | LAR@DEN | Jaylen Watson | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | J.Waddlex2 |
| 3 | LAR@DEN | Josh Wallace | CB | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | C.Suttonx1, E.Engramx1 |
| 4 | LAR@PHI | Kamren Kinchens | S | 5 | 4 | 32 | 0 | 0 | 1 | 0 | 0 | M.Lemonx3, W.Shipleyx1, Z.Ertzx1 |
| 4 | LAR@PHI | Nate Landman | LB | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | D.Wicksx2, Z.Ertzx1 |
| 4 | LAR@PHI | Trent McDuffie | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | D.Cooperx1 |
| 4 | LAR@PHI | Josh Wallace | CB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | S.Barkleyx1 |
| 4 | LAR@PHI | Kam Curl | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | Z.Ertzx1 |
| 5 | BUF@LAR | Kamren Kinchens | S | 2 | 2 | 74 | 0 | 1 | 0 | 0 | 0 | K.Shakirx2 |
| 5 | BUF@LAR | Kam Curl | S | 2 | 2 | 31 | 0 | 1 | 0 | 0 | 0 | T.Johnsonx2 |
| 5 | BUF@LAR | Quentin Lake | S | 1 | 1 | 31 | 0 | 1 | 0 | 0 | 0 | R.Davisx1 |
| 5 | BUF@LAR | Josh Wallace | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | D.Kincaidx1 |
| 5 | BUF@LAR | Nate Landman | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | K.Shakirx1 |
| 5 | BUF@LAR | Omar Speights | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | D.Knoxx1 |
| 5 | BUF@LAR | Jaylen Watson | CB | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | K.Colemanx1, S.Bellx1 |
| 6 | ARI@LAR | Josh Wallace | CB | 7 | 5 | 41 | 0 | 1 | 2 | 0 | 0 | Mi.Wilsonx3, K.Bournex2, T.McBridex1, J.Brooksx1 |
| 6 | ARI@LAR | Quentin Lake | S | 6 | 5 | 39 | 0 | 0 | 0 | 1 | 0 | T.McBridex3, K.Bournex1, E.Higginsx1, Mi.Wilsonx1 |
| 6 | ARI@LAR | Kam Curl | S | 1 | 1 | 26 | 0 | 1 | 0 | 0 | 0 | T.McBridex1 |
| 6 | ARI@LAR | Nate Landman | LB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | Z.Knightx1, E.Higginsx1 |
| 6 | ARI@LAR | Jaylen Watson | CB | 4 | 4 | 21 | 0 | 0 | 0 | 0 | 0 | E.Higginsx1, T.Allgeierx1, J.Brooksx1, T.McBridex1 |
| 6 | ARI@LAR | Kamren Kinchens | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | T.McBridex1 |
| 6 | ARI@LAR | Emmanuel Forbes | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | K.Bournex1 |
| 6 | ARI@LAR | Omar Speights | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | K.Bournex1 |
| 6 | ARI@LAR | Jaylen McCollough | S | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | T.McBridex1 |
| 7 | LAR@LV | Josh Wallace | CB | 7 | 6 | 78 | 0 | 1 | 1 | 0 | 0 | B.Bowersx2, J.Nailorx1, A.Jeantyx1, I.Thomasx1, T.Tuckerx1, M.Mayerx1 |
| 7 | LAR@LV | Kamren Kinchens | S | 3 | 3 | 47 | 0 | 0 | 0 | 0 | 0 | B.Bowersx2, M.Mayerx1 |
| 7 | LAR@LV | Jaylen McCollough | S | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, B.Bowersx1 |
| 7 | LAR@LV | Jaylen Watson | CB | 6 | 2 | 17 | 0 | 0 | 4 | 0 | 0 | T.Tuckerx5, C.Whitex1 |
| 7 | LAR@LV | Quentin Lake | S | 3 | 2 | 13 | 0 | 0 | 1 | 0 | 0 | B.Bowersx1, T.Tuckerx1, J.Nailorx1 |
| 7 | LAR@LV | Emmanuel Forbes | CB | 3 | 2 | 12 | 0 | 0 | 1 | 0 | 0 | T.Tuckerx2, C.Whitex1 |
| 7 | LAR@LV | Kam Curl | S | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, M.Mayerx1 |
| 7 | LAR@LV | Omar Speights | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1 |
| 8 | LAC@LAR | Jaylen Watson | CB | 2 | 2 | 64 | 0 | 1 | 0 | 0 | 0 | L.McConkeyx1, T.Harrisx1 |
| 8 | LAC@LAR | Quentin Lake | S | 5 | 3 | 48 | 0 | 1 | 1 | 1 | 0 | L.McConkeyx2, O.Gadsdenx2, C.Kolarx1 |
| 8 | LAC@LAR | Kam Curl | S | 3 | 3 | 47 | 0 | 1 | 0 | 0 | 0 | C.Kolarx1, O.Gadsdenx1, K.Mitchellx1 |
| 8 | LAC@LAR | Josh Wallace | CB | 4 | 4 | 32 | 0 | 0 | 0 | 0 | 0 | T.Harrisx2, K.Mitchellx1, O.Gadsdenx1 |
| 8 | LAC@LAR | Omar Speights | LB | 4 | 3 | 23 | 0 | 1 | 1 | 0 | 0 | L.McConkeyx1, C.Kolarx1, Q.Johnstonx1, O.Hamptonx1 |
| 8 | LAC@LAR | Nate Landman | LB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | K.Mitchellx1, O.Gadsdenx1 |
| 8 | LAC@LAR | Trent McDuffie | CB | 5 | 4 | 10 | 0 | 0 | 0 | 1 | 0 | L.McConkeyx1, K.Vidalx1, O.Hamptonx1, Q.Johnstonx1, C.Kolarx1 |
| 8 | LAC@LAR | Kamren Kinchens | S | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | Q.Johnstonx1 |
| 8 | LAC@LAR | Jaylen McCollough | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | K.Vidalx1 |
| 8 | LAC@LAR | Emmanuel Forbes | CB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Q.Johnstonx1 |

## Who beat them each week

**Wk1 SF@LAR** (vs SF offense, 205 rec yds allowed; 15% of targets unattributed)
- Top receivers: D.Robinson (WR3+, intermediate (aDOT 8-13)) 2/3 50y 1TD; M.Evans (WR1, deep (aDOT 13+)) 6/7 49y 1TD; D.Samuel (WR2, short/YAC (aDOT <8)) 6/7 48y 1TD; C.McCaffrey (RB, short/YAC (aDOT <8)) 5/8 20y
- 20+ catches: D.Robinson(WR3+) 39y deep_middle TD - no tackler named [unattributed]
- 15+ runs: C.McCaffrey(RB) 16y rush left guard; B.Purdy(QB) 18y rush left end

**Wk2 NYG@LAR** (vs NYG offense, 131 rec yds allowed; 25% of targets unattributed)
- Top receivers: D.Mooney (WR3+, deep (aDOT 13+)) 2/3 48y; I.Likely (TE1, short/YAC (aDOT <8)) 5/10 33y; M.Fields (WR2, deep (aDOT 13+)) 2/6 30y; C.Skattebo (RB, short/YAC (aDOT <8)) 4/4 19y
- 20+ catches: D.Mooney(WR3+) 33y deep_left - K.Curl [tackler]

**Wk3 LAR@DEN** (vs DEN offense, 186 rec yds allowed; 39% of targets unattributed)
- Top receivers: C.Sutton (WR2, intermediate (aDOT 8-13)) 3/7 46y; P.Bryant (WR3+, short/YAC (aDOT <8)) 2/3 44y 1TD; R.Harvey (RB, short/YAC (aDOT <8)) 6/7 41y; T.Franklin (WR3+, deep (aDOT 13+)) 1/1 21y
- 20+ catches: C.Sutton(WR2) 27y deep_left - no tackler named [unattributed]; P.Bryant(WR3+) 39y short_right - K.Curl [tackler]; T.Franklin(WR3+) 21y short_right - T.McDuffie [tackler]

**Wk4 LAR@PHI** (vs PHI offense, 93 rec yds allowed; 48% of targets unattributed)
- Top receivers: D.Cooper (WR3+, intermediate (aDOT 8-13)) 3/7 33y 2TD; M.Lemon (WR1, short/YAC (aDOT <8)) 3/6 27y; D.Wicks (WR3+, deep (aDOT 13+)) 3/5 18y; Z.Ertz (TE2+, short/YAC (aDOT <8)) 2/4 13y
- 15+ runs: T.Bigsby(RB) 19y rush left guard

**Wk5 BUF@LAR** (vs BUF offense, 210 rec yds allowed; 32% of targets unattributed)
- Top receivers: K.Shakir (WR1, short/YAC (aDOT <8)) 3/3 80y; T.Johnson (RB, short/YAC (aDOT <8)) 4/4 72y; R.Davis (RB, short/YAC (aDOT <8)) 1/1 31y; D.Kincaid (TE1, intermediate (aDOT 8-13)) 1/3 7y
- 20+ catches: T.Johnson(RB) 40y short_right - B.Young [tackler]; T.Johnson(RB) 26y short_left - K.Curl [tackler]; R.Davis(RB) 31y short_left - Q.Lake [tackler]; K.Shakir(WR1) 57y short_middle - K.Kinchens [tackler]
- 15+ runs: J.Cook(RB) 15y rush middle; J.Cook(RB) 17y rush right tackle; J.Cook(RB) 18y rush middle; J.Allen(QB) 22y rush middle; J.Allen(QB) 15y rush right guard; J.Allen(QB) 21y rush right guard; J.Allen(QB) 19y rush middle

**Wk6 ARI@LAR** (vs ARI offense, 218 rec yds allowed; 21% of targets unattributed)
- Top receivers: T.McBride (TE1, short/YAC (aDOT <8)) 7/9 53y; K.Bourne (WR2, short/YAC (aDOT <8)) 5/8 47y; Mi.Wilson (WR1, intermediate (aDOT 8-13)) 4/7 32y; J.Brooks (WR3+, deep (aDOT 13+)) 2/3 30y
- 20+ catches: T.McBride(TE1) 26y short_middle - K.Curl [tackler]; J.Brooks(WR3+) 21y deep_middle - J.Wallace [tackler]
- 15+ runs: Z.Knight(RB) 31y rush left end

**Wk7 LAR@LV** (vs LV offense, 308 rec yds allowed; 28% of targets unattributed)
- Top receivers: T.Tucker (WR1, deep (aDOT 13+)) 5/12 103y 1TD; B.Bowers (TE1, intermediate (aDOT 8-13)) 6/9 73y; A.Jeanty (RB, short/YAC (aDOT <8)) 8/8 61y 1TD; M.Mayer (TE2+, short/YAC (aDOT <8)) 3/3 32y
- 20+ catches: A.Jeanty(RB) 22y deep_right - no tackler named [unattributed]; T.Tucker(WR1) 41y short_right - J.Wallace [tackler]; T.Tucker(WR1) 37y deep_left TD - no tackler named [unattributed]
- 15+ runs: M.Washington(RB) 21y rush left end

**Wk8 LAC@LAR** (vs LAC offense, 257 rec yds allowed; 7% of targets unattributed)
- Top receivers: L.McConkey (WR3+, intermediate (aDOT 8-13)) 4/6 86y; O.Gadsden (TE1, short/YAC (aDOT <8)) 5/5 52y; Q.Johnston (WR2, deep (aDOT 13+)) 4/4 37y; T.Harris (WR1, intermediate (aDOT 8-13)) 3/3 31y
- 20+ catches: L.McConkey(WR3+) 30y short_left - Q.Lake [tackler]; C.Kolar(TE2+) 20y short_right - K.Curl [tackler]; Q.Johnston(WR2) 21y deep_middle - O.Speights [tackler]; L.McConkey(WR3+) 54y deep_right - J.Watson [tackler]

## Seed notes from defenders/LAR_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 3:55 Ladd McConkey (WR) rec 30 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q2 12:32 Charlie Kolar (TE) rec 20 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 8:26 Quentin Johnston (WR) rec 21 — defender unknown [unknown; no public source]; alignment: middle (this-play pass_location proxy)
- Q2 0:04 Ladd McConkey (WR) rec 54 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)

