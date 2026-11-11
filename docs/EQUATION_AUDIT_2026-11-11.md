# Equation audit, 2026-11-11

Every formula below was checked against its stated purpose, either algebraically or by simulation against
the bundled 2025 and 2026 play-by-play. The audit covers the period engine (`core/period_engine_v0`),
the possession engine (`core/possession_engine_v0`), market no-vig and the MNF joint Monte Carlo
(`research/third_down`). Weeks 1–8 of 2026 were already inspected during development, so the measured
differences are development evidence, not a holdout result. Nothing here changes `projection_ready`
(still false).

## Verified correct (no change)

| Formula | Where | Check |
| --- | --- | --- |
| Spread grade: cover iff margin + line > 0, push iff = 0 | `settlement.settle_spread_2way` | Algebra; docstring examples hold |
| Total / team total grade, push on the exact line | `settlement.settle_total_2way` | Algebra |
| `p_win_decisive = p_win / (1 − p_push)` | `monte_carlo.raw_probs_from_sim` | Equals P(win given no push) |
| Brier score `mean((p − y)^2)` and log loss with eps clipping | `walkforward.py`, `market_calibration/calibration.py` | Standard definitions |
| American price to implied probability | `market.american_to_implied` | +150 → 0.400, −150 → 0.600, ±100 → 0.5 |
| Multiplicative no-vig `q_i / sum(q)` | `market.novig_two_way` / `novig_three_way` | Sums to 1 |
| Missed field goal: defence takes over at the kick spot (LOS + 7), or at its 20 | `simulate._missed_fg_recv_yl` | `min(80, 100 − (yl + 7))` matches the rule |
| Field-goal distance = yardline_100 + 18 | `simulate._attempt_fg` | Same convention as nflverse `kick_distance` |
| Turnover, turnover-on-downs and punt field flips `100 − spot` | `simulate._apply_snap` | Algebra |
| Lognormal shock `lognormal(−σ²/2, σ)` has mean 1 | `monte_carlo`, MNF script | E[S] = exp(μ + σ²/2) = 1 |
| MNF TD/FG Poisson split keeps the mean: `7·(0.72e/7) + 3·(0.28e/3) = e` | `mnf_20261109_joint_monte_carlo.draw_qscores` | Algebra (but see dispersion below) |

## Fixed: equations that did not do what they were meant to

### 1. Game-randomness (GR) shock double-counted variance (period engine)

The GR branch multiplies both teams' bootstrapped points by one shared shock S with
`CV(S) = CV(team points)`. The bootstrap already carries all of that variance. For independent h, a with
E[S] = 1 and cv = σ/μ:

- Var(h·S) = σ²(2 + cv²), so each team's SD grows by √(2 + cv²) ≈ 1.47×.
- corr(h·S, a·S) = 1 / (2 + cv²) ≈ 0.47.

In the data, team regulation points have SD 9.8 and corr(home, away) = −0.004. Within quarters the
correlation is negative (Q1 −0.10, Q2 −0.16, Q3 −0.10): one team's long drive takes possessions from the
other. Simulated BAL–JAX: SD 10.3 → 14.6 and corr 0.47 with GR on.

**Change:** the default `gr_scale="within_game_covariance"` sizes the shock so that it adds exactly the
observed same-game covariance: `Var(S) = max(0, Cov(scored, allowed)) / (mean scored · mean allowed)`.
On 2025–2026 data that covariance is ≤ 0, so the shock is correctly off. `gr_scale="legacy_total_cv"`
reproduces old runs. Tests: `tests/test_equation_audit.py`.

### 2. Kickoffs always started at the own 25 (possession engine)

Every kickoff (opening kick, after a TD, FG or safety, at halftime and in OT) placed the receiving team
at yardline_100 = 75. Since the 2025 rule change, touchbacks come out to the 35 (yl 65). Real drives
after a kickoff start at a mean yardline_100 of 69.2 (2025) and 69.4 (2026), about 6 yards better.

**Change:** `PlayCatalog.kickoff_starts` holds the receiving team's first-snap yardline after each as-of
kickoff in the configured games. `simulate_one` samples from it (`cfg["kickoff_start"]`, default
`"empirical"`; `"fixed_75"` restores the old behaviour). Measured with the data-only configs, 800 games each:

| Game | Real total (team averages) | Fixed own 25 | Empirical kickoffs | Punts: real / old / new |
| --- | --- | --- | --- | --- |
| JAX @ BAL | 50.4 | 38.9 | 41.8 | 7.82 / 8.40 / 7.81 |
| DAL @ IND | 47.5 | 35.7 | 37.7 | 5.50 / 6.43 / 6.05 |

Field-goal attempts also moved toward reality (2.85 → 3.11 and 4.56 → 4.74). Tests: `tests/test_kickoff_start.py`.

### 3. Odds validation (market)

`american_to_implied(-50)` used to return 0.333, but a price between −100 and +100 is not a valid
American price. It now raises a `ValueError`.

## Added: optional improvements (default behaviour unchanged)

- **`simulate_game(..., sampling="matchup_pair")`, period engine.** Each trial draws one real as-of game:
  with probability ½ from the home team's games (home = scored, away = allowed), otherwise from the away
  team's games. This brings in the opponent's defence (home mean = average of home offence and away
  defence allowed) and keeps real within-game structure: negative quarter correlation, key numbers and
  tie rates. `compare_sampling.py` writes `artifacts/sampling_comparison_2026_w1_8.json`. Highlights,
  independent → matchup_pair:

  | Period | Total MAE | Margin MAE | Home-win Brier | Model tie % vs actual |
  | --- | --- | --- | --- | --- |
  | Q1 | 4.71 → 4.40 | 4.87 → 4.75 | 0.260 → 0.243 | 24.1 → 22.7 (21.5) |
  | Q3 | 5.20 → 4.99 | 5.23 → 5.20 | 0.240 → 0.241 | 22.0 → 19.3 (18.2) |
  | Regulation | 11.59 → 11.00 | 9.99 → 9.59 | 0.244 → 0.239 | 3.7 → 5.5 (9.1) |
  | Final | 11.78 → 11.23 | 10.07 → 9.75 | 0.243 → 0.235 | 0.2 → 0.3 (0.8) |

  Q2 and Q4 home-win Brier and the regulation 3-way log loss got worse, so it stays opt-in until it is
  confirmed on weeks 9 and later.
- **`novig_two_way(..., method="power")`**: `p_i = q_i^k` with k chosen so the probabilities sum to 1.
  It takes more margin from long shots than the proportional method (−400/+300: 0.238 → 0.218 for the dog)
  and is identical on evenly priced markets.
- Settlement in `raw_probs_from_sim` is vectorised. The results are identical to the scalar rules (tested),
  and it is much faster at 100k trials.

## Tried and rejected

**Shrinking sparse 4th-down cells toward the pooled (field position × distance) cell.** This raised go-for-it
attempts on JAX @ BAL from 1.41 to 2.17 per game (real: 1.71) and lowered FG attempts. It was not kept.

## Open: known remaining gaps

1. **Possession engine scores 9–10 points per game too few, even with the kickoff fix.** The biggest missing
   piece is penalties: in 2026, defensive penalties give offences 53.8 yards per game, with automatic first
   downs, and the engine has none (NFL-43). The engine also runs about 116 offensive snaps per game
   against 123 real, and has no end-of-half field goals before 4th down and no return or defensive TDs.
2. **Overtime.** A field goal on the first OT possession ends the game in the engine. The 2025 regular-season
   rule gives both teams a possession.
3. **Two-point tries.** Every TD is followed by a kick. In 2026, 58 two-point tries were made against 553 kicks
   (9.5%, 55% successful). The expected value is similar to a kick, but the score distribution around key
   numbers is not.
4. **MNF joint Monte Carlo dispersion.** The Poisson TD/FG process gives Var(points) ≈ 5.88·mean, an SD of
   11.6 at 22.8 points, while the real team-points SD is 9.8. That is about 18% too wide, which overstates
   tail outcomes (big overs and unders, blowout spreads). A fixed number of drives (about 11 per team) with
   a multinomial TD/FG/none outcome per drive bounds the count and matches the observed spread better. The
   script is a dated research record, so it was left unchanged.
5. **Independent bootstrap (default period sampler).** It ignores the opponent's defence and home field,
   weights a 2025 game the same as last week's, and has no shrinkage for teams with few as-of games. The
   matchup_pair sampler addresses the first point. Recency weights and shrinkage toward the league are
   the next candidates.
