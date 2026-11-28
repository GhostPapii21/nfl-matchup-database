# Canonical Sunday path

`python -m sunday` writes `manifest.json` for every game. `projection_ready` stays false.

The manifest is not PASS while any orchestrator child is `REFUSED`, `BLOCKED`, or `MISSING`. The orchestrator row itself can still be `EXECUTED` when the fan-out ran. Freshness and the phase ledger stay checks (`analytical_execution` false).

Kickoff is canonical only from an offline NFL.com schedule capture at `data/schedule/nfl_official_schedule.json` (`source` containing `https://www.nfl.com/schedules/`, plus `retrieved_utc` and `as_of`). This checkout does not have that file, so every resolution is `UNVERIFIED` and the schedule row is `BLOCKED`. ESPN, `games.csv`, and the possession-engine config are recorded originals. For LV@CLE, TEN@JAX, and NE@LAC those originals disagree; none of them is promoted.

## Commands

```text
python3 -m sunday replay --game 2026_12_DEN_PIT --out sunday/acceptance/canonical/den_pit
python3 -m sunday slate --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --concurrency 4 --out sunday/acceptance/canonical/sunday_2026-11-29
```

The manifests in this folder are replaced when those commands are run again on this code.
