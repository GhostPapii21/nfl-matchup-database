# Week 9 phase ledger refresh — 2026-11-08 14:41 ET

> Follow-up refresh to the 14:18 ET snapshot. Captured 2026-11-08T14:41:09-05:00 (19:41:09Z). The frozen 08:56 ET forecast remains unchanged.

**Captured:** 2026-11-08T14:18:44-05:00 (2026-11-08T19:18:44Z)  
**Scope:** Six games not yet started: HOU–LAC, LV–SF, GB–NE, ARI–SEA, TB–CHI, and BUF–MIN Monday. The 9:30 and 1 p.m. windows are underway or final and are not part of this pregame refresh.  
**Readiness:** research only; `projection_ready=false`, `full_integration_acceptance=false`, calibration not established.  
**Locked forecast:** `NFL_W9_PROSPECTIVE_FREEZE_20261108_0856ET` remains unchanged. No weather or injury update was used to regenerate probabilities.

## Audit result

- **Frozen-artifact validator:** PASS, rerun at 14:17 ET. Verified locked file hashes, 471 rows × 100,000 simulations, 157 book-market lines, and 139 exact-threshold rows.
- **Current snapshot/source checks:** PASS. All 15 ordered phases remain; all six remaining games have official NFL inactive, team status, NWS weather, and roof sources with retrieval timestamps.
- **Fail-closed gates:** PASS. Production readiness and calibration remain false.
- **Forecast lock:** unchanged; no frozen files or inputs were edited.

## Ordered phase ledger

| Phase | Name | Status | Evidence / blocker |
|---:|---|---|---|
| 1 | slate_schedule_venue | COMPLETE | NFL.com Week 9 schedule |
| 2 | player_identity_position | PARTIAL | current player pool and prop tracker; unresolved joins possible |
| 3 | verified_player_game_history | PARTIAL | verified Weeks 1-8 file; zero-opportunity vs inactive unresolved |
| 4 | role_snaps_routes_opportunity | PARTIAL | historical market opportunity and role board; incomplete route/snap availability |
| 5 | team_offense_defense_baselines | PARTIAL | existing team and defense snapshot; source freshness not uniform |
| 6 | opponent_context_game_script | PARTIAL | capped exploratory factors; not independently validated |
| 7 | coverage_structure_shell | BLOCKED_QUALITATIVE | full-slate verified coverage chart unavailable |
| 8 | defender_assignment_explosive_allowance | BLOCKED_QUALITATIVE | full-slate assignment/exposure unavailable |
| 9 | qb_pressure_blitz_scramble | PARTIAL_NOT_IN_CURRENT_SIM | not fully integrated into current slate simulations |
| 10 | offensive_line_pass_rush_coaching | PARTIAL | not a complete verified matchup-adjustment layer |
| 11 | injury_depth_chart | PENDING_LATE_FINAL_INACTIVES | NFL.com consolidated Week 9 inactive page rechecked at 2026-11-08T14:18:44-05:00; the page still has no late-window inactive names. Official team Week 9 injury/game-status pages were rechecked; those contain OUT/questionable designations, not final game-day lists. HOU-LAC game-day window has not arrived; later Sunday and Monday lists remain pending. |
| 12 | weather_roof_travel | PARTIAL_KICKOFF_NEAR_WEATHER_REFRESH | Official NWS venue-area forecasts refreshed at 14:18 ET for all six not-yet-started games; issue/observation times captured per row. Chicago has an NWS hourly forecast at 7 p.m. CST; Seattle and Foxborough have updated this afternoon. Roof configuration source URLs and retrieval times recorded per row. No locked forecast inputs changed. |
| 13 | timestamped_book_prices | PARTIAL | 08:23 ET DK/FD refresh for 79 player-market rows; no 09:30 quote |
| 14 | projection_simulation | PARTIAL_RESEARCH_ONLY | 471 rows; 157 lines times three 100000-draw models; no Bengals-Falcons rows |
| 15 | final_inactives_pregame_freeze | PARTIAL_WAITING_LATE_WINDOWS | NFL official lists posted for seven 13:00 ET games. Late Sunday games have no final inactives posted as of 11:58:52 ET and are not yet in the 90-minute window; Monday BUF-MIN is not yet due. Whole-slate pregame freeze remains pending. |

## Remaining games

| Kickoff | Game | Venue | Inactive status | Weather / roof |
|---|---|---|---|---|
| 16:05 ET | HOU–LAC | SoFi Stadium | PENDING_NOT_YET_POSTED | FIXED_ROOF_CLIMATE_CONTROLLED / FIXED_ROOF_CLIMATE_CONTROLLED |
| 16:25 ET | LV–SF | Levi's Stadium | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST / OUTDOOR_OPEN_AIR |
| 16:25 ET | GB–NE | Gillette Stadium | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST / OUTDOOR_OPEN_AIR |
| 16:25 ET | ARI–SEA | Lumen Field | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST / OPEN_AIR_FIELD_PARTIAL_CANOPY |
| 20:20 ET | TB–CHI | Soldier Field | PENDING_NOT_YET_POSTED | OPEN_AIR_KICKOFF_HOURLY / OUTDOOR_FIELD |
| 20:15 Monday ET | BUF–MIN | U.S. Bank Stadium | PENDING_NOT_YET_DUE | FIXED_ROOF_CLIMATE_CONTROLLED / FIXED_ROOF_CLIMATE_CONTROLLED |

## Inactives

The [NFL Week 9 inactive page](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season) was checked at 2026-11-08T14:18:44-05:00. Its displayed last update remains 11:43 a.m. ET and it still lists the late game headers without player inactive lists. The official team Week 9 reports below are game-status/injury reports, not final active/inactive lists. Do not convert OUT or QUESTIONABLE to a final inactive entry.

| Game | Official team sources checked | Final list |
|---|---|---|
| HOU–LAC | [team report](https://www.houstontexans.com/news/week-9-injury-report-texans-at-chargers); [team report](https://www.chargers.com/media/2026-season/week-9) | PENDING_NOT_YET_POSTED |
| LV–SF | [team report](https://www.raiders.com/news/raiders-49ers-week-9-injury-report); [team report](https://www.49ers.com/team/injury-report/) | PENDING_NOT_YET_POSTED |
| GB–NE | [team report](https://www.packers.com/team/injury-report/); [team report](https://www.patriots.com/news/week-9-injury-report-patriots-vs-packers) | PENDING_NOT_YET_POSTED |
| ARI–SEA | [team report](https://www.azcardinals.com/news/injury-report-week-9-vs-seahawks-x2054); [team report](https://www.seahawks.com/news/week-9-injury-report-cardinals-at-seahawks) | PENDING_NOT_YET_POSTED |
| TB–CHI | [team report](https://www.buccaneers.com/news/buccaneers-bears-injury-report-nov-6-week-9-2026); [team report](https://www.chicagobears.com/team/injury-report/index-mobile) | PENDING_NOT_YET_POSTED |
| BUF–MIN | [team report](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings-week-9); [team report](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season) | PENDING_NOT_YET_DUE |

At 14:18 ET, HOU–LAC is 1 hour 47 minutes before its 4:05 p.m. kickoff, so its expected game-day inactive window has not arrived. The 4:25 p.m. games, Sunday night game, and Monday game remain pending their official releases.

## Weather and roof refresh

All NWS and venue pages below were retrieved during this pass at 2026-11-08T14:18:44-05:00. Forecast issue/observation timestamps are stated separately; where a source did not expose an issue time, that limitation is recorded.

| Game | Updated weather evidence | Roof evidence |
|---|---|---|
| HOU–LAC | NWS Hawthorne/Inglewood observation 10:20 a.m. PST: 82°F, NE 4 mph. Forecast sunny, high near 87°F, NE 5–10 mph becoming WNW. [NWS](https://forecast.weather.gov/MapClick.php?CityName=Inglewood&lat=33.9345&lon=-118.332&site=LOX&state=CA), forecast updated 10:26 a.m. PST. | Fixed roof and climate control; outside weather not applied to field conditions. [SoFi official A–Z guide](https://www.sofistadium.com/plan-your-visit/a-z-guide). |
| LV–SF | NWS San Jose observation 10:35 a.m. PST: 63°F, calm. Mostly sunny, high near 74°F; NNW around 6 mph afternoon. [NWS](https://forecast.weather.gov/MapClick.php?lat=37.35&lon=-121.96), point forecast updated 10:26 a.m. PST. | Levi’s is predominantly open and airy. [Official stadium facts](https://levisstadium.com/seats/). |
| GB–NE | NWS Norwood observation 12:53 p.m. EST: 56°F, west 16 mph gusting 24. Updated forecast for afternoon: clouds becoming sun, high near 58°F; west around 14 mph, gusts near 29. [NWS](https://forecast.weather.gov/MapClick.php?lat=42.065870000000075&lon=-71.24838999999997), forecast update 1:21 p.m. EST. | Open-air venue. [Patriots venue statement](https://www.patriots.com/news/p-g-extends-naming-rights-for-gillette-stadium-through-the-2031-season). |
| ARI–SEA | NWS Boeing Field observation 10:53 a.m. PST: 57°F, south 11 mph. Forecast partly sunny, high near 56°F; SSW 8–14 mph. [NWS](https://forecast.weather.gov/MapClick.php?lat=47.6015014648438&lon=-122.334297180176), point forecast update 10:26 a.m. PST. Recheck nearer 1:25 p.m. PST kickoff. | Open-air playing field with partial seating canopy. [Seahawks gameday FAQ](https://www.seahawks.com/game-day/frequently-asked-questions/mobile-view). |
| TB–CHI | NWS hourly forecast for the 7 p.m. CST kickoff hour: about 51°F, clear, NW around 9 mph, 0% precipitation. [NWS hourly forecast](https://beta.weather.gov/forecast/point/41.85/-87.65/7-day/). The page does not expose the hourly product issue time; its underlying point forecast shows a 9:41 a.m. CST update. | Open-air field. [AP venue context](https://apnews.com/article/f1b075eff96cfbec693cf23962745c74). |
| BUF–MIN | Monday NWS Minneapolis forecast: cloud early then clearing, high near 59°F, south 5–10 mph becoming west. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=1&lat=44.9486&lg=english&lon=-93.2451&unit=0), forecast updated 10:46 a.m. CST Nov 8. | Fixed roof and climate controlled; outdoor forecast not applied to field. [Vikings stadium guide](https://www.vikings.com/stadium/a-to-z). |

## Still open

1. Recheck official NFL and team inactive lists after each game-day release window; retain pending status until names are published.
2. Recheck Seattle weather nearer kickoff; the 10:26 a.m. PST update precedes kickoff by about two hours.
3. Score the prospective forecasts only after verified official outcomes. Week 9 alone does not establish calibration.
4. Complete full integration and production acceptance evidence. Keep production readiness and calibration false until those gates pass.


## Follow-up refresh — 14:41 ET

Official NFL inactive article was rechecked at **2026-11-08 14:41 ET**. The early-game entries remain populated, but no names are published beneath the remaining-game headers. The HOU–LAC inactive window (about 2:35 p.m. ET) has passed; its list is now **overdue and pending official publication**. The 4:25 p.m. ET games are not due until about 2:55 p.m.; TB–CHI is due about 6:50 p.m.; BUF–MIN is Monday. The Chargers’ official game page still exposes an INACTIVES heading without an accessible list. Do not infer final status from weekly OUT/QUESTIONABLE designations.

NWS venue-area pages and venue roof sources were rechecked at 14:41 ET. Forecasts reviewed: Inglewood mostly clear/sunny, high near 87°F; Santa Clara mostly sunny, high near 74°F; Foxborough/Norwood partly cloudy becoming sunnier, high near 58°F with west wind/gusts; Seattle chance of light rain then mostly cloudy, high near 56°F; Chicago kickoff-hour clear near 51°F with NW wind around 9 mph; Minneapolis Monday high near 59°F (outdoor weather not relevant inside fixed-roof U.S. Bank Stadium). Roof classifications are unchanged. Exact source URLs, retrieval times, and forecast issue timestamps are in the companion snapshot.

**Audit:** Existing validator rerun at 14:41 ET — PASS for 15 phases, frozen hashes, 471 × 100,000 simulations, 157 lines, and 139 exact-threshold rows. Production readiness and calibration remain false. No forecast, odds, simulation, or overlay inputs were changed.
