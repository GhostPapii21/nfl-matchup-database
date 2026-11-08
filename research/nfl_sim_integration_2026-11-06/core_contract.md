# NFL shared simulation integration contract — phase 1

Contract ID: `nfl-sim-core-contract-v1`  
Schema version: `1.0.0`  
Producer export wire: [`1.0.0-producer`](core_contract_wire_v1.md), frozen example and field-name lock.  
Authored: 2026-11-06 (UTC)  
Coordination: Ghost6 simulation producer; Ghost6 and BetGuru consumer adapters. These are interface responsibilities, not evidence of approval or implementation by either party.

This document defines the required future integration interface: **one trial is one coherent full-game draw**, shared by both adapters. Phase 1 writes documentation only. Requirements below are normative (`MUST`/`MUST NOT`); they do not claim the existing engines satisfy them. No simulations, TNF fitting, calibration, odds acquisition, or betting-rule changes are part of this phase.

The companion `core_contract.checklist.json` indexes the requirements and future acceptance checks. A requirement marked defined means the contract covers it; implementation and runtime verification remain `NOT_RUN`.

## 1. Read-only context and known limitations

Source tree inspected: `/workspace/wt-nfl-sim-core-2026-11-06`, branch `research-nfl-sim-core-2026-11-06`, HEAD `3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6`.

Local references:

- `research/possession_engine_v0/README.md`, `state.py`, `simulate.py`, `validation/accounting.py`, `effects/missing_feature_adapters.py`, and `config/jax_bal_tnf_2026-11-05_data_only.json`.
- `research/period_engine_v0/README.md`, `reconstruct.py`, `monte_carlo.py`, `market.py`, `settlement.py`, and `PLAYER_EVIDENCE_SPEC.md`.
- Evidence only: `/workspace/nfl-database/live/2026-11-05_JAX_BAL/actual_role_coverage_audit.md`.

The possession engine currently bootstraps historical outcomes and credits player yards using names; it exports period score arrays and player-yard samples. That is not evidence of stable player IDs, opportunity-first generation, or complete attempt conservation. Its `game_seconds_remaining` state variable is actually the current period clock. Its declared OT profile is `single_possession_approx_declared_limitation`; it must not be represented as a verified current official OT implementation. The period engine has a separate team-quarter bootstrap; its independent draws cannot be combined with possession-engine player draws and called one joint trial.

The TNF audit states **coverage UNKNOWN; routes MISSING; 11/12/13 personnel MISSING** and retains a receiving-yard source discrepancy. It is postgame evidence, not a pregame model input. No TNF fit, accuracy, or calibration numbers are asserted here. The inspected data-only config labels W1–8 as inspected development data and contains multiple provenance timestamps; a filename or nominal freeze timestamp alone does not establish a valid frozen forecast.

## 2. Stable identity, cutoff, and reproducibility

### 2.1 Identity conventions

| Field | Required convention |
| --- | --- |
| `game_id` | Opaque, case-sensitive canonical ID from the frozen schedule/PBP registry, with `game_id_namespace` (for example `nflverse`). Preserve source bytes, including zero padding. A date/matchup label is not a canonical ID. |
| Game metadata | `season`, `season_type`, `week`, `home_team_id`, `away_team_id`, scheduled `kickoff_utc`; canonical team namespace and a frozen alias map. These validate identity rather than replace it. |
| `player_id` | Opaque authoritative ID plus `player_id_namespace` (prefer GSIS when available). Never derive an ID from a display name, jersey, depth slot, or team. Identity persists through team changes. |
| Crosswalk | Versioned, hashed rows `(source_namespace, source_id, canonical_namespace, canonical_id, evidence_ref)`; unique within the relevant entity/scope. Preserve external event IDs as aliases. No guessed event or player joins. |
| `trial_index` | Zero-based nonnegative integer, assigned before dispatch and stable under retries or parallel execution. |
| `forecast_id` | `sha256:` plus the digest of the canonical frozen run specification described below. Changing any modeling input, version, seed policy, or cutoff creates a new ID. |
| `trial_id` | Exact string `<forecast_id>/trial/<trial_index>`. Unique across forecasts; array position alone is not an ID. |
| `event_id`, `possession_id` | Unique and ordered within `trial_id`; event IDs include all transitions, not only stat-bearing snaps. Possessions may span quarters and reference multiple period segments. |

An unresolved real player has `player_id: null`, an identity flag, and a separate unassigned accounting bucket. Never create a fake named player to force reconciliation. Ambiguous or conflicting crosswalks block the affected player projection/quote join. Missing canonical game identity blocks the whole shared-trial export. Display names remain optional presentation metadata.

### 2.2 Frozen inputs and clocks of observation

Every forecast MUST carry:

- `cutoff_utc`, an explicit RFC 3339 UTC instant ending in `Z`, such as the format `YYYY-MM-DDTHH:MM:SSZ`. This is the information cutoff, not document creation or simulation execution time.
- `frozen_at_utc` and `generated_at_utc`, separately recorded. All input observations must have been available by `cutoff_utc`; record source event time, source publication/availability time, and retrieval time. A later extraction of earlier data requires verifiable as-of contents or an `ASOF_UNVERIFIED` block, not an assumed pregame freeze.
- `engine_version` (full code commit plus component versions), `contract_version`, dependency/RNG versions, `config_id`, and `mode` (`data_only`, `script_adjusted`, or `market_informed`). Dirty code requires its patch content hash; a clean commit alone cannot identify uncommitted code. Keep modes distinct.
- A frozen input manifest listing logical input ID, source, selected record IDs, byte size, SHA-256 digest, schema version, timestamp evidence, and intended use for every consumed input. Include history selections, roster/crosswalk, availability/depth/rotation distributions, config/effect tables, fallback policies, split manifest, and any permitted scenario input. Preserve original timestamp strings and normalized UTC.

`input_content_hash` is `sha256:` plus SHA-256 of the canonical manifest, whose entries are sorted by logical input ID and include the SHA-256 of each frozen file's exact bytes. Use UTF-8 canonical JSON: sorted object keys, compact separators, no NaN/Infinity, no ambiguous numeric encodings; specify serializer version. Use logical relative paths rather than mutable absolute paths. Hash exclusions must be listed; creation times and self-hash fields are excluded from the hash they would otherwise recursively define. Hashes establish identity, not as-of eligibility.

The canonical run specification includes `input_content_hash`, cutoff, canonical game identity, engine/dependency/contract versions, mode/config, OT/stat profiles, ordered trial-index range, and RNG specification. Its digest defines `forecast_id`. Quote snapshots are separately frozen and hashed by the adapter; a changed quote does not regenerate a data-only model forecast. If market data enters a `market_informed` model, that snapshot belongs in its input manifest and changes its forecast ID.

### 2.3 Seeds

Record `seed` as the nonnegative base seed in a lossless decimal string, `rng_algorithm`, `rng_version`, and `seed_derivation_version`. For the shared interface, derive each `trial_seed` as the unsigned big-endian integer in the first eight SHA-256 bytes of the canonical JSON array `[seed_derivation_version, seed, game_id_namespace, game_id, input_content_hash, trial_index]`; encode that integer as a decimal string. Hash the UTF-8 serialization using the canonicalization above. Record the resulting seed on the trial. Any named substreams use the same documented derivation with an additional stream label and draw scope; never use process-randomized `hash()` or worker order.

The existing `stable_seed(base, week, game_id)` helpers are legacy context, not proof of compliance with this future per-trial scheme. Replaying a trial requires the same frozen run specification and runtime/RNG version. Extending a batch creates a new forecast specification but must preserve overlapping trial draws when their derivation inputs are unchanged. Adapters must never reseed or independently resample player and team marginals.

## 3. Clock, period, possession, and score boundaries

Regulation consists of Q1–Q4, each 900 game-clock seconds, totaling 3,600. Use explicit `period_id` values `Q1`–`Q4`, then `OT1`, `OT2`, etc., and `period_kind: REG|OT`. `period_seconds_remaining` is never mislabeled as whole-game time. In regulation, `regulation_seconds_remaining = (4 - quarter_number) * 900 + period_seconds_remaining`; after regulation it is zero, with OT clocks stored separately. Wall-clock timestamps, play clock, and game clock are separate quantities.

For each event record `period_id`, `event_seq`, pre/post period clock, elapsed clock seconds, pre/post possession, and pre/post state. Clock bounds are `[0, period_length_seconds]`; elapsed clock is nonnegative and exactly reconciles the clock transition within a period. Stopped-clock events may have zero elapsed time and are ordered by sequence. Period-end residual runoff must be explicit. No negative clock debt may silently carry into the next quarter. Record halftime and OT resets as boundary events rather than elapsed play time.

A snap belongs to the period in which it starts. A play that legally finishes at an expiring clock, an untimed down, or an associated try is assigned by a versioned event/period attribution profile, not a timestamp-only bucket. Boundary events occur after required linked events complete; no event or score is counted twice at 0:00. Q1→Q2 and Q3→Q4 do not themselves force a new possession. Halftime has an explicit receiving-team transition. Punt, turnover, downs, score, kickoff/free kick, and finalization transitions have explicit causes; model limitations remain flags.

OT is separate from regulation and entered only after a regulation tie under the selected game rule profile. The frozen `ot_rule_profile` MUST specify period duration, possession entitlement, termination/tie behavior, season/game-type applicability, and limitations. Preserve the current approximation label on legacy runs; do not silently replace it or claim official-rule correctness. Missing or incompatible OT semantics block any consumer requiring them. A safety cap or `final_max_steps` termination is `INCOMPLETE`, not a valid full-game draw. Do not fill the remainder with invented zeros. OT that was not played has known zero totals, not MISSING totals.

For each team and every additive player/team stat, derive all aggregates from the same event ledger:

```text
H1  = Q1 + Q2
H2  = Q3 + Q4                         # regulation only
REG = H1 + H2
OT  = sum(OT1, OT2, ...)
FG  = REG + OT
```

Score credits include offense, defense, and special teams; team points are not assumed to equal player offensive points. Possession segments partition game-clock consumption with explicit unattributed/boundary time; the two teams cannot each consume the same elapsed seconds. In a complete regulation draw, all consumed and explicit runoff seconds sum to 3,600. OT reconciles only played OT time. Player credits belong to the player's team on that event. Player/team period totals, possessions, turnovers, field position, and final scores must reconcile; a possession clock cannot continue after its terminating event.

## 4. Opportunity-first generation and provenance

Player TARGETS and CARRIES are opportunity counts, generated before their associated yards.

The required causal order is:

1. Freeze eligible roster, identity mapping, information cutoff, model settings, and sourced pregame role distributions. Draw trial-level availability, depth, rotation, and shared game environment uncertainty from those frozen distributions.
2. At each pre-snap state, draw usage/play intent conditional on score, clock, possession, down/distance, field position, and the trial's available players and rotation. Target-depth uncertainty means a sourced or explicitly modeled intended-depth distribution; it never means invented routes or charted coverage. Depth-chart uncertainty is recorded separately.
3. **Generate the player TARGET or CARRY assignment and increment its opportunity count BEFORE generating its associated yards.** For pass intent, first resolve mutually exclusive sack/scramble/attempt outcomes; a targeted attempt selects an eligible receiver and increments TARGETS before catch/yard draws. A rush outcome selects the carrier and increments CARRIES before rush-yard generation. Non-target attempts have no player target; scrambles/kneels follow the accounting profile below.
4. Draw catch/incompletion/interception and then associated yards/turnover/scoring outcomes conditional on the allocated opportunity and shared state. Apply bounded field-position and stat-credit transitions, update state, and repeat. Subsequent usage may respond to earlier realized outcomes.
5. Sum realized opportunities and credits from the ledger to obtain full-game counts and yards. If game-level usage budgets are drawn, record them as latent budgets and reconcile them to actual opportunities; unused budgets are not credited targets/carries.

This order is causal per opportunity; it does not freeze future game state before the game is simulated. Targets/carries MUST NOT be inferred by dividing sampled yards by an average, assigned after yard totals, or independently sampled without team reconciliation. Historical player-yard row sampling is not by itself opportunity-first generation. Catch counts cannot be drawn independently of available targets.

Each role/usage/yard decision carries `provenance_refs`, `generation_stage`, distribution/model version, sample size if known, and flags from `SOURCED`, `MODELED`, `PROXY`, `SPARSE`, `FALLBACK`, `SCENARIO_ONLY`, `MISSING`, `UNKNOWN`. A simulated draw is `MODELED`, never an observed fact. Missing sample sizes are null with a reason. Record depth/rotation changes, uncertainty states and conditional weights; unsupported role assumptions remain explicit. A depth-chart role is not evidence of measured route participation or 11/12/13 personnel. Scenarios remain separately identified and cannot be promoted to fitted/measured evidence.

## 5. Team attempt and player accounting conservation

Use nonnegative integer opportunity counts and signed finite yards. Apply a frozen `stat_credit_profile` identifying provider definitions and version. Every counted snap has one terminal classification plus orthogonal flags for penalties, turnovers, lateral credits, and stat eligibility. Nullified/no-play snaps consume no official attempts, targets, catches, carries, or yards unless the selected profile explicitly credits a surviving component. Tries, special teams, and return yards are separate ledgers; they are not ordinary offensive attempts.

For each team, trial, and period, the following quantities and equations MUST be exposed. Categories on each right-hand side are mutually exclusive:

```text
dropbacks = dropback_pass_attempts + sacks + scrambles + aborted_dropbacks_no_attempt
pass_attempts = dropback_pass_attempts + non_dropback_pass_attempts
pass_attempts = eligible_target_attempts + throwaways + spikes + other_untargeted_attempts
eligible_target_attempts = sum(player.targets) + unassigned_targets
completions = sum(player.catches) + unassigned_catches
0 <= player.catches <= player.targets
0 <= unassigned_catches <= unassigned_targets
completions <= eligible_target_attempts <= pass_attempts

rush_attempts = designed_rushes + scrambles + kneels + credited_aborted_rushes
rush_attempts = sum(player.carries) + unassigned_carries
```

`dropbacks` is the pass-intent count under this contract. `non_dropback_pass_attempts` separately accounts for trick/non-pass-intent throws; do not force a non-QB passer into a QB-only ledger. A dropback scramble contributes once to dropbacks and once to rushing attempts, but zero pass attempts/targets. Sacks contribute zero pass attempts/targets/carries. Kneels contribute to rushing attempts under the declared credit profile and remain separately visible. Spikes are untargeted pass attempts. A target-bearing interception is a targeted attempt with zero catch. An interception without a verified intended receiver remains unassigned; it is not an invented player target. Throwaways never become eligible player targets.

`designed_rushes` includes QB designed runs and non-RB rushes. Direct-snap runs, end-arounds, and aborted snaps require explicit classifications; an aborted snap credited as a rush is not also an `aborted_dropbacks_no_attempt` terminal outcome. Preserve pass intent as an auxiliary flag if needed. The actuals audit's aborted-snap conventions are evidence to retain, not permission to rewrite settlement or silently assume every data provider agrees. Any unsupported residual terminal outcome is separately named and flagged; never hide it in zero or in an unrelated category. The source adapter must map its classifications to this ledger or mark the affected accounting `UNSUPPORTED`.

At team and player levels, expose targeted attempts, catches, attempts by passer, carries by runner, gross passing yards, receiving yards, rushing yards, sack loss, and net passing yards. Require:

```text
team.pass_attempts = sum(player.pass_attempts) + unassigned_pass_attempts
team.sacks = sum(player.sacks_taken) + unassigned_sacks
team.gross_pass_yards = sum(player.pass_yards) + unassigned_pass_yards
team.receiving_yards = sum(player.rec_yards) + unassigned_rec_yards
team.rush_yards = sum(player.rush_yards) + unassigned_rush_yards
team.net_pass_yards = team.gross_pass_yards - team.sack_loss_yards
team.gross_pass_yards = team.receiving_yards + pass_receiving_credit_adjustment
```

Sack loss is stored as nonnegative loss magnitude, distinct from signed net yards. Lateral/fumble/provider stat-credit adjustments must have event references, signed amounts, and explanations; do not change a player's yards merely to force equality. A lateral recipient's yards need not create a catch or target. Keep field advancement and official credited yards separate where penalties/fumbles/laterals require it. Unassigned buckets remain visible and block affected named-player projections; they are not zero or synthetic players. Zero opportunities means known zero opportunity-derived production; unavailable data is null plus a flag.

Validate all equations per trial, per team, per primitive period, and again after aggregation. Integer counts/scores reconcile exactly; yard values use a declared exact integer/fixed-decimal unit, not a permissive floating-point tolerance. Invariant failures produce `INVALID` and suppress adapter projections; never silently clip, redistribute, or discard inconvenient trials. Report requested, complete, incomplete, invalid, and usable counts, exclusions, and conditioning basis. A partial sample must never masquerade as the full forecast.

## 6. Joint trial output schema

The wire format is a versioned JSON-compatible object; JSON Lines may carry one object per trial. Integers are actual integers except lossless seed strings. Numeric values must be finite; optional unknown values are `null` with a status/reason. Required missing keys are schema errors. References may point into a separately frozen run manifest/event artifact only when its hash and exact record keys accompany the trial.

| Required object/key | Type and semantics |
| --- | --- |
| `contract_version`, `forecast_id`, `trial_id`, `trial_index` | Version string; IDs and integer index as defined in §2. |
| `game` | Object with canonical `game_id`, namespace, season/type/week, home/away team IDs, kickoff UTC, crosswalk reference. |
| `freeze` | Object with cutoff/frozen/generated UTC, `input_content_hash`, input manifest reference and digest, mode/config ID, split manifest ID/hash. |
| `engine` | Object with full engine/component/dependency versions, dirty-patch hash if applicable, `ot_rule_profile`, `stat_credit_profile`, limitations. |
| `rng` | Object with `seed`, `trial_seed`, algorithm/version, derivation version, optional substream references. |
| `status` | `COMPLETE`, `INCOMPLETE`, or `INVALID`; completion reason, terminal state, `went_ot`, and validation result references. COMPLETE alone does not mean every consumer field is available. |
| `latent_state` | Sourced/model-labeled availability, depth-chart, rotation, target-depth and shared environment draws, or immutable references to them; no invented charted attributes. |
| `events` | Ordered event rows or a hashed artifact reference. Each row includes event/possession IDs, clocks and period, pre/post state, acting teams/player IDs, opportunity-before-yard stage references, terminal category, stat credits, score delta, flags and provenance. |
| `possessions` | Rows keyed by possession ID and team: start/end events and cause, ordered period segments, clock consumption, yards/points/turnovers with definitions. |
| `team_periods` | Exactly one row per `(team_id, period_id)` for both teams for each played primitive period; includes points, all §5 counts/yards/residuals, stat status/provenance. |
| `player_periods` | Rows unique by `(team_id, player_id_namespace, player_id, period_id)` for rostered identified players, including known zeros. Include targets, catches, carries, pass attempts, sacks taken, pass/rec/rush yards, field statuses/provenance. Unassigned credits are separate team residual rows. |
| `aggregates` | Team and player rows for `H1`, `H2`, `REG`, `OT`, `FG` derived exclusively from primitive periods; score margin and total derived from the same team scores. |
| `feature_availability` | Feature IDs, explicit status/value, evidence scope, source/as-of references, and whether a simulation effect is allowed; required missing features in §7. |
| `provenance`, `flags`, `validation` | Referenced source registry, structured flags with scope/reason, and per-invariant expected/actual/pass results. Absence of a warning is not a passing check. |

A field status is separate from trial completion: an aggregate score can be known while routes are MISSING. Stats unsupported by a producer stay null/UNSUPPORTED, never backfilled with independent draws. Exporting this interface as usable for a named player requires their identity, opportunity and accounting fields to be supported.

Both adapters MUST consume the identical `(forecast_id, game_id, trial_id)` population and retain trial IDs through joins. Ghost6 derives game/team/period/player summaries and diagnostics from these rows. BetGuru projects requested stat/period values from these same rows. No adapter may shuffle trials, redraw totals, multiply marginal probabilities to impersonate a joint draw, or substitute the period engine's independently simulated score. Any consumer-specific exclusion requires an explicit retained-ID list and disclosed conditioning, never an unreported sample change.

## 7. Required missingness and evidence boundaries

The default availability record for the supplied TNF evidence is:

```json
{
  "coverage": {"status": "UNKNOWN", "value": null, "allows_sim_effect": false},
  "routes": {"status": "MISSING", "value": null, "allows_sim_effect": false},
  "personnel_11": {"status": "MISSING", "value": null, "allows_sim_effect": false},
  "personnel_12": {"status": "MISSING", "value": null, "allows_sim_effect": false},
  "personnel_13": {"status": "MISSING", "value": null, "allows_sim_effect": false}
}
```

Attach the audit source reference with `usage: EVIDENCE_ONLY_POSTGAME`, not as a pre-cutoff simulation input. Propagate these statuses to events and adapter evidence displays. UNKNOWN means the attribute is unresolved; MISSING means required measurement is unavailable. Neither means zero. A missing feature may leave an otherwise supported score/stat draw usable, but blocks any claim or effect requiring that feature.

Never infer coverage assignments from tacklers, player names, box scores, an explosive gain, or a highlight. Never infer routes or 11/12/13 package usage from targets, TE catches, depth charts, or nominal positions. Do not fabricate blockers, defenders, H2H sample sizes, source URLs, or measured coefficients. Proxy/scenario flags cannot replace measured availability. Future sourced charting requires verified scope, provenance, as-of eligibility and a new input hash; it does not retroactively repair an earlier freeze. Keep source discrepancies as separate source values with a discrepancy flag and an explicit reconciliation policy.

## 8. BetGuru quote adapter contract

This is a consumer identity/transport interface, not a change to betting selection, settlement, staking, thresholds, or execution rules. It consumes only already supplied, authorized quote snapshots. No new odds requests or spend are authorized.

Each quote row MUST retain:

| Field | Requirement |
| --- | --- |
| `quote_id`, `snapshot_id`, `source_ref`, `source_hash` | Immutable source identity and evidence; preserve raw quote fields alongside normalized fields. |
| `quote_timestamp_utc`, `retrieved_at_utc` | Actual timezone-qualified quote/observation timestamp normalized to UTC and retrieval instant, separately. Preserve raw timestamp/offset. Missing or ambiguous source time is not filled with current time. |
| `book`, `book_market_id` | Canonical book identity and source market ID if supplied; do not invent absent IDs. |
| `game_id`, namespace, `subject_type`, `subject_id`, subject namespace | Exact game/team/player join through frozen crosswalk; subject type is game, team, or player. |
| `stat`, `stat_unit`, `period`, `ot_inclusion` | Versioned stat dictionary, units and exact period scope; `Q2` means standalone Q2, `H2` means regulation Q3+Q4. Quote-specific OT scope must be explicit. |
| `line`, `side`, `price`, `price_format` | Exact source decimal/signed line, side and price. State American/decimal/etc. Null line is allowed only for a genuinely lineless market under its existing definition. |
| `settlement_type`, `settlement_rule_ref` | Existing rule identity, including push/tie, player participation/void and OT provisions. Unknown provisions block compatibility; this contract supplies no replacement rules. |

Pair both sides using the exact same book, game, subject, stat/unit, period/OT scope, settlement definition and snapshot/co-observation identity. Over and under require identical lines. Opposing spread sides require complementary signed lines from the same market/rung; do not compare equal signed values. Lineless two-way winner pairs require opposite teams and identical applicable rules. If source timestamps differ, pairing is allowed only under an already documented consumer co-observation policy; absent such a policy require the same snapshot timestamp. Do not invent a time tolerance or stale-price threshold.

Three-way markets require every outcome, including tie. Never drop tie and renormalize to two sides. Never cross-pair books, alternate lines, players, quarters/halves, or snapshots; never synthesize the missing side, price or quote time. Preserve both original quote IDs and a deterministic `pair_id` derived from their sorted IDs and snapshot hash.

Return adapter status `MATCHED` only when quote identity, both-side completeness (or all three outcomes), timestamps under existing policy, stat support, rule compatibility, and the trial population checks pass. Any missing/ambiguous/unpaired identity, stat, price, timestamp, line, period, OT or settlement compatibility yields **`NOLINE`**, with specific reason codes such as `GAME_ID_MISMATCH`, `PLAYER_ID_UNRESOLVED`, `STAT_UNSUPPORTED`, `PERIOD_MISMATCH`, `LINE_MISMATCH`, `BOOK_MISMATCH`, `PAIR_MISSING`, `QUOTE_TIME_MISSING`, `SNAPSHOT_MISMATCH`, `OT_SCOPE_MISMATCH`, `SETTLEMENT_UNKNOWN`, or `TRIAL_INVALID`.

An output projection includes `forecast_id`, input hash, adapter version, `pair_id`, quote IDs, exact retained trial IDs/count, projected stat/period, raw trial values, and status/reasons. `NOLINE` carries null actionable comparison/edge fields; the raw simulation may remain available for research. Preserve win/lose/push/tie probabilities separately under existing settlement rules. Do not invent a replacement line or promote raw-model disagreement into a betting-rule change.

## 9. Frozen forecasts and calibration split ID policy

This section defines ID bookkeeping only. Do not read, edit, regenerate, or create anything inside `/workspace/wt-market-calibration` or any `market_calibration/` tree. No calibration is performed in phase 1.

Future manifests outside those excluded trees use `split_manifest_id`, manifest content hash, policy/version, `created_at_utc`, and disjoint arrays `train_game_ids`, `dev_game_ids`, `holdout_game_ids`. Entries include game ID namespace; every game appears in at most one split. Related quarters, player rows, duplicate feeds, and all trials/forecasts of the same game inherit the game's split. Trial IDs are not independent calibration examples. Do not invent populated ID lists when the authoritative registry is unavailable; record `UNASSIGNED` and block split-dependent claims.

Freeze membership before model/threshold selection and before holdout inspection. Record which IDs were actually inspected and when. Already inspected W1–8 IDs cannot be relabeled untouched holdout. The supplied TNF actuals are now inspected postgame evidence; exclude that game from any newly claimed untouched holdout. Record its canonical ID only after a verified registry join; retain source event alias `401873037` without asserting a fabricated canonical mapping. No fit or selection on TNF actuals is authorized here.

Train IDs may be used for fitting; dev IDs for selection and diagnostics; untouched holdout IDs only for a locked evaluation after forecast/model freeze. Once inspected for selection, retire that holdout claim and version the policy; do not quietly move IDs. Changing assignments creates a new manifest and dependent forecast/model IDs, with lineage. For walk-forward evaluations, each fold has explicit train/dev/holdout IDs and cutoff; input availability and history must precede the target cutoff, not merely have a lower nominal week. Preserve legacy evaluation provenance rather than retroactively declaring it clean.

Every frozen forecast ledger row references `(forecast_id, game_id, cutoff_utc, engine_version, input_content_hash, mode, split_manifest_id, split_membership, trial_id range/list)`, immutable forecast artifact hashes and later evidence-only result IDs. Post-cutoff corrections create a separately labeled revision; they cannot overwrite the original pregame forecast. Keep result/actual IDs in an evaluation namespace separate from predictive input IDs. No calibration coefficients, fit statistics, ROI or TNF performance numbers are supplied by this contract.

## 10. Integration acceptance checklist

All boxes below are **future acceptance gates, not completed implementation checks**. Contract coverage is complete; runtime status for every gate is `NOT_RUN`.

- [ ] **C01 — Identity:** canonical game/player/team IDs and hashed unambiguous crosswalks; unresolved identities propagate, never guessed.
- [ ] **C02 — Freeze:** cutoff/source availability UTC evidence, complete frozen manifest/content hash, code/config/mode/runtime versions; post-cutoff data blocked.
- [ ] **C03 — Replay:** trial IDs/seeds deterministic across worker order/retries; replay matches the frozen runtime and artifact values.
- [ ] **C04 — Clock:** Q1–Q4/halftime/OT/untimed-play transitions, possession continuity and clock partitions reconcile; cap termination flagged INCOMPLETE.
- [ ] **C05 — Periods:** both teams' scores and additive team/player stats reconcile Q→H→REG→FG, with OT separate and score-credit events complete.
- [ ] **C06 — Generation order:** trace proves targets/carries allocated before associated yards, with shared state/depth/rotation uncertainty and decision provenance.
- [ ] **C07 — Attempts:** dropbacks/attempts/throwaways/spikes/sacks/scrambles/kneels/trick/aborted/no-play categories satisfy §5 without double counting.
- [ ] **C08 — Credits:** eligible targets, catches≤targets, carry totals and all team/player yard/credit adjustments reconcile per trial and period; residuals visible.
- [ ] **C09 — Joint schema:** required typed fields, unique event/period/player keys and equal trial-ID population across Ghost6 and BetGuru; no independent marginal redraws.
- [ ] **C10 — Missingness:** coverage UNKNOWN, routes MISSING, personnel 11/12/13 MISSING preserved end to end; no unsupported measured effects or fabricated assignments.
- [ ] **C11 — Quotes:** quote time/book/stat/period/line/side/price and rule identity preserved; exact both-side/all-outcome pairing; mismatch fixtures return NOLINE.
- [ ] **C12 — Freeze/splits:** versioned disjoint game-ID manifests, inspected-data exclusions and frozen forecast/result separation; no split-dependent claims on UNASSIGNED IDs.
- [ ] **C13 — Scope:** no engine changes in phase 1, no new odds/spend, no betting-rule changes, no fabricated coverage/routes/TNF fit numbers, no Cursor paid cloud, and no excluded-tree access or edits.

Later validation must include boundary plays at quarter expiration, halftime possession changes, OT/no-OT draws, a safety-cap draw, target-bearing interceptions, throwaways, spikes, sacks, scrambles, kneels, non-QB throws, direct snaps, aborted snaps, nullified plays, lateral/fumble credit differences, zero-opportunity and unresolved players, and deliberate quote identity/pairing mismatches. These are required test cases, not a claim that tests were written or run in phase 1.

## 11. Explicit phase-1 exclusions and handoff

Only this Markdown contract and its checklist companion are deliverables. No engine implementation or rerun, parameter fitting, calibration, new data/odds purchases or pulls, spend, betting-rule/settlement-policy changes, bet placement, Cursor Cloud/paid cloud use, fabricated coverage/routes/personnel or TNF fit numbers are authorized. The two existing engine packages and TNF audit are read-only context. The excluded calibration worktree and every `market_calibration/` tree remain untouched.

The later implementation handoff is the acceptance checklist above: producer adds the shared ledger/IDs/opportunity order, adapters consume that ledger with explicit missingness and exact quote identity, and verification supplies evidence for each gate. No gate is marked passed merely because its definition appears in this document.
