# Search for the "13 paid line-history snapshots" (not committed)

**refs NFL-75. Research notes only. No merge implied.**

Ghost6 asked that 13 paid Odds API line-history snapshots, already pulled and never committed, be saved to a draft PR (data only; no `pregame/*.py`, no workflow files).

I searched `/workspace/nfl-database`, `/workspace/nfl56*`, `/workspace/research`, `/tmp`, and `/home/box` for Odds API / line-history snapshot JSON that is not on `origin/main` of `GhostPapii21/nfl-matchup-database`. I could **not** uniquely identify a set of 13 uncommitted paid snapshots, so I did not invent one or commit a substitute corpus under that name.

## Closest "13" that is already on main

`pregame/line_history/*.jsonl` on `origin/main` (head `7364335`, last touched in `e2e5f49` / PR #31 and the packet refresh `a932bda`) has **13 rows** timestamped `2026-11-13T02:49:26Z` through `2026-11-13T02:50:12Z` (9:49–9:50 PM ET on Nov 12, 2026), one per Week 10 game except a 14th file that was already present. Local copies in `/workspace/nfl56` match `origin/main` byte-for-byte. These are already committed; re-adding them would be a no-op and would also touch `pregame/` paths, which this PR avoids.

## Paid Odds API artifacts found that are **not** on `origin/main`

These are real paid (or paid-adjacent) files. None is a clean set of 13 line-history snapshots.

1. **`/workspace/nfl-database/week9/model/raw/`** — 7 daily slate Odds API pulls, `odds_20261101_2125.json` through `odds_20261107_1001.json`, with matching `hdr_*.txt`. Headers show paid live calls (`x-requests-last: 2`). Pull times from those headers (UTC dates in the response): Nov 1–7, 2026, around 10:00 AM ET except Nov 1 at 9:25 PM ET. Tracked on the local `nfl-database` branch `mws-matchup-2026-11-04` only; **not** on `origin/main`. Plus `week10/model/raw/odds_20261111_1000.json` (8th daily slate file). Not 13, and these are live-slate snapshots, not historical event-odds.

2. **`/workspace/nfl-database/runs/line_movement_wk10/`** — paid open / T-120 / T-60 / T-30 / close pulls for JAX@BAL (Nov 5) and T-120 / T-60 / T-30 / close for BUF@MIN (Nov 9). 39 tracked files on the local `nfl-database` branch; **not** present on `origin/main`. 9 unique pull events, not 13.

3. **`/workspace/nfl-database/backtests/yardage_markets_wk3_8/raw/`** — 88–95 historical event-odds JSON files for Weeks 3–8 yardage markets, committed on `mws-matchup-2026-11-04` (`282e20c`, Nov 3, 2026, 6:52 AM ET). **Not** on `origin/main`. Wrong count and already on a local branch.

4. **`/workspace/research/nfl_historical_odds_2026-11-07/raw_oddsapi/`** — 760 Odds API JSON files (NFL historical / live mix, including 2024–2026). Not in the git repo (the repo only has a slim `data/historical/odds_coverage/historical_odds_inventory_2026-11-07/` summary). Too large to treat as "the 13," and many are older-season.

5. **`/home/box/odds_hist_cache/`** — 163 historical Odds API files, but they are **NBA** player-prop snapshots (Oct 20–31, 2026), not NFL.

6. **Week 9 Sunday (13 games, Nov 8, 2026):** there are 13 Sunday games in Week 9 once TNF (`JAX_BAL`) and MNF (`BUF_MIN`) are excluded. I found **no** per-game Odds API snapshot files for those 13 Sunday games. Only TNF and MNF have dedicated run folders under `/workspace/nfl-database/runs/`.

## What this PR contains instead

Only the new Week 9 alt-price test (3 historical event-odds responses + ledger + this note), under `data/odds_history/`. No `pregame/` and no `.github/` paths.
