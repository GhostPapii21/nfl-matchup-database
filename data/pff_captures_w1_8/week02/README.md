# PFF NFL Week 2 — 2026 recap capture

- Schedule source: https://www.pff.com/nfl/scores?week=2
- Coverage: 16 visible games; captured 16 of 16. Every recap text showed Week 2 and 2026 Season.
- Per-game files: accessible recap transcript PDF, derived `.txt`, and `*_metadata.json` under `games/`.
- Workflow: normal supported UI navigation to each visible schedule game; open **Recap** and activate **Generate Key Takeaways**. No hidden APIs, purchases, exports, or account-setting changes.
- Captured all seven sections and final accessible card markers per recap: Game Overview (12), Team Rushing Reports (4), Team Passing Reports (11), Quarterback Comparison (5), Player Participation & Snap Counts (4), Initial PFF Grades (12), Box Score Breakdown (12).
- Provenance: PFF-generated Key Takeaways are retrospective analysis; the separate report and box-score sections are displayed postgame measurements. Text is kept as shown; Initial PFF Grades are subject to review.
- QA: No matchup/date/score discrepancies detected in this batch. Full away/home names, date, score order, source URL, and retrieval ET are in `manifest.csv`. No completeness claim is based only on section labels; final card ratios are recorded there. No metric-by-metric table reconciliation was performed.
- Schedule note: The visible schedule H1 was "NFL Scores & Schedule" and the browser title was "NFL Scores"; 16 visible game links under `/nfl/scores/2026/2/` confirmed Week 2.
- `.txt` files derive from the PDF conversion and may normalize non-ASCII typography; PDFs are primary local captures.
