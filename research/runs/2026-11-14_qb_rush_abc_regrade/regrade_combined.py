"""NFL-75: diagnostic re-grade of the 23 gated rush-under backtest spots on a LOCAL, UNMERGED
combination of draft PRs A (settlement/EV), B (volume_fix), C (QB gate) and PR #47 (qb_rush_prior
at f4ce5e1). Research only; not counted; projection_ready stays false. 0 Odds API credits. refs NFL-75

    python research/runs/2026-11-14_qb_rush_abc_regrade/regrade_combined.py --code-sha <sha> \
        --mode off|prior|components --volume-fix --out-root <dir>

`--mode off` means qb_rush_prior is off; volume_fix and the EV gate still apply when those flags
are on. Refuses unless HEAD is --code-sha and calibration/ has no uncommitted change.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from calibration import simv56_pmodel as SV  # noqa: E402
from calibration import selective_edge as se  # noqa: E402
from calibration import settlement_ev as SEV  # noqa: E402  (PR A)

WORK = Path(os.environ.get("SELECTIVE_EDGE_WORK", "/tmp/selective_edge_phase4"))
FIX = ROOT / "calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv"
P4 = ROOT / "research/runs/2026-11-13_selective_edge_phase4"


def study(E):
    E = SEV.apply_ev_gate(E, se.CANDIDATE_LABELS, se.NO_EDGE)   # PR A: candidate labels need EV > 0 at the price
    rec = E[(E.kind == "main") & (E.market == "rushyds") & (E.side == "Under") & E.label.isin([se.STRONG_UNDER, se.STANDARD])]
    return rec[rec.edge >= 0.05 - 1e-12]


def _git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-sha", required=True, help="commit the code must be at (HEAD), full or prefix")
    ap.add_argument("--mode", choices=["prior", "components", "off"], default="prior")
    ap.add_argument("--label", default=None)
    ap.add_argument("--out-root", default=str(HERE))
    ap.add_argument("--volume-fix", action="store_true", help="PR B opt-in engine volume fixes")
    a = ap.parse_args(argv)
    head = _git("rev-parse", "HEAD")
    if not head.startswith(a.code_sha):
        raise SystemExit(f"HEAD {head} is not --code-sha {a.code_sha}; check out that commit first")
    if _git("status", "--porcelain", "--", "calibration"):
        raise SystemExit("calibration/ has uncommitted changes; the regrade must run on committed code")
    qrp = {"prior": True, "components": "components", "off": False}[a.mode]
    label = a.label or {"prior": "QB-prior fix only", "components": "QB-prior fix + designed/scramble/kneel components",
                        "off": "unfixed Phase 4 ensemble (control)"}[a.mode]
    label = ("combined, unmerged, research only, not counted: " + label
             + (" + volume_fix" if a.volume_fix else "") + " + EV gate")
    OUT = Path(a.out_root) / f"combined_{a.mode}{'_vf' if a.volume_fix else ''}_{head[:7]}"
    OUT.mkdir(parents=True, exist_ok=True)
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
            per = SV.run_all(lw, week=w, src=SV.make_src(Path(td) / "src"), workdir=Path(td), qb_rush_prior=qrp,
                             volume_fix=a.volume_fix)
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
    T[out].to_csv(OUT / "regrade_23_spots.csv", index=False)
    S = []
    def add(view, d):
        S.append(dict(view=view, **se.summarize(d)))
    print(f"== {label} | mode={a.mode} | code {head}")
    add("OLD 18-5 study rule (gated, edge >= +5), all positions", o5)
    add("NEW same rule, corrected QB prior, all positions", n5)
    add("OLD the 23, QB only", o5[o5.position == "QB"])
    add("NEW still-flagged of the 23 + new flags, QB only", n5[n5.position == "QB"])
    add("NEW the original 23 that stay flagged", n5[n5.set_index(K).index.isin(o5.set_index(K).index)])
    oE = SEV.apply_ev_gate(old_E, se.CANDIDATE_LABELS, se.NO_EDGE)
    nE = SEV.apply_ev_gate(new_E, se.CANDIDATE_LABELS, se.NO_EDGE)
    so = oE[(oE.label == se.STRONG_UNDER) & (old_E.market == "rushyds")]
    sn = nE[(nE.label == se.STRONG_UNDER) & (nE.market == "rushyds")]
    add("OLD Phase 4 STRONG UNDER rushyds (edge >= 0), all", so)
    add("NEW Phase 4 STRONG UNDER rushyds (edge >= 0), all", sn)
    add("OLD Phase 4 STRONG UNDER rushyds, QB only (the 15-4)", so[so.position == "QB"])
    add("NEW Phase 4 STRONG UNDER rushyds, QB only", sn[sn.position == "QB"])
    pd.DataFrame(S).to_csv(OUT / "regrade_summary.csv", index=False)
    PN.to_csv(OUT / "p_model_old_new_w8_w9_rushyds.csv", index=False)
    (OUT / "regrade_meta.json").write_text(json.dumps(dict(
        runs=meta, n_trials=SV.N_TRIALS, opp=SV.OPP, engines=list(SV.ENGINES), engine_sha256=SV.verify_engines(),
        pbp=str(SV.PBP_DEFAULT.relative_to(ROOT)), pbp_sha256=SV._sha(SV.PBP_DEFAULT),
        legs_w4_9_sha256=sha, params_w4_7_sha256=SV._sha(P4 / "params_w4_7.json"), pandas_version=pd.__version__,
        bootstrap="game-cluster, B=%d, seed=%d (selective_edge.summarize)" % (se.BOOT_B, se.BOOT_SEED),
        odds_api_credits=0, qb_rush_prior=qrp, volume_fix=a.volume_fix, ev_gate=True, mode=a.mode, label=label,
        code_sha=head, diagnostic_only=True, counted=False, projection_ready=False,
        combined_of=["PR A settlement/EV", "PR B volume_fix", "PR C QB gate", "PR #47 qb_rush_prior f4ce5e1"]),
        indent=1, default=str) + "\n")
    pd.set_option("display.width", 250)
    print(T[out].round(4).to_string(index=False))
    print(pd.DataFrame(S).round(4).to_string(index=False))
    print(json.dumps(meta, default=str))


if __name__ == "__main__":
    main()
