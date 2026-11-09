# NFL source connectors (experimental, opt-in)

**Separate NFL repository only.** No automatic ingest, no model input
changes, no live bets, no key in Git, no production readiness change.

The source registry is in `source_adapters/nfl_external_sources.py`.
`python -m source_adapters.nfl_external_sources` lists sources without making any network request.
Unit tests only mock the external providers. **Green tests do not mean a
live API is authenticated, entitled or delivering usable observations.**

## Safe research connectors

| Source | Integration | Notes |
|---|---|---|
| SportsDataverse | Optional Python loader import via `get_sportsdataverse_module(enabled=True)` | Install separately; preview/beta version is not part of production dependencies. Confirm function coverage and data license before use. |
| BALLDONTLIE NFL | Read-only authenticated GET adapter `balldontlie_nfl` | Requires `NFL_BDL_API_KEY` and relevant endpoint tier. Raw response is research-only. |
| API-SPORTS NFL | Read-only authenticated GET adapter `api_sports_nfl` | Requires `NFL_API_SPORTS_KEY`; uses **v1.american-football.api-sports.io** only. Not the soccer API. |
| Cloudbet Sports MCP | Candidate disabled | Contains NFL odds coverage, but the sample tool is not verified as a player-prop or historical NFL charting service. No trading or live integration. |

## Operational restrictions

- Call `fetch_http(..., enabled=True)` only for a user-authorized,
  documented source. The library never activates on import.
- Network calls are **disabled** in CI; tests inject fake responses.
- Keep credentials in your local secrets manager or CI encrypted secrets;
  never in code, issue comments, CSVs or README examples.
- Don't infer coverage, blitz, rotation, player opportunity or quality fields
  that a provider did not return. Always preserve provider record ID, game ID,
  UTC retrieval time, historical availability and source rights.
- Scraped or postgame results cannot masquerade as pre-kickoff snapshots.
- Read-only response does not imply its contents are rights-cleared to
  redistribute or publish.
- This code **does not** publish odds, generate slips or change simulation
  weights; promotion requires independent date-locked backtests and separate
  approval.
- This public repository does not copy private/licensed PFF or FTN
  responses into tracked files. All existing NFL source attribution applies.

## Example, optional and explicitly gated

```python
from source_adapters.nfl_external_sources import catalog, fetch_http
print(catalog()) # No network access
# When a provider key and entitlement are available:
# evidence = fetch_http("balldontlie_nfl", "games", enabled=True)
# Validate IDs, response scope, and source timestamps before any ingestion.
```

## Upstream project locations

- SportsDataverse: https://github.com/sportsdataverse/sportsdataverse-py
- BALLDONTLIE: https://nfl.balldontlie.io/
- API-SPORTS: https://api-sports.io/documentation/nfl/v1
- Cloudbet: https://github.com/cloudbet/sports-mcp-server
