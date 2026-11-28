# PROPOSAL (not applied): mismatch conviction score, strong read vs soft lean, opportunity ceiling board

Status: **proposal only**, for Rico's review. refs NFL-47. Nothing here is live. It does not change a betting rule, a
gate, a skill, a weight or `projection_ready` (stays false). It does not loosen the verified-defender rule; that
change is a separate pending approval. Weights are the mission file's starting weights and are **uncalibrated** until
the validation in section 5 runs and passes.

## 1. Hard rules come first

The score never overrides these. A leg that fails one is PASS whatever its score:

- `projection_ready` false: everything is research, not a pick. Ghost6 VETTED is required before anything is called a pick.
- No passing-yards legs.
- RB projected under 50% of team carries: do not play.
- Receiving legs: the current verified-main-defender rule applies until Rico approves a change.
- Never pair a game-total under with same-game player overs.
- Weather data only from NWS and Open-Meteo; no PFF paid content.

## 2. Mismatch conviction score (0-100)

Each component is scored 0-1 from data we already hold, multiplied by its weight, summed, times 100.

| Component | Weight | How it is scored (all inputs dated before kickoff) |
|---|---|---|
| Defensive matchup | 25 | Percentile (0-1, 1 = most allowed) of the defense's **opponent-adjusted** per-game allowance for the player's group and stat (`allowances_windows.csv`, `_oa_pg`), average of season and L5. Receptions legs use `rec_oa_pg`; yards legs use `yds_oa_pg`; rushing legs use `rb_rush_yds_oa_pg`. Fewer than 6 defense games: component capped at 0.5 |
| Opportunity and usage | 25 | Player's target share (WR/TE) or carry share (RB) percentile within position, average of season and L5 with the current QB (`data/scheme_profiles`, nflverse pbp). Below the opportunity floor (WR/TE share < 15%, RB carries < 50%): component = 0 |
| Recent production | 15 | Median (not mean) of the player's last 5 games for the leg's stat, divided by the line, mapped to 0-1 with 1.0x line = 0.5. The median stops one big game from carrying the score |
| Coverage / scheme compatibility | 15 | Sharp man rate and MOFC for the defense (season and L5 from `sharp_defense_windows.csv`) against the player's own man/zone or single/two-high split **if a free dated source has it**. Today no free 2026 source gives player splits by coverage, so this component is scored 0.5 (neutral) and flagged UNKNOWN |
| Weather and game script | 10 | Weather category (see WEATHER_CATEGORIES_PROPOSAL.md) and the frozen-price script label: 1.0 when both favour the leg's volume, 0.5 neutral, 0 when either works against it |
| Personnel and injury | 10 | Official injury report and inactives with source times: 1.0 when a teammate's absence adds volume, 0.5 no change, 0 when a key blocker/QB is out against the leg, or the player is Questionable |

Any UNKNOWN component scores 0.5 and is listed. A leg with **two or more** UNKNOWN components cannot be labelled above
POSITIVE LEAN. A leg with **any** UNKNOWN component cannot be ELITE.

## 3. Labels

| Score | Label | Meaning |
|---|---|---|
| 90-100 | ELITE MISMATCH | every component known; defense and opportunity both top-quintile |
| 80-89 | STRONG READ | multiple independent sources agree; contradictory evidence written down and weaker |
| 70-79 | POSITIVE LEAN | favourable, but at least one important piece is missing or mixed |
| 60-69 | SOFT / CONDITIONAL LEAN | only playable if a named condition is met (inactive, weather, line move) |
| < 60 | PASS / INSUFFICIENT EVIDENCE | |

Proposed working definitions, in plain words:

- **Strong read**: the defense gives up this exact thing to this exact role (opponent-adjusted, season and L5 agree),
  the player reliably gets the opportunity (share floor met in season and L5), his median recent output clears the
  line, no hard rule blocks it, and the written contradictory evidence is weaker than the support.
- **Soft lean**: the matchup or the opportunity is favourable but not both; or season and L5 disagree; or the edge
  rests on one game, one source, or an UNKNOWN component. It is labelled with the condition that would upgrade it.

Every STRONG READ or ELITE line must show: defensive evidence (table, window, value, rank), opportunity evidence,
production evidence, coverage compatibility (or UNKNOWN), weather, coaching tendency, contradictory evidence,
conservative / median / upper projection (sim p25 / p50 / p80), probability of clearing the standard line, and
probability of each alternate line, each with source and timestamp.

## 4. Opportunity ceiling board

A separate board, informational only. A player is listed when all of these hold:

1. Opportunity floor met (WR/TE target share >= 20% in season and L5, or RB >= 50% of carries projected).
2. The defense's opponent-adjusted allowance for his group and stat ranks top 8 (most allowed) in season **and** L5,
   with at least 6 defense games.
3. The existing sim's p80 clears at least one alternate rung above the standard line.

For each listed player: expected opportunities, conservative / median / upper projection, standard-line probability,
probability at each alternate rung, conviction score and label. An alternate rung is marked **consider** only when it
meets the existing mirror-over bar (average model p minus no-vig >= .03, shrunk edge > 0, minimum model p >= .45, every
median over the line). The board never retreats to the safest line by default and never promotes a leg past a hard rule.

Example triggers from the current tables (research only, not reads): opposing TEs vs Washington (opp-adjusted
+34.1 yds/g season, +35.5 L3, 1st in both); opposing RB rushing vs Las Vegas (+37.0 yds/g season, 1st).

## 5. Validation before any label is used

1. Rebuild every input with `--through-week N-1` and score weeks 4-12 legs chronologically (no postgame inputs).
2. Report hit rate, Brier score and projection error by label, position, matchup category and weather category, with
   failed and zero-output games included.
3. Labels stay "uncalibrated" unless hit rate rises monotonically across bands and Brier beats the current gate's
   probabilities on the held-out weeks. Weights may be refit only on train weeks, then frozen before the held-out test.
4. Results go to Linear NFL-75 and Rico. No label becomes a rule without Rico's explicit approval.
