# JAX at CHI: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: outdoors; surface: grass. Rest: JAX 7 days, CHI 10 days. Listed QBs: Trevor Lawrence (JAX), Caleb Williams (CHI).

Market (schedule consensus, not a timestamped quote): CHI n/a, total n/a.

Generated 2026-11-26T19:39:46+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T14:01:05Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | CHI -2.5 | -115 | -105 | 51.1% | 48.9% | 4.7% | 2026-11-26T14:01:05+00:00 |
| total | fanduel | Over 50.5 | -105 | -115 | 48.9% | 51.1% | 4.7% | 2026-11-26T14:01:05+00:00 |
| moneyline | fanduel | CHI | -144 | +122 | 56.7% | 43.3% | 4.1% | 2026-11-26T14:01:05+00:00 |

Player props: OK.

## Matchup edges

### JAX offense vs CHI defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| JAX OFFENCE STRENGTH | explosive passes (20+) | 3.9 | 2.5 | 3.0 | JAX offence ranks 3 of 32, CHI defence ranks 6 of 32 (1 = best at its own job) |
| JAX OFFENCE STRENGTH | passing yards | 269.9 | 229.8 | 235.6 | JAX offence ranks 5 of 32, CHI defence ranks 15 of 32 (1 = best at its own job) |
| JAX OFFENCE STRENGTH | points | 30.0 | 18.9 | 23.0 | JAX offence ranks 4 of 32, CHI defence ranks 7 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | third-down conversions | 45.2% | 25.6% | 39.2% | JAX offence ranks 3 of 32, CHI defence ranks 2 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | red-zone touchdowns | 55.2% | 50.0% | 58.0% | JAX offence ranks 22 of 32, CHI defence ranks 4 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | sacks (pass protection vs pass rush) | 5.0% | 9.5% | 6.6% | JAX offence ranks 9 of 32, CHI defence ranks 2 of 32 (1 = best at its own job) |
| CHI DEFENCE STRENGTH | pressure (sacks + hits) | 14.6% | 18.0% | 15.7% | JAX offence ranks 12 of 32, CHI defence ranks 5 of 32 (1 = best at its own job) |

### CHI offense vs JAX defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| CHI OFFENCE ADVANTAGE | wide receiver yards | 167.4 | 163.0 | 147.8 | CHI offence ranks 8 of 32, JAX defence ranks 24 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | tight end yards | 63.4 | 32.4 | 54.7 | CHI offence ranks 9 of 32, JAX defence ranks 1 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | running back rushing yards | 101.8 | 67.0 | 92.5 | CHI offence ranks 11 of 32, JAX defence ranks 5 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | explosive passes (20+) | 3.8 | 2.0 | 3.0 | CHI offence ranks 6 of 32, JAX defence ranks 2 of 32 (1 = best at its own job) |
| JAX DEFENCE ADVANTAGE | explosive runs (15+) | 0.8 | 0.9 | 1.2 | CHI offence ranks 27 of 32, JAX defence ranks 8 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | points | 25.0 | 17.1 | 23.0 | CHI offence ranks 11 of 32, JAX defence ranks 3 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | third-down conversions | 43.6% | 33.0% | 39.2% | CHI offence ranks 5 of 32, JAX defence ranks 4 of 32 (1 = best at its own job) |
| JAX DEFENCE STRENGTH | red-zone touchdowns | 57.6% | 50.0% | 58.0% | CHI offence ranks 16 of 32, JAX defence ranks 4 of 32 (1 = best at its own job) |
| JAX DEFENCE WEAK SPOT | sacks (pass protection vs pass rush) | 5.3% | 4.1% | 6.6% | CHI offence ranks 11 of 32, JAX defence ranks 30 of 32 (1 = best at its own job) |
| CHI OFFENCE ADVANTAGE | pressure (sacks + hits) | 12.3% | 13.9% | 15.7% | CHI offence ranks 5 of 32, JAX defence ranks 23 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | JAX 25.3 - CHI 22.1 | 47.4 | -3.2 | 49.1% | n/a | n/a | JAX 13.0 - CHI 10.5 |
| independent | JAX 27.9 - CHI 26.0 | 53.9 | -2 | 41.9% | n/a | n/a | JAX 14.9 - CHI 12.8 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### JAX offense vs CHI defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P.Washington | WR | receiving yards | 8 | 77.7 | 1.017 | 10.3 | 13.5 | 17.5 | 26.0 | 34.6 | 63.5 |
| P.Washington | WR | receptions | 8 | 4.1 | 0.95 | 0.9 | 0.9 | 1.0 | 1.3 | 1.7 | 3.3 |
| J.Meyers | WR | receiving yards | 8 | 55.1 | 1.017 | 27.6 | 30.8 | 33.6 | 34.0 | 34.3 | 51.3 |
| J.Meyers | WR | receptions | 8 | 3.5 | 0.95 | 1.9 | 1.9 | 1.9 | 2.3 | 2.6 | 3.3 |
| B.Strange | TE | receiving yards | 8 | 35.0 | 0.905 | 10.4 | 12.6 | 14.7 | 16.6 | 18.5 | 34.4 |
| B.Strange | TE | receptions | 8 | 3.2 | 0.886 | 1.8 | 1.8 | 1.8 | 1.8 | 1.8 | 2.7 |
| J.Cameron | WR | receiving yards | 7 | 32.8 | 1.017 | 1.8 | 3.7 | 5.5 | 7.3 | 9.1 | 42.7 |
| J.Cameron | WR | receptions | 7 | 1.9 | 0.95 | 0.3 | 0.6 | 0.9 | 0.9 | 0.9 | 1.9 |
| B.Tuten | RB | rushing yards | 8 | 55.0 | 0.883 | 26.8 | 28.1 | 29.4 | 31.3 | 33.1 | 64.0 |
| C.Rodriguez | RB | rushing yards | 8 | 23.9 | 0.883 | 4.4 | 4.4 | 5.0 | 9.4 | 13.7 | 27.8 |
| A.Abdullah | RB | rushing yards | 3 | 16.0 | 0.883 | 2.7 | 3.7 | 4.7 | 5.7 | 6.6 | 11.5 |
| T.Lawrence | QB | passing yards | 8 | 272.0 | 0.988 | 189.4 | 199.1 | 208.2 | 214.1 | 220.0 | 268.1 |

### CHI offense vs JAX defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L.Burden | WR | receiving yards | 8 | 72.7 | 1.051 | 24.1 | 37.7 | 49.9 | 53.2 | 56.5 | 65.2 |
| L.Burden | WR | receptions | 8 | 5.7 | 1.07 | 2.9 | 3.6 | 4.3 | 4.3 | 4.3 | 5.9 |
| C.Loveland | TE | receiving yards | 8 | 41.9 | 0.85 | 19.1 | 22.1 | 24.7 | 25.3 | 25.9 | 47.2 |
| C.Loveland | TE | receptions | 8 | 4.4 | 0.898 | 2.1 | 2.4 | 2.7 | 3.1 | 3.4 | 4.5 |
| R.Odunze | WR | receiving yards | 8 | 62.9 | 1.051 | 41.4 | 41.7 | 42.3 | 43.7 | 45.2 | 55.2 |
| R.Odunze | WR | receptions | 8 | 4.2 | 1.07 | 3.2 | 3.2 | 3.2 | 3.2 | 3.2 | 4.3 |
| K.Raymond | WR | receiving yards | 8 | 21.2 | 1.051 | 2.2 | 4.4 | 6.3 | 6.3 | 6.3 | 14.7 |
| K.Raymond | WR | receptions | 8 | 2.5 | 1.07 | 0.4 | 0.7 | 1.1 | 1.5 | 1.9 | 2.1 |
| D.Swift | RB | receiving yards | 8 | 12.3 | 0.983 | 1.4 | 2.8 | 4.1 | 5.5 | 6.9 | 10.8 |
| D.Swift | RB | receptions | 8 | 2.6 | 1.091 | 0.8 | 1.5 | 2.2 | 2.2 | 2.2 | 2.2 |
| D.Swift | RB | rushing yards | 8 | 48.1 | 0.862 | 30.3 | 34.0 | 37.1 | 37.4 | 37.7 | 47.0 |
| K.Monangai | RB | rushing yards | 3 | 54.8 | 0.862 | 16.6 | 17.8 | 18.9 | 20.0 | 21.1 | 26.7 |
| R.Johnson | RB | rushing yards | 5 | 18.0 | 0.862 | 6.4 | 7.6 | 8.8 | 10.0 | 11.2 | 13.8 |
| C.Williams | QB | passing yards | 5 | 250.3 | 0.982 | 190.8 | 203.7 | 216.7 | 229.7 | 242.6 | 274.1 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## JAX (last 8 games: weeks 3, 4, 5, 6, 8, 9, 10, 11)

### JAX defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 17.1 | 3/32 | 23.0 |
| Pass yards allowed / game | 227.2 | 11/32 | 235.6 |
| Yards per pass attempt allowed | 6.36 | 7/32 | 7.14 |
| Rush yards allowed / game | 72.4 | 5/32 | 99.5 |
| Yards per carry allowed | 3.53 | 7/32 | 4.07 |
| RB rush yards allowed / game | 67.0 | 5/32 | 92.5 |
| WR yards allowed / game | 163.0 | 24/32 | 147.8 |
| WR receptions allowed / game | 13.0 | 27/32 | 11.4 |
| TE yards allowed / game | 32.4 | 1/32 | 54.7 |
| TE receptions allowed / game | 4.2 | 4/32 | 5.3 |
| RB receiving yards allowed / game | 31.9 | 14/32 | 33.0 |
| RB receptions allowed / game | 5.2 | 24/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.00 | 2/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.88 | 8/32 | 1.21 |
| Sack rate | 4.1% | 30/32 | 6.6% |
| Pressure rate (sacks + hits) | 13.9% | 23/32 | 15.7% |
| Third-down conversions allowed | 33.0% | 4/32 | 39.2% |
| Red-zone TD rate allowed | 50.0% | 4/32 | 58.0% |
| Takeaways / game | 1.62 | 5/32 | 1.23 |

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
| Points / game | 30.0 | 4/32 | 23.2 |
| Pass yards / game | 269.9 | 5/32 | 234.2 |
| Yards per pass attempt | 8.47 | 3/32 | 7.12 |
| Rush yards / game | 105.8 | 13/32 | 100.6 |
| Yards per carry | 3.99 | 18/32 | 4.10 |
| RB rush yards / game | 97.8 | 13/32 | 93.4 |
| WR yards / game | 172.0 | 6/32 | 147.5 |
| TE yards / game | 64.9 | 7/32 | 53.4 |
| RB receiving yards / game | 33.0 | 14/32 | 33.2 |
| Explosive passes (20+) / game | 3.88 | 3/32 | 2.96 |
| Explosive runs (15+) / game | 1.25 | 14/32 | 1.23 |
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

### JAX lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Walker Little, LG Emmanuel Pregnon, C Robert Hainsey, RG Ezra Cleveland, RT Cole Van Lanen.  
Defensive front: LDE Travon Walker, LDT Arik Armstead, RDT Jordan Davis, RDE Josh Hines-Allen, WLB Foyesade Oluokun, SLB Dennis Gardeck.

### JAX injuries

Official report not posted yet for this week.

ESPN live list (designations only): Danny Striggow (DE) Questionable; Matt Dickerson (DE) Questionable; Robert Hainsey (C) Questionable; Jakobi Meyers (WR) Questionable; Cole Van Lanen (OT) Questionable; Jonah Monheim (C) Questionable; Dennis Gardeck (LB) Questionable; Bhayshul Tuten (RB) Questionable; Patrick Mekari (G) Injured Reserve.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### JAX roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Joey Aguilar (QB) to ARI.

## CHI (last 8 games: weeks 3, 4, 5, 6, 7, 8, 9, 11)

### CHI defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 18.9 | 7/32 | 23.0 |
| Pass yards allowed / game | 229.8 | 15/32 | 235.6 |
| Yards per pass attempt allowed | 7.56 | 22/32 | 7.14 |
| Rush yards allowed / game | 73.4 | 6/32 | 99.5 |
| Yards per carry allowed | 4.13 | 18/32 | 4.07 |
| RB rush yards allowed / game | 70.9 | 7/32 | 92.5 |
| WR yards allowed / game | 152.8 | 21/32 | 147.8 |
| WR receptions allowed / game | 10.2 | 9/32 | 11.4 |
| TE yards allowed / game | 44.2 | 7/32 | 54.7 |
| TE receptions allowed / game | 4.1 | 3/32 | 5.3 |
| RB receiving yards allowed / game | 32.8 | 16/32 | 33.0 |
| RB receptions allowed / game | 4.6 | 19/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.50 | 6/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.00 | 11/32 | 1.21 |
| Sack rate | 9.5% | 2/32 | 6.6% |
| Pressure rate (sacks + hits) | 18.0% | 5/32 | 15.7% |
| Third-down conversions allowed | 25.6% | 2/32 | 39.2% |
| Red-zone TD rate allowed | 50.0% | 4/32 | 58.0% |
| Takeaways / game | 1.25 | 12/32 | 1.23 |

Blitz rate 33.2% and play-action faced 22.3% on 283 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.5 per game, 46.4% completed.

### CHI defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs PHI | 7 | 153 | 83 | 82 | 11-126 | 2-13 | 3-14 | 1 | 2 | 2 |
| 4 | vs NYJ | 12 | 119 | 59 | 59 | 5-100 | 1-11 | 2-8 | 1 | 0 | 3 |
| 5 | @ GB | 31 | 367 | 66 | 64 | 16-286 | 5-64 | 4-17 | 6 | 1 | 2 |
| 6 | @ ATL | 23 | 225 | 62 | 62 | 9-158 | 6-66 | 4-1 | 4 | 1 | 5 |
| 7 | vs NE | 24 | 321 | 44 | 44 | 7-87 | 10-127 | 7-107 | 2 | 1 | 2 |
| 8 | @ SEA | 17 | 188 | 61 | 61 | 10-151 | 2-23 | 5-14 | 2 | 0 | 3 |
| 9 | vs TB | 24 | 243 | 126 | 113 | 7-130 | 4-25 | 7-88 | 3 | 1 | 4 |
| 11 | vs NO | 13 | 222 | 86 | 82 | 17-184 | 3-25 | 5-13 | 1 | 2 | 6 |

### Best individual lines allowed by CHI

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | PHI | D.Smith (WR) 6/8 for 65, 0 TD | S.Barkley (RB) 15 for 82, 0 TD |
| 4 | NYJ | I.Williams (WR) 2/3 for 73, 1 TD | B.Allen (RB) 14 for 59, 0 TD |
| 5 | GB | C.Watson (WR) 6/8 for 143, 2 TD | M.Lloyd (RB) 10 for 31, 2 TD |
| 6 | ATL | J.Dotson (WR) 3/5 for 87, 1 TD | Bi.Robinson (RB) 9 for 61, 0 TD |
| 7 | NE | R.Stevenson (RB) 5/5 for 93, 1 TD | R.Stevenson (RB) 6 for 22, 0 TD |
| 8 | SEA | J.Smith-Njigba (WR) 6/11 for 118, 1 TD | J.Price (RB) 10 for 29, 0 TD |
| 9 | TB | T.Johnson (WR) 2/5 for 76, 0 TD | B.Irving (RB) 20 for 97, 2 TD |
| 11 | NO | C.Olave (WR) 9/15 for 102, 0 TD | T.Etienne (RB) 14 for 76, 0 TD |

### CHI run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| left guard | 28 | 102 | 3.64 | 0 |
| left tackle | 26 | 128 | 4.92 | 2 |
| left end | 22 | 102 | 4.64 | 1 |
| right tackle | 20 | 69 | 3.45 | 0 |
| right guard | 19 | 70 | 3.68 | 1 |
| middle | 16 | 73 | 4.56 | 0 |
| right end | 11 | 43 | 3.91 | 1 |

### CHI defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Jaylon Johnson | 8 | 39 | 26 | 381 | 9.8 | 1 | 1 | 8 |
| Devin Bush Jr. | 8 | 35 | 22 | 200 | 5.7 | 2 | 0 | 1 |
| Tyrique Stevenson | 6 | 34 | 19 | 276 | 8.1 | 2 | 0 | 3 |
| Dillon Thieneman | 8 | 20 | 10 | 121 | 6.0 | 1 | 2 | 5 |
| Malik Muhammad | 5 | 19 | 12 | 197 | 10.4 | 1 | 0 | 2 |
| T.J. Edwards | 6 | 18 | 11 | 94 | 5.2 | 0 | 1 | 2 |
| Cameron Lewis | 7 | 16 | 12 | 152 | 9.5 | 2 | 1 | 3 |
| Kyler Gordon | 4 | 14 | 8 | 124 | 8.9 | 0 | 0 | 0 |
| D'Marco Jackson | 4 | 9 | 4 | 36 | 4.0 | 0 | 1 | 1 |
| Clark Phillips | 3 | 8 | 3 | 13 | 1.6 | 0 | 0 | 0 |

### CHI pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Montez Sweat | 6 | 12 | 3.0 | 2 | 0 |
| Austin Booker | 6 | 11 | 4.0 | 3 | 1 |
| Grady Jarrett | 7 | 6 | 0.5 | 2 | 0 |
| Jeffery Simmons | 3 | 5 | 5.0 | 0 | 0 |
| Daniel Hardy | 3 | 5 | 2.0 | 0 | 0 |
| Kyler Gordon | 4 | 5 | 4.0 | 0 | 14 |
| Dayo Odeyingbo | 2 | 4 | 2.0 | 2 | 0 |
| Devin Bush Jr. | 8 | 3 | 2.0 | 1 | 30 |

### CHI offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 25.0 | 11/32 | 23.2 |
| Pass yards / game | 253.8 | 12/32 | 234.2 |
| Yards per pass attempt | 7.49 | 11/32 | 7.12 |
| Rush yards / game | 116.5 | 7/32 | 100.6 |
| Yards per carry | 3.90 | 20/32 | 4.10 |
| RB rush yards / game | 101.8 | 11/32 | 93.4 |
| WR yards / game | 167.4 | 8/32 | 147.5 |
| TE yards / game | 63.4 | 9/32 | 53.4 |
| RB receiving yards / game | 23.0 | 25/32 | 33.2 |
| Explosive passes (20+) / game | 3.75 | 6/32 | 2.96 |
| Explosive runs (15+) / game | 0.75 | 27/32 | 1.23 |
| Sack rate allowed | 5.3% | 11/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 12.3% | 5/32 | 15.4% |
| Third-down conversion rate | 43.6% | 5/32 | 39.4% |
| Red-zone TD rate | 57.6% | 16/32 | 58.9% |

Neutral-situation pass rate 55.2%; 67.6 plays per game; target share WR 58% / TE 27% / RB 15%.

### CHI offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs PHI | 27 | 247 | 123 | 115 | 17-196 | 5-47 | 2-4 | 3 | 1 | 0 |
| 4 | vs NYJ | 23 | 268 | 231 | 220 | 12-163 | 9-78 | 4-27 | 5 | 2 | 1 |
| 5 | @ GB | 7 | 195 | 67 | 49 | 11-104 | 3-27 | 9-64 | 2 | 0 | 4 |
| 6 | @ ATL | 31 | 305 | 97 | 95 | 16-189 | 8-68 | 6-48 | 3 | 0 | 4 |
| 7 | vs NE | 30 | 308 | 98 | 91 | 8-199 | 10-97 | 4-12 | 8 | 0 | 3 |
| 8 | @ SEA | 34 | 247 | 125 | 86 | 14-161 | 7-65 | 3-21 | 4 | 1 | 1 |
| 9 | vs TB | 27 | 279 | 56 | 56 | 16-202 | 6-77 | 0-0 | 4 | 0 | 1 |
| 11 | vs NO | 21 | 181 | 135 | 102 | 9-125 | 4-48 | 2-8 | 1 | 2 | 2 |

**QB C.Williams** (5 games): 113/163, 1320 yds, 8 TD, 5 INT, 11 sacks, 8.10 yds/att, depth of target 8.3, pressured on 13.2% of dropbacks. Yards by game: W6 305, W7 308, W8 247, W9 279, W11 181.

**QB T.Bagent** (2 games): 37/55, 355 yds, 0 TD, 3 INT, 3 sacks, 6.45 yds/att, depth of target 6.6, pressured on 10.3% of dropbacks. Yards by game: W4 268, W5 87.

### CHI receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L.Burden | WR | 8 | 57 | 43 | 559 | 4 | 22% | 20% | 6.9 | 9 | 13 | 61 63 47 95 130 56 97 10 |
| C.Loveland | TE | 8 | 55 | 39 | 389 | 3 | 21% | 18% | 6.5 | 10 | 2 | 31 57 19 65 69 65 54 29 |
| R.Odunze | WR | 8 | 48 | 31 | 478 | 1 | 19% | 33% | 13.6 | 9 | 13 | 44 94 40 39 69 87 60 45 |
| K.Raymond | WR | 8 | 31 | 20 | 180 | 1 | 12% | 14% | 8.9 | 4 | 1 | 90 6 6 18 0 14 32 14 |
| D.Swift | RB | 8 | 25 | 20 | 106 | 1 | 10% | -1% | -0.8 | 2 | 0 | 4 16 30 26 12 10 0 8 |
| Z.Thomas | WR | 6 | 13 | 9 | 110 | 0 | 5% | 11% | 16.7 | 0 | 1 | 1 11 25 4 13 56 |
| R.Johnson | RB | 4 | 11 | 9 | 86 | 0 | 4% | 1% | 2.3 | 2 | 0 | 7 34 34 11 |
| C.Kmet | TE | 5 | 10 | 8 | 52 | 0 | 4% | 2% | 3.5 | 1 | 0 | 0 13 8 3 28 |
| S.Roush | TE | 4 | 5 | 5 | 66 | 0 | 2% | 1% | 5.0 | 0 | 0 | 16 8 23 19 |

### CHI rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| D.Swift | RB | 8 | 134 | 458 | 3.42 | 7 | 56% | 32 | 1 | 84 58 43 44 78 69 31 51 |
| K.Monangai | RB | 3 | 48 | 195 | 4.06 | 2 | 20% | 12 | 2 | 31 146 18 |
| R.Johnson | RB | 5 | 29 | 103 | 3.55 | 1 | 12% | 11 | 0 | 16 6 51 13 17 |
| S.Ahmed | RB | 2 | 11 | 58 | 5.27 | 0 | 5% | 1 | 1 | 25 33 |
| L.Burden | WR | 5 | 8 | 30 | 3.75 | 0 | 3% | 3 | 0 | 7 11 2 7 3 |

### CHI run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| right guard | 50 | 169 | 3.38 | 1 |
| right tackle | 44 | 176 | 4.0 | 1 |
| left guard | 39 | 119 | 3.05 | 0 |
| right end | 34 | 199 | 5.85 | 2 |
| left end | 29 | 143 | 4.93 | 1 |
| left tackle | 22 | 91 | 4.14 | 1 |
| middle | 20 | 35 | 1.75 | 0 |

### CHI by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 277 | 51% | 72% | 5.72 | -0.037 |
| offense | Under center | 234 | 43% | 38% | 5.35 | 0.028 |
| offense | No huddle | 30 | 6% | 50% | 2.9 | 0.108 |
| defense vs | Shotgun | 245 | 58% | 80% | 5.37 | -0.155 |
| defense vs | Under center | 138 | 32% | 36% | 5.89 | 0.032 |
| defense vs | No huddle | 42 | 10% | 86% | 6.05 | 0.017 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 61 | 22% | 74% | 5.34 | 1 |
| offense | Short middle | 61 | 22% | 75% | 8.72 | 5 |
| offense | Short right | 94 | 35% | 74% | 6.17 | 5 |
| offense | Deep left | 16 | 6% | 62% | 17.06 | 7 |
| offense | Deep middle | 15 | 6% | 47% | 11.07 | 6 |
| offense | Deep right | 24 | 9% | 29% | 6.38 | 6 |
| defense allows | Short left | 79 | 32% | 58% | 4.29 | 0 |
| defense allows | Short middle | 37 | 15% | 73% | 5.54 | 0 |
| defense allows | Short right | 83 | 34% | 69% | 6.58 | 5 |
| defense allows | Deep left | 21 | 9% | 43% | 13.43 | 6 |
| defense allows | Deep middle | 8 | 3% | 88% | 35.88 | 5 |
| defense allows | Deep right | 15 | 6% | 40% | 11.93 | 4 |

### CHI lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Theo Benedet, LG Joe Thuney, C Garrett Bradbury, RG Jonah Jackson, RT Darnell Wright.  
Defensive front: LDE Montez Sweat, LDT Grady Jarrett, RDT Jeffery Simmons, RDE James Lynch, WLB Devin Bush, SLB Noah Sewell.

### CHI injuries

Official report not posted yet for this week.

ESPN live list (designations only): Roschon Johnson (RB) Out; Kyler Gordon (CB) Out; Isaac Yiadom (CB) Out; Jayden Loving (DT) Out; Jordan McFadden (G) Out; Elijah Hicks (S) Out; Case Keenum (QB) Out; Colston Loveland (TE) Out.
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
