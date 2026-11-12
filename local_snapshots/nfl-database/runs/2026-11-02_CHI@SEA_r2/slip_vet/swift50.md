# Swift 50+ rush+rec (FD 'ALT RUSHING + RECEIVING YDS'): CHI@SEA MNF 2026-11-02. Tag: fixed-model, copies only. NOT VETTED.
Sim: tools/sim_v6_fix via slip_vet/swift50_sims.py, market rushrec, current_qb Caleb Williams (4 games), spread CHI +3, MC/Bias/GR x 100k, seed 20261101. Raw: raw_swift50.json.
Odds: The Odds API, pulled 8:27 AM ET (odds_m_sw.csv, 1250 rows, 0 in-play). Fresh until 9:27 AM ET.

## Price
- FD main rush+rec 81.5 -113/-113 → overround 1.061.
- FD alt rush+rec ladder: NOT in the feed (FD alt rush, alt rec posted; alt rush+rec absent). Slip screenshot shows no per-leg price. → FD 49.5 price MISSING.
- Proxy: DK alt 49.5 = -670 (implied .870); DK main 82.5 -111/-115 (overround 1.061) → no-vig .820. Comparison only, not price of record.
- Break-even: shrunk p' .775 clears only if FD alt is longer than about -460.

## Models (49.5 / 59.5 / 81.5; median)
| Model | p 49.5 | p 59.5 | p 81.5 | median |
|---|---|---|---|---|
| MC | .908 | .819 | .552 | 85.6 |
| Bias | .914 | .828 | .565 | 86.8 |
| GR | .856 | .767 | .537 | 85.0 |
avg p(49.5) .893. vs no-vig .820 (DK proxy): raw +7.3; Ghost6 shrink p' .775 → -4.5; x0.7 +5.1. Bar (+3 after shrink) FAILS. Min p .856 ≥ .45 PASS; medians clear 49.5 PASS; median vs main 81.5 within 12 (no MODEL-SUSPECT).

## §7 at 50 with Caleb (pbp verified): 134, 99, 70, 90 → 4/4 PASS (Wk1,2,6,7). Non-Caleb games 88,74,73 also clear.
## Opportunity: carries 18,16,16,22 (share 46/52/48/73% of team rushes incl. QB); targets 1,5,5,4. Carries stable 16+ in 4/4 → NOT mixed, PASS. Receiving volume variable (1-5).
## Context: SEA 71.0 RB rush ypg allowed (29th), 3.40-3.48 YPC (suppression ≤3.8), 5.4 RB rec/g (4th most). Monangai OUT → Swift lead back. Projection ~17 car × 3.45 ≈ 59 + ~15 rec yds ≈ 74. Earlier Swift rush U59.5 cut on §7 (2/4) — consistent with this over at 50 holding. CHI +3 dog: RB legs follow RB fix D, not the 10G blanket block.
## Verdict: CUT on price (shrunk edge -4.5 vs proxy; FD alt price MISSING). Strong lean on the outcome (~86-91%), but no edge at ~-670.
