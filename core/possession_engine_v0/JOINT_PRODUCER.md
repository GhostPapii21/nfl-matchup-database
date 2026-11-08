# Frozen opportunity-first CORE producer

`simulate_games` dispatches to `joint_producer.simulate_joint_games` when the config contains `joint_producer`. The original historical yard-row bootstrap remains available for legacy research; its output now explicitly blocks shared-contract projection. Its accounting diagnostic cannot report a full contract PASS.

The new path requires frozen **registry**, **model**, and **splits** JSON inputs. It does not manufacture real-game source inputs from names or historical yard outcomes. Only synthetic fixtures have been executed for this implementation. See `CORE_MANIFEST.json` for implemented components and remaining blockers.

```python
from simulate import simulate_games

# cfg is an explicitly supplied JSON config, with matching outer mode/config_id.
# joint_producer = {spec, input_root, inputs, output_root}
result = simulate_games(cfg, pbp_path="unused_by_joint_path", n=2, seed=123)
```

Use `tests/test_joint_producer.py::fixture_inputs` as the runnable **SYNTHETIC_TEST** format example. Those IDs, distributions, roles and clock costs are test values, never real player evidence. Do not promote them to forecasts. The durable review smoke artifact contains two synthetic draws and all frozen input bytes.

## Input interface

`spec` includes canonical `game`, information `cutoff_utc`, `frozen_at_utc`, `generated_at_utc`, `mode`, `config_id`, and optional `trial_start` and `max_steps`. Each `inputs` entry has a logical input ID, relative path, source, selected record IDs, schema version, usage, source event/publication/retrieval UTC clocks and an as-of evidence reference. Retrieval after cutoff requires `asof_verified: true` and evidence. This validates supplied evidence declarations; it cannot authenticate an arbitrary source's assertion. Real-data source certification is a handoff blocker.

The registry retains authoritative, namespaced strings and crosswalk evidence, including zero padding. It includes canonical game metadata, the versioned team alias map, player roster records and entity-scoped crosswalk rows. Null player identities require `identity_status: UNRESOLVED`; they feed unassigned buckets, never named projections.

The model contains explicit version/provenance/sample-size metadata and market lineage, joint trial role states (availability, depth-chart state, rotation weights and intended target-depth distributions), a shared environment distribution, pre-snap usage cells, catch distributions, outcome cells and try-point distributions. Every distribution is a list of `{value, weight}` rows. Cells are evaluated in supplied order and have explicit IDs; `when` keys compare the shared state using exact matches or `_min`/`_max` bounds. There is no silent league/player/role fallback. If all eligible identities are unavailable, allocation is unassigned. Referenced role weights and distributions remain in the decision trace.

The supported terminal categories are targeted and non-dropback targeted passes, throwaways, spikes, other untargeted attempts, sacks, scrambles, aborted dropbacks without attempts, designed rushes, kneels, credited aborted rushes, no-play, punts, field goals, and explicit period-end runoff. Direct-snap/end-around/QB rush design is an orthogonal label; non-QB throws use the supplied passer identity. Unsupported penalty, untimed-down and defensive-return effects reject execution. Punt/FG/try credits are identified as separate stat ledgers. No betting or settlement profile is defined here.

Per snap: sample usage/terminal category and eligible identities; **increment TARGETS/CARRIES and attempt counts**; draw catch/interception; draw conditional yards/field advancement; apply state changes. The tests intercept the actual outcome call and verify that opportunity counters already exist. Stages retain model/version/source references, sample-size evidence and MODELED flags. Intended depth and depth-chart uncertainty are separate from missing charted routes/personnel/coverage.

Counts and stat yards use exact integers. Ordinary modeled gains stop at the goal line, recorded in the yard trace. Explicit lateral/provider/fumble differences retain separate field advancement, signed adjustments, explanations and event references; failed conservation marks INVALID without redistribution. Unknown identities retain visible unassigned counts and yards and conservatively block the trial's adapter projection.

## Output and replay

One JSONL row is one joint game draw. No marginal resampling or period-engine merge occurs. Every trial includes the full contract object set, ledger-derived primitive/aggregate team and player rows (including rostered known zeros), all terminal counts/residuals, scores, possessions, stages and missing-feature records. Coverage stays UNKNOWN; routes and personnel 11/12/13 stay MISSING, with null values and effects disabled on every event. The TNF audit is referenced only as contract evidence, not loaded into predictive inputs.

Q1–Q4 clocks use 900 seconds each; possession persists over Q1/Q2 and Q3/Q4, with explicit halftime receiving transition. Costs are capped at the current period, with no clock debt. Explicit runoff is supported as a separate transition event. Linked tries stay in the snap's period at 0:00. The only supported OT profile is the existing **single_possession_approx_declared_limitation**, frozen with its duration/termination/entitlement limitations. Consumers requiring official OT must block this profile. Unplayed OT is known zero; cap-limited future/unfinished aggregates are null/INCOMPLETE, never invented zeros.

Canonical UTF-8 JSON uses sorted keys, compact separators, `ensure_ascii=False`, and rejects nonfinite numbers (`python-json-sorted-compact-utf8-v1`). Wire count/yard values are integers; finite model weights may be fractional. Input manifests sort by logical ID and hash exact file bytes. Run hashes include model settings, cutoff, mode, seed policy, trial range, full commit and dirty/source hashes, dependency/RNG versions and profiles. Creation clocks are excluded from forecast identity and recorded separately. Changed input bytes/cutoff/mode create a new identity. Quote snapshots never enter independent forecasts.

Trial seeds follow contract §2.3 with derivation label `sha256-first-eight-big-endian-v1`, lossless decimal strings and PCG64/NumPy version. Trial order/retries cannot change draws. Batch extension changes the forecast ID while preserving overlapping trial seeds/draws. Code and dependency mismatches or mutation of prepared input bytes block execution.

`output_root/<forecast_digest>/` retains `run_spec.json`, `input_manifest.json`, exact input bytes, exact source snapshot and hash manifest, `trials.jsonl`, and `forecast_ledger.json`. Existing bytes are immutable: differing retry output raises a conflict. The writer checks the exact ordered trial population and recomputes validation, never trusting a caller-supplied PASS. The ledger records input/split/artifact hashes, trial IDs and separate empty result-evidence IDs. New information revisions have new identities. The writer stores invalid/incomplete trials, exposes their counts and explicit exclusions, and never silently conditions the population.

Independent data_only/script_adjusted reject market inputs, market-tainted lineage and postgame evidence. Scenario-only models remain explicitly flagged and block actionable projection. Split IDs are either frozen/disjoint or explicitly UNASSIGNED; UNASSIGNED blocks split-dependent claims. Game-level splits apply to every period/player/trial row through the forecast freeze; no trials are independent evaluation examples.

## Remaining work

Real canonical registry/crosswalk verification, certified as-of source bundles and sourced role/outcome tables are **BLOCKED** pending supplied inputs. No TNF inputs were fitted or used for validation. Official OT, penalty/untimed-play rules, defensive/special-teams returns, raw-PBP classification ingestion and both consumer integrations remain **UNIMPLEMENTED**. Consumers must explicitly check supported stat/period/OT profiles and retained IDs; `adapter_projection_allowed` does not certify quote compatibility. No quote matching or settlement changes are part of this producer.

Testing is plumbing/accounting evidence only. Predictive impact: **NOT MEASURED**. Ghost final vet and external independent review remain outstanding.
