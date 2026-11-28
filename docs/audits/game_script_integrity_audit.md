# Game-script integrity audit: can the architecture keep three script branches apart?

- **Date:** 2026-11-27 (ET)
- **Repository state audited:** `origin/main` at `ef4cc690`
- **Branch:** `audit/game-script-integrity`
- **Status:** research audit. **Nothing in the engines changed.** No model weights, projections, configs or
  betting-readiness controls were touched. Those controls are `projection_ready`, `source_adapters/tools/run_gate.py`,
  `rocket_gate/`, the release gates and the `rico*_rules`.

## 0. Answer in brief

**No. Today the architecture cannot preserve meaningful differences between the three branches.** It can partition
the outcomes of one simulation by final margin. The engine's behaviour inside a game, though, does not depend on the
score.

- **The engine ignores the score when it picks plays.** The production path is the NFL-43 possession engine that
  `pipeline/sim100k.py` runs. It picks every play from a pool keyed on team, down, distance and field position. The
  score and the clock never enter, so play calling is the same in every branch.
- **The fitted joint producer ignores the score as well.** It has a `score_margin` hook, but its fitted tables are
  conditioned on team and down only.
- **Splitting the trials gives different scores, but the same behaviour.** The scores differ by construction. Pass/run
  mix, pace, player volume, red-zone usage, pressure/coverage and late-game rotation are the same per-play behaviour,
  merely selected.
- **Two places collapse the script before props are priced:**
  - the research board's opportunity model, `dashboard/opportunity.py`
  - an analyst scenario layer, `research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py`
- **What this branch adds:**
  - the scenario-output schema
  - the 100% allocation contract and validator
  - pooling and duplication detectors
  - read-only architecture tests that pin each gap as a strict expected failure

## 1. Scope and constraints

| Asked | Delivered (all new files) |
|---|---|
| Scenario-output schema | `schemas/game_script/scenario_output.schema.json` (JSON Schema 2020-12) + typed mirror `game_script_contract/schema.py` |
| Probability-allocation contract (100%) | `game_script_contract/allocation.py` + `docs/specs/game_script_probability_contract.md` |
| Tests for branch pooling and duplicated outputs | `game_script_contract/tests/` (wired into `scripts/test_offline.sh`, one added line) |
| Standalone report | this file |

**Not done, on purpose:**

- No new simulation engine was built.
- No `tools/sim_v6.py` was created (see §3).
- No existing module was edited. The only edit to an existing file is one `run .  game_script_contract/tests` line
  in `scripts/test_offline.sh`, so CI's offline suite runs the new tests.

**One read-only helper was added.** `game_script_contract/partition.py` groups trials the engine *already wrote*
(`snapshots/*/sim_arrays.npz`) into the three branches. It draws no random numbers and computes no play outcomes. It
exists to show what the current output can and cannot support.

## 2. Inventory: where "script" and "scenario" live today

I searched the repo for: script, scenario, favorite/underdog, leading/trailing, score_margin, spread, margin,
script_adjusted, SCENARIO_ONLY, pooling, and averaging over scenarios. The results below are only the places that
generate or consume game-script behaviour.

| # | Location | What it does with script | Branch-separated? |
|---|---|---|---|
| 1 | `core/possession_engine_v0/simulate.py` `PlayCatalog.sample_snap` (L260–315) | Picks the next play from historical rows keyed `(team, down, dist_bucket, yl_bucket)` (L300). Fallbacks: defense-conditioned, opponent-allowed and goal-line pools (L261–299). **No score or clock in any key.** | No. Every cell pools plays from all game states. |
| 2 | `simulate.py` `_rare_onside` (L1053–1062) → `rare_plays.onside_rate` (`rare_plays.py` L243) | Onside-kick rate by quarter, deficit and seconds. Opt-in (NFL-75 rare plays). | The **only** score-aware behaviour in the engine. |
| 3 | `simulate.py` `_clock_cost` (L20) and the clock map built at L161–191 | Seconds per play by play type (mean of historical deltas). | No. Pace has no score state. |
| 4 | `core/possession_engine_v0/state.py` `add_score` / `period_snapshot` (L63–88) | Keeps per-quarter scoreboards for every trial. | Per-trial quarter scores exist (useful for partitioning). |
| 5 | `snapshots/lock.py` `summarize` (L131–150) | Collapses all trials into one summary: mean points, pooled margin/total percentiles, **mean** halves and quarters (L141–142). | No. One pooled summary. |
| 6 | `pipeline/sim100k.py` `default_engine` (L222–279) | Runs the possession engine for 100k trials, then `L.summarize` (L259). It also returns per-trial player box lines, `player_box_trials` (L277), which `--write` saves to `.npz`. | Summary pooled. Per-trial lines kept, so a partition is *possible*. |
| 7 | `core/possession_engine_v0/player_box.py` `summarize` (L320–330) | Per-player mean/median/p10–p90 over **all** trials. | No. |
| 8 | `core/possession_engine_v0/joint_producer.py` `OpportunityModel.context` (L106–109) and `matches` (L55–65) | The context passed to usage-cell matching includes `score_margin`, and cells can condition on `_min`/`_max` ranges. | **Capable**, but unused (row 9). |
| 9 | `core/possession_engine_v0/fit_prospective_usage.py` L77 | The fitted usage cells are `when: {team_id, down}` with `'pooling': '... distance/field/score/period deliberately unconditioned'`. The committed `runs/**/model.json` files carry only `down` and `team_id` keys. | No. |
| 10 | `joint_producer.py` `role` (L123–138) | Target/carry rotation by **half** (`rotation_by_half`, L127), not by score state. | No. |
| 11 | `joint_producer.py` `missing_features` (L28–37) | `coverage` is `UNKNOWN`; routes and personnel are `MISSING` (`allows_sim_effect: False`). | Coverage not modeled. |
| 12 | `joint_producer.py` `write_forecast` (L469–481) | Writes every trial to `trials.jsonl`. | Per-trial joint output kept. |
| 13 | `core/possession_engine_v0/joint_inputs.py` L123, L211–215 | Allows `mode ∈ {data_only, script_adjusted, market_informed}`. SCENARIO inputs require a separately labelled `script_adjusted` run. | One scenario per run. No 3-branch structure or probabilities. |
| 14 | `core/possession_engine_v0/config/jax_bal_tnf_2026-11-05_script_adjusted.json` (with `adjustment_ledger.py` L52) | "script_adjusted" here means QB/injury availability edits. It is not a game-script branch. | No. |
| 15 | `core/period_engine_v0/monte_carlo.py` (docstring L1–10, `simulate_game` L78) | Bootstraps each team's quarter scoring vectors from as-of games, home/away pooled, plus a shared game shock. | No branches. Quarter vectors are independent of the opponent's game state. |
| 16 | `dashboard/opportunity.py` `script_multipliers` (L233–238), used in `board_side` (L278, L282–283) | Turns the implied margin into **one** deterministic pass and rush multiplier (`SCRIPT_PASS`, `SCRIPT_RUSH`, L210–211). Team attempts are scaled by it, and then player volume is simulated around that single expectation. | No. **The script is collapsed to its expectation before props are priced.** |
| 17 | `research/runs/2026-11-12_TNF_WAS_NYG_layers/script_layer.py` | Three named scenarios with weights 0.50/0.25/0.25 (`S`, L8–11). `W` averages their scores by weight (L13). Markets are then priced from `norm.cdf(·, m, SDm)` on that **pooled** margin (L17–21). | No. **Pooled before pricing.** Labelled "ANALYST READ", with no edge computed (header L1–5). |
| 18 | `research/third_down/mnf_week9_route_opportunity_scenarios.py` `SCENARIOS` (L39–44) | Four named volume scenarios (low volume, competitive, trailing pass-heavy, protection) with **no probabilities**, by design ("NO fitted probabilities", L172). | Kept separate, but cannot be allocated to 100%. |
| 19 | `calibration/simv56/engines/cc_sim_v6.py` (vendored sim_v6 copy) L95–134 | In `gr` mode only, draws a continuous margin per trial, `Mg ~ N(−spread, 13.5)` (L106), and scales team volume by `exp(b·(Mg+spread))`. `mc` and `bias` ignore script (L101). The output per mode is pooled mean/median/p10/p90/rungs (L133). | No. Continuous script inside one pooled distribution. |
| 20 | `cc_sim_v6.py` `rb_script_trigger` / `rb_script_boosts` (L139–145) | A favorite-spread ≤ −7 rule that applies one carry boost to every trial. | No. A single-state adjustment. |
| 21 | `calibration/simv56_pmodel.py` (docstring L5–7, L231) | `p = mean(p_mc, p_bias, p_gr)`, with an ensemble across engines. | A model ensemble, not branch pooling (see the spec, §3). |
| 22 | `pregame/packet.py` L159, L407 | States outright: "role changes and game script are not applied: the analyst must adjust for them." Phase 6 is `PARTIAL`: "The script call itself is the analyst's." | Script is manual. |

## 3. sim_v6 is absent from the repository

- **It is required in two places:**
  - `source_adapters/tools/run_gate.py` L34 and L173–174 require runs dated ≥ `SIMV6_FROM` to name
    `tools/sim_v6.py` as the sim script.
  - `workflows/operational_specs/PHASE_SCRIPT.md` L15 and L118 describe the "three-model consensus with
    tools/sim_v6.py".
- **The file does not exist:** there is no `tools/` directory at `ef4cc690`.
- **The closest code is a vendored copy.** `calibration/simv56/engines/cc_sim_v6.py` (header L1: "SCRATCH COPY for
  confidence_check_2026-11-03 (originals untouched)") and `cc_sim_v6_fix.py` are vendored copies used for p_model
  backtests. They are sha256-pinned by `calibration/simv56_pmodel.py`.
- **This audit left all of it alone.** It did not create, restore or modify any sim_v6 code. Row 19 describes the
  vendored copy's script handling from its source only.
- **The absence is pinned by a test:** `test_sim_v6_is_referenced_but_absent_and_documented`. It skips with a
  "re-audit" message if `tools/sim_v6.py` ever appears.

## 4. Where pooling or duplication happens, or could happen

1. **Inside play selection (structural pooling).** Every `PlayCatalog` cell (row 1) mixes plays from all score states:
   leading, trailing, garbage time and two-minute drill. A trial that is "favorite up 17 in Q4" draws plays from the
   same pool as a tied Q1. This is where branch differences get averaged away, *before* any summary.
2. **Measured in committed runs.**
   - **What I measured:** in the 28 committed 100k snapshots (`snapshots/*/*/sim_arrays.npz`), the correlation between
     the margin after Q3 and the Q4 margin is −0.011 to −0.043 (median −0.027).
   - **The real-game baseline:** for real 2022 regular-season games (`data/historical/nflverse/pbp_2022.parquet`,
     n = 271), the same correlation is **−0.234**. Trailing teams outscore leaders in Q4.
   - **What it means:** the engine's Q4 barely reacts to game state.
   - **How it is pinned:** `test_engine_q4_scoring_responds_to_game_state_like_real_games` (strict xfail). The test
     recomputes both numbers.
3. **In summaries.** `lock.summarize` (row 5) and `player_box.summarize` (row 7) report pooled means and percentiles.
   A consumer that prices props from those numbers is pricing a pooled line.
4. **In the research board.** `dashboard/opportunity.py` (row 16) feeds a single script multiplier into team attempts.
   Then it draws player volume with gamma-Poisson around that one expectation. The branch spread in team volume
   (blowout vs comeback) is replaced by the one expectation, so tail probabilities (80+ yards, 7+ catches) are
   computed from a pooled opportunity line.
5. **In the analyst scenario layer.** `script_layer.py` (row 17) prices from the weighted-average margin. Using its
   **own** inputs (weights 0.50/0.25/0.25, scores 21–18 / 27–14 / 17–23, SD 13.5):

   | Market | Pooled normal | Proper mixture | Difference |
   |---|---:|---:|---:|
   | NYG −1.5 | 0.5516 | 0.5451 | 0.65 pp |
   | NYG −2.5 | 0.5222 | 0.5189 | 0.32 pp |

   The gap is small for sides here. For player tails, the error from pooling volume is larger. The file is labelled
   an analyst read, with no edge computed, so this is a pattern to avoid, not a production defect.
6. **Duplication risks.** No current code emits three branch objects, so no duplicated branch output exists today.
   The risk is in future adapters: copying one branch's dict into another, sharing list objects, or filling an
   unmodeled dimension with the pooled value. The new detectors catch each of these (§6).

## 5. The ten dimensions: branch-aware now, derivable, or missing

Key:

- **Modeled:** the engine's behaviour depends on game state.
- **Derivable:** per-trial output exists, so partitioning trials by branch gives branch-specific distributions, but
  the per-play behaviour is the same in every branch.
- **Missing:** no output.

"Possession engine" means the `sim100k` path.

| Dimension | Possession engine (production research path) | Joint producer | Evidence |
|---|---|---|---|
| Score distributions | **Derivable** (`fg_*` per trial) | Derivable (`trials.jsonl`) | `state.py` L63–88. Committed `.npz` keys. `partition.py`. |
| Quarter-by-quarter scoring | **Derivable** (`q1..q4_*` per trial), but Q4 is ~independent of game state (§4.2) | Derivable | npz keys. Correlation test. |
| Plays and possessions | Derivable only via `player_box_trials` team `plays` (not saved in snapshots) | Derivable | `sim100k.py` L277. `player_box.py` `TEAM_ONLY_STATS`. |
| Pass/run distribution | Derivable as counts. **Not modeled:** play choice ignores score (`sample_snap` L300) | Not modeled: usage cells are `team_id, down` only (`fit_prospective_usage.py` L77) | xfail tests 1–2 |
| Team pace | **Not modeled:** clock cost by play type only (`_clock_cost`, L161–191) | Clock from model tables, no score state | `simulate.py` L20, L161–191 |
| Player targets / receptions / carries / rush opps | Derivable via `player_box_trials` (`targets`, `rec`, `carries`). Who gets the ball comes from the sampled historical row, not from game state. | Derivable. Rotation by half only (L127). | `player_box.py` L36–39. `joint_producer.py` L123–138. |
| Red-zone opportunities | Derivable in principle (yard line is in state), but the player box does not record red-zone splits. **Missing** as output. | Missing as a field | `player_box.py` `PLAYER_STATS` has no RZ fields |
| Touchdown opportunities | TDs derivable (`pass_td`, `rec_td`, `rush_td`). Inside-10 opportunities **missing**. | TDs derivable | `player_box.py` L36 |
| Pressure and coverage changes | Blitz strata (opt-in) condition called-pass outcomes on blitz rate, with no score state (`simulate.py` L1599–1615). Coverage **missing**. | Coverage `UNKNOWN` (`missing_features`, L28–37) | config `effects.semantics: "conditions called-pass outcome only"` |
| Late-game substitution / rotation | **Missing.** No starter-rest or score-state snap model. Player identities come from historical rows. | Rotation by half only; no score state | `joint_producer.py` L127 |

**Summary:**

- **Modeled:** none of the ten dimensions is modeled branch-aware today.
- **Derivable by partition:** score and quarter scoring. Plays, pass/run counts, player volume and TDs too, when
  `player_box_trials` is saved.
- **Missing as outputs:** pace by state, red-zone and inside-10 opportunity splits, coverage, and late-game rotation.

## 6. What the new contract and tests do

**Schema.** Exactly three branch objects. Every one of the ten dimensions has a `dimension_status` of `modeled`,
`derived` or `not_modeled`, and every distribution must carry samples or a pmf. A missing dimension is null with a
reason. It is never filled in.

**Allocation and pricing.**

- Exactly the three ids.
- Each probability finite and in [0, 1]; the sum within 1e-6.
- For trial partitions, counts must match the probabilities.
- `prop_probability` mixes per-branch conditionals, and refuses rather than borrowing another branch.
- `check_prop_probability` flags pooled-line, point-estimate and single-branch prices.

**Pooling detectors.** Identical distributions in all branches, collapsed means, score samples that violate their
branch definition, branches out of order, and a warning for derived-only behaviour.

**Duplication detectors.** The same branch object reused, shared sub-objects, identical payloads (also when only id
and probability differ), near-identical payloads within a tolerance, and a dimension copied between branches.

**Architecture tests** (`test_existing_architecture.py`, read-only). Five pass and record what the architecture *can*
carry (a sixth passing test, `test_script_layer_pooling_changes_the_price`, quantifies §4.5):

- the sim_v6 absence check
- the `score_margin` hook
- per-trial joint output
- per-trial sim100k arrays
- a valid 3-branch partition of the committed CIN@WAS run

The CIN@WAS partition (favorite = CIN by engine mean margin, 8.7 pts; final margin ±9):

| Branch | Probability | Note |
|---|---:|---|
| A | 0.501 | |
| B | 0.383 | |
| C | 0.116 | first 5,000 trials in the test; 100k in the table |

Eight **strict xfails** each pin a verified gap. Each one fails on an assertion today (checked with `--runxfail`). Each
will XPASS, and fail the suite, once its gap is fixed, which forces this report to be updated.

| xfail test | Finding |
|---|---|
| `test_possession_engine_play_selection_conditions_on_game_state` | `sample_snap` has no score or clock |
| `test_fitted_usage_cells_condition_on_score_margin` | Fitted usage cells use only `team_id`, `down` |
| `test_engine_q4_scoring_responds_to_game_state_like_real_games` | Sim correlation −0.027 vs real −0.234 |
| `test_engine_summary_emits_three_branch_blocks` | `lock.summarize` pools everything |
| `test_board_prices_player_volume_per_branch` | `script_multipliers` returns one tuple, e.g. `(0.9813, 1.0275)` at +7 |
| `test_script_layer_prices_from_branch_distributions` | Weighted-mean margin, then a normal CDF |
| `test_mnf_route_scenarios_carry_branch_probabilities` | Four scenarios, no probabilities |
| `test_simv56_engine_returns_branch_separated_rungs` | Continuous margin inside one pooled output |

**Run:**

```
pip install -r requirements-test.txt
python3 -m pytest -q game_script_contract/tests        # this suite
bash scripts/test_offline.sh                           # everything, as CI does
```

## 7. Gaps, in priority order

1. **The engine ignores game state when picking plays.** This is the root cause. Until play selection (or usage
   cells) is conditioned on score margin × time remaining, branches can only select trials. They cannot change pass
   rate, pace, player volume or rotation.
2. **Outputs are pooled.** `lock.summarize` and `player_box.summarize` give one pooled summary. Snapshots save
   per-trial *scores* but not per-trial *player lines*, so player branches cannot be rebuilt from snapshots.
3. **The board collapses the script.** `dashboard/opportunity.py` prices from a single expected-script multiplier.
4. **The scenario layers don't meet the contract.** The analyst layers either pool (`script_layer.py`) or carry no
   probabilities (MNF route scenarios).
5. **Several dimensions have no output.** Red-zone/inside-10 opportunity splits, coverage, pace by state, and
   late-game rotation.
6. **Branch C's meaning is ambiguous** (see the spec, §1). It needs an owner decision.
7. **sim_v6 is missing.** `tools/sim_v6.py` is required by the run gate but absent, so the gate's sim_v6 rule cannot
   be satisfied from this repository.

## 8. Recommended follow-ups (not implemented; each needs its own review)

These are ordered.

1. **Decide the branch definitions.** Settle branch C's reading, the thresholds and the classifier point (final vs
   end of Q3). The favorite source should be the price freeze's market spread. Record the decision in the spec.
2. **Save per-trial player lines with every snapshot.** `sim100k --write` already produces them. Then build the
   branch payload with `game_script_contract.partition` (extended to player columns). That gives honest `derived`
   branches for score, quarters, plays, pass/run counts, player volume and TDs, with no engine change.
3. **Price props per branch, then mix.** Swap any pooled-summary price for `prop_probability`, and gate it with
   `validate_payload`. This should go through the normal NFL-49 / readiness process, because it changes what
   consumers read.
4. **Score-state conditioning (engine work, needs Rico's approval).** Add score-margin × time buckets to usage cells
   (`fit_prospective_usage.py`; `joint_producer.matches` already supports `_min`/`_max`), or to `PlayCatalog` keys
   with explicit sparse-cell fallbacks. Validate it against the real Q4 correlation (−0.23 in 2022) and the real
   pass-rate-by-margin curves. The xfails in §6 turn into passes when this lands.
5. **Board and analyst layers.** Replace `script_multipliers` with per-branch attempts, and replace the weighted means
   in `script_layer.py` with per-scenario pricing plus a mixture. Give the MNF scenarios probabilities, or label them
   as non-allocatable sensitivity cases.
6. **Missing outputs.** Add red-zone/inside-10 opportunity columns to `player_box`. Add coverage only once a sourced
   charting feed exists. Late-game rotation needs snap-count data split by score state, which the engine does not
   use today.
7. **Restore or retire sim_v6.** Either restore `tools/sim_v6.py` from its original source, or update the run gate and
   PHASE_SCRIPT to name the engine actually in use. That is the owner's call. This audit did neither.

## 9. Test results

See §6 for the commands. The results at commit time are reported in the pull-request description.

- New suite: 67 tests. 59 pass and 8 are strict xfail (expected failures that record findings).
  - The 53 contract tests (allocation, schema, prop mixture, pooling, duplication) all pass.
  - The 14 architecture tests are 6 passed and 8 strict xfail.
- Full `scripts/test_offline.sh`: see the PR description.
