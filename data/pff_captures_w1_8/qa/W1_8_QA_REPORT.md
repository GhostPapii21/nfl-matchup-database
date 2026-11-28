# PFF 2026 W1–8 recap capture — local QA / provenance (2026-11-06 ET)
Read-only local QA of browser captures in `pff/week01..week08/`. Originals untouched. No external calls, no official-stat validation.

## Coverage (proven by file inspection)
- 121 games: W1 16, W2 16, W3 16, W4 16, W5 15, W6 14, W7 14, W8 14. No duplicate game IDs, no identical transcript hashes.
- Every game has a text transcript, a metadata JSON, a local PDF, a source URL (pff.com …#recap) and an ET retrieval timestamp.
- Card markers complete in 121/121 games (12/4/11/5/4/12/12 = 60 each; 7,260 total).
- Numeric value lines per game: 1,025–1,205 (real table values, not headings only).
- "2026 SEASON" + correct "WEEK n" text present in all 121.
- Schedule score vs recap header: 120 match; **1 mismatch: 30658 NYJ@CHI schedule 12-23 vs recap 13-23** (kept as displayed, unreconciled).

## Flags retained (see `w1_8_consolidated_manifest.csv`)
- W5 (15) / W6 (14): browser page title anomaly ("NFL Player Prop Betting Tool…"); week identity corroborated by H1 + /2026/n/ links per capture notes.
- Ambiguous "LA" team labels (LAR vs LAC) in 12 games — map by column order.
- 30718, 30722: INT-return-yard attribution suspect (30722 credits LAC 71 though Herbert threw 2 INTs).
- 30722: snap rows 72 vs 73 declared players (one potential missing).
- All: text flattened one-value-per-line, needs structured parsing; generated takeaways are PFF hindsight analysis — keep separate; initial grades subject to review.

## Missing / not covered
Routes, coverage/alignment, PBP, Premium Stats views; no metric-level reconciliation to nflverse/ESPN/official; snap-row checks only spot-checked (30722).

## Provenance / rights
PDFs are local transcriptions of visible UI text, not PFF downloads. Existing local notes (`../BUNDLE_README.md`, `../INVENTORY.md`) state no PFF/other redistribution rights were verified. **Redistribution status: UNVERIFIED — keep raw PFF content private; do not publish in a public PR without rights review.** No license is asserted.
