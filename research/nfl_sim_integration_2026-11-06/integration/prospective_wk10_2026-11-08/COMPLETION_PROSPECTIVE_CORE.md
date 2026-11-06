# Prospective CORE repair — DAL@IND (Sun 2026-11-08)

## Separation
- Retrospective `integration/certified_asof` (JAX@BAL kickoff 2026-11-06T01:15Z) **unchanged**.
- This packet is **PROSPECTIVE_ASOF** for remaining Week 9 Sunday slate, scoped game **DAL@IND** ESPN `401873040` / nflverse `2026_09_DAL_IND` / kickoff `2026-11-08T18:00:00Z`.

## Why prior SUCCESS=0 was not exhausted access
Prior pass froze a **postgame** retrospective cutoff and treated ESPN homepage/HEAD + nflverse release pages as non-field coverage **without** pulling current week scoreboard, team rosters, depth charts, injuries, or connector schedules for a **future** kickoff. Public sources and live connectors can and did supply legitimate prospective identity/roster/depth/injury fields.

## Concrete acquisition (no new spend; no odds-bridge bypass)
| Attempt | Result | Fields |
| --- | --- | --- |
| ESPN site.api scoreboard `week=9&year=2026&seasontype=2` | SUCCESS (initial dates-only URL 403 repaired) | events, IDs, status |
| ESPN summary `event=401873040` | SUCCESS | kickoff, competitors, injuries |
| ESPN rosters DAL/IND | SUCCESS | 78+78 athletes |
| ESPN injuries league dump | SUCCESS | DAL/IND filtered |
| nflverse `schedules/games.csv` | SUCCESS (wrong `schedules.csv` asset 404 repaired) | espn↔game_id |
| nflverse roster/depth/injuries/players | SUCCESS | ACT roster, depth dt 2026-11-06T08:09:32Z, wk9 practice |
| balldontlie `nfl_get_games` week 9 | SUCCESS | id 1392339 DAL@IND scheduled |
| sports-leader scoreboard | SUCCESS identity; DK odds **NOLINE** | eventId slate |
| odds-bridge | LOGIN_REQUIRED | BetGuru owns auth |

Artifacts: `ACQUISITION_ATTEMPTS.json`, `raw/`, `records/`, `SOURCE_LEDGER_PROSPECTIVE.json`.

## Implemented CORE inputs + runs
- Frozen `inputs/{registry,model,splits,run_spec}.json` with real ESPN/nflverse IDs, ACT players, depth rotation, IR unavailable (Alec Pierce), Questionable retained with uncertainty; coverage/routes/personnel **allows_sim_effect=false**.
- Quotes **NOLINE** / no picks.
- `pytest tests/test_joint_producer.py`: **77 passed** (conservation/OT suite).
- Joint producer n=5 seed 20261108: see `runs/joint_trials_summary.json` / `runs/joint_producer_n5/` (usable trials after max_steps=400).
- Empirical possession sim n=500 DAL/IND W1–8: `runs/sim_dal_ind_summary.json` (means research-only, not calibrated).

## Readiness honesty
`projection_ready=false`. Ghost final **NOT_CLAIMED**. Impact **NOT_MEASURED**. 15 phases / brainstorm / final vet **NOT_COMPLETE**. Market auth does not block this public-source accounting run.

## Remaining genuine blockers
1. Complete brainstorm + 15-phase ledger + independent Ghost vet for projection_ready.
2. BetGuru odds-bridge auth for multi-book consensus (until then NOLINE).
3. Empirical usage-cell fit from PBP under same freeze (current joint terminals are depth/placeholder).
4. Official inactive/weather freeze closer to kickoff.
