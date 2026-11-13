# NFL-75: per-player rushing-yards distribution + P(under L) artifact (research only)

**Research only, not validated. `projection_ready` stays false. 0 Odds API credits. refs NFL-75.**
Engine, production weights, the frozen Phase 4 classifier (`calibration/selective_edge*.py`, `params_w4_7.json`),
`pregame/` and `.github/` are untouched. Golden digests (player box, opportunity, engine) pass unchanged.

## What it is
`pipeline/rush_dist.py` reads the per-trial per-player box lines the engine already records (PR #36) and writes, per
game, for every player with a carry in any trial (QBs, RBs, anyone with rush attempts):

| file | content |
|---|---|
| `<game>.rush_dist.summary.csv` | `game_id, team, player, gsis, position, full_name, n_trials, p_any_carry, carries_mean, mean, sd, min, max, q05, q10, q25, q50, q75, q90, q95` |
| `<game>.rush_dist.cdf.csv` | `game_id, team, player, gsis, position, line, p_under, p_over` on every half-yard line from -20.5 to 250.5 (extended to cover the simulated support); `p_under = P(rush_yds < line)` |
| `<game>.rush_dist.json` | schema `nfl75-rush-dist/1`, game, n_trials, seed, config, pbp, definitions, `research_only: true`, `projection_ready: false`, cdf sha256 |

`rush_yds` = box `rush_yds + kneel_yds` (official stats count kneel-downs as rushes), 0 in trials with no carry.
`rush_dist.p_under(cdf, line=L, team=, player=)` is exact for any line (integer lines also return `p_push`).

## Hand-off to the frozen Phase 4 grader (PR #40)
`selective_edge_live.py` reads a legs CSV with `p_model` = graded-side probability; `legs_from_freeze_v2` leaves it
blank, which the classifier labels INSUFFICIENT EVIDENCE (`model_prob_missing`). `rush_dist.attach_p_model` (CLI
`attach`) fills `p_model` on `market == "rushyds"` rows only, matched by `gsis`, else a unique first-initial.last name
in the game; `p_model = P(side) / (P(under) + P(over))` at the leg line (push removed; equals P(side) on x.5 lines).
It never overwrites a preset `p_model` and only appends `p_model_match`, `p_model_source`. The classifier is not edited.

## Opt-in flag
`python -m pipeline.sim100k --game <id> --write --rush-dist`. Without `--rush-dist` sim100k writes exactly the same
files and bytes as before (test `test_sim100k_rush_dist_flag_is_opt_in`). `--rush-dist` without `--write` is an error;
a refused run writes no rush_dist files.

## Demo: Week 9 BUF@MIN, n = 20,000 (retro smoke test, `run_demo.py`, `demo_table.md`)
Research config built in memory from the Week 10 data_only/NFL-43 template (history W1-8, home MIN). Box
reconciliation 0 failures / 20,000. Actuals: nflverse rushing yards incl. kneels from the committed W1-9 PBP. FanDuel
main lines: historical snapshot in draft PR #41 (no new credits).

| Player | sim p10/p50/p90 | actual | PIT | FD line | model P(under) | FD no-vig under |
|---|---|---|---|---|---|---|
| J.Cook (BUF RB) | 70 / 112 / 164 | 107 | 0.447 | 84.5 | 0.211 | 0.500 |
| J.Allen (BUF QB) | 13 / 37 / 70 | 15 | 0.128 | 30.5 | 0.376 | 0.500 |
| R.Davis (BUF RB) | 0 / 6 / 15 | 2 | 0.234 | 5.5 | 0.464 | 0.515 |
| A.Jones (MIN RB) | 39 / 67 / 102 | 16 | 0.004 | 30.5 | 0.043 | 0.500 |
| J.Mason (MIN RB) | 5 / 21 / 46 | 35 | 0.784 | 47.5 | 0.912 | 0.500 |
| C.Wentz (MIN QB) | 0 / 0 / 4 | 0 | 0.310 | 7.5 | 0.991 | 0.500 |

8 players with an actual: 6 of 8 PITs inside [0.1, 0.9], mean PIT 0.43. One game is a smoke test, not calibration.

**Problems the smoke test shows (must be read before any Sunday use):**
1. **Starter identity comes from history, not the depth chart.** The data_only engine draws rows by the names in W1-8;
   it gives MIN's QB rush share to K.Murray (3.1 carries) and treats C.Wentz, who started, as a backup (0.6 carries).
   Wentz Under 7.5 at 0.991 against a 0.50 market would be a +49 pt "edge" from the classifier: a model artifact.
2. **Player-level means sit far from the market**: Cook 115 vs line 84.5, A.Jones 69 vs 30.5. Model-vs-no-vig gaps of
   25-45 pts are not believable edges; they would flood STRONG UNDER / NO EDGE with noise.
3. **Different model from the frozen fit.** The W4-7 fit and the W8-9 21-6 used `p_model` from the walk-forward sim
   ensemble (sim_v5/v6/v6_fix), not the possession engine. Grading Week 10 with engine probabilities tests a different
   model through the same gates; label it that way.

## Sunday Week 10 run (per game, after the freezes exist)
```bash
# 1. gated 100k (fails closed; writes pipeline/ledgers/<game>.sim100k.{json,player_box.npz} + <game>.rush_dist.*)
python -m pipeline.sim100k --game 2026_10_BUF_NYJ --write --rush-dist
# 2. legs from the committed price freeze (read only), then fill p_model on rush-yd legs
python - <<'PY'
import glob, pandas as pd
from calibration.selective_edge_live import legs_from_freeze_v2
ros = pd.read_parquet("data/historical/nflverse/ros_2026.parquet")
fs = sorted(glob.glob("pregame/price_freezes/*/freeze_v2_*.json"))   # Week 10 freezes only
pd.concat([legs_from_freeze_v2(f, ros) for f in fs]).to_csv("/tmp/legs_w10.csv", index=False)
PY
python -m pipeline.rush_dist attach --legs /tmp/legs_w10.csv --dist pipeline/ledgers --out /tmp/legs_w10_p.csv
# 3. frozen Phase 4 grader (Weeks 10-12 only; freeze manifest checked first)
python -m calibration.selective_edge_live --legs /tmp/legs_w10_p.csv \
    --pbp data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet --out /tmp/w10_graded
```
Timing: sim100k's G4 gate needs official inactives pulled after T-90, so for 1:00 PM ET games step 1 refuses before
about 11:30 AM ET. A 7 AM run of step 1 will refuse by design. If a source already holds a `<game>.sim100k.player_box.npz`,
`python -m pipeline.rush_dist build --npz <npz> --game <game> --pbp <as-of pbp>` rebuilds the artifact alone.
