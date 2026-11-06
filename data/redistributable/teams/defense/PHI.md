# PHI DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 WSH@PHI, wk2 PHI@TEN, wk3 PHI@CHI, wk4 LAR@PHI, wk5 PHI@JAX, wk6 CAR@PHI, wk7 DAL@PHI, wk8 PHI@WSH). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 15.1% / Zone 72.8% | MOF closed 49.1% / MOF open 43.4% | Blitz 23.4% | Light box 52.4% / Heavy box 20.2% | Sub package 74.0% | Sharp YPT allowed WR 8.4, TE 7.0, RB 4.3, Outside 8.7, Slot 8.9

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR3+: 9.35 YPT on 52 tgts (league 7.67, +1.68), 9 catches of 20+
- depth behind_los: 6.15 YPT on 34 tgts (league 4.58, +1.57), 3 catches of 20+
- depth inter_10-19: 13.33 YPT on 58 tgts (league 10.17, +3.16), 12 catches of 20+
- depth/direction deep_right: 14.7 YPT on 30 tgts (league 11.85, +2.85), 14 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 36 | 26 | 149 | 0 | 1 | 4.14 | 4.50 | 18.60 | 5.61 | -1.47 |
| TE1 | 30 | 22 | 227 | 0 | 3 | 7.57 | 3.80 | 28.40 | 7.39 | 0.18 |
| TE2+ | 18 | 11 | 106 | 2 | 0 | 5.89 | 2.20 | 13.20 | 6.71 | -0.82 |
| WR1 | 73 | 43 | 590 | 7 | 9 | 8.08 | 9.10 | 73.80 | 8.16 | -0.08 |
| WR2 | 49 | 29 | 394 | 2 | 6 | 8.04 | 6.10 | 49.20 | 8.20 | -0.16 |
| WR3+ | 52 | 31 | 486 | 1 | 9 | 9.35 | 6.50 | 60.80 | 7.67 | 1.68 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 12 | 7 | 43 | 0 | 0 | 3.58 | 5.61 | -2.03 |
| TE1 | 15 | 9 | 100 | 0 | 2 | 6.67 | 7.39 | -0.72 |
| TE2+ | 9 | 8 | 77 | 2 | 0 | 8.56 | 6.71 | 1.85 |
| WR1 | 36 | 20 | 322 | 5 | 6 | 8.94 | 8.16 | 0.78 |
| WR2 | 29 | 17 | 245 | 1 | 4 | 8.45 | 8.20 | 0.25 |
| WR3+ | 26 | 14 | 254 | 0 | 5 | 9.77 | 7.67 | 2.10 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 34 | 26 | 209 | 2 | 3 | 6.15 | 4.58 | 1.57 |
| short_1-9 | 133 | 83 | 646 | 5 | 2 | 4.86 | 6.23 | -1.37 |
| inter_10-19 | 58 | 42 | 773 | 3 | 12 | 13.33 | 10.17 | 3.16 |
| deep_20+ | 31 | 11 | 324 | 2 | 11 | 10.45 | 12.32 | -1.87 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 13 | 6 | 133 | 1 | 4 | 10.23 | 11.28 | -1.05 |
| deep_middle | 7 | 1 | 19 | 1 | 0 | 2.71 | 14.90 | -12.19 |
| deep_right | 30 | 16 | 441 | 2 | 14 | 14.70 | 11.85 | 2.85 |
| short_left | 73 | 51 | 472 | 1 | 5 | 6.47 | 6.08 | 0.39 |
| short_middle | 56 | 39 | 456 | 3 | 3 | 8.14 | 7.43 | 0.71 |
| short_right | 77 | 49 | 431 | 4 | 2 | 5.60 | 5.95 | -0.35 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 28 | 13 | 199 | 0 | 4 | 7.11 | 8.94 | -1.83 |
| intermediate (aDOT 8-13) | 98 | 55 | 832 | 8 | 14 | 8.49 | 7.96 | 0.53 |
| short/YAC (aDOT <8) | 132 | 94 | 921 | 4 | 10 | 6.98 | 6.47 | 0.51 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 3, 'WR': 24} (28 total, 3.5/g)
- Pass 20+ by depth/direction: {'deep_left': 4, 'deep_right': 14, 'short_left': 5, 'short_middle': 3, 'short_right': 2}
- Rush 15+ by position: {'QB': 1, 'RB': 9} (10 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 22 | 123 | 1 | 5.59 | 15.40 |
| RB | 217 | 931 | 9 | 4.29 | 116.40 |
| TE | 1 | 1 | 0 | 1 | 0.10 |
| WR | 2 | 9 | 0 | 4.50 | 1.10 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Riq Woolen | CB | 7 | 98.30 | 27 | 3.90 | 21 | 261 | 37.30 | 9.67 | 0 | 4 | 6 | 0 | 0 |
| Quinyon Mitchell | CB | 8 | 92.10 | 31 | 3.90 | 23 | 244 | 30.50 | 7.87 | 0 | 2 | 7 | 1 | 0 |
| Kenny Moore II | CB | 3 | 47.20 | 8 | 2.70 | 8 | 176 | 58.70 | 22 | 0 | 4 | 0 | 0 | 0 |
| Cooper DeJean | CB | 7 | 99.40 | 24 | 3.40 | 19 | 169 | 24.10 | 7.04 | 0 | 0 | 4 | 1 | 0 |
| Jonathan Jones | CB | 3 | 14.80 | 5 | 1.70 | 4 | 48 | 16 | 9.60 | 0 | 1 | 1 | 0 | 0 |
| Michael Carter II | CB | 3 | 28.70 | 5 | 1.70 | 3 | 26 | 8.70 | 5.20 | 0 | 0 | 2 | 0 | 0 |
| Jihaad Campbell | LB | 5 | 82.40 | 15 | 3 | 15 | 170 | 34 | 11.33 | 0 | 3 | 0 | 0 | 0 |
| Zack Baun | LB | 7 | 98.90 | 20 | 2.90 | 15 | 114 | 16.30 | 5.70 | 0 | 1 | 5 | 0 | 0 |
| Jeremiah Trotter Jr. | LB | 2 | 53.60 | 14 | 7 | 13 | 97 | 48.50 | 6.93 | 0 | 0 | 1 | 0 | 0 |
| Andrew Mukuba | S | 8 | 99.50 | 18 | 2.20 | 16 | 222 | 27.80 | 12.33 | 0 | 4 | 1 | 1 | 0 |
| Marcus Epps | S | 4 | 52.50 | 6 | 1.50 | 5 | 76 | 19 | 12.67 | 0 | 2 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Riq Woolen** (CB): WR1:11t/125y, WR3+:6t/78y, WR2:4t/31y, TE1:3t/16y, RB:3t/11y | 20+: wk2 C.Ridley(WR3+) 25 deep_right; wk4 P.Nacua(WR1) 28 deep_right; wk4 P.Nacua(WR1) 32 deep_right; wk8 T.Burks(WR3+) 21 deep_right
- **Quinyon Mitchell** (CB): WR3+:7t/92y, WR2:10t/68y, WR1:9t/52y, TE2+:2t/21y, TE1:3t/11y | 20+: wk6 T.McMillan(WR1) 21 deep_left; wk8 T.Burks(WR3+) 53 deep_right
- **Kenny Moore II** (CB): WR2:3t/68y, WR3+:2t/47y, WR1:2t/34y, TE1:1t/27y | 20+: wk5 J.Cameron(WR3+) 32 short_left; wk5 B.Strange(TE1) 27 deep_left; wk8 S.Diggs(WR1) 20 short_middle; wk8 A.Williams(WR2) 30 deep_right
- **Cooper DeJean** (CB): WR2:5t/57y, RB:6t/40y, WR1:5t/36y, WR3+:6t/26y, TE1:2t/10y
- **Jonathan Jones** (CB): WR2:2t/21y, TE1:1t/14y, WR3+:1t/8y, RB:1t/5y | 20+: wk7 G.Pickens(WR2) 21 short_left
- **Michael Carter II** (CB): WR1:1t/16y, TE1:1t/5y, WR3+:2t/5y, WR2:1t/0y
- **Jihaad Campbell** (LB): WR3+:2t/54y, TE1:4t/42y, WR2:1t/33y, RB:5t/21y, WR1:3t/20y | 20+: wk1 A.Williams(WR2) 33 deep_left; wk2 E.Ayomanor(WR3+) 41 deep_right; wk4 T.Higbee(TE1) 20 deep_right
- **Zack Baun** (LB): WR3+:3t/40y, TE2+:5t/35y, WR1:4t/22y, WR2:2t/10y, TE1:2t/4y, RB:4t/3y | 20+: wk2 E.Ayomanor(WR3+) 28 short_left
- **Jeremiah Trotter Jr.** (LB): RB:6t/39y, WR1:4t/30y, TE1:1t/11y, WR2:2t/10y, WR3+:1t/7y
- **Andrew Mukuba** (S): WR1:4t/62y, TE1:5t/55y, WR3+:4t/55y, WR2:2t/41y, TE2+:1t/6y, RB:2t/3y | 20+: wk3 L.Burden(WR1) 25 short_left; wk6 J.Coker(WR2) 32 short_middle; wk7 R.Flournoy(WR3+) 35 deep_right; wk8 C.Okonkwo(TE1) 21 deep_left
- **Marcus Epps** (S): RB:2t/27y, WR2:1t/22y, WR1:1t/13y, TE2+:1t/8y, WR3+:1t/6y | 20+: wk2 T.Spears(RB) 27 short_right; wk3 R.Odunze(WR2) 22 deep_right

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WSH@PHI | Cooper DeJean | CB | 5 | 5 | 60 | 0 | 0 | 0 | 0 | 0 | S.Diggsx2, A.Williamsx1, J.Lanex1, T.McLaurinx1 |
| 1 | WSH@PHI | Jihaad Campbell | LB | 2 | 2 | 35 | 0 | 1 | 0 | 0 | 0 | A.Williamsx1, R.Whitex1 |
| 1 | WSH@PHI | Marcus Epps | S | 3 | 3 | 27 | 0 | 0 | 0 | 0 | 0 | S.Diggsx1, J.Batesx1, T.McLaurinx1 |
| 1 | WSH@PHI | Quinyon Mitchell | CB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | C.Okonkwox1, A.Williamsx1 |
| 1 | WSH@PHI | Andrew Mukuba | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | C.Okonkwox1 |
| 1 | WSH@PHI | Zack Baun | LB | 4 | 2 | -4 | 0 | 0 | 2 | 0 | 0 | S.Diggsx1, J.Croskey-Merrittx1, R.Whitex1, J.Batesx1 |
| 2 | PHI@TEN | Jihaad Campbell | LB | 4 | 4 | 52 | 0 | 1 | 0 | 0 | 0 | T.Pollardx1, T.Spearsx1, G.Helmx1, E.Ayomanorx1 |
| 2 | PHI@TEN | Riq Woolen | CB | 4 | 3 | 46 | 0 | 1 | 1 | 0 | 0 | C.Tatex3, C.Ridleyx1 |
| 2 | PHI@TEN | Zack Baun | LB | 1 | 1 | 28 | 0 | 1 | 0 | 0 | 0 | E.Ayomanorx1 |
| 2 | PHI@TEN | Marcus Epps | S | 1 | 1 | 27 | 0 | 1 | 0 | 0 | 0 | T.Spearsx1 |
| 2 | PHI@TEN | Quinyon Mitchell | CB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | C.Ridleyx1, C.Tatex1 |
| 2 | PHI@TEN | Andrew Mukuba | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1 |
| 2 | PHI@TEN | Cooper DeJean | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | G.Helmx1 |
| 3 | PHI@CHI | Quinyon Mitchell | CB | 7 | 5 | 42 | 0 | 0 | 2 | 0 | 0 | L.Burdenx3, R.Odunzex3, K.Raymondx1 |
| 3 | PHI@CHI | Andrew Mukuba | S | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | L.Burdenx1, K.Raymondx1 |
| 3 | PHI@CHI | Jihaad Campbell | LB | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1, K.Raymondx1, C.Lovelandx1 |
| 3 | PHI@CHI | Zack Baun | LB | 4 | 3 | 26 | 0 | 0 | 1 | 0 | 0 | L.Burdenx2, C.Lovelandx1, S.Roushx1 |
| 3 | PHI@CHI | Riq Woolen | CB | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | K.Raymondx1, D.Swiftx1, C.Lovelandx1 |
| 3 | PHI@CHI | Marcus Epps | S | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | R.Odunzex1 |
| 3 | PHI@CHI | Michael Carter II | CB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | C.Lovelandx1, K.Raymondx1 |
| 3 | PHI@CHI | Cooper DeJean | CB | 5 | 3 | 5 | 0 | 0 | 2 | 0 | 0 | D.Swiftx2, L.Burdenx2, Z.Thomasx1 |
| 4 | LAR@PHI | Riq Woolen | CB | 6 | 5 | 83 | 0 | 2 | 1 | 0 | 0 | P.Nacuax4, K.Williamsx2 |
| 4 | LAR@PHI | Jeremiah Trotter Jr. | LB | 11 | 10 | 81 | 0 | 0 | 1 | 0 | 0 | P.Nacuax4, K.Williamsx3, B.Corumx1, T.Higbeex1, K.Mumpfieldx1, D.Adamsx1 |
| 4 | LAR@PHI | Jihaad Campbell | LB | 5 | 5 | 47 | 0 | 1 | 0 | 0 | 0 | T.Higbeex2, K.Williamsx2, P.Nacuax1 |
| 4 | LAR@PHI | Quinyon Mitchell | CB | 3 | 3 | 27 | 0 | 0 | 0 | 0 | 0 | D.Adamsx3 |
| 4 | LAR@PHI | Cooper DeJean | CB | 5 | 3 | 20 | 0 | 0 | 1 | 1 | 0 | J.Whittingtonx2, B.Corumx1, P.Nacuax1, K.Williamsx1 |
| 4 | LAR@PHI | Andrew Mukuba | S | 3 | 2 | 14 | 0 | 0 | 0 | 1 | 0 | K.Mumpfieldx1, K.Williamsx1, P.Nacuax1 |
| 4 | LAR@PHI | Jonathan Jones | CB | 3 | 2 | 13 | 0 | 0 | 1 | 0 | 0 | K.Williamsx1, T.Atwellx1, D.Adamsx1 |
| 4 | LAR@PHI | Michael Carter II | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | D.Adamsx1, K.Mumpfieldx1 |
| 5 | PHI@JAX | Kenny Moore II | CB | 4 | 4 | 92 | 0 | 2 | 0 | 0 | 0 | J.Cameronx1, P.Washingtonx1, B.Strangex1, J.Meyersx1 |
| 5 | PHI@JAX | Cooper DeJean | CB | 4 | 4 | 38 | 0 | 0 | 0 | 0 | 0 | T.Hunterx1, B.Strangex1, C.Rodriguezx1, B.Tutenx1 |
| 5 | PHI@JAX | Quinyon Mitchell | CB | 6 | 4 | 31 | 0 | 0 | 1 | 1 | 0 | B.Strangex2, Bri.Thomasx2, N.Boerkircherx1, P.Washingtonx1 |
| 5 | PHI@JAX | Riq Woolen | CB | 4 | 3 | 29 | 0 | 0 | 1 | 0 | 0 | P.Washingtonx1, B.Strangex1, J.Meyersx1, Bri.Thomasx1 |
| 5 | PHI@JAX | Zack Baun | LB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | B.Tutenx1, N.Boerkircherx1, J.Cameronx1 |
| 5 | PHI@JAX | Michael Carter II | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | P.Washingtonx1 |
| 5 | PHI@JAX | Andrew Mukuba | S | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | J.Cameronx1, B.Strangex1 |
| 5 | PHI@JAX | Jonathan Jones | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | B.Strangex1 |
| 6 | CAR@PHI | Andrew Mukuba | S | 3 | 3 | 53 | 0 | 1 | 0 | 0 | 0 | T.McMillanx1, T.Tremblex1, J.Cokerx1 |
| 6 | CAR@PHI | Kenny Moore II | CB | 2 | 2 | 34 | 0 | 0 | 0 | 0 | 0 | J.Cokerx1, J.Metchiex1 |
| 6 | CAR@PHI | Cooper DeJean | CB | 3 | 2 | 32 | 0 | 0 | 1 | 0 | 0 | J.Cokerx3 |
| 6 | CAR@PHI | Quinyon Mitchell | CB | 5 | 2 | 30 | 0 | 1 | 3 | 0 | 0 | T.McMillanx3, J.Cokerx1, T.Tremblex1 |
| 6 | CAR@PHI | Zack Baun | LB | 4 | 3 | 26 | 0 | 0 | 1 | 0 | 0 | T.McMillanx1, J.Metchiex1, C.Hubbardx1, J.Cokerx1 |
| 6 | CAR@PHI | Riq Woolen | CB | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | D.Wallerx1, J.Cokerx1, T.McMillanx1 |
| 6 | CAR@PHI | Jihaad Campbell | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | T.McMillanx1 |
| 7 | DAL@PHI | Riq Woolen | CB | 5 | 3 | 36 | 0 | 0 | 2 | 0 | 0 | R.Flournoyx2, C.Lambx2, G.Pickensx1 |
| 7 | DAL@PHI | Andrew Mukuba | S | 1 | 1 | 35 | 0 | 1 | 0 | 0 | 0 | R.Flournoyx1 |
| 7 | DAL@PHI | Jonathan Jones | CB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | G.Pickensx1 |
| 7 | DAL@PHI | Quinyon Mitchell | CB | 3 | 2 | 18 | 0 | 0 | 1 | 0 | 0 | C.Lambx1, G.Pickensx1, R.Flournoyx1 |
| 7 | DAL@PHI | Zack Baun | LB | 3 | 2 | 11 | 0 | 0 | 1 | 0 | 0 | B.Spann-Fordx2, J.Fergusonx1 |
| 7 | DAL@PHI | Cooper DeJean | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | G.Pickensx1 |
| 8 | PHI@WSH | Quinyon Mitchell | CB | 3 | 3 | 65 | 0 | 1 | 0 | 0 | 0 | T.Burksx2, A.Williamsx1 |
| 8 | PHI@WSH | Kenny Moore II | CB | 2 | 2 | 50 | 0 | 2 | 0 | 0 | 0 | S.Diggsx1, A.Williamsx1 |
| 8 | PHI@WSH | Andrew Mukuba | S | 5 | 4 | 43 | 0 | 1 | 1 | 0 | 0 | C.Okonkwox3, R.Whitex1, S.Diggsx1 |
| 8 | PHI@WSH | Riq Woolen | CB | 2 | 2 | 25 | 0 | 1 | 0 | 0 | 0 | A.Williamsx1, T.Burksx1 |
| 8 | PHI@WSH | Jeremiah Trotter Jr. | LB | 3 | 3 | 16 | 0 | 0 | 0 | 0 | 0 | R.Whitex1, A.Williamsx1, J.McNicholsx1 |
| 8 | PHI@WSH | Zack Baun | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | A.Williamsx1 |
| 8 | PHI@WSH | Marcus Epps | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | R.Whitex1 |

## Who beat them each week

**Wk1 WSH@PHI** (vs WSH offense, 164 rec yds allowed; 40% of targets unattributed)
- Top receivers: A.Williams (WR2, intermediate (aDOT 8-13)) 4/4 64y 1TD; S.Diggs (WR1, intermediate (aDOT 8-13)) 4/9 55y 1TD; C.Okonkwo (TE1, short/YAC (aDOT <8)) 2/3 16y; T.McLaurin (WR3+, intermediate (aDOT 8-13)) 2/4 14y
- 20+ catches: A.Williams(WR2) 33y deep_left - J.Campbell [tackler]

**Wk2 PHI@TEN** (vs TEN offense, 183 rec yds allowed; 18% of targets unattributed)
- Top receivers: E.Ayomanor (WR3+, intermediate (aDOT 8-13)) 2/3 69y; C.Ridley (WR3+, intermediate (aDOT 8-13)) 2/2 35y; T.Spears (RB, short/YAC (aDOT <8)) 2/2 29y; C.Tate (WR1, intermediate (aDOT 8-13)) 3/5 27y
- 20+ catches: E.Ayomanor(WR3+) 28y short_left - Z.Baun [tackler]; T.Spears(RB) 27y short_right - M.Epps [tackler]; C.Ridley(WR3+) 25y deep_right - T.Woolen [tackler]; E.Ayomanor(WR3+) 41y deep_right - J.Campbell [tackler]
- 15+ runs: T.Pollard(RB) 18y rush left tackle; T.Spears(RB) 27y rush left end

**Wk3 PHI@CHI** (vs CHI offense, 247 rec yds allowed; 18% of targets unattributed)
- Top receivers: K.Raymond (WR3+, short/YAC (aDOT <8)) 6/7 90y 1TD; L.Burden (WR1, short/YAC (aDOT <8)) 7/11 61y 1TD; R.Odunze (WR2, deep (aDOT 13+)) 3/6 44y; C.Loveland (TE1, short/YAC (aDOT <8)) 4/4 31y
- 20+ catches: L.Burden(WR1) 25y short_left - A.Mukuba [tackler]; R.Odunze(WR2) 22y deep_right - M.Epps [tackler]; K.Raymond(WR3+) 41y short_middle TD - no tackler named [unattributed]
- 15+ runs: D.Swift(RB) 15y rush left tackle

**Wk4 LAR@PHI** (vs LAR offense, 317 rec yds allowed; 20% of targets unattributed)
- Top receivers: P.Nacua (WR1, short/YAC (aDOT <8)) 9/12 125y; T.Higbee (TE1, short/YAC (aDOT <8)) 5/6 67y; K.Williams (RB, short/YAC (aDOT <8)) 10/13 67y; D.Adams (WR2, deep (aDOT 13+)) 4/9 32y
- 20+ catches: P.Nacua(WR1) 28y deep_right - T.Woolen [tackler]; T.Higbee(TE1) 20y deep_right - J.Campbell [tackler]; P.Nacua(WR1) 32y deep_right - T.Woolen [tackler]
- 15+ runs: K.Williams(RB) 23y rush left tackle

**Wk5 PHI@JAX** (vs JAX offense, 331 rec yds allowed; 26% of targets unattributed)
- Top receivers: P.Washington (WR1, intermediate (aDOT 8-13)) 6/9 124y 2TD; B.Strange (TE1, short/YAC (aDOT <8)) 7/8 68y; J.Cameron (WR3+, short/YAC (aDOT <8)) 3/6 43y; J.Meyers (WR2, intermediate (aDOT 8-13)) 2/3 37y
- 20+ catches: P.Washington(WR1) 51y short_right TD - no tackler named [unattributed]; J.Cameron(WR3+) 32y short_left - K.Moore [tackler]; B.Strange(TE1) 27y deep_left - K.Moore [tackler]; P.Washington(WR1) 27y deep_right TD - no tackler named [unattributed]
- 15+ runs: T.Lawrence(QB) 16y rush left guard

**Wk6 CAR@PHI** (vs CAR offense, 281 rec yds allowed; 31% of targets unattributed)
- Top receivers: J.Coker (WR2, intermediate (aDOT 8-13)) 6/13 97y; T.McMillan (WR1, intermediate (aDOT 8-13)) 6/9 86y; T.Tremble (TE2+, short/YAC (aDOT <8)) 4/4 46y 2TD; D.Moore (WR3+, deep (aDOT 13+)) 1/1 27y
- 20+ catches: T.McMillan(WR1) 21y deep_right - no tackler named [unattributed]; T.McMillan(WR1) 21y deep_left - Q.Mitchell [tackler]; J.Coker(WR2) 32y short_middle - A.Mukuba [tackler]; D.Moore(WR3+) 27y short_left - B.Young [tackler]
- 15+ runs: C.Hubbard(RB) 19y rush left tackle

**Wk7 DAL@PHI** (vs DAL offense, 212 rec yds allowed; 46% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 5/12 74y 2TD; R.Flournoy (WR3+, short/YAC (aDOT <8)) 4/4 70y; G.Pickens (WR2, intermediate (aDOT 8-13)) 4/6 57y 1TD; B.Spann-Ford (TE2+, short/YAC (aDOT <8)) 2/2 11y
- 20+ catches: R.Flournoy(WR3+) 35y deep_right - A.Mukuba [tackler]; G.Pickens(WR2) 21y deep_right TD - no tackler named [unattributed]; G.Pickens(WR2) 21y short_left - J.Jones [tackler]; C.Lamb(WR1) 30y deep_right - no tackler named [unattributed]
- 15+ runs: J.Williams(RB) 15y rush left guard; J.Williams(RB) 34y rush left tackle

**Wk8 PHI@WSH** (vs WSH offense, 217 rec yds allowed; 33% of targets unattributed)
- Top receivers: T.Burks (WR3+, deep (aDOT 13+)) 3/5 81y; A.Williams (WR2, intermediate (aDOT 8-13)) 5/7 54y; S.Diggs (WR1, intermediate (aDOT 8-13)) 3/6 38y 1TD; C.Okonkwo (TE1, short/YAC (aDOT <8)) 2/4 32y
- 20+ catches: T.Burks(WR3+) 21y deep_right - T.Woolen [tackler]; S.Diggs(WR1) 20y short_middle - K.Moore [tackler]; C.Okonkwo(TE1) 21y deep_left - A.Mukuba [tackler]; T.Burks(WR3+) 53y deep_right - Q.Mitchell [tackler]; A.Williams(WR2) 30y deep_right - K.Moore [tackler]
- 15+ runs: A.Ekeler(RB) 18y rush left end; R.White(RB) 33y rush left tackle

