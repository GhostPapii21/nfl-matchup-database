# B6 Softened edges: aligned overs that were cut, softened, or played a rung down (Wk8, real lines)
Generated 2026-11-01 (ET), analysis only, nothing live, no rule changed. Scripts live in `backtests/rico_common/`.

**Method:**
- Data: leak-free sim_v6 RAW medians from `tools/sim_v6_backtest.csv`, Wk4–7, with each Engine cutoff set before week W and no calibration.
- Lines: **stand-in** lines of floor(prior median)+0.5, the same method as `p6_rush_exception`, `ol_dl_gap` and `rb_rec_script`.
- p: mean over mc/bias/gr of Normal(median, SD), with the SD taken walk-forward.
- Bet rule: over when p > .5238, the −110 break-even.
- Features: from weeks < W only.
- Not covered: Wk3 (under 2 priors) and Wk8 Sunday (no RAW medians).
- Stats: p-values are two-sided binomials vs break-even, and the bucket comparison uses a two-proportion z test. Every result is small-n.

Universe: the 16 `runs/2026-11-01_*` manifests, over legs graded from the Wk8 box scores.
- **Aligned** = no context FAIL (P3/P5/P6/P7/P11/P13/§7/injury), §7 3 of the last 4 over the line, and avg p(mc,gr) ≥ .55.
- **Full strength** = the main line (book consensus point) instead of the alt rung played, or the leg played instead of cut.
- PRESS was evaluated with `tools/press_tier.evaluate` (k=2), with matchup/script/qb set True by the aligned definition and coverage = a coverage block present.
- Edges are in points.

| Leg | Status/kind | p | edge→shrunk | full line | actual | full hit | PRESS? | cut reason |
|---|---|---|---|---|---|---|---|---|
| Puka Nacua Receptions Over 7.5 | CUT/cut | 0.62 | +8.2→+4.5 | 7.5 | 11 | ✔ | PRESS (all context aligned; 3/3 models clear) |  |
| Brenton Strange Receptions Over 2.5 | CUT/alt-rung | 0.80 | +4.9→-4.2 | 3.5 | 2 | ✘ | STANDARD (context not aligned ['coverage']) | P4 UNVERIFIED: TE defender mapping not ruled (ISS-05); man 26.2% / zone 66.5%, MOF closed 50.2% / open 44.7%; no stand-in allowed; P14 FAIL: shrunk edge -4.7 no |
| Kirk Cousins Pass Yds Over 232.5 | CUT/cut | 0.59 | +8.9→+6.2 | 232.5 | 247 | ✔ | STANDARD (0/3 models clear < 2) | P14 FAIL: edge +2.4 < +3; model p 0.395 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 250.8 vs FD main 232.5 / book consensus 233.5 (> |
| Jaylen Warren Rush Yds Over 64.5 | CUT/cut | 0.59 | +8.7→+6.1 | 64.5 | 143 | ✔ | STANDARD (context not aligned ['coverage']) | P14 FAIL: a model median does not clear the line |
| Jahmyr Gibbs Rush Yds Over 87.5 | CUT/cut | 0.58 | +8.0→+5.6 | 87.5 | 153 | ✔ | STANDARD (context not aligned ['coverage']) | P14 FAIL: a model median does not clear the line |
| Joe Burrow Pass Yds Over 249.5 | CUT/alt-rung | 0.69 | +5.7→-0.0 | 272.5 | 462 | ✔ | PRESS (all context aligned; 2/3 models clear) | P14 FAIL: edge -1.0 < +3; shrunk edge -4.7 not > 0; a model median does not clear the line; MODEL-SUSPECT: MC median 292.5 vs FD main 272.5 / book consensus 272 |
| Tee Higgins Rec Yds Over 69.5 | CUT/alt-rung | 0.62 | +10.8→+7.2 | 70.5 | 155 | ✔ | PRESS (all context aligned; 2/3 models clear) | P14 FAIL: placed-ticket bar: PP20 Higgins o68.5 rec yds; $51.50 SGP Higgins 50+ yds; MODEL-SUSPECT: MC median 84.8 vs FD main 70.5 / book consensus 70.8 (>=12 y |
| Tee Higgins Receptions Over 4.5 | CUT/alt-rung | 0.66 | +8.1→+3.4 | 5.5 | 10 | ✔ | PRESS (all context aligned; 2/3 models clear) | P14 FAIL: placed-ticket bar: PP40 Fantasy/PP20 rec yds/$51.50 SGP Higgins 50+ yds/FD 7-leg 4+ rec |
| George Pickens Rec Yds Over 59.5 | CUT/alt-rung | 0.60 | +3.9→+0.8 | 65.5 | 48 | ✘ | PRESS (all context aligned; 2/3 models clear) | P14 FAIL: edge +0.9 < +3; shrunk edge -1.3 not > 0 |
| Drake Maye Pass Yds Over 239.5 | CUT/cut | 0.61 | +10.9→+7.6 | 239.5 | 199 | ✘ | PRESS (all context aligned; 2/3 models clear) | P14 FAIL: model p 0.382 < .45; a model median does not clear the line; MODEL-SUSPECT: MC median 259.5 vs FD main 239.5 / book consensus 238.8 (>=12 yds) -> Debu |

Softened/cut aligned overs graded at full strength: 7/10 = 70.0%, ROI −110 +33.6%, p vs BE 0.35.
Of those, the ones PRESS (k=2) would have tagged went 4/6 = 66.7%.
Aligned overs that were played at full strength: 1/2.

## Recommendation
**The edges were real, and the softening cost us.** Aligned overs that were cut or played a rung down went 7/10 at full strength (ROI +33.6% at −110, n=10, p 0.35). Most of the cuts came from P14 (shrunk edge ≤ 0, or a model median below the line) and MODEL-SUSPECT, where the MC median sat ≥12 yds above the book and was treated as a bug instead of an edge (Burrow 462, Higgins 155, Gibbs 153, Warren 143).

**PRESS (live Nov 5)** would have tagged 6 of the 10, which went 4/6, including Burrow, Higgins ×2 and Puka. But PRESS is advisory and doesn't override P14 cuts or MODEL-SUSPECT, so those legs would *still have been cut*. **In that sense PRESS is too soft.**

**Recommendation, needs Rico's approval, not live:** for a PRESS-tagged leg, let MODEL-SUSPECT become a *manual review* rather than an automatic cut, and skip the extra P14 shrink. Retest over Wk9–10 before going live. The n is small and these are Wk8 results only.
