# 2026_12_ATL_MIN

Result: **PARTIAL**

Research only. `projection_ready` is false. This is not a pick and not a scheduler.

- As of: 2026-11-29T12:00:00+00:00
- Kickoff: 2026-11-29T18:00:00+00:00
- Command: `python -m sunday game --game 2026_12_ATL_MIN --as-of 2026-11-29T12:00:00+00:00`
- Code revision: `4345bfbc85ac1d68552d9c3e40b957a710c48ab6`
- Canonical sha256: `a1ea62edcee73c92edf11ac3b85bf4f63d87c5272360106e89ddbb4d095289ff`
- Wall time: 18.120695 s
- Memory: Per-game tracemalloc is off during fan-out. The slate index records process max RSS.

## Critical checks

- `identity` **PASS** — Schedule identity matches. Kickoff 2026-11-29T18:00:00+00:00.
- `roles` **PASS** — Both clubs have a depth chart, a QB, a skill starter, and an availability block.
- `leakage` **PASS** — Source stamps are at or before as-of. Postgame paths were listed and not read.
- `engine` **PASS** — Python 3.12.3. Possession-engine files are present and projection_ready is false.
- `disk` **PASS** — Output directory has the requested free space.
- `runtime` **PASS** — Wrote and read a probe file in the output directory.

## Required checks that are not clear

- `phases` **GAP** — phase 4 PARTIAL; phase 6 PARTIAL; phase 7 PARTIAL; phase 8 PARTIAL; phase 9 PARTIAL; phase 10 PARTIAL; phase 13 PARTIAL; phase 14 PARTIAL_RESEARCH_ONLY
- `freshness.schedule` **STALE** — as-of 2026-11-27T04:31:42+00:00 (live_pull (live endpoint; pull time is the quote time)) is 3328 min old; limit is 1440 min at 6.0 h to kickoff.
- `freshness.play_by_play` **MISSING** — 'sources.pbp': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.rosters` **MISSING** — 'sources.rosters': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.depth_charts` **MISSING** — 'sources.depth_charts': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.snap_counts` **MISSING** — 'sources.snap_counts': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ftn_charting` **MISSING** — 'sources.ftn': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.pfr_defense` **MISSING** — 'sources.pfr_def': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.official_injuries` **MISSING** — 'sources.injuries': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.news_injuries` **STALE** — as-of 2026-11-27T04:31:46+00:00 (live_pull (live endpoint; pull time is the quote time)) is 3328 min old; limit is 120 min at 6.0 h to kickoff.
- `freshness.odds` **STALE** — as-of 2026-11-27T04:26:21+00:00 (live_pull (live endpoint; pull time is the quote time)) is 3334 min old; limit is 60 min at 6.0 h to kickoff.
- `freshness.ngs_passing` **MISSING** — 'sources.ngs_passing': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ngs_receiving` **MISSING** — 'sources.ngs_receiving': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ngs_rushing` **MISSING** — 'sources.ngs_rushing': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.four_book_prices` **STALE** — 3334 min old; limit is 60 min.

Required checks that are clear: 5.

## Research layers

- `NFL-87` **UNAVAILABLE** — Per-game orchestration registry. No module is registered, so nothing was executed.
- `NFL-88` **UNAVAILABLE** — Coverage and advanced-stat research. No module is registered, so nothing was executed.
- `NFL-89` **UNAVAILABLE** — Player opportunity board. No module is registered, so nothing was executed.
- `NFL-90` **UNAVAILABLE** — Three game scripts and independent model runs. No module is registered, so nothing was executed.
- `NFL-91` **UNAVAILABLE** — Market comparison and adversarial board. No module is registered, so nothing was executed.

## Player roles

- ATL: listed QB Michael Penix Jr.; availability flags: Billy Bowman Jr. (Did Not Participate In Practice), DeMarcco Hellams (Did Not Participate In Practice), Jahan Dotson (Did Not Participate In Practice), Matthew Bergeron (Did Not Participate In Practice), Za'Darius Smith (Did Not Participate In Practice), Zachariah Branch (Did Not Participate In Practice).
- MIN: listed QB Kirk Cousins; availability flags: Christian Darrisaw (Did Not Participate In Practice), Harrison Smith (Did Not Participate In Practice), Isaiah Rodgers (Did Not Participate In Practice), Jalen Redmond (Did Not Participate In Practice), Jordan Addison (Did Not Participate In Practice).

## Leakage

Status: **PASS**.
Excluded paths (not read): 1.
- `grading/results/sources/espn_summary_2026_12_ATL_MIN_401873084.json` — postgame or final-stat path; not read

## Cited outputs

- team_projection: **CITED_NOT_RERUN** — Copied from the pregame packet. This command did not re-simulate.
- locked_snapshot: **ABSENT** — No snapshots directory for this game.
- hundred_k: **NOT_RUN** — This command does not call pipeline.sim100k and does not start trials.

Inputs read:

- `core/possession_engine_v0/config/atl_min_2026-11-29_data_only_nfl43.json`
- `known_flags/KNOWN_LIMITATIONS.json`
- `pregame/packets/2026_12_ATL_MIN/packet.json`
- `pregame/packets/latest.json`
- `pregame/price_freezes/2026-11-29_ATL@MIN/freeze_20261127T043152Z.json`
