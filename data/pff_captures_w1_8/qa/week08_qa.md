# PFF Week 8 capture QA (read-only, 2026-11-06 ET)
Scope: `pff/week08/` (14 txt, 14 pdf, 14 metadata, manifest 14 rows, README; 30713 partial.md + png sample kept). Originals untouched. Counts: `week08_qa_counts.json`.

## Proven
- 14/14 games; 14 distinct text hashes; no identical numeric sequences across games.
- All 7 section headings present in every game; distinct card markers complete in all: 12/4/11/5/4/12/12 = 60 per game, **840 total**.
- Header final score matches manifest schedule score for 14/14 (incl. TEN–CIN, ARZ–DAL OT).
- Genuinely data-bearing: ~1,030–1,205 numeric value lines per game (~35% of lines); scoring by quarter, team overview/drives/RZ/3rd-down/EPA, rushing/passing reports with percentiles, QB comparison, per-player snap counts (spot check 30722: 72 position rows vs 73 declared players), initial grades with player/team/pos/snaps, box score rows.
- No "Premium content locked" strings in captures.
- ~335 boilerplate lines common to all games (labels/UI) — expected, not duplication of values.

## Issues / missingness
- Text is flattened (one value per line); needs a structured parser before ingestion — not ingestion-ready as-is.
- 30722 (LAC–LAR): both teams labelled "LA" in comparison rows; map by column order.
- "INT RETURN YARDS" orientation suspect: 30722 credits Chargers 71 though Herbert threw 2 INTs (Rams' Lake 1 INT); 30718 99 vs 0 — verify side before use.
- Generated takeaways are PFF hindsight analysis; keep separate from measured rows. Initial grades subject to revision.
- Not present: routes, coverage/alignment, PBP, Premium Stats views. Generated-vs-table reconciliation not done. Weeks 1–7 not yet captured. No cross-source (nflverse/ESPN) comparison done (no trivially mapped cache checked).

## Rights
Keep raw PFF text/PDFs private (not committed to public repo) pending redistribution-rights review; commit only derived/minimal facts if approved.

Verdict: valid, complete visible-recap captures for Week 8; require structured extraction + the two flag checks before backfill. No model/source readiness claim.
