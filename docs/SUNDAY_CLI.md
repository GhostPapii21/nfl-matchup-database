# Sunday commands (NFL-92)

Local research commands for one game or a slate. They do not start GitHub Actions, do not register a schedule, do not call `pipeline.sim100k`, and do not change `projection_ready`. The result of every game is **PASS**, **PARTIAL**, or **BLOCKED**.

Run them from the repository root with the system Python. No extra install is required beyond the offline test dependencies already used by `scripts/test_offline.sh`.

## Commands

```sh
python -m sunday preflight --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
python -m sunday game --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
python -m sunday slate --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --concurrency 4
python -m sunday replay --game 2026_12_DEN_PIT
```

`preflight` checks one game and does not start the research stack. `game` and `slate` run that stack after the check. `replay` runs one historical game twice at the packet's `generated_utc` (unless `--as-of` is set) and compares the canonical sha256.

`game` and `slate` call the registered components in this order, and write `manifest.json` for every game:

1. `sunday.kickoff.resolve` — the canonical clock is `data/schedule/nfl_official_schedule.json` from the NFL.com week-12 schedule, corroborated by the Nov 17 flex note. The file was retrieved 2026-11-28 and is not a historical pregame capture. LV@CLE, TEN@JAX, and NE@LAC use that clock. `games.csv` disagreements stay in the conflict list. Config files are not rewritten. A missing route or coverage assignment downgrades that output only. A child `REFUSED`, `BLOCKED`, or `MISSING` analytical status still cannot make the manifest PASS. FTN charting for 2024–2026 is under `data/historical/nflverse/ftn/`; 2026 stops at week 11, `was_pressure` is absent, and a null blitz count is not zero.

The decision row reads the research packet, the script manifest, and the player board, and it checks those file hashes. Coverage assignments stay `unavailable` unless a verified charting field is present. A sack or `qb_hit` target is `inferred`, not charted pressure. Possession touchdown reconciliation is copied onto the script record when the player box ran. It is not estimated when the box is missing.

`tools/sim_v6.py` is the recovered historical prop engine's contract (blob `ab2144f03f6ca3b57950a1f2528e305193e723cd`). That source has `mc`, `bias`, and `gr` and no game-script argument, so the 3 x 3 x 100000 run is `REFUSED` with zero trials executed. Bias is refused without a dated holdout. No other engine is labeled sim_v6. A 24-trial or 400-trial possession or period run is not that acceptance.

`sunday.jobs.JobStore` is a local sqlite queue for idempotent game windows, lease recovery, a missed deadline, and an inactive lock. One handler failure stays on that job. It does not call GitHub Actions and it does not create a Render service.

`sunday-replacement-triad/1` is not sim_v6. It resamples nflverse home margins from weeks before the target week, 100000 draws, and it does not assign those draws to favorite, competitive, or underdog bins because `games.csv` has no closing spread. Period and possession 100k script cells are not started. The committed DEN@PIT lock already records one possession run of 100000 trials in 819.2 seconds. Sharp coverage, the 1096-row W4–7 backtest, and the snapshot locks are read in place. FTN charting, an NFL.com schedule capture, Main, and Lightning are unavailable in this checkout. Locks are not rewritten.
2. `pipeline.orchestrator.runner.run_games`
3. `pipeline.matchup_research.build.build_packet`
4. `sunday.script_models.run_historical_replay`
5. `sunday.player_board.from_packet`
6. `sunday.decision.board.build_board`

Each row is EXECUTED, BLOCKED, REFUSED, FAILED, or NOT_REGISTERED. A row that is not EXECUTED is not labeled EXECUTED and does not make the manifest PASS. `projection_ready` stays false.

## Arguments

| Argument | Commands | Meaning |
| --- | --- | --- |
| `--game` | preflight, game, replay, slate | Schedule id such as `2026_12_DEN_PIT`. On `slate`, repeat it to keep those games only. Replay defaults to `2026_12_DEN_PIT`. |
| `--as-of` | all | Pregame cutoff, UTC. Default is the current time, except `replay`, which defaults to the packet `generated_utc`. An as-of at or after kickoff is BLOCKED. |
| `--market` | all | Require a spread or total in the packet odds snapshot. A missing or stale odds row is then critical and the game is BLOCKED. |
| `--out` | all | Output directory. Default is `sunday/runs/` under the repository (gitignored). |
| `--repo` | all | Repository root. Default is this checkout. |
| `--min-free-mb` | all | Free space the output volume must have. Default 64. Below that, the game is BLOCKED. |
| `--week` | slate | Keep one NFL week. |
| `--date` | slate | Keep one calendar date (`YYYY-MM-DD`). |
| `--slot` | slate | Keep rows whose slot text contains this string. |
| `--concurrency` | slate | Maximum in-flight games. Default 4. Values above 8 are lowered to 8. |
| `--include-started` | slate | Keep games whose index kickoff is already at or before as-of. |
| `--all` | slate | Every game on the schedule index. |

Without `--all`, `--include-started`, or an explicit `--game`, the slate leaves out games whose index kickoff is already at or before as-of.

## What preflight checks

Critical failures are BLOCKED:

- Schedule identity: the packet game id, teams, date, week, and kickoff match the schedule index, and as-of is before kickoff.
- Leakage: source retrieval and publication stamps are at or before as-of. Postgame paths are listed and not opened. A snapshot directory stamped after as-of is not opened. A price-freeze filename after as-of is not opened.
- Roles: each club has an OK depth chart with a quarterback and at least one of RB, WR, or TE, plus an availability block and a listed quarterback.
- Engine: Python 3.11+, the possession-engine files, and `known_flags` `projection_ready: false`.
- Disk and a write/read probe in the output directory.
- Odds, only when `--market` is set.

Required gaps are PARTIAL. That includes a source `pipeline.freshness` marks STALE, GAP, or MISSING, a phase that is not AUTO, a missing per-game engine config, and any of NFL-87 through NFL-91 whose module is not registered. Those layers are not invented and are not counted as having run. Official inactives that are NOT_YET before T-90 stay acceptable.

Freshness uses `pipeline.freshness` offline. Publisher stamps that are not on the packet stay MISSING. This command does not turn that into a fresh source.

## Outputs

One game:

```text
<out>/preflight.json
<out>/packet.json
<out>/report.md
```

Slate:

```text
<out>/index.json
<out>/INDEX.md
<out>/<game_id>/preflight.json
<out>/<game_id>/packet.json
<out>/<game_id>/report.md
```

Replay:

```text
<out>/replay.json
<out>/replay.md
<out>/run_a/<game_id>/packet.json
<out>/run_b/<game_id>/packet.json
```

`packet.json` carries `result`, the checks, the role summary, the freshness rows, cited pregame outputs, excluded paths, wall time, and memory. `canonical_sha256` covers the projection and not wall time, RSS, or the output paths. Two replay runs match on that hash. `projection_ready` in the packet is false.

The last stdout line for a game is `sunday: <game_id> <RESULT> ...`. A slate ends with `sunday slate: N PASS, N PARTIAL, N BLOCKED`.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Every requested game wrote a packet and none is BLOCKED. The result may still be PARTIAL. |
| 1 | The arguments are invalid, the schedule index cannot be read, or no game matched. |
| 2 | At least one game is BLOCKED. |

Exit 0 does not mean the projection is validated.

## Historical replay

`python -m sunday replay --game 2026_12_DEN_PIT` uses the committed Week 12 packet's `generated_utc` (`2026-11-27T04:31:50+00:00`), which is before the 20:00 UTC kickoff. The locked snapshot from later that morning is excluded. Grading results, the final play log, the postgame projection file, and `runs/2026-11-27_DEN@PIT/` are listed and not read. The expected result on this checkout is PARTIAL: publisher as-of stamps are not proven offline, some phases are partial, and the NFL-87–91 layer modules are not registered. Reproducibility is PASS when the two canonical hashes match.

Tests: `python -m pytest -q -p no:cacheprovider sunday/tests`.

The run recorded for this change, including the pytest line, the DEN@PIT replay, and the 10-game Sunday slate, is in [sunday/acceptance/RESULT.md](../sunday/acceptance/RESULT.md).
