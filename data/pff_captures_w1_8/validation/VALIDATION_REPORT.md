# PFF 2026 W1–8 recap — independent numeric reconciliation (2026-11-06 ET)
Local, read-only. Independent source: local nflverse cache `/workspace/nfl-database/sources/nflverse/` (pbp_2026.csv.gz = GSIS-derived PBP, 2026 REG W1–8, 121 games; snap_counts_2026.csv.gz = PFR-derived). Cache mtime 2026-11-06 07:34 ET (local copy time, not original retrieval). Season/week/teams verified in-file (2026 only). **No ESPN/NFL.com official boxes fetched; this is a one-source cross-check, not official verification.** No web calls, no Git writes, no model changes.

## Results
- Games joined (week+team): 121/121. Finals: 120 match, **1 mismatch (30658)**. Dates: 119/119 compared match; 30713, 30715 unverifiable (no page title).
- Box fields (pass att/cmp/yds/TD/INT; rush att/yds/TD; tgt/rec/rec yds/rec TD), 13,134 compared: 12,051 exact, 561 within ±1, 172 mismatch (>1), 350 unverifiable (name-key ambiguity/no match). Pass TD/INT 100% where comparable; targets weakest (281 ±1, 71 >1; definitional differences likely).
- Snaps (off/def), 8,636 compared: 7,427 exact, 587 ±1, 476 >1, 146 unverifiable. 14 games quarantined for systemic snap disagreement (mostly Week 2, 30623–30634; e.g. GB OL PFF 50 vs PFR 59). Which source is wrong is undetermined.

## Priority anomalies
- 30658 NYJ@CHI: nflverse shows NYJ 4Q TD then XP **No Good** → 12-23. PFF schedule 12-23 correct; PFF recap header/quarter line (13) wrong. Quarantined, not corrected.
- 30722 LAC@LAR: INT return 71 actually Rams (Lake 45 + McDuffie 26); PFF takeaway credits Chargers → label inverted.
- 30718 IND@JAX: JAX 101 (Lane 92 pick-six + Combs 9), IND 0; PFF says "Colts had 99" → inverted and 2-yd diff.
- 30722 snaps 72 vs 73: QA artifact; 73/73 rows present. Resolved. Other "missing snap rows" were parser name collisions (e.g. Bijan/Brian Robinson). Resolved.
- "LA" labels: box/snap cards use nicknames and were joined; overview "LA" rows not parsed (open).
- 53 large player diffs (≥5) quarantined (e.g. Deebo Samuel 80 vs 0, Javonte Williams att 7 vs 24) — likely name-key/parse or stat-correction issues; unreviewed.

## Not comparable (PFF-native, NOT verified by box agreement)
Grades, pressures/hits/hurries/PR%, BTT/TWP, adjusted comp%, YBC/YCO/MTF, EPA/percentiles, blocking/run-D/coverage cards, generated takeaways.

## Pending
Team overview totals (first downs, 3rd down, RZ, drives), team report cards, defensive box, ESPN/NFL.com second-source check, review of quarantined rows. Box rows limited to PFF's top-12 per card.

## Files
`reconcile.py` (scratch), `games_reconciliation.json`, `field_reconciliation.csv` (per-field raw PFF/nflverse values, status), `field_status_counts.csv`, `quarantine.json` (61), `validation_summary.json`. Join confidence: games high (week+abbr); players medium (initial+last name within team; collisions → unverifiable). PFF URL/retrieval time per game in games_reconciliation.json.
