# BAL DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 BAL@IND, wk2 NO@BAL, wk3 BAL@DAL, wk4 TEN@BAL, wk5 BAL@ATL, wk6 BAL@CLE, wk7 CIN@BAL, wk8 BAL@BUF). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 15.9% / Zone 78.6% | MOF closed 36.4% / MOF open 61.4% | Blitz 29.2% | Light box 55.3% / Heavy box 16.2% | Sub package 81.0% | Sharp YPT allowed WR 9.3, TE 7.2, RB 2.5, Outside 9.8, Slot 9.5

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR1: 11.33 YPT on 64 tgts (league 8.16, +3.17), 12 catches of 20+
- depth deep_20+: 16.69 YPT on 26 tgts (league 12.32, +4.37), 13 catches of 20+
- depth/direction deep_left: 13.73 YPT on 15 tgts (league 11.28, +2.45), 6 catches of 20+
- depth/direction deep_middle: 18.46 YPT on 13 tgts (league 14.9, +3.56), 7 catches of 20+
- depth/direction deep_right: 16.0 YPT on 13 tgts (league 11.85, +4.15), 4 catches of 20+
- receiver archetype intermediate (aDOT 8-13): 10.47 YPT on 89 tgts (league 7.96, +2.51), 15 catches of 20+

Holds (-1.5 YPT or better): RB: 3.09 YPT on 46 tgts (league 5.61, -2.52)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 46 | 34 | 142 | 0 | 0 | 3.09 | 5.80 | 17.80 | 5.61 | -2.52 |
| TE1 | 32 | 22 | 250 | 5 | 4 | 7.81 | 4 | 31.20 | 7.39 | 0.42 |
| TE2+ | 18 | 13 | 122 | 1 | 0 | 6.78 | 2.20 | 15.20 | 6.71 | 0.07 |
| WR1 | 64 | 45 | 725 | 2 | 12 | 11.33 | 8 | 90.60 | 8.16 | 3.17 |
| WR2 | 49 | 33 | 354 | 2 | 3 | 7.22 | 6.10 | 44.20 | 8.20 | -0.98 |
| WR3+ | 42 | 24 | 342 | 1 | 5 | 8.14 | 5.20 | 42.80 | 7.67 | 0.47 |
| other | 1 | 0 | 0 | 0 | 0 | 0 | 0.10 | 0 | 2.86 | -2.86 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 24 | 17 | 105 | 0 | 0 | 4.38 | 5.61 | -1.23 |
| TE1 | 16 | 11 | 143 | 3 | 2 | 8.94 | 7.39 | 1.55 |
| TE2+ | 13 | 9 | 84 | 1 | 0 | 6.46 | 6.71 | -0.25 |
| WR1 | 29 | 19 | 345 | 1 | 5 | 11.90 | 8.16 | 3.74 |
| WR2 | 20 | 12 | 157 | 1 | 2 | 7.85 | 8.20 | -0.35 |
| WR3+ | 18 | 12 | 185 | 1 | 3 | 10.28 | 7.67 | 2.61 |
| other | 1 | 0 | 0 | 0 | 0 | 0 | 2.86 | -2.86 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 55 | 43 | 231 | 1 | 2 | 4.20 | 4.58 | -0.38 |
| short_1-9 | 113 | 77 | 665 | 5 | 4 | 5.88 | 6.23 | -0.35 |
| inter_10-19 | 55 | 38 | 605 | 3 | 5 | 11 | 10.17 | 0.83 |
| deep_20+ | 26 | 13 | 434 | 2 | 13 | 16.69 | 12.32 | 4.37 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 15 | 7 | 206 | 1 | 6 | 13.73 | 11.28 | 2.45 |
| deep_middle | 13 | 8 | 240 | 1 | 7 | 18.46 | 14.90 | 3.56 |
| deep_right | 13 | 8 | 208 | 1 | 4 | 16 | 11.85 | 4.15 |
| short_left | 78 | 56 | 462 | 2 | 1 | 5.92 | 6.08 | -0.16 |
| short_middle | 48 | 31 | 335 | 3 | 2 | 6.98 | 7.43 | -0.45 |
| short_right | 82 | 61 | 484 | 3 | 4 | 5.90 | 5.95 | -0.05 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 36 | 19 | 371 | 2 | 5 | 10.31 | 8.94 | 1.37 |
| intermediate (aDOT 8-13) | 89 | 64 | 932 | 4 | 15 | 10.47 | 7.96 | 2.51 |
| short/YAC (aDOT <8) | 127 | 88 | 632 | 5 | 4 | 4.98 | 6.47 | -1.49 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'TE': 4, 'WR': 20} (24 total, 3.0/g)
- Pass 20+ by depth/direction: {'deep_left': 6, 'deep_middle': 7, 'deep_right': 4, 'short_left': 1, 'short_middle': 2, 'short_right': 4}
- Rush 15+ by position: {'QB': 1, 'RB': 9} (10 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 36 | 153 | 1 | 4.25 | 19.10 |
| RB | 176 | 658 | 9 | 3.74 | 82.20 |
| WR | 5 | 16 | 0 | 3.20 | 2 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Marlon Humphrey | CB | 8 | 79.60 | 29 | 3.60 | 22 | 320 | 40 | 11.03 | 0 | 5 | 7 | 0 | 0 |
| Nate Wiggins | CB | 6 | 94.60 | 20 | 3.30 | 16 | 161 | 26.80 | 8.05 | 0 | 2 | 4 | 0 | 0 |
| Keyon Martin | CB | 4 | 26.40 | 7 | 1.80 | 6 | 71 | 17.80 | 10.14 | 0 | 1 | 1 | 0 | 0 |
| Chandler Rivers | CB | 4 | 38.20 | 6 | 1.50 | 6 | 55 | 13.80 | 9.17 | 0 | 1 | 0 | 0 | 0 |
| Chidobe Awuzie | CB | 3 | 23 | 6 | 2 | 4 | 37 | 12.30 | 6.17 | 0 | 0 | 2 | 0 | 0 |
| T.J. Tampa | CB | 1 | 27 | 1 | 1 | 1 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |
| Roquan Smith | LB | 8 | 93.80 | 20 | 2.50 | 17 | 174 | 21.80 | 8.70 | 0 | 1 | 2 | 1 | 0 |
| Trenton Simpson | LB | 7 | 61.50 | 14 | 2 | 13 | 95 | 13.60 | 6.79 | 0 | 0 | 0 | 1 | 0 |
| Kyle Hamilton | S | 8 | 96.60 | 27 | 3.40 | 23 | 229 | 28.60 | 8.48 | 0 | 4 | 3 | 1 | 0 |
| Jaylinn Hawkins | S | 6 | 81.30 | 15 | 2.50 | 15 | 216 | 36 | 14.40 | 0 | 2 | 0 | 0 | 0 |
| Malaki Starks | S | 6 | 97.80 | 16 | 2.70 | 15 | 204 | 34 | 12.75 | 0 | 4 | 1 | 0 | 0 |
| K'Von Wallace | S | 2 | 30.70 | 4 | 2 | 4 | 70 | 35 | 17.50 | 0 | 1 | 0 | 0 | 0 |
| Keondre Jackson | S | 2 | 18.70 | 2 | 1 | 2 | 48 | 24 | 24 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Marlon Humphrey** (CB): WR1:11t/137y, WR3+:8t/120y, WR2:8t/47y, RB:2t/16y | 20+: wk2 C.Olave(WR1) 20 deep_left; wk3 C.Lamb(WR1) 49 deep_left; wk5 Z.Branch(WR3+) 23 short_right; wk8 K.Shakir(WR1) 26 short_right; wk8 D.Moore(WR3+) 49 deep_middle
- **Nate Wiggins** (CB): WR2:7t/58y, WR1:3t/54y, TE1:1t/25y, RB:5t/14y, TE2+:1t/9y, WR3+:3t/1y | 20+: wk2 J.Johnson(TE1) 25 short_right; wk7 T.Higgins(WR1) 43 deep_right
- **Keyon Martin** (CB): WR1:3t/61y, WR2:2t/8y, TE1:1t/2y, RB:1t/0y | 20+: wk7 T.Higgins(WR1) 44 deep_middle
- **Chandler Rivers** (CB): WR2:1t/36y, TE1:2t/15y, WR3+:1t/9y, RB:2t/-5y | 20+: wk5 J.Dotson(WR2) 36 deep_right
- **Chidobe Awuzie** (CB): WR1:3t/35y, RB:1t/2y, TE1:1t/0y, WR3+:1t/0y
- **T.J. Tampa** (CB): WR3+:1t/4y
- **Roquan Smith** (LB): WR3+:6t/66y, RB:7t/47y, WR1:3t/22y, WR2:2t/22y, TE2+:2t/17y | 20+: wk1 A.Pierce(WR3+) 23 deep_middle
- **Trenton Simpson** (LB): WR1:3t/32y, TE2+:3t/23y, RB:6t/17y, TE1:1t/16y, WR3+:1t/7y
- **Kyle Hamilton** (S): WR1:11t/137y, TE1:4t/26y, WR3+:1t/22y, WR2:4t/20y, RB:6t/15y, TE2+:1t/9y | 20+: wk1 J.Downs(WR1) 25 short_middle; wk4 C.Tate(WR1) 22 deep_left; wk4 E.Ayomanor(WR3+) 22 deep_middle; wk4 C.Tate(WR1) 33 deep_right
- **Jaylinn Hawkins** (S): WR2:5t/90y, WR1:3t/42y, WR3+:3t/40y, TE1:2t/27y, RB:1t/9y, TE2+:1t/8y | 20+: wk2 D.Vele(WR2) 29 deep_middle; wk2 J.Johnson(TE1) 25 short_right
- **Malaki Starks** (S): WR1:7t/121y, WR3+:3t/55y, WR2:2t/16y, TE2+:1t/8y, TE1:2t/6y, RB:1t/-2y | 20+: wk4 C.Tate(WR1) 33 deep_left; wk5 D.London(WR1) 25 deep_right; wk5 D.London(WR1) 20 short_middle; wk6 J.Jeudy(WR3+) 33 deep_middle
- **K'Von Wallace** (S): TE1:1t/40y, WR1:1t/19y, RB:2t/11y | 20+: wk8 D.Kincaid(TE1) 40 deep_left
- **Keondre Jackson** (S): WR2:1t/30y, RB:1t/18y | 20+: wk7 J.Chase(WR2) 30 short_left

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BAL@IND | Roquan Smith | LB | 7 | 6 | 49 | 0 | 1 | 0 | 1 | 0 | J.Taylorx2, A.Piercex2, L.Treadwellx1, S.McGowanx1, K.Allenx1 |
| 1 | BAL@IND | Marlon Humphrey | CB | 5 | 4 | 42 | 0 | 0 | 1 | 0 | 0 | A.Piercex3, J.Taylorx1, K.Allenx1 |
| 1 | BAL@IND | Kyle Hamilton | S | 2 | 2 | 32 | 0 | 1 | 0 | 0 | 0 | K.Allenx1, J.Downsx1 |
| 1 | BAL@IND | Keyon Martin | CB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | J.Downsx1, T.Warrenx1 |
| 1 | BAL@IND | Nate Wiggins | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | K.Allenx1, A.Piercex1 |
| 1 | BAL@IND | Jaylinn Hawkins | S | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | T.Warrenx1 |
| 2 | NO@BAL | Jaylinn Hawkins | S | 2 | 2 | 54 | 0 | 2 | 0 | 0 | 0 | D.Velex1, J.Johnsonx1 |
| 2 | NO@BAL | Nate Wiggins | CB | 4 | 4 | 39 | 0 | 1 | 0 | 0 | 0 | A.Kamarax2, C.Olavex1, J.Johnsonx1 |
| 2 | NO@BAL | Marlon Humphrey | CB | 5 | 4 | 37 | 0 | 1 | 1 | 0 | 0 | C.Olavex3, B.Lancex1, D.Velex1 |
| 2 | NO@BAL | Kyle Hamilton | S | 5 | 5 | 34 | 0 | 0 | 0 | 0 | 0 | D.Velex2, C.Olavex2, T.Etiennex1 |
| 2 | NO@BAL | Malaki Starks | S | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | O.Delpx1, C.Olavex1, J.Johnsonx1 |
| 2 | NO@BAL | Roquan Smith | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | A.Kamarax1, T.Etiennex1 |
| 2 | NO@BAL | Chandler Rivers | CB | 2 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | J.Johnsonx1, A.Kamarax1 |
| 2 | NO@BAL | Trenton Simpson | LB | 2 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | A.Kamarax1, C.Olavex1 |
| 3 | BAL@DAL | Marlon Humphrey | CB | 6 | 5 | 86 | 0 | 1 | 1 | 0 | 0 | C.Lambx4, G.Pickensx2 |
| 3 | BAL@DAL | Jaylinn Hawkins | S | 3 | 3 | 42 | 0 | 0 | 0 | 0 | 0 | G.Pickensx2, R.Flournoyx1 |
| 3 | BAL@DAL | Malaki Starks | S | 3 | 3 | 34 | 0 | 0 | 0 | 0 | 0 | C.Lambx2, K.Turpinx1 |
| 3 | BAL@DAL | Nate Wiggins | CB | 5 | 4 | 22 | 0 | 0 | 1 | 0 | 0 | G.Pickensx3, J.Williamsx2 |
| 3 | BAL@DAL | Roquan Smith | LB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | G.Pickensx1 |
| 3 | BAL@DAL | Kyle Hamilton | S | 4 | 2 | 15 | 0 | 0 | 2 | 0 | 0 | J.Fergusonx2, L.Schoonmakerx1, J.Williamsx1 |
| 3 | BAL@DAL | Chidobe Awuzie | CB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | C.Lambx1 |
| 3 | BAL@DAL | Chandler Rivers | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | R.Flournoyx1 |
| 3 | BAL@DAL | Trenton Simpson | LB | 1 | 1 | -5 | 0 | 0 | 0 | 0 | 0 | T.Goodsonx1 |
| 4 | TEN@BAL | Kyle Hamilton | S | 6 | 5 | 91 | 0 | 3 | 1 | 0 | 0 | C.Tatex5, E.Ayomanorx1 |
| 4 | TEN@BAL | Malaki Starks | S | 4 | 4 | 55 | 0 | 1 | 0 | 0 | 0 | W.Robinsonx2, C.Tatex2 |
| 4 | TEN@BAL | Chidobe Awuzie | CB | 4 | 3 | 26 | 0 | 0 | 1 | 0 | 0 | C.Tatex2, C.Ridleyx1, T.Pollardx1 |
| 4 | TEN@BAL | Marlon Humphrey | CB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | C.Dikex1 |
| 4 | TEN@BAL | Roquan Smith | LB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | C.Tatex1 |
| 4 | TEN@BAL | Jaylinn Hawkins | S | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | C.Ridleyx1 |
| 4 | TEN@BAL | Chandler Rivers | CB | 2 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | T.Spearsx1, G.Helmx1 |
| 4 | TEN@BAL | Trenton Simpson | LB | 2 | 1 | 2 | 0 | 0 | 0 | 1 | 0 | T.Pollardx1, D.Bellingerx1 |
| 5 | BAL@ATL | Marlon Humphrey | CB | 3 | 3 | 45 | 0 | 1 | 0 | 0 | 0 | Bi.Robinsonx1, D.Londonx1, Z.Branchx1 |
| 5 | BAL@ATL | Malaki Starks | S | 2 | 2 | 45 | 0 | 2 | 0 | 0 | 0 | D.Londonx2 |
| 5 | BAL@ATL | Chandler Rivers | CB | 1 | 1 | 36 | 0 | 1 | 0 | 0 | 0 | J.Dotsonx1 |
| 5 | BAL@ATL | Trenton Simpson | LB | 3 | 3 | 29 | 0 | 0 | 0 | 0 | 0 | Bi.Robinsonx1, D.Londonx1, C.Woernerx1 |
| 5 | BAL@ATL | Kyle Hamilton | S | 3 | 2 | 28 | 0 | 0 | 0 | 1 | 0 | D.Londonx2, K.Pittsx1 |
| 5 | BAL@ATL | Jaylinn Hawkins | S | 2 | 2 | 27 | 0 | 0 | 0 | 0 | 0 | D.Londonx2 |
| 5 | BAL@ATL | Roquan Smith | LB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | Bi.Robinsonx2 |
| 5 | BAL@ATL | Nate Wiggins | CB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | Z.Branchx1, J.Dotsonx1 |
| 6 | BAL@CLE | Jaylinn Hawkins | S | 6 | 6 | 78 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx2, J.Jeudyx1, D.Bostonx1, B.Whiteheartx1, J.McLaughlinx1 |
| 6 | BAL@CLE | Malaki Starks | S | 3 | 2 | 46 | 0 | 1 | 1 | 0 | 0 | J.Jeudyx2, H.Fanninx1 |
| 6 | BAL@CLE | Roquan Smith | LB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | T.Wallacex1 |
| 6 | BAL@CLE | Nate Wiggins | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | J.Jeudyx1, D.Bostonx1 |
| 6 | BAL@CLE | Keyon Martin | CB | 3 | 2 | 8 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx2, J.McLaughlinx1 |
| 6 | BAL@CLE | Trenton Simpson | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | J.McLaughlinx1 |
| 6 | BAL@CLE | Marlon Humphrey | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | D.Bostonx2 |
| 6 | BAL@CLE | Kyle Hamilton | S | 2 | 2 | -2 | 0 | 0 | 0 | 0 | 0 | J.McLaughlinx1, K.Concepcionx1 |
| 7 | CIN@BAL | Nate Wiggins | CB | 5 | 4 | 72 | 0 | 1 | 1 | 0 | 0 | J.Chasex2, E.Allx1, C.Brownx1, T.Higginsx1 |
| 7 | CIN@BAL | Keyon Martin | CB | 1 | 1 | 44 | 0 | 1 | 0 | 0 | 0 | T.Higginsx1 |
| 7 | CIN@BAL | Trenton Simpson | LB | 3 | 3 | 34 | 0 | 0 | 0 | 0 | 0 | M.Tinsleyx1, T.Higginsx1, D.Samplex1 |
| 7 | CIN@BAL | K'Von Wallace | S | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | C.Brownx2, T.Higginsx1 |
| 7 | CIN@BAL | Keondre Jackson | S | 1 | 1 | 30 | 0 | 1 | 0 | 0 | 0 | J.Chasex1 |
| 7 | CIN@BAL | Roquan Smith | LB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | E.Allx2 |
| 7 | CIN@BAL | Marlon Humphrey | CB | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | J.Chasex3 |
| 7 | CIN@BAL | Kyle Hamilton | S | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | C.Brownx1, T.Higginsx1 |
| 8 | BAL@BUF | Marlon Humphrey | CB | 4 | 3 | 79 | 0 | 2 | 1 | 0 | 0 | D.Moorex2, K.Shakirx1, K.Colemanx1 |
| 8 | BAL@BUF | K'Von Wallace | S | 1 | 1 | 40 | 0 | 1 | 0 | 0 | 0 | D.Kincaidx1 |
| 8 | BAL@BUF | Trenton Simpson | LB | 2 | 2 | 28 | 0 | 0 | 0 | 0 | 0 | D.Kincaidx1, J.Cookx1 |
| 8 | BAL@BUF | Roquan Smith | LB | 4 | 2 | 27 | 0 | 0 | 2 | 0 | 0 | D.Moorex2, K.Shakirx2 |
| 8 | BAL@BUF | Kyle Hamilton | S | 3 | 3 | 19 | 0 | 0 | 0 | 0 | 0 | D.Kincaidx1, J.Cookx1, T.Johnsonx1 |
| 8 | BAL@BUF | Keondre Jackson | S | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1 |
| 8 | BAL@BUF | Keyon Martin | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | K.Shakirx1 |
| 8 | BAL@BUF | T.J. Tampa | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | D.Moorex1 |
| 8 | BAL@BUF | Chidobe Awuzie | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Kincaidx1 |
| 8 | BAL@BUF | Malaki Starks | S | 1 | 1 | -2 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1 |

## Who beat them each week

**Wk1 BAL@IND** (vs IND offense, 166 rec yds allowed; 24% of targets unattributed)
- Top receivers: A.Pierce (WR3+, deep (aDOT 13+)) 4/6 61y; J.Downs (WR1, intermediate (aDOT 8-13)) 2/4 37y; K.Allen (WR2, short/YAC (aDOT <8)) 6/6 32y; J.Taylor (RB, short/YAC (aDOT <8)) 3/4 23y
- 20+ catches: J.Downs(WR1) 25y short_middle - K.Hamilton [tackler]; A.Pierce(WR3+) 23y deep_middle - R.Smith [tackler]
- 15+ runs: J.Taylor(RB) 18y rush left tackle; J.Taylor(RB) 21y rush right tackle

**Wk2 NO@BAL** (vs NO offense, 252 rec yds allowed; 19% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 8/10 86y 1TD; J.Johnson (TE1, short/YAC (aDOT <8)) 4/4 66y; D.Vele (WR2, intermediate (aDOT 8-13)) 5/7 64y; B.Lance (WR3+, intermediate (aDOT 8-13)) 1/1 8y
- 20+ catches: C.Olave(WR1) 20y deep_left - M.Humphrey [tackler]; D.Vele(WR2) 29y deep_middle - J.Hawkins [tackler]; J.Johnson(TE1) 25y short_right - N.Wiggins [tackler]; C.Olave(WR1) 21y deep_middle TD - no tackler named [unattributed]; J.Johnson(TE1) 25y short_right - J.Hawkins [tackler]

**Wk3 BAL@DAL** (vs DAL offense, 276 rec yds allowed; 32% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 7/9 112y; G.Pickens (WR2, intermediate (aDOT 8-13)) 7/11 82y; J.Ferguson (TE1, short/YAC (aDOT <8)) 3/5 23y 1TD; R.Flournoy (WR3+, short/YAC (aDOT <8)) 2/8 22y
- 20+ catches: C.Lamb(WR1) 49y deep_left - M.Humphrey [tackler]
- 15+ runs: J.Williams(RB) 17y rush left tackle; J.Williams(RB) 22y rush left tackle; J.Williams(RB) 15y rush left tackle

**Wk4 TEN@BAL** (vs TEN offense, 222 rec yds allowed; 24% of targets unattributed)
- Top receivers: C.Tate (WR1, intermediate (aDOT 8-13)) 9/12 145y; E.Ayomanor (WR3+, intermediate (aDOT 8-13)) 1/1 22y; W.Robinson (WR2, short/YAC (aDOT <8)) 3/5 19y 1TD; C.Dike (WR3+, intermediate (aDOT 8-13)) 1/1 15y
- 20+ catches: C.Tate(WR1) 22y deep_left - K.Hamilton [tackler]; E.Ayomanor(WR3+) 22y deep_middle - K.Hamilton [tackler]; C.Tate(WR1) 33y deep_right - K.Hamilton [tackler]; C.Tate(WR1) 33y deep_left - M.Starks [tackler]
- 15+ runs: C.Ward(QB) 22y rush right end

**Wk5 BAL@ATL** (vs ATL offense, 274 rec yds allowed; 35% of targets unattributed)
- Top receivers: D.London (WR1, intermediate (aDOT 8-13)) 7/11 118y; J.Dotson (WR2, deep (aDOT 13+)) 2/4 54y; K.Pitts (TE1, short/YAC (aDOT <8)) 5/6 42y 1TD; Bi.Robinson (RB, short/YAC (aDOT <8)) 4/7 32y
- 20+ catches: D.London(WR1) 25y deep_right - M.Starks [tackler]; J.Dotson(WR2) 36y deep_right - C.Rivers [tackler]; Z.Branch(WR3+) 23y short_right - M.Humphrey [tackler]; D.London(WR1) 20y short_middle - M.Starks [tackler]
- 15+ runs: Bi.Robinson(RB) 20y rush left guard; Bi.Robinson(RB) 38y rush left tackle

**Wk6 BAL@CLE** (vs CLE offense, 164 rec yds allowed; 16% of targets unattributed)
- Top receivers: J.Jeudy (WR3+, intermediate (aDOT 8-13)) 4/4 69y; K.Concepcion (WR2, short/YAC (aDOT <8)) 4/6 37y; D.Boston (WR1, deep (aDOT 13+)) 1/5 15y; J.McLaughlin (RB, short/YAC (aDOT <8)) 4/4 14y
- 20+ catches: J.Jeudy(WR3+) 33y deep_middle - M.Starks [tackler]

**Wk7 CIN@BAL** (vs CIN offense, 292 rec yds allowed; 28% of targets unattributed)
- Top receivers: T.Higgins (WR1, deep (aDOT 13+)) 6/7 148y 1TD; J.Chase (WR2, intermediate (aDOT 8-13)) 5/7 62y 1TD; E.All (TE2+, short/YAC (aDOT <8)) 3/3 26y; D.Sample (TE2+, short/YAC (aDOT <8)) 2/2 24y 1TD
- 20+ catches: T.Higgins(WR1) 44y deep_middle - K.Martin [tackler]; J.Chase(WR2) 30y short_left - K.Jackson [tackler]; T.Higgins(WR1) 43y deep_right - N.Wiggins [tackler]
- 15+ runs: S.Perine(RB) 15y rush left tackle

**Wk8 BAL@BUF** (vs BUF offense, 289 rec yds allowed; 28% of targets unattributed)
- Top receivers: D.Kincaid (TE1, intermediate (aDOT 8-13)) 4/6 86y 1TD; D.Moore (WR3+, deep (aDOT 13+)) 4/7 82y 1TD; K.Shakir (WR1, short/YAC (aDOT <8)) 5/6 64y; J.Cook (RB, short/YAC (aDOT <8)) 2/3 21y
- 20+ catches: K.Shakir(WR1) 26y short_right - M.Humphrey [tackler]; D.Moore(WR3+) 49y deep_middle - M.Humphrey [tackler]; D.Kincaid(TE1) 40y deep_left - K.Wallace [tackler]; D.Kincaid(TE1) 23y deep_left TD - no tackler named [unattributed]
- 15+ runs: J.Cook(RB) 16y rush middle

## Seed notes from defenders/BAL_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 13:43 Khalil Shakir (WR) rec 26 — Keyon Martin [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Kyle Hamilton)]; alignment: slot (middle-target proxy) (pregame target-side proxy; ESPN season split L18/S67/R15)
- Q2 4:22 James Cook (RB) rush 16 — T.Tampa [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 9:44 Denarius Moore (WR) rec 49 — Marlon Humphrey [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L36/S26/R39)
- Q4 13:45 Dalton Kincaid (TE) rec 40 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q4 5:58 Dalton Kincaid (TE) rec 23 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Marlon Humphrey ← Denarius Moore: 6 tgt, 3 rec, 72 yds
- Keyon Martin ← Khalil Shakir: 6 tgt, 5 rec, 65 yds
- Nate Wiggins ← Keon Coleman: 3 tgt, 1 rec, 4 yds — limited his man


## TNF JAX@BAL 2026-11-05 (Week 10) — live log (tackler/PBU tag, not true coverage)
Final **JAX 33 – BAL 10**. Source: `live/2026-11-05_JAX_BAL/pbp_live.csv` + box reconcile. Hawkins OUT; Wiggins inactive → Awuzie up. Fagnano started for BAL (not relevant to this D file except opponent script).

**Vs JAX offense (242 pass yds, 1 pass TD, 0 INT forced by BAL; Lawrence 16/26):**
- Top receivers allowed: J.Meyers 4/6 65 (long 18); P.Washington 2/7 61 1TD (50-yd); N.Boerkircher 2/3 61 (52-yd); B.Strange 2/2 22; T.Koziol 2/2 15.
- Explosives allowed (pass20 / 15+ / 40+): Boerkircher 52 (M.Humphrey tackler), Washington 50 TD (unattributed), Meyers 16 (C.Awuzie), Meyers 17 (K.Hamilton), Meyers 18 (T.Tampa), Strange 15 (M.Starks). **No rush10+ allowed.**
- Tackler-after-catch totals (ledger): M.Humphrey 3/70 (Boerkircher 52, Strange 7, Koziol 11); K.Hamilton 2/28 (Meyers 17, Washington 11); K.Wallace 2/19; T.Tampa 1/18; C.Awuzie 1/16; M.Starks 1/15; R.Smith 2/15; T.Buchanan 1/8; T.Simpson 1/4.
- Note: Strange volume low (2 targets) despite Hawkins OUT / middle-seam prior; chunk TE play was Boerkircher. Washington cleared 40+ but missed main o63.5 (61).
