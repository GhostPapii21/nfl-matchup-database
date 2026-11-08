# MIA DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 MIA@LV, wk2 MIA@SF, wk3 KC@MIA, wk4 MIA@MIN, wk5 CIN@MIA, wk7 MIA@NYJ, wk8 NE@MIA). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 18.1% / Zone 73.4% | MOF closed 42.1% / MOF open 51.1% | Blitz 22.1% | Light box 40.8% / Heavy box 29.2% | Sub package 51.0% | Sharp YPT allowed WR 8.9, TE 9.3, RB 6.9, Outside 8.8, Slot 10.0

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE1: 11.92 YPT on 25 tgts (league 7.39, +4.53), 6 catches of 20+
- type WR1: 11.84 YPT on 19 tgts (league 8.16, +3.68), 4 catches of 20+
- type WR3+: 11.26 YPT on 31 tgts (league 7.67, +3.59), 3 catches of 20+
- depth inter_10-19: 16.44 YPT on 32 tgts (league 10.17, +6.27), 11 catches of 20+
- depth deep_20+: 20.06 YPT on 17 tgts (league 12.32, +7.74), 9 catches of 20+
- depth/direction deep_right: 22.36 YPT on 14 tgts (league 11.85, +10.51), 8 catches of 20+
- receiver archetype intermediate (aDOT 8-13): 10.34 YPT on 47 tgts (league 7.96, +2.38), 6 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 43 | 37 | 284 | 5 | 2 | 6.60 | 6.10 | 40.60 | 5.61 | 0.99 |
| TE1 | 25 | 24 | 298 | 3 | 6 | 11.92 | 3.60 | 42.60 | 7.39 | 4.53 |
| TE2+ | 31 | 24 | 185 | 3 | 2 | 5.97 | 4.40 | 26.40 | 6.71 | -0.74 |
| WR1 | 19 | 14 | 225 | 1 | 4 | 11.84 | 2.70 | 32.10 | 8.16 | 3.68 |
| WR2 | 37 | 23 | 275 | 1 | 4 | 7.43 | 5.30 | 39.30 | 8.20 | -0.77 |
| WR3+ | 31 | 28 | 349 | 3 | 3 | 11.26 | 4.40 | 49.90 | 7.67 | 3.59 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 28 | 22 | 162 | 1 | 1 | 5.79 | 5.61 | 0.18 |
| TE1 | 19 | 18 | 159 | 1 | 3 | 8.37 | 7.39 | 0.98 |
| TE2+ | 20 | 15 | 114 | 3 | 1 | 5.70 | 6.71 | -1.01 |
| WR1 | 10 | 7 | 124 | 1 | 2 | 12.40 | 8.16 | 4.24 |
| WR2 | 19 | 10 | 129 | 1 | 2 | 6.79 | 8.20 | -1.41 |
| WR3+ | 17 | 17 | 235 | 2 | 3 | 13.82 | 7.67 | 6.15 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 38 | 32 | 120 | 1 | 0 | 3.16 | 4.58 | -1.42 |
| short_1-9 | 98 | 83 | 629 | 8 | 1 | 6.42 | 6.23 | 0.19 |
| inter_10-19 | 32 | 26 | 526 | 5 | 11 | 16.44 | 10.17 | 6.27 |
| deep_20+ | 17 | 9 | 341 | 2 | 9 | 20.06 | 12.32 | 7.74 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 11 | 7 | 156 | 0 | 5 | 14.18 | 11.28 | 2.90 |
| deep_middle | 11 | 6 | 240 | 1 | 6 | 21.82 | 14.90 | 6.92 |
| deep_right | 14 | 11 | 313 | 2 | 8 | 22.36 | 11.85 | 10.51 |
| short_left | 53 | 48 | 343 | 5 | 0 | 6.47 | 6.08 | 0.39 |
| short_middle | 32 | 23 | 198 | 4 | 1 | 6.19 | 7.43 | -1.24 |
| short_right | 64 | 55 | 366 | 4 | 1 | 5.72 | 5.95 | -0.23 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 26 | 16 | 244 | 1 | 4 | 9.38 | 8.94 | 0.44 |
| intermediate (aDOT 8-13) | 47 | 35 | 486 | 7 | 6 | 10.34 | 7.96 | 2.38 |
| short/YAC (aDOT <8) | 113 | 99 | 886 | 8 | 11 | 7.84 | 6.47 | 1.37 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 8, 'WR': 11} (21 total, 3.0/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 6, 'deep_right': 8, 'short_middle': 1, 'short_right': 1}
- Rush 15+ by position: {'QB': 1, 'RB': 10} (11 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 17 | 73 | 1 | 4.29 | 10.40 |
| RB | 173 | 741 | 10 | 4.28 | 105.90 |
| WR | 4 | -3 | 0 | -0.75 | -0.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chris Johnson | CB | 7 | 97 | 24 | 3.40 | 22 | 273 | 39 | 11.38 | 0 | 4 | 2 | 0 | 0 |
| Jason Marshall Jr. | CB | 6 | 75.90 | 9 | 1.50 | 9 | 129 | 21.50 | 14.33 | 0 | 1 | 0 | 0 | 0 |
| Julius Brents | CB | 6 | 70.30 | 14 | 2.30 | 13 | 108 | 18 | 7.71 | 0 | 1 | 1 | 0 | 0 |
| Jaylin Simpson | CB | 1 | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Jacob Rodriguez | LB | 7 | 98.90 | 23 | 3.30 | 22 | 137 | 19.60 | 5.96 | 0 | 0 | 0 | 1 | 0 |
| Jordyn Brooks | OLB | 7 | 93.30 | 22 | 3.10 | 21 | 100 | 14.30 | 4.55 | 0 | 1 | 1 | 0 | 0 |
| Joshua Uche | OLB | 4 | 66.70 | 6 | 1.50 | 6 | 68 | 17 | 11.33 | 0 | 1 | 0 | 0 | 0 |
| Dante Trader Jr. | S | 6 | 81 | 14 | 2.30 | 12 | 206 | 34.30 | 14.71 | 0 | 3 | 1 | 1 | 0 |
| Michael Taaffe | S | 7 | 93.60 | 15 | 2.10 | 13 | 129 | 18.40 | 8.60 | 0 | 3 | 0 | 2 | 0 |
| Zayne Anderson | S | 4 | 28.20 | 7 | 1.80 | 6 | 108 | 27 | 15.43 | 0 | 2 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Chris Johnson** (CB): WR2:7t/102y, WR3+:6t/88y, TE2+:3t/39y, WR1:4t/22y, RB:3t/16y, TE1:1t/6y | 20+: wk3 R.Rice(WR2) 34 deep_right; wk4 J.Addison(WR2) 27 short_middle; wk7 O.Cooper(WR3+) 60 deep_middle; wk7 M.Taylor(TE2+) 20 deep_right
- **Jason Marshall Jr.** (CB): WR3+:3t/75y, WR1:2t/24y, WR2:2t/15y, TE1:1t/14y, RB:1t/1y | 20+: wk7 O.Cooper(WR3+) 52 deep_right
- **Julius Brents** (CB): WR2:4t/41y, RB:3t/25y, TE2+:3t/21y, WR3+:3t/15y, WR1:1t/6y | 20+: wk2 D.Samuel(WR2) 21 deep_middle
- **Jaylin Simpson** (CB): WR2:1t/0y
- **Jacob Rodriguez** (LB): WR3+:7t/38y, RB:4t/33y, TE1:5t/26y, WR2:4t/21y, WR1:2t/15y, TE2+:1t/4y
- **Jordyn Brooks** (OLB): RB:10t/42y, TE1:5t/38y, TE2+:5t/18y, WR2:1t/5y, WR3+:1t/-3y | 20+: wk4 T.Hockenson(TE1) 22 deep_right
- **Joshua Uche** (OLB): RB:3t/27y, WR1:1t/27y, TE2+:1t/8y, TE1:1t/6y | 20+: wk2 M.Evans(WR1) 27 deep_left
- **Dante Trader Jr.** (S): TE1:3t/83y, RB:2t/47y, WR3+:3t/40y, TE2+:2t/19y, WR2:3t/17y, WR1:1t/0y | 20+: wk3 T.Kelce(TE1) 48 deep_middle; wk7 I.Davis(RB) 41 short_right; wk8 H.Henry(TE1) 20 deep_left
- **Michael Taaffe** (S): WR1:2t/47y, TE1:3t/38y, RB:3t/19y, WR2:3t/14y, TE2+:3t/11y, WR3+:1t/0y | 20+: wk1 T.Tucker(WR1) 21 deep_left; wk2 G.Kittle(TE1) 26 deep_middle; wk8 D.Douglas(WR1) 26 deep_left
- **Zayne Anderson** (S): TE1:2t/60y, WR1:3t/36y, WR3+:1t/14y, TE2+:1t/-2y | 20+: wk2 G.Kittle(TE1) 40 deep_middle; wk4 T.Hockenson(TE1) 20 deep_right

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MIA@LV | Chris Johnson | CB | 6 | 4 | 39 | 0 | 0 | 2 | 0 | 0 | J.Nailorx2, M.Bensonx1, M.Mayerx1, C.Whitex1, T.Tuckerx1 |
| 1 | MIA@LV | Jordyn Brooks | OLB | 5 | 5 | 24 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx3, M.Mayerx2 |
| 1 | MIA@LV | Michael Taaffe | S | 2 | 1 | 21 | 0 | 1 | 0 | 1 | 0 | J.Bechx1, T.Tuckerx1 |
| 1 | MIA@LV | Julius Brents | CB | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | T.Tuckerx1, M.Mayerx1 |
| 1 | MIA@LV | Jacob Rodriguez | LB | 3 | 3 | 10 | 0 | 0 | 0 | 0 | 0 | J.Bechx2, A.Jeantyx1 |
| 1 | MIA@LV | Joshua Uche | OLB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1 |
| 1 | MIA@LV | Jason Marshall Jr. | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | J.Nailorx1 |
| 1 | MIA@LV | Dante Trader Jr. | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | J.Nailorx1 |
| 1 | MIA@LV | Zayne Anderson | S | 2 | 1 | -2 | 0 | 0 | 1 | 0 | 0 | T.Tuckerx1, M.Mayerx1 |
| 2 | MIA@SF | Zayne Anderson | S | 2 | 2 | 57 | 0 | 1 | 0 | 0 | 0 | G.Kittlex1, M.Evansx1 |
| 2 | MIA@SF | Joshua Uche | OLB | 3 | 3 | 51 | 0 | 1 | 0 | 0 | 0 | C.McCaffreyx2, M.Evansx1 |
| 2 | MIA@SF | Michael Taaffe | S | 4 | 4 | 47 | 0 | 1 | 0 | 0 | 0 | D.Samuelx2, C.McCaffreyx1, G.Kittlex1 |
| 2 | MIA@SF | Jason Marshall Jr. | CB | 2 | 2 | 29 | 0 | 0 | 0 | 0 | 0 | M.Evansx1, D.Robinsonx1 |
| 2 | MIA@SF | Julius Brents | CB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | D.Samuelx1 |
| 2 | MIA@SF | Chris Johnson | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | D.Robinsonx1 |
| 2 | MIA@SF | Jordyn Brooks | OLB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | C.McCaffreyx1 |
| 2 | MIA@SF | Jacob Rodriguez | LB | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | D.Robinsonx1, G.Kittlex1 |
| 3 | KC@MIA | Dante Trader Jr. | S | 5 | 5 | 100 | 0 | 1 | 0 | 0 | 0 | T.Kelcex1, R.Ricex1, T.Thorntonx1, N.Grayx1, J.Royalsx1 |
| 3 | KC@MIA | Chris Johnson | CB | 5 | 5 | 71 | 0 | 1 | 0 | 0 | 0 | X.Worthyx2, R.Ricex2, T.Thorntonx1 |
| 3 | KC@MIA | Michael Taaffe | S | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | B.Smithx1, R.Ricex1 |
| 3 | KC@MIA | Jason Marshall Jr. | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | R.Ricex1 |
| 3 | KC@MIA | Jordyn Brooks | OLB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | R.Ricex1 |
| 3 | KC@MIA | Jacob Rodriguez | LB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | R.Ricex1 |
| 4 | MIA@MIN | Jacob Rodriguez | LB | 9 | 9 | 64 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx3, D.Dallasx1, J.Jenningsx1, G.Bartholomewx1, A.Jonesx1, J.Addisonx1, M.Pricex1 |
| 4 | MIA@MIN | Jordyn Brooks | OLB | 6 | 5 | 39 | 0 | 1 | 1 | 0 | 0 | T.Hockensonx4, A.Jonesx2 |
| 4 | MIA@MIN | Chris Johnson | CB | 3 | 3 | 35 | 0 | 1 | 0 | 0 | 0 | J.Addisonx2, T.Hockensonx1 |
| 4 | MIA@MIN | Zayne Anderson | S | 2 | 2 | 34 | 0 | 1 | 0 | 0 | 0 | T.Hockensonx1, T.Feltonx1 |
| 4 | MIA@MIN | Julius Brents | CB | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | M.Pricex1, J.Addisonx1, A.Jonesx1 |
| 4 | MIA@MIN | Dante Trader Jr. | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1 |
| 4 | MIA@MIN | Jason Marshall Jr. | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1 |
| 4 | MIA@MIN | Michael Taaffe | S | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx2 |
| 4 | MIA@MIN | Joshua Uche | OLB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | A.Jonesx1 |
| 5 | CIN@MIA | Jacob Rodriguez | LB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | J.Chasex2, T.Higginsx1 |
| 5 | CIN@MIA | Chris Johnson | CB | 4 | 4 | 22 | 0 | 0 | 0 | 0 | 0 | C.Brownx2, T.Hudsonx1, J.Chasex1 |
| 5 | CIN@MIA | Julius Brents | CB | 4 | 3 | 21 | 0 | 0 | 1 | 0 | 0 | J.Chasex2, C.Brownx1, D.Meyersx1 |
| 5 | CIN@MIA | Jason Marshall Jr. | CB | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | T.Higginsx1, D.Meyersx1 |
| 5 | CIN@MIA | Michael Taaffe | S | 3 | 3 | 15 | 0 | 0 | 0 | 0 | 0 | E.Allx1, T.Hudsonx1, S.Perinex1 |
| 5 | CIN@MIA | Jordyn Brooks | OLB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | E.Allx1, D.Samplex1 |
| 5 | CIN@MIA | Dante Trader Jr. | S | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | J.Chasex1, T.Higginsx1 |
| 5 | CIN@MIA | Jaylin Simpson | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | J.Chasex1 |
| 7 | MIA@NYJ | Chris Johnson | CB | 3 | 3 | 87 | 0 | 2 | 0 | 0 | 0 | B.Allenx1, O.Cooperx1, M.Taylorx1 |
| 7 | MIA@NYJ | Jason Marshall Jr. | CB | 2 | 2 | 53 | 0 | 1 | 0 | 0 | 0 | O.Cooperx1, B.Allenx1 |
| 7 | MIA@NYJ | Dante Trader Jr. | S | 3 | 3 | 53 | 0 | 1 | 0 | 0 | 0 | M.Taylorx1, B.Allenx1, I.Davisx1 |
| 7 | MIA@NYJ | Zayne Anderson | S | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx1 |
| 7 | MIA@NYJ | Jacob Rodriguez | LB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | B.Allenx1, G.Wilsonx1 |
| 7 | MIA@NYJ | Julius Brents | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | M.Taylorx1 |
| 7 | MIA@NYJ | Joshua Uche | OLB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | K.Sadiqx1 |
| 7 | MIA@NYJ | Jordyn Brooks | OLB | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | J.Woodsx1, O.Cooperx1, B.Allenx1, I.Davisx1 |
| 7 | MIA@NYJ | Michael Taaffe | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | M.Taylorx1 |
| 8 | NE@MIA | Dante Trader Jr. | S | 2 | 2 | 32 | 0 | 1 | 0 | 0 | 0 | H.Henryx1, E.Chismx1 |
| 8 | NE@MIA | Michael Taaffe | S | 1 | 1 | 26 | 0 | 1 | 0 | 0 | 0 | D.Douglasx1 |
| 8 | NE@MIA | Jacob Rodriguez | LB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | E.Chismx2, H.Henryx1 |
| 8 | NE@MIA | Julius Brents | CB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | E.Raridonx1, R.Stevensonx1, E.Chismx1 |
| 8 | NE@MIA | Jordyn Brooks | OLB | 3 | 3 | 10 | 0 | 0 | 0 | 0 | 0 | R.Stevensonx2, H.Henryx1 |
| 8 | NE@MIA | Chris Johnson | CB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | D.Douglasx1, E.Chismx1 |

## Who beat them each week

**Wk1 MIA@LV** (vs LV offense, 160 rec yds allowed; 21% of targets unattributed)
- Top receivers: A.Jeanty (RB, short/YAC (aDOT <8)) 6/6 45y 2TD; M.Mayer (TE2+, short/YAC (aDOT <8)) 6/7 32y; J.Nailor (WR2, intermediate (aDOT 8-13)) 3/5 27y; T.Tucker (WR1, deep (aDOT 13+)) 2/4 27y
- 20+ catches: T.Tucker(WR1) 21y deep_left - M.Taaffe [tackler]
- 15+ runs: M.Washington(RB) 18y rush left guard; A.Jeanty(RB) 15y rush right tackle

**Wk2 MIA@SF** (vs SF offense, 287 rec yds allowed; 14% of targets unattributed)
- Top receivers: G.Kittle (TE1, short/YAC (aDOT <8)) 4/4 80y 1TD; M.Evans (WR1, deep (aDOT 13+)) 3/3 54y; C.McCaffrey (RB, short/YAC (aDOT <8)) 4/4 43y; D.Robinson (WR3+, intermediate (aDOT 8-13)) 3/3 34y
- 20+ catches: G.Kittle(TE1) 40y deep_middle - Z.Anderson [tackler]; D.Samuel(WR2) 21y deep_middle - J.Brents [tackler]; K.Juszczyk(RB) 21y deep_right - W.Gay [tackler]; M.Evans(WR1) 27y deep_left - J.Uche [tackler]; G.Kittle(TE1) 26y deep_middle - M.Taaffe [tackler]
- 15+ runs: B.Purdy(QB) 18y rush left end

**Wk3 KC@MIA** (vs KC offense, 246 rec yds allowed; 17% of targets unattributed)
- Top receivers: R.Rice (WR2, short/YAC (aDOT <8)) 7/9 88y; T.Kelce (TE1, short/YAC (aDOT <8)) 2/2 59y 1TD; N.Gray (TE2+, short/YAC (aDOT <8)) 3/3 39y; T.Thornton (WR3+, deep (aDOT 13+)) 2/2 22y
- 20+ catches: T.Kelce(TE1) 48y deep_middle - D.Trader [tackler]; N.Gray(TE2+) 24y deep_left - W.Gay [tackler]; R.Rice(WR2) 34y deep_right - C.Johnson [tackler]
- 15+ runs: K.Walker(RB) 22y rush right tackle; K.Walker(RB) 15y rush right guard

**Wk4 MIA@MIN** (vs MIN offense, 247 rec yds allowed; 15% of targets unattributed)
- Top receivers: T.Hockenson (TE1, short/YAC (aDOT <8)) 13/13 119y; J.Addison (WR2, deep (aDOT 13+)) 4/6 52y; A.Jones (RB, short/YAC (aDOT <8)) 4/8 34y; T.Felton (WR3+, intermediate (aDOT 8-13)) 1/1 14y
- 20+ catches: T.Hockenson(TE1) 20y deep_right - Z.Anderson [tackler]; J.Addison(WR2) 27y short_middle - C.Johnson [tackler]; T.Hockenson(TE1) 22y deep_right - J.Brooks [tackler]
- 15+ runs: A.Jones(RB) 15y rush right tackle; A.Jones(RB) 19y rush right end

**Wk5 CIN@MIA** (vs CIN offense, 190 rec yds allowed; 28% of targets unattributed)
- Top receivers: J.Chase (WR2, intermediate (aDOT 8-13)) 6/10 77y 1TD; E.All (TE2+, short/YAC (aDOT <8)) 3/3 25y; T.Higgins (WR1, deep (aDOT 13+)) 2/4 22y; C.Brown (RB, short/YAC (aDOT <8)) 3/4 21y
- 20+ catches: J.Chase(WR2) 45y deep_middle TD - no tackler named [unattributed]

**Wk7 MIA@NYJ** (vs NYJ offense, 287 rec yds allowed; 30% of targets unattributed)
- Top receivers: O.Cooper (WR3+, intermediate (aDOT 8-13)) 5/5 115y 1TD; M.Taylor (TE2+, intermediate (aDOT 8-13)) 5/7 62y 2TD; I.Davis (RB, short/YAC (aDOT <8)) 3/3 49y; B.Allen (RB, short/YAC (aDOT <8)) 6/7 30y
- 20+ catches: O.Cooper(WR3+) 52y deep_right - J.Marshall [tackler]; O.Cooper(WR3+) 60y deep_middle - C.Johnson [tackler]; M.Taylor(TE2+) 20y deep_right - C.Johnson [tackler]; I.Davis(RB) 41y short_right - D.Trader [tackler]
- 15+ runs: B.Allen(RB) 15y rush right tackle; B.Allen(RB) 27y rush right tackle; B.Allen(RB) 16y rush right guard

**Wk8 NE@MIA** (vs NE offense, 199 rec yds allowed; 26% of targets unattributed)
- Top receivers: D.Douglas (WR1, intermediate (aDOT 8-13)) 3/3 76y 1TD; K.Williams (WR3+, deep (aDOT 13+)) 1/1 43y 1TD; E.Chism (WR3+, short/YAC (aDOT <8)) 5/5 37y; H.Henry (TE1, short/YAC (aDOT <8)) 3/3 30y
- 20+ catches: H.Henry(TE1) 20y deep_left - D.Trader [tackler]; K.Williams(WR3+) 43y deep_right TD - no tackler named [unattributed]; D.Douglas(WR1) 26y deep_left - M.Taaffe [tackler]; D.Douglas(WR1) 48y deep_right TD - no tackler named [unattributed]
- 15+ runs: C.Kiner(RB) 20y rush middle

## Seed notes from defenders/MIA_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 10:49 Hunter Henry (TE) rec 20 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q1 3:39 Corey Kiner (RB) rush 20 — M.Taaffe; J.Marshall [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 7:17 DeMario Douglas (WR) rec 26 — Chris A. Johnson [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jason Marshall)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L9/S82/R9)
- Q4 12:39 DeMario Douglas (WR) rec 48 — Chris A. Johnson [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Jason Marshall)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L9/S82/R9)
- Chris A. Johnson ← DeMario Douglas: 3 tgt, 3 rec, 76 yds

