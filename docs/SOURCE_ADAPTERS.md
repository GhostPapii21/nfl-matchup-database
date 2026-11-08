# Source adapters & refresh (no embedded secrets)

| Adapter | Method | Auth | Redistributable in public repo? | Refresh |
|---|---|---|---|---|
| nflverse / local PBP parquet | file read / prior download | none for local file | usually yes (check nflverse license); fixtures materialized under `fixtures/` | re-download from nflverse; record sha256 |
| ESPN depth/injuries JSON in runs | HTTP fetch scripts historically | public endpoints; respect ToS | derived JSON often ok; verify | re-run team/injury fetch closer to kickoff |
| teams/fetch.py | scripted fetch | none embedded | team pages HTML/JSON — check source ToS | `python source_adapters/teams/fetch.py` (needs network) |
| penalties/fetch.py | scripted fetch | none embedded | same | network refresh |
| tools/run_gate.py | local gate | none | code yes | run after sources updated |
| odds-bridge / BetGuru quotes | MCP connector | **needsAuth** | raw quotes excluded from public package (hash-only) | authenticate connector; until then NOLINE |
| PFF | browser/authorized separate | proprietary | **hash-only / not redistributed** | authorized refresh only (NFL-48) |
| NGS / FTN charting | various | often restricted | FTN fulltext not assumed redistributable | see NFL-47 |
| Firecrawl / Codex | external tools | account limits | N/A — not embedded keys | optional; not required for offline smoke |

**Offline smoke does not pull live odds, PFF, or Firecrawl.**
