# NFL-75: Week 10 rush-yds p_model from the SAME sim_v5/v6/v6_fix ensemble the Phase 4 fit used, + QB starter gate

**Research only, not validated. `projection_ready` stays false. 0 Odds API credits. refs NFL-75.**
No core engine or production weight change; the frozen Phase 4 classifier (`calibration/selective_edge*.py`,
`params_w4_7.json`, freeze manifest) is untouched; no `pregame/` or `.github/` change.

## How Phase 4 produced p_model for historical legs (traced)
`selective_edge_run.build` reads `selective_under_alt_2026-11-12/candidates.csv` (sha256 pinned in the Phase 4
manifest). `s3_candidates.py`: main-Under p_model = 1 - mean(`sim_v5|0.5`, `sim_v6|0.5`, `sim_v6_fix|0.5`) from
`confidence_check_2026-11-03/legs_with_probs.csv`; `analyze.py`: each engine column = mean(p_mc, p_bias, p_gr) from
`sims/<engine>_opp0.5_w<W>.csv`; `run_sims.py`: CC_OPP 0.5, n=20,000, PBP `game_date <` first game date of week W
(W9: 2026-11-02), sim_v6 / sim_v6_fix multipliers refit from `<engine>_backtest.csv` weeks < min(W,8), one sim per leg,
p = P(stat >= line). It is the confidence_check scratch copies of the Nov 1-2 game-day engines, not the possession engine.

## What this adds
- `calibration/simv56/engines/`: those three engines + their backtest CSVs and fit JSONs, **byte-identical**, pinned in
  `SHA256SUMS` and verified before every run.
- `data/historical/nflverse/derived_pit/players_slim_shared_src_20261102.parquet`: the 4 columns the engines read
  (`gsis_id, display_name, position_group, latest_team`) of the Nov 2 nflverse players table the original runs used
  (full file sha256 `02ff5524...aea1`).
- `calibration/simv56_pmodel.py`: runs the engines with exactly those settings (each in its own subprocess), replays the
  original CSV hand-offs (pandas' default float parser can land 1 ulp off), and fills `p_model` on rushyds legs.
  Includes the QB gate, `fetch`, `run` and `grade` commands.

## Bit-for-bit proof (`reproduce_w8_w9.py`, `reproduction_summary.csv`, `reproduction_w8_w9.csv`)
Using the committed W1-9 PBP (not the Nov 2 pull the original read) + the slim players table:

| week | Phase 4 rushyds Under legs | exact vs candidates.csv text | exact vs Phase 4 in-memory value | max abs diff | runtime |
|---|---|---|---|---|---|
| 8 | 83 | 83 | 83 | 0.0 | 10.5 s |
| 9 | 5 | 5 | 5 | 0.0 | 1.4 s |

Unit test (runs in CI): W8 Jacoby Brissett rushyds 9.5. Engine triples (p_mc, p_bias, p_gr): sim_v5 (0.5985, 0.566,
0.56415), sim_v6 (0.5985, 0.60605, 0.56415), sim_v6_fix (0.5985, 0.5566, 0.56415), all equal to the saved sims.
p_model = **0.42037777777777774** = candidates.csv text; after pandas' default read (how Phase 4 read it)
**0.4203777777777777** = the Phase 4 in-memory value.

**pandas version matters for the last ulp.** Phase 4 ran on the box's pandas 3.0.6, whose C float parser lands 1 ulp
off the written text for some values (e.g. Brissett `0.42037777777777774` is read back as `0.4203777777777777`).
pandas 3.1.x parses the text exactly under every `float_precision`. So the 83/83 + 5/5 bit-exact result holds on
pandas 3.0.6, which is the box Sunday runs use. On 3.1.1 (CI), 77/83 + 4/5 legs are exact and the rest differ by
1 ulp (2.2e-16). The parser is pinned to `"high"`. `meta.json` records `pandas_version` and `phase4_bit_exact_env`.
The two in-memory-value tests skip off 3.0.6. The engine-run and ensemble text-value tests pass on both versions.

## QB / availability gate
Sources: nflverse `depth_charts_2026.parquet` (ESPN-fed, timestamped `dt` snapshots) and `injuries_2026.parquet`
(official NFL injury reports), pulled by `fetch` with URL, sha256 and retrieved_utc in `sources.json`; optional
inactives CSV (`team, gsis_id, player, source, retrieved_utc`). Starter = lowest-rank QB in the newest snapshot at or
before `--as-of`, skipping Out / Doubtful / inactive. Blocks (p_model left blank -> INSUFFICIENT EVIDENCE):
`qb_not_starter`, `qb_starter_unknown`, `out_or_doubtful` (any position), `qb_starter_thin_history` (< 2 prior games
with >= 10 attempts **for the leg's team**: these engines model a player from his current team's games only).
Every row carries depth/injury source URL and timestamps (`depth_dt`, `depth_retrieved_utc`, `injury_retrieved_utc`).
Live check (fetched 2026-11-13 16:46 UTC): the depth chart lists Kirk Cousins as MIN QB1 with 0 prior MIN games (9 for
LV); his rush legs would be blocked `qb_starter_thin_history`; Murray is QB2 (did not practice), Wentz QB3 (limited).

## Demo: Week 10 TNF WAS@NYG (`demo_w10_WAS_NYG/`)
Committed freeze `freeze_v2_20261113T000135Z.json` -> `legs_from_freeze_v2` -> `run` (as-of 2026-11-12 23:00 UTC)
-> `grade`. 12 rushyds legs, 6 players, all gate ok, 12 p_model filled, engine runtime 1.8 s. Frozen classifier:
STRONG UNDER Daniels U34.5 (p 0.742 vs no-vig 0.499) and McCarthy U15.5 (0.752 vs 0.499); RB legs NO EDGE (carry gate).
ESPN box (`grading/results/sources/espn_summary_2026_10_WAS_NYG_401873052.json`): Daniels 28 (Under wins), McCarthy 34
(Under loses). Run after the game with as-of pre-kick inputs except the injuries file (pulled later): plumbing demo,
not a counted live leg.

## Sunday Week 10 commands (repo root, worktree on this branch)
```bash
# 7:00 AM ET research run (pre-inactives). Uses the Friday final injury report + newest depth chart.
python -m calibration.simv56_pmodel fetch --out /tmp/w10_src_0700
python - <<'PY'
import glob, pandas as pd
from calibration.selective_edge_live import legs_from_freeze_v2
ros = pd.read_parquet("data/historical/nflverse/ros_2026.parquet")
import os
newest = {}
for f in sorted(glob.glob("pregame/price_freezes/2026-11-1[2-6]_*/freeze_v2_*.json")):   # Week 10 game dirs
    newest[os.path.dirname(f)] = f                                                      # newest freeze per game
fs = list(newest.values())
pd.concat([legs_from_freeze_v2(f, ros) for f in fs]).to_csv("/tmp/legs_w10_0700.csv", index=False)
PY
python -m calibration.simv56_pmodel run --legs /tmp/legs_w10_0700.csv --week 10 --sources /tmp/w10_src_0700 --out /tmp/w10_simv56_0700
python -m calibration.simv56_pmodel grade --legs /tmp/w10_simv56_0700/legs_p.csv --out /tmp/w10_simv56_0700/graded

# ~11:30 AM ET re-run (post-inactives for 1:00 PM games): fresh fetch, newest freezes, + inactives CSV.
python -m calibration.simv56_pmodel fetch --out /tmp/w10_src_1130
#   (rebuild /tmp/legs_w10_1130.csv from the newest freezes as above)
python -m calibration.simv56_pmodel run --legs /tmp/legs_w10_1130.csv --week 10 --sources /tmp/w10_src_1130 \
    --inactives /tmp/w10_inactives.csv --out /tmp/w10_simv56_1130
python -m calibration.simv56_pmodel grade --legs /tmp/w10_simv56_1130/legs_p.csv --out /tmp/w10_simv56_1130/graded
```
The snippet keeps only the newest freeze per game. `run` writes `legs_p.csv`, `ensemble.csv`, `qb_starters.csv`, per-engine CSV/JSON and `meta.json`.

Runtime: W8 83 legs 10.5 s total (3 engines in parallel), TNF 6 players 1.8 s -> about 0.1-0.15 s per player; a full
Sunday slate (~100-150 rush legs, ~70-90 players) is well under a minute. Disk: per run ~0.1 MB output + 3.4 MB fetched
parquet (box-local); committed: engines 284 KB + players table 476 KB.

## Embedded provenance (Ghost6 follow-up to PR #44)
The probability files carry their own provenance, so the PR #44 emitter can verify where p_model came from instead
of trusting `--prob-source` / `--qb-override-applied`.

- `run` now also writes `probs/<game_id>.simv56.probs.csv`, one file per game. It uses schema
  `nfl75-simv56-probs/1` (spec at the top of the provenance block in `calibration/simv56_pmodel.py`).
- Each row holds the ensemble `p_under` / `p_over` at a priced line of a gate-ok rush leg, written as `repr()`, so the
  values round-trip exactly.
- Every row carries the same provenance fields:
  - `prob_source=sim_v5_v6_ensemble`
  - `p_model_settings`
  - `code_git_sha`, plus `code_dirty` for the simv56 code paths
  - `code_sha256` of `simv56_pmodel.py`
  - `inputs_sha256`: pbp, players, games.csv, depth chart, injuries, legs, engines `SHA256SUMS`, home spreads, the
    freezes used, and the inactives CSV if given
  - `qb_overrides`: one entry per team in the game. Each entry has the team, the starter and starter gsis, a
    `qb_gate` (ok / qb_starter_unknown / qb_starter_thin_history), prior primary games for that team, the skipped
    QBs, and the depth-chart, injury and inactives source URLs with their retrieved-UTC timestamps, plus `as_of`
  - `generated_utc`
  - `data_sha256`, the digest of the data rows
  - `provenance_sha256`, the digest of the canonical JSON of the fields above
- `ensemble.csv` and `legs_p.csv` carry the same run-level provenance columns. `meta.json` has the full provenance
  block.
- Demo: `demo_w10_WAS_NYG/probs/2026_10_WAS_NYG.simv56.probs.csv`. It was regenerated at code sha 4844e12 (clean),
  and its probabilities are bit-identical to the earlier demo.

Feeding the emitter (the companion draft PR off main teaches `calibration/selective_edge_emit.py` to verify this):

```bash
python3 -m calibration.selective_edge_emit --date 2026-11-15 --freeze <freeze_v2 files> \
  --probs /tmp/w10_simv56_1130/probs --roster <roster parquet> --pbp <pbp parquet>
```

## Remaining blockers / caveats
- **No automated inactives source.** The 11:30 re-run needs an inactives CSV someone produces (gamebook / team PR);
  without it the gate uses the injury report only.
- **NE@DET kicks off 9:30 AM ET (London)**: the 7 AM run is pre-inactives for it and the 11:30 re-run is after kickoff.
- **Week 10 freezes don't exist yet**; legs need real prices and `legs_from_freeze_v2` reads only committed freezes.
- **Depth-chart quality**: the nflverse/ESPN depth chart can be stale or wrong (MIN lists Cousins QB1); the gate fails
  closed on thin history, but a human check of `qb_starters.csv` before trusting labels is still needed.
- `selective_edge_live` CLI (PR #40, frozen) crashes in `graduation()` before any leg is settled (no `win` column)
  after writing `live_graded.csv`; use `simv56_pmodel grade` pre-game. Not fixed here (frozen file).
- Engines' integer-line convention is P(stat >= line) with no push removal (same as the fit); half lines are unaffected.
