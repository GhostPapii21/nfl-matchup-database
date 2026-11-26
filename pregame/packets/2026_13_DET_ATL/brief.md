# DET at ATL: Week 13, Sunday early window

**Sunday 2026-12-06, 13:00 ET.** Site: Home; roof: not listed; surface: fieldturf. Rest: DET 10 days, ATL 7 days. Listed QBs: Jared Goff (DET), Michael Penix Jr. (ATL).

Market (schedule consensus, not a timestamped quote): ATL n/a, total n/a.

Generated 2026-11-26T19:39:42+00:00 UTC. **Research only. `projection_ready` is false. Not betting advice.** Every number below is a count of recorded plays; a missing value is unknown, not zero.

## Weather

KICKOFF_BEYOND_HOURLY_FORECAST: the hourly forecast covers about 6.5 days

## Book prices and no-vig

Retrieved 2026-11-26T14:01:05Z UTC from direct pulls (pregame/direct_lines) + Grok files when present; no Odds API. No-vig = each side's share of the two implied probabilities. Pinnacle is the sharp reference; books with prices here: fanduel.

| Market | Book | Side A / line | Price A | Price B | No-vig A | No-vig B | Hold | Book updated |
|---|---|---|---|---|---|---|---|---|
| spread | fanduel | ATL +3.5 | -105 | -115 | 48.9% | 51.1% | 4.7% | 2026-11-26T14:01:05+00:00 |
| total | fanduel | Over 50.5 | -110 | -110 | 50.0% | 50.0% | 4.8% | 2026-11-26T14:01:05+00:00 |
| moneyline | fanduel | ATL | +168 | -200 | 35.9% | 64.1% | 4.0% | 2026-11-26T14:01:05+00:00 |

Player props: OK.

## Matchup edges

### DET offense vs ATL defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| DET OFFENCE ADVANTAGE | wide receiver yards | 167.5 | 163.2 | 147.8 | DET offence ranks 7 of 32, ATL defence ranks 25 of 32 (1 = best at its own job) |
| DET OFFENCE ADVANTAGE | running back receiving yards | 46.0 | 38.6 | 33.0 | DET offence ranks 7 of 32, ATL defence ranks 23 of 32 (1 = best at its own job) |
| DET OFFENCE ADVANTAGE | running back rushing yards | 130.9 | 120.2 | 92.5 | DET offence ranks 3 of 32, ATL defence ranks 30 of 32 (1 = best at its own job) |
| DET OFFENCE ADVANTAGE | explosive runs (15+) | 1.6 | 1.6 | 1.2 | DET offence ranks 5 of 32, ATL defence ranks 26 of 32 (1 = best at its own job) |
| DET OFFENCE ADVANTAGE | passing yards | 275.1 | 251.4 | 235.6 | DET offence ranks 3 of 32, ATL defence ranks 23 of 32 (1 = best at its own job) |
| DET OFFENCE ADVANTAGE | third-down conversions | 43.2% | 43.9% | 39.2% | DET offence ranks 7 of 32, ATL defence ranks 23 of 32 (1 = best at its own job) |
| ATL DEFENCE WEAK SPOT | red-zone touchdowns | 61.3% | 75.0% | 58.0% | DET offence ranks 13 of 32, ATL defence ranks 32 of 32 (1 = best at its own job) |

### ATL offense vs DET defense

| Flag | Area | Offense (per game or rate) | Defense (allowed, or its own sack/pressure rate) | League avg | Ranks |
|---|---|---|---|---|---|
| DET DEFENCE WEAK SPOT | tight end yards | 43.0 | 69.1 | 54.7 | ATL offence ranks 21 of 32, DET defence ranks 29 of 32 (1 = best at its own job) |
| DET DEFENCE STRENGTH | running back rushing yards | 119.1 | 59.8 | 92.5 | ATL offence ranks 4 of 32, DET defence ranks 1 of 32 (1 = best at its own job) |
| DET DEFENCE WEAK SPOT | explosive passes (20+) | 3.2 | 3.4 | 3.0 | ATL offence ranks 13 of 32, DET defence ranks 23 of 32 (1 = best at its own job) |
| ATL OFFENCE STRENGTH | explosive runs (15+) | 1.8 | 0.9 | 1.2 | ATL offence ranks 2 of 32, DET defence ranks 8 of 32 (1 = best at its own job) |
| DET DEFENCE STRENGTH | sacks (pass protection vs pass rush) | 4.5% | 8.8% | 6.6% | ATL offence ranks 7 of 32, DET defence ranks 3 of 32 (1 = best at its own job) |
| ATL OFFENCE STRENGTH | pressure (sacks + hits) | 7.1% | 17.6% | 15.7% | ATL offence ranks 1 of 32, DET defence ranks 7 of 32 (1 = best at its own job) |

## Team score projection (research only)

| Sampler | Mean score | Total | Home margin | Home win | Home covers | Over | First half |
|---|---|---|---|---|---|---|---|
| matchup_pair | DET 26.1 - ATL 22.3 | 48.4 | -3.9 | 44.3% | n/a | n/a | DET 12.6 - ATL 10.7 |
| independent | DET 28.1 - ATL 20.5 | 48.6 | -7.5 | 32.6% | n/a | n/a | DET 13.8 - ATL 11.0 |

Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; treat probabilities near the market number as no information.

## Player baselines (research only)

### DET offense vs ATL defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A.St. Brown | WR | receiving yards | 8 | 77.8 | 1.052 | 26.6 | 33.2 | 39.4 | 42.7 | 46.0 | 75.8 |
| A.St. Brown | WR | receptions | 8 | 6.7 | 1.054 | 4.2 | 4.2 | 4.3 | 4.6 | 5.0 | 6.8 |
| J.Gibbs | RB | receiving yards | 8 | 41.5 | 1.085 | 5.7 | 11.4 | 16.5 | 18.4 | 20.3 | 31.5 |
| J.Gibbs | RB | receptions | 8 | 4.5 | 1.091 | 0.8 | 1.5 | 2.3 | 3.1 | 3.8 | 4.9 |
| J.Williams | WR | receiving yards | 8 | 70.0 | 1.052 | 38.5 | 44.4 | 49.6 | 50.3 | 51.0 | 63.1 |
| J.Williams | WR | receptions | 8 | 3.9 | 1.054 | 1.4 | 1.8 | 2.2 | 3.0 | 3.7 | 4.2 |
| S.LaPorta | TE | receiving yards | 8 | 42.8 | 0.953 | 15.9 | 16.6 | 17.8 | 22.5 | 27.2 | 36.7 |
| S.LaPorta | TE | receptions | 8 | 3.3 | 0.991 | 1.0 | 1.0 | 1.1 | 1.8 | 2.5 | 3.0 |
| I.TeSlaa | WR | receiving yards | 7 | 24.2 | 1.052 | 0.0 | 0.0 | 0.0 | 1.9 | 4.7 | 10.5 |
| I.TeSlaa | WR | receptions | 7 | 1.5 | 1.054 | 0.0 | 0.0 | 0.0 | 0.2 | 0.5 | 1.1 |
| J.Gibbs | RB | rushing yards | 8 | 130.2 | 1.15 | 64.2 | 75.4 | 86.5 | 96.1 | 105.8 | 123.6 |
| J.Goff | QB | passing yards | 8 | 276.5 | 1.034 | 177.9 | 180.0 | 186.7 | 220.4 | 254.0 | 284.2 |

### ATL offense vs DET defense

| Player | Pos | Stat | G | Wtd mean | Opp factor | Floor p5 | p10 | MAIN p15 | p20 | p25 | Median |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D.London | WR | receiving yards | 8 | 79.9 | 0.954 | 25.7 | 43.7 | 59.3 | 60.6 | 62.0 | 78.2 |
| D.London | WR | receptions | 8 | 5.5 | 1.032 | 2.1 | 3.2 | 4.2 | 4.5 | 4.9 | 5.7 |
| K.Pitts | TE | receiving yards | 8 | 36.4 | 1.132 | 6.1 | 6.5 | 7.7 | 14.0 | 20.4 | 36.8 |
| K.Pitts | TE | receptions | 8 | 4.0 | 1.108 | 1.5 | 1.9 | 2.3 | 2.7 | 3.0 | 3.9 |
| J.Dotson | WR | receiving yards | 8 | 47.2 | 0.954 | 7.4 | 9.1 | 10.7 | 12.4 | 14.1 | 51.5 |
| J.Dotson | WR | receptions | 8 | 2.1 | 1.032 | 1.0 | 1.0 | 1.1 | 1.4 | 1.8 | 2.1 |
| Bi.Robinson | RB | receiving yards | 6 | 18.6 | 1.049 | -6.3 | -4.2 | -2.1 | 0.0 | 0.5 | 11.0 |
| Bi.Robinson | RB | receptions | 6 | 2.3 | 0.964 | 0.2 | 0.5 | 0.7 | 1.0 | 1.2 | 1.9 |
| Bi.Robinson | RB | rushing yards | 6 | 80.4 | 0.85 | 52.3 | 52.7 | 53.1 | 53.5 | 56.3 | 68.8 |
| Br.Robinson | RB | rushing yards | 4 | 22.9 | 0.85 | 2.8 | 4.7 | 6.6 | 8.5 | 10.4 | 28.1 |
| M.Penix | QB | passing yards | 8 | 215.7 | 1.01 | 139.4 | 152.4 | 166.2 | 184.3 | 202.3 | 226.3 |

The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. This is NOT the three-model consensus and has not been validated against prices. Injury replacements, role changes and game script are not applied: the analyst must adjust for them.

## DET (last 8 games: weeks 3, 4, 5, 7, 8, 9, 10, 11)

### DET defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 18.6 | 6/32 | 23.0 |
| Pass yards allowed / game | 240.4 | 20/32 | 235.6 |
| Yards per pass attempt allowed | 6.77 | 12/32 | 7.14 |
| Rush yards allowed / game | 65.5 | 2/32 | 99.5 |
| Yards per carry allowed | 3.42 | 6/32 | 4.07 |
| RB rush yards allowed / game | 59.8 | 1/32 | 92.5 |
| WR yards allowed / game | 134.1 | 9/32 | 147.8 |
| WR receptions allowed / game | 12.1 | 21/32 | 11.4 |
| TE yards allowed / game | 69.1 | 29/32 | 54.7 |
| TE receptions allowed / game | 6.5 | 28/32 | 5.3 |
| RB receiving yards allowed / game | 36.2 | 18/32 | 33.0 |
| RB receptions allowed / game | 4.1 | 11/32 | 4.4 |
| Explosive passes (20+) allowed / game | 3.38 | 23/32 | 2.98 |
| Explosive runs (15+) allowed / game | 0.88 | 8/32 | 1.21 |
| Sack rate | 8.8% | 3/32 | 6.6% |
| Pressure rate (sacks + hits) | 17.6% | 7/32 | 15.7% |
| Third-down conversions allowed | 40.6% | 19/32 | 39.2% |
| Red-zone TD rate allowed | 58.3% | 19/32 | 58.0% |
| Takeaways / game | 0.75 | 30/32 | 1.23 |

Blitz rate 22.5% and play-action faced 21.6% on 329 charted dropbacks (FTN). Deep passes (20+ air yards) faced 5.0 per game, 30.0% completed.

### DET defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs NYJ | 24 | 321 | 46 | 46 | 12-131 | 13-164 | 6-26 | 6 | 0 | 5 |
| 4 | @ CAR | 32 | 329 | 124 | 124 | 19-261 | 8-56 | 2-12 | 4 | 3 | 3 |
| 5 | @ ARI | 21 | 299 | 38 | 37 | 13-145 | 14-138 | 2-9 | 3 | 1 | 5 |
| 7 | vs GB | 17 | 274 | 60 | 56 | 15-152 | 5-57 | 7-65 | 6 | 0 | 1 |
| 8 | vs MIN | 15 | 210 | 60 | 46 | 10-110 | 5-82 | 2-18 | 3 | 1 | 3 |
| 9 | @ MIA | 9 | 174 | 70 | 54 | 8-91 | 3-20 | 3-63 | 2 | 1 | 3 |
| 10 | vs NE | 10 | 129 | 42 | 31 | 8-79 | 3-28 | 4-22 | 2 | 0 | 5 |
| 11 | vs TB | 21 | 187 | 84 | 84 | 12-104 | 1-8 | 7-75 | 1 | 1 | 4 |

### Best individual lines allowed by DET

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | NYJ | G.Wilson (WR) 10/13 for 107, 1 TD | B.Hall (RB) 13 for 32, 0 TD |
| 4 | CAR | T.McMillan (WR) 14/16 for 192, 2 TD | C.Hubbard (RB) 20 for 122, 2 TD |
| 5 | ARI | K.Bourne (WR) 5/8 for 70, 0 TD | J.Love (RB) 12 for 22, 0 TD |
| 7 | GB | C.Watson (WR) 5/8 for 57, 0 TD | J.Jacobs (RB) 11 for 36, 0 TD |
| 8 | MIN | J.Addison (WR) 3/8 for 66, 0 TD | A.Jones (RB) 5 for 22, 0 TD |
| 9 | MIA | C.Douglas (WR) 6/8 for 70, 0 TD | O.Gordon (RB) 16 for 55, 0 TD |
| 10 | NE | M.Hollins (WR) 5/6 for 48, 0 TD | C.Kiner (RB) 10 for 25, 0 TD |
| 11 | TB | T.Hurst (WR) 5/7 for 56, 2 TD | B.Irving (RB) 18 for 68, 1 TD |

### DET run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 58 | 192 | 3.31 | 1 |
| left tackle | 19 | 71 | 3.74 | 2 |
| left end | 19 | 71 | 3.74 | 1 |
| right end | 19 | 67 | 3.53 | 0 |
| right tackle | 17 | 44 | 2.59 | 0 |
| left guard | 11 | 41 | 3.73 | 0 |
| right guard | 10 | 38 | 3.8 | 1 |

### DET defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| Roger McCreary | 8 | 59 | 35 | 456 | 7.7 | 4 | 1 | 2 |
| Chuck Clark | 8 | 34 | 12 | 142 | 4.2 | 0 | 1 | 4 |
| Derrick Barnes | 7 | 29 | 19 | 254 | 8.8 | 1 | 0 | 3 |
| Rock Ya-Sin | 6 | 26 | 14 | 127 | 4.9 | 1 | 0 | 0 |
| D.J. Reed | 5 | 25 | 13 | 182 | 7.3 | 2 | 1 | 2 |
| Jack Campbell | 5 | 25 | 19 | 240 | 9.6 | 2 | 0 | 1 |
| Ennis Rakestraw | 6 | 22 | 13 | 169 | 7.7 | 0 | 0 | 4 |
| Christian Izien | 4 | 19 | 14 | 115 | 6.1 | 2 | 0 | 1 |
| Malcolm Rodriguez | 7 | 12 | 10 | 51 | 4.2 | 3 | 0 | 1 |
| Brian Branch | 5 | 12 | 4 | 38 | 3.2 | 0 | 1 | 1 |

### DET pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Aidan Hutchinson | 7 | 21 | 3.0 | 8 | 0 |
| Alim McNeill | 8 | 12 | 5.5 | 2 | 0 |
| D.J. Wonnum | 7 | 11 | 7.0 | 1 | 0 |
| Derrick Moore | 7 | 10 | 4.5 | 2 | 1 |
| Skyler Gill-Howard | 6 | 6 | 2.0 | 1 | 0 |
| Tyler Lacy | 4 | 4 | 0.0 | 0 | 0 |
| Jack Campbell | 5 | 3 | 0.0 | 2 | 26 |
| Tyleik Williams | 2 | 3 | 0.0 | 2 | 0 |

### DET offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 28.2 | 6/32 | 23.2 |
| Pass yards / game | 275.1 | 3/32 | 234.2 |
| Yards per pass attempt | 8.56 | 2/32 | 7.12 |
| Rush yards / game | 134.8 | 3/32 | 100.6 |
| Yards per carry | 4.81 | 5/32 | 4.10 |
| RB rush yards / game | 130.9 | 3/32 | 93.4 |
| WR yards / game | 167.5 | 7/32 | 147.5 |
| TE yards / game | 61.6 | 10/32 | 53.4 |
| RB receiving yards / game | 46.0 | 7/32 | 33.2 |
| Explosive passes (20+) / game | 3.00 | 18/32 | 2.96 |
| Explosive runs (15+) / game | 1.62 | 5/32 | 1.23 |
| Sack rate allowed | 6.1% | 14/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 15.5% | 14/32 | 15.4% |
| Third-down conversion rate | 43.2% | 7/32 | 39.4% |
| Red-zone TD rate | 61.3% | 13/32 | 58.9% |

Neutral-situation pass rate 53.6%; 62.8 plays per game; target share WR 56% / TE 23% / RB 21%.

### DET offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | vs NYJ | 31 | 269 | 125 | 125 | 11-134 | 6-59 | 8-76 | 3 | 1 | 2 |
| 4 | @ CAR | 26 | 412 | 46 | 46 | 18-281 | 9-92 | 5-39 | 4 | 0 | 1 |
| 5 | @ ARI | 45 | 271 | 163 | 162 | 8-116 | 6-99 | 5-56 | 4 | 4 | 3 |
| 7 | vs GB | 20 | 303 | 120 | 121 | 15-254 | 2-22 | 5-27 | 4 | 1 | 1 |
| 8 | vs MIN | 19 | 176 | 232 | 218 | 11-116 | 4-40 | 3-20 | 1 | 3 | 4 |
| 9 | @ MIA | 19 | 181 | 98 | 88 | 12-142 | 4-32 | 2-7 | 1 | 1 | 3 |
| 10 | vs NE | 35 | 310 | 193 | 190 | 10-167 | 3-27 | 8-116 | 4 | 2 | 2 |
| 11 | vs TB | 31 | 279 | 101 | 97 | 9-130 | 6-122 | 5-27 | 3 | 1 | 1 |

**QB J.Goff** (8 games): 173/255, 2183 yds, 14 TD, 4 INT, 17 sacks, 8.56 yds/att, depth of target 7.6, pressured on 15.8% of dropbacks. Yards by game: W3 269, W4 412, W5 271, W7 303, W8 176, W9 170, W10 303, W11 279.

**QB J.Dobbs** (1 games): 1/1, 7 yds, 0 TD, 0 INT, 0 sacks, 7.00 yds/att, depth of target 6.0, pressured on 0.0% of dropbacks. Yards by game: W10 7.

### DET receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A.St. Brown | WR | 8 | 70 | 51 | 583 | 4 | 28% | 29% | 8.1 | 13 | 5 | 19 75 69 153 46 86 98 37 |
| J.Gibbs | RB | 8 | 45 | 34 | 313 | 1 | 18% | -0% | -0.1 | 7 | 3 | 65 31 56 27 15 0 99 20 |
| J.Williams | WR | 8 | 44 | 30 | 533 | 6 | 17% | 34% | 15.1 | 9 | 8 | 49 102 47 91 70 31 50 93 |
| S.LaPorta | TE | 8 | 44 | 28 | 377 | 2 | 17% | 19% | 8.6 | 9 | 5 | 44 84 88 18 33 32 16 62 |
| I.TeSlaa | WR | 7 | 25 | 11 | 199 | 1 | 10% | 12% | 9.5 | 6 | 2 | 66 95 0 10 9 19 0 |
| B.Wright | TE | 5 | 9 | 8 | 79 | 0 | 4% | 2% | 5.1 | 1 | 1 | 7 8 11 11 42 |
| S.Vaki | RB | 6 | 8 | 7 | 64 | 0 | 3% | 1% | 2.5 | 0 | 0 | 11 17 5 7 17 7 |
| T.Conklin | TE | 4 | 4 | 3 | 29 | 0 | 2% | 2% | 7.8 | 1 | 0 | 4 7 0 18 |
| D.Carter | WR | 1 | 1 | 1 | 5 | 0 | 0% | -0% | -2.0 | 0 | 0 | 5 |

### DET rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| J.Gibbs | RB | 8 | 177 | 890 | 5.03 | 11 | 79% | 43 | 13 | 99 46 151 116 153 74 153 98 |
| S.Vaki | RB | 7 | 34 | 148 | 4.35 | 0 | 15% | 1 | 0 | 26 11 5 65 14 28 -1 |
| J.Goff | QB | 7 | 7 | 11 | 1.57 | 1 | 3% | 3 | 0 | 0 1 0 2 1 3 4 |
| A.St. Brown | WR | 2 | 2 | 9 | 4.50 | 0 | 1% | 0 | 0 | -1 10 |
| J.Saylors | RB | 1 | 2 | 9 | 4.50 | 0 | 1% | 0 | 0 | 9 |

### DET run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 77 | 336 | 4.36 | 3 |
| right tackle | 43 | 240 | 5.58 | 5 |
| left tackle | 43 | 257 | 5.98 | 1 |
| left end | 23 | 60 | 2.61 | 1 |
| right end | 20 | 146 | 7.3 | 3 |
| right guard | 9 | 12 | 1.33 | 0 |
| left guard | 8 | 27 | 3.38 | 0 |

### DET by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Under center | 266 | 53% | 29% | 5.59 | 0.086 |
| offense | Shotgun | 214 | 43% | 88% | 7.62 | 0.23 |
| offense | No huddle | 22 | 4% | 59% | 3.95 | -0.004 |
| defense vs | Shotgun | 298 | 62% | 82% | 4.87 | 0.028 |
| defense vs | Under center | 145 | 30% | 37% | 5.14 | -0.019 |
| defense vs | No huddle | 39 | 8% | 77% | 4.08 | 0.022 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 75 | 29% | 69% | 7.01 | 3 |
| offense | Short middle | 66 | 26% | 74% | 7.23 | 3 |
| offense | Short right | 67 | 26% | 75% | 6.7 | 2 |
| offense | Deep left | 17 | 7% | 59% | 16.59 | 6 |
| offense | Deep middle | 18 | 7% | 39% | 12.94 | 4 |
| offense | Deep right | 14 | 5% | 50% | 16.71 | 6 |
| defense allows | Short left | 81 | 28% | 68% | 4.91 | 2 |
| defense allows | Short middle | 46 | 16% | 85% | 9.02 | 4 |
| defense allows | Short right | 97 | 34% | 69% | 5.66 | 3 |
| defense allows | Deep left | 19 | 7% | 32% | 7.68 | 5 |
| defense allows | Deep middle | 12 | 4% | 42% | 12.67 | 5 |
| defense allows | Deep right | 29 | 10% | 38% | 9.07 | 8 |

### DET lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Penei Sewell, LG Christian Mahogany, C Juice Scruggs, RG Tate Ratledge, RT Blake Miller.  
Defensive front: LDE Derrick Moore, LDT Alim McNeill, RDT Tyleik Williams, RDE DJ Wonnum, WLB Derrick Barnes, SLB Trevor Nowaske.

### DET injuries

Official report not posted yet for this week.

ESPN live list (designations only): Skyler Gill-Howard (DT) Injured Reserve; Ennis Rakestraw Jr. (CB) Out; Tyrus Wheat (LB) Out; Keith Abney II (CB) Out; Chuck Clark (S) Out; DJ Wonnum (LB) Out.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### DET roster moves (last 4 weeks)

Arrived: none.  
Left for another team: Bishop Fitzgerald (DB) to TEN.

## ATL (last 8 games: weeks 3, 4, 5, 6, 7, 8, 9, 10)

### ATL defense: what it allows (rank 1 = best defense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points allowed / game | 25.5 | 21/32 | 23.0 |
| Pass yards allowed / game | 251.4 | 23/32 | 235.6 |
| Yards per pass attempt allowed | 7.31 | 19/32 | 7.14 |
| Rush yards allowed / game | 129.5 | 29/32 | 99.5 |
| Yards per carry allowed | 4.84 | 30/32 | 4.07 |
| RB rush yards allowed / game | 120.2 | 30/32 | 92.5 |
| WR yards allowed / game | 163.2 | 25/32 | 147.8 |
| WR receptions allowed / game | 12.6 | 25/32 | 11.4 |
| TE yards allowed / game | 49.5 | 12/32 | 54.7 |
| TE receptions allowed / game | 5.2 | 16/32 | 5.3 |
| RB receiving yards allowed / game | 38.6 | 23/32 | 33.0 |
| RB receptions allowed / game | 5.2 | 24/32 | 4.4 |
| Explosive passes (20+) allowed / game | 3.12 | 17/32 | 2.98 |
| Explosive runs (15+) allowed / game | 1.62 | 26/32 | 1.21 |
| Sack rate | 5.7% | 22/32 | 6.6% |
| Pressure rate (sacks + hits) | 18.0% | 6/32 | 15.7% |
| Third-down conversions allowed | 43.9% | 23/32 | 39.2% |
| Red-zone TD rate allowed | 75.0% | 32/32 | 58.0% |
| Takeaways / game | 1.12 | 16/32 | 1.23 |

Blitz rate 26.7% and play-action faced 19.7% on 300 charted dropbacks (FTN). Deep passes (20+ air yards) faced 4.1 per game, 30.3% completed.

### ATL defense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ GB | 14 | 312 | 17 | 17 | 18-249 | 6-42 | 4-21 | 4 | 0 | 1 |
| 4 | @ NO | 24 | 286 | 47 | 50 | 15-177 | 6-59 | 9-50 | 3 | 0 | 2 |
| 5 | vs BAL | 30 | 201 | 206 | 175 | 15-124 | 6-54 | 3-23 | 1 | 3 | 4 |
| 6 | vs CHI | 31 | 305 | 97 | 95 | 16-189 | 8-68 | 6-48 | 3 | 0 | 4 |
| 7 | vs SF | 20 | 288 | 123 | 108 | 7-107 | 9-102 | 11-79 | 4 | 2 | 2 |
| 8 | @ TB | 16 | 0 | 322 | 310 | 0-0 | 0-0 | 0-0 | 0 | 4 | 1 |
| 9 | vs CIN | 34 | 271 | 117 | 100 | 18-238 | 3-15 | 3-18 | 3 | 3 | 2 |
| 10 | vs KC | 35 | 348 | 107 | 107 | 12-222 | 4-56 | 6-70 | 7 | 1 | 1 |

### Best individual lines allowed by ATL

| Wk | Opp | Top receiver | Top rusher |
|---|---|---|---|
| 3 | GB | M.Golden (WR) 5/12 for 100, 1 TD | M.Lloyd (RB) 4 for 11, 0 TD |
| 4 | NO | C.Olave (WR) 8/12 for 116, 0 TD | A.Kamara (RB) 7 for 23, 2 TD |
| 5 | BAL | R.Bateman (WR) 5/6 for 62, 0 TD | D.Henry (RB) 24 for 102, 0 TD |
| 6 | CHI | L.Burden (WR) 8/8 for 95, 0 TD | R.Johnson (RB) 13 for 51, 1 TD |
| 7 | SF | G.Kittle (TE) 8/10 for 88, 0 TD | K.Black (RB) 12 for 63, 1 TD |
| 8 | TB | T.Hurst (WR) 0/1 for 0, 0 TD | B.Irving (RB) 27 for 170, 1 TD |
| 9 | CIN | J.Chase (WR) 10/12 for 155, 1 TD | C.Brown (RB) 9 for 57, 0 TD |
| 10 | KC | R.Rice (WR) 5/6 for 82, 0 TD | E.Johnson (RB) 22 for 101, 0 TD |

### ATL run defense by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 69 | 338 | 4.9 | 5 |
| right guard | 35 | 166 | 4.74 | 1 |
| left end | 26 | 151 | 5.81 | 2 |
| right end | 23 | 109 | 4.74 | 1 |
| left guard | 21 | 53 | 2.52 | 0 |
| right tackle | 21 | 76 | 3.62 | 0 |
| left tackle | 14 | 123 | 8.79 | 4 |

### ATL defenders in coverage (Pro Football Reference)

| Defender | G | Targets | Comp | Yards | Yds/tgt | TD | INT | Missed tkl |
|---|---|---|---|---|---|---|---|---|
| C.J. Henderson | 7 | 42 | 23 | 318 | 7.6 | 2 | 0 | 2 |
| Harold Perkins | 8 | 36 | 21 | 170 | 4.7 | 1 | 0 | 5 |
| Mike Hughes | 7 | 35 | 22 | 323 | 9.2 | 3 | 0 | 4 |
| Kendal Daniels | 8 | 34 | 24 | 162 | 4.8 | 0 | 1 | 6 |
| Billy Bowman | 5 | 24 | 14 | 151 | 6.3 | 1 | 0 | 2 |
| Jessie Bates III | 6 | 23 | 16 | 195 | 8.5 | 3 | 1 | 1 |
| Xavier Watts | 7 | 22 | 16 | 182 | 8.3 | 0 | 1 | 6 |
| AJ Terrell | 4 | 17 | 11 | 199 | 11.7 | 4 | 0 | 3 |
| Divine Deablo | 5 | 11 | 10 | 110 | 10.0 | 0 | 0 | 1 |
| Sydney Brown | 6 | 10 | 7 | 58 | 5.8 | 1 | 0 | 3 |

### ATL pass rushers

| Defender | G | Pressures | Sacks | Hurries | Blitzes |
|---|---|---|---|---|---|
| Brandon Dorlus | 6 | 12 | 1.5 | 5 | 0 |
| Cameron Thomas | 7 | 12 | 1.5 | 3 | 0 |
| Gervon Dexter | 3 | 6 | 1.5 | 1 | 0 |
| Samson Ebukam | 3 | 6 | 2.0 | 1 | 0 |
| Maason Smith | 6 | 6 | 1.0 | 2 | 0 |
| Zach Harrison | 6 | 6 | 1.5 | 2 | 0 |
| Yasir Abdullah | 2 | 5 | 0.0 | 1 | 8 |
| Za'Darius Smith | 5 | 5 | 2.0 | 0 | 2 |

### ATL offense: what it produces (rank 1 = best offense)

| Metric | Value | Rank | League avg |
|---|---|---|---|
| Points / game | 23.1 | 16/32 | 23.2 |
| Pass yards / game | 220.5 | 20/32 | 234.2 |
| Yards per pass attempt | 7.23 | 18/32 | 7.12 |
| Rush yards / game | 121.4 | 6/32 | 100.6 |
| Yards per carry | 4.90 | 2/32 | 4.10 |
| RB rush yards / game | 119.1 | 4/32 | 93.4 |
| WR yards / game | 154.0 | 11/32 | 147.5 |
| TE yards / game | 43.0 | 21/32 | 53.4 |
| RB receiving yards / game | 23.5 | 24/32 | 33.2 |
| Explosive passes (20+) / game | 3.25 | 13/32 | 2.96 |
| Explosive runs (15+) / game | 1.75 | 2/32 | 1.23 |
| Sack rate allowed | 4.5% | 7/32 | 6.5% |
| Pressure rate allowed (sacks + hits) | 7.1% | 1/32 | 15.4% |
| Third-down conversion rate | 37.5% | 20/32 | 39.4% |
| Red-zone TD rate | 54.8% | 24/32 | 58.9% |

Neutral-situation pass rate 46.2%; 58.0 plays per game; target share WR 58% / TE 24% / RB 18%.

### ATL offense, game by game

| Wk | Opp | Pts | Pass yds | Rush yds | RB rush | WR rec-yds | TE rec-yds | RB rec-yds | Expl pass | Expl run | Sacks taken |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | @ GB | 35 | 256 | 244 | 244 | 13-221 | 3-16 | 2-19 | 3 | 3 | 0 |
| 4 | @ NO | 45 | 223 | 207 | 207 | 9-160 | 4-56 | 2-7 | 5 | 1 | 1 |
| 5 | vs BAL | 23 | 274 | 102 | 102 | 11-187 | 6-55 | 4-32 | 4 | 2 | 3 |
| 6 | vs CHI | 23 | 225 | 62 | 62 | 9-158 | 6-66 | 4-1 | 4 | 1 | 5 |
| 7 | vs SF | 29 | 213 | 83 | 72 | 9-95 | 10-54 | 6-64 | 1 | 0 | 0 |
| 8 | @ TB | 0 | 125 | 92 | 88 | 4-107 | 3-15 | 1-3 | 1 | 1 | 0 |
| 9 | vs CIN | 17 | 162 | 107 | 107 | 8-89 | 4-24 | 8-49 | 2 | 4 | 0 |
| 10 | vs KC | 13 | 286 | 74 | 71 | 12-215 | 5-58 | 6-13 | 6 | 2 | 3 |

**QB M.Penix** (8 games): 147/241, 1730 yds, 10 TD, 7 INT, 12 sacks, 7.18 yds/att, depth of target 7.6, pressured on 7.5% of dropbacks. Yards by game: W3 256, W4 223, W5 240, W6 225, W7 213, W8 125, W9 162, W10 286.

**QB T.Tagovailoa** (1 games): 2/3, 34 yds, 0 TD, 1 INT, 0 sacks, 11.33 yds/att, depth of target 9.7, pressured on 0.0% of dropbacks. Yards by game: W5 34.

### ATL receivers

| Player | Pos | G | Tgt | Rec | Yds | TD | Tgt share | Air share | aDOT | RZ tgt | 20+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D.London | WR | 8 | 70 | 44 | 721 | 1 | 30% | 43% | 10.8 | 5 | 13 | 194 96 118 62 66 8 68 109 |
| K.Pitts | TE | 8 | 38 | 28 | 255 | 4 | 16% | 10% | 4.5 | 8 | 3 | 5 47 42 60 22 6 23 50 |
| J.Dotson | WR | 8 | 31 | 16 | 386 | 2 | 13% | 28% | 15.9 | 7 | 7 | 11 54 54 87 6 95 16 63 |
| Bi.Robinson | RB | 6 | 19 | 14 | 104 | 0 | 8% | -1% | -1.4 | 2 | 0 | 19 2 32 -8 59 0 |
| O.Zaccheaus | WR | 6 | 16 | 6 | 35 | 0 | 7% | 7% | 8.0 | 5 | 0 | 9 0 0 4 5 17 |
| B.Robinson | RB | 2 | 12 | 10 | 53 | 0 | 5% | -0% | -0.7 | 3 | 1 | 47 6 |
| Z.Branch | WR | 5 | 10 | 8 | 50 | 0 | 4% | 2% | 3.7 | 1 | 1 | 7 10 15 9 9 |
| A.Hooper | TE | 6 | 8 | 8 | 64 | 1 | 3% | 2% | 4.0 | 1 | 0 | 11 9 6 21 9 8 |
| K.Herbert | RB | 4 | 8 | 6 | 31 | 0 | 3% | -1% | -1.4 | 1 | 0 | 19 3 2 7 |

### ATL rushers

| Player | Pos | G | Car | Yds | YPC | TD | Carry share | RZ car | 15+ | Yards by game |
|---|---|---|---|---|---|---|---|---|---|---|
| Bi.Robinson | RB | 6 | 113 | 625 | 5.53 | 4 | 57% | 24 | 7 | 194 145 86 61 63 76 |
| B.Robinson | RB | 2 | 35 | 171 | 4.89 | 2 | 18% | 8 | 3 | 100 71 |
| Br.Robinson | RB | 4 | 33 | 129 | 3.91 | 4 | 17% | 6 | 1 | 50 62 16 1 |
| K.Herbert | RB | 3 | 7 | 28 | 4.00 | 0 | 4% | 1 | 0 | 9 12 7 |
| M.Penix | QB | 6 | 7 | 7 | 1.00 | 0 | 4% | 0 | 0 | 0 0 0 4 0 3 |

### ATL run game by direction

| Direction | Carries | Yards | YPC | 15+ |
|---|---|---|---|---|
| middle | 45 | 146 | 3.24 | 1 |
| left tackle | 35 | 132 | 3.77 | 1 |
| left guard | 35 | 163 | 4.66 | 2 |
| left end | 31 | 260 | 8.39 | 5 |
| right tackle | 19 | 76 | 4.0 | 0 |
| right guard | 17 | 96 | 5.65 | 1 |
| right end | 13 | 98 | 7.54 | 1 |

### ATL by formation and pass zone

| Side | Formation | Plays | Share | Pass rate | Yards / play | EPA / play |
|---|---|---|---|---|---|---|
| offense | Shotgun | 232 | 50% | 78% | 6.36 | -0.063 |
| offense | Under center | 202 | 44% | 28% | 5.31 | 0.043 |
| offense | No huddle | 30 | 6% | 93% | 6.97 | -0.008 |
| defense vs | Shotgun | 297 | 58% | 74% | 5.98 | 0.054 |
| defense vs | Under center | 193 | 38% | 31% | 5.73 | 0.059 |
| defense vs | No huddle | 24 | 5% | 83% | 4.25 | 0.122 |

| Side | Pass zone | Attempts | Share | Completion | Yards / attempt | 20+ |
|---|---|---|---|---|---|---|
| offense | Short left | 95 | 39% | 65% | 4.92 | 4 |
| offense | Short middle | 37 | 15% | 62% | 6.27 | 3 |
| offense | Short right | 66 | 27% | 68% | 6.44 | 4 |
| offense | Deep left | 22 | 9% | 46% | 17.41 | 8 |
| offense | Deep middle | 11 | 4% | 27% | 8.73 | 3 |
| offense | Deep right | 13 | 5% | 46% | 12.38 | 4 |
| defense allows | Short left | 78 | 28% | 82% | 6.76 | 4 |
| defense allows | Short middle | 39 | 14% | 67% | 6.56 | 1 |
| defense allows | Short right | 109 | 40% | 69% | 5.73 | 5 |
| defense allows | Deep left | 24 | 9% | 29% | 9.08 | 5 |
| defense allows | Deep middle | 8 | 3% | 75% | 21.12 | 5 |
| defense allows | Deep right | 17 | 6% | 41% | 12.71 | 5 |

### ATL lines (depth chart as of 2026-11-26T17:41:02Z)

Offensive line: LT Jake Matthews, LG Matthew Bergeron, C Corey Levin, RG Chris Lindstrom, RT Jawaan Taylor.  
Defensive front: LDE Maason Smith, NT Gervon Dexter Sr., RDE Brandon Dorlus, WLB Cameron Thomas, SLB James Pearce Jr..

### ATL injuries

Official report not posted yet for this week.

ESPN live list (designations only): Matthew Bergeron (G) Questionable; Billy Bowman Jr. (CB) Questionable; DeMarcco Hellams (S) Questionable; Zachariah Branch (WR) Questionable; Za'Darius Smith (DE) Questionable; Cameron Thomas (DE) Questionable; Jahan Dotson (WR) Questionable; Kendal Daniels (LB) Questionable.
ESPN returns at most 25 entries per team, newest first; older entries (long-term injured reserve) can be cut off. 'Active' means ESPN lists the player with no game designation.

A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file.

### ATL roster moves (last 4 weeks)

Arrived: Terell Smith (DB) from PIT.  
Left for another team: Jessie Bates (DB) to JAX; Ryan Neuzil (OL) to BAL; Colby Sorsdal (OL) to NO.

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
