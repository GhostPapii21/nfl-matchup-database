# Sunday vertical slice

Research only. `projection_ready` stays false. Nothing here is `tools/sim_v6.py` or the 100,000-trial `pipeline.sim100k` gate. Inspected main remains `ef4cc690`. These commands were executed on this branch on 2026-11-28.

## What actually ran

| Piece | Call that was executed | Result |
| --- | --- | --- |
| Period engine | `core/period_engine_v0/monte_carlo.py` `simulate_game`, matchup-pair, as-of week < 12, n=200 and n=400 | Runs. Bias status `UNIMPLEMENTED_NO_FITTED_CALIB`. Game Randomness not applied. DEN@PIT n=200: home mean 20.255, away mean 22.325, total mean 42.58 |
| Neighbor cross-check | `dashboard/gamemodel.py` `neighbors` (k=250) and `outcome` on `dashboard/game_history.csv` (1238 data rows) | Runs. Three script shares summed to 1.0: favorite controls 0.34, competitive 0.556, underdog chases 0.104. Home +4.5 cover rate 0.516 |
| Opportunity board | `dashboard/opportunity.py` `league_pools` + `board_side`, both teams, default 20,000 draws, as-of plays with week < 12 | Runs in about 0.1s for both teams. No roster file, so WR/TE/RB catch pools fall back to the same plays |
| Possession engine | `core/possession_engine_v0/simulate.py` `simulate_games` on the DEN@PIT `data_only` config, n=5, n=20, and n=500 | Runs. n=500 took 16.6s and returned status OK. n=20 means were home 18.15, away 19.75. Direct call, so the NFL-42 / sim100k gates are bypassed |
| simv56 file check | `calibration.simv56_pmodel.verify_engines` | 9 vendored engine hashes match `SHA256SUMS`. Not used in the slice: it needs a legs file and a fetched source dir, and its `sim_v6` name is the scratch engine, not `tools/sim_v6.py` |
| Full site board | `python3 -m dashboard.build --offline --game 2026_12_DEN_PIT` | Exit 1: `board: schedule not available; nothing built`. `pregame/.cache` is absent |

## Composition without a new model

Primary team distribution: period engine, re-run from the committed week-11 play-by-play. The packet's stored `team_projection` is the same engine family at 20,000 trials and is not overwritten.

Independent cross-checks: neighbor outcomes (different method, no trials) and a small possession run (different engine, trial count written on the manifest). They are not averaged into one number.

Player distributions: `board_side`, once per script, by shifting the packet's implied margin to that script's center and holding the total fixed. The multipliers inside that call are the existing `script_multipliers`.

Not in this slice: `tools/sim_v6.py` (missing), calibrated Bias (unimplemented), `pipeline.sim100k` (separate 100,000-trial gate, not called).

## Commands

One game:

```bash
python -m pipeline.sunday --game 2026_12_DEN_PIT
```

Full slate (`pregame/packets/latest.json`):

```bash
python -m pipeline.sunday --slate
```

Defaults are 2,000 period-engine trials and 200 possession trials. `--possession-n 0` skips the possession cross-check. A missing packet, spread/total, or `pbp_<season>_w1_<week-1>_pulled_*.parquet` exits 2. A file whose max week is the target week or later exits 2. History that stops earlier still runs and records the data-through week.

DEN@PIT replay used `--now 2026-11-28T02:00:00+00:00`, which is after the 15:00 ET kickoff, so the manifest mode is `historical_replay`. The play-by-play max week was 11.

Tests:

```bash
python3 -m pytest -q -p no:cacheprovider pipeline/tests/test_sunday_slice.py
```

3 passed (DEN@PIT replay at n=80 / possession n=5, leaked-week refusal, missing-market refusal), together with the 6 inventory tests.

## Blockers that stop a run

1. No committed as-of parquet for the prior week. The slice refuses.
2. That parquet contains the target week. The slice refuses.
3. Packet has no spread and no total. The slice refuses. Scripts and the player shift have nothing to anchor to.

These do not stop the slice, and they are not hidden:

- `pregame/.cache` is missing, so `dashboard.build` cannot build the site board.
- No roster file, so catch pools are not separated by position.
- Period-engine Bias is unimplemented. Do not call the run calibrated.
- Possession trials here are not 100,000 and do not pass through `pipeline.sim100k`.
- Official inactives, routes, and true pressure rate stay gaps when the packet does not have them.
- simv56 is hash-verified and still not a per-game command.
