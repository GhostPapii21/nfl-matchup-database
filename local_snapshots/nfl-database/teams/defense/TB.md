# TB DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 TB@CIN, wk2 CLE@TB, wk3 MIN@TB, wk4 GB@TB, wk5 TB@DAL, wk6 PIT@TB, wk7 TB@CAR, wk8 ATL@TB). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 17.2% / Zone 78.0% | MOF closed 58.6% / MOF open 39.6% | Blitz 39.9% | Light box 37.0% / Heavy box 32.2% | Sub package 63.0% | Sharp YPT allowed WR 7.2, TE 7.6, RB 5.6, Outside 7.6, Slot 7.0

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- depth deep_20+: 14.04 YPT on 24 tgts (league 12.32, +1.72), 9 catches of 20+

Holds (-1.5 YPT or better): WR1: 6.61 YPT on 54 tgts (league 8.16, -1.55); WR3+: 5.57 YPT on 35 tgts (league 7.67, -2.1)

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 48 | 39 | 262 | 0 | 0 | 5.46 | 6 | 32.80 | 5.61 | -0.15 |
| TE1 | 40 | 26 | 271 | 3 | 4 | 6.78 | 5 | 33.90 | 7.39 | -0.61 |
| TE2+ | 25 | 17 | 178 | 2 | 2 | 7.12 | 3.10 | 22.20 | 6.71 | 0.41 |
| WR1 | 54 | 31 | 357 | 2 | 3 | 6.61 | 6.80 | 44.60 | 8.16 | -1.55 |
| WR2 | 56 | 39 | 498 | 3 | 6 | 8.89 | 7 | 62.20 | 8.20 | 0.69 |
| WR3+ | 35 | 16 | 195 | 0 | 2 | 5.57 | 4.40 | 24.40 | 7.67 | -2.10 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 20 | 14 | 101 | 0 | 0 | 5.05 | 5.61 | -0.56 |
| TE1 | 16 | 8 | 86 | 1 | 1 | 5.38 | 7.39 | -2.01 |
| TE2+ | 16 | 9 | 90 | 1 | 1 | 5.62 | 6.71 | -1.09 |
| WR1 | 32 | 18 | 150 | 0 | 0 | 4.69 | 8.16 | -3.47 |
| WR2 | 34 | 23 | 321 | 2 | 4 | 9.44 | 8.20 | 1.24 |
| WR3+ | 21 | 10 | 156 | 0 | 2 | 7.43 | 7.67 | -0.24 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 75 | 59 | 312 | 1 | 0 | 4.16 | 4.58 | -0.42 |
| short_1-9 | 111 | 76 | 663 | 5 | 3 | 5.97 | 6.23 | -0.26 |
| inter_10-19 | 47 | 24 | 449 | 2 | 5 | 9.55 | 10.17 | -0.62 |
| deep_20+ | 24 | 9 | 337 | 2 | 9 | 14.04 | 12.32 | 1.72 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 17 | 6 | 205 | 2 | 4 | 12.06 | 11.28 | 0.78 |
| deep_middle | 10 | 5 | 159 | 1 | 4 | 15.90 | 14.90 | 1 |
| deep_right | 9 | 2 | 57 | 0 | 2 | 6.33 | 11.85 | -5.52 |
| short_left | 90 | 64 | 489 | 3 | 3 | 5.43 | 6.08 | -0.65 |
| short_middle | 43 | 29 | 313 | 1 | 2 | 7.28 | 7.43 | -0.15 |
| short_right | 88 | 62 | 538 | 3 | 2 | 6.11 | 5.95 | 0.16 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 48 | 26 | 466 | 3 | 6 | 9.71 | 8.94 | 0.77 |
| intermediate (aDOT 8-13) | 72 | 41 | 473 | 3 | 7 | 6.57 | 7.96 | -1.39 |
| short/YAC (aDOT <8) | 138 | 101 | 822 | 4 | 4 | 5.96 | 6.47 | -0.51 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'TE': 6, 'WR': 11} (17 total, 2.1/g)
- Pass 20+ by depth/direction: {'deep_left': 4, 'deep_middle': 4, 'deep_right': 2, 'short_left': 3, 'short_middle': 2, 'short_right': 2}
- Rush 15+ by position: {'QB': 1, 'RB': 6} (7 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 19 | 101 | 1 | 5.32 | 12.60 |
| RB | 149 | 542 | 6 | 3.64 | 67.80 |
| TE | 1 | 3 | 0 | 3 | 0.40 |
| WR | 3 | 10 | 0 | 3.33 | 1.20 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Zyon McCollum | CB | 8 | 99.80 | 32 | 4 | 23 | 273 | 34.10 | 8.53 | 0 | 2 | 7 | 2 | 0 |
| Jacob Parrish | CB | 7 | 88.70 | 34 | 4.90 | 21 | 214 | 30.60 | 6.29 | 0 | 2 | 11 | 2 | 0 |
| Keionte Scott | CB | 8 | 63.40 | 21 | 2.60 | 18 | 152 | 19 | 7.24 | 0 | 1 | 3 | 0 | 0 |
| Benjamin Morrison | CB | 2 | 56.30 | 12 | 6 | 10 | 51 | 25.50 | 4.25 | 0 | 0 | 2 | 0 | 0 |
| Josiah Trotter | LB | 6 | 90.90 | 24 | 4 | 21 | 166 | 27.70 | 6.92 | 0 | 0 | 2 | 1 | 0 |
| Alex Anzalone | LB | 7 | 98.90 | 18 | 2.60 | 15 | 163 | 23.30 | 9.06 | 0 | 2 | 0 | 3 | 0 |
| Antoine Winfield Jr. | S | 5 | 97 | 11 | 2.20 | 11 | 218 | 43.60 | 19.82 | 0 | 3 | 0 | 0 | 0 |
| Tykee Smith | S | 8 | 94.90 | 19 | 2.40 | 17 | 146 | 18.20 | 7.68 | 0 | 2 | 1 | 1 | 0 |
| Ifeatu Melifonwu | S | 2 | 62.20 | 4 | 2 | 4 | 62 | 31 | 15.50 | 0 | 1 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Zyon McCollum** (CB): WR1:10t/91y, WR2:11t/80y, TE2+:5t/40y, WR3+:3t/30y, TE1:1t/25y, RB:2t/7y | 20+: wk1 M.Gesicki(TE1) 25 short_right; wk4 M.Redman(TE2+) 25 deep_right
- **Jacob Parrish** (CB): WR2:13t/95y, WR1:11t/60y, WR3+:6t/28y, TE1:2t/13y, RB:1t/9y, TE2+:1t/9y | 20+: wk3 J.Jefferson(WR1) 22 deep_middle; wk5 G.Pickens(WR2) 21 deep_middle
- **Keionte Scott** (CB): WR2:6t/42y, WR3+:5t/39y, WR1:3t/28y, RB:5t/25y, TE1:2t/18y | 20+: wk5 R.Flournoy(WR3+) 26 short_right
- **Benjamin Morrison** (CB): WR2:3t/14y, RB:3t/13y, WR3+:2t/10y, WR1:3t/8y, TE1:1t/6y
- **Josiah Trotter** (LB): RB:13t/95y, TE1:3t/33y, WR2:4t/17y, WR1:2t/13y, TE2+:1t/8y, WR3+:1t/0y
- **Alex Anzalone** (LB): WR3+:3t/71y, TE1:4t/31y, RB:5t/29y, TE2+:2t/18y, WR1:3t/14y, WR2:1t/0y | 20+: wk2 H.Fannin(TE1) 21 short_left; wk5 R.Flournoy(WR3+) 48 deep_middle
- **Antoine Winfield Jr.** (S): WR2:2t/94y, TE1:4t/59y, RB:3t/32y, WR1:1t/29y, WR3+:1t/4y | 20+: wk1 T.Higgins(WR1) 29 short_middle; wk1 M.Gesicki(TE1) 24 deep_left; wk8 J.Dotson(WR2) 76 deep_left
- **Tykee Smith** (S): TE2+:5t/68y, TE1:7t/26y, RB:3t/22y, WR2:2t/18y, WR1:1t/12y, WR3+:1t/0y | 20+: wk5 G.Pickens(WR2) 20 short_left; wk7 M.Evans(TE2+) 32 deep_right
- **Ifeatu Melifonwu** (S): WR2:2t/36y, WR3+:1t/15y, WR1:1t/11y | 20+: wk5 G.Pickens(WR2) 27 short_left

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TB@CIN | Zyon McCollum | CB | 9 | 7 | 89 | 0 | 1 | 2 | 0 | 0 | T.Higginsx2, C.Brownx1, J.Chasex1, A.Iosivasx1, D.Samplex1, M.Gesickix1, T.Hudsonx1, D.Meyersx1 |
| 1 | TB@CIN | Antoine Winfield Jr. | S | 3 | 3 | 67 | 0 | 2 | 0 | 0 | 0 | T.Higginsx1, M.Gesickix1, S.Perinex1 |
| 1 | TB@CIN | Josiah Trotter | LB | 4 | 3 | 34 | 0 | 0 | 0 | 1 | 0 | M.Gesickix2, S.Perinex1, A.Iosivasx1 |
| 1 | TB@CIN | Keionte Scott | CB | 3 | 3 | 28 | 0 | 0 | 0 | 0 | 0 | S.Perinex1, J.Chasex1, C.Brownx1 |
| 1 | TB@CIN | Tykee Smith | S | 3 | 2 | 15 | 0 | 0 | 1 | 0 | 0 | C.Brownx1, M.Gesickix1, D.Samplex1 |
| 1 | TB@CIN | Jacob Parrish | CB | 2 | 1 | 12 | 0 | 0 | 1 | 0 | 0 | J.Chasex1, T.Higginsx1 |
| 1 | TB@CIN | Benjamin Morrison | CB | 5 | 4 | 5 | 0 | 0 | 1 | 0 | 0 | C.Brownx2, A.Iosivasx1, J.Chasex1, T.Higginsx1 |
| 2 | CLE@TB | Benjamin Morrison | CB | 7 | 6 | 46 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx2, D.Bostonx2, Q.Judkinsx1, H.Fanninx1, I.Bondx1 |
| 2 | CLE@TB | Josiah Trotter | LB | 5 | 5 | 35 | 0 | 0 | 0 | 0 | 0 | Q.Judkinsx2, R.Sandersx1, K.Concepcionx1, H.Fanninx1 |
| 2 | CLE@TB | Alex Anzalone | LB | 3 | 3 | 34 | 0 | 1 | 0 | 0 | 0 | H.Fanninx1, D.Bostonx1, Q.Judkinsx1 |
| 2 | CLE@TB | Zyon McCollum | CB | 3 | 3 | 30 | 0 | 0 | 0 | 0 | 0 | D.Bostonx2, K.Concepcionx1 |
| 2 | CLE@TB | Antoine Winfield Jr. | S | 1 | 1 | 13 | 0 | 0 | 0 | 0 | 0 | H.Fanninx1 |
| 2 | CLE@TB | Keionte Scott | CB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | H.Fanninx1 |
| 2 | CLE@TB | Tykee Smith | S | 1 | 1 | -2 | 0 | 0 | 0 | 0 | 0 | K.Concepcionx1 |
| 3 | MIN@TB | Jacob Parrish | CB | 3 | 3 | 36 | 0 | 1 | 0 | 0 | 0 | J.Addisonx2, J.Jeffersonx1 |
| 3 | MIN@TB | Tykee Smith | S | 2 | 2 | 17 | 0 | 0 | 0 | 0 | 0 | T.Hockensonx1, A.Jonesx1 |
| 3 | MIN@TB | Alex Anzalone | LB | 1 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | A.Jonesx1 |
| 3 | MIN@TB | Antoine Winfield Jr. | S | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | A.Jonesx1 |
| 3 | MIN@TB | Keionte Scott | CB | 2 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | J.Jenningsx2 |
| 3 | MIN@TB | Zyon McCollum | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | T.Feltonx1, J.Addisonx1 |
| 4 | GB@TB | Antoine Winfield Jr. | S | 3 | 3 | 51 | 0 | 0 | 0 | 0 | 0 | T.Kraftx1, C.Watsonx1, M.Lloydx1 |
| 4 | GB@TB | Zyon McCollum | CB | 2 | 2 | 41 | 0 | 1 | 0 | 0 | 0 | C.Watsonx1, M.Redmanx1 |
| 4 | GB@TB | Tykee Smith | S | 2 | 2 | 22 | 0 | 0 | 0 | 0 | 0 | T.Kraftx1, J.Smithx1 |
| 4 | GB@TB | Josiah Trotter | LB | 3 | 3 | 21 | 0 | 0 | 0 | 0 | 0 | M.Lloydx2, C.Brooksx1 |
| 4 | GB@TB | Jacob Parrish | CB | 4 | 2 | 15 | 0 | 0 | 1 | 1 | 0 | M.Goldenx2, T.Kraftx1, C.Watsonx1 |
| 4 | GB@TB | Alex Anzalone | LB | 2 | 2 | 14 | 0 | 0 | 0 | 0 | 0 | M.Goldenx1, T.Kraftx1 |
| 4 | GB@TB | Keionte Scott | CB | 3 | 3 | 14 | 0 | 0 | 0 | 0 | 0 | M.Lloydx2, T.Kraftx1 |
| 5 | TB@DAL | Jacob Parrish | CB | 13 | 9 | 98 | 0 | 1 | 4 | 0 | 0 | G.Pickensx7, J.Mingox2, J.Williamsx1, C.Lambx1, J.Fergusonx1, R.Flournoyx1 |
| 5 | TB@DAL | Alex Anzalone | LB | 5 | 4 | 66 | 0 | 1 | 0 | 1 | 0 | J.Fergusonx2, K.Turpinx1, R.Flournoyx1, L.Schoonmakerx1 |
| 5 | TB@DAL | Keionte Scott | CB | 5 | 4 | 51 | 0 | 1 | 1 | 0 | 0 | K.Turpinx1, C.Lambx1, R.Flournoyx1, J.Mingox1, G.Pickensx1 |
| 5 | TB@DAL | Ifeatu Melifonwu | S | 2 | 2 | 42 | 0 | 1 | 0 | 0 | 0 | G.Pickensx1, K.Turpinx1 |
| 5 | TB@DAL | Tykee Smith | S | 2 | 2 | 26 | 0 | 1 | 0 | 0 | 0 | G.Pickensx1, J.Fergusonx1 |
| 5 | TB@DAL | Josiah Trotter | LB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | J.Williamsx1, G.Pickensx1 |
| 5 | TB@DAL | Zyon McCollum | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | C.Lambx1, G.Pickensx1 |
| 6 | PIT@TB | Zyon McCollum | CB | 10 | 9 | 88 | 0 | 0 | 1 | 0 | 0 | D.Metcalfx5, G.Bernardx4, D.Washingtonx1 |
| 6 | PIT@TB | Josiah Trotter | LB | 6 | 5 | 43 | 0 | 0 | 1 | 0 | 0 | J.Warrenx3, D.Metcalfx1, G.Bernardx1, R.Dowdlex1 |
| 6 | PIT@TB | Keionte Scott | CB | 4 | 4 | 33 | 0 | 0 | 0 | 0 | 0 | G.Bernardx3, D.Metcalfx1 |
| 6 | PIT@TB | Jacob Parrish | CB | 5 | 3 | 30 | 0 | 0 | 2 | 0 | 0 | D.Metcalfx4, G.Bernardx1 |
| 6 | PIT@TB | Tykee Smith | S | 5 | 5 | 23 | 0 | 0 | 0 | 0 | 0 | D.Washingtonx2, P.Freiermuthx2, R.Dowdlex1 |
| 6 | PIT@TB | Alex Anzalone | LB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | D.Washingtonx1 |
| 7 | TB@CAR | Tykee Smith | S | 3 | 2 | 44 | 0 | 1 | 0 | 1 | 0 | T.McMillanx1, J.Metchiex1, M.Evansx1 |
| 7 | TB@CAR | Alex Anzalone | LB | 3 | 3 | 33 | 0 | 0 | 0 | 0 | 0 | J.Metchiex1, C.Hubbardx1, T.Etiennex1 |
| 7 | TB@CAR | Ifeatu Melifonwu | S | 2 | 2 | 20 | 0 | 0 | 0 | 0 | 0 | J.Cokerx1, T.McMillanx1 |
| 7 | TB@CAR | Josiah Trotter | LB | 4 | 3 | 18 | 0 | 0 | 1 | 0 | 0 | T.McMillanx1, C.Hubbardx1, J.Cokerx1, T.Tremblex1 |
| 7 | TB@CAR | Jacob Parrish | CB | 4 | 2 | 14 | 0 | 0 | 2 | 0 | 0 | J.Metchiex2, T.McMillanx1, D.Moorex1 |
| 7 | TB@CAR | Keionte Scott | CB | 1 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | T.Etiennex1 |
| 7 | TB@CAR | Zyon McCollum | CB | 2 | 1 | 6 | 0 | 0 | 0 | 1 | 0 | C.Hubbardx1, J.Cokerx1 |
| 8 | ATL@TB | Antoine Winfield Jr. | S | 3 | 3 | 85 | 0 | 1 | 0 | 0 | 0 | K.Pittsx1, O.Zaccheausx1, J.Dotsonx1 |
| 8 | ATL@TB | Zyon McCollum | CB | 2 | 1 | 19 | 0 | 0 | 0 | 1 | 0 | J.Dotsonx1, C.Woernerx1 |
| 8 | ATL@TB | Jacob Parrish | CB | 3 | 1 | 9 | 0 | 0 | 1 | 1 | 0 | D.Londonx1, A.Hooperx1, J.Dotsonx1 |
| 8 | ATL@TB | Keionte Scott | CB | 2 | 1 | 8 | 0 | 0 | 1 | 0 | 0 | J.Dotsonx1, D.Londonx1 |
| 8 | ATL@TB | Alex Anzalone | LB | 3 | 1 | 3 | 0 | 0 | 0 | 2 | 0 | D.Londonx1, J.Dotsonx1, K.Herbertx1 |
| 8 | ATL@TB | Tykee Smith | S | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | K.Pittsx1 |

## Who beat them each week

**Wk1 TB@CIN** (vs CIN offense, 254 rec yds allowed; 12% of targets unattributed)
- Top receivers: M.Gesicki (TE1, intermediate (aDOT 8-13)) 5/7 78y 1TD; T.Higgins (WR1, deep (aDOT 13+)) 3/6 59y; S.Perine (RB, short/YAC (aDOT <8)) 3/3 30y; C.Brown (RB, short/YAC (aDOT <8)) 5/6 22y
- 20+ catches: M.Gesicki(TE1) 25y short_right - Z.McCollum [tackler]; T.Higgins(WR1) 29y short_middle - A.Winfield [tackler]; M.Gesicki(TE1) 24y deep_left - A.Winfield [tackler]

**Wk2 CLE@TB** (vs CLE offense, 238 rec yds allowed; 23% of targets unattributed)
- Top receivers: D.Boston (WR1, deep (aDOT 13+)) 5/7 95y 1TD; H.Fannin (TE1, short/YAC (aDOT <8)) 5/6 54y; K.Concepcion (WR2, short/YAC (aDOT <8)) 6/6 28y; Q.Judkins (RB, short/YAC (aDOT <8)) 5/5 27y
- 20+ catches: H.Fannin(TE1) 21y short_left - A.Anzalone [tackler]; D.Boston(WR1) 55y short_middle TD - no tackler named [unattributed]

**Wk3 MIN@TB** (vs MIN offense, 168 rec yds allowed; 28% of targets unattributed)
- Top receivers: J.Addison (WR2, deep (aDOT 13+)) 5/9 90y 1TD; A.Jones (RB, short/YAC (aDOT <8)) 5/6 34y; J.Jefferson (WR1, intermediate (aDOT 8-13)) 2/2 32y; T.Hockenson (TE1, short/YAC (aDOT <8)) 2/4 11y
- 20+ catches: J.Jefferson(WR1) 22y deep_middle - J.Parrish [tackler]; J.Addison(WR2) 30y deep_left - no tackler named [unattributed]; J.Addison(WR2) 41y deep_left TD - no tackler named [unattributed]

**Wk4 GB@TB** (vs GB offense, 197 rec yds allowed; 30% of targets unattributed)
- Top receivers: C.Watson (WR2, deep (aDOT 13+)) 3/3 47y; T.Kraft (TE1, short/YAC (aDOT <8)) 6/7 42y 1TD; M.Lloyd (RB, short/YAC (aDOT <8)) 5/5 36y; M.Redman (TE2+, deep (aDOT 13+)) 2/2 29y
- 20+ catches: M.Redman(TE2+) 25y deep_right - Z.McCollum [tackler]
- 15+ runs: C.Brooks(RB) 27y rush left tackle; K.Johnson(RB) 31y rush middle

**Wk5 TB@DAL** (vs DAL offense, 316 rec yds allowed; 23% of targets unattributed)
- Top receivers: G.Pickens (WR2, intermediate (aDOT 8-13)) 9/13 130y 1TD; R.Flournoy (WR3+, short/YAC (aDOT <8)) 3/5 90y; K.Turpin (WR3+, short/YAC (aDOT <8)) 2/4 22y; J.Mingo (WR3+, deep (aDOT 13+)) 2/4 20y
- 20+ catches: G.Pickens(WR2) 21y deep_middle - J.Parrish [tackler]; R.Flournoy(WR3+) 48y deep_middle - A.Anzalone [tackler]; G.Pickens(WR2) 27y short_left - I.Melifonwu [tackler]; G.Pickens(WR2) 20y short_left - T.Smith [tackler]; R.Flournoy(WR3+) 26y short_right - K.Scott [tackler]
- 15+ runs: J.Williams(RB) 21y rush middle

**Wk6 PIT@TB** (vs PIT offense, 253 rec yds allowed; 14% of targets unattributed)
- Top receivers: D.Metcalf (WR1, intermediate (aDOT 8-13)) 11/15 93y; G.Bernard (WR2, short/YAC (aDOT <8)) 11/12 87y 1TD; J.Warren (RB, short/YAC (aDOT <8)) 2/4 28y; D.Washington (TE2+, short/YAC (aDOT <8)) 4/6 25y 1TD
- 15+ runs: J.Warren(RB) 16y rush right end; R.Dowdle(RB) 15y rush right guard

**Wk7 TB@CAR** (vs CAR offense, 210 rec yds allowed; 28% of targets unattributed)
- Top receivers: D.Waller (TE1, intermediate (aDOT 8-13)) 1/2 50y 1TD; T.McMillan (WR1, intermediate (aDOT 8-13)) 4/6 40y; M.Evans (TE2+, short/YAC (aDOT <8)) 2/2 39y; C.Hubbard (RB, short/YAC (aDOT <8)) 4/5 27y
- 20+ catches: D.Waller(TE1) 50y deep_middle TD - no tackler named [unattributed]; M.Evans(TE2+) 32y deep_right - T.Smith [tackler]
- 15+ runs: K.Pickett(QB) 15y rush middle

**Wk8 ATL@TB** (vs ATL offense, 125 rec yds allowed; 35% of targets unattributed)
- Top receivers: J.Dotson (WR2, deep (aDOT 13+)) 2/5 95y; A.Hooper (TE2+, short/YAC (aDOT <8)) 1/1 9y; D.London (WR1, intermediate (aDOT 8-13)) 1/6 8y; K.Pitts (TE1, short/YAC (aDOT <8)) 2/5 6y
- 20+ catches: J.Dotson(WR2) 76y deep_left - A.Winfield [tackler]
- 15+ runs: Bi.Robinson(RB) 26y rush left guard

## Seed notes from defenders/TB_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q2 14:54 Bijan Robinson (RB) rush 26 — J.Parrish [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 4:35 Jahan Dotson (WR) rec 76 — Zyon McCollum [inferred; pregame matchup: ESPN WR/CB cheat sheet 10/29 + week8 coverage.json (two sources agree)]; alignment: outside, offense-right side (pregame target-side proxy; ESPN season split L33/S23/R44)
- Zyon McCollum ← Jahan Dotson: 4 tgt, 2 rec, 95 yds
- Jacob Parrish ← Drake London: 4 tgt, 1 rec, 8 yds — limited his man
- Keionte Scott ← Olamide Zaccheaus: 2 tgt, 1 rec, 4 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 ATL@TB: Jahan Dotson (WR-deep speed) 2/5tgt 95y 0TD | shell 17 man/78 zone, MOFC 59 | One 76y deep left shot vs TB zone (MOFC 59) — pregame matchup McCollum (outside right, inferred), Winfield tackled. Deep-speed WR vs single-high zone in garbage time. [inferred]
- wk8 ATL@TB: Bijan Robinson (RB-home-run zone runner) 19-76 0TD; 0/1tgt 0y 0TD | shell 17 man/78 zone, MOFC 59 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]

