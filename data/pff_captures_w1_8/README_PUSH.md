# PFF 2026 Weeks 1-8 recap captures

refs NFL-49, NFL-56. Pushed 2026-11-26 on repo-owner (Rico) authorization, 4:54 AM ET. The owner states he holds written permission to publish this PFF content; that permission is not independently verified here. The earlier "keep raw PFF private" note in `qa/W1_8_QA_REPORT.md` is retained as historical text.

- Source: pff.com game recap "Key Takeaways" pages (URL per game in `weekNN/manifest.csv` and `*_metadata.json`), captured via normal UI browsing.
- Pull time: retrieved 2026-11-06 18:11:39 ET to 18:50:57 ET (per `qa/w1_8_consolidated_manifest.csv`). Box source: `research/nfl_backfill_2026-11-06/pff/`.
- Count: **121 games** (W1 16, W2 16, W3 16, W4 16, W5 15, W6 14, W7 14, W8 14); per game a PDF, a derived `.txt` and a metadata JSON.
- `validation/`: ESPN/nflverse reconciliation (ESPN raw bodies + box extracts), quarantine lists.

## Gaps / flags
- No Week 9 captures; W5-8 have fewer games due to byes.
- 1 score mismatch: 30658 NYJ@CHI schedule 12-23 vs recap 13-23 (unreconciled).
- W5/W6 page-title anomaly; "LA" ambiguity in 12 games; 30718/30722 INT-return attribution suspect; 30722 snap rows 72 vs 73.
- No routes, coverage/alignment, PBP or Premium Stats views. Initial PFF grades are subject to PFF review.
