# JAX@BAL Pinnacle/book close (held artifact)

**Source:** `/workspace/nfl-database/runs/line_movement_wk10/odds_20261105_JAXBAL_close_game.csv`  
**SHA-256:** see `CERTIFIED_CLOSE_PINNACLE_FD_DK.json`  
**pulled_utc:** `2026-11-06T01:12:42Z` (pre-kick; commence in file `2026-11-06T01:20:00Z`; ESPN header kickoff `2026-11-06T01:15:00Z`)  
**Status:** SAVED_ONLY — usable for diagnostic close comparison; not auto-promoted to SUCCESS/`projection_ready`.  
**Spend:** 0. No Odds API live pull. Firecrawl used only for live shell corroboration (postgame pages cannot recreate this historical close).

## Pinnacle close (snapshot=close)

| Market | Side | Point | Price |
| --- | --- | --- | --- |
| h2h | Baltimore Ravens | — | +313 |
| h2h | Jacksonville Jaguars | — | −373 |
| spreads | Baltimore Ravens | +10.0 | −127 |
| spreads | Jacksonville Jaguars | −10.0 | +115 |
| totals | Over | 39.5 | −110 |
| totals | Under | 39.5 | −102 |

H2H multiplicative no-vig (research arithmetic only): BAL ≈ 0.235 / JAX ≈ 0.765.

FD/DK close rows retained in the same CSV and JSON card. T-30 and open snapshots also extracted under `closes/`.

## Delivery guard note (Rico)
Any model−market probability gap ≥ 40pp must be quarantined as DIAGNOSTIC_ANOMALY (not surfaced as an edge) pending ID/units/price-time/calibration inspection. Raw values preserved; Bias UNIMPLEMENTED; NOLINE.
