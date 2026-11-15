# Diagnostic re-grade: unmerged A + B + C + PR #47 (not counted)

**Research only. Not counted. Do not merge this combination. `projection_ready` stays false. 0 Odds API credits. refs NFL-75**

Local, unmerged tree at `527e3a1`, made by cherry-picking the three memo draft PRs onto PR #47 (`research/qb-rush-prior-fix-2026-11-13` at `f4ce5e1`):

| Piece | SHA | What is on |
|---|---|---|
| PR #47 | `f4ce5e1` | opt-in `qb_rush_prior` (allowlist + kneels-only guard) |
| PR A (draft) | `1e6ef35` | settlement/EV module; candidate labels need EV > 0 at the actual price |
| PR B (draft) | `b12b4ec` (on `64731b2`) | opt-in `volume_fix` (keep played zero-carry games; spread moves expected volume; 2x cap and YPC guard; True allowlist) |
| PR C (draft) | `9c4b712` | QB starter gate on every leg; case-insensitive matching |

`--mode off|prior|components` is the #47 `qb_rush_prior` flag. Every run here also has `volume_fix=True` and the EV gate. The 23-spot study rule is unchanged: gated main rushyds unders with edge vs no-vig >= +5. Break-even, margin and the game-cluster bootstrap (B=1000, seed from `selective_edge.summarize`) are from the actual graded prices in the Phase 4 `legs_w4_9.csv` (sha256 checked against the freeze manifest). Engines: 20,000 trials, opp 0.5, W8/W9 cutoffs, 0 engine errors, 0 Odds API credits. Pulled Sat Nov 14, 2026, 1:52 PM ET.

This does **not** replace the #47-only scorecard on `f4ce5e1`. Those remain:

| #47 only (no volume_fix) | Record | Hit vs break-even | Margin [95% CI] |
|---|---|---|---|
| off | 18-5 | (control; 18-5 reproduced) | (control) |
| prior | 17-4 (21 spots) | 81.0% vs 53.1% | **+27.9 [+6.0, +42.6]** |
| components | 17-3 (20 spots) | 85.0% vs 53.1% | +31.9 [+9.6, +46.7] |

## Combined result (study rule, all positions)

| Mode (`qb_rush_prior`) | Record (n) | Hit vs break-even | Margin [95% CI] vs #47-only |
|---|---|---|---|
| off + volume_fix + EV gate | **20-7** (27) | 74.1% vs 53.4% | **+20.7 [-1.2, +36.6]** — CI lower bound is below 0. The original 23 stayed flagged at 18-5; four new flags were 2-2. |
| prior + volume_fix + EV gate | **19-4** (23) | 82.6% vs 53.5% | **+29.1 [+8.9, +42.8]** — vs #47 prior 17-4, +27.9 [+6.0, +42.6] |
| components + volume_fix + EV gate | **20-4** (24) | 83.3% vs 53.5% | **+29.8 [+13.3, +42.6]** — vs #47 components 17-3, +31.9 [+9.6, +46.7] |

The EV gate did not drop any of the original 23: each already had edge vs no-vig >= +5, which is above break-even at the graded prices. PR C's attach/gate change is in the combined code but is not on the path this script uses (`se.evaluate` on the Phase 4 legs file).

Whether any of these combined probabilities can count, and any W4-7 refit, is still Rico's call.

## Files

- `regrade_combined.py` — the script that produced these folders.
- `combined_{off,prior,components}_vf_527e3a1/` — `regrade_23_spots.csv`, `regrade_summary.csv`, `p_model_old_new_w8_w9_rushyds.csv`, `regrade_meta.json` (credits=0, `diagnostic_only=true`, `counted=false`).
