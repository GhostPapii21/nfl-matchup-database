# WEEK9 Data Package References

**As of:** 2026-11-07 ~11:11 ET
**Purpose:** Point to source-verified numerical CSVs in the sportsbook-odds-bridge repo without duplicating large files into this research branch.

## Source repository
- **Repo:** GhostPapii21/sportsbook-odds-bridge
- **Path:** `data_packages/nfl_2026_w1_8/`
- **Branch/ref:** main (tree SHA a7a836c495949e7fc8791883c8c18dc866480eaf at time of note)

## Key numerical files
| File | Size (approx) | SHA | Description |
|------|---------------|-----|-------------|
| schedule_reg_w1_8.csv | 9 KB | ce3a577fb652f3d0730508090ebf7f2ce5cd61fb | Weeks 1–8 regular-season schedule |
| team_play_counts.csv | 10 KB | f7a7d350b923b2506bc476f68378e935639c96d9 | Team play counts |
| snaps_w1_8.csv.gz | 249 KB | f421b369ba871778d8764c84c83f26de548e114a | Player snap counts (gzipped) |
| player_game_observations_w1_8.csv.gz | 936 KB | c4b6a4fd60b920b15cb3ba2c943836397955347b | Player game observations (gzipped) |
| plays_public_w1_8.csv.gz | 220 KB | 714b7b8bf717a76d9c7bed06c6368c4511367d13 | Public play-by-play (gzipped) |
| coverage.json | 13 KB | 95ae481f7895b22c61745277e5bd4931d14673d5 | Coverage metadata |
| eval_summary.json | 7 KB | 722bb3953955d5ac217e750f98dd1087adb44b80 | Evaluation summary |
| import_proof.json | 1 KB | ca4e4c1ac3b448ff65e0cb24a3a206d95c4b1497 | Import proof |

## Notes
- These files support the Weeks 1–8 historical dataset used for projection inputs.
- Large gzipped files are left in the source repo to avoid duplication and to respect existing backfill isolation rules.
- This research branch references them only; it does not modify the packages or related PRs.
- For TE-specific numerical extracts, see `WEEK9_TE_USAGE_TARGET_ROUTE.csv` in this directory (compiled from public aggregators).

**Restricted PRs untouched. Model remains NOT READY.**
