# B5 Missed 100+ yard receivers, Wk7–8
Generated 2026-11-01 (ET), analysis only, nothing live, no rule changed. Scripts live in `backtests/rico_common/`.

**Method:**
- Data: leak-free sim_v6 RAW medians from `tools/sim_v6_backtest.csv`, Wk4–7, with each Engine cutoff set before week W and no calibration.
- Lines: **stand-in** lines of floor(prior median)+0.5, the same method as `p6_rush_exception`, `ol_dl_gap` and `rb_rec_script`.
- p: mean over mc/bias/gr of Normal(median, SD), with the SD taken walk-forward.
- Bet rule: over when p > .5238, the −110 break-even.
- Features: from weeks < W only.
- Not covered: Wk3 (under 2 priors) and Wk8 Sunday (no RAW medians).
- Stats: p-values are two-sided binomials vs break-even, and the bucket comparison uses a two-proportion z test. Every result is small-n.

## Every WR/TE/RB with 100+ receiving yards
Wk7 and Wk8 TNF come from nflverse pbp. Wk8 Sunday comes from the 11 `playlogs/2026_wk8/*_box.json` games on the box, so any 100+ games in the other Sunday games are not listed. The pool is every leg in the 16 `runs/2026-11-01_*` manifests. No Wk7 run records exist, so the Wk7 pool can't be reconstructed.

| Wk | Player | Rec yds | Candidate pool / what cut him | Signals lit (pregame, weeks < W) |
|---|---|---|---|---|
| Wk7 | Zay Flowers (WR, BAL vs CIN) | 137 on 11.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22%, explosives_allowed_top3rd, script_dog |
| Wk7 | Tee Higgins (WR, CIN vs BAL) | 148 on 7.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22%, passrush_vs_OL_mismatch |
| Wk7 | KC Concepcion (WR, CLE vs TEN) | 129 on 10.0 tgt | n/a (no Wk7 run records on the box) | coverage_vs_type(ypt>=1.10x lg), passrush_vs_OL_mismatch |
| Wk7 | Trey McBride (TE, ARI vs DEN) | 111 on 13.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22%, passrush_vs_OL_mismatch, script_dog |
| Wk7 | Amon-Ra St. Brown (WR, DET vs GB) | 153 on 11.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22% |
| Wk7 | Jaxon Smith-Njigba (WR, SEA vs KC) | 150 on 12.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22%, passrush_vs_OL_mismatch |
| Wk7 | Tre Tucker (WR, LV vs LA) | 103 on 12.0 tgt | n/a (no Wk7 run records on the box) | script_dog |
| Wk7 | Omar Cooper Jr. (WR, NYJ vs MIA) | 115 on 5.0 tgt | n/a (no Wk7 run records on the box) | none |
| Wk7 | Luther Burden III (WR, CHI vs NE) | 130 on 4.0 tgt | n/a (no Wk7 run records on the box) | none |
| Wk7 | Malik Nabers (WR, NYG vs HOU) | 111 on 9.0 tgt | n/a (no Wk7 run records on the box) | target_share>=22%, explosives_allowed_top3rd, passrush_vs_OL_mismatch, script_dog |
| Wk8 | Christian Watson (WR, GB vs CAR) | 113 on 10.0 tgt | NOT in candidate pool (no leg in any 11-01 run manifest) | none |
| Wk8 | Michael Wilson (WR, ARI vs DAL) | 111 on 15.0 tgt | Michael Wilson Rec Yds Under 56.5 [CUT] cut: P4 MISSING: defender not in PFR cache; P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player; Michael Wilson Receptions Under 4.5 [CUT] cut: P4 MISSING: defender not in PFR cache; P10 UNVERIFIED: no cited caption play re-matched a fresh pbp row for this player | target_share>=22%, explosives_allowed_top3rd, coverage_vs_type(ypt>=1.10x lg), script_dog |
| Wk8 | Harold Fannin Jr. (TE, CLE vs PIT) | 154 on 12.0 tgt | Harold Fannin Jr. Rec Yds Under 34.5 [CUT] cut: P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%; no stand-in allowed; Harold Fannin Jr. Receptions Under 3.5 [CUT] cut: P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 12.6% / zone 82.2%, MOF closed 45.5% / open 51.5%; no stand-in allowed | explosives_allowed_top3rd, passrush_vs_OL_mismatch, script_dog |
| Wk8 | Emmett Johnson (RB, KC vs DEN) | 128 on 5.0 tgt | NOT in candidate pool (no leg in any 11-01 run manifest) | passrush_vs_OL_mismatch, script_dog |
| Wk8 | Adonai Mitchell (WR, NYJ vs LV) | 142 on 9.0 tgt | NOT in candidate pool (no leg in any 11-01 run manifest) | coverage_vs_type(ypt>=1.10x lg), passrush_vs_OL_mismatch |
| Wk8 | Tee Higgins (WR, CIN vs TEN) | 155 on 11.0 tgt | [PP $40 6-pick Power] Tee Higgins Fantasy Score 14.5 [CUT] cut: P14 MISSING: no sim model: no sim model for fantasy score; leg left ungraded (not invented); [PP $20 6-pick Power] Tee Higgins Rec Yds Over 68.5 [CUT] cut: P14 MISSING: no book price at this rung: no-vig MISSING, edge not computable; MODEL-SUSPECT: MC median 84.8 vs FD main 70.5 / book consensus 70.8 (>=12 yds) -> Debugging; [FD 7-leg +694] Tee Higgins Receptions Over 3.5 [CUT] cut: P14 FAIL: edge +2.3 < +3; shrunk edge -5.3 not > 0 | target_share>=22%, explosives_allowed_top3rd, coverage_vs_type(ypt>=1.10x lg), passrush_vs_OL_mismatch |
| Wk8 | Ja'Marr Chase (WR, CIN vs TEN) | 141 on 16.0 tgt | Ja'Marr Chase Rec Yds Under 79.5 [CUT] cut: P3 FAIL: under vs soft WR D (YPT>=9.0); P4 MISSING: defender not in PFR cache; Ja'Marr Chase Receptions Under 6.5 [CUT] cut: P3 FAIL: under vs soft WR D (YPT>=9.0); P4 MISSING: defender not in PFR cache | explosives_allowed_top3rd, coverage_vs_type(ypt>=1.10x lg), passrush_vs_OL_mismatch |

| Signal | n on | 100+ rate on | 100+ rate off | lift | recyds-over hit on (stand-in) | p (hit on vs off) |
|---|---|---|---|---|---|---|
| target_share>=22% | 102 | 24.5% | 2.3% | 10.59x | 43.1% | 0.11 |
| explosives_allowed_top3rd | 414 | 3.9% | 5.0% | 0.77x | 50.7% | 0.97 |
| coverage_vs_type(ypt>=1.10x lg) | 298 | 3.0% | 5.2% | 0.58x | 49.0% | 0.50 |
| passrush_vs_OL_mismatch | 358 | 5.0% | 4.3% | 1.17x | 53.1% | 0.25 |
| script_dog | 501 | 4.2% | 4.9% | 0.85x | 52.1% | 0.36 |

| # signals lit | n | 100+ rate | recyds-over hit | ROI −110 |
|---|---|---|---|---|
| 0 | 156 | 3.2% | 55.8% | +6.5% |
| 1 | 328 | 3.4% | 46.3% | -11.5% |
| 2 | 293 | 5.1% | 52.2% | -0.3% |
| 3 | 171 | 7.0% | 49.1% | -6.2% |
| 4+ | 61 | 4.9% | 57.4% | +9.5% |

The signal test covers Wk3–8 (pbp) player-games of WR/TE/RB with targets and ≥2 priors, with signals from weeks < W. Target share ≥22% is a strong 100+ predictor (24.5% vs 2.3%), but on stand-in lines it doesn't beat the median line (43.1%), because the line already prices it in.

## Recommendation
**Why they were missed (Wk8):**
- Wilson, Fannin and Chase were in the pool *only as UNDERS*, and those were correctly cut: P4 missing defender, P3 soft-D. No over was ever built.
- Higgins was in the pool as overs, but they were cut on price/model-suspect/edge reasons, which are softened edges; see B6.
- Watson, E. Johnson and A. Mitchell were never in the pool.

**Recommendations (non-live):**
- (1) When an under is cut by P3 soft-D or 'defender missing', **auto-generate the mirror OVER as a candidate** so it gets evaluated, not silently dropped.
- (2) Add target share ≥22% as a pool-entry trigger for overs. It doesn't predict beating the line by itself, so no edge change.
- (3) Explosives-allowed and coverage-vs-type, as team-level walk-forward proxies, did **not** lift the 100+ rate (0.77x and 0.58x), so don't add them as signals in this form.
