# Point-in-time derived tables (NFL-75 Phase 2)

`depth_qb1_snapshots_2025_2026.csv`: every nflverse depth-chart snapshot's rank-1 QB per team (columns season, team,
dt [snapshot time, UTC], gsis_id, player_name). Derived from the nflverse release assets
https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2025.parquet (sha256 14f74185b3c2c48df234ced284ba3596bda3333d0b2a8df40841f68cd34539fa)
and .../depth_charts_2026.parquet (sha256 288f3dbb414da991ddb9a2e5389c80d6c826a99ad8f2881252efb2224c7d8f8f), retrieved 2026-11-13T08:01:05Z. Rows with pos_abb == "QB" and
pos_rank == 1, first row per (season, team, dt). Output sha256 c1ab52498fad542f62677e02977494a9283e4e3d78e6d2eb08a3344b0068d5d2.

Use (calibration/opportunity_fit.py): for a game, the QB1 of the latest snapshot with dt < 04:00 UTC on the game day
(before midnight ET of game day, so no game-day information). 2024 has no dated snapshots, so the depth signal is
unknown (not applied) for 2024 training games. Rows 16435. Research only.
