# LAC at TB: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: outdoors; surface: grass. Rest: LAC 7 days, TB 6 days. Listed QBs: Justin Herbert (LAC), Baker Mayfield (TB).

Market (schedule consensus, not a timestamped quote): TB -5.5, total 40.5.

Generated 2026-11-27T18:39:03+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-27T18:32:28Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | TB -5.5 | -116 | -104 | 51.3% | 48.7% | 4.7% | 2026-11-27T18:32:28+00:00 |
| total | fanduel | Over 40.5 | -115 | -105 | 51.1% | 48.9% | 4.7% | 2026-11-27T18:32:28+00:00 |
| moneyline | fanduel | TB | -270 | +220 | 70.0% | 30.0% | 4.2% | 2026-11-27T18:32:28+00:00 |

Player props: OK.

## Matchup edges

### LAC offense vs TB defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| TB DEFENCE WEAK SPOT | tight end yards | 36.1 | 59.5 | 54.3 | LAC offence ranks 25 of 32, TB defence ranks 24 of 32 (1 = best at its own job) |
| TB DEFENCE ADVANTAGE | explosive passes (20+) | 2.2 | 2.4 | 3.0 | LAC offence ranks 24 of 32, TB defence ranks 5 of 32 (1 = best at its own job) |
| LAC OFFENCE WEAK SPOT | passing yards | 184.2 | 228.4 | 235.6 | LAC offence ranks 29 of 32, TB defence ranks 14 of 32 (1 = best at its own job) |
| TB DEFENCE ADVANTAGE | points | 17.5 | 19.1 | 23.3 | LAC offence ranks 28 of 32, TB defence ranks 6 of 32 (1 = best at its own job) |
| TB DEFENCE ADVANTAGE | third-down conversions | 35.9% | 34.4% | 39.2% | LAC offence ranks 25 of 32, TB defence ranks 9 of 32 (1 = best at its own job) |
| TB DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 11.5% | 5.1% | 6.7% | LAC offence ranks 32 of 32, TB defence ranks 25 of 32 (1 = best at its own job) |
| TB DEFENCE WEAK SPOT | pressure (sacks + hits) | 19.8% | 12.3% | 15.7% | LAC offence ranks 31 of 32, TB defence ranks 30 of 32 (1 = best at its own job) |

### TB offense vs LAC defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| TB OFFENCE WEAK SPOT | wide receiver yards | 98.6 | 146.2 | 147.7 | TB offence ranks 31 of 32, LAC defence ranks 17 of 32 (1 = best at its own job) |
| TB OFFENCE WEAK SPOT | tight end yards | 22.6 | 56.8 | 54.3 | TB offence ranks 32 of 32, LAC defence ranks 19 of 32 (1 = best at its own job) |
| TB OFFENCE ADVANTAGE | running back rushing yards | 141.9 | 107.6 | 93.5 | TB offence ranks 2 of 32, LAC defence ranks 23 of 32 (1 = best at its own job) |
| LAC DEFENCE ADVANTAGE | explosive passes (20+) | 1.5 | 2.8 | 3.0 | TB offence ranks 32 of 32, LAC defence ranks 8 of 32 (1 = best at its own job) |
| TB OFFENCE STRENGTH | explosive runs (15+) | 1.8 | 1.4 | 1.2 | TB offence ranks 2 of 32, LAC defence ranks 18 of 32 (1 = best at its own job) |
| TB OFFENCE WEAK SPOT | passing yards | 151.5 | 228.9 | 235.6 | TB offence ranks 32 of 32, LAC defence ranks 15 of 32 (1 = best at its own job) |
| LAC DEFENCE WEAK SPOT | points | 22.1 | 26.8 | 23.3 | TB offence ranks 20 of 32, LAC defence ranks 25 of 32 (1 = best at its own job) |
| LAC DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 9.3% | 5.1% | 6.7% | TB offence ranks 29 of 32, LAC defence ranks 26 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | LAC 21.4 - TB 22.5 | 44.0 | +1.1 | 50.0% | 32.0% | 57.5% | LAC 10.9 - TB 11.6 |
| independent | LAC 19.8 - TB 22.5 | 42.3 | +2.7 | 58.2% | 39.5% | 55.9% | LAC 9.8 - TB 11.2 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### LAC offense vs TB defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T.Harris | WR | receiving yards | 7 | 41.1 | 0.986 | 8.9 | 11.8 | 14.8 | 18.1 | 21.7 | 30.6 |
| T.Harris | WR | receptions | 7 | 3.3 | 1.001 | 2.0 | 2.0 | 2.0 | 2.2 | 2.5 | 3.0 |
| O.Gadsden | TE | receiving yards | 7 | 19.9 | 1.048 | 0.0 | 0.0 | 0.0 | 1.5 | 3.7 | 17.8 |
| O.Gadsden | TE | receptions | 7 | 2.2 | 0.97 | 0.0 | 0.0 | 0.0 | 0.2 | 0.5 | 1.9 |
| K.Mitchell | RB | receiving yards | 8 | 10.4 | 0.878 | -2.9 | -1.3 | 0.0 | 0.0 | 0.0 | 10.1 |
| K.Mitchell | RB | receptions | 8 | 1.9 | 0.92 | 0.0 | 0.0 | 0.0 | 0.4 | 0.7 | 2.8 |
| Q.Johnston | WR | receiving yards | 7 | 32.7 | 0.986 | 6.8 | 7.7 | 8.6 | 14.4 | 22.7 | 39.4 |
| Q.Johnston | WR | receptions | 7 | 1.6 | 1.001 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| L.McConkey | WR | receiving yards | 5 | 41.5 | 0.986 | 3.4 | 6.7 | 10.1 | 13.4 | 16.8 | 36.5 |
| L.McConkey | WR | receptions | 5 | 3.0 | 1.001 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 | 4.0 |
| C.Kolar | TE | receiving yards | 6 | 21.4 | 1.048 | 10.5 | 12.6 | 14.7 | 16.8 | 17.8 | 21.0 |
| C.Kolar | TE | receptions | 6 | 2.0 | 0.97 | 1.0 | 1.0 | 1.0 | 1.0 | 1.2 | 2.4 |
| K.Vidal | RB | receiving yards | 8 | 9.9 | 0.878 | 1.3 | 3.4 | 5.3 | 5.6 | 5.9 | 11.0 |
| K.Vidal | RB | receptions | 8 | 1.6 | 0.92 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 1.8 |
| O.Hampton | RB | rushing yards | 8 | 50.9 | 0.895 | 16.7 | 17.4 | 18.5 | 22.6 | 26.6 | 45.2 |
| K.Vidal | RB | rushing yards | 8 | 22.2 | 0.895 | 1.9 | 3.8 | 6.0 | 10.7 | 15.4 | 21.5 |
| K.Mitchell | RB | rushing yards | 7 | 16.8 | 0.895 | 3.6 | 3.6 | 3.6 | 3.9 | 4.5 | 9.8 |
| J.Herbert | QB | passing yards | 8 | 174.4 | 0.985 | 121.9 | 124.7 | 127.1 | 127.8 | 128.5 | 188.1 |

### TB offense vs LAC defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E.Egbuka | WR | receiving yards | 6 | 34.5 | 0.995 | 14.2 | 15.4 | 16.7 | 17.9 | 22.9 | 37.8 |
| E.Egbuka | WR | receptions | 6 | 4.0 | 0.979 | 2.0 | 2.0 | 2.0 | 2.0 | 2.2 | 3.9 |
| C.Godwin | WR | receiving yards | 8 | 21.5 | 0.995 | 4.5 | 9.1 | 13.1 | 14.1 | 15.2 | 25.9 |
| C.Godwin | WR | receptions | 8 | 2.9 | 0.979 | 0.7 | 1.4 | 2.0 | 2.3 | 2.7 | 2.9 |
| C.Otton | TE | receiving yards | 7 | 19.5 | 1.023 | 1.2 | 2.5 | 3.7 | 4.9 | 6.1 | 25.6 |
| C.Otton | TE | receptions | 7 | 2.0 | 0.923 | 0.3 | 0.6 | 0.8 | 0.9 | 0.9 | 2.8 |
| T.Hurst | WR | receiving yards | 7 | 22.2 | 0.995 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 24.9 |
| T.Hurst | WR | receptions | 7 | 1.6 | 0.979 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| K.Gainwell | RB | receiving yards | 7 | 21.8 | 0.884 | 1.9 | 3.7 | 5.6 | 6.7 | 7.5 | 12.4 |
| K.Gainwell | RB | receptions | 7 | 2.1 | 0.962 | 0.3 | 0.6 | 0.9 | 1.2 | 1.4 | 1.9 |
| B.Irving | RB | receiving yards | 6 | 14.6 | 0.884 | 2.9 | 3.1 | 3.3 | 3.5 | 4.9 | 9.7 |
| B.Irving | RB | receptions | 6 | 2.4 | 0.962 | 1.2 | 1.4 | 1.7 | 1.9 | 1.9 | 1.9 |
| T.Johnson | WR | receiving yards | 7 | 33.4 | 0.995 | 7.3 | 7.6 | 7.9 | 9.8 | 12.4 | 16.9 |
| T.Johnson | WR | receptions | 7 | 1.7 | 0.979 | 1.0 | 1.0 | 1.0 | 1.2 | 1.5 | 2.0 |
| B.Irving | RB | rushing yards | 8 | 104.6 | 1.075 | 49.5 | 49.5 | 50.3 | 55.9 | 61.6 | 88.7 |
| K.Gainwell | RB | rushing yards | 8 | 43.8 | 1.075 | -0.9 | 2.5 | 6.0 | 10.1 | 14.2 | 17.7 |
| S.Tucker | RB | rushing yards | 3 | 33.7 | 1.075 | 11.6 | 12.5 | 13.3 | 14.2 | 15.1 | 19.4 |
| B.Mayfield | QB | passing yards | 5 | 144.1 | 0.986 | 12.6 | 25.2 | 37.8 | 50.5 | 63.1 | 184.3 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## LAC (last 8 games: weeks 3, 4, 5, 6, 8, 9, 10, 11)

### LAC defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 26.8 | 25/32 | 23.3 |
| Pass yards allowed / game | 228.9 | 15/32 | 235.6 |
| Yards per pass attempt allowed | 7.76 | 24/32 | 7.15 |
| Rush yards allowed / game | 117.8 | 26/32 | 100.5 |
| Yards per carry allowed | 4.40 | 24/32 | 4.10 |
| RB rush yards allowed / game | 107.6 | 23/32 | 93.5 |
| WR yards allowed / game | 146.2 | 17/32 | 147.7 |
| WR receptions allowed / game | 10.9 | 15/32 | 11.4 |
| TE yards allowed / game | 56.8 | 19/32 | 54.3 |
| TE receptions allowed / game | 4.5 | 5/32 | 5.3 |
| RB receiving yards allowed / game | 25.8 | 8/32 | 33.5 |
| RB receptions allowed / game | 4.1 | 11/32 | 4.5 |
| Explosive passes (20+) allowed / game | 2.75 | 8/32 | 2.97 |
| Explosive runs (15+) allowed / game | 1.38 | 18/32 | 1.22 |
| Sack rate | 5.1% | 26/32 | 6.7% |
| Pressure rate (sacks + hits) | 14.8% | 19/32 | 15.7% |
| Third-down conversions allowed | 40.4% | 17/32 | 39.2% |
| Red-zone TD rate allowed | 58.1% | 17/32 | 58.5% |
| Takeaways / game | 1.50 | 7/32 | 1.22 |

Blitz rate 23.3% and play-action faced 24.9% on 257 charted dropbacks (FTN). Deep passes (20+ air yards) faced 2.8 per game, 50.0% completed.

### LAC defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ BUF | 24 | 204 | 169 | 154 | 8-110 | 3-43 | 4-50 | 3 | 3 | 4 |
| 4 | @ SEA | 30 | 168 | 132 | 99 | 8-115 | 1-12 | 4-41 | 4 | 3 | 3 |
| 5 | vs DEN | 23 | 123 | 105 | 84 | 9-67 | 4-55 | 3-1 | 1 | 0 | 1 |
| 6 | @ KC | 22 | 272 | 144 | 134 | 12-137 | 7-106 | 4-29 | 3 | 2 | 0 |
| 8 | @ LA | 24 | 157 | 129 | 129 | 13-132 | 3-22 | 1-3 | 1 | 1 | 1 |
| 9 | vs HOU | 44 | 391 | 86 | 86 | 17-334 | 2-42 | 3-15 | 5 | 0 | 1 |
| 10 | @ BAL | 20 | 340 | 16 | 14 | 12-177 | 11-119 | 10-44 | 4 | 0 | 2 |
| 11 | vs NYJ | 27 | 176 | 161 | 161 | 8-98 | 5-55 | 4-23 | 1 | 2 | 1 |

### Best individual lines allowed by LAC

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | BUF | D.Moore (WR) 6/10 for 67, 0 TD | J.Cook (RB) 24 for 154, 1 TD |
| 4 | SEA | J.Smith-Njigba (WR) 5/6 for 76, 0 TD | E.Wilson (RB) 21 for 81, 1 TD |
| 5 | DEN | E.Engram (TE) 4/4 for 55, 0 TD | J.Dobbins (RB) 18 for 68, 1 TD |
| 6 | KC | X.Worthy (WR) 7/7 for 73, 0 TD | K.Walker (RB) 19 for 128, 2 TD |
| 8 | LA | P.Nacua (WR) 11/12 for 80, 1 TD | B.Corum (RB) 11 for 73, 1 TD |
| 9 | HOU | K.Boutte (WR) 4/5 for 125, 2 TD | W.Marks (RB) 18 for 70, 0 TD |
| 10 | BAL | M.Andrews (TE) 8/8 for 82, 0 TD | D.Henry (RB) 10 for 10, 2 TD |
| 11 | NYJ | G.Wilson (WR) 3/5 for 39, 0 TD | B.Hall (RB) 20 for 86, 0 TD |

### LAC run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 81 | 357 | 4.41 | 4 |
| left guard | 29 | 105 | 3.62 | 0 |
| right tackle | 24 | 85 | 3.54 | 0 |
| right end | 23 | 72 | 3.13 | 0 |
| left end | 19 | 151 | 7.95 | 3 |
| left tackle | 19 | 98 | 5.16 | 3 |
| right guard | 19 | 74 | 3.89 | 1 |

### LAC defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Tarheeb Still | 7 | 35 | 22 | 250 | 7.1 | 3 | 1 | 4 |
| Daiyan Henley | 7 | 28 | 23 | 202 | 7.2 | 0 | 1 | 2 |
| Cam Hart | 8 | 26 | 14 | 209 | 8.0 | 0 | 1 | 2 |
| Genesis Smith | 7 | 21 | 11 | 157 | 7.5 | 2 | 2 | 2 |
| Tony Jefferson | 8 | 18 | 13 | 152 | 8.4 | 0 | 0 | 5 |
| Elijah Molden | 7 | 16 | 13 | 221 | 13.8 | 1 | 0 | 1 |
| Del'Shawn Phillips | 8 | 16 | 13 | 99 | 6.2 | 1 | 1 | 3 |
| Donte Jackson | 5 | 12 | 8 | 155 | 12.9 | 4 | 0 | 2 |
| Isas Waxter | 3 | 10 | 5 | 9 | 0.9 | 0 | 0 | 0 |
| Deane Leonard | 4 | 9 | 6 | 74 | 8.2 | 0 | 0 | 0 |

### LAC pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Tuli Tuipulotu | 7 | 12 | 3.0 | 2 | 10 |
| Akheem Mesidor | 6 | 8 | 2.0 | 1 | 1 |
| Khalil Mack | 5 | 7 | 2.0 | 3 | 5 |
| Teair Tart | 6 | 4 | 0.0 | 0 | 0 |
| Troy Dye | 6 | 4 | 2.0 | 2 | 6 |
| Daiyan Henley | 7 | 4 | 0.0 | 3 | 19 |
| Dalvin Tomlinson | 3 | 3 | 2.0 | 0 | 0 |
| Justin Eboigbe | 2 | 2 | 0.5 | 0 | 0 |

### LAC offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 17.5 | 28/32 | 23.3 |
| Pass yards / game | 184.2 | 29/32 | 234.4 |
| Yards per pass attempt | 6.52 | 23/32 | 7.13 |
| Rush yards / game | 104.9 | 14/32 | 101.0 |
| Yards per carry | 4.07 | 17/32 | 4.11 |
| RB rush yards / game | 96.6 | 15/32 | 93.8 |
| WR yards / game | 115.2 | 27/32 | 147.6 |
| TE yards / game | 36.1 | 25/32 | 53.3 |
| RB receiving yards / game | 32.9 | 16/32 | 33.4 |
| Explosive passes (20+) / game | 2.25 | 24/32 | 2.98 |
| Explosive runs (15+) / game | 1.50 | 8/32 | 1.22 |
| Sack rate allowed | 11.5% | 32/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 19.8% | 31/32 | 15.4% |
| Third-down conversion rate | 35.9% | 25/32 | 39.4% |
| Red-zone TD rate | 50.0% | 25/32 | 58.9% |

Neutral-situation pass rate 40.1%; 61.8 plays per game; target share WR 47% / TE 24% / RB 28%.

### LAC offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ BUF | 16 | 226 | 122 | 114 | 13-182 | 0-0 | 7-44 | 5 | 1 | 2 |
| 4 | @ SEA | 23 | 189 | 110 | 109 | 5-110 | 5-36 | 9-43 | 3 | 3 | 4 |
| 5 | vs DEN | 17 | 121 | 125 | 101 | 5-54 | 4-44 | 5-23 | 0 | 2 | 5 |
| 6 | @ KC | 6 | 204 | 54 | 43 | 9-127 | 6-37 | 7-40 | 1 | 0 | 4 |
| 8 | @ LA | 9 | 257 | 53 | 49 | 11-154 | 6-72 | 7-31 | 4 | 0 | 2 |
| 9 | vs HOU | 22 | 217 | 131 | 123 | 6-129 | 5-48 | 4-40 | 2 | 1 | 8 |
| 10 | @ BAL | 23 | 129 | 109 | 109 | 6-92 | 3-23 | 3-14 | 2 | 3 | 2 |
| 11 | vs NYJ | 24 | 131 | 135 | 125 | 8-74 | 3-29 | 4-28 | 1 | 2 | 6 |

**QB J.Herbert** (8 games): 139/218, 1450 yds, 6 TD, 8 INT, 33 sacks, 6.65 yds/att, depth of target 6.7, pressured on 22.3% of dropbacks. Yards by game: W3 226, W4 189, W5 121, W6 204, W8 257, W9 193, W10 129, W11 131.

**QB D.Uiagalelei** (1 games): 2/7, 24 yds, 1 TD, 0 INT, 0 sacks, 3.43 yds/att, depth of target 7.0, pressured on 0.0% of dropbacks. Yards by game: W9 24.

### LAC receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T.Harris | WR | 7 | 33 | 24 | 303 | 0 | 15% | 23% | 10.8 | 4 | 7 | 76 60 16 31 6 86 28 |
| O.Gadsden | TE | 7 | 26 | 16 | 129 | 0 | 12% | 12% | 7.2 | 5 | 0 | 0 36 0 17 52 17 7 |
| K.Mitchell | RB | 8 | 23 | 18 | 94 | 1 | 11% | 0% | 0.0 | 2 | 0 | -5 24 18 0 17 34 0 6 |
| Q.Johnston | WR | 7 | 22 | 12 | 251 | 1 | 10% | 22% | 15.4 | 1 | 5 | 40 44 57 37 58 6 9 |
| L.McConkey | WR | 5 | 22 | 14 | 206 | 2 | 10% | 15% | 10.7 | 2 | 3 | 66 0 17 86 37 |
| C.Kolar | TE | 6 | 21 | 13 | 132 | 0 | 10% | 7% | 5.3 | 2 | 1 | 37 20 20 31 16 8 |
| K.Vidal | RB | 8 | 21 | 14 | 88 | 1 | 10% | -1% | -0.6 | 2 | 0 | 14 11 -1 19 7 6 14 18 |
| O.Hampton | RB | 7 | 14 | 11 | 46 | 0 | 6% | -1% | -1.1 | 0 | 0 | 0 8 6 21 7 0 4 |
| K.Lambert-Smith | WR | 2 | 13 | 6 | 82 | 0 | 6% | 10% | 11.5 | 2 | 1 | 32 50 |

### LAC rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| O.Hampton | RB | 8 | 103 | 426 | 4.14 | 2 | 50% | 19 | 5 | 56 45 33 18 20 60 105 89 |
| K.Vidal | RB | 8 | 45 | 198 | 4.40 | 1 | 22% | 3 | 2 | 6 25 57 21 23 30 0 36 |
| K.Mitchell | RB | 7 | 40 | 149 | 3.73 | 0 | 19% | 3 | 2 | 52 39 11 4 6 33 4 |
| J.Herbert | QB | 8 | 12 | 55 | 4.58 | 1 | 6% | 3 | 1 | 8 3 24 7 4 0 0 9 |
| Q.Johnston | WR | 3 | 3 | 2 | 0.67 | 0 | 1% | 0 | 0 | -4 5 1 |

### LAC run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 53 | 162 | 3.06 | 1 |
| left end | 40 | 152 | 3.8 | 2 |
| right end | 38 | 146 | 3.84 | 2 |
| right guard | 21 | 127 | 6.05 | 3 |
| left guard | 21 | 65 | 3.1 | 0 |
| left tackle | 19 | 99 | 5.21 | 1 |
| right tackle | 14 | 88 | 6.29 | 1 |

### LAC by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 307 | 62% | 69% | 4.85 | -0.126 |
| offense | Under center | 163 | 33% | 32% | 4.63 | -0.054 |
| offense | No huddle | 24 | 5% | 92% | 2.46 | -0.643 |
| defense vs | Shotgun | 269 | 57% | 72% | 6.51 | 0.074 |
| defense vs | Under center | 181 | 38% | 30% | 4.48 | -0.052 |
| defense vs | No huddle | 21 | 4% | 38% | 8.62 | 0.438 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 56 | 25% | 71% | 5.39 | 1 |
| offense | Short middle | 40 | 18% | 70% | 6.5 | 0 |
| offense | Short right | 96 | 42% | 62% | 4.9 | 5 |
| offense | Deep left | 9 | 4% | 44% | 16.33 | 3 |
| offense | Deep middle | 6 | 3% | 33% | 6.17 | 1 |
| offense | Deep right | 19 | 8% | 42% | 13.58 | 8 |
| defense allows | Short left | 62 | 26% | 73% | 6.18 | 2 |
| defense allows | Short middle | 56 | 24% | 68% | 7.43 | 2 |
| defense allows | Short right | 80 | 34% | 69% | 5.79 | 3 |
| defense allows | Deep left | 8 | 3% | 25% | 9.25 | 2 |
| defense allows | Deep middle | 10 | 4% | 50% | 15.7 | 4 |
| defense allows | Deep right | 20 | 8% | 60% | 16.9 | 9 |

### LAC lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Joe Alt, LG Logan Taylor, C Jake Slaughter, RG Kayode Awosika, RT Travis Burke.  
Defensive front: LDE Teair Tart, NT Jamaree Caldwell, RDE Justin Eboigbe, WLB Tuli Tuipulotu, SLB Khalil Mack.

### LAC injuries

Official report not posted yet for this week.

ESPN live list (designations only): Kendall Williamson (S) Questionable; Keaton Mitchell (RB) Questionable; Daiyan Henley (LB) Questionable; Tarheeb Still (CB) Questionable; Dalvin Tomlinson (DT) Questionable; Brenen Thompson (WR) Questionable; Tuli Tuipulotu (LB) Questionable; Akheem Mesidor (LB) Questionable; Deane Leonard (CB) Injured Reserve; Justin Herbert (QB) Questionable; David Njoku (TE) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### LAC roster moves (last 4 weeks)

Arrived: Avery Smith (DB) from SEA.  
Left for another team: Hayden Rucci (TE) to PHI; Gregory Desrosiers (RB) to NYG.

## TB (last 8 games: weeks 3, 4, 5, 6, 7, 8, 9, 11)

### TB defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 19.1 | 6/32 | 23.3 |
| Pass yards allowed / game | 228.4 | 14/32 | 235.6 |
| Yards per pass attempt allowed | 6.82 | 13/32 | 7.15 |
| Rush yards allowed / game | 76.5 | 7/32 | 100.5 |
| Yards per carry allowed | 3.75 | 9/32 | 4.10 |
| RB rush yards allowed / game | 73.9 | 8/32 | 93.5 |
| WR yards allowed / game | 143.5 | 16/32 | 147.7 |
| WR receptions allowed / game | 11.4 | 17/32 | 11.4 |
| TE yards allowed / game | 59.5 | 24/32 | 54.3 |
| TE receptions allowed / game | 5.0 | 11/32 | 5.3 |
| RB receiving yards allowed / game | 25.4 | 7/32 | 33.5 |
| RB receptions allowed / game | 3.8 | 7/32 | 4.5 |
| Explosive passes (20+) allowed / game | 2.38 | 5/32 | 2.97 |
| Explosive runs (15+) allowed / game | 1.00 | 11/32 | 1.22 |
| Sack rate | 5.1% | 25/32 | 6.7% |
| Pressure rate (sacks + hits) | 12.3% | 30/32 | 15.7% |
| Third-down conversions allowed | 34.4% | 9/32 | 39.2% |
| Red-zone TD rate allowed | 61.1% | 20/32 | 58.5% |
| Takeaways / game | 2.25 | 2/32 | 1.22 |

Blitz rate 41.8% and play-action faced 24.0% on 292 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.5 per game, 42.9% completed.

### TB defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs MIN | 23 | 168 | 61 | 61 | 8-123 | 2-11 | 5-34 | 3 | 0 | 3 |
| 4 | vs GB | 17 | 197 | 98 | 85 | 7-66 | 9-90 | 6-41 | 1 | 2 | 0 |
| 5 | @ DAL | 16 | 316 | 50 | 50 | 18-271 | 4-28 | 2-17 | 5 | 1 | 0 |
| 6 | vs PIT | 26 | 253 | 90 | 90 | 22-180 | 6-36 | 5-37 | 0 | 2 | 5 |
| 7 | @ CAR | 13 | 210 | 64 | 64 | 7-69 | 4-97 | 6-44 | 2 | 1 | 5 |
| 8 | vs ATL | 0 | 125 | 92 | 88 | 4-107 | 3-15 | 1-3 | 1 | 1 | 0 |
| 9 | @ CHI | 27 | 279 | 56 | 56 | 16-202 | 6-77 | 0-0 | 4 | 0 | 1 |
| 11 | @ DET | 31 | 279 | 101 | 97 | 9-130 | 6-122 | 5-27 | 3 | 1 | 1 |

### Best individual lines allowed by TB

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | MIN | J.Addison (WR) 5/9 for 90, 1 TD | A.Jones (RB) 17 for 58, 0 TD |
| 4 | GB | C.Watson (WR) 3/3 for 47, 0 TD | K.Johnson (RB) 8 for 42, 0 TD |
| 5 | DAL | G.Pickens (WR) 9/13 for 130, 1 TD | J.Williams (RB) 12 for 45, 1 TD |
| 6 | PIT | D.Metcalf (WR) 11/15 for 93, 0 TD | J.Warren (RB) 14 for 50, 0 TD |
| 7 | CAR | D.Waller (TE) 1/2 for 50, 1 TD | C.Hubbard (RB) 7 for 33, 0 TD |
| 8 | ATL | J.Dotson (WR) 2/5 for 95, 0 TD | Bi.Robinson (RB) 19 for 76, 0 TD |
| 9 | CHI | L.Burden (WR) 7/10 for 97, 1 TD | D.Swift (RB) 12 for 31, 0 TD |
| 11 | DET | J.Williams (WR) 4/4 for 93, 1 TD | J.Gibbs (RB) 23 for 98, 2 TD |

### TB run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 50 | 210 | 4.2 | 3 |
| left tackle | 27 | 91 | 3.37 | 1 |
| right end | 22 | 117 | 5.32 | 1 |
| left guard | 19 | 71 | 3.74 | 1 |
| right tackle | 16 | 45 | 2.81 | 0 |
| left end | 15 | 29 | 1.93 | 0 |
| right guard | 13 | 49 | 3.77 | 1 |

### TB defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Jacob Parrish | 8 | 51 | 26 | 359 | 7.0 | 1 | 2 | 3 |
| Zyon McCollum | 7 | 42 | 19 | 236 | 5.6 | 1 | 4 | 6 |
| Tykee Smith | 8 | 41 | 20 | 223 | 5.4 | 1 | 2 | 3 |
| Alex Anzalone | 8 | 39 | 26 | 221 | 5.7 | 0 | 4 | 1 |
| Keionte Scott | 8 | 37 | 24 | 212 | 5.7 | 3 | 0 | 7 |
| Josiah Trotter | 7 | 25 | 15 | 126 | 5.0 | 1 | 0 | 3 |
| Ifeatu Melifonwu | 5 | 14 | 6 | 109 | 7.8 | 0 | 0 | 1 |
| Antoine Winfield Jr. | 4 | 8 | 3 | 27 | 3.4 | 0 | 0 | 0 |
| Benjamin Morrison | 1 | 6 | 5 | 131 | 21.8 | 2 | 0 | 0 |
| YaYa Diaby | 6 | 5 | 3 | 45 | 9.0 | 0 | 1 | 0 |

### TB pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| David Walker | 8 | 11 | 4.0 | 4 | 2 |
| Al-Quadin Muhammad | 6 | 7 | 2.0 | 5 | 0 |
| YaYa Diaby | 6 | 7 | 3.0 | 1 | 6 |
| Rueben Bain | 6 | 6 | 1.0 | 3 | 1 |
| Calijah Kancey | 5 | 6 | 0.5 | 3 | 0 |
| Josiah Trotter | 7 | 5 | 0.0 | 5 | 33 |
| Tykee Smith | 8 | 5 | 0.0 | 1 | 23 |
| Vita Vea | 5 | 5 | 1.0 | 1 | 0 |

### TB offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 22.1 | 20/32 | 23.3 |
| Pass yards / game | 151.5 | 32/32 | 234.4 |
| Yards per pass attempt | 5.77 | 31/32 | 7.13 |
| Rush yards / game | 151.4 | 1/32 | 101.0 |
| Yards per carry | 4.90 | 5/32 | 4.11 |
| RB rush yards / game | 141.9 | 2/32 | 93.8 |
| WR yards / game | 98.6 | 31/32 | 147.6 |
| TE yards / game | 22.6 | 32/32 | 53.3 |
| RB receiving yards / game | 30.6 | 19/32 | 33.4 |
| Explosive passes (20+) / game | 1.50 | 32/32 | 2.98 |
| Explosive runs (15+) / game | 1.75 | 2/32 | 1.22 |
| Sack rate allowed | 9.3% | 29/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 15.4% | 14/32 | 15.4% |
| Third-down conversion rate | 36.6% | 24/32 | 39.4% |
| Red-zone TD rate | 56.0% | 19/32 | 58.9% |

Neutral-situation pass rate 42.6%; 63.2 plays per game; target share WR 62% / TE 17% / RB 21%.

### TB offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs MIN | 16 | 217 | 42 | 42 | 10-135 | 3-56 | 4-26 | 3 | 0 | 6 |
| 4 | vs GB | 14 | 148 | 95 | 76 | 13-89 | 4-37 | 2-22 | 1 | 1 | 3 |
| 5 | @ DAL | 24 | 189 | 218 | 201 | 10-139 | 4-30 | 5-20 | 2 | 2 | 1 |
| 6 | vs PIT | 19 | 164 | 63 | 63 | 16-132 | 2-25 | 3-10 | 2 | 1 | 5 |
| 7 | @ CAR | 43 | 64 | 261 | 246 | 6-60 | 0-0 | 1-4 | 0 | 4 | 0 |
| 8 | vs ATL | 16 | 0 | 322 | 310 | 0-0 | 0-0 | 0-0 | 0 | 4 | 1 |
| 9 | @ CHI | 24 | 243 | 126 | 113 | 7-130 | 4-25 | 7-88 | 3 | 1 | 4 |
| 11 | @ DET | 21 | 187 | 84 | 84 | 12-104 | 1-8 | 7-75 | 1 | 1 | 4 |

**QB B.Mayfield** (5 games): 62/112, 711 yds, 4 TD, 3 INT, 15 sacks, 6.35 yds/att, depth of target 7.5, pressured on 18.1% of dropbacks. Yards by game: W3 217, W7 64, W8 0, W9 243, W11 187.

**QB J.Daniels** (4 games): 60/98, 501 yds, 3 TD, 5 INT, 9 sacks, 5.11 yds/att, depth of target 6.1, pressured on 15.9% of dropbacks. Yards by game: W3 0, W4 148, W5 189, W6 164.

### TB receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E.Egbuka | WR | 6 | 48 | 25 | 217 | 1 | 24% | 33% | 9.5 | 5 | 3 | 62 13 38 48 38 18 |
| C.Godwin | WR | 8 | 34 | 25 | 186 | 0 | 17% | 9% | 3.6 | 4 | 0 | 25 31 37 37 27 0 16 13 |
| C.Otton | TE | 7 | 30 | 16 | 155 | 0 | 15% | 16% | 7.3 | 4 | 1 | 56 37 25 4 0 25 8 |
| T.Hurst | WR | 7 | 22 | 11 | 161 | 3 | 11% | 20% | 12.5 | 4 | 4 | 40 25 40 0 0 0 56 |
| K.Gainwell | RB | 7 | 21 | 15 | 156 | 1 | 10% | 1% | 0.3 | 3 | 1 | 14 22 10 7 0 60 43 |
| B.Irving | RB | 6 | 21 | 14 | 89 | 1 | 10% | 1% | 0.8 | 6 | 0 | 12 10 3 4 28 32 |
| T.Johnson | WR | 7 | 18 | 12 | 222 | 1 | 9% | 17% | 13.1 | 1 | 2 | 8 17 64 7 33 76 17 |
| P.Durham | TE | 2 | 2 | 1 | 5 | 0 | 1% | 0% | 3.0 | 0 | 0 | 0 5 |
| K.Johnson | WR | 1 | 2 | 1 | 3 | 0 | 1% | 0% | 1.0 | 0 | 0 | 3 |

### TB rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| B.Irving | RB | 8 | 160 | 759 | 4.74 | 7 | 65% | 36 | 7 | 46 61 165 46 106 170 97 68 |
| K.Gainwell | RB | 8 | 60 | 296 | 4.93 | 0 | 24% | 5 | 4 | -4 5 18 17 88 140 16 16 |
| S.Tucker | RB | 3 | 15 | 80 | 5.33 | 2 | 6% | 5 | 1 | 10 18 52 |
| B.Mayfield | QB | 5 | 4 | 13 | 3.25 | 0 | 2% | 1 | 0 | 0 1 12 0 0 |
| C.Godwin | WR | 2 | 2 | 15 | 7.50 | 0 | 1% | 0 | 0 | 3 12 |

### TB run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 49 | 211 | 4.31 | 3 |
| right tackle | 45 | 207 | 4.6 | 3 |
| left guard | 37 | 149 | 4.03 | 1 |
| left tackle | 33 | 219 | 6.64 | 3 |
| right guard | 30 | 119 | 3.97 | 0 |
| left end | 27 | 204 | 7.56 | 2 |
| right end | 22 | 82 | 3.73 | 0 |

### TB by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 305 | 60% | 66% | 4.59 | -0.092 |
| offense | Under center | 168 | 33% | 18% | 5.63 | 0.018 |
| offense | No huddle | 33 | 6% | 82% | 2.79 | -0.101 |
| defense vs | Shotgun | 234 | 51% | 82% | 5.93 | -0.19 |
| defense vs | Under center | 179 | 39% | 38% | 4.26 | -0.049 |
| defense vs | No huddle | 42 | 9% | 79% | 6.5 | 0.155 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 73 | 35% | 68% | 4.36 | 0 |
| offense | Short middle | 23 | 11% | 56% | 5.57 | 1 |
| offense | Short right | 82 | 39% | 58% | 5.06 | 2 |
| offense | Deep left | 10 | 5% | 40% | 10.8 | 4 |
| offense | Deep middle | 5 | 2% | 40% | 19.6 | 2 |
| offense | Deep right | 17 | 8% | 29% | 8.53 | 3 |
| defense allows | Short left | 79 | 30% | 70% | 5.62 | 2 |
| defense allows | Short middle | 53 | 20% | 62% | 6.25 | 1 |
| defense allows | Short right | 90 | 34% | 63% | 5.3 | 2 |
| defense allows | Deep left | 20 | 8% | 35% | 12.35 | 5 |
| defense allows | Deep middle | 11 | 4% | 46% | 18.0 | 5 |
| defense allows | Deep right | 15 | 6% | 27% | 8.67 | 4 |

### TB lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Tristan Wirfs, LG Ben Bredeson, C Graham Barton, RG Cody Mauch, RT Luke Goedeke.  
Defensive front: LDE Calijah Kancey, NT Vita Vea, RDE A'Shawn Robinson, WLB Rueben Bain Jr., SLB Yaya Diaby.

### TB injuries

Official report not posted yet for this week.

ESPN live list (designations only): Benjamin Morrison (CB) Questionable; Elijah Simmons (DT) Questionable; Christian Rozeboom (LB) Injured Reserve; Jalen McMillan (WR) Injured Reserve; Josiah Trotter (LB) Questionable; Antoine Winfield Jr. (S) Questionable; Jacob Parrish (CB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### TB roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Brett Rypien (QB) to LV.

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
