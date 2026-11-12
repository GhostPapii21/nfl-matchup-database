# BetGuru — PHASE 10G — GAME SCRIPT, WEIGHTS, SIMS, GATES, FINAL CARD
Written Sat Oct 31, 2026, ~8:20 PM ET. Prices: FanDuel sbapi 7:37 PM ET snapshot. Sims: BetGuru `bg_sim.py` v3, N=100,000 per model, **UNCALIBRATED** (calibration NOT PASSED; engine `outputs/nfl.py` absent → SIMULATION NOT RUN for engine). Nothing placed.

## 10G-1 Game classification and weights (both teams' evidence)
No numeric classification thresholds were supplied by the script → classes are reviewed judgments from spread + 7A EPA + 9C stakes, not invented cutoffs. Sharp matchup evidence: STALE (Oct 27) → PARTIAL on every game.

| Game | Spread (FD) | Leg side | Class | Weight | Swing variable | Evidence status |
|---|---|---|---|---|---|---|
| MIN@DET | DET −3 | Gibbs | toss-up | 0.85 | DET run game vs #1 MIN D (EPA −.193) | EPA+stakes PASS; Sharp STALE → PARTIAL |
| BAL@BUF | BUF −3 | Cook | toss-up | 0.85 | BUF giveaways (9 in L4) | EPA+stakes PASS; Sharp STALE → PARTIAL |
| KC@DEN | KC −1.5 | Walker | toss-up | 0.85 | Walker RYOE +2.26 vs DEN #7 D, left-side leak 6.2 ypc | EPA+stakes PASS; Sharp STALE → PARTIAL |
| TEN@CIN | CIN −10 (Ghost6 −12.5) | Higgins | blowout favorite | 1.00 | Q4 sit / run-out once CIN leads | EPA+stakes PASS; Sharp STALE → PARTIAL |
| LAC@LAR | LAR −6.5 | Puka | moderate fav (possession) | 1.00 | LAC 0-6, off EPA #32 — LAR may run late | EPA+stakes PASS; Sharp STALE → PARTIAL |
| ARI@DAL | DAL −7 | Flournoy (cmp) | moderate fav (possession) | 1.00 | — | EPA+stakes PASS; Sharp STALE → PARTIAL |
| IND@JAX | JAX −10 | Tuten (cmp) | blowout favorite | 1.00 | wind 14–15 soft review | EPA+stakes PASS; Sharp STALE → PARTIAL |
| PHI@WSH | WSH −6 (Ghost6 −5.5) | A. Williams (cmp) | moderate fav (possession) | 1.00 | — | EPA+stakes PASS; Sharp STALE → PARTIAL |
| CLE@PIT | PIT −3.5 | Metcalf (cmp) | moderate fav (deep-ball) | 0.90 | — | EPA+stakes PASS; Sharp STALE → PARTIAL |

Weights are policy labels; they were NOT multiplied into sim probabilities.

## 10G-2 Underdog gate (Ghost6 10G rule)
BLOCK unless the opponent is verified ELIMINATED/TRAP. 9C: no team eliminated in week 8; no reviewed TRAP evidence.

| Leg | Team spread | Result |
|---|---|---|
| McBride rec | ARI +7 | **BLOCKED** (no exception). Simmed for the record only |
| Bowers rec | LV +1.5 | **BLOCKED** (no exception). Simmed for the record only |
| Goedert | PHI +6 | **BLOCKED** (no exception). Simmed for the record only |
| J. Taylor | IND +10 | **BLOCKED** (no exception). Simmed for the record only |
| Jefferson recyds | MIN +3 | **BLOCKED** (no exception). Simmed for the record only |
| A. Jones | MIN +3 | **BLOCKED** (no exception). Simmed for the record only |
| Bijan | ATL +2.5 | **BLOCKED** (no exception). Simmed for the record only |
| London recyds | ATL +2.5 | **BLOCKED** (no exception). Simmed for the record only |
| Flowers recyds | BAL +3 | **BLOCKED** (no exception). Simmed for the record only |

## 10G-3 Edge table (all non-underdog legs; edge = avg(MC,bias,GR) − FD no-vig; pass band +3…+15; robustness = edge under 30% per-play-yards shrink toward league position mean)

| Leg | Rung | FD | No-vig | MC | Bias | GR | Avg | Edge | Shrink-30 edge | Medians MC/B/GR | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs|rushyds | 50+ | -800 ⚠bonus(<−250) | 0.838 | 0.941 | 0.885 | 0.901 | 0.909 | +7.1 | +6.2 | 100.2/87.6/97.2 | PASS |
| Jahmyr Gibbs|rushyds | 60+ | -420 ⚠bonus(<−250) | 0.761 | 0.886 | 0.806 | 0.833 | 0.842 | +8.1 | +6.5 | 100.2/87.6/97.2 | PASS |
| Jahmyr Gibbs|rushyds | 70+ | -250 | 0.673 | 0.812 | 0.701 | 0.750 | 0.754 | +8.1 | +6.3 | 100.2/87.6/97.2 | PASS |
| Jahmyr Gibbs|rushyds | 80+ | -162 | 0.583 | 0.720 | 0.592 | 0.661 | 0.657 | +7.5 | +4.4 | 100.2/87.6/97.2 | PASS |
| CeeDee Lamb|rec | 5+ | -440 ⚠bonus(<−250) | 0.761 | 0.746 | 0.667 | 0.716 | 0.710 | -5.2 | n/a | 7.0/6.0/7.0 | FAIL edge |
| CeeDee Lamb|rec | 6+ | -205 | 0.628 | 0.643 | 0.556 | 0.618 | 0.606 | -2.3 | n/a | 7.0/6.0/7.0 | FAIL edge |
| CeeDee Lamb|rec | 7+ | -106 | 0.481 | 0.538 | 0.449 | 0.521 | 0.503 | +2.2 | n/a | 7.0/6.0/7.0 | FAIL edge |
| James Cook|rushyds | 50+ | -650 ⚠bonus(<−250) | 0.817 | 0.923 | 0.857 | 0.896 | 0.892 | +7.5 | +4.8 | 96.6/83.6/94.7 | PASS |
| James Cook|rushyds | 60+ | -340 ⚠bonus(<−250) | 0.728 | 0.861 | 0.762 | 0.828 | 0.817 | +8.9 | +5.1 | 96.6/83.6/94.7 | PASS |
| James Cook|rushyds | 70+ | -210 | 0.638 | 0.774 | 0.654 | 0.736 | 0.722 | +8.3 | +3.6 | 96.6/83.6/94.7 | PASS |
| James Cook|rushyds | 80+ | -130 | 0.533 | 0.680 | 0.539 | 0.643 | 0.621 | +8.8 | +2.8 | 96.6/83.6/94.7 | FAIL robustness |
| Kenneth Walker III|rushyds | 50+ | -670 ⚠bonus(<−250) | 0.820 | 0.936 | 0.888 | 0.901 | 0.908 | +8.8 | +6.1 | 107.9/93.7/105.9 | PASS |
| Kenneth Walker III|rushyds | 60+ | -360 ⚠bonus(<−250) | 0.738 | 0.885 | 0.810 | 0.843 | 0.846 | +10.9 | +6.2 | 107.9/93.7/105.9 | PASS |
| Kenneth Walker III|rushyds | 70+ | -225 | 0.652 | 0.814 | 0.721 | 0.768 | 0.768 | +11.5 | +6.1 | 107.9/93.7/105.9 | PASS |
| Kenneth Walker III|rushyds | 80+ | -144 | 0.556 | 0.730 | 0.616 | 0.688 | 0.678 | +12.2 | +6.1 | 107.9/93.7/105.9 | PASS |
| Tee Higgins|recyds | 40+ | -500 ⚠bonus(<−250) | 0.785 | 0.873 | 0.808 | 0.877 | 0.853 | +6.7 | +4.3 | 96.2/79.3/95.2 | PASS |
| Tee Higgins|recyds | 50+ | -300 ⚠bonus(<−250) | 0.707 | 0.817 | 0.733 | 0.820 | 0.790 | +8.3 | +5.3 | 96.2/79.3/95.2 | PASS |
| Tee Higgins|recyds | 60+ | -186 | 0.613 | 0.748 | 0.652 | 0.750 | 0.716 | +10.4 | +6.9 | 96.2/79.3/95.2 | PASS |
| Tee Higgins|recyds | 70+ | -120 | 0.514 | 0.680 | 0.571 | 0.681 | 0.644 | +13.0 | +8.8 | 96.2/79.3/95.2 | PASS |
| Puka Nacua|rec | 7+ | -260 ⚠bonus(<−250) | 0.675 | 0.701 | 0.616 | 0.711 | 0.676 | +0.1 | +0.1 | 9.0/8.0/9.0 | FAIL edge |
| Puka Nacua|rec | 8+ | -138 | 0.542 | 0.622 | 0.531 | 0.626 | 0.593 | +5.1 | +5.1 | 9.0/8.0/9.0 | PASS |
| Puka Nacua|recyds | 70+ | -290 ⚠bonus(<−250) | 0.701 | 0.664 | 0.555 | 0.667 | 0.629 | -7.2 | -4.2 | 94.5/78.4/94.5 | FAIL edge |
| Jahmyr Gibbs|rushrec (main) | 121.5+ | -113 | 0.498 | 0.644 | 0.468 | 0.601 | 0.571 | +7.3 | +3.3 | 136.8/118.3/133.7 | gates pass, NOT CARDED (bias med <121.5; shrink +3.3 marginal; same player as Gibbs rush) |
| Amon-Ra St. Brown|rec | 5+ | -670 ⚠bonus(<−250) | 0.814 | 0.848 | 0.771 | 0.801 | 0.807 | -0.7 | n/a | 7.0/6.0/7.0 | FAIL edge |
| Amon-Ra St. Brown|rec | 6+ | -300 ⚠bonus(<−250) | 0.701 | 0.731 | 0.627 | 0.685 | 0.681 | -2.1 | n/a | 7.0/6.0/7.0 | FAIL edge |
| Amon-Ra St. Brown|rec | 7+ | -158 | 0.573 | 0.590 | 0.471 | 0.556 | 0.539 | -3.4 | n/a | 7.0/6.0/7.0 | FAIL edge |
| Garrett Wilson|recyds | 40+ | -390 ⚠bonus(<−250) | 0.750 | 0.678 | 0.585 | 0.639 | 0.634 | -11.6 | n/a | 57.1/48.0/54.9 | FAIL edge |
| Garrett Wilson|recyds | 50+ | -230 | 0.657 | 0.575 | 0.480 | 0.543 | 0.533 | -12.4 | n/a | 57.1/48.0/54.9 | FAIL edge |
| Parker Washington|recyds | 40+ | -440 ⚠bonus(<−250) | 0.768 | 0.718 | 0.631 | 0.674 | 0.674 | -9.4 | n/a | 63.3/53.2/61.2 | FAIL edge |
| Parker Washington|recyds | 50+ | -250 | 0.673 | 0.623 | 0.530 | 0.588 | 0.580 | -9.3 | n/a | 63.3/53.2/61.2 | FAIL edge |
| Javonte Williams|rushyds | 50+ | -470 ⚠bonus(<−250) | 0.777 | 0.697 | 0.596 | 0.638 | 0.644 | -13.3 | n/a | 65.3/57.2/62.2 | FAIL edge |
| Javonte Williams|rushyds | 60+ | -260 ⚠bonus(<−250) | 0.681 | 0.576 | 0.460 | 0.528 | 0.522 | -15.9 | n/a | 65.3/57.2/62.2 | FAIL edge |
| Javonte Williams|rushyds | 70+ | -160 | 0.580 | 0.446 | 0.327 | 0.416 | 0.396 | -18.4 | n/a | 65.3/57.2/62.2 | FAIL edge |
| DK Metcalf|recyds | 40+ | -225 | 0.652 | 0.563 | 0.480 | 0.560 | 0.534 | -11.8 | n/a | 45.4/38.2/45.4 | FAIL edge |
| Ryan Flournoy|rec | 3+ | -240 | 0.660 | 0.715 | 0.642 | 0.665 | 0.674 | +1.3 | n/a | 4.0/3.0/3.0 | FAIL edge |
| Antonio Williams|rec | 3+ | -200 | 0.623 | 0.587 | 0.510 | 0.554 | 0.550 | -7.3 | n/a | 3.0/3.0/3.0 | FAIL edge |
| Bhayshul Tuten|rushyds | 50+ | -270 ⚠bonus(<−250) | 0.688 | 0.775 | 0.656 | 0.744 | 0.725 | +3.7 | +3.7 | 67.9/59.5/67.9 | edge passes, but comparison-only (not walked Ph1–4); JAX wind soft review |
| Bhayshul Tuten|rushyds | 60+ | -158 | 0.577 | 0.623 | 0.487 | 0.605 | 0.572 | -0.5 | -0.5 | 67.9/59.5/67.9 | FAIL edge |
| Jahmyr Gibbs|rushrec | **90+** | **NOT POSTED** | — | 0.887 | 0.779 | 0.842 | 0.836 | GAP | — | 136.8/118.3/133.7 | **UNPRICED → cannot pass edge gate** |

Gibbs rush 121.5 R+R main: edge +7.3 but bias median 118 < 121.5 and shrink-30 edge ≈ +3.2 (marginal); same player as the Gibbs rush leg → not stacked. Not carded.

### Requested separate edges
- **Gibbs 60+ rush (−420):** avg .842 vs no-vig .761 → **+8.1** (shrink-30 +6.5). PASS gates; ⚠ bonus flag (shorter than −250; a bonus bet returns only ~$0.24 per $1).
- **Gibbs 50+ rush fallback (−800):** +7.1. PASS; ⚠ bonus flag (~$0.125 per $1).
- **Lamb 5+ rec (−440):** avg .710 vs .761 → **−5.2 FAIL** (6+ −2.3, 7+ +2.2 — all fail). Lamb is cut.

### Gibbs 90+ rush+rec (Rico's change)
- FD fresh pull (7:37 PM): only the main **O121.5 −113 / U121.5 −115**; **no alt rush+rec ladder posted** → 90+ is UNPRICED (GAP). Not manufactured.
- Ours: MC .887 / bias .779 / GR .842 → avg .836, fair ≈ −510. Ghost6: .759/.646/.734 → avg .713, fair ≈ −248. Ours runs higher because our medians (137/118/134) sit above the market (121.5) and Ghost6's (121/105/121).
- 8A: the receiving part has the Phase 2 GAP (no RB→defender mapping) — disclosed, not counted as a pass; per 10G, RB receiving YPT cannot block the rushing component, so the rushing part is graded on its own evidence.
- Verdict: cannot be carded under our edge rule until FD posts a 90+ price. If FD prices it on Sunday: it passes only if the no-vig is ≤ .806 (our avg − 3), i.e. at roughly −585 or longer once ~6% vig is applied.

## 10G-4 GR input tables (card legs + Ghost6 comparison legs)
Common: margin ~ N(−spread, 13.5) [13.5 assumed, not fit]; pass-att slope bP −0.00679 / rush-att slope bR +0.00994 per margin pt (2026 pbp regression on final margin — endogeneity caveat); pace = lognormal with team log-SD of attempts; share ~ Beta (method of moments, L3-weighted, κ floor 2); GR mean volume anchored to the MC weighted mean (v2 fix); opp adjustment v3 shrunk 50% to 1.0; per-play yards bootstrapped from 2026 pbp. Correlation: within-leg volume↔script only; cross-leg independence assumed (all card legs are different games). Sources: nflverse pbp 2026 (sha e61a4040…), FD spread 7:37 PM.

| Leg | Dist (vol / yds) | Weighted mean vol | Team PA/RA | Pace σ | Spread shock | Opp adj (ypt/cr/ypc) | GR mean / median / p10–p90 | Seed (GR) |
|---|---|---|---|---|---|---|---|---|
| Jahmyr Gibbs|rushyds | Beta-share×team vol / bootstrap yds | car 22.6 | 39.2/26.7 | 0.19/0.32 | N(+3,13.5) | 0.86/0.95/0.99 | 103.7 / 97.2 / 50.6–165.663 | 27749317 |
| James Cook|rushyds | Beta-share×team vol / bootstrap yds | car 19.6 | 30.5/28.0 | 0.21/0.26 | N(+3,13.5) | 0.73/0.96/0.96 | 100.2 / 94.7 / 49.7–157.824 | 25035581 |
| Kenneth Walker III|rushyds | Beta-share×team vol / bootstrap yds | car 19.3 | 33.0/25.8 | 0.24/0.26 | N(+1.5,13.5) | 0.96/0.95/1.04 | 117.2 / 105.864 / 50.9–199.273 | 21841648 |
| Tee Higgins|recyds | Beta-share×team vol / bootstrap yds | tgt 8.6 | 38.2/21.7 | 0.21/0.24 | N(+10,13.5) | 1.07/1.09/1.00 | 103.9 / 95.2 / 35.3–183.553 | 27754971 |
| Puka Nacua|rec | Beta-share×team vol / binom catch | tgt 12.9 | 41.3/25.4 | 0.31/0.18 | N(+6.5,13.5) | 1.05/1.06/1.01 | 9.8 / 9 / 4–17 | 28079128 |
| Jahmyr Gibbs|rushrec | Beta-share×team vol / bootstrap yds | car 22.6 + tgt 6.5 | 39.2/26.7 | 0.19/0.32 | N(+3,13.5) | 0.86/0.95/0.99 | 139.9 / 133.665 / 79.606–207.644 | 26148938 |
| CeeDee Lamb|rec | Beta-share×team vol / binom catch | tgt 11.6 | 40.0/22.9 | 0.24/0.38 | N(+7,13.5) | 1.06/0.98/1.02 | 7.4 / 7 / 2–13 | 27574490 |
| Puka Nacua|recyds | Beta-share×team vol / bootstrap yds | tgt 12.9 | 41.3/25.4 | 0.31/0.18 | N(+6.5,13.5) | 1.05/1.06/1.01 | 105.1 / 94.5 / 33.8–190.008 | 28960684 |
| DK Metcalf|recyds | Beta-share×team vol / bootstrap yds | tgt 8.3 | 40.6/21.4 | 0.18/0.15 | N(+3.5,13.5) | 1.00/0.96/1.06 | 53.0 / 45.4 / 10.3–106.283 | 34248892 |
| Ryan Flournoy|rec | Beta-share×team vol / binom catch | tgt 5.7 | 40.0/22.9 | 0.24/0.38 | N(+7,13.5) | 1.06/0.98/1.02 | 3.7 / 3 / 1–7 | 34892896 |
| Antonio Williams|rec | Beta-share×team vol / binom catch | tgt 4.6 | 35.7/26.8 | 0.12/0.28 | N(+6,13.5) | 1.02/0.98/1.02 | 3.1 / 3 / 1–6 | 21285772 |
| Bhayshul Tuten|rushyds | Beta-share×team vol / bootstrap yds | car 16.2 | 32.2/26.8 | 0.22/0.09 | N(+10,13.5) | 1.20/0.94/1.04 | 69.9 / 67.9 / 34.5–108.635 | 25640654 |

## 10G-5 Leg-by-leg diff vs Ghost6 (`ghost6_sims.json`, `ghost6_gibbs_rr_sims.json`, `ghost6_phase9_10G_final.md`)

| Leg | Rung | Ghost6 MC/B/GR (avg) | Ours MC/B/GR (avg) | Gap | Why |
|---|---|---|---|---|---|
| Puka recyds | 70+ | 0.683/0.649/0.673 (0.668) | 0.664/0.555/0.667 (0.629) | -4.0 | Our bias mode is harsher on yds; our opp adj for LAC (12th pass D) slightly negative |
| Metcalf recyds | 40+ | 0.618/0.594/0.616 (0.609) | 0.563/0.480/0.560 (0.534) | -7.5 | Our bootstrap keeps his low-cushion, high-variance yds; CLE pass D 11th |
| Tuten rush | 50+ | 0.696/0.652/0.680 (0.676) | 0.775/0.656/0.744 (0.725) | +4.9 | Ours higher at 50 (bootstrap fat right tail + IND left-side run leak); comparison-only |
| Tuten rush | 60+ | 0.580/0.544/0.572 (0.565) | 0.623/0.487/0.605 (0.572) | +0.7 | Near-identical |
| Flournoy rec | 3+ | 0.683/0.622/0.676 (0.660) | 0.715/0.642/0.665 (0.674) | +1.4 | Our catch rate (rec+1)/(tgt+2) + ARI cr-allowed adj up |
| AWilliams rec | 3+ | 0.622/0.556/0.617 (0.598) | 0.587/0.510/0.554 (0.550) | -4.8 | We weight L3 at 0.4 on a small 26-tgt sample; lower share |
| Lamb rec | 5+ | 0.724/0.658/0.717 (0.700) | 0.746/0.667/0.716 (0.710) | +1.0 | Close |
| Lamb rec | 6+ | 0.609/0.529/0.604 (0.581) | 0.643/0.556/0.618 (0.606) | +2.5 | Close |
| Gibbs rush | 50+ | 0.869/0.841/0.850 (0.853) | 0.941/0.885/0.901 (0.909) | +5.6 | Ours higher: 0.6/0.4 season/L3 volume (L3 car 25,29…) vs Ghost6 wider gamma volume; MIN opp adj only via shrunk ypc → ours may be TOO OPTIMISTIC vs #1 MIN D (flag, not fixed further; shrink-30 kept edge ≥3) |
| Gibbs rush | 60+ | 0.796/0.767/0.778 (0.780) | 0.886/0.806/0.833 (0.842) | +6.2 | Ours higher: 0.6/0.4 season/L3 volume (L3 car 25,29…) vs Ghost6 wider gamma volume; MIN opp adj only via shrunk ypc → ours may be TOO OPTIMISTIC vs #1 MIN D (flag, not fixed further; shrink-30 kept edge ≥3) |
| Gibbs rush | 70+ | 0.713/0.677/0.697 (0.696) | 0.812/0.701/0.750 (0.754) | +5.9 | Ours higher: 0.6/0.4 season/L3 volume (L3 car 25,29…) vs Ghost6 wider gamma volume; MIN opp adj only via shrunk ypc → ours may be TOO OPTIMISTIC vs #1 MIN D (flag, not fixed further; shrink-30 kept edge ≥3) |
| McBride rec | 6+ | 0.723/0.651/0.711 (0.695) | 0.858/0.781/0.779 (0.806) | +11.1 | Ours higher (DAL TE catch-rate allowed); blocked anyway |
| McBride rec | 7+ | 0.622/0.538/0.614 (0.592) | 0.756/0.650/0.678 (0.695) | +10.3 | Ours higher (DAL TE catch-rate allowed); blocked anyway |
| Bowers rec | 5+ | 0.619/0.540/0.608 (0.589) | 0.760/0.671/0.687 (0.706) | +11.7 | Ours higher (NYJ TE adj); blocked anyway |
| Bowers rec | 6+ | 0.487/0.404/0.486 (0.459) | 0.611/0.505/0.559 (0.558) | +9.9 | Ours higher (NYJ TE adj); blocked anyway |
| Higgins rec | 5+ | 0.577/0.501/0.574 (0.551) | — | — | Not comparable: Ghost6 priced receptions, we priced yards |
| Gibbs R+R | 90+ | .759/.646/.734 (.713) | 0.887/0.779/0.842 | +12.3 | Our R+R median 137 vs Ghost6 121; game log 186/113/164/68/207/143. Ours likely optimistic vs MIN #1 D — moot (unpriced) |

**Over-optimism fixes we made (disclosed):** (1) v1 GR multiplied share × team mean and inflated volume (Walker GR median 118 vs MC 104; Javonte 75 vs 64) → **ours was too optimistic, fixed** in v2 by anchoring GR mean volume to MC. (2) v2 had no opponent effect → v3 added shrunk opponent adjustment. (3) Our RB medians still run 10–20 yds over FD mains → added the shrink-30 robustness gate; Cook 80+ and Gibbs R+R main fail/marginal under it and were dropped.

## 10G-6 Flags
- **Ticket 2 exact-prop bar** (Gibbs rec, St. Brown recyds, Godwin rec, London rec, Cook rushrec, Flowers rec, Pickens rec, Lamb recyds): no card leg is one of these. Same-player FLAGS: Gibbs rush (Ticket 2 has Gibbs rec), Cook rush (Ticket 2 has Cook rushrec — highly correlated exposure).
- **Higgins:** Higgins 50+ rec yds is on the open FD 8-leg SGP ($51.50) — our Higgins 60+ yds doubles that exposure. FLAG; the user decides.
- Ghost6's 'no player on more than one slip' rule: not ours — flag only.
- Same-game: every card leg is a different game → no FD SGP repricing within the card; still, do not add Gibbs R+R or St. Brown to Gibbs's group (same game, FD reprices).
- Film: all 8A reads UNVERIFIED → GAP (disclosed), never a pass.
- Bonus bets: Gibbs 60+ (−420) and 50+ (−800) are flagged; card uses Gibbs 70+ (−250, not shorter than −250).


## 10G-7 FINAL CARD (only legs passing every gate; no padding)
Gates applied to each leg: G1 non-underdog (10G) · G2 MC & GR medians ≥ rung (bias median disclosed) · G3 edge vs FD no-vig ≥ +3 and ≤ +15 · G4 shrink-30 robustness ≥ +3 · G5 not a Ticket-2 exact prop · G6 walked Phases 1–4 · G7 weather/injury PASS (9A/9D) · film = GAP disclosed (never a pass) · receiving legs: PFR cache Oct 29 (fresh pull 403).

**Group 1 — 5 legs, 5 different games (not an SGP), ≈ +829 at 7:37 PM FD prices**
| # | Leg | FD | MC / Bias / GR | Avg | No-vig | Edge (shrink-30) | Class/weight | Flags |
|---|---|---|---|---|---|---|---|---|
| 1 | Gibbs 70+ rush yds (DET −3 vs MIN) | −250 | .812 / .701 / .750 | .754 | .673 | +8.1 (+6.3) | toss-up 0.85 | MIN #1 D EPA — ours may be optimistic; Ticket 2 has Gibbs rec (same player, flag) |
| 2 | Cook 70+ rush yds (BUF −3 vs BAL) | −210 | .774 / .654 / .736 | .722 | .638 | +8.3 (+3.6) | toss-up 0.85 | Ticket 2 Cook rushrec → correlated exposure (flag); BUF 9 giveaways L4 |
| 3 | Walker 80+ rush yds (KC −1.5 at DEN) | −144 | .730 / .616 / .688 | .678 | .556 | +12.2 (+6.1) | toss-up 0.85 | largest edge → treat as model-suspect-adjacent |
| 4 | Higgins 60+ rec yds (CIN −10 vs TEN) | −186 | .748 / .652 / .750 | .716 | .613 | +10.4 (+6.9) | blowout 1.00 | open FD SGP has Higgins 50+ (doubled exposure); Q4-sit risk; chart UNVERIFIED; spread −10 vs Ghost6 −12.5 |
| 5 | Puka 8+ rec (LAR −6.5 vs LAC) | −138 | .622 / .531 / .626 | .593 | .542 | +5.1 (+5.1) | moderate fav possession 1.00 | bias median 8 = rung; Adams IR not modeled |
Product of avg probs (different games, independence assumed, UNCALIBRATED) ≈ .157 vs book-implied ≈ .108. Caveat: 3 of 5 are RB rushing overs where our model already runs 10–20 yds above FD mains — model error is correlated across these legs.
Groups 2 and 3: **not built** — no further legs pass every gate (no padding).
Separate edges (requested, not on card): Gibbs 60+ rush −420 +8.1 ⚠bonus; Gibbs 50+ −800 +7.1 ⚠bonus; Lamb 5+ −440 −5.2 FAIL.

## 10G-8 Side by side vs Ghost6's card (~+735)
| Ghost6 leg | FD | Ghost6 avg | Ours avg | No-vig | Our edge | Our verdict |
|---|---|---|---|---|---|---|
| Flournoy 3+ rec | −240 | .660 | .674 | .660 | +1.3 | FAIL edge (also not walked by us) |
| Tuten 60+ rush | −158 | .565 | .572 | .577 | −0.5 | FAIL edge; bias median 59.5 < 60; JAX wind soft review |
| Metcalf 40+ yds | −225 | .609 | .534 | .652 | −11.8 | FAIL edge; bias median 38 |
| Puka 70+ yds | −290 | .668 | .629 | .701 | −7.2 | FAIL edge; ⚠bonus |
| A. Williams 3+ rec | −200 | .598 | .550 | .623 | −7.3 | FAIL edge |
| Gibbs 90+ rush+rec | not posted | .713 (fair −248) | .836 (fair ≈ −510) | — | GAP | UNPRICED → cannot pass |
Agree: underdog blocks (McBride, Bowers, Flowers, etc.); Lamb not a play; Gibbs is the strongest DET piece; Puka is LAR's best angle (we prefer catches 8+ over 70+ yds).
Disagree: none of Ghost6's 5 priced legs beats FD no-vig by 3 in our sims; Ghost6's card is a lower-variance, short-price build, while ours takes rushing overs with larger modeled (uncalibrated) edges.
