# 2026 scheme and opportunity profiles

Research extracts for all 32 NFL teams. `projection_ready` is false. Nothing here changes model weights, formulas, or a scheduled job.

The play-level counts come from the public nflverse 2026 play-by-play release. Official NFL gamebooks are the check on the games that were opened: the 15 owner-supplied Week 9 PDFs already in `data/gamebooks/2026/wk09/`, and the Week 10 Commanders at Giants book, which was hashed and compared and then not stored. Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are `unknown`.

Start with [2026/verified_batch_was_nyg.md](2026/verified_batch_was_nyg.md), then [2026/COVERAGE.md](2026/COVERAGE.md). One JSON profile and one markdown profile for each team are in `2026/teams/`. `2026/evidence_plays.csv.gz` is the row extract those counts are summed from. `2026/manifest.json` lists every regular-season game, which ones are included, and the gamebook rights status.

Rebuild only from the recorded pulls. The script checks the sha256 values in `build_profiles.py` and stops if the files differ. It does not download new gamebook PDFs into the repo.

```sh
python3 data/scheme_profiles/build_profiles.py \
  --pbp /path/to/play_by_play_2026.parquet \
  --schedule /path/to/games.csv \
  --links /path/to/game_center_links.json \
  --week10-text /path/to/2026_10_WAS_NYG_gamebook.txt
```

The schedule file's spread and moneyline columns are not read. A rate with no plays is `unknown`, not zero.
