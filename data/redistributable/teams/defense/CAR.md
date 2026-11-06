# CAR DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 7 (wk1 CHI@CAR, wk2 CAR@ATL, wk3 CAR@CLE, wk4 DET@CAR, wk6 CAR@PHI, wk7 TB@CAR, wk8 CAR@GB). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 11.6% / Zone 83.3% | MOF closed 56.8% / MOF open 39.6% | Blitz 38.8% | Light box 45.0% / Heavy box 18.3% | Sub package 67.0% | Sharp YPT allowed WR 7.3, TE 5.9, RB 4.7, Outside 8.7, Slot 5.9

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- nothing flagged

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 42 | 32 | 186 | 1 | 0 | 4.43 | 6 | 26.60 | 5.61 | -1.18 |
| TE1 | 42 | 28 | 264 | 4 | 2 | 6.29 | 6 | 37.70 | 7.39 | -1.10 |
| TE2+ | 11 | 6 | 67 | 1 | 1 | 6.09 | 1.60 | 9.60 | 6.71 | -0.62 |
| WR1 | 45 | 29 | 337 | 1 | 3 | 7.49 | 6.40 | 48.10 | 8.16 | -0.67 |
| WR2 | 53 | 31 | 389 | 1 | 4 | 7.34 | 7.60 | 55.60 | 8.20 | -0.86 |
| WR3+ | 40 | 25 | 294 | 2 | 2 | 7.35 | 5.70 | 42 | 7.67 | -0.32 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 25 | 18 | 84 | 1 | 0 | 3.36 | 5.61 | -2.25 |
| TE1 | 28 | 20 | 198 | 2 | 2 | 7.07 | 7.39 | -0.32 |
| TE2+ | 3 | 2 | 12 | 0 | 0 | 4 | 6.71 | -2.71 |
| WR1 | 30 | 18 | 182 | 1 | 1 | 6.07 | 8.16 | -2.09 |
| WR2 | 37 | 25 | 317 | 1 | 3 | 8.57 | 8.20 | 0.37 |
| WR3+ | 22 | 12 | 186 | 1 | 1 | 8.45 | 7.67 | 0.78 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 49 | 35 | 193 | 0 | 0 | 3.94 | 4.58 | -0.64 |
| short_1-9 | 111 | 81 | 612 | 4 | 0 | 5.51 | 6.23 | -0.72 |
| inter_10-19 | 48 | 28 | 452 | 4 | 5 | 9.42 | 10.17 | -0.75 |
| deep_20+ | 24 | 7 | 280 | 2 | 7 | 11.67 | 12.32 | -0.65 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| ?_? | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| deep_left | 8 | 5 | 155 | 2 | 5 | 19.38 | 11.28 | 8.10 |
| deep_middle | 8 | 2 | 71 | 0 | 1 | 8.88 | 14.90 | -6.02 |
| deep_right | 20 | 5 | 162 | 1 | 3 | 8.10 | 11.85 | -3.75 |
| short_left | 66 | 41 | 329 | 1 | 1 | 4.98 | 6.08 | -1.10 |
| short_middle | 46 | 38 | 396 | 2 | 2 | 8.61 | 7.43 | 1.18 |
| short_right | 84 | 60 | 424 | 4 | 0 | 5.05 | 5.95 | -0.90 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 52 | 33 | 472 | 3 | 6 | 9.08 | 8.94 | 0.14 |
| intermediate (aDOT 8-13) | 43 | 25 | 320 | 1 | 1 | 7.44 | 7.96 | -0.52 |
| short/YAC (aDOT <8) | 138 | 93 | 745 | 6 | 5 | 5.40 | 6.47 | -1.07 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'TE': 3, 'WR': 9} (12 total, 1.7/g)
- Pass 20+ by depth/direction: {'deep_left': 5, 'deep_middle': 1, 'deep_right': 3, 'short_left': 1, 'short_middle': 2}
- Rush 15+ by position: {'QB': 2, 'RB': 8, 'WR': 1} (11 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| QB | 25 | 149 | 2 | 5.96 | 21.30 |
| RB | 171 | 809 | 8 | 4.73 | 115.60 |
| WR | 4 | 32 | 1 | 8 | 4.60 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Will Lee III | CB | 6 | 73 | 27 | 4.50 | 21 | 239 | 39.80 | 8.85 | 0 | 2 | 6 | 0 | 0 |
| Akayleb Evans | CB | 4 | 72.80 | 15 | 3.80 | 13 | 176 | 44 | 11.73 | 0 | 2 | 2 | 0 | 0 |
| Jaycee Horn | CB | 3 | 87.30 | 5 | 1.70 | 4 | 59 | 19.70 | 11.80 | 0 | 1 | 1 | 0 | 0 |
| Marco Wilson | CB | 1 | 100 | 9 | 9 | 7 | 47 | 47 | 5.22 | 0 | 0 | 2 | 0 | 0 |
| Mike Jackson | CB | 2 | 69 | 2 | 1 | 2 | 22 | 11 | 11 | 0 | 0 | 0 | 0 | 0 |
| Chau Smith-Wade | CB | 1 | 25 | 2 | 2 | 2 | 19 | 19 | 9.50 | 0 | 0 | 0 | 0 | 0 |
| Devin Lloyd | LB | 5 | 91.50 | 22 | 4.40 | 20 | 169 | 33.80 | 7.68 | 0 | 0 | 0 | 2 | 0 |
| Bobby Okereke | LB | 7 | 89 | 22 | 3.10 | 17 | 109 | 15.60 | 4.95 | 0 | 0 | 4 | 1 | 0 |
| Nick Scott | S | 5 | 81.80 | 14 | 2.80 | 12 | 133 | 26.60 | 9.50 | 0 | 1 | 2 | 0 | 0 |
| Lathan Ransom | S | 4 | 41.70 | 8 | 2 | 6 | 104 | 26 | 13 | 0 | 2 | 2 | 0 | 0 |
| Zakee Wheatley | S | 6 | 63.30 | 12 | 2 | 9 | 101 | 16.80 | 8.42 | 0 | 2 | 2 | 1 | 0 |
| Tre'von Moehrig | S | 5 | 95 | 8 | 1.60 | 8 | 67 | 13.40 | 8.38 | 0 | 0 | 0 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Will Lee III** (CB): WR2:10t/132y, WR1:4t/34y, RB:5t/27y, TE1:2t/21y, WR3+:4t/21y, TE2+:2t/4y | 20+: wk1 R.Odunze(WR2) 47 deep_right; wk8 C.Watson(WR2) 53 deep_middle
- **Akayleb Evans** (CB): WR3+:4t/85y, WR2:5t/38y, WR1:4t/27y, TE1:2t/26y | 20+: wk4 I.TeSlaa(WR3+) 57 deep_left; wk4 S.LaPorta(TE1) 21 short_middle
- **Jaycee Horn** (CB): WR1:3t/46y, TE2+:1t/13y, TE1:1t/0y | 20+: wk3 D.Boston(WR1) 28 deep_right
- **Marco Wilson** (CB): WR1:3t/25y, WR2:4t/17y, RB:2t/5y
- **Mike Jackson** (CB): RB:1t/19y, WR2:1t/3y
- **Chau Smith-Wade** (CB): WR1:1t/11y, TE1:1t/8y
- **Devin Lloyd** (LB): WR1:5t/56y, RB:5t/34y, WR2:5t/30y, TE1:4t/27y, WR3+:2t/14y, TE2+:1t/8y
- **Bobby Okereke** (LB): RB:11t/44y, WR1:4t/37y, WR2:3t/16y, TE1:2t/12y, WR3+:2t/0y
- **Nick Scott** (S): WR3+:3t/56y, TE1:4t/31y, WR1:2t/21y, WR2:4t/21y, RB:1t/4y | 20+: wk1 K.Raymond(WR3+) 28 deep_left
- **Lathan Ransom** (S): WR2:2t/49y, WR3+:3t/25y, WR1:1t/24y, TE1:1t/6y, RB:1t/0y | 20+: wk1 L.Burden(WR1) 24 deep_left; wk4 J.Williams(WR2) 49 deep_right
- **Zakee Wheatley** (S): TE1:5t/47y, WR2:3t/40y, WR1:2t/7y, WR3+:2t/7y | 20+: wk4 S.LaPorta(TE1) 25 short_middle; wk8 C.Watson(WR2) 24 short_left
- **Tre'von Moehrig** (S): RB:4t/27y, WR3+:3t/26y, WR1:1t/14y

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CHI@CAR | Will Lee III | CB | 5 | 4 | 73 | 0 | 1 | 1 | 0 | 0 | K.Raymondx3, L.Burdenx1, R.Odunzex1 |
| 1 | CHI@CAR | Nick Scott | S | 2 | 2 | 40 | 0 | 1 | 0 | 0 | 0 | K.Raymondx2 |
| 1 | CHI@CAR | Devin Lloyd | LB | 6 | 6 | 36 | 0 | 0 | 0 | 0 | 0 | L.Burdenx2, K.Raymondx2, R.Odunzex1, K.Monangaix1 |
| 1 | CHI@CAR | Lathan Ransom | S | 2 | 2 | 31 | 0 | 1 | 0 | 0 | 0 | K.Raymondx1, L.Burdenx1 |
| 1 | CHI@CAR | Jaycee Horn | CB | 2 | 2 | 25 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1, C.Kmetx1 |
| 1 | CHI@CAR | Mike Jackson | CB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | K.Monangaix1 |
| 1 | CHI@CAR | Bobby Okereke | LB | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 0 | D.Swiftx1 |
| 2 | CAR@ATL | Devin Lloyd | LB | 5 | 3 | 39 | 0 | 0 | 0 | 2 | 0 | D.Londonx2, J.Dotsonx2, K.Pittsx1 |
| 2 | CAR@ATL | Bobby Okereke | LB | 5 | 4 | 25 | 0 | 0 | 0 | 1 | 0 | Bi.Robinsonx3, D.Londonx1, Br.Robinsonx1 |
| 2 | CAR@ATL | Will Lee III | CB | 4 | 2 | 14 | 0 | 0 | 2 | 0 | 0 | Bi.Robinsonx1, J.Dotsonx1, Br.Robinsonx1, A.Hooperx1 |
| 2 | CAR@ATL | Jaycee Horn | CB | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | K.Pittsx1, D.Londonx1 |
| 2 | CAR@ATL | Lathan Ransom | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | C.Blairx1 |
| 2 | CAR@ATL | Mike Jackson | CB | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | J.Dotsonx1 |
| 2 | CAR@ATL | Tre'von Moehrig | S | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | O.Zaccheausx1 |
| 2 | CAR@ATL | Zakee Wheatley | S | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | Z.Branchx1 |
| 3 | CAR@CLE | Jaycee Horn | CB | 1 | 1 | 28 | 0 | 1 | 0 | 0 | 0 | D.Bostonx1 |
| 3 | CAR@CLE | Will Lee III | CB | 5 | 4 | 28 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx2, R.Sandersx1, D.Bostonx1, Q.Judkinsx1 |
| 3 | CAR@CLE | Zakee Wheatley | S | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | H.Fanninx2 |
| 3 | CAR@CLE | Bobby Okereke | LB | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | R.Sandersx1 |
| 3 | CAR@CLE | Tre'von Moehrig | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | R.Sandersx1 |
| 3 | CAR@CLE | Lathan Ransom | S | 2 | 1 | 6 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx1, H.Fanninx1 |
| 3 | CAR@CLE | Akayleb Evans | CB | 2 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx1, D.Bostonx1 |
| 4 | DET@CAR | Akayleb Evans | CB | 9 | 8 | 133 | 0 | 2 | 1 | 0 | 0 | J.Williamsx3, A.St. Brownx3, I.TeSlaax2, S.LaPortax1 |
| 4 | DET@CAR | Devin Lloyd | LB | 7 | 7 | 72 | 0 | 0 | 0 | 0 | 0 | S.LaPortax2, S.Vakix1, J.Williamsx1, B.Wrightx1, A.St. Brownx1, J.Gibbsx1 |
| 4 | DET@CAR | Lathan Ransom | S | 3 | 2 | 61 | 0 | 1 | 1 | 0 | 0 | J.Gibbsx1, J.Williamsx1, I.TeSlaax1 |
| 4 | DET@CAR | Bobby Okereke | LB | 6 | 5 | 43 | 0 | 0 | 1 | 0 | 0 | A.St. Brownx2, J.Gibbsx2, I.TeSlaax1, S.LaPortax1 |
| 4 | DET@CAR | Tre'von Moehrig | S | 2 | 2 | 30 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1, I.TeSlaax1 |
| 4 | DET@CAR | Zakee Wheatley | S | 1 | 1 | 25 | 0 | 1 | 0 | 0 | 0 | S.LaPortax1 |
| 4 | DET@CAR | Will Lee III | CB | 2 | 2 | 24 | 0 | 0 | 0 | 0 | 0 | J.Williamsx1, I.TeSlaax1 |
| 4 | DET@CAR | Nick Scott | S | 2 | 2 | 11 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx1, S.LaPortax1 |
| 6 | CAR@PHI | Nick Scott | S | 5 | 4 | 43 | 0 | 0 | 1 | 0 | 0 | D.Goedertx3, D.Smithx1, M.Lemonx1 |
| 6 | CAR@PHI | Will Lee III | CB | 7 | 5 | 36 | 0 | 0 | 2 | 0 | 0 | D.Smithx3, M.Lemonx2, D.Goedertx1, J.Mundtx1 |
| 6 | CAR@PHI | Akayleb Evans | CB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | D.Goedertx1, D.Cooperx1, D.Smithx1 |
| 6 | CAR@PHI | Zakee Wheatley | S | 3 | 2 | 20 | 0 | 0 | 1 | 0 | 0 | D.Smithx2, E.Moorex1 |
| 6 | CAR@PHI | Tre'von Moehrig | S | 2 | 2 | 18 | 0 | 0 | 0 | 0 | 0 | D.Piercex1, D.Wicksx1 |
| 6 | CAR@PHI | Bobby Okereke | LB | 6 | 4 | 17 | 0 | 0 | 2 | 0 | 0 | D.Smithx2, D.Piercex1, C.Steelex1, M.Lemonx1, D.Goedertx1 |
| 6 | CAR@PHI | Devin Lloyd | LB | 2 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | D.Piercex2 |
| 7 | TB@CAR | Akayleb Evans | CB | 1 | 1 | 19 | 0 | 0 | 0 | 0 | 0 | T.Johnsonx1 |
| 7 | TB@CAR | Nick Scott | S | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | C.Godwinx1 |
| 7 | TB@CAR | Bobby Okereke | LB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | T.Hurstx1, C.Godwinx1 |
| 7 | TB@CAR | Zakee Wheatley | S | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | C.Ottonx1 |
| 8 | CAR@GB | Will Lee III | CB | 4 | 4 | 64 | 0 | 1 | 0 | 0 | 0 | C.Watsonx2, J.Jacobsx1, T.Kraftx1 |
| 8 | CAR@GB | Marco Wilson | CB | 9 | 7 | 47 | 0 | 0 | 2 | 0 | 0 | C.Watsonx4, M.Goldenx3, J.Jacobsx2 |
| 8 | CAR@GB | Zakee Wheatley | S | 4 | 3 | 38 | 0 | 1 | 0 | 1 | 0 | M.Goldenx2, C.Watsonx1, T.Kraftx1 |
| 8 | CAR@GB | Nick Scott | S | 4 | 3 | 32 | 0 | 0 | 1 | 0 | 0 | C.Watsonx2, J.Sturdivantx1, M.Goldenx1 |
| 8 | CAR@GB | Chau Smith-Wade | CB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | M.Goldenx1, T.Kraftx1 |
| 8 | CAR@GB | Devin Lloyd | LB | 2 | 2 | 15 | 0 | 0 | 0 | 0 | 0 | T.Kraftx1, C.Watsonx1 |
| 8 | CAR@GB | Tre'von Moehrig | S | 2 | 2 | 9 | 0 | 0 | 0 | 0 | 0 | M.Lloydx1, J.Jacobsx1 |
| 8 | CAR@GB | Bobby Okereke | LB | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | J.Jacobsx1 |

## Who beat them each week

**Wk1 CHI@CAR** (vs CHI offense, 269 rec yds allowed; 23% of targets unattributed)
- Top receivers: K.Raymond (WR3+, short/YAC (aDOT <8)) 8/9 84y; L.Burden (WR1, short/YAC (aDOT <8)) 5/5 63y; R.Odunze (WR2, deep (aDOT 13+)) 2/3 52y; C.Kmet (TE2+, short/YAC (aDOT <8)) 2/3 35y 1TD
- 20+ catches: R.Odunze(WR2) 47y deep_right - W.Lee [tackler]; C.Kmet(TE2+) 22y deep_left TD - no tackler named [unattributed]; K.Raymond(WR3+) 28y deep_left - N.Scott [tackler]; L.Burden(WR1) 24y deep_left - L.Ransom [tackler]
- 15+ runs: D.Swift(RB) 32y rush right tackle; C.Williams(QB) 29y rush left end; K.Mogai(RB) 61y rush middle; D.Swift(RB) 28y rush right guard

**Wk2 CAR@ATL** (vs ATL offense, 145 rec yds allowed; 26% of targets unattributed)
- Top receivers: D.London (WR1, intermediate (aDOT 8-13)) 4/5 51y; A.Hooper (TE2+, short/YAC (aDOT <8)) 2/4 20y; Br.Robinson (RB, short/YAC (aDOT <8)) 2/2 16y; K.Pitts (TE1, short/YAC (aDOT <8)) 1/3 15y

**Wk3 CAR@CLE** (vs CLE offense, 144 rec yds allowed; 39% of targets unattributed)
- Top receivers: H.Fannin (TE1, short/YAC (aDOT <8)) 7/9 51y 2TD; D.Boston (WR1, deep (aDOT 13+)) 2/5 41y; R.Sanders (RB, short/YAC (aDOT <8)) 4/5 34y; K.Concepcion (WR2, short/YAC (aDOT <8)) 2/9 9y
- 20+ catches: D.Boston(WR1) 28y deep_right - Ja.Horn [tackler]
- 15+ runs: R.Sanders(RB) 17y rush right tackle; D.Watson(QB) 21y rush left guard

**Wk4 DET@CAR** (vs DET offense, 412 rec yds allowed; 27% of targets unattributed)
- Top receivers: J.Williams (WR2, deep (aDOT 13+)) 6/8 102y; I.TeSlaa (WR3+, intermediate (aDOT 8-13)) 4/8 95y; A.St. Brown (WR1, intermediate (aDOT 8-13)) 8/11 84y; S.LaPorta (TE1, short/YAC (aDOT <8)) 8/13 84y 1TD
- 20+ catches: J.Williams(WR2) 49y deep_right - L.Ransom [tackler]; I.TeSlaa(WR3+) 57y deep_left - A.Evans [tackler]; S.LaPorta(TE1) 25y short_middle - Z.Wheatley [tackler]; S.LaPorta(TE1) 21y short_middle - A.Evans [tackler]

**Wk6 CAR@PHI** (vs PHI offense, 215 rec yds allowed; 30% of targets unattributed)
- Top receivers: D.Smith (WR2, intermediate (aDOT 8-13)) 7/14 75y 1TD; D.Goedert (TE1, short/YAC (aDOT <8)) 6/8 61y; D.Wicks (WR3+, deep (aDOT 13+)) 2/4 24y; M.Lemon (WR1, short/YAC (aDOT <8)) 3/6 19y

**Wk7 TB@CAR** (vs TB offense, 64 rec yds allowed; 18% of targets unattributed)
- Top receivers: T.Johnson (WR3+, deep (aDOT 13+)) 2/2 33y 1TD; C.Godwin (WR2, short/YAC (aDOT <8)) 4/5 27y; B.Irving (RB, short/YAC (aDOT <8)) 1/2 4y; C.Otton (TE1, short/YAC (aDOT <8)) 0/1 0y
- 15+ runs: B.Irving(RB) 15y rush right tackle; K.Gainwell(RB) 29y rush right tackle; K.Gainwell(RB) 16y rush middle; S.Tucker(RB) 46y rush left guard

**Wk8 CAR@GB** (vs GB offense, 288 rec yds allowed; 21% of targets unattributed)
- Top receivers: C.Watson (WR2, deep (aDOT 13+)) 8/10 113y; M.Golden (WR1, deep (aDOT 13+)) 7/13 79y 1TD; T.Kraft (TE1, short/YAC (aDOT <8)) 6/6 53y 1TD; J.Sturdivant (WR3+, deep (aDOT 13+)) 1/1 16y
- 20+ catches: C.Watson(WR2) 24y short_left - Z.Wheatley [tackler]; C.Watson(WR2) 53y deep_middle - W.Lee [tackler]; M.Golden(WR1) 24y deep_left TD - no tackler named [unattributed]
- 15+ runs: S.Williams(WR) 18y rush right end

