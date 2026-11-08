# Week 9 Phase Ledger — 2026-11-08 17:51 ET

Captured: 2026-11-08T17:51:07-05:00  
Remaining Week 9: HOU-LAC, LV-SF, GB-NE and ARI-SEA are underway; TB-CHI is scheduled for Sunday night; BUF-MIN is scheduled Monday.  
NFL consolidated inactive source: [NFL Week 9 inactives](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season), retrieved 17:51 ET; page last updated 3:04 PM ET.  
Locked forecast: `NFL_W9_PROSPECTIVE_FREEZE_20261108_0856ET` remains unchanged.

## Inactives, weather and roof

| Game | Inactives / official team-source status | Kickoff-near weather | Roof status |
|---|---|---|---|
| HOU-LAC (4:05 ET) | NFL final list captured; underway. [Chargers official inactive page](https://www.chargers.com/news/texans-inactives-week-9-2026) corroborates LAC. No Houston-specific final inactive page located. | [NWS Hawthorne](https://forecast.weather.gov/MapClick.php?CityName=Inglewood&lat=33.9345&lon=-118.332&site=LOX&state=CA): clear, 87°F, N calm; latest displayed observation 12:53 PM PST. | SoFi fixed roof, climate controlled. [Venue guide](https://www.sofistadium.com/plan-your-visit/a-z-guide). |
| LV-SF (4:25 ET) | NFL final list captured; underway. [Raiders official list](https://www.raiders.com/news/las-vegas-raiders-week-9-inactives-vs-san-francisco-49ers) confirms LV. [49ers injury page](https://www.49ers.com/team/injury-report/week/div-2) is weekly status; no 49ers final inactive article located. | [NWS San Jose/Santa Clara](https://forecast.weather.gov/MapClick.php?lat=37.35&lon=-121.96): mostly cloudy, 71°F, N 3 mph; observation 12:53 PM PST. Forecast partly sunny, high near 74°F, NNW near 6 mph. | Levi’s Stadium open air. [Venue page](https://levisstadium.com/seats/). |
| GB-NE (4:25 ET) | NFL final list captured; underway. [Patriots official game-day report](https://www.patriots.com/news/week-9-inactives-packers-at-patriots-x4933) lists both teams. | [NWS Norwood](https://forecast.weather.gov/MapClick.php?lat=42.065870000000075&lon=-71.24838999999997): fair, 55°F, W 9 mph gusting 21; latest observation 3:53 PM EST, close to kickoff. | Gillette Stadium open air. [Patriots venue announcement](https://www.patriots.com/news/p-g-extends-naming-rights-for-gillette-stadium-through-the-2031-season). |
| ARI-SEA (4:25 ET) | NFL final list captured; underway. [Seahawks official game-day report](https://www.seahawks.com/news/seahawks-vs-cardinals-week-9-inactives) lists both teams. | [NWS Boeing Field/Seattle](https://forecast.weather.gov/MapClick.php?lat=47.6015014648438&lon=-122.334297180176): clear, 59°F, S 13 mph; observation 1:30 PM PST. Forecast partly sunny, high near 56°F, SSW 8–11 mph. | Lumen open-air playing surface, partial spectator canopy. [Seahawks FAQ](https://www.seahawks.com/game-day/frequently-asked-questions/mobile-view). |
| TB-CHI (8:20 ET) | **Pending.** NFL article checked 5:51 PM ET still has no Sunday-night names. Expected 90-minute window ~6:50 PM ET (about 59 minutes after this check). [Buccaneers](https://www.buccaneers.com/news/buccaneers-bears-injury-report-nov-6-week-9-2026) and [Bears](https://www.chicagobears.com/team/injury-report/index-mobile) pages show weekly statuses, not final inactive lists. | [NWS Chicago hourly forecast](https://beta.weather.gov/forecast/point/41.85/-87.65/7-day/): 7 PM CST clear, 53°F, W 9 mph; 8 PM clear, 51°F, NW 9 mph; 0% precipitation. Latest displayed Midway observation is 2:53 PM CST: 60°F, W 16 mph gusting 26. | Soldier Field open air. [Official stadium info](https://www.soldierfield.com/stadium-info). |
| BUF-MIN (Monday 8:15 ET) | **Pending—not yet due.** Sunday NFL list is not the final report for Monday's game. Bills and Vikings weekly status pages checked: [Bills](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings-week-9), [Vikings](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season). | [NWS Minneapolis](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=1&lat=44.9486&lg=english&lon=-93.2451&unit=0): Monday cloudy early then clearing, high near 60°F, S 5–10 mph becoming west; latest forecast issue 3:16 PM CST Nov 8. | U.S. Bank Stadium fixed roof. [Vikings stadium guide](https://www.vikings.com/stadium/a-to-z). |

Source retrieval: NFL page, late-window team reports, NWS venue forecasts, and venue/roof pages rechecked 2026-11-08T17:51:07-05:00. NWS observation/forecast issue times are listed separately above. Team-specific Houston and San Francisco final-list pages remain unavailable; the NFL consolidated page is the available final source for those teams.

## Phase ledger

| Phase | Name | Status |
|---:|---|---|
| 1 | Slate, schedule, venue | COMPLETE |
| 2 | Player identity and position | PARTIAL |
| 3 | Verified player game history | PARTIAL |
| 4 | Role, snaps, routes, opportunity | PARTIAL |
| 5 | Team offense/defense baselines | PARTIAL |
| 6 | Opponent context and game script | PARTIAL |
| 7 | Coverage structure and shell | BLOCKED_QUALITATIVE |
| 8 | Defender assignment and explosive allowance | BLOCKED_QUALITATIVE |
| 9 | QB pressure, blitz, scramble | PARTIAL_NOT_IN_CURRENT_SIM |
| 10 | Offensive line, pass rush, coaching | PARTIAL |
| 11 | Injury and depth chart | PARTIAL_FINAL_INACTIVES_POSTED_LATE_WINDOWS_PENDING |
| 12 | Weather, roof, travel | PARTIAL_KICKOFF_NEAR_WEATHER_REFRESH |
| 13 | Timestamped book prices | PARTIAL |
| 14 | Projection and simulation | PARTIAL_RESEARCH_ONLY |
| 15 | Final inactive pregame freeze | PARTIAL_FINAL_LISTS_POSTED; SUNDAY_NIGHT_AND_MONDAY_PENDING |

## Readiness audit

Run: `research/validate_week9_readiness.py` at 17:52 ET.

```text
PASS: 15 phase IDs, frozen artifact hashes, 471 x 100000 simulations, 157 lines, and 139 exact-threshold rows verified.
FAIL-CLOSED: production readiness and calibration remain false; outcomes are pending; CIN-ATL 09:30 is uncovered.
```

Integrity checks pass. Fail-closed readiness remains intentional: `projection_ready=false`, `full_integration_acceptance=false`, calibration is pending, and production is research-only. TB-CHI final inactives are not due for about 59 minutes; BUF-MIN final inactives are not due until Monday. No frozen forecast, simulation, line snapshot, overlay, lock, or model parameter was modified.
