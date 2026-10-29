# Data Gaps — latest Phase 10 source run

Run: 2026-10-27T04:43:39.891731+00:00

All source families are checked independently. Historical/stale evidence is retained but cannot satisfy current mandatory checks.

| Source | Fetch | Parsed observations | Freshness | Gaps |
| --- | --- | --- | --- | --- |
| espn_win_rates | OK | 144 | STALE | FRESHNESS_STALE; PARTIAL_LEADERBOARD; REQUESTED_COLUMNS_MISSING |
| sharp_position | OK | 160 | STALE | FRESHNESS_STALE |
| sharp_scheme | OK | 128 | STALE | FRESHNESS_STALE |
| sharp_tendencies | OK | 128 | STALE | FRESHNESS_STALE |
| sharp_advanced | OK | 84 | FRESH | REQUESTED_COLUMNS_MISSING |
| raiders_cb | FETCH_ERROR | 0 | UNKNOWN | FETCH_ERROR |
| statrankings_explosive_rate | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| statrankings_explosive_count | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| statrankings_adot | OK | 4 | FRESH | PLAYER_ID_UNRESOLVED; PARTIAL_PAID_METRICS |
| statrankings_perimeter | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| hashtag_discovery | OK | 0 | UNKNOWN | FRESHNESS_UNKNOWN; DISCOVERY_ONLY |

Detailed gap records and raw snapshot paths are in external_sources_status.json and SQLite external_gaps. No-source and missing metric cells remain INSUFFICIENT DATA.

Latest provider snapshots and original masters are separate. The profile links label season aggregates as scouting context, not game measurements. Full Phases 1–10 green-card readiness is not certified by this pipeline.


## Incremental verified Sharp update — 2026-10-28T12:08:52.932600+00:00

Imported 84 verified Week 7 observations (EPA per play, success rate, pressure rate allowed) across 28 team-game rows through the existing Phase 10 parser/persist/export path. Publisher update: 2026-10-27T13:34:45Z. Exact data-through cutoff remains unstated beyond Week 7. Other source families were not newly ingested; earlier gaps remain open. Detailed requested-column gaps remain in external_sources_status.json. Raw evidence is publisher-rendered text with documented transport. No model weights or schedules changed.

## Publication review — 2026-10-29

This snapshot preserves the collected source records. Passing SQLite integrity and checksum checks does not certify every football statistic or model assumption. The following issues remain open; the database is usable for research with these limitations, and the projection model is not promoted or included in this publication.

| Issue | Evidence and limitation | Required before model release |
| --- | --- | --- |
| `ISS-ebcc83ddaf58bbde92e64b5c260b3e215c47332a1f10ef04d67d6d43ebce6fcc` — credited play yards | For game `401873007`, play `401873007411`, the stored numeric yardage is 7 while the description reports a Golden 37-yard reception followed by a taunting penalty. Numeric play yardage, descriptive gains and player box-score credits cannot be treated as interchangeable. WR/RB explosive and run-stuff counts derived from these fields remain provisional. | Declare credited-gain semantics; reconcile with authoritative game books; preserve raw evidence; test penalties, no-plays, laterals, negative runs and fumbles. Do not repair facts by parsing text alone. |
| `ISS-776429323d7fceffc2dfb4a3936b85f3b8d2dadfc18029b96cb54cf3b508fc94` — returning-player workload | Jacobs' return includes 11 carries and 7 targets in his recorded Week 7 appearance, while the baseline allocation dilutes his role with earlier absence/backup history. Savion Williams' short participation history also needs separate treatment. | Verify participation and current role, distinguish inactive periods from active zero production, then evaluate one scoped allocation change against the frozen baseline. |
| `ISS-1eb28b14b506fd56de4656150ed4ac8810586389e17bd7707e607ec00d71ec9b` — participation denominator | Coker has five recorded appearances; a missing player-stat row is not evidence of a verified zero-opportunity game. The baseline denominator can depress his projected share. | Audit participation independently before changing denominators or accepting an under signal. |
| `ISS-ff1caad18347c10f7c7a299a7af8cf6991261bd0771604a5e7a6540a9caf6114` — QB rushing | QB rushing currently uses team designed-run yardage templates and omits endgame kneels. | Separate player scramble, designed-run and kneel behavior; add regression and chronological evaluation before promotion. |

Regulation/overtime scoring scope has been reviewed, but complete player-level overtime splits and overtime simulation are not certified. Passing-volume changes, receiving opportunity versus efficiency, and probability/selection calibration still require independent evaluation. Previously inspected games are development evidence, not an untouched holdout. No 70–80% selection accuracy or complete-ticket success rate has been established.

Sharp alignment/scheme freshness, complete routes and coverage assignments remain gaps. Official NGS receiving aggregates and two Week 7 NFL highlight transcripts were reviewed separately for the matchup; they were not ingested as a complete fresh database layer. Highlights are incomplete film evidence and cannot establish all routes or defender responsibility. Legal receiving laterals can produce receiving yards without a reception; do not turn those records into fabricated catches or targets.
