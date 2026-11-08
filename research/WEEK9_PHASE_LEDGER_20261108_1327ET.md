# Week 9 phase ledger refresh — 2026-11-08 13:27 ET

**Captured:** 2026-11-08T13:27:24-05:00 (2026-11-08T18:27:24Z)  
**Scope:** Remaining games not yet kicked off: HOU–LAC, LV–SF, GB–NE, ARI–SEA, TB–CHI on Sunday and BUF–MIN Monday. Seven 1 p.m. games have started and are outside this pregame refresh; CIN–ATL is final.  
**Readiness:** research only; `projection_ready=false`, `full_integration_acceptance=false`, calibration not established.  
**Locked forecast:** `NFL_W9_PROSPECTIVE_FREEZE_20261108_0856ET` remains unchanged. Availability and environment notes are contextual; no simulation or forecast input was regenerated.

## Readiness audit

- **Full frozen-artifact integrity:** PASS. `python research/validate_week9_readiness.py` ran at 2026-11-08T13:27:24-05:00; frozen hashes, 471 × 100,000 simulations, 157 book-market lines, and 139 exact-threshold rows matched.
- **Current phase/source audit:** PASS. All 15 phase IDs remain ordered; each of the six unstarted games has NFL inactive, NWS weather, and roof source URLs with retrieval timestamps. Final inactives remain pending.
- **Fail-closed gates:** PASS. Production readiness and calibration remain false.
- **Forecast lock:** unchanged. No locked forecast inputs were edited.

## Ordered phase ledger

| Phase | Name | Status | Current evidence / blocker |
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
| 11 | injury_depth_chart | PENDING_LATE_FINAL_INACTIVES | NFL.com consolidated Week 9 inactives rechecked at 2026-11-08T13:27:24-05:00; article last updated 11:43 a.m. ET and still has no late-window player lists. All five remaining Sunday games and Monday BUF-MIN remain pending final inactive reports. Weekly injury designations are not treated as final inactives. |
| 12 | weather_roof_travel | PARTIAL_LATE_WEATHER_AND_ROOF_REFRESH | NWS venue-area pages rechecked at 13:27 ET; issue/update times are retained per game. Weather context refreshed for all six unstarted games; Seattle and Chicago need closer kickoff checks because the latest forecast periods are older or broad. Roof configuration/status checked against official stadium/team sources. No locked forecast inputs were changed. |
| 13 | timestamped_book_prices | PARTIAL | 08:23 ET DK/FD refresh for 79 player-market rows; no 09:30 quote |
| 14 | projection_simulation | PARTIAL_RESEARCH_ONLY | 471 rows; 157 lines times three 100000-draw models; no Bengals-Falcons rows |
| 15 | final_inactives_pregame_freeze | PARTIAL_WAITING_LATE_WINDOWS | NFL official lists posted for seven 13:00 ET games. Late Sunday games have no final inactives posted as of 11:58:52 ET and are not yet in the 90-minute window; Monday BUF-MIN is not yet due. Whole-slate pregame freeze remains pending. |

## Remaining-game status

| Kickoff | Game / venue | Final inactive report | Weather and roof |
|---|---|---|---|
| 16:05 ET | HOU–LAC (SoFi Stadium) | PENDING_NOT_YET_POSTED | FIXED_ROOF_CLIMATE_CONTROLLED; roof FIXED_ROOF_CLIMATE_CONTROLLED |
| 16:25 ET | LV–SF (Levi's Stadium) | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST; roof OUTDOOR_OPEN_AIR |
| 16:25 ET | GB–NE (Gillette Stadium) | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST; roof OUTDOOR_OPEN_AIR |
| 16:25 ET | ARI–SEA (Lumen Field) | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST_NEAR_KICKOFF_REFRESH_PENDING; roof OPEN_AIR_FIELD_PARTIAL_CANOPY |
| 20:20 ET | TB–CHI (Soldier Field) | PENDING_NOT_YET_POSTED | OPEN_AIR_FORECAST_NEAR_KICKOFF_REFRESH_PENDING; roof OUTDOOR_FIELD |
| 20:15 Monday ET | BUF–MIN (U.S. Bank Stadium) | PENDING_NOT_YET_DUE | FIXED_ROOF_CLIMATE_CONTROLLED; roof FIXED_ROOF_CLIMATE_CONTROLLED |

### Inactive-report finding

The [official NFL Week 9 inactive article](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season) was checked at 2026-11-08T13:27:24-05:00. It was last updated at 11:43 a.m. ET and still contains no late-game inactive player lists. Official team sources below were reviewed for Week 9 game-status information, but weekly injury reports are not final inactive lists. No final inactives are inferred from OUT or QUESTIONABLE designations. The remaining Sunday lists and Monday BUF–MIN list remain pending.

| Game | Official team status sources checked (weekly status only) |
|---|---|
| HOU–LAC | [Texans](https://www.houstontexans.com/news/week-9-injury-report-texans-at-chargers); [Chargers](https://www.chargers.com/news/texans-injury-report-week-9-david-njoku) |
| LV–SF | [Raiders](https://www.raiders.com/news/raiders-49ers-week-9-injury-report); [49ers](https://www.49ers.com/team/injury-report/) |
| GB–NE | [Packers](https://www.packers.com/team/injury-report/week/REG-9); [Patriots](https://www.patriots.com/news/week-9-injury-report-patriots-vs-packers) |
| ARI–SEA | [Cardinals](https://www.azcardinals.com/news/injury-report-week-9-vs-seahawks-x2054); [Seahawks](https://www.seahawks.com/news/week-9-injury-report-cardinals-at-seahawks) |
| TB–CHI | [Buccaneers](https://www.buccaneers.com/news/buccaneers-bears-injury-report-nov-6-week-9-2026); [Bears](https://www.chicagobears.com/team/injury-report/index-mobile) |
| BUF–MIN | [Bills](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings); [Vikings](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season) |

## Weather and roof evidence

All NWS sources below were retrieved at 2026-11-08T13:27:24-05:00; forecast issue/update times are preserved in the readiness snapshot.

- **HOU–LAC, SoFi Stadium:** Inglewood forecast sunny, high near 87°F; NE 5–10 mph becoming WNW in the afternoon. Outdoor weather is not applied to field conditions: SoFi’s official guide states it has a fixed roof and climate control. [NWS](https://forecast.weather.gov/MapClick.php?CityName=Inglewood&lat=33.9345&lon=-118.332&site=LOX&state=CA) · [SoFi A–Z guide](https://www.sofistadium.com/plan-your-visit/a-z-guide).
- **LV–SF, Levi’s Stadium:** Mostly sunny after morning fog, high near 74°F; NNW around 6 mph in the afternoon. The stadium describes its design as predominantly open and airy. [NWS](https://forecast.weather.gov/MapClick.php?lat=37.3541079&lon=-121.95523559999998) · [Levi’s Stadium facts](https://levisstadium.com/seats/).
- **GB–NE, Gillette Stadium:** NWS matrix for the 4 p.m. kickoff hour: about 47°F and west wind around 10 mph; dry. No gust value is specified for that hour. The Patriots describe Gillette as an open-air facility. [NWS matrix](https://forecast.weather.gov/product.php?format=CI&glossary=0&issuedby=BOX&product=AFM&site=AFC&version=1) · [Patriots venue statement](https://www.patriots.com/news/p-g-extends-naming-rights-for-gillette-stadium-through-the-2031-season).
- **ARI–SEA, Lumen Field:** NWS forecast: showers mainly before noon/early afternoon, then partly sunny; high near 56°F, SSW 8–14 mph with gusts up to 23 mph. Forecast page last updated 11:45 p.m. PST Nov 7; current observation at Boeing Field was 54°F, S 13 mph at 8:35 a.m. PST. A closer weather check remains due. [NWS](https://forecast.weather.gov/MapClick.php?lat=47.6015014648438&lon=-122.334297180176) · [Seahawks gameday FAQ](https://www.seahawks.com/game-day/frequently-asked-questions/mobile-view).
- **TB–CHI, Soldier Field:** NWS Chicago forecast is sunny by day, mostly clear at night, low near 41°F, WNW 5–10 mph with gusts up to 15 mph. Forecast is broad for 7:20 p.m. kickoff; refresh hourly data closer to game time. Soldier Field is recorded as open-air. [NWS](https://forecast.weather.gov/MapClick.php?lat=41.8181&lon=-87.6954) · [AP stadium context](https://apnews.com/article/f1b075eff96cfbec693cf23962745c74).
- **BUF–MIN, U.S. Bank Stadium:** Minneapolis Monday forecast: clouds early then clearing, high near 58°F, S 5–10 mph becoming W. No outdoor field exposure under the stadium’s fixed roof. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=1&lat=44.9486&lg=english&lon=-93.2451&unit=0) · [Vikings stadium guide](https://www.vikings.com/stadium/a-to-z).

## Still open

1. Recheck NFL and team inactive pages as game-day release windows arrive; keep each matchup pending until an official list appears.
2. Refresh ARI–SEA and TB–CHI weather nearer kickoff; the available forecasts are still broad or stale for the later windows.
3. Score prospective forecasts only after verified official outcomes. Week 9 alone cannot establish calibration.
4. Complete independent integration and production acceptance; readiness and calibration stay false until acceptance evidence passes.
