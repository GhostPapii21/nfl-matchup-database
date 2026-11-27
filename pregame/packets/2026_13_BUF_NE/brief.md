# BUF at NE: Week 13, Sunday late window

**Sunday 2026-12-06, 16:25 ET.** Site: Home; roof: outdoors; surface: fieldturf. Rest: BUF 10 days, NE 7 days. Listed QBs: Josh Allen (BUF), Drake Maye (NE).

Market (schedule consensus, not a timestamped quote): NE +12.5, total 44.5.

Generated 2026-11-27T18:39:19+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-27T18:32:28Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | NE +13.5 | -115 | -105 | 51.1% | 48.9% | 4.7% | 2026-11-27T18:32:28+00:00 |
| total | fanduel | Over 44.5 | -105 | -115 | 48.9% | 51.1% | 4.7% | 2026-11-27T18:32:28+00:00 |
| moneyline | fanduel | NE | +590 | -850 | 13.9% | 86.1% | 4.0% | 2026-11-27T18:32:28+00:00 |

Player props: OK.

## Matchup edges

### BUF offense vs NE defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| NE DEFENCE WEAK SPOT | wide receiver yards | 132.9 | 186.4 | 147.7 | BUF offence ranks 22 of 32, NE defence ranks 30 of 32 (1 = best at its own job) |
| BUF OFFENCE STRENGTH | running back receiving yards | 47.8 | 36.6 | 33.5 | BUF offence ranks 5 of 32, NE defence ranks 19 of 32 (1 = best at its own job) |
| BUF OFFENCE STRENGTH | running back rushing yards | 112.8 | 97.2 | 93.5 | BUF offence ranks 5 of 32, NE defence ranks 17 of 32 (1 = best at its own job) |
| BUF OFFENCE ADVANTAGE | explosive passes (20+) | 3.5 | 4.0 | 3.0 | BUF offence ranks 9 of 32, NE defence ranks 31 of 32 (1 = best at its own job) |
| BUF OFFENCE STRENGTH | explosive runs (15+) | 1.6 | 1.0 | 1.2 | BUF offence ranks 5 of 32, NE defence ranks 11 of 32 (1 = best at its own job) |
| NE DEFENCE WEAK SPOT | passing yards | 231.5 | 272.4 | 235.6 | BUF offence ranks 18 of 32, NE defence ranks 31 of 32 (1 = best at its own job) |
| BUF OFFENCE ADVANTAGE | points | 28.1 | 28.2 | 23.3 | BUF offence ranks 6 of 32, NE defence ranks 28 of 32 (1 = best at its own job) |
| BUF OFFENCE ADVANTAGE | third-down conversions | 42.2% | 45.5% | 39.2% | BUF offence ranks 9 of 32, NE defence ranks 26 of 32 (1 = best at its own job) |
| NE DEFENCE WEAK SPOT | red-zone touchdowns | 58.1% | 65.5% | 58.5% | BUF offence ranks 16 of 32, NE defence ranks 23 of 32 (1 = best at its own job) |

### NE offense vs BUF defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| BUF DEFENCE STRENGTH | wide receiver yards | 162.5 | 115.5 | 147.7 | NE offence ranks 9 of 32, BUF defence ranks 4 of 32 (1 = best at its own job) |
| NE OFFENCE ADVANTAGE | tight end yards | 64.5 | 67.5 | 54.3 | NE offence ranks 9 of 32, BUF defence ranks 28 of 32 (1 = best at its own job) |
| NE OFFENCE STRENGTH | explosive passes (20+) | 3.9 | 2.8 | 3.0 | NE offence ranks 3 of 32, BUF defence ranks 8 of 32 (1 = best at its own job) |
| BUF DEFENCE STRENGTH | explosive runs (15+) | 1.1 | 0.6 | 1.2 | NE offence ranks 22 of 32, BUF defence ranks 2 of 32 (1 = best at its own job) |
| BUF DEFENCE STRENGTH | points | 23.9 | 17.5 | 23.3 | NE offence ranks 13 of 32, BUF defence ranks 5 of 32 (1 = best at its own job) |
| BUF DEFENCE STRENGTH | third-down conversions | 42.9% | 30.2% | 39.2% | NE offence ranks 8 of 32, BUF defence ranks 3 of 32 (1 = best at its own job) |
| BUF DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 6.4% | 4.7% | 6.7% | NE offence ranks 17 of 32, BUF defence ranks 28 of 32 (1 = best at its own job) |
| BUF DEFENCE STRENGTH | pressure (sacks + hits) | 14.2% | 19.8% | 15.7% | NE offence ranks 11 of 32, BUF defence ranks 4 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | BUF 24.8 - NE 23.6 | 48.5 | -1.2 | 46.6% | 80.3% | 56.3% | BUF 12.0 - NE 13.2 |
| independent | BUF 28.7 - NE 26.3 | 55.0 | -2.5 | 42.5% | 77.7% | 77.6% | BUF 13.4 - NE 14.8 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### BUF offense vs NE defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K.Shakir | WR | receiving yards | 8 | 65.8 | 1.131 | 32.2 | 34.9 | 37.4 | 37.8 | 38.2 | 69.0 |
| K.Shakir | WR | receptions | 8 | 4.2 | 1.056 | 2.5 | 2.9 | 3.2 | 3.2 | 3.2 | 4.2 |
| D.Moore | WR | receiving yards | 6 | 60.6 | 1.131 | 13.6 | 14.7 | 15.8 | 17.0 | 19.8 | 60.5 |
| D.Moore | WR | receptions | 6 | 4.1 | 1.056 | 1.3 | 1.6 | 1.8 | 2.1 | 2.4 | 3.7 |
| K.Coleman | WR | receiving yards | 8 | 26.6 | 1.131 | 1.6 | 3.2 | 4.7 | 5.9 | 7.1 | 15.8 |
| K.Coleman | WR | receptions | 8 | 2.1 | 1.056 | 0.4 | 0.7 | 1.1 | 1.1 | 1.1 | 1.6 |
| D.Kincaid | TE | receiving yards | 7 | 34.0 | 0.955 | 6.7 | 6.7 | 6.7 | 7.8 | 9.5 | 26.7 |
| D.Kincaid | TE | receptions | 7 | 2.8 | 0.97 | 1.0 | 1.0 | 1.0 | 1.2 | 1.5 | 1.9 |
| T.Johnson | RB | receiving yards | 8 | 29.5 | 1.046 | 6.0 | 7.8 | 9.6 | 10.7 | 11.8 | 22.5 |
| T.Johnson | RB | receptions | 8 | 2.8 | 0.962 | 1.3 | 1.6 | 1.9 | 1.9 | 1.9 | 1.9 |
| D.Knox | TE | receiving yards | 8 | 12.4 | 0.955 | 0.0 | 0.0 | 0.3 | 2.3 | 4.3 | 6.2 |
| D.Knox | TE | receptions | 8 | 1.4 | 0.97 | 0.3 | 0.7 | 1.0 | 1.0 | 1.0 | 1.0 |
| J.Cook | RB | rushing yards | 8 | 108.3 | 1.02 | 78.3 | 80.1 | 82.0 | 85.3 | 88.5 | 103.0 |
| J.Allen | QB | passing yards | 8 | 239.3 | 1.078 | 130.7 | 174.1 | 212.0 | 217.3 | 222.6 | 262.5 |

### NE offense vs BUF defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D.Douglas | WR | receiving yards | 8 | 46.4 | 0.891 | 7.0 | 10.4 | 13.7 | 16.2 | 18.7 | 45.9 |
| D.Douglas | WR | receptions | 8 | 3.0 | 0.918 | 0.9 | 0.9 | 1.0 | 1.3 | 1.6 | 2.8 |
| H.Henry | TE | receiving yards | 8 | 44.2 | 1.122 | 12.3 | 19.0 | 25.1 | 28.3 | 31.4 | 44.3 |
| H.Henry | TE | receptions | 8 | 3.7 | 1.052 | 1.4 | 1.8 | 2.2 | 2.5 | 2.9 | 3.2 |
| M.Hollins | WR | receiving yards | 4 | 46.6 | 0.891 | 33.7 | 35.3 | 36.9 | 38.5 | 40.1 | 45.0 |
| M.Hollins | WR | receptions | 4 | 3.8 | 0.918 | 2.8 | 2.8 | 2.8 | 2.8 | 2.8 | 3.7 |
| E.Chism | WR | receiving yards | 8 | 22.4 | 0.891 | 0.0 | 0.0 | 0.0 | 0.4 | 0.7 | 23.6 |
| E.Chism | WR | receptions | 8 | 2.2 | 0.918 | 0.0 | 0.0 | 0.0 | 0.4 | 0.7 | 1.4 |
| E.Raridon | TE | receiving yards | 7 | 31.3 | 1.122 | 5.9 | 6.3 | 6.6 | 7.9 | 9.5 | 13.5 |
| E.Raridon | TE | receptions | 7 | 2.2 | 1.052 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 |
| R.Stevenson | RB | receiving yards | 7 | 31.3 | 1.044 | 3.2 | 5.4 | 7.6 | 10.0 | 12.5 | 21.9 |
| R.Stevenson | RB | receptions | 7 | 3.1 | 1.059 | 1.7 | 2.3 | 3.0 | 3.2 | 3.2 | 3.2 |
| R.Stevenson | RB | rushing yards | 8 | 33.4 | 0.888 | 9.1 | 14.7 | 19.5 | 19.5 | 19.5 | 30.2 |
| C.Kiner | RB | rushing yards | 7 | 32.8 | 0.888 | 12.9 | 14.2 | 15.5 | 17.2 | 19.1 | 33.7 |
| T.Henderson | RB | rushing yards | 5 | 21.4 | 0.888 | 10.3 | 12.6 | 14.9 | 17.2 | 19.5 | 20.4 |
| D.Maye | QB | passing yards | 8 | 226.9 | 0.966 | 97.4 | 148.4 | 192.2 | 192.2 | 192.2 | 243.4 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## BUF (last 8 games: weeks 4, 5, 6, 8, 9, 10, 11, 12)

### BUF defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 17.5 | 5/32 | 23.3 |
| Pass yards allowed / game | 219.5 | 8/32 | 235.6 |
| Yards per pass attempt allowed | 6.01 | 3/32 | 7.15 |
| Rush yards allowed / game | 75.1 | 5/32 | 100.5 |
| Yards per carry allowed | 3.80 | 11/32 | 4.10 |
| RB rush yards allowed / game | 72.5 | 7/32 | 93.5 |
| WR yards allowed / game | 115.5 | 4/32 | 147.7 |
| WR receptions allowed / game | 9.5 | 6/32 | 11.4 |
| TE yards allowed / game | 67.5 | 28/32 | 54.3 |
| TE receptions allowed / game | 5.9 | 25/32 | 5.3 |
| RB receiving yards allowed / game | 36.5 | 18/32 | 33.5 |
| RB receptions allowed / game | 5.0 | 23/32 | 4.5 |
| Explosive passes (20+) allowed / game | 2.75 | 8/32 | 2.97 |
| Explosive runs (15+) allowed / game | 0.62 | 2/32 | 1.22 |
| Sack rate | 4.7% | 28/32 | 6.7% |
| Pressure rate (sacks + hits) | 19.8% | 4/32 | 15.7% |
| Third-down conversions allowed | 30.2% | 3/32 | 39.2% |
| Red-zone TD rate allowed | 52.2% | 11/32 | 58.5% |
| Takeaways / game | 1.62 | 4/32 | 1.22 |

Blitz rate 36.9% and play-action faced 22.0% on 287 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.8 per game, 30.0% completed.

### BUF defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | vs NE | 29 | 269 | 90 | 89 | 13-168 | 6-74 | 3-27 | 3 | 2 | 1 |
| 5 | @ LA | 34 | 383 | 77 | 68 | 23-193 | 8-110 | 9-80 | 5 | 0 | 1 |
| 6 | @ LV | 30 | 313 | 65 | 65 | 6-106 | 11-165 | 6-42 | 4 | 1 | 0 |
| 8 | vs BAL | 10 | 91 | 73 | 73 | 2-35 | 4-29 | 6-27 | 1 | 0 | 4 |
| 9 | @ MIN | 6 | 139 | 51 | 51 | 6-92 | 4-33 | 4-14 | 1 | 0 | 2 |
| 10 | @ NYJ | 12 | 285 | 83 | 83 | 14-189 | 5-23 | 5-73 | 5 | 0 | 4 |
| 11 | vs MIA | 9 | 102 | 90 | 79 | 7-85 | 2-12 | 3-5 | 1 | 2 | 2 |
| 12 | vs KC | 10 | 174 | 72 | 72 | 5-56 | 7-94 | 4-24 | 2 | 0 | 1 |

### Best individual lines allowed by BUF

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 4 | NE | H.Henry (TE) 5/5 for 62, 0 TD | R.Stevenson (RB) 13 for 47, 1 TD |
| 5 | LA | P.Nacua (WR) 17/24 for 138, 1 TD | K.Williams (RB) 16 for 49, 1 TD |
| 6 | LV | T.Tucker (WR) 5/7 for 97, 2 TD | M.Washington (RB) 9 for 43, 0 TD |
| 8 | BAL | R.Bateman (WR) 1/3 for 22, 0 TD | D.Henry (RB) 11 for 53, 1 TD |
| 9 | MIN | J.Jefferson (WR) 3/11 for 58, 0 TD | J.Mason (RB) 6 for 35, 0 TD |
| 10 | NYJ | G.Wilson (WR) 7/14 for 106, 0 TD | B.Hall (RB) 11 for 41, 0 TD |
| 11 | MIA | M.Washington (WR) 3/6 for 30, 0 TD | O.Gordon (RB) 11 for 69, 0 TD |
| 12 | KC | T.Kelce (TE) 4/7 for 71, 0 TD | E.Johnson (RB) 17 for 72, 1 TD |

### BUF run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 65 | 215 | 3.31 | 1 |
| right guard | 20 | 102 | 5.1 | 1 |
| left tackle | 18 | 53 | 2.94 | 0 |
| left guard | 18 | 58 | 3.22 | 0 |
| right tackle | 17 | 63 | 3.71 | 0 |
| left end | 11 | 78 | 7.09 | 1 |
| right end | 4 | 32 | 8.0 | 0 |
| right | 1 | 0 | 0.0 | 0 |

### BUF defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Davison Igbinosun | 7 | 46 | 19 | 231 | 5.0 | 2 | 2 | 3 |
| Cole Bishop | 7 | 33 | 17 | 220 | 6.7 | 0 | 0 | 4 |
| Terrel Bernard | 7 | 30 | 18 | 118 | 3.9 | 1 | 1 | 4 |
| Christian Benford | 5 | 29 | 14 | 155 | 5.3 | 1 | 0 | 0 |
| Maxwell Hairston | 7 | 23 | 11 | 123 | 5.3 | 2 | 0 | 1 |
| Damar Hamlin | 7 | 15 | 8 | 140 | 9.3 | 0 | 1 | 0 |
| Dorian Williams | 6 | 15 | 10 | 117 | 7.8 | 0 | 2 | 2 |
| C.J. Gardner-Johnson | 3 | 14 | 10 | 153 | 10.9 | 1 | 0 | 2 |
| Kaleb Elarms-Orr | 7 | 12 | 7 | 78 | 6.5 | 0 | 0 | 0 |
| Dee Alford | 5 | 11 | 5 | 32 | 2.9 | 0 | 1 | 0 |

### BUF pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Gregory Rousseau | 7 | 25 | 4.0 | 8 | 25 |
| Ed Oliver | 5 | 9 | 0.5 | 0 | 0 |
| Bradley Chubb | 6 | 8 | 0.0 | 4 | 24 |
| T.J. Parker | 5 | 7 | 3.5 | 1 | 5 |
| Deone Walker | 4 | 5 | 0.0 | 3 | 0 |
| Landon Jackson | 3 | 4 | 1.0 | 2 | 0 |
| T.J. Sanders | 3 | 3 | 0.0 | 0 | 0 |
| DeWayne Carter | 4 | 3 | 1.0 | 0 | 0 |

### BUF offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 28.1 | 6/32 | 23.3 |
| Pass yards / game | 231.5 | 18/32 | 234.4 |
| Yards per pass attempt | 7.78 | 8/32 | 7.13 |
| Rush yards / game | 126.9 | 4/32 | 101.0 |
| Yards per carry | 4.16 | 13/32 | 4.11 |
| RB rush yards / game | 112.8 | 5/32 | 93.8 |
| WR yards / game | 132.9 | 22/32 | 147.6 |
| TE yards / game | 50.9 | 17/32 | 53.3 |
| RB receiving yards / game | 47.8 | 5/32 | 33.4 |
| Explosive passes (20+) / game | 3.50 | 9/32 | 2.98 |
| Explosive runs (15+) / game | 1.62 | 5/32 | 1.22 |
| Sack rate allowed | 5.6% | 12/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 13.0% | 7/32 | 15.4% |
| Third-down conversion rate | 42.2% | 9/32 | 39.4% |
| Red-zone TD rate | 58.1% | 16/32 | 58.9% |

Neutral-situation pass rate 49.0%; 64.1 plays per game; target share WR 56% / TE 24% / RB 20%.

### BUF offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | vs NE | 26 | 253 | 87 | 81 | 15-212 | 3-20 | 5-21 | 5 | 2 | 1 |
| 5 | @ LA | 37 | 210 | 127 | 113 | 4-87 | 2-13 | 6-110 | 4 | 7 | 1 |
| 6 | @ LV | 33 | 255 | 104 | 102 | 9-130 | 8-38 | 6-87 | 4 | 0 | 2 |
| 8 | vs BAL | 36 | 289 | 135 | 114 | 10-150 | 6-99 | 5-40 | 4 | 1 | 1 |
| 9 | @ MIN | 23 | 234 | 132 | 110 | 10-100 | 9-98 | 2-36 | 3 | 0 | 4 |
| 10 | @ NYJ | 31 | 196 | 204 | 165 | 7-127 | 3-65 | 1-4 | 3 | 2 | 1 |
| 11 | vs MIA | 26 | 334 | 96 | 94 | 15-209 | 3-61 | 10-64 | 5 | 0 | 3 |
| 12 | vs KC | 13 | 81 | 130 | 123 | 5-48 | 2-13 | 3-20 | 0 | 1 | 2 |

**QB J.Allen** (8 games): 148/237, 1822 yds, 9 TD, 9 INT, 15 sacks, 7.69 yds/att, depth of target 8.4, pressured on 13.9% of dropbacks. Yards by game: W4 253, W5 210, W6 255, W8 289, W9 234, W10 196, W11 304, W12 81.

**QB T.Doman** (1 games): 1/1, 30 yds, 0 TD, 0 INT, 0 sacks, 30.00 yds/att, depth of target 27.0, pressured on 0.0% of dropbacks. Yards by game: W11 30.

### BUF receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K.Shakir | WR | 8 | 45 | 33 | 478 | 1 | 20% | 13% | 5.6 | 5 | 6 | 82 80 34 64 58 26 101 33 |
| D.Moore | WR | 6 | 36 | 22 | 314 | 3 | 16% | 26% | 13.6 | 7 | 4 | 11 82 25 90 91 15 |
| K.Coleman | WR | 8 | 32 | 18 | 231 | 3 | 14% | 25% | 15.0 | 4 | 5 | 116 7 59 4 17 11 17 0 |
| D.Kincaid | TE | 7 | 26 | 20 | 237 | 1 | 12% | 9% | 6.6 | 6 | 3 | 7 7 38 86 28 58 13 |
| T.Johnson | RB | 8 | 24 | 23 | 231 | 0 | 11% | 0% | 0.0 | 4 | 3 | 9 72 24 19 36 4 55 12 |
| D.Knox | TE | 8 | 20 | 12 | 100 | 0 | 9% | 5% | 4.3 | 5 | 1 | 13 6 0 6 37 7 31 0 |
| J.Cook | RB | 8 | 14 | 11 | 105 | 0 | 6% | -0% | -0.4 | 1 | 2 | 8 7 58 21 0 0 3 8 |
| J.Palmer | WR | 3 | 7 | 2 | 40 | 0 | 3% | 11% | 29.1 | 0 | 1 | 3 37 0 |
| R.Davis | RB | 6 | 7 | 4 | 46 | 0 | 3% | -1% | -2.0 | 0 | 1 | 4 31 5 0 6 0 |

### BUF rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| J.Cook | RB | 8 | 183 | 831 | 4.54 | 9 | 75% | 39 | 8 | 75 111 95 80 107 157 89 117 |
| J.Allen | QB | 7 | 24 | 57 | 2.38 | 5 | 10% | 12 | 0 | 0 14 2 17 11 6 7 |
| R.Davis | RB | 8 | 20 | 58 | 2.90 | 0 | 8% | 1 | 0 | 3 2 4 30 2 8 3 6 |
| T.Johnson | RB | 5 | 8 | 13 | 1.62 | 0 | 3% | 4 | 0 | 3 3 4 1 2 |
| K.Shakir | WR | 2 | 5 | 31 | 6.20 | 0 | 2% | 2 | 0 | 29 2 |

### BUF run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 80 | 314 | 3.92 | 4 |
| right guard | 41 | 169 | 4.12 | 0 |
| left guard | 35 | 125 | 3.57 | 0 |
| right tackle | 35 | 197 | 5.63 | 2 |
| left tackle | 22 | 76 | 3.45 | 1 |
| left end | 19 | 103 | 5.42 | 1 |
| right end | 11 | 31 | 2.82 | 0 |

### BUF by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Under center | 266 | 52% | 29% | 5.44 | 0.107 |
| offense | Shotgun | 225 | 44% | 78% | 5.7 | 0.011 |
| offense | No huddle | 22 | 4% | 73% | 8.82 | 0.444 |
| defense vs | Shotgun | 264 | 56% | 81% | 5.01 | -0.112 |
| defense vs | Under center | 182 | 38% | 43% | 4.65 | -0.049 |
| defense vs | No huddle | 30 | 6% | 90% | 6.5 | 0.156 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 69 | 29% | 67% | 6.49 | 5 |
| offense | Short middle | 34 | 14% | 62% | 7.59 | 3 |
| offense | Short right | 86 | 36% | 73% | 6.03 | 3 |
| offense | Deep left | 15 | 6% | 33% | 9.53 | 5 |
| offense | Deep middle | 14 | 6% | 57% | 19.0 | 6 |
| offense | Deep right | 20 | 8% | 30% | 10.9 | 6 |
| defense allows | Short left | 81 | 28% | 59% | 5.58 | 3 |
| defense allows | Short middle | 51 | 18% | 61% | 5.73 | 0 |
| defense allows | Short right | 104 | 36% | 61% | 4.66 | 1 |
| defense allows | Deep left | 21 | 7% | 38% | 9.71 | 7 |
| defense allows | Deep middle | 16 | 6% | 44% | 11.44 | 6 |
| defense allows | Deep right | 19 | 6% | 32% | 7.37 | 5 |

### BUF lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Dion Dawkins, LG Alec Anderson, C Connor McGovern, RG O'Cyrus Torrence, RT Spencer Brown.  
Defensive front: LDE T.J. Sanders, NT Deone Walker, RDE Ed Oliver, WLB Greg Rousseau, SLB Bradley Chubb.

### BUF injuries

Official report not posted yet for this week.

ESPN live list (designations only): Jalon Kilgore (S) Out; Jude Bowry (OT) Out; Mike Danna (DE) Out; Greg Gaines (DT) Out; Skyler Bell (WR) Out; Christian Benford (CB) Out.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### BUF roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Austin Johnson (DL) to JAX; Shane Buechele (QB) to IND; A.J. Woods (DB) to LV; Chase Lundt (OL) to SEA.

## NE (last 8 games: weeks 3, 4, 5, 6, 7, 8, 9, 10)

### NE defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 28.2 | 28/32 | 23.3 |
| Pass yards allowed / game | 272.4 | 31/32 | 235.6 |
| Yards per pass attempt allowed | 8.61 | 31/32 | 7.15 |
| Rush yards allowed / game | 103.8 | 17/32 | 100.5 |
| Yards per carry allowed | 4.13 | 17/32 | 4.10 |
| RB rush yards allowed / game | 97.2 | 17/32 | 93.5 |
| WR yards allowed / game | 186.4 | 30/32 | 147.7 |
| WR receptions allowed / game | 12.6 | 24/32 | 11.4 |
| TE yards allowed / game | 49.4 | 13/32 | 54.3 |
| TE receptions allowed / game | 5.0 | 11/32 | 5.3 |
| RB receiving yards allowed / game | 36.6 | 19/32 | 33.5 |
| RB receptions allowed / game | 4.1 | 11/32 | 4.5 |
| Explosive passes (20+) allowed / game | 4.00 | 31/32 | 2.97 |
| Explosive runs (15+) allowed / game | 1.00 | 11/32 | 1.22 |
| Sack rate | 7.4% | 10/32 | 6.7% |
| Pressure rate (sacks + hits) | 16.0% | 13/32 | 15.7% |
| Third-down conversions allowed | 45.5% | 26/32 | 39.2% |
| Red-zone TD rate allowed | 65.5% | 23/32 | 58.5% |
| Takeaways / game | 1.00 | 19/32 | 1.22 |

Blitz rate 34.4% and play-action faced 23.8% on 282 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.0 per game, 50.0% completed.

### NE defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ JAX | 35 | 182 | 129 | 112 | 12-124 | 3-32 | 4-26 | 1 | 1 | 1 |
| 4 | @ BUF | 26 | 253 | 87 | 81 | 15-212 | 3-20 | 5-21 | 5 | 2 | 1 |
| 5 | vs LV | 17 | 291 | 35 | 41 | 8-99 | 10-121 | 7-71 | 4 | 0 | 3 |
| 6 | vs NYJ | 19 | 252 | 98 | 94 | 11-162 | 6-54 | 3-36 | 1 | 1 | 3 |
| 7 | @ CHI | 30 | 308 | 98 | 91 | 8-199 | 10-97 | 4-12 | 8 | 0 | 3 |
| 8 | @ MIA | 19 | 211 | 74 | 74 | 17-168 | 4-43 | 0-0 | 2 | 1 | 5 |
| 9 | vs GB | 45 | 372 | 116 | 95 | 20-360 | 1-1 | 2-11 | 7 | 1 | 3 |
| 10 | @ DET | 35 | 310 | 193 | 190 | 10-167 | 3-27 | 8-116 | 4 | 2 | 2 |

### Best individual lines allowed by NE

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | JAX | J.Meyers (WR) 7/8 for 64, 1 TD | B.Tuten (RB) 15 for 73, 1 TD |
| 4 | BUF | K.Coleman (WR) 6/7 for 116, 1 TD | J.Cook (RB) 12 for 75, 1 TD |
| 5 | LV | B.Bowers (TE) 8/10 for 110, 1 TD | A.Jeanty (RB) 10 for 27, 0 TD |
| 6 | NYJ | O.Cooper (WR) 6/7 for 103, 1 TD | B.Allen (RB) 17 for 78, 0 TD |
| 7 | CHI | L.Burden (WR) 4/4 for 130, 1 TD | D.Swift (RB) 22 for 78, 1 TD |
| 8 | MIA | K.Coleman (WR) 3/3 for 46, 1 TD | O.Gordon (RB) 19 for 69, 0 TD |
| 9 | GB | C.Watson (WR) 7/8 for 171, 1 TD | K.Johnson (RB) 14 for 68, 1 TD |
| 10 | DET | J.Gibbs (RB) 7/8 for 99, 0 TD | J.Gibbs (RB) 22 for 153, 2 TD |

### NE run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 54 | 235 | 4.35 | 2 |
| left end | 32 | 158 | 4.94 | 2 |
| right guard | 30 | 91 | 3.03 | 0 |
| right tackle | 24 | 78 | 3.25 | 1 |
| left guard | 21 | 67 | 3.19 | 0 |
| right end | 20 | 99 | 4.95 | 1 |
| left tackle | 19 | 102 | 5.37 | 2 |

### NE defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Marcus Jones | 8 | 39 | 26 | 324 | 8.3 | 3 | 1 | 5 |
| Christian Gonzalez | 6 | 34 | 25 | 445 | 13.1 | 3 | 1 | 2 |
| Carlton Davis | 4 | 29 | 23 | 235 | 8.1 | 0 | 0 | 2 |
| Christian Elliss | 8 | 29 | 23 | 186 | 6.4 | 2 | 0 | 3 |
| Kevin Byard | 8 | 24 | 12 | 201 | 8.4 | 2 | 2 | 6 |
| Charles Woods | 7 | 23 | 14 | 234 | 10.2 | 3 | 1 | 3 |
| Craig Woodson | 7 | 22 | 12 | 165 | 7.5 | 1 | 1 | 2 |
| Robert Spillane | 8 | 20 | 11 | 93 | 4.7 | 0 | 0 | 5 |
| Jaylen Reed | 6 | 8 | 6 | 73 | 9.1 | 1 | 0 | 2 |
| Kindle Vildor | 2 | 7 | 4 | 59 | 8.4 | 0 | 0 | 0 |

### NE pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Elijah Ponder | 8 | 16 | 6.5 | 5 | 4 |
| Gabe Jacas | 7 | 9 | 2.5 | 2 | 14 |
| Christian Elliss | 8 | 7 | 0.5 | 2 | 45 |
| Cory Durden | 7 | 7 | 1.5 | 1 | 0 |
| Christian Barmore | 6 | 7 | 3.5 | 0 | 0 |
| Dre'Mont Jones | 6 | 5 | 0.5 | 3 | 6 |
| Milton Williams | 5 | 5 | 2.0 | 2 | 0 |
| Leonard Taylor | 3 | 3 | 2.0 | 1 | 0 |

### NE offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 23.9 | 13/32 | 23.3 |
| Pass yards / game | 261.5 | 9/32 | 234.4 |
| Yards per pass attempt | 8.27 | 5/32 | 7.13 |
| Rush yards / game | 90.9 | 20/32 | 101.0 |
| Yards per carry | 3.91 | 20/32 | 4.11 |
| RB rush yards / game | 88.2 | 18/32 | 93.8 |
| WR yards / game | 162.5 | 9/32 | 147.6 |
| TE yards / game | 64.5 | 9/32 | 53.3 |
| RB receiving yards / game | 34.5 | 13/32 | 33.4 |
| Explosive passes (20+) / game | 3.88 | 3/32 | 2.98 |
| Explosive runs (15+) / game | 1.12 | 22/32 | 1.22 |
| Sack rate allowed | 6.4% | 17/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 14.2% | 11/32 | 15.4% |
| Third-down conversion rate | 42.9% | 8/32 | 39.4% |
| Red-zone TD rate | 58.3% | 15/32 | 58.9% |

Neutral-situation pass rate 53.4%; 60.1 plays per game; target share WR 60% / TE 24% / RB 16%.

### NE offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ JAX | 6 | 245 | 64 | 63 | 12-209 | 1-5 | 5-31 | 5 | 0 | 3 |
| 4 | @ BUF | 29 | 269 | 90 | 89 | 13-168 | 6-74 | 3-27 | 3 | 2 | 1 |
| 5 | vs LV | 45 | 374 | 143 | 138 | 13-241 | 8-101 | 5-32 | 5 | 2 | 1 |
| 6 | vs NYJ | 26 | 235 | 124 | 124 | 12-167 | 5-59 | 1-9 | 2 | 1 | 0 |
| 7 | @ CHI | 24 | 321 | 44 | 44 | 7-87 | 10-127 | 7-107 | 2 | 1 | 2 |
| 8 | @ MIA | 24 | 199 | 129 | 126 | 9-156 | 4-35 | 3-8 | 4 | 1 | 3 |
| 9 | vs GB | 27 | 320 | 91 | 91 | 13-193 | 6-87 | 3-40 | 8 | 2 | 4 |
| 10 | @ DET | 10 | 129 | 42 | 31 | 8-79 | 3-28 | 4-22 | 2 | 0 | 5 |

**QB D.Maye** (8 games): 144/220, 1944 yds, 17 TD, 7 INT, 15 sacks, 8.84 yds/att, depth of target 9.5, pressured on 15.7% of dropbacks. Yards by game: W3 199, W4 269, W5 374, W6 235, W7 321, W8 199, W9 299, W10 48.

**QB T.DeVito** (3 games): 16/32, 132 yds, 1 TD, 1 INT, 4 sacks, 4.12 yds/att, depth of target 9.1, pressured on 11.1% of dropbacks. Yards by game: W3 30, W9 21, W10 81.

### NE receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D.Douglas | WR | 8 | 40 | 26 | 409 | 4 | 17% | 21% | 12.1 | 4 | 8 | 38 15 65 86 23 76 102 4 |
| H.Henry | TE | 8 | 32 | 28 | 317 | 2 | 13% | 8% | 5.8 | 5 | 4 | 5 62 44 48 71 30 35 22 |
| M.Hollins | WR | 4 | 25 | 17 | 224 | 1 | 11% | 15% | 14.3 | 5 | 4 | 87 53 36 48 |
| E.Chism | WR | 8 | 25 | 19 | 202 | 2 | 11% | 9% | 8.2 | 5 | 2 | 1 42 57 0 16 37 49 0 |
| E.Raridon | TE | 7 | 25 | 15 | 199 | 1 | 11% | 7% | 7.0 | 5 | 3 | 12 57 11 56 5 52 6 |
| R.Stevenson | RB | 7 | 24 | 21 | 212 | 2 | 10% | 2% | 1.6 | 1 | 2 | 16 27 21 93 8 46 1 |
| A.Brown | WR | 3 | 22 | 8 | 102 | 0 | 9% | 13% | 14.3 | 3 | 1 | 27 48 27 |
| R.Doubs | WR | 4 | 17 | 11 | 165 | 3 | 7% | 12% | 16.0 | 5 | 3 | 49 58 16 42 |
| K.Williams | WR | 8 | 14 | 6 | 180 | 2 | 6% | 13% | 22.4 | 0 | 4 | 34 0 91 12 0 43 0 0 |

### NE rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| R.Stevenson | RB | 8 | 84 | 309 | 3.68 | 2 | 45% | 12 | 2 | 22 47 64 36 22 82 32 4 |
| C.Kiner | RB | 7 | 52 | 258 | 4.96 | 1 | 28% | 8 | 3 | 18 52 57 13 38 55 25 |
| T.Henderson | RB | 5 | 36 | 127 | 3.53 | 0 | 19% | 2 | 0 | 23 42 22 31 9 |
| D.Maye | QB | 8 | 9 | 19 | 2.11 | 2 | 5% | 4 | 0 | 1 1 3 0 0 3 0 11 |
| L.Larison | RB | 3 | 4 | 12 | 3.00 | 0 | 2% | 0 | 0 | 6 4 2 |

### NE run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 78 | 298 | 3.82 | 2 |
| left guard | 23 | 88 | 3.83 | 0 |
| left end | 23 | 96 | 4.17 | 1 |
| right tackle | 22 | 100 | 4.55 | 1 |
| right guard | 21 | 82 | 3.9 | 0 |
| left tackle | 13 | 45 | 3.46 | 1 |
| right end | 4 | 17 | 4.25 | 0 |

### NE by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 298 | 62% | 79% | 6.51 | 0.086 |
| offense | Under center | 178 | 37% | 32% | 4.98 | -0.038 |
| offense | No huddle | 5 | 1% | 80% | 11.2 | 0.483 |
| defense vs | Shotgun | 243 | 50% | 79% | 6.2 | 0.115 |
| defense vs | Under center | 212 | 44% | 32% | 5.67 | 0.083 |
| defense vs | No huddle | 28 | 6% | 75% | 8.07 | 0.247 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 78 | 31% | 62% | 5.55 | 4 |
| offense | Short middle | 34 | 13% | 71% | 6.71 | 0 |
| offense | Short right | 81 | 32% | 72% | 6.89 | 3 |
| offense | Deep left | 27 | 11% | 44% | 11.85 | 10 |
| offense | Deep middle | 5 | 2% | 80% | 15.0 | 2 |
| offense | Deep right | 28 | 11% | 54% | 17.07 | 12 |
| defense allows | Short left | 74 | 29% | 69% | 6.54 | 4 |
| defense allows | Short middle | 46 | 18% | 72% | 7.65 | 3 |
| defense allows | Short right | 84 | 33% | 74% | 6.3 | 4 |
| defense allows | Deep left | 22 | 9% | 55% | 16.32 | 10 |
| defense allows | Deep middle | 10 | 4% | 50% | 16.5 | 4 |
| defense allows | Deep right | 17 | 7% | 65% | 17.06 | 7 |

### NE lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Will Campbell, LG Greg Van Roten, C Jared Wilson, RG Matt Pryor, RT Morgan Moses.  
Defensive front: LDE Christian Barmore, NT Cory Durden, RDE Milton Williams, WLB Elijah Ponder, SLB Dre'Mont Jones.

### NE injuries

Official report not posted yet for this week.

ESPN live list (designations only): Dre'Mont Jones (DE) Questionable; Drake Maye (QB) Out; Alijah Vera-Tucker (G) Injured Reserve; Reggie Gilliam (FB) Questionable; Walter Rouse (OL) Questionable; A.J. Brown (WR) Out; Romeo Doubs (WR) Injured Reserve; Carlton Davis III (CB) Out.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### NE roster moves (last 4 weeks)

Arrived: none.  
Left for another team: K.J. Britt (LB) to DET; Jake Kubas (OL) to DAL.

## Keyed connectors in this run

| Secret | Provider | Status | Used for |
|---|---|---|---|
| ODDS_API_KEY | The Odds API | KEY_NOT_CONFIGURED_IN_THIS_RUN | Pinnacle / DraftKings / FanDuel prices, props and line movement in every packet |
| NFL_BDL_API_KEY | BallDontLie NFL | KEY_NOT_CONFIGURED_IN_THIS_RUN | second-source check of the slate (schedule and teams) |
| NFL_API_SPORTS_KEY | API-Sports NFL | KEY_NOT_CONFIGURED_IN_THIS_RUN | access check only; not used in the packet |

Scheduled runs only see GitHub repository secrets. A key connected inside a chat tool is not visible here.

## Phase ledger

| Phase | Name | Status | What this packet has / what is missing |
|---|---|---|---|
| 1 | Slate, schedule, venue | AUTO | Schedule, kickoff, site, roof, surface, rest days, listed QBs. |
| 2 | Player identity and position | AUTO | Positions from weekly rosters (GSIS IDs). Name-only joins are used for snap counts and PFR defenders. |
| 3 | Verified player game history | AUTO | Per-game logs for QBs, receivers and rushers over the window, from play-by-play. |
| 4 | Role, snaps, routes, opportunity | PARTIAL | Target share, air-yards share, carry share, red-zone looks, snap share. Routes run and route participation are NOT available. |
| 5 | Team offense/defense baselines | AUTO | Allowed and produced tables with league ranks and game-by-game trends. |
| 6 | Opponent context and game script | PARTIAL | Market spread/total, neutral pass rate, pace. The script call itself is the analyst's. |
| 7 | Coverage structure and shell | PARTIAL | Blitz and play-action rates from FTN charting. Man/zone and shell are NOT in any free source here. |
| 8 | Defender assignment and explosive allowance | PARTIAL | Per-defender targets/yards allowed (PFR) and explosive plays allowed. Who covers whom is NOT known. |
| 9 | QB pressure, blitz, scramble | PARTIAL | Sack rate, sacks + QB hits rate (a floor on pressure), blitz rate, scrambles. |
| 10 | Offensive line, pass rush, coaching | PARTIAL | Depth-chart line, pressure allowed, run yards by direction, pass-rush leaders. No line grades. |
| 11 | Injury and depth chart | PARTIAL | Official weekly report and depth chart; ESPN live list when reachable. Recent roster arrivals/departures. |
| 12 | Weather, roof, travel | PARTIAL | Roof, surface, rest days, site; National Weather Service kickoff forecast: KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days. |
| 13 | Timestamped book prices | PARTIAL | Pinnacle / DraftKings / FanDuel prices with no-vig and first-seen-to-now movement, no player props in this run. No FTN model, no true opening line. |
| 14 | Projection and simulation | PARTIAL_RESEARCH_ONLY | Period-engine team scores; player baselines. Not the three-model consensus; not validated. |
| 15 | Final inactive pregame freeze | PENDING | Inactives post about 90 minutes before kickoff. Re-run or check them by hand before any final call. |

## Sources

| Dataset | Status | Retrieved (UTC) | SHA-256 (first 12) |
|---|---|---|---|
| games | OK | 2026-11-27T18:38:47+00:00 | 4fdf3a2bbfb1 |
| pbp | OK | 2026-11-27T18:38:47+00:00 | 2b2ef85b4456 |
| rosters | OK | 2026-11-27T18:38:48+00:00 | 06b4b4cecfb8 |
| injuries | OK | 2026-11-27T18:38:48+00:00 | ace8009e13f6 |
| depth_charts | OK | 2026-11-27T18:38:48+00:00 | 57991dafec0f |
| snap_counts | OK | 2026-11-27T18:38:48+00:00 | a671bbfca0a9 |
| ftn | OK | 2026-11-27T18:38:48+00:00 | ee09d5f28f5f |
| pfr_def | OK | 2026-11-27T18:38:48+00:00 | f1217d79cc1e |
| pfr_rec | OK | 2026-11-27T18:38:48+00:00 | 14b79cccde48 |
| pfr_rush | OK | 2026-11-27T18:38:49+00:00 | 45b28d9bfb26 |
| ngs_receiving | OK | 2026-11-27T18:38:49+00:00 | 115f58b6825a |
| ngs_rushing | OK | 2026-11-27T18:38:49+00:00 | cefb252761e8 |
| ngs_passing | OK | 2026-11-27T18:38:49+00:00 | 23d6077e29fc |
| espn_injuries | OK | 2026-11-27T18:38:50+00:00 |  |
| nfl_savant | SAME_DATA_AS_NFLVERSE_PBP: its season download is the nflverse play-by-play (checked 2026-11-11), so no second download is made |  |  |
| book_odds | NO_KEY: set the ODDS_API_KEY repository secret to include book prices |  |  |

Play-by-play, rosters, injuries, depth charts, snap counts and PFR advanced defense: nflverse (github.com/nflverse/nflverse-data). FTN charting via nflverse: FTN Data, CC-BY-SA 4.0. Third-party data keep their own terms; see SOURCES.md.
