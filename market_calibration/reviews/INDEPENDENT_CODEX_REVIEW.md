# Independent Codex review — BetGuru market adapter

Reviewed 2026-11-06 in `/workspace/wt-market-calibration`, branch
`betguru-market-calibration-2026-11-06`, HEAD
`3448ad77ef3ce46488b4cccfb0cd7478c4d4b6b6`. This is an independent review of
the working files, not just that commit: `git status --short` reports the entire
`research/market_calibration/` tree as untracked. No commit or publication was made.

Disposition: suitable for **nonactionable research transport only** after the
two narrow fixes below. Full core acceptance, projection readiness, sportsbook
compatibility and predictive validation remain unestablished. Network requests,
odds pulls and simulations in this review: **0**.

## Findings and disposition

1. **P1 — Contradictory manifest success claims passed validation. FIXED.**
   `manifest.py:9` checked selected section statuses but accepted, for example,
   `quotes.actionable_status="MATCHED"`, verified crosswalk/rule claims, claimed
   producer simulation completion and implemented player targets while returning
   `True`. Existing tests passed because they mutated other status fields.
   Nine independent mutations reproduced this false validation success before
   any production edit. `manifest.py:19` now rejects these contradictory declared
   results, including network, namespace, absent Pinnacle spreads and raw-output
   claims. This validates declarations against current capabilities; it does not
   establish source truth or implement a general core/run-manifest validator.

2. **P2 — Opposite sides with different explicit snapshot IDs paired. FIXED.**
   `quotes.py:253` grouped only by snapshot source and line timing, after timestamp
   selection. Mutating one leg's `snapshot_id` to a different ID, or to null while
   the other was explicit, still returned research `MATCHED` with probabilities.
   Two independent regression cases reproduced this. Grouping now includes
   `snapshot_id`; incompatible legs produce no pair/probabilities, and an explicit
   coherent pair still matches. Missing IDs on both sides can still use the saved
   source/timestamp identity; this does not invent a source snapshot ID.

3. **P2 — Persisted audit needs regeneration after the snapshot fix. OPEN handoff.**
   Read-only regeneration finds exactly **76 changed leaf values, all `pair_id`**,
   relative to `artifacts/saved_quote_audit.json`. The previous grouping selected
   equivalent duplicates across absent/explicit snapshot IDs; the stricter grouping
   can select a different complete copy. No probability, grade, count or other leaf
   differs. Do not join the old artifact's pair IDs to newly generated matches.
   Artifact regeneration is outside this review's permitted write paths, so its
   bytes are preserved. The original 97 tests do not compare the persisted audit
   to a complete regenerated report. Owner must regenerate/version it before use.

4. **P2 integration boundary — Local metadata checks do not prove canonical
   identity, frozen inputs, split lineage or producer acceptance. UNIMPLEMENTED.**
   `joint_trial_adapter.py:97` validates score transport and retains opaque source
   objects. It does not recompute `forecast_id`, open/hash the frozen manifest or
   crosswalk, validate event/opportunity/accounting ledgers, or establish truth of
   a producer's `validation` object. `expected_trial_ids` is optional; Ghost must
   supply its independently retained ordered list. `calibration.py:66` prevents
   overlap for identical namespace/ID pairs, not cross-namespace aliases of the
   same game. A previously unseen canonical TNF alias cannot be recognized without
   a verified crosswalk/inspection registry. These limits are compatible with the
   explicitly narrow status, but block treating transport as core acceptance,
   using a changed namespace to claim untouched holdout, or releasing an edge.

Production changes were restricted to `quotes.py` and `manifest.py` under the
user's true-false-PASS exception. The regression file lives in `reviews/`; the
original `tests/` and artifacts were not edited. Regression sequence:
**11 failed → 11 passed**. The original suite passed **97 → 97**.

## Rubric results

| Area | Evidence and limit |
| --- | --- |
| Leakage | Quote loader whitelists raw quote fields, excluding grades/scores/notes. Actual scores are read by the separate hindsight audit. Timestamp gates check both retrieval and update against the earlier cutoff/as-of. No immutable freeze proof is supplied. |
| False PASS | Two reproducible validation holes fixed above. `compare_grade` PASS remains `SCORE_CONVENTION_ONLY`, `book_rules_verified=false`, hindsight-labelled. It proves arithmetic under a convention only. |
| Raw/anchor separation | Raw output is deep-copied; identity and probability basis gate blending. Caller weight is explicit/unfitted. Anchors stay PENDING_VALIDATION, nonactionable, edge basis RAW_ONLY. Empty raw/anchor artifacts do not establish any forecasts. Caller-labelled RAW is not independently verified model lineage. |
| NOLINE | All quote/trial outputs remain actionable NOLINE. Research MATCHED is narrower than contract §8. Unknown rule refs, OT scope and canonical joins are not silently verified. Pin Q2–Q4 spreads remain absent. |
| TNF/holdout | Known TNF aliases and 2026 W1–8 are inspected development; train-only fit gate rejects them and holdout. Descriptive baseline scoring checks chronology; no immutable artifact or untouched-holdout proof. Alias-wide enforcement awaits registry integration. |
| Invented prices/defenders | Loader opens exactly three saved CSVs. No missing side/price synthesis; synthetic tests are labelled. No defender/route/player generation. Feature missingness is retained; this adapter is not an inspector of all opaque producer content. |
| Trial IDs/seeds | Exact ID derivation, decimal-string seeds, contract seed derivation, duplicate/population checks, deep copy and optional ordered population comparison. No shuffle/reseed/resample. Synthetic fixtures establish software behavior only. |
| Contract claims | Bound core SHA-256 matches; status CONTRACT_SCORE_TRANSPORT_ONLY is accurate. Empty event/player fixture payloads are transport fixtures, not accepted full core forecasts. |

## Honestly unimplemented or not run

- Bias/calibration fitting, coefficients and fitted weights: `UNIMPLEMENTED_NO_FITTED_CALIB`.
- Supplied raw forecasts, anchored forecasts, locked same-set model comparison,
  untouched holdout, forecast accuracy and ROI: absent/not measured.
- Canonical schedule/team/player crosswalk, versioned alias-wide split/inspection
  registry and immutable forecast/as-of verification: not integrated.
- Verified book settlement references, participation/void/tie and quote OT scope:
  unverified; `book_rules_verified=false`.
- End-to-end quote/core projection envelope retaining values, win/lose/push/tie
  probabilities and actionable edge: not implemented. `settle` is currently
  JAX/BAL-specific and cannot accept arbitrary canonical team IDs directly.
- Player target/carry/yard projections and producer event/clock/opportunity/team
  accounting acceptance: not implemented here; full acceptance NOT_RUN.
- Source/run-gate invocation, actual source retrieval and projection workflow:
  NOT_RUN by this review. No duplicate Blitz entrypoint was created.

## Core contract and source/run-gate cross-check

Read the whole `core_contract.md` (schema 1.0.0), SHA-256
`d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9`.
Its documentation-author excluded-tree instructions are not authorization to
rewrite it; this review followed the user's separate market-only authorization.
No core or integration-owned file was written by this reviewer.

`source_run_gate/REQUIREMENT.md` was present. It changed externally during the
review from observed version 1.0.0 to 1.1.0; the latest contents were reread.
Before/after hashes are retained in the evidence JSON. This was not a reviewer
edit and was not reverted. Version 1.1.0 requires the existing file-backed
`source_run_gate/readiness.py` entrypoint, full source inventory, scenario-first
brainstorm and all 15 authoritative phases for projection readiness. Market
adapter code neither invokes nor duplicates that entrypoint. That is cooperation
for this engineering-only pass; integration must attach the adapter to the
Blitz-approved producer pipeline rather than assume automatic enforcement.

Its current ledger statuses are `SUCCESS | SAVED_ONLY | MISSING | LOGIN_REQUIRED |
STALE | ERROR | NOT_APPLICABLE`. These retained quotes are SAVED_ONLY, not live
SUCCESS or projection-ready evidence. Do not translate older lowercase tracking
labels into approvals. Engineering tests cannot satisfy workflow phases or
readiness. Weather/WR/edge automatic cuts remain disabled with approval evidence
MISSING under the current requirement.

## Ghost integration checklist

- [ ] Use Blitz's existing gate; retain approved scope, source ledger, actual
  workflow evidence, hashes and cutoff. Never use this pytest result as readiness.
- [ ] Produce and fully validate one shared frozen trial population; retain its
  independent ordered trial-ID list and all invalid/incomplete counts.
- [ ] Supply supported inline team-period scores, known OT state and metadata;
  call `adapt_joint_trials(rows, expected_trial_ids=ghost_ids)` without resampling.
- [ ] Verify canonical game/team crosswalk and alias-wide inspected split lineage;
  never substitute `401873037` for an unverified canonical game ID.
- [ ] Freeze exact saved quote bytes and verify sportsbook/stat/OT rules before
  any future actionable join; current outputs stay NOLINE.
- [ ] Regenerate/version the persisted audit after this fix, retaining prior
  artifact identity and replacing dependent pair-ID references consistently.
- [ ] Retain coverage UNKNOWN, routes/personnel MISSING, null values and
  `allows_sim_effect=false`; TNF actuals remain EVIDENCE_ONLY_POSTGAME.
- [ ] Keep raw and pending anchored outputs separate; Bias stays unfitted.

Detailed call and field contract: `../tracking/GHOST_HANDOFF_MARKET_ADAPTER.md`.

## Same-set engineering metrics

| Classification | Before → after, identical test set | Evidence |
| --- | --- | --- |
| IMPROVED | Independent 11-case suite: 0 passed / 11 failed → 11 passed / 0 failed | `pytest_independent_red.txt`, `pytest_independent_green.txt` |
| HURT | No original-suite pass losses observed: 97/97 → 97/97 | `pytest_independent_baseline.txt`, `pytest_independent_required.txt` |
| MIXED | Not established by pytest counts; no mixed pass/fail change on either same set | Same logs |
| NOT MEASURED | Forecast quality, calibration quality, coverage, ROI, producer replay and full contract/readiness | Engineering pytest supplies no such measurements |

Combined collection: 108 passed; this is **97 original + 11 independent cases**,
not an accuracy metric and not an assertion that earlier 74/93/96-test runs were
same-set comparisons.

Required CLI after fixes, exit code 0:

```bash
export PYTHONDONTWRITEBYTECODE=1
python(){ python3 "$@"; }
python -m pytest research/market_calibration/tests -q
```

Exact output:

```text
........................................................................ [ 74%]
.........................                                                [100%]
97 passed in 0.21s
```

Machine-readable commands, full red/green output paths and file hashes are in
`codex_independent_review_evidence.json`. No network access or simulations were
needed to complete this independent engineering review.

## Addendum — Ghost anomaly / consensus delivery guard fold-in
(2026-11-06; folded by Grok Bot into this same review; **no duplicate independent runner**)

Packet ingested (read-only):
- `GHOST_INDEPENDENT_PACKET_ANOMALY_GUARD_2026-11-06.json`
- `ANOMALY_DELIVERY_GUARD_COMPLETION.md`
- CORE interface: `/workspace/research/nfl_sim_integration_2026-11-06/integration/certified_asof/MARKET_INTERFACE_CONSENSUS_ANOMALY.md`
- CORE readiness: `SOURCE_READINESS_EVIDENCE.json` (`projection_ready=false`)
- Calib sufficiency: `CALIBRATION_DATA_SUFFICIENCY_2026-11-06.json`
- Quote inventory: `QUOTE_EXTRACTION_INVENTORY_2026-11-06.json`

### Owner-reported counts (engineering only — **not acceptance**)
| Suite | Owner packet / log | This fold-in re-check |
| --- | --- | --- |
| market suite at anomaly packet | 235 (`pytest_anomaly_guard_market_suite.txt`) | log confirmed 235 |
| parent market + independent | 246 (`pytest_parent_verify_anomaly_guard.txt`) | log confirmed 246 |
| guard collect at packet time | 67 | post-consensus collect now **132** (`pytest_consensus_guard_green.txt`); market suite after consensus follow-up **300** (`pytest_consensus_guard_market_suite.txt`) |
| targeted consensus/40pp re-verify (2026-11-06 07:37 ET) | — | **63 passed**, 69 deselected (`pytest_ghost_foldin_verify_targeted.txt`) |

Counts are same-set engineering hygiene only. They do **not** establish source readiness, forecast quality, ROI, or Ghost final acceptance.

### Multi-book consensus (not paired single-book alone) — VERIFIED in code+tests
- Default `consensus_requested=True`; `MIN_CONSENSUS_BOOKS=2`.
- Comparison target is consensus equal-weight mean of ≥2 distinct **retrieved**, registry-eligible books with matching identity/basis/cutoff; imputed/guessed/missing/duplicate books fail closed.
- Single retrieved book with requested consensus → status `DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS`, `surfaceable_payload=null` (cannot fall back to paired single-book as consensus).
- Zero eligible books → `CONSENSUS_INSUFFICIENT`, NOLINE.
- Explicit `consensus_requested=False` retains legacy single-book research path labelled `SINGLE_BOOK` only.
- `separate_outputs` always attaches `delivery_guard`; default consumer without consensus cannot surface.
- Tests: `test_threshold_uses_consensus_and_not_the_single_quote`, `test_requested_consensus_cannot_fall_back_to_single_quote`, `test_default_consumer_requires_consensus…`, `test_direct_guard_defaults_to_consensus_and_object_cannot_be_bypassed`, `test_minimum_is_distinct_retrieved_books_and_never_imputed`, `test_no_quotes_means_insufficient_consensus_and_noline`.

### Exact 40pp boundary / negative gaps / aggregate honesty — VERIFIED
- Threshold inclusive via `Decimal`: `|raw − comparison| ≥ 0.40` → `EDGE_GAP_GE_40PP` / `DIAGNOSTIC_ANOMALY`.
- Both signs covered (`.9−.5`, `.5−.9`, `.7−.3`, `.3−.7`).
- Float near-miss `.6999999999999998−.3` stays non-quarantine (honest float, not invented shrink).
- Declared `consensus_p` that disagrees with recomputed mean fails `CONSENSUS_AGGREGATE_CHECK`.
- Raw and market-anchored objects deep-copied; quarantine preserves raw; Bias remains `UNIMPLEMENTED_NO_FITTED_CALIB` / fitted=false.

### Nov 5 11PM ET cutoff quote probe — research-only
- Inventory `pairing_probe.asof_utc_used = 2026-11-06T04:00:00Z` ≡ **2026-11-05 23:00 America/New_York**.
- Probe over saved CSVs only; 60/60 research MATCHED pairs still `actionable: NOLINE`.
- `public_probes: []`; Odds API spend 0; Pin Q2–Q4 spreads absent → NOLINE.
- Postgame ESPN/gamebook evidence remains EVIDENCE_ONLY_POSTGAME under CORE readiness — not frozen pregame SUCCESS.

### Provenance-compatible calibration-data path (BetGuru coordination)
- `CalibrationBias.fit` requires train `Provenance` rows (RAW family, explicit as-of/split); **refuses holdout**.
- Legacy holdout `n=1230` exists but `usable_for_market_calibration_Bias_fit_this_package=false` — insufficient evidence for Bias fit.
- Until genuine OOS train rows are assembled under package provenance rules: Bias = `UNIMPLEMENTED_NO_FITTED_CALIB`; actionable = `NOLINE`; source readiness = false.
- CORE does not invent consensus weights or calib rows; BetGuru owns quote/consensus construction against CORE `BOOK_SOURCE_REGISTRY` (currently retrieved: pinnacle/DK/FD SAVED_ONLY; Circa/BetCRIS/Bookmaker/… MISSING).

### Disposition (unchanged honesty gates)
- `projection_ready=false`; source gate BLOCKED; SUCCESS=0 / SAVED_ONLY=15 / MISSING=16 / ERROR=1.
- Ghost final: **NOT_CLAIMED** / `UNVERIFIED_NOT_CLAIMED`.
- Forecast/calibration/ROI impact: **NOT_MEASURED**.
- Suitable only for nonactionable research transport + diagnostic quarantine. No acceptance from pytest counts.
- CORE source work remains priority; this fold-in does not resolve source readiness or authorize new Odds spend.
