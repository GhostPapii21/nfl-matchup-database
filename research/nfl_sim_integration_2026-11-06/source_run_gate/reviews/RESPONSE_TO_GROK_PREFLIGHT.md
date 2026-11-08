# Response to independent Grok preflight REJECT

Date: 2026-11-06. Local follow-up only. Reviewed the supplied independent review at `../../reviews/grok_preflight_align_review.md`, the prior completion review, REQUIREMENT.md, schema, readiness.py, tests and MANIFEST.json. This response does not overturn the live vet-ready rejection. **projection_ready remains false; live vet-ready remains false; predictive quality impact: NOT_MEASURED.**

## Gap reconciliation

ALREADY_TRUE means confirmed in the pre-follow-up implementation, not inferred from this patch. FIXED denotes a concrete local change. DEFERRED identifies evidence or work outside this authorized local pass.

| Grok gap | Disposition | Actual code/evidence and remaining boundary |
| --- | --- | --- |
| Full 15-phase implementation/authoritative checklist absent | DEFERRED | The schema already requires phases 1–15 exactly once, and readiness checks distinct checked rows and referenced evidence. Authoritative phase definitions and authentic phase execution are absent. Numbered synthetic placeholders do not establish workflow completion; no invented definitions were added. |
| No real source records; synthetic tests only | DEFERRED | Tests exercise populated local JSON records and byte/hash/scope/cutoff failures, but records are explicitly synthetic. Authorized real frozen records and provider authenticity review are absent. Live/API pulls are prohibited for this pass. |
| Brainstorm/checklist enforcement and weather/WR/edge cuts | FIXED (cuts); ALREADY_TRUE (artifact checks); DEFERRED (workflow authority) | Brainstorm marker, checklist rows and evidence paths were already checked. New required run-level automatic_cuts declarations, schema disablement and explicit readiness guard reject enablement and missing declarations. Authentic workflow content remains unverified. |
| Status enum missing SAVED_ONLY; incomplete N/A reason handling | ALREADY_TRUE | Grok's enum claim is stale/wrong. Existing enum is exactly SUCCESS / SAVED_ONLY / MISSING / LOGIN_REQUIRED / STALE / ERROR / NOT_APPLICABLE. The reason is a separate non-whitespace field, not literal text appended to the enum. Existing red tests cover omitted/empty/whitespace reasons; additional tests confirm runtime schema rejection of null, empty, spaces and tab/newline reasons. |
| Infra success conflated with usable/projection data | ALREADY_TRUE; FIXED (clearer documentation) | Existing assess rejects infrastructure_only/schema_only, unusable SUCCESS and every other usable source status. Full synthetic acceptance returns projection_ready false. REQUIREMENT and MANIFEST now explicitly say pytest green ≠ projection_ready and synthetic_fixture_ready ≠ live vet-ready. |
| Schema present but not validated in readiness | ALREADY_TRUE | Grok's claim is stale/wrong. readiness.py already loads the schema, builds Draft202012Validator with FormatChecker and calls iter_errors before artifact checks. The run's source_ledger.items references $defs/ledger_row. No redundant validation path was added. |
| Completion review lacks authentic phase/source traceability | DEFERRED; FIXED (local traceability) | This response maps findings to code/tests and captured red/green evidence. The prior completion review is marked historical. Real citations and phase evidence cannot be supplied without authorized retained sources and authoritative workflow definitions. |
| MANIFEST lacks full vet-ready criteria | FIXED (explicit boundaries); DEFERRED (live fulfillment) | Added explicit readiness_boundaries, cut policy and follow-up evidence references. Existing blockers still report missing real inputs, workflow definitions and target/cutoff. The package status manifest is not a run manifest and does not certify live readiness. |

## False-pass risk reconciliation

| Grok risk | Disposition | Evidence/boundary |
| --- | --- | --- |
| Mocked data bypasses records, cut logic and projection integrity | FIXED (cut guard); ALREADY_TRUE (file checks); DEFERRED (authenticity) | Tests use actual temporary artifacts, not mocked assess/schema responses. Hashes, populated fields, scopes and cutoff checks already exist. New cut regressions close the missing run declaration. Synthetic artifacts do not prove source truth or projection integrity. |
| Silent re-enablement of automatic cuts | FIXED | Each weather/WR/edge declaration is mandatory and enabled must be false. Runtime diagnostics explicitly require DISABLED. Missing approval and unsupported dated approval claims both fail. No engine effects or thresholds were enabled. |
| Engineering tests imply projection readiness | ALREADY_TRUE; FIXED (explicit documentation) | Existing engineering-PASS and synthetic-live rejection tests keep projection_ready false; REQUIREMENT/MANIFEST state the boundary explicitly. |
| Stale/incomplete/misaligned records could be called SUCCESS | ALREADY_TRUE (existing checks); DEFERRED (source truth) | Existing schema and semantic checks reject unusable statuses, missing fields, scope and time violations. Provider authenticity, field relevance, freshness-policy correctness and authorization remain review responsibilities. No live gate success is claimed. |

## Required-fix mapping from Grok

| Grok requested fix | Disposition |
| --- | --- |
| Full authoritative 15-phase implementation, traceability and real records | DEFERRED: authoritative definitions and authorized real inputs absent. Existing structural checks do not establish completion. |
| Exact status enum | ALREADY_TRUE: includes SAVED_ONLY; NOT_APPLICABLE has separate required reason. |
| Mandatory real ingestion, no mocks in vet-ready path | DEFERRED: no live pulls authorized; existing pipeline reads file-backed records and rejects labeled synthetic evidence for live readiness. Unlabeled fabrication cannot be authenticated by file validation. |
| Guard against silent weather/WR/edge enablement | FIXED: explicit schema and readiness guard plus tests. |
| Separate infra and usable/projection readiness | ALREADY_TRUE in code; FIXED with explicit documentation and manifest boundaries. |
| Real or production-like core test records | ALREADY_TRUE for JSON record-shaped synthetic artifacts and negative cases; DEFERRED for authentic records. Synthetic observations were not relabeled as real. |
| Runtime schema and all brainstorm/checklist items | ALREADY_TRUE for runtime schema and existing structural artifact checks; DEFERRED for semantic execution of authoritative workflows. |
| Completion/MANIFEST phase evidence and real citations | FIXED for local evidence traceability and boundaries; DEFERRED for authentic phase/source evidence. No sources or citations invented. |
| Integration against live/replayed feeds | DEFERRED: no authorized retained feed supplied and live pulls prohibited. Existing subprocess tests verify the local entry point only. |

## Captured red/green

Baseline command: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest source_run_gate/tests -q -p no:cacheprovider` → **51 passed in 1.34s** before edits.

Actual pre-implementation regression command (new tests and fixture declaration added, old validator/schema):

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest source_run_gate/tests -q -p no:cacheprovider -k automatic_cuts
5 failed, 3 passed, 55 deselected in 0.27s
```

Full output: [grok_followup_red.txt](grok_followup_red.txt). The missing whole declaration test exposed the actual false-pass: old assess returned no errors after the declaration was removed. Other failures show that the old schema rejected the new disabled configuration as unknown and had no explicit cut diagnostics. Three omitted-individual-cut cases already rejected the unknown configuration; those are not claimed as new pre-fix bypasses.

Final command: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest source_run_gate/tests -q -p no:cacheprovider` → **66 passed in 1.62s**. Full output: [grok_followup_green.txt](grok_followup_green.txt).

Added 15 cases: three unapproved enablement rejections, three missing individual declarations, one missing whole declaration, one disabled acceptance, four schema-enforced invalid N/A reasons, and three unsupported dated approval claims. Existing tests continue checking exact enum, provenance, artifacts, synthetic/live separation and CLI behavior. Green means rejection assertions worked and the full labeled fixture was accepted for software verification only.

## Remaining boundaries

All cuts remain DISABLED with approval_status MISSING in the package. This version has no automatic unlock path, including when a manifest merely claims approval. Any future enablement requires retained, reviewed, scoped dated approval evidence and a separately reviewed contract/code change. No such evidence or authorization is established here.

All persistent writes are within source_run_gate/. No Cursor Cloud, spend, auth bypass, live API pulls, engine edits, simulations, fitting or calibration work occurred. Live retrieval, authentic workflow execution, projection execution and predictive validation remain NOT_RUN. Historical completion/test/probe artifacts are retained as prior-pass evidence; the current follow-up evidence is linked above. SHA256SUMS contains current file digests and excludes itself.
