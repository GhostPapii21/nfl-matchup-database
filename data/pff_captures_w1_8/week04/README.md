# PFF NFL Week 4 — 2026 recap capture

- Schedule source: https://www.pff.com/nfl/scores?week=4
- Schedule coverage: 16 visible games; captured 16 of 16. All recap text showed Week 4 and 2026 Season.
- Per-game outputs: `games/*_accessible-recap-text.pdf`, PDF-derived `.txt`, and `*_metadata.json`.
- Workflow: visible PFF schedule/game pages; open **Recap**; activate **Generate Key Takeaways**; capture the rendered recap iframe text. No hidden APIs, purchases, exports, or account-setting changes.
- Captured sections and final card markers per game: Game Overview (12), Team Rushing Reports (4), Team Passing Reports (11), Quarterback Comparison (5), Player Participation & Snap Counts (4), Initial PFF Grades (12), Box Score Breakdown (12).
- Provenance: PFF-generated Key Takeaways are retrospective analysis; the separate report/box-score tables are displayed postgame measurements. Their source text/order is retained. Initial PFF Grades are subject to review.
- Schedule versus recap QA: Discrepancy preserved: Game 30658 (New York Jets at Chicago Bears): schedule 12-23, recap 13-23. Both sources retained; not corrected. Full away/home names and score ordering are in `manifest.csv`; the PDFs preserve the original recap columns. The Los Angeles Rams and Los Angeles Chargers are kept distinct by full matchup names.
- INT return-yard QA: no differing repeated INT return-yard values were found in the within-recap comparison across these 16 games. Raw PFF figures were retained without correction; this was not an external attribution audit. Per-game note is in the manifest.
- Schedule-page note: The schedule page title was "NFL Scores"; its visible H1 said "NFL Scores & Schedule" and 16 visible links under `/2026/4/` confirmed Week 4.
- `.txt` files are derived from the PDFs; some non-ASCII typography is normalized in conversion. PDFs are the primary local captures.
