# NFL-75 Phase 4: selective-edge classifier (fit Weeks 4-7, frozen, scored Weeks 8-9)

**Research only, not validated. Not a pick list. `projection_ready` stays false. 0 Odds API credits. refs NFL-75.**
Engine, production weights, `pregame/` and `.github/` are untouched.

Code: `calibration/selective_edge.py` (gates, labels, fit, evaluate, graduation), `selective_edge_freeze.py`,
`selective_edge_live.py` (Weeks 10-12 only, frozen), `selective_edge_run.py` (build / fit / eval),
`selective_edge_report.py` (read-only position split). Tests: `calibration/tests/test_selective_edge*.py`.

## Labels and gates (in order)
1. `pass*` markets excluded -> NO EDGE.
2. RB/FB rushing legs: >=60% of team carries in >=3 of last 4 prior games (same gate as the 18-5 study; 0 mismatches
   against that study's gate on all W4-9 rows). <3 prior games -> INSUFFICIENT EVIDENCE; gate fails -> NO EDGE
   (`do_not_play_rb_carry_lt_60`). QB/WR rush legs are not subject to this gate.
3. Receiving legs (recyds, rec, rushrec) need a verified main defender -> otherwise INSUFFICIENT EVIDENCE. No
   historical defender source exists, so **every W4-9 receiving leg is INSUFFICIENT EVIDENCE**.
4. Real price required (decimal + price_source); missing -> INSUFFICIENT EVIDENCE. Nothing is filled in.
5. Model probability required; missing -> INSUFFICIENT EVIDENCE.
6. Edge vs no-vig (main) or vs break-even (alt). +1 / +3 pt tiers are flags (`edge_tier`), not cuts. Edge < 0 -> NO EDGE.
7. Main Under in a W4-7 strong market -> STRONG UNDER; other main legs -> STANDARD-LINE CANDIDATE.
8. Alt Over rung at/below usual output (median of last 4 prior games, needs 3) with cushion >= fitted minimum ->
   ALT-LINE CANDIDATE.

## Fit on Weeks 4-7 (`params_w4_7.json`)
- Strong markets: **rushyds only** (n=101, 60-41, 59.4% vs 53.2% BE, +6.2 pts, CI -4.0 to +16.0).
- Alt-floor cushion: **none qualifies** (every cushion 10-50% was about -10 to -13 pts vs BE on gated rush-yds alt
  overs, n=51-122), so alt floors are NO EDGE (`alt_floor_not_shown_in_train`) until a new fit says otherwise.
- Frozen in `freeze_manifest.json` before Weeks 8-9 were scored by this classifier. The manifest was re-frozen once
  after scoring to fix the live adapter (`selective_edge_live.py`); `selective_edge.py` and the params sha256 are
  unchanged between the two freezes.

## Weeks 8-9 out of sample (game-cluster bootstrap 10k, seed 0)
| label | market | n | W-L | hit | BE | margin [95% CI] |
|---|---|---|---|---|---|---|
| STRONG UNDER | rushyds | 27 | 21-6 | 77.8% | 52.9% | +24.8 [+7.2, +38.2] |
| ALT-LINE CANDIDATE | - | 0 | - | - | - | disabled by the W4-7 fit |
| STANDARD-LINE CANDIDATE | - | 0 | - | - | - | receiving legs all lack a verified defender |
| INSUFFICIENT EVIDENCE | - | 4,437 legs | not graded | | | |
| NO EDGE | - | 1,481 legs | not graded | | | |

Edge-tier flags inside STRONG UNDER OOS: +3 tier 20-6 (n=26), no tier 1-0 (n=1).

**What the rush-yds edge actually is (by position, `results_rush_under_by_position.csv`):**
| set | group | n | W-L | margin [CI] |
|---|---|---|---|---|
| W4-7 | QB | 74 | 44-30 | +6.6 [-4.9, +17.6] |
| W4-7 | RB (60% gated) | 18 | 8-10 | -8.6 [-30.9, +13.7] |
| W8-9 | QB | 19 | 15-4 | +26.4 [+6.1, +42.4] |
| W8-9 | RB (60% gated) | 6 | 4-2 | +13.7 [-33.0, +47.1] |
| W8-9 | RB failing the gate | 37 | 14-23 | -15.2 [-32.5, +1.7] |

The gate keeps losing RB unders out, but the winning rows are mostly **QB** rush unders. Gated RB unders on their own
are not shown to beat their price.

## Reconciliation with the 18-5 result
Same rows, same prices: the prior control rule (gated, edge vs no-vig >= +5 pts) reproduces **18-5, 78.3% vs 52.9%,
+25.3 [+5.8, +39.5]** on Weeks 8-9 (`reconcile_18_5.csv`). Of those 23: 17 QB, 4 RB, 2 WR; 22 in Week 8 and 1 in
Week 9 (13 games). Pricing: each is the one book's main-line two-sided Under price in `legs_with_probs.csv`, snapshot
34.4 min before kickoff (FanDuel 13, DraftKings 9, BetRivers 1), not a multibook best price and not a live bet.
Weeks 8-9 had already been looked at by earlier studies, so they are not a clean holdout.

## Graduation rule (report only)
`se.graduation`: a (label, market, side) is **spot-ready, research** when n >= 30 settled legs at real prices,
margin >= +3 pts over BE and CI lower bound > 0. It never writes `projection_ready`. Default counts `live` (Weeks
10-12) legs only; `sources=("backtest_oos","live")` shows the combined view. Current backtest_oos alone: STRONG UNDER
rushyds n=27, +24.8 [+7.2, +38.2] -> not yet (n<30).

## Inputs (box-local, sha256 in the manifest; book prices are not committed)
candidates.csv `5aa84712...6f23`, legs_with_probs.csv `3a945f3c...69a2`, committed PBP `1028614b...5b8`.
p_model = the pre-registered walk-forward sim ensemble (sim_v5/v6/v6_fix, opp 0.5), not the Phase 2 opportunity model.

## Open gaps
- Live legs need a per-leg model probability (P(under)) from the 100k / opportunity sims; without it, a leg is
  INSUFFICIENT EVIDENCE. There are no player-level rush probabilities in `runs/2026-11-12_tnf_100k`.
- Sunday Week 10 has no committed price freezes yet; `legs_from_freeze_v2` reads them once they exist.
- No main-defender source, so receiving labels are untested; no under-direction alt prices; game markets out of scope.
- `selective_edge_live.py` CLI `main()` and `legs_from_freeze_v2` were written before their test
  (`test_selective_edge_report.py::test_freeze_v2_adapter_reads_real_prices_only`, added after; it caught a real bug).
