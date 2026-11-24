# Sharp Advanced Box Scores — 2026 Weeks 1–10

This package contains authorized, normalized publisher-provided NFL team-game and quarter-level observations for completed regular-season Weeks 1–10.

## Coverage

- 150 completed games
- 300 team-game records (two team rows per game)
- 1,224 team-quarter records, including overtime periods where present
- 43 metric definitions from the publisher's metric catalog, preserved as database records as well as in the manifest
- 60 distinct raw source fields per team-game/quarter metric payload, including numerator and denominator components
- 2026 season, Weeks 1–10 only

The publisher's source includes per-team raw numerators/denominators and counts. Preserve those fields. Do not treat absent quarter metrics as zero, and do not recompute publisher rates using a different denominator. Some quarters or individual metrics are absent when no qualifying event/sample exists.

## Files

- `team_games.jsonl`: one row per team per game
- `team_quarters.jsonl`: one row per team per quarter/OT period
- `manifest.json`: metric catalog, source timestamps, coverage and per-week counts

Each row preserves the Sharp source game key, date, week, team/opponent, home/away role, and raw metric values. Team-game rows also retain the listed quarterback when supplied.

## Import

The existing database has a generic `supplemental_records` table. The importer uses it, so no destructive schema migration is needed:

```sh
python3 data_ingest/import_sharp_advanced_boxscores.py --db /path/to/private/nfl_matchups.sqlite
python3 data_ingest/import_sharp_advanced_boxscores.py --db /path/to/private/nfl_matchups.sqlite --apply
```

The importer stores 300 team-game rows, 1,224 team-quarter rows, and 43 metric-catalog definition rows in `supplemental_records` (1,567 records total). The four catalog groups are `box`, `eff`, `pass`, and `run`; `run` contains rushing efficiency and personnel/formation tendencies. This makes the metric definitions available to database-only consumers. The first command is a dry run. The second performs an idempotent upsert. It links a record to an existing `games.game_id` only when date and both team abbreviations produce one unique match; otherwise it retains the source game key in the JSON payload and leaves the relational game_id null. After import, run the normal audited snapshot exporter and publication verifier. This package itself does not change model weights or set projection readiness.

## Source and permission

Sharp Football Analysis, [NFL Advanced Box Scores](https://www.sharpfootballanalysis.com/analysis/nfl-advanced-box-scores/). Static data assets are listed in `manifest.json`. The repository owner reports holding written permission for public redistribution; the permission letter is retained outside this repository.
