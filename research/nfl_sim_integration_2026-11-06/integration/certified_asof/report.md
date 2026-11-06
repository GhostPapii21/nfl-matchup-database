# JAX@BAL source readiness diagnostic — NOT_COMPLETE

projection_ready=false; source gate BLOCKED; research/NOLINE. SIMULATION NOT RUN; no forecasts or picks released.
Game alias ESPN 401873037; kickoff 2026-11-05 20:15 ET / 2026-11-06T01:15:00Z. Provider season 2026/week 9; local odds data_week 10 retained.
run_kind=diagnostic_evaluation; synthetic=false. The packet freeze occurs after kickoff; no claim of a pregame-authored read or forecast.
Inventory: SOURCE_INVENTORY_CORE_2026-11-06.md; ledger: source_ledger.json; attempt details: attempts.json; byte hashes: provenance.json.
Source ledger statuses: {'SAVED_ONLY': 15, 'ERROR': 1, 'MISSING': 16, 'NOT_APPLICABLE': 2}. No usable SUCCESS rows.
Foundational: final ESPN summary and gamebook saved, postgame only; nflverse roster used for diagnostic IDs. PFR HTTP 403; PBP/snaps/participation not certified.
Coverage/charting and NGS: required records missing. Availability: saved roster/inactive/injury evidence held, incomplete provenance. Environment: saved dated NWS/Open-Meteo responses held; current probes cannot replace frozen forecast evidence.
Markets: FD/DK/Pinnacle raw saved quote fields/meta verified; kickoff/time/week conflicts block promotion. OddsAPI no network; PP/Outlier/Polymarket scoped records missing. Official film not reconciled.
Local engineering: original actual-role audit retained with receiving-credit discrepancy. No new engine run or engine changes by this source pass.

Brainstorm: brainstorm.md provides conditional base and two flip scripts, falsifiers and missing dependencies; no model effects, assumed rates or numeric projections.
All 15 phases: see checklist.md; {'UNVERIFIED': 6, 'MISSING': 8, 'FAIL': 1}. Every phase remains execution BLOCKED. Definitions located; explicit skill versions absent, so NOT_COMPLETE.
Exact player joins use ESPN athlete IDs and team, validated against saved nflverse roster bytes. Full unmatched list retained; nested college/position false positives corrected without name joins.
Game provider aliases reconcile teams/kickoff/season/week for diagnostic identity only. Frozen schedule/PBP canonical registry join remains UNVERIFIED; odds event alias not force-joined.
Postgame ESPN final JAX 33, BAL 10 and gamebook/actual-role audit remain EVIDENCE_ONLY_POSTGAME. TNF is inspected evidence; not untouched holdout.
Coverage UNKNOWN; routes/personnel 11/12/13 MISSING; allows_sim_effect=false. Targets, position and depth do not supply charted measurements.
frozen_at_utc/generated_at_utc identify this diagnostic packet only; cutoff_utc is the requested historical boundary. Input/source/code hashes retained; no model config/seed/trial output exists.
Automatic weather/WR/edge cuts remain DISABLED regardless of older rule text. No betting placement, keyed odds request, new spend, cloud jobs, calibration edits or heavy simulations.
Engineering verification is separate: captured source_run_gate pytest and readiness.py live logs are referenced by SOURCE_READINESS_EVIDENCE.json. Passing tests cannot make projection_ready true.

Phase evidence (source: retained nfl-game-script-run skill; no phase is execution COMPLETE):

| Phase | Authoritative name | Status | Missing input / evidence |
| --- | --- | --- | --- |
| 01 | Data pull and reconcile | UNVERIFIED | Pregame PBP/box/snaps/participation and credit reconciliation missing; saved final box only. |
| 02 | Opportunity gate (FIRST; nothing else runs on a leg that fails it) | MISSING | No last-3 share/attempt or carry model, efficiency denominator or eligible priced leg. |
| 03 | Defensive profile (both teams) | MISSING | Both-team positional/slot/outside YPT, RB-only YPC, explosive and money-down denominators missing. |
| 04 | Defender coverage check (HARD, every WR/TE leg and every RB receiving leg) | MISSING | No per-defender targets/completions/YPT/rating or charted alignment/routes; coverage UNKNOWN. |
| 05 | Pressure, blitz and checkdown layer | MISSING | No certified blitz/pressure denominators, QB splits or conditional target samples; no proxy invented. |
| 06 | QB grade card | MISSING | No current-QB percentile reference set or sourced component grades. |
| 07 | Role and RB market rules | MISSING | No certified current-QB role history, last-4 carry shares or RB receiving efficiency. |
| 08 | Injuries, both sides | UNVERIFIED | Saved injury/inactive notes/images and roster bytes held; complete practice/depth provenance unverified. |
| 09 | Next Gen Stats | MISSING | NGS shell response only; no separation, route, RYOE or time-to-throw tables. |
| 10 | Film | UNVERIFIED | Saved gamebook/highlight audit is postgame; no official film-to-PBP reconciliation completed. |
| 11 | Environment | UNVERIFIED | Held dated weather responses; source availability/completeness and roof/rest/travel review unverified. |
| 12 | Source audit | FAIL | All 34 providers assessed in inventory; required usable categories absent, so source gate FAIL. |
| 13 | Game-script / underdog gate (10G) | UNVERIFIED | Conditional base/flip hypotheses only; no certified spread/EPA/Sharp profile or modeled minutes. |
| 14 | Models, price and edge | MISSING | SIMULATION NOT RUN; no model p/median/no-vig/edge; quote settlement and joins unverified: NOLINE. |
| 15 | Inactives check | UNVERIFIED | Held 18:55/18:56 declarations cannot prove complete pre-kick refresh, live price or final vet. |

Blockers:

- NOT_COMPLETE: skill definitions present but explicit authoritative skill version tags absent; no full workflow execution or final vet.
- No usable SUCCESS source rows; saved odds retain week/kickoff/canonical identity and settlement conflicts.
- Required pregame PBP/snaps/participation, defender coverage, route/personnel charting, pressure splits and QB grade cards not certified.
- Saved injury/weather/roster declarations are incomplete as-of evidence; postgame ESPN/gamebook/audit cannot repair a frozen forecast.
- Canonical game registry join UNVERIFIED; exact player aliases diagnostic only; unmatched IDs explicit.
- BetGuru binding for DIRECT wire pending; Ghost final acceptance not claimed.
- Forecast/model/market impact NOT_MEASURED; no before/after forecast evidence or untouched TNF holdout.

Next handoff: supply an authorized versioned workflow binding, review eligible original pregame sources and resolve identity/settlement discrepancies; preserve existing freeze and missingness. No impossible historic re-pull is required or claimed.
Impact/model improvement, calibration, accuracy and ROI: NOT_MEASURED; genuine before/after forecast evidence absent.
GHOST_ACCEPTANCE_PACKET addendum: source readiness still blocks projection; waiting BetGuru binding for DIRECT wire; Ghost final UNVERIFIED.

Captured verification: 87 source_run_gate engineering tests passed; 0 failures / 0 errors. Packet byte/lineage checks PASS. readiness.py live exited 1 with projection_ready=false and 36 reported blockers. Exact commands/logs: SOURCE_READINESS_EVIDENCE.json.
