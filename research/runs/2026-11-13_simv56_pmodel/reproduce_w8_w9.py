"""NFL-75 proof: calibration/simv56_pmodel reproduces the Phase 4 p_model for EVERY Week 8-9 main rush-yds Under leg.

Reads the box-local Phase 4 inputs (not committed; sha256 checked against the Phase 4 freeze manifest):
  confidence_check_2026-11-03/legs.csv          the legs the original sims ran on (player, gsis, team, opp, spread, line)
  selective_under_alt_2026-11-12/candidates.csv the Phase 4 p_model (kind=under, market=rushyds)
Runs the vendored engines on the COMMITTED W1-9 PBP + players table (cut at each week's run_sims cutoff), n=20,000,
opp 0.5, and compares exactly (the file's text value, parsed round_trip) and after pandas' default parse (Phase 4).

    python research/runs/2026-11-13_simv56_pmodel/reproduce_w8_w9.py [--weeks 8 9]"""
from __future__ import annotations
import argparse, hashlib, json, sys, tempfile, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from calibration import simv56_pmodel as SV  # noqa: E402

LEGS = Path("/workspace/nfl-database/backtests/confidence_check_2026-11-03/legs.csv")
CANDS = Path("/workspace/research/selective_under_alt_2026-11-12/candidates.csv")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", type=int, nargs="+", default=[8, 9])
    a = ap.parse_args(argv)
    man = json.loads((ROOT / "research/runs/2026-11-13_selective_edge_phase4/freeze_manifest.json").read_text())
    want = json.dumps(man)
    sha_c = hashlib.sha256(CANDS.read_bytes()).hexdigest()
    assert sha_c in want, "candidates.csv differs from the Phase 4 freeze manifest"
    C = pd.read_csv(CANDS, low_memory=False, float_precision="round_trip")
    C4 = pd.read_csv(CANDS, low_memory=False)                       # exactly how selective_edge_run reads it
    sel = (C.kind == "under") & (C.market == "rushyds")
    L = pd.read_csv(LEGS)
    rows, summary = [], []
    for w in a.weeks:
        lw = L[(L.week == w) & (L.market == "rushyds")].rename(columns={"team_spread": "spread"})
        with tempfile.TemporaryDirectory(dir="/tmp") as td:
            t0 = time.time()
            per = SV.run_all(lw[["player", "gsis", "team", "opp", "market", "spread", "line"]], week=w,
                             src=SV.make_src(Path(td) / "src"), workdir=Path(td))
            rt = time.time() - t0
        ens = SV.ensemble(per)
        c = C[sel & (C.week == w)][["gsis", "rung", "p_model"]]
        c4 = C4[sel & (C4.week == w)][["gsis", "p_model"]].rename(columns={"p_model": "p_model_phase4_mem"})
        m = ens.merge(c.assign(line=c.rung.astype(float)).drop(columns="rung"), on=["gsis", "line"]).merge(c4, on="gsis")
        rt_csv = pd.read_csv(pd.io.common.StringIO(m[["p_under"]].to_csv(index=False))).p_under.values
        m["exact_file"] = m.p_under == m.p_model
        m["exact_phase4_mem_after_csv"] = rt_csv == m.p_model_phase4_mem.values
        rows.append(m.assign(week=w))
        summary.append(dict(week=w, legs_run=len(lw), phase4_under_rows=int((sel & (C.week == w)).sum()), compared=len(m),
                            exact_file=int(m.exact_file.sum()), exact_phase4_after_csv=int(m.exact_phase4_mem_after_csv.sum()),
                            max_abs_diff=float((m.p_under - m.p_model).abs().max()), runtime_sec=round(rt, 1)))
    R = pd.concat(rows)
    R[["week", "gsis", "line", "p_under", "p_model", "exact_file", "exact_phase4_mem_after_csv"]].to_csv(
        HERE / "reproduction_w8_w9.csv", index=False)
    S = pd.DataFrame(summary)
    S.to_csv(HERE / "reproduction_summary.csv", index=False)
    print(S.to_string(index=False))


if __name__ == "__main__":
    main()
