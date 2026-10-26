# Data Gaps — latest Phase 10 source run

Run: 2026-10-25T22:56:46.490235+00:00

All source families are checked independently. Historical/stale evidence is retained but cannot satisfy current mandatory checks.

| Source | Fetch | Parsed observations | Freshness | Gaps |
| --- | --- | --- | --- | --- |
| espn_win_rates | OK | 144 | STALE | FRESHNESS_STALE; PARTIAL_LEADERBOARD; REQUESTED_COLUMNS_MISSING |
| sharp_position | OK | 160 | STALE | FRESHNESS_STALE |
| sharp_scheme | OK | 128 | STALE | FRESHNESS_STALE |
| sharp_tendencies | OK | 128 | STALE | FRESHNESS_STALE |
| sharp_advanced | OK | 84 | STALE | FRESHNESS_STALE; REQUESTED_COLUMNS_MISSING |
| raiders_cb | FETCH_ERROR | 0 | UNKNOWN | FETCH_ERROR |
| statrankings_explosive_rate | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| statrankings_explosive_count | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| statrankings_adot | OK | 4 | FRESH | PLAYER_ID_UNRESOLVED; PARTIAL_PAID_METRICS |
| statrankings_perimeter | OK | 5 | FRESH | PARTIAL_PAID_METRICS |
| hashtag_discovery | OK | 0 | UNKNOWN | FRESHNESS_UNKNOWN; DISCOVERY_ONLY |

Detailed gap records and raw snapshot paths are in external_sources_status.json and SQLite external_gaps. No-source and missing metric cells remain INSUFFICIENT DATA.

Latest provider snapshots and original masters are separate. The profile links label season aggregates as scouting context, not game measurements. Full Phases 1–10 green-card readiness is not certified by this pipeline.

## Weeks 1–6 historical coverage

All 93 ESPN games and 93 Sharp Source 5 game joins are verified. Other source/week archive gaps and cumulative-only snapshots are recorded in weeks_1_6_backfill_status.json. See WEEKS_1_6_REPORT.md.

## New public sources found

The prior broad coverage/NGS/injury/snap-count gaps are partly resolved by additional FTN/PFR/NGS/nflverse imports for all 93 games. See MISSING_DATA_SOURCING_REPORT.md for exact fields, counts, attribution and remaining limits. This does not establish full route trees, coverage shells or a verified day-by-day injury chronology.
