# Validation result

As of America/New_York Fri Nov 6, 2026 ~9:20 AM ET.

## Deliverable data
- `build_status.json`: **COMPLETE**
- 121/121 W1–8 REG games, 32/32 teams, OT 11, ties 1
- Period panels PRESENT 0 missing; PFF overviews 121 MISSING (NOT_ATTEMPTED)
- Market spread/total: **NOLINE** ×121 (`NO_VERIFIED_CLOSER_QUOTE`)

## Acquisition path
1. Codex builder authored under research workspace; initial fetch blocked (Codex sandbox DNS to github.com).
2. Parent shell seeded checksummed `data/raw/schedules_2026_w1_8.parquet` + `pbp_2026_w1_8.parquet` via nflreadpy; manifest FETCHED.
3. Codex fix pass: skip stale non-scoring score regressions; force NOLINE. Second Codex invoke hit ChatGPT usage limit (~retry 11:08 AM ET) after ledger already rebuilt COMPLETE.
4. Unit tests: fixture play-id ordering adjusted so Q-end markers stay terminal; **58 passed**.

## Commands
```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_ledger.py --offline --as-of 2026-11-06T14:00:00+00:00
TMPDIR=/workspace/research/nfl_period_w1_8_2026/.tmp PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q
```
