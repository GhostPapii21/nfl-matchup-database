# IND DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 BAL@IND, wk2 IND@KC, wk3 HOU@IND, wk4 IND@WSH, wk5 IND@PIT, wk6 TEN@IND, wk7 IND@MIN, wk8 IND@JAX). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 26.2% / Zone 66.5% | MOF closed 50.2% / MOF open 44.7% | Blitz 21.9% | Light box 38.6% / Heavy box 26.9% | Sub package 67.0% | Sharp YPT allowed WR 8.4, TE 6.3, RB 7.7, Outside 7.0, Slot 10.7

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type RB: 8.79 YPT on 39 tgts (league 5.61, +3.18), 5 catches of 20+
- type WR3+: 9.29 YPT on 42 tgts (league 7.67, +1.62), 7 catches of 20+
- depth behind_los: 7.68 YPT on 50 tgts (league 4.58, +3.1), 6 catches of 20+
- depth/direction deep_left: 13.69 YPT on 16 tgts (league 11.28, +2.41), 5 catches of 20+
- receiver archetype deep (aDOT 13+): 13.23 YPT on 22 tgts (league 8.94, +4.29), 6 catches of 20+
- receiver archetype short/YAC (aDOT <8): 8.08 YPT on 115 tgts (league 6.47, +1.61), 12 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 39 | 27 | 343 | 2 | 5 | 8.79 | 4.90 | 42.90 | 5.61 | 3.18 |
| TE1 | 38 | 29 | 319 | 4 | 2 | 8.39 | 4.80 | 39.90 | 7.39 | 1 |
| TE2+ | 16 | 9 | 92 | 2 | 1 | 5.75 | 2 | 11.50 | 6.71 | -0.96 |
| WR1 | 48 | 32 | 403 | 3 | 4 | 8.40 | 6 | 50.40 | 8.16 | 0.24 |
| WR2 | 37 | 20 | 250 | 0 | 4 | 6.76 | 4.60 | 31.20 | 8.20 | -1.44 |
| WR3+ | 42 | 23 | 390 | 3 | 7 | 9.29 | 5.20 | 48.80 | 7.67 | 1.62 |
| other | 1 | 1 | 13 | 0 | 0 | 13 | 0.10 | 1.60 | 2.86 | 10.14 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 16 | 11 | 166 | 2 | 3 | 10.38 | 5.61 | 4.77 |
| TE1 | 14 | 11 | 134 | 3 | 2 | 9.57 | 7.39 | 2.18 |
| TE2+ | 8 | 5 | 68 | 1 | 1 | 8.50 | 6.71 | 1.79 |
| WR1 | 20 | 14 | 142 | 1 | 1 | 7.10 | 8.16 | -1.06 |
| WR2 | 22 | 13 | 146 | 0 | 2 | 6.64 | 8.20 | -1.56 |
| WR3+ | 13 | 4 | 49 | 1 | 1 | 3.77 | 7.67 | -3.90 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 50 | 37 | 384 | 2 | 6 | 7.68 | 4.58 | 3.10 |
| short_1-9 | 92 | 69 | 626 | 9 | 3 | 6.80 | 6.23 | 0.57 |
| inter_10-19 | 46 | 26 | 449 | 1 | 5 | 9.76 | 10.17 | -0.41 |
| deep_20+ | 33 | 9 | 351 | 2 | 9 | 10.64 | 12.32 | -1.68 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 16 | 6 | 219 | 2 | 5 | 13.69 | 11.28 | 2.41 |
| deep_middle | 4 | 2 | 36 | 0 | 1 | 9 | 14.90 | -5.90 |
| deep_right | 24 | 11 | 311 | 0 | 7 | 12.96 | 11.85 | 1.11 |
| short_left | 69 | 47 | 432 | 3 | 4 | 6.26 | 6.08 | 0.18 |
| short_middle | 37 | 24 | 321 | 3 | 2 | 8.68 | 7.43 | 1.25 |
| short_right | 71 | 51 | 491 | 6 | 4 | 6.92 | 5.95 | 0.97 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 22 | 12 | 291 | 1 | 6 | 13.23 | 8.94 | 4.29 |
| intermediate (aDOT 8-13) | 84 | 51 | 590 | 6 | 5 | 7.02 | 7.96 | -0.94 |
| short/YAC (aDOT <8) | 115 | 78 | 929 | 7 | 12 | 8.08 | 6.47 | 1.61 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 5, 'TE': 3, 'WR': 15} (23 total, 2.9/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 1, 'deep_right': 7, 'short_left': 4, 'short_middle': 2, 'short_right': 4}
- Rush 15+ by position: {'QB': 4, 'RB': 8} (12 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| DL | 1 | 3 | 0 | 3 | 0.40 |
| QB | 21 | 186 | 4 | 8.86 | 23.20 |
| RB | 177 | 827 | 8 | 4.67 | 103.40 |
| TE | 1 | 1 | 0 | 1 | 0.10 |
| WR | 8 | 45 | 0 | 5.62 | 5.60 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sauce Gardner | CB | 6 | 89.40 | 21 | 3.50 | 15 | 230 | 38.30 | 10.95 | 0 | 4 | 6 | 0 | 0 |
| Justin Walley | CB | 7 | 72.10 | 22 | 3.10 | 19 | 180 | 25.70 | 8.18 | 0 | 1 | 3 | 0 | 0 |
| Charvarius Ward | CB | 6 | 91.40 | 14 | 2.30 | 8 | 88 | 14.70 | 6.29 | 0 | 1 | 6 | 0 | 0 |
| Cam Taylor-Britt | CB | 4 | 25 | 5 | 1.20 | 3 | 47 | 11.80 | 9.40 | 0 | 1 | 2 | 0 | 0 |
| Kapena Gushiken | CB | 3 | 17 | 4 | 1.30 | 3 | 18 | 6 | 4.50 | 0 | 0 | 1 | 0 | 0 |
| Kenneth Harris | CB | 1 |  | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Akeem Davis-Gaither | LB | 8 | 91.80 | 19 | 2.40 | 18 | 163 | 20.40 | 8.58 | 0 | 1 | 1 | 0 | 0 |
| Jaylon Carlies | LB | 4 | 54.20 | 8 | 2 | 7 | 87 | 21.80 | 10.88 | 0 | 1 | 0 | 1 | 0 |
| A.J. Haulcy | S | 8 | 82.80 | 16 | 2 | 14 | 223 | 27.90 | 13.94 | 0 | 4 | 2 | 0 | 0 |
| Camryn Bynum | S | 6 | 99 | 13 | 2.20 | 11 | 174 | 29 | 13.38 | 0 | 2 | 1 | 1 | 0 |
| Hunter Wohler | S | 1 | 21.20 | 1 | 1 | 1 | 30 | 30 | 30 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Sauce Gardner** (CB): WR3+:8t/94y, WR1:5t/49y, WR2:3t/49y, TE1:2t/23y, RB:2t/15y, TE2+:1t/0y | 20+: wk2 R.Rice(WR2) 30 short_right; wk3 X.Hutchinson(WR1) 28 deep_right; wk3 J.Wayne(WR3+) 20 deep_middle; wk4 D.Brown(WR3+) 48 deep_right
- **Justin Walley** (CB): WR1:7t/97y, WR3+:5t/32y, TE1:3t/29y, WR2:2t/16y, TE2+:2t/6y, RB:3t/0y | 20+: wk1 Z.Flowers(WR1) 49 deep_left
- **Charvarius Ward** (CB): WR1:4t/40y, WR2:2t/21y, RB:1t/10y, WR3+:5t/8y, TE1:1t/5y, TE2+:1t/4y | 20+: wk5 G.Bernard(WR2) 21 deep_right
- **Cam Taylor-Britt** (CB): WR2:2t/37y, RB:1t/10y, TE1:1t/0y, WR1:1t/0y | 20+: wk2 R.Rice(WR2) 31 short_middle
- **Kapena Gushiken** (CB): WR2:2t/14y, WR1:2t/4y
- **Kenneth Harris** (CB): WR3+:1t/0y
- **Akeem Davis-Gaither** (LB): RB:4t/50y, WR1:5t/39y, WR3+:3t/20y, TE1:3t/19y, WR2:3t/18y, TE2+:1t/17y | 20+: wk4 J.Croskey-Merritt(RB) 35 short_left
- **Jaylon Carlies** (LB): WR3+:1t/45y, RB:2t/19y, TE1:2t/11y, WR1:1t/6y, WR2:2t/6y | 20+: wk2 T.Thornton(WR3+) 45 deep_right
- **A.J. Haulcy** (S): TE1:4t/74y, WR3+:5t/48y, WR2:3t/48y, RB:2t/30y, WR1:2t/23y | 20+: wk5 G.Bernard(WR2) 25 short_left; wk7 T.Hockenson(TE1) 22 deep_right; wk7 J.Jennings(WR3+) 20 short_right; wk8 B.Strange(TE1) 46 deep_right
- **Camryn Bynum** (S): WR3+:1t/53y, TE1:4t/52y, WR2:4t/32y, RB:1t/22y, TE2+:2t/15y, WR1:1t/0y | 20+: wk1 C.Moore(WR3+) 53 deep_left; wk2 K.Walker(RB) 22 short_left
- **Hunter Wohler** (S): WR3+:1t/30y | 20+: wk2 T.Thornton(WR3+) 30 deep_right

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BAL@IND | Justin Walley | CB | 6 | 6 | 109 | 0 | 1 | 0 | 0 | 0 | Z.Flowersx2, M.Andrewsx2, L.Westerx2 |
| 1 | BAL@IND | Camryn Bynum | S | 4 | 4 | 88 | 0 | 1 | 0 | 0 | 0 | M.Andrewsx2, M.Hibnerx1, C.Moorex1 |
| 1 | BAL@IND | A.J. Haulcy | S | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | D.Henryx1 |
| 1 | BAL@IND | Sauce Gardner | CB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | Z.Flowersx1 |
| 1 | BAL@IND | Akeem Davis-Gaither | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | J.Lanex1 |
| 1 | BAL@IND | Charvarius Ward | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | D.Smythex1 |
| 2 | IND@KC | Sauce Gardner | CB | 7 | 6 | 73 | 0 | 1 | 1 | 0 | 0 | T.Kelcex2, R.Ricex1, T.Thorntonx1, J.Royalsx1, N.Grayx1, K.Walkerx1 |
| 2 | IND@KC | Jaylon Carlies | LB | 3 | 3 | 59 | 0 | 1 | 0 | 0 | 0 | E.Johnsonx1, T.Thorntonx1, R.Ricex1 |
| 2 | IND@KC | Camryn Bynum | S | 3 | 3 | 54 | 0 | 1 | 0 | 0 | 0 | R.Ricex1, T.Kelcex1, K.Walkerx1 |
| 2 | IND@KC | Akeem Davis-Gaither | LB | 5 | 5 | 41 | 0 | 0 | 0 | 0 | 0 | X.Worthyx2, T.Kelcex2, K.Walkerx1 |
| 2 | IND@KC | Cam Taylor-Britt | CB | 2 | 2 | 41 | 0 | 1 | 0 | 0 | 0 | K.Walkerx1, R.Ricex1 |
| 2 | IND@KC | Hunter Wohler | S | 1 | 1 | 30 | 0 | 1 | 0 | 0 | 0 | T.Thorntonx1 |
| 2 | IND@KC | A.J. Haulcy | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | K.Walkerx1 |
| 2 | IND@KC | Justin Walley | CB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | K.Walkerx1, T.Thorntonx1 |
| 2 | IND@KC | Kapena Gushiken | CB | 2 | 1 | -2 | 0 | 0 | 1 | 0 | 0 | X.Worthyx1, R.Ricex1 |
| 3 | HOU@IND | Sauce Gardner | CB | 6 | 4 | 69 | 0 | 2 | 2 | 0 | 0 | X.Hutchinsonx2, J.Waynex2, W.Marksx1, K.Bouttex1 |
| 3 | HOU@IND | Charvarius Ward | CB | 4 | 3 | 32 | 0 | 0 | 1 | 0 | 0 | J.Waynex1, D.Montgomeryx1, D.Schultzx1, X.Hutchinsonx1 |
| 3 | HOU@IND | Justin Walley | CB | 4 | 2 | 18 | 0 | 0 | 2 | 0 | 0 | F.Moreaux2, J.Noelx1, L.Bondx1 |
| 3 | HOU@IND | Akeem Davis-Gaither | LB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | X.Hutchinsonx1, K.Bouttex1 |
| 3 | HOU@IND | Jaylon Carlies | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | X.Hutchinsonx1 |
| 3 | HOU@IND | A.J. Haulcy | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | J.Noelx1 |
| 4 | IND@WSH | Sauce Gardner | CB | 3 | 2 | 57 | 0 | 1 | 1 | 0 | 0 | D.Brownx1, A.Williamsx1, T.Burksx1 |
| 4 | IND@WSH | Akeem Davis-Gaither | LB | 4 | 4 | 55 | 0 | 1 | 0 | 0 | 0 | S.Diggsx2, J.Croskey-Merrittx1, C.Okonkwox1 |
| 4 | IND@WSH | Justin Walley | CB | 4 | 4 | 16 | 0 | 0 | 0 | 0 | 0 | S.Diggsx2, A.Williamsx1, J.Croskey-Merrittx1 |
| 4 | IND@WSH | Jaylon Carlies | LB | 3 | 2 | 13 | 0 | 0 | 0 | 1 | 0 | C.Okonkwox1, A.Williamsx1, A.Ekelerx1 |
| 4 | IND@WSH | A.J. Haulcy | S | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | C.Okonkwox1, D.Brownx1 |
| 4 | IND@WSH | Charvarius Ward | CB | 4 | 1 | 8 | 0 | 0 | 3 | 0 | 0 | D.Brownx2, A.Williamsx1, T.Burksx1 |
| 4 | IND@WSH | Camryn Bynum | S | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | A.Williamsx1, S.Diggsx1 |
| 4 | IND@WSH | Cam Taylor-Britt | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | S.Diggsx1 |
| 5 | IND@PIT | A.J. Haulcy | S | 3 | 2 | 38 | 0 | 1 | 1 | 0 | 0 | G.Bernardx2, R.Wilsonx1 |
| 5 | IND@PIT | Charvarius Ward | CB | 1 | 1 | 21 | 0 | 1 | 0 | 0 | 0 | G.Bernardx1 |
| 5 | IND@PIT | Camryn Bynum | S | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | D.Washingtonx1, P.Freiermuthx1 |
| 5 | IND@PIT | Sauce Gardner | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | D.Metcalfx1 |
| 5 | IND@PIT | Justin Walley | CB | 2 | 2 | 9 | 0 | 0 | 0 | 0 | 0 | D.Metcalfx1, G.Bernardx1 |
| 5 | IND@PIT | Akeem Davis-Gaither | LB | 3 | 3 | 7 | 0 | 0 | 0 | 0 | 0 | G.Bernardx2, J.Warrenx1 |
| 6 | TEN@IND | A.J. Haulcy | S | 3 | 3 | 33 | 0 | 0 | 0 | 0 | 0 | C.Tatex2, W.Robinsonx1 |
| 6 | TEN@IND | Justin Walley | CB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | C.Tatex2 |
| 6 | TEN@IND | Akeem Davis-Gaither | LB | 2 | 2 | 9 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1, E.Ayomanorx1 |
| 6 | TEN@IND | Cam Taylor-Britt | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1 |
| 6 | TEN@IND | Camryn Bynum | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | W.Robinsonx1 |
| 7 | IND@MIN | A.J. Haulcy | S | 4 | 4 | 62 | 0 | 2 | 0 | 0 | 0 | T.Hockensonx2, J.Jenningsx2 |
| 7 | IND@MIN | Akeem Davis-Gaither | LB | 1 | 1 | 17 | 0 | 0 | 0 | 0 | 0 | G.Bartholomewx1 |
| 7 | IND@MIN | Camryn Bynum | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | J.Addisonx1 |
| 7 | IND@MIN | Charvarius Ward | CB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | J.Jeffersonx2 |
| 7 | IND@MIN | Kapena Gushiken | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | J.Jeffersonx1 |
| 7 | IND@MIN | Justin Walley | CB | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1, A.Jonesx1 |
| 7 | IND@MIN | Cam Taylor-Britt | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.Hockensonx1 |
| 7 | IND@MIN | Kenneth Harris | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.Feltonx1 |
| 8 | IND@JAX | A.J. Haulcy | S | 1 | 1 | 46 | 0 | 1 | 0 | 0 | 0 | B.Strangex1 |
| 8 | IND@JAX | Akeem Davis-Gaither | LB | 1 | 1 | 17 | 0 | 0 | 0 | 0 | 0 | C.Rodriguezx1 |
| 8 | IND@JAX | Charvarius Ward | CB | 2 | 1 | 16 | 0 | 0 | 1 | 0 | 0 | Bri.Thomasx1, P.Washingtonx1 |
| 8 | IND@JAX | Kapena Gushiken | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | J.Meyersx1 |
| 8 | IND@JAX | Sauce Gardner | CB | 3 | 1 | 10 | 0 | 0 | 2 | 0 | 0 | P.Washingtonx1, J.Meyersx1, J.Cameronx1 |
| 8 | IND@JAX | Jaylon Carlies | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | B.Strangex1 |

## Who beat them each week

**Wk1 BAL@IND** (vs BAL offense, 324 rec yds allowed; 33% of targets unattributed)
- Top receivers: Z.Flowers (WR1, intermediate (aDOT 8-13)) 5/6 150y 1TD; C.Moore (WR3+, deep (aDOT 13+)) 1/2 53y; M.Andrews (TE1, short/YAC (aDOT <8)) 4/6 49y; D.Henry (RB, short/YAC (aDOT <8)) 1/1 19y
- 20+ catches: Z.Flowers(WR1) 49y deep_left - J.Walley [tackler]; Z.Flowers(WR1) 54y short_middle TD - no tackler named [unattributed]; C.Moore(WR3+) 53y deep_left - C.Bynum [tackler]
- 15+ runs: L.Jackson(QB) 16y rush right end; D.Henry(RB) 32y rush left tackle; L.Jackson(QB) 19y rush left end; D.Henry(RB) 22y rush left tackle

**Wk2 IND@KC** (vs KC offense, 382 rec yds allowed; 23% of targets unattributed)
- Top receivers: T.Kelce (TE1, short/YAC (aDOT <8)) 9/11 101y 1TD; T.Thornton (WR3+, deep (aDOT 13+)) 4/4 86y; R.Rice (WR2, short/YAC (aDOT <8)) 4/6 83y; K.Walker (RB, short/YAC (aDOT <8)) 6/10 61y
- 20+ catches: R.Rice(WR2) 30y short_right - A.Gardner [tackler]; T.Thornton(WR3+) 45y deep_right - J.Carlies [tackler]; R.Rice(WR2) 31y short_middle - C.Taylor-Britt [tackler]; T.Thornton(WR3+) 30y deep_right - H.Wohler [tackler]; K.Walker(RB) 22y short_left - C.Bynum [tackler]
- 15+ runs: K.Walker(RB) 19y rush left guard

**Wk3 HOU@IND** (vs HOU offense, 167 rec yds allowed; 16% of targets unattributed)
- Top receivers: X.Hutchinson (WR1, intermediate (aDOT 8-13)) 3/6 51y; D.Schultz (TE1, short/YAC (aDOT <8)) 3/3 30y; K.Boutte (WR3+, intermediate (aDOT 8-13)) 2/2 21y; J.Wayne (WR3+, deep (aDOT 13+)) 1/4 20y
- 20+ catches: X.Hutchinson(WR1) 28y deep_right - A.Gardner [tackler]; J.Wayne(WR3+) 20y deep_middle - A.Gardner [tackler]

**Wk4 IND@WSH** (vs WSH offense, 232 rec yds allowed; 28% of targets unattributed)
- Top receivers: D.Brown (WR3+, deep (aDOT 13+)) 3/4 65y; T.Burks (WR3+, deep (aDOT 13+)) 1/3 47y 1TD; S.Diggs (WR1, intermediate (aDOT 8-13)) 5/9 35y; J.Croskey-Merritt (RB, short/YAC (aDOT <8)) 2/4 35y
- 20+ catches: J.Croskey-Merritt(RB) 35y short_left - A.Davis-Gaither [tackler]; T.Burks(WR3+) 47y deep_left TD - no tackler named [unattributed]; D.Brown(WR3+) 48y deep_right - A.Gardner [tackler]
- 15+ runs: M.Mariota(QB) 35y rush left end

**Wk5 IND@PIT** (vs PIT offense, 235 rec yds allowed; 27% of targets unattributed)
- Top receivers: J.Warren (RB, short/YAC (aDOT <8)) 6/6 87y 1TD; G.Bernard (WR2, short/YAC (aDOT <8)) 6/9 80y; P.Freiermuth (TE1, intermediate (aDOT 8-13)) 5/7 44y 2TD; D.Metcalf (WR1, intermediate (aDOT 8-13)) 3/4 12y
- 20+ catches: J.Warren(RB) 80y short_right TD - no tackler named [unattributed]; G.Bernard(WR2) 21y deep_right - C.Ward [tackler]; G.Bernard(WR2) 25y short_left - A.Haulcy [tackler]
- 15+ runs: J.Warren(RB) 50y rush left guard

**Wk6 TEN@IND** (vs TEN offense, 102 rec yds allowed; 36% of targets unattributed)
- Top receivers: C.Tate (WR1, intermediate (aDOT 8-13)) 6/7 70y 1TD; W.Robinson (WR2, short/YAC (aDOT <8)) 3/7 22y; T.Spears (RB, short/YAC (aDOT <8)) 1/1 7y; E.Ayomanor (WR3+, intermediate (aDOT 8-13)) 1/2 3y
- 15+ runs: T.Pollard(RB) 16y rush right guard

**Wk7 IND@MIN** (vs MIN offense, 150 rec yds allowed; 38% of targets unattributed)
- Top receivers: J.Jefferson (WR1, intermediate (aDOT 8-13)) 4/7 44y; T.Hockenson (TE1, short/YAC (aDOT <8)) 4/5 35y 1TD; J.Jennings (WR3+, intermediate (aDOT 8-13)) 2/3 34y; J.Addison (WR2, deep (aDOT 13+)) 2/3 20y
- 20+ catches: J.Jefferson(WR1) 21y deep_left - no tackler named [unattributed]; T.Hockenson(TE1) 22y deep_right - A.Haulcy [tackler]; J.Jennings(WR3+) 20y short_right - A.Haulcy [tackler]
- 15+ runs: K.Murray(QB) 35y rush right tackle; A.Jones(RB) 17y rush right end

**Wk8 IND@JAX** (vs JAX offense, 218 rec yds allowed; 28% of targets unattributed)
- Top receivers: B.Strange (TE1, short/YAC (aDOT <8)) 2/2 55y; B.Tuten (RB, short/YAC (aDOT <8)) 2/2 55y 1TD; N.Boerkircher (TE2+, short/YAC (aDOT <8)) 1/1 31y 1TD; J.Meyers (WR2, intermediate (aDOT 8-13)) 2/3 24y
- 20+ catches: B.Strange(TE1) 46y deep_right - A.Haulcy [tackler]; N.Boerkircher(TE2+) 31y deep_left TD - no tackler named [unattributed]; B.Tuten(RB) 30y short_left - C.Curry [tackler]; B.Tuten(RB) 25y short_right TD - no tackler named [unattributed]
- 15+ runs: B.Tuten(RB) 39y rush right tackle; C.Rodriguez(RB) 28y rush middle

## Seed notes from defenders/IND_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 10:33 Brenton Strange (TE) rec 46 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 7:14 Nate Boerkircher (TE) rec 31 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 1:51 Bhayshul Tuten (RB) rush 39 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 9:08 Chris Rodriguez Jr. (RB) rush 28 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 3:50 Bhayshul Tuten (RB) rec 30 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q3 0:00 Bhayshul Tuten (RB) rec 25 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Charvarius Ward ← Jakobi Meyers: 3 tgt, 2 rec, 24 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 IND@JAX: Bhayshul Tuten (RB-home-run zone runner) 16-104 1TD; 2/2tgt 55y 1TD | shell 26/67, MOFC 50 | JAX -10 favorite, IND run D 4.49/RB rec YPT 7.7 (soft vs RB receiving); 104 rush + 55 rec, 2 TD. [unknown]
- wk8 IND@JAX: Trevor Lawrence (QB-pocket) 10/14 210y 3TD 0INT; 3-10 0TD | shell 26/67, MOFC 50 | 10/14 210y 3TD — efficiency, not volume; IND zone (MOFC 50) beaten deep (46y, inferred Haulcy). [inferred;unknown]
- wk8 IND@JAX: Chris Rodriguez Jr. (RB-committee/change-of-pace) 6-41 1TD; 1/1tgt 17y 0TD | shell 26/67, MOFC 50 | Script/volume; no specific matchup attribution — see explosives table. [unknown]
- wk8 IND@JAX: Brenton Strange (TE-move/seam) 2/2tgt 55y 0TD | shell 26/67, MOFC 50 | Script/volume; no specific matchup attribution — see explosives table. [inferred]
- wk8 IND@JAX: Nate Boerkircher (TE-inline) 1/1tgt 31y 1TD | shell 26/67, MOFC 50 | Script/volume; no specific matchup attribution — see explosives table. [unknown]
- wk8 IND@JAX: Parker Washington (WR-slot separator) 1-10 0TD; 1/2tgt 16y 0TD | shell 26/67, MOFC 50 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 IND@JAX: Brian Thomas Jr. (WR-deep speed) 1/2tgt 12y 1TD | shell 26/67, MOFC 50 | Script/volume; no specific matchup attribution — see explosives table. [none (no explosive)]

