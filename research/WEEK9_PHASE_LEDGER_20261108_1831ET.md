# Week 9 Phase Ledger — 2026-11-08 18:31 ET

Captured: 2026-11-08T18:31:27-05:00.  
Remaining games: HOU-LAC, LV-SF, GB-NE and ARI-SEA are underway; TB-CHI is tonight; BUF-MIN is Monday.  
NFL source: [NFL Week 9 inactives](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season), checked 18:31 ET. No TB-CHI list is posted yet.  
Forecast lock `NFL_W9_PROSPECTIVE_FREEZE_20261108_0856ET`: **UNCHANGED**.

## Current inactive, weather and roof status

| Game | Inactive status | Weather and roof |
|---|---|---|
| HOU-LAC, 4:05 ET | NFL final list already captured; game underway. Team corroboration: [Chargers inactives](https://www.chargers.com/news/texans-inactives-week-9-2026) confirms LAC. Houston final team page not located; NFL source used for HOU. | [NWS Hawthorne](https://forecast.weather.gov/MapClick.php?CityName=Inglewood&lat=33.9345&lon=-118.332&site=LOX&state=CA): clear, 87°F, calm N wind; observation 12:53 PM PST. SoFi fixed roof ([venue guide](https://www.sofistadium.com/plan-your-visit/a-z-guide)). |
| LV-SF, 4:25 ET | NFL final list captured; game underway. [Raiders final report](https://www.raiders.com/news/las-vegas-raiders-week-9-inactives-vs-san-francisco-49ers); no 49ers final team report located ([49ers weekly injury page](https://www.49ers.com/team/injury-report/week/div-2)). | [NWS San Jose](https://forecast.weather.gov/MapClick.php?lat=37.35&lon=-121.96): mostly cloudy, 71°F, N 3 mph; observation 12:53 PM PST; forecast high 74°F, NNW 6 mph. Levi’s open air ([venue page](https://levisstadium.com/seats/)). |
| GB-NE, 4:25 ET | NFL final list captured; game underway. [Patriots official game-day report](https://www.patriots.com/news/week-9-inactives-packers-at-patriots-x4933) lists both teams. | [NWS Norwood](https://forecast.weather.gov/MapClick.php?lat=42.065870000000075&lon=-71.24838999999997): fair, 55°F, W 9 gusting 21 mph; observation 3:53 PM EST near kickoff. Gillette open air ([venue info](https://www.patriots.com/news/p-g-extends-naming-rights-for-gillette-stadium-through-the-2031-season)). |
| ARI-SEA, 4:25 ET | NFL final list captured; game underway. [Seahawks official game-day report](https://www.seahawks.com/news/seahawks-vs-cardinals-week-9-inactives) lists both teams. | [NWS Boeing Field](https://forecast.weather.gov/MapClick.php?lat=47.6015014648438&lon=-122.334297180176): clear, 59°F, S 13 mph; observation 1:30 PM PST; forecast partly sunny, high near 56°F, SSW 8–11 mph. Lumen open-air playing field with partial canopy ([Seahawks FAQ](https://www.seahawks.com/game-day/frequently-asked-questions/mobile-view)). |
| TB-CHI, 8:20 ET | **Pending; not due yet.** NFL page checked at 18:31 ET still has no SNF player list. Expected 90-minute release is ~18:50 ET, about 19 minutes after retrieval. Team pages checked: [Buccaneers injury report](https://www.buccaneers.com/team/injury-report/) and [Bears injury report](https://www.chicagobears.com/team/injury-report/index-mobile); both show weekly designations, not final inactives. | [NWS Chicago hourly forecast](https://beta.weather.gov/forecast/point/41.85/-87.65/7-day/): at 8 PM CST (near 7:20 PM CST kickoff), clear, ~51°F, NW 9 mph, 0% precipitation. Latest displayed Midway observation is earlier at 2:53 PM CST: 60°F, W 16 gusting 26 mph. Soldier Field open air ([official venue info](https://www.soldierfield.com/stadium-info)). |
| BUF-MIN, Monday 8:15 ET | **Pending; Monday game-day list not yet due.** Sunday inactive report is not the final Monday report. Weekly pages: [Bills](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings-week-9), [Vikings](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season). | [NWS Minneapolis](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=1&lat=44.9486&lg=english&lon=-93.2451&unit=0): Monday cloudy early, then clearing; high near 60°F, S 5–10 mph becoming W. Forecast issue 4:31 PM CST Nov 8. U.S. Bank fixed roof ([Vikings stadium guide](https://www.vikings.com/stadium/a-to-z)). |

Retrieval times:
- NFL consolidated page and TB/CHI team availability pages: 2026-11-08T18:31:27-05:00.
- Chicago and Minneapolis NWS pages: 2026-11-08T18:31:27-05:00. Chicago NWS latest station observation remains 2:53 PM CST; the 8 PM hourly forecast is the kickoff-near value.
- Soldier Field and U.S. Bank venue/roof pages: 2026-11-08T18:31:27-05:00.
- Earlier four games' inactive lists, team corroboration and venue checks remain from the 17:51 ET capture; the NFL page was rechecked at 18:31 ET and their posted lists remain recorded.

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

Validator: `research/validate_week9_readiness.py`, rerun at 18:32 ET.

```text
PASS: 15 phase IDs, frozen artifact hashes, 471 x 100000 simulations, 157 lines, and 139 exact-threshold rows verified.
FAIL-CLOSED: production readiness and calibration remain false; outcomes are pending; CIN-ATL 09:30 is uncovered.
```

Audit integrity passed. The model remains research-only: `projection_ready=false`, `full_integration_acceptance=false`, and calibration is pending. The Sunday-night inactives are due around 18:50 ET; Monday inactives remain pending. No frozen inputs or forecast artifacts were changed.
