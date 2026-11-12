# ARI DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 ARI@LAC, wk2 SEA@ARI, wk3 ARI@SF, wk4 ARI@NYG, wk5 DET@ARI, wk6 ARI@LAR, wk7 DEN@ARI, wk8 ARI@DAL). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 9.1% / Zone 70.9% | MOF closed 21.9% / MOF open 56.7% | Blitz 25.4% | Light box 28.8% / Heavy box 29.3% | Sub package 43.0% | Sharp YPT allowed WR 9.7, TE 8.2, RB 6.7, Outside 11.3, Slot 9.9

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR1: 9.94 YPT on 66 tgts (league 8.16, +1.78), 10 catches of 20+
- depth/direction deep_right: 14.14 YPT on 22 tgts (league 11.85, +2.29), 8 catches of 20+
- depth/direction short_left: 8.29 YPT on 68 tgts (league 6.08, +2.21), 5 catches of 20+
- receiver archetype deep (aDOT 13+): 10.62 YPT on 34 tgts (league 8.94, +1.68), 6 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 37 | 25 | 240 | 2 | 2 | 6.49 | 4.60 | 30 | 5.61 | 0.88 |
| TE1 | 34 | 26 | 300 | 3 | 4 | 8.82 | 4.20 | 37.50 | 7.39 | 1.43 |
| TE2+ | 23 | 18 | 149 | 2 | 0 | 6.48 | 2.90 | 18.60 | 6.71 | -0.23 |
| WR1 | 66 | 44 | 656 | 6 | 10 | 9.94 | 8.20 | 82 | 8.16 | 1.78 |
| WR2 | 32 | 17 | 283 | 3 | 5 | 8.84 | 4 | 35.40 | 8.20 | 0.64 |
| WR3+ | 31 | 17 | 273 | 2 | 4 | 8.81 | 3.90 | 34.10 | 7.67 | 1.14 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 22 | 17 | 180 | 2 | 2 | 8.18 | 5.61 | 2.57 |
| TE1 | 12 | 10 | 112 | 1 | 1 | 9.33 | 7.39 | 1.94 |
| TE2+ | 13 | 10 | 73 | 1 | 0 | 5.62 | 6.71 | -1.09 |
| WR1 | 36 | 23 | 255 | 0 | 4 | 7.08 | 8.16 | -1.08 |
| WR2 | 17 | 10 | 179 | 2 | 3 | 10.53 | 8.20 | 2.33 |
| WR3+ | 14 | 8 | 111 | 1 | 1 | 7.93 | 7.67 | 0.26 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 42 | 35 | 241 | 3 | 2 | 5.74 | 4.58 | 1.16 |
| short_1-9 | 90 | 67 | 601 | 6 | 2 | 6.68 | 6.23 | 0.45 |
| inter_10-19 | 60 | 34 | 672 | 5 | 10 | 11.20 | 10.17 | 1.03 |
| deep_20+ | 30 | 11 | 387 | 4 | 11 | 12.90 | 12.32 | 0.58 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 16 | 7 | 200 | 0 | 5 | 12.50 | 11.28 | 1.22 |
| deep_middle | 8 | 5 | 103 | 1 | 3 | 12.88 | 14.90 | -2.02 |
| deep_right | 22 | 8 | 311 | 4 | 8 | 14.14 | 11.85 | 2.29 |
| short_left | 68 | 48 | 564 | 3 | 5 | 8.29 | 6.08 | 2.21 |
| short_middle | 45 | 30 | 318 | 5 | 3 | 7.07 | 7.43 | -0.36 |
| short_right | 63 | 49 | 405 | 5 | 1 | 6.43 | 5.95 | 0.48 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 34 | 17 | 361 | 5 | 6 | 10.62 | 8.94 | 1.68 |
| intermediate (aDOT 8-13) | 83 | 51 | 703 | 6 | 11 | 8.47 | 7.96 | 0.51 |
| short/YAC (aDOT <8) | 106 | 79 | 837 | 7 | 8 | 7.90 | 6.47 | 1.43 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 4, 'WR': 19} (25 total, 3.1/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 3, 'deep_right': 8, 'short_left': 5, 'short_middle': 3, 'short_right': 1}
- Rush 15+ by position: {'QB': 2, 'RB': 7} (9 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 18 | 161 | 2 | 8.94 | 20.10 |
| RB | 201 | 797 | 7 | 3.97 | 99.60 |
| TE | 2 | 1 | 0 | 0.50 | 0.10 |
| WR | 5 | 24 | 0 | 4.80 | 3 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Max Melton | CB | 7 | 63.60 | 20 | 2.90 | 16 | 190 | 27.10 | 9.50 | 0 | 4 | 4 | 0 | 0 |
| Denzel Burke | CB | 8 | 86 | 20 | 2.50 | 13 | 140 | 17.50 | 7 | 0 | 1 | 6 | 1 | 0 |
| Garrett Williams | CB | 3 | 44.70 | 9 | 3 | 8 | 98 | 32.70 | 10.89 | 0 | 2 | 1 | 0 | 0 |
| Will Johnson | CB | 2 | 89.50 | 5 | 2.50 | 4 | 55 | 27.50 | 11 | 0 | 0 | 1 | 0 | 0 |
| Kalen King | CB | 2 | 32.60 | 4 | 2 | 3 | 53 | 26.50 | 13.25 | 0 | 1 | 1 | 0 | 0 |
| Kei'Trel Clark | CB | 5 | 41.10 | 8 | 1.60 | 5 | 46 | 9.20 | 5.75 | 0 | 0 | 3 | 0 | 0 |
| Mack Wilson | LB | 7 | 98.60 | 15 | 2.10 | 14 | 138 | 19.70 | 9.20 | 0 | 1 | 1 | 0 | 0 |
| Jack Gibbens | LB | 7 | 85.60 | 16 | 2.30 | 15 | 127 | 18.10 | 7.94 | 0 | 1 | 1 | 0 | 0 |
| Budda Baker | S | 7 | 99.40 | 20 | 2.90 | 16 | 227 | 32.40 | 11.35 | 0 | 3 | 3 | 1 | 0 |
| Andrew Wingard | S | 5 | 80.80 | 12 | 2.40 | 11 | 175 | 35 | 14.58 | 0 | 2 | 0 | 1 | 0 |
| Wydett Williams Jr. | S | 2 | 39 | 2 | 1 | 1 | 40 | 20 | 20 | 0 | 1 | 1 | 0 | 0 |
| Dadrion Taylor-Demerson | S | 1 | 39 | 1 | 1 | 1 | 18 | 18 | 18 | 0 | 0 | 0 | 0 | 0 |
| Kitan Crawford | S | 1 | 10 | 1 | 1 | 1 | 11 | 11 | 11 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Max Melton** (CB): WR1:7t/103y, TE1:5t/36y, WR3+:2t/33y, RB:3t/11y, WR2:3t/7y | 20+: wk3 J.Watkins(WR3+) 26 short_middle; wk4 M.Nabers(WR1) 28 deep_left; wk5 A.St. Brown(WR1) 36 deep_left; wk8 C.Lamb(WR1) 27 deep_left
- **Denzel Burke** (CB): WR2:5t/54y, WR3+:5t/43y, TE2+:3t/17y, TE1:2t/14y, WR1:5t/12y | 20+: wk8 G.Pickens(WR2) 37 short_left
- **Garrett Williams** (CB): WR1:3t/73y, WR2:1t/16y, TE1:3t/8y, TE2+:1t/1y, WR3+:1t/0y | 20+: wk6 P.Nacua(WR1) 43 short_middle; wk7 J.Waddle(WR1) 27 deep_right
- **Will Johnson** (CB): WR3+:2t/34y, TE2+:1t/15y, TE1:1t/6y, WR2:1t/0y
- **Kalen King** (CB): WR3+:2t/47y, WR1:1t/4y, RB:1t/2y | 20+: wk7 M.Mims(WR3+) 47 deep_right
- **Kei'Trel Clark** (CB): WR1:5t/35y, WR2:3t/11y
- **Mack Wilson** (LB): TE1:3t/38y, WR3+:2t/34y, TE2+:3t/26y, RB:2t/18y, WR1:4t/16y, WR2:1t/6y | 20+: wk3 J.Watkins(WR3+) 34 deep_left
- **Jack Gibbens** (LB): WR2:2t/42y, RB:8t/34y, TE2+:2t/25y, WR1:3t/15y, TE1:1t/11y | 20+: wk2 R.Shaheed(WR2) 23 short_middle
- **Budda Baker** (S): WR1:9t/84y, TE1:3t/49y, WR3+:3t/42y, TE2+:3t/28y, WR2:2t/24y | 20+: wk1 L.McConkey(WR3+) 23 deep_middle; wk4 I.Likely(TE1) 34 deep_right; wk7 C.Sutton(WR2) 20 deep_middle
- **Andrew Wingard** (S): WR1:4t/72y, TE1:3t/55y, RB:2t/25y, TE2+:2t/23y, WR3+:1t/0y | 20+: wk1 O.Gadsden(TE1) 26 short_left; wk4 M.Nabers(WR1) 39 deep_right
- **Wydett Williams Jr.** (S): WR2:1t/40y, WR1:1t/0y | 20+: wk4 M.Fields(WR2) 40 deep_left
- **Dadrion Taylor-Demerson** (S): RB:1t/18y
- **Kitan Crawford** (S): RB:1t/11y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ARI@LAC | Budda Baker | S | 3 | 3 | 53 | 0 | 1 | 0 | 0 | 0 | L.McConkeyx2, T.Harrisx1 |
| 1 | ARI@LAC | Denzel Burke | CB | 4 | 4 | 41 | 0 | 0 | 0 | 0 | 0 | L.McConkeyx1, T.Harrisx1, Q.Johnstonx1, D.Njokux1 |
| 1 | ARI@LAC | Will Johnson | CB | 3 | 3 | 39 | 0 | 0 | 0 | 0 | 0 | L.McConkeyx1, D.Njokux1, O.Gadsdenx1 |
| 1 | ARI@LAC | Andrew Wingard | S | 2 | 1 | 26 | 0 | 1 | 0 | 1 | 0 | O.Gadsdenx1, D.Davisx1 |
| 1 | ARI@LAC | Jack Gibbens | LB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | D.Njokux2 |
| 1 | ARI@LAC | Mack Wilson | LB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | D.Njokux1, L.McConkeyx1 |
| 1 | ARI@LAC | Max Melton | CB | 3 | 1 | 3 | 0 | 0 | 2 | 0 | 0 | T.Harrisx2, Q.Johnstonx1 |
| 1 | ARI@LAC | Kei'Trel Clark | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.Harrisx1 |
| 2 | SEA@ARI | Budda Baker | S | 4 | 3 | 28 | 0 | 0 | 1 | 0 | 0 | J.Smith-Njigbax2, R.Shaheedx1, E.Arroyox1 |
| 2 | SEA@ARI | Andrew Wingard | S | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax2 |
| 2 | SEA@ARI | Jack Gibbens | LB | 2 | 1 | 23 | 0 | 1 | 1 | 0 | 0 | R.Shaheedx1, E.Wilsonx1 |
| 2 | SEA@ARI | Will Johnson | CB | 2 | 1 | 16 | 0 | 0 | 1 | 0 | 0 | R.Shaheedx1, C.Kuppx1 |
| 2 | SEA@ARI | Kei'Trel Clark | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 2 | SEA@ARI | Max Melton | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 2 | SEA@ARI | Mack Wilson | LB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | A.Barnerx1 |
| 2 | SEA@ARI | Denzel Burke | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | R.Shaheedx1 |
| 3 | ARI@SF | Andrew Wingard | S | 4 | 4 | 54 | 0 | 0 | 0 | 0 | 0 | C.McCaffreyx2, G.Kittlex2 |
| 3 | ARI@SF | Mack Wilson | LB | 2 | 2 | 45 | 0 | 1 | 0 | 0 | 0 | J.Watkinsx1, C.McCaffreyx1 |
| 3 | ARI@SF | Max Melton | CB | 4 | 3 | 43 | 0 | 1 | 1 | 0 | 0 | M.Evansx1, J.Watkinsx1, G.Kittlex1, C.McCaffreyx1 |
| 3 | ARI@SF | Jack Gibbens | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | G.Kittlex1 |
| 3 | ARI@SF | Budda Baker | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | M.Evansx1 |
| 3 | ARI@SF | Denzel Burke | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | M.Evansx1, J.Cowingx1 |
| 4 | ARI@NYG | Budda Baker | S | 5 | 3 | 54 | 0 | 1 | 1 | 1 | 0 | I.Likelyx3, D.Mooneyx1, M.Nabersx1 |
| 4 | ARI@NYG | Wydett Williams Jr. | S | 1 | 1 | 40 | 0 | 1 | 0 | 0 | 0 | M.Fieldsx1 |
| 4 | ARI@NYG | Andrew Wingard | S | 1 | 1 | 39 | 0 | 1 | 0 | 0 | 0 | M.Nabersx1 |
| 4 | ARI@NYG | Max Melton | CB | 2 | 2 | 35 | 0 | 1 | 0 | 0 | 0 | I.Likelyx1, M.Nabersx1 |
| 4 | ARI@NYG | Jack Gibbens | LB | 3 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | M.Nabersx1, C.Skattebox1, P.Ricardx1 |
| 4 | ARI@NYG | Garrett Williams | CB | 4 | 3 | 8 | 0 | 0 | 1 | 0 | 0 | I.Likelyx3, B.Berriosx1 |
| 4 | ARI@NYG | Denzel Burke | CB | 2 | 1 | 6 | 0 | 0 | 0 | 1 | 0 | M.Nabersx1, M.Fieldsx1 |
| 5 | DET@ARI | Max Melton | CB | 3 | 2 | 41 | 0 | 1 | 1 | 0 | 0 | J.Gibbsx1, J.Williamsx1, A.St. Brownx1 |
| 5 | DET@ARI | Mack Wilson | LB | 3 | 3 | 37 | 0 | 0 | 0 | 0 | 0 | S.LaPortax2, A.St. Brownx1 |
| 5 | DET@ARI | Budda Baker | S | 3 | 3 | 35 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx2, B.Wrightx1 |
| 5 | DET@ARI | Dadrion Taylor-Demerson | S | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx1 |
| 5 | DET@ARI | Denzel Burke | CB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | S.LaPortax1 |
| 5 | DET@ARI | Kei'Trel Clark | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | J.Williamsx1 |
| 5 | DET@ARI | Wydett Williams Jr. | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | A.St. Brownx1 |
| 6 | ARI@LAR | Garrett Williams | CB | 4 | 4 | 63 | 0 | 1 | 0 | 0 | 0 | P.Nacuax2, C.Parkinsonx1, D.Adamsx1 |
| 6 | ARI@LAR | Mack Wilson | LB | 5 | 5 | 33 | 0 | 0 | 0 | 0 | 0 | C.Parkinsonx2, P.Nacuax2, K.Williamsx1 |
| 6 | ARI@LAR | Max Melton | CB | 5 | 5 | 31 | 0 | 0 | 0 | 0 | 0 | T.Higbeex3, D.Adamsx1, K.Mumpfieldx1 |
| 6 | ARI@LAR | Budda Baker | S | 3 | 2 | 28 | 0 | 0 | 1 | 0 | 0 | P.Nacuax2, C.Parkinsonx1 |
| 6 | ARI@LAR | Jack Gibbens | LB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | K.Williamsx2, B.Corumx1 |
| 6 | ARI@LAR | Denzel Burke | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | C.Parkinsonx1 |
| 6 | ARI@LAR | Kalen King | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | K.Mumpfieldx1 |
| 7 | DEN@ARI | Kalen King | CB | 3 | 3 | 53 | 0 | 1 | 0 | 0 | 0 | J.Waddlex1, R.Harveyx1, M.Mimsx1 |
| 7 | DEN@ARI | Garrett Williams | CB | 1 | 1 | 27 | 0 | 1 | 0 | 0 | 0 | J.Waddlex1 |
| 7 | DEN@ARI | Jack Gibbens | LB | 2 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | J.Colemanx1, C.Suttonx1 |
| 7 | DEN@ARI | Budda Baker | S | 1 | 1 | 20 | 0 | 1 | 0 | 0 | 0 | C.Suttonx1 |
| 7 | DEN@ARI | Kei'Trel Clark | CB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | J.Waddlex2, C.Suttonx1 |
| 7 | DEN@ARI | Kitan Crawford | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | J.Colemanx1 |
| 7 | DEN@ARI | Mack Wilson | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 7 | DEN@ARI | Denzel Burke | CB | 3 | 1 | 2 | 0 | 0 | 2 | 0 | 0 | E.Engramx1, T.Franklinx1, J.Waddlex1 |
| 8 | ARI@DAL | Denzel Burke | CB | 6 | 4 | 67 | 0 | 1 | 2 | 0 | 0 | R.Flournoyx2, G.Pickensx2, C.Lambx1, B.Spann-Fordx1 |
| 8 | ARI@DAL | Andrew Wingard | S | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | B.Spann-Fordx2, C.Lambx1 |
| 8 | ARI@DAL | Max Melton | CB | 2 | 2 | 28 | 0 | 1 | 0 | 0 | 0 | J.Williamsx1, C.Lambx1 |
| 8 | ARI@DAL | Kei'Trel Clark | CB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | C.Lambx1, G.Pickensx1 |
| 8 | ARI@DAL | Jack Gibbens | LB | 3 | 3 | 14 | 0 | 0 | 0 | 0 | 0 | C.Lambx2, T.Goodsonx1 |
| 8 | ARI@DAL | Mack Wilson | LB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | C.Lambx1 |

## Who beat them each week

**Wk1 ARI@LAC** (vs LAC offense, 209 rec yds allowed; 19% of targets unattributed)
- Top receivers: L.McConkey (WR3+, intermediate (aDOT 8-13)) 5/7 82y 1TD; D.Njoku (TE2+, short/YAC (aDOT <8)) 5/5 58y; O.Gadsden (TE1, short/YAC (aDOT <8)) 2/2 32y; T.Harris (WR1, intermediate (aDOT 8-13)) 3/6 20y
- 20+ catches: L.McConkey(WR3+) 23y deep_middle - B.Baker [tackler]; O.Gadsden(TE1) 26y short_left - A.Wingard [tackler]

**Wk2 SEA@ARI** (vs SEA offense, 235 rec yds allowed; 27% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 9/11 155y 3TD; R.Shaheed (WR2, intermediate (aDOT 8-13)) 3/6 35y; C.Kupp (WR3+, intermediate (aDOT 8-13)) 2/2 20y; E.Arroyo (TE2+, deep (aDOT 13+)) 1/1 17y
- 20+ catches: J.Smith-Njigba(WR1) 82y deep_right TD - no tackler named [unattributed]; R.Shaheed(WR2) 23y short_middle - J.Gibbens [tackler]
- 15+ runs: J.Price(RB) 25y rush right end; E.Wilson(RB) 18y rush right tackle

**Wk3 ARI@SF** (vs SF offense, 297 rec yds allowed; 38% of targets unattributed)
- Top receivers: M.Evans (WR1, deep (aDOT 13+)) 3/6 114y 2TD; G.Kittle (TE1, short/YAC (aDOT <8)) 6/7 82y 2TD; J.Watkins (WR3+, deep (aDOT 13+)) 2/2 60y; C.McCaffrey (RB, short/YAC (aDOT <8)) 4/5 41y
- 20+ catches: M.Evans(WR1) 82y short_left TD - no tackler named [unattributed]; J.Watkins(WR3+) 26y short_middle - M.Melton [tackler]; M.Evans(WR1) 23y deep_right TD - no tackler named [unattributed]; J.Watkins(WR3+) 34y deep_left - Ma.Wilson [tackler]; G.Kittle(TE1) 20y deep_right TD - no tackler named [unattributed]
- 15+ runs: B.Purdy(QB) 35y rush left end

**Wk4 ARI@NYG** (vs NYG offense, 250 rec yds allowed; 37% of targets unattributed)
- Top receivers: M.Nabers (WR1, intermediate (aDOT 8-13)) 6/7 112y 1TD; I.Likely (TE1, short/YAC (aDOT <8)) 7/12 66y; M.Fields (WR2, deep (aDOT 13+)) 2/3 52y 1TD; T.Johnson (TE2+, intermediate (aDOT 8-13)) 1/1 11y 1TD
- 20+ catches: M.Nabers(WR1) 39y deep_right - A.Wingard [tackler]; M.Nabers(WR1) 25y deep_middle TD - no tackler named [unattributed]; M.Nabers(WR1) 28y deep_left - M.Melton [tackler]; M.Fields(WR2) 40y deep_left - W.Williams [tackler]; I.Likely(TE1) 34y deep_right - B.Baker [tackler]

**Wk5 DET@ARI** (vs DET offense, 271 rec yds allowed; 34% of targets unattributed)
- Top receivers: S.LaPorta (TE1, short/YAC (aDOT <8)) 5/5 88y 1TD; A.St. Brown (WR1, intermediate (aDOT 8-13)) 6/11 69y; J.Gibbs (RB, short/YAC (aDOT <8)) 5/6 56y; J.Williams (WR2, deep (aDOT 13+)) 2/4 47y 2TD
- 20+ catches: S.LaPorta(TE1) 38y short_right TD - no tackler named [unattributed]; J.Gibbs(RB) 23y short_left - R.Lopez [tackler]; J.Williams(WR2) 39y deep_right TD - no tackler named [unattributed]; A.St. Brown(WR1) 36y deep_left - M.Melton [tackler]
- 15+ runs: J.Gibbs(RB) 16y rush right tackle; J.Gibbs(RB) 18y rush left tackle; J.Gibbs(RB) 22y rush right end; J.Gibbs(RB) 15y rush right tackle

**Wk6 ARI@LAR** (vs LAR offense, 222 rec yds allowed; 22% of targets unattributed)
- Top receivers: P.Nacua (WR1, short/YAC (aDOT <8)) 6/7 80y; D.Adams (WR2, deep (aDOT 13+)) 3/4 39y; C.Parkinson (TE2+, short/YAC (aDOT <8)) 5/6 31y 1TD; T.Higbee (TE1, short/YAC (aDOT <8)) 4/4 22y
- 20+ catches: P.Nacua(WR1) 43y short_middle - G.Williams [tackler]

**Wk7 DEN@ARI** (vs DEN offense, 222 rec yds allowed; 28% of targets unattributed)
- Top receivers: R.Harvey (RB, short/YAC (aDOT <8)) 2/2 54y 1TD; M.Mims (WR3+, short/YAC (aDOT <8)) 2/2 53y; J.Waddle (WR1, intermediate (aDOT 8-13)) 4/7 48y; C.Sutton (WR2, intermediate (aDOT 8-13)) 3/5 45y
- 20+ catches: C.Sutton(WR2) 20y deep_middle - B.Baker [tackler]; R.Harvey(RB) 52y short_left TD - no tackler named [unattributed]; M.Mims(WR3+) 47y deep_right - K.King [tackler]; J.Waddle(WR1) 27y deep_right - G.Williams [tackler]
- 15+ runs: B.Nix(QB) 62y rush middle; J.Coleman(RB) 15y rush middle

**Wk8 ARI@DAL** (vs DAL offense, 195 rec yds allowed; 18% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 7/11 58y; G.Pickens (WR2, intermediate (aDOT 8-13)) 2/4 48y; R.Flournoy (WR3+, short/YAC (aDOT <8)) 3/4 38y 1TD; B.Spann-Ford (TE2+, short/YAC (aDOT <8)) 4/5 31y
- 20+ catches: C.Lamb(WR1) 27y deep_left - M.Melton [tackler]; G.Pickens(WR2) 37y short_left - D.Burke [tackler]

## Seed notes from defenders/ARI_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 10:03 CeeDee Lamb (WR) rec 27 — Denzel Burke [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Garrett Williams)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L28/S38/R34)
- Q3 0:51 George Pickens (WR) rec 37 — Max Melton [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Denzel Burke)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L57/S10/R32)
- Denzel Burke ← CeeDee Lamb: 11 tgt, 7 rec, 58 yds — limited his man
- Max Melton ← George Pickens: 4 tgt, 2 rec, 48 yds
- Garrett Williams ← Ryan Flournoy: 4 tgt, 3 rec, 38 yds

