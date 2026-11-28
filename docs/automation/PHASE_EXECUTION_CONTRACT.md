# Phase execution contract (NFL-83)

Version `nfl83-phase-execution/2`. Machine-readable copy: `pipeline/execution/contract.json`.

The 15 phase names and freshness sources are the ledger already defined by `pipeline/phases.py` `PHASES` and
`docs/PHASE_WORKFLOWS.md`. NFL-82 had not merged a separate inventory file when this contract was written, so
those two files are the canonical list this contract follows. This package does not replace that freshness
checker.

## What a receipt proves

Each attempt is one JSON file:

`pipeline/execution_receipts/<game_id>/<run_id>/phase_NN/attempt_NNN.json`

A later attempt never overwrites an earlier one. A successful retry with the same code revision, contract hash,
and input hashes returns the existing `PASS` receipt instead of writing another file.

A `PASS` receipt has `evidence_class: VALIDATED`. It names the canonical module and function that ran, the
command, the input artifact ids with content hashes, source, provenance, and as-of timestamps, and an output
whose body carries `equation_id`, `module_id`, numeric equation metrics, a denominator, and provenance.
A row that only counts players, snaps, or markets is `COUNT_ONLY` or `ANALYTIC_OUTPUT_MISSING` and is not a
pass. `projection_ready` is false and `research_only` is true. The freshness block is stored beside that work
with `satisfies_execution: false`.

`DISCOVERED` means the packet was presented and freshness was not accepted. `FRESH` means the NFL-56 checker
(or a caller-supplied freshness row) judged the phase's sources current. Neither value is execution.

## Statuses

`PASS`, `PARTIAL`, `MISSING`, `STALE`, `BLOCKED`, `FAILED`, `NOT_YET`, `NOT_APPLICABLE`.

`PASS` requires every mandatory task to have a successful invocation and a validated output. Optional tasks are
listed on `optional_tasks`. An optional failure is `PARTIAL`, which is not acceptance.

`NOT_APPLICABLE` is allowed only for an objective condition. Indoor weather uses `indoor-roof-weather`. A
policy with `when: always` is rejected. Routes, coverage shell, assignment, true pressure, line grades, the
analyst script, and the true open are mandatory and `BLOCKED` (`SOURCE_UNAVAILABLE` or `MODULE_ABSENT`). They
stay visible on `blocked_tasks` and the phase cannot `PASS`.

The orchestrator rejects a run when a receipt is missing, malformed, for the wrong game or run, stamped with
a different code revision or contract hash, missing an output, or carrying an output hash that does not match
the body.

## What this run does not do

Phase 14 names `tools/sim_v6.py`, which is not in the tree, and stays `BLOCKED`. `pipeline.sim100k` is not
called and is not accepted as a sim_v6 substitute. Phase 15 names the official-inactives hook and does not
call it; a source pull is not an equation. No production database write, secret change, deploy, or
`projection_ready` flip is part of this command. The Week 12 readiness assertion stays on draft PR #137;
this branch does not edit `evaluation/tests/test_readiness.py`.

```
python -m pipeline.execution --game <game_id> --run-id <run_id> --receipt-dir pipeline/execution_receipts --strict
```

`--strict` exits 3 when the selected phases are not all `PASS`. The printed slate separates executed phases
from phases that were merely available, and it lists partial games and refused games on their own lines.
