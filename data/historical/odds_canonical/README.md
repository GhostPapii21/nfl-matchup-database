# Historical NFL odds, 2026 Weeks 1-9 (canonical + quote bodies)

refs NFL-49, NFL-56. Pushed 2026-11-26 on repo-owner (Rico) authorization, 4:54 AM ET. Evidence/research data only: no model, readiness, calibration or REQUIRED_BOOKS change. No Odds API calls were made for this push; everything is copied from box exports built 2026-11-07 and canonicalized 2026-11-22.

## Folders
- `ghost6_inventory/` (source: box `research/historical_nfl_odds_inventory_2026-11-07/`, built 2026-11-07 ET; canonical built 2026-11-22 08:16 ET)
  - `canonical/CANONICAL_PREGAME_GHOST6.csv.gz`: 104,742 earliest verified-pregame keys from 264,785 observations (223,869 eligible; 119,127 removed by dedup; 0 tie conflicts). See `canonical/summary.json`.
  - `sportsbook_observations.csv.gz` (264,785 rows), `sportsbook_latest_verified_pregame.csv.gz` (104,742), `week9_verified_pregame.csv.gz` (9,120), `non_sportsbook_platform_observations.csv.gz` (71,188, pick'em/exchange, not sportsbook coverage), `provenance.csv.gz`, `retrospective_game_lines_book_unknown.csv` (816, book/timestamp unknown).
  - `source_artifacts/`: SHA256-deduplicated raw source bodies; credential query params were redacted at build time (see `SOURCE_README.md`).
- `blitz_v2/` (source: box `research/nfl_historical_odds_2026-11-07/`, built 2026-11-07 19:14 ET; canonical 2026-11-22)
  - `canonical/CANONICAL_PREGAME_BLITZ.csv.gz`, `COLLISION_AUDIT.csv`, `CANONICAL_SUMMARY.md`.
  - `SCOPED_2026_W1_9_ALL.csv.gz` (145,489), `key_csvs/SCOPED_2026_W1_9_STRICT_PREGAME.csv.gz` (100,996), `SCOPED_2026_W1_9_UNKNOWN_OR_POSTKICK.csv.gz` (44,493), `LEGACY_ALL_ROWS_FLAGGED.csv.gz` (181,362).
  - `raw_oddsapi/` (760 raw Odds API v4 JSON bodies), `supplemental_raw/` (45 unnormalized quote files, incl. JAX@BAL open/T120/T60/T30/close).

Large CSVs were gzipped (-9) to stay under GitHub's 100 MB limit; contents are byte-identical to the box originals after `gunzip`.

## Coverage gaps (unchanged from source)
- Weeks 1-2: no named-book timestamped quotes (GAP).
- Week 6: ~40k rows with no snapshot time (timing UNKNOWN).
- Quarter/half quotes: ~280 rows total (effectively absent).
- Only opening/close series: JAX@BAL (supplemental, unnormalized).
- `latest_verified_pregame` is not a closing-line claim.

## Excluded
- `.zip` bundles and `delivery/` split CSVs (duplicates of included files).
- Empty/broken files: none in this folder.
Secret scan before staging (Odds API and other key literals, apiKey= params, auth headers, cookies, session tokens, JWTs, emails): 0 credential hits.
