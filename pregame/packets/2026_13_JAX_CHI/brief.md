# JAX at CHI: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: outdoors; surface: grass. Rest: JAX 7 days, CHI 10 days. Listed QBs: Trevor Lawrence (JAX), Caleb Williams (CHI).

Market (schedule consensus, not a timestamped quote): CHI -3, total 49.5.

Generated 2026-11-27T18:39:01+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-27T18:32:28Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | CHI -3 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-27T18:32:28+00:00 |
| total | fanduel | Over 50.5 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-27T18:32:28+00:00 |
| moneyline | fanduel | CHI | -158 | +136 | 59.1% | 40.9% | 3.6% | 2026-11-27T18:32:28+00:00 |

Player props: OK.

## Matchup edges

### JAX offense vs CHI defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| JAX OFFENCE ADVANTAGE | wide receiver yards | 172.0 | 162.9 | 147.7 | JAX offence ranks 7 of 32, CHI defence ranks 23 of 32 (1 = best at its own job) |
| JAX OFFENCE STRENGTH | explosive passes (20+) | 3.9 | 3.0 | 3.0 | JAX offence ranks 3 of 32, CHI defence ranks 17 of 32 (1 = best at its own job) |
| JAX OFFENCE STRENGTH | passing yards | 269.9 | 247.9 | 235.6 | JAX offence ranks 5 of 32, CHI defence ranks 21 of 32 (1 = best at its own job) |
| JAX OFFENCE STRENGTH | points | 30.0 | 22.4 | 23.3 | JAX offence ranks 4 of 32, CHI defence ranks 15 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | third-down conversions | 45.2% | 27.0% | 39.2% | JAX offence ranks 3 of 32, CHI defence ranks 2 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | sacks (pass protection vs pass rush) | 5.0% | 8.9% | 6.7% | JAX offence ranks 9 of 32, CHI defence ranks 3 of 32 (1 = best at its own job) |

### CHI offense vs JAX defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| CHI OFFENCE ADVANTAGE | wide receiver yards | 161.8 | 163.0 | 147.7 | CHI offence ranks 10 of 32, JAX defence ranks 24 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | tight end yards | 65.8 | 32.4 | 54.3 | CHI offence ranks 6 of 32, JAX defence ranks 1 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | running back rushing yards | 103.6 | 67.0 | 93.5 | CHI offence ranks 10 of 32, JAX defence ranks 4 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | explosive passes (20+) | 3.8 | 2.0 | 3.0 | CHI offence ranks 5 of 32, JAX defence ranks 2 of 32 (1 = best at its own job) |
| JAX DEFENCE ADVANTAGE | explosive runs (15+) | 0.9 | 0.9 | 1.2 | CHI offence ranks 25 of 32, JAX defence ranks 8 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | points | 26.5 | 17.1 | 23.3 | CHI offence ranks 9 of 32, JAX defence ranks 3 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | third-down conversions | 45.0% | 33.0% | 39.2% | CHI offence ranks 4 of 32, JAX defence ranks 5 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | red-zone touchdowns | 60.6% | 50.0% | 58.5% | CHI offence ranks 12 of 32, JAX defence ranks 4 of 32 (1 = best at its own job) |
| JAX DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 6.3% | 4.1% | 6.7% | CHI offence ranks 16 of 32, JAX defence ranks 30 of 32 (1 = best at its own job) |
| CHI OFFENCE ADVANTAGE | pressure (sacks + hits) | 12.6% | 13.9% | 15.7% | CHI offence ranks 5 of 32, JAX defence ranks 24 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | JAX 25.5 - CHI 22.3 | 47.8 | -3.2 | 49.6% | 39.6% | 36.1% | JAX 13.1 - CHI 10.5 |
| independent | JAX 27.9 - CHI 26.4 | 54.4 | -1.5 | 43.5% | 36.6% | 63.2% | JAX 14.9 - CHI 12.7 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### JAX offense vs CHI defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P.Washington | WR | receiving yards | 8 | 80.3 | 1.051 | 10.7 | 14.0 | 18.1 | 26.9 | 35.7 | 65.7 |
| P.Washington | WR | receptions | 8 | 4.1 | 0.962 | 1.0 | 1.0 | 1.0 | 1.3 | 1.7 | 3.4 |
| J.Meyers | WR | receiving yards | 8 | 57.0 | 1.051 | 28.5 | 31.9 | 34.7 | 35.1 | 35.5 | 53.1 |
| J.Meyers | WR | receptions | 8 | 3.5 | 0.962 | 1.9 | 1.9 | 2.0 | 2.3 | 2.6 | 3.4 |
| B.Strange | TE | receiving yards | 8 | 36.8 | 0.954 | 10.9 | 13.3 | 15.5 | 17.5 | 19.5 | 36.2 |
| B.Strange | TE | receptions | 8 | 3.3 | 0.923 | 1.8 | 1.8 | 1.8 | 1.8 | 1.8 | 2.8 |
| J.Cameron | WR | receiving yards | 7 | 34.0 | 1.051 | 1.9 | 3.8 | 5.7 | 7.6 | 9.5 | 44.2 |
| J.Cameron | WR | receptions | 7 | 1.9 | 0.962 | 0.3 | 0.6 | 0.9 | 1.0 | 1.0 | 1.9 |
| B.Tuten | RB | rushing yards | 8 | 60.6 | 0.974 | 29.6 | 31.0 | 32.4 | 34.5 | 36.5 | 70.6 |
| C.Rodriguez | RB | rushing yards | 8 | 26.3 | 0.974 | 4.9 | 4.9 | 5.6 | 10.3 | 15.1 | 30.7 |
| A.Abdullah | RB | rushing yards | 3 | 17.6 | 0.974 | 3.0 | 4.1 | 5.2 | 6.2 | 7.3 | 12.7 |
| T.Lawrence | QB | passing yards | 8 | 282.5 | 1.026 | 196.8 | 206.8 | 216.3 | 222.4 | 228.5 | 278.6 |

### CHI offense vs JAX defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L.Burden | WR | receiving yards | 8 | 68.8 | 1.052 | 23.0 | 35.5 | 46.4 | 47.5 | 48.6 | 62.6 |
| L.Burden | WR | receptions | 8 | 5.1 | 1.073 | 2.5 | 2.9 | 3.3 | 3.6 | 4.0 | 4.3 |
| C.Loveland | TE | receiving yards | 8 | 36.8 | 0.85 | 8.4 | 12.6 | 16.6 | 19.6 | 22.5 | 47.2 |
| C.Loveland | TE | receptions | 8 | 3.9 | 0.899 | 1.2 | 1.5 | 1.8 | 2.2 | 2.5 | 4.5 |
| R.Odunze | WR | receiving yards | 8 | 68.8 | 1.052 | 41.4 | 41.8 | 42.3 | 44.2 | 46.0 | 67.8 |
| R.Odunze | WR | receptions | 8 | 4.6 | 1.073 | 3.2 | 3.2 | 3.3 | 3.6 | 4.0 | 4.3 |
| D.Swift | RB | receiving yards | 8 | 26.4 | 0.975 | 2.7 | 5.5 | 7.9 | 8.6 | 9.3 | 13.7 |
| D.Swift | RB | receptions | 8 | 3.5 | 1.087 | 0.8 | 1.5 | 2.2 | 2.2 | 2.2 | 3.3 |
| K.Raymond | WR | receiving yards | 8 | 15.7 | 1.052 | 2.2 | 4.4 | 6.3 | 6.3 | 6.3 | 14.7 |
| K.Raymond | WR | receptions | 8 | 2.3 | 1.073 | 0.4 | 0.8 | 1.1 | 1.5 | 1.9 | 2.1 |
| D.Swift | RB | rushing yards | 8 | 47.3 | 0.858 | 30.2 | 33.8 | 36.9 | 37.2 | 37.5 | 46.8 |
| K.Monangai | RB | rushing yards | 3 | 38.7 | 0.858 | 13.1 | 13.4 | 13.6 | 13.9 | 14.2 | 15.4 |
| R.Johnson | RB | rushing yards | 5 | 17.9 | 0.858 | 6.4 | 7.6 | 8.8 | 10.0 | 11.2 | 13.7 |
| C.Williams | QB | passing yards | 6 | 270.9 | 0.982 | 194.0 | 210.2 | 226.4 | 242.6 | 250.5 | 286.8 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## JAX (last 8 games: weeks 3, 4, 5, 6, 8, 9, 10, 11)

### JAX defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 17.1 | 3/32 | 23.3 |
| Pass yards allowed / game | 227.2 | 12/32 | 235.6 |
| Yards per pass attempt allowed | 6.36 | 8/32 | 7.15 |
| Rush yards allowed / game | 72.4 | 4/32 | 100.5 |
| Yards per carry allowed | 3.53 | 6/32 | 4.10 |
| RB rush yards allowed / game | 67.0 | 4/32 | 93.5 |
| WR yards allowed / game | 163.0 | 24/32 | 147.7 |
| WR receptions allowed / game | 13.0 | 26/32 | 11.4 |
| TE yards allowed / game | 32.4 | 1/32 | 54.3 |
| TE receptions allowed / game | 4.2 | 3/32 | 5.3 |
| RB receiving yards allowed / game | 31.9 | 14/32 | 33.5 |
| RB receptions allowed / game | 5.2 | 25/32 | 4.5 |
| Explosive passes (20+) allowed / game | 2.00 | 2/32 | 2.97 |
| Explosive runs (15+) allowed / game | 0.88 | 8/32 | 1.22 |
| Sack rate | 4.1% | 30/32 | 6.7% |
| Pressure rate (sacks + hits) | 13.9% | 24/32 | 15.7% |
| Third-down conversions allowed | 33.0% | 5/32 | 39.2% |
| Red-zone TD rate allowed | 50.0% | 4/32 | 58.5% |
| Takeaways / game | 1.62 | 4/32 | 1.22 |

Blitz rate 30.1% and play-action faced 20.6% on 316 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.6 per game, 27.6% completed.

### JAX defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs NE | 6 | 245 | 64 | 63 | 12-209 | 1-5 | 5-31 | 5 | 0 | 3 |
| 4 | @ CIN | 17 | 428 | 18 | 17 | 24-315 | 4-42 | 11-71 | 3 | 0 | 2 |
| 5 | vs PHI | 17 | 220 | 20 | 20 | 12-177 | 6-38 | 3-5 | 1 | 0 | 1 |
| 6 | vs HOU | 34 | 312 | 109 | 99 | 14-241 | 7-39 | 3-32 | 4 | 1 | 0 |
| 8 | vs IND | 7 | 152 | 98 | 95 | 13-110 | 4-18 | 4-24 | 0 | 2 | 4 |
| 9 | @ BAL | 10 | 57 | 163 | 142 | 5-26 | 3-24 | 3-7 | 0 | 1 | 1 |
| 10 | @ TEN | 23 | 231 | 66 | 61 | 13-136 | 6-29 | 9-66 | 2 | 2 | 1 |
| 11 | @ NYG | 23 | 173 | 41 | 39 | 11-90 | 3-64 | 4-19 | 1 | 1 | 1 |

### Best individual lines allowed by JAX

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | NE | M.Hollins (WR) 6/9 for 87, 0 TD | T.Henderson (RB) 8 for 23, 0 TD |
| 4 | CIN | T.Higgins (WR) 11/16 for 157, 0 TD | C.Brown (RB) 9 for 10, 0 TD |
| 5 | PHI | D.Cooper (WR) 2/3 for 71, 1 TD | D.Pierce (RB) 11 for 14, 0 TD |
| 6 | HOU | J.Noel (WR) 4/4 for 107, 1 TD | W.Marks (RB) 15 for 56, 0 TD |
| 8 | IND | K.Allen (WR) 7/7 for 67, 0 TD | D.Giddens (RB) 6 for 43, 0 TD |
| 9 | BAL | M.Andrews (TE) 2/2 for 19, 0 TD | J.Hill (RB) 9 for 85, 1 TD |
| 10 | TEN | E.Ayomanor (WR) 5/10 for 79, 0 TD | T.Pollard (RB) 9 for 33, 0 TD |
| 11 | NYG | M.Nabers (WR) 7/12 for 55, 1 TD | C.Skattebo (RB) 14 for 34, 0 TD |

### JAX run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 41 | 115 | 2.8 | 1 |
| right end | 25 | 90 | 3.6 | 1 |
| left end | 22 | 68 | 3.09 | 0 |
| left tackle | 21 | 96 | 4.57 | 1 |
| left guard | 20 | 34 | 1.7 | 0 |
| right tackle | 19 | 146 | 7.68 | 2 |
| right guard | 12 | 30 | 2.5 | 0 |

### JAX defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Jarrian Jones | 7 | 46 | 26 | 330 | 7.2 | 0 | 1 | 4 |
| Foyesade Oluokun | 8 | 40 | 33 | 256 | 6.4 | 2 | 1 | 6 |
| Travis Hunter | 8 | 38 | 25 | 345 | 9.1 | 0 | 3 | 4 |
| Ventrell Miller | 8 | 31 | 19 | 137 | 4.4 | 0 | 0 | 6 |
| Antonio Johnson | 7 | 27 | 14 | 145 | 5.4 | 1 | 0 | 1 |
| Jourdan Lewis | 8 | 26 | 12 | 81 | 3.1 | 1 | 2 | 1 |
| Montaric Brown | 6 | 23 | 14 | 165 | 7.2 | 1 | 1 | 1 |
| Rayuan Lane | 6 | 18 | 11 | 138 | 7.7 | 1 | 1 | 2 |
| Branson Combs | 3 | 7 | 5 | 64 | 9.1 | 0 | 1 | 1 |
| Eric Murray | 3 | 7 | 5 | 56 | 8.0 | 2 | 0 | 0 |

### JAX pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Josh Hines-Allen | 8 | 15 | 1.5 | 6 | 5 |
| Travon Walker | 7 | 14 | 1.5 | 7 | 4 |
| Foyesade Oluokun | 8 | 9 | 2.0 | 2 | 28 |
| Arik Armstead | 4 | 6 | 1.5 | 3 | 0 |
| Ruke Orhorhoro | 3 | 4 | 1.0 | 2 | 0 |
| Antonio Johnson | 7 | 3 | 1.5 | 1 | 25 |
| Ventrell Miller | 8 | 3 | 0.0 | 1 | 19 |
| Rayuan Lane | 6 | 3 | 0.0 | 2 | 10 |

### JAX offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 30.0 | 4/32 | 23.3 |
| Pass yards / game | 269.9 | 5/32 | 234.4 |
| Yards per pass attempt | 8.47 | 3/32 | 7.13 |
| Rush yards / game | 105.8 | 13/32 | 101.0 |
| Yards per carry | 3.99 | 19/32 | 4.11 |
| RB rush yards / game | 97.8 | 13/32 | 93.8 |
| WR yards / game | 172.0 | 7/32 | 147.6 |
| TE yards / game | 64.9 | 8/32 | 53.3 |
| RB receiving yards / game | 33.0 | 15/32 | 33.4 |
| Explosive passes (20+) / game | 3.88 | 3/32 | 2.98 |
| Explosive runs (15+) / game | 1.25 | 13/32 | 1.22 |
| Sack rate allowed | 5.0% | 9/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 14.6% | 12/32 | 15.4% |
| Third-down conversion rate | 45.2% | 3/32 | 39.4% |
| Red-zone TD rate | 55.2% | 22/32 | 58.9% |

Neutral-situation pass rate 53.2%; 61.5 plays per game; target share WR 64% / TE 22% / RB 14%.

### JAX offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs NE | 35 | 182 | 129 | 112 | 12-124 | 3-32 | 4-26 | 1 | 1 | 1 |
| 4 | @ CIN | 22 | 227 | 113 | 108 | 8-99 | 8-110 | 2-18 | 3 | 3 | 4 |
| 5 | vs PHI | 19 | 331 | 77 | 77 | 12-213 | 9-88 | 3-30 | 4 | 1 | 2 |
| 6 | vs HOU | 31 | 306 | 95 | 95 | 13-206 | 7-52 | 4-48 | 6 | 0 | 0 |
| 8 | vs IND | 42 | 218 | 175 | 158 | 4-52 | 4-94 | 3-72 | 4 | 2 | 3 |
| 9 | @ BAL | 33 | 242 | 78 | 78 | 8-131 | 6-98 | 2-13 | 2 | 0 | 0 |
| 10 | @ TEN | 40 | 352 | 101 | 93 | 18-298 | 4-29 | 3-25 | 6 | 2 | 1 |
| 11 | @ NYG | 18 | 301 | 78 | 61 | 17-253 | 3-16 | 5-32 | 5 | 1 | 3 |

**QB T.Lawrence** (8 games): 161/252, 2151 yds, 18 TD, 6 INT, 14 sacks, 8.54 yds/att, depth of target 8.7, pressured on 15.4% of dropbacks. Yards by game: W3 182, W4 227, W5 331, W6 306, W8 210, W9 242, W10 352, W11 301.

**QB Q.Ewers** (1 games): 1/3, 8 yds, 0 TD, 0 INT, 0 sacks, 2.67 yds/att, depth of target 12.3, pressured on 0.0% of dropbacks. Yards by game: W8 8.

### JAX receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P.Washington | WR | 8 | 63 | 32 | 567 | 5 | 25% | 36% | 12.7 | 15 | 10 | 40 7 124 64 16 61 152 103 |
| J.Meyers | WR | 8 | 50 | 30 | 425 | 1 | 20% | 25% | 11.1 | 13 | 6 | 64 33 37 83 24 65 34 85 |
| B.Strange | TE | 8 | 38 | 31 | 341 | 1 | 15% | 13% | 7.6 | 3 | 5 | 32 95 68 44 55 22 9 16 |
| J.Cameron | WR | 7 | 22 | 13 | 214 | 2 | 9% | 10% | 10.2 | 3 | 4 | 12 42 43 0 6 67 44 |
| B.Tuten | RB | 7 | 20 | 18 | 207 | 3 | 8% | -2% | -2.5 | 3 | 3 | 17 18 24 48 55 25 20 |
| Bri.Thomas | WR | 7 | 17 | 8 | 84 | 3 | 7% | 10% | 12.9 | 6 | 0 | 8 17 0 0 12 29 18 |
| N.Boerkircher | TE | 7 | 13 | 9 | 147 | 2 | 5% | 5% | 9.2 | 4 | 2 | 0 15 20 8 31 61 12 |
| T.Hunter | WR | 6 | 10 | 9 | 86 | 1 | 4% | 1% | 2.5 | 2 | 1 | 9 59 0 -1 16 3 |
| L.Allen | RB | 5 | 8 | 3 | 8 | 0 | 3% | 1% | 1.9 | 0 | 0 | 9 0 0 0 -1 |

### JAX rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| B.Tuten | RB | 8 | 130 | 511 | 3.93 | 4 | 61% | 29 | 4 | 73 73 72 39 104 29 88 33 |
| C.Rodriguez | RB | 8 | 51 | 225 | 4.41 | 4 | 24% | 11 | 3 | 37 35 5 55 41 19 5 28 |
| A.Abdullah | RB | 3 | 16 | 45 | 2.81 | 0 | 8% | 4 | 0 | 2 13 30 |
| T.Lawrence | QB | 7 | 8 | 34 | 4.25 | 0 | 4% | 2 | 1 | 17 2 0 0 2 5 8 |
| T.Hunter | WR | 3 | 3 | 17 | 5.67 | 0 | 1% | 0 | 0 | 5 3 9 |

### JAX run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 44 | 192 | 4.36 | 2 |
| right tackle | 33 | 147 | 4.45 | 1 |
| left guard | 33 | 160 | 4.85 | 2 |
| right guard | 32 | 88 | 2.75 | 0 |
| left end | 26 | 101 | 3.88 | 2 |
| left tackle | 23 | 87 | 3.78 | 0 |
| right end | 20 | 64 | 3.2 | 1 |

### JAX by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 256 | 52% | 80% | 6.08 | 0.092 |
| offense | Under center | 222 | 45% | 28% | 5.71 | 0.148 |
| offense | No huddle | 14 | 3% | 93% | 9.79 | 0.153 |
| defense vs | Shotgun | 305 | 64% | 77% | 5.56 | -0.143 |
| defense vs | Under center | 123 | 26% | 31% | 3.4 | -0.145 |
| defense vs | No huddle | 52 | 11% | 85% | 6.54 | 0.11 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 94 | 37% | 62% | 6.16 | 4 |
| offense | Short middle | 53 | 21% | 68% | 9.19 | 4 |
| offense | Short right | 64 | 25% | 72% | 7.44 | 4 |
| offense | Deep left | 21 | 8% | 57% | 15.67 | 10 |
| offense | Deep middle | 9 | 4% | 44% | 9.89 | 3 |
| offense | Deep right | 14 | 6% | 43% | 14.21 | 6 |
| defense allows | Short left | 89 | 31% | 67% | 4.85 | 2 |
| defense allows | Short middle | 50 | 18% | 64% | 6.94 | 2 |
| defense allows | Short right | 98 | 34% | 71% | 5.23 | 1 |
| defense allows | Deep left | 18 | 6% | 33% | 9.17 | 3 |
| defense allows | Deep middle | 8 | 3% | 38% | 11.0 | 2 |
| defense allows | Deep right | 23 | 8% | 39% | 11.87 | 6 |

### JAX lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Walker Little, LG Emmanuel Pregnon, C Robert Hainsey, RG Ezra Cleveland, RT Cole Van Lanen.  
Defensive front: LDE Travon Walker, LDT Arik Armstead, RDT Jordan Davis, RDE Josh Hines-Allen, WLB Foyesade Oluokun, SLB Dennis Gardeck.

### JAX injuries

Official report not posted yet for this week.

ESPN live list (designations only): Matt Dickerson (DE) Questionable; Robert Hainsey (C) Questionable; Jakobi Meyers (WR) Questionable; Cole Van Lanen (OT) Questionable; Jonah Monheim (C) Questionable; Dennis Gardeck (LB) Questionable; Patrick Mekari (G) Injured Reserve; Parker Washington (WR) Out; Bhayshul Tuten (RB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### JAX roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Joey Aguilar (QB) to ARI.

## CHI (last 8 games: weeks 4, 5, 6, 7, 8, 9, 11, 12)

### CHI defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 22.4 | 15/32 | 23.3 |
| Pass yards allowed / game | 247.9 | 21/32 | 235.6 |
| Yards per pass attempt allowed | 7.84 | 25/32 | 7.15 |
| Rush yards allowed / game | 92.8 | 13/32 | 100.5 |
| Yards per carry allowed | 4.79 | 29/32 | 4.10 |
| RB rush yards allowed / game | 88.6 | 13/32 | 93.5 |
| WR yards allowed / game | 162.9 | 23/32 | 147.7 |
| WR receptions allowed / game | 10.5 | 12/32 | 11.4 |
| TE yards allowed / game | 49.2 | 12/32 | 54.3 |
| TE receptions allowed / game | 4.5 | 5/32 | 5.3 |
| RB receiving yards allowed / game | 35.8 | 17/32 | 33.5 |
| RB receptions allowed / game | 5.1 | 24/32 | 4.5 |
| Explosive passes (20+) allowed / game | 3.00 | 17/32 | 2.97 |
| Explosive runs (15+) allowed / game | 1.12 | 14/32 | 1.22 |
| Sack rate | 8.9% | 3/32 | 6.7% |
| Pressure rate (sacks + hits) | 17.5% | 6/32 | 15.7% |
| Third-down conversions allowed | 27.0% | 2/32 | 39.2% |
| Red-zone TD rate allowed | 54.2% | 12/32 | 58.5% |
| Takeaways / game | 1.00 | 19/32 | 1.22 |

Blitz rate 31.3% and play-action faced 23.0% on 252 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.0 per game, 50.0% completed.

### CHI defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | vs NYJ | 12 | 119 | 59 | 59 | 5-100 | 1-11 | 2-8 | 1 | 0 | 3 |
| 5 | @ GB | 31 | 367 | 66 | 64 | 16-286 | 5-64 | 4-17 | 6 | 1 | 2 |
| 6 | @ ATL | 23 | 225 | 62 | 62 | 9-158 | 6-66 | 4-1 | 4 | 1 | 5 |
| 7 | vs NE | 24 | 321 | 44 | 44 | 7-87 | 10-127 | 7-107 | 2 | 1 | 2 |
| 8 | @ SEA | 17 | 188 | 61 | 61 | 10-151 | 2-23 | 5-14 | 2 | 0 | 3 |
| 9 | vs TB | 24 | 243 | 126 | 113 | 7-130 | 4-25 | 7-88 | 3 | 1 | 4 |
| 11 | vs NO | 13 | 222 | 86 | 82 | 17-184 | 3-25 | 5-13 | 1 | 2 | 6 |
| 12 | @ DET | 35 | 298 | 238 | 224 | 13-207 | 5-53 | 7-38 | 5 | 3 | 1 |

### Best individual lines allowed by CHI

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 4 | NYJ | I.Williams (WR) 2/3 for 73, 1 TD | B.Allen (RB) 14 for 59, 0 TD |
| 5 | GB | C.Watson (WR) 6/8 for 143, 2 TD | M.Lloyd (RB) 10 for 31, 2 TD |
| 6 | ATL | J.Dotson (WR) 3/5 for 87, 1 TD | Bi.Robinson (RB) 9 for 61, 0 TD |
| 7 | NE | R.Stevenson (RB) 5/5 for 93, 1 TD | R.Stevenson (RB) 6 for 22, 0 TD |
| 8 | SEA | J.Smith-Njigba (WR) 6/11 for 118, 1 TD | J.Price (RB) 10 for 29, 0 TD |
| 9 | TB | T.Johnson (WR) 2/5 for 76, 0 TD | B.Irving (RB) 20 for 97, 2 TD |
| 11 | NO | C.Olave (WR) 9/15 for 102, 0 TD | T.Etienne (RB) 14 for 76, 0 TD |
| 12 | DET | A.St. Brown (WR) 7/10 for 146, 0 TD | J.Gibbs (RB) 21 for 205, 3 TD |

### CHI run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| left tackle | 30 | 227 | 7.57 | 4 |
| left guard | 28 | 97 | 3.46 | 0 |
| middle | 23 | 111 | 4.83 | 0 |
| right guard | 22 | 89 | 4.05 | 1 |
| right tackle | 21 | 101 | 4.81 | 1 |
| left end | 20 | 85 | 4.25 | 1 |
| right end | 11 | 32 | 2.91 | 0 |

### CHI defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Devin Bush Jr. | 7 | 34 | 22 | 189 | 5.6 | 2 | 0 | 1 |
| Tyrique Stevenson | 6 | 34 | 19 | 276 | 8.1 | 2 | 0 | 3 |
| Jaylon Johnson | 7 | 32 | 20 | 316 | 9.9 | 1 | 1 | 7 |
| Dillon Thieneman | 7 | 17 | 9 | 117 | 6.9 | 1 | 1 | 5 |
| Cameron Lewis | 6 | 15 | 11 | 139 | 9.3 | 2 | 1 | 2 |
| Malik Muhammad | 4 | 15 | 9 | 154 | 10.3 | 1 | 0 | 1 |
| Kyler Gordon | 4 | 14 | 8 | 124 | 8.9 | 0 | 0 | 0 |
| T.J. Edwards | 5 | 13 | 9 | 83 | 6.4 | 0 | 0 | 1 |
| D'Marco Jackson | 3 | 8 | 4 | 36 | 4.5 | 0 | 1 | 1 |
| Clark Phillips | 3 | 8 | 3 | 13 | 1.6 | 0 | 0 | 0 |

### CHI pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Montez Sweat | 5 | 11 | 2.0 | 2 | 0 |
| Austin Booker | 5 | 10 | 4.0 | 3 | 1 |
| Grady Jarrett | 6 | 5 | 0.5 | 1 | 0 |
| Daniel Hardy | 3 | 5 | 2.0 | 0 | 0 |
| Jeffery Simmons | 3 | 5 | 5.0 | 0 | 0 |
| Kyler Gordon | 4 | 5 | 4.0 | 0 | 14 |
| Cameron Lewis | 6 | 3 | 1.0 | 1 | 5 |
| Devin Bush Jr. | 7 | 3 | 2.0 | 1 | 24 |

### CHI offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 26.5 | 9/32 | 23.3 |
| Pass yards / game | 266.0 | 8/32 | 234.4 |
| Yards per pass attempt | 7.57 | 12/32 | 7.13 |
| Rush yards / game | 117.8 | 7/32 | 101.0 |
| Yards per carry | 4.11 | 15/32 | 4.11 |
| RB rush yards / game | 103.6 | 10/32 | 93.8 |
| WR yards / game | 161.8 | 10/32 | 147.6 |
| TE yards / game | 65.8 | 6/32 | 53.3 |
| RB receiving yards / game | 38.5 | 10/32 | 33.4 |
| Explosive passes (20+) / game | 3.75 | 5/32 | 2.98 |
| Explosive runs (15+) / game | 0.88 | 25/32 | 1.22 |
| Sack rate allowed | 6.3% | 16/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 12.6% | 5/32 | 15.4% |
| Third-down conversion rate | 45.0% | 4/32 | 39.4% |
| Red-zone TD rate | 60.6% | 12/32 | 58.9% |

Neutral-situation pass rate 55.4%; 68.2 plays per game; target share WR 55% / TE 28% / RB 18%.

### CHI offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | vs NYJ | 23 | 268 | 231 | 220 | 12-163 | 9-78 | 4-27 | 5 | 2 | 1 |
| 5 | @ GB | 7 | 195 | 67 | 49 | 11-104 | 3-27 | 9-64 | 2 | 0 | 4 |
| 6 | @ ATL | 31 | 305 | 97 | 95 | 16-189 | 8-68 | 6-48 | 3 | 0 | 4 |
| 7 | vs NE | 30 | 308 | 98 | 91 | 8-199 | 10-97 | 4-12 | 8 | 0 | 3 |
| 8 | @ SEA | 34 | 247 | 125 | 86 | 14-161 | 7-65 | 3-21 | 4 | 1 | 1 |
| 9 | vs TB | 27 | 279 | 56 | 56 | 16-202 | 6-77 | 0-0 | 4 | 0 | 1 |
| 11 | vs NO | 21 | 181 | 135 | 102 | 9-125 | 4-48 | 2-8 | 1 | 2 | 2 |
| 12 | @ DET | 39 | 345 | 133 | 130 | 12-151 | 8-66 | 10-128 | 3 | 2 | 4 |

**QB C.Williams** (6 games): 143/207, 1665 yds, 10 TD, 5 INT, 15 sacks, 8.04 yds/att, depth of target 8.3, pressured on 13.1% of dropbacks. Yards by game: W6 305, W7 308, W8 247, W9 279, W11 181, W12 345.

**QB T.Bagent** (2 games): 37/55, 355 yds, 0 TD, 3 INT, 3 sacks, 6.45 yds/att, depth of target 6.6, pressured on 10.3% of dropbacks. Yards by game: W4 268, W5 87.

### CHI receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L.Burden | WR | 8 | 53 | 39 | 542 | 3 | 20% | 20% | 8.2 | 5 | 13 | 63 47 95 130 56 97 10 44 |
| C.Loveland | TE | 8 | 52 | 36 | 363 | 3 | 19% | 16% | 6.8 | 9 | 2 | 57 19 65 69 65 54 29 5 |
| R.Odunze | WR | 8 | 51 | 34 | 521 | 3 | 19% | 34% | 14.5 | 9 | 13 | 94 40 39 69 87 60 45 87 |
| D.Swift | RB | 8 | 30 | 25 | 199 | 1 | 11% | -0% | -0.2 | 3 | 1 | 16 30 26 12 10 0 8 97 |
| K.Raymond | WR | 8 | 29 | 17 | 110 | 0 | 11% | 11% | 8.3 | 3 | 0 | 6 6 18 0 14 32 14 20 |
| Z.Thomas | WR | 5 | 12 | 8 | 109 | 0 | 4% | 10% | 18.4 | 0 | 1 | 11 25 4 13 56 |
| R.Johnson | RB | 4 | 11 | 9 | 86 | 0 | 4% | 1% | 2.3 | 2 | 0 | 7 34 34 11 |
| C.Kmet | TE | 4 | 9 | 8 | 52 | 0 | 3% | 1% | 3.2 | 1 | 0 | 13 8 3 28 |
| S.Roush | TE | 4 | 9 | 9 | 81 | 0 | 3% | 2% | 3.7 | 0 | 0 | 8 23 19 31 |

### CHI rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| D.Swift | RB | 8 | 123 | 439 | 3.57 | 8 | 54% | 27 | 1 | 58 43 44 78 69 31 51 65 |
| K.Monangai | RB | 3 | 46 | 179 | 3.89 | 4 | 20% | 13 | 2 | 146 18 15 |
| R.Johnson | RB | 5 | 29 | 103 | 3.55 | 1 | 13% | 11 | 0 | 16 6 51 13 17 |
| S.Ahmed | RB | 3 | 14 | 108 | 7.71 | 0 | 6% | 1 | 2 | 25 33 50 |
| L.Burden | WR | 5 | 8 | 24 | 3.00 | 0 | 3% | 3 | 0 | 11 2 7 3 1 |

### CHI run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| right guard | 46 | 163 | 3.54 | 1 |
| right tackle | 43 | 182 | 4.23 | 1 |
| right end | 36 | 220 | 6.11 | 3 |
| left guard | 35 | 102 | 2.91 | 0 |
| left end | 28 | 143 | 5.11 | 1 |
| middle | 25 | 57 | 2.28 | 0 |
| left tackle | 15 | 75 | 5.0 | 1 |

### CHI by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 291 | 53% | 73% | 6.11 | 0.015 |
| offense | Under center | 219 | 40% | 38% | 4.99 | -0.008 |
| offense | No huddle | 36 | 7% | 56% | 3.72 | 0.102 |
| defense vs | Shotgun | 252 | 56% | 80% | 5.73 | -0.087 |
| defense vs | Under center | 158 | 35% | 37% | 6.53 | 0.061 |
| defense vs | No huddle | 36 | 8% | 86% | 5.33 | -0.051 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 60 | 21% | 70% | 4.88 | 0 |
| offense | Short middle | 58 | 21% | 76% | 8.4 | 4 |
| offense | Short right | 103 | 37% | 78% | 6.91 | 6 |
| offense | Deep left | 18 | 6% | 56% | 15.17 | 7 |
| offense | Deep middle | 16 | 6% | 44% | 10.38 | 6 |
| offense | Deep right | 26 | 9% | 31% | 7.58 | 7 |
| defense allows | Short left | 89 | 35% | 58% | 4.16 | 0 |
| defense allows | Short middle | 38 | 15% | 82% | 5.89 | 0 |
| defense allows | Short right | 75 | 30% | 67% | 6.63 | 5 |
| defense allows | Deep left | 27 | 11% | 52% | 14.59 | 9 |
| defense allows | Deep middle | 9 | 4% | 100% | 36.56 | 6 |
| defense allows | Deep right | 15 | 6% | 33% | 11.27 | 4 |

### CHI lines (depth chart as of 2026-11-27T17:24:38Z)

Offensive line: LT Theo Benedet, LG Joe Thuney, C Garrett Bradbury, RG Jonah Jackson, RT Darnell Wright.  
Defensive front: LDE Montez Sweat, LDT Grady Jarrett, RDT Jeffery Simmons, RDE James Lynch, WLB Devin Bush, SLB Noah Sewell.

### CHI injuries

Official report not posted yet for this week.

ESPN live list (designations only): Roschon Johnson (RB) Out; Kyler Gordon (CB) Out; Isaac Yiadom (CB) Out; Jayden Loving (DT) Out; Jordan McFadden (G) Out; Elijah Hicks (S) Out; Case Keenum (QB) Out; Caleb Williams (QB) Questionable; Colston Loveland (TE) Doubtful.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### CHI roster moves (last 4 weeks)

Arrived: Isaac Yiadom (DB) from WAS.  
Left for another team: none.

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
