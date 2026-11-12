# HOU DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 BUF@HOU, wk2 CIN@HOU, wk3 HOU@IND, wk4 DAL@HOU, wk5 HOU@TEN, wk6 HOU@JAX, wk7 NYG@HOU). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 15.7% / Zone 80.3% | MOF closed 58.2% / MOF open 39.9% | Blitz 23.8% | Light box 47.1% / Heavy box 22.4% | Sub package 79.0% | Sharp YPT allowed WR 8.8, TE 7.3, RB 3.6, Outside 10.1, Slot 7.9

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR2: 9.84 YPT on 45 tgts (league 8.2, +1.64), 9 catches of 20+
- depth deep_20+: 14.68 YPT on 28 tgts (league 12.32, +2.36), 12 catches of 20+
- depth/direction deep_right: 16.61 YPT on 18 tgts (league 11.85, +4.76), 8 catches of 20+
- receiver archetype deep (aDOT 13+): 10.47 YPT on 34 tgts (league 8.94, +1.53), 8 catches of 20+

Holds (-1.5 YPT or better): RB: 3.65 YPT on 40 tgts (league 5.61, -1.96)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 40 | 33 | 146 | 2 | 1 | 3.65 | 5.70 | 20.90 | 5.61 | -1.96 |
| TE1 | 32 | 24 | 252 | 0 | 4 | 7.88 | 4.60 | 36 | 7.39 | 0.49 |
| TE2+ | 12 | 8 | 70 | 1 | 1 | 5.83 | 1.70 | 10 | 6.71 | -0.88 |
| WR1 | 73 | 43 | 582 | 1 | 9 | 7.97 | 10.40 | 83.10 | 8.16 | -0.19 |
| WR2 | 45 | 31 | 443 | 3 | 9 | 9.84 | 6.40 | 63.30 | 8.20 | 1.64 |
| WR3+ | 39 | 24 | 346 | 3 | 5 | 8.87 | 5.60 | 49.40 | 7.67 | 1.20 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 27 | 24 | 112 | 2 | 1 | 4.15 | 5.61 | -1.46 |
| TE1 | 16 | 10 | 67 | 0 | 1 | 4.19 | 7.39 | -3.20 |
| TE2+ | 7 | 4 | 42 | 1 | 1 | 6 | 6.71 | -0.71 |
| WR1 | 46 | 29 | 370 | 1 | 5 | 8.04 | 8.16 | -0.12 |
| WR2 | 25 | 17 | 294 | 0 | 6 | 11.76 | 8.20 | 3.56 |
| WR3+ | 25 | 15 | 178 | 1 | 2 | 7.12 | 7.67 | -0.55 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 56 | 45 | 178 | 1 | 1 | 3.18 | 4.58 | -1.40 |
| short_1-9 | 96 | 73 | 606 | 4 | 4 | 6.31 | 6.23 | 0.08 |
| inter_10-19 | 60 | 33 | 644 | 2 | 12 | 10.73 | 10.17 | 0.56 |
| deep_20+ | 28 | 12 | 411 | 3 | 12 | 14.68 | 12.32 | 2.36 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 20 | 10 | 241 | 0 | 7 | 12.05 | 11.28 | 0.77 |
| deep_middle | 11 | 7 | 177 | 1 | 3 | 16.09 | 14.90 | 1.19 |
| deep_right | 18 | 10 | 299 | 3 | 8 | 16.61 | 11.85 | 4.76 |
| short_left | 62 | 48 | 306 | 1 | 1 | 4.94 | 6.08 | -1.14 |
| short_middle | 48 | 33 | 374 | 1 | 6 | 7.79 | 7.43 | 0.36 |
| short_right | 81 | 55 | 442 | 4 | 4 | 5.46 | 5.95 | -0.49 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 34 | 18 | 356 | 2 | 8 | 10.47 | 8.94 | 1.53 |
| intermediate (aDOT 8-13) | 97 | 60 | 908 | 3 | 16 | 9.36 | 7.96 | 1.40 |
| short/YAC (aDOT <8) | 110 | 85 | 575 | 5 | 5 | 5.23 | 6.47 | -1.24 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 5, 'WR': 23} (29 total, 4.1/g)
- Pass 20+ by depth/direction: {'deep_left': 7, 'deep_middle': 3, 'deep_right': 8, 'short_left': 1, 'short_middle': 6, 'short_right': 4}
- Rush 15+ by position: {'QB': 1, 'RB': 4} (5 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 18 | 55 | 1 | 3.06 | 7.90 |
| RB | 155 | 635 | 4 | 4.10 | 90.70 |
| TE | 1 | 2 | 0 | 2 | 0.30 |
| WR | 2 | -3 | 0 | -1.50 | -0.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kamari Lassiter | CB | 7 | 100 | 35 | 5 | 30 | 360 | 51.40 | 10.29 | 0 | 5 | 5 | 0 | 0 |
| Derek Stingley Jr. | CB | 5 | 99.10 | 15 | 3 | 11 | 155 | 31 | 10.33 | 0 | 3 | 4 | 0 | 0 |
| Tremon Smith | CB | 2 | 27.70 | 5 | 2.50 | 3 | 40 | 20 | 8 | 0 | 0 | 2 | 0 | 0 |
| Jaylin Smith | CB | 1 | 12 | 1 | 1 | 1 | 16 | 16 | 16 | 0 | 0 | 0 | 0 | 0 |
| Azeez Al-Shaair | LB | 6 | 93.20 | 21 | 3.50 | 19 | 229 | 38.20 | 10.90 | 0 | 4 | 2 | 0 | 0 |
| Jake Hansen | LB | 2 | 66.90 | 11 | 5.50 | 9 | 56 | 28 | 5.09 | 0 | 1 | 1 | 1 | 0 |
| Calen Bullock | S | 6 | 97.60 | 23 | 3.80 | 19 | 298 | 49.70 | 12.96 | 0 | 5 | 3 | 1 | 0 |
| Reed Blankenship | S | 6 | 85.50 | 28 | 4.70 | 25 | 240 | 40 | 8.57 | 0 | 4 | 2 | 1 | 0 |
| Jalen Pitre | S | 4 | 92 | 11 | 2.80 | 8 | 71 | 17.80 | 6.45 | 0 | 1 | 3 | 0 | 0 |
| M.J. Stewart | S | 2 | 73.50 | 9 | 4.50 | 8 | 64 | 32 | 7.11 | 0 | 1 | 1 | 0 | 0 |
| Kamari Ramsey | S | 2 | 16.20 | 3 | 1.50 | 3 | 14 | 7 | 4.67 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Kamari Lassiter** (CB): WR1:10t/152y, WR2:7t/131y, WR3+:7t/33y, TE1:7t/30y, TE2+:2t/14y, RB:2t/0y | 20+: wk4 C.Lamb(WR1) 30 deep_left; wk4 G.Pickens(WR2) 53 deep_middle; wk6 P.Washington(WR1) 27 deep_left; wk7 M.Nabers(WR1) 42 deep_right; wk7 M.Fields(WR2) 47 short_right
- **Derek Stingley Jr.** (CB): WR1:7t/56y, TE1:3t/54y, WR2:2t/24y, RB:3t/21y | 20+: wk1 D.Kincaid(TE1) 38 deep_right; wk2 T.Higgins(WR1) 23 deep_right; wk7 M.Nabers(WR1) 27 deep_left
- **Tremon Smith** (CB): WR3+:2t/26y, WR2:2t/14y, WR1:1t/0y
- **Jaylin Smith** (CB): RB:1t/16y
- **Azeez Al-Shaair** (LB): WR1:8t/107y, WR3+:3t/50y, WR2:4t/32y, RB:3t/25y, TE1:3t/15y | 20+: wk2 T.Higgins(WR1) 23 short_middle; wk3 J.Downs(WR1) 24 short_right; wk3 K.Allen(WR2) 26 deep_right; wk6 T.Hunter(WR3+) 26 short_middle
- **Jake Hansen** (LB): WR3+:2t/23y, RB:7t/17y, WR1:1t/11y, TE2+:1t/5y | 20+: wk5 C.Ridley(WR3+) 23 short_middle
- **Calen Bullock** (S): WR1:8t/107y, TE1:6t/90y, WR2:5t/54y, WR3+:4t/47y | 20+: wk1 D.Kincaid(TE1) 40 deep_right; wk3 L.Treadwell(WR3+) 20 deep_middle; wk6 B.Strange(TE1) 24 deep_left; wk6 J.Meyers(WR2) 28 deep_left; wk7 M.Fields(WR2) 20 deep_right
- **Reed Blankenship** (S): WR2:8t/85y, WR1:6t/63y, WR3+:5t/52y, TE1:4t/20y, TE2+:2t/16y, RB:3t/4y | 20+: wk2 T.Higgins(WR1) 21 short_middle; wk3 K.Allen(WR2) 20 short_middle; wk4 C.Lamb(WR1) 21 short_left; wk4 G.Pickens(WR2) 22 deep_left
- **Jalen Pitre** (S): TE1:2t/44y, WR1:5t/17y, RB:4t/10y | 20+: wk1 D.Kincaid(TE1) 35 short_right
- **M.J. Stewart** (S): TE2+:1t/29y, RB:4t/20y, WR1:2t/11y, TE1:1t/4y, WR3+:1t/0y | 20+: wk7 T.Fidone(TE2+) 29 deep_left
- **Kamari Ramsey** (S): WR2:1t/8y, WR1:2t/6y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BUF@HOU | Calen Bullock | S | 5 | 4 | 88 | 0 | 1 | 1 | 0 | 0 | D.Moorex2, D.Kincaidx2, K.Shakirx1 |
| 1 | BUF@HOU | Derek Stingley Jr. | CB | 2 | 2 | 44 | 0 | 1 | 0 | 0 | 0 | D.Kincaidx1, J.Cookx1 |
| 1 | BUF@HOU | Jalen Pitre | S | 3 | 2 | 38 | 0 | 1 | 1 | 0 | 0 | K.Shakirx1, J.Cookx1, D.Kincaidx1 |
| 1 | BUF@HOU | Reed Blankenship | S | 4 | 4 | 35 | 0 | 0 | 0 | 0 | 0 | J.Cookx1, K.Colemanx1, D.Moorex1, D.Kincaidx1 |
| 1 | BUF@HOU | Azeez Al-Shaair | LB | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | K.Shakirx2 |
| 1 | BUF@HOU | Kamari Lassiter | CB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | D.Moorex1, D.Knoxx1 |
| 2 | CIN@HOU | Azeez Al-Shaair | LB | 6 | 6 | 68 | 0 | 1 | 0 | 0 | 0 | T.Higginsx3, C.Youngx1, C.Brownx1, J.Chasex1 |
| 2 | CIN@HOU | Reed Blankenship | S | 3 | 3 | 28 | 0 | 1 | 0 | 0 | 0 | T.Higginsx1, A.Iosivasx1, E.Allx1 |
| 2 | CIN@HOU | Derek Stingley Jr. | CB | 2 | 1 | 23 | 0 | 1 | 1 | 0 | 0 | T.Higginsx2 |
| 2 | CIN@HOU | Jaylin Smith | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | S.Perinex1 |
| 2 | CIN@HOU | Kamari Lassiter | CB | 4 | 4 | 13 | 0 | 0 | 0 | 0 | 0 | J.Chasex3, C.Brownx1 |
| 3 | HOU@IND | Calen Bullock | S | 6 | 6 | 64 | 0 | 1 | 0 | 0 | 0 | J.Downsx2, K.Allenx2, T.Warrenx1, L.Treadwellx1 |
| 3 | HOU@IND | Azeez Al-Shaair | LB | 3 | 3 | 57 | 0 | 2 | 0 | 0 | 0 | J.Downsx1, T.Warrenx1, K.Allenx1 |
| 3 | HOU@IND | Reed Blankenship | S | 8 | 6 | 55 | 0 | 1 | 1 | 1 | 0 | T.Warrenx3, K.Allenx2, J.Downsx2, M.Alie-Coxx1 |
| 3 | HOU@IND | Kamari Lassiter | CB | 5 | 5 | 25 | 0 | 0 | 0 | 0 | 0 | T.Warrenx3, J.Taylorx1, K.Allenx1 |
| 3 | HOU@IND | Jalen Pitre | S | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | T.Warrenx1, J.Downsx1 |
| 4 | DAL@HOU | Kamari Lassiter | CB | 10 | 8 | 122 | 0 | 2 | 2 | 0 | 0 | C.Lambx5, J.Fergusonx3, J.Mingox1, G.Pickensx1 |
| 4 | DAL@HOU | Reed Blankenship | S | 6 | 6 | 80 | 0 | 2 | 0 | 0 | 0 | C.Lambx3, R.Flournoyx2, G.Pickensx1 |
| 4 | DAL@HOU | Calen Bullock | S | 5 | 5 | 57 | 0 | 0 | 0 | 0 | 0 | C.Lambx3, R.Flournoyx1, J.Fergusonx1 |
| 4 | DAL@HOU | Jake Hansen | LB | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | J.Williamsx3, C.Lambx1 |
| 4 | DAL@HOU | Jalen Pitre | S | 5 | 4 | 20 | 0 | 0 | 1 | 0 | 0 | C.Lambx3, J.Williamsx1, H.Luepkex1 |
| 4 | DAL@HOU | Kamari Ramsey | S | 2 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | C.Lambx2 |
| 4 | DAL@HOU | Derek Stingley Jr. | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | C.Lambx2 |
| 5 | HOU@TEN | Azeez Al-Shaair | LB | 5 | 4 | 42 | 0 | 0 | 1 | 0 | 0 | T.Spearsx2, C.Tatex1, E.Ayomanorx1, G.Helmx1 |
| 5 | HOU@TEN | Kamari Lassiter | CB | 5 | 4 | 39 | 0 | 0 | 1 | 0 | 0 | C.Dikex3, C.Ridleyx1, W.Robinsonx1 |
| 5 | HOU@TEN | Reed Blankenship | S | 6 | 5 | 33 | 0 | 0 | 1 | 0 | 0 | W.Robinsonx3, T.Spearsx2, C.Dikex1 |
| 5 | HOU@TEN | Jake Hansen | LB | 7 | 5 | 30 | 0 | 1 | 1 | 1 | 0 | T.Spearsx3, C.Ridleyx2, T.Pollardx1, D.Bellingerx1 |
| 5 | HOU@TEN | Kamari Ramsey | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1 |
| 5 | HOU@TEN | Jalen Pitre | S | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | T.Spearsx1 |
| 5 | HOU@TEN | Calen Bullock | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | C.Tatex1 |
| 6 | HOU@JAX | Kamari Lassiter | CB | 6 | 5 | 61 | 0 | 1 | 1 | 0 | 0 | P.Washingtonx4, N.Boerkircherx1, B.Strangex1 |
| 6 | HOU@JAX | Calen Bullock | S | 4 | 2 | 52 | 0 | 2 | 1 | 1 | 0 | B.Strangex2, J.Meyersx2 |
| 6 | HOU@JAX | Derek Stingley Jr. | CB | 6 | 5 | 51 | 0 | 0 | 1 | 0 | 0 | B.Strangex2, J.Meyersx2, P.Washingtonx1, B.Tutenx1 |
| 6 | HOU@JAX | Tremon Smith | CB | 4 | 2 | 26 | 0 | 0 | 2 | 0 | 0 | T.Hunterx2, P.Washingtonx1, J.Meyersx1 |
| 6 | HOU@JAX | Azeez Al-Shaair | LB | 2 | 1 | 26 | 0 | 1 | 1 | 0 | 0 | J.Meyersx1, T.Hunterx1 |
| 6 | HOU@JAX | Reed Blankenship | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1 |
| 6 | HOU@JAX | M.J. Stewart | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | B.Tutenx1 |
| 7 | NYG@HOU | Kamari Lassiter | CB | 3 | 3 | 93 | 0 | 2 | 0 | 0 | 0 | M.Nabersx1, M.Fieldsx1, D.Mooneyx1 |
| 7 | NYG@HOU | M.J. Stewart | S | 8 | 7 | 56 | 0 | 1 | 1 | 0 | 0 | D.Singletaryx2, M.Nabersx2, T.Tracyx1, T.Fidonex1, D.Mooneyx1, I.Likelyx1 |
| 7 | NYG@HOU | Derek Stingley Jr. | CB | 3 | 3 | 37 | 0 | 1 | 0 | 0 | 0 | M.Nabersx2, D.Singletaryx1 |
| 7 | NYG@HOU | Calen Bullock | S | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | M.Nabersx1, M.Fieldsx1 |
| 7 | NYG@HOU | Azeez Al-Shaair | LB | 3 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | M.Nabersx1, I.Likelyx1, M.Fieldsx1 |
| 7 | NYG@HOU | Tremon Smith | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | M.Fieldsx1 |

## Who beat them each week

**Wk1 BUF@HOU** (vs BUF offense, 334 rec yds allowed; 24% of targets unattributed)
- Top receivers: D.Kincaid (TE1, intermediate (aDOT 8-13)) 5/6 130y; D.Moore (WR3+, deep (aDOT 13+)) 5/8 100y 1TD; K.Shakir (WR1, short/YAC (aDOT <8)) 4/6 40y; J.Palmer (WR3+, deep (aDOT 13+)) 1/2 34y 1TD
- 20+ catches: D.Kincaid(TE1) 38y deep_right - D.Stingley [tackler]; D.Moore(WR3+) 43y deep_right TD - no tackler named [unattributed]; D.Kincaid(TE1) 40y deep_right - C.Bullock [tackler]; D.Kincaid(TE1) 35y short_right - J.Pitre [tackler]; J.Palmer(WR3+) 34y deep_middle TD - no tackler named [unattributed]
- 15+ runs: J.Allen(QB) 21y rush right end

**Wk2 CIN@HOU** (vs CIN offense, 207 rec yds allowed; 32% of targets unattributed)
- Top receivers: T.Higgins (WR1, deep (aDOT 13+)) 5/10 95y; J.Chase (WR2, intermediate (aDOT 8-13)) 7/9 75y 2TD; S.Perine (RB, short/YAC (aDOT <8)) 1/1 16y; A.Iosivas (WR3+, short/YAC (aDOT <8)) 1/1 7y
- 20+ catches: T.Higgins(WR1) 21y short_middle - R.Blankenship [tackler]; T.Higgins(WR1) 23y short_middle - A.Al-Shaair [tackler]; J.Chase(WR2) 32y deep_right TD - no tackler named [unattributed]; T.Higgins(WR1) 23y deep_right - D.Stingley [tackler]

**Wk3 HOU@IND** (vs IND offense, 235 rec yds allowed; 23% of targets unattributed)
- Top receivers: J.Downs (WR1, intermediate (aDOT 8-13)) 5/11 77y; K.Allen (WR2, short/YAC (aDOT <8)) 6/9 63y 1TD; T.Warren (TE1, short/YAC (aDOT <8)) 9/10 55y; L.Treadwell (WR3+, intermediate (aDOT 8-13)) 1/1 20y
- 20+ catches: J.Downs(WR1) 24y short_right - A.Al-Shaair [tackler]; K.Allen(WR2) 20y short_middle - R.Blankenship [tackler]; K.Allen(WR2) 26y deep_right - A.Al-Shaair [tackler]; L.Treadwell(WR3+) 20y deep_middle - C.Bullock [tackler]

**Wk4 DAL@HOU** (vs DAL offense, 335 rec yds allowed; 14% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 17/21 189y 1TD; G.Pickens (WR2, intermediate (aDOT 8-13)) 2/3 75y; R.Flournoy (WR3+, short/YAC (aDOT <8)) 4/5 37y; J.Williams (RB, short/YAC (aDOT <8)) 5/5 21y
- 20+ catches: C.Lamb(WR1) 30y deep_left - K.Lassiter [tackler]; G.Pickens(WR2) 53y deep_middle - K.Lassiter [tackler]; C.Lamb(WR1) 21y short_left - R.Blankenship [tackler]; G.Pickens(WR2) 22y deep_left - R.Blankenship [tackler]

**Wk5 HOU@TEN** (vs TEN offense, 170 rec yds allowed; 20% of targets unattributed)
- Top receivers: W.Robinson (WR2, short/YAC (aDOT <8)) 6/7 53y; C.Ridley (WR3+, intermediate (aDOT 8-13)) 2/3 33y; C.Dike (WR3+, intermediate (aDOT 8-13)) 3/4 28y; T.Spears (RB, short/YAC (aDOT <8)) 9/9 28y
- 20+ catches: C.Ridley(WR3+) 23y short_middle - J.Hansen [tackler]

**Wk6 HOU@JAX** (vs JAX offense, 306 rec yds allowed; 32% of targets unattributed)
- Top receivers: J.Meyers (WR2, intermediate (aDOT 8-13)) 5/10 83y; P.Washington (WR1, intermediate (aDOT 8-13)) 4/11 64y; T.Hunter (WR3+, short/YAC (aDOT <8)) 4/4 59y 1TD; B.Tuten (RB, short/YAC (aDOT <8)) 4/4 48y 2TD
- 20+ catches: B.Strange(TE1) 24y deep_left - C.Bullock [tackler]; P.Washington(WR1) 27y deep_left - K.Lassiter [tackler]; B.Tuten(RB) 27y short_right TD - no tackler named [unattributed]; J.Meyers(WR2) 22y short_middle - H.To'oTo'o [tackler]; J.Meyers(WR2) 28y deep_left - C.Bullock [tackler]; T.Hunter(WR3+) 26y short_middle - A.Al-Shaair [tackler]

**Wk7 NYG@HOU** (vs NYG offense, 252 rec yds allowed; 19% of targets unattributed)
- Top receivers: M.Nabers (WR1, intermediate (aDOT 8-13)) 7/9 111y; M.Fields (WR2, deep (aDOT 13+)) 4/5 83y; T.Fidone (TE2+, deep (aDOT 13+)) 1/1 29y; D.Singletary (RB, short/YAC (aDOT <8)) 3/3 14y
- 20+ catches: M.Nabers(WR1) 42y deep_right - K.Lassiter [tackler]; M.Fields(WR2) 47y short_right - K.Lassiter [tackler]; T.Fidone(TE2+) 29y deep_left - M.Stewart [tackler]; M.Nabers(WR1) 27y deep_left - D.Stingley [tackler]; M.Fields(WR2) 20y deep_right - C.Bullock [tackler]
- 15+ runs: C.Skattebo(RB) 19y rush right end; C.Skattebo(RB) 16y rush right guard; C.Skattebo(RB) 42y rush middle; D.Singletary(RB) 30y rush middle

