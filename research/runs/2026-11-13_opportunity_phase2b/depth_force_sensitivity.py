"""Phase 2b: why the depth signal does not re-add stale charted players (McLaurin / Croskey-Merritt), from data.

1. Training log likelihood (Dirichlet-multinomial, kappa profiled) of the W10 fit's carry / target slots under
   force = False / "top" / True and K = 0 / 1 / 99, all other parameters at the frozen W10 fit (data through W9).
2. WAS Week-10 candidate base shares under the fitted rule vs force=True (NOT fitted; sensitivity only), with each
   player's point-in-time depth rank. No Week 10 actual is read.
    python3 research/runs/2026-11-13_opportunity_phase2b/depth_force_sensitivity.py
Research only."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from calibration import opportunity_fit as F  # noqa: E402

p = json.loads((HERE / "params/params_2026_w10.json").read_text())
kap = np.array(F.KAPPA_GRID)
L = ["# Depth signal: forcing stale charted players (W10 fit, data through 2026 W9)", "",
     "Training DM log likelihood (higher is better), other parameters at the frozen W10 fit:", "",
     "| slot | K | force=False (fitted) | force=top (RB2/WR3/TE1) | force=True |", "|---|---|---|---|---|"]
for slot in ("carry", "target"):
    q = p["slots"][slot]
    tr = F.train_set(2026, 10, slot)
    for K in (0, 1, 99):
        cells = []
        for force in (False, "top", True):
            dp = {**q["depth"], "force": force}
            u = F._u_for(tr, q["lam"], q["gamma"], K, dp)
            cells.append(float(F._dm_ll(F._preds(tr, q["lam"], q["gamma"], K, q["alpha"], u, dp), kap).max()))
        L.append(f"| {slot} | {K} | {cells[0]:.1f} | {cells[1]:.1f} | {cells[2]:.1f} |")
ch = F.depth_skill(2026, "WAS", 10)
L += ["", "WAS Week 10 base shares (before availability), fitted rule vs force=True (sensitivity, not fitted):", "",
      "| slot | player | depth chart | share fitted | share force=True |", "|---|---|---|---|---|"]
for slot in ("carry", "target"):
    q = p["slots"][slot]
    x = F.team_game_inputs(2026, "WAS", 10, slot)
    res = {}
    for lab, force in (("fit", False), ("force", True)):
        keep, s = F.base_shares(x, q["lam"], q["gamma"], q["K"], q["u"], {**q["depth"], "force": force})
        res[lab] = {x["names"][j]: float(v) for j, v in zip(np.where(keep)[0], s[:-1])}
    pid = dict(zip(x["names"], x["pids"]))
    for nm in sorted(set(res["fit"]) | set(res["force"]), key=lambda n: -res["force"].get(n, 0)):
        d = ch.get(pid.get(nm)) if ch else None
        L.append(f"| {slot} | {nm} | {d[0] + str(d[1]) if d else 'not charted'} | {res['fit'].get(nm, 0):.3f} | "
                 f"{res['force'].get(nm, 0):.3f} |")
L.append("")
(HERE / "depth_force_sensitivity.md").write_text("\n".join(L))
print("\n".join(L))
