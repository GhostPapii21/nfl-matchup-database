# Data licenses (checked 2026-11-03 via GitHub API and nflreadr source)
| Data | Source | License / terms | Attribution | Used here |
|---|---|---|---|---|
| nflverse-data releases (snap counts, pbp_participation, NGS) | https://github.com/nflverse/nflverse-data | CC-BY-4.0 (repo license, GitHub API `cc-by-4.0`) | "Data: nflverse (nflverse-data), CC-BY-4.0" | snap_counts_2026 (Wk1-8, updated 2026-11-03 12:01 UTC); pbp_participation_2025 inspected only |
| FTN charting via nflverse | https://github.com/nflverse/nflverse-data/releases/tag/ftn_charting | **CC-BY-SA 4.0** (nflreadr `load_ftn_charting` docs: "released under CC-BY-SA 4.0 ... attribution must be made to FTN Data via nflverse") | "Charting data: FTN Data via nflverse, CC-BY-SA 4.0" | ftn_charting_2026 (Wk1-8). Any derived dataset we SHARE (t3a_leg_features.csv) must also be CC-BY-SA 4.0 with that attribution. Internal analysis is fine. |
| nfldata games.csv (Lee Sharpe) | https://github.com/nflverse/nfldata | **No license stated** (GitHub API license endpoint 404) | credit Lee Sharpe / nfldata | Data read for analysis only; no code copied. Raw file kept local in data/ for reproducibility; do not redistribute. |
| play_by_play_2026 (already on disk) | nflverse | CC-BY-4.0 | nflverse | possession/defense team join for FTN plays |
github.com/robots.txt saved in data/; downloads were release assets and raw files (public, normal use).
Not available for 2026: pbp_participation (coverage shell, man/zone, routes — last file 2025), NGS (last 2024 in releases). So the C2 fields (coverage shell, area, alignment share) cannot be filled for 2026 from nflverse.
