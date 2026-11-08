# Optional player evidence interface (not a prop engine)

Rico ask (Ghost6 relay ~1:07 PM ET 2026-11-05): when emitting player-prop-related analysis alongside period work, include Outlier H2H/recent form, comparable allowances, target-location vs defense-area overlay (short/intermediate/deep × left/middle/right), alignment/route and verified defenders; source chart/screenshot tied to exact market/rung. H2H n, QB/role/injury/coverage changes and miss audit explicit. Green chart ≠ automatic edge.

## What this module does
- Optional Outlier CSV, if supplied locally: `core/period_engine_v0/optional_inputs/outlier_props.csv`. That file is not in this repository. Missing input stays MISSING.
- Ties a player+market+line+side to that row and/or a screenshot hash under the gamesim audit folder
- **Flags** location overlay, alignment, verified defenders, QB/role/injury/coverage, miss audit as MISSING unless caller attaches sourced material

## What it does NOT do
- Invent historical location overlays or H2H n
- Open Outlier in a browser / room sign-in (executor has no desktop for that)
- Replace nfl-game-script-run Phase 4 defender checks
- Produce prop engine probabilities or pad cards

## Chart gaps to report
Outlier CSV columns present: player, team, opponent, market, line, side, odds_*, IP, Opp_Rank, L5, L10, H2H, hit_2026/2025, source, notes.  
**Absent from CSV (need separate chart/screenshot or charting source):** target depth×horizon grid, alignment/route tree, named verified coverage defender, parsed H2H sample size, miss-audit causes.
