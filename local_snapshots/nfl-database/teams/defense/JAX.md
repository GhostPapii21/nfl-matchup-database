# JAX DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 CLE@JAX, wk2 JAX@DEN, wk3 NE@JAX, wk4 JAX@CIN, wk5 PHI@JAX, wk6 HOU@JAX, wk8 IND@JAX). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 21.0% / Zone 73.4% | MOF closed 46.0% / MOF open 51.1% | Blitz 26.0% | Light box 48.5% / Heavy box 21.3% | Sub package 75.0% | Sharp YPT allowed WR 10.0, TE 5.6, RB 5.8, Outside 10.4, Slot 9.9

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR2: 10.18 YPT on 28 tgts (league 8.2, +1.98), 5 catches of 20+
- type WR3+: 9.79 YPT on 63 tgts (league 7.67, +2.12), 9 catches of 20+
- depth deep_20+: 18.4 YPT on 25 tgts (league 12.32, +6.08), 12 catches of 20+
- depth/direction deep_right: 15.57 YPT on 21 tgts (league 11.85, +3.72), 8 catches of 20+
- receiver archetype intermediate (aDOT 8-13): 10.51 YPT on 63 tgts (league 7.96, +2.55), 11 catches of 20+

Holds (-1.5 YPT or better): TE1: 4.78 YPT on 36 tgts (league 7.39, -2.61)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 45 | 37 | 254 | 0 | 1 | 5.64 | 6.40 | 36.30 | 5.61 | 0.03 |
| TE1 | 36 | 21 | 172 | 1 | 0 | 4.78 | 5.10 | 24.60 | 7.39 | -2.61 |
| TE2+ | 11 | 8 | 54 | 3 | 0 | 4.91 | 1.60 | 7.70 | 6.71 | -1.80 |
| WR1 | 50 | 33 | 468 | 2 | 6 | 9.36 | 7.10 | 66.90 | 8.16 | 1.20 |
| WR2 | 28 | 23 | 285 | 0 | 5 | 10.18 | 4 | 40.70 | 8.20 | 1.98 |
| WR3+ | 63 | 39 | 617 | 2 | 9 | 9.79 | 9 | 88.10 | 7.67 | 2.12 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 28 | 21 | 132 | 0 | 0 | 4.71 | 5.61 | -0.90 |
| TE1 | 30 | 17 | 129 | 1 | 0 | 4.30 | 7.39 | -3.09 |
| TE2+ | 7 | 4 | 8 | 2 | 0 | 1.14 | 6.71 | -5.57 |
| WR1 | 31 | 22 | 233 | 1 | 1 | 7.52 | 8.16 | -0.64 |
| WR2 | 15 | 13 | 168 | 0 | 2 | 11.20 | 8.20 | 3 |
| WR3+ | 41 | 28 | 442 | 2 | 5 | 10.78 | 7.67 | 3.11 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 46 | 38 | 174 | 0 | 0 | 3.78 | 4.58 | -0.80 |
| short_1-9 | 104 | 72 | 594 | 4 | 2 | 5.71 | 6.23 | -0.52 |
| inter_10-19 | 58 | 39 | 622 | 2 | 7 | 10.72 | 10.17 | 0.55 |
| deep_20+ | 25 | 12 | 460 | 2 | 12 | 18.40 | 12.32 | 6.08 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 18 | 8 | 177 | 0 | 3 | 9.83 | 11.28 | -1.45 |
| deep_middle | 6 | 5 | 183 | 1 | 4 | 30.50 | 14.90 | 15.60 |
| deep_right | 21 | 11 | 327 | 1 | 8 | 15.57 | 11.85 | 3.72 |
| short_left | 73 | 54 | 427 | 2 | 3 | 5.85 | 6.08 | -0.23 |
| short_middle | 35 | 23 | 250 | 1 | 1 | 7.14 | 7.43 | -0.29 |
| short_right | 80 | 60 | 486 | 3 | 2 | 6.08 | 5.95 | 0.13 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 51 | 33 | 512 | 1 | 7 | 10.04 | 8.94 | 1.10 |
| intermediate (aDOT 8-13) | 63 | 41 | 662 | 4 | 11 | 10.51 | 7.96 | 2.55 |
| short/YAC (aDOT <8) | 119 | 87 | 676 | 3 | 3 | 5.68 | 6.47 | -0.79 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'WR': 20} (21 total, 3.0/g)
- Pass 20+ by depth/direction: {'deep_left': 3, 'deep_middle': 4, 'deep_right': 8, 'short_left': 3, 'short_middle': 1, 'short_right': 2}
- Rush 15+ by position: {'RB': 4, 'WR': 1} (5 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 23 | 93 | 0 | 4.04 | 13.30 |
| RB | 123 | 404 | 4 | 3.28 | 57.70 |
| TE | 3 | 11 | 0 | 3.67 | 1.60 |
| WR | 6 | 39 | 1 | 6.50 | 5.60 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Jarrian Jones | CB | 6 | 75 | 26 | 4.30 | 20 | 227 | 37.80 | 8.73 | 0 | 2 | 5 | 1 | 0 |
| Jourdan Lewis | CB | 5 | 64.10 | 16 | 3.20 | 14 | 172 | 34.40 | 10.75 | 0 | 3 | 0 | 2 | 0 |
| Montaric Brown | CB | 5 | 60.20 | 11 | 2.20 | 9 | 115 | 23 | 10.45 | 0 | 1 | 2 | 0 | 0 |
| Foyesade Oluokun | LB | 5 | 87.10 | 20 | 4 | 18 | 103 | 20.60 | 5.15 | 0 | 0 | 0 | 2 | 0 |
| Ventrell Miller | LB | 7 | 72 | 14 | 2 | 11 | 72 | 10.30 | 5.14 | 0 | 0 | 3 | 0 | 0 |
| Branson Combs | LB | 4 | 21.30 | 7 | 1.80 | 5 | 47 | 11.80 | 6.71 | 0 | 0 | 1 | 1 | 0 |
| Antonio Johnson | S | 6 | 85.70 | 14 | 2.30 | 13 | 182 | 30.30 | 13 | 0 | 4 | 1 | 0 | 0 |
| Rayuan Lane III | S | 3 | 56.60 | 13 | 4.30 | 9 | 103 | 34.30 | 7.92 | 0 | 1 | 3 | 1 | 0 |
| Eric Murray | S | 4 | 80.60 | 7 | 1.80 | 7 | 91 | 22.80 | 13 | 0 | 0 | 0 | 0 | 0 |
| Caleb Ransaw | S | 2 | 35.30 | 3 | 1.50 | 3 | 49 | 24.50 | 16.33 | 0 | 2 | 0 | 0 | 0 |
| Kaevon Merriweather | S | 2 | 57.30 | 2 | 1 | 2 | 34 | 17 | 17 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Jarrian Jones** (CB): WR3+:11t/140y, WR1:7t/25y, WR2:2t/21y, RB:4t/19y, TE2+:1t/18y, TE1:1t/4y | 20+: wk3 K.Williams(WR3+) 34 deep_right; wk6 J.Noel(WR3+) 50 deep_middle
- **Jourdan Lewis** (CB): WR1:4t/61y, RB:5t/54y, WR2:4t/46y, TE1:2t/11y, WR3+:1t/0y | 20+: wk1 K.Concepcion(WR2) 25 deep_right; wk2 T.Badie(RB) 27 short_left; wk2 J.Waddle(WR1) 29 deep_right
- **Montaric Brown** (CB): WR1:4t/78y, WR2:3t/19y, WR3+:2t/10y, RB:2t/8y | 20+: wk2 J.Waddle(WR1) 49 deep_middle
- **Foyesade Oluokun** (LB): WR1:5t/40y, RB:7t/25y, TE1:3t/21y, WR2:1t/9y, WR3+:3t/6y, TE2+:1t/2y
- **Ventrell Miller** (LB): RB:6t/25y, TE2+:2t/21y, TE1:3t/15y, WR3+:1t/6y, WR2:1t/5y, WR1:1t/0y
- **Branson Combs** (LB): RB:2t/25y, WR3+:2t/21y, WR1:1t/1y, TE1:2t/0y
- **Antonio Johnson** (S): WR1:4t/68y, WR3+:2t/50y, WR2:3t/38y, RB:2t/18y, TE1:1t/9y, TE2+:2t/-1y | 20+: wk2 J.Waddle(WR1) 20 short_right; wk3 R.Doubs(WR2) 21 deep_left; wk4 T.Higgins(WR1) 26 deep_right; wk6 J.Noel(WR3+) 34 short_middle
- **Rayuan Lane III** (S): WR3+:3t/34y, TE1:6t/32y, RB:2t/18y, WR1:1t/14y, WR2:1t/5y | 20+: wk4 D.Meyers(WR3+) 29 deep_right
- **Eric Murray** (S): WR3+:4t/49y, WR1:3t/42y
- **Caleb Ransaw** (S): WR2:1t/20y, WR3+:1t/20y, RB:1t/9y | 20+: wk1 J.Jeudy(WR3+) 20 short_left; wk3 R.Doubs(WR2) 20 deep_middle
- **Kaevon Merriweather** (S): WR3+:1t/18y, TE1:1t/16y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CLE@JAX | Jourdan Lewis | CB | 2 | 2 | 30 | 0 | 1 | 0 | 0 | 0 | K.Concepcionx1, R.Sandersx1 |
| 1 | CLE@JAX | Caleb Ransaw | S | 2 | 2 | 29 | 0 | 1 | 0 | 0 | 0 | J.Jeudyx1, R.Sandersx1 |
| 1 | CLE@JAX | Ventrell Miller | LB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | B.Whiteheartx1, Q.Judkinsx1, K.Concepcionx1 |
| 1 | CLE@JAX | Antonio Johnson | S | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1, R.Sandersx1 |
| 1 | CLE@JAX | Foyesade Oluokun | LB | 3 | 2 | 18 | 0 | 0 | 0 | 1 | 0 | J.Jeudyx2, H.Fanninx1 |
| 1 | CLE@JAX | Montaric Brown | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | D.Bostonx1 |
| 2 | JAX@DEN | Jourdan Lewis | CB | 5 | 4 | 70 | 0 | 2 | 0 | 1 | 0 | C.Suttonx2, T.Badiex1, J.Colemanx1, J.Waddlex1 |
| 2 | JAX@DEN | Montaric Brown | CB | 4 | 4 | 65 | 0 | 1 | 0 | 0 | 0 | J.Waddlex2, J.Colemanx1, T.Badiex1 |
| 2 | JAX@DEN | Antonio Johnson | S | 2 | 2 | 28 | 0 | 1 | 0 | 0 | 0 | C.Suttonx1, J.Waddlex1 |
| 2 | JAX@DEN | Jarrian Jones | CB | 2 | 1 | 18 | 0 | 0 | 1 | 0 | 0 | N.Adkinsx1, L.Humphreyx1 |
| 2 | JAX@DEN | Foyesade Oluokun | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | J.Waddlex2 |
| 2 | JAX@DEN | Eric Murray | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | J.Waddlex1 |
| 2 | JAX@DEN | Ventrell Miller | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | N.Adkinsx1 |
| 2 | JAX@DEN | Branson Combs | LB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | J.Waddlex1 |
| 3 | NE@JAX | Jarrian Jones | CB | 4 | 3 | 48 | 0 | 1 | 0 | 1 | 0 | K.Williamsx2, M.Hollinsx1, E.Chismx1 |
| 3 | NE@JAX | Antonio Johnson | S | 2 | 2 | 37 | 0 | 1 | 0 | 0 | 0 | M.Hollinsx1, R.Doubsx1 |
| 3 | NE@JAX | Ventrell Miller | LB | 5 | 4 | 25 | 0 | 0 | 1 | 0 | 0 | R.Stevensonx2, T.Hendersonx1, D.Douglasx1, H.Henryx1 |
| 3 | NE@JAX | Caleb Ransaw | S | 1 | 1 | 20 | 0 | 1 | 0 | 0 | 0 | R.Doubsx1 |
| 3 | NE@JAX | Montaric Brown | CB | 2 | 1 | 10 | 0 | 0 | 1 | 0 | 0 | R.Doubsx1, M.Hollinsx1 |
| 3 | NE@JAX | Eric Murray | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | M.Hollinsx1 |
| 4 | JAX@CIN | Rayuan Lane III | S | 7 | 6 | 73 | 0 | 1 | 1 | 0 | 0 | D.Meyersx2, M.Gesickix2, C.Brownx2, T.Higginsx1 |
| 4 | JAX@CIN | Jarrian Jones | CB | 10 | 7 | 58 | 0 | 0 | 3 | 0 | 0 | T.Higginsx4, C.Brownx3, J.Chasex2, M.Tinsleyx1 |
| 4 | JAX@CIN | Eric Murray | S | 3 | 3 | 44 | 0 | 0 | 0 | 0 | 0 | T.Higginsx2, D.Meyersx1 |
| 4 | JAX@CIN | Antonio Johnson | S | 2 | 2 | 43 | 0 | 1 | 0 | 0 | 0 | T.Higginsx2 |
| 4 | JAX@CIN | Jourdan Lewis | CB | 4 | 3 | 25 | 0 | 0 | 0 | 1 | 0 | C.Brownx2, D.Meyersx1, T.Higginsx1 |
| 4 | JAX@CIN | Foyesade Oluokun | LB | 5 | 4 | 21 | 0 | 0 | 0 | 1 | 0 | C.Brownx3, M.Tinsleyx1, T.Hudsonx1 |
| 4 | JAX@CIN | Branson Combs | LB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | D.Meyersx1 |
| 4 | JAX@CIN | Ventrell Miller | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | C.Brownx1 |
| 5 | PHI@JAX | Jourdan Lewis | CB | 3 | 3 | 29 | 0 | 0 | 0 | 0 | 0 | M.Lemonx2, D.Goedertx1 |
| 5 | PHI@JAX | Rayuan Lane III | S | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | D.Goedertx2 |
| 5 | PHI@JAX | Foyesade Oluokun | LB | 5 | 5 | 24 | 0 | 0 | 0 | 0 | 0 | D.Goedertx2, M.Lemonx2, D.Piercex1 |
| 5 | PHI@JAX | Jarrian Jones | CB | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1, D.Wicksx1, D.Cooperx1 |
| 5 | PHI@JAX | Kaevon Merriweather | S | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | D.Wicksx1 |
| 5 | PHI@JAX | Antonio Johnson | S | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | W.Shipleyx1, J.Mundtx1 |
| 5 | PHI@JAX | Montaric Brown | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Cooperx1 |
| 5 | PHI@JAX | Ventrell Miller | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Goedertx1 |
| 6 | HOU@JAX | Jarrian Jones | CB | 5 | 4 | 76 | 0 | 1 | 1 | 0 | 0 | M.Harrisonx2, J.Noelx1, X.Hutchinsonx1, J.Jordanx1 |
| 6 | HOU@JAX | Antonio Johnson | S | 4 | 4 | 47 | 0 | 1 | 0 | 0 | 0 | X.Hutchinsonx1, J.Noelx1, B.Jordanx1, D.Schultzx1 |
| 6 | HOU@JAX | Branson Combs | LB | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | W.Marksx2, M.Harrisonx1 |
| 6 | HOU@JAX | Eric Murray | S | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | M.Harrisonx1, J.Noelx1 |
| 6 | HOU@JAX | Jourdan Lewis | CB | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1, N.Collinsx1 |
| 6 | HOU@JAX | Kaevon Merriweather | S | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | D.Schultzx1 |
| 6 | HOU@JAX | Ventrell Miller | LB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | W.Marksx1, K.Bouttex1 |
| 8 | IND@JAX | Montaric Brown | CB | 3 | 3 | 27 | 0 | 0 | 0 | 0 | 0 | K.Allenx2, J.Downsx1 |
| 8 | IND@JAX | Foyesade Oluokun | LB | 5 | 5 | 23 | 0 | 0 | 0 | 0 | 0 | J.Taylorx3, J.Downsx1, K.Allenx1 |
| 8 | IND@JAX | Ventrell Miller | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | T.Warrenx1 |
| 8 | IND@JAX | Jarrian Jones | CB | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | T.Warrenx1, J.Downsx1 |
| 8 | IND@JAX | Rayuan Lane III | S | 4 | 1 | 5 | 0 | 0 | 2 | 1 | 0 | T.Warrenx2, K.Allenx1, L.Treadwellx1 |
| 8 | IND@JAX | Branson Combs | LB | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | T.Warrenx2 |

## Who beat them each week

**Wk1 CLE@JAX** (vs CLE offense, 205 rec yds allowed; 23% of targets unattributed)
- Top receivers: D.Boston (WR1, deep (aDOT 13+)) 2/4 59y 1TD; K.Concepcion (WR2, short/YAC (aDOT <8)) 4/5 43y; J.Jeudy (WR3+, intermediate (aDOT 8-13)) 2/4 26y; R.Sanders (RB, short/YAC (aDOT <8)) 3/3 25y
- 20+ catches: J.Jeudy(WR3+) 20y short_left - C.Ransaw [tackler]; K.Concepcion(WR2) 25y deep_right - J.Lewis [tackler]; D.Boston(WR1) 46y deep_middle TD - no tackler named [unattributed]

**Wk2 JAX@DEN** (vs DEN offense, 288 rec yds allowed; 21% of targets unattributed)
- Top receivers: J.Waddle (WR1, intermediate (aDOT 8-13)) 8/10 138y; N.Adkins (TE2+, short/YAC (aDOT <8)) 3/3 32y 1TD; T.Badie (RB, short/YAC (aDOT <8)) 2/3 28y; T.Franklin (WR3+, deep (aDOT 13+)) 1/2 27y
- 20+ catches: J.Waddle(WR1) 49y deep_middle - M.Brown [tackler]; J.Waddle(WR1) 20y short_right - A.Johnson [tackler]; T.Badie(RB) 27y short_left - J.Lewis [tackler]; T.Franklin(WR3+) 27y deep_left - no tackler named [unattributed]; J.Waddle(WR1) 29y deep_right - J.Lewis [tackler]
- 15+ runs: J.Dobbins(RB) 15y rush right guard; P.Bryant(WR) 16y rush right end

**Wk3 NE@JAX** (vs NE offense, 245 rec yds allowed; 30% of targets unattributed)
- Top receivers: M.Hollins (WR3+, deep (aDOT 13+)) 6/9 87y; R.Doubs (WR2, deep (aDOT 13+)) 3/4 49y; D.Douglas (WR1, intermediate (aDOT 8-13)) 1/5 38y; K.Williams (WR3+, deep (aDOT 13+)) 1/3 34y
- 20+ catches: M.Hollins(WR3+) 21y short_left - T.Hunter [tackler]; D.Douglas(WR1) 38y deep_left - T.Hunter [tackler]; R.Doubs(WR2) 21y deep_left - A.Johnson [tackler]; K.Williams(WR3+) 34y deep_right - J.Jones [tackler]; R.Doubs(WR2) 20y deep_middle - C.Ransaw [tackler]

**Wk4 JAX@CIN** (vs CIN offense, 428 rec yds allowed; 21% of targets unattributed)
- Top receivers: T.Higgins (WR1, deep (aDOT 13+)) 11/16 157y; D.Meyers (WR3+, short/YAC (aDOT <8)) 7/9 82y; C.Brown (RB, short/YAC (aDOT <8)) 11/11 71y; M.Tinsley (WR3+, intermediate (aDOT 8-13)) 3/7 49y
- 20+ catches: D.Meyers(WR3+) 29y deep_right - R.Lane [tackler]; T.Higgins(WR1) 26y deep_right - A.Johnson [tackler]; M.Tinsley(WR3+) 29y deep_right - no tackler named [unattributed]

**Wk5 PHI@JAX** (vs PHI offense, 220 rec yds allowed; 32% of targets unattributed)
- Top receivers: D.Cooper (WR3+, intermediate (aDOT 8-13)) 2/3 71y 1TD; D.Wicks (WR3+, deep (aDOT 13+)) 5/8 63y; M.Lemon (WR1, short/YAC (aDOT <8)) 5/7 43y; D.Goedert (TE1, short/YAC (aDOT <8)) 6/9 38y
- 20+ catches: D.Cooper(WR3+) 62y deep_right TD - no tackler named [unattributed]

**Wk6 HOU@JAX** (vs HOU offense, 312 rec yds allowed; 25% of targets unattributed)
- Top receivers: J.Noel (WR3+, intermediate (aDOT 8-13)) 4/4 107y 1TD; N.Collins (WR2, intermediate (aDOT 8-13)) 3/5 74y; M.Harrison (WR3+, deep (aDOT 13+)) 3/4 34y; D.Schultz (TE1, short/YAC (aDOT <8)) 4/6 33y
- 20+ catches: N.Collins(WR2) 42y deep_right - T.Hunter [tackler]; J.Noel(WR3+) 34y short_middle - A.Johnson [tackler]; J.Noel(WR3+) 50y deep_middle - Jar.Jones [tackler]; N.Collins(WR2) 21y short_right - T.Hunter [tackler]
- 15+ runs: J.Jordan(RB) 25y rush left tackle

**Wk8 IND@JAX** (vs IND offense, 152 rec yds allowed; 20% of targets unattributed)
- Top receivers: K.Allen (WR2, short/YAC (aDOT <8)) 7/7 67y; J.Taylor (RB, short/YAC (aDOT <8)) 4/5 24y; J.Downs (WR1, intermediate (aDOT 8-13)) 4/5 23y 1TD; L.Treadwell (WR3+, intermediate (aDOT 8-13)) 1/2 18y
- 15+ runs: J.Taylor(RB) 19y rush right end; S.McGowan(RB) 16y rush middle

## Seed notes from defenders/JAX_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 14:56 Jonathan Taylor (RB) rush 19 — M.Brown [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 6:04 Seth McGowan (RB) rush 16 — K.Merriweather; R.Lane [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Jarrian Jones ← Keenan Allen: 7 tgt, 7 rec, 67 yds
- Jourdan Lewis ← Josh Downs: 5 tgt, 4 rec, 23 yds — limited his man
- Travis Hunter ← Laquon Treadwell: 2 tgt, 1 rec, 18 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 IND@JAX: Keenan Allen (WR-slot separator) 7/7tgt 67y 0TD | shell 21/73, MOFO 51 | Trailing IND slot volume (7/7) vs JAX middle-of-field zone (JAX WR-mid YPT 15.7 season — softest area). [none (no explosive)]
- wk8 IND@JAX: DJ Giddens (RB-power/volume early-down) 6-43 0TD | shell 21/73, MOFO 51 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 IND@JAX: Jonathan Taylor (RB-power/volume early-down) 8-23 0TD; 4/5tgt 24y 0TD | shell 21/73, MOFO 51 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 IND@JAX: Josh Downs (WR-slot separator) 4/5tgt 23y 1TD | shell 21/73, MOFO 51 | Script/volume; no specific matchup attribution — see explosives table. [none (no explosive)]
- wk8 IND@JAX: Seth McGowan (RB-committee/change-of-pace) 5-29 0TD | shell 21/73, MOFO 51 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]


## TNF JAX@BAL 2026-11-05 (Week 10) — live log (tackler/PBU tag, not true coverage)
Final **JAX 33 – BAL 10**. Vs BAL offense with UDFA QB J.Fagnano (10/18, 60 yds, 0 TD, 2 INT, 1 sack).

**Pass defense:** held BAL to 57 receiving yards. Flowers 3/6 for 6; Bateman 1/2 for 6; Andrews 2/2 for 19; Hill 3/3 for 7; Wester 1/1 for 14; Hibner 1/2 for 5. **No pass20 allowed.**
- INTs: M.Brown (Q3, Flowers), J.Lewis (Q4, Flowers).
- Tackler-after-catch / INT ledger: M.Brown 5 tags (4 rec/28 + 1 INT); F.Oluokun 2/9 (both Flowers); A.Johnson 2/9; T.Hunter 1/12 (Andrews); T.Walker 1/−3 (Flowers); V.Miller 1/2; J.Lewis 1 INT.

**Run defense:** Henry 17/57 (long 8) — no explosive. Hill 9/85 with **65-yd TD** Q4 (only rush10+/40+ of the game; JAX D allowed 1 explosive). Flowers 3/17 rush; Fagnano 3/13.
