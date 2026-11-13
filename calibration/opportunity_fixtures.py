"""Build the two frozen opportunity models committed for tests / the WAS@NYG sanity table:
  model_2026_w10_WAS_NYG.json  (fit on 2024-2025 + 2026 weeks 1-9; pregame model for Nov 12 TNF, never scored)
  model_2026_w09_JAX_BAL.json  (fit on 2024-2025 + 2026 weeks 1-8; matches config research_variant_def_allowed_w05)
    python3 -m calibration.opportunity_fixtures
Research only. projection_ready stays false."""
from __future__ import annotations
import json
from concurrent.futures import ProcessPoolExecutor

from calibration import opportunity_fit as F

OUT = F.ROOT / "research/runs/2026-11-13_opportunity_phase2"
GAMES = ((10, "WAS", "NYG"), (9, "JAX", "BAL"))


def _one(g):
    w, away, home = g
    pf = OUT / f"params/params_2026_w{w:02d}.json"
    if pf.exists():
        params = json.loads(pf.read_text())
    else:
        params = F.fit_week(2026, w)
        pf.write_text(json.dumps(params, indent=1, default=str) + "\n")
    m = F.build_model(2026, w, [home, away], params)
    m["meta"]["sources"] = F.verify_sources()
    (OUT / f"models/model_2026_w{w:02d}_{away}_{home}.json").write_text(json.dumps(m, indent=0, default=float) + "\n")
    return str(pf)


if __name__ == "__main__":
    (OUT / "params").mkdir(parents=True, exist_ok=True)
    (OUT / "models").mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(2) as ex:
        print(list(ex.map(_one, GAMES)))
