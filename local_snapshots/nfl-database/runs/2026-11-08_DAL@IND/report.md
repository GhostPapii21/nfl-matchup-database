# Projection report — DAL @ IND — PRELIMINARY RESEARCH (no picks)
**Slate/game:** Dallas Cowboys @ Indianapolis Colts, Week 9 REG 2026  
**Kickoff:** Sunday 2026-11-08 13:00 America/New_York (2026-11-08T18:00:00Z)  
**Data pulled:** 2026-11-06 ~07:39–07:50 America/New_York  
**Checklist:** `/workspace/nfl-database/runs/2026-11-08_DAL@IND/checklist.md`  
**Brainstorm:** `brainstorm.md` (loaded before checklist)  
**Packet:** `/workspace/research/nfl_sim_integration_2026-11-06/integration/prospective_wk10_2026-11-08` (dir name misnomer; week **9**)

## Status banner
This is **preliminary research**, not a final projection card. **No picks.** Quotes **NOLINE**. Phase 15 inactives are **unknown** until published. `projection_ready=false`. Joint↔empirical paths currently **NONINTEGRATED**.

## Phases run (truthful)
| Phase | Result |
|---|---|
| 1 Data | PASS partial (ESPN/nflverse/PBP W1–8) |
| 2 Opportunity | MISSING (no priced leg; empirical usage fit pending) |
| 3 Defense profile | MISSING |
| 4 Defender coverage | MISSING (effects disabled) |
| 5 Pressure/blitz | MISSING |
| 6 QB grade | MISSING |
| 7 Roles/RB | PARTIAL (eligibility audited) |
| 8 Injuries | PASS preliminary (Pierce IR out of ACT; Q retained) |
| 9 NGS | MISSING |
| 10 Film | MISSING |
| 11 Environment | PASS preliminary (NWS/Open-Meteo; roof retractable) |
| 12 Source audit | PASS partial |
| 13 Script gate | MISSING (spread NOLINE) |
| 14 Models/price | PARTIAL plumbing; edge NOT MEASURED; 100k×3 not run; Bias UNIMPLEMENTED |
| 15 Inactives | NOT_YET |

## Sources used, by category
1. **Core stats / PBP:** nflverse `games.csv` + `play_by_play_2026.parquet` filtered W1–8 DAL/IND; ESPN summary/rosters/scoreboard. schedules.csv endpoints returned stub (9 bytes) — repaired via games.csv.
2. **Coverage schemes / matchups:** **MISSING** this pass (FTN/Sharp/StatRankings not pulled). `allows_sim_effect=false`.
3. **NGS:** **MISSING** this pass.
4. **Film:** **MISSING** — no claims.
5. **Injuries/news:** ESPN summary injuries + nflverse roster status; practice notes not fully Wed–Fri tabled. Pierce IR confirmed.
6. **Weather:** NWS api.weather.gov + Open-Meteo only (SRC-1). Kick hour sunny ~56°F, wind ~10 mph, precip 0%. Retractable roof → contingency only.
7. **Odds/props:** sports-leader single-book DK-only → consensus **NOLINE**; odds-bridge LOGIN_REQUIRED (BetGuru; no auth bypass). Auth is not the sole possible source, but multi-book public consensus not available this pass.
8. **Simulation:** Joint producer n=5 conservation OK (data_only); empirical possession n=500 score_means fg_home 12.722 / fg_away 22.012 / p_ot 0.026. **Not** 100k Monte Carlo + Bias + Game Randomness. Paths do not yet share opportunity/yard ledgers.

## Simulations
- Confirmed **not** run: 100,000-sim Monte Carlo / Bias / Game Randomness triad.
- Joint n=5: forecast_id `sha256:8be81b96…`, input_hash `sha256:c9b4fa3d…`, quotes NOLINE, coverage_effects false.
- Empirical n=500: seed 1329861859, config_id dal_ind_2026-11-08_data_only.
- Reproducibility re-run after usage-cell fit: pending Codex completion.
- Independent vs anchored: **data_only only**; no market_informed conditioning.

## Projections and picks
**None.** Research scenario brainstorm only. No edge published. No slip.

## Risks and checks still to come
- Phase 15 inactives (~11:30 ET Sunday for 1 PM kick).
- Questionable skill players (Ferguson, Gould, etc.) — dual share scenarios if still unconfirmed.
- Empirical usage-cell fit under leakage controls (W1–8 only) + re-freeze.
- Coverage/NGS/FTN pulls or keep MISSING cuts.
- Multi-book quotes when BetGuru/public sources deliver (≥2 books) else remain NOLINE.
- Honest reconcile of joint trial 4 INCOMPLETE vs complete_pass 5/5 claim.
- Full integration acceptance requires shared opportunity/yard/accounting semantics **or** permanent NONINTEGRATED label — not schema test counts.

## Label / week reconciliation (do not rewrite frozen certified_asof)
- `2026-11-06T01:15:00Z` = 2026-11-05 20:15 EST **kickoff** (TNF JAX@BAL), not postgame.
- Packet `prospective_wk10_*` vs nflverse `2026_09_DAL_IND` → week **9**.

## Update — usage-cell fit + BetGuru research quotes (2026-11-06 07:54 EST)
- Fitted joint n=5 forecast `sha256:09f1c4336d5f62c61ffcc0c2c9771733f924e51d309b9841979369c665961403` means DAL 27.2 / IND 14.2 (reproducible). Placeholder before was DAL 22.0 / IND 30.4.
- PATH upgraded placeholder NONINTEGRATED → **SHARED_PARTIAL_SEMANTICS** (see packet PATH_SEMANTICS + Codex COMPLETION_PHASES_AND_FIT.md).
- BetGuru: actionable **NOLINE**; DK research snapshot DAL -5.5 / 51.5 / ML -230/+190 @ 07:50:49 ET — comparison only, not acceptance.
- Independent Grok review: `reviews/INDEPENDENT_GROK_ASSUMPTION_OUTPUT_REVIEW.md` — joint/empirical totals and margins diverge from research DK; high-variance n=5; **no picks**.
- Full integration acceptance: **still false**. Genuine blockers unchanged: Phase 15 inactives; multi-book verified quotes; coverage/NGS; Bias; shared accounting lineage; 100k triad not run.

## Final authoritative fitted joint ID (2026-11-06 07:58 EST)
- forecast_id `sha256:40c23caa5a0327c8ebc757520ad430e1401305518cd653549d542cc0300a3919`
- means DAL 27.2 / IND 14.2; reproducible True; pytest 82 passed
- Independent Codex + Grok reviews agree: SHARED_PARTIAL correct; research DK comparison only; acceptance not claimed.

## Update — empirical roles + shared accounting (2026-11-06 08:07 EST)
- Replaced equal-weight depth roles with pre-cutoff empirical shares + half shrinkage.
- SHARED_ACCOUNTING_V1: player opps→yards→team/period via joint event ledger; crosscheck 60/0 fails.
- Forecast `sha256:5cf792ce2fdc9351362ec77c9ed856a46314980745ec4b23622413312803d485` means DAL 18.8 / IND 14.2.
- Research DK comparison only; actionable NOLINE. Phase15 NOT_YET. No picks. projection_ready=false.
- DEFERRED_100K_UNFINISHED_SEMANTICS.

## Update — suite fix / robust roles (2026-11-06 08:25 EST)
- pytest 167 passed. Selected role policy mix_equal_0.25 (not unshrunk MLE). Shared path conservation 0 fails; team scores invariant to roles when coupling=false.
- Research DK still NOLINE actionable. No picks. projection_ready=false. DEFERRED_100K.
