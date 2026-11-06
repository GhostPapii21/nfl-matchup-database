# Source inventory — BetGuru market/calibration (engineering)
Pulled_et: 2026-11-06 06:20:44 EST
Task type: ENGINEERING adapter (not a projected-game card). Phases 2–13 mostly N/A with reason.

| Source | Route attempted | Result | Cached vs live | Notes |
|---|---|---|---|---|
| ESPN | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://www.espn.com/nfl/'` | rc=0 | LIVE | public homepage; snip=200 |
| nflverse_github | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://github.com/nflverse/nflverse-data'` | rc=0 | LIVE | public repo page; snip=200 |
| PFR | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://www.pro-football-reference.com/'` | rc=0 | LIVE | public homepage; snip=403 |
| NGS | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://nextgenstats.nfl.com/'` | rc=0 | LIVE | public NGS; snip=200 |
| PFF | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://www.pff.com/nfl'` | rc=0 | LIVE | public; paid grades not pulled this turn; snip=200 |
| FanDuel | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://sportsbook.fanduel.com/'` | rc=0 | LIVE | public sportsbook shell; snip=403 |
| DraftKings | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://sportsbook.draftkings.com/'` | rc=0 | LIVE | public sportsbook shell; snip=200 |
| Pinnacle | `curl -sS -o /dev/null -w '%{http_code}' --max-time 8 'https://www.pinnacle.com/en/football/matchups/'` | rc=0 | LIVE | public matchups shell; snip=200 |
| OddsAPI_status_no_spend | `python3 - <<'PY'
import os
from pathlib import Path
# Do NOT call Odds API network with key. Inventory key presence only.
cands=[Path.home()/'.config/oddsapi', Path('/workspace/nfl-database/tools')]
print('no_network_probe_by_policy')
print('ODDS_API_KEY_env', 'SET' if os.environ.get('ODDS_API_KEY') else 'UNSET')
PY` | rc=0 | LIVE | policy: no new paid pulls; env presence only; snip=no_network_probe_by_policy ODDS_API_KEY_env SET  |

## Cached quote / pbp inventory (used by adapter; historical cutoff)
| Artifact | Exists | mtime ET | Role |
|---|---|---|---|
| /workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds/odds_jaxbal_game.csv | YES | 2026-11-04 15:00:37 EST | CACHED |
| /workspace/nfl-database/runs/2026-11-05_JAX@BAL_r6/odds/odds_r6.csv | YES | 2026-11-04 14:59:57 EST | CACHED |
| /workspace/nfl-database/live/2026-11-05_JAX_BAL/period_q1_q2_q3_fd_dk_cleared.csv | YES | 2026-11-05 23:13:47 EST | CACHED |
| /workspace/nfl-database/live/2026-11-05_JAX_BAL/period_line_grades.csv | YES | 2026-11-05 23:12:08 EST | CACHED |
| /workspace/wt-market-calibration/research/period_engine_v0/data/play_by_play_2026.parquet | YES | 2026-11-03 19:13:53 EST | CACHED |
| /workspace/wt-market-calibration/research/period_engine_v0/data/play_by_play_2025.parquet | YES | 2026-10-29 06:01:57 EDT | CACHED |
| /workspace/research/model_rerun_audit_2026-11-06/AUDIT_COMPLETION.json | YES | 2026-11-06 05:31:26 EST | CACHED |
| /workspace/research/nfl_sim_integration_2026-11-06/core_contract.md | YES | 2026-11-06 06:13:52 EST | CACHED |

## Odds books in cached r6 odds_jaxbal_game.csv
books {'draftkings': 8, 'fanduel': 12, 'pinnacle': 12}
pinnacle_markets {'h2h_h1': 2, 'h2h_q1': 2, 'spreads_h1': 2, 'spreads_q1': 2, 'team_totals': 4}
PINNACLE_Q2_Q4_SPREADS ABSENT→NOLINE
