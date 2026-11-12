# Local nfl-database snapshot (review only)

Squashed snapshot of BetGuru's local matchup database, placed under `local_snapshots/` so it cannot match any GitHub Actions path filter on main (including `pregame/*.py`, which triggers the packet workflow and can spend Odds API credits).

- Source path: `/workspace/nfl-database`
- Local branch: `mws-matchup-2026-11-04` (no remote; history is unrelated to this GitHub repo)
- Local HEAD: `a813affd8dfe18b72232bb3ab77553a57c4043d8`
- Also includes the uncommitted working tree at copy time
- Snapshot root on this branch: `local_snapshots/nfl-database/`
- Rooted at current `main` (`aca9406` or newer) as a single squashed commit
- Original local commits: see `LOCAL_COMMITS.txt`
- What was left out: see `EXCLUSIONS.md`
- Research only, not a validated projection. `projection_ready` is not set.
- Do not merge this branch.

Commit messages use `[skip ci]`.
