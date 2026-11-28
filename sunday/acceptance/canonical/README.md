# Canonical Sunday path

`python -m sunday` calls the registered components in order and writes `manifest.json` for every game. `projection_ready` stays false. A manifest result of PASS means every component returned EXECUTED. The game line stays PARTIAL while publisher as-of stamps and phase rows are incomplete.

## DEN@PIT replay

```text
python3 -m sunday replay --game 2026_12_DEN_PIT --out sunday/acceptance/canonical/den_pit
sunday: 2026_12_DEN_PIT PARTIAL reproducibility=PASS
```

Both runs: component counts `EXECUTED: 6`. The stable component records match. Wall-clock fields are not part of that comparison. Kickoff source `espn_event_date`, `2026-11-27T20:00:00+00:00`.

Manifests: `den_pit/run_a/2026_12_DEN_PIT/manifest.json` and `den_pit/run_b/2026_12_DEN_PIT/manifest.json`.

## Sunday 2026-11-29 slate

```text
python3 -m sunday slate --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --concurrency 4 --out sunday/acceptance/canonical/sunday_2026-11-29
sunday slate: 0 PASS, 10 PARTIAL, 0 BLOCKED
```

Peak in-flight 4. Every game has a manifest and `EXECUTED: 6`.

LV@CLE, TEN@JAX, and NE@LAC use the ESPN event date, which matches the possession-engine config. The nflverse `games.csv` times are recorded as conflicts and are not applied. The config files were not rewritten.

| Game | Canonical kickoff (UTC) | csv time that was not used |
| --- | --- | --- |
| 2026_12_LV_CLE | 2026-11-30T01:20:00+00:00 | 2026-11-29T18:00:00+00:00 |
| 2026_12_TEN_JAX | 2026-11-29T18:00:00+00:00 | 2026-11-29T21:05:00+00:00 |
| 2026_12_NE_LAC | 2026-11-29T21:05:00+00:00 | 2026-11-30T01:20:00+00:00 |
