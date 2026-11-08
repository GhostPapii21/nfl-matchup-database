# Data update steps

These are free public refresh methods. They do not include credentials, paid API calls, or a new odds purchase. Re-fetched bodies stay out of git when the license is uncertain. Record the SHA-256 in a local note or in a follow-up exclusion record.

## nflverse

Play-by-play, rosters, players, games, and depth charts already in `fixtures/` and `research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08/raw/` come from the public nflverse data releases.

1. Read the current license at https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md.
2. Download the release file you need from https://github.com/nflverse/nflverse-data.
3. Compare the new SHA-256 with `inventory/EXCLUSIONS.json` and with the file already committed.
4. Replace a committed nflverse file only when the license still allows redistribution, and say which release you used.

FTN charting distributed through nflverse is CC BY-SA 4.0 and requires FTN attribution. Those parquet files are not in this repository. An authorized local copy can sit at `data/licensed/ftn_charting_2026.parquet`. Do not commit it.

## ESPN public endpoints

`data/redistributable/teams/fetch.py` and `source_adapters/teams/fetch.py` call the public ESPN summary endpoint with `curl`. No key is set. Raw JSON from those calls is excluded. Derived penalty CSVs under `data/redistributable/teams/` remain, with the same ESPN attribution already used by the matchup snapshot.

To refresh penalties, run the fetch script from `data/redistributable/teams/` on a machine that may call the network, rebuild with the existing `penparse.py` / `build.py` tools, and review the diff before committing derived tables. Do not add `espn_raw/`.

Phase 15 inactive and roster bodies (`espn_injuries.json`, `espn_roster_*.json`, `espn_summary_*.json`, scoreboard JSON) are the same class of file. Pull them again from the public ESPN site API when a freeze is authorized, hash them, and keep the bodies off the public branch until redistribution is explicit. NFL-46.

## Books, ORCA, and FTN mirrors

There is no public scraper in this repository that returns live Pinnacle, DraftKings, FanDuel, ORCA, or FTN model prices.

- Odds-bridge remains unauthenticated. Do not embed a token.
- Until that connector is signed in, calibration stays `NOLINE` and `fitted` stays false.
- ORCA access and identity are unknown (NFL-53, NFL-54).
- FTN model-mirror access is unknown (NFL-55).

## Weather

NWS point forecasts are public. The checkpoint documents a weather hook and does not treat a stored scenario file as a game-time freeze. NFL-57 tracks the missing game-time adapter. A later pull should store the NWS URL, issuance time, and the grid that was requested.

## What not to refresh from this tree

Do not buy data. Do not run a 100k simulation. Do not call Firecrawl with an account key. Do not duplicate the PFF browser lane. Historical stderr logs and scraped page copies are hash-only in `inventory/EXCLUSIONS.json`.
