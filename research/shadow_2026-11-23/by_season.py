"""Season-by-season check of the side-by-side candidates (owner, 2026-11-23): hold out 2023, 2024 and 2025 one at a
time, fit on every other season 2022-2026, and compare held-out log loss and Brier with and without each candidate.

    python3 research/shadow_2026-11-23/by_season.py      # writes by_season.json
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "watch_model_2026-11-16"))
sys.path.insert(0, str(HERE.parents[0] / "star_review_2026-11-23"))
spec = importlib.util.spec_from_file_location("shadow_study", HERE / "study.py")
S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
import fit as F  # noqa: E402


def score(tr, te, cols):
    m = sm.GLM(tr.hit80, sm.add_constant(tr[cols].astype(float)), family=sm.families.Binomial()).fit()
    p = m.predict(sm.add_constant(te[cols].astype(float), has_constant="add")).clip(1e-4, 1 - 1e-4)
    return m, float(-(te.hit80 * np.log(p) + (1 - te.hit80) * np.log(1 - p)).mean()), float(((p - te.hit80) ** 2).mean()), p


def main():
    r = S.add_streak_role(F.receivers())
    rc = S.add_coverage(r).dropna(subset=["cov_match"])
    cands = {"rising role (last game)": (r, ["last1"]), "streakiness (all three)": (r, ["l_cv", "big80", "ex20_rate"]), "man vs zone": (rc, ["cov_match"])}
    out = {}
    for name, (d, cols) in cands.items():
        rows = []
        for yr in (2023, 2024, 2025):
            tr, te = d[d.season != yr], d[d.season == yr]
            if te.empty:
                continue
            _, l0, b0, p0 = score(tr, te, S.RX)
            m, l1, b1, p1 = score(tr, te, S.RX + cols)
            st0, st1 = te[p0 >= 0.30], te[p1 >= 0.30]
            rows.append({"held_out": yr, "rows": int(len(te)), "logloss": [round(l0, 5), round(l1, 5)], "brier": [round(b0, 5), round(b1, 5)],
                         "better_both": bool(l1 < l0 and b1 < b0), "z": {c: round(float(m.params[c] / m.bse[c]), 2) for c in cols},
                         "stars_base": {"n": int(len(st0)), "hit": round(float(st0.hit80.mean()), 3) if len(st0) else None},
                         "stars_with": {"n": int(len(st1)), "hit": round(float(st1.hit80.mean()), 3) if len(st1) else None}})
        out[name] = {"seasons": rows, "better_in": f"{sum(x['better_both'] for x in rows)} of {len(rows)}"}
    (HERE / "by_season.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
