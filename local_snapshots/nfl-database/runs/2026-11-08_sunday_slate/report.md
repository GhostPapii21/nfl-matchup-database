# Projection report — 2026 Week 9 Sunday slate — BLOCKED (no picks)
**Slate:** NFL 2026 Week 9 Sunday games (CIN@ATL through TB@CHI). TNF JAX@BAL is final. MNF BUF@MIN is Monday and is listed only for context.
**Kickoffs (America/New_York):** CIN@ATL 9:30 AM ET (Madrid, Santiago Bernabéu, ESPN indoor=True); 1:00 PM ET DAL@IND, NYJ@KC, DET@MIA, CLE@NO, NYG@PHI, LAR@WSH, DEN@CAR; 4:05 PM ET HOU@LAC; 4:25 PM ET GB@NE, LV@SF, ARI@SEA; 8:20 PM ET TB@CHI.
**Data pulled:** 2026-11-08 07:10–07:15 America/New_York
**Checklist:** `/workspace/nfl-database/runs/2026-11-08_sunday_slate/checklist.md`
**Manifest:** `/workspace/nfl-database/runs/2026-11-08_sunday_slate/source_manifest.json` (sha256 `7dac4e58562ab4adb6ade63f7bc1f1289b904a6c0a3fc5f6d21411489cc581c6`)

## Status banner
This is a truthful blocked game-day preflight, not a projection card. **No picks. No slips. SIMULATION NOT RUN.** `projection_ready=false`. NFL-49 final acceptance and Ghost vet are still prerequisites. The 100k Monte Carlo / Bias / Game Randomness triad and the executable 15-phase workflow remain incomplete (NFL-56). Historical `sim_v6` was not executed and no calibration is claimed.

## Phases run
| Phase | Result |
|---|---|
| 1 Data | PASS partial (ESPN scoreboard week 9, 15 events including completed TNF and upcoming MNF) |
| 2 Opportunity | MISSING (no priced leg) |
| 3 Defense profile | MISSING |
| 4 Defender coverage | MISSING (man/zone and MOF not pulled; NFL-47) |
| 5 Pressure/blitz | MISSING |
| 6 QB grade | MISSING |
| 7 Roles/RB | N/A (no priced RB leg) |
| 8 Injuries | PASS as research designations from ESPN (conflicts noted; Phase 15 still NOT_YET) |
| 9 NGS | MISSING |
| 10 Film | MISSING |
| 11 Environment | PASS forecast pulled (SRC-1); several GUST20 flags |
| 12 Source audit | PASS with listed gaps |
| 13 Script gate | MISSING (actionable spreads/totals NOLINE) |
| 14 Models/price | FAIL blocked; SIMULATION NOT RUN; no seed or trial count |
| 15 Inactives | NOT_YET |

## Sources used, by category
1. **Core stats and play-by-play:** No new nflverse PBP pull this morning. Saturday local refresh (`week9/model/REFRESH_2026-11-07_1001.md`, local commit `12df5aa`) remains the last results-feed stamp. ESPN public scoreboard used for today's kickoffs, venues, and game state (CIN@ATL still Scheduled at 07:12 ET).
2. **Coverage schemes and matchups:** **MISSING.** Checkpoint `docs/SOURCE_STATUS.md` at `fe2e371` lists FTN charting/NGS coverage effects disabled (NFL-47). Sharp/StatRankings/PFF were not pulled. Nothing invented.
3. **Next Gen Stats:** **MISSING.** Public NGS pages were not opened this run.
4. **Film:** **MISSING.** No highlight or gamebook URLs cited.
5. **Injuries and news:** ESPN injuries API, feed timestamp 2026-11-08T12:12:19Z, pulled 07:12 AM ET. Full body sha256 `6d0a3c335555e9cc85116fa3ec9de852e8cf31038a7fb69332a125f97e66b21e` (hashed only). Extract at `raw/espn_injuries_extract.json`. Compared with Saturday 10:01 ET refresh:
   - Unchanged research tags: Drew Lock Active; Sam Darnold OUT; Christian McCaffrey Active; Saquon Barkley Active; Alvin Kamara Active; Malik Nabers Active; Cam Skattebo Doubtful; A.J. Brown (NE) OUT; Garrett Wilson OUT; Cade Mays OUT; Kyler Murray (MIN) OUT for MNF; George Pickens Questionable; Amon-Ra St. Brown Questionable (Pelissero note in feed says slated to play — still official Q); Deshaun Watson Questionable; Kaytron Allen Questionable.
   - Saturday OUT/IR updates confirmed: Deebo Samuel Sr. OUT; Christian Kirk placed on IR Saturday; Dyami Brown IR Saturday.
   - ESPN also lists, as of this pull: DeVonta Smith OUT (hamstring) vs NYG; Micah Parsons OUT (knee) at NE; Charles Cross OUT (ankle) vs ARI; TreVeyon Henderson OUT (illness) vs GB; Jaelan Phillips and Bobby Okereke OUT vs DEN; D.J. Reed and Kerby Joseph OUT vs MIA.
   - Feed-quality flag: Justin Jefferson appears as Active on both Minnesota and Cleveland in the same ESPN injuries payload. That conflict is logged, not resolved, and is not used as a roster fact.
6. **Weather:** NWS (`api.weather.gov`) and Open-Meteo only, via `tools/weather_forecast.py --week 9`, wrote `week9/weather_forecast/forecast_2026-11-08_0711.json` (sha256 `7b96dd6af6d5a2e25b4d2aeeac03bcfecc95761cae4a2f6f6c6e65684e5b427a`). Flags: NYG@PHI gusts 20.4; LAR@WSH gusts 21.7; TB@CHI gusts 27.3; DAL@IND runner flag gusts 26.8 on a retractable/indoor venue (do not treat as an automatic outdoor weather cut). ARI@SEA gusts 19.9 (near flag). CIN@ATL NWS missing, Open-Meteo 5% precip / 14.1 gusts.
7. **Odds and props:** FanDuel price of record was **not** re-pulled (Odds API last used Saturday 10:01 ET, 2 credits, 2,309 remaining). Actionable multi-book quotes stay **NOLINE** (NFL-45, NFL-25). ESPN scoreboard displayed DraftKings numbers at 07:12 ET for movement context only. Versus Saturday FanDuel refresh: no 1.5-point moves. Notable half-point / one-point display differences: NYJ@KC total 48.5 (Sat FD 47.5); CHI -6 (Sat FD -6.5); HOU -6 (Sat FD -5.5); BUF MNF total 43.5 (Sat FD 44.5). These are not priced edges.
8. **Simulation models:** **SIMULATION NOT RUN.**

## Simulations
Monte Carlo, Bias, and Game Randomness each ran **0** trials. No seed. No script path. No model probability or median exists for any leg. Raw vs anchored: not computed. A 40-percentage-point consensus anomaly check was not applicable because no model probabilities were produced.

Independent note: GitHub `main` at `6e1b932` (06:53 AM ET) updates `research/WEEK9_DAY1_DK_FD_PRICE_TRACKER_20261108.csv` and labels those ranges **uncalibrated**. That tracker is not this run, not a vetted card, and not adopted as the model.

## Projections and picks
**None.** Zero qualifying legs. Passing-yards markets remain off slips under the standing rule, and no other market was priced.

Cut reason for the whole slate: engine/acceptance gates (NFL-49, NFL-56, unmerged PR 1, `projection_ready=false`) plus missing required source-map fields (coverage/man-zone/MOF, NGS, film, actionable quotes, Phase 15).

## Risks and checks still to come
- Phase 15 inactives: Madrid ~8:00 AM ET; 1 PM window ~11:30 AM ET; late windows 2:35 PM and 6:50 PM ET.
- Questionable players (Pickens, St. Brown, Watson, Kaytron Allen, others) need dual-share treatment if still unconfirmed at inactives.
- Roof-status conflicts: DAL@IND (runner open-air vs ESPN indoor) and HOU@LAC (runner indoor vs ESPN SoFi indoor=False).
- TB@CHI, NYG@PHI, and LAR@WSH carry live GUST20 review flags if a later accepted engine ever prices those games.
- Do not treat the main-branch DK/FD tracker CSV as live edges.

Local GitHub write was not pushed: this working tree has no git remote, and `main` was independently updated this morning. Public-safe artifacts live in this run folder; restricted ESPN injuries body is hashed only.
