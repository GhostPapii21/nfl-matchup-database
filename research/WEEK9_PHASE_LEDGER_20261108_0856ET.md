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
