# Possession Engine Completion Checklist — 2026-11-05 EST

**Worktree:** `/workspace/wt-period-engine` branch `research-period-engine-2026-11-05`
**Base before this pass:** `64b564b`
**Scope:** research-only; no production/merge/publish/bets; no paid FTN/cloud spend.
**Reviews:** Codex (`codex exec -s read-only`, 2026-11-05 17:03:47 EST) + Grok (`grok-4.3`, 2026-11-05 17:00:56 EST) on frozen/local bundle; re-review status below.

Legend: **IV** = implemented + validated (tests/green grade) · **IU** = implemented, unvalidated / partial · **MS** = missing-source (adapters only; never labeled fitted)

---

## Rico-requested features

| Feature | Status | Evidence / next source |
|---|---|---|
| Team-only then both-team as-of W1–8 grade | **IV** | 13/15 GRADED_FULL; W1 skips; `asof_grade_per_game.csv` |
| Period Q1–Q4/H1/H2/reg/OT scoreboards + MAE/Brier | **IV** | `run_period_realism_grade.py`; N=150/game, 13 games, ~30s period + ~60s full script |
| Apples-to-apples pace (combined both-offense snaps) | **IV** | `actual_combined_snaps_per_game`; sim 116.2 vs actual combined 121.1; Δ −4.9 (was 133 vs 2×59.9) |
| Snap accounting includes TD/TO/TOD | **IV** | Codex P1 fix; `test_each_offensive_play_emits_one_snap` |
| Punt net from `kick_distance − return_yards` | **IV** | was always 25 via `yards_gained=0`; `test_punt_uses_explicit_net_distance_not_yards_gained` |
| Safety when loss crosses own goal | **IV** | `test_backed_up_loss_scores_safety` |
| PAT does not consume game clock | **IV** | `test_pat_does_not_consume_game_clock` |
| Empirical clock medians (else fixed defaults) | **IU** | medians when Δ∈[3,55] n≥30; still Gaussian σ=4 + 3s floor; not situational |
| Hard sparse vs coarse reporting | **IV** | `sparse_rate` hard-only; `coarse_rate` separate (post-fix: sparse=0, coarse=1.0 @N=50) |
| Defense-conditioned sampling (H2H) | **IU** | enabled; **0 DEF_COND events** for JAX–BAL (no H2H pools in W1–8 catalog) — not a full O/D interaction model |
| EffectsCatalog wired without crash | **IV** | duck-typed `clock_map` / defense; `test_effects_catalog_runs_complete_game` |
| Blitz strata preserves non-pass selection | **IU** | still pass-pool when strata fire (Codex open P1 partial) — not forced for completion |
| Missing pressure/man/zone/MOFO/CB-S-DT | **MS** | `effects/missing_feature_adapters.py` + dossier; FeatureGate NEVER fitted |
| True pressure (FTN qbp) | **MS** | paid FTN; free 29-col has blitz only; no connector in MCP catalog |
| Charted coverage / routes | **MS** | not in free FTN 29-col; balldontlie/statshawk/sports-leader lack charting |
| CB/S/DT replacement coefficients | **MS** | no authorized measured source; do not invent |
| Weather NWS auto-downgrade | **MS** | hook PENDING_NWS only |
| OT single-possession approx | **IU** | declared limitation; accounting checks tie-only OT |
| 4th-down / FG distance conditioning | **MS**/open | team-wide probs; Codex P1 still open |
| Joint player sample distribution (not mean-only) | **IU** | `player_joint` = mean accumulation; not per-sim joint export |
| 3-model Bias / GR / Pinnacle validation | **IU**/incomplete | configs exist; market conditioning **unwired** (`run_jaxbal_demo.py`); **not** three independently validated models |
| Calibration / untouched holdout | **MS** | W1–8 development inspected; no chronological untouched holdout this pass |
| Interval / MC uncertainty bands | **IU** | N=150 period; no bootstrap CIs published this pass |

---

## Quantified post-fix grading (America/New_York)

- **As-of FG:** 13/15 GRADED_FULL (2 W1 skips)
- **Period (N=150/game, 13 games):** H1 MAE home/away 6.06 / 4.70; Brier H1 0.230; Reg MAE 9.35 / 7.95; Brier reg 0.325
- **Pace:** actual combined 121.1 (n=15); sim mean snaps 116.2 (realism n_sims=200 seed=11); Δ combined −4.9
- **Simulate diag N=50 seed=42:** sparse_rate 0.0; coarse_rate 1.0; DEF_COND events 0; mean FG ~18.4–22.0; runtime ~0.8s
- **Full pytest:** 51 passed (~12s)
- **Period+realism script runtime:** ~60s

Seeds: period grade uses script defaults (N_SIMS=150); realism seed=11 n=200; diag seed=42 n=50.

---

## Codex + Grok review artifacts

| Reviewer | Model/route | Pulled (ET) | Artifact | Status |
|---|---|---|---|---|
| Grok | grok-4.3 via xAI chat completions | 2026-11-05 17:00:56 EST | `reviews/grok_review_possession.md`, `grok_meta_possession.json` | OK (pre-patch + local uncommitted noted) |
| Codex | `codex exec -s read-only` (short prompt; worktree read) | 2026-11-05 17:03:47 EST | `reviews/codex_stdout_possession.txt`, `codex_meta_possession.json` | OK; argv-too-long on full bundle → short prompt retry |
| Claude / Google | — | — | UNAVAILABLE (Anthropic absent; prior period UNAVAILABLE preserved; **not overwritten**) | — |

**Final-diff re-review:** see `reviews/FINAL_DIFF_REVIEW_STATUS.md`.
Codex+Grok re-reviewed patched bundle (review-complete, not P1-closed).
Post-re-review microfix: NaN-safe punt touchback (tested; marked unreviewed in FINAL_DIFF_REVIEW_STATUS).

---

## Remaining blockers (actionable sources)

1. **Paid FTN `qbp` / charting** — true pressure, man/zone, MOFO/MOFC, routes. Free 29-col insufficient.
2. **Measured CB/S/DT replacement study** — no invent; need authorized coefficients or leave MISSING.
3. **H2H / opponent-defense pools** beyond raw head-to-head rows — or accept DEF_COND unused for cold matchups.
4. **Situational 4th/FG/clock** — field position, distance, score, time; kick distance-conditioned make rates.
5. **Untouched chronological holdout + calibration bands** — not W1–8 development reuse.
6. **Wire Bias/GR/Pinnacle as real validators** only with authorized market feeds — currently unwired; do not claim 3-model agreement.
7. **Coarse_rate≈1.0** — fine state support still weak; coarsening expected under team-only min_n=5.

---

## Commands

```bash
cd core/possession_engine_v0
python3 -m pytest tests/ -q
python3 run_period_realism_grade.py
```

## Do-not-touch

- `research/period_engine_v0/reviews/*` teammate/dirty audits — not overwritten this pass.


---
## Pass 2 update (2026-11-05 18:45 ET) — supersedes rows above where they conflict
See FEATURE_EXECUTION_MATRIX.md and artifacts/validation/pass2/pass2_metrics.json.
- EffectsCatalog wired via single build_catalog() into simulate_games/accounting/realism/as-of/period: **IV**
- Blitz conditions called passes only: **IV**; 4th-down state cells + FG distance + missed-FG spot: **IV** (mechanics tested, not predictively validated)
- DEF_COND H2H for JAX–BAL: **unsupported by data (0 H2H rows)**; opponent-allowed mixture executed in variant only, weight unfitted, worse FG MAE
- Player credit fixes (foreign rows, TD cap, negatives, fumbles) + per-sim samples: **IV** (mechanics)
- Weather: NWS metadata only. Pressure/coverage: adapters + 2025 descriptive only. Market: unwired.
- Grading (N=150/game, seed_base 20261105, 13/15 graded, W1 skips 2026_01_BAL_IND, 2026_01_CLE_JAX):
  data_only FG MAE 9.74 vs as-of PPG baseline 9.28 (game-bootstrap diff 95% [-1.86, 3.00]);
  H1 MAE 5.36 vs PPG/2 baseline 5.37; Brier reg 0.314 vs coin-flip 0.25; H1 Brier 0.214.
  **No predictive improvement over naive baselines demonstrated. Development set, not holdout.**
- Pace: sim 116.1 vs actual combined 121.1 (Δ −5.0); approx plays/drive sim 6.6 vs actual 7.5 (actual measure not exact apples-to-apples).
- 100k: NOT run — correctness gates pass for mechanics but no predictive gate passed.


## Pass 2c (after Codex final review of 8a4ce01) — CURRENT NUMBERS (supersede pass-2 numbers above)
Fixed RED-first (tests/test_final_review.py): TOD/INT/punt spots no longer clipped to 10–90; end-zone punt/INT -> touchback; snap events log realized yards (+hist_yards).
Regrade 2026-11-05 18:46–18:55 ET, N=150/game, seed_base 20261105, 13/15 graded (W1 skips 2026_01_BAL_IND, 2026_01_CLE_JAX), accounting 9/9 checks pass:
- data_only: FG MAE 9.88 vs as-of PPG baseline 9.28 (paired game-bootstrap diff 95% [-1.71, 3.08]); H1 MAE 5.41 vs 5.37; Brier H1 0.203, reg 0.317 (95% [0.172, 0.495]) vs coin-flip 0.25
- variant_def_allowed_w05: FG MAE 10.09; H1 5.35; Brier reg 0.316
- Pace: sim 116.6 / 119.0 vs actual combined 121.1; approx plays/drive 6.55 / 6.22 vs 7.54
- JAX@BAL forward (n=300, seed 20261105, data_only): JAX 20.53, BAL 15.54, MC SE ~0.48; per-snap coarse 7.5%
Status: mechanics complete & reviewed for feasible scope; predictive validity NOT established.
