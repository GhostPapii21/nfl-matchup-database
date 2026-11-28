# Sunday research command

Research only. `projection_ready` stays false. The command does not start the gated 100,000-trial path, does not call the network, and does not write a database.

`tools/sim_v6.py` is the documented three-method entrypoint. When that file is absent the run says so. It does not relabel the possession engine, the period engine, or `calibration/simv56/engines/cc_sim_v6.py` as sim_v6.

## Commands

Preflight one game (no simulator):

```sh
python -m sunday preflight --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
```

One game:

```sh
python -m sunday game --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00 --trials 200
```

Full slate for a schedule date. Games run in separate processes. A refusal in one game still writes the others.

```sh
python -m sunday slate --date 2026-11-29 --as-of 2026-11-28T18:00:00+00:00 --trials 200
```

Historical replay. `--as-of` defaults to the pregame packet's `generated_utc`, which for DEN@PIT is before kickoff. Final scores in the schedule file are not read.

```sh
python -m sunday replay --game 2026_12_DEN_PIT --trials 200
```

`--trials` is capped at 20,000. The gated command remains `python -m pipeline.sim100k --game <id>`.

If the schedule file and the pregame packet (or possession config) name kickoffs more than a minute apart, that game is refused. The run does not pick one. Final scores are not read from the schedule.

## Output

Each game writes `<out>/<game_id>/manifest.json` and `report.md`. A slate also writes `<out>/slate.json`. Exit 0 means every game completed. Exit 2 means at least one game was refused or only partly run; the other games are still written. The manifest records the command, git revision, per-component status and output hash, the as-of play-by-play check, and the ten layers. Critical preflight failures (missing packet, as-of at or after kickoff, target-week play-by-play) refuse that game before any simulator starts.
