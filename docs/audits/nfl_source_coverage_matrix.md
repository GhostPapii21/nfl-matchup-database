# NFL source-availability and data-quality matrix (12 analytical components)

Independent audit, 2026-11-27 (about 8:30 PM to 9:30 PM ET; the box clock read Sat 2026-11-28 01:50 UTC at the last probe).
Repo state audited: `main` at `ef4cc690` (PR #146). Research only: no model weight, gate, `projection_ready`, hook, workflow or `pregame/` change.
Free public endpoints only. No purchase, no subscription, no paid API call, **no Odds API call** (the account has no credits; its docs were read, not called).

> **Rule used throughout.** A column name that looks like the statistic is not evidence of the statistic. Every "verified" below was
> checked by downloading the file and counting non-null values by season, or by reading the field definition, or by a one-off probe
> listed in section 17. Anything not checked is marked **NOT VERIFIED**. Anything with no free source is marked **NOT FOUND (free)**.
> No number in this file is estimated.

## 0. Scope and what this does not repeat

| Open PR | What it owns | How this audit relates |
| --- | --- | --- |
| #140 (draft) | Read rules (flags only): targets first, defense-allowed profile, hourly weather grade (NWS + Open-Meteo forecast) | Referenced only. Section 14 audits the *historical* weather sources it does not cover. |
| #143 (draft) | 2026 defender coverage profiles; inferred attribution (held-out top-1 25%); PFR/pbp/Sharp/StatRankings inputs | Referenced only. Section 6 audits *which free fields exist at all* for assignment; it does not build or re-validate attribution. |
| #144 (draft) | 2026 positional allowances by window, opponent-adjusted, situational splits | Referenced only. Section 11 (third down / red zone) confirms the input sample sizes behind those splits; it adds no allowance table. |
| #149, #151 (open) | Phase 0 inventory; execution-receipt contract that marks missing sources `SOURCE_UNAVAILABLE` | Context. The verdicts here are the evidence for which phase inputs are genuinely unavailable versus not yet wired. |

Verdict scale: **SUPPORTED** (a free source carries the actual statistic at a usable grain), **LIMITED** (carries it, but the season range, grain, sample, point-in-time safety or definition is a problem),
**NOT SUPPORTED** (no free source carries the statistic; only a proxy or a paid source does).

## 1. Summary: component by best free source by verdict

| # | Component | Best free source (verified) | Verdict | One-line reason | Paid alternative (not accessed) |
| --- | --- | --- | --- | --- | --- |
| 1 | Receiver routes and route participation | nflverse `pbp_participation` `route` (target-conditional) plus `offense_players` on-field list, 2016-2025 | **NOT SUPPORTED** | `route` is only the *primary receiver's* route on a play (blank on sacks, scrambles). No file says who ran a route. On-field presence is only an upper bound. No 2026 file. | FTN API `rte`, `skp_role` (route runner flag); PFF |
| 2 | Target depth and route distribution | nflverse `pbp` `air_yards`, `pass_length`, `pass_location` (99.4% to 99.6% of attempts, 2016-2026); route mix of targets from participation | **SUPPORTED** (depth) / **LIMITED** (route distribution) | aDOT and depth splits are solid. "Route distribution" exists only for targeted routes, only 2016-2025, and the label set changed in 2023. | FTN `dot`, `rte`; PFF |
| 3 | Man, zone, single-high, split-safety | 2018-2025: participation `defense_man_zone_type`, `defense_coverage_type`. 2026: Sharp team man/zone and middle-of-field open/closed (season to date) | **LIMITED** | Play-level only through 2025 and the definition shifts (man share 28.8% in 2022, 41.3%, 48.5%, 31.0% in 2025). 2026 is team-level, season-to-date, not point-in-time. No field is named single-high or split-safety. | FTN `shell`, PFF coverage reports |
| 4 | Defender-to-receiver assignments | PFR `advstats_week_def` targeted-defender lines (2018-2026) | **NOT SUPPORTED** | Only when targeted. No snaps-in-coverage, alignment, or who-covers-whom for non-targets. | FTN `def(1-5)`, `cushion`; PFF; NGS NFL Pro (not held) |
| 5 | True pressure and blitz rates | Team/QB: participation `was_pressure` (2018-2025), FTN `n_blitzers`/`n_pass_rushers` (2022-2026 wk 11), PFR pass/def pressure columns (2018-2026) | **LIMITED** | Sources disagree materially on the same plays (2025: 5,906 vs 4,277 pressures). Pressure definition changed in 2023. 2026 has no play-level pressure flag. | FTN `qbp`, `ttp`, pressure defender |
| 6 | QB performance vs pressure and vs coverage | participation x pbp EPA, 2018-2025 | **LIMITED** | Per-QB-season splits are thin (2025: median 112 pressured and 126 man dropbacks among 45 QBs). 2026 has no pressure or coverage split. | FTN, PFF |
| 7 | OL and DL grades | ESPN Analytics win rates (player and team, tracking-based) and Sharp team OL/DL tables | **NOT SUPPORTED** (grades) / **LIMITED** (win rates) | No free per-player grade. Win-rate pages are current-season snapshots with no verified archive. | PFF grades |
| 8 | RB opportunity, carries, targets, rushing concepts | nflverse `stats_player_week`, `pbp`, `snap_counts`; direction and gap from `pbp` | **SUPPORTED** (opportunity, direction, gap) / **NOT SUPPORTED** (zone vs gap concept, RB routes) | `run_gap` is blank on every middle run by construction. No scheme or concept field. | FTN `concept`, `dir`; PFF |
| 9 | Third-down and red-zone tendencies | nflverse `pbp` (down, distance, yardline 100% non-null) plus FTN blitz | **SUPPORTED** | Sample per defense-season is large enough for rates (3rd-down dropbacks median 165). 2026 in-season samples need shrinkage. | none needed |
| 10 | Official injury reports and inactive lists | Injury report: nflverse `injuries` (mirror of the NFL report) and the NFL.com page. Inactives: club "Inactives" articles (repo parser) | **LIMITED** | nflverse has no publication timestamp in 2025-2026 files. NFL.com is one snapshot per week. No free historical inactives list found. | none |
| 11 | Timestamped sportsbook opening and current lines | None free with open-line timestamps. Closing: nflverse `games`. Open/close without time: ESPN core API (one book). Timestamped: self-captured polls only | **NOT SUPPORTED** (timestamped opens) / **LIMITED** (closing and untimed opens) | The only timestamped history is paid (The Odds API historical, paid plans only) or captured by this repo going forward. | The Odds API historical |
| 12 | Weather and historical weather effects | Observed: nflverse `pbp` `weather` text and `games` temp/wind; hourly: Open-Meteo archive (1940 to yesterday) | **SUPPORTED** (observed, kickoff-window) / **LIMITED** (point-in-time forecast history) | Kickoff observations are near-complete once the text is parsed. Forecast-as-issued history is only 2022+ (Open-Meteo) and the repo has none saved before late 2026. | none needed |

## 2. Master source register

"Integrated" means code in this repo reads it today (path given). "Partial" means a prior-season, local-only, hash-only or one-purpose use. Seasons are the verified range, not the claimed range.

| ID | Source and dataset | Class | Verified coverage | Update cadence | Credentials | Integrated |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | nflverse `pbp/play_by_play_{season}.parquet` (372 columns in 2026) | Third party (nflfastR parse of the NFL play feed) | 2016-2026 downloaded; 2026 = weeks 1-12 (four week-12 games) | Nightly after game days plus gameday refreshes (nflreadr schedule page); asset re-stamped 2026-11-27 20:40 ET | None (CC-BY 4.0 base) | **Yes** `pregame/sources.py` `DATASETS["pbp"]`, `pipeline/freshness.py` |
| S2 | nflverse `pbp_participation/pbp_participation_{season}.parquet` | Third party. 2016-2022 NFL NGS; 2023 on FTN (nflreadr `load_participation` doc) | Files 2016-2025 (+ `old_2023`); **2026 file returns HTTP 404** | FTN years "provided after all post-season games are completed" (doc). 2025 file stamped 2026-02-10 | None (CC-BY-SA 4.0, attribute FTN / NGS) | **Partial** `dashboard/extras.py` (downloads the prior-season file for the board's man/zone and pressure view); `pipeline/matchup_sources.py` `participation_routes()` returns MISSING; copy is not in the repo (`data/licensed/README.md`) |
| S3 | nflverse `ftn_charting/ftn_charting_{season}.parquet` | Third party (FTN manual charting, subset) | 2022-2026; 2026 = weeks 1-11 | Charted within 48 h of each game (doc). Asset stamped 2026-11-25 19:02 ET | None (CC-BY-SA 4.0, attribute FTN) | **Yes** `pregame/sources.py` `"ftn"`, `pipeline/freshness.py`; file is hash-only in the repo (`SOURCES.md`) |
| S4 | nflverse `nextgen_stats/ngs_{passing,receiving,rushing}.parquet` | Official (NFL Next Gen Stats), mirrored by nflverse | 2016-2026, REG and POST, week 0 = season row; max week 12 | Nightly 3-5 AM ET (nflreadr schedule page); stamped 2026-11-27 16:54 ET | None | **Yes** `pregame/sources.py`, `data/ngs/` |
| S5 | nflverse `pfr_advstats/advstats_week_{pass,rec,rush,def}_{season}.parquet` | Third party (Pro Football Reference) | 2018-2026; 2026 = weeks 1-11 | 0, 6, 12, 18 UTC (doc); stamped 2026-11-27 19:02 ET | None | **Partial** `def`, `rec`, `rush` in `pregame/sources.py`; `pass` only in `dashboard/extras.py` |
| S6 | nflverse `snap_counts/snap_counts_{season}.parquet` | Third party (PFR) | Docs: 2012+. Verified 2024-2026 only; 2026 = weeks 1-12 | 0, 6, 12, 18 UTC (doc); stamped 2026-11-27 07:01 ET | None | **Yes** `pregame/sources.py`, `pipeline/freshness.py` |
| S7 | nflverse `injuries/injuries_{season}.parquet` | Mirror of the NFL official injury report ("collected from an API", nflreadr doc) | Docs: 2009+. Verified 2016-2026; 2026 = weeks 1-12 | Daily 07:00 UTC (doc); stamped 2026-11-27 12:24 ET | None | **Yes** `pregame/sources.py` `"injuries"`; freshness row `official_injuries` |
| S8 | nflverse `weekly_rosters/roster_weekly_{season}.parquet`, `depth_charts` | Third party | 2026 weeks 1-12 (roster `status` has `INA`) | Rosters 07:00 UTC; depth charts 07:00 UTC (docs) | None | **Yes** `pregame/sources.py` |
| S9 | nflverse `schedules/games.parquet` (closing lines, roof, temp, wind) | Third party (nfldata lineage per `data/lines/README.md`) | 2016-2026 verified (1999+ present) | About every 5 minutes in season (doc) | None | **Yes** `pregame/sources.py` `"games"` |
| S10 | nflverse `stats_player/stats_player_week_{season}.parquet` | Third party (derived from pbp) | 2025 verified (columns) | Nightly with pbp | None | **Yes** `data/historical/nflverse/stats_player_week_*.parquet` |
| S11 | ESPN site API: `scoreboard`, `summary`, `injuries` (`site.api.espn.com/apis/site/v2/sports/football/nfl/`) | Third party (ESPN, unofficial, undocumented) | Live and recent games | Live | None | **Yes** `pregame/sources.py` `espn_injuries()`, `pipeline/kickoffs.py`, `grading/espn.py` |
| S12 | ESPN core API odds (`sports.core.api.espn.com/v2/.../events/{id}/competitions/{id}/odds`) | Third party (ESPN, unofficial) | See section 13 | Live | None | **No** (only a one-off live poller in `runs/2026-11-27_DEN@PIT/pbp/poll_live.py`) |
| S13 | NFL.com official injury report page `nfl.com/injuries/league/{season}/reg{week}` | **Official** (NFL) | Week selector lists 2000-2026; Week 12 2026 fetched | Per report posting | None | **No** (only the nflverse mirror S7) |
| S14 | Club "Inactives" articles (NFL Clubs sites) | **Official** (clubs) | 2026 in-season only | About 90 min before kickoff | None | **Yes** `phase15/official_inactives.py` (fail-closed) |
| S15 | NFL official Game Summary PDFs | **Official** (NFL; media-use restriction) | 2026 Week 9 only, owner supplied | Postgame | Owner supplied | **Yes (postgame only)** `data/gamebooks/2026/wk09/` |
| S16 | Sharp Football Analysis public tables (coverage, OL, DL, defensive tendencies, red zone, pace, advanced box scores) | Third party | 2026 season to date; no archive found | Weekly ("Updated: November 24", 15:23 ET) | None (page scrape) | **Yes** `pregame/coverage_rates.py` (coverage only), `data_ingest/` (box scores, merged #122). OL/DL/red-zone tables **not** integrated |
| S17 | StatRankings team coverage chips | Third party (partly paid) | NOT VERIFIED (home page loads, HTTP 200) | Chips stamped 2026-11-26 00:02Z per PR #143 | Free tier; premium tools listed | **Draft only** PR #143 |
| S18 | ESPN Analytics win rates (pass rush, run stop, pass block, run block; player and team) `espn.com/nfl/story/_/id/49742016/...` | Third party (ESPN; says it uses NGS tracking) | 2026 snapshot "Through Week 10 games, Nov. 24 at 10 a.m. ET" | Weekly | None | **No** (cited in `SOURCES.md` only) |
| S19 | Public book endpoints (DraftKings, FanDuel, Pinnacle, Caesars) and Action Network scoreboard | Unofficial web endpoints | Snapshots only | On demand | None; can be refused by IP or state | **Yes** `pregame/sportsbooks.py`, `pregame/direct_books.py`, `pregame/line_history/*.jsonl` |
| S20 | The Odds API v4 (`odds`, `historical`) | Third-party API | Historical from 2020-06-06 (doc) | Live | **Paid key; 0 credits left** | **Yes** `pregame/odds.py` (not callable now) |
| S21 | Sportsbook Reviews Online NFL odds archive | Third-party archive | Index lists 2007-08 through 2021-22 only | Static | None | **No** |
| S22 | Open-Meteo: Forecast, Historical Forecast, Historical Weather (archive) APIs | Third party (open weather models, ERA5) | Archive: 1940 to the day before the call (verified through 2026-11-26). Historical Forecast: "from 2022" (doc) | Daily | None; free tier is non-commercial, under 10,000 calls a day, CC-BY 4.0 | **Partial** forecast API in `data/historical/refreshes/week9/tools/weather.py` and PR #140; archive **not** used |
| S23 | NWS `api.weather.gov` (points, hourly forecast, observations) | **Official** (US government) | Forecast about 6.5 days; observations recent only (section 14) | Live | None (User-Agent header) | **Yes** `pregame/weather.py` (forecast only) |
| S24 | NOAA ISD "global-hourly" on S3 (`noaa-global-hourly-pds`) | **Official** (NOAA) | KBUF 2025 file ends 2025-08-27 | Stale mirror (section 14) | None | **No** |
| S25 | Meteostat (bulk files, JSON API) | Third party | Legacy bulk file KBUF-area ends 2026-02-11 | Stale (section 14) | JSON API needs a RapidAPI key (HTTP 401 without) | **No** |
| S26 | Paid: FTN Data API/CSV, PFF, SIS, NFL Pro | Paid third party | Not accessed | n/a | Paid | **No** (PFF captured by hand: `data/pff_captures_w1_8`, first paid tier only) |

## 3. Component 1: receiver routes and route participation

**Verdict: NOT SUPPORTED** for routes run and route participation. Target-conditional route type is available for 2016-2025 only.

| Candidate | Verified | Supports an equation? | Limits and missing fields |
| --- | --- | --- | --- |
| S2 participation `route` | Definition (nflreadr dictionary): "the route the **primary receiver** on a play took". Check: on regular-season sacks `route` is non-null on 0.0% (2016-2022), 1.1% (2023), 0.2% (2024), 0.1% (2025) of rows; on pass attempts with a receiver id it is non-null 98.6% to 99.4%. One value per play. Labels: 12 in 2022 (HITCH, FLAT, OUT, CROSS, GO, SCREEN, IN, SLANT, POST, ANGLE, CORNER, WHEEL), 13 in 2025 (QUICK OUT, HITCH/CURL, GO, SCREEN, IN/DIG, DEEP OUT, SHALLOW CROSS/DRAG, SLANT, POST, SWING, CORNER, WHEEL, TEXAS/ANGLE). | **Limited.** Target route mix per team or receiver is computable (2025 league mix: QUICK OUT 18.4%, HITCH/CURL 17.8%, GO 9.0%, SCREEN 8.9%, IN/DIG 8.8%). Targets per route run, yards per route run, route participation are **not** computable. | Taxonomy changed between 2022 and 2023: do not pool without a mapping. No 2026 file (HTTP 404, released after the post-season). |
| S2 `offense_players`, `offense_positions` (on-field list per play) | `n_offense == 11` on 100% of 2025 regular-season dropbacks. Position labels seen: WR, T, G, TE, RB, C, QB, FB, DT. These are roster positions, not alignment (no slot or wide label). | **Limited.** "On the field for a dropback" is an **upper bound** on routes run (includes pass blockers). Targets per on-field dropback is computable. | No route-run flag, no alignment, no 2026. |
| S6 snap counts | `offense_snaps`, `offense_pct`, `defense_snaps`, `st_snaps` per player-game, 100% non-null (2024, 2026 checked); 2026 weeks 1-12. | **Limited.** Snap share for opportunity context. Not routes. | PFR snap counts count all offensive snaps, run and pass. |
| S4 NGS receiving | Columns: `avg_cushion`, `avg_separation`, `avg_intended_air_yards`, `percent_share_of_intended_air_yards`, `targets`, `receptions`, `avg_yac`, `avg_expected_yac`, `avg_yac_above_expectation`. No route columns. | No for routes. | Qualifiers only (section 10). Public NGS route charts are images of targeted routes (repo `data/ngs/README.md`), not a feed. |
| S3 FTN (nflverse subset) | 29 columns; none contain `route`, `cover`, or `press` (checked by name). | No. | The paid FTN catalog does list `rte` (route type 0-12) and a participation feed with `skp_role` (RTE, FRTE, BRTE, PPRO, FPRO, RBL, FHO, RUN) per FTN's public catalog; the nflverse subset omits them. |
| Paid: FTN API | Per FTN's public pages (read as search excerpts 2026-11-27, not purchased): charting and all-22 participation back to 2019, expanded participation back to 2021; API from $5,000 a year commercial or $3,000 private; CSV package $599 a year is base stats only. | Yes, if bought. | **NOT VERIFIED** beyond the vendor's own pages. Needs the owner's approval. |

**Integration risk.** `pipeline/matchup_sources.py` lists participation `route` as the source for `receiver_routes` and `rb_routes`. Today `participation_routes()` returns MISSING ("not wired yet"), so nothing is mislabeled. If it is ever wired, those two fields would be filled with a statistic that is not routes run.

## 4. Component 2: target depth and route distribution

**Verdict: SUPPORTED for depth and aDOT. LIMITED for route distribution.**

| Candidate | Verified (regular season) | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S1 pbp `air_yards`, `pass_length`, `pass_location`, `receiver_player_id` | Share of pass attempts (no sacks, no spikes) with `air_yards`: 99.4% to 99.6% in every season 2016-2026. `pass_location`: 99.4% to 99.6%. `receiver_player_id`: 98.8% (2016) falling to 95.7% to 96.0% (2023-2026). About 17,500 to 18,800 attempts a season (2026: 10,995 through week 12). | **Yes.** aDOT per receiver, offense, or defense; short, intermediate, deep splits; left, middle, right. About 550 attempts per offense-season. | `air_yards` is distance to the target spot, not the route stem. Non-targeted receivers have no depth. Direction is the offense's view. |
| S4 NGS receiving | `avg_intended_air_yards`, `percent_share_of_intended_air_yards` present in 100% of rows. 2025 regular-season coverage: rows exist for 28.1% of player-weeks with at least one target, covering 54.8% of targets (smallest row has 5 targets). | **Limited.** Good for starters; silent for the rest. | Absence is not zero. Do not average over missing player-weeks. |
| S5 PFR defense `def_adot` | Non-null on 66% to 69% of defender rows (blank when the defender had no completion data). | **Limited.** Defender aDOT-when-targeted. | See component 4. |
| S2 `route` for distribution | See component 1. | **Limited.** Targeted-route mix only. | 2016-2025. |

## 5. Component 3: man, zone, single-high, split-safety coverage

**Verdict: LIMITED.** Play-level through 2025; team-level, non-point-in-time for 2026.

Regular-season dropbacks, participation joined to pbp (reproduce with `docs/audits/nfl_source_coverage_verify.py`):

| Season | Dropbacks | `defense_man_zone_type` non-null | `defense_coverage_type` non-null | Man share of known | Provider |
| --- | --- | --- | --- | --- | --- |
| 2016, 2017 | 20,073; 19,418 | 0.0% | 0.0% | n/a | NGS |
| 2018 | 19,766 | 88.6% | 88.6% | 35.0% | NGS |
| 2019 | 19,923 | 88.9% | 88.9% | 37.2% | NGS |
| 2020 | 20,024 | 89.3% | 89.3% | 34.4% | NGS |
| 2021 | 20,907 | 89.0% | 89.0% | 30.3% | NGS |
| 2022 | 20,299 | 88.6% | 88.6% | 28.8% | NGS |
| 2023 | 20,775 | 99.6% | 99.6% | 41.3% | FTN |
| 2024 | 20,215 | 99.8% | 99.8% | 48.5% | FTN |
| 2025 | 19,830 | 99.9% | 99.9% | 31.0% | FTN |

Verified field values: `defense_man_zone_type` = MAN_COVERAGE or ZONE_COVERAGE. `defense_coverage_type` = COVER_0, COVER_1, 2_MAN, COVER_2, COVER_3, COVER_4, COVER_6, COVER_9, COMBO, BLOWN in 2023-2025; the 2022 file also carries PREVENT and has no COVER_9, COMBO or BLOWN.

| Candidate | Supports an equation? | Limits |
| --- | --- | --- |
| S2 participation (2018-2025) | **Yes at team-season grain** (about 550 to 650 known dropbacks per defense-season). Man or zone EPA per dropback and cover-type splits are computable. | Man share swings 28.8% (2022), 41.3% (2023), 48.5% (2024), 31.0% (2025). The jump at 2023 is a provider change; 2024 to 2025 is a 17.5-point drop inside one provider. **Do not pool seasons without checking.** No single-high or split-safety field exists; the usual mapping (COVER_1, COVER_3 as single-high; COVER_2, COVER_4, COVER_6, 2_MAN as two-high) is an **assumption**, not a delivered field. No 2026 file. |
| S16 Sharp `nfl-coverage-schemes` | **Limited.** Verified columns: Team, Man Rate, Zone Rate, Middle Closed Rate, Middle Open Rate for 32 teams, season to date, stamped 2026-11-24 15:23 ET. Middle-closed (MOFC) and middle-open (MOFO) are the closest free single-high and two-high proxies. | Team level only; no weekly history, so a past week cannot be reconstructed point-in-time. Sharp's underlying charting provider is **NOT VERIFIED** from the page. Repo copy `data/coverage/sharp_coverage_2026.csv` carries a "November 17" stamp (pulled 2026-11-24 6:26 AM ET); the live page read here said "Updated: November 24". Sharp and StatRankings differ by about 15 points on man % (PR #143); never mix them on one slip. |
| S17 StatRankings | **NOT VERIFIED.** Free team chips exist (PR #143 used them). | Premium tools (coverage IQ, shadow coverage) are listed with a paywall marker; which fields are free was not re-verified here. |
| S1 pbp 2026 | No. pbp has no coverage columns (checked by name on the 372 columns). | n/a |
| Paid: FTN `shell` coverage, PFF | Would give 2026 play-level. | Not accessed. |

## 6. Component 4: defender-to-receiver assignments

**Verdict: NOT SUPPORTED** (NOT FOUND (free) for who covered whom).

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S5 PFR `advstats_week_def` | Columns: `def_targets`, `def_completions_allowed`, `def_yards_allowed`, `def_receiving_td_allowed`, `def_passer_rating_allowed`, `def_adot`, `def_air_yards_completed`, `def_yards_after_catch`, `def_times_blitzed`, `def_times_hurried`, `def_times_hitqb`, `def_sacks`, `def_pressures`, `def_tackles_combined`, `def_missed_tackles`. 2018-2026. Summed `def_targets` equals 97.5% of pbp pass attempts (no sacks) over 541 team-games in 2025 (median 97.2%, 10th to 90th percentile 88.6% to 110.3%), with a median 14 defenders per team-game. | **Limited.** A defender-level "allowed when targeted" equation is valid (targets, yards, rating, aDOT). | Targeted plays only. No snaps in coverage, no alignment, no receiver name. Yard fields are blank when no completion was allowed (non-null about 59% to 61%). PFR's attribution method is **NOT VERIFIED** (its glossary was not read). |
| S1 pbp `pass_defense_*`, tackle, sack, `qb_hit_*` player columns | Present (verified by column name). | **Limited.** Verified outcomes only (PBU, INT, tackler, sacker). | Not an assignment. This is what PR #143's inferred layer builds on (held-out top-1 25%). |
| S2 `defense_players`, `defense_positions` | On-field defenders per play. | No. | No assignment, no alignment. |
| S4 NGS | `avg_separation`, `avg_cushion` are receiver aggregates. | No. | No defender fields. NFL Pro coverage responsibility is not held (repo ledger, Rico 2026-11-21). |
| Paid: FTN participation feed | Public catalog lists `def(1-5)` "ID of associated defender", `def_pos`, `cushion`. | Yes, if bought. | Not accessed; owner approval needed. |

## 7. Component 5: true pressure and blitz rates

**Verdict: LIMITED.** Four free measures exist; they are not the same statistic and they disagree.

| Measure | Verified | Seasons | Notes |
| --- | --- | --- | --- |
| S2 `was_pressure`, `number_of_pass_rushers`, `time_to_throw` | `was_pressure` non-null on dropbacks 88.7% to 90.8% (2016-2022), 100% (2023-2025). Regular-season pressure rate: 2022 29.1%, 2023 29.5%, 2024 30.9%, 2025 29.8%. | 2016-2025; no 2026 | **Definition changed in 2023.** In the NGS years `was_pressure` and `time_to_throw` are null on 100% of 2022 sacks (1,356 of 1,356, all season types). In 2023-2025 pressure is true on 99.9% to 100% of sacks and on 99.9% to 100% of QB hits. Pre-2023 and post-2023 rates are not comparable. |
| S3 FTN `n_blitzers`, `n_pass_rushers` | Non-null on 99.7% (2022), 100% (2023-2025), 97.8% (2026, weeks 1-11) of dropbacks. Share of dropbacks with at least one blitzer: 23.9%, 27.2%, 28.8%, 29.3%, 31.0% (2022-2026). | 2022-2026 wk 11 | No pressure flag. Participation `number_of_pass_rushers` equals FTN `n_pass_rushers` on 100.0% (2023), 99.9% (2024), 100.0% (2025) of plays, 76.5% in 2022: **in 2023-2025 these are one source, not two.** |
| S5 PFR pass: `times_blitzed`, `times_hurried`, `times_hit`, `times_pressured`, `times_pressured_pct`, `times_sacked`; def: `def_pressures`, `def_times_blitzed`, `def_times_hurried`, `def_times_hitqb`, `def_sacks` | All non-null (2018-2026, 2026 to week 11). In `week_pass`, the columns `def_times_blitzed`, `def_times_hurried`, `def_times_hitqb`, `receiving_drop`, `receiving_drop_pct` are 100% null (placeholders). | 2018-2026 wk 11 | Only source with a per-defender pressure count (`def_pressures`). |
| S1 pbp `qb_hit`, `sack` | 100% non-null; `qb_hit` 2,730 to 3,021 and sacks 1,118 to 1,410 per season on dropbacks (2016-2025). | 2016-2026 | Outcome events only (hits and sacks), not pressure. |
| S16 Sharp OL and DL tables | Team Pressure Rate, No-Blitz Pressure Rate (Allowed on the OL page), Time to Throw (OL page). Stamped 2026-11-24. | 2026 to date | Team only; charting provider NOT VERIFIED. |

**Cross-source disagreement (2025 regular season, 544 team-games).**

| Pair | Sum A | Sum PFR | Correlation | Exact team-game match |
| --- | --- | --- | --- | --- |
| participation `was_pressure` vs PFR `times_pressured` | 5,906 | 4,277 | 0.658 | 8.6% |
| FTN `n_blitzers > 0` dropbacks vs PFR `times_blitzed` | 5,820 | 4,574 | 0.732 | 12.5% |
| pbp `qb_hit` vs PFR `times_hit` | 2,891 | 1,567 | 0.760 | 11.9% |
| pbp `sack` vs PFR `times_sacked` | 1,287 | 1,281 | 0.998 | 98.9% |

Sacks reconcile; pressure, blitz and hit do not. No free source says which pressure definition is "true". An equation can use one source consistently (team and QB rates, hundreds of dropbacks per team-season) but must not mix them. **For 2026, no free play-level pressure flag exists**; the best in-season inputs are FTN blitz (through week 11), PFR pressure counts (through week 11) and Sharp season-to-date rates.

## 8. Component 6: QB performance vs pressure and vs coverage

**Verdict: LIMITED.** Computable for 2018-2025 from S2 joined to S1; thin per QB; not available for 2026.

| Season (REG) | QBs with at least 100 dropbacks | Median pressured dropbacks | Median man-coverage dropbacks | Fewest man dropbacks | QBs with at least 50 pressured | QBs with at least 50 man |
| --- | --- | --- | --- | --- | --- | --- |
| 2022 | 47 | 92.0 | 91.0 | 11 | 38 | 37 |
| 2023 | 48 | 110.5 | 162.5 | 16 | 41 | 45 |
| 2024 | 46 | 117.5 | 195.0 | 49 | 43 | 45 |
| 2025 | 45 | 112.0 | 126.0 | 29 | 41 | 39 |

League-level sanity check, 2025 regular season dropbacks (descriptive, not a model; dropbacks include sacks): EPA per dropback when pressured -0.367 (n = 5,906) versus not pressured +0.210 (n = 13,924). Man +0.057 (n = 6,134) versus zone +0.030 (n = 13,679). The pressure split is large; the man/zone split is small, and a per-QB man/zone split at about 126 plays is well inside noise.

| Candidate | Supports an equation? | Limits |
| --- | --- | --- |
| S2 x S1 (EPA, success, CPOE) | **Yes for pooled multi-season or league-level work; limited per QB-season.** | Definition drift (components 3 and 5). No 2026. |
| S4 NGS passing | **Limited.** `avg_time_to_throw`, `aggressiveness`, `avg_air_yards_to_sticks`, `completion_percentage_above_expectation` present in 100% of rows, 2016-2026 (week 12). | Starters only. No pressure or coverage splits. |
| S5 PFR pass | **Limited.** `times_pressured_pct`, `passing_bad_throw_pct`, drops, per QB-game, 2018-2026. | Different pressure definition than S2. |
| S3 FTN | **Limited.** `is_play_action`, `is_qb_out_of_pocket`, `read_thrown`, `is_throw_away`, blitz counts. | No pressure or coverage field. |

## 9. Component 7: offensive-line and defensive-line grades

**Verdict: NOT SUPPORTED** for grades. LIMITED for win-rate and team-level proxies.

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S18 ESPN Analytics win rates | Page loaded (HTTP 200). Tables found: Edge and DT pass rush win rate, OT and IOL pass block win rate, Edge and DT run stop win rate, OT and IOL run block win rate, plus team win rates. Player rows carry Rank, Name, Team, Wins, Plays, win rate, double-team %. Stamped "Last updated: Through Week 10 games, Nov. 24 at 10 a.m. ET". Stated basis: NGS tracking data. | **Limited.** Player and team matchup of pass-block vs pass-rush win rates for the current season. | No downloadable file or API. HTML only. Prior-week archive **NOT VERIFIED** (so not point-in-time for backtests unless snapshots are captured weekly). Page showed Week 10 although the nflverse schedule has Week 11 played 2026-11-19 to 2026-11-23. Terms of use for scraping **NOT VERIFIED**. |
| S16 Sharp OL page | Columns: Pressure Rate Allowed, No Blitz Pressure Rate Allowed, Time to Throw, Yards Before Contact Per RB Rush, Rush Stuff Rate (32 teams). Stamped 2026-11-24. | **Limited.** Team-level only. | Not integrated. Provider and definitions **NOT VERIFIED**. |
| S16 Sharp DL page | Columns: Pressure Rate, No Blitz Pressure Rate, Yards Before Contact Per RB Rush, Rush Stuff Rate. | **Limited.** Team level. | Same. |
| S5 PFR | `rushing_yards_before_contact` and `_avg` per RB game (all non-null 2018-2026); `def_pressures`, `def_sacks` per defender. | **Limited** proxies. | These attribute to the runner or rusher, not to individual linemen. |
| S1 pbp | `sack_player_id`, `qb_hit_1_player_id`, `tackle_for_loss_*` names. | **Limited.** Counting stats. | Not grades. |
| Paid: PFF grades | The repo holds the first paid tier only (SOURCE_STATUS); pro-only facets out of scope. | n/a | Not accessed; needs owner approval for any refresh. |

## 10. Component 8: RB opportunity, carries, targets, rushing concepts

**Verdict: SUPPORTED** for opportunity, direction and gap. **NOT SUPPORTED** for zone vs gap scheme and RB routes.

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S10 `stats_player_week_2025` | Contains `carries`, `rushing_yards`, `rushing_first_downs`, `rushing_epa`, `targets`, `receptions`, `receiving_air_yards`, `target_share`, `air_yards_share`, `wopr`, `racr`. No route, snap, pressure or coverage column (the only substring hits were `fumble_recovery_*`). | **Yes.** Carries, targets and shares per player-week. | No routes. |
| S6 snap counts | `offense_snaps`, `offense_pct`; 2026 weeks 1-12. | **Yes** (snap share). | Not pass-route snaps. |
| S1 pbp `run_location`, `run_gap` | `run_location` non-null on 98.8% to 99.1% of designed rushes (no kneels, no scrambles) every season 2016-2026. `run_gap` non-null on 69.0% to 74.2%. **`run_gap` is blank on 100% of `run_location == middle` rushes and on 0% of left or right rushes, in every season 2016-2026.** Gap values: guard, tackle, end. Middle runs were 24.7% (2022), 25.1% (2024), 26.6% (2025) of rushes. 2025 league totals: 3,458 guard, 3,230 tackle, 2,808 end. | **Yes.** Direction YPC and EPA per RB, team, defense; about 88 to 108 gap-tagged rushes per team-season in 2025 (league total divided by 32). | The blank gap is structural (no gap for a middle run), not random missingness as `data/scheme_profiles/build_profiles.py` implies ("often blank"). Splits by gap, side and defense type get small fast. |
| S4 NGS rushing | `efficiency`, `percent_attempts_gte_eight_defenders`, `avg_time_to_los`, `rush_yards_over_expected` (and per attempt, and percent over expected). Expected-yards columns are null before 2018. 2025: rows for 25.2% of rusher-weeks covering 60.3% of carries (smallest row 10 attempts). | **Limited.** | Qualifiers only. |
| S5 PFR rush | `carries`, `rushing_yards_before_contact`, `rushing_yards_after_contact`, `rushing_broken_tackles` (non-null 2018-2026). `receiving_broken_tackles` is 100% null in this table. | **Yes** (contact splits). | |
| Run concept (zone, gap, power, counter) | **NOT FOUND (free).** No column in pbp, FTN subset, NGS, PFR or participation. | No. | The paid FTN catalog lists `concept` and `dir` (LE, LT, LG, RM, RG, RT, RE). Not accessed. |
| RB routes and RB target-per-route | See component 1. | No. | |

## 11. Component 9: third-down and red-zone tendencies

**Verdict: SUPPORTED.**

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S1 pbp `down`, `ydstogo`, `yardline_100`, `posteam`, `defteam`, `play_type` | 100% non-null on rush and pass plays (2016-2026). 2025 per defense-season: third-down dropbacks median 165 (min 142); red-zone (inside 20) dropbacks median 92.5 (min 63); red-zone plays median 162.5; inside the 5 median 45 (min 27). | **Yes.** Pass rate, conversion, EPA, and play-type tendency by down and zone. | 2026 weeks 1-12 hold about 70% of a full season, so inside-5 and blitz-by-down cells are small (shrink toward a prior). |
| S3 FTN (blitz on third down) | 2025 third-down blitzed dropbacks (`n_blitzers > 0`) per defense: median 60 (min 42). | **Yes** with shrinkage. | 2022+, 2026 through week 11. |
| S2 (coverage and rushers by down) | Available 2018-2025. | **Limited.** | No 2026. |
| S16 Sharp red-zone page | Page exists (HTTP 200, "NFL Red Zone Stats 2026"). Columns **NOT VERIFIED**. | n/a | Team level. |
| PR #144 `situational_allowed.csv` | Already builds third-down, 3rd-and-7+, red-zone, FTN blitz and play-action splits for 2026. | n/a | **Not duplicated here.** This section only confirms the sample sizes behind it. |

## 12. Component 10: official injury reports and inactive lists

**Verdict: LIMITED.**

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S7 nflverse `injuries` | Columns (2026): `season, season_type, game_type, team, week, gsis_id, position, full_name, report_primary_injury, report_secondary_injury, report_status, practice_primary_injury, practice_secondary_injury, practice_status`. **`date_modified` exists 2016-2024 (100% non-null) and is absent from the 2025 and 2026 files.** In 2024 the median team-week carries 7 distinct stamps, so intraweek progression is reconstructable for 2016-2024 only. `practice_status` non-null 99.3% to 100%; `report_status` non-null 41% to 60% (blank rows are listed on the practice report only; blank is not zero-filled). 2026 weeks 1-12: 3,824 rows; week 12: 343 rows (23 Out, 23 Questionable, 297 blank) in the file stamped 2026-11-27 12:24 ET. | **Limited.** Weekly status, practice participation, and Out counts for 2016-2026. | One row per player-week. No publication time in 2025-2026, so "known before kickoff" cannot be proven from the file (also noted in `calibration/outputs/WEATHER_INJURY_EVIDENCE.md`). |
| S13 NFL.com official report page | Fetched `nfl.com/injuries/league/2026/reg12` (HTTP 200, about 8:40 PM ET). Columns: Player, Position, Injuries, Practice Status, Game Status. 352 player rows: Out 76, Questionable 64, Doubtful 3, blank 209 (31 team-table headers parsed against 32 teams playing; difference not investigated). Season selector lists 2000-2026. | **Limited.** Official, current week. | One snapshot per page view, no row timestamps, no intraweek history. Its Week 12 counts (Out 76) are far above the nflverse file's (Out 23) fetched hours earlier: consistent with the nflverse copy predating Friday's designations, **not investigated further**. Not integrated. |
| S11 ESPN `injuries` | 800 entries across 32 teams; statuses Active 583, Out 113, Questionable 59, Injured Reserve 40, Doubtful 4, Suspension 1; each entry has its own `date` (2026-11-14T02:55Z to 2026-11-28T01:31Z). | **Limited.** Per-entry as-of time. | Current only, newswire-sourced, not official, capped per team (repo note: 25), "Active" is not "healthy". Integrated. |
| S14 club "Inactives" articles | Repo parser `phase15/official_inactives.py`, fail-closed; no API. | **Limited.** Official game-day list, 2026 in-season. | About 90 minutes before kickoff. No free history. |
| S8 `weekly_rosters` `status == INA` | 2026 weeks 1-12: 2,093 `INA` rows, mean 6.27 per team-week (min 4, max 8). **0% of `INA` rows have a snap-count row**, while 73% of `ACT` rows do. | **NOT VERIFIED as an inactives list.** Consistent with game-day inactives; not compared to an official list. | Candidate historical proxy only. Snapshot timing unknown. |
| nflverse release catalogue | 25 release tags listed on 2026-11-27; none is an inactives or game-day active list. | n/a | **NOT FOUND (free)** for a historical official inactives dataset. |
| S15 NFL game summaries | Week 9 only, owner supplied, media-use restriction. | postgame only | Not a pregame input. |

## 13. Component 11: timestamped sportsbook opening and current lines

**Verdict: NOT SUPPORTED** for timestamped opening lines from any free source. LIMITED for closing and untimed opening lines.

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S9 nflverse `games` closing lines | `spread_line`, `total_line` non-null 100% of finished regular-season games 2016-2026 (`home_moneyline` 99.6% in 2017 only). One consensus close per game; no timestamp, no open, no book. | **Yes** for closing-line calibration. | Not an opening line; not point-in-time. Sign convention: positive means home favored. |
| S12 ESPN core odds (`.../odds`, items `open`, `close`, `current`) | All 14 games probed for 2026 week 12 (events 2026-11-26 to 2026-11-30) return one provider (Draft Kings) with `open`, `close`, `current` for spread, total, moneyline. KC@BUF: open BUF -2.5, total 49.5; close and current -3, 46.5. nflverse for the same game: 3.0 and 46.5. **No timestamp on `open`**; the `history/0/movement` endpoint returned 0 items for 6 of 6 events tried. First event of each prior season probed (one game each): 2025 and 2024 have `open` (ESPN BET); 2021-2023 list 15 to 18 providers with **no** `open`. | **Limited.** A single book's untimed open and close, 2024+. | One book, no time, sample of one game per past season. Unofficial. Not integrated. |
| S19 public book endpoints and Action Network scoreboard | Action Network `web/v2/scoreboard/nfl` (one request): current outcomes only; no field matching `open`, `updated`, `time` or `created` in the market objects. Repo polls books itself and stores `pregame/line_history/*.jsonl` (14 files, all week 10) and `pregame/direct_lines/` (45 files). | **Yes, only from the first capture onward.** | Snapshot-only feeds; the "open" is whatever the first poll saw. Books can refuse requests (repo notes DraftKings 403 from GitHub runners). Weeks 1-2 2026 have no named-book timestamped quotes (`data/historical/MANIFEST.md`). |
| S21 SportsbookReviewsOnline | Archive index lists NFL seasons 2007-08 to 2021-22 (and preseason). The spreadsheets were **not downloaded**; open and close columns and timestamps **NOT VERIFIED**. | Unknown. | Ends 2021-22. |
| S20 The Odds API historical | Docs (read 2026-11-27): historical snapshots from 2020-06-06 at 10-minute intervals, 5-minute from September 2022; player props, alternates and period markets after 2023-05-03; **paid plans only**. | Yes, if credits are bought. | Account has no credits; **not called**. Owner approval needed. |

A true timestamped opener therefore comes from two places only: the repo's own going-forward capture (already in place) or a paid historical feed. Do not label a first poll an "open" without recording that it is the first capture (already the repo's rule in `data/lines/README.md`).

## 14. Component 12: weather and historical weather effects

**Verdict: SUPPORTED** (observed kickoff conditions). **LIMITED** (forecast-as-issued history).

| Candidate | Verified | Supports an equation? | Limits |
| --- | --- | --- | --- |
| S1 pbp `weather` text (per game) | Non-empty for outdoor games 99.4% to 100%. Text carries a condition word, `Temp: NN° F`, `Humidity: NN%`, `Wind: DIR N mph`. Temperature parses on 99.0% to 100% of outdoor games every season 2016-2026; wind on 97.4% to 100% from 2021 (88% to 91% before 2021, where the numeric column fills the gap). **Dome games also carry text** (an example dome game reads "Sunny Temp: 83° F...", i.e. outside conditions): filter on `roof`. | **Yes.** Outdoor games 2016-2025: 1,878; with wind of 15 mph or more 186 (13 to 24 per season), 20 mph or more 37; precipitation word 152 (keyword match: rain, shower, snow, drizzle, storm, sleet, flurry); 32°F or colder 101. | One kickoff-time observation per game (no hourly path, no gusts, no precipitation amount). |
| S9 `games` / pbp numeric `temp`, `wind` | Non-null for outdoor games: 2016 99.0%, 2020 100%, 2021 94.3%, **2022 51.3%**, 2023 78.5%, 2024 97.2%, 2025 97.8%, **2026 37.9% (116 outdoor or open games finished)**. Where both numeric and text exist: identical in 2020 and near-identical in 2023 (mean absolute difference 0.1°F, 0.3 mph); **differ in 2021 (mean absolute difference 1.9°F temperature, 2.7 mph wind, exact wind match 12%) and 2022 (2.7°F, 3.3 mph, 10%).** | **Limited.** Use the parsed text as the primary kickoff observation, numeric as a cross-check. | Two sources inside one file disagree in 2021-2022. |
| S22 Open-Meteo Historical Weather (archive) | Buffalo (42.7738, -78.787): 168 hourly rows for 2026-11-20 to 2026-11-26, 0 nulls across temperature, wind, gust, precipitation, rain, snowfall, humidity, surface pressure; a 2016-09-11 request also returned 24 rows. Docs: ERA5 from 1940, 0.25 degree grid (about 25 km); IFS 9 km from 2017. | **Yes.** Hourly path across kickoff plus three hours; precipitation amount and gusts. | Model reanalysis at a grid cell, not the stadium sensor; data run to the day before the call. Free tier is non-commercial, under 10,000 calls a day, CC-BY 4.0. Roof state (retractable) is not in the weather API. |
| S22 Open-Meteo Historical Forecast and Previous Runs | Docs: Historical Forecast from about 2022 (stitched first hours of each model run); Previous Runs from January 2024 at fixed 1-7 day lead (GFS from March 2021); Single Runs from 2024-03 for ECMWF IFS and 2026-04-02 for other models. A 2018-09-09 request returned 24 values although docs say about 2022: **not relied on**. | **Limited.** Forecast-error and as-forecast effects from 2022 (2024 for fixed lead times). | Stitched series is not a forecast "as issued at T-24h" unless Previous Runs or Single Runs are used. |
| S23 NWS | Points and gridpoint lookups work (BUF 39,42). Observations endpoint returned 500 features from 2026-11-26 23:55Z back to 2026-11-22 07:00Z (limit reached) and **0 features for 2025-11-20 to 2025-11-21**. | **Limited.** Forecast: yes (integrated). Observations: recent days only. | Not a historical archive. |
| S24 NOAA ISD S3 | KBUF station file for 2025: 10,236 rows from 2025-01-01 to **2025-08-27**, object last modified 2025-10-04; the 2024 file last modified 2025-03-01. Fields are encoded strings (`WND` like `040,5,N,0021,5`, `TMP` like `-0061,5`). | **Limited.** Station-measured history, needs decoding and a station map. | Mirror is not current in-season. NOT VERIFIED whether another NOAA path (NCEI access service) is current. |
| S25 Meteostat | Legacy bulk file for station 72528: 690,994 hourly rows to 2026-02-11 14:00; gusts non-null on 5% of rows 2018-early 2025 versus temperature 100%. JSON API: HTTP 401 without a key. | **Limited.** | Stale; key required for the live API. License NOT VERIFIED. |

The repo's measured weather effects (`calibration/outputs/WEATHER_INJURY_EVIDENCE.md`: train-only 2018-2025 coefficients, 19 weather games in the 2026 walk-forward, every CI spans zero) rest on kickoff observations, so they are optimistic relative to a forecast.

## 15. Field-name traps (similar names, different statistics)

1. **`pbp_participation.route`** is the primary receiver's route on the play, not routes run (component 1).
2. **`pbp_participation.offense_players`** is on-field presence, not route participation or alignment (component 1).
3. **`defense_coverage_type` / `defense_man_zone_type`** are play-level team coverage labels with no per-defender assignment; no field says single-high or split-safety (components 3, 4).
4. **`was_pressure`** is null on sacks in 2016-2022 and true on essentially every sack and hit in 2023-2025; PFR `times_pressured`, FTN `n_blitzers`, and pbp `qb_hit` are different measures that disagree (component 5).
5. **Participation `number_of_pass_rushers` and FTN `n_pass_rushers`** match 99.9% to 100.0% in 2023-2025: one source counted twice if both are used as independent evidence.
6. **PFR `def_*`** describes targeted plays only; `def_times_blitzed`, `def_times_hurried`, `def_times_hitqb` exist in `week_pass` as 100% null placeholders.
7. **pbp `run_gap`** is blank because a middle run has no gap, not because data is missing at random. There is no run-scheme field.
8. **`games.temp` / `wind`** are blank on many outdoor games (2022: 48.7%, 2026: 62.1%) while the pbp `weather` text exists; numeric and text differ in 2021-2022.
9. **`games.spread_line` / `total_line`** are closing consensus lines, not opens, with no timestamp.
10. **ESPN odds `open`** has no timestamp and comes from one book.
11. **nflverse `injuries`** has `date_modified` through 2024 and not in 2025-2026.
12. **`weekly_rosters.status == INA`** looks like inactives but is not verified against an official list.
13. **FTN "participation" in nflverse is not the FTN participation feed.** The nflverse participation file has no route-run or defender-association fields; the vendor's paid feed does.

## 16. Gaps and recommendations (no purchase, no source change is made by this PR)

Ranked by decision value. Items 1 to 4 are free engineering; 5 to 7 need the owner.

1. **Relabel, do not wire, participation `route`.** Keep `receiver_routes` and `rb_routes` MISSING; add a separate field `targeted_route_type` if the 2025 file is used. Add a null-rate guard (the file has blank strings, not nulls).
2. **Capture weekly snapshots of the current-season free tables now**: Sharp coverage, OL, DL, red zone; ESPN win rates; NFL.com injury page. All are current-season snapshots with no verified archive, so past weeks cannot be rebuilt later. Store pulled time and the page's own stamp.
3. **Choose one pressure and one blitz definition per equation** (recommend FTN blitz for 2022-2026 and PFR or participation pressure within one season range), and record the 2023 boundary in any backtest. Do not average sources.
4. **Use the parsed pbp `weather` text** as the primary kickoff observation (numeric `temp` and `wind` are only 37.9% to 100% complete by season for outdoor games, with 2022 at 51.3% and 2026 at 37.9%), and Open-Meteo archive for hourly paths and gusts. Exclude dome and closed rows by `roof`. Start saving Open-Meteo Previous Runs (fixed lead) output going forward if forecast-error effects are wanted.
5. **Decide whether to pay for FTN** (route runner flag, defender association, pressure flags back to 2019/2021). It is the only source in this audit that covers components 1, 3 (2026 play level), 4 and the zone/gap run concept. Public price from FTN's pages: $5,000 a year commercial or $3,000 private for the API. Needs the owner's explicit approval; nothing was purchased or called.
6. **Historical timestamped lines**: either accept going-forward capture only (already running) or approve The Odds API historical credits. The ESPN core odds `open` can seed an untimed open for 2024+ if clearly labelled.
7. **Inactives history**: no free official list was found. If a backtest needs it, the owner can supply NFL game summaries (as for Week 9), or test whether `weekly_rosters` `INA` matches the official lists on a few 2026 weeks first.

## 17. Methodology and verification log

All times America/New_York unless marked UTC. Measurements marked "script" are reproduced by `docs/audits/nfl_source_coverage_verify.py` (output saved as `docs/audits/nfl_source_coverage_verify_output.md`). Everything else was a one-off request on the dates shown.

| What | How | Date and time |
| --- | --- | --- |
| Repo and PR review | Cloned `main` at `ef4cc690`; read README, `SOURCES.md`, `DATA_GAPS.md`, `docs/SOURCE_*`, `docs/PHASE_WORKFLOWS.md`, `pipeline/freshness.py`, `pipeline/matchup_sources.py`, `pregame/sources.py`, `pregame/weather.py`, `pregame/sportsbooks.py`, `phase15/official_inactives.py`; fetched PRs #140, #143, #144, #149, #151 (descriptions, files, #143 and #144 READMEs, #140 rules doc). `/workspace/nfl-sim/specs/matchup_database_spec.md` read. | 2026-11-27 8:36 to 8:50 PM |
| nflverse release inventory | GitHub releases API listing of `nflverse-data`; per-release `timestamp.txt` | 2026-11-27 8:37 and 8:50 PM |
| nflverse downloads | pbp 2016-2026; participation 2016-2025 and `old_2023`; FTN 2022-2026; NGS (3 files); PFR week pass/rec/rush/def 2018-2026; injuries 2016-2026; snap counts 2024-2026; games; rosters 2026; stats_player 2025; depth charts 2025-2026. `pbp_participation_2026.parquet` returned HTTP 404. | 2026-11-27 8:38 PM |
| Null rates by season, joins, cross-source agreement | Script (pandas). Regular season only; blank strings counted as null. | 2026-11-27 8:50 PM to 9:20 PM |
| Field definitions | nflreadr data dictionaries (participation, FTN, PFR, injuries, NGS, snap counts), `load_*` reference pages, nflverse data schedule page, nflverse-data `LICENSE.md` (CC-BY 4.0) | 2026-11-27 |
| ESPN site API | `scoreboard` (2026-11-26, 2026-11-29, five prior-season openers), `summary` (KC@BUF event 401873082), `injuries` | 2026-11-27 8:45 to 9:10 PM |
| ESPN core odds | `/odds` for 14 week-12 events and 5 prior-season openers; `/odds/100/history/0/movement` for KC@BUF and the 5 openers | 2026-11-27 9:00 to 9:10 PM |
| Action Network | One `scoreboard/nfl` request (date 20261129) | 2026-11-27 8:55 PM |
| Open-Meteo | Archive (Buffalo, 2026-11-20 to 2026-11-26; 2016-09-11); Historical Forecast (2022-09-11, 2018-09-09); docs pages and terms page | 2026-11-27 8:55 PM |
| NWS | `points`, `gridpoints/.../stations`, `stations/KBUF/observations` for 2026-11-20 to 2026-11-27 and 2025-11-20 | 2026-11-27 8:57 PM |
| NOAA, Meteostat | S3 object and headers for KBUF 2024 and 2025 files; Meteostat legacy bulk `72528.csv.gz`; JSON API without a key | 2026-11-27 8:58 PM |
| NFL.com | `injuries/league/2026/reg12` parsed; operations.nfl.com injury-report URL returned 404; a game-centre page loaded but no inactives text was found in its static HTML (**not investigated further**) | 2026-11-27 9:05 PM |
| Sharp | Coverage, OL, DL, defensive tendencies, offensive tendencies, red zone pages loaded; tables read for the first four; `nfl-offensive-line-rankings` returned 404 | 2026-11-27 9:08 PM |
| ESPN win rates | Page loaded; table names and stamp read | 2026-11-27 9:12 PM |
| The Odds API | Public guide page only (historical section). **No API call.** | 2026-11-27 9:00 PM |
| FTN pricing and catalog | Web search excerpts of FTN's public pages. **No purchase, no key, no API call.** | 2026-11-27 9:15 PM |
| SBR | Index page only (season links); no spreadsheet downloaded | 2026-11-27 9:02 PM |

### NOT VERIFIED
PFR's definition of targeted-defender attribution; Sharp's and StatRankings' underlying charting provider and free-field list; ESPN win-rate archive and scraping terms; SBR spreadsheet contents; Meteostat license; whether another NOAA path is current; SIS and PFF pricing and fields (not researched; PFF tier is from the repo's `docs/SOURCE_STATUS.md`); whether `INA` roster status equals the official inactives list; why NFL.com showed 31 team tables; participation provider mapping beyond the nflreadr doc statement; Historical Forecast coverage before 2022.

### NOT FOUND (free)
Routes run and route participation; per-defender coverage assignment or alignment; play-level coverage and pressure for 2026; per-player OL/DL grades; run scheme (zone, gap, power) and run concept; timestamped opening lines; historical official inactives.

### Rights and use
nflverse data is CC-BY 4.0 by default; participation from 2023 and FTN charting are CC-BY-SA 4.0 and need FTN attribution (`SOURCES.md` already says so). Participation 2016-2022 needs NFL NGS attribution. Open-Meteo's free tier is non-commercial. ESPN, Action Network, Sharp, StatRankings and book endpoints are page or endpoint reads with no stated license here; the repo's existing hash-only and "do not redistribute" rules apply.
