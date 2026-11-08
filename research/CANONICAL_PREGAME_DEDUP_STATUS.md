# Canonical Pregame Deduplication Status

**Completed:** 2026-11-08 ~07:20 ET

## Ghost6
- Source: full snapshot history (264,785 observations)
- Excluded unusable timestamps: 25,660
- Excluded at/after kickoff: 15,256
- Eligible before dedup: 223,869
- Removed by dedup: 119,127
- **Canonical output: 104,742 rows**
- 19,154 keys had multiple snapshots; no earliest-timestamp ties or same-time price conflicts
- File: `CANONICAL_PREGAME_GHOST6.csv` (local to bot)
- New columns: `canonical_source=Ghost6`, `provenance_notes`

## Blitz
- Source: SCOPED_2026_W1_9_STRICT_PREGAME.csv (100,996 rows)
- **Canonical output: 90,948 rows** (removed 10,048 duplicates)
- All input rows passed strict pre-kickoff check
- 3,894 duplicate-key groups (2,600 with differing prices); earliest snapshot wins; no earliest-timestamp ties
- File: `CANONICAL_PREGAME_BLITZ.csv.gz` (local to bot)
- New columns: `canonical_source=Blitz`, `provenance_notes`

## Standardized rule applied
Earliest snapshot timestamp strictly before kickoff, per (game_id, book, market, period, player, selection/outcome, line).

## Next
Full CSVs remain in bot packages. Provenance columns added. Research-only. Model remains NOT READY.
