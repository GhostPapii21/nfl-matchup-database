# HOU at PIT: Week 13, Sunday Night Football

**Sunday 2026-12-06, 20:20 ET.** Site: Home; roof: outdoors; surface: grass. Rest: HOU 7 days, PIT 9 days. Listed QBs: C.J. Stroud (HOU), Mason Rudolph (PIT).

Market (schedule consensus, not a timestamped quote): PIT +4.5, total 41.5.

Generated 2026-11-26T11:17:48+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T10:45:27Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | PIT +4.5 | -105 | -115 | 48.9% | 51.1% | 4.7% | 2026-11-26T10:45:27+00:00 |
| total | fanduel | Over 42.5 | -105 | -115 | 48.9% | 51.1% | 4.7% | 2026-11-26T10:45:27+00:00 |
| moneyline | fanduel | PIT | +184 | -220 | 33.9% | 66.1% | 4.0% | 2026-11-26T10:45:27+00:00 |

Player props: OK.

## Matchup edges

### HOU offense vs PIT defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| HOU OFFENCE ADVANTAGE | wide receiver yards | 196.8 | 168.0 | 147.8 | HOU offence ranks 4 of 32, PIT defence ranks 26 of 32 (1 = best at its own job) |
| PIT DEFENCE WEAK SPOT | running back receiving yards | 18.2 | 42.8 | 33.0 | HOU offence ranks 29 of 32, PIT defence ranks 29 of 32 (1 = best at its own job) |
| PIT DEFENCE ADVANTAGE | running back rushing yards | 78.2 | 60.1 | 92.5 | HOU offence ranks 24 of 32, PIT defence ranks 2 of 32 (1 = best at its own job) |
| HOU OFFENCE ADVANTAGE | explosive passes (20+) | 3.5 | 3.4 | 3.0 | HOU offence ranks 10 of 32, PIT defence ranks 23 of 32 (1 = best at its own job) |
| PIT DEFENCE ADVANTAGE | explosive runs (15+) | 0.4 | 0.6 | 1.2 | HOU offence ranks 31 of 32, PIT defence ranks 2 of 32 (1 = best at its own job) |
| PIT DEFENCE WEAK SPOT | passing yards | 254.5 | 266.9 | 235.6 | HOU offence ranks 11 of 32, PIT defence ranks 27 of 32 (1 = best at its own job) |
| PIT DEFENCE STRENGTH | red-zone touchdowns | 66.7% | 50.0% | 58.0% | HOU offence ranks 9 of 32, PIT defence ranks 4 of 32 (1 = best at its own job) |
| HOU OFFENCE ADVANTAGE | pressure (sacks + hits) | 10.1% | 13.8% | 15.7% | HOU offence ranks 3 of 32, PIT defence ranks 24 of 32 (1 = best at its own job) |

### PIT offense vs HOU defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| HOU DEFENCE WEAK SPOT | wide receiver yards | 125.4 | 174.0 | 147.8 | PIT offence ranks 23 of 32, HOU defence ranks 28 of 32 (1 = best at its own job) |
| HOU DEFENCE STRENGTH | tight end yards | 61.1 | 42.6 | 54.7 | PIT offence ranks 11 of 32, HOU defence ranks 5 of 32 (1 = best at its own job) |
| HOU DEFENCE WEAK SPOT | explosive passes (20+) | 3.1 | 3.6 | 3.0 | PIT offence ranks 17 of 32, HOU defence ranks 28 of 32 (1 = best at its own job) |
| HOU DEFENCE STRENGTH | explosive runs (15+) | 1.6 | 0.8 | 1.2 | PIT offence ranks 5 of 32, HOU defence ranks 5 of 32 (1 = best at its own job) |
| HOU DEFENCE WEAK SPOT | red-zone touchdowns | 46.2% | 68.2% | 58.0% | PIT offence ranks 29 of 32, HOU defence ranks 25 of 32 (1 = best at its own job) |
| HOU DEFENCE ADVANTAGE | sacks (pass protection vs pass rush) | 8.0% | 8.7% | 6.6% | PIT offence ranks 25 of 32, HOU defence ranks 4 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | HOU 23.2 - PIT 20.8 | 43.9 | -2.4 | 48.9% | 68.8% | 54.4% | HOU 11.9 - PIT 9.9 |
| independent | HOU 24.7 - PIT 22.6 | 47.4 | -2.1 | 47.7% | 60.0% | 69.0% | HOU 13.3 - PIT 11.1 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### HOU offense vs PIT defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N.Collins | WR | receiving yards | 7 | 68.3 | 1.068 | 22.1 | 37.8 | 53.5 | 59.0 | 59.3 | 62.0 |
| N.Collins | WR | receptions | 7 | 5.2 | 1.114 | 2.6 | 2.9 | 3.2 | 3.3 | 3.3 | 4.5 |
| X.Hutchinson | WR | receiving yards | 8 | 36.6 | 1.068 | 11.8 | 12.9 | 14.1 | 15.6 | 17.1 | 40.1 |
| X.Hutchinson | WR | receptions | 8 | 3.3 | 1.114 | 2.2 | 2.2 | 2.3 | 2.7 | 3.1 | 3.3 |
| D.Schultz | TE | receiving yards | 8 | 26.4 | 1.017 | 9.9 | 10.6 | 11.2 | 11.2 | 11.2 | 30.5 |
| D.Schultz | TE | receptions | 8 | 2.5 | 0.991 | 1.0 | 1.0 | 1.0 | 1.4 | 1.7 | 2.5 |
| K.Boutte | WR | receiving yards | 8 | 41.6 | 1.068 | 6.0 | 12.0 | 17.4 | 19.2 | 21.1 | 32.6 |
| K.Boutte | WR | receptions | 8 | 2.3 | 1.114 | 0.4 | 0.8 | 1.2 | 1.6 | 1.9 | 2.2 |
| W.Marks | RB | rushing yards | 7 | 44.2 | 0.85 | 14.5 | 16.3 | 18.1 | 23.5 | 30.6 | 47.6 |
| D.Montgomery | RB | rushing yards | 4 | 42.1 | 0.85 | 11.0 | 12.7 | 14.3 | 16.0 | 17.6 | 24.2 |
| E.Demercado | RB | rushing yards | 3 | 20.0 | 0.85 | 13.6 | 13.6 | 13.6 | 13.6 | 13.6 | 13.6 |
| C.Stroud | QB | passing yards | 8 | 268.7 | 1.066 | 168.4 | 173.6 | 179.5 | 189.6 | 199.7 | 251.7 |

### PIT offense vs HOU defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D.Metcalf | WR | receiving yards | 8 | 46.2 | 1.088 | 2.9 | 3.7 | 4.8 | 7.8 | 10.9 | 46.3 |
| D.Metcalf | WR | receptions | 8 | 3.3 | 1.021 | 1.0 | 1.0 | 1.1 | 1.4 | 1.8 | 2.6 |
| G.Bernard | WR | receiving yards | 8 | 38.8 | 1.088 | 4.2 | 8.4 | 12.1 | 13.3 | 14.4 | 31.0 |
| G.Bernard | WR | receptions | 8 | 4.4 | 1.021 | 0.4 | 0.7 | 1.1 | 1.4 | 1.8 | 4.1 |
| J.Warren | RB | receiving yards | 8 | 27.4 | 0.951 | 0.3 | 0.7 | 2.1 | 10.5 | 18.8 | 29.0 |
| J.Warren | RB | receptions | 8 | 3.4 | 1.105 | 1.5 | 1.9 | 2.2 | 2.2 | 2.2 | 3.3 |
| P.Freiermuth | TE | receiving yards | 8 | 26.4 | 0.89 | 11.7 | 13.5 | 15.3 | 16.2 | 17.1 | 28.9 |
| P.Freiermuth | TE | receptions | 8 | 2.7 | 0.933 | 1.9 | 1.9 | 1.9 | 1.9 | 1.9 | 1.9 |
| D.Washington | TE | receiving yards | 8 | 27.4 | 0.89 | 3.9 | 4.2 | 4.8 | 6.9 | 9.1 | 20.9 |
| D.Washington | TE | receptions | 8 | 2.3 | 0.933 | 0.9 | 0.9 | 1.0 | 1.3 | 1.6 | 2.8 |
| J.Warren | RB | rushing yards | 8 | 74.0 | 0.963 | 18.8 | 23.2 | 28.0 | 35.5 | 42.9 | 93.5 |
| R.Dowdle | RB | rushing yards | 5 | 32.2 | 0.963 | 16.6 | 18.7 | 20.8 | 22.9 | 25.0 | 38.5 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## HOU (last 8 games: weeks 3, 4, 5, 6, 7, 9, 10, 11)

### HOU defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 20.8 | 11/32 | 23.0 |
| Pass yards allowed / game | 246.4 | 21/32 | 235.6 |
| Yards per pass attempt allowed | 6.94 | 15/32 | 7.14 |
| Rush yards allowed / game | 91.4 | 13/32 | 99.5 |
| Yards per carry allowed | 3.79 | 11/32 | 4.07 |
| RB rush yards allowed / game | 85.8 | 13/32 | 92.5 |
| WR yards allowed / game | 174.0 | 28/32 | 147.8 |
| WR receptions allowed / game | 11.9 | 20/32 | 11.4 |
| TE yards allowed / game | 42.6 | 5/32 | 54.7 |
| TE receptions allowed / game | 4.6 | 7/32 | 5.3 |
| RB receiving yards allowed / game | 29.8 | 12/32 | 33.0 |
| RB receptions allowed / game | 5.4 | 26/32 | 4.4 |
| Explosive passes (20+) allowed / game | 3.62 | 28/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.75 | 5/32 | 1.21 |
| Sack rate | 8.7% | 4/32 | 6.6% |
| Pressure rate (sacks + hits) | 16.8% | 9/32 | 15.7% |
| Third-down conversions allowed | 38.3% | 15/32 | 39.2% |
| Red-zone TD rate allowed | 68.2% | 25/32 | 58.0% |
| Takeaways / game | 1.25 | 12/32 | 1.23 |

Blitz rate 24.8% and play-action faced 20.8% on 322 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.4 per game, 28.6% completed.

### HOU defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ IND | 19 | 235 | 88 | 82 | 12-160 | 10-71 | 2-4 | 4 | 0 | 4 |
| 4 | vs DAL | 34 | 335 | 68 | 74 | 23-301 | 3-11 | 6-23 | 4 | 0 | 3 |
| 5 | @ TEN | 3 | 170 | 55 | 55 | 13-137 | 1-5 | 9-28 | 1 | 0 | 4 |
| 6 | @ JAX | 31 | 306 | 95 | 95 | 13-206 | 7-52 | 4-48 | 6 | 0 | 0 |
| 7 | vs NYG | 27 | 252 | 188 | 180 | 12-198 | 3-41 | 5-13 | 5 | 4 | 3 |
| 9 | @ LAC | 22 | 217 | 131 | 123 | 6-129 | 5-48 | 4-40 | 2 | 1 | 8 |
| 10 | @ CLE | 27 | 312 | 71 | 44 | 11-157 | 7-91 | 7-64 | 3 | 1 | 4 |
| 11 | vs IND | 3 | 144 | 35 | 33 | 5-104 | 1-22 | 6-18 | 4 | 0 | 2 |

### Best individual lines allowed by HOU

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | IND | J.Downs (WR) 5/11 for 77, 0 TD | J.Taylor (RB) 23 for 68, 0 TD |
| 4 | DAL | C.Lamb (WR) 17/21 for 189, 1 TD | J.Williams (RB) 19 for 62, 3 TD |
| 5 | TEN | W.Robinson (WR) 6/7 for 53, 0 TD | T.Pollard (RB) 14 for 52, 0 TD |
| 6 | JAX | J.Meyers (WR) 5/10 for 83, 0 TD | C.Rodriguez (RB) 11 for 55, 0 TD |
| 7 | NYG | M.Nabers (WR) 7/9 for 111, 0 TD | C.Skattebo (RB) 17 for 124, 1 TD |
| 9 | LAC | Q.Johnston (WR) 1/4 for 58, 1 TD | O.Hampton (RB) 13 for 60, 0 TD |
| 10 | CLE | H.Fannin (TE) 7/9 for 91, 0 TD | Q.Judkins (RB) 10 for 38, 1 TD |
| 11 | IND | A.Gould (WR) 2/3 for 48, 0 TD | J.Taylor (RB) 11 for 21, 0 TD |

### HOU run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 61 | 273 | 4.48 | 2 |
| right guard | 30 | 123 | 4.1 | 1 |
| right tackle | 25 | 95 | 3.8 | 1 |
| left end | 22 | 54 | 2.45 | 0 |
| left guard | 22 | 84 | 3.82 | 0 |
| left tackle | 17 | 34 | 2.0 | 0 |
| right end | 15 | 64 | 4.27 | 1 |

### HOU defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Kamari Lassiter | 8 | 55 | 28 | 327 | 5.9 | 1 | 1 | 2 |
| Derek Stingley Jr. | 8 | 37 | 19 | 299 | 8.1 | 1 | 1 | 7 |
| Calen Bullock | 8 | 34 | 19 | 320 | 9.4 | 1 | 2 | 5 |
| Jake Hansen | 6 | 31 | 21 | 219 | 7.1 | 0 | 1 | 3 |
| Reed Blankenship | 5 | 26 | 18 | 159 | 6.1 | 0 | 1 | 2 |
| M.J. Stewart | 4 | 25 | 16 | 193 | 7.7 | 1 | 0 | 2 |
| Jalen Pitre | 6 | 24 | 13 | 82 | 3.4 | 1 | 0 | 4 |
| Azeez Al-Shaair | 5 | 19 | 13 | 114 | 6.0 | 1 | 0 | 5 |
| Henry To'oTo'o | 5 | 14 | 9 | 108 | 7.7 | 1 | 0 | 3 |
| Tremon Smith | 2 | 7 | 3 | 80 | 11.4 | 0 | 0 | 1 |

### HOU pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Will Anderson | 7 | 24 | 10.0 | 3 | 5 |
| Danielle Hunter | 6 | 19 | 3.0 | 11 | 2 |
| Sheldon Rankins | 6 | 9 | 3.0 | 3 | 0 |
| Logan Hall | 6 | 8 | 3.0 | 2 | 0 |
| Jadeveon Clowney | 4 | 8 | 4.5 | 2 | 0 |
| Azeez Al-Shaair | 5 | 4 | 0.0 | 1 | 12 |
| M.J. Stewart | 4 | 4 | 1.5 | 1 | 7 |
| Jalen Pitre | 6 | 2 | 0.0 | 2 | 11 |

### HOU offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 27.8 | 7/32 | 23.2 |
| Pass yards / game | 254.5 | 11/32 | 234.2 |
| Yards per pass attempt | 8.02 | 8/32 | 7.12 |
| Rush yards / game | 84.4 | 24/32 | 100.6 |
| Yards per carry | 3.59 | 26/32 | 4.10 |
| RB rush yards / game | 78.2 | 24/32 | 93.4 |
| WR yards / game | 196.8 | 4/32 | 147.5 |
| TE yards / game | 39.5 | 23/32 | 53.4 |
| RB receiving yards / game | 18.2 | 29/32 | 33.2 |
| Explosive passes (20+) / game | 3.50 | 10/32 | 2.96 |
| Explosive runs (15+) / game | 0.38 | 31/32 | 1.23 |
| Sack rate allowed | 4.0% | 6/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 10.1% | 3/32 | 15.4% |
| Third-down conversion rate | 42.1% | 10/32 | 39.4% |
| Red-zone TD rate | 66.7% | 9/32 | 58.9% |

Neutral-situation pass rate 60.5%; 58.2 plays per game; target share WR 68% / TE 19% / RB 12%.

### HOU offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ IND | 17 | 167 | 62 | 48 | 8-109 | 5-37 | 3-21 | 2 | 0 | 3 |
| 4 | vs DAL | 30 | 347 | 50 | 46 | 16-285 | 5-62 | 0-0 | 8 | 0 | 2 |
| 5 | @ TEN | 26 | 261 | 81 | 73 | 17-200 | 5-38 | 4-23 | 2 | 0 | 2 |
| 6 | @ JAX | 34 | 312 | 109 | 99 | 14-241 | 7-39 | 3-32 | 4 | 1 | 0 |
| 7 | vs NYG | 21 | 153 | 82 | 66 | 10-94 | 6-44 | 1-15 | 2 | 0 | 1 |
| 9 | @ LAC | 44 | 391 | 86 | 86 | 17-334 | 2-42 | 3-15 | 5 | 0 | 1 |
| 10 | @ CLE | 24 | 211 | 68 | 68 | 16-173 | 1-11 | 3-27 | 3 | 0 | 1 |
| 11 | vs IND | 26 | 194 | 137 | 140 | 10-138 | 6-43 | 5-13 | 2 | 2 | 1 |

**QB C.Stroud** (8 games): 166/252, 2029 yds, 20 TD, 4 INT, 11 sacks, 8.05 yds/att, depth of target 9.8, pressured on 10.6% of dropbacks. Yards by game: W3 167, W4 347, W5 261, W6 312, W7 153, W9 384, W10 211, W11 194.

**QB D.Mills** (1 games): 1/2, 7 yds, 0 TD, 0 INT, 0 sacks, 3.50 yds/att, depth of target 5.0, pressured on 0.0% of dropbacks. Yards by game: W9 7.

### HOU receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N.Collins | WR | 7 | 50 | 33 | 461 | 5 | 21% | 26% | 12.0 | 5 | 7 | 118 56 74 6 55 94 58 |
| X.Hutchinson | WR | 8 | 42 | 24 | 289 | 3 | 17% | 20% | 11.3 | 4 | 3 | 51 46 65 10 17 29 58 13 |
| D.Schultz | TE | 8 | 28 | 21 | 211 | 1 | 12% | 9% | 7.3 | 6 | 2 | 30 9 30 33 45 42 11 11 |
| K.Boutte | WR | 8 | 24 | 17 | 301 | 3 | 10% | 15% | 14.5 | 3 | 6 | 21 36 38 16 25 125 0 40 |
| T.Dell | WR | 4 | 18 | 11 | 196 | 1 | 7% | 9% | 11.6 | 1 | 4 | 43 105 21 27 |
| J.Noel | WR | 5 | 16 | 16 | 247 | 2 | 7% | 7% | 10.0 | 4 | 4 | 17 85 41 107 -3 |
| W.Marks | RB | 7 | 15 | 10 | 88 | 0 | 6% | 1% | 1.1 | 2 | 0 | 6 0 23 25 15 4 15 |
| F.Moreau | TE | 5 | 11 | 8 | 31 | 3 | 5% | 2% | 4.2 | 4 | 0 | 7 1 8 7 8 |
| M.Harrison | WR | 3 | 11 | 6 | 60 | 1 | 5% | 7% | 15.2 | 2 | 0 | 34 6 20 |

### HOU rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| W.Marks | RB | 7 | 90 | 341 | 3.79 | 2 | 48% | 18 | 0 | 15 22 62 56 66 70 50 |
| D.Montgomery | RB | 4 | 52 | 175 | 3.37 | 0 | 28% | 6 | 1 | 33 24 11 107 |
| E.Demercado | RB | 3 | 18 | 65 | 3.61 | 0 | 10% | 2 | 0 | 16 16 33 |
| C.Stroud | QB | 8 | 9 | 10 | 1.11 | 1 | 5% | 1 | 0 | 2 0 7 0 4 0 0 -3 |
| J.Jordan | RB | 1 | 6 | 43 | 7.17 | 1 | 3% | 2 | 1 | 43 |

### HOU run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 42 | 133 | 3.17 | 0 |
| right guard | 31 | 107 | 3.45 | 1 |
| right tackle | 29 | 117 | 4.03 | 0 |
| left guard | 24 | 74 | 3.08 | 0 |
| left tackle | 21 | 111 | 5.29 | 1 |
| right end | 21 | 81 | 3.86 | 0 |
| left end | 20 | 52 | 2.6 | 0 |

### HOU by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 309 | 66% | 73% | 6.39 | 0.138 |
| offense | Under center | 147 | 32% | 29% | 4.77 | -0.015 |
| offense | No huddle | 10 | 2% | 100% | 7.0 | -0.018 |
| defense vs | Shotgun | 331 | 64% | 76% | 5.27 | -0.033 |
| defense vs | Under center | 160 | 31% | 34% | 4.65 | -0.03 |
| defense vs | No huddle | 24 | 5% | 71% | 3.83 | 0.038 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 58 | 23% | 74% | 4.83 | 1 |
| offense | Short middle | 53 | 21% | 72% | 7.36 | 2 |
| offense | Short right | 86 | 34% | 71% | 6.6 | 4 |
| offense | Deep left | 12 | 5% | 8% | 4.33 | 1 |
| offense | Deep middle | 13 | 5% | 62% | 22.15 | 7 |
| offense | Deep right | 32 | 13% | 50% | 14.31 | 13 |
| defense allows | Short left | 85 | 30% | 73% | 5.35 | 3 |
| defense allows | Short middle | 49 | 17% | 57% | 6.88 | 5 |
| defense allows | Short right | 89 | 31% | 70% | 6.01 | 4 |
| defense allows | Deep left | 26 | 9% | 38% | 10.5 | 8 |
| defense allows | Deep middle | 17 | 6% | 47% | 13.82 | 4 |
| defense allows | Deep right | 18 | 6% | 28% | 7.56 | 5 |

### HOU lines (depth chart as of 2026-11-26T07:01:42Z)

Offensive line: LT Aireontae Ersery, LG Keylan Rutledge, C Evan Brown, RG Ed Ingram, RT Trent Brown.  
Defensive front: LDE Will Anderson Jr., LDT Tommy Togiai, RDT Sheldon Rankins, RDE Danielle Hunter, WLB Jake Hansen, SLB Wade Woodaz.

### HOU injuries

Official report not posted yet for this week.

ESPN live list (designations only): Keylan Rutledge (G) Questionable; Wyatt Teller (G) Questionable; Brevin Jordan (TE) Questionable; Logan Hall (DE) Doubtful; Jake Hummel (LB) Questionable; Woody Marks (RB) Questionable; Marvin Harrison Jr. (WR) Questionable; Kayshon Boutte (WR) Questionable; Danielle Hunter (DE) Questionable; Sheldon Rankins (DT) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### HOU roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Zaire Mitchell-Paden (TE) to CLE.

## PIT (last 8 games: weeks 3, 4, 5, 6, 7, 8, 10, 11)

### PIT defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 21.0 | 15/32 | 23.0 |
| Pass yards allowed / game | 266.9 | 27/32 | 235.6 |
| Yards per pass attempt allowed | 7.14 | 18/32 | 7.14 |
| Rush yards allowed / game | 61.6 | 1/32 | 99.5 |
| Yards per carry allowed | 3.16 | 1/32 | 4.07 |
| RB rush yards allowed / game | 60.1 | 2/32 | 92.5 |
| WR yards allowed / game | 168.0 | 26/32 | 147.8 |
| WR receptions allowed / game | 14.0 | 31/32 | 11.4 |
| TE yards allowed / game | 56.5 | 19/32 | 54.7 |
| TE receptions allowed / game | 5.2 | 16/32 | 5.3 |
| RB receiving yards allowed / game | 42.8 | 29/32 | 33.0 |
| RB receptions allowed / game | 6.0 | 31/32 | 4.4 |
| Explosive passes (20+) allowed / game | 3.38 | 23/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.62 | 2/32 | 1.21 |
| Sack rate | 6.9% | 14/32 | 6.6% |
| Pressure rate (sacks + hits) | 13.8% | 24/32 | 15.7% |
| Third-down conversions allowed | 35.6% | 11/32 | 39.2% |
| Red-zone TD rate allowed | 50.0% | 4/32 | 58.0% |
| Takeaways / game | 1.00 | 20/32 | 1.23 |

Blitz rate 28.8% and play-action faced 13.5% on 333 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.2 per game, 44.1% completed.

### PIT defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs CIN | 27 | 282 | 70 | 70 | 19-219 | 6-50 | 3-13 | 4 | 0 | 1 |
| 4 | @ CLE | 27 | 268 | 86 | 90 | 13-191 | 3-27 | 8-50 | 3 | 2 | 2 |
| 5 | vs IND | 22 | 267 | 66 | 61 | 10-126 | 10-101 | 4-40 | 5 | 1 | 1 |
| 6 | @ TB | 19 | 164 | 63 | 63 | 16-132 | 2-25 | 3-10 | 2 | 1 | 5 |
| 7 | @ NO | 10 | 278 | 12 | 11 | 16-179 | 4-20 | 10-79 | 2 | 0 | 2 |
| 8 | vs CLE | 6 | 326 | 32 | 32 | 10-77 | 11-163 | 8-86 | 4 | 0 | 8 |
| 10 | @ CIN | 38 | 409 | 70 | 70 | 18-317 | 5-28 | 12-64 | 5 | 0 | 1 |
| 11 | @ PHI | 19 | 141 | 94 | 84 | 10-103 | 1-38 | 0-0 | 2 | 1 | 3 |

### Best individual lines allowed by PIT

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | CIN | J.Chase (WR) 9/12 for 98, 1 TD | C.Brown (RB) 13 for 61, 0 TD |
| 4 | CLE | D.Boston (WR) 4/7 for 89, 0 TD | Q.Judkins (RB) 17 for 53, 1 TD |
| 5 | IND | T.Warren (TE) 7/9 for 83, 0 TD | J.Taylor (RB) 15 for 45, 0 TD |
| 6 | TB | E.Egbuka (WR) 7/16 for 48, 1 TD | B.Irving (RB) 19 for 46, 0 TD |
| 7 | NO | B.Brown (WR) 3/3 for 57, 0 TD | K.Miller (RB) 8 for 6, 0 TD |
| 8 | CLE | H.Fannin (TE) 10/12 for 154, 0 TD | Q.Judkins (RB) 11 for 25, 0 TD |
| 10 | CIN | J.Chase (WR) 11/14 for 231, 0 TD | C.Brown (RB) 10 for 44, 0 TD |
| 11 | PHI | D.Cooper (WR) 4/5 for 59, 0 TD | S.Barkley (RB) 17 for 75, 1 TD |

### PIT run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 39 | 77 | 1.97 | 0 |
| left tackle | 30 | 85 | 2.83 | 1 |
| left guard | 25 | 73 | 2.92 | 0 |
| right tackle | 20 | 41 | 2.05 | 0 |
| right guard | 20 | 70 | 3.5 | 0 |
| left end | 12 | 90 | 7.5 | 1 |
| right end | 10 | 57 | 5.7 | 1 |

### PIT defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Jamel Dean | 7 | 51 | 29 | 302 | 5.9 | 0 | 1 | 3 |
| Jalen Ramsey | 8 | 49 | 30 | 252 | 5.1 | 5 | 0 | 2 |
| Payton Wilson | 8 | 47 | 30 | 241 | 5.1 | 1 | 1 | 6 |
| Asante Samuel Jr. | 8 | 43 | 20 | 317 | 7.4 | 2 | 0 | 2 |
| Patrick Queen | 8 | 43 | 25 | 222 | 5.2 | 0 | 0 | 4 |
| Jaquan Brisker | 8 | 40 | 20 | 299 | 7.5 | 1 | 0 | 7 |
| Daylen Everette | 8 | 34 | 19 | 283 | 8.3 | 1 | 1 | 0 |
| Robert Spears-Jennings | 7 | 21 | 12 | 137 | 6.5 | 0 | 1 | 2 |
| Alex Highsmith | 7 | 5 | 5 | 31 | 6.2 | 1 | 0 | 1 |
| Nick Herbig | 6 | 4 | 4 | 45 | 11.2 | 0 | 0 | 4 |

### PIT pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| T.J. Watt | 7 | 10 | 4.0 | 2 | 1 |
| Alex Highsmith | 7 | 9 | 2.5 | 3 | 5 |
| Cameron Heyward | 6 | 9 | 2.5 | 2 | 0 |
| Nick Herbig | 6 | 5 | 3.0 | 1 | 3 |
| Keeanu Benton | 7 | 5 | 0.5 | 1 | 0 |
| Patrick Queen | 8 | 5 | 3.5 | 0 | 26 |
| Yahya Black | 3 | 3 | 1.0 | 0 | 0 |
| Payton Wilson | 8 | 3 | 1.0 | 1 | 16 |

### PIT offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 23.9 | 13/32 | 23.2 |
| Pass yards / game | 229.4 | 19/32 | 234.2 |
| Yards per pass attempt | 6.53 | 22/32 | 7.12 |
| Rush yards / game | 115.2 | 9/32 | 100.6 |
| Yards per carry | 5.21 | 1/32 | 4.10 |
| RB rush yards / game | 110.5 | 8/32 | 93.4 |
| WR yards / game | 125.4 | 23/32 | 147.5 |
| TE yards / game | 61.1 | 11/32 | 53.4 |
| RB receiving yards / game | 42.9 | 8/32 | 33.2 |
| Explosive passes (20+) / game | 3.12 | 17/32 | 2.96 |
| Explosive runs (15+) / game | 1.62 | 5/32 | 1.23 |
| Sack rate allowed | 8.0% | 25/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 15.7% | 17/32 | 15.4% |
| Third-down conversion rate | 40.7% | 14/32 | 39.4% |
| Red-zone TD rate | 46.2% | 29/32 | 58.9% |

Neutral-situation pass rate 59.6%; 61.2 plays per game; target share WR 55% / TE 24% / RB 20%.

### PIT offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs CIN | 30 | 292 | 128 | 127 | 10-144 | 6-99 | 3-49 | 5 | 2 | 2 |
| 4 | @ CLE | 24 | 299 | 92 | 92 | 13-222 | 6-44 | 3-33 | 5 | 1 | 5 |
| 5 | vs IND | 34 | 235 | 123 | 107 | 9-92 | 7-56 | 6-87 | 3 | 1 | 1 |
| 6 | @ TB | 26 | 253 | 90 | 90 | 22-180 | 6-36 | 5-37 | 0 | 2 | 5 |
| 7 | @ NO | 16 | 212 | 142 | 142 | 7-107 | 3-24 | 9-81 | 4 | 3 | 3 |
| 8 | vs CLE | 27 | 172 | 200 | 199 | 7-43 | 5-129 | 1-0 | 3 | 4 | 1 |
| 10 | @ CIN | 18 | 145 | 94 | 84 | 5-69 | 3-40 | 8-36 | 3 | 0 | 3 |
| 11 | @ PHI | 16 | 227 | 53 | 43 | 16-146 | 8-61 | 6-20 | 2 | 0 | 5 |

**QB A.Rodgers** (8 games): 173/278, 1833 yds, 15 TD, 5 INT, 25 sacks, 6.59 yds/att, depth of target 7.3, pressured on 16.2% of dropbacks. Yards by game: W3 292, W4 299, W5 235, W6 253, W7 212, W8 172, W10 143, W11 227.

**QB M.Rudolph** (1 games): 1/3, 2 yds, 0 TD, 0 INT, 0 sacks, 0.67 yds/att, depth of target 3.7, pressured on 0.0% of dropbacks. Yards by game: W10 2.

### PIT receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D.Metcalf | WR | 8 | 55 | 28 | 367 | 2 | 21% | 39% | 13.6 | 5 | 6 | 31 115 12 93 56 4 54 2 |
| G.Bernard | WR | 8 | 47 | 34 | 289 | 1 | 18% | 14% | 5.9 | 9 | 3 | 14 11 80 87 27 30 0 40 |
| J.Warren | RB | 8 | 35 | 25 | 260 | 1 | 13% | -3% | -1.6 | 3 | 3 | 49 33 87 28 36 0 26 1 |
| P.Freiermuth | TE | 8 | 33 | 23 | 231 | 4 | 12% | 15% | 8.5 | 5 | 3 | 30 17 44 11 20 35 35 39 |
| D.Washington | TE | 8 | 30 | 20 | 256 | 3 | 11% | 9% | 5.7 | 7 | 4 | 67 27 12 25 4 94 5 22 |
| R.Wilson | WR | 4 | 19 | 9 | 177 | 2 | 7% | 17% | 17.1 | 3 | 3 | 60 74 0 43 |
| R.Dowdle | RB | 4 | 17 | 15 | 81 | 0 | 6% | -2% | -2.4 | 2 | 0 | 9 45 8 19 |
| M.Pittman | WR | 2 | 9 | 4 | 31 | 0 | 3% | 4% | 8.9 | 0 | 0 | 16 15 |
| M.Hurleman | WR | 1 | 7 | 6 | 61 | 1 | 3% | 4% | 10.6 | 2 | 1 | 61 |

### PIT rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| J.Warren | RB | 8 | 114 | 658 | 5.77 | 2 | 64% | 11 | 10 | 127 93 101 50 101 143 15 28 |
| R.Dowdle | RB | 5 | 41 | 178 | 4.34 | 1 | 23% | 8 | 3 | 40 41 56 26 15 |
| L.Nichols | RB | 3 | 8 | 49 | 6.12 | 0 | 5% | 2 | 0 | 0 6 43 |
| T.Homer | RB | 3 | 4 | -1 | -0.25 | 0 | 2% | 3 | 0 | 0 -1 0 |
| P.Freiermuth | TE | 4 | 4 | 4 | 1.00 | 1 | 2% | 1 | 0 | 1 1 1 1 |

### PIT run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 48 | 307 | 6.4 | 5 |
| left guard | 30 | 165 | 5.5 | 2 |
| left tackle | 25 | 93 | 3.72 | 0 |
| right guard | 23 | 101 | 4.39 | 2 |
| left end | 22 | 127 | 5.77 | 2 |
| right tackle | 17 | 58 | 3.41 | 1 |
| right end | 10 | 64 | 6.4 | 1 |

### PIT by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 291 | 59% | 81% | 5.49 | 0.038 |
| offense | Under center | 161 | 33% | 30% | 5.11 | 0.043 |
| offense | No huddle | 38 | 8% | 74% | 5.08 | 0.094 |
| defense vs | Shotgun | 370 | 76% | 76% | 5.67 | 0.006 |
| defense vs | Under center | 81 | 17% | 21% | 3.12 | -0.103 |
| defense vs | No huddle | 38 | 8% | 90% | 6.16 | 0.267 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 76 | 27% | 67% | 5.54 | 4 |
| offense | Short middle | 55 | 20% | 76% | 7.35 | 3 |
| offense | Short right | 96 | 34% | 68% | 5.57 | 3 |
| offense | Deep left | 19 | 7% | 37% | 11.26 | 7 |
| offense | Deep middle | 10 | 4% | 40% | 11.5 | 3 |
| offense | Deep right | 25 | 9% | 20% | 5.84 | 5 |
| defense allows | Short left | 113 | 38% | 77% | 6.18 | 5 |
| defense allows | Short middle | 55 | 18% | 74% | 7.56 | 2 |
| defense allows | Short right | 88 | 29% | 64% | 4.82 | 2 |
| defense allows | Deep left | 21 | 7% | 38% | 12.33 | 8 |
| defense allows | Deep middle | 7 | 2% | 43% | 13.0 | 2 |
| defense allows | Deep right | 15 | 5% | 53% | 16.47 | 8 |

### PIT lines (depth chart as of 2026-11-26T07:01:42Z)

Offensive line: LT Troy Fautanu, LG Spencer Anderson, C Zach Frazier, RG Brock Hoffman, RT Max Iheanachor.  
Defensive front: LDE Derrick Harmon, NT Keeanu Benton, RDE Cameron Heyward, WLB T.J. Watt, SLB Alex Highsmith.

### PIT injuries

Official report not posted yet for this week.

ESPN live list (designations only): Alex Highsmith (LB) Doubtful; Ben Skowronek (WR) Questionable; Nick Herbig (LB) Questionable; Gennings Dunker (G) Injured Reserve; Cole Holcomb (LB) Questionable; Michael Pittman Jr. (WR) Injured Reserve; DeShon Elliott (S) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### PIT roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Terell Smith (DB) to ATL.

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
| games | OK | 2026-11-26T11:17:03+00:00 | d8fca4cae777 |
| pbp | OK | 2026-11-26T11:17:03+00:00 | f530660deb4f |
| rosters | OK | 2026-11-26T11:17:03+00:00 | 78bcb0df4af5 |
| injuries | OK | 2026-11-26T11:17:03+00:00 | 1540681821fb |
| depth_charts | OK | 2026-11-26T11:17:04+00:00 | f6eec5e5e059 |
| snap_counts | OK | 2026-11-26T11:17:04+00:00 | ef0897b31ad5 |
| ftn | OK | 2026-11-26T11:17:04+00:00 | ee09d5f28f5f |
| pfr_def | OK | 2026-11-26T11:17:04+00:00 | c4251b1fd2fa |
| pfr_rec | OK | 2026-11-26T11:17:04+00:00 | 8f0fd28d26e7 |
| pfr_rush | OK | 2026-11-26T11:17:04+00:00 | b0d1aa83f4d1 |
| ngs_receiving | OK | 2026-11-26T11:17:04+00:00 | be5f07804748 |
| ngs_rushing | OK | 2026-11-26T11:17:05+00:00 | 66aedd0a8d42 |
| ngs_passing | OK | 2026-11-26T11:17:05+00:00 | b88e8dfa5fb8 |
| espn_injuries | OK | 2026-11-26T11:17:06+00:00 |  |
| nfl_savant | SAME_DATA_AS_NFLVERSE_PBP: its season download is the nflverse play-by-play (checked 2026-11-11), so no second download is made |  |  |
| book_odds | NO_KEY: set the ODDS_API_KEY repository secret to include book prices |  |  |

Play-by-play, rosters, injuries, depth charts, snap counts and PFR advanced defense: nflverse (github.com/nflverse/nflverse-data). FTN charting via nflverse: FTN Data, CC-BY-SA 4.0. Third-party data keep their own terms; see SOURCES.md.
