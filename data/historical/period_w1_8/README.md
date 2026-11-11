# 2026 W1–8 period coverage research

All files and generated artifacts belong to this isolated workspace. See [current counts and acquisition failures](reviews/COUNTS.md) before using the CSVs. See [definitions](data/DEFINITIONS.md) for period and quote rules.

Run from `/workspace/research/nfl_period_w1_8_2026` using Python 3.10+ with the dependencies in `requirements.txt` installed. The current environment already has those versions; no installation was performed.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_ledger.py --as-of 2026-11-06T14:00:00+00:00
mkdir -p .tmp
TMPDIR=/workspace/research/nfl_period_w1_8_2026/.tmp PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider
```

Omit `--as-of` to use current UTC. The builder restricts every acquisition to season 2026 and weeks 1–8 before retention. `data/raw/manifest.json` records fetch failures and successful snapshot hashes. Successful acquisitions can be replayed without networking:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_ledger.py --offline --as-of 2026-11-06T14:00:00+00:00
```

Offline mode requires a successful manifest and matching raw snapshot checksums. A fresh network run replaces the manifest and generated outputs; failed pulls cannot silently reuse stale snapshots. In a partial fetch, known schedule games remain present with missing PBP panels. If no schedule can be fetched, all three CSVs remain schema-only and the builder exits 2. It never invents 121 games or imports fixtures as actual results.

The test suite separates synthetic logic checks from `source` artifact checks. Add `-m 'not source'` to the pytest command above for offline unit validation. Test temporary files stay in the workspace's `.tmp` directory. The full suite deliberately fails its completeness gate until real sources are fetched and all required period panels reconcile; data-dependent checks skip with an explicit reason when no real schedule is available. Unit success alone does not mean the research deliverables are complete.
