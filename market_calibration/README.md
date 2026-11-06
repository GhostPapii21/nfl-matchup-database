# BetGuru saved market and calibration research

Saved-only quote matching, score settlement, an unfitted calibration interface,
and a shared-trial score adapter. No network calls, odds acquisition, simulations,
player targets, defenders, fitted coefficients, or model-performance claims.

The bounded public check is `bash scripts/smoke_offline.sh` from the repository root. It does not run this package.

Saved quote CSVs are not published. `python3 -m market_calibration.audit` stays fail-closed until those files are supplied locally under `market_calibration/saved_quotes/`, and a missing file is not a fitted calibration.

Pytest's local configuration disables its cache. The tests complete in well under
30 seconds. These commands write only inside `research/market_calibration/`.
The existing engine `market.py` and `settlement.py` are imported read-only.

## Saved quotes and identity

`quotes.load_saved_quotes()` reads exactly these three files:

- `/workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds/odds_jaxbal_game.csv`
- `/workspace/nfl-database/live/2026-11-05_JAX_BAL/period_q1_q2_q3_fd_dk_cleared.csv`
- `/workspace/nfl-database/live/2026-11-05_JAX_BAL/period_line_grades.csv`

Only FD/FanDuel, DK/DraftKings, and Pinnacle are accepted. The raw r6 CSV has no
game ID: its known source registration binds it to source-event alias `401873037`
for `2026-11-05_JAX@BAL`. Namespace `saved_csv_game_id` is deliberately separate
from a canonical schedule namespace. No canonical crosswalk is supplied here.
Referenced `source_file` paths are snapshot identities; the loader never opens
additional referenced files. The other two saved files already embed their
quote rows, including earlier r2 and later FD snapshots.

Each quote retains exact raw quote fields (excluding scores, grades and notes),
its input file/hash/row, referenced snapshot, original timestamps, normalized
side and signed line, and a deterministic quote ID. No outcome features enter
quote matching. Source conflicts remain blocked.

`MatchRequest` specifies game, book, market, period, side, signed line,
settlement, team if applicable, information cutoff and evaluation as-of time.
Optional exact quote/retrieval timestamps and line timing further constrain it.
The earlier of cutoff/as-of applies to both observation and retrieval. Timestamps
must include a timezone; ambiguous or absent timestamps raise `ValueError`.
The latest eligible snapshot is selected before line matching. A missing leg in
that snapshot never triggers fallback to an older complete pair.

Both legs must share book, game, subject, market, period, settlement, timing,
snapshot source, retrieval instant and quote-update instant. Spread lines are
complementary signed values; total lines are identical. Equivalent duplicate
rows retain provenance; conflicting prices block comparison. No cross-book,
cross-snapshot, cross-line or cross-period pairing, price synthesis, or made-up
opposite side occurs. Q2–Q4 Pinnacle spreads are absent and return `NOLINE`.

No-vig arithmetic calls `period_engine_v0.market.novig_two_way` or
`novig_three_way`. Every outcome of a three-way market, including Tie, is required.
Saved `h2h` rows carry two team prices, and the research convention is
`ml_2way`; these probabilities exclude pushes. This is not evidence of verified
book tie/void rules. Three-way probabilities include Tie unconditionally.

**`MATCHED` in `quotes.py` means a complete saved research quote pair only.**
`scope=QUOTE_PAIR_RESEARCH_ONLY` and `actionable_status=NOLINE` remain explicit.
The supplied CSVs do not establish sportsbook rule references or full-game OT
provisions. Canonical identity, rule compatibility and a shared trial population
have not been joined. This is not an end-to-end `MATCHED` result under section 8
of the core contract, and no actionable edge is emitted. Missing pairs return
`NOLINE`; identity conflicts return `IDENTITY_BLOCKED`, with null probabilities.

## Score settlement and hindsight evidence

`ScoreCard` stores known standalone quarter scores `(home, away)`. Unknown
quarters remain absent. H1=Q1+Q2, H2=Q3+Q4, REG=sum(Q1..Q4), and FG=REG+OT.
`overtime=None` means unknown and blocks FG; `(0,0)` explicitly means known zero
OT. No missing period is filled with zero. Spread and total pushes use the
existing settlement helpers. Two-way winner ties push under the stated research
convention; three-way Tie is a separate winning selection.

`compare_grade` checks all quote/request identity fields and timestamps before a
score audit can `PASS`. A PASS has `scope=SCORE_CONVENTION_ONLY`,
`book_rules_verified=false`, and label `hindsight_settlement_audit`. It verifies
arithmetic under the declared convention, not sportsbook rules or model quality.

`python -m research.market_calibration.audit` writes
`artifacts/saved_quote_audit.json`. It independently reads evidence-only actual
scores from the cleared file, derives H1 from Q1+Q2, and compares saved W/L/P
labels. The grades file's repeated `q1_*` fields are never used as H1 totals.
Q4 and OT remain unknown. The audit covers 132 quote rows, 100 available grades,
and explicit Q2–Q4 Pinnacle absence checks. Raw CSV rows without grades are
`NOT_PRESENT`, never falsely passed. This artifact is hindsight evidence only.

## Calibration, bias and output separation

`Provenance` records source/hash, model, namespaced game ID, season/week,
inspection state, split, prediction/start/outcome timestamps, scoring label and
prediction family. Split overlap is checked at game level across seasons and
all periods/forecasts of that ID. W1–8 2026 and inspected TNF JAX@BAL are
`development_inspected`, never untouched holdout. `CalibrationBias.fit` refuses
holdout and any non-train/effectively inspected data. Eligible train calls return
`UNIMPLEMENTED_NO_FITTED_CALIB`, null coefficients and provenance; no fit occurs.

`score_predictions` provides descriptive raw Brier scores for one split and one
label at a time. Baseline requires prediction before event start and outcome.
Hindsight is separately labelled. Timestamp checks alone do not verify an
immutable pregame forecast; the result explicitly records that limitation and
makes no validation claim. Market-anchored provenance is refused by raw scoring.

`separate_outputs` deep-copies raw outputs unchanged. A caller-proposed blend
requires exact raw/quote market identity, namespaced game alias, line and
probability basis. Missing or mismatched identity/basis suppresses the blend.
A two-way push-excluded model probability must be explicitly supplied; this
module never drops a raw Tie probability and renormalizes it. Weights have no
default, are not fitted, and are labelled `CALLER_PROPOSED_NOT_FITTED`.
All anchors are `PENDING_VALIDATION`, research arithmetic only, and excluded from
edge selection (`RAW_ONLY`); their actionable status remains `NOLINE`.

The separate `raw_model_outputs.json` and `market_anchored_outputs.json` artifacts
are honestly empty: no raw forecasts or proposed weights were supplied. Saved
no-vig market probabilities in the audit are never labelled raw model outputs.

## Required edge delivery guard

`guard_edge_delivery` is exported from `research.market_calibration` and implemented
in `delivery_guard.py`. `separate_outputs` calls it on every return, with or without
a caller-proposed anchor, and adds a separate `delivery_guard` envelope. Any future
consumer that surfaces edges must use this check immediately before delivery:

```python
outputs = separate_outputs(raw, matched, quote_policy={
    "asof_utc": delivery_asof_utc,
    "max_age_seconds": permitted_quote_age_seconds,
    "expected_line_timing": "pregame",
})
guard = outputs["delivery_guard"]
if guard["surfaceable"]:
    surface_research_comparison(guard["surfaceable_payload"])
else:
    retain_diagnostic(guard)
```

There is no other edge delivery entrypoint in this package. Consumers bypassing
`separate_outputs` must call `guard_edge_delivery(raw_p, market_p, ...)` themselves,
supplying raw/quote identities, each probability basis, quote provenance, the raw
model object and `calibration_status={"status": "UNIMPLEMENTED_NO_FITTED_CALIB",
"fitted": False}`. Only `surfaceable_payload` is eligible for research display;
it is null on quarantine. The research objects alone do not approve delivery.

The threshold is `ANOMALY_EDGE_PP_THRESHOLD = 0.40`, in probability units (40pp).
An absolute raw-versus-no-vig gap **at least** this large returns
`DIAGNOSTIC_ANOMALY` with `EDGE_GAP_GE_40PP`. Both signs are checked using decimal
representations to avoid the `.7 - .3` binary-rounding boundary. A 39.9pp gap
passes the threshold check but still requires all other checks. An anchor or
caller weight cannot hide a raw gap or release quarantine. All raw values are
deep-copied without conversion, clipping, shrink, or fitted coefficients.

The other diagnostic reason codes are:

- `ID_CHECK`: missing/mismatched game namespace/ID, player, team, market, period,
  side, line or settlement. Player identity must match when supplied; current
  `QuoteRecord` has no player subject and cannot authorize player comparisons.
- `UNITS_CHECK`: missing/nonfinite/out-of-range probability, percent or American
  odds supplied as a probability, different comparison bases, or a raw model
  object contradicting the checked probability/basis. No unit conversion occurs.
- `PRICE_TIME_CHECK`: missing/invalid American price, source/hash, timezone-bearing
  observation/retrieval timestamps, inconsistent ordering, missing timing/in-play
  declarations, or failure of a declared quote policy.
- `CALIBRATION_CHECK`: missing or contradictory calibration declarations, fitted
  claims, or a market-anchored object supplied as RAW. Honest `fitted=False` is
  retained and permits only the raw research comparison.

`quote_policy` can declare `asof_utc`, `max_age_seconds`, `expected_line_timing`,
`allow_in_play` (default false), and `freshness_status="STALE"`. Age is measured
from `last_update_utc`; retrieval must not follow the as-of time. An age equal to
the limit is allowed. A maximum age without an as-of time fails closed. Explicit
STALE in either policy or quote provenance quarantines. The guard always checks
quote timestamps; without an age/as-of policy, freshness is `NOT_DECLARED` and
age is null. No wall-clock freshness or universal age limit is invented. Open
versus close must be supplied via `expected_line_timing` when that distinction
matters. Direct callers must declare `price_format="american"`; `separate_outputs`
sets this from the existing `QuoteRecord` price convention.

Quarantine is metadata on the delivery envelope only. It does not alter either
research output or recompute the caller-proposed anchor. Anchors remain
`PENDING_VALIDATION` / `CALLER_PROPOSED_NOT_FITTED` (or `ABSENT` when no weight was
provided); Bias remains `UNIMPLEMENTED_NO_FITTED_CALIB`. `edge_basis=RAW_ONLY`
and `actionable_status=NOLINE` apply even to surfaceable comparisons. This guard
does not establish licensing, canonical joins, rule compatibility, independent
model lineage, historical validation, or predictive impact (`NOT_MEASURED`).

## Shared trial contract

The core contract appeared during implementation and was read in full:
`/workspace/research/nfl_sim_integration_2026-11-06/core_contract.md`.
The adapter is bound to its exact SHA-256 in code and MANIFEST. A changed contract
blocks transport pending realignment. No files in that integration tree were
written. The phase-1 exclusions in the external document apply to its own author;
the user's explicit authorization governs this separate implementation.

`adapt_joint_trials(rows, expected_trial_ids=...)` consumes the contract 1.0.0
objects, including game/freeze/engine/RNG metadata and `team_periods`. It preserves
`forecast_id`, `<forecast_id>/trial/<trial_index>`, decimal-string base `seed`,
derived `trial_seed`, input hash, source rows and missingness. The seed derivation
is independently checked with the contract's SHA-256 procedure. It rejects
incomplete/invalid/duplicate trials, inconsistent populations, missing scores,
invalid OT boundaries, missing/unknown features with invented values/effects,
and requested trial-ID/order mismatches. No rows are silently discarded, shuffled
or resampled. Primitive score rows alone produce H1/H2/REG/FG; player data stays
opaque and no targets or player projections are invented.

Status is `CONTRACT_SCORE_TRANSPORT_ONLY`. Full event, opportunity, accounting,
canonical crosswalk and frozen-manifest acceptance remain **NOT_RUN**, and
transport is always nonactionable. Synthetic unit fixtures verify transport;
there was no producer simulation or cross-consumer runtime validation. This
limited scope is distinct from full contract acceptance and from calibration.

`MANIFEST.json` and `manifest.validate_manifest` reject unsupported FITTED/OK/
VALIDATED claims, non-existent artifacts, mislabeled inspected data, contract
hash changes, and missing raw/anchor separation. Execution logs and the second
review are recorded in `reviews/COMPLETION_CODEX.md` and
`reviews/codex_exec_evidence.json`.
