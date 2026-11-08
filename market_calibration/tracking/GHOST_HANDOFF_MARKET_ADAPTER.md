# Ghost handoff — BetGuru market adapter

2026-11-06. Worktree `/workspace/wt-market-calibration`, branch
`betguru-market-calibration-2026-11-06`, base HEAD
`3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6`. Market files are untracked working
files; HEAD alone does not identify them. Retain reviewed file/patch hashes.

The adapter transports existing shared scores for research. It runs no simulator,
acquires no odds and fits no Bias. Current outputs are nonactionable NOLINE.
Core binding: schema 1.0.0, SHA-256
`6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`.
Binding authorized by
[CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md](/workspace/research/nfl_sim_integration_2026-11-06/integration/wire/CONTRACT_BINDING_AUTHORIZATION_2026-11-06.md)
for the additive documentation pointer only; content semantics remain v1.0.0.
A changed/missing contract makes transport raise pending realignment.

B01 native producer-wire interpretation is specified in
[WIRE_AGREEMENT_v1.0.1.md](WIRE_AGREEMENT_v1.0.1.md), agreement ID
`market-producer-wire-v1.0.1`. Wire version remains `1.0.0-producer` and content
contract version remains `1.0.0`. See
[binding completion review](../reviews/BINDING_REBIND_COMPLETION.md) for current
official reruns and immutable-example evidence. The
[B01 completion review](../reviews/B01_WIRE_FIX_COMPLETION.md) and verification counts below are
prior evidence, not a new Ghost acceptance claim.

## Calling the existing adapter

Run from the worktree root with bytecode disabled. The following illustrates a
consumer call with **already retained producer objects**, not a projection run:

```python
from research.market_calibration.joint_trial_adapter import adapt_joint_trials

# Supply Ghost's independently retained ordered IDs, not a list reconstructed
# from a possibly truncated market-side subset.
transported = adapt_joint_trials(blitz_joint_rows, expected_trial_ids=ghost_trial_ids)
assert [t.trial_id for t in transported] == list(ghost_trial_ids)

for t in transported:
    # Each is a (home_points, away_points) tuple from this same trial.
    h1 = t.scorecard.points("H1")
    h2 = t.scorecard.points("H2")
    regulation = t.scorecard.points("REG")
    full_game = t.scorecard.points("FG")
    # Retain t.trial_id, t.forecast_id, t.seed, t.trial_seed,
    # t.trial_index, t.input_content_hash and t.source with all derived values.
    assert t.interface_status == "CONTRACT_SCORE_TRANSPORT_ONLY"
    assert t.actionable_status == "NOLINE"
```

The function rejects the whole batch on invalid/incomplete/duplicate rows or
population/order mismatch; it does not filter, reorder, redraw or repair trials.
Keep the rejected source batch and reason. Never discard failed rows and reuse
the full population label. `expected_trial_ids` is optional in the library but
required by this integration procedure. No player target/carry API is supplied.

## Required Blitz joint-trial fields

| Object | Fields/semantics required for this call |
| --- | --- |
| Top level | `contract_version="1.0.0"`, `forecast_id` as `sha256:<64 lowercase hex>`, `trial_id="<forecast_id>/trial/<trial_index>"`, integer nonnegative `trial_index`; `status` object with `state="COMPLETE"`, `completion_reason`, `terminal_state`, Boolean `went_ot`. Legacy scalar COMPLETE with sibling fields is accepted; duplicate sibling declarations must agree. |
| `game` | Nonempty `game_id`, `game_id_namespace`, `home_team_id`, `away_team_id`, `crosswalk_ref`; `season`, `season_type`, `week`, `kickoff_utc`. IDs must actually come from the verified canonical registry, although this transport only checks part of that declaration. |
| `freeze` | `cutoff_utc`, `frozen_at_utc`, `generated_at_utc`, `input_content_hash`, `input_manifest_ref`, `input_manifest_digest` (or legacy `input_manifest_hash`; both must agree), `mode`, `config_id`, `split_manifest_id`, `split_manifest_hash`. Hashes use `sha256:` prefix; clocks end in Z, cutoff ≤ frozen ≤ generated, cutoff < kickoff. Mode is data_only/script_adjusted/market_informed and must stay distinct downstream. |
| `engine` | `engine_version`, `component_version` (or `component_versions`), `dependencies` (or equal `dependency_versions`), nonempty `ot_rule_profile`, `stat_credit_profile`, `limitations`; retain dirty-patch hash where applicable. |
| `rng` | Lossless nonnegative decimal-string `seed` and `trial_seed`; `rng_algorithm`, `rng_version`, `seed_derivation_version`. Trial seed is independently recomputed per core §2.3. |
| `team_periods` | Inline list with exactly one `(team_id, period_id)` per team per Q1–Q4; nonnegative integer `stats.points` (or legacy `points`; both must agree). OT1…OTn must be contiguous, have both teams, agree with `status.went_ot`, and require regulation tie. Known no OT means no OT rows plus went_ot=false; even known-zero primitive OT rows with false are rejected, never silently dropped. Core additionally requires all accounting fields; this score adapter does not validate them. |
| Missingness | `feature_availability` includes coverage, routes, personnel_11/12/13 with status/value/allows_sim_effect. UNKNOWN/MISSING/UNSUPPORTED require null value and false effect. TNF defaults are coverage UNKNOWN, others MISSING. |
| Opaque retained payloads | `latent_state`, `events`, `possessions`, `player_periods`, `aggregates`, `provenance`, `flags`, `validation` are required and copied, not fully accepted/verified by this adapter. Core-valid production payloads must satisfy their complete schema and invariants independently. |

All rows must be finite JSON-compatible data and share forecast/game/freeze/engine
and base RNG metadata. `JointTrial.source` is an unchanged deep copy, including
nested status, engine declarations, scores and producer blockers. H1/H2/REG/FG derive
from the primitive scores, never independently simulated marginals. Full event,
clock, opportunity-before-yard, accounting, forecast-hash and manifest/crosswalk
acceptance remain Blitz producer responsibilities and NOT_RUN here.

## SAVED_ONLY quotes

`load_saved_quotes()` reads exactly:

1. `/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds/odds_jaxbal_game.csv`
2. `/workspace/nfl-database/live/2026-11-05_JAX_BAL/period_q1_q2_q3_fd_dk_cleared.csv`
3. `/workspace/nfl-database/live/2026-11-05_JAX_BAL/period_line_grades.csv`

Referenced `source_file` values are provenance, not additional file opens.
Do not pull replacements. Freeze actual bytes/hashes and preserve row numbers,
raw quote fields, original timestamps, snapshot IDs and sources. Saved scores
and grades are hindsight evidence only; the quote loader excludes them.

Call `match_quote(saved_quotes, MatchRequest(...))` only for an exact saved market
identity. Requests require game, book, market, period, side, signed line (or null
for a lineless winner market), settlement, cutoff/as-of, and team for team totals.
Optional exact retrieval/update/timing fields narrow selection. The earlier
cutoff/as-of applies to both clocks. Opposite spread lines are complementary;
totals share a line; all three winner outcomes are required for three-way markets.
Snapshot IDs now participate in pairing. Research `status="MATCHED"` means a
complete saved pair; use `actionable_status`, which remains NOLINE. Exceptions
and IDENTITY_BLOCKED must also become nonactionable NOLINE at any future external
contract envelope, with the specific reason retained.

Do not call the audit CLI as part of review-only integration: it writes the
artifact directory. `build_saved_audit()` can be used read-only in memory. The
persisted audit currently needs owner regeneration after the independent fix:
76 pair-ID references change, while probabilities/grades/counts remain identical.

## Blockers and gate ownership

- **Crosswalk:** `401873037` is a saved source-event alias, not an asserted
  canonical ID. No frozen canonical game/team/player crosswalk exists here. Do
  not mutate a canonical trial ID to force it through the JAX/BAL-specific
  settlement helper. Add verified consumer mapping in a separately authorized
  integration change, retaining both namespaces and original rows.
- **Rules:** `book_rules_verified=false`; tie/push/participation/void rules and
  quote-specific OT inclusion lack verified source references. Score-convention
  PASS is not sportsbook verification. Current research rows do not supply every
  core §8 stat/unit/subject/price-format/rule field needed for compatibility.
- **Pinnacle Q2–Q4 spreads:** no saved rows; NOLINE. No borrowed Q1 line/price or
  opposite book side. The audit's -2.5 request is an absence probe only.
- **Bias:** UNIMPLEMENTED_NO_FITTED_CALIB, coefficients null. No fitted forecast,
  no default weight, no performance or ROI claim. Raw and pending anchors must
  stay separate; weights are caller-proposed research arithmetic only.
- **TNF/splits:** 2026 W1–8 and inspected JAX/BAL remain development_inspected.
  No fit/selection against TNF actuals or untouched-holdout relabeling. Verify
  alias-wide split membership and immutable forecasts externally; preserve TNF
  actual evidence as EVIDENCE_ONLY_POSTGAME.
- **Missingness:** no coverage assignments, routes, personnel counts, defenders
  or player opportunities may be invented to satisfy producer fields.
- **Run gate:** Blitz owns entrypoint/manifest enforcement. Use the existing
  `source_run_gate/readiness.py` described in REQUIREMENT.md v1.1.0 after the
  approved source inventory, betting-game-brainstorm and all 15 authoritative
  workflow phases. Retain checklist/report/ledger/frozen artifacts. This adapter
  cooperates through retained provenance and blockers; it does not duplicate or
  automatically execute the gate. Saved quotes are SAVED_ONLY, usable_for_run
  false until the authoritative process establishes permitted use. Synthetic
  engineering tests do not authorize a projection or satisfy the workflow.

## Verification available to Ghost

Required suite: **97 passed in 0.21s**. Independent false-PASS regression suite:
**11 failed before fixes → 11 passed in 0.03s**. Combined: **108 passed in 0.16s**.
The independent tests reside under `reviews/`, so the ordinary tests-only command
does not collect them; use the combined command in the evidence JSON for both.
These are engineering counts only. No network requests or simulations ran.
See `../reviews/INDEPENDENT_CODEX_REVIEW.md` and its JSON evidence for exact CLI,
limitations and the two narrowly authorized production fixes.

## P2 audit regeneration closed — 2026-11-06

The owner regeneration required above is complete; this note supersedes the
earlier pending-regeneration statement. P2 is CLOSED. Prior bytes are retained in
`../artifacts/saved_quote_audit.pre_snapshot_fix_2026-11-06.json` with SHA-256
`3d1ff2defa75b964b99278640429c1d21ff5b69fb635a144bec360073399cb89`. The regenerated
`../artifacts/saved_quote_audit.json` has SHA-256
`a376a9ff4d445fce2b40964e27a0d72dfadb5d38eb53ca97d6e019f78a7f5e76`. Exactly 76
`pair_id` leaf values changed; all other values are identical. The new persisted
audit regression failed before regeneration and passes afterward. Requested
combined suite: **109 passed in 0.17s**. Network: 0; simulations: 0.
See `../reviews/AUDIT_REGEN_COMPLETION.md` and
`../reviews/codex_audit_regen_evidence.json`. Research and NOLINE restrictions
remain in force.


## Parent verify post-rebind (Grok independent, 2026-11-06 07:11 ET)

Independent re-runs after Codex authorized rebind (no override/remap):

| Suite | Result | Log |
| --- | --- | --- |
| market suite | **179 passed** (0.31s) | `reviews/pytest_parent_verify_market_post_rebind.txt` |
| DIRECT B01 | **1 passed** (0.21s) | `reviews/pytest_parent_verify_direct_post_rebind.txt` |
| binding local | **6 passed** (0.06s) | `reviews/pytest_parent_verify_binding_local.txt` |

Bound contract SHA-256 (full):
`6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367`
(live file match; MANIFEST match; adapter `CONTRACT_SHA256` match).

Immutable example SHA-256:
`50be826a2bc1cf67db052aa8095ae0d7b3e75d674ef31c65165a5fbe3c881cdd` (unchanged).

Wire: `1.0.0-producer`. Agreement: `market-producer-wire-v1.0.1`.
Actionable: **NOLINE**. Bias: **UNIMPLEMENTED_NO_FITTED_CALIB**.
Full CORE acceptance: **NOT_RUN**. Ghost final acceptance: **NOT_CLAIMED**.
Source readiness: **false** (NOLINE / Bias unfitted). No forecast acceptance implied.
Network: 0. Sims: 0.

Residual (outside market rebind scope): integration adversarial suite still has
stale SHA / inventory mismatches (see `integration/wire/PARENT_VERIFY_POST_REBIND.json`);
DIRECT transport itself is GREEN.


## ≥40pp anomaly delivery guard (2026-11-06 parent verify)

Rico t367u / market-side `delivery_guard.guard_edge_delivery`.
Threshold `ANOMALY_EDGE_PP_THRESHOLD = 0.40`. Quarantine status `DIAGNOSTIC_ANOMALY`.
Reasons: `ID_CHECK` / `UNITS_CHECK` / `PRICE_TIME_CHECK` / `CALIBRATION_CHECK` / `EDGE_GAP_GE_40PP`.
Raw preserved; no shrink/anchor hide; actionable **NOLINE**; Bias **UNIMPLEMENTED_NO_FITTED_CALIB**.

| Check | Result |
| --- | --- |
| Codex market suite | **235 passed** (`pytest_anomaly_guard_market_suite.txt`) |
| Parent Grok market+independent | **246 passed** (`pytest_parent_verify_anomaly_guard.txt`) |
| Guard unit tests collected | **67** |
| Contract SHA | `6471e69b97b19b85ce0a4b8e4c25117b0e40ceefa1a225ee06d7c1b7440e8367` preserved |
| Example | `50be826a…1cdd` preserved |

Quote recovery (authorized saved only): loader **132** records; pairing probe **MATCHED 60** research pairs; Pin Q2–Q4 spreads **NOLINE**; Firecrawl Pin ERROR; Odds API no spend.
Calibration data sufficiency for package Bias.fit: **false** (legacy holdout 1230 exists but not package Provenance train rows).
Ghost final: **NOT_CLAIMED**. Forecast acceptance: **false**. Impact: **NOT_MEASURED**.
Packet files: `reviews/ANOMALY_DELIVERY_GUARD_COMPLETION.md`, `reviews/codex_anomaly_guard_evidence.json`, `reviews/QUOTE_EXTRACTION_INVENTORY_2026-11-06.json`, `reviews/CALIBRATION_DATA_SUFFICIENCY_2026-11-06.json`, `reviews/GHOST_INDEPENDENT_PACKET_ANOMALY_GUARD_2026-11-06.json`.
Parent verify ET: 2026-11-06 07:25:31 ET.
