# Established local source scaffold — NOT_COMPLETE

`run_manifest.json` and `source_ledger.json` use the existing source-run-gate
schema. All retained provider evidence is SAVED_ONLY and `usable_for_run=false`.
The ledger covers the full mandatory source inventory; MISSING means no usable
artifact in this pass's explicitly bounded selection. No login requirement,
service outage or freshness claim is inferred. No network requests were made.

`snapshots/` contains exact local source bytes and `provenance.json` records
original paths, hashes, sizes, local read times and non-authoritative mtimes.
`records/` contains real-shaped extracted records pointing to those snapshots.
Saved quote extracts retain row numbers and original quote fields/timestamps;
score/grade columns remain hindsight evidence in the raw snapshots. All three
quote files named in the market handoff are retained. No adapter code is used
to map producer fields or establish acceptance.

`pull_timestamp` on SAVED_ONLY ledger rows means this pass's local read/copy
time. It is not a new external pull. Original external pull declarations remain
in source bytes and derived records. Source availability is uncertified, and
filesystem mtimes cannot establish historical availability. No forecast cutoff
or canonical game identity is fabricated. The ESPN header labels the event week
9; some local planning notes use week10. That discrepancy is unresolved.

This is scaffolding for certified as-of review; certification is NOT_COMPLETE.
Postgame ESPN/gamebook/audit artifacts remain EVIDENCE_ONLY_POSTGAME. Coverage
UNKNOWN, routes/personnel MISSING and the receiving-yard discrepancy remain.
Workflow definitions are absent; brainstorm/checklist/report are incomplete
stubs, with all 15 phase boxes unchecked. `projection_ready` stays false.

Reproduce the inventory with `python3 build_local_ledger.py`. Run the gate in
live mode (without `--synthetic-fixture`):

```sh
python3 ../../source_run_gate/readiness.py run_manifest.json
```

Expected result: exit 1, `projection_ready=false`,
`synthetic_fixture_ready=false`. This is an expected blocked result, not a
projection approval. Impact NOT_MEASURED; no 15-phase completion or predictive
improvement is claimed.


## Separate certified-as-of diagnostic follow-up

The original scaffold above remains historical. A separate [certified_asof diagnostic packet](../certified_asof/report.md) now retains the located workflow bodies, exact phase names, corrected athlete-only aliases, saved pregame-source assessment and provenance tests. It supersedes the earlier present-tense claim that no workflow definitions could be found; explicit skill version tags and execution evidence remain incomplete. Saved unknown provider pull times remain null in the new packet. No pregame forecast or source readiness is inferred from this follow-up.
