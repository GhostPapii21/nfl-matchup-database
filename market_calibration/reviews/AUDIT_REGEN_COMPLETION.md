# Audit regeneration completion — 2026-11-06

P2 is CLOSED. Preserved the previous audit bytes in
`artifacts/saved_quote_audit.pre_snapshot_fix_2026-11-06.json`, then regenerated
`artifacts/saved_quote_audit.json` using `python -m research.market_calibration.audit`
with `PYTHONDONTWRITEBYTECODE=1`.

- Prior SHA-256: `3d1ff2defa75b964b99278640429c1d21ff5b69fb635a144bec360073399cb89`
- Regenerated SHA-256: `a376a9ff4d445fce2b40964e27a0d72dfadb5d38eb53ca97d6e019f78a7f5e76`

A recursive comparison confirms exactly 76 changed leaf values, all
`rows[*].pair_id`; all other values remain identical. The preserved prior artifact
is historical evidence. Use the regenerated artifact for the corrected snapshot
identity pairing.

Added `test_persisted_saved_audit_matches_regeneration`, which compares the
persisted artifact against the complete serialized regenerated report. It failed
before regeneration (`1 failed in 0.07s`) and passed in the requested combined
suite: **109 passed in 0.17s**.

```bash
export PYTHONDONTWRITEBYTECODE=1
python(){ python3 "$@"; }
python -m pytest research/market_calibration/tests research/market_calibration/reviews/test_independent_false_pass.py -q
```

Evidence: `codex_audit_regen_evidence.json`, `pytest_audit_regen_red.txt`,
`pytest_audit_regen_combined.txt`, and `audit_regen_execution.txt` in this directory.
Network requests: 0. Simulations: 0. No paid odds acquired. All writes were within
`research/market_calibration/`; Blitz CORE, `core_contract.md`, and `source_run_gate`
were not edited. This is a saved research audit; model validation remains NOT_RUN,
book rules remain unverified, and all 132 rows remain nonactionable NOLINE.
