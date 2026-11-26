# WAS at TEN: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: outdoors; surface: grass. Rest: WAS 7 days, TEN 7 days. Listed QBs: Jayden Daniels (WAS), Cam Ward (TEN).

Market (schedule consensus, not a timestamped quote): TEN +4.5, total 47.5.

Generated 2026-11-26T19:39:53+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T19:22:36Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | TEN +4.5 | -115 | -105 | 51.1% | 48.9% | 4.7% | 2026-11-26T19:22:36+00:00 |
| total | fanduel | Over 46.5 | -120 | +100 | 52.2% | 47.8% | 4.5% | 2026-11-26T19:22:36+00:00 |
| moneyline | fanduel | TEN | +180 | -215 | 34.4% | 65.6% | 4.0% | 2026-11-26T19:22:36+00:00 |

Player props: OK.

## Matchup edges

### WAS offense vs TEN defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| WAS OFFENCE ADVANTAGE | wide receiver yards | 164.4 | 211.9 | 147.8 | WAS offence ranks 9 of 32, TEN defence ranks 32 of 32 (1 = best at its own job) |
| WAS OFFENCE ADVANTAGE | explosive passes (20+) | 3.8 | 4.1 | 3.0 | WAS offence ranks 6 of 32, TEN defence ranks 32 of 32 (1 = best at its own job) |
| WAS OFFENCE ADVANTAGE | explosive runs (15+) | 1.5 | 1.8 | 1.2 | WAS offence ranks 8 of 32, TEN defence ranks 28 of 32 (1 = best at its own job) |
| TEN DEFENCE WEAK SPOT | passing yards | 242.9 | 297.5 | 235.6 | WAS offence ranks 16 of 32, TEN defence ranks 32 of 32 (1 = best at its own job) |
| TEN DEFENCE WEAK SPOT | points | 22.0 | 30.4 | 23.0 | WAS offence ranks 21 of 32, TEN defence ranks 31 of 32 (1 = best at its own job) |
| TEN DEFENCE WEAK SPOT | third-down conversions | 28.7% | 46.2% | 39.2% | WAS offence ranks 32 of 32, TEN defence ranks 27 of 32 (1 = best at its own job) |
| TEN DEFENCE WEAK SPOT | red-zone touchdowns | 50.0% | 70.6% | 58.0% | WAS offence ranks 25 of 32, TEN defence ranks 29 of 32 (1 = best at its own job) |
| TEN DEFENCE WEAK SPOT | pressure (sacks + hits) | 17.0% | 13.6% | 15.7% | WAS offence ranks 22 of 32, TEN defence ranks 26 of 32 (1 = best at its own job) |

### TEN offense vs WAS defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| WAS DEFENCE WEAK SPOT | tight end yards | 28.8 | 85.5 | 54.7 | TEN offence ranks 31 of 32, WAS defence ranks 32 of 32 (1 = best at its own job) |
| WAS DEFENCE WEAK SPOT | running back receiving yards | 22.4 | 48.6 | 33.0 | TEN offence ranks 26 of 32, WAS defence ranks 31 of 32 (1 = best at its own job) |
| WAS DEFENCE ADVANTAGE | explosive runs (15+) | 1.1 | 0.6 | 1.2 | TEN offence ranks 23 of 32, WAS defence ranks 2 of 32 (1 = best at its own job) |
| WAS DEFENCE WEAK SPOT | passing yards | 204.9 | 269.9 | 235.6 | TEN offence ranks 25 of 32, WAS defence ranks 30 of 32 (1 = best at its own job) |
| TEN OFFENCE WEAK SPOT | third-down conversions | 32.6% | 36.1% | 39.2% | TEN offence ranks 29 of 32, WAS defence ranks 12 of 32 (1 = best at its own job) |
| WAS DEFENCE WEAK SPOT | red-zone touchdowns | 50.0% | 70.4% | 58.0% | TEN offence ranks 25 of 32, WAS defence ranks 28 of 32 (1 = best at its own job) |
| TEN OFFENCE ADVANTAGE | sacks (pass protection vs pass rush) | 4.8% | 4.6% | 6.6% | TEN offence ranks 8 of 32, WAS defence ranks 29 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | WAS 24.7 - TEN 21.8 | 46.6 | -2.9 | 39.3% | 53.2% | 42.8% | WAS 12.3 - TEN 10.1 |
| independent | WAS 21.1 - TEN 17.9 | 39.1 | -3.2 | 40.0% | 55.7% | 25.0% | WAS 9.8 - TEN 7.7 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### WAS offense vs TEN defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S.Diggs | WR | receiving yards | 7 | 56.6 | 1.15 | 38.6 | 39.3 | 40.0 | 40.9 | 42.0 | 50.6 |
| S.Diggs | WR | receptions | 7 | 5.1 | 1.15 | 3.4 | 3.4 | 3.4 | 3.7 | 4.0 | 4.6 |
| A.Williams | WR | receiving yards | 8 | 57.5 | 1.15 | 19.7 | 22.1 | 24.4 | 26.0 | 27.6 | 42.0 |
| A.Williams | WR | receptions | 8 | 4.6 | 1.15 | 2.3 | 2.3 | 2.4 | 2.8 | 3.2 | 3.4 |
| C.Okonkwo | TE | receiving yards | 7 | 43.7 | 0.944 | 10.1 | 15.5 | 20.9 | 24.2 | 26.4 | 53.8 |
| C.Okonkwo | TE | receptions | 7 | 4.0 | 0.944 | 1.9 | 1.9 | 1.9 | 2.3 | 2.8 | 3.8 |
| T.Burks | WR | receiving yards | 7 | 48.8 | 1.15 | 19.4 | 23.9 | 28.4 | 30.1 | 30.5 | 34.5 |
| T.Burks | WR | receptions | 7 | 2.7 | 1.15 | 1.5 | 1.8 | 2.2 | 2.3 | 2.3 | 2.3 |
| J.Croskey-Merritt | RB | rushing yards | 4 | 51.6 | 1.029 | 18.7 | 21.9 | 25.2 | 28.4 | 31.6 | 46.3 |
| R.White | RB | rushing yards | 6 | 37.4 | 1.029 | 20.8 | 23.2 | 25.5 | 27.8 | 28.0 | 32.4 |
| A.Ekeler | RB | rushing yards | 7 | 23.7 | 1.029 | 0.2 | 1.4 | 2.7 | 5.8 | 9.8 | 26.8 |
| J.Daniels | QB | passing yards | 6 | 292.6 | 1.131 | 230.2 | 235.3 | 240.4 | 245.5 | 254.6 | 295.9 |

### TEN offense vs WAS defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W.Robinson | WR | receiving yards | 7 | 29.1 | 0.959 | 7.6 | 8.4 | 9.3 | 11.3 | 13.9 | 21.1 |
| W.Robinson | WR | receptions | 7 | 4.6 | 1.037 | 3.1 | 3.1 | 3.1 | 3.1 | 3.1 | 4.1 |
| C.Tate | WR | receiving yards | 6 | 63.2 | 0.959 | 18.2 | 30.7 | 43.2 | 55.6 | 55.6 | 60.9 |
| C.Tate | WR | receptions | 6 | 4.7 | 1.037 | 1.3 | 1.6 | 1.8 | 2.1 | 2.9 | 5.7 |
| E.Ayomanor | WR | receiving yards | 8 | 31.2 | 0.959 | 5.6 | 8.2 | 10.8 | 12.9 | 14.9 | 23.5 |
| E.Ayomanor | WR | receptions | 8 | 2.6 | 1.037 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 2.1 |
| T.Pollard | RB | receiving yards | 8 | 21.3 | 1.15 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 12.7 |
| T.Pollard | RB | receptions | 8 | 3.0 | 1.147 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.9 |
| G.Helm | TE | receiving yards | 7 | 27.7 | 1.15 | 1.7 | 3.5 | 5.2 | 7.8 | 10.9 | 16.1 |
| G.Helm | TE | receptions | 7 | 3.0 | 1.15 | 0.3 | 0.7 | 1.0 | 1.4 | 1.7 | 2.3 |
| C.Dike | WR | receiving yards | 6 | 36.3 | 0.959 | 5.8 | 8.6 | 11.5 | 14.4 | 14.6 | 21.1 |
| C.Dike | WR | receptions | 6 | 3.5 | 1.037 | 1.0 | 1.0 | 1.0 | 1.0 | 1.3 | 2.6 |
| T.Pollard | RB | rushing yards | 8 | 75.5 | 0.917 | 35.1 | 39.9 | 44.2 | 45.5 | 46.8 | 68.8 |
| C.Ward | QB | passing yards | 8 | 226.1 | 1.073 | 135.0 | 160.5 | 183.0 | 187.1 | 191.2 | 216.2 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## WAS (last 8 games: weeks 3, 4, 5, 6, 8, 9, 10, 11)

### WAS defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 22.8 | 16/32 | 23.0 |
| Pass yards allowed / game | 269.9 | 30/32 | 235.6 |
| Yards per pass attempt allowed | 6.85 | 14/32 | 7.14 |
| Rush yards allowed / game | 82.1 | 11/32 | 99.5 |
| Yards per carry allowed | 3.59 | 9/32 | 4.07 |
| RB rush yards allowed / game | 77.1 | 10/32 | 92.5 |
| WR yards allowed / game | 135.8 | 11/32 | 147.8 |
| WR receptions allowed / game | 12.2 | 22/32 | 11.4 |
| TE yards allowed / game | 85.5 | 32/32 | 54.7 |
| TE receptions allowed / game | 7.6 | 32/32 | 5.3 |
| RB receiving yards allowed / game | 48.6 | 31/32 | 33.0 |
| RB receptions allowed / game | 5.8 | 30/32 | 4.4 |
| Explosive passes (20+) allowed / game | 3.12 | 17/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.62 | 2/32 | 1.21 |
| Sack rate | 4.6% | 29/32 | 6.6% |
| Pressure rate (sacks + hits) | 14.4% | 21/32 | 15.7% |
| Third-down conversions allowed | 36.1% | 12/32 | 39.2% |
| Red-zone TD rate allowed | 70.4% | 28/32 | 58.0% |
| Takeaways / game | 1.75 | 3/32 | 1.23 |

Blitz rate 42.4% and play-action faced 18.7% on 347 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.1 per game, 36.4% completed.

### WAS defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs SEA | 31 | 393 | 39 | 39 | 19-236 | 6-82 | 7-75 | 4 | 0 | 0 |
| 4 | vs IND | 30 | 143 | 131 | 126 | 12-93 | 5-41 | 2-9 | 1 | 0 | 2 |
| 5 | vs NYG | 27 | 326 | 76 | 74 | 15-155 | 13-129 | 5-42 | 4 | 2 | 2 |
| 6 | @ SF | 23 | 264 | 102 | 98 | 5-129 | 5-69 | 11-66 | 4 | 0 | 2 |
| 8 | vs PHI | 10 | 212 | 66 | 64 | 10-93 | 7-83 | 6-36 | 3 | 1 | 5 |
| 9 | vs LA | 20 | 228 | 123 | 103 | 18-186 | 5-26 | 3-16 | 1 | 2 | 1 |
| 10 | @ NYG | 21 | 293 | 88 | 81 | 10-114 | 10-135 | 3-44 | 5 | 0 | 1 |
| 11 | vs CIN | 20 | 300 | 32 | 32 | 9-80 | 10-119 | 9-101 | 3 | 0 | 3 |

### Best individual lines allowed by WAS

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | SEA | J.Smith-Njigba (WR) 10/14 for 128, 2 TD | J.Price (RB) 5 for 15, 0 TD |
| 4 | IND | L.Treadwell (WR) 5/6 for 42, 0 TD | J.Taylor (RB) 20 for 95, 2 TD |
| 5 | NYG | M.Nabers (WR) 11/20 for 121, 1 TD | C.Skattebo (RB) 13 for 59, 0 TD |
| 6 | SF | M.Evans (WR) 3/5 for 94, 0 TD | C.McCaffrey (RB) 16 for 64, 2 TD |
| 8 | PHI | M.Lemon (WR) 6/9 for 57, 0 TD | E.Mitchell (RB) 11 for 34, 0 TD |
| 9 | LA | P.Nacua (WR) 14/19 for 150, 1 TD | B.Corum (RB) 11 for 58, 1 TD |
| 10 | NYG | I.Likely (TE) 9/11 for 127, 1 TD | C.Skattebo (RB) 18 for 78, 2 TD |
| 11 | CIN | M.Gesicki (TE) 5/6 for 77, 0 TD | S.Perine (RB) 6 for 26, 0 TD |

### WAS run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 57 | 167 | 2.93 | 0 |
| left guard | 31 | 120 | 3.87 | 0 |
| left end | 22 | 80 | 3.64 | 1 |
| right tackle | 21 | 97 | 4.62 | 1 |
| right end | 21 | 76 | 3.62 | 1 |
| right guard | 18 | 61 | 3.39 | 0 |
| left tackle | 13 | 56 | 4.31 | 0 |

### WAS defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Amik Robertson | 7 | 55 | 35 | 394 | 7.2 | 1 | 0 | 2 |
| Sonny Styles | 8 | 47 | 32 | 313 | 6.7 | 1 | 1 | 6 |
| Rasul Douglas | 8 | 40 | 21 | 225 | 5.6 | 1 | 3 | 1 |
| Trey Amos | 5 | 30 | 16 | 195 | 6.5 | 2 | 0 | 2 |
| Frankie Luvu | 7 | 30 | 19 | 182 | 6.1 | 0 | 0 | 1 |
| Jeremy Reaves | 8 | 30 | 16 | 198 | 6.6 | 0 | 0 | 1 |
| Nick Cross | 5 | 22 | 13 | 125 | 5.7 | 0 | 1 | 1 |
| Quan Martin | 7 | 16 | 8 | 135 | 8.4 | 0 | 0 | 0 |
| Mike Sainristil | 6 | 13 | 9 | 104 | 8.0 | 3 | 0 | 1 |
| Kain Medrano | 4 | 12 | 9 | 83 | 6.9 | 1 | 1 | 3 |

### WAS pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| K'Lavon Chaisson | 8 | 14 | 3.0 | 4 | 12 |
| Charles Omenihu | 5 | 11 | 1.0 | 4 | 0 |
| Odafe Oweh | 7 | 11 | 4.0 | 6 | 9 |
| Dorance Armstrong Jr. | 7 | 7 | 1.0 | 2 | 5 |
| Frankie Luvu | 7 | 7 | 1.0 | 3 | 58 |
| Sonny Styles | 8 | 5 | 0.0 | 4 | 49 |
| Daron Payne | 4 | 5 | 1.0 | 1 | 0 |
| Nick Cross | 5 | 4 | 0.5 | 2 | 18 |

### WAS offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 22.0 | 21/32 | 23.2 |
| Pass yards / game | 242.9 | 16/32 | 234.2 |
| Yards per pass attempt | 7.47 | 13/32 | 7.12 |
| Rush yards / game | 79.6 | 27/32 | 100.6 |
| Yards per carry | 3.75 | 23/32 | 4.10 |
| RB rush yards / game | 73.8 | 26/32 | 93.4 |
| WR yards / game | 164.4 | 9/32 | 147.5 |
| TE yards / game | 47.1 | 18/32 | 53.4 |
| RB receiving yards / game | 29.8 | 19/32 | 33.2 |
| Explosive passes (20+) / game | 3.75 | 6/32 | 2.96 |
| Explosive runs (15+) / game | 1.50 | 8/32 | 1.23 |
| Sack rate allowed | 7.4% | 20/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 17.0% | 22/32 | 15.4% |
| Third-down conversion rate | 28.7% | 32/32 | 39.4% |
| Red-zone TD rate | 50.0% | 25/32 | 58.9% |

Neutral-situation pass rate 53.1%; 60.1 plays per game; target share WR 63% / TE 21% / RB 16%.

### WAS offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs SEA | 33 | 183 | 80 | 71 | 15-159 | 2-11 | 2-13 | 2 | 1 | 2 |
| 4 | vs IND | 13 | 232 | 83 | 49 | 12-168 | 2-5 | 3-46 | 3 | 1 | 2 |
| 5 | vs NYG | 27 | 199 | 100 | 99 | 10-121 | 5-61 | 2-17 | 3 | 5 | 5 |
| 6 | @ SF | 17 | 300 | 43 | 43 | 15-193 | 8-73 | 6-34 | 4 | 0 | 4 |
| 8 | vs PHI | 27 | 217 | 112 | 112 | 11-173 | 2-32 | 3-12 | 5 | 2 | 2 |
| 9 | vs LA | 13 | 274 | 45 | 44 | 13-152 | 7-63 | 4-59 | 3 | 0 | 4 |
| 10 | @ NYG | 24 | 249 | 85 | 77 | 10-152 | 8-66 | 5-31 | 5 | 1 | 1 |
| 11 | vs CIN | 22 | 289 | 89 | 95 | 15-197 | 4-66 | 4-26 | 5 | 2 | 3 |

**QB J.Daniels** (6 games): 132/192, 1528 yds, 7 TD, 2 INT, 19 sacks, 7.96 yds/att, depth of target 7.7, pressured on 16.1% of dropbacks. Yards by game: W5 199, W6 300, W8 217, W9 274, W10 249, W11 289.

**QB M.Mariota** (2 games): 22/35, 229 yds, 3 TD, 0 INT, 3 sacks, 6.54 yds/att, depth of target 7.6, pressured on 28.9% of dropbacks. Yards by game: W3 183, W4 46.

### WAS receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S.Diggs | WR | 7 | 50 | 31 | 329 | 3 | 20% | 19% | 7.7 | 5 | 5 | 33 35 44 38 51 83 45 |
| A.Williams | WR | 8 | 45 | 30 | 360 | 1 | 18% | 22% | 10.4 | 2 | 6 | 15 21 31 50 54 25 42 122 |
| C.Okonkwo | TE | 7 | 41 | 29 | 313 | 0 | 16% | 12% | 6.2 | 1 | 5 | 5 60 69 32 57 24 66 |
| T.Burks | WR | 7 | 27 | 16 | 290 | 2 | 11% | 21% | 16.0 | 3 | 5 | 13 47 26 66 81 27 30 |
| A.Ekeler | RB | 6 | 15 | 12 | 77 | 0 | 6% | -1% | -1.5 | 1 | 0 | 11 15 4 18 26 3 |
| R.White | RB | 6 | 15 | 11 | 89 | 2 | 6% | 0% | 0.4 | 3 | 1 | 6 2 30 5 41 5 |
| T.McLaurin | WR | 3 | 14 | 11 | 166 | 1 | 6% | 8% | 12.2 | 1 | 3 | 77 62 27 |
| V.Jefferson | WR | 3 | 9 | 5 | 58 | 1 | 4% | 5% | 12.6 | 1 | 1 | 0 58 0 |
| D.Brown | WR | 4 | 8 | 5 | 73 | 0 | 3% | 8% | 19.9 | 0 | 1 | 0 65 2 6 |

### WAS rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| J.Croskey-Merritt | RB | 4 | 52 | 187 | 3.60 | 2 | 31% | 7 | 2 | 36 15 82 54 |
| R.White | RB | 6 | 51 | 210 | 4.12 | 1 | 30% | 5 | 3 | 35 18 27 55 28 47 |
| A.Ekeler | RB | 7 | 40 | 150 | 3.75 | 0 | 24% | 4 | 2 | 29 -1 3 36 16 26 41 |
| J.McNichols | RB | 2 | 10 | 34 | 3.40 | 0 | 6% | 3 | 0 | 13 21 |
| J.Daniels | QB | 6 | 7 | 4 | 0.57 | 0 | 4% | 1 | 0 | 1 0 0 1 8 -6 |

### WAS run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 43 | 127 | 2.95 | 1 |
| right guard | 32 | 95 | 2.97 | 0 |
| right end | 26 | 122 | 4.69 | 3 |
| left tackle | 21 | 99 | 4.71 | 1 |
| right tackle | 19 | 40 | 2.11 | 0 |
| left guard | 16 | 48 | 3.0 | 0 |
| left end | 13 | 106 | 8.15 | 3 |

### WAS by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 317 | 66% | 77% | 5.88 | -0.038 |
| offense | Under center | 118 | 24% | 28% | 5.08 | 0.001 |
| offense | No huddle | 46 | 10% | 76% | 5.02 | -0.002 |
| defense vs | Shotgun | 335 | 63% | 77% | 5.42 | 0.018 |
| defense vs | Under center | 146 | 28% | 35% | 4.49 | -0.049 |
| defense vs | No huddle | 49 | 9% | 80% | 6.84 | 0.185 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 72 | 28% | 74% | 5.71 | 2 |
| offense | Short middle | 53 | 20% | 66% | 7.15 | 4 |
| offense | Short right | 80 | 31% | 71% | 5.78 | 4 |
| offense | Deep left | 23 | 9% | 30% | 7.87 | 4 |
| offense | Deep middle | 10 | 4% | 70% | 18.6 | 6 |
| offense | Deep right | 22 | 8% | 46% | 14.73 | 10 |
| defense allows | Short left | 105 | 33% | 64% | 4.99 | 3 |
| defense allows | Short middle | 64 | 20% | 78% | 7.98 | 2 |
| defense allows | Short right | 95 | 30% | 67% | 5.21 | 3 |
| defense allows | Deep left | 16 | 5% | 56% | 13.5 | 8 |
| defense allows | Deep middle | 15 | 5% | 47% | 12.73 | 4 |
| defense allows | Deep right | 20 | 6% | 40% | 11.1 | 5 |

### WAS lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Brandon Coleman, LG Chris Paul, C Lucas Patrick, RG Sam Cosmi, RT Josh Conerly Jr..  
Defensive front: LDE Charles Omenihu, NT Tim Settle, RDE Shy Tuttle, WLB Odafe Oweh, SLB Dorance Armstrong.

### WAS injuries

Official report not posted yet for this week.

ESPN live list (designations only): Laremy Tunsil (OT) Injured Reserve; Stefon Diggs (WR) Questionable; Treylon Burks (WR) Questionable; Charles Omenihu (DE) Questionable; Amik Robertson (CB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### WAS roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Isaac Yiadom (DB) to CHI.

## TEN (last 8 games: weeks 3, 4, 5, 6, 7, 8, 10, 11)

### TEN defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 30.4 | 31/32 | 23.0 |
| Pass yards allowed / game | 297.5 | 32/32 | 235.6 |
| Yards per pass attempt allowed | 8.59 | 30/32 | 7.14 |
| Rush yards allowed / game | 114.4 | 24/32 | 99.5 |
| Yards per carry allowed | 4.28 | 21/32 | 4.07 |
| RB rush yards allowed / game | 97.9 | 18/32 | 92.5 |
| WR yards allowed / game | 211.9 | 32/32 | 147.8 |
| WR receptions allowed / game | 16.2 | 32/32 | 11.4 |
| TE yards allowed / game | 48.5 | 10/32 | 54.7 |
| TE receptions allowed / game | 4.8 | 8/32 | 5.3 |
| RB receiving yards allowed / game | 37.1 | 20/32 | 33.0 |
| RB receptions allowed / game | 4.1 | 11/32 | 4.4 |
| Explosive passes (20+) allowed / game | 4.12 | 32/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.75 | 28/32 | 1.21 |
| Sack rate | 5.8% | 21/32 | 6.6% |
| Pressure rate (sacks + hits) | 13.6% | 26/32 | 15.7% |
| Third-down conversions allowed | 46.2% | 27/32 | 39.2% |
| Red-zone TD rate allowed | 70.6% | 29/32 | 58.0% |
| Takeaways / game | 1.25 | 12/32 | 1.23 |

Blitz rate 26.2% and play-action faced 25.9% on 309 charted dropbacks (FTN). Deep passes (20+ air yards) faced 5.0 per game, 40.0% completed.

### TEN defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ NYG | 12 | 118 | 124 | 115 | 9-65 | 2-13 | 3-40 | 1 | 1 | 3 |
| 4 | @ BAL | 24 | 285 | 88 | 76 | 12-196 | 7-61 | 4-28 | 4 | 1 | 2 |
| 5 | vs HOU | 26 | 261 | 81 | 73 | 17-200 | 5-38 | 4-23 | 2 | 0 | 2 |
| 6 | @ IND | 20 | 269 | 135 | 121 | 16-184 | 4-28 | 2-57 | 3 | 3 | 6 |
| 7 | vs CLE | 27 | 308 | 176 | 141 | 15-177 | 6-91 | 4-40 | 6 | 4 | 1 |
| 8 | @ CIN | 43 | 462 | 64 | 65 | 24-330 | 5-77 | 9-55 | 6 | 0 | 3 |
| 10 | vs JAX | 40 | 352 | 101 | 93 | 18-298 | 4-29 | 3-25 | 6 | 2 | 1 |
| 11 | @ DAL | 51 | 325 | 146 | 99 | 19-245 | 5-51 | 4-29 | 5 | 3 | 0 |

### Best individual lines allowed by TEN

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | NYG | C.Skattebo (RB) 3/4 for 40, 0 TD | C.Skattebo (RB) 20 for 60, 0 TD |
| 4 | BAL | Z.Flowers (WR) 8/10 for 118, 1 TD | D.Henry (RB) 23 for 73, 1 TD |
| 5 | HOU | X.Hutchinson (WR) 4/5 for 65, 0 TD | W.Marks (RB) 15 for 62, 0 TD |
| 6 | IND | K.Allen (WR) 8/11 for 82, 0 TD | J.Taylor (RB) 21 for 94, 1 TD |
| 7 | CLE | K.Concepcion (WR) 8/10 for 129, 0 TD | Q.Judkins (RB) 17 for 96, 2 TD |
| 8 | CIN | T.Higgins (WR) 10/11 for 155, 2 TD | C.Brown (RB) 12 for 55, 0 TD |
| 10 | JAX | P.Washington (WR) 7/9 for 152, 1 TD | B.Tuten (RB) 26 for 88, 1 TD |
| 11 | DAL | C.Lamb (WR) 11/12 for 132, 1 TD | J.Williams (RB) 18 for 67, 1 TD |

### TEN run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 51 | 130 | 2.55 | 0 |
| left guard | 35 | 150 | 4.29 | 1 |
| left end | 28 | 169 | 6.04 | 3 |
| right tackle | 26 | 99 | 3.81 | 0 |
| right end | 26 | 129 | 4.96 | 4 |
| left tackle | 24 | 133 | 5.54 | 2 |
| right guard | 24 | 105 | 4.38 | 0 |

### TEN defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Cordale Flott | 8 | 41 | 26 | 324 | 7.9 | 3 | 2 | 2 |
| Joshua Williams | 5 | 40 | 30 | 365 | 9.1 | 2 | 0 | 4 |
| Anthony Hill | 7 | 26 | 21 | 227 | 8.7 | 2 | 0 | 1 |
| Alontae Taylor | 6 | 25 | 22 | 309 | 12.4 | 1 | 0 | 2 |
| Marcus Harris | 7 | 24 | 18 | 255 | 10.6 | 0 | 0 | 2 |
| Amani Hooker | 5 | 23 | 13 | 157 | 6.8 | 0 | 4 | 0 |
| Cody Barton | 7 | 22 | 15 | 259 | 11.8 | 1 | 0 | 0 |
| Kevin Winston | 6 | 16 | 11 | 109 | 6.8 | 2 | 0 | 0 |
| Cedric Gray | 8 | 15 | 12 | 89 | 5.9 | 2 | 1 | 2 |
| Tony Adams | 6 | 15 | 6 | 49 | 3.3 | 0 | 0 | 0 |

### TEN pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Jacob Martin | 6 | 19 | 6.5 | 7 | 1 |
| Jermaine Johnson II | 7 | 11 | 3.0 | 5 | 0 |
| Jeffery Simmons | 4 | 9 | 3.0 | 5 | 0 |
| John Franklin-Myers | 5 | 8 | 0.5 | 4 | 0 |
| Alontae Taylor | 6 | 6 | 1.0 | 3 | 17 |
| Anthony Hill | 7 | 5 | 0.0 | 4 | 14 |
| Solomon Thomas | 1 | 4 | 0.0 | 3 | 0 |
| Cedric Gray | 8 | 3 | 0.5 | 2 | 8 |

### TEN offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 20.9 | 22/32 | 23.2 |
| Pass yards / game | 204.9 | 25/32 | 234.2 |
| Yards per pass attempt | 6.21 | 25/32 | 7.12 |
| Rush yards / game | 92.2 | 19/32 | 100.6 |
| Yards per carry | 4.22 | 13/32 | 4.10 |
| RB rush yards / game | 87.6 | 19/32 | 93.4 |
| WR yards / game | 153.8 | 12/32 | 147.5 |
| TE yards / game | 28.8 | 31/32 | 53.4 |
| RB receiving yards / game | 22.4 | 26/32 | 33.2 |
| Explosive passes (20+) / game | 2.12 | 27/32 | 2.96 |
| Explosive runs (15+) / game | 1.12 | 23/32 | 1.23 |
| Sack rate allowed | 4.8% | 8/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 13.0% | 6/32 | 15.4% |
| Third-down conversion rate | 32.6% | 29/32 | 39.4% |
| Red-zone TD rate | 50.0% | 25/32 | 58.9% |

Neutral-situation pass rate 48.7%; 58.5 plays per game; target share WR 66% / TE 17% / RB 17%.

### TEN offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ NYG | 7 | 181 | 81 | 79 | 15-129 | 4-30 | 4-22 | 1 | 1 | 0 |
| 4 | @ BAL | 18 | 222 | 58 | 57 | 15-214 | 2-7 | 3-1 | 4 | 1 | 1 |
| 5 | vs HOU | 3 | 170 | 55 | 55 | 13-137 | 1-5 | 9-28 | 1 | 0 | 4 |
| 6 | @ IND | 26 | 102 | 80 | 77 | 10-95 | 0-0 | 1-7 | 0 | 1 | 0 |
| 7 | vs CLE | 24 | 181 | 136 | 136 | 12-120 | 4-28 | 4-33 | 1 | 2 | 1 |
| 8 | @ CIN | 36 | 304 | 138 | 117 | 15-172 | 8-112 | 3-20 | 5 | 2 | 2 |
| 10 | vs JAX | 23 | 231 | 66 | 61 | 13-136 | 6-29 | 9-66 | 2 | 2 | 1 |
| 11 | @ DAL | 30 | 248 | 124 | 119 | 17-227 | 3-19 | 1-2 | 3 | 0 | 5 |

**QB C.Ward** (8 games): 172/264, 1639 yds, 9 TD, 6 INT, 14 sacks, 6.21 yds/att, depth of target 7.1, pressured on 13.7% of dropbacks. Yards by game: W3 181, W4 222, W5 170, W6 102, W7 181, W8 304, W10 231, W11 248.

### TEN receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W.Robinson | WR | 7 | 47 | 32 | 225 | 3 | 19% | 17% | 6.6 | 10 | 0 | 57 19 53 22 7 57 10 |
| C.Tate | WR | 6 | 45 | 29 | 406 | 2 | 18% | 31% | 12.8 | 5 | 5 | 58 145 6 70 69 58 |
| E.Ayomanor | WR | 8 | 33 | 18 | 237 | 0 | 13% | 17% | 9.4 | 7 | 4 | 11 22 17 3 44 34 79 27 |
| T.Pollard | RB | 8 | 28 | 20 | 136 | 1 | 11% | 1% | 0.6 | 0 | 1 | 22 2 0 0 26 20 66 0 |
| G.Helm | TE | 7 | 26 | 17 | 156 | 0 | 10% | 9% | 6.1 | 1 | 2 | 14 5 0 24 76 23 14 |
| C.Dike | WR | 6 | 22 | 18 | 202 | 1 | 9% | 12% | 10.0 | 1 | 3 | 3 15 28 71 16 69 |
| C.Ridley | WR | 6 | 17 | 9 | 124 | 1 | 7% | 9% | 9.5 | 3 | 2 | 0 13 33 0 10 68 |
| D.Bellinger | TE | 8 | 17 | 11 | 74 | 1 | 7% | 3% | 3.8 | 3 | 0 | 16 2 5 0 4 36 6 5 |
| T.Spears | RB | 4 | 12 | 12 | 34 | 0 | 5% | -2% | -3.0 | 0 | 0 | -1 28 7 0 |

### TEN rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| T.Pollard | RB | 8 | 142 | 639 | 4.50 | 6 | 81% | 28 | 7 | 74 48 52 76 129 117 33 110 |
| T.Spears | RB | 5 | 12 | 41 | 3.42 | 0 | 7% | 1 | 0 | 5 7 0 1 28 |
| M.Carter | RB | 2 | 7 | 16 | 2.29 | 0 | 4% | 2 | 0 | 7 9 |
| C.Ward | QB | 8 | 7 | 27 | 3.86 | 1 | 4% | 2 | 0 | 2 0 0 3 0 21 0 1 |
| N.Singleton | RB | 1 | 3 | 2 | 0.67 | 0 | 2% | 1 | 0 | 2 |

### TEN run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 48 | 153 | 3.19 | 1 |
| left tackle | 28 | 103 | 3.68 | 0 |
| left guard | 23 | 68 | 2.96 | 0 |
| right guard | 23 | 108 | 4.7 | 1 |
| right tackle | 22 | 180 | 8.18 | 4 |
| right end | 16 | 46 | 2.88 | 0 |
| left end | 15 | 80 | 5.33 | 1 |

### TEN by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 248 | 53% | 72% | 5.06 | -0.085 |
| offense | No huddle | 129 | 28% | 68% | 5.93 | 0.065 |
| offense | Under center | 91 | 19% | 30% | 3.82 | -0.212 |
| defense vs | Shotgun | 306 | 58% | 77% | 6.88 | 0.175 |
| defense vs | Under center | 204 | 39% | 31% | 5.45 | 0.09 |
| defense vs | No huddle | 13 | 2% | 85% | 6.15 | -0.315 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 94 | 36% | 69% | 6.04 | 4 |
| offense | Short middle | 38 | 14% | 63% | 6.16 | 2 |
| offense | Short right | 92 | 35% | 74% | 5.23 | 2 |
| offense | Deep left | 14 | 5% | 43% | 11.29 | 3 |
| offense | Deep middle | 10 | 4% | 60% | 12.4 | 4 |
| offense | Deep right | 16 | 6% | 19% | 4.62 | 2 |
| defense allows | Short left | 96 | 35% | 82% | 7.73 | 4 |
| defense allows | Short middle | 42 | 15% | 71% | 9.29 | 5 |
| defense allows | Short right | 83 | 30% | 80% | 6.8 | 2 |
| defense allows | Deep left | 19 | 7% | 58% | 15.63 | 11 |
| defense allows | Deep middle | 6 | 2% | 50% | 15.5 | 3 |
| defense allows | Deep right | 31 | 11% | 39% | 9.48 | 8 |

### TEN lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Dan Moore Jr., LG Chandler Zavala, C Austin Schlottmann, RG Atonio Mafi, RT JC Latham.  
Defensive front: LDE Jacob Martin, LDT John Franklin-Myers, RDT Solomon Thomas, RDE Jermaine Johnson II, WLB Cedric Gray, SLB Cody Barton.

### TEN injuries

Official report not posted yet for this week.

ESPN live list (designations only): Dan Moore Jr. (OT) Questionable; John Franklin-Myers (DE) Questionable; Cor'Dale Flott (CB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### TEN roster moves (last 4 weeks)

Arrived: Corey Thornton (DB) from CAR.  
Left for another team: Amani Hooker (DB) to BUF.

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
