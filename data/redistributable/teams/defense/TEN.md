# TEN DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 NYJ@TEN, wk2 PHI@TEN, wk3 TEN@NYG, wk4 TEN@BAL, wk5 HOU@TEN, wk6 TEN@IND, wk7 CLE@TEN, wk8 TEN@CIN). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 16.5% / Zone 77.2% | MOF closed 45.6% / MOF open 51.2% | Blitz 23.0% | Light box 44.5% / Heavy box 24.3% | Sub package 67.0% | Sharp YPT allowed WR 9.2, TE 5.3, RB 7.5, Outside 8.5, Slot 11.8

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR2: 10.16 YPT on 64 tgts (league 8.2, +1.96), 9 catches of 20+
- depth/direction short_left: 7.95 YPT on 84 tgts (league 6.08, +1.87), 5 catches of 20+
- receiver archetype deep (aDOT 13+): 11.24 YPT on 41 tgts (league 8.94, +2.3), 7 catches of 20+

Holds (-1.5 YPT or better): TE2+: 3.86 YPT on 21 tgts (league 6.71, -2.85)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 40 | 33 | 280 | 0 | 3 | 7 | 5 | 35 | 5.61 | 1.39 |
| TE1 | 35 | 24 | 262 | 2 | 4 | 7.49 | 4.40 | 32.80 | 7.39 | 0.10 |
| TE2+ | 21 | 14 | 81 | 2 | 1 | 3.86 | 2.60 | 10.10 | 6.71 | -2.85 |
| WR1 | 57 | 41 | 524 | 3 | 7 | 9.19 | 7.10 | 65.50 | 8.16 | 1.03 |
| WR2 | 64 | 49 | 650 | 2 | 9 | 10.16 | 8 | 81.20 | 8.20 | 1.96 |
| WR3+ | 44 | 32 | 385 | 2 | 6 | 8.75 | 5.50 | 48.10 | 7.67 | 1.08 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 22 | 19 | 175 | 0 | 2 | 7.95 | 5.61 | 2.34 |
| TE1 | 19 | 13 | 197 | 1 | 4 | 10.37 | 7.39 | 2.98 |
| TE2+ | 12 | 7 | 37 | 2 | 0 | 3.08 | 6.71 | -3.63 |
| WR1 | 33 | 21 | 287 | 2 | 3 | 8.70 | 8.16 | 0.54 |
| WR2 | 44 | 32 | 408 | 1 | 6 | 9.27 | 8.20 | 1.07 |
| WR3+ | 24 | 19 | 196 | 1 | 2 | 8.17 | 7.67 | 0.50 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 48 | 42 | 284 | 0 | 3 | 5.92 | 4.58 | 1.34 |
| short_1-9 | 127 | 103 | 922 | 6 | 7 | 7.26 | 6.23 | 1.03 |
| inter_10-19 | 51 | 34 | 583 | 3 | 6 | 11.43 | 10.17 | 1.26 |
| deep_20+ | 34 | 14 | 393 | 2 | 14 | 11.56 | 12.32 | -0.76 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 16 | 8 | 199 | 1 | 7 | 12.44 | 11.28 | 1.16 |
| deep_middle | 6 | 3 | 89 | 1 | 3 | 14.83 | 14.90 | -0.07 |
| deep_right | 30 | 15 | 361 | 3 | 9 | 12.03 | 11.85 | 0.18 |
| short_left | 84 | 70 | 668 | 3 | 5 | 7.95 | 6.08 | 1.87 |
| short_middle | 45 | 31 | 344 | 3 | 4 | 7.64 | 7.43 | 0.21 |
| short_right | 79 | 66 | 521 | 0 | 2 | 6.59 | 5.95 | 0.64 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 41 | 30 | 461 | 2 | 7 | 11.24 | 8.94 | 2.30 |
| intermediate (aDOT 8-13) | 113 | 80 | 933 | 6 | 14 | 8.26 | 7.96 | 0.30 |
| short/YAC (aDOT <8) | 107 | 83 | 788 | 3 | 9 | 7.36 | 6.47 | 0.89 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 3, 'TE': 5, 'WR': 22} (30 total, 3.8/g)
- Pass 20+ by depth/direction: {'deep_left': 7, 'deep_middle': 3, 'deep_right': 9, 'short_left': 5, 'short_middle': 4, 'short_right': 2}
- Rush 15+ by position: {'QB': 3, 'RB': 5, 'WR': 1} (9 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 26 | 145 | 3 | 5.58 | 18.10 |
| RB | 194 | 799 | 5 | 4.12 | 99.90 |
| TE | 1 | 3 | 0 | 3 | 0.40 |
| WR | 10 | 54 | 1 | 5.40 | 6.80 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Alontae Taylor | CB | 6 | 94.50 | 18 | 3 | 18 | 244 | 40.70 | 13.56 | 0 | 4 | 0 | 0 | 0 |
| Cordale Flott | CB | 7 | 92.30 | 19 | 2.70 | 16 | 240 | 34.30 | 12.63 | 0 | 4 | 1 | 2 | 0 |
| Marcus Harris | CB | 8 | 56 | 19 | 2.40 | 18 | 172 | 21.50 | 9.05 | 0 | 2 | 0 | 1 | 0 |
| Micah Robinson | CB | 2 | 31.40 | 4 | 2 | 4 | 69 | 34.50 | 17.25 | 0 | 1 | 0 | 0 | 0 |
| Joshua Williams | CB | 3 | 100 | 10 | 3.30 | 8 | 68 | 22.70 | 6.80 | 0 | 0 | 2 | 0 | 0 |
| Anthony Hill Jr. | LB | 8 | 99.50 | 31 | 3.90 | 28 | 268 | 33.50 | 8.65 | 0 | 2 | 3 | 0 | 0 |
| Cody Barton | LB | 8 | 73.20 | 15 | 1.90 | 14 | 130 | 16.20 | 8.67 | 0 | 1 | 1 | 0 | 0 |
| Cedric Gray | OLB | 7 | 46 | 12 | 1.70 | 12 | 97 | 13.90 | 8.08 | 0 | 0 | 0 | 0 | 0 |
| Amani Hooker | S | 7 | 99.30 | 25 | 3.60 | 19 | 252 | 36 | 10.08 | 0 | 4 | 1 | 5 | 0 |
| Kevin Winston Jr. | S | 5 | 98.70 | 14 | 2.80 | 14 | 206 | 41.20 | 14.71 | 0 | 5 | 0 | 0 | 0 |
| Tony Adams | S | 2 | 39.30 | 9 | 4.50 | 8 | 85 | 42.50 | 9.44 | 0 | 1 | 1 | 0 | 0 |
| Terrell Burgess | S | 2 | 27.70 | 6 | 3 | 5 | 72 | 36 | 12 | 0 | 2 | 1 | 0 | 0 |
| Isaiah Oliver | S | 2 | 26 | 3 | 1.50 | 2 | 24 | 12 | 8 | 0 | 0 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Alontae Taylor** (CB): WR2:6t/81y, WR1:4t/64y, WR3+:3t/51y, TE2+:1t/25y, TE1:1t/14y, RB:3t/9y | 20+: wk1 O.Cooper(WR3+) 30 short_left; wk1 G.Wilson(WR1) 31 deep_right; wk4 M.Hibner(TE2+) 25 deep_left; wk4 R.Bateman(WR2) 28 short_left
- **Cordale Flott** (CB): WR2:5t/80y, WR1:5t/65y, WR3+:4t/52y, TE1:2t/27y, TE2+:2t/9y, RB:1t/7y | 20+: wk1 G.Wilson(WR1) 22 deep_left; wk4 Z.Flowers(WR1) 23 short_middle; wk7 K.Concepcion(WR2) 32 short_right; wk7 H.Fannin(TE1) 21 deep_left
- **Marcus Harris** (CB): WR2:5t/54y, WR1:7t/52y, WR3+:3t/35y, RB:3t/22y, TE1:1t/9y | 20+: wk2 D.Wicks(WR3+) 20 deep_right; wk8 T.Higgins(WR1) 32 deep_middle
- **Micah Robinson** (CB): WR3+:2t/32y, WR2:1t/19y, WR1:1t/18y | 20+: wk2 D.Wicks(WR3+) 27 deep_middle
- **Joshua Williams** (CB): WR2:3t/29y, WR1:3t/26y, WR3+:2t/13y, TE2+:2t/0y
- **Anthony Hill Jr.** (LB): WR1:5t/69y, RB:10t/59y, TE1:6t/57y, WR2:5t/57y, WR3+:3t/20y, TE2+:2t/6y | 20+: wk6 J.Downs(WR1) 23 deep_right; wk8 M.Gesicki(TE1) 28 short_middle
- **Cody Barton** (LB): WR1:3t/70y, TE1:5t/25y, WR2:3t/15y, TE2+:3t/13y, WR3+:1t/7y | 20+: wk4 Z.Flowers(WR1) 52 deep_right
- **Cedric Gray** (OLB): TE1:3t/30y, WR2:2t/27y, WR1:2t/26y, TE2+:2t/8y, RB:3t/6y
- **Amani Hooker** (S): WR2:9t/93y, RB:6t/87y, WR3+:5t/50y, WR1:3t/16y, TE1:2t/6y | 20+: wk1 A.Mitchell(WR2) 40 deep_right; wk3 C.Skattebo(RB) 30 deep_left; wk6 J.Taylor(RB) 38 short_right; wk7 K.Concepcion(WR2) 23 short_left
- **Kevin Winston Jr.** (S): WR1:5t/65y, RB:3t/46y, TE1:1t/36y, WR3+:3t/32y, WR2:1t/21y, TE2+:1t/6y | 20+: wk2 D.Cooper(WR3+) 23 short_middle; wk7 K.Concepcion(WR2) 21 short_middle; wk7 D.Sampson(RB) 22 short_left; wk7 H.Fannin(TE1) 36 short_left; wk8 T.Higgins(WR1) 21 deep_left
- **Tony Adams** (S): WR2:5t/38y, RB:1t/19y, TE1:1t/18y, TE2+:1t/5y, WR1:1t/5y | 20+: wk8 J.Chase(WR2) 23 deep_right
- **Terrell Burgess** (S): WR3+:3t/47y, WR2:3t/25y | 20+: wk5 N.Collins(WR2) 20 deep_right; wk6 D.Burks(WR3+) 36 deep_left
- **Isaiah Oliver** (S): WR2:1t/13y, RB:1t/11y, WR1:1t/0y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NYJ@TEN | Alontae Taylor | CB | 3 | 3 | 69 | 0 | 2 | 0 | 0 | 0 | O.Cooperx1, B.Hallx1, G.Wilsonx1 |
| 1 | NYJ@TEN | Cordale Flott | CB | 3 | 3 | 46 | 0 | 1 | 0 | 0 | 0 | A.Mitchellx1, G.Wilsonx1, K.Sadiqx1 |
| 1 | NYJ@TEN | Amani Hooker | S | 2 | 2 | 42 | 0 | 1 | 0 | 0 | 0 | A.Mitchellx2 |
| 1 | NYJ@TEN | Marcus Harris | CB | 4 | 4 | 24 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx3, I.Williamsx1 |
| 1 | NYJ@TEN | Kevin Winston Jr. | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx1, M.Taylorx1 |
| 1 | NYJ@TEN | Cody Barton | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | K.Sadiqx1, J.Ruckertx1 |
| 1 | NYJ@TEN | Anthony Hill Jr. | LB | 3 | 1 | 8 | 0 | 0 | 2 | 0 | 0 | M.Taylorx1, B.Allenx1, B.Hallx1 |
| 2 | PHI@TEN | Micah Robinson | CB | 3 | 3 | 51 | 0 | 1 | 0 | 0 | 0 | D.Wicksx2, D.Smithx1 |
| 2 | PHI@TEN | Kevin Winston Jr. | S | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | M.Lemonx1, D.Cooperx1 |
| 2 | PHI@TEN | Alontae Taylor | CB | 4 | 4 | 28 | 0 | 0 | 0 | 0 | 0 | D.Smithx3, W.Shipleyx1 |
| 2 | PHI@TEN | Marcus Harris | CB | 3 | 2 | 27 | 0 | 1 | 0 | 1 | 0 | W.Shipleyx1, D.Smithx1, D.Wicksx1 |
| 2 | PHI@TEN | Amani Hooker | S | 3 | 2 | 23 | 0 | 0 | 0 | 1 | 0 | D.Smithx2, D.Wicksx1 |
| 2 | PHI@TEN | Anthony Hill Jr. | LB | 3 | 3 | 23 | 0 | 0 | 0 | 0 | 0 | T.Bigsbyx1, D.Smithx1, J.Mundtx1 |
| 2 | PHI@TEN | Cody Barton | LB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | D.Goedertx1, D.Wicksx1, J.Mundtx1 |
| 2 | PHI@TEN | Cedric Gray | OLB | 2 | 2 | 9 | 0 | 0 | 0 | 0 | 0 | T.Bigsbyx1, S.Barkleyx1 |
| 3 | TEN@NYG | Amani Hooker | S | 2 | 1 | 30 | 0 | 1 | 1 | 0 | 0 | O.Beckhamx1, C.Skattebox1 |
| 3 | TEN@NYG | Cordale Flott | CB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | D.Mooneyx1, M.Nabersx1 |
| 3 | TEN@NYG | Anthony Hill Jr. | LB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | D.Mooneyx1, M.Fieldsx1, I.Likelyx1 |
| 3 | TEN@NYG | Alontae Taylor | CB | 3 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | M.Nabersx2, C.Skattebox1 |
| 3 | TEN@NYG | Marcus Harris | CB | 4 | 4 | 15 | 0 | 0 | 0 | 0 | 0 | M.Nabersx2, M.Fieldsx1, C.Skattebox1 |
| 3 | TEN@NYG | Cedric Gray | OLB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | I.Likelyx1 |
| 3 | TEN@NYG | Cody Barton | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | I.Likelyx1 |
| 4 | TEN@BAL | Cody Barton | LB | 4 | 4 | 70 | 0 | 1 | 0 | 0 | 0 | M.Andrewsx2, Z.Flowersx2 |
| 4 | TEN@BAL | Alontae Taylor | CB | 3 | 3 | 66 | 0 | 2 | 0 | 0 | 0 | M.Hibnerx1, R.Batemanx1, E.Sarrattx1 |
| 4 | TEN@BAL | Amani Hooker | S | 4 | 4 | 40 | 0 | 0 | 0 | 0 | 0 | D.Walkerx1, Z.Flowersx1, M.Andrewsx1, J.Hillx1 |
| 4 | TEN@BAL | Cordale Flott | CB | 2 | 2 | 32 | 0 | 1 | 0 | 0 | 0 | Z.Flowersx1, M.Hibnerx1 |
| 4 | TEN@BAL | Anthony Hill Jr. | LB | 4 | 4 | 31 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx2, M.Andrewsx1, D.Henryx1 |
| 4 | TEN@BAL | Marcus Harris | CB | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | R.Batemanx1 |
| 4 | TEN@BAL | Kevin Winston Jr. | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | J.Hillx1 |
| 4 | TEN@BAL | Cedric Gray | OLB | 1 | 1 | -3 | 0 | 0 | 0 | 0 | 0 | D.Henryx1 |
| 5 | HOU@TEN | Alontae Taylor | CB | 3 | 3 | 40 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1, X.Hutchinsonx1, K.Bouttex1 |
| 5 | HOU@TEN | Terrell Burgess | S | 5 | 4 | 36 | 0 | 1 | 1 | 0 | 0 | N.Collinsx3, J.Noelx2 |
| 5 | HOU@TEN | Cedric Gray | OLB | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1, F.Moreaux1, X.Hutchinsonx1 |
| 5 | HOU@TEN | Anthony Hill Jr. | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1, J.Noelx1, W.Marksx1 |
| 5 | HOU@TEN | Cody Barton | LB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | F.Moreaux1, X.Hutchinsonx1 |
| 5 | HOU@TEN | Cordale Flott | CB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | N.Collinsx1, K.Bouttex1 |
| 5 | HOU@TEN | Micah Robinson | CB | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | X.Hutchinsonx1 |
| 5 | HOU@TEN | Isaiah Oliver | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | W.Marksx1 |
| 5 | HOU@TEN | Marcus Harris | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | J.Noelx1 |
| 6 | TEN@IND | Amani Hooker | S | 6 | 5 | 73 | 0 | 1 | 0 | 1 | 0 | J.Downsx2, K.Allenx2, J.Taylorx1, L.Treadwellx1 |
| 6 | TEN@IND | Tony Adams | S | 6 | 5 | 42 | 0 | 0 | 1 | 0 | 0 | K.Allenx3, W.Malloryx1, J.Downsx1, J.Taylorx1 |
| 6 | TEN@IND | Terrell Burgess | S | 1 | 1 | 36 | 0 | 1 | 0 | 0 | 0 | D.Burksx1 |
| 6 | TEN@IND | Marcus Harris | CB | 2 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | J.Downsx1, K.Allenx1 |
| 6 | TEN@IND | Anthony Hill Jr. | LB | 2 | 1 | 23 | 0 | 1 | 1 | 0 | 0 | J.Downsx1, L.Treadwellx1 |
| 6 | TEN@IND | Joshua Williams | CB | 4 | 2 | 16 | 0 | 0 | 2 | 0 | 0 | W.Malloryx2, D.Burksx1, K.Allenx1 |
| 6 | TEN@IND | Cordale Flott | CB | 2 | 1 | 14 | 0 | 0 | 0 | 1 | 0 | W.Malloryx1, L.Treadwellx1 |
| 6 | TEN@IND | Isaiah Oliver | S | 2 | 1 | 13 | 0 | 0 | 1 | 0 | 0 | K.Allenx1, J.Downsx1 |
| 6 | TEN@IND | Cedric Gray | OLB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | P.Brownx1 |
| 6 | TEN@IND | Cody Barton | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | K.Allenx1 |
| 7 | CLE@TEN | Kevin Winston Jr. | S | 7 | 7 | 109 | 0 | 3 | 0 | 0 | 0 | J.Jeudyx2, D.Bostonx2, K.Concepcionx1, D.Sampsonx1, H.Fanninx1 |
| 7 | CLE@TEN | Cordale Flott | CB | 3 | 2 | 53 | 0 | 2 | 0 | 1 | 0 | D.Bostonx1, K.Concepcionx1, H.Fanninx1 |
| 7 | CLE@TEN | Anthony Hill Jr. | LB | 6 | 6 | 47 | 0 | 0 | 0 | 0 | 0 | H.Fanninx2, K.Concepcionx2, D.Sampsonx2 |
| 7 | CLE@TEN | Cedric Gray | OLB | 2 | 2 | 28 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1, H.Fanninx1 |
| 7 | CLE@TEN | Marcus Harris | CB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1, Q.Judkinsx1, H.Fanninx1 |
| 7 | CLE@TEN | Amani Hooker | S | 1 | 1 | 23 | 0 | 1 | 0 | 0 | 0 | K.Concepcionx1 |
| 7 | CLE@TEN | Joshua Williams | CB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | J.Jeudyx1, D.Bostonx1 |
| 7 | CLE@TEN | Cody Barton | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1 |
| 8 | TEN@CIN | Anthony Hill Jr. | LB | 7 | 7 | 94 | 0 | 1 | 0 | 0 | 0 | C.Brownx3, T.Higginsx2, M.Gesickix1, J.Chasex1 |
| 8 | TEN@CIN | Cordale Flott | CB | 5 | 4 | 50 | 0 | 0 | 1 | 0 | 0 | J.Chasex2, T.Higginsx1, C.Brownx1, D.Meyersx1 |
| 8 | TEN@CIN | Tony Adams | S | 3 | 3 | 43 | 0 | 1 | 0 | 0 | 0 | J.Chasex2, M.Gesickix1 |
| 8 | TEN@CIN | Joshua Williams | CB | 4 | 4 | 38 | 0 | 0 | 0 | 0 | 0 | J.Chasex2, T.Higginsx2 |
| 8 | TEN@CIN | Marcus Harris | CB | 1 | 1 | 32 | 0 | 1 | 0 | 0 | 0 | T.Higginsx1 |
| 8 | TEN@CIN | Kevin Winston Jr. | S | 2 | 2 | 30 | 0 | 1 | 0 | 0 | 0 | S.Perinex1, T.Higginsx1 |
| 8 | TEN@CIN | Alontae Taylor | CB | 2 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | J.Chasex2 |
| 8 | TEN@CIN | Amani Hooker | S | 7 | 4 | 21 | 0 | 0 | 0 | 3 | 0 | C.Brownx3, J.Chasex2, M.Gesickix1, D.Meyersx1 |
| 8 | TEN@CIN | Cedric Gray | OLB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | T.Higginsx1, J.Chasex1 |
| 8 | TEN@CIN | Cody Barton | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | J.Chasex1 |

## Who beat them each week

**Wk1 NYJ@TEN** (vs NYJ offense, 215 rec yds allowed; 9% of targets unattributed)
- Top receivers: G.Wilson (WR1, intermediate (aDOT 8-13)) 6/7 79y; A.Mitchell (WR2, deep (aDOT 13+)) 3/3 60y; O.Cooper (WR3+, intermediate (aDOT 8-13)) 1/1 30y; K.Sadiq (TE1, short/YAC (aDOT <8)) 3/3 21y
- 20+ catches: O.Cooper(WR3+) 30y short_left - A.Taylor [tackler]; G.Wilson(WR1) 31y deep_right - A.Taylor [tackler]; A.Mitchell(WR2) 40y deep_right - A.Hooker [tackler]; G.Wilson(WR1) 22y deep_left - C.Flott [tackler]

**Wk2 PHI@TEN** (vs PHI offense, 264 rec yds allowed; 32% of targets unattributed)
- Top receivers: D.Smith (WR2, intermediate (aDOT 8-13)) 10/13 117y 1TD; D.Wicks (WR3+, deep (aDOT 13+)) 5/6 74y; D.Cooper (WR3+, intermediate (aDOT 8-13)) 2/3 26y 1TD; M.Lemon (WR1, short/YAC (aDOT <8)) 1/1 14y
- 20+ catches: D.Wicks(WR3+) 27y deep_middle - M.Robinson [tackler]; D.Smith(WR2) 22y deep_right TD - no tackler named [unattributed]; D.Cooper(WR3+) 23y short_middle - K.Winston [tackler]; D.Wicks(WR3+) 20y deep_right - M.Harris [tackler]

**Wk3 TEN@NYG** (vs NYG offense, 118 rec yds allowed; 19% of targets unattributed)
- Top receivers: C.Skattebo (RB, short/YAC (aDOT <8)) 3/4 40y; M.Nabers (WR1, intermediate (aDOT 8-13)) 5/6 26y; D.Mooney (WR3+, deep (aDOT 13+)) 2/3 20y; M.Fields (WR2, deep (aDOT 13+)) 2/2 19y
- 20+ catches: C.Skattebo(RB) 30y deep_left - A.Hooker [tackler]
- 15+ runs: J.Winston(QB) 15y rush right end

**Wk4 TEN@BAL** (vs BAL offense, 285 rec yds allowed; 24% of targets unattributed)
- Top receivers: Z.Flowers (WR1, intermediate (aDOT 8-13)) 8/10 118y 1TD; R.Bateman (WR2, deep (aDOT 13+)) 2/2 46y; M.Hibner (TE2+, short/YAC (aDOT <8)) 2/2 34y; M.Andrews (TE1, short/YAC (aDOT <8)) 5/6 27y 1TD
- 20+ catches: Z.Flowers(WR1) 23y short_middle - C.Flott [tackler]; M.Hibner(TE2+) 25y deep_left - A.Taylor [tackler]; R.Bateman(WR2) 28y short_left - A.Taylor [tackler]; Z.Flowers(WR1) 52y deep_right - C.Barton [tackler]
- 15+ runs: L.Jackson(QB) 17y rush right guard

**Wk5 HOU@TEN** (vs HOU offense, 261 rec yds allowed; 21% of targets unattributed)
- Top receivers: X.Hutchinson (WR1, intermediate (aDOT 8-13)) 4/5 65y; N.Collins (WR2, intermediate (aDOT 8-13)) 5/7 56y; J.Noel (WR3+, intermediate (aDOT 8-13)) 5/5 41y 1TD; K.Boutte (WR3+, intermediate (aDOT 8-13)) 3/5 38y
- 20+ catches: N.Collins(WR2) 20y deep_right - T.Burgess [tackler]; K.Boutte(WR3+) 23y deep_right - no tackler named [unattributed]

**Wk6 TEN@IND** (vs IND offense, 269 rec yds allowed; 26% of targets unattributed)
- Top receivers: K.Allen (WR2, short/YAC (aDOT <8)) 8/11 82y; J.Taylor (RB, short/YAC (aDOT <8)) 2/4 57y; D.Burks (WR3+, deep (aDOT 13+)) 2/2 41y; J.Downs (WR1, intermediate (aDOT 8-13)) 4/8 40y
- 20+ catches: D.Burks(WR3+) 36y deep_left - T.Burgess [tackler]; J.Taylor(RB) 38y short_right - A.Hooker [tackler]; J.Downs(WR1) 23y deep_right - A.Hill [tackler]
- 15+ runs: S.McGowan(RB) 18y rush right end; J.Taylor(RB) 20y rush right end; D.Jones(QB) 17y rush middle

**Wk7 CLE@TEN** (vs CLE offense, 308 rec yds allowed; 26% of targets unattributed)
- Top receivers: K.Concepcion (WR2, short/YAC (aDOT <8)) 8/10 129y; H.Fannin (TE1, short/YAC (aDOT <8)) 6/9 91y; D.Sampson (RB, short/YAC (aDOT <8)) 3/3 32y; D.Boston (WR1, deep (aDOT 13+)) 3/8 27y
- 20+ catches: K.Concepcion(WR2) 23y short_left - A.Hooker [tackler]; K.Concepcion(WR2) 21y short_middle - K.Winston [tackler]; K.Concepcion(WR2) 32y short_right - C.Flott [tackler]; H.Fannin(TE1) 21y deep_left - C.Flott [tackler]; D.Sampson(RB) 22y short_left - K.Winston [tackler]; H.Fannin(TE1) 36y short_left - K.Winston [tackler]
- 15+ runs: Q.Judkins(RB) 30y rush left tackle; Q.Judkins(RB) 15y rush left guard; D.Sampson(RB) 19y rush left end; K.Concepcion(WR) 18y rush right end

**Wk8 TEN@CIN** (vs CIN offense, 462 rec yds allowed; 23% of targets unattributed)
- Top receivers: T.Higgins (WR1, deep (aDOT 13+)) 10/12 155y 2TD; J.Chase (WR2, intermediate (aDOT 8-13)) 11/16 141y 1TD; M.Gesicki (TE1, intermediate (aDOT 8-13)) 4/6 76y 1TD; C.Brown (RB, short/YAC (aDOT <8)) 8/9 46y
- 20+ catches: J.Chase(WR2) 30y deep_middle TD - no tackler named [unattributed]; T.Higgins(WR1) 32y deep_middle - M.Harris [tackler]; M.Gesicki(TE1) 28y short_middle - A.Hill [tackler]; J.Chase(WR2) 23y deep_right - T.Adams [tackler]; M.Gesicki(TE1) 25y deep_left TD - no tackler named [unattributed]; T.Higgins(WR1) 21y deep_left - K.Winston [tackler]

## Seed notes from defenders/TEN_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 13:20 Ja'Marr Chase (WR) rec 30 — Joshua Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Cordale Flott)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L40/S24/R35)
- Q2 6:51 Tee Higgins (WR) rec 32 — Cordale Flott [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L43/S14/R43)
- Q2 2:12 Mike Gesicki (TE) rec 28 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 8:02 Ja'Marr Chase (WR) rec 23 — Joshua Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Cordale Flott)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L40/S24/R35)
- Q5 8:32 Tee Higgins (WR) rec 21 — Cordale Flott [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L43/S14/R43)
- Cordale Flott ← Tee Higgins: 11 tgt, 10 rec, 155 yds
- Joshua Williams ← Ja'Marr Chase: 14 tgt, 11 rec, 141 yds
- Marcus X. Harris ← Dohnte Meyers: 3 tgt, 3 rec, 34 yds

