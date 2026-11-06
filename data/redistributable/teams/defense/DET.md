# DET DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 NO@DET, wk2 DET@BUF, wk3 NYJ@DET, wk4 DET@CAR, wk5 DET@ARI, wk7 GB@DET, wk8 MIN@DET). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 18.2% / Zone 76.4% | MOF closed 47.6% / MOF open 49.0% | Blitz 23.6% | Light box 47.2% / Heavy box 30.4% | Sub package 54.0% | Sharp YPT allowed WR 8.4, TE 8.2, RB 4.2, Outside 7.9, Slot 9.7

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type TE1: 9.24 YPT on 50 tgts (league 7.39, +1.85), 7 catches of 20+
- depth deep_20+: 13.97 YPT on 38 tgts (league 12.32, +1.65), 16 catches of 20+
- depth/direction deep_middle: 18.5 YPT on 16 tgts (league 14.9, +3.6), 8 catches of 20+
- depth/direction deep_right: 15.17 YPT on 24 tgts (league 11.85, +3.32), 10 catches of 20+
- depth/direction short_middle: 9.07 YPT on 42 tgts (league 7.43, +1.64), 4 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 37 | 28 | 164 | 1 | 1 | 4.43 | 5.30 | 23.40 | 5.61 | -1.18 |
| TE1 | 50 | 37 | 462 | 6 | 7 | 9.24 | 7.10 | 66 | 7.39 | 1.85 |
| TE2+ | 30 | 24 | 222 | 5 | 3 | 7.40 | 4.30 | 31.70 | 6.71 | 0.69 |
| WR1 | 77 | 52 | 626 | 4 | 10 | 8.13 | 11 | 89.40 | 8.16 | -0.03 |
| WR2 | 40 | 26 | 325 | 1 | 6 | 8.12 | 5.70 | 46.40 | 8.20 | -0.08 |
| WR3+ | 40 | 21 | 285 | 1 | 5 | 7.12 | 5.70 | 40.70 | 7.67 | -0.55 |
| other | 1 | 1 | 7 | 0 | 0 | 7 | 0.10 | 1 | 2.86 | 4.14 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 17 | 13 | 104 | 1 | 1 | 6.12 | 5.61 | 0.51 |
| TE1 | 27 | 20 | 208 | 3 | 2 | 7.70 | 7.39 | 0.31 |
| TE2+ | 14 | 12 | 125 | 2 | 2 | 8.93 | 6.71 | 2.22 |
| WR1 | 44 | 29 | 299 | 3 | 4 | 6.80 | 8.16 | -1.36 |
| WR2 | 25 | 13 | 193 | 0 | 4 | 7.72 | 8.20 | -0.48 |
| WR3+ | 28 | 15 | 176 | 0 | 3 | 6.29 | 7.67 | -1.38 |
| other | 1 | 1 | 7 | 0 | 0 | 7 | 2.86 | 4.14 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 34 | 26 | 123 | 0 | 0 | 3.62 | 4.58 | -0.96 |
| short_1-9 | 146 | 116 | 882 | 10 | 3 | 6.04 | 6.23 | -0.19 |
| inter_10-19 | 53 | 31 | 555 | 4 | 13 | 10.47 | 10.17 | 0.30 |
| deep_20+ | 38 | 16 | 531 | 4 | 16 | 13.97 | 12.32 | 1.65 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 18 | 6 | 146 | 0 | 5 | 8.11 | 11.28 | -3.17 |
| deep_middle | 16 | 10 | 296 | 2 | 8 | 18.50 | 14.90 | 3.60 |
| deep_right | 24 | 14 | 364 | 3 | 10 | 15.17 | 11.85 | 3.32 |
| short_left | 78 | 55 | 373 | 3 | 2 | 4.78 | 6.08 | -1.30 |
| short_middle | 42 | 37 | 381 | 3 | 4 | 9.07 | 7.43 | 1.64 |
| short_right | 93 | 67 | 531 | 7 | 3 | 5.71 | 5.95 | -0.24 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 56 | 28 | 354 | 1 | 6 | 6.32 | 8.94 | -2.62 |
| intermediate (aDOT 8-13) | 94 | 67 | 842 | 6 | 14 | 8.96 | 7.96 | 1 |
| short/YAC (aDOT <8) | 125 | 94 | 895 | 11 | 12 | 7.16 | 6.47 | 0.69 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 10, 'WR': 21} (32 total, 4.6/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 8, 'deep_right': 10, 'short_left': 2, 'short_middle': 4, 'short_right': 3}
- Rush 15+ by position: {'QB': 2, 'RB': 7} (9 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 23 | 154 | 2 | 6.70 | 22 |
| RB | 130 | 524 | 7 | 4.03 | 74.90 |
| WR | 4 | 6 | 0 | 1.50 | 0.90 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D.J. Reed | CB | 7 | 94 | 27 | 3.90 | 20 | 296 | 42.30 | 10.96 | 0 | 4 | 6 | 1 | 0 |
| Roger McCreary | CB | 6 | 77.30 | 28 | 4.70 | 21 | 290 | 48.30 | 10.36 | 0 | 7 | 7 | 0 | 0 |
| Rock Ya-Sin | CB | 5 | 56 | 14 | 2.80 | 14 | 112 | 22.40 | 8 | 0 | 0 | 0 | 0 | 0 |
| Ennis Rakestraw Jr. | CB | 4 | 31.40 | 9 | 2.20 | 7 | 112 | 28 | 12.44 | 0 | 2 | 2 | 0 | 0 |
| Khalil Dorsey | CB | 2 | 21.30 | 5 | 2.50 | 4 | 72 | 36 | 14.40 | 0 | 1 | 1 | 0 | 0 |
| Keith Abney II | CB | 3 | 53.20 | 7 | 2.30 | 5 | 51 | 17 | 7.29 | 0 | 1 | 1 | 1 | 0 |
| Jack Campbell | LB | 6 | 96.70 | 24 | 4 | 24 | 215 | 35.80 | 8.96 | 0 | 2 | 0 | 0 | 0 |
| Derrick Barnes | OLB | 6 | 81 | 13 | 2.20 | 11 | 74 | 12.30 | 5.69 | 0 | 0 | 1 | 1 | 0 |
| Chuck Clark | S | 6 | 87.60 | 21 | 3.50 | 19 | 205 | 34.20 | 9.76 | 0 | 3 | 1 | 1 | 0 |
| Thomas Harper | S | 2 | 52.50 | 6 | 3 | 4 | 87 | 43.50 | 14.50 | 0 | 3 | 2 | 0 | 0 |
| Avonte Maddox | S | 2 | 65 | 6 | 3 | 4 | 74 | 37 | 12.33 | 0 | 2 | 2 | 0 | 0 |
| Christian Izien | S | 2 | 61 | 9 | 4.50 | 9 | 55 | 27.50 | 6.11 | 0 | 0 | 0 | 0 | 0 |
| Brian Branch | S | 2 | 55 | 2 | 1 | 1 | 22 | 11 | 11 | 0 | 1 | 0 | 1 | 0 |
| Jalen Mills | S | 2 | 17.50 | 2 | 1 | 2 | 12 | 6 | 6 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **D.J. Reed** (CB): WR1:15t/175y, WR3+:3t/45y, TE2+:1t/38y, TE1:3t/23y, WR2:4t/11y, RB:1t/4y | 20+: wk1 C.Olave(WR1) 47 deep_right; wk1 C.Olave(WR1) 42 deep_middle; wk3 G.Wilson(WR1) 32 deep_middle; wk5 E.Higgins(TE2+) 38 deep_right
- **Roger McCreary** (CB): WR2:7t/74y, WR1:6t/65y, TE1:2t/54y, TE2+:3t/51y, WR3+:9t/42y, RB:1t/4y | 20+: wk3 J.Woods(TE2+) 20 deep_left; wk3 K.Sadiq(TE1) 43 deep_left; wk5 K.Bourne(WR2) 22 short_middle; wk5 K.Bourne(WR2) 23 deep_left; wk7 M.Golden(WR1) 22 deep_left; wk7 S.Williams(WR3+) 20 deep_middle; wk8 B.Yurosek(TE2+) 24 short_right
- **Rock Ya-Sin** (CB): WR2:6t/44y, WR1:3t/28y, TE1:1t/18y, TE2+:1t/10y, WR3+:2t/8y, RB:1t/4y
- **Ennis Rakestraw Jr.** (CB): WR1:5t/68y, WR3+:4t/44y | 20+: wk4 T.McMillan(WR1) 26 short_middle; wk7 S.Williams(WR3+) 27 deep_right
- **Khalil Dorsey** (CB): WR2:2t/56y, RB:1t/10y, WR1:1t/6y, WR3+:1t/0y | 20+: wk8 J.Addison(WR2) 51 deep_middle
- **Keith Abney II** (CB): WR2:1t/28y, TE1:2t/20y, RB:2t/3y, WR1:2t/0y | 20+: wk7 C.Watson(WR2) 28 deep_middle
- **Jack Campbell** (LB): TE2+:6t/55y, TE1:5t/48y, WR3+:2t/39y, WR2:3t/28y, RB:5t/20y, WR1:2t/18y, other:1t/7y | 20+: wk4 B.Tremayne(WR3+) 21 deep_middle; wk7 T.Kraft(TE1) 22 short_middle
- **Derrick Barnes** (OLB): TE1:4t/31y, WR1:4t/19y, RB:3t/16y, WR2:1t/8y, TE2+:1t/0y
- **Chuck Clark** (S): WR1:6t/73y, TE1:4t/41y, RB:3t/29y, WR2:3t/29y, WR3+:2t/19y, TE2+:3t/14y | 20+: wk2 K.Coleman(WR2) 22 short_right; wk2 D.Kincaid(TE1) 23 short_left; wk4 T.McMillan(WR1) 21 short_right
- **Thomas Harper** (S): TE1:3t/34y, WR2:1t/31y, WR1:1t/22y, WR3+:1t/0y | 20+: wk1 C.Olave(WR1) 22 short_middle; wk1 D.Vele(WR2) 31 deep_right; wk1 J.Johnson(TE1) 27 deep_right
- **Avonte Maddox** (S): TE1:2t/43y, WR1:3t/31y, WR2:1t/0y | 20+: wk1 C.Olave(WR1) 20 deep_right; wk2 D.Kincaid(TE1) 25 deep_middle
- **Christian Izien** (S): RB:4t/20y, TE1:2t/14y, TE2+:2t/12y, WR3+:1t/9y
- **Brian Branch** (S): TE1:1t/22y, WR2:1t/0y | 20+: wk8 T.Hockenson(TE1) 22 deep_right
- **Jalen Mills** (S): TE1:2t/12y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NO@DET | D.J. Reed | CB | 6 | 5 | 130 | 0 | 2 | 1 | 0 | 0 | C.Olavex4, B.Lancex2 |
| 1 | NO@DET | Thomas Harper | S | 4 | 3 | 80 | 0 | 3 | 1 | 0 | 0 | J.Johnsonx2, C.Olavex1, D.Velex1 |
| 1 | NO@DET | Rock Ya-Sin | CB | 6 | 6 | 50 | 0 | 0 | 0 | 0 | 0 | D.Velex2, C.Olavex2, B.Lancex1, N.Fantx1 |
| 1 | NO@DET | Avonte Maddox | S | 5 | 3 | 49 | 0 | 1 | 2 | 0 | 0 | C.Olavex3, D.Velex1, J.Johnsonx1 |
| 1 | NO@DET | Jack Campbell | LB | 5 | 5 | 26 | 0 | 0 | 0 | 0 | 0 | T.Etiennex2, N.Fantx1, D.Velex1, C.Olavex1 |
| 1 | NO@DET | Chuck Clark | S | 3 | 2 | 22 | 0 | 0 | 0 | 1 | 0 | T.Etiennex2, N.Fantx1 |
| 1 | NO@DET | Roger McCreary | CB | 2 | 2 | 13 | 0 | 0 | 0 | 0 | 0 | D.Velex1, T.Etiennex1 |
| 1 | NO@DET | Derrick Barnes | OLB | 3 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | N.Fantx1, T.Etiennex1, J.Johnsonx1 |
| 1 | NO@DET | Keith Abney II | CB | 1 | 1 | -2 | 0 | 0 | 0 | 0 | 0 | C.Donaldsonx1 |
| 2 | DET@BUF | Chuck Clark | S | 4 | 4 | 67 | 0 | 2 | 0 | 0 | 0 | D.Kincaidx2, K.Colemanx1, K.Shakirx1 |
| 2 | DET@BUF | Jack Campbell | LB | 3 | 3 | 31 | 0 | 0 | 0 | 0 | 0 | K.Shakirx1, D.Kincaidx1, K.Colemanx1 |
| 2 | DET@BUF | Rock Ya-Sin | CB | 4 | 4 | 29 | 0 | 0 | 0 | 0 | 0 | K.Colemanx4 |
| 2 | DET@BUF | Avonte Maddox | S | 1 | 1 | 25 | 0 | 1 | 0 | 0 | 0 | D.Kincaidx1 |
| 2 | DET@BUF | Derrick Barnes | OLB | 1 | 1 | 12 | 0 | 0 | 0 | 0 | 0 | D.Kincaidx1 |
| 2 | DET@BUF | Thomas Harper | S | 2 | 1 | 7 | 0 | 0 | 1 | 0 | 0 | J.Palmerx1, D.Kincaidx1 |
| 2 | DET@BUF | D.J. Reed | CB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | J.Cookx1 |
| 3 | NYJ@DET | Roger McCreary | CB | 6 | 6 | 96 | 0 | 2 | 0 | 0 | 0 | G.Wilsonx3, J.Ruckertx1, J.Woodsx1, K.Sadiqx1 |
| 3 | NYJ@DET | D.J. Reed | CB | 4 | 3 | 45 | 0 | 1 | 1 | 0 | 0 | G.Wilsonx2, K.Sadiqx2 |
| 3 | NYJ@DET | Christian Izien | S | 6 | 6 | 30 | 0 | 0 | 0 | 0 | 0 | J.Ruckertx2, B.Hallx2, K.Sadiqx1, B.Allenx1 |
| 3 | NYJ@DET | Derrick Barnes | OLB | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx1, K.Sadiqx1, B.Allenx1 |
| 3 | NYJ@DET | Jack Campbell | LB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | J.Ruckertx1, K.Sadiqx1 |
| 3 | NYJ@DET | Rock Ya-Sin | CB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | G.Wilsonx1, B.Hallx1 |
| 3 | NYJ@DET | Ennis Rakestraw Jr. | CB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | G.Wilsonx2 |
| 3 | NYJ@DET | Chuck Clark | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | K.Sadiqx1 |
| 4 | DET@CAR | Chuck Clark | S | 6 | 6 | 67 | 0 | 1 | 0 | 0 | 0 | T.McMillanx4, J.Metchiex1, M.Evansx1 |
| 4 | DET@CAR | Ennis Rakestraw Jr. | CB | 4 | 3 | 62 | 0 | 1 | 1 | 0 | 0 | T.McMillanx3, J.Reedx1 |
| 4 | DET@CAR | Jack Campbell | LB | 4 | 4 | 47 | 0 | 1 | 0 | 0 | 0 | T.Tremblex2, B.Tremaynex1, J.Metchiex1 |
| 4 | DET@CAR | D.J. Reed | CB | 4 | 4 | 42 | 0 | 0 | 0 | 0 | 0 | T.McMillanx2, B.Tremaynex1, D.Wallerx1 |
| 4 | DET@CAR | Christian Izien | S | 3 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | A.Dillonx1, J.Metchiex1, D.Wallerx1 |
| 4 | DET@CAR | Jalen Mills | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | D.Wallerx1 |
| 4 | DET@CAR | Roger McCreary | CB | 2 | 1 | 9 | 0 | 0 | 1 | 0 | 0 | T.McMillanx1, J.Metchiex1 |
| 4 | DET@CAR | Derrick Barnes | OLB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | T.McMillanx1 |
| 5 | DET@ARI | Roger McCreary | CB | 11 | 5 | 80 | 0 | 2 | 6 | 0 | 0 | J.Brooksx4, K.Bournex4, R.Virgilx2, T.McBridex1 |
| 5 | DET@ARI | D.J. Reed | CB | 5 | 4 | 60 | 0 | 1 | 1 | 0 | 0 | Mi.Wilsonx4, E.Higginsx1 |
| 5 | DET@ARI | Jack Campbell | LB | 4 | 4 | 33 | 0 | 0 | 0 | 0 | 0 | K.Bournex1, J.Brissettx1, E.Higginsx1, T.Allgeierx1 |
| 5 | DET@ARI | Chuck Clark | S | 4 | 4 | 30 | 0 | 0 | 0 | 0 | 0 | E.Higginsx1, Mi.Wilsonx1, T.McBridex1, J.Brooksx1 |
| 5 | DET@ARI | Keith Abney II | CB | 4 | 3 | 25 | 0 | 0 | 0 | 1 | 0 | T.McBridex2, Mi.Wilsonx1, T.Allgeierx1 |
| 5 | DET@ARI | Ennis Rakestraw Jr. | CB | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | R.Virgilx1 |
| 5 | DET@ARI | Derrick Barnes | OLB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | K.Bournex1, T.McBridex1 |
| 5 | DET@ARI | Jalen Mills | S | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | T.McBridex1 |
| 7 | GB@DET | Jack Campbell | LB | 6 | 6 | 54 | 0 | 1 | 0 | 0 | 0 | T.Kraftx3, M.Lloydx1, J.Smithx1, J.Jacobsx1 |
| 7 | GB@DET | Roger McCreary | CB | 3 | 3 | 50 | 0 | 2 | 0 | 0 | 0 | M.Goldenx1, S.Williamsx1, C.Watsonx1 |
| 7 | GB@DET | Ennis Rakestraw Jr. | CB | 2 | 2 | 31 | 0 | 1 | 0 | 0 | 0 | B.Meltonx1, S.Williamsx1 |
| 7 | GB@DET | Keith Abney II | CB | 2 | 1 | 28 | 0 | 1 | 1 | 0 | 0 | M.Goldenx1, C.Watsonx1 |
| 7 | GB@DET | Khalil Dorsey | CB | 4 | 3 | 21 | 0 | 0 | 1 | 0 | 0 | J.Jacobsx1, B.Meltonx1, C.Watsonx1, M.Goldenx1 |
| 7 | GB@DET | Derrick Barnes | OLB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | M.Goldenx2, J.Jacobsx1 |
| 7 | GB@DET | Chuck Clark | S | 3 | 2 | 14 | 0 | 0 | 1 | 0 | 0 | C.Watsonx2, J.Jacobsx1 |
| 7 | GB@DET | D.J. Reed | CB | 3 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | M.Goldenx3 |
| 7 | GB@DET | Rock Ya-Sin | CB | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | S.Williamsx1 |
| 7 | GB@DET | Brian Branch | S | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | C.Watsonx1 |
| 8 | MIN@DET | Khalil Dorsey | CB | 1 | 1 | 51 | 0 | 1 | 0 | 0 | 0 | J.Addisonx1 |
| 8 | MIN@DET | Roger McCreary | CB | 4 | 4 | 42 | 0 | 1 | 0 | 0 | 0 | B.Yurosekx1, J.Jenningsx1, J.Jeffersonx1, J.Addisonx1 |
| 8 | MIN@DET | Brian Branch | S | 1 | 1 | 22 | 0 | 1 | 0 | 0 | 0 | T.Hockensonx1 |
| 8 | MIN@DET | Rock Ya-Sin | CB | 1 | 1 | 18 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1 |
| 8 | MIN@DET | D.J. Reed | CB | 4 | 1 | 11 | 0 | 0 | 2 | 1 | 0 | J.Addisonx4 |

## Who beat them each week

**Wk1 NO@DET** (vs NO offense, 410 rec yds allowed; 26% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 10/13 182y; D.Vele (WR2, intermediate (aDOT 8-13)) 7/9 69y 1TD; J.Johnson (TE1, short/YAC (aDOT <8)) 3/7 54y 1TD; B.Lance (WR3+, intermediate (aDOT 8-13)) 3/5 42y
- 20+ catches: C.Olave(WR1) 22y short_middle - T.Harper [tackler]; C.Olave(WR1) 47y deep_right - D.Reed [tackler]; D.Vele(WR2) 31y deep_right - T.Harper [tackler]; C.Olave(WR1) 42y deep_middle - D.Reed [tackler]; C.Olave(WR1) 20y deep_right - A.Maddox [tackler]; J.Johnson(TE1) 27y deep_right - T.Harper [tackler]
- 15+ runs: T.Etienne(RB) 18y rush middle

**Wk2 DET@BUF** (vs BUF offense, 248 rec yds allowed; 36% of targets unattributed)
- Top receivers: D.Kincaid (TE1, intermediate (aDOT 8-13)) 7/8 95y 1TD; K.Coleman (WR2, deep (aDOT 13+)) 6/6 63y; J.Palmer (WR3+, deep (aDOT 13+)) 1/3 43y 1TD; K.Shakir (WR1, short/YAC (aDOT <8)) 3/6 38y
- 20+ catches: D.Kincaid(TE1) 25y deep_middle - A.Maddox [tackler]; J.Palmer(WR3+) 43y deep_middle TD - no tackler named [unattributed]; K.Coleman(WR2) 22y short_right - C.Clark [tackler]; D.Kincaid(TE1) 23y short_left - C.Clark [tackler]
- 15+ runs: J.Cook(RB) 20y rush middle; J.Cook(RB) 35y rush left guard; J.Cook(RB) 22y rush right tackle

**Wk3 NYJ@DET** (vs NYJ offense, 321 rec yds allowed; 24% of targets unattributed)
- Top receivers: G.Wilson (WR1, intermediate (aDOT 8-13)) 10/14 107y 1TD; K.Sadiq (TE1, short/YAC (aDOT <8)) 7/8 105y 1TD; J.Ruckert (TE2+, short/YAC (aDOT <8)) 5/5 39y 1TD; B.Hall (RB, short/YAC (aDOT <8)) 3/3 23y
- 20+ catches: J.Woods(TE2+) 20y deep_left - R.McCreary [tackler]; K.Sadiq(TE1) 24y deep_right TD - no tackler named [unattributed]; G.Wilson(WR1) 32y deep_middle - D.Reed [tackler]; I.Williams(WR3+) 21y deep_left - no tackler named [unattributed]; K.Sadiq(TE1) 43y deep_left - R.McCreary [tackler]; G.Wilson(WR1) 23y deep_right TD - no tackler named [unattributed]

**Wk4 DET@CAR** (vs CAR offense, 329 rec yds allowed; 26% of targets unattributed)
- Top receivers: T.McMillan (WR1, intermediate (aDOT 8-13)) 14/16 192y 2TD; J.Metchie (WR3+, short/YAC (aDOT <8)) 3/5 37y; D.Waller (TE1, intermediate (aDOT 8-13)) 3/6 36y; B.Tremayne (WR3+, deep (aDOT 13+)) 2/3 32y
- 20+ catches: T.McMillan(WR1) 21y short_right - C.Clark [tackler]; T.McMillan(WR1) 26y short_middle - E.Rakestraw [tackler]; T.McMillan(WR1) 32y deep_right TD - no tackler named [unattributed]; B.Tremayne(WR3+) 21y deep_middle - J.Campbell [tackler]
- 15+ runs: C.Hubbard(RB) 15y rush left tackle; C.Hubbard(RB) 25y rush right guard; C.Hubbard(RB) 32y rush left tackle

**Wk5 DET@ARI** (vs ARI offense, 299 rec yds allowed; 22% of targets unattributed)
- Top receivers: K.Bourne (WR2, short/YAC (aDOT <8)) 5/8 70y; T.McBride (TE1, short/YAC (aDOT <8)) 9/10 66y 1TD; E.Higgins (TE2+, short/YAC (aDOT <8)) 3/3 57y; Mi.Wilson (WR1, intermediate (aDOT 8-13)) 4/7 30y
- 20+ catches: K.Bourne(WR2) 22y short_middle - R.McCreary [tackler]; K.Bourne(WR2) 23y deep_left - R.McCreary [tackler]; E.Higgins(TE2+) 38y deep_right - D.Reed [tackler]
- 15+ runs: J.Brissett(QB) 18y rush left end

**Wk7 GB@DET** (vs GB offense, 274 rec yds allowed; 28% of targets unattributed)
- Top receivers: C.Watson (WR2, deep (aDOT 13+)) 5/8 57y; J.Jacobs (RB, short/YAC (aDOT <8)) 5/7 55y 1TD; T.Kraft (TE1, short/YAC (aDOT <8)) 4/6 48y 1TD; S.Williams (WR3+, short/YAC (aDOT <8)) 3/3 47y
- 20+ catches: M.Golden(WR1) 22y deep_left - R.McCreary [tackler]; S.Williams(WR3+) 27y deep_right - E.Rakestraw [tackler]; T.Kraft(TE1) 22y short_middle - J.Campbell [tackler]; S.Williams(WR3+) 20y deep_middle - R.McCreary [tackler]; C.Watson(WR2) 28y deep_middle - K.Abney [tackler]; J.Jacobs(RB) 25y short_left TD - no tackler named [unattributed]

**Wk8 MIN@DET** (vs MIN offense, 210 rec yds allowed; 41% of targets unattributed)
- Top receivers: J.Addison (WR2, deep (aDOT 13+)) 3/9 66y; T.Hockenson (TE1, short/YAC (aDOT <8)) 4/5 58y 1TD; J.Jefferson (WR1, intermediate (aDOT 8-13)) 5/9 33y 1TD; B.Yurosek (TE2+, intermediate (aDOT 8-13)) 1/2 24y
- 20+ catches: B.Yurosek(TE2+) 24y short_right - R.McCreary [tackler]; T.Hockenson(TE1) 22y deep_right - B.Branch [tackler]; J.Addison(WR2) 51y deep_middle - K.Dorsey [tackler]
- 15+ runs: K.Murray(QB) 22y rush middle

## Seed notes from defenders/DET_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 15:00 Ben Yurosek (TE) rec 24 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q1 0:51 T.J. Hockenson (TE) rec 22 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q2 2:00 Kyler Murray (QB) rush 22 — R.Ya-Sin [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: ?
- Q4 10:16 Jordan Addison (WR) rec 51 — D.J. Reed [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said Ennis Rakestraw)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L35/S32/R33)
- D.J. Reed ← Jordan Addison: 7 tgt, 3 rec, 66 yds
- Ennis Rakestraw Jr. ← Justin Jefferson: 8 tgt, 4 rec, 32 yds — limited his man
- Roger McCreary ← Jauan Jennings: 2 tgt, 2 rec, 11 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 MIN@DET: Kyler Murray (QB-scrambler) 17/29 210y 2TD 1INT; 4-35 0TD | shell 18/76, MOFO 49 | Scrambler 4-35 rush + 2 TD vs DET zone. [confirmed-tackler;inferred;unknown]
- wk8 MIN@DET: T.J. Hockenson (TE-move/seam) 4/5tgt 58y 1TD | shell 18/76, MOFO 49 | Seam TE vs DET (TE YPT 8.2 allowed, top-tier soft); pregame matchup S Izien (inferred) 22y. [inferred]
- wk8 MIN@DET: Jordan Addison (WR-X outside volume) 3/8tgt 66y 0TD | shell 18/76, MOFO 49 | 51y vs D.J. Reed (inferred, outside-left). [inferred]
- wk8 MIN@DET: Justin Jefferson (WR-X outside volume) 5/9tgt 33y 1TD | shell 18/76, MOFO 49 | TD only; 33y — DET bracket/zone capped yards. [none (no explosive)]
- wk8 MIN@DET: Jordan Mason (RB-power/volume early-down) 8-20 0TD | shell 18/76, MOFO 49 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 MIN@DET: Ben Yurosek (TE-inline) 1/2tgt 24y 0TD | shell 18/76, MOFO 49 | Script/volume; no specific matchup attribution — see explosives table. [unknown]

