# WSH DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 WSH@PHI, wk2 WSH@DAL, wk3 SEA@WSH, wk4 IND@WSH, wk5 NYG@WSH, wk6 WSH@SF, wk8 PHI@WSH). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 12.9% / Zone 76.9% | MOF closed 29.6% / MOF open 62.8% | Blitz 42.5% | Light box 38.1% / Heavy box 24.7% | Sub package 50.0% | Sharp YPT allowed WR 8.1, TE 9.0, RB 5.2, Outside 9.6, Slot 6.6

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- depth/direction deep_right: 17.95 YPT on 20 tgts (league 11.85, +6.1), 8 catches of 20+
- receiver archetype deep (aDOT 13+): 10.7 YPT on 23 tgts (league 8.94, +1.76), 4 catches of 20+

Holds (-1.5 YPT or better): WR2: 6.68 YPT on 19 tgts (league 8.2, -1.52)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 50 | 36 | 253 | 0 | 3 | 5.06 | 7.10 | 36.10 | 5.61 | -0.55 |
| TE1 | 48 | 38 | 423 | 7 | 3 | 8.81 | 6.90 | 60.40 | 7.39 | 1.42 |
| TE2+ | 8 | 6 | 101 | 1 | 2 | 12.62 | 1.10 | 14.40 | 6.71 | 5.91 |
| WR1 | 65 | 44 | 564 | 5 | 11 | 8.68 | 9.30 | 80.60 | 8.16 | 0.52 |
| WR2 | 19 | 13 | 127 | 0 | 1 | 6.68 | 2.70 | 18.10 | 8.20 | -1.52 |
| WR3+ | 50 | 31 | 352 | 2 | 3 | 7.04 | 7.10 | 50.30 | 7.67 | -0.63 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 34 | 24 | 153 | 0 | 2 | 4.50 | 5.61 | -1.11 |
| TE1 | 30 | 25 | 234 | 3 | 1 | 7.80 | 7.39 | 0.41 |
| TE2+ | 6 | 5 | 88 | 0 | 2 | 14.67 | 6.71 | 7.96 |
| WR1 | 38 | 23 | 288 | 1 | 5 | 7.58 | 8.16 | -0.58 |
| WR2 | 2 | 2 | 20 | 0 | 0 | 10 | 8.20 | 1.80 |
| WR3+ | 32 | 17 | 162 | 0 | 2 | 5.06 | 7.67 | -2.61 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 53 | 40 | 238 | 0 | 2 | 4.49 | 4.58 | -0.09 |
| short_1-9 | 107 | 81 | 615 | 7 | 1 | 5.75 | 6.23 | -0.48 |
| inter_10-19 | 50 | 35 | 583 | 7 | 8 | 11.66 | 10.17 | 1.49 |
| deep_20+ | 30 | 12 | 384 | 1 | 12 | 12.80 | 12.32 | 0.48 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 12 | 5 | 102 | 0 | 4 | 8.50 | 11.28 | -2.78 |
| deep_middle | 11 | 6 | 129 | 1 | 4 | 11.73 | 14.90 | -3.17 |
| deep_right | 20 | 11 | 359 | 2 | 8 | 17.95 | 11.85 | 6.10 |
| short_left | 79 | 53 | 435 | 4 | 2 | 5.51 | 6.08 | -0.57 |
| short_middle | 45 | 35 | 383 | 5 | 2 | 8.51 | 7.43 | 1.08 |
| short_right | 73 | 58 | 412 | 3 | 3 | 5.64 | 5.95 | -0.31 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 23 | 13 | 246 | 1 | 4 | 10.70 | 8.94 | 1.76 |
| intermediate (aDOT 8-13) | 89 | 60 | 728 | 6 | 10 | 8.18 | 7.96 | 0.22 |
| short/YAC (aDOT <8) | 128 | 95 | 846 | 8 | 9 | 6.61 | 6.47 | 0.14 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 3, 'TE': 5, 'WR': 15} (23 total, 3.3/g)
- Pass 20+ by depth/direction: {'deep_left': 4, 'deep_middle': 4, 'deep_right': 8, 'short_left': 2, 'short_middle': 2, 'short_right': 3}
- Rush 15+ by position: {'QB': 3, 'RB': 2} (5 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 27 | 167 | 3 | 6.19 | 23.90 |
| RB | 146 | 530 | 2 | 3.63 | 75.70 |
| TE | 1 | 2 | 0 | 2 | 0.30 |
| WR | 1 | 1 | 0 | 1 | 0.10 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Amik Robertson | CB | 7 | 98.90 | 37 | 5.30 | 29 | 269 | 38.40 | 7.27 | 0 | 4 | 8 | 0 | 0 |
| Rasul Douglas | CB | 7 | 61.30 | 26 | 3.70 | 20 | 147 | 21 | 5.65 | 0 | 1 | 4 | 2 | 0 |
| Trey Amos | CB | 2 | 72.50 | 7 | 3.50 | 5 | 95 | 47.50 | 13.57 | 0 | 3 | 2 | 0 | 0 |
| Mike Sainristil | CB | 3 | 47.70 | 7 | 2.30 | 7 | 66 | 22 | 9.43 | 0 | 0 | 0 | 0 | 0 |
| Fabian Moreau | CB | 2 | 32.70 | 6 | 3 | 5 | 39 | 19.50 | 6.50 | 0 | 0 | 1 | 0 | 0 |
| Sonny Styles | LB | 5 | 92.10 | 19 | 3.80 | 15 | 106 | 21.20 | 5.58 | 1 | 0 | 3 | 1 | 0 |
| Frankie Luvu | LB | 4 | 89.20 | 9 | 2.20 | 8 | 38 | 9.50 | 4.22 | 0 | 0 | 1 | 0 | 0 |
| K'Lavon Chaisson | OLB | 5 | 69.30 | 6 | 1.20 | 6 | 83 | 16.60 | 13.83 | 0 | 1 | 0 | 0 | 0 |
| Jeremy Reaves | S | 7 | 91 | 21 | 3 | 18 | 265 | 37.90 | 12.62 | 0 | 4 | 3 | 0 | 0 |
| Quan Martin | S | 7 | 63.30 | 15 | 2.10 | 15 | 237 | 33.90 | 15.80 | 0 | 4 | 0 | 0 | 0 |
| Nick Cross | S | 4 | 96.80 | 7 | 1.80 | 7 | 111 | 27.80 | 15.86 | 0 | 2 | 0 | 0 | 0 |
| Percy Butler | S | 1 | 24 | 1 | 1 | 1 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Amik Robertson** (CB): WR1:11t/107y, WR3+:10t/59y, RB:8t/50y, TE1:6t/40y, WR2:2t/13y | 20+: wk2 C.Lamb(WR1) 23 deep_middle; wk4 A.Dulin(WR3+) 23 short_right; wk5 M.Nabers(WR1) 20 deep_left; wk6 M.Evans(WR1) 24 deep_middle
- **Rasul Douglas** (CB): TE1:6t/45y, WR2:4t/44y, WR3+:9t/30y, RB:4t/16y, WR1:3t/12y | 20+: wk1 D.Smith(WR2) 31 deep_right
- **Trey Amos** (CB): TE2+:2t/46y, WR1:3t/27y, WR3+:2t/22y | 20+: wk6 J.Watkins(WR3+) 22 deep_left; wk8 M.Lemon(WR1) 20 deep_left; wk8 E.Stowers(TE2+) 34 short_left
- **Mike Sainristil** (CB): WR3+:3t/32y, WR2:3t/30y, RB:1t/4y
- **Fabian Moreau** (CB): WR1:3t/19y, WR3+:2t/13y, WR2:1t/7y
- **Sonny Styles** (LB): TE1:5t/38y, RB:7t/29y, WR1:6t/26y, TE2+:1t/13y
- **Frankie Luvu** (LB): WR1:2t/15y, TE1:3t/9y, RB:2t/7y, TE2+:1t/7y, WR3+:1t/0y
- **K'Lavon Chaisson** (OLB): TE1:2t/36y, RB:3t/32y, WR1:1t/15y | 20+: wk3 A.Barner(TE1) 32 short_right
- **Jeremy Reaves** (S): WR3+:5t/94y, WR1:5t/73y, TE1:7t/41y, RB:2t/27y, TE2+:1t/21y, WR2:1t/9y | 20+: wk1 D.Wicks(WR3+) 64 deep_right; wk3 J.Smith-Njigba(WR1) 20 deep_middle; wk5 T.Tracy(RB) 21 short_right; wk5 T.Johnson(TE2+) 21 short_middle
- **Quan Martin** (S): WR3+:6t/77y, WR1:4t/67y, TE1:2t/47y, RB:1t/20y, TE2+:1t/14y, WR2:1t/12y | 20+: wk2 C.Lamb(WR1) 35 deep_right; wk3 B.Russell(RB) 20 short_left; wk5 M.Nabers(WR1) 28 deep_middle; wk6 G.Kittle(TE1) 35 deep_right
- **Nick Cross** (S): WR1:4t/93y, TE1:1t/12y, WR3+:1t/9y, RB:1t/-3y | 20+: wk2 C.Lamb(WR1) 38 deep_right; wk6 M.Evans(WR1) 54 deep_right
- **Percy Butler** (S): WR1:1t/12y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WSH@PHI | Jeremy Reaves | S | 1 | 1 | 64 | 0 | 1 | 0 | 0 | 0 | D.Wicksx1 |
| 1 | WSH@PHI | Rasul Douglas | CB | 2 | 1 | 31 | 0 | 1 | 1 | 0 | 0 | D.Wicksx1, D.Smithx1 |
| 1 | WSH@PHI | Amik Robertson | CB | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1, D.Goedertx1, W.Shipleyx1, D.Smithx1 |
| 1 | WSH@PHI | Quan Martin | S | 2 | 2 | 9 | 0 | 0 | 0 | 0 | 0 | D.Smithx1, M.Lemonx1 |
| 1 | WSH@PHI | Nick Cross | S | 3 | 3 | 4 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1, D.Goedertx1, S.Barkleyx1 |
| 2 | WSH@DAL | Amik Robertson | CB | 6 | 4 | 45 | 0 | 1 | 2 | 0 | 0 | C.Lambx3, R.Flournoyx1, G.Pickensx1, J.Fergusonx1 |
| 2 | WSH@DAL | Quan Martin | S | 2 | 2 | 40 | 0 | 1 | 0 | 0 | 0 | R.Flournoyx1, C.Lambx1 |
| 2 | WSH@DAL | Nick Cross | S | 1 | 1 | 38 | 0 | 1 | 0 | 0 | 0 | C.Lambx1 |
| 2 | WSH@DAL | Mike Sainristil | CB | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | R.Flournoyx2, G.Pickensx1 |
| 2 | WSH@DAL | Jeremy Reaves | S | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | C.Lambx1, R.Flournoyx1, G.Pickensx1 |
| 2 | WSH@DAL | K'Lavon Chaisson | OLB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | C.Lambx1 |
| 2 | WSH@DAL | Sonny Styles | LB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | J.Williamsx1 |
| 2 | WSH@DAL | Rasul Douglas | CB | 3 | 3 | 4 | 0 | 0 | 0 | 0 | 0 | G.Pickensx2, R.Flournoyx1 |
| 3 | SEA@WSH | Quan Martin | S | 4 | 4 | 68 | 0 | 1 | 0 | 0 | 0 | T.Hortonx3, B.Russellx1 |
| 3 | SEA@WSH | Jeremy Reaves | S | 5 | 4 | 63 | 0 | 1 | 1 | 0 | 0 | J.Smith-Njigbax2, G.Holanix1, C.Kuppx1, A.Barnerx1 |
| 3 | SEA@WSH | K'Lavon Chaisson | OLB | 2 | 2 | 45 | 0 | 1 | 0 | 0 | 0 | A.Barnerx1, G.Holanix1 |
| 3 | SEA@WSH | Rasul Douglas | CB | 4 | 3 | 29 | 0 | 0 | 1 | 0 | 0 | A.Barnerx2, R.Shaheedx1, J.Pricex1 |
| 3 | SEA@WSH | Amik Robertson | CB | 8 | 4 | 28 | 0 | 0 | 4 | 0 | 0 | J.Smith-Njigbax3, A.Barnerx2, C.Kuppx2, G.Holanix1 |
| 3 | SEA@WSH | Sonny Styles | LB | 4 | 2 | 24 | 1 | 0 | 1 | 1 | 0 | J.Smith-Njigbax2, J.Pricex1, E.Saubertx1 |
| 3 | SEA@WSH | Mike Sainristil | CB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | C.Kuppx1, R.Shaheedx1 |
| 3 | SEA@WSH | Percy Butler | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | J.Smith-Njigbax1 |
| 4 | IND@WSH | Amik Robertson | CB | 7 | 6 | 58 | 0 | 1 | 1 | 0 | 0 | A.Dulinx2, L.Treadwellx2, J.Downsx1, T.Warrenx1, D.Burksx1 |
| 4 | IND@WSH | Jeremy Reaves | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | J.Downsx1, L.Treadwellx1 |
| 4 | IND@WSH | Rasul Douglas | CB | 4 | 3 | 15 | 0 | 0 | 0 | 1 | 0 | L.Treadwellx2, A.Dulinx2 |
| 4 | IND@WSH | Quan Martin | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | T.Warrenx1 |
| 4 | IND@WSH | Frankie Luvu | LB | 3 | 3 | 9 | 0 | 0 | 0 | 0 | 0 | T.Warrenx2, J.Taylorx1 |
| 4 | IND@WSH | K'Lavon Chaisson | OLB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | S.McGowanx1 |
| 4 | IND@WSH | Fabian Moreau | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | D.Burksx1 |
| 5 | NYG@WSH | Jeremy Reaves | S | 5 | 4 | 57 | 0 | 2 | 1 | 0 | 0 | I.Likelyx2, D.Mooneyx1, T.Tracyx1, T.Johnsonx1 |
| 5 | NYG@WSH | Rasul Douglas | CB | 9 | 8 | 56 | 0 | 0 | 1 | 0 | 0 | I.Likelyx3, M.Nabersx3, C.Skattebox2, D.Mooneyx1 |
| 5 | NYG@WSH | Quan Martin | S | 3 | 3 | 49 | 0 | 1 | 0 | 0 | 0 | M.Nabersx2, T.Johnsonx1 |
| 5 | NYG@WSH | Amik Robertson | CB | 4 | 3 | 44 | 0 | 1 | 1 | 0 | 0 | M.Nabersx2, I.Likelyx1, D.Mooneyx1 |
| 5 | NYG@WSH | Fabian Moreau | CB | 5 | 4 | 33 | 0 | 0 | 1 | 0 | 0 | M.Nabersx3, D.Mooneyx1, M.Fieldsx1 |
| 5 | NYG@WSH | Sonny Styles | LB | 4 | 3 | 21 | 0 | 0 | 1 | 0 | 0 | I.Likelyx2, M.Nabersx2 |
| 5 | NYG@WSH | Mike Sainristil | CB | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | M.Fieldsx1, T.Tracyx1 |
| 5 | NYG@WSH | Frankie Luvu | LB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | N.Harrisx1, I.Likelyx1 |
| 6 | WSH@SF | Amik Robertson | CB | 5 | 5 | 61 | 0 | 1 | 0 | 0 | 0 | C.McCaffreyx3, M.Evansx1, K.Juszczykx1 |
| 6 | WSH@SF | Nick Cross | S | 1 | 1 | 54 | 0 | 1 | 0 | 0 | 0 | M.Evansx1 |
| 6 | WSH@SF | Quan Martin | S | 2 | 2 | 48 | 0 | 1 | 0 | 0 | 0 | B.Cooksx1, G.Kittlex1 |
| 6 | WSH@SF | Sonny Styles | LB | 6 | 5 | 33 | 0 | 0 | 1 | 0 | 0 | G.Kittlex3, C.McCaffreyx2, M.Evansx1 |
| 6 | WSH@SF | Trey Amos | CB | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | J.Watkinsx1 |
| 6 | WSH@SF | Jeremy Reaves | S | 2 | 1 | 16 | 0 | 0 | 1 | 0 | 0 | M.Evansx1, G.Kittlex1 |
| 6 | WSH@SF | K'Lavon Chaisson | OLB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | C.McCaffreyx1 |
| 6 | WSH@SF | Rasul Douglas | CB | 2 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | G.Kittlex1, C.McCaffreyx1 |
| 6 | WSH@SF | Frankie Luvu | LB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | B.Cooksx1 |
| 8 | PHI@WSH | Trey Amos | CB | 6 | 4 | 73 | 0 | 2 | 2 | 0 | 0 | M.Lemonx3, E.Stowersx2, D.Cooperx1 |
| 8 | PHI@WSH | Jeremy Reaves | S | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | D.Goedertx3 |
| 8 | PHI@WSH | Frankie Luvu | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | M.Lemonx2, E.Stowersx1 |
| 8 | PHI@WSH | Sonny Styles | LB | 4 | 4 | 22 | 0 | 0 | 0 | 0 | 0 | E.Mitchellx2, M.Lemonx1, J.Bluex1 |
| 8 | PHI@WSH | Nick Cross | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | M.Lemonx1, M.Brownx1 |
| 8 | PHI@WSH | Quan Martin | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | D.Cooperx1 |
| 8 | PHI@WSH | Rasul Douglas | CB | 2 | 1 | 8 | 0 | 0 | 0 | 1 | 0 | M.Brownx1, D.Cooperx1 |
| 8 | PHI@WSH | Amik Robertson | CB | 3 | 3 | 7 | 0 | 0 | 0 | 0 | 0 | E.Mitchellx2, D.Cooperx1 |
| 8 | PHI@WSH | K'Lavon Chaisson | OLB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | D.Goedertx1 |

## Who beat them each week

**Wk1 WSH@PHI** (vs PHI offense, 203 rec yds allowed; 41% of targets unattributed)
- Top receivers: D.Goedert (TE1, short/YAC (aDOT <8)) 4/5 77y 2TD; D.Wicks (WR3+, deep (aDOT 13+)) 2/4 73y 1TD; D.Smith (WR2, intermediate (aDOT 8-13)) 3/6 53y; W.Shipley (RB, short/YAC (aDOT <8)) 1/1 8y
- 20+ catches: D.Wicks(WR3+) 64y deep_right - J.Reaves [tackler]; D.Smith(WR2) 31y deep_right - R.Douglas [tackler]; D.Goedert(TE1) 43y short_middle TD - no tackler named [unattributed]
- 15+ runs: S.Barkley(RB) 42y rush right guard; J.Hurts(QB) 22y rush middle

**Wk2 WSH@DAL** (vs DAL offense, 279 rec yds allowed; 23% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 8/9 153y 2TD; J.Ferguson (TE1, short/YAC (aDOT <8)) 4/4 43y 2TD; G.Pickens (WR2, intermediate (aDOT 8-13)) 6/8 40y; R.Flournoy (WR3+, short/YAC (aDOT <8)) 5/6 23y
- 20+ catches: C.Lamb(WR1) 23y deep_middle - A.Robertson [tackler]; C.Lamb(WR1) 38y deep_right - N.Cross [tackler]; C.Lamb(WR1) 35y deep_right - Q.Martin [tackler]; C.Lamb(WR1) 24y deep_right TD - no tackler named [unattributed]

**Wk3 SEA@WSH** (vs SEA offense, 393 rec yds allowed; 18% of targets unattributed)
- Top receivers: J.Smith-Njigba (WR1, intermediate (aDOT 8-13)) 10/14 128y 2TD; A.Barner (TE1, short/YAC (aDOT <8)) 5/9 69y; G.Holani (RB, short/YAC (aDOT <8)) 5/5 48y; T.Horton (WR3+, intermediate (aDOT 8-13)) 3/3 48y
- 20+ catches: J.Smith-Njigba(WR1) 20y deep_middle - J.Reaves [tackler]; A.Barner(TE1) 32y short_right - K.Chaisson [tackler]; B.Russell(RB) 20y short_left - Q.Martin [tackler]; J.Smith-Njigba(WR1) 26y deep_right - no tackler named [unattributed]

**Wk4 IND@WSH** (vs IND offense, 143 rec yds allowed; 21% of targets unattributed)
- Top receivers: L.Treadwell (WR3+, intermediate (aDOT 8-13)) 5/6 42y; T.Warren (TE1, short/YAC (aDOT <8)) 5/5 41y; A.Dulin (WR3+, short/YAC (aDOT <8)) 3/6 29y; J.Downs (WR1, intermediate (aDOT 8-13)) 3/4 16y
- 20+ catches: A.Dulin(WR3+) 23y short_right - A.Robertson [tackler]

**Wk5 NYG@WSH** (vs NYG offense, 326 rec yds allowed; 33% of targets unattributed)
- Top receivers: M.Nabers (WR1, intermediate (aDOT 8-13)) 11/20 121y 1TD; I.Likely (TE1, short/YAC (aDOT <8)) 11/13 94y 2TD; T.Johnson (TE2+, intermediate (aDOT 8-13)) 2/3 35y; T.Tracy (RB, short/YAC (aDOT <8)) 2/3 25y
- 20+ catches: M.Nabers(WR1) 20y deep_left - A.Robertson [tackler]; T.Tracy(RB) 21y short_right - J.Reaves [tackler]; T.Johnson(TE2+) 21y short_middle - J.Reaves [tackler]; M.Nabers(WR1) 28y deep_middle - Q.Martin [tackler]
- 15+ runs: J.Winston(QB) 15y rush right end; C.Skattebo(RB) 19y rush right end

**Wk6 WSH@SF** (vs SF offense, 264 rec yds allowed; 17% of targets unattributed)
- Top receivers: M.Evans (WR1, deep (aDOT 13+)) 3/5 94y; G.Kittle (TE1, short/YAC (aDOT <8)) 5/8 69y 1TD; C.McCaffrey (RB, short/YAC (aDOT <8)) 9/10 53y; J.Watkins (WR3+, deep (aDOT 13+)) 1/1 22y
- 20+ catches: M.Evans(WR1) 24y deep_middle - A.Robertson [tackler]; M.Evans(WR1) 54y deep_right - N.Cross [tackler]; J.Watkins(WR3+) 22y deep_left - T.Amos [tackler]; G.Kittle(TE1) 35y deep_right - Q.Martin [tackler]

**Wk8 PHI@WSH** (vs PHI offense, 212 rec yds allowed; 22% of targets unattributed)
- Top receivers: M.Lemon (WR1, short/YAC (aDOT <8)) 6/9 57y; E.Stowers (TE2+, short/YAC (aDOT <8)) 3/3 53y; D.Goedert (TE1, short/YAC (aDOT <8)) 4/4 30y; S.Barkley (RB, short/YAC (aDOT <8)) 1/1 24y
- 20+ catches: M.Lemon(WR1) 20y deep_left - T.Amos [tackler]; S.Barkley(RB) 24y deep_left - no tackler named [unattributed]; E.Stowers(TE2+) 34y short_left - T.Amos [tackler]
- 15+ runs: T.McKee(QB) 15y rush left end

