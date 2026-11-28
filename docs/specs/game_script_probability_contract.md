# Game-script probability-allocation contract (v2)

Status: research contract. It does not change any engine, model weight, projection, or betting-readiness control
(`projection_ready`, run gates, rocket gate and release gates are untouched). Code: `game_script_contract/`.
Schema: `schemas/game_script/scenario_output.schema.json`. Audit: `docs/audits/game_script_integrity_audit.md`.

## 1. Branches

There are exactly three branches per game. They are always these three, with these ids. **Branch C is the underdog
trailing and chasing, not the underdog leading.** That owner decision was recorded on 2026-11-27 (ET).

Margins are favorite points minus underdog points. The classifier (`q3_lead_held_or_chased`) uses only two
checkpoints the engine already records: the score at the end of Q3, and the regulation score (end of Q4). Mid-quarter
swings and overtime are not inputs.

| id | Name | Default rule (thresholds are data in every payload) |
|---|---|---|
| `favorite_controls` | A. Favorite controls the game | `m_q3 >= q3_control_margin` AND `m_reg >= q4_hold_min_margin` |
| `underdog_chases` | C. Underdog chases the game | `m_q3 >= q3_control_margin` AND `m_reg < q4_hold_min_margin` (equivalently `m_reg <= one_score_max_deficit`) |
| `competitive` | B. Competitive game | `m_q3 < q3_control_margin` — everything else, **including games the underdog leads** |

Defaults: `q3_control_margin = 9`, `q4_hold_min_margin = 9`, `one_score_max_deficit = 8` (a deficit of 8 or fewer is
"within one score", because a touchdown plus a two-point conversion ties). Those two hold/one-score numbers must
satisfy `q4_hold_min_margin = one_score_max_deficit + 1`.

In words:

- **A.** The favorite leads by two scores at the Q3 gun and still leads by more than one score at the Q4 gun (lead
  held). The underdog never gets within one score *as observed at the end of Q4*.
- **C.** The underdog trails by two scores at the Q3 gun and cuts the deficit to one score or less in Q4, including
  ties and taking the lead. A Q4 comeback that ties is C even if the favorite then wins in overtime.
- **B.** Everything else. This includes close games and every game the underdog leads at the end of Q3. Underdog-ahead
  by 9+ at the end of Q3 is a documented **sub-case of B**, carried in the optional `competitive_composition` block. It
  is not a fourth branch and must not enter the probability allocation or the prop mixture.

The A/C split is complementary given the same Q3 precondition, so the three branches are mutually exclusive and
exhaustive: every trial lands in exactly one. Flipping who is the favorite sends A (and C) into B, never into C — C
is not A seen from the other sideline.

Why end of Q3, not also "led at half": the engine does not record mid-quarter scores, and a favorite that pulls away
in Q3 still controls the game entering Q4. Requiring a half lead would mix those games into B. "Through the end of
Q3" is the score at the Q3 gun.

Limitation (must be stated in `branch_definition.limitations`): a lead that briefly tightened inside Q4 and then
re-opened is still A, because only the Q4 gun is observed.

The payload must name the favorite and say where it came from (`favorite_source`, for example `market_spread_close` or
`engine_mean_margin`). `competitive_includes_underdog_ahead` must be true. `observation_points` must be
`["end_q3", "regulation"]`.

## 2. Allocation rules (validate_allocation)

1. **Exactly three branches.** The keys must be exactly the three ids above. A missing branch is an error, and so is
   an extra branch (for example a fourth `garbage_time` branch, even at probability 0). JSON with a duplicated key is
   rejected by `loads_strict`, because a plain JSON load would silently keep only the last value.
2. **`branch_id` matches its key.**
3. **Valid probabilities.** Each probability must be a finite real number in [0, 1]. Booleans, strings, null, NaN and
   ±inf are errors.
4. **No offsetting.** A negative probability is an error even when the three still add to 1.
5. **Total of 100%.** `|P(A) + P(B) + P(C) − 1| <= 1e-6` (`TOLERANCE`), summed with `math.fsum`.
6. **Counts match probabilities.** When `probability_basis == "trial_partition"`:
   - `sum(n_trials) == n_trials_total`
   - `|P(b) − n_trials(b)/n_trials_total| <= 1e-6` for every branch.

## 3. Prop probabilities (prop_probability)

```
P(prop) = Σ_b P(b) · P(prop | b)
```

- **Each branch uses its own distribution.** `P(prop | b)` comes only from branch `b`'s distribution for that
  player/team stat, using its per-trial `samples` or its `pmf`.
- **Over, under and push.** Over is `P(X > line)` and under is `P(X < line)`. A push (`X == line`) is reported
  separately.
- **Refusals.** If a branch with `P(b) > 0` has no distribution for the stat, pricing raises `ContractError`. It never
  borrows another branch's distribution and never falls back to a pooled line.
- **Forbidden: pricing from an averaged stat line.** That means computing `μ = Σ_b P(b)·mean_b` and then evaluating
  `P(X > line)` under any single distribution centred on `μ` (Poisson, normal, an indicator, …).
  `check_prop_probability` flags a reported probability that differs from the mixture. It names the pattern the number
  matches: Poisson(pooled mean), indicator(pooled mean vs line), or a single branch only.
- **Mixing models is a separate step.** Averaging probabilities across different models (for example
  `calibration/simv56_pmodel.py` averaging `p_mc`, `p_bias` and `p_gr`) is a model ensemble, not a branch mixture. If
  branches are adopted, each model's branch mixture is computed first, and the ensemble is taken afterwards.

## 4. Integrity rules (validate_payload)

- **JSON Schema.** The payload must pass `schemas/game_script/scenario_output.schema.json`.
- **Distributions must be priceable.** Every distribution carries `samples` or a `pmf`. A point estimate alone fails
  the schema.
- **`dimension_status` per branch, for all ten dimensions:**

  | Status | Meaning | Field rule |
  |---|---|---|
  | `modeled` | The engine's behaviour depends on branch state | Fields must be non-null; null → `MISSING_DIMENSION_OUTPUT` |
  | `derived` | Trial selection from a game-state-blind engine | Fields must be non-null; null → `MISSING_DIMENSION_OUTPUT` |
  | `not_modeled` | No output | Fields must be null; a value → `FAKED_DIMENSION` |

- **Same teams and players in every branch.** `TEAM_SET_MISMATCH`, `PLAYER_SET_MISMATCH` or `PLAYER_DUPLICATED`
  otherwise.
- **Samples come from the branch's own trials.** For a trial partition, each `samples` array has length
  `n_trials(branch)`, aligned by trial (`SAMPLE_COUNT_MISMATCH` otherwise).
- **Pooling detectors** (`detect_branch_pooling`):
  - `BRANCH_DISTRIBUTIONS_IDENTICAL`: all three branches carry the same distribution.
  - `BRANCH_MEANS_COLLAPSED`: the shapes differ, but all three share one mean.
  - `SCORE_OUTSIDE_BRANCH`: a branch's score trials violate its own definition.
  - `BRANCH_ORDER_VIOLATION`: the mean regulation margin for A (lead held) is not above C (lead cut). A > B > C on final margin is not required: B includes underdog-ahead games, so C's mean is often above B's.
  - `DERIVED_NOT_MODELED` (warning): a behavioural dimension is only a trial selection.
- **Duplication detectors** (`detect_duplicate_branches`):
  - `SHARED_BRANCH_OBJECT` / `SHARED_SUBOBJECT`: the same Python object is referenced by two branches.
  - `IDENTICAL_BRANCH_PAYLOAD`: equal apart from `branch_id`, `probability` and `n_trials`.
  - `NEAR_IDENTICAL_BRANCH_PAYLOAD`: every numeric value matches within `rel_tol`.
  - `DUPLICATED_DIMENSION`: every distribution of one dimension is identical across two branches.
  - `DUPLICATED_FIELD` (warning): a single distribution is identical across two branches.

## 5. Dimension → fields

| Dimension | Team fields | Player fields |
|---|---|---|
| score_distribution | points | |
| quarter_scoring | quarter_points.q1–q4 (+ot) | |
| plays_possessions | plays, possessions | |
| pass_run | pass_attempts, rush_attempts | |
| pace | sec_per_play | |
| player_opportunity | | targets, receptions, carries, rush_opportunities |
| red_zone | red_zone_trips | red_zone_targets, red_zone_carries |
| touchdown_opportunity | touchdowns | td_opportunities |
| pressure_coverage | pressure_rate_faced, coverage_mix_faced | |
| late_game_rotation | starters_rested_prob | snap_share_q4 |

## 6. Known limits of the detectors

- **Some pooling only shows up with aligned samples.** Suppose one branch silently carries the pooled distribution of
  a stat while the other two branches are genuine. The detectors catch this when the branch carries aligned per-trial
  samples (sample count and score-partition checks). They cannot prove it from a `pmf` alone.
- **`derived` versus `modeled` is declared, not proven.** The validator cannot tell from a payload whether behaviour
  truly depends on game state. The architecture tests in `game_script_contract/tests/test_existing_architecture.py`
  check that against the engine code itself.
