# MIN DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 GB@MIN, wk2 MIN@CHI, wk3 MIN@TB, wk4 MIA@MIN, wk5 MIN@NO, wk7 IND@MIN, wk8 MIN@DET). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 5.3% / Zone 86.5% | MOF closed 31.6% / MOF open 61.2% | Blitz 68.4% | Light box 24.1% / Heavy box 36.5% | Sub package 37.0% | Sharp YPT allowed WR 7.3, TE 6.1, RB 3.9, Outside 8.0, Slot 6.1

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- type WR2: 10.06 YPT on 34 tgts (league 8.2, +1.86), 4 catches of 20+

Holds (-1.5 YPT or better): RB: 4.03 YPT on 32 tgts (league 5.61, -1.58); WR3+: 4.87 YPT on 31 tgts (league 7.67, -2.8)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 32 | 22 | 129 | 0 | 1 | 4.03 | 4.60 | 18.40 | 5.61 | -1.58 |
| TE1 | 25 | 14 | 173 | 0 | 3 | 6.92 | 3.60 | 24.70 | 7.39 | -0.47 |
| TE2+ | 19 | 8 | 100 | 0 | 1 | 5.26 | 2.70 | 14.30 | 6.71 | -1.45 |
| WR1 | 51 | 32 | 366 | 0 | 3 | 7.18 | 7.30 | 52.30 | 8.16 | -0.98 |
| WR2 | 34 | 23 | 342 | 3 | 4 | 10.06 | 4.90 | 48.90 | 8.20 | 1.86 |
| WR3+ | 31 | 15 | 151 | 1 | 1 | 4.87 | 4.40 | 21.60 | 7.67 | -2.80 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 14 | 11 | 38 | 0 | 0 | 2.71 | 5.61 | -2.90 |
| TE1 | 10 | 7 | 49 | 0 | 0 | 4.90 | 7.39 | -2.49 |
| TE2+ | 11 | 5 | 41 | 0 | 0 | 3.73 | 6.71 | -2.98 |
| WR1 | 23 | 18 | 177 | 0 | 0 | 7.70 | 8.16 | -0.46 |
| WR2 | 18 | 11 | 127 | 1 | 1 | 7.06 | 8.20 | -1.14 |
| WR3+ | 11 | 4 | 33 | 0 | 0 | 3 | 7.67 | -4.67 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 36 | 30 | 181 | 0 | 1 | 5.03 | 4.58 | 0.45 |
| short_1-9 | 91 | 57 | 434 | 2 | 0 | 4.77 | 6.23 | -1.46 |
| inter_10-19 | 46 | 21 | 435 | 1 | 6 | 9.46 | 10.17 | -0.71 |
| deep_20+ | 19 | 6 | 211 | 1 | 6 | 11.11 | 12.32 | -1.21 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 11 | 3 | 79 | 0 | 2 | 7.18 | 11.28 | -4.10 |
| deep_middle | 11 | 5 | 227 | 2 | 4 | 20.64 | 14.90 | 5.74 |
| deep_right | 11 | 4 | 101 | 0 | 3 | 9.18 | 11.85 | -2.67 |
| short_left | 60 | 42 | 356 | 1 | 2 | 5.93 | 6.08 | -0.15 |
| short_middle | 37 | 20 | 198 | 0 | 1 | 5.35 | 7.43 | -2.08 |
| short_right | 62 | 40 | 300 | 1 | 1 | 4.84 | 5.95 | -1.11 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 45 | 24 | 427 | 4 | 7 | 9.49 | 8.94 | 0.55 |
| intermediate (aDOT 8-13) | 47 | 29 | 284 | 0 | 1 | 6.04 | 7.96 | -1.92 |
| short/YAC (aDOT <8) | 100 | 61 | 550 | 0 | 5 | 5.50 | 6.47 | -0.97 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 4, 'WR': 8} (13 total, 1.9/g)
- Pass 20+ by depth/direction: {'deep_left': 2, 'deep_middle': 4, 'deep_right': 3, 'short_left': 2, 'short_middle': 1, 'short_right': 1}
- Rush 15+ by position: {'QB': 1, 'RB': 6} (7 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 16 | 83 | 1 | 5.19 | 11.90 |
| RB | 159 | 721 | 6 | 4.53 | 103 |
| TE | 1 | 2 | 0 | 2 | 0.30 |
| WR | 3 | 13 | 0 | 4.33 | 1.90 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Byron Murphy | CB | 5 | 89.90 | 25 | 5 | 19 | 232 | 46.40 | 9.28 | 0 | 4 | 3 | 3 | 0 |
| Isaiah Rodgers | CB | 6 | 87.10 | 14 | 2.30 | 11 | 117 | 19.50 | 8.36 | 0 | 2 | 3 | 0 | 0 |
| James Pierre | CB | 6 | 40.70 | 16 | 2.70 | 12 | 102 | 17 | 6.38 | 0 | 1 | 2 | 2 | 0 |
| Blake Cashman | LB | 6 | 96.10 | 22 | 3.70 | 17 | 136 | 22.70 | 6.18 | 0 | 0 | 5 | 0 | 0 |
| Eric Wilson | LB | 4 | 94.30 | 8 | 2 | 7 | 65 | 16.20 | 8.12 | 0 | 1 | 1 | 0 | 0 |
| Josh Metellus | S | 7 | 99.60 | 19 | 2.70 | 16 | 214 | 30.60 | 11.26 | 0 | 3 | 3 | 0 | 0 |
| Harrison Smith | S | 7 | 54.90 | 10 | 1.40 | 7 | 68 | 9.70 | 6.80 | 0 | 0 | 2 | 1 | 0 |
| Theo Jackson | S | 4 | 58.70 | 6 | 1.50 | 5 | 57 | 14.20 | 9.50 | 0 | 0 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Byron Murphy** (CB): WR2:4t/102y, TE1:6t/81y, WR1:6t/26y, RB:5t/12y, WR3+:3t/11y, TE2+:1t/0y | 20+: wk1 T.Kraft(TE1) 30 deep_left; wk1 T.Kraft(TE1) 23 short_left; wk1 C.Watson(WR2) 32 deep_left; wk8 J.Williams(WR2) 46 deep_middle
- **Isaiah Rodgers** (CB): TE2+:1t/43y, WR2:4t/40y, WR1:4t/22y, RB:4t/12y, WR3+:1t/0y | 20+: wk1 J.Smith(TE2+) 43 deep_right; wk2 R.Odunze(WR2) 21 deep_right
- **James Pierre** (CB): WR1:4t/40y, WR3+:4t/33y, WR2:7t/29y, RB:1t/0y | 20+: wk1 M.Golden(WR1) 20 deep_right
- **Blake Cashman** (LB): TE1:3t/36y, WR2:3t/29y, RB:5t/27y, TE2+:5t/25y, WR1:5t/15y, WR3+:1t/4y
- **Eric Wilson** (LB): RB:3t/41y, TE2+:1t/9y, WR3+:1t/7y, WR1:1t/5y, WR2:1t/3y, TE1:1t/0y | 20+: wk2 D.Swift(RB) 32 short_left
- **Josh Metellus** (S): WR1:7t/117y, TE1:3t/42y, WR2:3t/27y, RB:1t/11y, WR3+:4t/10y, TE2+:1t/7y | 20+: wk1 M.Golden(WR1) 42 deep_middle; wk3 C.Otton(TE1) 37 short_right; wk3 E.Egbuka(WR1) 21 short_middle
- **Harrison Smith** (S): WR1:3t/27y, WR3+:1t/16y, TE1:1t/8y, TE2+:2t/7y, WR2:2t/7y, RB:1t/3y
- **Theo Jackson** (S): WR1:3t/33y, WR2:1t/15y, TE2+:2t/9y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GB@MIN | Byron Murphy | CB | 7 | 6 | 113 | 0 | 3 | 1 | 0 | 0 | T.Kraftx3, C.Watsonx2, J.Smithx1, J.Reedx1 |
| 1 | GB@MIN | Josh Metellus | S | 3 | 3 | 66 | 0 | 1 | 0 | 0 | 0 | M.Goldenx2, C.Watsonx1 |
| 1 | GB@MIN | Isaiah Rodgers | CB | 3 | 3 | 54 | 0 | 1 | 0 | 0 | 0 | C.Watsonx1, M.Goldenx1, J.Smithx1 |
| 1 | GB@MIN | James Pierre | CB | 5 | 3 | 34 | 0 | 1 | 1 | 1 | 0 | J.Reedx2, C.Watsonx1, M.Goldenx1, M.Lloydx1 |
| 1 | GB@MIN | Harrison Smith | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | J.Smithx1 |
| 2 | MIN@CHI | Eric Wilson | LB | 2 | 2 | 41 | 0 | 1 | 0 | 0 | 0 | S.Roushx1, D.Swiftx1 |
| 2 | MIN@CHI | Byron Murphy | CB | 6 | 4 | 34 | 0 | 0 | 1 | 1 | 0 | L.Burdenx3, D.Swiftx1, K.Monangaix1, K.Raymondx1 |
| 2 | MIN@CHI | Harrison Smith | S | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | K.Raymondx1, D.Swiftx1, R.Odunzex1 |
| 2 | MIN@CHI | Isaiah Rodgers | CB | 3 | 2 | 22 | 0 | 1 | 1 | 0 | 0 | D.Swiftx1, R.Odunzex1, L.Burdenx1 |
| 2 | MIN@CHI | Josh Metellus | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | D.Swiftx1, K.Raymondx1 |
| 2 | MIN@CHI | Theo Jackson | S | 2 | 1 | 15 | 0 | 0 | 1 | 0 | 0 | R.Odunzex1, S.Roushx1 |
| 2 | MIN@CHI | James Pierre | CB | 3 | 2 | 14 | 0 | 0 | 1 | 0 | 0 | L.Burdenx2, R.Odunzex1 |
| 2 | MIN@CHI | Blake Cashman | LB | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | K.Raymondx1, K.Monangaix1 |
| 3 | MIN@TB | Josh Metellus | S | 5 | 4 | 73 | 0 | 2 | 1 | 0 | 0 | C.Ottonx2, E.Egbukax2, J.McMillanx1 |
| 3 | MIN@TB | Isaiah Rodgers | CB | 5 | 5 | 39 | 0 | 0 | 0 | 0 | 0 | E.Egbukax2, C.Godwinx1, B.Irvingx1, K.Gainwellx1 |
| 3 | MIN@TB | Blake Cashman | LB | 4 | 3 | 36 | 0 | 0 | 1 | 0 | 0 | K.Gainwellx2, C.Ottonx1, C.Godwinx1 |
| 3 | MIN@TB | Harrison Smith | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | E.Egbukax1 |
| 3 | MIN@TB | James Pierre | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1 |
| 3 | MIN@TB | Eric Wilson | LB | 3 | 2 | 7 | 0 | 0 | 1 | 0 | 0 | B.Irvingx1, C.Ottonx1, C.Godwinx1 |
| 4 | MIA@MIN | Blake Cashman | LB | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | W.Kacmarekx1, O.Gordonx1, M.Washingtonx1 |
| 4 | MIA@MIN | Josh Metellus | S | 2 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | K.Colemanx2 |
| 4 | MIA@MIN | Harrison Smith | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | C.Bellx1 |
| 4 | MIA@MIN | Isaiah Rodgers | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | K.Colemanx1 |
| 5 | MIN@NO | Blake Cashman | LB | 5 | 5 | 32 | 0 | 0 | 0 | 0 | 0 | C.Olavex1, D.Velex1, N.Fantx1, J.Johnsonx1, C.Donaldsonx1 |
| 5 | MIN@NO | Theo Jackson | S | 2 | 2 | 27 | 0 | 0 | 0 | 0 | 0 | C.Olavex2 |
| 5 | MIN@NO | James Pierre | CB | 3 | 3 | 16 | 0 | 0 | 0 | 0 | 0 | D.Velex3 |
| 5 | MIN@NO | Josh Metellus | S | 1 | 1 | 14 | 0 | 0 | 0 | 0 | 0 | C.Olavex1 |
| 5 | MIN@NO | Byron Murphy | CB | 5 | 3 | 9 | 0 | 0 | 0 | 2 | 0 | J.Johnsonx2, A.Kamarax1, B.Lancex1, C.Olavex1 |
| 5 | MIN@NO | Harrison Smith | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | C.Olavex1 |
| 5 | MIN@NO | Isaiah Rodgers | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | D.Velex1 |
| 7 | IND@MIN | James Pierre | CB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | K.Allenx1, D.Burksx1 |
| 7 | IND@MIN | Harrison Smith | S | 2 | 1 | 13 | 0 | 0 | 0 | 1 | 0 | J.Downsx1, W.Malloryx1 |
| 7 | IND@MIN | Blake Cashman | LB | 6 | 2 | 13 | 0 | 0 | 4 | 0 | 0 | J.Downsx2, M.Alie-Coxx1, K.Allenx1, A.Ogletreex1, W.Malloryx1 |
| 7 | IND@MIN | Theo Jackson | S | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | A.Ogletreex1 |
| 7 | IND@MIN | Josh Metellus | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | K.Allenx1 |
| 7 | IND@MIN | Eric Wilson | LB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | L.Treadwellx1 |
| 7 | IND@MIN | Byron Murphy | CB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | J.Taylorx1, J.Downsx1 |
| 7 | IND@MIN | Isaiah Rodgers | CB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | S.McGowanx1 |
| 8 | MIN@DET | Byron Murphy | CB | 5 | 5 | 71 | 0 | 1 | 0 | 0 | 0 | J.Williamsx2, A.St. Brownx1, J.Gibbsx1, S.LaPortax1 |
| 8 | MIN@DET | Josh Metellus | S | 5 | 4 | 32 | 0 | 0 | 1 | 0 | 0 | A.St. Brownx2, S.LaPortax1, T.Conklinx1, J.Williamsx1 |
| 8 | MIN@DET | Blake Cashman | LB | 2 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1, S.LaPortax1 |
| 8 | MIN@DET | Eric Wilson | LB | 2 | 2 | 10 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1, S.Vakix1 |
| 8 | MIN@DET | Harrison Smith | S | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | S.LaPortax1 |
| 8 | MIN@DET | James Pierre | CB | 2 | 1 | 6 | 0 | 0 | 0 | 1 | 0 | J.Williamsx1, A.St. Brownx1 |
| 8 | MIN@DET | Theo Jackson | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1 |

## Who beat them each week

**Wk1 GB@MIN** (vs GB offense, 387 rec yds allowed; 50% of targets unattributed)
- Top receivers: C.Watson (WR2, deep (aDOT 13+)) 6/8 147y 2TD; M.Golden (WR1, deep (aDOT 13+)) 6/12 95y; T.Kraft (TE1, short/YAC (aDOT <8)) 3/6 65y; J.Smith (TE2+, short/YAC (aDOT <8)) 2/3 50y
- 20+ catches: C.Watson(WR2) 81y deep_middle TD - no tackler named [unattributed]; T.Kraft(TE1) 30y deep_left - B.Murphy [tackler]; T.Kraft(TE1) 23y short_left - B.Murphy [tackler]; C.Watson(WR2) 32y deep_left - B.Murphy [tackler]; J.Smith(TE2+) 43y deep_right - I.Rodgers [tackler]; M.Golden(WR1) 42y deep_middle - J.Metellus [tackler]; M.Golden(WR1) 20y deep_right - J.Pierre [tackler]

**Wk2 MIN@CHI** (vs CHI offense, 192 rec yds allowed; 17% of targets unattributed)
- Top receivers: D.Swift (RB, short/YAC (aDOT <8)) 5/5 54y; R.Odunze (WR2, deep (aDOT 13+)) 3/4 43y; K.Raymond (WR3+, short/YAC (aDOT <8)) 5/5 40y; L.Burden (WR1, short/YAC (aDOT <8)) 3/7 32y
- 20+ catches: D.Swift(RB) 32y short_left - E.Wilson [tackler]; R.Odunze(WR2) 21y deep_right - I.Rodgers [tackler]
- 15+ runs: C.Williams(QB) 17y rush; K.Mogai(RB) 15y rush right end

**Wk3 MIN@TB** (vs TB offense, 217 rec yds allowed; 37% of targets unattributed)
- Top receivers: E.Egbuka (WR1, intermediate (aDOT 8-13)) 5/9 62y; C.Otton (TE1, short/YAC (aDOT <8)) 3/6 56y; T.Hurst (WR3+, deep (aDOT 13+)) 1/3 40y 1TD; C.Godwin (WR2, short/YAC (aDOT <8)) 3/4 25y
- 20+ catches: T.Hurst(WR3+) 40y deep_middle TD - no tackler named [unattributed]; C.Otton(TE1) 37y short_right - J.Metellus [tackler]; E.Egbuka(WR1) 21y short_middle - J.Metellus [tackler]

**Wk4 MIA@MIN** (vs MIA offense, 85 rec yds allowed; 35% of targets unattributed)
- Top receivers: M.Washington (WR1, intermediate (aDOT 8-13)) 5/5 67y; W.Kacmarek (TE2+, short/YAC (aDOT <8)) 1/2 15y; K.Coleman (WR3+, deep (aDOT 13+)) 1/4 3y; C.Bell (WR2, deep (aDOT 13+)) 0/3 0y
- 15+ runs: O.Gordon(RB) 53y rush left tackle

**Wk5 MIN@NO** (vs NO offense, 96 rec yds allowed; 21% of targets unattributed)
- Top receivers: C.Olave (WR1, intermediate (aDOT 8-13)) 4/6 46y; D.Vele (WR2, intermediate (aDOT 8-13)) 4/6 26y; J.Johnson (TE1, short/YAC (aDOT <8)) 4/5 16y; C.Donaldson (RB, short/YAC (aDOT <8)) 1/1 7y

**Wk7 IND@MIN** (vs IND offense, 108 rec yds allowed; 14% of targets unattributed)
- Top receivers: K.Allen (WR2, short/YAC (aDOT <8)) 3/3 31y; L.Treadwell (WR3+, intermediate (aDOT 8-13)) 2/2 19y; J.Downs (WR1, intermediate (aDOT 8-13)) 2/4 18y; J.Taylor (RB, short/YAC (aDOT <8)) 2/3 15y
- 15+ runs: J.Taylor(RB) 38y rush left tackle

**Wk8 MIN@DET** (vs DET offense, 176 rec yds allowed; 20% of targets unattributed)
- Top receivers: J.Williams (WR2, deep (aDOT 13+)) 4/6 70y 1TD; A.St. Brown (WR1, intermediate (aDOT 8-13)) 7/8 46y; S.LaPorta (TE1, short/YAC (aDOT <8)) 3/5 33y; J.Gibbs (RB, short/YAC (aDOT <8)) 2/4 15y
- 20+ catches: J.Williams(WR2) 46y deep_middle - B.Murphy [tackler]
- 15+ runs: J.Gibbs(RB) 19y rush middle; J.Gibbs(RB) 30y rush middle; J.Gibbs(RB) 17y rush right tackle

## Seed notes from defenders/MIN_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 4:55 Jameson Williams (WR) rec 46 — Isaiah Rodgers [inferred; pregame matchup: ESPN cheat sheet primary (single-source; coverage.json said James Pierre)]; alignment: outside, offense-left side (pregame target-side proxy; ESPN season split L35/S22/R42)
- Q2 0:12 Jahmyr Gibbs (RB) rush 19 — B.Murphy [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q3 4:40 Jahmyr Gibbs (RB) rush 30 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Q4 8:39 Jahmyr Gibbs (RB) rush 17 — J.Metellus [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Isaiah Rodgers ← Jameson Williams: 5 tgt, 4 rec, 70 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 MIN@DET: Jahmyr Gibbs (RB-home-run zone runner) 23-153 1TD; 2/4tgt 15y 0TD | shell 5 man/87 zone, MOFO 61, blitz 71% | DET run-heavy (39 rushes; Goff sacked 4); MIN zone 87%/MOFO 61 + 71% blitz = light boxes; 6 run explosives, 153y. Rushing was the edge, not receiving. [confirmed-tackler;unknown]
- wk8 MIN@DET: Jameson Williams (WR-deep speed) 4/6tgt 70y 1TD | shell 5 man/87 zone, MOFO 61, blitz 71% | Deep speed vs MIN two-high zone when blitz left 1-on-1; 70y TD. [inferred]
- wk8 MIN@DET: Sione Vaki (RB-power/volume early-down) 11-65 0TD; 1/1tgt 5y 0TD | shell 5 man/87 zone, MOFO 61, blitz 71% | RB2 in DET run script (11-65). [confirmed-tackler]
- wk8 MIN@DET: Amon-Ra St. Brown (WR-slot separator) 1-10 0TD; 7/8tgt 46y 0TD | shell 5 man/87 zone, MOFO 61, blitz 71% | Slot volume (7/8) but capped 46y — MIN soft-middle zone gave catches, not yards. [none (no explosive)]

