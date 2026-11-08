# Standing Rico 6:19 source/run contract

Contract version: 1.1.1. Local schema/readiness alignment authored 2026-11-06.
Authority: coordinator-loaded Ghost skill `nfl-projection-source-preflight`, standing Rico 6:19, and the explicit local follow-up requirements. The skill body was not available in this workspace/local skill catalog; no independent skill-body review is claimed.
This is a standing requirement, not evidence of retrieved data or a completed projection.

Before **ANY projection/matchup/prop/simulation projection run**, execute in order:

1. Systematic source inventory: assess every source listed below individually; freeze and review the usable evidence and blockers.
2. `betting-game-brainstorm`: scenario-first hypotheses, alternatives, falsifiers and required evidence before selecting model effects or outputs.
3. All **15 `nfl-game-script-run` phases**, in their authoritative order. Use `nfl-betting-script` and `football-period-game-flow` when relevant, with applicability reasons recorded.

Do not start projection execution until the source gate and scenario-first step are documented. Phases that execute projections require those gates first; phase completion and output release require evidence for every applicable phase. A required unavailable workflow definition blocks claims of workflow completion. This package does not contain or invent the authoritative phase definitions: templates supply 15 numbered placeholders to be mapped to the actual workflow version before use. An N/A phase requires an explicit scoped reason and workflow support; omission is not completion.

Each run MUST retain `checklist.md`, `report.md`, a schema-conforming run manifest and source ledger rows, plus referenced frozen artifacts. Blank templates do not satisfy a run. Record workflow versions, cutoff, season/week, game identity, code/config/input hashes and retained evidence. Use a separate run directory for each run; do not overwrite a frozen forecast with later evidence.

## Mandatory source inventory

Inventory and status **each** listed source, including separate providers within a family. Names here are established inventory requirements, not claims of availability, account entitlement, exact tool routes, measured fields or prices.

| Family | Sources/tools to assess individually |
| --- | --- |
| Foundational data | ESPN, nflverse, PFR, gamebooks |
| Advanced/charting | FTN via nflverse, NGS, PFF, Sharp, StatRankings, PropsMadness, SumerSports, FantasyPoints, NFLPro |
| Availability/depth | official injury/depth, ESPN availability/depth, Ourlads, AP, RotoWire, official X |
| Environment | NWS, OpenMeteo, stadium tools, weather_forecast.py |
| Markets | FD, DK, Pinnacle, OddsAPI, Outlier, PP, Polymarket |
| Film | official film reconciled to PBP |
| Local engineering | local DB, local sim, local engines |

For this local package, all inventory entries are `MISSING`, assessment `not_attempted`, with reason **not retrieved or assessed for a projection by this pass**. This denotes missing run evidence; it does not diagnose a provider outage or an authentication barrier. Local contract inspection is documentation context, not a source-data pull.

## Ledger and usability

Source status enum is exactly `SUCCESS | SAVED_ONLY | MISSING | LOGIN_REQUIRED | STALE | ERROR | NOT_APPLICABLE` (case-sensitive). Each row MUST retain source identity, `fields_retrieved`, season, week, `data_through_timestamp`, `pull_timestamp`, `cutoff_utc`, `source_available_timestamp`, artifact path/SHA-256, fallback, scope and status reason. `NOT_APPLICABLE` additionally requires a non-whitespace `reason` that excludes the scoped dependency honestly. Unknown provenance is null with a field-specific `unknown_reasons` entry; it cannot satisfy SUCCESS. Never fill retrieval timestamps with document creation time or nominal week. Attempt time is separate from pull time.

`SUCCESS` requires scoped retained fields, usable_for_run true, verified as-of eligibility and current freshness. `SAVED_ONLY` means retained bytes without established run usability. `STALE` means evidence fails freshness/scope requirements. `MISSING` means absent evidence; `LOGIN_REQUIRED` requires an observed authentication barrier; `ERROR` records an observed retrieval/processing error. All statuses except SUCCESS have usable_for_run false. Saved or stale evidence cannot be promoted to live success. Never manufacture access attempts, source values, URLs, routes or fields.

**Listed ≠ usable retrieved.** A homepage, HTTP 200, tool listing, installed library, cached filename, account/key presence or earlier inventory does not prove required fields were retrieved. Record partial fields precisely.

Mark `usable_for_run` true only after verifying the artifact and hash, target scope, required field coverage, source availability at or before the cutoff, freshness policy and conflicts. A later pull requires verifiable as-of contents; otherwise `ASOF_UNVERIFIED` blocks use. The schema captures declarations; a local reviewer/validator must check actual bytes, timestamps, required source coverage and cross-record consistency. Schema validity is not source-gate approval.

Fallback is mandatory: state `none`, `blocked`, or an explicit policy referencing another ledger row or a separately labeled model/scenario assumption. A fallback never turns missing charting into observed evidence. Record all skipped scopes and blockers. An irrelevant source may be explicitly excluded with NOT_APPLICABLE and a scoped reason while a narrower projection remains supported, but any claim or effect depending on the missing source/feature is blocked. Gate approval must state the permitted scope, all blocking dependencies and excluded claims. No gate approval may override missingness or authorization.

## Core integration and evidence boundaries

Follow [core_contract.md](../core_contract.md), especially §§2, 4, 7–9. Preserve canonical IDs, cutoff/frozen/generated clocks, input hashes, source discrepancies and provenance. Carry `MISSING`/`UNKNOWN` and null values into feature availability and consumer outputs; neither status means zero. For the supplied TNF evidence: coverage UNKNOWN; routes MISSING; personnel 11/12/13 MISSING; `allows_sim_effect: false` for those unsupported features. Preserve postgame evidence as `EVIDENCE_ONLY_POSTGAME`. No invented coverage assignments, routes, personnel, player joins, source values or measured coefficients. Unsupported quote joins retain `NOLINE` under the core contract; never synthesize missing prices or sides.

Keep scenarios and proxies explicitly labeled. Official film must be reconciled to PBP with actual event references, scope, discrepancies and timestamp provenance before supporting measured claims. Depth charts and targets do not establish routes or personnel.

**Engineering pytest green ≠ projection_ready; synthetic_fixture_ready ≠ live vet-ready.** Both are software verification outcomes only. Live vet-ready status still requires authentic authorized frozen sources, authoritative workflow definitions and reviewed completion evidence. No engineering result promotes the package to projection_ready.

**Engineering unit/regression tests ≠ projection runs.** Synthetic fixtures, schema checks and accounting regression tests verify software behavior; they do not retrieve sources, complete the 15-phase workflow, produce an eligible forecast or establish predictive performance. A test that actually produces a real matchup/prop forecast is a projection run regardless of its command or filename, and this gate applies. Report engineering checks and projection execution separately.

**TNF is not holdout validation by fitting.** Fitting, selecting, tuning or replaying against inspected TNF actuals cannot establish untouched holdout performance. Preserve split lineage and pre-cutoff freeze evidence. TNF actuals are inspected postgame evidence; no relabeling as untouched holdout, invented canonical ID, accuracy or fit numbers.

## File-backed readiness entry point

Run `python source_run_gate/readiness.py /path/to/run/manifest.json`. Exit 1 is red; exit 0 requires the complete artifact contract. Runtime dependencies are local Python, jsonschema and (for regressions) pytest; this package performs no installations or retrieval.

A run manifest must explicitly request projection_ready, use validation_basis `full_source_run`, declare projection run kind, scope/freeze fields, approved source gate, completed brainstorm and all 15 completed or supported N/A phases. Engineering checks do not set readiness. Infrastructure-only or schema-only validation is never readiness evidence.

readiness.py loads source_ledger.schema.json and validates the run manifest with local jsonschema Draft202012Validator and FormatChecker before artifact checks. The source_ledger array references $defs/ledger_row, so every nested row is schema-validated, including NOT_APPLICABLE reasons. This enforcement predates the Grok follow-up.

The validator checks a populated ledger covering every inventory provider (unique IDs/providers), at least one usable SUCCESS, and explicit N/A reasons for excluded providers. Every SUCCESS must reference hashed, nonempty JSON record arrays with all declared retrieved fields populated; the current entry point supports JSON arrays only. It checks season/week/cutoff agreement, data-through ≤ source availability ≤ cutoff, and pull ≥ source availability. A later pull still requires declared verified as-of contents. Required files stay inside the run directory. Retain nonempty report.md, brainstorm evidence containing `betting-game-brainstorm`, and checklist.md with exactly one checked table row `| [x] | NN | ... |` for each phase 01–15. Completed phase and supplemental evidence paths must exist. Workflow definitions, freshness policy, dependency relevance, source truth and latest approvals still require review; file checks cannot establish those facts.

Synthetic FULL regression fixtures are generated under pytest temporary directories and labeled in records, workflow versions and artifacts. `--synthetic-fixture` permits their engineering acceptance with synthetic_fixture_ready true while projection_ready stays false. Without that flag they fail. Synthetic markers also block relabeling fixtures as live. No test claims actual retrieval or authentic workflow completion.

## Automatic-cut approval alignment

Weather, WR and edge automatic cuts remain **DISABLED**. Approval evidence is `MISSING`: no latest dated approval artifacts authorizing these cuts were supplied or found in the local task materials. Stale rules do not constitute approval. This pass neither applies thresholds nor changes engine effects; resolve dated authorization before a future enablement. Missing coverage/routes/personnel remain unsupported under the core contract.

Every run manifest must explicitly include `automatic_cuts.weather`, `automatic_cuts.WR` and `automatic_cuts.edge`, each with `enabled: false`, non-empty `approval_status` and `reason`. Missing declarations fail schema validation; any enabled cut fails readiness, including synthetic fixture acceptance. Attempting enablement without dated approval evidence is explicitly rejected. This local contract has no automatic enablement path: an approval label or dated prose alone cannot unlock it. Any future enablement requires retained, reviewed, scoped dated approval evidence and a separately reviewed contract/code change. This follow-up supplies neither and leaves every cut DISABLED.

## Scope of this pass

Operational diagnostic extension (2026-11-06): the schema also accepts
`run_kind: diagnostic_evaluation` for retained source audits created after the
event. This kind cannot request projection readiness or completed projection
execution; the existing conditions still require `run_kind: projection` for
either claim. See integration/certified_asof for the separate diagnostic run,
hashed workflow bodies and current evidence. This does not revise historical
scaffold claims or authorize forecast execution, source promotion or cuts.

Saved-byte provenance alignment: SAVED_ONLY may retain a null original
pull_timestamp with its field-specific unknown_reasons entry. This corrects
the earlier schema requirement that forced a string even when the provider
pull instant was unavailable. Local reads and mtimes must never fill that gap.
SUCCESS and STALE still require a pull timestamp; SUCCESS additionally retains
all existing as-of, freshness, populated-artifact and usability requirements.

Local schema/readiness code, templates, regression tests and documentation only. No external APIs, live pulls, paid pulls, spend, auth bypass, heavy simulations, model fitting, cloud jobs or Cursor Cloud. No access or edits to calibration trees; no edits to phase2 CORE possession/period engines. Writes are confined to source_run_gate/ (temporary command helpers under /tmp). IMPLEMENTED describes schema/tests/validator; live retrieval, projection execution and predictive validation remain NOT_RUN. Predictive quality impact is NOT_MEASURED. No false PASS.
