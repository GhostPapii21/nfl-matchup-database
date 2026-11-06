# CLE DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 CLE@JAX, wk2 CLE@TB, wk3 CAR@CLE, wk4 PIT@CLE, wk5 CLE@NYJ, wk6 BAL@CLE, wk7 CLE@TEN, wk8 CLE@PIT). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 42.4% / Zone 54.0% | MOF closed 72.6% / MOF open 24.4% | Blitz 25.6% | Light box 37.9% / Heavy box 25.9% | Sub package 94.0% | Sharp YPT allowed WR 8.0, TE 6.1, RB 4.0, Outside 7.6, Slot 9.8

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE2+: 9.3 YPT on 30 tgts (league 6.71, +2.59), 4 catches of 20+

Holds (-1.5 YPT or better): RB: 3.59 YPT on 39 tgts (league 5.61, -2.02); TE1: 5.74 YPT on 34 tgts (league 7.39, -1.65); WR2: 6.61 YPT on 23 tgts (league 8.2, -1.59)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 39 | 28 | 140 | 0 | 2 | 3.59 | 4.90 | 17.50 | 5.61 | -2.02 |
| TE1 | 34 | 23 | 195 | 2 | 1 | 5.74 | 4.20 | 24.40 | 7.39 | -1.65 |
| TE2+ | 30 | 21 | 279 | 2 | 4 | 9.30 | 3.80 | 34.90 | 6.71 | 2.59 |
| WR1 | 60 | 34 | 474 | 3 | 8 | 7.90 | 7.50 | 59.20 | 8.16 | -0.26 |
| WR2 | 23 | 18 | 152 | 1 | 2 | 6.61 | 2.90 | 19 | 8.20 | -1.59 |
| WR3+ | 62 | 32 | 477 | 3 | 6 | 7.69 | 7.80 | 59.60 | 7.67 | 0.02 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 17 | 11 | 53 | 0 | 0 | 3.12 | 5.61 | -2.49 |
| TE1 | 12 | 8 | 66 | 0 | 1 | 5.50 | 7.39 | -1.89 |
| TE2+ | 16 | 11 | 166 | 1 | 3 | 10.38 | 6.71 | 3.67 |
| WR1 | 35 | 19 | 243 | 1 | 3 | 6.94 | 8.16 | -1.22 |
| WR2 | 12 | 9 | 37 | 0 | 0 | 3.08 | 8.20 | -5.12 |
| WR3+ | 20 | 11 | 135 | 0 | 1 | 6.75 | 7.67 | -0.92 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 51 | 43 | 153 | 1 | 1 | 3 | 4.58 | -1.58 |
| short_1-9 | 104 | 72 | 676 | 6 | 2 | 6.50 | 6.23 | 0.27 |
| inter_10-19 | 51 | 29 | 507 | 1 | 8 | 9.94 | 10.17 | -0.23 |
| deep_20+ | 41 | 12 | 381 | 3 | 12 | 9.29 | 12.32 | -3.03 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 19 | 9 | 226 | 1 | 8 | 11.89 | 11.28 | 0.61 |
| deep_middle | 16 | 6 | 193 | 1 | 6 | 12.06 | 14.90 | -2.84 |
| deep_right | 20 | 5 | 127 | 1 | 3 | 6.35 | 11.85 | -5.50 |
| short_left | 73 | 47 | 419 | 2 | 2 | 5.74 | 6.08 | -0.34 |
| short_middle | 34 | 25 | 241 | 4 | 1 | 7.09 | 7.43 | -0.34 |
| short_right | 85 | 64 | 511 | 2 | 3 | 6.01 | 5.95 | 0.06 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 28 | 10 | 233 | 1 | 5 | 8.32 | 8.94 | -0.62 |
| intermediate (aDOT 8-13) | 105 | 64 | 814 | 5 | 11 | 7.75 | 7.96 | -0.21 |
| short/YAC (aDOT <8) | 115 | 82 | 670 | 5 | 7 | 5.83 | 6.47 | -0.64 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 5, 'WR': 16} (23 total, 2.9/g)
- Pass 20+ by depth/direction: {'deep_left': 8, 'deep_middle': 6, 'deep_right': 3, 'short_left': 2, 'short_middle': 1, 'short_right': 3}
- Rush 15+ by position: {'RB': 13} (13 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 17 | 76 | 0 | 4.47 | 9.50 |
| RB | 190 | 927 | 13 | 4.88 | 115.90 |
| TE | 1 | 1 | 0 | 1 | 0.10 |
| WR | 6 | 18 | 0 | 3 | 2.20 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tyson Campbell | CB | 7 | 91.90 | 17 | 2.40 | 14 | 254 | 36.30 | 14.94 | 0 | 5 | 3 | 0 | 0 |
| Myles Harden | CB | 8 | 60.50 | 24 | 3 | 18 | 206 | 25.80 | 8.58 | 0 | 2 | 5 | 1 | 0 |
| Denzel Ward | CB | 8 | 99 | 26 | 3.20 | 17 | 185 | 23.10 | 7.12 | 0 | 2 | 6 | 3 | 0 |
| Mekhi Blackmon | CB | 3 | 26.50 | 9 | 3 | 7 | 84 | 28 | 9.33 | 0 | 1 | 2 | 0 | 0 |
| Noah Igbinoghene | CB | 1 | 7.50 | 2 | 2 | 2 | 37 | 37 | 18.50 | 0 | 1 | 0 | 0 | 0 |
| Carson Schwesinger | LB | 7 | 100 | 20 | 2.90 | 19 | 232 | 33.10 | 11.60 | 0 | 3 | 1 | 0 | 0 |
| Quincy Williams | OLB | 8 | 96.40 | 20 | 2.50 | 17 | 74 | 9.20 | 3.70 | 0 | 0 | 3 | 0 | 0 |
| Ronnie Hickman Jr. | S | 6 | 98.80 | 18 | 3 | 16 | 207 | 34.50 | 11.50 | 0 | 4 | 1 | 1 | 0 |
| Grant Delpit | S | 7 | 87.50 | 20 | 2.90 | 16 | 118 | 16.90 | 5.90 | 0 | 1 | 3 | 1 | 0 |
| Emmanuel McNeil-Warren | S | 5 | 41.90 | 8 | 1.60 | 5 | 71 | 14.20 | 8.88 | 0 | 0 | 3 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Tyson Campbell** (CB): WR3+:8t/151y, WR1:6t/84y, WR2:2t/10y, TE1:1t/9y | 20+: wk2 T.Hurst(WR3+) 21 deep_left; wk2 T.Johnson(WR3+) 49 deep_middle; wk4 R.Wilson(WR3+) 49 deep_middle; wk4 D.Metcalf(WR1) 22 deep_left; wk4 D.Metcalf(WR1) 28 deep_left
- **Myles Harden** (CB): WR1:6t/98y, WR3+:6t/38y, TE1:5t/34y, WR2:4t/22y, TE2+:1t/8y, RB:2t/6y | 20+: wk4 D.Metcalf(WR1) 43 deep_right; wk6 Z.Flowers(WR1) 31 deep_left
- **Denzel Ward** (CB): WR3+:12t/74y, WR1:6t/39y, RB:1t/30y, TE1:5t/29y, WR2:2t/13y | 20+: wk3 C.Hubbard(RB) 30 short_middle; wk5 G.Wilson(WR1) 21 deep_left
- **Mekhi Blackmon** (CB): WR3+:3t/37y, TE2+:2t/24y, WR2:4t/23y | 20+: wk3 B.Tremayne(WR3+) 31 deep_left
- **Noah Igbinoghene** (CB): WR2:1t/24y, TE1:1t/13y | 20+: wk2 C.Godwin(WR2) 24 deep_right
- **Carson Schwesinger** (LB): TE2+:4t/93y, WR3+:5t/71y, WR1:4t/31y, RB:5t/19y, TE1:2t/18y | 20+: wk3 B.Tremayne(WR3+) 20 deep_middle; wk8 D.Washington(TE2+) 24 short_right; wk8 D.Washington(TE2+) 58 short_left
- **Quincy Williams** (OLB): RB:9t/26y, TE2+:5t/22y, WR2:1t/15y, TE1:4t/11y, WR1:1t/0y
- **Ronnie Hickman Jr.** (S): WR1:7t/86y, TE2+:5t/46y, WR3+:2t/37y, TE1:2t/28y, RB:2t/10y | 20+: wk1 P.Washington(WR1) 22 deep_left; wk6 J.Cuevas(TE2+) 29 short_right; wk7 E.Ayomanor(WR3+) 26 deep_middle; wk8 P.Freiermuth(TE1) 28 deep_middle
- **Grant Delpit** (S): RB:4t/40y, TE1:5t/27y, WR3+:3t/16y, TE2+:2t/15y, WR2:4t/13y, WR1:2t/7y | 20+: wk1 B.Tuten(RB) 22 short_left
- **Emmanuel McNeil-Warren** (S): TE2+:3t/48y, WR1:4t/17y, RB:1t/6y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CLE@JAX | Tyson Campbell | CB | 4 | 4 | 46 | 0 | 0 | 0 | 0 | 0 | P.Washingtonx1, Bri.Thomasx1, J.Meyersx1, B.Strangex1 |
| 1 | CLE@JAX | Denzel Ward | CB | 2 | 2 | 28 | 0 | 0 | 0 | 0 | 0 | Bri.Thomasx1, J.Cameronx1 |
| 1 | CLE@JAX | Grant Delpit | S | 2 | 1 | 22 | 0 | 1 | 1 | 0 | 0 | B.Strangex1, B.Tutenx1 |
| 1 | CLE@JAX | Ronnie Hickman Jr. | S | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | P.Washingtonx1 |
| 1 | CLE@JAX | Quincy Williams | OLB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | N.Boerkircherx1 |
| 1 | CLE@JAX | Myles Harden | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | P.Washingtonx1 |
| 2 | CLE@TB | Tyson Campbell | CB | 2 | 2 | 70 | 0 | 2 | 0 | 0 | 0 | T.Hurstx1, T.Johnsonx1 |
| 2 | CLE@TB | Noah Igbinoghene | CB | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | C.Godwinx1, C.Ottonx1 |
| 2 | CLE@TB | Myles Harden | CB | 5 | 3 | 19 | 0 | 0 | 1 | 1 | 0 | T.Hurstx2, C.Ottonx1, K.Gainwellx1, C.Godwinx1 |
| 2 | CLE@TB | Grant Delpit | S | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | B.Irvingx1, C.Godwinx1 |
| 2 | CLE@TB | Denzel Ward | CB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | C.Ottonx1, E.Egbukax1 |
| 2 | CLE@TB | Mekhi Blackmon | CB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | T.Hurstx2 |
| 2 | CLE@TB | Quincy Williams | OLB | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | B.Irvingx1, C.Ottonx1 |
| 2 | CLE@TB | Carson Schwesinger | LB | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | B.Irvingx2 |
| 3 | CAR@CLE | Mekhi Blackmon | CB | 6 | 5 | 73 | 0 | 1 | 1 | 0 | 0 | J.Cokerx3, T.Tremblex2, B.Tremaynex1 |
| 3 | CAR@CLE | Denzel Ward | CB | 4 | 3 | 56 | 0 | 1 | 1 | 0 | 0 | D.Wallerx2, C.Hubbardx1, J.Metchiex1 |
| 3 | CAR@CLE | Carson Schwesinger | LB | 2 | 2 | 36 | 0 | 1 | 0 | 0 | 0 | B.Tremaynex2 |
| 3 | CAR@CLE | Emmanuel McNeil-Warren | S | 2 | 2 | 36 | 0 | 0 | 0 | 0 | 0 | T.Tremblex1, M.Evansx1 |
| 3 | CAR@CLE | Myles Harden | CB | 4 | 3 | 25 | 0 | 0 | 1 | 0 | 0 | D.Wallerx4 |
| 3 | CAR@CLE | Grant Delpit | S | 3 | 3 | 24 | 0 | 0 | 0 | 0 | 0 | C.Hubbardx1, B.Tremaynex1, M.Evansx1 |
| 3 | CAR@CLE | Ronnie Hickman Jr. | S | 3 | 2 | 16 | 0 | 0 | 0 | 1 | 0 | T.McMillanx1, M.Evansx1, D.Wallerx1 |
| 3 | CAR@CLE | Quincy Williams | OLB | 2 | 2 | -4 | 0 | 0 | 0 | 0 | 0 | C.Hubbardx2 |
| 4 | PIT@CLE | Tyson Campbell | CB | 5 | 4 | 106 | 0 | 3 | 1 | 0 | 0 | D.Metcalfx2, M.Pittmanx1, R.Wilsonx1, B.Skowronekx1 |
| 4 | PIT@CLE | Myles Harden | CB | 2 | 2 | 56 | 0 | 1 | 0 | 0 | 0 | D.Metcalfx1, R.Wilsonx1 |
| 4 | PIT@CLE | Grant Delpit | S | 5 | 4 | 34 | 0 | 0 | 0 | 1 | 0 | P.Freiermuthx2, D.Metcalfx1, J.Warrenx1, R.Wilsonx1 |
| 4 | PIT@CLE | Denzel Ward | CB | 4 | 3 | 21 | 0 | 0 | 0 | 1 | 0 | M.Pittmanx3, G.Bernardx1 |
| 4 | PIT@CLE | Ronnie Hickman Jr. | S | 4 | 3 | 21 | 0 | 0 | 1 | 0 | 0 | D.Washingtonx3, D.Metcalfx1 |
| 4 | PIT@CLE | Quincy Williams | OLB | 2 | 1 | 11 | 0 | 0 | 1 | 0 | 0 | J.Warrenx2 |
| 4 | PIT@CLE | Carson Schwesinger | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Warrenx1 |
| 4 | PIT@CLE | Mekhi Blackmon | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | G.Bernardx1 |
| 4 | PIT@CLE | Emmanuel McNeil-Warren | S | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | D.Metcalfx2 |
| 5 | CLE@NYJ | Carson Schwesinger | LB | 5 | 4 | 45 | 0 | 0 | 1 | 0 | 0 | G.Wilsonx2, I.Davisx1, T.Patrickx1, J.Woodsx1 |
| 5 | CLE@NYJ | Denzel Ward | CB | 3 | 3 | 43 | 0 | 1 | 0 | 0 | 0 | G.Wilsonx2, T.Patrickx1 |
| 5 | CLE@NYJ | Myles Harden | CB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | M.Taylorx1, I.Williamsx1 |
| 5 | CLE@NYJ | Quincy Williams | OLB | 4 | 3 | 11 | 0 | 0 | 1 | 0 | 0 | M.Taylorx1, B.Allenx1, K.Sadiqx1, G.Wilsonx1 |
| 5 | CLE@NYJ | Tyson Campbell | CB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx1 |
| 5 | CLE@NYJ | Grant Delpit | S | 3 | 2 | 8 | 0 | 0 | 1 | 0 | 0 | K.Sadiqx1, M.Taylorx1, G.Wilsonx1 |
| 6 | BAL@CLE | Ronnie Hickman Jr. | S | 4 | 4 | 49 | 0 | 1 | 0 | 0 | 0 | Z.Flowersx1, J.Cuevasx1, J.Hillx1, J.Lanex1 |
| 6 | BAL@CLE | Carson Schwesinger | LB | 5 | 5 | 41 | 0 | 0 | 0 | 0 | 0 | J.Lanex2, Z.Flowersx2, J.Cuevasx1 |
| 6 | BAL@CLE | Myles Harden | CB | 4 | 2 | 35 | 0 | 1 | 2 | 0 | 0 | Z.Flowersx2, J.Hillx1, D.Walkerx1 |
| 6 | BAL@CLE | Emmanuel McNeil-Warren | S | 2 | 1 | 17 | 0 | 0 | 1 | 0 | 0 | Z.Flowersx2 |
| 6 | BAL@CLE | Denzel Ward | CB | 3 | 1 | 8 | 0 | 0 | 2 | 0 | 0 | J.Lanex2, M.Andrewsx1 |
| 6 | BAL@CLE | Quincy Williams | OLB | 3 | 3 | 8 | 0 | 0 | 0 | 0 | 0 | D.Henryx1, M.Andrewsx1, J.Cuevasx1 |
| 6 | BAL@CLE | Tyson Campbell | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Walkerx1 |
| 7 | CLE@TEN | Ronnie Hickman Jr. | S | 5 | 5 | 71 | 0 | 1 | 0 | 0 | 0 | C.Tatex3, M.Carterx1, E.Ayomanorx1 |
| 7 | CLE@TEN | Quincy Williams | OLB | 4 | 4 | 23 | 0 | 0 | 0 | 0 | 0 | T.Pollardx2, G.Helmx1, D.Bellingerx1 |
| 7 | CLE@TEN | Myles Harden | CB | 4 | 3 | 23 | 0 | 0 | 1 | 0 | 0 | C.Tatex2, W.Robinsonx2 |
| 7 | CLE@TEN | Tyson Campbell | CB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | E.Ayomanorx1, C.Tatex1 |
| 7 | CLE@TEN | Grant Delpit | S | 4 | 3 | 16 | 0 | 0 | 1 | 0 | 0 | W.Robinsonx2, E.Ayomanorx1, G.Helmx1 |
| 7 | CLE@TEN | Denzel Ward | CB | 4 | 1 | 11 | 0 | 0 | 2 | 1 | 0 | E.Ayomanorx3, G.Helmx1 |
| 7 | CLE@TEN | Carson Schwesinger | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | G.Helmx1 |
| 7 | CLE@TEN | Emmanuel McNeil-Warren | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | T.Pollardx1 |
| 8 | CLE@PIT | Carson Schwesinger | LB | 4 | 4 | 89 | 0 | 2 | 0 | 0 | 0 | D.Washingtonx2, P.Freiermuthx1, J.Warrenx1 |
| 8 | CLE@PIT | Ronnie Hickman Jr. | S | 1 | 1 | 28 | 0 | 1 | 0 | 0 | 0 | P.Freiermuthx1 |
| 8 | CLE@PIT | Myles Harden | CB | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | G.Bernardx1, B.Johnsonx1 |
| 8 | CLE@PIT | Quincy Williams | OLB | 2 | 1 | 15 | 0 | 0 | 1 | 0 | 0 | D.Washingtonx1, G.Bernardx1 |
| 8 | CLE@PIT | Emmanuel McNeil-Warren | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | D.Washingtonx1 |
| 8 | CLE@PIT | Denzel Ward | CB | 4 | 2 | 11 | 0 | 0 | 1 | 1 | 0 | D.Metcalfx3, G.Bernardx1 |
| 8 | CLE@PIT | Tyson Campbell | CB | 2 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | D.Metcalfx1, G.Bernardx1 |
| 8 | CLE@PIT | Grant Delpit | S | 1 | 1 | -3 | 0 | 0 | 0 | 0 | 0 | G.Bernardx1 |

## Who beat them each week

**Wk1 CLE@JAX** (vs JAX offense, 245 rec yds allowed; 38% of targets unattributed)
- Top receivers: P.Washington (WR1, intermediate (aDOT 8-13)) 5/6 83y 1TD; Bri.Thomas (WR3+, intermediate (aDOT 8-13)) 3/3 40y; J.Meyers (WR2, intermediate (aDOT 8-13)) 2/2 40y 1TD; B.Strange (TE1, short/YAC (aDOT <8)) 2/3 23y 1TD
- 20+ catches: P.Washington(WR1) 30y deep_right TD - no tackler named [unattributed]; P.Washington(WR1) 22y deep_left - R.Hickman [tackler]; B.Tuten(RB) 22y short_left - G.Delpit [tackler]; J.Meyers(WR2) 32y deep_left TD - no tackler named [unattributed]

**Wk2 CLE@TB** (vs TB offense, 182 rec yds allowed; 33% of targets unattributed)
- Top receivers: T.Johnson (WR3+, deep (aDOT 13+)) 1/4 49y; C.Godwin (WR2, short/YAC (aDOT <8)) 3/3 46y; C.Otton (TE1, short/YAC (aDOT <8)) 5/6 38y; T.Hurst (WR3+, deep (aDOT 13+)) 2/7 27y
- 20+ catches: T.Hurst(WR3+) 21y deep_left - T.Campbell [tackler]; C.Godwin(WR2) 24y deep_right - N.Igbinoghene [tackler]; T.Johnson(WR3+) 49y deep_middle - T.Campbell [tackler]
- 15+ runs: B.Irving(RB) 38y rush left end

**Wk3 CAR@CLE** (vs CAR offense, 291 rec yds allowed; 36% of targets unattributed)
- Top receivers: B.Tremayne (WR3+, deep (aDOT 13+)) 4/6 83y; D.Waller (TE1, intermediate (aDOT 8-13)) 5/8 51y; T.Tremble (TE2+, short/YAC (aDOT <8)) 3/4 41y; M.Evans (TE2+, short/YAC (aDOT <8)) 3/3 36y
- 20+ catches: C.Hubbard(RB) 30y short_middle - D.Ward [tackler]; B.Tremayne(WR3+) 31y deep_left - M.Blackmon [tackler]; B.Tremayne(WR3+) 20y deep_middle - C.Schwesinger [tackler]
- 15+ runs: C.Hubbard(RB) 16y rush left guard

**Wk4 PIT@CLE** (vs PIT offense, 299 rec yds allowed; 35% of targets unattributed)
- Top receivers: D.Metcalf (WR1, intermediate (aDOT 8-13)) 5/9 115y; R.Wilson (WR3+, deep (aDOT 13+)) 3/6 74y 1TD; J.Warren (RB, short/YAC (aDOT <8)) 3/7 33y; D.Washington (TE2+, short/YAC (aDOT <8)) 3/5 27y 1TD
- 20+ catches: R.Wilson(WR3+) 49y deep_middle - T.Campbell [tackler]; D.Metcalf(WR1) 43y deep_right - M.Harden [tackler]; D.Washington(TE2+) 21y deep_middle TD - no tackler named [unattributed]; D.Metcalf(WR1) 22y deep_left - T.Campbell [tackler]; D.Metcalf(WR1) 28y deep_left - T.Campbell [tackler]
- 15+ runs: J.Warren(RB) 24y rush left end

**Wk5 CLE@NYJ** (vs NYJ offense, 182 rec yds allowed; 34% of targets unattributed)
- Top receivers: G.Wilson (WR1, intermediate (aDOT 8-13)) 7/11 104y 1TD; T.Patrick (WR3+, short/YAC (aDOT <8)) 2/3 26y; M.Taylor (TE2+, intermediate (aDOT 8-13)) 3/3 24y; I.Williams (WR3+, intermediate (aDOT 8-13)) 1/2 16y
- 20+ catches: G.Wilson(WR1) 21y deep_left - D.Ward [tackler]; G.Wilson(WR1) 32y short_right TD - no tackler named [unattributed]
- 15+ runs: B.Allen(RB) 17y rush right tackle; B.Allen(RB) 18y rush right end; B.Allen(RB) 22y rush left tackle

**Wk6 BAL@CLE** (vs BAL offense, 165 rec yds allowed; 23% of targets unattributed)
- Top receivers: Z.Flowers (WR1, intermediate (aDOT 8-13)) 6/11 66y; J.Cuevas (TE2+, short/YAC (aDOT <8)) 4/5 44y 1TD; J.Lane (WR3+, intermediate (aDOT 8-13)) 4/5 40y; J.Hill (RB, short/YAC (aDOT <8)) 3/3 9y
- 20+ catches: J.Cuevas(TE2+) 29y short_right - R.Hickman [tackler]; Z.Flowers(WR1) 31y deep_left - M.Harden [tackler]
- 15+ runs: D.Henry(RB) 17y rush left end

**Wk7 CLE@TEN** (vs TEN offense, 181 rec yds allowed; 17% of targets unattributed)
- Top receivers: C.Tate (WR1, intermediate (aDOT 8-13)) 5/7 69y; E.Ayomanor (WR3+, intermediate (aDOT 8-13)) 3/7 44y; T.Pollard (RB, short/YAC (aDOT <8)) 3/3 26y; G.Helm (TE1, short/YAC (aDOT <8)) 3/4 24y
- 20+ catches: E.Ayomanor(WR3+) 26y deep_middle - R.Hickman [tackler]
- 15+ runs: T.Pollard(RB) 36y rush right tackle; T.Pollard(RB) 17y rush middle

**Wk8 CLE@PIT** (vs PIT offense, 172 rec yds allowed; 23% of targets unattributed)
- Top receivers: D.Washington (TE2+, short/YAC (aDOT <8)) 3/5 94y; P.Freiermuth (TE1, intermediate (aDOT 8-13)) 2/2 35y; G.Bernard (WR2, short/YAC (aDOT <8)) 5/5 30y; B.Johnson (WR3+, short/YAC (aDOT <8)) 1/1 9y
- 20+ catches: D.Washington(TE2+) 24y short_right - C.Schwesinger [tackler]; P.Freiermuth(TE1) 28y deep_middle - R.Hickman [tackler]; D.Washington(TE2+) 58y short_left - C.Schwesinger [tackler]
- 15+ runs: R.Dowdle(RB) 15y rush middle; J.Warren(RB) 15y rush right guard; J.Warren(RB) 51y rush middle; J.Warren(RB) 23y rush middle

## Seed notes from defenders/CLE_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 9:19 Rico Dowdle (RB) rush 15 — R.Hickman [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 6:17 Jaylen Warren (RB) rush 15 — R.Hickman; E.McNeil-Warren [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 4:17 Jaylen Warren (RB) rush 51 — C.Schwesinger [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 7:54 Darnell Washington (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 0:40 Jaylen Warren (RB) rush 23 — G.Delpit [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 0:25 Pat Freiermuth (TE) rec 28 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 10:23 Darnell Washington (TE) rec 58 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Myles Harden ← Germie Bernard: 5 tgt, 5 rec, 30 yds
- Tyson Campbell ← DK Metcalf: 5 tgt, 1 rec, 4 yds — limited his man

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 CLE@PIT: Jaylen Warren (RB-home-run zone runner) 17-143 1TD; 1/2tgt 0y 0TD | shell 42 man/54, MOFC 73 (single-high man) | PIT favored, CLE run D 4.61 YPC; 51y up the middle (Schwesinger tackled) vs CLE single-high man front; clock-kill second half. [confirmed-tackler]
- wk8 CLE@PIT: Darnell Washington (TE-inline (YAC big body)) 3/5tgt 94y 0TD | shell 42 man/54, MOFC 73 (single-high man) | Big-body inline TE YAC vs CLE man (42%) — 94y on 3 catches incl. 58y; coverage defender unknown. [unknown]
- wk8 CLE@PIT: Rico Dowdle (RB-receiving/scat) 15-56 1TD | shell 42 man/54, MOFC 73 (single-high man) | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 CLE@PIT: Pat Freiermuth (TE-move/seam) 1-1 1TD; 2/2tgt 35y 0TD | shell 42 man/54, MOFC 73 (single-high man) | Script/volume; no specific matchup attribution — see explosives table. [inferred]

