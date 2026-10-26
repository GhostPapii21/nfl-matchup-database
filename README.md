# NFL matchup database

Public research snapshot, built October 26, 2026. Download the database and query it locally with Python or SQLite. This is a snapshot; updates are not automatically synchronized.

## Get the data

```sh
git clone https://github.com/GhostPapii21/nfl-matchup-database.git
cd nfl-matchup-database
python3 prepare.py
python3 query.py --tables
python3 query.py --sql 'SELECT game_id,date,status FROM games ORDER BY date DESC LIMIT 12'
```

Or download **nfl_matchups.sqlite.gz** from this repository and decompress it. `manifest.json` contains table counts, snapshot time and SHA-256 checksums. `schema.sql` documents the database structure. Python tools use only the standard library.

## Coverage

106 ingested games: all 93 games in Weeks 1–6 and 13 Week 7 games, including all 12 October 25 games. Layers include ESPN play-by-play and player/box-score statistics, offensive and defensive profiles, external observations and gaps, supplemental public datasets, and official NGS chart URL indexes.

Supplemental coverage is strongest for Weeks 1–6: FTN charting, snap counts, PFR advanced statistics, weekly injuries, NGS aggregate statistics, pregame depth charts and Sharp advanced box scores. Do not assume every layer covers every game. Query tables and inspect source timestamps before combining records.

NGS indexes contain 187 targeted receiving charts and 182 carry charts. Targeted charts are not complete route trees. NFL chart images, user video, screenshots and raw webpage archives are not bundled; original source links remain available. Local filesystem paths have been removed from this public copy. Original private working files remain separate.

## Interpretation and gaps

Verified source inputs and inferred profiles are separate layers. Player ID namespaces differ by provider. Null/missing is not zero. Season aggregates are scouting context, not game-specific measurements. Retrospective retrieval does not establish what was known before kickoff.

Complete route participation, TPRR/YPRR by coverage, comprehensive RB run concepts, coverage shells, player-level assignments, film attribution and daily injury chronology remain incomplete. Phase 9 environmental/situational requirements are documented requirements, not a complete implemented context pipeline. Source freshness and missing mandatory checks still block full readiness. Phase 10G policy weights are uncalibrated rules, not validated predictions. This repository provides research data, not betting recommendations.

See `DATA_GAPS.md` for the recorded source audit. In-database `external_gaps` and source timestamps provide detailed evidence. No automated green-card readiness is certified.

## Sources and reuse

See [SOURCES.md](SOURCES.md). Third-party data retain their original ownership and applicable source terms; this repository does not relicense those data. In particular FTN charting distributed through nflverse requires its source attribution and applicable share-alike license. Cite original providers and this snapshot when using derived results.
