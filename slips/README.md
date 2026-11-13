# slips/: same-game slip probability from simulation joint outcomes (research only, not validated)

Rico's Nov 12 list, item 8 (Phase 6). `slips/joint.py` gives a slip's probability as the **empirical joint hit rate
across simulated trials** (the share of trials where every leg hits), and reports the **independent product** of the
same trials' marginals next to it, plus the lift (joint / independent). Inputs are `simulate_games` outputs
(`arrays.fg_home/fg_away` for game legs, `player_samples` for player legs). No prices are read or produced; a missing
quote is not an opportunity.

```python
from slips.joint import Leg, slip_probability
r = slip_probability(sim, [Leg("rec_yards", "NYG|M.Nabers", ">=", 40), Leg("game", "total", "<", 54.5)])
r["p_joint"], r["p_independent"], r["lift_joint_over_independent"], r["p_joint_wilson95"]
```

**Status: opt-in. It does not replace anything by default**, because the historical validation below does not show
that it beats independence yet.

## Historical validation (weeks 4-9 2026, BACKTEST on already-seen weeks, not a clean holdout)
`python3 -m calibration.slip_joint_validation --n 2000 --workers 7 --tag wk04_09`. Engine main 3dad900 (clean),
new_off arm, point-in-time history, seed base 20261112. 88 games, 1,320 slips built, 1,128 graded (192 void: a push or a
player with no credited play). Slip legs use the real consensus close total/spread (ba83615, sha256 matches
data/lines/README.md) or the sim's own player/team medians. Outputs:
`calibration/outputs/slip_joint_validation_wk04_09_n2000.json` and `..._slips.csv`.

| Family | Slips | Hit rate | Mean p_joint | Mean p_indep | Brier joint | Brier indep | Δ Brier (indep − joint), 95% game-bootstrap CI |
|---|---|---|---|---|---|---|---|
| All | 1128 | 0.233 | 0.265 | 0.229 | 0.1879 | 0.1850 | −0.0029 [−0.0068, +0.0013] |
| Total × side (close lines) | 340 | 0.250 | 0.247 | 0.247 | 0.2109 | 0.2093 | −0.0016 [−0.0030, −0.0001] |
| QB1 + WR1 | 142 | 0.190 | 0.335 | 0.246 | 0.1723 | 0.1571 | −0.0152 [−0.0281, −0.0013] |
| QB1 + team points | 154 | 0.299 | 0.319 | 0.230 | 0.2130 | 0.2155 | +0.0026 [−0.0113, +0.0166] |
| RB1 + team win | 150 | 0.287 | 0.279 | 0.249 | 0.2108 | 0.2107 | −0.0001 [−0.0039, +0.0038] |
| RB1 + QB1 | 133 | 0.211 | 0.245 | 0.244 | 0.1673 | 0.1676 | +0.0002 [−0.0009, +0.0014] |
| QB1 + QB1 (both teams) | 67 | 0.254 | 0.226 | 0.247 | 0.1903 | 0.1897 | −0.0006 [−0.0057, +0.0037] |
| QB1 + WR1 + over close | 142 | 0.120 | 0.202 | 0.122 | 0.1156 | 0.1084 | −0.0072 [−0.0172, +0.0045] |

Read: positive Δ means the joint method beat independence. **Overall it did not** (CI spans 0, point estimate worse).
It is clearly worse on QB1+WR1 stacks: the sim puts their joint at 0.335 (lift 1.37) but they hit 0.190, below even
the independent 0.246. What the data shows (neither point is fixed here):
1. **Main identified issue: player marginals are biased.** Legs set at the sim's own median should hit about 50%.
   Counted once per distinct leg, they hit **46.8% for passing yards (72/154), 40.4% for rushing yards (61/151) and
   34.5% for receiving yards (49/142)**. Picking WR1 by sim mean also selects players whose sim median runs high. Even
   with the realized correlation, an independent product of about 0.25 times lift 1.19 is about 0.29, still far above
   the 0.19 hit rate.
2. **Correlation overstatement: plausible, not established.** In the real games, the 142 QB1 + WR1 slips show a
   realized lift of **1.19** (P(QB leg) 0.465, P(WR leg) 0.345, P(both) 0.190), with a 95% game-bootstrap CI of about
   **[0.93, 1.44]** (Ghost6's review; an independent rerun with 5,000 resamples gives [0.94, 1.45]). The sim's mean
   lift on the same slips is **1.37**, which sits inside that range. Because the yard-row bootstrap ties a receiver's
   yards to his QB's in the same rows, overstatement is plausible, but this sample does not show it.
Same-team QB1 + team points is the only family where joint points the right way (+0.0026), and that is not
significant.

**Recommendation:** keep reporting the independent product as the baseline and show p_joint next to it, labeled
"sim joint, not validated". Do not price slips from p_joint until a holdout (weeks 10-12) shows it beats independence.
Fixing the player-marginal bias is the precondition.

Figures above are recomputed from `calibration/outputs/slip_joint_validation_wk04_09_n2000_slips.csv` (unique legs
per game/player/line; QB1 + WR1 family for the lift).

Tests: `slips/tests` (10 synthetic exact-answer tests + 1 seeded engine integration test) and
`calibration/tests/test_slip_joint_validation.py` (grading, void and sign rules).
