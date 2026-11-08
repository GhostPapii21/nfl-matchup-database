# CIN DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 TB@CIN, wk2 CIN@HOU, wk3 CIN@PIT, wk4 JAX@CIN, wk5 CIN@MIA, wk7 CIN@BAL, wk8 TEN@CIN). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 26.6% / Zone 65.3% | MOF closed 51.3% / MOF open 43.1% | Blitz 17.2% | Light box 58.6% / Heavy box 18.3% | Sub package 80.0% | Sharp YPT allowed WR 7.6, TE 9.4, RB 6.8, Outside 5.7, Slot 11.3

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE2+: 10.78 YPT on 18 tgts (league 6.71, +4.07), 2 catches of 20+
- depth behind_los: 7.56 YPT on 45 tgts (league 4.58, +2.98), 3 catches of 20+
- depth/direction short_left: 7.69 YPT on 61 tgts (league 6.08, +1.61), 3 catches of 20+
- depth/direction short_right: 8.23 YPT on 78 tgts (league 5.95, +2.28), 6 catches of 20+
- receiver archetype short/YAC (aDOT <8): 8.69 YPT on 114 tgts (league 6.47, +2.22), 12 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 33 | 27 | 209 | 0 | 2 | 6.33 | 4.70 | 29.90 | 5.61 | 0.72 |
| TE1 | 51 | 36 | 427 | 0 | 6 | 8.37 | 7.30 | 61 | 7.39 | 0.98 |
| TE2+ | 18 | 13 | 194 | 0 | 2 | 10.78 | 2.60 | 27.70 | 6.71 | 4.07 |
| WR1 | 42 | 26 | 318 | 2 | 2 | 7.57 | 6 | 45.40 | 8.16 | -0.59 |
| WR2 | 22 | 16 | 177 | 1 | 2 | 8.05 | 3.10 | 25.30 | 8.20 | -0.15 |
| WR3+ | 67 | 36 | 502 | 5 | 10 | 7.49 | 9.60 | 71.70 | 7.67 | -0.18 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 13 | 9 | 68 | 0 | 0 | 5.23 | 5.61 | -0.38 |
| TE1 | 28 | 19 | 231 | 0 | 3 | 8.25 | 7.39 | 0.86 |
| TE2+ | 11 | 7 | 91 | 0 | 0 | 8.27 | 6.71 | 1.56 |
| WR1 | 22 | 15 | 187 | 1 | 2 | 8.50 | 8.16 | 0.34 |
| WR2 | 17 | 11 | 123 | 1 | 1 | 7.24 | 8.20 | -0.96 |
| WR3+ | 34 | 21 | 266 | 3 | 6 | 7.82 | 7.67 | 0.15 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 45 | 40 | 340 | 1 | 3 | 7.56 | 4.58 | 2.98 |
| short_1-9 | 103 | 74 | 750 | 3 | 5 | 7.28 | 6.23 | 1.05 |
| inter_10-19 | 58 | 34 | 578 | 2 | 10 | 9.97 | 10.17 | -0.20 |
| deep_20+ | 24 | 6 | 159 | 2 | 6 | 6.62 | 12.32 | -5.70 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 14 | 4 | 106 | 1 | 3 | 7.57 | 11.28 | -3.71 |
| deep_middle | 11 | 6 | 125 | 0 | 4 | 11.36 | 14.90 | -3.54 |
| deep_right | 15 | 2 | 45 | 1 | 2 | 3 | 11.85 | -8.85 |
| short_left | 61 | 47 | 469 | 1 | 3 | 7.69 | 6.08 | 1.61 |
| short_middle | 51 | 32 | 440 | 2 | 6 | 8.63 | 7.43 | 1.20 |
| short_right | 78 | 63 | 642 | 3 | 6 | 8.23 | 5.95 | 2.28 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 30 | 13 | 192 | 2 | 2 | 6.40 | 8.94 | -2.54 |
| intermediate (aDOT 8-13) | 89 | 52 | 644 | 4 | 10 | 7.24 | 7.96 | -0.72 |
| short/YAC (aDOT <8) | 114 | 89 | 991 | 2 | 12 | 8.69 | 6.47 | 2.22 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 8, 'WR': 14} (24 total, 3.4/g)
- Pass 20+ by depth/direction: {'deep_left': 3, 'deep_middle': 4, 'deep_right': 2, 'short_left': 3, 'short_middle': 6, 'short_right': 6}
- Rush 15+ by position: {'QB': 1, 'RB': 9, 'WR': 2} (12 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 28 | 203 | 1 | 7.25 | 29 |
| RB | 138 | 600 | 9 | 4.35 | 85.70 |
| TE | 1 | 1 | 0 | 1 | 0.10 |
| WR | 6 | 59 | 2 | 9.83 | 8.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Daxton Hill | CB | 7 | 96.70 | 27 | 3.90 | 22 | 291 | 41.60 | 10.78 | 0 | 2 | 5 | 0 | 0 |
| D.J. Ivey | CB | 5 | 39.90 | 13 | 2.60 | 10 | 105 | 21 | 8.08 | 0 | 1 | 3 | 0 | 0 |
| DJ Turner II | CB | 7 | 94.90 | 18 | 2.60 | 13 | 92 | 13.10 | 5.11 | 0 | 0 | 5 | 0 | 0 |
| Jalen Davis | CB | 3 | 61.30 | 9 | 3 | 7 | 67 | 22.30 | 7.44 | 0 | 1 | 2 | 0 | 0 |
| Tacario Davis | CB | 4 | 18.30 | 6 | 1.50 | 5 | 46 | 11.50 | 7.67 | 0 | 0 | 1 | 0 | 0 |
| Josh Newton | CB | 1 | 45.50 | 2 | 2 | 1 | 25 | 25 | 12.50 | 0 | 1 | 1 | 0 | 0 |
| Demetrius Knight Jr. | LB | 7 | 83.30 | 15 | 2.10 | 14 | 132 | 18.90 | 8.80 | 0 | 1 | 0 | 1 | 0 |
| Barrett Carter | LB | 7 | 99.10 | 18 | 2.60 | 16 | 124 | 17.70 | 6.89 | 0 | 1 | 2 | 0 | 0 |
| Jordan Battle | S | 7 | 97.90 | 31 | 4.40 | 25 | 325 | 46.40 | 10.48 | 0 | 5 | 3 | 3 | 0 |
| Bryan Cook | S | 4 | 87.30 | 13 | 3.20 | 13 | 193 | 48.20 | 14.85 | 0 | 4 | 0 | 0 | 0 |
| Kyle Dugger | S | 1 | 66 | 5 | 5 | 5 | 88 | 88 | 17.60 | 0 | 1 | 0 | 0 | 0 |
| Russ Yeast | S | 1 | 34 | 2 | 2 | 2 | 38 | 38 | 19 | 0 | 1 | 0 | 0 | 0 |
| PJ Jules | S | 1 | 39 | 1 | 1 | 1 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Daxton Hill** (CB): WR3+:10t/123y, WR2:3t/49y, TE1:5t/43y, WR1:5t/37y, RB:3t/30y, TE2+:1t/9y | 20+: wk5 K.Coleman(WR3+) 23 deep_middle; wk8 C.Dike(WR3+) 28 short_right
- **D.J. Ivey** (CB): WR3+:7t/68y, RB:2t/16y, TE1:2t/16y, WR1:1t/5y, WR2:1t/0y | 20+: wk5 J.Tolbert(WR3+) 22 deep_right
- **DJ Turner II** (CB): WR1:9t/48y, WR3+:4t/26y, TE1:2t/10y, RB:1t/5y, WR2:2t/3y
- **Jalen Davis** (CB): WR3+:4t/38y, TE1:1t/15y, TE2+:1t/9y, RB:2t/5y, WR1:1t/0y | 20+: wk2 K.Boutte(WR3+) 21 deep_left
- **Tacario Davis** (CB): WR2:1t/14y, WR3+:2t/12y, TE1:2t/11y, RB:1t/9y
- **Josh Newton** (CB): TE1:1t/25y, WR2:1t/0y | 20+: wk8 G.Helm(TE1) 25 short_right
- **Demetrius Knight Jr.** (LB): TE1:6t/40y, WR2:2t/37y, RB:3t/24y, WR3+:2t/20y, WR1:2t/11y | 20+: wk1 C.Godwin(WR2) 30 short_middle
- **Barrett Carter** (LB): WR1:5t/38y, TE1:3t/26y, WR2:1t/22y, TE2+:2t/15y, RB:6t/13y, WR3+:1t/10y | 20+: wk4 J.Meyers(WR2) 22 deep_middle
- **Jordan Battle** (S): TE1:8t/104y, WR3+:8t/65y, RB:4t/55y, WR1:3t/37y, TE2+:3t/32y, WR2:5t/32y | 20+: wk2 D.Schultz(TE1) 35 short_right; wk2 D.Schultz(TE1) 25 deep_middle; wk3 J.Warren(RB) 30 short_middle; wk8 E.Ayomanor(WR3+) 23 short_middle; wk8 C.Dike(WR3+) 21 deep_middle
- **Bryan Cook** (S): TE2+:4t/66y, WR1:4t/57y, RB:3t/41y, TE1:1t/24y, WR2:1t/5y | 20+: wk1 B.Irving(RB) 22 short_left; wk2 F.Moreau(TE2+) 25 short_middle; wk7 Z.Flowers(WR1) 20 short_middle; wk8 G.Helm(TE1) 24 short_left
- **Kyle Dugger** (S): TE2+:2t/58y, WR1:1t/14y, TE1:1t/8y, RB:1t/8y | 20+: wk3 D.Washington(TE2+) 47 short_right
- **Russ Yeast** (S): TE1:2t/38y | 20+: wk4 B.Strange(TE1) 23 short_middle
- **PJ Jules** (S): TE1:1t/12y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TB@CIN | Jordan Battle | S | 5 | 5 | 46 | 0 | 0 | 0 | 0 | 0 | E.Egbukax2, C.Ottonx1, C.Godwinx1, B.Irvingx1 |
| 1 | TB@CIN | Bryan Cook | S | 3 | 3 | 34 | 0 | 1 | 0 | 0 | 0 | B.Irvingx2, C.Godwinx1 |
| 1 | TB@CIN | DJ Turner II | CB | 3 | 3 | 33 | 0 | 0 | 0 | 0 | 0 | E.Egbukax2, C.Godwinx1 |
| 1 | TB@CIN | Demetrius Knight Jr. | LB | 2 | 2 | 33 | 0 | 1 | 0 | 0 | 0 | C.Godwinx1, C.Ottonx1 |
| 1 | TB@CIN | Daxton Hill | CB | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | T.Hurstx2, B.Irvingx1 |
| 1 | TB@CIN | Jalen Davis | CB | 4 | 3 | 17 | 0 | 0 | 1 | 0 | 0 | B.Irvingx2, E.Egbukax1, T.Hurstx1 |
| 1 | TB@CIN | Barrett Carter | LB | 3 | 3 | 9 | 0 | 0 | 0 | 0 | 0 | E.Egbukax1, K.Gainwellx1, B.Irvingx1 |
| 2 | CIN@HOU | Jordan Battle | S | 6 | 5 | 81 | 0 | 2 | 1 | 0 | 0 | D.Schultzx3, D.Montgomeryx1, W.Marksx1, J.Waynex1 |
| 2 | CIN@HOU | Daxton Hill | CB | 12 | 8 | 80 | 0 | 0 | 4 | 0 | 0 | D.Schultzx4, X.Hutchinsonx3, J.Waynex2, D.Montgomeryx1, J.Noelx1, F.Moreaux1 |
| 2 | CIN@HOU | Bryan Cook | S | 3 | 3 | 55 | 0 | 1 | 0 | 0 | 0 | W.Marksx1, F.Moreaux1, X.Hutchinsonx1 |
| 2 | CIN@HOU | Demetrius Knight Jr. | LB | 4 | 4 | 37 | 0 | 0 | 0 | 0 | 0 | D.Schultzx2, K.Bouttex1, W.Marksx1 |
| 2 | CIN@HOU | Jalen Davis | CB | 3 | 2 | 36 | 0 | 1 | 1 | 0 | 0 | J.Waynex1, D.Schultzx1, K.Bouttex1 |
| 2 | CIN@HOU | DJ Turner II | CB | 6 | 4 | 24 | 0 | 0 | 2 | 0 | 0 | X.Hutchinsonx3, K.Bouttex1, D.Schultzx1, J.Waynex1 |
| 2 | CIN@HOU | Tacario Davis | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1 |
| 2 | CIN@HOU | Barrett Carter | LB | 2 | 2 | -2 | 0 | 0 | 0 | 0 | 0 | W.Marksx2 |
| 3 | CIN@PIT | Kyle Dugger | S | 5 | 5 | 88 | 0 | 1 | 0 | 0 | 0 | D.Washingtonx2, P.Freiermuthx1, J.Warrenx1, D.Metcalfx1 |
| 3 | CIN@PIT | Jordan Battle | S | 3 | 2 | 32 | 0 | 1 | 0 | 1 | 0 | J.Warrenx1, R.Wilsonx1, R.Tonyanx1 |
| 3 | CIN@PIT | Demetrius Knight Jr. | LB | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | D.Metcalfx1, J.Warrenx1 |
| 3 | CIN@PIT | Tacario Davis | CB | 3 | 2 | 22 | 0 | 0 | 1 | 0 | 0 | M.Pittmanx1, G.Bernardx1, P.Freiermuthx1 |
| 3 | CIN@PIT | Daxton Hill | CB | 2 | 1 | 17 | 0 | 0 | 1 | 0 | 0 | R.Wilsonx2 |
| 3 | CIN@PIT | Jalen Davis | CB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | R.Wilsonx1, D.Washingtonx1 |
| 3 | CIN@PIT | D.J. Ivey | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | M.Pittmanx1 |
| 3 | CIN@PIT | DJ Turner II | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Metcalfx1 |
| 3 | CIN@PIT | Barrett Carter | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Washingtonx1 |
| 4 | JAX@CIN | Barrett Carter | LB | 5 | 4 | 50 | 0 | 1 | 1 | 0 | 0 | J.Meyersx1, N.Boerkircherx1, P.Washingtonx1, B.Tutenx1, B.Strangex1 |
| 4 | JAX@CIN | Russ Yeast | S | 2 | 2 | 38 | 0 | 1 | 0 | 0 | 0 | B.Strangex2 |
| 4 | JAX@CIN | D.J. Ivey | CB | 3 | 2 | 29 | 0 | 0 | 1 | 0 | 0 | J.Meyersx1, J.Cameronx1, B.Strangex1 |
| 4 | JAX@CIN | Jordan Battle | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1, B.Strangex1 |
| 4 | JAX@CIN | DJ Turner II | CB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | P.Washingtonx2, Bri.Thomasx1 |
| 4 | JAX@CIN | PJ Jules | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | B.Strangex1 |
| 4 | JAX@CIN | Daxton Hill | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | B.Strangex1 |
| 4 | JAX@CIN | Tacario Davis | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | B.Tutenx1 |
| 4 | JAX@CIN | Demetrius Knight Jr. | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1 |
| 5 | CIN@MIA | Daxton Hill | CB | 2 | 2 | 31 | 0 | 1 | 0 | 0 | 0 | M.Washingtonx1, K.Colemanx1 |
| 5 | CIN@MIA | D.J. Ivey | CB | 4 | 2 | 27 | 0 | 1 | 2 | 0 | 0 | J.Tolbertx1, G.Dulcichx1, M.Washingtonx1, K.Colemanx1 |
| 5 | CIN@MIA | Jordan Battle | S | 3 | 1 | 13 | 0 | 0 | 0 | 2 | 0 | K.Colemanx2, M.Washingtonx1 |
| 5 | CIN@MIA | Barrett Carter | LB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx1, M.Washingtonx1 |
| 5 | CIN@MIA | Demetrius Knight Jr. | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx1 |
| 5 | CIN@MIA | Tacario Davis | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | K.Colemanx1 |
| 5 | CIN@MIA | DJ Turner II | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | J.Tolbertx1 |
| 7 | CIN@BAL | Daxton Hill | CB | 4 | 4 | 64 | 0 | 0 | 0 | 0 | 0 | R.Batemanx2, Z.Flowersx1, J.Hillx1 |
| 7 | CIN@BAL | Bryan Cook | S | 4 | 4 | 58 | 0 | 1 | 0 | 0 | 0 | Z.Flowersx3, J.Cuevasx1 |
| 7 | CIN@BAL | Barrett Carter | LB | 3 | 3 | 37 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx2, M.Andrewsx1 |
| 7 | CIN@BAL | D.J. Ivey | CB | 4 | 4 | 33 | 0 | 0 | 0 | 0 | 0 | J.Lanex3, J.Hillx1 |
| 7 | CIN@BAL | Jordan Battle | S | 2 | 2 | 31 | 0 | 0 | 0 | 0 | 0 | J.Cuevasx1, L.Westerx1 |
| 7 | CIN@BAL | DJ Turner II | CB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | M.Andrewsx1, Z.Flowersx1 |
| 7 | CIN@BAL | Demetrius Knight Jr. | LB | 2 | 1 | 4 | 0 | 0 | 0 | 1 | 0 | D.Henryx1, Z.Flowersx1 |
| 8 | TEN@CIN | Jordan Battle | S | 10 | 8 | 104 | 0 | 2 | 2 | 0 | 0 | G.Helmx3, W.Robinsonx3, C.Dikex2, E.Ayomanorx1, D.Bellingerx1 |
| 8 | TEN@CIN | Daxton Hill | CB | 3 | 3 | 57 | 0 | 1 | 0 | 0 | 0 | W.Robinsonx1, C.Dikex1, E.Ayomanorx1 |
| 8 | TEN@CIN | Bryan Cook | S | 3 | 3 | 46 | 0 | 1 | 0 | 0 | 0 | D.Bellingerx2, G.Helmx1 |
| 8 | TEN@CIN | Josh Newton | CB | 2 | 1 | 25 | 0 | 1 | 1 | 0 | 0 | W.Robinsonx1, G.Helmx1 |
| 8 | TEN@CIN | Demetrius Knight Jr. | LB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | G.Helmx2, C.Dikex1 |
| 8 | TEN@CIN | Barrett Carter | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | C.Ridleyx1, T.Pollardx1 |
| 8 | TEN@CIN | D.J. Ivey | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | T.Pollardx1 |
| 8 | TEN@CIN | DJ Turner II | CB | 2 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | T.Pollardx1, W.Robinsonx1 |

## Who beat them each week

**Wk1 TB@CIN** (vs TB offense, 216 rec yds allowed; 11% of targets unattributed)
- Top receivers: E.Egbuka (WR1, intermediate (aDOT 8-13)) 5/6 63y; B.Irving (RB, short/YAC (aDOT <8)) 7/7 48y; C.Godwin (WR2, short/YAC (aDOT <8)) 4/4 40y; T.Hurst (WR3+, deep (aDOT 13+)) 3/3 36y
- 20+ catches: C.Godwin(WR2) 30y short_middle - D.Knight [tackler]; B.Irving(RB) 22y short_left - B.Cook [tackler]

**Wk2 CIN@HOU** (vs HOU offense, 353 rec yds allowed; 26% of targets unattributed)
- Top receivers: D.Schultz (TE1, short/YAC (aDOT <8)) 12/14 140y; K.Boutte (WR3+, intermediate (aDOT 8-13)) 3/5 37y; X.Hutchinson (WR1, intermediate (aDOT 8-13)) 3/9 37y; F.Moreau (TE2+, short/YAC (aDOT <8)) 2/2 34y
- 20+ catches: D.Schultz(TE1) 35y short_right - J.Battle [tackler]; F.Moreau(TE2+) 25y short_middle - B.Cook [tackler]; K.Boutte(WR3+) 21y deep_left - J.Davis [tackler]; J.Noel(WR3+) 31y deep_left - no tackler named [unattributed]; D.Schultz(TE1) 25y deep_middle - J.Battle [tackler]

**Wk3 CIN@PIT** (vs PIT offense, 292 rec yds allowed; 32% of targets unattributed)
- Top receivers: D.Washington (TE2+, short/YAC (aDOT <8)) 3/4 67y; R.Wilson (WR3+, deep (aDOT 13+)) 3/6 60y 1TD; J.Warren (RB, short/YAC (aDOT <8)) 3/4 49y; D.Metcalf (WR1, intermediate (aDOT 8-13)) 3/5 31y 1TD
- 20+ catches: J.Warren(RB) 30y short_middle - J.Battle [tackler]; R.Wilson(WR3+) 38y deep_left TD - no tackler named [unattributed]; B.Skowronek(WR3+) 23y deep_right TD - no tackler named [unattributed]; P.Freiermuth(TE1) 22y short_left - C.Howell [tackler]; D.Washington(TE2+) 47y short_right - K.Dugger [tackler]
- 15+ runs: J.Warren(RB) 35y rush left end; J.Warren(RB) 26y rush left guard

**Wk4 JAX@CIN** (vs JAX offense, 227 rec yds allowed; 17% of targets unattributed)
- Top receivers: B.Strange (TE1, short/YAC (aDOT <8)) 7/8 95y; J.Cameron (WR3+, short/YAC (aDOT <8)) 2/2 42y; J.Meyers (WR2, intermediate (aDOT 8-13)) 3/4 33y; B.Tuten (RB, short/YAC (aDOT <8)) 2/2 18y
- 20+ catches: B.Strange(TE1) 23y short_middle - R.Yeast [tackler]; J.Meyers(WR2) 22y deep_middle - B.Carter [tackler]; J.Cameron(WR3+) 29y short_right - O.Burks [tackler]
- 15+ runs: B.Tuten(RB) 15y rush left end; B.Tuten(RB) 20y rush middle; C.Rodriguez(RB) 25y rush left guard

**Wk5 CIN@MIA** (vs MIA offense, 137 rec yds allowed; 33% of targets unattributed)
- Top receivers: M.Washington (WR1, intermediate (aDOT 8-13)) 6/8 43y; G.Dulcich (TE1, short/YAC (aDOT <8)) 4/6 37y; K.Coleman (WR3+, deep (aDOT 13+)) 3/7 30y 1TD; J.Tolbert (WR3+, intermediate (aDOT 8-13)) 1/2 22y
- 20+ catches: J.Tolbert(WR3+) 22y deep_right - D.Ivey [tackler]; K.Coleman(WR3+) 23y deep_middle - D.Hill [tackler]
- 15+ runs: M.Washington(WR) 18y rush right end; O.Gordon(RB) 22y rush right tackle; C.Bell(WR) 26y rush right end; M.Willis(QB) 39y rush left tackle; O.Gordon(RB) 15y rush left guard

**Wk7 CIN@BAL** (vs BAL offense, 298 rec yds allowed; 28% of targets unattributed)
- Top receivers: Z.Flowers (WR1, intermediate (aDOT 8-13)) 8/11 137y 1TD; J.Cuevas (TE2+, short/YAC (aDOT <8)) 2/3 35y; R.Bateman (WR2, deep (aDOT 13+)) 2/4 33y; J.Hill (RB, short/YAC (aDOT <8)) 3/4 26y
- 20+ catches: Z.Flowers(WR1) 48y short_right TD - no tackler named [unattributed]; Z.Flowers(WR1) 20y short_middle - B.Cook [tackler]

**Wk8 TEN@CIN** (vs TEN offense, 304 rec yds allowed; 30% of targets unattributed)
- Top receivers: G.Helm (TE1, short/YAC (aDOT <8)) 5/10 76y; C.Dike (WR3+, intermediate (aDOT 8-13)) 5/6 71y 1TD; W.Robinson (WR2, short/YAC (aDOT <8)) 6/7 57y 1TD; D.Bellinger (TE2+, short/YAC (aDOT <8)) 3/4 36y
- 20+ catches: E.Ayomanor(WR3+) 23y short_middle - J.Battle [tackler]; G.Helm(TE1) 24y short_left - B.Cook [tackler]; C.Dike(WR3+) 21y deep_middle - J.Battle [tackler]; C.Dike(WR3+) 28y short_right - D.Hill [tackler]; G.Helm(TE1) 25y short_right - J.Newton [tackler]
- 15+ runs: T.Pollard(RB) 40y rush right tackle; T.Pollard(RB) 22y rush left end

## Seed notes from defenders/CIN_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 7:55 Tony Pollard (RB) rush 40 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q1 5:57 Elic Ayomanor (WR) rec 23 — DJ Ivey [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said DJ Turner)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S15/R40)
- Q2 11:06 Gunnar Helm (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 10:01 Chimere Dike (WR) rec 21 — defender unknown [unknown; no public source]; alignment: middle (this-play pass_location proxy)
- Q3 10:15 Chimere Dike (WR) rec 28 — defender unknown [unknown; no public source]; alignment: outside (this-play pass_location proxy)
- Q4 12:06 Tony Pollard (RB) rush 22 — M.Murphy [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 5:05 Gunnar Helm (TE) rec 25 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Daxton Hill ← Wan'Dale Robinson: 7 tgt, 6 rec, 56 yds
- DJ Ivey ← Elic Ayomanor: 5 tgt, 3 rec, 34 yds

