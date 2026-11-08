# NFL Week 9 Sunday phase ledger

**Snapshot:** Sunday, 2026-11-08 08:56 ET / 13:56 UTC  
**Scope:** all 13 Sunday games, Week 9. This is an evidence ledger, not a green-light.  
**Readiness:** `RESEARCH_ONLY`; `projection_ready=false`; `full_integration_acceptance=false`.  
**Important:** phase labels below are a day-of-slate operational map for NFL-56. They do not replace NFL-9's canonical 60-check ledger.

## 15-phase status

| Phase | Input / gate | Status at snapshot | Evidence and limitation |
|---:|---|---|---|
| 1 | Slate, kickoff, venue | COMPLETE for schedule | NFL.com Week 9 schedule; 13 Sunday games listed below. |
| 2 | Player identity, team, position | PARTIAL | Player names/positions are present in the tracked prop board; unresolved joins and team changes remain possible. |
| 3 | Verified player game histories | PARTIAL | Week 1–8 player-game history is used in the saved simulation. It does not reliably distinguish inactive/no-opportunity games from healthy zero-opportunity games. |
| 4 | Role, snaps, routes, opportunity | PARTIAL | Historical market opportunity and role board exist. Full route participation, snap limits, and inactive-aware opportunity are not complete for every player. |
| 5 | Team offense/defense baselines | PARTIAL | Existing team/defense snapshots support a first-pass rate forecast; source coverage and freshness are not uniform. |
| 6 | Opponent context and game script | PARTIAL | Opponent factors are capped exploratory adjustments; not independently validated. Game-script uncertainty is not fully simulated. |
| 7 | Coverage structure and MOFO/MOFC | BLOCKED / QUALITATIVE | No complete, current, source-verified team coverage chart for every matchup. Do not treat inferred shell as measured coverage. |
| 8 | CB/S/LB responsibilities and explosive allowance | BLOCKED / QUALITATIVE | Named assignment and defender-level coverage exposure are unavailable for the full slate; no fabricated defender attribution. |
| 9 | QB pressure, blitz, scramble response | PARTIAL / NOT IN CURRENT SIM | Historical summaries exist, but pressure timing and fully sourced splits are not integrated into these slate simulations. |
| 10 | Offensive line, pass rush, coaching/game plan | PARTIAL | Injury/context notes exist, but no complete verified matchup-adjustment layer for all games. |
| 11 | Injury report and depth-chart state | PARTIAL | NFL.com Week 9 injury report checked at snapshot. Questionable/doubtful designations are not equivalent to final active status. |
| 12 | Weather, roof, travel | PARTIAL | Day-level forecast checked for each venue. Kickoff-hour stadium wind/precipitation and roof status still require a final check; indoor/roof status is noted below. |
| 13 | Sportsbook prices with provenance | PARTIAL | DK/FD refresh file captured 08:23 ET with source and quote timestamps for 79 player/market rows. Coverage is not full-slate; no 9:30 game quote is in that file. |
| 14 | Projection and simulation | PARTIAL / RESEARCH ONLY | Existing export: 471 rows = 157 book-market lines × 3 models, each 100,000 bootstrap draws. These are raw empirical frequencies, not calibrated probabilities. The export does not cover Bengals–Falcons. Refreshed line overlay includes rows whose current threshold differs from the saved simulation threshold. |
| 15 | Final inactives and pregame freeze | PARTIAL / WAITING | Bengals–Falcons official inactive lists are published. Later games' official inactives are not yet due at 08:56 ET; start checking the 1 p.m. window around 11:30 ET and subsequent games 90 minutes before kickoff. No whole-slate final freeze yet. |

## Sunday games and final-inactive/weather state

| Kickoff ET | Game | Inactives at 08:56 ET | Venue/weather snapshot |
|---|---|---|---|
| 9:30 AM | Bengals at Falcons | **Posted.** CIN: S Kyle Dugger, C Connor Lew, OT Myles Hinton, DT Landon Robinson. ATL: QB Andy Dalton (emergency third QB), QB Jack Strand, WR Zachariah Branch, DB Billy Bowman, DB Robert Longerbeam, DE Drake Jackson. | Santiago Bernabéu, Madrid. Cloudy, daily high about 62°F; retractable roof status not verified in this snapshot. |
| 1:00 PM | Broncos at Panthers | **Not yet posted.** NFL injury report: DEN WR Pat Bryant and S Talanoa Hufanga questionable; CAR OL Corey Bullock, Brady Christensen, Torricelli Simpkins questionable; multiple players already ruled out. | Charlotte: sunny, high about 68°F; outdoor. |
| 1:00 PM | Cowboys at Colts | **Not yet posted.** DAL WR George Pickens and TE Jake Ferguson questionable; KaVontae Turpin already out. IND listed Akeem Davis-Gaither, Justin Walley, A.J. Haulcy out. | Indianapolis: Lucas Oil Stadium; indoor/retractable roof, final roof state not checked. |
| 1:00 PM | Jets at Chiefs | **Not yet posted.** NYJ WR Garrett Wilson out. KC CB Mansoor Delane out; WR Nikko Remigio questionable. | Kansas City: sunny, high about 66°F; outdoor. |
| 1:00 PM | Lions at Dolphins | **Not yet posted.** DET WR Amon-Ra St. Brown questionable; C Cade Mays, EDGE D.J. Wonnum, LB Jack Campbell, CB D.J. Reed, S Kerby Joseph out. MIA RB Kaytron Allen and Jaylen Wright questionable. | Miami Gardens: partly sunny with passing-shower risk; high about 87°F; outdoor. |
| 1:00 PM | Browns at Saints | **Not yet posted.** CLE QB Deshaun Watson questionable. NO WR Jordyn Tyson, OTs Kelvin Banks Jr. and Asim Richards, CB Martin Emerson questionable; RB CJ Donaldson out. | New Orleans: Caesars Superdome; indoor. |
| 1:00 PM | Giants at Eagles | **Not yet posted.** NYG RB Cam Skattebo doubtful; WR Charlie Jones questionable. PHI WR DeVonta Smith and Dontayvion Wicks out. | Philadelphia: breezy, high about 60°F; outdoor. |
| 1:00 PM | Rams at Commanders | **Not yet posted.** LAR WR Jordan Whittington and TE Colby Parkinson questionable; TE Terrance Ferguson out. WSH WR Dyami Brown and Treylon Burks out. | Landover: sunny with steady breeze; high about 62°F; outdoor. |
| 4:05 PM | Texans at Chargers | **Not yet posted.** HOU RB David Montgomery and S Reed Blankenship out. LAC WR Brenen Thompson, TE David Njoku, G Kayode Awosika, LB Denzel Perryman questionable. | Inglewood: SoFi Stadium; fixed roof. |
| 4:25 PM | Raiders at 49ers | **Not yet posted.** SF WR Mike Evans, Christian Kirk, Deebo Samuel out. LV CB Darien Porter questionable; SF DBs Upton Stout, Nate Hobbs, Siran Neal questionable. | Santa Clara: low clouds then sun, high about 72°F; outdoor. |
| 4:25 PM | Packers at Patriots | **Not yet posted.** GB RB Chris Brooks and MarShawn Lloyd questionable. NE WR A.J. Brown out; WR Mack Hollins and TE Hunter Henry questionable. | Foxborough: breezy at times, high about 58°F; outdoor. |
| 4:25 PM | Cardinals at Seahawks | **Not yet posted.** ARI RB Bam Knight out; OL Isaiah Adams, DL Walter Nolen, CB Max Melton questionable. SEA QB Sam Darnold, WR Rashid Shaheed, OT Charles Cross, G Quenton Nelson and several defenders out. | Seattle: showers and breezy conditions; high about 58°F; outdoor. Recheck near kickoff. |
| 8:20 PM | Buccaneers at Bears | **Not yet posted.** TB WR Emeka Egbuka questionable; EDGE YaYa Diaby out. CHI RB Kyle Monangai and DBs Malik Muhammad, Tyrique Stevenson questionable. | Chicago: breezy, dry, high about 60°F; outdoor. |

## Prospective evaluation / calibration status

- The existing saved 100,000-draw distributions and this morning's quotes are being frozen as pregame research inputs where their timestamps precede kickoff.
- Existing Week 5–8 results are retrospective development data, not a clean untouched calibration set. Historical exact prop lines are not present in the available research package, so those results cannot establish market-line Brier score/log loss.
- Week 9 outcomes are not yet known at this snapshot. The prospective score is therefore **PENDING OUTCOMES**; calibration has not been demonstrated.
- Any row without an exact saved threshold/probability match is unscorable for exact-line probability until the distribution is rerun from the frozen input and its provenance is retained.
- Exclude Bengals–Falcons from exact-prop evaluation unless its pregame player projections and exact time-stamped lines are frozen before kickoff. The current saved simulation file has no 9:30 AM rows.

## Sources and retrieval

- Schedule and published injury report: [NFL.com Week 9 injury report](https://www.nfl.com/news/nfl-week-9-injury-report-2026-season), retrieved 2026-11-08 08:56 ET.
- Bengals–Falcons inactive list: [NFL.com Week 9 inactives](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season), retrieved 2026-11-08 08:56 ET; cross-check [Atlanta Falcons official report](https://www.atlantafalcons.com/news/atlanta-falcons-week-9-inactives-cincinnati-bengals), published 08:01 ET.
- Weather: venue-city daily forecasts retrieved 2026-11-08 08:56 ET. These are daily forecasts, not stadium-hour observations; no stadium-specific wind/precipitation API payload is archived here.
- Current price snapshot: `research/WEEK9_DAY1_DK_FD_REFRESH_20261108_0823ET.csv`; captured 08:23 ET; each book quote's source and received time are recorded per row.
- Saved projection/simulation: `research/WEEK9_DAY1_MODEL_SIMULATION_20261108.csv` and `research/WEEK9_DAY1_REFRESHED_PROJECTION_OVERLAY_20261108_0823ET.csv`.

## Checklist decision

- [x] Record current slate, latest published injury report, available Bengals–Falcons inactives, day-level weather, and timestamped odds/projection artifacts.
- [x] Preserve the existing projection files in the repository (confirmed present).
- [ ] Capture final official inactives for every remaining game before each kickoff.
- [ ] Refresh kickoff-near weather/roof state and update projections only from verified inputs.
- [ ] Score the frozen Week 9 forecasts after verified final stats are available; report eligible coverage, Brier/log loss and calibration by market with uncertainty.
- [ ] Pass the full source-to-output reproducibility and production acceptance gate. This ledger alone does not make the model ready.


---

# Game-day refresh — 2026-11-08 11:33 ET

**Refresh capture:** 2026-11-08T11:33:27-05:00 / 16:33:27 UTC  
**Purpose:** update official inactives, NWS venue-area forecasts and stadium roof state for every remaining Week 9 game. This addendum supersedes the 08:56 operational status below; the original locked 08:56 files and forecast artifacts are preserved unchanged.

## Readiness and lock

- Production: `RESEARCH_ONLY`; `projection_ready=false`; `full_integration_acceptance=false`.
- Calibration: `PROSPECTIVE_LOCKED_OUTCOMES_PENDING`; no new accuracy claim.
- The 08:56 prospective lock remains unchanged. Simulation CSV, DK/FD line snapshot, overlay, original lock, and original 08:56 ledger/snapshot were not modified. No weather or inactive observation was applied to the forecast.
- Baseline readiness validator result: **PASS** — 15 ordered phase IDs, locked artifact SHA-256 values, 471 rows × 100,000 draws, 157 market lines, and 139 exact-threshold overlay rows verified.
- Fail-closed result: **PASS** — readiness and calibration remain false; outcomes pending; CIN–ATL 9:30 a.m. remains outside the frozen simulation.
- New snapshot structure check: **PASS** — 15 ordered phases, all 13 remaining games represented, and source URL/retrieval timestamps present. Missing official lists and future near-kickoff weather refreshes remain pending.

## Updated phases

| Phase | 11:33 ET status | Evidence / remaining blocker |
|---:|---|---|
| 11 Injury/depth chart | PARTIAL — FINAL INACTIVES PENDING | NFL.com’s official Week 9 inactives article was rechecked at 2026-11-08T11:33:27-05:00; it still displayed only CIN–ATL. The 1 p.m. lists were not present at the 11:33 check. Later Sunday lists and Monday BUF–MIN are not yet due. Weekly injury designations are not final inactive lists. |
| 12 Weather/roof/travel | PARTIAL — REFRESHED | NWS forecasts and official stadium sources were checked during 2026-11-08 11:30–11:33 ET. Lucas Oil Stadium’s official Colts gameday page reports roof OPEN and window OPEN. Fixed-roof indoor venues are identified below. Several late-game NWS pages were issued hours before kickoff; run another near-kickoff check. |
| 15 Final inactives/pregame freeze | PARTIAL — WAITING | No remaining game-day inactive list has been verified in the official NFL listing. No full-slate freeze. |

All other phase statuses remain as recorded in the 08:56 ledger. The 13-game locked simulation coverage is not extended to Monday BUF–MIN.

## Remaining games: inactives, weather, roof

Inactive source for each row: [NFL.com Week 9 inactives](<https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season>), checked 2026-11-08T11:33:27-05:00. For team-specific final reports, no separate official team list was verified in this pass; the blocker is left pending. Weather source retrieval was during 2026-11-08 11:30–11:33 ET; source issuance times are shown separately.

| Kickoff ET | Game / venue | Official inactives | NWS forecast near venue | Roof / exposure |
|---|---|---|---|---|
| 13:00 | DEN at CAR, Bank of America Stadium | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Sunny; NWS daily high near 66°F, west-southwest wind 5–7 mph afternoon. [NWS](https://forecast.weather.gov/MapClick.php?CityName=Charlotte&lat=35.1975&lon=-80.8345&site=GSP&state=NC); forecast issued 2026-11-08 06:43 ET | **OUTDOOR_NO_ROOF** |
| 13:00 | DAL at IND, Lucas Oil Stadium | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Sunny; NWS Indianapolis forecast high near 60°F and light winds. Roof and window confirmed open by Colts game-day page. [NWS](https://forecast.weather.gov/MapClick.php?CityName=Indianapolis&lat=39.7764&lon=-86.1462&site=IND&state=IN); forecast issued 2026-11-08 08:45 ET | **OPEN; window OPEN** ([official venue](https://www.colts.com/game-day/regular-season-game-4)) |
| 13:00 | NYJ at KC, Arrowhead Stadium | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Sunny; NWS daily high near 65°F, northwest wind around 6 mph. [NWS](https://forecast.weather.gov/MapClick.php?CityName=Kansas+City&lat=39.0904&lon=-94.5837&site=EAX&state=MO); forecast issued 2026-11-08 06:31 CST | **OUTDOOR_NO_ROOF** |
| 13:00 | DET at MIA, Hard Rock Stadium | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | NWS hourly point forecast near kickoff: about 82°F, north wind near 6 mph, 3% precipitation potential; mostly sunny. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=digital&lat=25.98&lon=-80.2&unit=0); forecast issued 2026-11-08 02:56 ET | **OUTDOOR_NO_ROOF** |
| 13:00 | CLE at NO, Caesars Superdome | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Outdoor forecast omitted from game conditions because the venue is enclosed. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=digital&lat=30.0585&lg=english&lon=-89.9476); forecast issued 2026-11-08 00:57 CST | **FIXED_INDOOR_DOME** ([official venue](https://www.caesarssuperdome.com/stadium)) |
| 13:00 | NYG at PHI, Lincoln Financial Field | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Partly sunny; NWS high near 61°F with light-to-moderate west wind. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=2&lat=39.9489&lg=english&lon=-75.15&unit=0); forecast issued 2026-11-08 04:07 ET | **OUTDOOR_NO_ROOF** |
| 13:00 | LAR at WAS, Northwest Stadium | **PENDING_OFFICIAL_LIST** — 1 p.m. release window reached; NFL consolidated article still had no team lists at 11:33 ET; no verified team final list located. | Sunny; NWS high near 63°F, west wind 7–10 mph with gusts up to 22 mph. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=digital&FcstType=text&lat=38.9308&lg=english&lon=-76.9074&menu=1); forecast issued 2026-11-08 09:00 ET | **OUTDOOR_NO_ROOF** |
| 16:05 | HOU at LAC, SoFi Stadium | **PENDING_NOT_YET_POSTED** — Final inactive window is later; NFL page had no game list at 11:33 ET. | Outdoor weather excluded from game conditions because fixed roof and climate-controlled environment. [NWS](https://beta.weather.gov/forecast/point/33.962/-118.353/7-day/); forecast issued 2026-11-08 morning local; forecast page | **FIXED_ROOF_CLIMATE_CONTROLLED** ([official venue](https://www.sofistadium.com/plan-your-visit/a-z-guide)) |
| 16:25 | LV at SF, Levi's Stadium | **PENDING_NOT_YET_POSTED** — Final inactive window is later; NFL page had no game list at 11:33 ET. | NWS day forecast: patchy fog before 9 a.m. local, then partly sunny, high near 74°F, afternoon north-northwest wind around 6 mph. Forecast was issued early; refresh closer to kickoff. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=2&lat=37.3524&lg=english&lon=-121.9531&unit=0); forecast issued 2026-11-08 00:26 PST | **OUTDOOR_NO_ROOF** |
| 16:25 | GB at NE, Gillette Stadium | **PENDING_NOT_YET_POSTED** — Final inactive window is later; NFL page had no game list at 11:33 ET. | NWS day forecast: partly sunny becoming sunny, high near 58°F; west wind 7–11 mph with gust potential to 25 mph in the day. Refresh closer to kickoff. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&lat=42.0812&lg=english&lon=-71.2434); forecast issued 2026-11-08 01:32 ET | **OUTDOOR_NO_ROOF** |
| 16:25 | ARI at SEA, Lumen Field | **PENDING_NOT_YET_POSTED** — Final inactive window is later; NFL page had no game list at 11:33 ET. | NWS forecast: mostly cloudy; slight shower chance early afternoon local; south wind 15–25 mph easing to 10–15 mph; mid-to-upper 50s. Refresh closer to kickoff. [NWS](https://forecast.weather.gov/MapClick.php?FcstType=text&TextType=1&zoneid=WAZ315); forecast issued 2026-11-08 01:36 PST | **OUTDOOR_NO_ROOF** |
| 20:20 | TB at CHI, Soldier Field | **PENDING_NOT_YET_POSTED** — Final inactive window is later; NFL page had no game list at 11:33 ET. | NWS day forecast: sunny, high near 59°F; west/southwest wind 10–15 mph with gusts up to 30 mph. Exact evening-hour conditions need a later refresh. [NWS](https://forecast.weather.gov/MapClick.php?lat=41.848845&lon=-87.67125); forecast issued 2026-11-08 02:21 CST | **OUTDOOR_NO_ROOF** |
| 20:15 Monday | BUF at MIN, U.S. Bank Stadium | **PENDING_NOT_YET_DUE** — Monday inactive release window is not yet due; no official final lists expected until 90 minutes before kickoff. | NWS Monday forecast Minneapolis: cloud cover early then gradual clearing, high near 58°F, south wind 5–10 mph becoming west. Outdoor conditions not applied under fixed roof. [NWS](https://forecast.weather.gov/MapClick.php?lat=44.9657&lon=-93.2385); forecast issued 2026-11-08 05:43 CST | **FIXED_ROOF_CLIMATE_CONTROLLED** ([official venue](https://www.usbankstadium.com/plan-your-visit/a-z-guide)) |

### Official source checks

- [NFL Week 9 inactives](<https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season>) — page published 08:05 ET; checked at 2026-11-08T11:33:27-05:00; still only CIN–ATL lists.
- [NFL Week 9 injury report](<https://www.nfl.com/news/nfl-week-9-injury-report-2026-season>) — checked during 2026-11-08 11:30–11:33 ET; used only as weekly status context, not as final inactive evidence.
- [NFL Week 9 schedule](<https://www.nfl.com/news/nfl-how-to-watch-week-9-nfl-games-schedule-madrid-game-details-and-more>) — checked during 2026-11-08 11:30–11:33 ET; confirms Sunday games and Monday BUF–MIN.
- [Colts Cowboys gameday page](https://www.colts.com/game-day/regular-season-game-4) — checked 11:30 ET; roof OPEN, window OPEN.
- [SoFi Stadium A–Z guide](https://www.sofistadium.com/plan-your-visit/a-z-guide) — fixed roof and climate-controlled.
- [U.S. Bank Stadium A–Z guide](https://www.usbankstadium.com/plan-your-visit/a-z-guide) — fixed roof and climate-controlled.
- [Caesars Superdome venue](https://www.caesarssuperdome.com/stadium) — enclosed indoor stadium.

### What remains pending

1. Final inactives for every remaining game. The 1 p.m. release window has passed but the NFL page had not populated those lists at capture; team-specific official reports were not verified. Check again immediately.
2. Later Sunday inactive lists at their 90-minute pre-kickoff windows and BUF–MIN near Monday kickoff.
3. Updated NWS hourly forecast and field exposure close to the 4:05, 4:25, 8:20 p.m. and Monday kickoffs; several cited forecast pages are earlier-issued day forecasts.
4. A deliberate, separately versioned forecast rerun if verified information warrants it. Do not overwrite or grade against the 08:56 lock.
5. Week 9 outcome scoring, multi-slate untouched calibration evidence, and full production acceptance. No promotion until those gates pass.

## Current readiness snapshot

See `research/WEEK9_READINESS_SNAPSHOT_20261108_1133ET.json`. It preserves every readiness gate as false and points to the unchanged 08:56 lock.