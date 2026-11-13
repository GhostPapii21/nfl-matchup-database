# NFL-75: QB rush YPC prior fix + kneel model (+ opt-in designed/scramble/kneel components), and the 18-5 re-grade

**Research only, not validated. Not a pick list. `projection_ready` stays false. 0 Odds API credits. refs NFL-75.**
Fix logged on Linear NFL-75 (comment 6ce79e04). The engine change touches **only the QB rush YPC prior and kneel
handling**, and only when a leg carries `qb_rush_prior` in the allowlist True / "prior" / "components" (default off; the string "false" stays off). No betting-rule gate, no frozen classifier
file (`calibration/selective_edge*.py`, `params_w4_7.json`, freeze manifest), no shrink weight (K=100), opponent
strength, volume model or fitted multiplier changed. No `pregame/` or `.github/` change.

## The bug (all three vendored engines: sim_v5, sim_v6, sim_v6_fix)
`A_ypc = ((w*pm + (1-w)*lgA)/pm) * (oppY/lgA)`, `w = n/(n+100)`, where `pm` is the rusher's mean over **all** his
rush attempts including kneels (`qb_kneel==1`, about -1 yd each), kneels also count as carries in the volume model,
and `lgA` is the league mean over **all rushers** (RB-dominated: 4.18 on 2026 W1-9 incl kneels). On the committed
W1-9 PBP: all rushers 4.18, all non-kneel 4.33, RB 4.15, **QB non-kneel 5.57**, QB incl kneels 4.22.
Evidence: `runs/2026-11-15_NE@DET_friday/ghost6_check_maye.md`, `runs/2026-11-15_week10_focus7_qb_recal.md` (box).

## The fix (`calibration/simv56/engines/qb_rush_prior.py`, hooks in the three engines)
For a QB (players table `position_group == QB`) on rushyds / rushrec with `qb_rush_prior=True`:
1. Kneels are removed from his YPC sample and from his per-game carry counts (active-game set unchanged).
2. Shrink target = league **QB non-kneel** YPC before the cutoff (same K=100 weight; sim_v6_fix bias model keeps its
   own `100*BIAS_REG` weight and `BIAS_OPP` strength).
3. Opponent factor = opp-allowed / league YPC over non-kneel rushes.
4. Separate kneel model: per trial, margin ~ N(-spread, 13.5); team kneel count resampled from the league's team-game
   kneel counts before the cutoff for winning (margin > 0) or non-winning teams; each kneel's yards resampled from
   league kneel yards; the QB takes all team kneels (starter). Kneel yards are added after the YPC/opponent factor and
   before the engine's fitted per-market multiplier. Kneel draws use their own RNG stream.
Plumbing: `simv56_pmodel.run_all(..., qb_rush_prior=True)`. The `run` CLI has no switch for it, so a probability
file stamped `prob_source=sim_v5_v6_ensemble` (what the Phase 4 classifier was fit on and what #46 counts) cannot
carry the fixed prior. `SHA256SUMS` is updated for the three edited engines and the new module.

Flag-off proof: `test_simv56_pmodel.py` still reproduces all 88 W8-9 Phase 4 legs within 1e-12 and the Brissett
leg bit-for-bit. Non-QB legs are identical with the flag on (test + every RB/WR row below).

## Component model (leg `qb_rush_prior="components"`, added after the outside-AI review MEMO item 4)
Y = sum(designed-run yards) + sum(scramble yards) + kneel yards. Designed runs (non-kneel, `qb_scramble != 1`) and
scrambles get separate per-game counts through each engine's own `vol()` (same 0.6/0.4 weights, NB / GR share; a
component with no history gets zero volume). Per-carry yards are a mixture instead of a resample of his own carries:
with prob p0 a non-positive atom (resampled from the league QB pool of that component's <= 0 gains), else a lognormal
bulk + heavy right tail; p0 and the log-mean are shrunk player -> league QB with the unchanged n/(n+100) weight
(sim_v6_fix bias model: its own `100*BIAS_REG`), sigma is the league QB log-sd (fully pooled). Spikes past his
longest observed run (Allen 121, Maye 54) are now reachable: with the W8 cutoff (sim_v6 mc, no fitted multiplier, n=20,000), P(Maye >= 80) goes from
0.27% (QB-prior only) to 2.4%, and P(Allen >= 80) from 3.3% to 6.0%. Not done here (MEMO items 3/4): scrambles as
Binomial(dropbacks, q), script-driven designed-run volume (B3), zero-carry games (B2), clock in the kneel model.

## Re-grade (`regrade.py`, one command by code sha; outputs in `<mode>_<sha7>/`)
    python research/runs/2026-11-13_qb_rush_prior_regrade/regrade.py --code-sha <sha> --mode prior|components|off
It refuses unless HEAD is that sha and `calibration/` is clean. Rerun it after the settlement/EV, zero-carry and
QB-gate PRs land; this is **not** the final regrade. Committed runs, all at code `b7c9a7d`:
`off_b7c9a7d/` (control: reproduces 18-5 exactly), `prior_b7c9a7d/` (**QB-prior fix only**),
`components_b7c9a7d/` (QB-prior fix + components).
Review follow-up at code `a5a69b0` (flag allowlist + kneels-only nb() guard): `off_a5a69b0/`,
`prior_a5a69b0/`, `components_a5a69b0/`. Summaries, the 23-spot tables and all 88 p_model values match the
`b7c9a7d` runs exactly (max abs 0). Off mode still reproduces the 18-5 and all 88 Phase 4 legs with |d_p|=0.
Same 88 W8-9 rushyds legs (committed fixture), same engines/settings (opp 0.5, n=20,000, cutoffs W8 2026-10-29,
W9 2026-11-02, calib rule weeks < min(W,8)), committed W1-9 PBP, `qb_rush_prior=True`. Prices, outcomes and gates from
the box-local Phase 4 `legs_w4_9.csv` (sha256 = freeze manifest). Frozen classifier + the 18-5 study rule (gated,
edge vs no-vig >= +5 pts) applied unchanged. Game-cluster bootstrap 10k, seed 0. Book prices are not committed.

### QB-prior fix only (`prior_b7c9a7d/`)
| view | n | W-L | hit | BE | margin [95% CI] |
|---|---|---|---|---|---|
| OLD 18-5 rule, all | 23 | 18-5 | 78.3% | 52.9% | +25.3 [+5.8, +39.5] |
| **NEW same rule, corrected QB prior, all** | **21** | **17-4** | **81.0%** | **53.1%** | **+27.9 [+6.0, +42.6]** |
| NEW, only the original 23 that stay flagged | 20 | 16-4 | 80.0% | 53.1% | +26.9 [+3.6, +42.4] |
| OLD the 23, QB only | 17 | 13-4 | 76.5% | 52.5% | +23.9 [+0.9, +41.8] |
| **NEW same rule, QB only** | **15** | **12-3** | **80.0%** | **52.7%** | **+27.3 [+4.3, +47.1]** |
| OLD Phase 4 STRONG UNDER rushyds, QB only (the 15-4) | 19 | 15-4 | 78.9% | 52.6% | +26.4 [+6.1, +42.4] |
| **NEW Phase 4 STRONG UNDER rushyds, QB only** | **18** | **14-4** | **77.8%** | **52.6%** | **+25.2 [+3.9, +42.0]** |
| OLD Phase 4 STRONG UNDER rushyds, all | 27 | 21-6 | 77.8% | 52.9% | +24.8 [+7.2, +38.2] |
| NEW Phase 4 STRONG UNDER rushyds, all | 26 | 20-6 | 76.9% | 52.9% | +24.0 [+6.0, +37.7] |

Changes: **flagged -> unflagged** (edge fell under +5): Deshaun Watson U26.5 (+13.2 -> +3.2, was a W),
Michael Penix Jr. U2.5 (+11.8 -> +3.9, was an L), Justin Herbert U24.5 (+10.9 -> +0.9, was a W).
**New flag**: Trevor Lawrence U11.5 (+4.5 -> +7.2, W). Phase 4 STRONG UNDER (edge >= 0) also loses Daniel Jones U7.5
(+0.3 -> -8.9, was a W). No result flips: outcomes are settled facts; only the flag set changes. RB and WR spots are
unchanged. Tanner McKee U0.5 is unchanged (his 2-carry sample is 0 and 1 yd; scaling cannot move P(>= 0.5)).

### QB-prior fix + components (`components_b7c9a7d/`), for information
| view | n | W-L | hit | BE | margin [95% CI] |
|---|---|---|---|---|---|
| NEW 18-5 rule, all | 20 | 17-3 | 85.0% | 53.1% | +31.9 [+9.6, +46.7] |
| NEW 18-5 rule, QB only | 14 | 12-2 | 85.7% | 52.7% | +33.0 [+7.1, +47.5] |
| NEW original 23 that stay flagged | 19 | 16-3 | 84.2% | 53.1% | +31.1 [+7.2, +46.6] |
| NEW Phase 4 STRONG UNDER rushyds, QB only | 19 | 15-4 | 78.9% | 52.6% | +26.4 [+6.1, +42.4] |
Flagged -> unflagged: Jayden Daniels U36.5 (+16.5 -> +2.0, W), Tanner McKee U0.5 (+12.7 -> +2.5, L), Michael Penix
Jr. U2.5 (+11.8 -> +1.7, L), Justin Herbert U24.5 (+10.9 -> +2.0, W). New flag: Trevor Lawrence U11.5 (+4.5 -> +9.4, W).
Watson stays flagged here (+7.0).

## Caveats
- This is effectively one week (22 of 23 spots are Week 8), and Weeks 8-9 were already looked at by earlier studies,
  so it is not a clean holdout. The bug was found from W1-9 season logs, which include these games.
- The Phase 4 classifier was fit on the **unfixed** ensemble. Using fixed probabilities for countable spots would need
  a refit/re-freeze on W4-7 and is a betting-rule decision for Ghost6/Rico; this PR does not do it.
- The multiplicative YPC factor can be extreme on tiny samples (McKee A_ypc 10.9 on 2 carries); unchanged structure.
- Games with zero rushes stay out of the engines' active-game set (Geno W4), as before.
