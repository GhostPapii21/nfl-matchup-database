"""NFL-75: re-grade the 23 gated rush-under backtest spots (the 18-5, Weeks 8-9 OOS) with the QB rush YPC prior fix.

Old p_model = the Phase 4 fit ensemble (committed fixture calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv,
phase4_p_model). New p_model = the same three engines, same settings (opp 0.5, n=20,000, same cutoffs, same calib
rule), run on the committed W1-9 PBP with qb_rush_prior=True (only QB rush legs change). Prices, outcomes and gates
are the box-local Phase 4 legs (legs_w4_9.csv, sha256 checked against the Phase 4 freeze manifest); 0 Odds API
credits. The frozen classifier (params_w4_7.json) and the 18-5 study rule (gated, edge vs no-vig >= +5 pts) are
applied unchanged. Book prices are not committed: the per-leg CSV carries probabilities, edges and outcomes only.

    python research/runs/2026-11-13_qb_rush_prior_regrade/regrade.py"""
from __future__ import annotations
import hashlib, json, os, sys, tempfile, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from calibration import simv56_pmodel as SV  # noqa: E402
from calibration import selective_edge as se  # noqa: E402

WORK = Path(os.environ.get("SELECTIVE_EDGE_WORK", "/tmp/selective_edge_phase4"))
FIX = ROOT / "calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv"
P4 = ROOT / "research/runs/2026-11-13_selective_edge_phase4"


def study(E):
    rec = E[(E.kind == "main") & (E.market == "rushyds") & (E.side == "Under") & E.label.isin([se.STRONG_UNDER, se.STANDARD])]
    return rec[rec.edge >= 0.05 - 1e-12]


def main():
    man = json.loads((P4 / "freeze_manifest.json").read_text())
    legs_f = WORK / "legs_w4_9.csv"
    sha = hashlib.sha256(legs_f.read_bytes()).hexdigest()
    assert sha == man["inputs_sha256"]["legs_w4_9.csv (built)"], "legs_w4_9.csv differs from the Phase 4 manifest"
    params = json.loads((P4 / "params_w4_7.json").read_text())
    F = pd.read_csv(FIX, float_precision="round_trip")
    new, meta = [], []
    for w in (8, 9):
        lw = F[F.week == w]
        with tempfile.TemporaryDirectory(dir="/tmp") as td:
            t0 = time.time()
            per = SV.run_all(lw, week=w, src=SV.make_src(Path(td) / "src"), workdir=Path(td), qb_rush_prior=True)
            rt = time.time() - t0
            errs = {e: int(d.err.notna().sum()) if "err" in d else 0 for e, d in per.items()}
        ens = SV.ensemble(per)[["gsis", "line", "p_under"]].assign(week=w)
        new.append(ens)
        meta.append(dict(week=w, legs=len(lw), cutoff=SV.cutoff_for_week(w), runtime_sec=round(rt, 1), engine_errors=errs))
    N = pd.concat(new).rename(columns={"p_under": "p_new"})
    O = F[["week", "gsis", "line", "player", "phase4_p_model"]].rename(columns={"phase4_p_model": "p_old"})
    PN = O.merge(N, on=["week", "gsis", "line"], how="left")
    L = pd.read_csv(legs_f, low_memory=False)
    L = L[L.week.isin(se.EVAL_WEEKS)].reset_index(drop=True)
    old_E = se.evaluate(L, params)
    m = (L.kind == "main") & (L.market == "rushyds")
    Ln = L.merge(PN[["week", "gsis", "line", "p_new", "p_old"]], on=["week", "gsis", "line"], how="left")
    assert len(Ln) == len(L)
    # old p_model must equal the fixture (Phase 4 values) on every main rush leg
    chk = Ln[m.values & Ln.p_old.notna()]
    assert (chk.p_model - chk.p_old).abs().max() <= 1e-12, "legs_w4_9 p_model differs from the Phase 4 fixture"
    Ln.loc[m.values & Ln.p_new.notna(), "p_model"] = Ln.loc[m.values & Ln.p_new.notna(), "p_new"]
    new_E = se.evaluate(Ln.drop(columns=["p_new", "p_old"]), params)
    o5, n5 = study(old_E), study(new_E)
    K = ["week", "gsis", "line"]
    keys = pd.concat([o5[K], n5[K]]).drop_duplicates()
    cols = ["week", "game_id", "player", "position", "line", "p_model", "edge", "label", "win", "push"]
    mo = old_E[(old_E.kind == "main") & (old_E.market == "rushyds") & (old_E.side == "Under")]
    mn = new_E[(new_E.kind == "main") & (new_E.market == "rushyds") & (new_E.side == "Under")]
    assert not mo.duplicated(K).any() and not mn.duplicated(K).any()
    T = keys.merge(mo[cols + ["gsis"]], on=K).merge(mn[K + ["p_model", "edge", "label"]], on=K, suffixes=("_old", "_new"))
    assert len(T) == len(keys)
    T["flag_old"] = T.set_index(K).index.isin(o5.set_index(K).index)
    T["flag_new"] = T.set_index(K).index.isin(n5.set_index(K).index)
    T["d_p"] = T.p_model_new - T.p_model_old
    T["result"] = T.win.map({1.0: "W", 0.0: "L"}).fillna("P")
    T["change"] = [("unchanged (not QB)" if pos != "QB" else "flagged -> flagged") if a and b else
                   ("flagged -> UNFLAGGED" if a else "NEW flag") for pos, a, b in zip(T.position, T.flag_old, T.flag_new)]
    T = T.sort_values(["flag_old", "position", "edge_old"], ascending=[False, True, False])
    out = ["week", "game_id", "player", "position", "line", "p_model_old", "p_model_new", "d_p", "edge_old", "edge_new",
           "label_old", "label_new", "flag_old", "flag_new", "result", "change"]
    T[out].to_csv(HERE / "regrade_23_spots.csv", index=False)
    S = []
    def add(view, d):
        S.append(dict(view=view, **se.summarize(d)))
    add("OLD 18-5 study rule (gated, edge >= +5), all positions", o5)
    add("NEW same rule, corrected QB prior, all positions", n5)
    add("OLD the 23, QB only", o5[o5.position == "QB"])
    add("NEW still-flagged of the 23 + new flags, QB only", n5[n5.position == "QB"])
    add("NEW the original 23 that stay flagged", n5[n5.set_index(K).index.isin(o5.set_index(K).index)])
    so = old_E[(old_E.label == se.STRONG_UNDER) & (old_E.market == "rushyds")]
    sn = new_E[(new_E.label == se.STRONG_UNDER) & (new_E.market == "rushyds")]
    add("OLD Phase 4 STRONG UNDER rushyds (edge >= 0), all", so)
    add("NEW Phase 4 STRONG UNDER rushyds (edge >= 0), all", sn)
    add("OLD Phase 4 STRONG UNDER rushyds, QB only (the 15-4)", so[so.position == "QB"])
    add("NEW Phase 4 STRONG UNDER rushyds, QB only", sn[sn.position == "QB"])
    pd.DataFrame(S).to_csv(HERE / "regrade_summary.csv", index=False)
    PN.to_csv(HERE / "p_model_old_new_w8_w9_rushyds.csv", index=False)
    (HERE / "regrade_meta.json").write_text(json.dumps(dict(
        runs=meta, n_trials=SV.N_TRIALS, opp=SV.OPP, engines=list(SV.ENGINES), engine_sha256=SV.verify_engines(),
        pbp=str(SV.PBP_DEFAULT.relative_to(ROOT)), pbp_sha256=SV._sha(SV.PBP_DEFAULT),
        legs_w4_9_sha256=sha, params_w4_7_sha256=SV._sha(P4 / "params_w4_7.json"), pandas_version=pd.__version__,
        bootstrap="game-cluster, B=%d, seed=%d (selective_edge.summarize)" % (se.BOOT_B, se.BOOT_SEED),
        odds_api_credits=0, qb_rush_prior=True), indent=1, default=str) + "\n")
    pd.set_option("display.width", 250)
    print(T[out].round(4).to_string(index=False))
    print(pd.DataFrame(S).round(4).to_string(index=False))
    print(json.dumps(meta, default=str))


if __name__ == "__main__":
    main()
