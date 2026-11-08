# NYG DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 DAL@NYG, wk2 NYG@LAR, wk3 TEN@NYG, wk4 ARI@NYG, wk5 NYG@WSH, wk6 NO@NYG, wk7 NYG@HOU). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 26.1% / Zone 68.6% | MOF closed 49.2% / MOF open 47.5% | Blitz 38.8% | Light box 40.8% / Heavy box 34.3% | Sub package 70.0% | Sharp YPT allowed WR 6.9, TE 5.5, RB 5.8, Outside 7.9, Slot 5.7

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- receiver archetype deep (aDOT 13+): 10.48 YPT on 31 tgts (league 8.94, +1.54), 5 catches of 20+

Holds (-1.5 YPT or better): TE1: 4.88 YPT on 32 tgts (league 7.39, -2.51); WR1: 5.98 YPT on 43 tgts (league 8.16, -2.18); WR3+: 5.91 YPT on 46 tgts (league 7.67, -1.76)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 25 | 22 | 144 | 3 | 1 | 5.76 | 3.60 | 20.60 | 5.61 | 0.15 |
| TE1 | 32 | 20 | 156 | 0 | 2 | 4.88 | 4.60 | 22.30 | 7.39 | -2.51 |
| TE2+ | 26 | 21 | 157 | 2 | 1 | 6.04 | 3.70 | 22.40 | 6.71 | -0.67 |
| WR1 | 43 | 25 | 257 | 3 | 3 | 5.98 | 6.10 | 36.70 | 8.16 | -2.18 |
| WR2 | 41 | 26 | 359 | 3 | 4 | 8.76 | 5.90 | 51.30 | 8.20 | 0.56 |
| WR3+ | 46 | 24 | 272 | 3 | 3 | 5.91 | 6.60 | 38.90 | 7.67 | -1.76 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 13 | 10 | 66 | 1 | 1 | 5.08 | 5.61 | -0.53 |
| TE1 | 26 | 16 | 136 | 0 | 2 | 5.23 | 7.39 | -2.16 |
| TE2+ | 9 | 7 | 39 | 1 | 0 | 4.33 | 6.71 | -2.38 |
| WR1 | 26 | 14 | 155 | 2 | 2 | 5.96 | 8.16 | -2.20 |
| WR2 | 14 | 8 | 79 | 0 | 0 | 5.64 | 8.20 | -2.56 |
| WR3+ | 30 | 16 | 187 | 3 | 3 | 6.23 | 7.67 | -1.44 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 42 | 35 | 158 | 1 | 1 | 3.76 | 4.58 | -0.82 |
| short_1-9 | 106 | 73 | 602 | 9 | 2 | 5.68 | 6.23 | -0.55 |
| inter_10-19 | 39 | 26 | 446 | 4 | 7 | 11.44 | 10.17 | 1.27 |
| deep_20+ | 24 | 4 | 139 | 0 | 4 | 5.79 | 12.32 | -6.53 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 16 | 4 | 81 | 0 | 2 | 5.06 | 11.28 | -6.22 |
| deep_middle | 7 | 4 | 107 | 0 | 3 | 15.29 | 14.90 | 0.39 |
| deep_right | 15 | 4 | 133 | 1 | 3 | 8.87 | 11.85 | -2.98 |
| short_left | 69 | 47 | 408 | 5 | 1 | 5.91 | 6.08 | -0.17 |
| short_middle | 32 | 21 | 212 | 5 | 3 | 6.62 | 7.43 | -0.81 |
| short_right | 72 | 58 | 404 | 3 | 2 | 5.61 | 5.95 | -0.34 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 31 | 17 | 325 | 4 | 5 | 10.48 | 8.94 | 1.54 |
| intermediate (aDOT 8-13) | 82 | 48 | 476 | 4 | 5 | 5.80 | 7.96 | -2.16 |
| short/YAC (aDOT <8) | 100 | 73 | 544 | 6 | 4 | 5.44 | 6.47 | -1.03 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 3, 'WR': 10} (14 total, 2.0/g)
- Pass 20+ by depth/direction: {'deep_left': 2, 'deep_middle': 3, 'deep_right': 3, 'short_left': 1, 'short_middle': 3, 'short_right': 2}
- Rush 15+ by position: {'QB': 4, 'RB': 11} (15 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 22 | 177 | 4 | 8.05 | 25.30 |
| RB | 154 | 711 | 11 | 4.62 | 101.60 |
| TE | 1 | 0 | 0 | 0 | 0 |
| WR | 4 | 14 | 0 | 3.50 | 2 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Greg Newsome II | CB | 6 | 90.70 | 21 | 3.50 | 15 | 186 | 31 | 8.86 | 0 | 3 | 5 | 1 | 0 |
| Andru Phillips | CB | 7 | 70.40 | 15 | 2.10 | 13 | 135 | 19.30 | 9 | 0 | 1 | 2 | 0 | 0 |
| Deonte Banks | CB | 5 | 96.60 | 21 | 4.20 | 11 | 102 | 20.40 | 4.86 | 0 | 1 | 9 | 1 | 0 |
| Colton Hood | CB | 2 | 68.30 | 6 | 3 | 6 | 49 | 24.50 | 8.17 | 0 | 1 | 0 | 0 | 0 |
| Paulson Adebo | CB | 2 | 58.50 | 3 | 1.50 | 3 | 24 | 12 | 8 | 0 | 0 | 0 | 0 | 0 |
| Nic Jones | CB | 1 | 17 | 1 | 1 | 1 | 7 | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| Arvell Reese | LB | 7 | 99.30 | 26 | 3.70 | 23 | 147 | 21 | 5.65 | 0 | 1 | 2 | 1 | 0 |
| Tremaine Edmunds | LB | 6 | 100 | 18 | 3 | 16 | 124 | 20.70 | 6.89 | 0 | 0 | 2 | 0 | 0 |
| Jevon Holland | S | 6 | 100 | 12 | 2 | 8 | 156 | 26 | 13 | 0 | 2 | 2 | 2 | 0 |
| Tyler Nubin | S | 4 | 67 | 12 | 3 | 9 | 102 | 25.50 | 8.50 | 0 | 2 | 3 | 0 | 0 |
| Ar'Darius Washington | S | 5 | 36.30 | 7 | 1.40 | 7 | 59 | 11.80 | 8.43 | 0 | 0 | 0 | 0 | 0 |
| Jason Pinnock | S | 3 | 65.20 | 4 | 1.30 | 2 | 36 | 12 | 9 | 0 | 1 | 2 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Greg Newsome II** (CB): WR2:6t/68y, WR1:5t/57y, TE1:2t/27y, WR3+:5t/20y, TE2+:1t/9y, RB:2t/5y | 20+: wk2 D.Adams(WR2) 27 deep_right; wk4 Mi.Wilson(WR1) 24 deep_right; wk5 C.Okonkwo(TE1) 25 short_right
- **Andru Phillips** (CB): WR3+:2t/56y, WR2:6t/55y, WR1:3t/12y, TE2+:1t/7y, RB:2t/5y, TE1:1t/0y | 20+: wk7 T.Dell(WR3+) 43 deep_middle
- **Deonte Banks** (CB): WR3+:7t/49y, WR1:6t/16y, WR2:4t/15y, TE1:3t/14y, TE2+:1t/8y | 20+: wk5 T.McLaurin(WR3+) 22 short_middle
- **Colton Hood** (CB): WR1:3t/33y, TE2+:2t/14y, RB:1t/2y | 20+: wk3 C.Tate(WR1) 20 short_left
- **Paulson Adebo** (CB): WR1:1t/15y, WR3+:1t/10y, TE2+:1t/-1y
- **Nic Jones** (CB): TE2+:1t/7y
- **Arvell Reese** (LB): TE2+:5t/56y, TE1:5t/41y, WR2:5t/37y, RB:8t/17y, WR1:1t/0y, WR3+:2t/-4y | 20+: wk2 T.Ferguson(TE2+) 20 short_middle
- **Tremaine Edmunds** (LB): RB:5t/50y, TE1:8t/26y, WR1:2t/25y, TE2+:3t/23y
- **Jevon Holland** (S): WR2:4t/72y, WR3+:5t/51y, WR1:2t/33y, TE1:1t/0y | 20+: wk2 D.Adams(WR2) 64 deep_right; wk4 Mi.Wilson(WR1) 20 deep_left
- **Tyler Nubin** (S): TE2+:4t/24y, TE1:3t/23y, WR2:1t/23y, WR1:2t/18y, WR3+:1t/12y, RB:1t/2y | 20+: wk2 D.Adams(WR2) 23 deep_left; wk5 C.Okonkwo(TE1) 23 deep_middle
- **Ar'Darius Washington** (S): WR2:3t/41y, WR1:2t/15y, TE2+:2t/3y
- **Jason Pinnock** (S): WR3+:3t/36y, TE1:1t/0y | 20+: wk7 K.Boutte(WR3+) 25 deep_middle

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DAL@NYG | Deonte Banks | CB | 6 | 4 | 30 | 0 | 0 | 2 | 0 | 0 | R.Flournoyx2, C.Lambx2, K.Turpinx1, G.Pickensx1 |
| 1 | DAL@NYG | Tremaine Edmunds | LB | 5 | 5 | 29 | 0 | 0 | 0 | 0 | 0 | J.Fergusonx2, B.Spann-Fordx1, C.Lambx1, J.Williamsx1 |
| 1 | DAL@NYG | Paulson Adebo | CB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | C.Lambx1, J.Mingox1 |
| 1 | DAL@NYG | Jevon Holland | S | 1 | 1 | 17 | 0 | 0 | 0 | 0 | 0 | R.Flournoyx1 |
| 1 | DAL@NYG | Greg Newsome II | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | G.Pickensx1, J.Williamsx1 |
| 1 | DAL@NYG | Arvell Reese | LB | 3 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | J.Williamsx2, B.Spann-Fordx1 |
| 1 | DAL@NYG | Tyler Nubin | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | L.Schoonmakerx1 |
| 1 | DAL@NYG | Andru Phillips | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | G.Pickensx1 |
| 2 | NYG@LAR | Jevon Holland | S | 2 | 1 | 64 | 0 | 1 | 0 | 1 | 0 | D.Adamsx2 |
| 2 | NYG@LAR | Greg Newsome II | CB | 4 | 3 | 52 | 0 | 1 | 1 | 0 | 0 | D.Adamsx3, T.Fergusonx1 |
| 2 | NYG@LAR | Tyler Nubin | S | 5 | 4 | 47 | 0 | 1 | 1 | 0 | 0 | T.Fergusonx3, D.Adamsx1, K.Mumpfieldx1 |
| 2 | NYG@LAR | Arvell Reese | LB | 3 | 3 | 32 | 0 | 1 | 0 | 0 | 0 | T.Fergusonx2, D.Adamsx1 |
| 2 | NYG@LAR | Ar'Darius Washington | S | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | D.Adamsx1 |
| 2 | NYG@LAR | Tremaine Edmunds | LB | 2 | 1 | 13 | 0 | 0 | 1 | 0 | 0 | T.Fergusonx1, B.Corumx1 |
| 2 | NYG@LAR | Colton Hood | CB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | K.Williamsx1, C.Parkinsonx1 |
| 2 | NYG@LAR | Nic Jones | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | D.Allenx1 |
| 2 | NYG@LAR | Andru Phillips | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | C.Parkinsonx1 |
| 3 | TEN@NYG | Colton Hood | CB | 4 | 4 | 39 | 0 | 1 | 0 | 0 | 0 | C.Tatex3, D.Bellingerx1 |
| 3 | TEN@NYG | Arvell Reese | LB | 6 | 5 | 38 | 0 | 0 | 1 | 0 | 0 | W.Robinsonx3, T.Pollardx2, D.Bellingerx1 |
| 3 | TEN@NYG | Andru Phillips | CB | 6 | 6 | 35 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx3, C.Tatex2, T.Pollardx1 |
| 3 | TEN@NYG | Tremaine Edmunds | LB | 4 | 3 | 32 | 0 | 0 | 1 | 0 | 0 | G.Helmx3, T.Pollardx1 |
| 3 | TEN@NYG | Jevon Holland | S | 3 | 1 | 13 | 0 | 0 | 1 | 1 | 0 | W.Robinsonx1, C.Tatex1, E.Ayomanorx1 |
| 3 | TEN@NYG | Jason Pinnock | S | 1 | 1 | 11 | 0 | 0 | 0 | 0 | 0 | E.Ayomanorx1 |
| 3 | TEN@NYG | Ar'Darius Washington | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1 |
| 3 | TEN@NYG | Greg Newsome II | CB | 3 | 1 | 3 | 0 | 0 | 2 | 0 | 0 | W.Robinsonx1, C.Dikex1, E.Ayomanorx1 |
| 4 | ARI@NYG | Greg Newsome II | CB | 7 | 5 | 59 | 0 | 1 | 1 | 1 | 0 | Mi.Wilsonx5, M.Harrisonx1, T.McBridex1 |
| 4 | ARI@NYG | Arvell Reese | LB | 9 | 7 | 28 | 0 | 0 | 1 | 1 | 0 | T.McBridex4, T.Allgeierx1, M.Harrisonx1, Mi.Wilsonx1, J.Lovex1, H.Longx1 |
| 4 | ARI@NYG | Tremaine Edmunds | LB | 3 | 3 | 22 | 0 | 0 | 0 | 0 | 0 | T.McBridex2, E.Higginsx1 |
| 4 | ARI@NYG | Jevon Holland | S | 1 | 1 | 20 | 0 | 1 | 0 | 0 | 0 | Mi.Wilsonx1 |
| 4 | ARI@NYG | Tyler Nubin | S | 4 | 2 | 18 | 0 | 0 | 2 | 0 | 0 | T.McBridex2, Mi.Wilsonx2 |
| 4 | ARI@NYG | Deonte Banks | CB | 4 | 0 | 0 | 0 | 0 | 3 | 1 | 0 | Mi.Wilsonx2, M.Harrisonx1, T.McBridex1 |
| 4 | ARI@NYG | Andru Phillips | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | T.McBridex1, Mi.Wilsonx1 |
| 5 | NYG@WSH | Greg Newsome II | CB | 3 | 3 | 52 | 0 | 1 | 0 | 0 | 0 | C.Okonkwox1, T.McLaurinx1, A.Williamsx1 |
| 5 | NYG@WSH | Deonte Banks | CB | 4 | 3 | 47 | 0 | 1 | 1 | 0 | 0 | T.McLaurinx2, C.Okonkwox1, T.Burksx1 |
| 5 | NYG@WSH | Jevon Holland | S | 2 | 2 | 29 | 0 | 0 | 0 | 0 | 0 | T.Burksx1, T.McLaurinx1 |
| 5 | NYG@WSH | Tyler Nubin | S | 2 | 2 | 25 | 0 | 1 | 0 | 0 | 0 | C.Okonkwox1, R.Whitex1 |
| 5 | NYG@WSH | Andru Phillips | CB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | A.Williamsx1, T.Burksx1 |
| 5 | NYG@WSH | Tremaine Edmunds | LB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | A.Ekelerx1, C.Okonkwox1 |
| 5 | NYG@WSH | Arvell Reese | LB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | A.Williamsx1 |
| 5 | NYG@WSH | Ar'Darius Washington | S | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | J.Batesx1 |
| 6 | NO@NYG | Andru Phillips | CB | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | D.Velex1, A.Kamarax1 |
| 6 | NO@NYG | Ar'Darius Washington | S | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | D.Velex1, C.Olavex1, O.Delpx1 |
| 6 | NO@NYG | Deonte Banks | CB | 3 | 2 | 18 | 0 | 0 | 1 | 0 | 0 | C.Olavex2, O.Delpx1 |
| 6 | NO@NYG | Jevon Holland | S | 3 | 2 | 13 | 0 | 0 | 1 | 0 | 0 | J.Johnsonx1, D.Velex1, B.Brownx1 |
| 6 | NO@NYG | Tremaine Edmunds | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | K.Millerx1, C.Olavex1 |
| 6 | NO@NYG | Greg Newsome II | CB | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | B.Lancex1, A.Kamarax1 |
| 6 | NO@NYG | Jason Pinnock | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | J.Johnsonx1 |
| 6 | NO@NYG | Arvell Reese | LB | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | K.Millerx1 |
| 7 | NYG@HOU | Andru Phillips | CB | 1 | 1 | 43 | 0 | 1 | 0 | 0 | 0 | T.Dellx1 |
| 7 | NYG@HOU | Arvell Reese | LB | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | J.Noelx1, D.Schultzx1, W.Marksx1 |
| 7 | NYG@HOU | Jason Pinnock | S | 2 | 1 | 25 | 0 | 1 | 1 | 0 | 0 | K.Bouttex1, M.Harrisonx1 |
| 7 | NYG@HOU | Ar'Darius Washington | S | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | X.Hutchinsonx1 |
| 7 | NYG@HOU | Deonte Banks | CB | 4 | 2 | 7 | 0 | 0 | 2 | 0 | 0 | N.Collinsx3, D.Schultzx1 |
| 7 | NYG@HOU | Paulson Adebo | CB | 1 | 1 | -1 | 0 | 0 | 0 | 0 | 0 | C.Stoverx1 |

## Who beat them each week

**Wk1 DAL@NYG** (vs DAL offense, 175 rec yds allowed; 27% of targets unattributed)
- Top receivers: C.Lamb (WR1, intermediate (aDOT 8-13)) 5/8 44y 1TD; J.Williams (RB, short/YAC (aDOT <8)) 5/5 31y 1TD; G.Pickens (WR2, intermediate (aDOT 8-13)) 3/6 28y; R.Flournoy (WR3+, short/YAC (aDOT <8)) 2/4 22y

**Wk2 NYG@LAR** (vs LAR offense, 327 rec yds allowed; 30% of targets unattributed)
- Top receivers: D.Adams (WR2, deep (aDOT 13+)) 8/10 195y 2TD; T.Ferguson (TE2+, short/YAC (aDOT <8)) 6/9 54y 1TD; T.Atwell (WR3+, deep (aDOT 13+)) 1/2 19y; C.Parkinson (TE2+, short/YAC (aDOT <8)) 2/2 15y
- 20+ catches: D.Adams(WR2) 31y short_middle TD - no tackler named [unattributed]; D.Adams(WR2) 64y deep_right - J.Holland [tackler]; D.Adams(WR2) 27y deep_right - G.Newsome [tackler]; T.Ferguson(TE2+) 20y short_middle - A.Reese [tackler]; D.Adams(WR2) 23y deep_left - T.Nubin [tackler]
- 15+ runs: B.Corum(RB) 16y rush middle; K.Williams(RB) 20y rush right end; K.Williams(RB) 16y rush middle; B.Corum(RB) 18y rush right end

**Wk3 TEN@NYG** (vs TEN offense, 181 rec yds allowed; 20% of targets unattributed)
- Top receivers: C.Tate (WR1, intermediate (aDOT 8-13)) 6/9 58y; W.Robinson (WR2, short/YAC (aDOT <8)) 7/11 57y 1TD; T.Pollard (RB, short/YAC (aDOT <8)) 4/4 22y; D.Bellinger (TE2+, short/YAC (aDOT <8)) 2/2 16y
- 20+ catches: C.Tate(WR1) 20y short_left - C.Hood [tackler]
- 15+ runs: T.Pollard(RB) 16y rush right tackle

**Wk4 ARI@NYG** (vs ARI offense, 166 rec yds allowed; 11% of targets unattributed)
- Top receivers: Mi.Wilson (WR1, intermediate (aDOT 8-13)) 7/13 95y; T.McBride (TE1, short/YAC (aDOT <8)) 7/12 31y; E.Higgins (TE2+, short/YAC (aDOT <8)) 2/2 19y 1TD; M.Harrison (WR3+, deep (aDOT 13+)) 1/4 12y 1TD
- 20+ catches: Mi.Wilson(WR1) 20y deep_left - J.Holland [tackler]; Mi.Wilson(WR1) 24y deep_right - G.Newsome [tackler]
- 15+ runs: J.Love(RB) 16y rush left end; T.Allgeier(RB) 22y rush left tackle

**Wk5 NYG@WSH** (vs WSH offense, 199 rec yds allowed; 21% of targets unattributed)
- Top receivers: T.McLaurin (WR3+, intermediate (aDOT 8-13)) 4/5 62y; C.Okonkwo (TE1, short/YAC (aDOT <8)) 4/6 60y; A.Williams (WR2, intermediate (aDOT 8-13)) 3/3 31y; T.Burks (WR3+, deep (aDOT 13+)) 2/5 26y
- 20+ catches: C.Okonkwo(TE1) 23y deep_middle - T.Nubin [tackler]; C.Okonkwo(TE1) 25y short_right - G.Newsome [tackler]; T.McLaurin(WR3+) 22y short_middle - D.Banks [tackler]
- 15+ runs: J.Croskey-Merritt(RB) 33y rush middle; J.Daniels(QB) 38y rush middle; J.Croskey-Merritt(RB) 22y rush right end; J.Daniels(QB) 26y rush left tackle; J.Daniels(QB) 16y rush right end

**Wk6 NO@NYG** (vs NO offense, 144 rec yds allowed; 43% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 4/7 43y 1TD; D.Vele (WR2, intermediate (aDOT 8-13)) 3/6 42y; A.Kamara (RB, short/YAC (aDOT <8)) 2/4 35y 1TD; O.Delp (TE2+, short/YAC (aDOT <8)) 2/2 10y
- 20+ catches: A.Kamara(RB) 31y short_right TD - no tackler named [unattributed]
- 15+ runs: T.Shough(QB) 25y rush right end; C.Donaldson(RB) 17y rush right end; A.Kamara(RB) 15y rush middle

**Wk7 NYG@HOU** (vs HOU offense, 153 rec yds allowed; 38% of targets unattributed)
- Top receivers: D.Schultz (TE1, short/YAC (aDOT <8)) 5/6 45y; T.Dell (WR3+, deep (aDOT 13+)) 1/1 43y; K.Boutte (WR3+, intermediate (aDOT 8-13)) 1/2 25y; X.Hutchinson (WR1, intermediate (aDOT 8-13)) 3/6 17y 1TD
- 20+ catches: K.Boutte(WR3+) 25y deep_middle - J.Pinnock [tackler]; T.Dell(WR3+) 43y deep_middle - A.Phillips [tackler]

