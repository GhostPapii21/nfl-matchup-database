# ATL DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 ATL@PIT, wk2 CAR@ATL, wk3 ATL@GB, wk4 ATL@NO, wk5 BAL@ATL, wk6 CHI@ATL, wk7 SF@ATL, wk8 ATL@TB). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 21.9% / Zone 70.3% | MOF closed 59.5% / MOF open 34.3% | Blitz 21.9% | Light box 44.3% / Heavy box 26.7% | Sub package 75.0% | Sharp YPT allowed WR 8.1, TE 7.2, RB 4.3, Outside 9.4, Slot 6.5

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- nothing flagged

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 61 | 43 | 260 | 3 | 1 | 4.26 | 7.60 | 32.50 | 5.61 | -1.35 |
| TE1 | 48 | 36 | 345 | 4 | 3 | 7.19 | 6 | 43.10 | 7.39 | -0.20 |
| TE2+ | 14 | 11 | 94 | 0 | 0 | 6.71 | 1.80 | 11.80 | 6.71 | 0 |
| WR1 | 61 | 38 | 505 | 1 | 9 | 8.28 | 7.60 | 63.10 | 8.16 | 0.12 |
| WR2 | 39 | 29 | 329 | 2 | 5 | 8.44 | 4.90 | 41.10 | 8.20 | 0.24 |
| WR3+ | 51 | 29 | 367 | 1 | 5 | 7.20 | 6.40 | 45.90 | 7.67 | -0.47 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 28 | 20 | 150 | 2 | 1 | 5.36 | 5.61 | -0.25 |
| TE1 | 24 | 18 | 181 | 1 | 2 | 7.54 | 7.39 | 0.15 |
| TE2+ | 5 | 5 | 43 | 0 | 0 | 8.60 | 6.71 | 1.89 |
| WR1 | 17 | 16 | 148 | 0 | 2 | 8.71 | 8.16 | 0.55 |
| WR2 | 11 | 8 | 113 | 0 | 2 | 10.27 | 8.20 | 2.07 |
| WR3+ | 22 | 14 | 159 | 1 | 1 | 7.23 | 7.67 | -0.44 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 62 | 48 | 252 | 1 | 0 | 4.06 | 4.58 | -0.52 |
| short_1-9 | 126 | 94 | 749 | 7 | 4 | 5.94 | 6.23 | -0.29 |
| inter_10-19 | 49 | 34 | 569 | 3 | 9 | 11.61 | 10.17 | 1.44 |
| deep_20+ | 36 | 10 | 330 | 0 | 10 | 9.17 | 12.32 | -3.15 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 27 | 7 | 202 | 0 | 6 | 7.48 | 11.28 | -3.80 |
| deep_middle | 8 | 6 | 173 | 0 | 5 | 21.62 | 14.90 | 6.72 |
| deep_right | 20 | 8 | 196 | 0 | 5 | 9.80 | 11.85 | -2.05 |
| short_left | 87 | 73 | 551 | 5 | 5 | 6.33 | 6.08 | 0.25 |
| short_middle | 32 | 22 | 227 | 2 | 1 | 7.09 | 7.43 | -0.34 |
| short_right | 99 | 70 | 551 | 4 | 1 | 5.57 | 5.95 | -0.38 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 56 | 33 | 486 | 3 | 9 | 8.68 | 8.94 | -0.26 |
| intermediate (aDOT 8-13) | 88 | 60 | 659 | 4 | 8 | 7.49 | 7.96 | -0.47 |
| short/YAC (aDOT <8) | 130 | 93 | 755 | 4 | 6 | 5.81 | 6.47 | -0.66 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 3, 'WR': 19} (23 total, 2.9/g)
- Pass 20+ by depth/direction: {'deep_left': 6, 'deep_middle': 5, 'deep_right': 5, 'short_left': 5, 'short_middle': 1, 'short_right': 1}
- Rush 15+ by position: {'QB': 1, 'RB': 9} (10 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 17 | 57 | 1 | 3.35 | 7.10 |
| RB | 192 | 884 | 9 | 4.60 | 110.50 |
| WR | 3 | 18 | 0 | 6 | 2.20 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C.J. Henderson | CB | 6 | 75 | 31 | 5.20 | 23 | 260 | 43.30 | 8.39 | 0 | 4 | 8 | 0 | 0 |
| Mike Hughes | CB | 8 | 72.50 | 22 | 2.80 | 17 | 249 | 31.10 | 11.32 | 0 | 3 | 5 | 0 | 0 |
| A.J. Terrell | CB | 3 | 75 | 9 | 3 | 6 | 86 | 28.70 | 9.56 | 0 | 1 | 3 | 0 | 0 |
| Billy Bowman Jr. | CB | 4 | 47 | 7 | 1.80 | 5 | 66 | 16.50 | 9.43 | 0 | 2 | 2 | 0 | 0 |
| Avieon Terrell | CB | 3 | 49.70 | 6 | 2 | 6 | 47 | 15.70 | 7.83 | 0 | 0 | 0 | 0 | 0 |
| Kendal Daniels | LB | 7 | 66.10 | 22 | 3.10 | 20 | 138 | 19.70 | 6.27 | 0 | 1 | 1 | 1 | 0 |
| Divine Deablo | LB | 6 | 82.50 | 12 | 2 | 11 | 103 | 17.20 | 8.58 | 0 | 1 | 1 | 0 | 0 |
| Harold Perkins Jr. | LB | 6 | 56.10 | 16 | 2.70 | 15 | 87 | 14.50 | 5.44 | 0 | 1 | 1 | 0 | 0 |
| Xavier Watts | S | 7 | 98.20 | 25 | 3.60 | 23 | 294 | 42 | 11.76 | 0 | 5 | 1 | 1 | 0 |
| Jessie Bates | S | 7 | 96.40 | 23 | 3.30 | 19 | 203 | 29 | 8.83 | 0 | 2 | 3 | 1 | 0 |
| Sydney Brown | S | 5 | 34.40 | 12 | 2.40 | 11 | 117 | 23.40 | 9.75 | 0 | 2 | 1 | 0 | 0 |
| DeMarcco Hellams | S | 1 | 7.30 | 2 | 2 | 1 | -1 | -1 | -0.50 | 0 | 0 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **C.J. Henderson** (CB): WR3+:9t/80y, WR2:8t/79y, WR1:8t/55y, TE1:2t/31y, TE2+:1t/9y, RB:3t/6y | 20+: wk1 M.Pittman(WR3+) 28 deep_left; wk2 T.McMillan(WR1) 28 deep_left; wk3 C.Watson(WR2) 34 deep_left; wk4 J.Johnson(TE1) 23 deep_right
- **Mike Hughes** (CB): WR3+:7t/90y, WR1:6t/86y, WR2:4t/48y, TE1:2t/16y, RB:2t/8y, TE2+:1t/1y | 20+: wk2 X.Legette(WR3+) 55 deep_middle; wk3 M.Golden(WR1) 45 deep_right; wk6 R.Odunze(WR2) 23 deep_middle
- **A.J. Terrell** (CB): WR1:5t/51y, RB:2t/20y, WR3+:2t/15y | 20+: wk2 T.McMillan(WR1) 26 deep_right
- **Billy Bowman Jr.** (CB): WR1:3t/43y, TE1:1t/16y, RB:2t/7y, WR3+:1t/0y | 20+: wk3 M.Golden(WR1) 20 short_left; wk4 C.Olave(WR1) 23 deep_left
- **Avieon Terrell** (CB): WR1:2t/20y, WR2:1t/12y, RB:2t/11y, WR3+:1t/4y
- **Kendal Daniels** (LB): WR3+:5t/45y, RB:7t/34y, TE1:5t/22y, TE2+:3t/22y, WR2:1t/14y, WR1:1t/1y | 20+: wk1 M.Pittman(WR3+) 21 short_left
- **Divine Deablo** (LB): WR1:4t/32y, WR3+:2t/20y, RB:3t/19y, TE2+:1t/17y, TE1:2t/15y | 20+: wk1 R.Wilson(WR3+) 20 deep_middle
- **Harold Perkins Jr.** (LB): RB:8t/43y, WR1:3t/20y, WR2:1t/14y, TE1:4t/10y | 20+: wk7 C.McCaffrey(RB) 24 short_left
- **Xavier Watts** (S): WR1:7t/102y, WR2:6t/79y, WR3+:2t/45y, TE1:6t/40y, RB:2t/24y, TE2+:2t/4y | 20+: wk2 T.McMillan(WR1) 27 deep_left; wk3 C.Watson(WR2) 22 deep_middle; wk4 C.Olave(WR1) 44 deep_left; wk5 R.Bateman(WR2) 20 short_left; wk7 J.Watkins(WR3+) 35 deep_middle
- **Jessie Bates** (S): TE1:10t/100y, TE2+:3t/38y, RB:3t/21y, WR1:2t/20y, WR3+:3t/13y, WR2:2t/11y | 20+: wk7 G.Kittle(TE1) 20 short_middle; wk7 G.Kittle(TE1) 21 short_left
- **Sydney Brown** (S): WR1:3t/54y, WR3+:4t/38y, TE1:1t/9y, RB:1t/8y, WR2:2t/5y, TE2+:1t/3y | 20+: wk6 L.Burden(WR1) 25 short_right; wk6 L.Burden(WR1) 22 deep_right
- **DeMarcco Hellams** (S): WR1:1t/0y, RB:1t/-1y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ATL@PIT | Jessie Bates | S | 3 | 3 | 35 | 0 | 0 | 0 | 0 | 0 | P.Freiermuthx1, R.Wilsonx1, D.Washingtonx1 |
| 1 | ATL@PIT | Kendal Daniels | LB | 3 | 3 | 30 | 0 | 1 | 0 | 0 | 0 | M.Pittmanx1, P.Freiermuthx1, J.Warrenx1 |
| 1 | ATL@PIT | A.J. Terrell | CB | 4 | 3 | 29 | 0 | 0 | 1 | 0 | 0 | D.Metcalfx3, J.Warrenx1 |
| 1 | ATL@PIT | C.J. Henderson | CB | 2 | 1 | 28 | 0 | 1 | 1 | 0 | 0 | M.Pittmanx1, D.Metcalfx1 |
| 1 | ATL@PIT | Xavier Watts | S | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | D.Metcalfx1, J.Warrenx1 |
| 1 | ATL@PIT | Sydney Brown | S | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | P.Freiermuthx1, D.Washingtonx1, M.Pittmanx1 |
| 1 | ATL@PIT | Divine Deablo | LB | 2 | 2 | 20 | 0 | 1 | 0 | 0 | 0 | J.Warrenx1, R.Wilsonx1 |
| 1 | ATL@PIT | Mike Hughes | CB | 4 | 2 | 7 | 0 | 0 | 2 | 0 | 0 | D.Metcalfx2, J.Warrenx1, R.Wilsonx1 |
| 1 | ATL@PIT | Avieon Terrell | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | R.Dowdlex1 |
| 1 | ATL@PIT | Harold Perkins Jr. | LB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | R.Dowdlex1 |
| 2 | CAR@ATL | Mike Hughes | CB | 2 | 2 | 67 | 0 | 1 | 0 | 0 | 0 | T.McMillanx1, X.Legettex1 |
| 2 | CAR@ATL | Xavier Watts | S | 4 | 4 | 43 | 0 | 1 | 0 | 0 | 0 | J.Cokerx2, T.McMillanx1, T.Tremblex1 |
| 2 | CAR@ATL | C.J. Henderson | CB | 5 | 4 | 35 | 0 | 1 | 1 | 0 | 0 | J.Cokerx2, X.Legettex1, J.Brooksx1, T.McMillanx1 |
| 2 | CAR@ATL | A.J. Terrell | CB | 2 | 1 | 26 | 0 | 1 | 1 | 0 | 0 | T.McMillanx2 |
| 2 | CAR@ATL | Kendal Daniels | LB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | M.Evansx1 |
| 2 | CAR@ATL | Avieon Terrell | CB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | J.Cokerx1 |
| 2 | CAR@ATL | Jessie Bates | S | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | J.Cokerx2 |
| 2 | CAR@ATL | Divine Deablo | LB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | T.McMillanx1 |
| 3 | ATL@GB | Mike Hughes | CB | 5 | 5 | 78 | 0 | 1 | 0 | 0 | 0 | M.Goldenx2, M.Lloydx1, C.Watsonx1, J.Sturdivantx1 |
| 3 | ATL@GB | C.J. Henderson | CB | 9 | 6 | 74 | 0 | 1 | 3 | 0 | 0 | C.Watsonx4, M.Goldenx2, J.Sturdivantx2, T.Kraftx1 |
| 3 | ATL@GB | Xavier Watts | S | 4 | 3 | 38 | 0 | 1 | 0 | 1 | 0 | T.Kraftx1, C.Watsonx1, S.Moorex1, J.Smithx1 |
| 3 | ATL@GB | Jessie Bates | S | 4 | 3 | 31 | 0 | 0 | 1 | 0 | 0 | T.Kraftx1, S.Moorex1, K.Johnsonx1, J.Smithx1 |
| 3 | ATL@GB | Billy Bowman Jr. | CB | 3 | 1 | 20 | 0 | 1 | 2 | 0 | 0 | M.Goldenx2, S.Moorex1 |
| 3 | ATL@GB | Divine Deablo | LB | 2 | 1 | 12 | 0 | 0 | 1 | 0 | 0 | S.Moorex1, M.Goldenx1 |
| 3 | ATL@GB | Sydney Brown | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | S.Moorex1 |
| 3 | ATL@GB | Harold Perkins Jr. | LB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | T.Kraftx1, C.Brooksx1 |
| 3 | ATL@GB | Kendal Daniels | LB | 2 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | M.Lloydx1, J.Smithx1 |
| 4 | ATL@NO | Xavier Watts | S | 6 | 6 | 96 | 0 | 1 | 0 | 0 | 0 | J.Johnsonx4, C.Olavex1, D.Velex1 |
| 4 | ATL@NO | C.J. Henderson | CB | 10 | 9 | 90 | 0 | 1 | 1 | 0 | 0 | C.Olavex4, A.Kamarax2, D.Velex2, J.Johnsonx1, B.Lancex1 |
| 4 | ATL@NO | Billy Bowman Jr. | CB | 2 | 2 | 28 | 0 | 1 | 0 | 0 | 0 | A.Kamarax1, C.Olavex1 |
| 4 | ATL@NO | Mike Hughes | CB | 3 | 2 | 21 | 0 | 0 | 1 | 0 | 0 | C.Olavex1, B.Lancex1, D.Velex1 |
| 4 | ATL@NO | Harold Perkins Jr. | LB | 5 | 4 | 20 | 0 | 0 | 1 | 0 | 0 | K.Millerx2, C.Olavex2, J.Johnsonx1 |
| 4 | ATL@NO | Divine Deablo | LB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | A.Kamarax2 |
| 4 | ATL@NO | Kendal Daniels | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | C.Donaldsonx1 |
| 4 | ATL@NO | Jessie Bates | S | 2 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | J.Johnsonx2 |
| 4 | ATL@NO | Sydney Brown | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Velex1 |
| 4 | ATL@NO | DeMarcco Hellams | S | 2 | 1 | -1 | 0 | 0 | 1 | 0 | 0 | C.Olavex1, C.Donaldsonx1 |
| 5 | BAL@ATL | Xavier Watts | S | 6 | 5 | 49 | 0 | 1 | 1 | 0 | 0 | Z.Flowersx3, R.Batemanx2, M.Andrewsx1 |
| 5 | BAL@ATL | Divine Deablo | LB | 4 | 4 | 38 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx2, M.Andrewsx1, J.Cuevasx1 |
| 5 | BAL@ATL | Jessie Bates | S | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx1, M.Andrewsx1 |
| 5 | BAL@ATL | Mike Hughes | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | R.Batemanx1 |
| 5 | BAL@ATL | C.J. Henderson | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Cuevasx1 |
| 5 | BAL@ATL | Sydney Brown | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | R.Batemanx1 |
| 5 | BAL@ATL | Kendal Daniels | LB | 3 | 2 | 3 | 0 | 0 | 1 | 0 | 0 | D.Henryx1, D.Walkerx1, Z.Flowersx1 |
| 5 | BAL@ATL | Harold Perkins Jr. | LB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | M.Andrewsx1 |
| 5 | BAL@ATL | Billy Bowman Jr. | CB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | J.Hillx1 |
| 6 | CHI@ATL | Sydney Brown | S | 6 | 6 | 82 | 0 | 2 | 0 | 0 | 0 | L.Burdenx3, D.Swiftx1, K.Raymondx1, Z.Thomasx1 |
| 6 | CHI@ATL | Mike Hughes | CB | 4 | 4 | 54 | 0 | 1 | 0 | 0 | 0 | C.Lovelandx1, R.Odunzex1, C.Kmetx1, Z.Thomasx1 |
| 6 | CHI@ATL | Avieon Terrell | CB | 4 | 4 | 31 | 0 | 0 | 0 | 0 | 0 | L.Burdenx2, D.Swiftx1, Z.Thomasx1 |
| 6 | CHI@ATL | Kendal Daniels | LB | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | C.Kmetx1, D.Swiftx1, R.Odunzex1, C.Lovelandx1 |
| 6 | CHI@ATL | Harold Perkins Jr. | LB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | R.Odunzex1, L.Burdenx1 |
| 6 | CHI@ATL | Billy Bowman Jr. | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | C.Lovelandx1 |
| 6 | CHI@ATL | Jessie Bates | S | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | D.Swiftx1, L.Burdenx1 |
| 6 | CHI@ATL | Divine Deablo | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | C.Lovelandx1 |
| 6 | CHI@ATL | Xavier Watts | S | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1 |
| 7 | SF@ATL | Jessie Bates | S | 8 | 6 | 88 | 0 | 2 | 1 | 1 | 0 | G.Kittlex5, L.Farrellx1, J.Cowingx1, C.McCaffreyx1 |
| 7 | SF@ATL | Kendal Daniels | LB | 8 | 7 | 56 | 0 | 0 | 0 | 1 | 0 | G.Kittlex3, J.Jamesx1, K.Juszczykx1, J.Watkinsx1, J.Cowingx1, B.Cooksx1 |
| 7 | SF@ATL | Xavier Watts | S | 2 | 2 | 41 | 0 | 1 | 0 | 0 | 0 | J.Watkinsx1, C.McCaffreyx1 |
| 7 | SF@ATL | A.J. Terrell | CB | 3 | 2 | 31 | 0 | 0 | 1 | 0 | 0 | J.Watkinsx2, C.McCaffreyx1 |
| 7 | SF@ATL | Harold Perkins Jr. | LB | 5 | 5 | 31 | 0 | 1 | 0 | 0 | 0 | C.McCaffreyx2, K.Juszczykx1, G.Kittlex1, K.Blackx1 |
| 7 | SF@ATL | C.J. Henderson | CB | 4 | 2 | 24 | 0 | 0 | 2 | 0 | 0 | J.Watkinsx2, J.Cowingx2 |
| 7 | SF@ATL | Mike Hughes | CB | 2 | 1 | 11 | 0 | 0 | 1 | 0 | 0 | J.Cowingx1, G.Kittlex1 |
| 8 | ATL@TB | Mike Hughes | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.Hurstx1 |

## Who beat them each week

**Wk1 ATL@PIT** (vs PIT offense, 221 rec yds allowed; 27% of targets unattributed)
- Top receivers: M.Pittman (WR3+, intermediate (aDOT 8-13)) 3/3 58y; P.Freiermuth (TE1, intermediate (aDOT 8-13)) 5/5 46y 1TD; D.Metcalf (WR1, intermediate (aDOT 8-13)) 4/10 40y; J.Warren (RB, short/YAC (aDOT <8)) 5/6 27y
- 20+ catches: M.Pittman(WR3+) 21y short_left - K.Daniels [tackler]; R.Wilson(WR3+) 20y deep_middle - D.Deablo [tackler]; M.Pittman(WR3+) 28y deep_left - C.Henderson [tackler]
- 15+ runs: J.Warren(RB) 17y rush right tackle

**Wk2 CAR@ATL** (vs CAR offense, 287 rec yds allowed; 31% of targets unattributed)
- Top receivers: T.McMillan (WR1, intermediate (aDOT 8-13)) 5/10 101y; J.Coker (WR2, intermediate (aDOT 8-13)) 8/9 66y; X.Legette (WR3+, deep (aDOT 13+)) 2/4 64y; D.Waller (TE1, intermediate (aDOT 8-13)) 3/3 33y 2TD
- 20+ catches: T.McMillan(WR1) 26y deep_right - Aj.Terrell [tackler]; T.McMillan(WR1) 27y deep_left - X.Watts [tackler]; J.Coker(WR2) 25y deep_right - no tackler named [unattributed]; X.Legette(WR3+) 55y deep_middle - M.Hughes [tackler]; T.McMillan(WR1) 28y deep_left - C.Henderson [tackler]

**Wk3 ATL@GB** (vs GB offense, 312 rec yds allowed; 33% of targets unattributed)
- Top receivers: M.Golden (WR1, deep (aDOT 13+)) 5/12 100y 1TD; C.Watson (WR2, deep (aDOT 13+)) 7/10 96y 1TD; S.Moore (WR3+, short/YAC (aDOT <8)) 3/7 31y; T.Kraft (TE1, short/YAC (aDOT <8)) 4/8 26y
- 20+ catches: M.Golden(WR1) 45y deep_right - M.Hughes [tackler]; C.Watson(WR2) 22y deep_middle - X.Watts [tackler]; C.Watson(WR2) 34y deep_left - C.Henderson [tackler]; M.Golden(WR1) 20y short_left - B.Bowman [tackler]

**Wk4 ATL@NO** (vs NO offense, 286 rec yds allowed; 23% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 8/12 116y; J.Johnson (TE1, short/YAC (aDOT <8)) 6/8 59y; D.Vele (WR2, intermediate (aDOT 8-13)) 6/9 54y 1TD; A.Kamara (RB, short/YAC (aDOT <8)) 5/7 35y
- 20+ catches: J.Johnson(TE1) 23y deep_right - C.Henderson [tackler]; C.Olave(WR1) 44y deep_left - X.Watts [tackler]; C.Olave(WR1) 23y deep_left - B.Bowman [tackler]

**Wk5 BAL@ATL** (vs BAL offense, 201 rec yds allowed; 28% of targets unattributed)
- Top receivers: R.Bateman (WR2, deep (aDOT 13+)) 5/6 62y; Z.Flowers (WR1, intermediate (aDOT 8-13)) 8/9 53y; M.Andrews (TE1, short/YAC (aDOT <8)) 4/7 28y; J.Cuevas (TE2+, short/YAC (aDOT <8)) 2/2 26y
- 20+ catches: R.Bateman(WR2) 20y short_left - X.Watts [tackler]
- 15+ runs: J.Hill(RB) 21y rush left tackle; T.Huntley(QB) 15y rush middle; J.Hill(RB) 47y rush middle

**Wk6 CHI@ATL** (vs CHI offense, 305 rec yds allowed; 9% of targets unattributed)
- Top receivers: L.Burden (WR1, short/YAC (aDOT <8)) 8/8 95y; C.Loveland (TE1, short/YAC (aDOT <8)) 6/7 65y 1TD; R.Odunze (WR2, deep (aDOT 13+)) 3/4 51y; D.Swift (RB, short/YAC (aDOT <8)) 4/5 26y
- 20+ catches: R.Odunze(WR2) 23y deep_middle - M.Hughes [tackler]; L.Burden(WR1) 25y short_right - S.Brown [tackler]; L.Burden(WR1) 22y deep_right - S.Brown [tackler]

**Wk7 SF@ATL** (vs SF offense, 288 rec yds allowed; 18% of targets unattributed)
- Top receivers: G.Kittle (TE1, short/YAC (aDOT <8)) 8/10 88y; C.McCaffrey (RB, short/YAC (aDOT <8)) 6/7 61y; J.Watkins (WR3+, deep (aDOT 13+)) 3/6 56y; J.Cowing (WR3+, intermediate (aDOT 8-13)) 3/5 38y
- 20+ catches: C.McCaffrey(RB) 24y short_left - H.Perkins [tackler]; G.Kittle(TE1) 20y short_middle - J.Bates [tackler]; J.Watkins(WR3+) 35y deep_middle - X.Watts [tackler]; G.Kittle(TE1) 21y short_left - J.Bates [tackler]
- 15+ runs: K.Black(RB) 15y rush right guard; K.Black(RB) 30y rush middle

**Wk8 ATL@TB** (vs TB offense, 0 rec yds allowed; 67% of targets unattributed)
- Top receivers: C.Godwin (WR2, short/YAC (aDOT <8)) 0/1 0y; K.Gainwell (RB, short/YAC (aDOT <8)) 0/1 0y; T.Hurst (WR3+, deep (aDOT 13+)) 0/1 0y
- 15+ runs: B.Irving(RB) 24y rush middle; K.Gainwell(RB) 20y rush left tackle; B.Irving(RB) 46y rush left end; K.Gainwell(RB) 28y rush left end

## Seed notes from defenders/ATL_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 9:55 Bucky Irving (RB) rush 24 — J.Bates; S.Ebukam [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q2 7:11 Kenny Gainwell (RB) rush 20 — A.Terrell [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 6:31 Bucky Irving (RB) rush 46 — C.Henderson [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 4:59 Kenny Gainwell (RB) rush 28 — K.Daniels; M.Smith [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Mike Hughes ← Chris Godwin Jr.: 1 tgt, 0 rec, 0 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 ATL@TB: Bucky Irving (RB-home-run zone runner) 27-170 1TD | shell 22/70, MOFC 60 | Rain (5.7mm) + TB lead → 56 rushes/3 passes; ATL run D 4.09 YPC, missed fits by Bates/Daniels/Henderson on 4 explosives (46y Henderson). Game-script RB rule spot. [confirmed-tackler]
- wk8 ATL@TB: Kenny Gainwell (RB-receiving/scat (used as volume back in rain)) 25-140 0TD; 0/1tgt 0y 0TD | shell 22/70, MOFC 60 | RB2 volume in rain run-fest (25 car); ATL edge contain failed (left/right end 28y, 20y). RB2 should be modeled when weather-flagged. [confirmed-tackler]

