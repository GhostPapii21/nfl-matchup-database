# Proposed patch: pull_odds.py pregame guard (NOT applied; pull_odds.py lives in a past run folder)
Apply to the next run's copy (runs/2026-11-05_shared_src/pull_odds.py when created). Helper + tests already landed:
tools/odds_pregame.py, tools/tests/test_odds_pregame.py (3 tests, pass).

```diff
-SUN=[e for e in ev if e["commence_time"][:10] in ("2026-11-01","2026-11-02") and not e["commence_time"].startswith("2026-11-02T0") or e["commence_time"]=="2026-11-02T01:20:00Z"]
+sys.path.insert(0,"/workspace/nfl-database/tools"); import odds_pregame
+SUN=odds_pregame.pregame_events([e for e in ev if SLATE_START_UTC <= e["commence_time"] < SLATE_END_UTC])  # drop games already kicked off
```
Also: add column `inplay` = odds_pregame.flag_inplay(rows, commence) so any already-written file can be filtered.
Evidence: inplay_rows_2026-11-01.txt (odds_i1435 5055/10206 rows quoted after kickoff; i1850 1062/2188, e.g. Stafford pass yds DK 168.5 vs Pinnacle 248.5).
