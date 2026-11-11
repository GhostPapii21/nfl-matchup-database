# Defensive coverage profile — descriptive (JAX @ BAL Final)

2026-11-05 23:14:40 ET. Final **JAX 33 – BAL 10**. No predictions/picks.

## Hard constraints
- Tackler ≠ coverage defender; pass direction ≠ assignment; incomplete ≠ drop.
- Live folder has **no** snap-level NGS alignment / film tags for this game.
- Pregame PFR/NGS/statrankings files are **priors only**.

## Tonight’s observable distribution (box + PBP)
- **JAX WR/TE target mix:** Washington led targets (7) but caught 2/7 for 61 + TD (includes 50-yd). Meyers 4/6 for 65 (long 18 — productive without explosive threshold). Strange 2/2/22 (efficient, low volume) vs Boerkircher 2/3/61 (explosive TE) and Koziol 2/2/15.
- **BAL pass outcomes under duress:** Fagnano 10/18, 60 yds, 2 INT, 1 sack; Flowers 3/6 for only 6 yds. JAX INT credit: Montaric Brown, Jourdan Lewis (box).
- **Lawrence:** 0 INT, 0 sacks on 26 attempts — clean pocket outcomes by box sack count, not pressure charting.
- **Q4 BAL:** after earlier INTs, offensive snaps skew **run** by play-text classification (see audit_findings sequence). Not a coverage claim.

## Pregame supplement pointers (existing)
- `runs/2026-11-05_JAX@BAL_r6/codex/coverage.json` top-level keys: ['Strange 4+ rec (o3.5)', 'Strange 40+ rec yds (o39.5)', 'Washington rec yds o63.5']
  - Strange 4+ rec (o3.5): nested keys ['defenders', 'man_zone', 'mof', 'assignment_source', 'assignment_status', 'caution', 'matchup_source', 'injury_note']
  - Strange 40+ rec yds (o39.5): nested keys ['defenders', 'man_zone', 'mof', 'assignment_source', 'assignment_status', 'caution', 'matchup_source', 'injury_note']
  - Washington rec yds o63.5: nested keys ['defenders', 'man_zone', 'mof', 'assignment_source', 'assignment_status', 'caution', 'matchup_source', 'injury_note']
- Overrides keys: ['_meta', 'Strange 4+ rec (o3.5)', 'Strange 40+ rec yds (o39.5)', 'Washington rec yds o63.5']
- Also on disk: `runs/2026-11-05_JAX_BAL/src/fc_statrankings_com_nfl_coverage_team_{jax,bal}.json`, SharpFootball coverage-schemes fetch, NGS parquet priors.
- **Gap:** without alignment/film, do not assert man/zone or who covered Meyers/Washington/Strange on individual targets.

