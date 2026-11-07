# NFL 2026 Week 9 (Sun Nov 8): CB/S cover profiles, 26 defenses. RESEARCH BRANCH ONLY
Status: INTEGRATION_READY_FORMAT. PARTIAL; this is NOT complete coverage stats. Make no model, pick or production changes from this.
## Contents
- DEFENDER_PROFILES (479 rows): every current depth-chart DB plus historically scoped DBs.
  - Current depth: ESPN depth charts fetched Nov 7 2026.
  - 130 are rank-1 rows: 5 listed per team, which includes the nickel slot as ESPN lists it. Not our guess.
  - PFR season coverage: cache mtime Nov 4 07:02 ET, cutoff unverified. PFF free season profiles. Kept separate, with their own sources.
- DEFENDER_GAME_OBSERVATIONS (1389 rows): W5-8 nflverse pbp + snap counts. Team is the team as of each game.
- DEFENDER_RECEIVER_OBSERVATIONS (1682 rows): explicit pbp credits for PBU, INT or tackle-after-catch, with the receiver named.
- DEPTH_CHART_ROWS (309 rows), SOURCES_AND_GAPS, TEAM_COUNTS, OPPONENT_RECEIVER_CONTEXT (team context, separate).
## Hard caveats
- Individual per-game targets, receptions, yards and explosives allowed are ALL NULL. No game-level charted coverage source was found, and pbp does not identify the coverage defender.
- NEVER count tackles as coverage. A tackle-after-catch row's yards are the play's yards, not yards charged to that DB.
- PBU/INT events are observed events, not full coverage stat lines.
- Roster/team in game rows is historical (as of that game), not current.
- Current role and IR status are as of Nov 7 and do not guarantee a player is active.
- Team 20+ yd completions are TEAM context only.
- PFF Week 9 projected WR-DB rows are projections, not observed coverage.
- PFR live returns 403 and was not retried. No paid data was used.
## Provenance
- Codex session 01a1b814-6162-7f72-ae38-dbde5c53069c; existing ChatGPT login; web search + normal sandbox; exit 0; 11m28s.
- Tests: INTEGRITY_TESTS 72 PASS lines = 38 internal + 34 EXPORT (17 export assertions logged twice) / 0 FAIL; verify_exports rerun 17 PASS / 0 FAIL.
