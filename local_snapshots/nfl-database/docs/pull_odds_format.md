# NFL odds pull output format (canonical `tools/pull_odds.py`, 2026-11-03)

Replaces the 13 `runs/*/pull_odds.py` copies (3 diverging versions). Those copies stay in place, marked DEPRECATED.

Run: `python3 tools/pull_odds.py <tag> --start <UTC> --end <UTC> --out runs/<date>_shared_src [--label T-30] [--dry-run]`

| File | Content |
|---|---|
| `odds_<tag>.csv` | Player props + alts. **The first 9 columns are unchanged** (`game,book,market,player,side,point,price,last_update_utc,inplay`), so readers that select those by name (assemble.py cites `SH+odds_<tag>.csv`) still work. Added columns: `event_id,commence_utc,pulled_utc,quote_age_min,snapshot`. |
| `odds_<tag>_game.csv` | Same columns. Game h2h/spreads/totals, alternate_spreads/totals, team_totals, and `{h2h,spreads,totals}_{h1,h2,q1..q4}` where books post them. `player` is empty. |
| `odds_<tag>_stale.csv` | Quotes older than `--max-age` (default 30 min) at pull time. These are never in the main files. |
| `odds_<tag>_meta.json` | Plan (events × markets × region units), per-event books and row counts, `remaining`/`used`, status. |
| `snapshots/odds_snapshots.csv` | Append-only open → T-120 → T-60 → T-30 → close history (props + game rows). `snapshots/state.json` records which checkpoints each event already has. |
| `quota_log.csv` | One row per call: `ts_et,ts_utc,job,endpoint,checkpoint,estimate,cost,used,remaining` (taken from the `x-requests-*` headers). |

Guards:
- Pregame only. Quotes stamped at or after kickoff are dropped.
- The call planner prints its estimate first and stops if `remaining - estimate < 10% of (used + remaining)`.
- The key is read from `ODDS_API_KEY` and redacted from every error.

Books: fanduel (price of record), draftkings, pinnacle (sharp / no-vig), prizepicks, underdog. Five books sent through `bookmakers=` count as 1 region unit.

`lines_<tag>.json` (game lines from the older separate pull) is unchanged. `odds_<tag>_game.csv` is additive. Moving assemble.py over to it is left to the build that owns assemble.py.
