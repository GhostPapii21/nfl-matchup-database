# Source attribution

- ESPN NFL scoreboards, play-by-play and box scores: https://www.espn.com/nfl/ ; ESPN Analytics win-rate leaderboards: https://www.espn.com/nfl/
- NFL Next Gen Stats: https://nextgenstats.nfl.com/ ; official chart URLs are retained in the chart tables. Targeted charts do not enumerate all routes run.
- Sharp Football Analysis: https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/ ; https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/ ; https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/ ; https://www.sharpfootballanalysis.com/analysis/nfl-advanced-box-scores/
- nflverse public data: https://github.com/nflverse/nflverse-data ; source-specific license: https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md . Includes provider-specific NGS, PFR, snap-count, injury and depth-chart layers. Check original sources and licenses before redistribution.
- FTN Data charting via nflverse: https://ftndata.com/ ; attribution to FTN Data is required. Applicable CC BY-SA 4.0 terms: https://creativecommons.org/licenses/by-sa/4.0/ . FTN subset and adaptations retain these terms; no blanket license supersedes them.
- Pro Football Reference: https://www.pro-football-reference.com/ . Advanced statistics retain provider attribution.
- Secondary defensive-back sources: https://www.raidersrundown.com/ ; https://statrankings.com/ ; https://hashtagfootball.com/ . Availability and missing fields are recorded independently.

Each available observation includes its provider/source URL, retrieval time or linked fetch metadata. Consult those record-level URLs for the exact source. Source-specific metric definitions can differ: Sharp defaults for explosive plays, for example, must not silently be substituted for a different threshold.

No paid Fantasy Points Data Suite export is included. No third-party chart images or full webpage archives are bundled. Public accessibility does not imply a universal license; downstream users must observe each provider's applicable terms.

The 15 official 2026 Week 9 NFL Game Summaries were supplied by the owner and are stored under `data/gamebooks/2026/wk09/`. They are postgame research inputs, not a projection source. Each PDF carries this restriction: "This summary and play-by-play is for the express purpose of assisting media in their coverage of the game; any other use of this material is prohibited without the written permission of the National Football League." The full notice, the PDF SHA-256, the source URL, and the ingest date are in each game folder's `provenance.json`.

## Model checkpoint additions

The model tree follows the same rule. nflverse play-by-play, roster, game, and depth-chart files that were already redistributable are included as regular files. FTN charting parquets, raw ESPN API bodies, scraped book pages, and saved book-quote audits are hash-only. See `inventory/EXCLUSIONS.json` and `docs/SOURCE_STATUS.md`. ORCA and FTN model mirrors were not retrieved. No odds credential is included.

## 2026 scheme and opportunity profiles

`data/scheme_profiles/2026/` is a research extract. It does not change `projection_ready` or model weights. Play-level counts cite the nflverse 2026 play-by-play release `https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet`, retrieved 2026-11-15T12:45:04Z, sha256 `05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8`. Final-score identity cites the nflverse schedule release retrieved 2026-11-15T12:44:36Z; spread and moneyline columns were not copied. Week 9 gamebook PDFs remain the owner-supplied files under `data/gamebooks/2026/wk09/` and keep the NFL media-assistance restriction quoted above. The Week 10 Commanders at Giants gamebook was hashed for a cross-check and was not added to the repo. Route, coverage, man/zone, blocking, matchup, and personnel fields are unknown.

## Sharp advanced box-score package — 2026 Weeks 1–10

The repository includes a normalized publisher-data package under `data_packages/sharp_advanced_2026_w1_10/`, covering 150 games, 300 team-game records and 1,224 team-quarter records (including overtime periods where present). It preserves the publisher's 43 metric definitions and raw metric numerators/denominators. The repository owner reports holding written permission for public redistribution; the permission letter is retained outside the repository. Import is performed through `data_ingest/import_sharp_advanced_boxscores.py` into `supplemental_records`; the public SQLite snapshot must be rebuilt and independently verified after the private source database import.


## Sharp advanced box-score package — 2026 Weeks 1–10

- Publisher metrics: Sharp Football Analysis [NFL Advanced Box Scores](https://www.sharpfootballanalysis.com/stats-nfl/nfl-advanced-box-scores/), including the source team-game and quarter JSON assets. Public redistribution permission is reported by the repository owner and retained outside the repository.
- Game identity and final-score crosswalk: [NFLverse schedules](https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv) mapped source game IDs to ESPN event IDs; [ESPN NFL scoreboard](https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard) independently verified final status, home/away teams, and scores for each of the 150 Weeks 1–10 games.
- The package is stored in `data_packages/sharp_advanced_2026_w1_10/`. The public snapshot records 300 team-game rows, 1,224 team-quarter/OT rows and 43 metric-catalog records. Existing 84 Week 7 Sharp advanced observations are retained in `external_observations` unchanged.
