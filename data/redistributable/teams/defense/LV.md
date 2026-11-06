# LV DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 MIA@LV, wk2 LV@LAC, wk3 LV@NO, wk4 KC@LV, wk5 LV@NE, wk6 BUF@LV, wk7 LAR@LV, wk8 LV@NYJ). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 21.4% / Zone 70.0% | MOF closed 47.2% / MOF open 47.2% | Blitz 22.4% | Light box 48.2% / Heavy box 29.1% | Sub package 78.0% | Sharp YPT allowed WR 9.0, TE 6.5, RB 8.3, Outside 9.0, Slot 10.2

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type RB: 7.76 YPT on 33 tgts (league 5.61, +2.15), 2 catches of 20+
- type WR3+: 10.73 YPT on 45 tgts (league 7.67, +3.06), 7 catches of 20+
- depth behind_los: 6.15 YPT on 53 tgts (league 4.58, +1.57), 2 catches of 20+
- depth/direction deep_left: 15.5 YPT on 24 tgts (league 11.28, +4.22), 9 catches of 20+
- receiver archetype deep (aDOT 13+): 10.98 YPT on 47 tgts (league 8.94, +2.04), 10 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 33 | 30 | 256 | 0 | 2 | 7.76 | 4.10 | 32 | 5.61 | 2.15 |
| TE1 | 33 | 27 | 222 | 4 | 3 | 6.73 | 4.10 | 27.80 | 7.39 | -0.66 |
| TE2+ | 36 | 28 | 224 | 4 | 1 | 6.22 | 4.50 | 28 | 6.71 | -0.49 |
| WR1 | 64 | 39 | 533 | 4 | 6 | 8.33 | 8 | 66.60 | 8.16 | 0.17 |
| WR2 | 31 | 17 | 288 | 2 | 5 | 9.29 | 3.90 | 36 | 8.20 | 1.09 |
| WR3+ | 45 | 25 | 483 | 4 | 7 | 10.73 | 5.60 | 60.40 | 7.67 | 3.06 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 16 | 16 | 155 | 0 | 2 | 9.69 | 5.61 | 4.08 |
| TE1 | 17 | 13 | 118 | 1 | 2 | 6.94 | 7.39 | -0.45 |
| TE2+ | 22 | 18 | 144 | 2 | 1 | 6.55 | 6.71 | -0.16 |
| WR1 | 33 | 22 | 250 | 4 | 2 | 7.58 | 8.16 | -0.58 |
| WR2 | 18 | 12 | 217 | 2 | 4 | 12.06 | 8.20 | 3.86 |
| WR3+ | 15 | 11 | 230 | 2 | 3 | 15.33 | 7.67 | 7.66 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 53 | 46 | 326 | 1 | 2 | 6.15 | 4.58 | 1.57 |
| short_1-9 | 86 | 70 | 588 | 10 | 2 | 6.84 | 6.23 | 0.61 |
| inter_10-19 | 56 | 34 | 524 | 5 | 4 | 9.36 | 10.17 | -0.81 |
| deep_20+ | 46 | 16 | 568 | 2 | 16 | 12.35 | 12.32 | 0.03 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 24 | 11 | 372 | 1 | 9 | 15.50 | 11.28 | 4.22 |
| deep_middle | 14 | 6 | 159 | 1 | 4 | 11.36 | 14.90 | -3.54 |
| deep_right | 25 | 10 | 261 | 1 | 6 | 10.44 | 11.85 | -1.41 |
| short_left | 74 | 55 | 478 | 7 | 2 | 6.46 | 6.08 | 0.38 |
| short_middle | 28 | 20 | 197 | 2 | 1 | 7.04 | 7.43 | -0.39 |
| short_right | 76 | 64 | 539 | 6 | 2 | 7.09 | 5.95 | 1.14 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 47 | 25 | 516 | 5 | 10 | 10.98 | 8.94 | 2.04 |
| intermediate (aDOT 8-13) | 82 | 49 | 674 | 3 | 8 | 8.22 | 7.96 | 0.26 |
| short/YAC (aDOT <8) | 113 | 92 | 816 | 10 | 6 | 7.22 | 6.47 | 0.75 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 2, 'TE': 4, 'WR': 18} (24 total, 3.0/g)
- Pass 20+ by depth/direction: {'deep_left': 9, 'deep_middle': 4, 'deep_right': 6, 'short_left': 2, 'short_middle': 1, 'short_right': 2}
- Rush 15+ by position: {'QB': 1, 'RB': 14} (15 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| DL | 1 | 0 | 0 | 0 | 0 |
| P | 1 | 12 | 0 | 12 | 1.50 |
| QB | 18 | 115 | 1 | 6.39 | 14.40 |
| RB | 195 | 1036 | 14 | 5.31 | 129.50 |
| WR | 4 | 19 | 0 | 4.75 | 2.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Eric Stokes | CB | 8 | 98 | 20 | 2.50 | 17 | 190 | 23.80 | 9.50 | 0 | 3 | 3 | 0 | 0 |
| Hezekiah Masses | CB | 7 | 54.40 | 19 | 2.70 | 12 | 149 | 21.30 | 7.84 | 0 | 1 | 4 | 3 | 0 |
| Darien Porter | CB | 4 | 49.20 | 15 | 3.80 | 10 | 148 | 37 | 9.87 | 0 | 2 | 5 | 0 | 0 |
| Taron Johnson | CB | 5 | 76.60 | 14 | 2.80 | 12 | 118 | 23.60 | 8.43 | 0 | 0 | 2 | 0 | 0 |
| Jermod McCoy | CB | 2 | 31.70 | 2 | 1 | 2 | 30 | 15 | 15 | 0 | 1 | 0 | 0 | 0 |
| Quay Walker | LB | 8 | 99.50 | 19 | 2.40 | 19 | 180 | 22.50 | 9.47 | 0 | 2 | 0 | 0 | 0 |
| Nakobe Dean | LB | 7 | 99.20 | 20 | 2.90 | 18 | 162 | 23.10 | 8.10 | 0 | 0 | 1 | 1 | 0 |
| Jeremy Chinn | S | 8 | 100 | 27 | 3.40 | 25 | 337 | 42.10 | 12.48 | 0 | 5 | 1 | 1 | 0 |
| Treydan Stukes | S | 5 | 92.30 | 19 | 3.80 | 16 | 308 | 61.60 | 16.21 | 0 | 6 | 2 | 1 | 0 |
| Isaiah Pola-Mao | S | 2 | 53.70 | 5 | 2.50 | 5 | 64 | 32 | 12.80 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Eric Stokes** (CB): WR1:9t/92y, WR3+:4t/31y, RB:1t/23y, WR2:1t/20y, TE2+:4t/18y, TE1:1t/6y | 20+: wk4 X.Worthy(WR1) 41 deep_middle; wk6 J.Cook(RB) 23 short_right; wk8 A.Mitchell(WR2) 20 deep_right
- **Hezekiah Masses** (CB): WR3+:7t/57y, WR1:5t/53y, WR2:1t/16y, TE1:2t/15y, RB:2t/8y, TE2+:2t/0y | 20+: wk4 T.Thornton(WR3+) 42 deep_left
- **Darien Porter** (CB): WR3+:1t/49y, TE2+:2t/38y, WR1:5t/31y, WR2:5t/15y, RB:1t/8y, TE1:1t/7y | 20+: wk5 E.Raridon(TE2+) 31 deep_left; wk5 K.Williams(WR3+) 49 deep_right
- **Taron Johnson** (CB): WR3+:3t/40y, WR1:5t/33y, TE1:3t/32y, TE2+:1t/13y, RB:1t/0y, WR2:1t/0y
- **Jermod McCoy** (CB): WR2:1t/22y, WR3+:1t/8y | 20+: wk8 A.Mitchell(WR2) 22 deep_left
- **Quay Walker** (LB): TE2+:7t/75y, WR3+:3t/50y, WR1:2t/24y, TE1:3t/21y, RB:4t/10y | 20+: wk1 C.Douglas(WR3+) 30 deep_middle; wk5 H.Henry(TE1) 26 short_right
- **Nakobe Dean** (LB): RB:11t/98y, WR2:2t/24y, WR3+:2t/20y, WR1:3t/20y, TE1:1t/0y, TE2+:1t/0y
- **Jeremy Chinn** (S): WR1:5t/107y, RB:5t/72y, WR2:4t/60y, WR3+:1t/37y, TE1:6t/36y, TE2+:6t/25y | 20+: wk1 M.Washington(WR1) 24 deep_middle; wk2 T.Harris(WR1) 53 deep_left; wk6 J.Palmer(WR3+) 37 deep_right; wk6 K.Coleman(WR2) 21 short_middle; wk6 J.Cook(RB) 26 short_left
- **Treydan Stukes** (S): WR3+:4t/97y, WR2:3t/83y, WR1:4t/79y, TE1:5t/22y, RB:2t/18y, TE2+:1t/9y | 20+: wk1 C.Douglas(WR3+) 25 deep_right; wk1 C.Bell(WR2) 25 deep_right; wk1 M.Washington(WR1) 30 deep_middle; wk4 T.Thornton(WR3+) 55 deep_left; wk8 G.Wilson(WR1) 31 deep_left; wk8 A.Mitchell(WR2) 47 deep_left
- **Isaiah Pola-Mao** (S): TE1:1t/22y, WR3+:1t/19y, WR1:2t/15y, TE2+:1t/8y | 20+: wk3 J.Johnson(TE1) 22 short_left

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MIA@LV | Treydan Stukes | S | 5 | 4 | 94 | 0 | 3 | 0 | 1 | 0 | C.Douglasx2, D.Achanex1, C.Bellx1, M.Washingtonx1 |
| 1 | MIA@LV | Quay Walker | LB | 3 | 3 | 47 | 0 | 1 | 0 | 0 | 0 | C.Douglasx2, D.Achanex1 |
| 1 | MIA@LV | Jeremy Chinn | S | 3 | 3 | 43 | 0 | 1 | 0 | 0 | 0 | D.Achanex1, G.Dulcichx1, M.Washingtonx1 |
| 1 | MIA@LV | Eric Stokes | CB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx1, C.Douglasx1 |
| 1 | MIA@LV | Darien Porter | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | M.Washingtonx1, C.Bellx1 |
| 1 | MIA@LV | Hezekiah Masses | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | K.Colemanx1 |
| 1 | MIA@LV | Taron Johnson | CB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | 0 | M.Washingtonx1 |
| 2 | LV@LAC | Jeremy Chinn | S | 2 | 2 | 68 | 0 | 1 | 0 | 0 | 0 | T.Harrisx1, K.Mitchellx1 |
| 2 | LV@LAC | Nakobe Dean | LB | 3 | 3 | 29 | 0 | 0 | 0 | 0 | 0 | Q.Johnstonx1, O.Hamptonx1, L.McConkeyx1 |
| 2 | LV@LAC | Isaiah Pola-Mao | S | 2 | 2 | 27 | 0 | 0 | 0 | 0 | 0 | L.McConkeyx1, C.Kolarx1 |
| 2 | LV@LAC | Taron Johnson | CB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | B.Thompsonx1, L.McConkeyx1 |
| 2 | LV@LAC | Quay Walker | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | D.Njokux1, C.Kolarx1 |
| 2 | LV@LAC | Eric Stokes | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | C.Kolarx1 |
| 2 | LV@LAC | Hezekiah Masses | CB | 3 | 1 | 3 | 0 | 0 | 0 | 2 | 0 | D.Njokux1, O.Hamptonx1, D.Davisx1 |
| 3 | LV@NO | Taron Johnson | CB | 6 | 5 | 60 | 0 | 0 | 1 | 0 | 0 | J.Johnsonx3, C.Olavex2, D.Velex1 |
| 3 | LV@NO | Hezekiah Masses | CB | 5 | 4 | 40 | 0 | 0 | 0 | 1 | 0 | C.Olavex3, A.Kamarax1, B.Lancex1 |
| 3 | LV@NO | Jeremy Chinn | S | 3 | 3 | 39 | 0 | 0 | 0 | 0 | 0 | D.Velex3 |
| 3 | LV@NO | Isaiah Pola-Mao | S | 3 | 3 | 37 | 0 | 1 | 0 | 0 | 0 | C.Olavex2, J.Johnsonx1 |
| 3 | LV@NO | Nakobe Dean | LB | 6 | 5 | 25 | 0 | 0 | 1 | 0 | 0 | C.Olavex2, K.Millerx2, T.Etiennex1, J.Johnsonx1 |
| 3 | LV@NO | Eric Stokes | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | N.Fantx1 |
| 3 | LV@NO | Quay Walker | LB | 1 | 1 | -4 | 0 | 0 | 0 | 0 | 0 | J.Johnsonx1 |
| 4 | KC@LV | Eric Stokes | CB | 5 | 4 | 67 | 0 | 1 | 1 | 0 | 0 | X.Worthyx3, T.Thorntonx1, J.Royalsx1 |
| 4 | KC@LV | Hezekiah Masses | CB | 6 | 4 | 64 | 0 | 1 | 2 | 0 | 0 | T.Thorntonx3, T.Kelcex2, X.Worthyx1 |
| 4 | KC@LV | Treydan Stukes | S | 1 | 1 | 55 | 0 | 1 | 0 | 0 | 0 | T.Thorntonx1 |
| 4 | KC@LV | Quay Walker | LB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | N.Grayx1, K.Walkerx1 |
| 4 | KC@LV | Nakobe Dean | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | E.Johnsonx1 |
| 4 | KC@LV | Jeremy Chinn | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | N.Grayx1 |
| 4 | KC@LV | Taron Johnson | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | X.Worthyx1 |
| 5 | LV@NE | Darien Porter | CB | 5 | 3 | 87 | 0 | 2 | 2 | 0 | 0 | R.Doubsx2, E.Raridonx2, K.Williamsx1 |
| 5 | LV@NE | Nakobe Dean | LB | 4 | 4 | 44 | 0 | 0 | 0 | 0 | 0 | R.Stevensonx2, E.Chismx1, C.Kinerx1 |
| 5 | LV@NE | Taron Johnson | CB | 4 | 4 | 34 | 0 | 0 | 0 | 0 | 0 | D.Douglasx1, E.Chismx1, E.Raridonx1, R.Stevensonx1 |
| 5 | LV@NE | Quay Walker | LB | 2 | 2 | 34 | 0 | 1 | 0 | 0 | 0 | H.Henryx1, K.Williamsx1 |
| 5 | LV@NE | Eric Stokes | CB | 2 | 2 | 29 | 0 | 0 | 0 | 0 | 0 | E.Chismx1, D.Douglasx1 |
| 5 | LV@NE | Treydan Stukes | S | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | E.Chismx1, T.Hendersonx1, H.Henryx1 |
| 5 | LV@NE | Hezekiah Masses | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | R.Doubsx1 |
| 5 | LV@NE | Jermod McCoy | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | E.Chismx1 |
| 5 | LV@NE | Jeremy Chinn | S | 3 | 2 | 6 | 0 | 0 | 1 | 0 | 0 | E.Raridonx2, H.Henryx1 |
| 6 | BUF@LV | Jeremy Chinn | S | 9 | 9 | 117 | 0 | 3 | 0 | 0 | 0 | D.Kincaidx3, T.Johnsonx2, J.Palmerx1, K.Colemanx1, D.Knoxx1, J.Cookx1 |
| 6 | BUF@LV | Eric Stokes | CB | 2 | 2 | 29 | 0 | 1 | 0 | 0 | 0 | J.Cookx1, K.Shakirx1 |
| 6 | BUF@LV | Treydan Stukes | S | 5 | 4 | 29 | 0 | 0 | 1 | 0 | 0 | D.Kincaidx3, K.Colemanx1, K.Shakirx1 |
| 6 | BUF@LV | Darien Porter | CB | 3 | 2 | 22 | 0 | 0 | 1 | 0 | 0 | K.Colemanx2, D.Kincaidx1 |
| 6 | BUF@LV | Quay Walker | LB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | K.Shakirx1 |
| 6 | BUF@LV | Nakobe Dean | LB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | R.Davisx1 |
| 7 | LAR@LV | Quay Walker | LB | 7 | 7 | 62 | 0 | 0 | 0 | 0 | 0 | C.Parkinsonx4, B.Corumx1, P.Nacuax1, T.Higbeex1 |
| 7 | LAR@LV | Darien Porter | CB | 5 | 5 | 39 | 0 | 0 | 0 | 0 | 0 | P.Nacuax4, K.Williamsx1 |
| 7 | LAR@LV | Hezekiah Masses | CB | 2 | 2 | 26 | 0 | 0 | 0 | 0 | 0 | P.Nacuax1, K.Mumpfieldx1 |
| 7 | LAR@LV | Jeremy Chinn | S | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | D.Allenx1, T.Higbeex1 |
| 7 | LAR@LV | Nakobe Dean | LB | 3 | 2 | 21 | 0 | 0 | 0 | 1 | 0 | P.Nacuax1, K.Williamsx1, C.Parkinsonx1 |
| 7 | LAR@LV | Eric Stokes | CB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | C.Parkinsonx1 |
| 8 | LV@NYJ | Treydan Stukes | S | 5 | 4 | 102 | 0 | 2 | 1 | 0 | 0 | G.Wilsonx2, K.Sadiqx1, M.Taylorx1, A.Mitchellx1 |
| 8 | LV@NYJ | Jeremy Chinn | S | 4 | 3 | 37 | 0 | 0 | 0 | 1 | 0 | G.Wilsonx3, M.Taylorx1 |
| 8 | LV@NYJ | Eric Stokes | CB | 6 | 4 | 30 | 0 | 1 | 2 | 0 | 0 | G.Wilsonx4, A.Mitchellx1, M.Taylorx1 |
| 8 | LV@NYJ | Nakobe Dean | LB | 2 | 2 | 28 | 0 | 0 | 0 | 0 | 0 | A.Mitchellx1, B.Allenx1 |
| 8 | LV@NYJ | Jermod McCoy | CB | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | A.Mitchellx1 |
| 8 | LV@NYJ | Hezekiah Masses | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | M.Taylorx1 |
| 8 | LV@NYJ | Quay Walker | LB | 1 | 1 | -5 | 0 | 0 | 0 | 0 | 0 | B.Allenx1 |

## Who beat them each week

**Wk1 MIA@LV** (vs MIA offense, 220 rec yds allowed; 26% of targets unattributed)
- Top receivers: C.Douglas (WR3+, intermediate (aDOT 8-13)) 5/7 94y; M.Washington (WR1, intermediate (aDOT 8-13)) 3/8 53y; D.Achane (RB, short/YAC (aDOT <8)) 4/5 30y; C.Bell (WR2, deep (aDOT 13+)) 1/2 25y
- 20+ catches: C.Douglas(WR3+) 25y deep_right - T.Stukes [tackler]; C.Douglas(WR3+) 30y deep_middle - Q.Walker [tackler]; C.Bell(WR2) 25y deep_right - T.Stukes [tackler]; M.Washington(WR1) 30y deep_middle - T.Stukes [tackler]; M.Washington(WR1) 24y deep_middle - J.Chinn [tackler]

**Wk2 LV@LAC** (vs LAC offense, 192 rec yds allowed; 35% of targets unattributed)
- Top receivers: T.Harris (WR1, intermediate (aDOT 8-13)) 1/3 53y; L.McConkey (WR3+, intermediate (aDOT 8-13)) 3/3 35y; O.Hampton (RB, short/YAC (aDOT <8)) 2/2 21y; C.Kolar (TE2+, short/YAC (aDOT <8)) 3/3 21y
- 20+ catches: T.Harris(WR1) 53y deep_left - J.Chinn [tackler]
- 15+ runs: O.Hampton(RB) 17y rush middle

**Wk3 LV@NO** (vs NO offense, 255 rec yds allowed; 32% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 9/13 107y; J.Johnson (TE1, short/YAC (aDOT <8)) 8/8 53y 2TD; D.Vele (WR2, intermediate (aDOT 8-13)) 3/6 39y; N.Fant (TE2+, short/YAC (aDOT <8)) 4/4 33y 2TD
- 20+ catches: J.Johnson(TE1) 22y short_left - I.Pola-Mao [tackler]
- 15+ runs: T.Shough(QB) 36y rush right end; T.Etienne(RB) 16y rush right tackle

**Wk4 KC@LV** (vs KC offense, 225 rec yds allowed; 36% of targets unattributed)
- Top receivers: T.Thornton (WR3+, deep (aDOT 13+)) 5/8 111y 2TD; X.Worthy (WR1, intermediate (aDOT 8-13)) 4/7 70y; N.Gray (TE2+, short/YAC (aDOT <8)) 2/3 17y; T.Kelce (TE1, short/YAC (aDOT <8)) 2/4 15y
- 20+ catches: X.Worthy(WR1) 41y deep_middle - E.Stokes [tackler]; T.Thornton(WR3+) 42y deep_left - H.Masses [tackler]; T.Thornton(WR3+) 55y deep_left - T.Stukes [tackler]
- 15+ runs: K.Walker(RB) 21y rush left tackle; K.Walker(RB) 76y rush right guard; K.Walker(RB) 22y rush right end

**Wk5 LV@NE** (vs NE offense, 374 rec yds allowed; 19% of targets unattributed)
- Top receivers: K.Williams (WR3+, deep (aDOT 13+)) 3/3 91y 1TD; E.Chism (WR3+, short/YAC (aDOT <8)) 5/6 69y; D.Douglas (WR1, intermediate (aDOT 8-13)) 4/5 65y 2TD; E.Raridon (TE2+, short/YAC (aDOT <8)) 5/5 57y
- 20+ catches: D.Douglas(WR1) 35y deep_right TD - no tackler named [unattributed]; H.Henry(TE1) 26y short_right - Q.Walker [tackler]; K.Williams(WR3+) 34y deep_left TD - no tackler named [unattributed]; E.Raridon(TE2+) 31y deep_left - D.Porter [tackler]; K.Williams(WR3+) 49y deep_right - D.Porter [tackler]
- 15+ runs: R.Stevenson(RB) 20y rush left end; C.Kiner(RB) 32y rush right tackle

**Wk6 BUF@LV** (vs BUF offense, 255 rec yds allowed; 23% of targets unattributed)
- Top receivers: K.Coleman (WR2, deep (aDOT 13+)) 4/6 59y 1TD; J.Cook (RB, short/YAC (aDOT <8)) 3/3 58y; D.Kincaid (TE1, intermediate (aDOT 8-13)) 7/8 38y; J.Palmer (WR3+, deep (aDOT 13+)) 1/2 37y
- 20+ catches: J.Palmer(WR3+) 37y deep_right - J.Chinn [tackler]; K.Coleman(WR2) 21y short_middle - J.Chinn [tackler]; J.Cook(RB) 23y short_right - E.Stokes [tackler]; J.Cook(RB) 26y short_left - J.Chinn [tackler]

**Wk7 LAR@LV** (vs LAR offense, 195 rec yds allowed; 28% of targets unattributed)
- Top receivers: P.Nacua (WR1, short/YAC (aDOT <8)) 8/10 68y 1TD; C.Parkinson (TE2+, short/YAC (aDOT <8)) 5/6 48y; K.Williams (RB, short/YAC (aDOT <8)) 2/2 22y; D.Allen (TE2+, short/YAC (aDOT <8)) 4/5 20y 2TD
- 15+ runs: B.Corum(RB) 17y rush right guard; K.Williams(RB) 17y rush left end; B.Corum(RB) 15y rush middle

**Wk8 LV@NYJ** (vs NYJ offense, 290 rec yds allowed; 28% of targets unattributed)
- Top receivers: A.Mitchell (WR2, deep (aDOT 13+)) 7/9 142y 1TD; G.Wilson (WR1, intermediate (aDOT 8-13)) 6/12 83y; K.Sadiq (TE1, short/YAC (aDOT <8)) 1/2 22y; M.Taylor (TE2+, intermediate (aDOT 8-13)) 3/5 19y
- 20+ catches: G.Wilson(WR1) 31y deep_left - T.Stukes [tackler]; A.Mitchell(WR2) 20y deep_right - E.Stokes [tackler]; A.Mitchell(WR2) 22y deep_left - J.McCoy [tackler]; K.Sadiq(TE1) 22y deep_left - T.Eichenberg [tackler]; A.Mitchell(WR2) 47y deep_left - T.Stukes [tackler]
- 15+ runs: B.Allen(RB) 15y rush right end; B.Allen(RB) 15y rush left guard; B.Allen(RB) 24y rush middle; B.Allen(RB) 21y rush left end

## Seed notes from defenders/LV_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 15:00 Garrett Wilson (WR) rec 31 — Eric Stokes [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L42/S22/R36)
- Q1 14:28 Braelon Allen (RB) rush 15 — Q.Walker; T.Stukes [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q1 13:56 Braelon Allen (RB) rush 15 — A.Butler [confirmed; ESPN play text: Defensive Holding on play (single-source)]; alignment: backfield (position default)
- Q2 14:01 Adonai Mitchell (WR) rec 20 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)
- Q2 11:32 Adonai Mitchell (WR) rec 22 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)
- Q2 8:42 Braelon Allen (RB) rush 24 — T.Johnson; E.Stokes [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 9:09 Kenyon Sadiq (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 8:20 Braelon Allen (RB) rush 21 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 6:11 Adonai Mitchell (WR) rec 47 — Darien Porter [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Hezekiah Masses)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L45/S16/R39)
- Darien Porter ← Adonai Mitchell: 9 tgt, 7 rec, 142 yds
- Eric Stokes ← Garrett Wilson: 11 tgt, 6 rec, 83 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 LV@NYJ: Braelon Allen (RB-power/volume early-down) 21-147 1TD; 2/2tgt 6y 0TD | shell 21/70, MOFC/MOFO 47/47 | Backup promoted (Hall out) vs LV run D 5.17 YPC (worst-tier); 147 on 7.0 YPC, 5 run explosives. [confirmed-tackler;unknown]
- wk8 LV@NYJ: Adonai Mitchell (WR-deep speed) 7/9tgt 142y 1TD | shell 21/70, MOFC/MOFO 47/47 | Deep shots vs LV boundary CB Darien Porter (pregame outside-left, inferred; 3 explosives incl. 47y) in shootout; LV WR-outside YPT 8.7. [inferred]
- wk8 LV@NYJ: Geno Smith (QB-pocket) 20/32 290y 2TD 1INT; 1-4 0TD | shell 21/70, MOFC/MOFO 47/47 | Shootout (38-33) vs LV zone; 290y 2TD. [inferred;unknown]
- wk8 LV@NYJ: Garrett Wilson (WR-X outside volume) 6/12tgt 83y 0TD | shell 21/70, MOFC/MOFO 47/47 | Target volume (12) in shootout vs LV zone; pregame CB Eric Stokes (inferred). [inferred]
- wk8 LV@NYJ: Isaiah Williams (WR-slot separator) 1/1tgt 18y 1TD | shell 21/70, MOFC/MOFO 47/47 | Script/volume; no specific matchup attribution — see explosives table. [none (no explosive)]
- wk8 LV@NYJ: Kenyon Sadiq (TE-inline) 1/2tgt 22y 0TD | shell 21/70, MOFC/MOFO 47/47 | Script/volume; no specific matchup attribution — see explosives table. [unknown]

