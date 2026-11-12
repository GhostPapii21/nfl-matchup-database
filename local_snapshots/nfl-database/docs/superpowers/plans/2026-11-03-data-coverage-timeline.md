# Data coverage: have vs need, and the timeline to close the gaps (2026-11-03)

Rico decided the three items at 00:46 ET on Nov 3. They are now **required** (BLOCK) in `sportsbook-odds-bridge/research_data_requirements.json`, and the box audit passes: BLOCK 0, WARN 1.

## NFL

| Item | Before tonight | Now (tools/pull_odds.py, commit 53cf26f) |
|---|---|---|
| Props + alts (pass/rush/rec yds, receptions, rush+rec, completions) | yes (13 copies, 3 versions) | yes (one canonical puller; copies marked DEPRECATED) |
| Game h2h/spreads/totals, alt spreads/totals, team totals | separate `lines_<tag>.json` pull | yes, `odds_<tag>_game.csv` |
| 1H/2H/Q1–Q4 h2h/spreads/totals (rule N3) | no | yes, where books post them |
| Books FD, DK, Pinnacle, PrizePicks, Underdog | yes | yes (5 books = 1 region unit) |
| Open → T-120 → T-60 → T-30 → close snapshots | no | yes, `snapshots/odds_snapshots.csv` + state.json |
| Max quote age | no (in-play flag only) | 30 min; stale quotes go to `odds_<tag>_stale.csv` |
| Quota planner / 10% floor / quota_log.csv | no | yes |
| assemble.py reads the new files | n/a | **not done**: owned by another build. The first 9 props columns are unchanged; format is in docs/pull_odds_format.md |
| Scheduled checkpoint runs (cron/routine) | none | **not done** (see timeline) |
| Historical snapshots for weeks 1–8 | none | **cannot be closed tonight** (see timeline) |

## NBA (nba-matchup/line_tracker, commit ec98a26)

| Item | Before | Now |
|---|---|---|
| PRA + PTS/REB/AST/PA/PR main + alt | yes | yes |
| Books | FD, DK | FD, DK, BetMGM, Caesars, ESPN BET, Fanatics, BetRivers, Bovada, BetOnline, **Pinnacle** (10 books = same 1 region-unit cost) |
| Pinnacle no-vig per row | no | `pin_novig_p` column |
| Per-book move since last snapshot | no | `prev_price, prev_line, move_pp, prev_ts_utc` + `price_moves.csv` |
| Quote age / stale | no | `last_update, quote_age_min, stale` (30 min) |
| Snapshot schedule open/T-120/T-60/T-30/every 3h | yes | unchanged |
| CSV columns / closing / grading | — | append-only. The existing snapshots.csv is migrated in place on the next run (backup at /tmp/nba_snapshots_backup_20261103.csv); closing.py and grade.py are unchanged |
| Quota floor + planner | log only | planner + 10% floor + `--dry-run` |
| Pinnacle history for games before Nov 4 | none | **cannot be closed tonight** |

## Dry-run call estimates (upper bounds: only markets a book returns are billed)

Quota at the last NBA log (Nov 2, 22:35 ET): used 3,550, remaining 16,450, so the plan is 20,000 and the floor is 2,000.

| Slate | Calc | Credits (max) |
|---|---|---|
| NFL Thu Nov 5, JAX @ BAL (8:15 PM ET) | 1 event × 35 markets × 1 unit = 35 per pull; × 5 checkpoints | **175** (was 11 per pull props-only) |
| NBA tonight, Tue Nov 3 | ESPN shows 0 games (Election Day) | **0** |
| NBA next slate, Wed Nov 4 (14 games) | open 14×12 = 168; T-30 168; 2× every-3h + T-120 + T-60 at 14×6 = 84 each | **672** (same as before; Pinnacle and the extra US books cost nothing extra) |
| Total | 847, leaving 15,603 | above the floor |

No live calls were made. `--live-sample` is still available (capped at 3 calls) and was not run.

## Timeline for the gaps not closed tonight

| Date (ET) | Item | Owner |
|---|---|---|
| Tue Nov 3 | Rico reviews the bridge PR (no merge without OK). Run `tools/pull_odds.py --dry-run` once with the key to confirm the event list | Rico / agent |
| Wed Nov 4, before ~1 PM ET | First NBA run with Pinnacle: header migration, first price_moves.csv rows; check `pin_novig_p` fill rate | agent |
| Thu Nov 5, ~9 AM ET | NFL **open** snapshot for JAX @ BAL via the canonical puller (`--out runs/2026-11-05_shared_src`) | agent |
| Thu Nov 5, 6:15 / 7:15 / 7:45 PM / ~8:05 PM ET | T-120 / T-60 / T-30 / close pulls (35 credits each max) | routine (to schedule after Rico OKs) |
| Fri Nov 6 | Check whether books actually posted 1H/Q lines for TNF; trim GAME_MARKETS to what was returned | agent |
| Fri Nov 6 – Sat Nov 7 | assemble.py owner switches from `lines_<tag>.json` to `odds_<tag>_game.csv` (doc: docs/pull_odds_format.md) | assemble/gate build |
| Sun Nov 8 | First full Sunday-slate snapshot run (about 13 games × 35 × 5 ≈ 2,275 max); planner re-checks the floor before each call | routine |
| Weeks 1–8 history (NFL) and pre-Nov 4 Pinnacle (NBA) | Needs The Odds API historical endpoint (10× cost per market/region on paid plans) or a licensed archive. **Rico decision on spend.** Until then, CLV and movement studies start at Nov 4–5 | Rico |
| CFB / MLB | Placeholders in the requirements file; fill them before those pulls are used | later |
