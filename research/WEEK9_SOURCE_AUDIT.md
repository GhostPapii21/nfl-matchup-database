# WEEK9 Source Audit

**As of:** 2026-11-07 ~11:31 ET
**Status:** Research evidence only. Model NOT READY.

## Verified sources used
- Public aggregators (FantasyTools.ai, SumerSports, LineupExperts, FTA, Parlae, Footballguys, PerThirtySix, StickToTheModel, RankFantasy, StartWho, KofSports) for TE snap %, target share, and available route participation.
- Ghost6 v14 + priority delta (PFF authenticated/free pages) for TE LB-group coverage context (24/26) and the published Anzalone projection for Colston Loveland.
- Blitz WEEK9_USAGE_BUNDLE_v2 for official role statements, recent-vs-season comparisons, CLE/PHI starter resolutions, and weather refresh.
- sportsbook-odds-bridge `data_packages/nfl_2026_w1_8/` for historical numerical CSVs (referenced only; not duplicated).
- NFL.com / official team reports / ESPN / public PFF pages for matchup quality and injury context (team-level only).
- Prior baseline (official game logs, nflverse, recovered PFR coverage pages for 249 CBs/safeties) retained.

## Counts
- Sunday games covered: all Week 9 games (team-level and primary TE focus).
- Players researched (primary TEs): 10+ with numerical usage; 26 with group coverage context.
- Defensive teams covered: group-level for 24/26 TE matchups.
- Verified source rows: see CSVs (TE usage, defensive matchups, injuries/weather).
- Unresolved discrepancies: Ferguson/Henry group cards; named individual assignments deferred.
- Material data blockers: game-day inactives and full route participation deferred to Sunday morning.

## Restricted items
- No restricted PFF charting redistributed.
- No production database writes.
- No model parameter or weight changes.

**PR #2 handoff package staged. Model remains NOT READY.**
