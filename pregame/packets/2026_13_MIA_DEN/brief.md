# MIA at DEN: Week 13, Sunday late window

**Sunday 2026-12-06, 16:05 ET.** Site: Home; roof: outdoors; surface: grass. Rest: MIA 7 days, DEN 9 days. Listed QBs: Kyle McCord (MIA), Bo Nix (DEN).

Market (schedule consensus, not a timestamped quote): DEN -14.5, total 39.5.

Generated 2026-11-26T11:17:35+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T10:45:27Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | DEN -14.5 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-26T10:45:27+00:00 |
| total | fanduel | Over 38.5 | -115 | -105 | 51.1% | 48.9% | 4.7% | 2026-11-26T10:45:27+00:00 |
| moneyline | fanduel | DEN | -1400 | +830 | 89.7% | 10.3% | 4.1% | 2026-11-26T10:45:27+00:00 |

Player props: OK.

## Matchup edges

### MIA offense vs DEN defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| DEN DEFENCE WEAK SPOT | tight end yards | 34.8 | 74.1 | 54.7 | MIA offence ranks 26 of 32, DEN defence ranks 31 of 32 (1 = best at its own job) |
| DEN DEFENCE WEAK SPOT | running back receiving yards | 18.0 | 53.4 | 33.0 | MIA offence ranks 30 of 32, DEN defence ranks 32 of 32 (1 = best at its own job) |
| MIA OFFENCE WEAK SPOT | explosive passes (20+) | 2.0 | 2.9 | 3.0 | MIA offence ranks 28 of 32, DEN defence ranks 12 of 32 (1 = best at its own job) |
| DEN DEFENCE WEAK SPOT | passing yards | 171.2 | 267.9 | 235.6 | MIA offence ranks 31 of 32, DEN defence ranks 28 of 32 (1 = best at its own job) |
| MIA OFFENCE WEAK SPOT | points | 16.4 | 20.8 | 23.0 | MIA offence ranks 30 of 32, DEN defence ranks 11 of 32 (1 = best at its own job) |
| DEN DEFENCE STRENGTH | pressure (sacks + hits) | 15.5% | 21.0% | 15.7% | MIA offence ranks 16 of 32, DEN defence ranks 2 of 32 (1 = best at its own job) |

### DEN offense vs MIA defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| MIA DEFENCE ADVANTAGE | wide receiver yards | 111.4 | 132.8 | 147.8 | DEN offence ranks 29 of 32, MIA defence ranks 8 of 32 (1 = best at its own job) |
| MIA DEFENCE WEAK SPOT | tight end yards | 30.5 | 58.8 | 54.7 | DEN offence ranks 29 of 32, MIA defence ranks 23 of 32 (1 = best at its own job) |
| DEN OFFENCE STRENGTH | running back receiving yards | 50.1 | 32.5 | 33.0 | DEN offence ranks 4 of 32, MIA defence ranks 15 of 32 (1 = best at its own job) |
| MIA DEFENCE WEAK SPOT | running back rushing yards | 76.8 | 109.5 | 92.5 | DEN offence ranks 25 of 32, MIA defence ranks 25 of 32 (1 = best at its own job) |
| DEN OFFENCE WEAK SPOT | explosive runs (15+) | 0.4 | 1.4 | 1.2 | DEN offence ranks 31 of 32, MIA defence ranks 18 of 32 (1 = best at its own job) |
| MIA DEFENCE ADVANTAGE | passing yards | 192.0 | 224.0 | 235.6 | DEN offence ranks 27 of 32, MIA defence ranks 9 of 32 (1 = best at its own job) |
| MIA DEFENCE WEAK SPOT | third-down conversions | 35.6% | 46.6% | 39.2% | DEN offence ranks 26 of 32, MIA defence ranks 29 of 32 (1 = best at its own job) |
| MIA DEFENCE STRENGTH | red-zone touchdowns | 72.0% | 50.0% | 58.0% | DEN offence ranks 5 of 32, MIA defence ranks 4 of 32 (1 = best at its own job) |
| DEN OFFENCE STRENGTH | sacks (pass protection vs pass rush) | 2.9% | 6.1% | 6.6% | DEN offence ranks 1 of 32, MIA defence ranks 19 of 32 (1 = best at its own job) |
| DEN OFFENCE STRENGTH | pressure (sacks + hits) | 7.9% | 16.7% | 15.7% | DEN offence ranks 2 of 32, MIA defence ranks 10 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | MIA 18.9 - DEN 24.2 | 43.1 | +5.3 | 75.2% | 18.7% | 63.1% | MIA 9.8 - DEN 10.5 |
| independent | MIA 18.7 - DEN 23.3 | 42.0 | +4.6 | 63.5% | 19.2% | 57.2% | MIA 10.4 - DEN 10.3 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### MIA offense vs DEN defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M.Washington | WR | receiving yards | 8 | 38.8 | 0.975 | 22.5 | 24.6 | 26.5 | 27.5 | 28.5 | 40.5 |
| M.Washington | WR | receptions | 8 | 3.8 | 0.999 | 2.3 | 2.7 | 3.0 | 3.0 | 3.0 | 4.0 |
| G.Dulcich | TE | receiving yards | 7 | 35.6 | 1.15 | 4.1 | 8.3 | 12.4 | 14.3 | 14.9 | 42.5 |
| G.Dulcich | TE | receptions | 7 | 3.2 | 1.15 | 0.7 | 1.4 | 2.1 | 2.3 | 2.3 | 4.6 |
| C.Douglas | WR | receiving yards | 5 | 53.7 | 0.975 | 31.8 | 34.3 | 36.8 | 39.4 | 41.9 | 68.2 |
| C.Douglas | WR | receptions | 5 | 3.4 | 0.999 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 3.0 |
| C.Bell | WR | receiving yards | 7 | 16.0 | 0.975 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 7.8 |
| C.Bell | WR | receptions | 7 | 1.6 | 0.999 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| K.Coleman | WR | receiving yards | 7 | 12.5 | 0.975 | 0.0 | 0.0 | 0.0 | 0.6 | 1.5 | 2.9 |
| K.Coleman | WR | receptions | 7 | 1.2 | 0.999 | 0.0 | 0.0 | 0.0 | 0.2 | 0.5 | 1.0 |
| O.Gordon | RB | receiving yards | 7 | 10.6 | 1.15 | -1.6 | -0.9 | -0.2 | 0.0 | 0.0 | 0.0 |
| O.Gordon | RB | receptions | 7 | 2.1 | 1.105 | 0.3 | 0.7 | 1.0 | 1.1 | 1.1 | 2.2 |
| O.Gordon | RB | rushing yards | 8 | 73.7 | 0.986 | 45.2 | 50.1 | 54.9 | 59.7 | 64.6 | 71.5 |

### DEN offense vs MIA defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| J.Waddle | WR | receiving yards | 8 | 32.7 | 0.949 | 12.5 | 15.5 | 18.2 | 19.2 | 20.2 | 28.0 |
| J.Waddle | WR | receptions | 8 | 2.7 | 0.933 | 1.3 | 1.6 | 1.9 | 1.9 | 1.9 | 2.8 |
| C.Sutton | WR | receiving yards | 8 | 27.4 | 0.949 | 1.3 | 2.7 | 4.5 | 9.1 | 13.8 | 30.4 |
| C.Sutton | WR | receptions | 8 | 2.4 | 0.933 | 0.3 | 0.7 | 1.0 | 1.3 | 1.6 | 2.3 |
| E.Engram | TE | receiving yards | 8 | 26.7 | 1.037 | 0.0 | 0.0 | 0.1 | 0.8 | 1.6 | 9.9 |
| E.Engram | TE | receptions | 8 | 2.7 | 1.061 | 0.0 | 0.0 | 0.1 | 0.4 | 0.8 | 1.6 |
| R.Harvey | RB | receiving yards | 5 | 38.1 | 0.992 | 6.2 | 12.3 | 18.5 | 24.6 | 30.8 | 40.7 |
| R.Harvey | RB | receptions | 5 | 3.9 | 1.049 | 0.4 | 0.8 | 1.3 | 1.7 | 2.1 | 3.1 |
| J.Dobbins | RB | rushing yards | 8 | 30.3 | 1.092 | 5.0 | 9.9 | 14.5 | 16.4 | 18.3 | 34.4 |
| J.Coleman | RB | rushing yards | 4 | 77.5 | 1.092 | 46.9 | 49.0 | 51.1 | 53.3 | 55.4 | 60.6 |
| B.Nix | QB | passing yards | 8 | 191.9 | 0.975 | 109.8 | 115.3 | 123.1 | 144.6 | 166.1 | 212.6 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## MIA (last 8 games: weeks 3, 4, 5, 7, 8, 9, 10, 11)

### MIA defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 23.5 | 19/32 | 23.0 |
| Pass yards allowed / game | 224.0 | 9/32 | 235.6 |
| Yards per pass attempt allowed | 7.56 | 21/32 | 7.14 |
| Rush yards allowed / game | 112.8 | 23/32 | 99.5 |
| Yards per carry allowed | 4.34 | 23/32 | 4.07 |
| RB rush yards allowed / game | 109.5 | 25/32 | 92.5 |
| WR yards allowed / game | 132.8 | 8/32 | 147.8 |
| WR receptions allowed / game | 9.9 | 8/32 | 11.4 |
| TE yards allowed / game | 58.8 | 23/32 | 54.7 |
| TE receptions allowed / game | 6.0 | 26/32 | 5.3 |
| RB receiving yards allowed / game | 32.5 | 15/32 | 33.0 |
| RB receptions allowed / game | 4.9 | 22/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.88 | 12/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.38 | 18/32 | 1.21 |
| Sack rate | 6.1% | 19/32 | 6.6% |
| Pressure rate (sacks + hits) | 16.7% | 10/32 | 15.7% |
| Third-down conversions allowed | 46.6% | 29/32 | 39.2% |
| Red-zone TD rate allowed | 50.0% | 4/32 | 58.0% |
| Takeaways / game | 1.12 | 16/32 | 1.23 |

Blitz rate 17.0% and play-action faced 25.0% on 264 charted dropbacks (FTN). Deep passes (20+ air yards) faced 3.1 per game, 48.0% completed.

### MIA defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs KC | 24 | 246 | 87 | 87 | 12-141 | 5-98 | 3-7 | 3 | 2 | 0 |
| 4 | @ MIN | 15 | 247 | 113 | 106 | 8-80 | 14-123 | 5-44 | 3 | 2 | 4 |
| 5 | vs CIN | 31 | 190 | 108 | 107 | 10-111 | 8-48 | 5-31 | 1 | 0 | 0 |
| 7 | @ NYJ | 25 | 287 | 108 | 108 | 7-141 | 7-67 | 9-79 | 4 | 3 | 2 |
| 8 | vs NE | 24 | 199 | 129 | 126 | 9-156 | 4-35 | 3-8 | 4 | 1 | 3 |
| 9 | vs DET | 19 | 181 | 98 | 88 | 12-142 | 4-32 | 2-7 | 1 | 1 | 3 |
| 10 | @ IND | 24 | 108 | 163 | 160 | 6-82 | 3-6 | 2-20 | 2 | 2 | 1 |
| 11 | @ BUF | 26 | 334 | 96 | 94 | 15-209 | 3-61 | 10-64 | 5 | 0 | 3 |

### Best individual lines allowed by MIA

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | KC | R.Rice (WR) 7/9 for 88, 0 TD | K.Walker (RB) 18 for 70, 1 TD |
| 4 | MIN | T.Hockenson (TE) 13/13 for 119, 0 TD | A.Jones (RB) 20 for 94, 0 TD |
| 5 | CIN | J.Chase (WR) 6/10 for 77, 1 TD | S.Perine (RB) 14 for 68, 0 TD |
| 7 | NYJ | O.Cooper (WR) 5/5 for 115, 1 TD | B.Allen (RB) 17 for 104, 0 TD |
| 8 | NE | D.Douglas (WR) 3/3 for 76, 1 TD | R.Stevenson (RB) 19 for 82, 0 TD |
| 9 | DET | A.St. Brown (WR) 8/10 for 86, 0 TD | J.Gibbs (RB) 20 for 74, 1 TD |
| 10 | IND | A.Dulin (WR) 1/2 for 30, 0 TD | J.Taylor (RB) 16 for 83, 0 TD |
| 11 | BUF | K.Shakir (WR) 5/9 for 101, 0 TD | J.Cook (RB) 22 for 89, 1 TD |

### MIA run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 78 | 278 | 3.56 | 1 |
| right guard | 30 | 156 | 5.2 | 3 |
| left guard | 23 | 99 | 4.3 | 0 |
| left end | 22 | 72 | 3.27 | 1 |
| right tackle | 21 | 113 | 5.38 | 4 |
| left tackle | 18 | 76 | 4.22 | 0 |
| right end | 14 | 107 | 7.64 | 2 |

### MIA defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Jacob Rodriguez | 8 | 43 | 30 | 265 | 6.2 | 2 | 2 | 7 |
| Jordyn Brooks | 8 | 38 | 23 | 193 | 5.1 | 0 | 0 | 5 |
| Jason Marshall | 7 | 32 | 20 | 289 | 9.0 | 2 | 0 | 2 |
| Julius Brents | 8 | 31 | 21 | 247 | 8.0 | 1 | 0 | 6 |
| Chris Johnson | 8 | 29 | 21 | 285 | 9.8 | 1 | 2 | 3 |
| Michael Taaffe | 8 | 25 | 15 | 250 | 10.0 | 3 | 2 | 4 |
| Dante Trader | 7 | 15 | 8 | 95 | 6.3 | 0 | 0 | 5 |
| Zayne Anderson | 4 | 12 | 4 | 34 | 2.8 | 2 | 1 | 0 |
| Willie Gay Jr. | 5 | 8 | 6 | 64 | 8.0 | 1 | 0 | 3 |
| Joshua Uche | 6 | 6 | 2 | 12 | 2.0 | 0 | 0 | 1 |

### MIA pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Chop Robinson | 8 | 24 | 5.0 | 10 | 1 |
| Joshua Uche | 6 | 9 | 3.0 | 3 | 1 |
| Zach Sieler | 5 | 7 | 2.0 | 2 | 0 |
| Zeek Biggers | 4 | 4 | 1.0 | 0 | 0 |
| Malik Herring | 2 | 3 | 1.0 | 1 | 0 |
| Jordyn Brooks | 8 | 3 | 1.0 | 1 | 9 |
| Jacob Rodriguez | 8 | 3 | 1.0 | 1 | 13 |
| Chris Johnson | 8 | 2 | 0.0 | 1 | 10 |

### MIA offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 16.4 | 30/32 | 23.2 |
| Pass yards / game | 171.2 | 31/32 | 234.2 |
| Yards per pass attempt | 6.14 | 26/32 | 7.12 |
| Rush yards / game | 95.6 | 18/32 | 100.6 |
| Yards per carry | 4.01 | 17/32 | 4.10 |
| RB rush yards / game | 82.0 | 21/32 | 93.4 |
| WR yards / game | 118.5 | 25/32 | 147.5 |
| TE yards / game | 34.8 | 26/32 | 53.4 |
| RB receiving yards / game | 18.0 | 30/32 | 33.2 |
| Explosive passes (20+) / game | 2.00 | 28/32 | 2.96 |
| Explosive runs (15+) / game | 1.50 | 8/32 | 1.23 |
| Sack rate allowed | 7.6% | 21/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 15.5% | 16/32 | 15.4% |
| Third-down conversion rate | 37.6% | 19/32 | 39.4% |
| Red-zone TD rate | 55.6% | 20/32 | 58.9% |

Neutral-situation pass rate 51.3%; 56.9 plays per game; target share WR 66% / TE 21% / RB 13%.

### MIA offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs KC | 10 | 210 | 76 | 58 | 12-141 | 5-55 | 3-14 | 3 | 0 | 0 |
| 4 | @ MIN | 10 | 85 | 113 | 107 | 6-70 | 1-15 | 2-0 | 0 | 1 | 2 |
| 5 | vs CIN | 24 | 137 | 144 | 99 | 10-95 | 5-42 | 0-0 | 2 | 5 | 3 |
| 7 | @ NYJ | 28 | 208 | 121 | 111 | 8-122 | 5-86 | 1-0 | 2 | 1 | 2 |
| 8 | vs NE | 19 | 211 | 74 | 74 | 17-168 | 4-43 | 0-0 | 2 | 1 | 5 |
| 9 | vs DET | 9 | 174 | 70 | 54 | 8-91 | 3-20 | 3-63 | 2 | 1 | 3 |
| 10 | @ IND | 22 | 243 | 77 | 74 | 9-176 | 1-5 | 8-62 | 4 | 1 | 3 |
| 11 | @ BUF | 9 | 102 | 90 | 79 | 7-85 | 2-12 | 3-5 | 1 | 2 | 2 |

**QB M.Willis** (6 games): 92/156, 979 yds, 5 TD, 5 INT, 15 sacks, 6.28 yds/att, depth of target 9.4, pressured on 14.6% of dropbacks. Yards by game: W3 210, W4 85, W5 137, W7 208, W8 211, W9 128.

**QB K.McCord** (2 games): 29/65, 311 yds, 0 TD, 1 INT, 5 sacks, 4.78 yds/att, depth of target 9.2, pressured on 22.9% of dropbacks. Yards by game: W10 209, W11 102.

### MIA receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M.Washington | WR | 8 | 44 | 32 | 334 | 1 | 20% | 22% | 9.9 | 4 | 4 | 56 67 43 27 40 21 50 30 |
| G.Dulcich | TE | 7 | 36 | 22 | 247 | 0 | 17% | 13% | 7.4 | 4 | 2 | 55 37 86 43 14 0 12 |
| C.Douglas | WR | 5 | 35 | 17 | 284 | 2 | 16% | 24% | 14.0 | 4 | 4 | 70 43 70 71 30 |
| C.Bell | WR | 7 | 26 | 12 | 131 | 0 | 12% | 17% | 12.9 | 0 | 1 | 67 0 0 25 31 0 8 |
| K.Coleman | WR | 7 | 26 | 9 | 88 | 2 | 12% | 16% | 12.7 | 3 | 2 | 3 3 30 0 46 6 0 |
| O.Gordon | RB | 7 | 18 | 13 | 60 | 0 | 8% | -1% | -1.4 | 1 | 0 | 14 0 0 0 9 39 -2 |
| W.Kacmarek | TE | 5 | 8 | 4 | 31 | 0 | 4% | 2% | 4.4 | 1 | 0 | 15 5 0 6 5 |
| J.Tolbert | WR | 5 | 7 | 5 | 96 | 1 | 3% | 5% | 13.3 | 1 | 2 | 0 22 8 49 17 |
| J.Wright | RB | 3 | 4 | 2 | 17 | 0 | 2% | 0% | 1.2 | 0 | 0 | 0 0 17 |

### MIA rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| O.Gordon | RB | 8 | 135 | 601 | 4.45 | 4 | 71% | 26 | 7 | 41 100 88 103 69 55 76 69 |
| J.Wright | RB | 6 | 27 | 39 | 1.44 | 0 | 14% | 3 | 0 | 7 11 8 5 -2 10 |
| M.Willis | QB | 6 | 10 | 21 | 2.10 | 1 | 5% | 3 | 0 | 13 3 1 2 2 0 |
| M.Washington | WR | 6 | 10 | 45 | 4.50 | 0 | 5% | 2 | 2 | 5 3 18 8 0 11 |
| D.Achane | RB | 1 | 3 | 17 | 5.67 | 0 | 2% | 0 | 0 | 17 |

### MIA run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 73 | 256 | 3.51 | 1 |
| right guard | 24 | 91 | 3.79 | 1 |
| left end | 23 | 124 | 5.39 | 4 |
| left guard | 23 | 90 | 3.91 | 1 |
| right end | 17 | 61 | 3.59 | 2 |
| left tackle | 16 | 91 | 5.69 | 1 |
| right tackle | 14 | 52 | 3.71 | 1 |

### MIA by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 250 | 55% | 75% | 5.02 | -0.091 |
| offense | Under center | 190 | 42% | 33% | 4.64 | -0.065 |
| offense | No huddle | 15 | 3% | 87% | 3.93 | -0.103 |
| defense vs | Shotgun | 277 | 59% | 70% | 5.31 | 0.04 |
| defense vs | Under center | 180 | 38% | 33% | 6.12 | 0.06 |
| defense vs | No huddle | 15 | 3% | 73% | 4.2 | -0.063 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 57 | 26% | 60% | 5.14 | 2 |
| offense | Short middle | 33 | 15% | 70% | 8.48 | 2 |
| offense | Short right | 81 | 36% | 62% | 4.73 | 0 |
| offense | Deep left | 20 | 9% | 25% | 7.15 | 4 |
| offense | Deep middle | 12 | 5% | 25% | 7.25 | 3 |
| offense | Deep right | 20 | 9% | 40% | 9.2 | 5 |
| defense allows | Short left | 70 | 30% | 76% | 5.94 | 1 |
| defense allows | Short middle | 36 | 15% | 67% | 5.47 | 2 |
| defense allows | Short right | 90 | 38% | 72% | 5.08 | 2 |
| defense allows | Deep left | 9 | 4% | 67% | 15.78 | 5 |
| defense allows | Deep middle | 11 | 5% | 55% | 19.82 | 4 |
| defense allows | Deep right | 21 | 9% | 57% | 17.24 | 9 |

### MIA lines (depth chart as of 2026-11-26T07:01:42Z)

Offensive line: LT Patrick Paul, LG Kadyn Proctor, C Aaron Brewer, RG Jonah Savaiinaea, RT Austin Jackson.  
Defensive front: LDE Chop Robinson, LDT Keith Cooper Jr., RDT Kenneth Grant, RDE Josh Uche, WLB Jordyn Brooks, SLB Willie Gay Jr..

### MIA injuries

Official report not posted yet for this week.

ESPN live list (designations only): Malik Willis (QB) Injured Reserve; Ronnie Harrison Jr. (LB) Injured Reserve; Dante Trader Jr. (S) Questionable; Bradley Pinion (P) Questionable; Austin Jackson (OT) Questionable; Jackson Woodard (LB) Questionable; Rodney McGraw (DE) Questionable; JuJu Brents (CB) Questionable; Jared Wayne (WR) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### MIA roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Rob Beal Jr. (DL) to SF; Jamree Kromah (DL) to CLE.

## DEN (last 8 games: weeks 3, 4, 5, 6, 7, 8, 9, 11)

### DEN defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 20.8 | 11/32 | 23.0 |
| Pass yards allowed / game | 267.9 | 28/32 | 235.6 |
| Yards per pass attempt allowed | 6.72 | 11/32 | 7.14 |
| Rush yards allowed / game | 102.4 | 16/32 | 99.5 |
| Yards per carry allowed | 4.27 | 20/32 | 4.07 |
| RB rush yards allowed / game | 89.9 | 14/32 | 92.5 |
| WR yards allowed / game | 140.4 | 13/32 | 147.8 |
| WR receptions allowed / game | 11.4 | 17/32 | 11.4 |
| TE yards allowed / game | 74.1 | 31/32 | 54.7 |
| TE receptions allowed / game | 7.4 | 31/32 | 5.3 |
| RB receiving yards allowed / game | 53.4 | 32/32 | 33.0 |
| RB receptions allowed / game | 5.4 | 26/32 | 4.4 |
| Explosive passes (20+) allowed / game | 2.88 | 12/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.38 | 18/32 | 1.21 |
| Sack rate | 7.5% | 9/32 | 6.6% |
| Pressure rate (sacks + hits) | 21.0% | 2/32 | 15.7% |
| Third-down conversions allowed | 40.0% | 17/32 | 39.2% |
| Red-zone TD rate allowed | 52.0% | 12/32 | 58.0% |
| Takeaways / game | 1.38 | 9/32 | 1.23 |

Blitz rate 34.3% and play-action faced 19.6% on 362 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.0 per game, 28.1% completed.

### DEN defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs LA | 26 | 390 | 106 | 103 | 11-230 | 11-90 | 8-70 | 6 | 1 | 4 |
| 4 | @ SF | 24 | 218 | 118 | 65 | 10-102 | 4-70 | 5-46 | 2 | 2 | 0 |
| 5 | @ LAC | 17 | 121 | 125 | 101 | 5-54 | 4-44 | 5-23 | 0 | 2 | 5 |
| 6 | vs SEA | 14 | 278 | 94 | 92 | 23-263 | 3-16 | 1--1 | 2 | 1 | 5 |
| 7 | @ ARI | 16 | 272 | 82 | 67 | 8-105 | 13-128 | 6-39 | 4 | 2 | 3 |
| 8 | vs KC | 24 | 321 | 88 | 84 | 13-90 | 8-88 | 9-143 | 3 | 1 | 2 |
| 9 | @ CAR | 21 | 276 | 83 | 86 | 10-125 | 14-134 | 4-17 | 4 | 1 | 3 |
| 11 | vs LV | 24 | 267 | 123 | 121 | 11-154 | 2-23 | 5-90 | 2 | 1 | 5 |

### Best individual lines allowed by DEN

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | LA | D.Adams (WR) 7/13 for 137, 0 TD | K.Williams (RB) 15 for 88, 0 TD |
| 4 | SF | M.Evans (WR) 5/8 for 76, 0 TD | C.McCaffrey (RB) 15 for 52, 1 TD |
| 5 | LAC | C.Kolar (TE) 3/4 for 37, 0 TD | K.Vidal (RB) 8 for 57, 1 TD |
| 6 | SEA | J.Smith-Njigba (WR) 12/16 for 134, 0 TD | E.Wilson (RB) 14 for 52, 0 TD |
| 7 | ARI | T.McBride (TE) 10/13 for 111, 1 TD | Z.Knight (RB) 7 for 48, 0 TD |
| 8 | KC | E.Johnson (RB) 5/5 for 128, 1 TD | K.Walker (RB) 21 for 69, 0 TD |
| 9 | CAR | D.Waller (TE) 8/10 for 90, 1 TD | C.Hubbard (RB) 16 for 79, 0 TD |
| 11 | LV | A.Jeanty (RB) 5/8 for 90, 1 TD | A.Jeanty (RB) 11 for 79, 0 TD |

### DEN run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 65 | 292 | 4.49 | 5 |
| right end | 36 | 153 | 4.25 | 1 |
| left end | 26 | 109 | 4.19 | 2 |
| right guard | 21 | 60 | 2.86 | 0 |
| left tackle | 20 | 109 | 5.45 | 2 |
| left guard | 14 | 57 | 4.07 | 0 |
| right tackle | 10 | 39 | 3.9 | 0 |

### DEN defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Ja'Quan McMillian | 8 | 41 | 23 | 210 | 5.1 | 1 | 2 | 3 |
| Alex Singleton | 8 | 39 | 28 | 268 | 6.9 | 1 | 0 | 8 |
| Justin Strnad | 8 | 37 | 23 | 218 | 5.9 | 0 | 0 | 4 |
| Jahdae Barron | 7 | 34 | 21 | 241 | 7.1 | 2 | 0 | 3 |
| Patrick Surtain II | 5 | 32 | 16 | 171 | 5.3 | 2 | 0 | 3 |
| Riley Moss | 6 | 29 | 14 | 184 | 6.3 | 2 | 0 | 4 |
| Brandon Jones | 6 | 24 | 16 | 257 | 10.7 | 1 | 1 | 8 |
| Kris Abrams-Draine | 4 | 23 | 14 | 112 | 4.9 | 1 | 1 | 1 |
| Talanoa Hufanga | 4 | 14 | 5 | 88 | 6.3 | 0 | 2 | 5 |
| Devon Key | 6 | 13 | 9 | 111 | 8.5 | 1 | 0 | 0 |

### DEN pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Zach Allen | 8 | 22 | 3.0 | 3 | 0 |
| Nik Bonitto | 8 | 14 | 5.0 | 5 | 29 |
| Malcolm Roach | 8 | 13 | 4.0 | 1 | 0 |
| Alex Singleton | 8 | 10 | 3.0 | 3 | 33 |
| Jonathon Cooper | 4 | 7 | 2.5 | 3 | 5 |
| Quandarrius Robinson | 7 | 7 | 1.0 | 3 | 24 |
| Eyioma Uwazurike | 4 | 6 | 1.0 | 1 | 0 |
| Dondrea Tillman | 6 | 6 | 0.0 | 2 | 11 |

### DEN offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 25.8 | 10/32 | 23.2 |
| Pass yards / game | 192.0 | 27/32 | 234.2 |
| Yards per pass attempt | 5.84 | 29/32 | 7.12 |
| Rush yards / game | 88.1 | 23/32 | 100.6 |
| Yards per carry | 3.54 | 27/32 | 4.10 |
| RB rush yards / game | 76.8 | 25/32 | 93.4 |
| WR yards / game | 111.4 | 29/32 | 147.5 |
| TE yards / game | 30.5 | 29/32 | 53.4 |
| RB receiving yards / game | 50.1 | 4/32 | 33.2 |
| Explosive passes (20+) / game | 2.50 | 21/32 | 2.96 |
| Explosive runs (15+) / game | 0.38 | 31/32 | 1.23 |
| Sack rate allowed | 2.9% | 1/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 7.9% | 2/32 | 15.4% |
| Third-down conversion rate | 35.6% | 26/32 | 39.4% |
| Red-zone TD rate | 72.0% | 5/32 | 58.9% |

Neutral-situation pass rate 54.2%; 59.8 plays per game; target share WR 57% / TE 20% / RB 23%.

### DEN offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs LA | 30 | 186 | 78 | 57 | 8-121 | 1-8 | 8-57 | 3 | 0 | 1 |
| 4 | @ SF | 14 | 214 | 72 | 72 | 10-96 | 1-6 | 14-112 | 2 | 0 | 0 |
| 5 | @ LAC | 23 | 123 | 105 | 84 | 9-67 | 4-55 | 3-1 | 1 | 0 | 1 |
| 6 | vs SEA | 17 | 107 | 72 | 72 | 9-58 | 2-13 | 6-36 | 0 | 1 | 2 |
| 7 | @ ARI | 30 | 222 | 91 | 83 | 10-151 | 1-2 | 4-69 | 4 | 2 | 1 |
| 8 | vs KC | 28 | 222 | 73 | 54 | 11-115 | 4-34 | 5-73 | 4 | 0 | 1 |
| 9 | @ CAR | 26 | 237 | 83 | 75 | 14-154 | 6-48 | 5-35 | 2 | 0 | 1 |
| 11 | vs LV | 38 | 225 | 131 | 117 | 7-129 | 8-78 | 4-18 | 4 | 0 | 1 |

**QB B.Nix** (8 games): 154/263, 1536 yds, 10 TD, 3 INT, 8 sacks, 5.84 yds/att, depth of target 6.1, pressured on 8.1% of dropbacks. Yards by game: W3 186, W4 214, W5 123, W6 107, W7 222, W8 222, W9 237, W11 225.

### DEN receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J.Waddle | WR | 8 | 45 | 24 | 258 | 2 | 19% | 30% | 10.4 | 5 | 4 | 10 35 19 24 48 39 22 61 |
| C.Sutton | WR | 8 | 39 | 20 | 230 | 2 | 17% | 30% | 11.9 | 7 | 3 | 46 4 18 19 45 53 45 0 |
| E.Engram | TE | 8 | 32 | 18 | 183 | 0 | 14% | 13% | 6.0 | 3 | 2 | 0 6 55 13 2 0 33 74 |
| R.Harvey | RB | 5 | 24 | 21 | 194 | 1 | 10% | -4% | -2.4 | 4 | 1 | 41 68 0 31 54 |
| M.Mims | WR | 7 | 18 | 11 | 128 | 0 | 8% | 7% | 5.7 | 0 | 2 | 10 6 13 53 10 0 36 |
| J.Coleman | RB | 4 | 16 | 14 | 127 | 0 | 7% | -2% | -2.3 | 1 | 1 | 15 63 31 18 |
| T.Franklin | WR | 7 | 14 | 8 | 73 | 0 | 6% | 13% | 14.6 | 2 | 1 | 21 16 2 0 3 31 0 |
| P.Bryant | WR | 4 | 14 | 12 | 179 | 2 | 6% | 8% | 8.7 | 2 | 4 | 44 47 56 32 |
| J.Dobbins | RB | 5 | 10 | 9 | 31 | 0 | 4% | -0% | -0.7 | 1 | 0 | 4 12 6 5 4 |

### DEN rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| J.Dobbins | RB | 8 | 81 | 252 | 3.11 | 3 | 41% | 11 | 1 | 49 40 68 41 23 13 18 0 |
| J.Coleman | RB | 4 | 61 | 263 | 4.31 | 5 | 31% | 14 | 1 | 54 41 57 111 |
| R.Harvey | RB | 5 | 21 | 69 | 3.29 | 1 | 11% | 1 | 0 | 6 25 7 25 6 |
| B.Nix | QB | 8 | 20 | 27 | 1.35 | 1 | 10% | 6 | 0 | 7 0 9 0 5 0 3 3 |
| M.Mims | WR | 5 | 6 | 41 | 6.83 | 0 | 3% | 2 | 0 | 3 3 19 5 11 |

### DEN run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 62 | 221 | 3.56 | 1 |
| right end | 28 | 95 | 3.39 | 0 |
| left end | 25 | 78 | 3.12 | 0 |
| left guard | 25 | 122 | 4.88 | 1 |
| right tackle | 24 | 80 | 3.33 | 0 |
| right guard | 17 | 63 | 3.71 | 0 |
| left tackle | 16 | 46 | 2.88 | 0 |

### DEN by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 279 | 58% | 72% | 5.25 | 0.037 |
| offense | Under center | 169 | 35% | 32% | 4.04 | -0.02 |
| offense | No huddle | 30 | 6% | 77% | 4.6 | 0.082 |
| defense vs | Shotgun | 316 | 57% | 81% | 5.56 | -0.022 |
| defense vs | Under center | 196 | 35% | 37% | 4.31 | -0.04 |
| defense vs | No huddle | 42 | 8% | 81% | 7.26 | 0.2 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 88 | 34% | 77% | 6.51 | 3 |
| offense | Short middle | 25 | 10% | 32% | 3.2 | 1 |
| offense | Short right | 108 | 41% | 59% | 4.57 | 3 |
| offense | Deep left | 19 | 7% | 32% | 8.74 | 6 |
| offense | Deep middle | 5 | 2% | 40% | 11.0 | 2 |
| offense | Deep right | 18 | 7% | 33% | 9.33 | 5 |
| defense allows | Short left | 87 | 27% | 62% | 5.95 | 3 |
| defense allows | Short middle | 56 | 18% | 70% | 8.11 | 2 |
| defense allows | Short right | 123 | 39% | 68% | 5.72 | 4 |
| defense allows | Deep left | 18 | 6% | 28% | 7.39 | 5 |
| defense allows | Deep middle | 9 | 3% | 33% | 8.22 | 2 |
| defense allows | Deep right | 26 | 8% | 31% | 10.0 | 7 |

### DEN lines (depth chart as of 2026-11-26T07:01:42Z)

Offensive line: LT Garett Bolles, LG Matt Peart, C Luke Wattenberg, RG Quinn Meinerz, RT Mike McGlinchey.  
Defensive front: LDE Zach Allen, NT D.J. Jones, RDE Malcolm Roach, WLB Jonathon Cooper, SLB Nik Bonitto.

### DEN injuries

Official report not posted yet for this week.

ESPN live list (designations only): Tyler Badie (RB) Injured Reserve; Jonah Elliss (LB) Injured Reserve; J.K. Dobbins (RB) Suspension; Taylor Rapp (S) Out; Sai'vion Jones (DE) Out.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

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
