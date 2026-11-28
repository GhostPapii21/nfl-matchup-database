# PFF NFL Week 6 — 2026 recap capture

- Schedule source: https://www.pff.com/nfl/scores?week=6
- Schedule coverage: 14 visible game links, all under `/nfl/scores/2026/6/`; 14 of 14 game recaps captured.
- Per-game outputs: `games/*_accessible-recap-text.pdf`, PDF-derived `.txt`, and `*_metadata.json`.
- Workflow: normal browser navigation through visible PFF schedule/game pages; open **Recap**; activate **Generate Key Takeaways**; save rendered recap iframe text. No hidden APIs, purchase, export, or account-setting changes.
- Coverage per game: all 7 accessible sections and final carousel card markers: Game Overview (12), Team Rushing Reports (4), Team Passing Reports (11), Quarterback Comparison (5), Player Participation & Snap Counts (4), Initial PFF Grades (12), Box Score Breakdown (12).
- Source semantics: Key Takeaways are PFF-generated postgame analysis. Displayed report/box-score tables are separate measured postgame statistics; the transcript preserves them as presented. Initial PFF Grades are subject to review.
- Validation: schedule matchup/date and final score checked against recap title/header; no identity/date/score mismatch found. All expected card markers were present. Metric-by-metric content reconciliation was not performed. Row-level details and exact source URLs are in `manifest.csv`.
- Schedule page note: Schedule page title anomaly noted: visible H1 "NFL Scores & Schedule" and fourteen /2026/6/ links corroborated Week 6; browser title was "NFL Player Prop Betting Tool | Data-Driven Insights by PFF+".
- `.txt` files are derived from the PDFs; non-ASCII typography may be normalized in that conversion. PDFs are primary local captures.
