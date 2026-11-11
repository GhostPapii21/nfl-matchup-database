# Hamilton / BAL slot+TE suppression test (2026 Wk1-8) — read-only
Data: nflverse pbp_2026 + roster_2026 (local). Participation 2026 not published on nflverse releases (404) and local copies corrupt, so NO alignment data.
Player selection: every TE (roster position) targeted vs BAL + known slot WRs (Downs, Lamb, Tate, Concepcion, Shakir; public role, not alignment-verified; Tate's slot role is least certain). Coverage by Hamilton is ASSUMED, not charted.
Baseline: mean & median of the player's 2026 games NOT vs BAL (Wk1-8). Kept rows with >=2 tgt vs BAL or >=3 baseline tgt/game. UNDER = below both mean and median yds.
Full table: hamilton_test.csv (script hamilton_test.py).

## Results
- All 18: 11 OVER, 5 UNDER, 2 MIXED; avg yds +7.3 vs mean (+11.7 vs median); receptions -0.08.
- TEs (13): 8 OVER / 4 UNDER / 1 MIXED; avg yds 0.0 vs mean.
- Primary TEs only (8): Warren -31, J.Johnson +35, Ferguson +8, Helm -21, Pitts +20, Fannin -48, Gesicki -41, Kincaid +34 → 4 under / 4 over, avg -5.7 yds. Coin flip.
- Slot WRs (5): 3 OVER / 1 UNDER / 1 MIXED; avg +26 yds (Tate +100, Lamb +27/+42, Shakir +17; Downs -5, Concepcion ~0).
Context: Wk1 IND (Warren held) and Wk6 CLE (Fannin held, rookie QB/low-volume pass game) and Wk7 CIN (Gesicki 1 tgt; targets went to Higgins/Chase) explain unders more by volume/game script than coverage. Kincaid 86 came vs BAL's Wk8 loss where BUF controlled.

## Verdict
No real evidence Hamilton/BAL suppresses slot or TE production. TEs land at their normal output (half under, half over); slot WRs are above normal. Per Rico's rule, "Hamilton strong in slot" and PFF "BAL top-5 vs TE" should NOT count as data.
- Strange rec yds o35.5: the PFF CAUTION flag loses weight; neutral-to-supportive (TEs not suppressed, seam/deep middle 18.4 yds/tgt from prior snapshot). Still needs his own 3-of-4 gate.
- P. Washington rec u4.5: the "Hamilton locks the slot" rationale is undercut (slots averaged +0.7 rec). Leg must stand on Washington's own baseline/volume, not the matchup.
