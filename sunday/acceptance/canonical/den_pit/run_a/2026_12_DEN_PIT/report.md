# 2026_12_DEN_PIT

Result: **PARTIAL**

Research only. `projection_ready` is false. This is not a pick and not a scheduler.

- As of: 2026-11-27T04:31:50+00:00
- Kickoff: 2026-11-27T20:00:00+00:00
- Command: `python -m sunday game --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00`
- Code revision: `ec20087a829796efe52665f9e3b4f110543586f4`
- Canonical sha256: `f6b18d5d69cab230f7dd44dddc90f0dcb490bea660dab3230f3906dfbf70976c`
- Wall time: 8.390486 s
- Memory: tracemalloc peak 57604404 bytes; process max RSS 504808 KB

## Critical checks

- `identity` **PASS** — Schedule identity matches. Kickoff 2026-11-27T20:00:00+00:00.
- `roles` **PASS** — Both clubs have a depth chart, a QB, a skill starter, and an availability block.
- `leakage` **PASS** — Source stamps are at or before as-of. Postgame paths were listed and not read.
- `engine` **PASS** — Python 3.12.3. Possession-engine files are present and projection_ready is false.
- `disk` **PASS** — Output directory has the requested free space.
- `runtime` **PASS** — Wrote and read a probe file in the output directory.

## Required checks that are not clear

- `phases` **GAP** — phase 4 PARTIAL; phase 6 PARTIAL; phase 7 PARTIAL; phase 8 PARTIAL; phase 9 PARTIAL; phase 10 PARTIAL; phase 13 PARTIAL; phase 14 PARTIAL_RESEARCH_ONLY
- `freshness.play_by_play` **MISSING** — 'sources.pbp': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.rosters` **MISSING** — 'sources.rosters': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.depth_charts` **MISSING** — 'sources.depth_charts': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.snap_counts` **MISSING** — 'sources.snap_counts': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ftn_charting` **MISSING** — 'sources.ftn': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.pfr_defense` **MISSING** — 'sources.pfr_def': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.official_injuries` **MISSING** — 'sources.injuries': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.weather` **MISSING** — 'weather': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ngs_passing` **MISSING** — 'sources.ngs_passing': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ngs_receiving` **MISSING** — 'sources.ngs_receiving': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.
- `freshness.ngs_rushing` **MISSING** — 'sources.ngs_rushing': UNKNOWN_NO_SOURCE_TIMESTAMP: no publisher as-of stamp for this copy; our fetch time alone does not show the data is current.

Required checks that are clear: 8.

## Research layers

- `NFL-87` **UNAVAILABLE** — Per-game orchestration registry. No module is registered, so nothing was executed.
- `NFL-88` **UNAVAILABLE** — Coverage and advanced-stat research. No module is registered, so nothing was executed.
- `NFL-89` **UNAVAILABLE** — Player opportunity board. No module is registered, so nothing was executed.
- `NFL-90` **UNAVAILABLE** — Three game scripts and independent model runs. No module is registered, so nothing was executed.
- `NFL-91` **UNAVAILABLE** — Market comparison and adversarial board. No module is registered, so nothing was executed.

## Player roles

- DEN: listed QB Bo Nix; availability flags: J.K. Dobbins (Did Not Participate In Practice), Sai'vion Jones (Out), Taylor Rapp (Out).
- PIT: listed QB Mason Rudolph; availability flags: Aaron Rodgers (Did Not Participate In Practice), Alex Highsmith (Did Not Participate In Practice), Ben Skowronek (Did Not Participate In Practice), Cameron Heyward (Did Not Participate In Practice).

## Leakage

Status: **PASS**.
Excluded paths (not read): 24.
- `data/historical/playlogs/2026_wk12/DEN_PIT.csv` — postgame or final-stat path; not read
- `data/historical/projections/matchup_master_postgame_DEN_PIT.csv` — postgame or final-stat path; not read
- `grading/results/sources/espn_summary_2026_12_DEN_PIT_401873083.json` — postgame or final-stat path; not read
- `runs/2026-11-27_DEN@PIT/LIVE_DEFENSE.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/LIVE_DEFENSE_FINAL.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/LIVE_EXPLOSIVES.csv` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/LIVE_EXPLOSIVES_FINAL.csv` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/LIVE_LEGS.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/LIVE_LEGS_FINAL.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/POSTGAME_REVIEW.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/PREGAME_PROJECTION.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/RICO_SLIPS_LOCK.md` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/matchup_master_postgame_rows.csv` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/GAME_FINAL` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/coreplays_FINAL.json` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/plays_FINAL.csv` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/plays_latest.csv` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/poll.log` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/poll_live.py` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/pbp/summary_FINAL.json` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/rico_slips/09ddbbb2eb09dc2fd2316875f506a25382d2fc0a43a8909ad9b9ea3eeaecf3c3.png` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/rico_slips/5725a8c1c4c3c57af14bc9ef9f7252f1651c680df9e68388d66f8ad1bcf7b3c5.png` — game run folder sits beside postgame files; not read
- `runs/2026-11-27_DEN@PIT/rico_slips/8c220398b73e3f5c6f8d95fc46307ba02acd2eb4e8808cda6d0fc6ae02c67782.png` — game run folder sits beside postgame files; not read
- `snapshots/2026_12_DEN_PIT/20261127T111648Z` — snapshot directory is after as-of or at/after kickoff; not opened

## Cited outputs

- team_projection: **CITED_NOT_RERUN** — Copied from the pregame packet. This command did not re-simulate.
- locked_snapshot: **EXCLUDED** — No locked snapshot at or before as-of.
- hundred_k: **NOT_RUN** — This command does not call pipeline.sim100k and does not start trials.

Inputs read:

- `core/possession_engine_v0/config/den_pit_2026-11-27_data_only_nfl43.json`
- `known_flags/KNOWN_LIMITATIONS.json`
- `pregame/packets/2026_12_DEN_PIT/packet.json`
- `pregame/packets/latest.json`
- `pregame/price_freezes/2026-11-27_DEN@PIT/freeze_20261127T043150Z.json`
