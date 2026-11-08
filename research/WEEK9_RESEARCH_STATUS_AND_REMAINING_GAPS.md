# NFL Week 9 Research Status and Remaining Gaps

**As of:** 2026-11-07 ~18:45 ET
**Branch:** research/nfl-w9-source-verified-evidence-20261107
**PR:** #2
**Status:** PARTIAL research package. Model NOT READY.

## Completed / Staged

### Ghost6 CB/Safety Research Package (INTEGRATION_READY_FORMAT)
- Location: `research/week9_cb_safety_profiles/`
- 26 defenses, 479 scoped profiles, 1,389 Weeks 5–8 defender-game rows, 1,682 explicitly credited receiver-linked events.
- Depth charts, game observations, receiver observations, opponent context, sources/gaps, integrity tests (passed).
- Individual per-game targets/receptions/yards/explosives allowed: **NULL** (no charted source).
- Current depth vs historical roster scopes kept separate.
- Projected Week 9 pairings isolated in separate verification table (not observed).

### Team-Level Coverage Schemes
- `research/WEEK9_COVERAGE_SCHEMES_TEAM.csv` — Sharp Football man/zone/middle open/closed rates.

### Individual Metrics Note
- `research/WEEK9_INDIVIDUAL_COVERAGE_METRICS_NOTE.md` — sample StatRankings target rates vs zone + PFR limits.

### Other Staged Artifacts
- Team matchup sheet, TE usage/target/route, quarter scores verification, pressure-to-sack audit, QB scramble audit, source audits, injury/weather notes, calibration ledger placeholder, etc.
- All labeled PARTIAL or RESTRICTED where applicable.

## Remaining Lingering Issues (from original prompt / handoff)

1. **Individual charted game-level coverage metrics** — targets_allowed, receptions_allowed, yards_allowed, explosives_allowed remain NULL for every defender-game. No free public source provides full charted individual responsibility.
2. **Named defender assignments / alignments** — Blitz coverage task incomplete (usage limit hit). Route-type frequencies and film-observed alignments not fully verified.
3. **Full man/zone/shell per snap** — restricted or unavailable without paid charting. Team aggregates only.
4. **Sunday game-day inactives and official designations** — deferred until Sunday morning. No-designation ≠ confirmed active.
5. **AJ Barner / Tyler Warren target conflicts** — previously flagged; retain both values or exclude from model inputs until resolved.
6. **Historical period market quotes** — limited by Odds API credits; no full backtest-ready quarter/half lines staged.
7. **Calibration ledger** — no archived pregame model forecasts available for joining.
8. **Pressure-to-sack splits** — charted pressure denominators incomplete for some teams; rates left unavailable where source lacks charting.
9. **QB scramble vs designed run** — nflfastR fields used; sample-size warnings remain for stratified rates.
10. **Route participation / slot-outside exact shares** — partial for many skill players.

## Rules Followed
- No model weights, code, production, or database writes.
- No inferred individual assignments.
- Observed results kept separate from projections.
- Missing fields null with reasons.
- Source rights respected; restricted data not redistributed.

**Next possible actions (Sunday morning or later):** official inactives, any new public charting releases, or paid-source aggregates if rights allow. Research-only until then.

Model remains **NOT READY**.
