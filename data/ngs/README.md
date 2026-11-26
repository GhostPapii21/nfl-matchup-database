# Next Gen Stats data (previously held back per data/historical/MANIFEST.md "NGS weekly caches ... held back (rights)")

refs NFL-49, NFL-56. Pushed 2026-11-26 on repo-owner (Rico) authorization, 4:54 AM ET; owner states publishing permission was obtained.

- `nflverse_ngs_raw/ngs_{passing,receiving,rushing}.csv.gz`: nflverse-data release `nextgen_stats` (2016-2026, REG/POST, weekly + week 0 season rows). Asset updated_at 2026-11-07 07:04Z; fetched ~2026-11-07 07:25 ET. Box source: `research/nfl_week9_usage_2026-11-07/raw/`. SHA256 in that folder's SOURCES.csv.
- `NGS_WEEKLY_W1_8.csv.gz`: 2026 Weeks 1-8 weekly NGS rows for 162/187 selected players (passing 26, receiving 95, rushing 41), built 2026-11-07 07:27 ET from the files above. Absence != zero (NGS only publishes qualifying players). Box source: `research/nfl_week9_usage_2026-11-07/v2/NGS_WEEKLY_W1_8.csv`.
- `ngs_public_ui/`: nextgenstats.nfl.com public UI evidence (screenshots, cutoff/receiving check, evidence CSV) from `research/week9_defensive_matchups_2026-11-07/ngs_public/` (2026-11-07), plus route-chart notes viewed 2026-11-05 ~7:35-7:40 ET (`ngs_routes_notes_2026-11-05.txt`).

## Gaps
- No routes run, route participation, slot/outside or RB alignment fields; route charts show receiver paths only, no defenders.
- No data after the 2026-11-07 pull (Weeks 9+ not included).
- Excluded: `ngs_2026_{passing,receiving,rushing}.parquet` (9-byte files; the per-season asset returned HTTP 404 at pull time).
