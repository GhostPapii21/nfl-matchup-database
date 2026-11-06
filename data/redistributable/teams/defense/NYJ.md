# NYJ DEFENSE - team database (built 2026-11-03 08:09 ET by Blitz)

Games covered: 8 (wk1 NYJ@TEN, wk2 GB@NYJ, wk3 NYJ@DET, wk4 NYJ@CHI, wk5 CLE@NYJ, wk6 NYJ@NE, wk7 MIA@NYJ, wk8 LV@NYJ). Source: nflverse 2026 pbp (public), weekly rosters, snap counts; Sharp coverage tables (2026-10-29, thru wk7).
**Per-defender numbers are TACKLER/PBU TAG, NOT TRUE COVERAGE.** A completion is charged to the first defensive tackler named; an incompletion to the PBU-named defender; INT to the interceptor; DPI to the flagged player. TDs/out-of-bounds with no tackler stay unattributed. 'tags' = plays charged (stand-in for targets). Free public data never names the coverage defender (PFF/FTN premium only).

## Scheme (Sharp Football Analysis, thru wk7, dateModified 2026-10-29)

Man 23.8% / Zone 66.6% | MOF closed 45.2% / MOF open 50.0% | Blitz 40.0% | Light box 43.4% / Heavy box 24.1% | Sub package 67.0% | Sharp YPT allowed WR 7.6, TE 7.3, RB 4.4, Outside 8.0, Slot 8.1

## Which receiver types beat them (season, vs league YPT; flagged at +1.5 YPT on 12+ targets)

- depth deep_20+: 14.42 YPT on 19 tgts (league 12.32, +2.1), 9 catches of 20+
- depth/direction deep_right: 14.57 YPT on 14 tgts (league 11.85, +2.72), 6 catches of 20+

Holds (-1.5 YPT or better): none

## Pass allowed by receiver type (WR1/WR2/WR3+ = offense's season target rank at the position)

| rtype | tgt | rec | yds | td | exp20 | ypt | tgt_pg | yds_pg | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|---|---|
| RB | 38 | 27 | 215 | 2 | 1 | 5.66 | 4.80 | 26.90 | 5.61 | 0.05 |
| TE1 | 45 | 32 | 374 | 3 | 4 | 8.31 | 5.60 | 46.80 | 7.39 | 0.92 |
| TE2+ | 17 | 13 | 107 | 0 | 0 | 6.29 | 2.10 | 13.40 | 6.71 | -0.42 |
| WR1 | 45 | 29 | 337 | 3 | 4 | 7.49 | 5.60 | 42.10 | 8.16 | -0.67 |
| WR2 | 38 | 28 | 332 | 3 | 6 | 8.74 | 4.80 | 41.50 | 8.20 | 0.54 |
| WR3+ | 44 | 22 | 302 | 3 | 5 | 6.86 | 5.50 | 37.80 | 7.67 | -0.81 |

## Last 4 games, by receiver type

| rtype | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| RB | 15 | 9 | 80 | 0 | 1 | 5.33 | 5.61 | -0.28 |
| TE1 | 24 | 17 | 230 | 3 | 3 | 9.58 | 7.39 | 2.19 |
| TE2+ | 10 | 6 | 64 | 0 | 0 | 6.40 | 6.71 | -0.31 |
| WR1 | 19 | 13 | 159 | 2 | 2 | 8.37 | 8.16 | 0.21 |
| WR2 | 10 | 9 | 110 | 2 | 1 | 11 | 8.20 | 2.80 |
| WR3+ | 30 | 12 | 202 | 2 | 4 | 6.73 | 7.67 | -0.94 |

## By air depth

| airb | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| behind_los | 51 | 39 | 240 | 3 | 1 | 4.71 | 4.58 | 0.13 |
| short_1-9 | 109 | 78 | 731 | 7 | 3 | 6.71 | 6.23 | 0.48 |
| inter_10-19 | 48 | 25 | 422 | 2 | 7 | 8.79 | 10.17 | -1.38 |
| deep_20+ | 19 | 9 | 274 | 2 | 9 | 14.42 | 12.32 | 2.10 |

## By depth x direction (nflverse pass_length/pass_location)

| dd | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep_left | 12 | 5 | 118 | 1 | 4 | 9.83 | 11.28 | -1.45 |
| deep_middle | 10 | 5 | 153 | 0 | 5 | 15.30 | 14.90 | 0.40 |
| deep_right | 14 | 7 | 204 | 1 | 6 | 14.57 | 11.85 | 2.72 |
| short_left | 69 | 46 | 429 | 2 | 2 | 6.22 | 6.08 | 0.14 |
| short_middle | 46 | 33 | 308 | 2 | 2 | 6.70 | 7.43 | -0.73 |
| short_right | 76 | 55 | 455 | 8 | 1 | 5.99 | 5.95 | 0.04 |

## By receiver archetype (receiver's season aDOT)

| arch | tgt | rec | yds | td | exp20 | ypt | lg_ypt | ypt_vs_lg |
|---|---|---|---|---|---|---|---|---|
| deep (aDOT 13+) | 62 | 32 | 468 | 3 | 10 | 7.55 | 8.94 | -1.39 |
| intermediate (aDOT 8-13) | 56 | 39 | 473 | 8 | 5 | 8.45 | 7.96 | 0.49 |
| short/YAC (aDOT <8) | 109 | 80 | 726 | 3 | 5 | 6.66 | 6.47 | 0.19 |

## Explosives allowed (rec 20+ / rush 15+), season

- Pass 20+ by position: {'RB': 1, 'TE': 4, 'WR': 15} (20 total, 2.5/g)
- Pass 20+ by depth/direction: {'deep_left': 4, 'deep_middle': 5, 'deep_right': 6, 'short_left': 2, 'short_middle': 2, 'short_right': 1}
- Rush 15+ by position: {'QB': 2, 'RB': 5} (7 total)

## Rush allowed by ball-carrier position

| rpos | car | yds | exp15 | ypc | yds_pg |
|---|---|---|---|---|---|
| P | 1 | 0 | 0 | 0 | 0 |
| QB | 25 | 142 | 2 | 5.68 | 17.80 |
| RB | 211 | 838 | 5 | 3.97 | 104.80 |
| WR | 3 | 19 | 0 | 6.33 | 2.40 |

## Defenders - CB / S / coverage LBs (LB/OLB shown with 6+ tags) - tackler/PBU tag, not true coverage

| name | pos | games | def snap% | tags | tags_pg | rec | yds | yds_pg | ypt | td | exp20 | pbu | ints | dpi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Azareye'h Thomas | CB | 8 | 100 | 27 | 3.40 | 22 | 185 | 23.10 | 6.85 | 0 | 0 | 5 | 0 | 0 |
| Brandon Stephens | CB | 7 | 97.60 | 18 | 2.60 | 13 | 164 | 23.40 | 9.11 | 0 | 3 | 5 | 0 | 0 |
| Jarvis Brownlee Jr. | CB | 4 | 60.30 | 9 | 2.20 | 9 | 82 | 20.50 | 9.11 | 0 | 2 | 0 | 0 | 0 |
| D'Angelo Ponds | CB | 1 | 14.80 | 1 | 1 | 1 | 5 | 5 | 5 | 0 | 0 | 0 | 0 | 0 |
| Demario Davis | LB | 7 | 99.80 | 21 | 3 | 17 | 164 | 23.40 | 7.81 | 0 | 1 | 4 | 0 | 0 |
| Jamien Sherwood | LB | 8 | 96.20 | 21 | 2.60 | 16 | 158 | 19.80 | 7.52 | 0 | 2 | 5 | 0 | 0 |
| Dane Belton | S | 8 | 100 | 29 | 3.60 | 25 | 309 | 38.60 | 10.66 | 0 | 5 | 4 | 0 | 0 |
| Minkah Fitzpatrick | S | 4 | 85.30 | 14 | 3.50 | 11 | 150 | 37.50 | 10.71 | 0 | 2 | 2 | 1 | 0 |
| Andre Cisco | S | 3 | 45.90 | 11 | 3.70 | 10 | 130 | 43.30 | 11.82 | 0 | 1 | 1 | 0 | 0 |

### Receiver types charged to each defender / explosives charged

- **Azareye'h Thomas** (CB): WR1:8t/54y, WR2:7t/49y, TE1:5t/45y, WR3+:3t/19y, RB:3t/10y, TE2+:1t/8y
- **Brandon Stephens** (CB): WR2:4t/53y, WR1:5t/47y, TE1:2t/41y, WR3+:6t/23y, RB:1t/0y | 20+: wk4 L.Burden(WR1) 22 deep_right; wk4 R.Odunze(WR2) 20 deep_left; wk7 G.Dulcich(TE1) 32 deep_left
- **Jarvis Brownlee Jr.** (CB): WR3+:4t/60y, RB:2t/17y, TE1:2t/5y, WR1:1t/0y | 20+: wk5 I.Bond(WR3+) 24 deep_right; wk5 I.Bond(WR3+) 30 deep_right
- **D'Angelo Ponds** (CB): WR1:1t/5y
- **Demario Davis** (LB): TE1:2t/40y, WR3+:5t/36y, RB:5t/31y, WR1:3t/23y, TE2+:3t/17y, WR2:3t/17y | 20+: wk3 S.LaPorta(TE1) 28 deep_right
- **Jamien Sherwood** (LB): RB:10t/90y, WR1:3t/38y, TE2+:3t/14y, TE1:3t/11y, WR2:2t/5y | 20+: wk6 D.Douglas(WR1) 39 deep_right; wk8 A.Jeanty(RB) 45 short_left
- **Dane Belton** (S): TE1:12t/135y, WR2:5t/54y, TE2+:6t/51y, WR1:3t/40y, WR3+:3t/29y | 20+: wk2 C.Watson(WR2) 20 deep_middle; wk4 R.Odunze(WR2) 21 short_middle; wk5 I.Bond(WR3+) 20 short_right; wk8 B.Bowers(TE1) 23 short_middle; wk8 B.Bowers(TE1) 27 deep_middle
- **Minkah Fitzpatrick** (S): WR2:4t/62y, TE1:7t/61y, WR1:1t/20y, TE2+:1t/7y, WR3+:1t/0y | 20+: wk4 L.Burden(WR1) 20 deep_middle; wk4 R.Odunze(WR2) 37 deep_middle
- **Andre Cisco** (S): WR3+:2t/54y, WR1:2t/28y, RB:2t/21y, TE1:2t/15y, WR2:2t/10y, TE2+:1t/2y | 20+: wk3 I.TeSlaa(WR3+) 49 deep_middle

### Per game (tackler/PBU tag, not true coverage)

| week | game | name | pos | tags | rec | yds | td | exp20 | pbu | ints | dpi | receivers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NYJ@TEN | Andre Cisco | S | 5 | 5 | 47 | 0 | 0 | 0 | 0 | 0 | G.Helmx2, W.Robinsonx1, C.Tatex1, T.Spearsx1 |
| 1 | NYJ@TEN | Azareye'h Thomas | CB | 5 | 5 | 27 | 0 | 0 | 0 | 0 | 0 | C.Tatex2, T.Pollardx1, G.Helmx1, T.Spearsx1 |
| 1 | NYJ@TEN | Demario Davis | LB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | W.Robinsonx2, T.Spearsx1 |
| 1 | NYJ@TEN | Jamien Sherwood | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | D.Bellingerx1, W.Robinsonx1 |
| 1 | NYJ@TEN | Jarvis Brownlee Jr. | CB | 2 | 2 | 8 | 0 | 0 | 0 | 0 | 0 | C.Dikex1, G.Helmx1 |
| 1 | NYJ@TEN | Dane Belton | S | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | W.Robinsonx1 |
| 2 | GB@NYJ | Dane Belton | S | 4 | 4 | 53 | 0 | 1 | 0 | 0 | 0 | C.Watsonx2, T.Kraftx1, M.Goldenx1 |
| 2 | GB@NYJ | Brandon Stephens | CB | 3 | 3 | 20 | 0 | 0 | 0 | 0 | 0 | M.Lloydx1, C.Watsonx1, S.Moorex1 |
| 2 | GB@NYJ | Azareye'h Thomas | CB | 3 | 2 | 17 | 0 | 0 | 1 | 0 | 0 | S.Moorex1, C.Watsonx1, M.Goldenx1 |
| 2 | GB@NYJ | Jarvis Brownlee Jr. | CB | 1 | 1 | 15 | 0 | 0 | 0 | 0 | 0 | C.Brooksx1 |
| 2 | GB@NYJ | Andre Cisco | S | 2 | 1 | 14 | 0 | 0 | 1 | 0 | 0 | C.Watsonx1, M.Goldenx1 |
| 2 | GB@NYJ | Demario Davis | LB | 2 | 2 | 12 | 0 | 0 | 0 | 0 | 0 | J.Reedx1, M.Goldenx1 |
| 2 | GB@NYJ | Jamien Sherwood | LB | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | C.Watsonx1, T.Kraftx1 |
| 3 | NYJ@DET | Andre Cisco | S | 4 | 4 | 69 | 0 | 1 | 0 | 0 | 0 | I.TeSlaax2, J.Gibbsx1, B.Wrightx1 |
| 3 | NYJ@DET | Demario Davis | LB | 4 | 4 | 57 | 0 | 1 | 0 | 0 | 0 | B.Wrightx1, J.Gibbsx1, I.TeSlaax1, S.LaPortax1 |
| 3 | NYJ@DET | Azareye'h Thomas | CB | 4 | 4 | 29 | 0 | 0 | 0 | 0 | 0 | J.Williamsx2, S.LaPortax1, J.Gibbsx1 |
| 3 | NYJ@DET | Jamien Sherwood | LB | 4 | 4 | 26 | 0 | 0 | 0 | 0 | 0 | J.Gibbsx2, A.St. Brownx1, S.Vakix1 |
| 3 | NYJ@DET | Brandon Stephens | CB | 1 | 1 | 16 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1 |
| 3 | NYJ@DET | Dane Belton | S | 3 | 2 | 16 | 0 | 0 | 1 | 0 | 0 | S.LaPortax2, J.Meeksx1 |
| 3 | NYJ@DET | Jarvis Brownlee Jr. | CB | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | A.St. Brownx1 |
| 4 | NYJ@CHI | Minkah Fitzpatrick | S | 5 | 4 | 87 | 0 | 2 | 0 | 1 | 0 | C.Lovelandx3, L.Burdenx1, R.Odunzex1 |
| 4 | NYJ@CHI | Brandon Stephens | CB | 3 | 2 | 42 | 0 | 2 | 1 | 0 | 0 | L.Burdenx2, R.Odunzex1 |
| 4 | NYJ@CHI | Azareye'h Thomas | CB | 5 | 4 | 36 | 0 | 0 | 1 | 0 | 0 | R.Odunzex2, L.Burdenx2, S.Roushx1 |
| 4 | NYJ@CHI | Demario Davis | LB | 5 | 5 | 34 | 0 | 0 | 0 | 0 | 0 | L.Burdenx1, C.Lovelandx1, D.Swiftx1, K.Raymondx1, C.Kmetx1 |
| 4 | NYJ@CHI | Dane Belton | S | 6 | 5 | 33 | 0 | 1 | 1 | 0 | 0 | C.Lovelandx3, R.Odunzex2, K.Raymondx1 |
| 4 | NYJ@CHI | Jamien Sherwood | LB | 4 | 3 | 17 | 0 | 0 | 1 | 0 | 0 | C.Lovelandx2, C.Kmetx1, K.Monangaix1 |
| 5 | CLE@NYJ | Jarvis Brownlee Jr. | CB | 5 | 5 | 59 | 0 | 2 | 0 | 0 | 0 | I.Bondx2, Q.Judkinsx1, J.Jeudyx1, H.Fanninx1 |
| 5 | CLE@NYJ | Dane Belton | S | 2 | 2 | 28 | 0 | 1 | 0 | 0 | 0 | I.Bondx1, J.Jeudyx1 |
| 5 | CLE@NYJ | Brandon Stephens | CB | 3 | 2 | 21 | 0 | 0 | 1 | 0 | 0 | D.Bostonx2, J.Jeudyx1 |
| 5 | CLE@NYJ | Minkah Fitzpatrick | S | 2 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | K.Concepcionx1, J.Jeudyx1 |
| 5 | CLE@NYJ | Jamien Sherwood | LB | 2 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | Q.Judkinsx1, D.Bostonx1 |
| 5 | CLE@NYJ | Azareye'h Thomas | CB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | D.Bostonx2 |
| 6 | NYJ@NE | Jamien Sherwood | LB | 2 | 2 | 48 | 0 | 1 | 0 | 0 | 0 | T.Hendersonx1, D.Douglasx1 |
| 6 | NYJ@NE | Azareye'h Thomas | CB | 4 | 4 | 45 | 0 | 0 | 0 | 0 | 0 | H.Henryx2, A.Brownx1, K.Williamsx1 |
| 6 | NYJ@NE | Dane Belton | S | 4 | 3 | 37 | 0 | 0 | 1 | 0 | 0 | E.Raridonx2, D.Douglasx1, H.Henryx1 |
| 6 | NYJ@NE | Demario Davis | LB | 3 | 2 | 23 | 0 | 0 | 1 | 0 | 0 | A.Brownx2, D.Douglasx1 |
| 6 | NYJ@NE | Brandon Stephens | CB | 2 | 1 | 4 | 0 | 0 | 1 | 0 | 0 | A.Brownx2 |
| 7 | MIA@NYJ | Brandon Stephens | CB | 4 | 2 | 40 | 0 | 1 | 2 | 0 | 0 | G.Dulcichx1, K.Colemanx1, C.Bellx1, C.Douglasx1 |
| 7 | MIA@NYJ | Dane Belton | S | 3 | 3 | 40 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx2, M.Washingtonx1 |
| 7 | MIA@NYJ | Minkah Fitzpatrick | S | 3 | 3 | 34 | 0 | 0 | 0 | 0 | 0 | G.Dulcichx2, C.Bellx1 |
| 7 | MIA@NYJ | Azareye'h Thomas | CB | 2 | 2 | 19 | 0 | 0 | 0 | 0 | 0 | M.Washingtonx1, C.Bellx1 |
| 7 | MIA@NYJ | D'Angelo Ponds | CB | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | M.Washingtonx1 |
| 7 | MIA@NYJ | Demario Davis | LB | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | C.Bellx1, O.Gordonx1 |
| 7 | MIA@NYJ | Jamien Sherwood | LB | 3 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | O.Gordonx2, S.Traorex1 |
| 8 | LV@NYJ | Dane Belton | S | 6 | 5 | 96 | 0 | 2 | 1 | 0 | 0 | B.Bowersx3, M.Mayerx3 |
| 8 | LV@NYJ | Jamien Sherwood | LB | 2 | 2 | 49 | 0 | 1 | 0 | 0 | 0 | A.Jeantyx2 |
| 8 | LV@NYJ | Minkah Fitzpatrick | S | 4 | 3 | 24 | 0 | 0 | 1 | 0 | 0 | B.Bowersx2, J.Nailorx1, M.Mayerx1 |
| 8 | LV@NYJ | Demario Davis | LB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | A.Jeantyx1, M.Mayerx1 |
| 8 | LV@NYJ | Brandon Stephens | CB | 2 | 2 | 21 | 0 | 0 | 0 | 0 | 0 | J.Nailorx1, B.Bowersx1 |
| 8 | LV@NYJ | Azareye'h Thomas | CB | 2 | 1 | 12 | 0 | 0 | 1 | 0 | 0 | J.Nailorx1, B.Bowersx1 |

## Who beat them each week

**Wk1 NYJ@TEN** (vs TEN offense, 140 rec yds allowed; 36% of targets unattributed)
- Top receivers: C.Tate (WR1, intermediate (aDOT 8-13)) 4/6 38y; W.Robinson (WR2, short/YAC (aDOT <8)) 5/6 38y; G.Helm (TE1, short/YAC (aDOT <8)) 4/5 28y; T.Spears (RB, short/YAC (aDOT <8)) 2/4 12y

**Wk2 GB@NYJ** (vs GB offense, 145 rec yds allowed; 41% of targets unattributed)
- Top receivers: M.Golden (WR1, deep (aDOT 13+)) 4/6 58y; C.Watson (WR2, deep (aDOT 13+)) 4/11 41y 1TD; T.Kraft (TE1, short/YAC (aDOT <8)) 2/3 15y; C.Brooks (RB, short/YAC (aDOT <8)) 1/2 15y
- 20+ catches: C.Watson(WR2) 20y deep_middle - D.Belton [tackler]

**Wk3 NYJ@DET** (vs DET offense, 269 rec yds allowed; 28% of targets unattributed)
- Top receivers: I.TeSlaa (WR3+, intermediate (aDOT 8-13)) 3/3 66y; J.Gibbs (RB, short/YAC (aDOT <8)) 7/8 65y 1TD; J.Williams (WR2, deep (aDOT 13+)) 4/4 49y; S.LaPorta (TE1, short/YAC (aDOT <8)) 3/4 44y
- 20+ catches: S.LaPorta(TE1) 28y deep_right - D.Davis [tackler]; J.Williams(WR2) 21y deep_left - no tackler named [unattributed]; I.TeSlaa(WR3+) 49y deep_middle - A.Cisco [tackler]
- 15+ runs: J.Gibbs(RB) 17y rush right end

**Wk4 NYJ@CHI** (vs CHI offense, 268 rec yds allowed; 3% of targets unattributed)
- Top receivers: R.Odunze (WR2, deep (aDOT 13+)) 6/7 94y; L.Burden (WR1, short/YAC (aDOT <8)) 4/6 63y; C.Loveland (TE1, short/YAC (aDOT <8)) 6/9 57y; D.Swift (RB, short/YAC (aDOT <8)) 2/2 16y
- 20+ catches: R.Odunze(WR2) 21y short_middle - D.Belton [tackler]; L.Burden(WR1) 20y deep_middle - M.Fitzpatrick [tackler]; L.Burden(WR1) 22y deep_right - B.Stephens [tackler]; R.Odunze(WR2) 37y deep_middle - M.Fitzpatrick [tackler]; R.Odunze(WR2) 20y deep_left - B.Stephens [tackler]
- 15+ runs: K.Mogai(RB) 19y rush right end; K.Mogai(RB) 26y rush right guard

**Wk5 CLE@NYJ** (vs CLE offense, 155 rec yds allowed; 38% of targets unattributed)
- Top receivers: I.Bond (WR3+, deep (aDOT 13+)) 3/7 74y; D.Boston (WR1, deep (aDOT 13+)) 3/7 46y 1TD; J.Jeudy (WR3+, intermediate (aDOT 8-13)) 3/7 19y; Q.Judkins (RB, short/YAC (aDOT <8)) 3/4 6y
- 20+ catches: I.Bond(WR3+) 20y short_right - D.Belton [tackler]; I.Bond(WR3+) 24y deep_right - J.Brownlee [tackler]; I.Bond(WR3+) 30y deep_right - J.Brownlee [tackler]; D.Boston(WR1) 29y deep_left TD - no tackler named [unattributed]
- 15+ runs: D.Watson(QB) 20y rush middle

**Wk6 NYJ@NE** (vs NE offense, 235 rec yds allowed; 47% of targets unattributed)
- Top receivers: D.Douglas (WR1, intermediate (aDOT 8-13)) 7/8 86y 1TD; H.Henry (TE1, short/YAC (aDOT <8)) 4/5 48y 1TD; R.Doubs (WR2, deep (aDOT 13+)) 1/1 42y 1TD; A.Brown (WR3+, deep (aDOT 13+)) 3/10 27y
- 20+ catches: R.Doubs(WR2) 42y deep_right TD - no tackler named [unattributed]; D.Douglas(WR1) 39y deep_right - J.Sherwood [tackler]
- 15+ runs: D.Maye(QB) 21y rush right guard

**Wk7 MIA@NYJ** (vs MIA offense, 208 rec yds allowed; 14% of targets unattributed)
- Top receivers: G.Dulcich (TE1, short/YAC (aDOT <8)) 5/5 86y; C.Douglas (WR3+, intermediate (aDOT 8-13)) 2/3 70y 2TD; M.Washington (WR1, intermediate (aDOT 8-13)) 3/3 27y; C.Bell (WR2, deep (aDOT 13+)) 3/4 25y
- 20+ catches: G.Dulcich(TE1) 32y deep_left - B.Stephens [tackler]; C.Douglas(WR3+) 63y short_left TD - no tackler named [unattributed]
- 15+ runs: O.Gordon(RB) 25y rush left end

**Wk8 LV@NYJ** (vs LV offense, 247 rec yds allowed; 24% of targets unattributed)
- Top receivers: B.Bowers (TE1, intermediate (aDOT 8-13)) 7/10 92y 2TD; A.Jeanty (RB, short/YAC (aDOT <8)) 3/4 64y; M.Mayer (TE2+, short/YAC (aDOT <8)) 5/6 53y; J.Nailor (WR2, intermediate (aDOT 8-13)) 4/4 38y 1TD
- 20+ catches: B.Bowers(TE1) 23y short_middle - D.Belton [tackler]; B.Bowers(TE1) 27y deep_middle - D.Belton [tackler]; A.Jeanty(RB) 45y short_left - J.Sherwood [tackler]
- 15+ runs: M.Washington(RB) 15y rush left end

## Seed notes from defenders/NYJ_secondary.md (wk8 ESPN-text dissection; 'inferred' = pregame matchup, not charted)

- Q1 8:59 Brock Bowers (TE) rec 23 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 15:00 Brock Bowers (TE) rec 27 — defender unknown [unknown; no public source]; alignment: TE: inline/slot not charted (no public alignment)
- Q3 13:39 Mike Washington Jr. (RB) rush 15 — J.Sherwood [tackler-of-record; ESPN play text (single-source; not fit assignment)]; alignment: backfield (position default)
- Q4 15:00 Ashton Jeanty (RB) rec 45 — defender unknown [unknown; no public source]; alignment: backfield (position default)
- Brandon Stephens ← Jalen Nailor: 4 tgt, 4 rec, 38 yds
- Azareye'h Thomas ← Tre Tucker: 1 tgt, 0 rec, 0 yds

## Seed: playlogs/archetype_vs_defense_2026.csv rows

- wk8 LV@NYJ: Brock Bowers (TE-move/seam) 7/10tgt 92y 2TD | shell 24/67, MOFO 50 | TE-primary vs NYJ zone (67%), 2 TD; DPI declined on J.Brownlee on TD — NYJ LB/S seam coverage weak. TE YPT allowed 7.3. [inferred]
- wk8 LV@NYJ: Kirk Cousins (QB-pocket) 19/26 247y 3TD 0INT; 5-3 1TD | shell 24/67, MOFO 50 | Efficient vs NYJ zone; 3 TD went to TE/slot (Bowers, Nailor). [inferred;unknown]
- wk8 LV@NYJ: Mike Washington Jr. (RB-committee/change-of-pace) 25-83 0TD | shell 24/67, MOFO 50 | Script/volume; no specific matchup attribution — see explosives table. [confirmed-tackler]
- wk8 LV@NYJ: Ashton Jeanty (RB-power/volume early-down) 2-9 0TD; 3/4tgt 64y 0TD | shell 24/67, MOFO 50 | Receiving role (3/4, 64y incl. 23/27y vs Ponds-area, inferred) though only 2 carries. [unknown]
- wk8 LV@NYJ: Jalen Nailor (WR-deep speed) 4/4tgt 38y 1TD | shell 24/67, MOFO 50 | Red-zone TD vs NYJ zone. [none (no explosive)]

