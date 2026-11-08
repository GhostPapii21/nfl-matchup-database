# NO DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 NO@DET, wk2 NO@BAL, wk3 LV@NO, wk4 ATL@NO, wk5 MIN@NO, wk6 NO@NYG, wk7 PIT@NO). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 15.5% / Zone 74.7% | MOF closed 65.4% / MOF open 30.4% | Blitz 31.9% | Light box 45.7% / Heavy box 20.8% | Sub package 70.0% | Sharp YPT allowed WR 8.4, TE 7.6, RB 7.3, Outside 7.7, Slot 10.2

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type RB: 7.14 YPT on 37 tgts (league 5.61, +1.53), 3 catches of 20+
- depth deep_20+: 19.14 YPT on 22 tgts (league 12.32, +6.82), 13 catches of 20+
- depth/direction deep_left: 18.24 YPT on 17 tgts (league 11.28, +6.96), 9 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 37 | 33 | 264 | 1 | 3 | 7.14 | 5.30 | 37.70 | 5.61 | 1.53 |
| TE1 | 48 | 33 | 386 | 2 | 5 | 8.04 | 6.90 | 55.10 | 7.39 | 0.65 |
| TE2+ | 15 | 12 | 93 | 2 | 0 | 6.20 | 2.10 | 13.30 | 6.71 | -0.51 |
| WR1 | 53 | 39 | 506 | 3 | 6 | 9.55 | 7.60 | 72.30 | 8.16 | 1.39 |
| WR2 | 37 | 19 | 249 | 2 | 5 | 6.73 | 5.30 | 35.60 | 8.20 | -1.47 |
| WR3+ | 31 | 16 | 250 | 1 | 5 | 8.06 | 4.40 | 35.70 | 7.67 | 0.39 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 22 | 19 | 155 | 1 | 1 | 7.05 | 5.61 | 1.44 |
| TE1 | 20 | 12 | 173 | 1 | 4 | 8.65 | 7.39 | 1.26 |
| TE2+ | 10 | 8 | 56 | 1 | 0 | 5.60 | 6.71 | -1.11 |
| WR1 | 35 | 25 | 396 | 1 | 6 | 11.31 | 8.16 | 3.15 |
| WR2 | 16 | 7 | 100 | 1 | 3 | 6.25 | 8.20 | -1.95 |
| WR3+ | 19 | 12 | 179 | 0 | 4 | 9.42 | 7.67 | 1.75 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 50 | 39 | 281 | 0 | 3 | 5.62 | 4.58 | 1.04 |
| short_1-9 | 97 | 77 | 639 | 6 | 2 | 6.59 | 6.23 | 0.36 |
| inter_10-19 | 49 | 23 | 407 | 2 | 6 | 8.31 | 10.17 | -1.86 |
| deep_20+ | 22 | 13 | 421 | 3 | 13 | 19.14 | 12.32 | 6.82 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 17 | 10 | 310 | 1 | 9 | 18.24 | 11.28 | 6.96 |
| deep_middle | 10 | 5 | 163 | 2 | 5 | 16.30 | 14.90 | 1.40 |
| deep_right | 16 | 7 | 142 | 1 | 3 | 8.88 | 11.85 | -2.97 |
| short_left | 74 | 56 | 472 | 5 | 4 | 6.38 | 6.08 | 0.30 |
| short_middle | 38 | 29 | 262 | 0 | 2 | 6.89 | 7.43 | -0.54 |
| short_right | 63 | 45 | 399 | 2 | 1 | 6.33 | 5.95 | 0.38 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 45 | 24 | 400 | 2 | 7 | 8.89 | 8.94 | -0.05 |
| intermediate (aDOT 8-13) | 80 | 54 | 680 | 5 | 9 | 8.50 | 7.96 | 0.54 |
| short/YAC (aDOT <8) | 96 | 74 | 668 | 4 | 8 | 6.96 | 6.47 | 0.49 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 3, 'TE': 5, 'WR': 16} (24 total, 3.4/g)
- Pass 20+ by depth/direction: {'deep_left': 9, 'deep_middle': 5, 'deep_right': 3, 'short_left': 4, 'short_middle': 2, 'short_right': 1}
- Rush 15+ by position: {'QB': 2, 'RB': 10, 'WR': 1} (13 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 19 | 134 | 2 | 7.05 | 19.10 |
| RB | 172 | 843 | 10 | 4.90 | 120.40 |
| WR | 2 | 9 | 1 | 4.50 | 1.30 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Quincy Riley | CB | 7 | 76.90 | 18 | 2.60 | 15 | 171 | 24.40 | 9.50 | 0 | 2 | 3 | 0 | 0 |
| Martin Emerson | CB | 5 | 43.60 | 19 | 3.80 | 15 | 164 | 32.80 | 8.63 | 0 | 1 | 2 | 2 | 0 |
| Kool-Aid McKinstry | CB | 7 | 91.70 | 18 | 2.60 | 12 | 146 | 20.90 | 8.11 | 0 | 3 | 6 | 0 | 0 |
| Kaden Elliss | LB | 3 | 100 | 13 | 4.30 | 12 | 141 | 47 | 10.85 | 0 | 1 | 1 | 0 | 0 |
| Pete Werner | LB | 6 | 78.40 | 20 | 3.30 | 18 | 134 | 22.30 | 6.70 | 0 | 0 | 2 | 0 | 0 |
| Danny Stutsman | LB | 4 | 62.30 | 9 | 2.20 | 8 | 70 | 17.50 | 7.78 | 0 | 1 | 1 | 0 | 0 |
| Justin Reid | S | 7 | 93.30 | 18 | 2.60 | 18 | 228 | 32.60 | 12.67 | 0 | 4 | 0 | 0 | 0 |
| Jonas Sanker | S | 7 | 68.90 | 19 | 2.70 | 18 | 209 | 29.90 | 11 | 0 | 4 | 1 | 0 | 0 |
| Julian Blackmon | S | 5 | 100 | 12 | 2.40 | 10 | 173 | 34.60 | 14.42 | 0 | 3 | 0 | 2 | 0 |
| Jordan Howden | S | 1 | 11.80 | 1 | 1 | 1 | 20 | 20 | 20 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Quincy Riley** (CB): WR1:6t/65y, WR3+:4t/62y, TE1:4t/31y, WR2:4t/13y | 20+: wk4 D.London(WR1) 27 deep_right; wk6 C.Jones(WR3+) 49 deep_left
- **Martin Emerson** (CB): WR3+:3t/70y, WR1:8t/44y, RB:3t/31y, WR2:5t/19y | 20+: wk2 D.Walker(WR3+) 47 deep_left
- **Kool-Aid McKinstry** (CB): TE1:5t/60y, WR1:6t/40y, WR2:3t/40y, TE2+:2t/6y, WR3+:2t/0y | 20+: wk3 B.Bowers(TE1) 20 deep_left; wk4 J.Dotson(WR2) 23 short_left; wk5 J.Jefferson(WR1) 21 deep_right
- **Kaden Elliss** (LB): TE1:6t/62y, RB:5t/53y, TE2+:1t/18y, WR1:1t/8y | 20+: wk3 A.Jeanty(RB) 22 short_left
- **Pete Werner** (LB): TE1:6t/50y, RB:4t/28y, WR1:5t/27y, WR2:4t/23y, WR3+:1t/6y
- **Danny Stutsman** (LB): WR1:3t/38y, TE2+:2t/21y, TE1:1t/8y, RB:2t/3y, WR2:1t/0y | 20+: wk6 M.Nabers(WR1) 27 deep_middle
- **Justin Reid** (S): WR1:6t/98y, RB:5t/46y, WR3+:2t/33y, TE1:3t/32y, TE2+:2t/19y | 20+: wk2 D.Henry(RB) 20 short_right; wk4 D.London(WR1) 37 deep_middle; wk5 J.Jones(WR3+) 32 deep_left; wk6 I.Likely(TE1) 20 deep_right
- **Jonas Sanker** (S): WR1:3t/61y, TE1:5t/55y, RB:5t/40y, WR2:2t/26y, TE2+:2t/14y, WR3+:2t/13y | 20+: wk6 I.Likely(TE1) 24 deep_left; wk7 J.Warren(RB) 26 short_left; wk7 D.Metcalf(WR1) 51 deep_left; wk7 G.Bernard(WR2) 20 short_middle
- **Julian Blackmon** (S): WR1:3t/69y, TE1:3t/41y, WR3+:2t/37y, WR2:2t/16y, TE2+:1t/8y, RB:1t/2y | 20+: wk4 K.Pitts(TE1) 28 short_left; wk5 T.Felton(WR3+) 23 deep_left; wk6 M.Nabers(WR1) 46 deep_middle
- **Jordan Howden** (S): WR3+:1t/20y | 20+: wk7 B.Smith(WR3+) 20 short_middle

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NO@DET | Kool-Aid McKinstry | CB | 4 | 3 | 34 | 0 | 0 | 1 | 0 | 0 | A.St. Brownx2, S.LaPortax1, J.Williamsx1 |
| 1 | NO@DET | Justin Reid | S | 4 | 4 | 27 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx2, A.St. Brownx1, S.LaPortax1 |
| 1 | NO@DET | Jonas Sanker | S | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | B.Wrightx1, J.Gibbsx1, A.St. Brownx1, S.LaPortax1 |
| 1 | NO@DET | Kaden Elliss | LB | 4 | 3 | 24 | 0 | 0 | 1 | 0 | 0 | S.LaPortax2, A.St. Brownx1, S.Vakix1 |
| 1 | NO@DET | Pete Werner | LB | 4 | 3 | 19 | 0 | 0 | 1 | 0 | 0 | A.St. Brownx3, J.Gibbsx1 |
| 1 | NO@DET | Martin Emerson | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | J.Williamsx1, A.St. Brownx1 |
| 1 | NO@DET | Danny Stutsman | LB | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | S.LaPortax1, A.St. Brownx1 |
| 1 | NO@DET | Quincy Riley | CB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | J.Williamsx2 |
| 2 | NO@BAL | Martin Emerson | CB | 2 | 2 | 55 | 0 | 1 | 0 | 0 | 0 | D.Walkerx1, J.Hillx1 |
| 2 | NO@BAL | Pete Werner | LB | 6 | 6 | 48 | 0 | 0 | 0 | 0 | 0 | M.Andrewsx3, R.Batemanx2, C.Moorex1 |
| 2 | NO@BAL | Justin Reid | S | 3 | 3 | 29 | 0 | 1 | 0 | 0 | 0 | D.Henryx1, M.Andrewsx1, J.Hillx1 |
| 2 | NO@BAL | Kool-Aid McKinstry | CB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | M.Andrewsx1, R.Batemanx1, C.Moorex1 |
| 2 | NO@BAL | Julian Blackmon | S | 2 | 1 | 14 | 0 | 0 | 0 | 1 | 0 | L.Westerx1, R.Batemanx1 |
| 2 | NO@BAL | Quincy Riley | CB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | R.Batemanx2 |
| 2 | NO@BAL | Jonas Sanker | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | M.Andrewsx1 |
| 3 | LV@NO | Kaden Elliss | LB | 6 | 6 | 99 | 0 | 1 | 0 | 0 | 0 | B.Bowersx3, A.Jeantyx2, M.Mayerx1 |
| 3 | LV@NO | Kool-Aid McKinstry | CB | 4 | 2 | 31 | 0 | 1 | 2 | 0 | 0 | B.Bowersx3, C.Whitex1 |
| 3 | LV@NO | Justin Reid | S | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | T.Tuckerx2 |
| 3 | LV@NO | Danny Stutsman | LB | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | M.Mayerx1, T.Tuckerx1 |
| 3 | LV@NO | Pete Werner | LB | 3 | 3 | 17 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, B.Bowersx1, T.Tuckerx1 |
| 3 | LV@NO | Julian Blackmon | S | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | J.Nailorx1 |
| 3 | LV@NO | Jonas Sanker | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | B.Bowersx1 |
| 3 | LV@NO | Quincy Riley | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | B.Bowersx2 |
| 4 | ATL@NO | Quincy Riley | CB | 3 | 3 | 50 | 0 | 1 | 0 | 0 | 0 | D.Londonx2, Z.Branchx1 |
| 4 | ATL@NO | Julian Blackmon | S | 3 | 3 | 42 | 0 | 1 | 0 | 0 | 0 | D.Londonx1, Bi.Robinsonx1, K.Pittsx1 |
| 4 | ATL@NO | Justin Reid | S | 2 | 2 | 38 | 0 | 1 | 0 | 0 | 0 | D.Londonx1, Z.Branchx1 |
| 4 | ATL@NO | Kool-Aid McKinstry | CB | 1 | 1 | 23 | 0 | 1 | 0 | 0 | 0 | J.Dotsonx1 |
| 4 | ATL@NO | Jonas Sanker | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | A.Hooperx1, D.Londonx1 |
| 5 | MIN@NO | Justin Reid | S | 4 | 4 | 70 | 0 | 1 | 0 | 0 | 0 | G.Bartholomewx2, J.Jeffersonx1, J.Jonesx1 |
| 5 | MIN@NO | Julian Blackmon | S | 3 | 3 | 42 | 0 | 1 | 0 | 0 | 0 | T.Feltonx1, G.Bartholomewx1, J.Jeffersonx1 |
| 5 | MIN@NO | Kool-Aid McKinstry | CB | 3 | 3 | 27 | 0 | 1 | 0 | 0 | 0 | G.Bartholomewx2, J.Jeffersonx1 |
| 5 | MIN@NO | Pete Werner | LB | 3 | 3 | 24 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1, D.Claibornex1, D.Dallasx1 |
| 5 | MIN@NO | Jonas Sanker | S | 3 | 3 | 14 | 0 | 0 | 0 | 0 | 0 | T.Feltonx1, A.Jonesx1, M.Pricex1 |
| 5 | MIN@NO | Danny Stutsman | LB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | A.Jonesx2, B.Yurosekx1 |
| 5 | MIN@NO | Quincy Riley | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | J.Jeffersonx2 |
| 5 | MIN@NO | Martin Emerson | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | M.Pricex1 |
| 6 | NO@NYG | Quincy Riley | CB | 6 | 5 | 78 | 0 | 1 | 1 | 0 | 0 | M.Nabersx2, I.Likelyx2, D.Mooneyx1, C.Jonesx1 |
| 6 | NO@NYG | Martin Emerson | CB | 10 | 6 | 61 | 0 | 0 | 2 | 2 | 0 | M.Nabersx6, M.Fieldsx3, C.Jonesx1 |
| 6 | NO@NYG | Julian Blackmon | S | 3 | 2 | 59 | 0 | 1 | 0 | 1 | 0 | I.Likelyx2, M.Nabersx1 |
| 6 | NO@NYG | Justin Reid | S | 2 | 2 | 29 | 0 | 1 | 0 | 0 | 0 | I.Likelyx1, M.Nabersx1 |
| 6 | NO@NYG | Danny Stutsman | LB | 2 | 1 | 27 | 0 | 1 | 1 | 0 | 0 | M.Fieldsx1, M.Nabersx1 |
| 6 | NO@NYG | Jonas Sanker | S | 2 | 1 | 24 | 0 | 1 | 1 | 0 | 0 | I.Likelyx2 |
| 6 | NO@NYG | Pete Werner | LB | 3 | 2 | 15 | 0 | 0 | 1 | 0 | 0 | M.Fieldsx2, M.Nabersx1 |
| 6 | NO@NYG | Kool-Aid McKinstry | CB | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | M.Nabersx1 |
| 7 | PIT@NO | Jonas Sanker | S | 6 | 6 | 108 | 0 | 3 | 0 | 0 | 0 | R.Dowdlex2, G.Bernardx2, J.Warrenx1, D.Metcalfx1 |
| 7 | PIT@NO | Martin Emerson | CB | 4 | 4 | 29 | 0 | 0 | 0 | 0 | 0 | R.Dowdlex2, D.Metcalfx1, G.Bernardx1 |
| 7 | PIT@NO | Jordan Howden | S | 1 | 1 | 20 | 0 | 1 | 0 | 0 | 0 | B.Smithx1 |
| 7 | PIT@NO | Kaden Elliss | LB | 3 | 3 | 18 | 0 | 0 | 0 | 0 | 0 | J.Warrenx1, P.Freiermuthx1, R.Dowdlex1 |
| 7 | PIT@NO | Justin Reid | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | R.Dowdlex1 |
| 7 | PIT@NO | Pete Werner | LB | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | P.Freiermuthx1 |
| 7 | PIT@NO | Quincy Riley | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | B.Smithx1 |
| 7 | PIT@NO | Kool-Aid McKinstry | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | D.Metcalfx2 |

## Who beat them each week

**Wk1 NO@DET** (vs DET offense, 206 rec yds allowed; 28% of targets unattributed)
- Top receivers: A.St. Brown (WR1, intermediate (aDOT 8-13)) 10/14 67y 2TD; S.LaPorta (TE1, short/YAC (aDOT <8)) 5/8 48y; J.Williams (WR2, deep (aDOT 13+)) 4/9 45y; J.Gibbs (RB, short/YAC (aDOT <8)) 5/5 30y
- 20+ catches: J.Williams(WR2) 22y deep_left - no tackler named [unattributed]
- 15+ runs: J.Gibbs(RB) 21y rush right end; J.Gibbs(RB) 18y rush left guard; J.Gibbs(RB) 15y rush left tackle

**Wk2 NO@BAL** (vs BAL offense, 235 rec yds allowed; 28% of targets unattributed)
- Top receivers: R.Bateman (WR2, deep (aDOT 13+)) 7/9 88y 1TD; M.Andrews (TE1, short/YAC (aDOT <8)) 6/7 49y; D.Walker (WR3+, deep (aDOT 13+)) 1/2 47y; D.Henry (RB, short/YAC (aDOT <8)) 3/3 19y
- 20+ catches: D.Henry(RB) 20y short_right - J.Reid [tackler]; D.Walker(WR3+) 47y deep_left - M.Emerson [tackler]; R.Bateman(WR2) 22y deep_middle TD - no tackler named [unattributed]

**Wk3 LV@NO** (vs LV offense, 248 rec yds allowed; 28% of targets unattributed)
- Top receivers: B.Bowers (TE1, intermediate (aDOT 8-13)) 10/13 116y 1TD; T.Tucker (WR1, deep (aDOT 13+)) 4/4 43y; A.Jeanty (RB, short/YAC (aDOT <8)) 3/4 37y; M.Mayer (TE2+, short/YAC (aDOT <8)) 3/3 32y 1TD
- 20+ catches: B.Bowers(TE1) 20y deep_left - K.McKinstry [tackler]; A.Jeanty(RB) 22y short_left - K.Elliss [tackler]
- 15+ runs: M.Washington(RB) 36y rush right guard

**Wk4 ATL@NO** (vs ATL offense, 223 rec yds allowed; 20% of targets unattributed)
- Top receivers: D.London (WR1, intermediate (aDOT 8-13)) 5/6 96y; J.Dotson (WR2, deep (aDOT 13+)) 2/3 54y 1TD; K.Pitts (TE1, short/YAC (aDOT <8)) 3/3 47y; Z.Branch (WR3+, short/YAC (aDOT <8)) 2/2 10y
- 20+ catches: D.London(WR1) 27y deep_right - Q.Riley [tackler]; D.London(WR1) 37y deep_middle - J.Reid [tackler]; J.Dotson(WR2) 23y short_left - K.McKinstry [tackler]; K.Pitts(TE1) 28y short_left - J.Blackmon [tackler]; J.Dotson(WR2) 31y deep_middle TD - no tackler named [unattributed]
- 15+ runs: Bi.Robinson(RB) 59y rush left end

**Wk5 MIN@NO** (vs MIN offense, 229 rec yds allowed; 21% of targets unattributed)
- Top receivers: J.Jefferson (WR1, intermediate (aDOT 8-13)) 6/7 79y 1TD; G.Bartholomew (TE2+, short/YAC (aDOT <8)) 5/6 33y; J.Jones (WR3+, deep (aDOT 13+)) 1/1 32y; T.Felton (WR3+, intermediate (aDOT 8-13)) 2/3 27y
- 20+ catches: T.Felton(WR3+) 23y deep_left - J.Blackmon [tackler]; J.Jefferson(WR1) 21y deep_right - K.McKinstry [tackler]; J.Jones(WR3+) 32y deep_left - J.Reid [tackler]
- 15+ runs: K.Murray(QB) 18y rush right end; A.Jones(RB) 19y rush right tackle; A.Jones(RB) 15y rush right tackle

**Wk6 NO@NYG** (vs NYG offense, 395 rec yds allowed; 27% of targets unattributed)
- Top receivers: M.Nabers (WR1, intermediate (aDOT 8-13)) 12/16 165y; I.Likely (TE1, short/YAC (aDOT <8)) 6/12 99y 1TD; C.Jones (WR3+, deep (aDOT 13+)) 2/3 66y; T.Tracy (RB, short/YAC (aDOT <8)) 2/3 27y 1TD
- 20+ catches: I.Likely(TE1) 24y deep_left - J.Sanker [tackler]; M.Nabers(WR1) 27y deep_middle - D.Stutsman [tackler]; C.Jones(WR3+) 49y deep_left - Q.Riley [tackler]; I.Likely(TE1) 24y deep_left TD - no tackler named [unattributed]; M.Nabers(WR1) 46y deep_middle - J.Blackmon [tackler]; I.Likely(TE1) 20y deep_right - J.Reid [tackler]
- 15+ runs: D.Mooney(WR) 20y rush right end; J.McCarthy(QB) 28y rush middle

**Wk7 PIT@NO** (vs PIT offense, 212 rec yds allowed; 28% of targets unattributed)
- Top receivers: D.Metcalf (WR1, intermediate (aDOT 8-13)) 2/6 56y; R.Dowdle (RB, short/YAC (aDOT <8)) 6/6 45y; J.Warren (RB, short/YAC (aDOT <8)) 3/4 36y; G.Bernard (WR2, short/YAC (aDOT <8)) 3/5 27y
- 20+ catches: J.Warren(RB) 26y short_left - J.Sanker [tackler]; D.Metcalf(WR1) 51y deep_left - J.Sanker [tackler]; G.Bernard(WR2) 20y short_middle - J.Sanker [tackler]; B.Smith(WR3+) 20y short_middle - J.Howden [tackler]
- 15+ runs: J.Warren(RB) 29y rush middle; J.Warren(RB) 15y rush middle; R.Dowdle(RB) 16y rush right tackle

