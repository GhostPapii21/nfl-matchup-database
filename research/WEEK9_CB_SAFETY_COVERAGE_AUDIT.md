# WEEK9 CB/Safety Coverage Audit (Weeks 1–8)

**As of:** 2026-11-07 ~11:52 ET
**Status:** Research evidence only. TE CSV does not satisfy this requirement. Model NOT READY.
**Retrieval date:** 2026-11-07.

## Available files already in research branch (exact names)
- `WEEK9_DEFENSIVE_AND_DB_PROFILES_SUMMARY.md` (2026-11-07 ~08:30 ET) — notes recovery of PFR individual coverage for **249 CBs and safeties** (targets, completions, yards allowed). Source: cached/recovered PFR pages + public NGS.
- `WEEK9_PFR_VS_PFF_DB_RECONCILIATION_SUMMARY.md` — prior reconciliation notes.
- `WEEK9_DEFENSIVE_MATCHUPS.csv` — TE-focused only; does not cover CB/safety coverage requirement.
- `WEEK9_TE_USAGE_TARGET_ROUTE.csv` — offensive TE usage only; does not satisfy defender coverage requirement.
- Other WEEK9_*.md / *.csv files are usage, injury, source audit, or missing-data notes.

## Public source: Pro-Football-Reference Advanced Defense 2026
- **URL:** https://www.pro-football-reference.com/years/2026/defense_advanced.htm
- **Update note on page:** Advanced stats updated through Week 8 of the 2026 season (updated Wednesday following games).
- **Directly available fields (Pass Coverage section):** Tgt, Cmp, Cmp%, Yds, Yds/Cmp, Yds/Tgt, TD, Rat, DADOT, Air, YAC, plus Int, PD, and related.
- **Sample:** Individual player rows for CBs, safeties, and other DBs (search results show dozens of CB/S rows with non-zero targets; prior branch note of 249 recovered individual pages is consistent with this public table).
- **Game/player IDs:** Player pages and advanced game logs available (example: https://www.pro-football-reference.com/players/B/BurgTe00.htm shows week-level Tgt/Cmp/Yds).
- **Missing from free PFR Advanced Defense table:** explosive completions (20+), coverage snaps/routes as a denominator, slot/outside alignment splits, man/zone or shell assignments, and source-defined middle-of-field open/closed labels.
- **Access:** Page returned 403 on direct browse in this session; fields confirmed from search extracts and prior recovered data. No scraping of restricted content.

## Public source: Sharp Football Analysis Coverage Stats by Position
- **URL:** https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/
- **Update date:** 2026-11-03.
- **Fields present (team-level, all 32 teams):** YPT Allowed WR, YPT Allowed TE, YPT Allowed RB, YPT Allowed Outside, YPT Allowed Slot.
- **Missing:** defender-level targets/receptions/yards, explosive completions, coverage snaps/routes, man/zone rates, shell assignments.
- **Note:** Slot/outside is team-level YPT only; not individual defender alignment.

## Man/zone or shell data
- StatRankings.com lists man coverage rates (e.g., Jevon Holland 73.3%) but requires subscription for full access; free tier does not provide a complete Weeks 1–8 defender-level export.
- PFF Coverage Matchup Tracker and premium tables are access-restricted; Ghost6 prior note confirms premium tables incomplete on account check.
- No free public source found that provides source-defined shell/coverage measures (Cover 2/3/4, middle-of-field open/closed) at defender or team level for all 32 teams with sample sizes and denominators.

## What remains unavailable (access restrictions or not published free)
- Defender-level explosive completions (20+ yards).
- Coverage snaps or routes defended as a consistent denominator across all 32 teams.
- Individual defender slot/outside alignment percentages.
- Source-defined man/zone rates or shell assignments for all teams (restricted to paid PFF/StatRankings/FTN).
- Guaranteed individual shadow assignments (explicitly not inferred from nearest-player or tackle credit).
- Full game-by-game defender coverage logs with player/game IDs for every CB/S (PFR advanced game logs exist but require per-player retrieval; bulk free export not available).

## Rules followed
- No inference of defender assignment from nearest-player list or tackle credit.
- No labeling of defenses as “middle of field open” from generic zone rates.
- Inferred observations kept separate from directly charted facts.
- Stopped at access restrictions.
- No model weights, code, database, or projections changed.

**Prior recovered PFR individual coverage (249 CBs/safeties) remains the best free defender-level targets/completions/yards source. Full coverage snaps, explosive, alignment, and shell data remain unavailable without restricted access.**
