# CANONICAL_PREGAME_BLITZ summary
Source: NFL_HISTORICAL_ODDS_2026_W1_9_v2.zip :: SCOPED_2026_W1_9_STRICT_PREGAME.csv (package unchanged). Read as strings; all original raw values preserved.
- Input rows: 100996
- Timing re-check (snapshot_ts_utc vs commence_time_utc, parsed tz-aware UTC; prior status field ignored): excluded 0 {'snapshot_blank_or_invalid': 0, 'kickoff_blank_or_invalid': 0, 'snapshot_equal_kickoff': 0, 'snapshot_after_kickoff': 0}; valid 100996
- After dedup: 90948 (removed 10048)
- Key: (game_id if nonblank else event_id, book, market, period, player, outcome, line). Price not in key. Exact strings. Line compared as exact string; numeric normalization would give 90948 groups vs 90948 exact, so no normalization needed.
- Null/blank key audit (valid rows): {'game_id': 0, 'event_id': 0, 'book': 0, 'market': 0, 'period': 0, 'player': 16848, 'outcome': 0, 'line': 5196}. Blank player = game-line markets (kept, blank is a key value).
- Duplicate key groups (>1 row): 3894; groups with >1 distinct price across snapshots: 2600
- Earliest-snapshot ties (>1 row at min snapshot): 0; with conflicting prices: 0; with any differing original values: 0
- Rules: keep earliest snapshot < kickoff; ties are broken by stable original input order (first row in source file). Output is the retained rows in original input order. Added columns: canonical_source='Blitz', provenance_notes.
- Retained by week: {'3.0': 4602, '4.0': 4436, '5.0': 3994, '6.0': 29599, '7.0': 31342, '8.0': 15527, '9.0': 1448}
- CANONICAL_PREGAME_BLITZ.csv.gz sha256 286c05609568536f64321cd70dabf0bb2578dc3cb4a5767c27f8b1f17f58bd69; uncompressed 74082515 bytes. COLLISION_AUDIT.csv = per duplicate group rows, price variants, and tie stats.
- Validations passed: unique keys, all snapshots < kickoff, earliest per key, column order = original + 2, raw values equal source, gzip readable.
