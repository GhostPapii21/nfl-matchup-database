# SF at NYG: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: outdoors; surface: fieldturf. Rest: SF 7 days, NYG 7 days. Listed QBs: Brock Purdy (SF), J.J. McCarthy (NYG).

Market (schedule consensus, not a timestamped quote): NYG +6.5, total 47.5.

Generated 2026-11-26T19:39:50+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T19:22:36Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | NYG +6.5 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-26T19:22:36+00:00 |
| total | fanduel | Over 46.5 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-26T19:22:36+00:00 |
| moneyline | fanduel | NYG | +245 | -300 | 27.9% | 72.1% | 4.0% | 2026-11-26T19:22:36+00:00 |

Player props: OK.

## Matchup edges

### SF offense vs NYG defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| NYG DEFENCE STRENGTH | tight end yards | 65.0 | 42.1 | 54.7 | SF offence ranks 6 of 32, NYG defence ranks 4 of 32 (1 = best at its own job) |
| NYG DEFENCE STRENGTH | running back receiving yards | 59.1 | 21.4 | 33.0 | SF offence ranks 1 of 32, NYG defence ranks 5 of 32 (1 = best at its own job) |
| SF OFFENCE ADVANTAGE | explosive runs (15+) | 1.6 | 1.9 | 1.2 | SF offence ranks 5 of 32, NYG defence ranks 30 of 32 (1 = best at its own job) |
| NYG DEFENCE STRENGTH | passing yards | 267.1 | 195.2 | 235.6 | SF offence ranks 8 of 32, NYG defence ranks 3 of 32 (1 = best at its own job) |
| SF OFFENCE STRENGTH | points | 31.8 | 20.8 | 23.0 | SF offence ranks 1 of 32, NYG defence ranks 11 of 32 (1 = best at its own job) |
| SF OFFENCE STRENGTH | third-down conversions | 50.0% | 33.6% | 39.2% | SF offence ranks 2 of 32, NYG defence ranks 7 of 32 (1 = best at its own job) |
| SF OFFENCE STRENGTH | red-zone touchdowns | 84.6% | 57.9% | 58.0% | SF offence ranks 1 of 32, NYG defence ranks 17 of 32 (1 = best at its own job) |

### NYG offense vs SF defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| NYG OFFENCE ADVANTAGE | tight end yards | 76.4 | 62.4 | 54.7 | NYG offence ranks 5 of 32, SF defence ranks 25 of 32 (1 = best at its own job) |
| SF DEFENCE STRENGTH | running back rushing yards | 82.6 | 64.2 | 92.5 | NYG offence ranks 20 of 32, SF defence ranks 4 of 32 (1 = best at its own job) |
| SF DEFENCE STRENGTH | explosive runs (15+) | 1.2 | 0.2 | 1.2 | NYG offence ranks 14 of 32, SF defence ranks 1 of 32 (1 = best at its own job) |
| SF DEFENCE WEAK SPOT | passing yards | 250.6 | 253.1 | 235.6 | NYG offence ranks 13 of 32, SF defence ranks 24 of 32 (1 = best at its own job) |
| SF DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 7.9% | 3.8% | 6.6% | NYG offence ranks 24 of 32, SF defence ranks 32 of 32 (1 = best at its own job) |
| SF DEFENCE WEAK SPOT | pressure (sacks + hits) | 16.4% | 13.8% | 15.7% | NYG offence ranks 20 of 32, SF defence ranks 25 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | SF 26.0 - NYG 22.1 | 48.2 | -3.9 | 33.0% | 58.7% | 51.2% | SF 13.3 - NYG 10.8 |
| independent | SF 28.0 - NYG 22.3 | 50.3 | -5.7 | 35.3% | 53.4% | 56.5% | SF 14.6 - NYG 11.3 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### SF offense vs NYG defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G.Kittle | TE | receiving yards | 8 | 54.2 | 0.885 | 24.3 | 27.4 | 31.2 | 38.6 | 46.0 | 61.5 |
| G.Kittle | TE | receptions | 8 | 5.1 | 1.003 | 3.4 | 3.7 | 4.0 | 4.0 | 4.0 | 5.0 |
| C.McCaffrey | RB | receiving yards | 8 | 43.2 | 0.85 | 11.6 | 12.2 | 12.9 | 13.8 | 14.7 | 25.5 |
| C.McCaffrey | RB | receptions | 8 | 3.6 | 0.88 | 1.8 | 1.8 | 1.8 | 2.1 | 2.4 | 3.1 |
| M.Evans | WR | receiving yards | 5 | 85.9 | 0.946 | 40.1 | 48.0 | 56.0 | 63.9 | 71.9 | 88.9 |
| M.Evans | WR | receptions | 5 | 4.9 | 0.993 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 5.0 |
| C.McCaffrey | RB | rushing yards | 8 | 55.4 | 0.945 | 40.1 | 43.4 | 46.4 | 47.4 | 48.4 | 59.5 |
| K.Black | RB | rushing yards | 8 | 34.2 | 0.945 | 9.2 | 10.9 | 12.4 | 13.4 | 14.4 | 24.1 |
| B.Purdy | QB | passing yards | 8 | 247.6 | 0.914 | 182.1 | 191.4 | 200.0 | 204.5 | 208.9 | 237.3 |

### NYG offense vs SF defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M.Nabers | WR | receiving yards | 8 | 83.5 | 1.017 | 32.5 | 38.5 | 43.8 | 44.1 | 44.5 | 84.4 |
| M.Nabers | WR | receptions | 8 | 7.9 | 1.103 | 5.5 | 5.5 | 5.5 | 5.5 | 5.5 | 7.2 |
| I.Likely | TE | receiving yards | 8 | 68.4 | 1.071 | 13.2 | 13.6 | 15.1 | 23.3 | 31.6 | 63.7 |
| I.Likely | TE | receptions | 8 | 6.0 | 1.132 | 1.5 | 1.9 | 2.3 | 2.3 | 2.3 | 6.2 |
| M.Fields | WR | receiving yards | 8 | 42.0 | 1.017 | 19.3 | 19.3 | 19.4 | 19.7 | 20.1 | 33.1 |
| M.Fields | WR | receptions | 8 | 2.8 | 1.103 | 2.2 | 2.2 | 2.2 | 2.2 | 2.2 | 2.2 |
| D.Mooney | WR | receiving yards | 8 | 12.9 | 1.017 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 6.1 |
| D.Mooney | WR | receptions | 8 | 1.4 | 1.103 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.7 |
| C.Skattebo | RB | rushing yards | 6 | 58.5 | 0.85 | 34.0 | 39.1 | 44.2 | 49.3 | 49.5 | 50.6 |
| D.Singletary | RB | rushing yards | 5 | 14.4 | 0.85 | 2.9 | 3.2 | 3.6 | 3.9 | 4.2 | 11.9 |
| N.Harris | RB | rushing yards | 4 | 15.7 | 0.85 | 2.6 | 3.5 | 4.4 | 5.3 | 6.2 | 16.6 |
| J.McCarthy | QB | passing yards | 5 | 222.3 | 1.037 | 141.3 | 150.8 | 160.4 | 169.9 | 179.4 | 252.1 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## SF (last 8 games: weeks 3, 4, 5, 6, 7, 9, 10, 11)

### SF defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 23.2 | 18/32 | 23.0 |
| Pass yards allowed / game | 253.1 | 24/32 | 235.6 |
| Yards per pass attempt allowed | 6.35 | 6/32 | 7.14 |
| Rush yards allowed / game | 69.9 | 3/32 | 99.5 |
| Yards per carry allowed | 3.35 | 3/32 | 4.07 |
| RB rush yards allowed / game | 64.2 | 4/32 | 92.5 |
| WR yards allowed / game | 152.9 | 22/32 | 147.8 |
| WR receptions allowed / game | 13.8 | 29/32 | 11.4 |
| TE yards allowed / game | 62.4 | 25/32 | 54.7 |
| TE receptions allowed / game | 6.8 | 29/32 | 5.3 |
| RB receiving yards allowed / game | 37.9 | 22/32 | 33.0 |
| RB receptions allowed / game | 6.5 | 32/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.88 | 12/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.25 | 1/32 | 1.21 |
| Sack rate | 3.8% | 32/32 | 6.6% |
| Pressure rate (sacks + hits) | 13.8% | 25/32 | 15.7% |
| Third-down conversions allowed | 43.1% | 21/32 | 39.2% |
| Red-zone TD rate allowed | 57.7% | 16/32 | 58.0% |
| Takeaways / game | 1.62 | 5/32 | 1.23 |

Blitz rate 29.0% and play-action faced 20.5% on 341 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.1 per game, 27.3% completed.

### SF defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs ARI | 30 | 280 | 93 | 89 | 16-151 | 13-100 | 9-29 | 0 | 0 | 2 |
| 4 | vs DEN | 14 | 214 | 72 | 72 | 10-96 | 1-6 | 14-112 | 2 | 0 | 0 |
| 5 | @ SEA | 29 | 195 | 84 | 68 | 9-140 | 3-20 | 6-35 | 3 | 1 | 5 |
| 6 | vs WAS | 17 | 300 | 43 | 43 | 15-193 | 8-73 | 6-34 | 4 | 0 | 4 |
| 7 | @ ATL | 29 | 213 | 83 | 72 | 9-95 | 10-54 | 6-64 | 1 | 0 | 0 |
| 9 | vs LV | 17 | 216 | 24 | 22 | 7-73 | 10-148 | 5--5 | 4 | 0 | 0 |
| 10 | @ DAL | 40 | 343 | 91 | 80 | 25-293 | 2-38 | 3-12 | 5 | 0 | 1 |
| 11 | vs MIN | 10 | 264 | 69 | 68 | 19-182 | 7-60 | 3-22 | 4 | 1 | 1 |

### Best individual lines allowed by SF

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | ARI | Mi.Wilson (WR) 11/17 for 89, 1 TD | J.Love (RB) 21 for 90, 0 TD |
| 4 | DEN | R.Harvey (RB) 10/10 for 68, 0 TD | J.Dobbins (RB) 11 for 40, 0 TD |
| 5 | SEA | J.Smith-Njigba (WR) 5/8 for 102, 1 TD | E.Wilson (RB) 20 for 61, 1 TD |
| 6 | WAS | C.Okonkwo (TE) 7/7 for 69, 0 TD | R.White (RB) 7 for 27, 0 TD |
| 7 | ATL | D.London (WR) 7/10 for 66, 1 TD | Bi.Robinson (RB) 20 for 63, 0 TD |
| 9 | LV | B.Bowers (TE) 7/8 for 111, 1 TD | A.Jeanty (RB) 6 for 25, 0 TD |
| 10 | DAL | G.Pickens (WR) 11/18 for 145, 3 TD | J.Williams (RB) 16 for 63, 0 TD |
| 11 | MIN | J.Jefferson (WR) 7/9 for 86, 0 TD | J.Mason (RB) 11 for 38, 0 TD |

### SF run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 61 | 171 | 2.8 | 0 |
| right guard | 26 | 104 | 4.0 | 0 |
| left guard | 26 | 84 | 3.23 | 0 |
| right end | 22 | 90 | 4.09 | 1 |
| left tackle | 12 | 47 | 3.92 | 1 |
| right tackle | 10 | 27 | 2.7 | 0 |
| left end | 8 | 36 | 4.5 | 0 |

### SF defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Renardo Green | 8 | 50 | 34 | 342 | 6.8 | 2 | 3 | 1 |
| Deommodore Lenoir | 8 | 48 | 29 | 330 | 6.9 | 5 | 0 | 1 |
| Fred Warner | 8 | 33 | 24 | 205 | 6.2 | 0 | 0 | 7 |
| Upton Stout | 7 | 29 | 23 | 260 | 9.0 | 2 | 0 | 4 |
| Dre Greenlaw | 6 | 28 | 19 | 103 | 3.7 | 0 | 0 | 7 |
| Malik Mustapha | 7 | 27 | 10 | 161 | 6.0 | 1 | 2 | 3 |
| Ji'Ayir Brown | 8 | 25 | 17 | 166 | 6.6 | 1 | 1 | 2 |
| Jaden Dugger | 7 | 24 | 21 | 129 | 5.4 | 1 | 1 | 6 |
| Jack Jones | 4 | 17 | 11 | 115 | 6.8 | 2 | 0 | 1 |
| Ephesians Prysock | 4 | 10 | 7 | 49 | 4.9 | 1 | 0 | 1 |

### SF pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Keion White | 8 | 17 | 2.5 | 9 | 0 |
| Osa Odighizuwa | 8 | 11 | 2.5 | 4 | 0 |
| Sebastian Valdez | 4 | 7 | 1.0 | 3 | 0 |
| Romello Height | 5 | 5 | 0.5 | 1 | 4 |
| Mykel Williams | 3 | 5 | 1.5 | 0 | 0 |
| Fred Warner | 8 | 4 | 0.0 | 0 | 34 |
| DeForest Buckner | 3 | 4 | 0.5 | 1 | 0 |
| Dre Greenlaw | 6 | 3 | 0.5 | 2 | 17 |

### SF offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 31.8 | 1/32 | 23.2 |
| Pass yards / game | 267.1 | 8/32 | 234.2 |
| Yards per pass attempt | 9.17 | 1/32 | 7.12 |
| Rush yards / game | 122.5 | 5/32 | 100.6 |
| Yards per carry | 4.80 | 6/32 | 4.10 |
| RB rush yards / game | 97.4 | 14/32 | 93.4 |
| WR yards / game | 143.0 | 17/32 | 147.5 |
| TE yards / game | 65.0 | 6/32 | 53.4 |
| RB receiving yards / game | 59.1 | 1/32 | 33.2 |
| Explosive passes (20+) / game | 3.62 | 9/32 | 2.96 |
| Explosive runs (15+) / game | 1.62 | 5/32 | 1.23 |
| Sack rate allowed | 5.3% | 12/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 13.3% | 7/32 | 15.4% |
| Third-down conversion rate | 50.0% | 2/32 | 39.4% |
| Red-zone TD rate | 84.6% | 1/32 | 58.9% |

Neutral-situation pass rate 54.0%; 58.4 plays per game; target share WR 47% / TE 27% / RB 26%.

### SF offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs ARI | 36 | 297 | 106 | 92 | 5-174 | 6-82 | 4-41 | 5 | 1 | 0 |
| 4 | vs DEN | 24 | 218 | 118 | 65 | 10-102 | 4-70 | 5-46 | 2 | 2 | 0 |
| 5 | @ SEA | 32 | 189 | 90 | 84 | 11-150 | 5-24 | 3-15 | 3 | 0 | 3 |
| 6 | vs WAS | 23 | 264 | 102 | 98 | 5-129 | 5-69 | 11-66 | 4 | 0 | 2 |
| 7 | @ ATL | 20 | 288 | 123 | 108 | 7-107 | 9-102 | 11-79 | 4 | 2 | 2 |
| 9 | vs LV | 38 | 232 | 157 | 153 | 11-155 | 4-58 | 2-19 | 3 | 3 | 1 |
| 10 | @ DAL | 46 | 389 | 193 | 115 | 10-141 | 6-74 | 6-174 | 6 | 4 | 5 |
| 11 | vs MIN | 35 | 260 | 91 | 64 | 13-186 | 4-41 | 5-33 | 2 | 1 | 1 |

**QB B.Purdy** (8 games): 161/232, 2132 yds, 18 TD, 4 INT, 14 sacks, 9.19 yds/att, depth of target 8.4, pressured on 14.2% of dropbacks. Yards by game: W3 297, W4 218, W5 189, W6 264, W7 288, W9 232, W10 389, W11 255.

**QB M.Jones** (1 games): 1/1, 5 yds, 0 TD, 0 INT, 0 sacks, 5.00 yds/att, depth of target -3.0, pressured on 0.0% of dropbacks. Yards by game: W11 5.

### SF receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G.Kittle | TE | 8 | 56 | 41 | 499 | 6 | 25% | 22% | 7.5 | 11 | 7 | 82 70 24 69 88 58 74 34 |
| C.McCaffrey | RB | 8 | 40 | 33 | 381 | 3 | 18% | 7% | 3.5 | 6 | 3 | 41 18 15 53 61 19 161 13 |
| M.Evans | WR | 5 | 36 | 24 | 426 | 4 | 16% | 29% | 15.6 | 5 | 10 | 34 76 113 94 109 |
| J.Watkins | WR | 6 | 17 | 13 | 292 | 1 | 7% | 14% | 16.5 | 0 | 8 | 60 22 56 86 49 19 |
| D.Samuel | WR | 4 | 16 | 13 | 98 | 2 | 7% | 0% | 0.5 | 3 | 0 | 26 21 31 20 |
| K.Juszczyk | RB | 5 | 11 | 8 | 62 | 1 | 5% | 4% | 6.7 | 2 | 0 | 0 28 10 11 13 |
| K.Allen | WR | 2 | 11 | 8 | 99 | 0 | 5% | 6% | 10.7 | 0 | 1 | 61 38 |
| J.Cowing | WR | 5 | 11 | 5 | 52 | 0 | 5% | 7% | 12.1 | 0 | 0 | 0 0 9 38 5 |
| B.Cooks | WR | 5 | 10 | 5 | 58 | 1 | 4% | 6% | 10.8 | 2 | 0 | 0 7 13 13 25 |

### SF rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| C.McCaffrey | RB | 8 | 107 | 477 | 4.46 | 9 | 52% | 25 | 2 | 75 52 68 64 39 68 62 49 |
| K.Black | RB | 8 | 64 | 274 | 4.28 | 2 | 31% | 10 | 5 | 17 13 16 34 63 70 53 8 |
| D.Samuel | WR | 5 | 12 | 167 | 13.92 | 1 | 6% | 0 | 4 | 14 44 4 78 27 |
| B.Purdy | QB | 7 | 12 | 22 | 1.83 | 0 | 6% | 2 | 0 | 0 7 2 4 5 4 0 |
| J.James | RB | 3 | 6 | 24 | 4.00 | 0 | 3% | 0 | 0 | 6 11 7 |

### SF run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 80 | 355 | 4.44 | 3 |
| left end | 27 | 227 | 8.41 | 4 |
| left tackle | 25 | 115 | 4.6 | 1 |
| left guard | 21 | 49 | 2.33 | 0 |
| right guard | 21 | 96 | 4.57 | 1 |
| right end | 19 | 95 | 5.0 | 2 |
| right tackle | 11 | 43 | 3.91 | 0 |

### SF by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 233 | 50% | 78% | 8.25 | 0.282 |
| offense | Under center | 220 | 47% | 34% | 5.47 | 0.116 |
| offense | No huddle | 14 | 3% | 57% | 4.5 | -0.08 |
| defense vs | Shotgun | 296 | 58% | 81% | 5.48 | -0.01 |
| defense vs | Under center | 169 | 33% | 38% | 3.83 | -0.099 |
| defense vs | No huddle | 43 | 8% | 81% | 6.05 | 0.219 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 87 | 37% | 70% | 7.76 | 5 |
| offense | Short middle | 44 | 19% | 70% | 7.43 | 2 |
| offense | Short right | 59 | 25% | 83% | 9.32 | 3 |
| offense | Deep left | 16 | 7% | 19% | 4.94 | 3 |
| offense | Deep middle | 16 | 7% | 75% | 19.94 | 10 |
| offense | Deep right | 11 | 5% | 55% | 17.0 | 6 |
| defense allows | Short left | 110 | 35% | 86% | 6.53 | 4 |
| defense allows | Short middle | 33 | 10% | 55% | 5.7 | 2 |
| defense allows | Short right | 113 | 36% | 70% | 4.8 | 2 |
| defense allows | Deep left | 21 | 7% | 38% | 9.33 | 5 |
| defense allows | Deep middle | 13 | 4% | 54% | 10.85 | 3 |
| defense allows | Deep right | 28 | 9% | 32% | 8.57 | 7 |

### SF lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Trent Williams, LG Connor Colby, C Jake Brendel, RG Dominick Puni, RT Vederian Lowe.  
Defensive front: LDE Keion White, LDT Osa Odighizuwa, RDT DeForest Buckner, RDE Nick Bosa, WLB Dre Greenlaw, SLB Jaden Dugger.

### SF injuries

Official report not posted yet for this week.

ESPN live list (designations only): Brock Purdy (QB) Questionable; Mike Evans (WR) Questionable; De'Zhaun Stribling (WR) Injured Reserve; Sam Okuayinonu (DT) Injured Reserve; Siran Neal (S) Questionable; Carver Willis (OT) Questionable; Upton Stout (CB) Questionable; Dre Greenlaw (LB) Questionable; Deommodore Lenoir (CB) Questionable; Jordan Watkins (WR) Questionable; Colton McKivitz (OT) Injured Reserve; Austen Pleasants (OT) Injured Reserve.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### SF roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Xavier Smith (WR) to LA.

## NYG (last 8 games: weeks 3, 4, 5, 6, 7, 9, 10, 11)

### NYG defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 20.8 | 11/32 | 23.0 |
| Pass yards allowed / game | 195.2 | 3/32 | 235.6 |
| Yards per pass attempt allowed | 5.85 | 2/32 | 7.14 |
| Rush yards allowed / game | 90.6 | 12/32 | 99.5 |
| Yards per carry allowed | 3.88 | 12/32 | 4.07 |
| RB rush yards allowed / game | 82.2 | 12/32 | 92.5 |
| WR yards allowed / game | 131.8 | 7/32 | 147.8 |
| WR receptions allowed / game | 11.2 | 16/32 | 11.4 |
| TE yards allowed / game | 42.1 | 4/32 | 54.7 |
| TE receptions allowed / game | 5.4 | 19/32 | 5.3 |
| RB receiving yards allowed / game | 21.4 | 5/32 | 33.0 |
| RB receptions allowed / game | 3.4 | 6/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.50 | 6/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.88 | 30/32 | 1.21 |
| Sack rate | 6.1% | 18/32 | 6.6% |
| Pressure rate (sacks + hits) | 14.6% | 20/32 | 15.7% |
| Third-down conversions allowed | 33.6% | 7/32 | 39.2% |
| Red-zone TD rate allowed | 57.9% | 17/32 | 58.0% |
| Takeaways / game | 1.25 | 12/32 | 1.23 |

Blitz rate 41.7% and play-action faced 19.7% on 309 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.8 per game, 13.3% completed.

### NYG defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs TEN | 7 | 181 | 81 | 79 | 15-129 | 4-30 | 4-22 | 1 | 1 | 0 |
| 4 | vs ARI | 24 | 166 | 115 | 105 | 8-107 | 10-60 | 3--1 | 2 | 2 | 2 |
| 5 | @ WAS | 27 | 199 | 100 | 99 | 10-121 | 5-61 | 2-17 | 3 | 5 | 5 |
| 6 | vs NO | 34 | 144 | 142 | 143 | 10-99 | 2-10 | 4-35 | 1 | 3 | 0 |
| 7 | @ HOU | 21 | 153 | 82 | 66 | 10-94 | 6-44 | 1-15 | 2 | 0 | 1 |
| 9 | @ PHI | 11 | 169 | 42 | 28 | 10-99 | 5-50 | 3-20 | 1 | 2 | 7 |
| 10 | vs WAS | 24 | 249 | 85 | 77 | 10-152 | 8-66 | 5-31 | 5 | 1 | 1 |
| 11 | vs JAX | 18 | 301 | 78 | 61 | 17-253 | 3-16 | 5-32 | 5 | 1 | 3 |

### Best individual lines allowed by NYG

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | TEN | C.Tate (WR) 6/9 for 58, 0 TD | T.Pollard (RB) 17 for 74, 0 TD |
| 4 | ARI | Mi.Wilson (WR) 7/13 for 95, 0 TD | J.Love (RB) 14 for 63, 0 TD |
| 5 | WAS | T.McLaurin (WR) 4/4 for 62, 0 TD | J.Croskey-Merritt (RB) 11 for 82, 1 TD |
| 6 | NO | C.Olave (WR) 4/7 for 43, 1 TD | K.Miller (RB) 20 for 70, 0 TD |
| 7 | HOU | D.Schultz (TE) 5/6 for 45, 0 TD | W.Marks (RB) 19 for 66, 0 TD |
| 9 | PHI | M.Lemon (WR) 6/9 for 61, 0 TD | S.Barkley (RB) 13 for 22, 1 TD |
| 10 | WAS | S.Diggs (WR) 6/10 for 83, 1 TD | R.White (RB) 11 for 47, 0 TD |
| 11 | JAX | P.Washington (WR) 8/17 for 103, 0 TD | B.Tuten (RB) 10 for 33, 0 TD |

### NYG run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 42 | 154 | 3.67 | 2 |
| right guard | 31 | 127 | 4.1 | 0 |
| left tackle | 30 | 85 | 2.83 | 1 |
| left guard | 29 | 100 | 3.45 | 1 |
| right end | 26 | 124 | 4.77 | 3 |
| left end | 14 | 72 | 5.14 | 1 |
| right tackle | 14 | 56 | 4.0 | 1 |

### NYG defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Deonte Banks | 7 | 44 | 19 | 187 | 4.2 | 3 | 2 | 5 |
| Andru Phillips | 8 | 41 | 24 | 270 | 6.6 | 2 | 0 | 7 |
| Arvell Reese | 8 | 37 | 31 | 154 | 4.2 | 0 | 1 | 3 |
| Greg Newsome II | 7 | 30 | 17 | 186 | 6.2 | 0 | 1 | 2 |
| Ar'Darius Washington | 7 | 24 | 14 | 145 | 6.0 | 0 | 1 | 4 |
| Micah McFadden | 4 | 23 | 14 | 121 | 5.3 | 1 | 0 | 6 |
| Jevon Holland | 7 | 23 | 10 | 154 | 6.7 | 2 | 2 | 5 |
| Tremaine Edmunds | 4 | 10 | 9 | 92 | 9.2 | 0 | 0 | 1 |
| Jason Pinnock | 5 | 9 | 5 | 73 | 8.1 | 2 | 0 | 4 |
| Paulson Adebo | 2 | 8 | 2 | 22 | 2.8 | 0 | 1 | 0 |

### NYG pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Abdul Carter | 6 | 14 | 3.0 | 3 | 21 |
| Arvell Reese | 8 | 9 | 4.5 | 3 | 65 |
| D.J. Reader | 4 | 7 | 2.0 | 1 | 0 |
| Kayvon Thibodeaux | 7 | 6 | 0.0 | 4 | 18 |
| Andru Phillips | 8 | 4 | 2.0 | 0 | 17 |
| Darius Alexander | 4 | 4 | 1.5 | 1 | 0 |
| Micah McFadden | 4 | 4 | 1.0 | 1 | 32 |
| Shelby Harris | 3 | 4 | 1.0 | 1 | 0 |

### NYG offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 24.0 | 12/32 | 23.2 |
| Pass yards / game | 250.6 | 13/32 | 234.2 |
| Yards per pass attempt | 7.24 | 17/32 | 7.12 |
| Rush yards / game | 89.0 | 21/32 | 100.6 |
| Yards per carry | 3.51 | 28/32 | 4.10 |
| RB rush yards / game | 82.6 | 20/32 | 93.4 |
| WR yards / game | 146.6 | 14/32 | 147.5 |
| TE yards / game | 76.4 | 5/32 | 53.4 |
| RB receiving yards / game | 27.6 | 21/32 | 33.2 |
| Explosive passes (20+) / game | 3.75 | 6/32 | 2.96 |
| Explosive runs (15+) / game | 1.25 | 14/32 | 1.23 |
| Sack rate allowed | 7.9% | 24/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 16.4% | 20/32 | 15.4% |
| Third-down conversion rate | 37.5% | 20/32 | 39.4% |
| Red-zone TD rate | 62.5% | 11/32 | 58.9% |

Neutral-situation pass rate 50.7%; 65.0 plays per game; target share WR 58% / TE 28% / RB 14%.

### NYG offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs TEN | 12 | 118 | 124 | 115 | 9-65 | 2-13 | 3-40 | 1 | 1 | 3 |
| 4 | vs ARI | 36 | 250 | 87 | 87 | 8-164 | 8-77 | 2-9 | 5 | 0 | 4 |
| 5 | @ WAS | 27 | 326 | 76 | 74 | 15-155 | 13-129 | 5-42 | 4 | 2 | 2 |
| 6 | vs NO | 27 | 395 | 57 | 34 | 16-250 | 6-99 | 3-46 | 6 | 2 | 5 |
| 7 | @ HOU | 27 | 252 | 188 | 180 | 12-198 | 3-41 | 5-13 | 5 | 4 | 3 |
| 9 | @ PHI | 19 | 198 | 51 | 51 | 11-137 | 5-53 | 2-8 | 3 | 0 | 6 |
| 10 | vs WAS | 21 | 293 | 88 | 81 | 10-114 | 10-135 | 3-44 | 5 | 0 | 1 |
| 11 | vs JAX | 23 | 173 | 41 | 39 | 11-90 | 3-64 | 4-19 | 1 | 1 | 1 |

**QB J.Winston** (6 games): 85/140, 917 yds, 8 TD, 4 INT, 14 sacks, 6.55 yds/att, depth of target 8.7, pressured on 18.2% of dropbacks. Yards by game: W3 118, W4 250, W5 326, W6 152, W9 71, W11 0.

**QB J.McCarthy** (5 games): 84/137, 1088 yds, 3 TD, 2 INT, 11 sacks, 7.94 yds/att, depth of target 10.9, pressured on 16.2% of dropbacks. Yards by game: W6 243, W7 252, W9 127, W10 293, W11 173.

### NYG receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M.Nabers | WR | 8 | 84 | 58 | 677 | 3 | 31% | 35% | 11.0 | 10 | 11 | 26 112 121 165 111 43 44 55 |
| I.Likely | TE | 8 | 65 | 43 | 499 | 5 | 24% | 19% | 7.6 | 8 | 7 | 13 66 94 99 12 53 127 35 |
| M.Fields | WR | 8 | 34 | 20 | 320 | 1 | 13% | 16% | 12.4 | 4 | 5 | 19 52 20 19 83 40 62 25 |
| D.Mooney | WR | 8 | 31 | 10 | 100 | 0 | 11% | 19% | 16.5 | 0 | 1 | 20 0 14 0 4 54 8 0 |
| C.Skattebo | RB | 6 | 20 | 13 | 115 | 0 | 7% | 1% | 1.6 | 2 | 2 | 40 8 12 -3 44 14 |
| D.Singletary | RB | 4 | 8 | 7 | 46 | 0 | 3% | -0% | -1.2 | 0 | 0 | 19 14 8 5 |
| T.Johnson | TE | 4 | 8 | 5 | 69 | 1 | 3% | 3% | 9.5 | 1 | 1 | 11 35 8 15 |
| T.Tracy | RB | 3 | 7 | 5 | 54 | 1 | 3% | 0% | 0.6 | 1 | 1 | 25 27 2 |
| C.Jones | WR | 1 | 3 | 2 | 66 | 0 | 1% | 3% | 23.7 | 0 | 1 | 66 |

### NYG rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| C.Skattebo | RB | 6 | 100 | 413 | 4.13 | 3 | 49% | 15 | 4 | 60 58 59 124 78 34 |
| D.Singletary | RB | 5 | 32 | 94 | 2.94 | 1 | 16% | 2 | 1 | 14 41 31 3 5 |
| N.Harris | RB | 4 | 27 | 93 | 3.44 | 0 | 13% | 5 | 0 | 52 30 9 2 |
| T.Tracy | RB | 5 | 17 | 41 | 2.41 | 2 | 8% | 4 | 0 | 3 -1 6 18 15 |
| J.Winston | QB | 7 | 12 | 16 | 1.33 | 2 | 6% | 4 | 0 | 0 0 5 4 1 1 5 |

### NYG run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 60 | 225 | 3.75 | 2 |
| left guard | 35 | 108 | 3.09 | 0 |
| left tackle | 29 | 83 | 2.86 | 0 |
| left end | 21 | 66 | 3.14 | 0 |
| right end | 21 | 93 | 4.43 | 3 |
| right guard | 21 | 86 | 4.1 | 1 |
| right tackle | 16 | 51 | 3.19 | 0 |

### NYG by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 314 | 60% | 76% | 5.98 | 0.048 |
| offense | Under center | 170 | 33% | 28% | 3.91 | -0.08 |
| offense | No huddle | 36 | 7% | 81% | 5.39 | -0.165 |
| defense vs | Shotgun | 291 | 59% | 76% | 4.47 | -0.197 |
| defense vs | Under center | 154 | 31% | 34% | 5.53 | 0.125 |
| defense vs | No huddle | 51 | 10% | 72% | 4.59 | 0.064 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 81 | 29% | 63% | 4.56 | 1 |
| offense | Short middle | 56 | 20% | 70% | 7.34 | 2 |
| offense | Short right | 78 | 28% | 68% | 5.65 | 3 |
| offense | Deep left | 21 | 8% | 62% | 17.9 | 13 |
| offense | Deep middle | 16 | 6% | 38% | 13.06 | 5 |
| offense | Deep right | 25 | 9% | 28% | 7.96 | 6 |
| defense allows | Short left | 92 | 34% | 55% | 4.62 | 2 |
| defense allows | Short middle | 49 | 18% | 67% | 6.27 | 2 |
| defense allows | Short right | 77 | 29% | 75% | 5.49 | 3 |
| defense allows | Deep left | 19 | 7% | 26% | 5.05 | 3 |
| defense allows | Deep middle | 14 | 5% | 50% | 12.43 | 5 |
| defense allows | Deep right | 16 | 6% | 38% | 8.56 | 5 |

### NYG lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Andrew Thomas, LG Jon Runyan, C Bryan Hudson, RG Francis Mauigoa, RT Jermaine Eluemunor.  
Defensive front: LDE Shelby Harris, NT DJ Reader, RDE Bobby Jamison-Travis, WLB Kayvon Thibodeaux, SLB Abdul Carter.

### NYG injuries

Official report not posted yet for this week.

ESPN live list (designations only): Greg Newsome II (CB) Injured Reserve; Isaiah Likely (TE) Questionable; Shelby Harris (DT) Questionable; Arvell Reese (LB) Questionable; Abdul Carter (LB) Questionable; Dru Phillips (CB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### NYG roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Eric Gray (RB) to IND.

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
| games | OK | 2026-11-26T19:39:34+00:00 | b22bfaa75225 |
| pbp | OK | 2026-11-26T19:39:34+00:00 | 1dcada615d88 |
| rosters | OK | 2026-11-26T19:39:34+00:00 | 73ab519d2b6d |
| injuries | OK | 2026-11-26T19:39:34+00:00 | b40c5c041074 |
| depth_charts | OK | 2026-11-26T19:39:35+00:00 | d4af2fc566a2 |
| snap_counts | OK | 2026-11-26T19:39:35+00:00 | 923df2bfeef1 |
| ftn | OK | 2026-11-26T19:39:35+00:00 | ee09d5f28f5f |
| pfr_def | OK | 2026-11-26T19:39:35+00:00 | f1217d79cc1e |
| pfr_rec | OK | 2026-11-26T19:39:35+00:00 | 14b79cccde48 |
| pfr_rush | OK | 2026-11-26T19:39:35+00:00 | 45b28d9bfb26 |
| ngs_receiving | OK | 2026-11-26T19:39:35+00:00 | 2b336f985ad8 |
| ngs_rushing | OK | 2026-11-26T19:39:36+00:00 | 9cde647ab3c8 |
| ngs_passing | OK | 2026-11-26T19:39:36+00:00 | 02d9d8211a15 |
| espn_injuries | OK | 2026-11-26T19:39:36+00:00 |  |
| nfl_savant | SAME_DATA_AS_NFLVERSE_PBP: its season download is the nflverse play-by-play (checked 2026-11-11), so no second download is made |  |  |
| book_odds | NO_KEY: set the ODDS_API_KEY repository secret to include book prices |  |  |

Play-by-play, rosters, injuries, depth charts, snap counts and PFR advanced defense: nflverse (github.com/nflverse/nflverse-data). FTN charting via nflverse: FTN Data, CC-BY-SA 4.0. Third-party data keep their own terms; see SOURCES.md.
