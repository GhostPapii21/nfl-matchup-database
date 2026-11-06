# Projection run checklist — empty template

Run ID: ___ | game ID/namespace: ___ | season/week: ___
Cutoff UTC: ___ | frozen/generated UTC: ___ | manifest path: ___
Workflow versions/definition artifacts: ___

## Source inventory gate — complete before scenario/projection execution

- [ ] Create a row for every source below using source_ledger.schema.json.
- [ ] Record actual fields, scope, timestamps, artifact path/hash, status reason, fallback and null reasons.
- [ ] Verify retrieved artifact bytes, availability by cutoff, freshness and required field coverage; listed ≠ usable retrieved.
- [ ] Reconcile source discrepancies; preserve MISSING/UNKNOWN and excluded claims.
- [ ] Record gate status, evidence, permitted scope and unresolved blocking dependencies in manifest/report.

Each row below is blank intentionally; choose only SUCCESS/SAVED_ONLY/MISSING/LOGIN_REQUIRED/STALE/ERROR/NOT_APPLICABLE based on evidence. No box or blank status implies success.

| Source/tool | Status | Ledger row/evidence | Fallback/blocker |
| --- | --- | --- | --- |
| ESPN | | | |
| nflverse | | | |
| PFR | | | |
| gamebooks | | | |
| FTN via nflverse | | | |
| NGS | | | |
| PFF | | | |
| Sharp | | | |
| StatRankings | | | |
| PropsMadness | | | |
| SumerSports | | | |
| FantasyPoints | | | |
| NFLPro | | | |
| official injury/depth | | | |
| ESPN availability/depth | | | |
| Ourlads | | | |
| AP | | | |
| RotoWire | | | |
| official X | | | |
| NWS | | | |
| OpenMeteo | | | |
| stadium tools | | | |
| weather_forecast.py | | | |
| FD | | | |
| DK | | | |
| Pinnacle | | | |
| OddsAPI | | | |
| Outlier | | | |
| PP | | | |
| Polymarket | | | |
| official film reconciled to PBP | | | |
| local DB | | | |
| local sim | | | |
| local engines | | | |

## Scenario-first gate

- [ ] Complete betting-game-brainstorm before the 15-phase workflow: hypothesis, alternatives, falsifiers and source dependencies.
- [ ] Record actual workflow version and evidence; unsupported scenarios stay labeled.

## Fifteen nfl-game-script-run phases

Map each placeholder to the authoritative phase definition/version; do not invent names or claim completion if definitions are unavailable. Record evidence or an explicit workflow-supported N/A reason.

| Done | Phase | Authoritative name | Evidence | Blocker / N/A reason |
| --- | --- | --- | --- | --- |
| [ ] | 01 | | | |
| [ ] | 02 | | | |
| [ ] | 03 | | | |
| [ ] | 04 | | | |
| [ ] | 05 | | | |
| [ ] | 06 | | | |
| [ ] | 07 | | | |
| [ ] | 08 | | | |
| [ ] | 09 | | | |
| [ ] | 10 | | | |
| [ ] | 11 | | | |
| [ ] | 12 | | | |
| [ ] | 13 | | | |
| [ ] | 14 | | | |
| [ ] | 15 | | | |

## Supplemental workflows and release

- [ ] nfl-betting-script: applicability/reason ___; version ___; evidence ___
- [ ] football-period-game-flow: applicability/reason ___; version ___; evidence ___
- [ ] Freeze canonical identity, code/config/inputs, artifact hashes and split lineage per core_contract.md.
- [ ] Preserve coverage UNKNOWN; routes and personnel 11/12/13 MISSING unless verified new evidence supports a new freeze.
- [ ] Keep TNF postgame evidence separate; no holdout claim by fitting.
- [ ] Complete report.md, manifest, blockers, excluded scopes and required phase evidence before releasing outputs.
- [ ] Record engineering unit/regression tests separately from projection runs; tests do not fulfill this workflow.

Projection execution status: ___ | engineering checks status/evidence: ___

Readiness: projection_ready ___ | validation_basis ___ | synthetic ___
Brainstorm artifact path (marker: betting-game-brainstorm): ___
Automatic weather/WR/edge cuts: DISABLED; approval evidence MISSING.
NOT_APPLICABLE source exclusions require a nonempty reason.
