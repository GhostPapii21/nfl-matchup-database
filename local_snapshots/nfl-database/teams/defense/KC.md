# KC DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 DEN@KC, wk2 IND@KC, wk3 KC@MIA, wk4 KC@LV, wk6 LAC@KC, wk7 KC@SEA, wk8 KC@DEN). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 17.6% / Zone 79.1% | MOF closed 44.6% / MOF open 52.8% | Blitz 26.8% | Light box 40.8% / Heavy box 24.3% | Sub package 66.0% | Sharp YPT allowed WR 6.9, TE 6.7, RB 6.3, Outside 7.5, Slot 7.5

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type RB: 7.15 YPT on 41 tgts (league 5.61, +1.54), 2 catches of 20+

Holds (-1.5 YPT or better): WR3+: 6.17 YPT on 47 tgts (league 7.67, -1.5)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 41 | 33 | 293 | 0 | 2 | 7.15 | 5.90 | 41.90 | 5.61 | 1.54 |
| TE1 | 43 | 28 | 264 | 3 | 3 | 6.14 | 6.10 | 37.70 | 7.39 | -1.25 |
| TE2+ | 27 | 20 | 195 | 2 | 2 | 7.22 | 3.90 | 27.90 | 6.71 | 0.51 |
| WR1 | 49 | 29 | 363 | 2 | 8 | 7.41 | 7 | 51.90 | 8.16 | -0.75 |
| WR2 | 27 | 14 | 194 | 0 | 3 | 7.19 | 3.90 | 27.70 | 8.20 | -1.01 |
| WR3+ | 47 | 28 | 290 | 0 | 2 | 6.17 | 6.70 | 41.40 | 7.67 | -1.50 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 29 | 22 | 216 | 0 | 2 | 7.45 | 5.61 | 1.84 |
| TE1 | 24 | 13 | 145 | 1 | 2 | 6.04 | 7.39 | -1.35 |
| TE2+ | 23 | 18 | 185 | 2 | 2 | 8.04 | 6.71 | 1.33 |
| WR1 | 27 | 16 | 233 | 2 | 6 | 8.63 | 8.16 | 0.47 |
| WR2 | 10 | 7 | 111 | 0 | 2 | 11.10 | 8.20 | 2.90 |
| WR3+ | 29 | 17 | 158 | 0 | 1 | 5.45 | 7.67 | -2.22 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 61 | 47 | 202 | 0 | 1 | 3.31 | 4.58 | -1.27 |
| short_1-9 | 107 | 72 | 664 | 3 | 3 | 6.21 | 6.23 | -0.02 |
| inter_10-19 | 37 | 22 | 375 | 1 | 5 | 10.14 | 10.17 | -0.03 |
| deep_20+ | 27 | 11 | 358 | 3 | 11 | 13.26 | 12.32 | 0.94 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 20 | 8 | 229 | 3 | 7 | 11.45 | 11.28 | 0.17 |
| deep_middle | 11 | 5 | 164 | 0 | 4 | 14.91 | 14.90 | 0.01 |
| deep_right | 6 | 1 | 20 | 1 | 1 | 3.33 | 11.85 | -8.52 |
| short_left | 58 | 43 | 335 | 0 | 2 | 5.78 | 6.08 | -0.30 |
| short_middle | 55 | 38 | 398 | 1 | 4 | 7.24 | 7.43 | -0.19 |
| short_right | 82 | 57 | 453 | 2 | 2 | 5.52 | 5.95 | -0.43 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 26 | 12 | 185 | 0 | 3 | 7.12 | 8.94 | -1.82 |
| intermediate (aDOT 8-13) | 84 | 52 | 649 | 3 | 12 | 7.73 | 7.96 | -0.23 |
| short/YAC (aDOT <8) | 124 | 88 | 765 | 4 | 5 | 6.17 | 6.47 | -0.30 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 5, 'WR': 13} (20 total, 2.9/g)
- Pass 20+ by depth/direction: {'deep_left': 7, 'deep_middle': 4, 'deep_right': 1, 'short_left': 2, 'short_middle': 4, 'short_right': 2}
- Rush 15+ by position: {'RB': 4} (4 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 23 | 117 | 0 | 5.09 | 16.70 |
| RB | 151 | 492 | 4 | 3.26 | 70.30 |
| TE | 4 | 7 | 0 | 1.75 | 1 |
| WR | 10 | 60 | 0 | 6 | 8.60 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L'Jarius Sneed | CB | 6 | 63.70 | 27 | 4.50 | 24 | 213 | 35.50 | 7.89 | 0 | 1 | 3 | 0 | 0 |
| Nohl Williams | CB | 7 | 93 | 21 | 3 | 14 | 209 | 29.90 | 9.95 | 0 | 3 | 6 | 1 | 0 |
| Mansoor Delane | CB | 5 | 78.80 | 18 | 3.60 | 13 | 179 | 35.80 | 9.94 | 0 | 4 | 4 | 1 | 0 |
| Kristian Fulton | CB | 4 | 52.80 | 7 | 1.80 | 6 | 31 | 7.80 | 4.43 | 0 | 0 | 0 | 1 | 0 |
| Jadon Canady | CB | 1 | 6 | 2 | 2 | 2 | 7 | 7 | 3.50 | 0 | 0 | 0 | 0 | 0 |
| Nick Bolton | LB | 6 | 99.90 | 21 | 3.50 | 19 | 136 | 22.70 | 6.48 | 0 | 0 | 2 | 0 | 0 |
| Jack Cochrane | LB | 4 | 25.30 | 6 | 1.50 | 5 | 80 | 20 | 13.33 | 0 | 1 | 0 | 1 | 0 |
| Drue Tranquill | OLB | 6 | 89.60 | 10 | 1.70 | 8 | 87 | 14.50 | 8.70 | 0 | 0 | 2 | 0 | 0 |
| Alohi Gilman | S | 6 | 81.30 | 10 | 1.70 | 9 | 148 | 24.70 | 14.80 | 0 | 2 | 1 | 0 | 0 |
| Chamarri Conner | S | 4 | 93.80 | 11 | 2.80 | 10 | 146 | 36.50 | 13.27 | 0 | 4 | 1 | 0 | 0 |
| Jaden Hicks | S | 6 | 65.10 | 11 | 1.80 | 10 | 103 | 17.20 | 9.36 | 0 | 1 | 1 | 0 | 0 |
| Christian Roland-Wallace | S | 5 | 32.70 | 12 | 2.40 | 10 | 76 | 15.20 | 6.33 | 0 | 0 | 2 | 0 | 0 |
| Xavier Nwankpa | S | 1 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

### Receiver types charged to each defender / explosives charged

- **L'Jarius Sneed** (CB): WR3+:8t/95y, WR1:7t/44y, TE1:5t/34y, RB:4t/24y, TE2+:3t/16y | 20+: wk2 L.Treadwell(WR3+) 48 deep_middle
- **Nohl Williams** (CB): RB:3t/62y, WR1:5t/56y, TE1:3t/51y, WR3+:7t/29y, TE2+:1t/11y, WR2:2t/0y | 20+: wk3 G.Dulcich(TE1) 42 deep_middle; wk7 J.Smith-Njigba(WR1) 33 short_middle; wk8 J.Coleman(RB) 51 short_right
- **Mansoor Delane** (CB): WR2:5t/79y, WR3+:6t/55y, WR1:4t/29y, TE1:1t/21y, RB:2t/-5y | 20+: wk3 M.Washington(WR1) 30 short_left; wk4 B.Bowers(TE1) 21 short_right; wk4 C.White(WR3+) 27 deep_left; wk6 Q.Johnston(WR2) 57 deep_left
- **Kristian Fulton** (CB): WR3+:3t/13y, WR2:3t/10y, RB:1t/8y
- **Jadon Canady** (CB): WR2:1t/4y, WR3+:1t/3y
- **Nick Bolton** (LB): TE1:8t/39y, WR3+:2t/32y, RB:6t/30y, TE2+:3t/21y, WR1:2t/14y
- **Jack Cochrane** (LB): RB:2t/38y, TE1:2t/33y, TE2+:1t/9y, WR3+:1t/0y | 20+: wk4 A.Jeanty(RB) 28 short_left
- **Drue Tranquill** (OLB): RB:5t/37y, TE1:2t/28y, WR3+:1t/14y, WR2:1t/8y, TE2+:1t/0y
- **Alohi Gilman** (S): WR2:4t/66y, WR1:2t/34y, RB:1t/19y, TE2+:1t/17y, WR3+:1t/13y, TE1:1t/-1y | 20+: wk2 J.Downs(WR1) 20 deep_left; wk3 C.Bell(WR2) 44 short_middle
- **Chamarri Conner** (S): TE2+:5t/54y, WR1:2t/44y, WR2:1t/23y, RB:1t/15y, WR3+:1t/10y, TE1:1t/0y | 20+: wk4 T.Tucker(WR1) 23 deep_middle; wk7 J.Smith-Njigba(WR1) 21 short_middle; wk8 C.Sutton(WR2) 23 deep_left; wk8 A.Trautman(TE2+) 22 short_middle
- **Jaden Hicks** (S): WR1:4t/52y, WR3+:2t/16y, RB:1t/15y, TE1:3t/14y, WR2:1t/6y | 20+: wk8 J.Waddle(WR1) 35 deep_middle
- **Christian Roland-Wallace** (S): WR1:4t/31y, RB:2t/27y, TE2+:1t/17y, TE1:3t/6y, WR2:1t/-2y, WR3+:1t/-3y
- **Xavier Nwankpa** (S): TE2+:1t/0y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DEN@KC | L'Jarius Sneed | CB | 7 | 7 | 41 | 0 | 0 | 0 | 0 | 0 | P.Bryantx2, R.Harveyx2, A.Trautmanx1, J.Waddlex1, E.Engramx1 |
| 1 | DEN@KC | Jaden Hicks | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1, E.Engramx1 |
| 1 | DEN@KC | Alohi Gilman | S | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | P.Bryantx1 |
| 1 | DEN@KC | Drue Tranquill | OLB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | R.Harveyx1 |
| 1 | DEN@KC | Nohl Williams | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | E.Engramx1, T.Franklinx1 |
| 1 | DEN@KC | Kristian Fulton | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 1 | DEN@KC | Nick Bolton | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | E.Engramx1 |
| 1 | DEN@KC | Mansoor Delane | CB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | C.Suttonx1 |
| 2 | IND@KC | L'Jarius Sneed | CB | 7 | 6 | 92 | 0 | 1 | 1 | 0 | 0 | J.Downsx5, A.Piercex1, L.Treadwellx1 |
| 2 | IND@KC | Alohi Gilman | S | 2 | 1 | 20 | 0 | 1 | 1 | 0 | 0 | K.Allenx1, J.Downsx1 |
| 2 | IND@KC | Jaden Hicks | S | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | T.Warrenx2, J.Taylorx1 |
| 2 | IND@KC | Nick Bolton | LB | 3 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | T.Warrenx2, J.Taylorx1 |
| 2 | IND@KC | Nohl Williams | CB | 3 | 2 | 15 | 0 | 0 | 1 | 0 | 0 | L.Treadwellx1, K.Allenx1, J.Downsx1 |
| 2 | IND@KC | Drue Tranquill | OLB | 2 | 1 | 14 | 0 | 0 | 1 | 0 | 0 | A.Ogletreex1, J.Taylorx1 |
| 2 | IND@KC | Christian Roland-Wallace | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | J.Downsx1 |
| 2 | IND@KC | Kristian Fulton | CB | 3 | 2 | 8 | 0 | 0 | 0 | 1 | 0 | K.Allenx2, L.Treadwellx1 |
| 3 | KC@MIA | Alohi Gilman | S | 3 | 3 | 67 | 0 | 1 | 0 | 0 | 0 | C.Bellx2, O.Gordonx1 |
| 3 | KC@MIA | Mansoor Delane | CB | 7 | 6 | 54 | 0 | 1 | 1 | 0 | 0 | C.Bellx2, M.Washingtonx2, O.Gordonx2, R.Millerx1 |
| 3 | KC@MIA | Nohl Williams | CB | 3 | 2 | 45 | 0 | 1 | 1 | 0 | 0 | K.Colemanx2, G.Dulcichx1 |
| 3 | KC@MIA | Nick Bolton | LB | 5 | 4 | 27 | 0 | 0 | 1 | 0 | 0 | G.Dulcichx3, M.Washingtonx2 |
| 3 | KC@MIA | Jaden Hicks | S | 3 | 2 | 12 | 0 | 0 | 1 | 0 | 0 | M.Washingtonx2, K.Colemanx1 |
| 3 | KC@MIA | L'Jarius Sneed | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx1 |
| 4 | KC@LV | Mansoor Delane | CB | 6 | 5 | 65 | 0 | 2 | 1 | 0 | 0 | C.Whitex3, D.Youngx1, B.Bowersx1, T.Tuckerx1 |
| 4 | KC@LV | L'Jarius Sneed | CB | 6 | 5 | 46 | 0 | 0 | 1 | 0 | 0 | B.Bowersx3, A.Jeantyx2, M.Mayerx1 |
| 4 | KC@LV | Chamarri Conner | S | 4 | 3 | 40 | 0 | 1 | 1 | 0 | 0 | M.Mayerx2, B.Bowersx1, T.Tuckerx1 |
| 4 | KC@LV | Jack Cochrane | LB | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | A.Jeantyx1, M.Mayerx1 |
| 4 | KC@LV | Nohl Williams | CB | 4 | 3 | 31 | 0 | 0 | 1 | 0 | 0 | T.Tuckerx2, M.Mayerx1, A.Jeantyx1 |
| 4 | KC@LV | Drue Tranquill | OLB | 3 | 2 | 27 | 0 | 0 | 1 | 0 | 0 | B.Bowersx1, A.Jeantyx1, C.Heywardx1 |
| 4 | KC@LV | Nick Bolton | LB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, B.Bowersx1, M.Mayerx1 |
| 4 | KC@LV | Christian Roland-Wallace | S | 1 | 1 | 17 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1 |
| 4 | KC@LV | Alohi Gilman | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | T.Tuckerx1 |
| 4 | KC@LV | Kristian Fulton | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1 |
| 4 | KC@LV | Xavier Nwankpa | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | M.Mayerx1 |
| 6 | LAC@KC | Mansoor Delane | CB | 1 | 1 | 57 | 0 | 1 | 0 | 0 | 0 | Q.Johnstonx1 |
| 6 | LAC@KC | Nick Bolton | LB | 4 | 4 | 50 | 0 | 0 | 0 | 0 | 0 | L.McConkeyx1, K.Lambert-Smithx1, O.Gadsdenx1, K.Vidalx1 |
| 6 | LAC@KC | Christian Roland-Wallace | S | 4 | 4 | 18 | 0 | 0 | 0 | 0 | 0 | O.Gadsdenx2, K.Lambert-Smithx1, O.Hamptonx1 |
| 6 | LAC@KC | Drue Tranquill | OLB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | O.Hamptonx1, T.Weasex1 |
| 6 | LAC@KC | Jaden Hicks | S | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | K.Lambert-Smithx1 |
| 6 | LAC@KC | Chamarri Conner | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | C.Kolarx2 |
| 6 | LAC@KC | L'Jarius Sneed | CB | 4 | 3 | 11 | 0 | 0 | 1 | 0 | 0 | K.Lambert-Smithx2, T.Weasex1, C.Kolarx1 |
| 6 | LAC@KC | Nohl Williams | CB | 4 | 2 | 4 | 0 | 0 | 2 | 0 | 0 | K.Lambert-Smithx2, O.Hamptonx1, O.Gadsdenx1 |
| 6 | LAC@KC | Jack Cochrane | LB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | K.Lambert-Smithx1 |
| 7 | KC@SEA | Nohl Williams | CB | 4 | 3 | 54 | 0 | 1 | 0 | 1 | 0 | J.Smith-Njigbax2, C.Kuppx1, R.Shaheedx1 |
| 7 | KC@SEA | Chamarri Conner | S | 2 | 2 | 36 | 0 | 1 | 0 | 0 | 0 | E.Wilsonx1, J.Smith-Njigbax1 |
| 7 | KC@SEA | Jack Cochrane | LB | 2 | 2 | 33 | 0 | 0 | 0 | 0 | 0 | A.Barnerx2 |
| 7 | KC@SEA | Christian Roland-Wallace | S | 4 | 3 | 24 | 0 | 0 | 1 | 0 | 0 | J.Smith-Njigbax2, R.Shaheedx1, G.Holanix1 |
| 7 | KC@SEA | L'Jarius Sneed | CB | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1, C.Kuppx1 |
| 7 | KC@SEA | Alohi Gilman | S | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | A.Barnerx1, E.Saubertx1 |
| 7 | KC@SEA | Drue Tranquill | OLB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | A.Barnerx1 |
| 7 | KC@SEA | Jaden Hicks | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 7 | KC@SEA | Mansoor Delane | CB | 3 | 1 | 3 | 0 | 0 | 2 | 0 | 0 | T.Hortonx1, R.Shaheedx1, J.Smith-Njigbax1 |
| 8 | KC@DEN | Chamarri Conner | S | 3 | 3 | 55 | 0 | 2 | 0 | 0 | 0 | C.Suttonx1, L.Humphreyx1, A.Trautmanx1 |
| 8 | KC@DEN | Nohl Williams | CB | 1 | 1 | 51 | 0 | 1 | 0 | 0 | 0 | J.Colemanx1 |
| 8 | KC@DEN | Jaden Hicks | S | 1 | 1 | 35 | 0 | 1 | 0 | 0 | 0 | J.Waddlex1 |
| 8 | KC@DEN | Nick Bolton | LB | 5 | 5 | 22 | 0 | 0 | 0 | 0 | 0 | J.Colemanx3, N.Adkinsx1, A.Trautmanx1 |
| 8 | KC@DEN | Alohi Gilman | S | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 8 | KC@DEN | Kristian Fulton | CB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | T.Franklinx1, M.Mimsx1 |
| 8 | KC@DEN | Jack Cochrane | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | A.Prenticex1 |
| 8 | KC@DEN | Drue Tranquill | OLB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 8 | KC@DEN | Jadon Canady | CB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | M.Mimsx1, C.Suttonx1 |
| 8 | KC@DEN | Christian Roland-Wallace | S | 2 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | E.Engramx1, J.Waddlex1 |

## Who beat them each week

**Wk1 DEN@KC** (vs DEN offense, 131 rec yds allowed; 26% of targets unattributed)
- Top receivers: E.Engram (TE1, short/YAC (aDOT <8)) 4/5 43y 1TD; P.Bryant (WR3+, short/YAC (aDOT <8)) 4/6 42y; R.Harvey (RB, short/YAC (aDOT <8)) 4/4 23y; C.Sutton (WR2, intermediate (aDOT 8-13)) 2/5 11y
- 15+ runs: J.Dobbins(RB) 17y rush left end

**Wk2 IND@KC** (vs IND offense, 210 rec yds allowed; 13% of targets unattributed)
- Top receivers: J.Downs (WR1, intermediate (aDOT 8-13)) 7/9 72y; L.Treadwell (WR3+, intermediate (aDOT 8-13)) 3/3 61y; J.Taylor (RB, short/YAC (aDOT <8)) 4/4 40y; T.Warren (TE1, short/YAC (aDOT <8)) 6/7 21y 1TD
- 20+ catches: J.Downs(WR1) 20y deep_left - A.Gilman [tackler]; L.Treadwell(WR3+) 48y deep_middle - L.Sneed [tackler]
- 15+ runs: J.Taylor(RB) 24y rush right end

**Wk3 KC@MIA** (vs MIA offense, 210 rec yds allowed; 31% of targets unattributed)
- Top receivers: C.Bell (WR2, deep (aDOT 13+)) 4/7 67y; M.Washington (WR1, intermediate (aDOT 8-13)) 5/10 56y; G.Dulcich (TE1, short/YAC (aDOT <8)) 5/7 55y; R.Miller (WR3+, intermediate (aDOT 8-13)) 2/3 15y
- 20+ catches: M.Washington(WR1) 30y short_left - M.Delane [tackler]; C.Bell(WR2) 44y short_middle - A.Gilman [tackler]; G.Dulcich(TE1) 42y deep_middle - N.Williams [tackler]

**Wk4 KC@LV** (vs LV offense, 365 rec yds allowed; 28% of targets unattributed)
- Top receivers: B.Bowers (TE1, intermediate (aDOT 8-13)) 6/11 86y 1TD; M.Mayer (TE2+, short/YAC (aDOT <8)) 8/10 82y; A.Jeanty (RB, short/YAC (aDOT <8)) 6/8 68y; T.Tucker (WR1, deep (aDOT 13+)) 4/8 44y
- 20+ catches: I.Thomas(TE2+) 27y deep_left TD - no tackler named [unattributed]; A.Jeanty(RB) 28y short_left - J.Cochrane [tackler]; B.Bowers(TE1) 21y short_right - M.Delane [tackler]; C.White(WR3+) 27y deep_left - M.Delane [tackler]; B.Bowers(TE1) 20y deep_right TD - no tackler named [unattributed]; T.Tucker(WR1) 23y deep_middle - C.Conner [tackler]
- 15+ runs: A.Jeanty(RB) 19y rush middle

**Wk6 LAC@KC** (vs LAC offense, 204 rec yds allowed; 19% of targets unattributed)
- Top receivers: Q.Johnston (WR2, deep (aDOT 13+)) 1/3 57y; K.Lambert-Smith (WR3+, short/YAC (aDOT <8)) 5/9 32y; O.Hampton (RB, short/YAC (aDOT <8)) 4/4 21y; T.Wease (WR3+, intermediate (aDOT 8-13)) 2/3 21y
- 20+ catches: Q.Johnston(WR2) 57y deep_left - M.Delane [tackler]

**Wk7 KC@SEA** (vs SEA offense, 257 rec yds allowed; 15% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 9/12 150y 1TD; A.Barner (TE1, short/YAC (aDOT <8)) 4/5 42y; C.Kupp (WR3+, intermediate (aDOT 8-13)) 2/2 20y; E.Saubert (TE2+, short/YAC (aDOT <8)) 1/1 17y
- 20+ catches: J.Smith-Njigba(WR1) 33y short_middle - N.Williams [tackler]; J.Smith-Njigba(WR1) 28y deep_left TD - no tackler named [unattributed]; J.Smith-Njigba(WR1) 21y short_middle - C.Conner [tackler]; J.Smith-Njigba(WR1) 28y deep_left - no tackler named [unattributed]
- 15+ runs: E.Wilson(RB) 21y rush left tackle

**Wk8 KC@DEN** (vs DEN offense, 222 rec yds allowed; 23% of targets unattributed)
- Top receivers: J.Coleman (RB, short/YAC (aDOT <8)) 4/5 63y; C.Sutton (WR2, intermediate (aDOT 8-13)) 4/4 53y; J.Waddle (WR1, intermediate (aDOT 8-13)) 3/7 39y 1TD; A.Trautman (TE2+, short/YAC (aDOT <8)) 2/2 30y
- 20+ catches: C.Sutton(WR2) 23y deep_left - C.Conner [tackler]; J.Waddle(WR1) 35y deep_middle - J.Hicks [tackler]; A.Trautman(TE2+) 22y short_middle - C.Conner [tackler]; J.Coleman(RB) 51y short_right - N.Williams [tackler]

## Seed notes from defenders/KC_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 0:05 Courtland Sutton (WR) rec 23 — Mansoor Delane [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L39/S29/R33)
- Q2 13:04 Jaylen Waddle (WR) rec 35 — Nohl Williams [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Mansoor Delane)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L27/S38/R35)
- Q4 11:23 Adam Trautman (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 2:31 Jonah Coleman (RB) rec 51 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Mansoor Delane ← Courtland Sutton: 4 tgt, 4 rec, 53 yds
- Nohl Williams ← Jaylen Waddle: 5 tgt, 2 rec, 38 yds
- Nohl Williams ← Marvin Mims Jr.: 3 tgt, 2 rec, 10 yds — limited his man

