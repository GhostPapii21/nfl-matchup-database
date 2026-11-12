# Source audit — 2026-11-01 (Weeks 7-8 sample)
Rico: "Do it to all NFL sites we use to see if that also things our data collection that clouds our judgement." Method: systematic-debugging. Every source is cross-checked against at least one independent source, every gap gets a root cause, and our own bugs are fixed test-first (BUGLOG SA-1..3). **This file recommends only; the source list is unchanged.** Times ET.

## What's tainting our data (plain language, read this first)
| Source | What was wrong | How far off | Evidence | What we do |
|---|---|---|---|---|
| PFF props tool weather | Same sun icon on every row, rain games included (ATL@TB, NE@MIA) | Total: TB had 0.18 in/hr and heavy rain at KTPA 2:15-2:53 PM; PFF showed sun | pff_raw/w8_player_props_tool.png; weather_wk8.json | Never use PFF weather. Use Open-Meteo/NWS only |
| PFF prop picks | Pick line isn't the consensus line (Gainwell pick u2.5 vs consensus 1.5; Coleman u3.5 vs 2.5); projections sit far below the lines (Washington 0.49 vs 5.5; McNichols 3.60 vs 6.5 att) | One full line off; edges of +30-42% are artifacts of a soft line | Screenshot. Actuals: Tuten u68.5 → 104 (lost), Coleman u3.5 → 4 (lost), Taylor o13.5 → 8 (lost), Gainwell u2.5 → 0 (won), Gibbs TD hit, McNichols already 21 yds > 20.5 at SNF Q3 | Re-price every PFF pick at our book line. Never take PFF's edge % |
| PFF lean vs its own matchup | Under leans next to GOOD matchups (Burden u4.5 rush yds); WR matchup GOOD for Pickens at 22/115 vs ARI (30th) | Direction contradicts itself | Screenshot / matchups tool | Treat a PFF lean as a hint. Confirm with our own matchup data |
| PFF week labels / staleness | Matchups "Updated Nov 01 10:27pm" but shows Week 8; weekAbbr=9 and /scores/2026/9 return Week 8; injury tool reads "WEEK 3 · SUNDAY NOV 1" with an inactives countdown after the games were final; finished games still show kickoff (GB vs CAR "THU 8:15PM"); Week 9 props page is empty | A whole week behind | Screenshots | Check the week on every PFF pull. Don't use PFF for Week 9 yet |
| PFF injury tool | Missing Mike Washington Jr. and Emmett Johnson; article dated Oct 28 | 4 days old | w8_injury_report.png | Use the ESPN injuries API |
| Sharp coverage | "Updated Oct 27": Week 8 isn't in it, and its man % disagrees with StatRankings (ATL 21.9 vs 35.9; CLE 42.4 vs 55.8) | 11-14 pts | Saved pages | Crosscheck. Never cite it alone |
| StatRankings OL page | Titled 2026 but says "2025 season stats, couldn't update" (last updated 07/23/26) | A full season backwards | Page text | Drop this page (we don't currently use it) |
| Outlier | Two lines for one player (Puka 91.5/94.5); Bowers 5.5 vs DK 6.5; Opp Rank uses 1 = toughest; relays Polymarket TD prices like -10639 | 1-3 yd or 1-rec line drift; the rank scale is backwards from other sites | Saved Oct 30/31 pulls | Use the DK/FD line only. Flip Opp Rank before comparing |
| Polymarket props | Odd low lines (Mahomes pass yds 124.5, Goff 174.5); titles list the away team first | Unusable lines | Gamma API | Results trusted. Props crosscheck |
| nflverse/NGS/FTN | Lag: NGS through Wk 7 only; FTN Wk 8 has only CAR_GB; participation parquet is a 9-byte "Not Found" | 1 week | Parquets | Check max(week) before use |
| Film / team notes | Film last processed Wk 6 (Oct 20); team_notes through Oct 24 | 1-2 weeks | processed-games.json | Mark stale. Don't use it for Wk 9 leans |
| OUR side | wind blank read as 0, WX8 missing NE@MIA, in-play odds counted as pregame (SA-1..3); LAC coverage numbers credited to "StatRankings/FTN" but they're Sharp's (SA-8); CAR@GB row was missing from game_scripts (SA-9, now fixed) | — | BUGLOG | Patches drafted / row added |

## Grades
| Source | Sampled? | Cross-check | Result | Grade |
|---|---|---|---|---|
| ESPN (scoreboard, summary box, standings) | Yes | 8 Wk8 finals vs PFF ticker + our playlogs; 8 team records rebuilt Wk1-8 | All match | **trusted** (but our playlog is ESPN-derived, so it's not an independent check of ESPN stats) |
| ESPN win rates (article) | Yes | vs our nflverse run-block composite | Direction agrees for 8/8 sampled teams on run block (KC 7th vs our 5th). The page lags: "thru Wk7, Oct 27" | **trusted, note the as-of date** |
| ESPN injuries API | Yes | file 11:52 vs 18:52 | Statuses agree; comment dates are stale (E. Johnson note dated Oct 27), and players drop on/off the list between pulls | **crosscheck-required** (pair with team reports/inactives) |
| nflverse pbp / snaps | Yes | vs ESPN scores; weather strings vs NWS | Accurate but lagged: the 07:09 pull holds only Wk8 TNF, and `wind` is NaN in 31/75 outdoor games (string still has it → our SA-1 bug) | **trusted, check freshness first** |
| PFR | Tried | — | 403 on box scores; respected, not retried | **unavailable** (don't depend on it) |
| NGS, NFL Football Ops | No (Wk8 not posted yet) | — | — | not sampled |
| Open-Meteo / NWS | Yes | each vs the other + our script notes | Agree (Tampa rain 1-5 PM; MIA rain ended ~4 PM) | **trusted** |
| PFF | Partly | see PFF_AUDIT_2026-11-01.md | Records & finals correct; grades padlocked on PFF+ Monthly (**unverifiable**); weather "sunny" for a rain game (screenshot); KC run-block 28th vs ESPN 7th / ours 5th; props page projections lean under (136/196) and are half-point snapped (54% vs ~4% expected); 5 of 7 key Wk8 RB unders lost | **crosscheck-required** for grades; **drop** PFF weather and PFF prop projections as inputs |
| The Odds API (incl. Pinnacle, DK, FD books through it) | Yes | pull time vs commence_time | 34-50% of rows in the afternoon re-pulls were quoted AFTER kickoff (live lines), e.g. Stafford DK 168.5 vs Pinnacle 248.5. Root cause: **our pull** has no kickoff filter (SA-3) | **trusted once our filter is applied** |
| FanDuel / DraftKings / PrizePicks raw files | Partly | cross-book spread | Main-market gaps of ≥5 yds are 34/145 in i1850, mostly the in-play rows above. Stamps ET, correct | **crosscheck-required** (pregame rows only) |
| Outlier (read-only), Polymarket (via Outlier rows) | No | — | — | not sampled |
| FTN, Sharp Football Analysis, StatRankings, PropsMadness, SumerSports, Fantasy Points (probation), film/news | No (time) | — | — | not sampled. Keep current status; Fantasy Points stays on probation |


### Third-pass grades (Weeks 7-8)
| Source | Grade | Why |
|---|---|---|
| FTN (via nflverse ftn_charting) | trusted (check freshness) | 2,537/2,537 Wk 7-8 rows match pbp. Wk 8 has only CAR_GB. ftnfantasy.com 403 → public site unavailable |
| NGS (via nflverse) | trusted, lagged | Wk 7 rush yds 26/26, rec yds 61/61, targets 58/61. No Wk 8. API 401 (respected) |
| Sharp coverage | crosscheck-required | Oct 27 stamp; man % 11-14 pts off StatRankings; man + zone ≠ 100 |
| StatRankings | coverage crosscheck-required; OL page drop | OL page shows 2025 data |
| SumerSports | trusted | Updated 11-01 7:50 PM ET; team rush yds exact for 6/6 teams through Wk 8 |
| PropsMadness | unavailable | Login wall; public sample shows 2025-26 |
| Fantasy Points | unavailable / stays on probation | No dated data on public pages |
| Outlier | crosscheck-required (read-only) | Duplicate/off lines, reversed rank scale |
| Polymarket | trusted for results / crosscheck-required for props | 8/8 Wk 8 resolutions correct |
| NFL Football Ops | unavailable | Schedule URL 404 |
| Film feed | stale | Wk 6 |
| News/team notes | stale | Oct 24. ESPN injuries API used instead |
| PFF | crosscheck-required (records/finals trusted; weather, week labels, pick lines are not; grades unverifiable on plan) | See PFF_AUDIT |

## Our own collection (the "clouds our judgement" part)
| Id | Issue | Class | Status |
|---|---|---|---|
| SA-1 | `wind.fillna(0)`: missing wind read as calm (scan_data, harness) | our-pipeline bug (None-as-0) | **fixed**, tools/tests/test_wind_parse.py; no wx flag changed in Wk1-8 |
| SA-2 | WX8 missing NE@MIA though phase15 flagged rain | our-pipeline bug | **fixed**, same test file |
| SA-3 | In-play odds mixed into pregame pulls (pull_odds.py, no commence filter, hardcoded dates) | our-pipeline bug | helper + 3 tests landed (tools/odds_pregame.py); **patch pending**: source_audit_patches/pull_odds_pregame.patch.md. No placed leg shown affected |
| SA-4 | `odds_final.csv` / `lines_final.json` = the 07:30 pull, OLDER than later pulls | naming/staleness hazard | recommend renaming to `odds_0730.csv`; not changed |
| SA-5 | pff_props csv `captured_et 07:40` > file mtime 07:34 | manual stamp, inaccurate | recommend using the file mtime / a real capture time |
| SA-6 | pull_props.py `float(line or 0)` makes fake line moves | None-as-0 (print only) | patch: source_audit_patches/pull_props_none_as_zero.patch.md |
| SA-7 | game_scripts_2026.csv Wk8 has no CAR@GB (TNF) row | coverage gap | note only |
| — | UTC vs ET: FD stamps ET, ESPN injury UTC matches mtimes, pull_weather KO hours UTC | checked | OK, no bug |

- SA-8: betguru_three_groups l.277 attributes "LAC man 10.6 / zone 58.0, MOFC 33.9 / MOFO 40.7" to StatRankings/FTN; they are Sharp's numbers. Fix the label (not edited by me).
- SA-9: game_scripts_2026.csv was missing CAR@GB Wk 8. Added 2 rows from ESPN summary 401873023 (backup .pre_cargb.bak; test playlogs/tools/test_game_scripts_wk8.py, red→green).

## Recommendations (need Rico's OK; nothing changed)
1. Weather: NWS + Open-Meteo only; never PFF/site icons.
2. PFF: use only for things a second public source confirms; drop PFF props-page projections/edges as a signal; grades are unverifiable on PFF+ Monthly, so either accept them as screenshots-only or upgrade if grades matter.
3. Odds: apply the SA-3 kickoff filter before any line-move / CLV / cross-book comparison.
4. Freshness gate: before a run, print the as-of time of nflverse pbp/snaps and ESPN win rates; the Wk8 OL view is Wk7 data everywhere until Monday.
5. PFR: treat as unavailable (403).
6. Sample the unsampled coverage/odds sources next pass (FTN, Sharp, StatRankings, PropsMadness, SumerSports, Fantasy Points, Outlier, Polymarket) on Wk7 finals.
