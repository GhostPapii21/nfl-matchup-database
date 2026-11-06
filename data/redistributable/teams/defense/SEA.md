# SEA DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 NE@SEA, wk2 SEA@ARI, wk3 SEA@WSH, wk4 LAC@SEA, wk5 SF@SEA, wk6 SEA@DEN, wk7 KC@SEA, wk8 CHI@SEA). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 5.4% / Zone 90.0% | MOF closed 36.9% / MOF open 60.6% | Blitz 20.9% | Light box 50.0% / Heavy box 15.9% | Sub package 87.0% | Sharp YPT allowed WR 5.8, TE 5.2, RB 5.1, Outside 7.5, Slot 3.8

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- nothing flagged

Holds (-1.5 YPT or better): TE1: 5.41 YPT on 46 tgts (league 7.39, -1.98); WR1: 5.68 YPT on 59 tgts (league 8.16, -2.48); WR3+: 5.53 YPT on 49 tgts (league 7.67, -2.14)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 48 | 41 | 244 | 2 | 0 | 5.08 | 6 | 30.50 | 5.61 | -0.53 |
| TE1 | 46 | 34 | 249 | 1 | 0 | 5.41 | 5.80 | 31.10 | 7.39 | -1.98 |
| TE2+ | 9 | 6 | 57 | 1 | 0 | 6.33 | 1.10 | 7.10 | 6.71 | -0.38 |
| WR1 | 59 | 35 | 335 | 2 | 6 | 5.68 | 7.40 | 41.90 | 8.16 | -2.48 |
| WR2 | 24 | 13 | 197 | 0 | 4 | 8.21 | 3 | 24.60 | 8.20 | 0.01 |
| WR3+ | 49 | 28 | 271 | 3 | 2 | 5.53 | 6.10 | 33.90 | 7.67 | -2.14 |
| other | 1 | 0 | 0 | 0 | 0 | 0 | 0.10 | 0 | 2.86 | -2.86 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 22 | 18 | 110 | 0 | 0 | 5 | 5.61 | -0.61 |
| TE1 | 25 | 18 | 146 | 0 | 0 | 5.84 | 7.39 | -1.55 |
| TE2+ | 4 | 3 | 44 | 0 | 0 | 11 | 6.71 | 4.29 |
| WR1 | 33 | 21 | 204 | 2 | 4 | 6.18 | 8.16 | -1.98 |
| WR2 | 12 | 8 | 127 | 0 | 3 | 10.58 | 8.20 | 2.38 |
| WR3+ | 22 | 11 | 77 | 1 | 0 | 3.50 | 7.67 | -4.17 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 69 | 57 | 305 | 1 | 1 | 4.42 | 4.58 | -0.16 |
| short_1-9 | 101 | 75 | 551 | 6 | 0 | 5.46 | 6.23 | -0.77 |
| inter_10-19 | 38 | 18 | 299 | 1 | 4 | 7.87 | 10.17 | -2.30 |
| deep_20+ | 27 | 7 | 198 | 1 | 7 | 7.33 | 12.32 | -4.99 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 17 | 4 | 93 | 1 | 3 | 5.47 | 11.28 | -5.81 |
| deep_middle | 10 | 7 | 148 | 0 | 4 | 14.80 | 14.90 | -0.10 |
| deep_right | 20 | 4 | 117 | 0 | 3 | 5.85 | 11.85 | -6 |
| short_left | 70 | 58 | 381 | 4 | 0 | 5.44 | 6.08 | -0.64 |
| short_middle | 35 | 23 | 207 | 3 | 1 | 5.91 | 7.43 | -1.52 |
| short_right | 83 | 61 | 407 | 1 | 1 | 4.90 | 5.95 | -1.05 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 37 | 23 | 342 | 2 | 7 | 9.24 | 8.94 | 0.30 |
| intermediate (aDOT 8-13) | 69 | 35 | 315 | 2 | 3 | 4.57 | 7.96 | -3.39 |
| short/YAC (aDOT <8) | 130 | 99 | 696 | 5 | 2 | 5.35 | 6.47 | -1.12 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'WR': 12} (12 total, 1.5/g)
- Pass 20+ by depth/direction: {'deep_left': 3, 'deep_middle': 4, 'deep_right': 3, 'short_middle': 1, 'short_right': 1}
- Rush 15+ by position: {'QB': 2, 'RB': 5, 'WR': 1} (8 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 26 | 134 | 2 | 5.15 | 16.80 |
| RB | 178 | 583 | 5 | 3.28 | 72.90 |
| TE | 1 | 2 | 0 | 2 | 0.20 |
| WR | 4 | 39 | 1 | 9.75 | 4.90 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Devon Witherspoon | CB | 7 | 98.90 | 30 | 4.30 | 27 | 177 | 25.30 | 5.90 | 0 | 1 | 3 | 0 | 0 |
| Josh Jobe | CB | 7 | 99 | 18 | 2.60 | 17 | 150 | 21.40 | 8.33 | 0 | 3 | 0 | 1 | 0 |
| Nehemiah Pritchett | CB | 6 | 36.40 | 11 | 1.80 | 6 | 60 | 10 | 5.45 | 0 | 1 | 3 | 2 | 0 |
| Trevon Diggs | CB | 1 | 11 | 1 | 1 | 1 | 6 | 6 | 6 | 0 | 0 | 0 | 0 | 0 |
| Ernest Jones | LB | 8 | 99.50 | 33 | 4.10 | 29 | 234 | 29.20 | 7.09 | 0 | 0 | 3 | 1 | 0 |
| Drake Thomas | LB | 4 | 86.20 | 11 | 2.80 | 10 | 57 | 14.20 | 5.18 | 0 | 0 | 0 | 1 | 0 |
| Uchenna Nwosu | OLB | 5 | 51 | 6 | 1.20 | 3 | 18 | 3.60 | 3 | 0 | 0 | 3 | 0 | 0 |
| Julian Love | S | 7 | 98.10 | 20 | 2.90 | 14 | 170 | 24.30 | 8.50 | 0 | 3 | 4 | 2 | 0 |
| Ty Okada | S | 4 | 97.80 | 10 | 2.50 | 9 | 113 | 28.20 | 11.30 | 0 | 0 | 0 | 1 | 0 |
| Rodney Thomas | S | 4 | 67.80 | 8 | 2 | 6 | 97 | 24.20 | 12.12 | 0 | 2 | 2 | 0 | 0 |
| Nick Emmanwori | S | 4 | 75.70 | 9 | 2.20 | 8 | 67 | 16.80 | 7.44 | 0 | 0 | 1 | 0 | 0 |
| AJ Finley | S | 1 | 52 | 2 | 2 | 2 | 23 | 23 | 11.50 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Devon Witherspoon** (CB): TE1:9t/56y, WR2:5t/48y, RB:8t/30y, WR1:4t/25y, WR3+:3t/16y, TE2+:1t/2y | 20+: wk8 R.Odunze(WR2) 24 deep_left
- **Josh Jobe** (CB): WR1:7t/77y, WR3+:7t/37y, WR2:1t/23y, RB:3t/13y | 20+: wk5 M.Evans(WR1) 23 deep_middle; wk5 M.Evans(WR1) 28 deep_right; wk8 R.Odunze(WR2) 23 deep_middle
- **Nehemiah Pritchett** (CB): WR2:4t/31y, WR3+:6t/28y, WR1:1t/1y | 20+: wk8 R.Odunze(WR2) 22 short_middle
- **Trevon Diggs** (CB): WR1:1t/6y
- **Ernest Jones** (LB): TE1:12t/101y, RB:9t/74y, WR1:5t/24y, WR3+:4t/20y, WR2:2t/9y, TE2+:1t/6y
- **Drake Thomas** (LB): RB:5t/22y, TE1:4t/15y, WR1:1t/11y, TE2+:1t/9y
- **Uchenna Nwosu** (OLB): WR3+:2t/15y, TE1:1t/3y, RB:2t/0y, WR1:1t/0y
- **Julian Love** (S): WR1:9t/88y, TE1:6t/33y, WR2:2t/32y, WR3+:1t/9y, RB:2t/8y | 20+: wk4 T.Harris(WR1) 26 deep_right; wk5 M.Evans(WR1) 23 deep_middle; wk8 L.Burden(WR1) 23 deep_middle
- **Ty Okada** (S): TE2+:2t/38y, WR1:3t/28y, RB:2t/19y, WR3+:2t/18y, WR2:1t/10y
- **Rodney Thomas** (S): WR2:1t/44y, WR1:4t/34y, WR3+:2t/19y, TE1:1t/0y | 20+: wk4 Q.Johnston(WR2) 44 deep_right; wk4 T.Harris(WR1) 21 deep_left
- **Nick Emmanwori** (S): RB:3t/26y, WR1:2t/20y, TE1:1t/12y, WR3+:2t/9y, other:1t/0y
- **AJ Finley** (S): WR3+:2t/23y | 20+: wk3 J.Lane(WR3+) 21 short_right

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NE@SEA | Ernest Jones | LB | 6 | 6 | 58 | 0 | 0 | 0 | 0 | 0 | M.Hollinsx2, R.Stevensonx2, D.Douglasx1, H.Henryx1 |
| 1 | NE@SEA | Rodney Thomas | S | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | D.Douglasx2, M.Hollinsx1 |
| 1 | NE@SEA | Josh Jobe | CB | 5 | 4 | 26 | 0 | 0 | 0 | 1 | 0 | L.Larisonx2, M.Hollinsx2, A.Brownx1 |
| 1 | NE@SEA | Nehemiah Pritchett | CB | 5 | 3 | 22 | 0 | 0 | 1 | 1 | 0 | A.Brownx3, R.Doubsx1, D.Douglasx1 |
| 1 | NE@SEA | Julian Love | S | 3 | 2 | 18 | 0 | 0 | 0 | 1 | 0 | H.Henryx1, R.Stevensonx1, D.Douglasx1 |
| 1 | NE@SEA | Drake Thomas | LB | 2 | 2 | 16 | 0 | 0 | 0 | 0 | 0 | R.Stevensonx2 |
| 1 | NE@SEA | Uchenna Nwosu | OLB | 2 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | H.Henryx1, R.Stevensonx1 |
| 2 | SEA@ARI | Devon Witherspoon | CB | 5 | 5 | 29 | 0 | 0 | 0 | 0 | 0 | T.Allgeierx2, K.Bournex2, T.McBridex1 |
| 2 | SEA@ARI | Ernest Jones | LB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | T.McBridex2, J.Lovex1 |
| 2 | SEA@ARI | Drake Thomas | LB | 4 | 4 | 19 | 0 | 0 | 0 | 0 | 0 | T.McBridex2, J.Lovex2 |
| 2 | SEA@ARI | Julian Love | S | 5 | 3 | 16 | 0 | 0 | 1 | 1 | 0 | T.McBridex3, Mi.Wilsonx2 |
| 2 | SEA@ARI | Josh Jobe | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | Mi.Wilsonx1 |
| 2 | SEA@ARI | Rodney Thomas | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | T.McBridex1 |
| 3 | SEA@WSH | Devon Witherspoon | CB | 5 | 5 | 37 | 0 | 0 | 0 | 0 | 0 | S.Diggsx2, T.McLaurinx1, C.Yankoffx1, A.Williamsx1 |
| 3 | SEA@WSH | AJ Finley | S | 2 | 2 | 23 | 0 | 1 | 0 | 0 | 0 | J.Lanex1, T.Burksx1 |
| 3 | SEA@WSH | Drake Thomas | LB | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | S.Diggsx1, J.Batesx1 |
| 3 | SEA@WSH | Ernest Jones | LB | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | A.Williamsx2, J.Croskey-Merrittx1 |
| 3 | SEA@WSH | Josh Jobe | CB | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | T.McLaurinx2 |
| 3 | SEA@WSH | Nehemiah Pritchett | CB | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | T.McLaurinx1 |
| 3 | SEA@WSH | Rodney Thomas | S | 2 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | T.McLaurinx1, S.Diggsx1 |
| 3 | SEA@WSH | Uchenna Nwosu | OLB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | S.Diggsx1 |
| 4 | LAC@SEA | Rodney Thomas | S | 2 | 2 | 65 | 0 | 2 | 0 | 0 | 0 | Q.Johnstonx1, T.Harrisx1 |
| 4 | LAC@SEA | Devon Witherspoon | CB | 6 | 6 | 33 | 0 | 0 | 0 | 0 | 0 | O.Gadsdenx3, O.Hamptonx2, K.Mitchellx1 |
| 4 | LAC@SEA | Julian Love | S | 2 | 1 | 26 | 0 | 1 | 1 | 0 | 0 | O.Gadsdenx1, T.Harrisx1 |
| 4 | LAC@SEA | Nick Emmanwori | S | 4 | 3 | 23 | 0 | 0 | 1 | 0 | 0 | K.Mitchellx2, T.Harrisx1, J.Herbertx1 |
| 4 | LAC@SEA | Ernest Jones | LB | 3 | 2 | 11 | 0 | 0 | 0 | 1 | 0 | L.McConkeyx1, K.Vidalx1, O.Gadsdenx1 |
| 4 | LAC@SEA | Uchenna Nwosu | OLB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | D.Davisx1 |
| 4 | LAC@SEA | Drake Thomas | LB | 3 | 2 | 2 | 0 | 0 | 0 | 1 | 0 | O.Gadsdenx2, K.Mitchellx1 |
| 4 | LAC@SEA | Nehemiah Pritchett | CB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | M.Valdes-Scantlingx1 |
| 5 | SF@SEA | Josh Jobe | CB | 3 | 3 | 60 | 0 | 2 | 0 | 0 | 0 | M.Evansx3 |
| 5 | SF@SEA | Julian Love | S | 4 | 3 | 50 | 0 | 1 | 1 | 0 | 0 | M.Evansx2, D.Samuelx1, G.Kittlex1 |
| 5 | SF@SEA | Ernest Jones | LB | 6 | 5 | 24 | 0 | 0 | 1 | 0 | 0 | G.Kittlex3, C.McCaffreyx2, B.Cooksx1 |
| 5 | SF@SEA | Ty Okada | S | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | M.Evansx1 |
| 5 | SF@SEA | Uchenna Nwosu | OLB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | J.Cowingx1 |
| 5 | SF@SEA | Devon Witherspoon | CB | 3 | 2 | 6 | 0 | 0 | 1 | 0 | 0 | G.Kittlex2, D.Samuelx1 |
| 5 | SF@SEA | Nehemiah Pritchett | CB | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | J.Cowingx1 |
| 6 | SEA@DEN | Ty Okada | S | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | J.Waddlex1, R.Harveyx1, C.Suttonx1 |
| 6 | SEA@DEN | Nick Emmanwori | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | R.Harveyx1, T.Franklinx1 |
| 6 | SEA@DEN | Devon Witherspoon | CB | 5 | 3 | 16 | 0 | 0 | 2 | 0 | 0 | M.Mimsx2, J.Waddlex2, E.Engramx1 |
| 6 | SEA@DEN | Ernest Jones | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | E.Engramx1 |
| 6 | SEA@DEN | Nehemiah Pritchett | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | C.Suttonx1 |
| 6 | SEA@DEN | Josh Jobe | CB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | J.Dobbinsx1, J.Waddlex1 |
| 6 | SEA@DEN | Trevon Diggs | CB | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | J.Waddlex1 |
| 6 | SEA@DEN | Julian Love | S | 2 | 1 | 3 | 0 | 0 | 1 | 0 | 0 | J.Waddlex1, R.Harveyx1 |
| 6 | SEA@DEN | Uchenna Nwosu | OLB | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | R.Harveyx1 |
| 7 | KC@SEA | Ty Okada | S | 5 | 4 | 63 | 0 | 0 | 0 | 1 | 0 | N.Grayx2, C.Allenx1, J.Royalsx1, K.Walkerx1 |
| 7 | KC@SEA | Ernest Jones | LB | 5 | 5 | 42 | 0 | 0 | 0 | 0 | 0 | T.Kelcex2, N.Grayx1, X.Worthyx1, E.Johnsonx1 |
| 7 | KC@SEA | Devon Witherspoon | CB | 3 | 3 | 26 | 0 | 0 | 0 | 0 | 0 | K.Walkerx2, T.Kelcex1 |
| 7 | KC@SEA | Julian Love | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | X.Worthyx1 |
| 7 | KC@SEA | Nick Emmanwori | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | J.Watsonx1 |
| 7 | KC@SEA | Josh Jobe | CB | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | X.Worthyx1 |
| 8 | CHI@SEA | Ernest Jones | LB | 6 | 5 | 54 | 0 | 0 | 1 | 0 | 0 | L.Burdenx3, C.Lovelandx2, R.Johnsonx1 |
| 8 | CHI@SEA | Julian Love | S | 3 | 3 | 50 | 0 | 1 | 0 | 0 | 0 | L.Burdenx1, R.Odunzex1, K.Raymondx1 |
| 8 | CHI@SEA | Josh Jobe | CB | 4 | 4 | 35 | 0 | 1 | 0 | 0 | 0 | Z.Thomasx1, L.Burdenx1, K.Raymondx1, R.Odunzex1 |
| 8 | CHI@SEA | Devon Witherspoon | CB | 3 | 3 | 30 | 0 | 1 | 0 | 0 | 0 | C.Lovelandx1, R.Odunzex1, D.Swiftx1 |
| 8 | CHI@SEA | Nehemiah Pritchett | CB | 2 | 1 | 22 | 0 | 1 | 1 | 0 | 0 | R.Odunzex2 |
| 8 | CHI@SEA | Nick Emmanwori | S | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1, C.Lovelandx1 |
| 8 | CHI@SEA | Ty Okada | S | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1 |

## Who beat them each week

**Wk1 NE@SEA** (vs NE offense, 178 rec yds allowed; 16% of targets unattributed)
- Top receivers: M.Hollins (WR3+, deep (aDOT 13+)) 4/5 51y; R.Stevenson (RB, short/YAC (aDOT <8)) 5/6 44y; A.Brown (WR3+, deep (aDOT 13+)) 3/4 26y; H.Henry (TE1, short/YAC (aDOT <8)) 3/3 26y
- 15+ runs: D.Maye(QB) 16y rush left tackle

**Wk2 SEA@ARI** (vs ARI offense, 95 rec yds allowed; 23% of targets unattributed)
- Top receivers: T.McBride (TE1, short/YAC (aDOT <8)) 8/10 41y 1TD; Mi.Wilson (WR1, intermediate (aDOT 8-13)) 2/7 18y; J.Love (RB, short/YAC (aDOT <8)) 3/3 16y; K.Bourne (WR2, short/YAC (aDOT <8)) 2/3 11y
- 15+ runs: Z.Knight(RB) 18y rush middle

**Wk3 SEA@WSH** (vs WSH offense, 183 rec yds allowed; 40% of targets unattributed)
- Top receivers: T.McLaurin (WR3+, intermediate (aDOT 8-13)) 6/9 77y 1TD; S.Diggs (WR1, intermediate (aDOT 8-13)) 4/7 33y; J.Lane (WR3+, short/YAC (aDOT <8)) 1/1 21y; A.Williams (WR2, intermediate (aDOT 8-13)) 2/4 15y
- 20+ catches: J.Lane(WR3+) 21y short_right - A.Finley [tackler]; T.McLaurin(WR3+) 30y deep_left TD - no tackler named [unattributed]
- 15+ runs: R.White(RB) 19y rush right end

**Wk4 LAC@SEA** (vs LAC offense, 189 rec yds allowed; 26% of targets unattributed)
- Top receivers: T.Harris (WR1, intermediate (aDOT 8-13)) 3/5 60y; Q.Johnston (WR2, deep (aDOT 13+)) 1/2 44y; O.Gadsden (TE1, short/YAC (aDOT <8)) 5/8 36y; K.Mitchell (RB, short/YAC (aDOT <8)) 5/6 24y
- 20+ catches: T.Harris(WR1) 26y deep_right - J.Love [tackler]; Q.Johnston(WR2) 44y deep_right - R.Thomas [tackler]; T.Harris(WR1) 21y deep_left - R.Thomas [tackler]
- 15+ runs: O.Hampton(RB) 15y rush right guard; J.Herbert(QB) 26y rush middle; K.Mitchell(RB) 20y rush right end

**Wk5 SF@SEA** (vs SF offense, 189 rec yds allowed; 25% of targets unattributed)
- Top receivers: M.Evans (WR1, deep (aDOT 13+)) 7/11 113y 1TD; G.Kittle (TE1, short/YAC (aDOT <8)) 5/6 24y; D.Samuel (WR2, short/YAC (aDOT <8)) 2/3 21y; C.McCaffrey (RB, short/YAC (aDOT <8)) 3/3 15y
- 20+ catches: M.Evans(WR1) 23y deep_middle - J.Jobe [tackler]; M.Evans(WR1) 23y deep_middle - J.Love [tackler]; M.Evans(WR1) 28y deep_right - J.Jobe [tackler]

**Wk6 SEA@DEN** (vs DEN offense, 107 rec yds allowed; 12% of targets unattributed)
- Top receivers: R.Harvey (RB, short/YAC (aDOT <8)) 3/4 31y; J.Waddle (WR1, intermediate (aDOT 8-13)) 4/7 24y; C.Sutton (WR2, intermediate (aDOT 8-13)) 2/3 19y; M.Mims (WR3+, short/YAC (aDOT <8)) 2/4 13y
- 15+ runs: J.Dobbins(RB) 16y rush left guard

**Wk7 KC@SEA** (vs KC offense, 165 rec yds allowed; 34% of targets unattributed)
- Top receivers: T.Kelce (TE1, short/YAC (aDOT <8)) 4/8 44y; N.Gray (TE2+, short/YAC (aDOT <8)) 3/3 44y; K.Walker (RB, short/YAC (aDOT <8)) 4/5 21y; C.Allen (WR3+, intermediate (aDOT 8-13)) 1/2 18y

**Wk8 CHI@SEA** (vs CHI offense, 247 rec yds allowed; 26% of targets unattributed)
- Top receivers: R.Odunze (WR2, deep (aDOT 13+)) 4/6 87y; C.Loveland (TE1, short/YAC (aDOT <8)) 7/9 65y; L.Burden (WR1, short/YAC (aDOT <8)) 7/9 56y 1TD; K.Raymond (WR3+, short/YAC (aDOT <8)) 2/3 14y
- 20+ catches: L.Burden(WR1) 23y deep_middle - J.Love [tackler]; R.Odunze(WR2) 24y deep_left - D.Witherspoon [tackler]; R.Odunze(WR2) 23y deep_middle - J.Jobe [tackler]; R.Odunze(WR2) 22y short_middle - N.Pritchett [tackler]
- 15+ runs: K.Raymond(WR) 39y rush right end

## MNF CHI@SEA live log (runs/2026-11-02_CHI@SEA_r3/live/sea_defender_log.csv, ESPN text, tackler/PBU tag, not true coverage)

By target, depth x direction (tgt / catches / yds / tacklers / PBU):

- C.Loveland deep right: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: L.Williams
- C.Loveland short middle: 4 tgt, 3 rec, 26 yds; tacklers: B.Murphy, E.Jones, N.Emmanwori; PBU: -
- C.Loveland short right: 4 tgt, 4 rec, 40 yds; tacklers: E.Jones, D.Witherspoon, J.Jackson; PBU: -
- D.Swift short left: 2 tgt, 1 rec, 2 yds; tacklers: D.Witherspoon; PBU: -
- D.Swift short right: 1 tgt, 1 rec, 8 yds; tacklers: J.Reed; PBU: -
- K.Raymond deep left: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- K.Raymond short left: 1 tgt, 1 rec, 5 yds; tacklers: J.Jobe; PBU: -
- K.Raymond short middle: 1 tgt, 1 rec, 9 yds; tacklers: J.Love; PBU: -
- L.Burden deep left: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- L.Burden deep middle: 1 tgt, 1 rec, 23 yds; tacklers: J.Love; PBU: -
- L.Burden short left: 2 tgt, 2 rec, 8 yds; tacklers: T.Okada, J.Jobe; PBU: -
- L.Burden short middle: 2 tgt, 1 rec, 8 yds; tacklers: E.Jones; PBU: -
- L.Burden short right: 3 tgt, 3 rec, 17 yds; tacklers: E.Jones, N.Emmanwori; PBU: -
- R.Johnson short left: 1 tgt, 1 rec, 11 yds; tacklers: D.Witherspoon; PBU: -
- R.Odunze deep left: 2 tgt, 1 rec, 24 yds; tacklers: D.Witherspoon; PBU: -
- R.Odunze deep middle: 3 tgt, 2 rec, 41 yds; tacklers: J.Love, J.Jobe; PBU: -
- R.Odunze short middle: 1 tgt, 1 rec, 22 yds; tacklers: N.Pritchett; PBU: N.Emmanwori
- Z.Thomas deep middle: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- Z.Thomas deep right: 1 tgt, 0 rec, 0 yds; tacklers: -; PBU: -
- Z.Thomas short left: 1 tgt, 1 rec, 4 yds; tacklers: J.Jobe; PBU: -

Tackler-after-catch totals: J.Love 3 rec/50y (K.Raymond, L.Burden, R.Odunze); E.Jones 4 rec/43y (C.Loveland, L.Burden); D.Witherspoon 4 rec/41y (C.Loveland, D.Swift, R.Johnson, R.Odunze); J.Jobe 4 rec/35y (K.Raymond, L.Burden, R.Odunze, Z.Thomas); N.Pritchett 1 rec/22y (R.Odunze); N.Emmanwori 2 rec/19y (C.Loveland, L.Burden); J.Jackson 1 rec/9y (C.Loveland); J.Reed 1 rec/8y (D.Swift); T.Okada 1 rec/5y (L.Burden); B.Murphy 1 rec/0y (C.Loveland)

