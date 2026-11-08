# Week 9 1 PM ET line, inactive and projection addendum

**Run:** 2026-11-08 12:56 ET, before 1 PM ET kickoff.  
**Scope:** DEN-CAR, DAL-IND, NYJ-KC, DET-MIA, CLE-NO, NYG-PHI, LAR-WAS.  
**Base freeze:** `NFL_W9_PROSPECTIVE_FREEZE_20261108_0856ET` remains unchanged.

## Completed

- Refreshed the live Fieldwork board API at `2026-11-08T17:56:11Z`. Captured 453 current DraftKings/FanDuel player-market quotes across 193 players. Each quote row preserves line, over/under price, source timestamp, receipt timestamp, and valid-until timestamp.
- Checked the official NFL inactive lists for all seven 1 PM games; see `WEEK9_1PM_INACTIVES_20261108.md`. Offensive skill players listed inactive were removed from the simulation.
- Generated 1,299 simulation rows: three empirical model distributions × 100,000 draws for each eligible book quote. The distributions retain zero-stat outcomes in games with a recorded positive opportunity.
- Ran the W5-W6 fit / W7-W8 untouched threshold diagnostic. Receptions and rushing-yard corrections passed the preset sample, positive-slope, Brier and log-loss rules; passing-yard and receiving-yard corrections did not. Diagnostic-passing corrections are recorded separately from raw probabilities.

## Readiness and calibration

`projection_ready=false`, `production_ready=false`, and `calibration_claim=false`. The diagnostic substitutes current lines for unavailable historical game lines; its weeks and player-game rows overlap across a limited four-week evaluation. It is not historical sportsbook-line calibration evidence and does not pass the full acceptance gate. Use the raw distribution columns as research estimates; the separate diagnostic-adjusted column is experimental sensitivity evidence.

This addendum is not a replacement for, or mutation of, the locked prospective forecast. It is a timestamped late market refresh using the same verified Weeks 1-8 player-game input. Defensive coverage assignment, routes, snap limits, pressure timing, and kickoff weather are not in these simulations.

## Artifacts

- `WEEK9_1PM_PROJECTIONS.md` — summarized projections and assumptions.
- `WEEK9_1PM_DK_FD_LINES_20261108_175611.028Z.csv` — raw DK/FD quote archive.
- `WEEK9_1PM_100K_SIMULATIONS.csv` — three 100,000-draw model results per eligible line.
- `WEEK9_1PM_CALIBRATION_DIAGNOSTIC.csv` and `WEEK9_1PM_WALK_FORWARD_EVENTS.csv` — calibration diagnostic and event-level audit.
- `WEEK9_1PM_SIMULATION_SKIPS.csv` — inactive and insufficient-history exclusions.
- `WEEK9_1PM_RUN_METADATA.json` — source timestamps, row counts, hashes and status.
- `run_current_week9_1pm.py` — reproducible refresh and simulation runner.

**Market source:** [Fieldwork Week 9 board](https://fieldworklines.com/nfl/2026/week-9); [methodology](https://fieldworklines.com/methodology). The board says it aggregates DraftKings, FanDuel, BetMGM and BetRivers through The Odds API and identifies its scheduled collection and quote-validity fields. It is an aggregator feed, not direct sportsbook API access.  
**Availability source:** [NFL.com official Week 9 inactives](https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season).
