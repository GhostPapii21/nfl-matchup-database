"""NFL-75 Phase 4 driver: build Weeks 4-9 candidate legs, fit on Weeks 4-7, evaluate the frozen classifier on 8-9.

    python3 -m calibration.selective_edge_run build   # box-local legs (book prices are NOT committed)
    python3 -m calibration.selective_edge_run fit     # Weeks 4-7 only -> params_w4_7.json (aggregates only)
    python3 -m calibration.selective_edge_freeze freeze <work>/inputs_sha256.json ; git commit
    python3 -m calibration.selective_edge_run eval    # verifies the freeze first, then scores Weeks 8-9

Inputs (box-local, sha256-pinned in the freeze manifest; 0 Odds API credits):
  CANDIDATES  backtests/selective_under_alt_2026-11-12 candidates.csv (real saved prices: main-line props = one book's
              two-sided price ~34 min pre-kick; alt rungs = best real one-sided price across books, verified pre-kick)
  LEGS        confidence_check_2026-11-03/legs_with_probs.csv (book name, pre-kick minutes for main legs)
  PBP         data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet (committed)
p_model is the pre-registered walk-forward sim ensemble (sim_v5/sim_v6/sim_v6_fix at opp 0.5) used by the
selective_under_alt study. Research only; projection_ready stays false."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from calibration import selective_edge as se
from calibration.selective_edge_freeze import PARAMS_FILE, ROOT, RUN, sha256, verify_hashes

WORK = Path(os.environ.get("SELECTIVE_EDGE_WORK", "/tmp/selective_edge_phase4"))
CANDIDATES = os.environ.get("SELECTIVE_CANDIDATES",
                            "/workspace/research/selective_under_alt_2026-11-12/candidates.csv")
LEGS = os.environ.get("SELECTIVE_LEGS",
                      "/workspace/nfl-database/backtests/confidence_check_2026-11-03/legs_with_probs.csv")
PBP = ROOT / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PBP_COLS = ["week", "game_id", "posteam", "rush_attempt", "rusher_player_id", "receiver_player_id", "qb_kneel",
            "pass_attempt", "rushing_yards", "receiving_yards", "complete_pass", "two_point_attempt", "season_type"]
PROP = ("rushyds", "recyds", "rec", "rushrec")


def build():
    C = pd.read_csv(CANDIDATES, low_memory=False)
    C = C[C.market.isin(PROP) & C.kind.isin(["under", "alt"]) & C.week.between(4, 9)].copy()
    L = pd.read_csv(LEGS, usecols=["week", "gsis", "market", "line", "book", "pre_kick_min", "actual"])
    L = L.drop_duplicates(["week", "gsis", "market", "line"])
    C = C.merge(L.rename(columns={"line": "main_line"}), on=["week", "gsis", "market", "main_line"], how="left")
    main = C.kind == "under"
    C["kind"] = np.where(main, "main", "alt")
    C["line"] = C.rung
    C["price_source"] = np.where(
        main, "legs_with_probs book=" + C.book.fillna("?") + " pre_kick_min=" + C.pre_kick_min.round(1).astype(str),
        "historical_nfl_odds_inventory_2026-11-07 best verified pre-kick alt price")
    C.loc[C.dec.isna() | (C.dec <= 1), "price_source"] = None
    C["defender_verified"] = False   # no historical main-defender source exists: receiving legs -> INSUFFICIENT
    C["source"] = np.where(C.week <= 7, "backtest_is", "backtest_oos")
    C["actual"] = np.nan             # settle from the study's pre-computed win/push (alts have no actual column)
    pbp = pd.read_parquet(PBP, columns=PBP_COLS)
    C = C.rename(columns={"carry_share": "carry_share_study", "n_prior": "n_prior_study", "n60": "n60_study"})
    C = se.attach_context(C.reset_index(drop=True), pbp)
    rb = C.market.isin(se.RUSH_MARKETS) & C.position.isin(se.RB_POSITIONS)
    mism = int((rb & ((C.carry_n_prior.fillna(0) != C.n_prior_study.fillna(0)) |
                      (C.carry_n60.fillna(0) != C.n60_study.fillna(0)))).sum())
    keep = ["week", "game_id", "player", "gsis", "position", "market", "side", "kind", "line", "main_line", "dec",
            "p_nv", "p_model", "defender_verified", "price_source", "book", "pre_kick_min", "actual", "win", "push",
            "source", "carry_n_prior", "carry_n60", "carry_share", "usual", "edge_study"]
    C = C.rename(columns={"edge": "edge_study"})[keep]
    WORK.mkdir(parents=True, exist_ok=True)
    C.to_csv(WORK / "legs_w4_9.csv", index=False)
    inputs = {"candidates.csv": sha256(CANDIDATES), "legs_with_probs.csv": sha256(LEGS),
              str(PBP.relative_to(ROOT)): sha256(PBP), "legs_w4_9.csv (built)": sha256(WORK / "legs_w4_9.csv")}
    (WORK / "inputs_sha256.json").write_text(json.dumps(inputs, indent=1))
    print(json.dumps(dict(rows=len(C), by=C.groupby(["source", "kind", "market"]).size().to_dict().__repr__(),
                          carry_gate_mismatch_vs_study=mism, inputs=inputs), indent=1))


def _legs():
    return pd.read_csv(WORK / "legs_w4_9.csv", low_memory=False)


def fit():
    L = _legs()
    p = se.fit(L[L.week.isin(se.TRAIN_WEEKS)].reset_index(drop=True), B=10000)
    p["inputs_sha256"] = json.loads((WORK / "inputs_sha256.json").read_text())
    (ROOT / PARAMS_FILE).write_text(json.dumps(p, indent=1, default=float) + "\n")
    print(json.dumps({k: p[k] for k in ("strong_markets", "alt_min_cushion")}),
          json.dumps(p["train_strong_under_by_market"], default=float)[:2000])


def evaluate():
    m = verify_hashes()                       # refuse before reading any Weeks 8-9 outcome
    if json.loads((WORK / "inputs_sha256.json").read_text()) != m.get("inputs_sha256"):
        raise SystemExit("box-local inputs differ from the freeze manifest's inputs_sha256")
    params = json.loads((ROOT / PARAMS_FILE).read_text())
    L = _legs()
    E = se.evaluate(L[L.week.isin(se.EVAL_WEEKS)].reset_index(drop=True), params)
    I = se.settle(se.classify(L[L.week.isin(se.TRAIN_WEEKS)].reset_index(drop=True), params))
    E.to_csv(WORK / "graded_w8_9.csv", index=False)
    out = []
    for setname, df in (("IS W4-7", I), ("OOS W8-9", E)):
        lab = df.groupby(["label", "market", "kind"]).size().rename("n_labeled").reset_index()
        t = se.table(df[df.label.isin(se.CANDIDATE_LABELS)], by=("label", "market", "side"))
        if len(t):
            out.append(t.assign(set=setname))
        lab.assign(set=setname).to_csv(RUN / f"label_counts_{setname.split()[0].lower()}.csv", index=False)
        df.groupby(["label", "reason"]).size().rename("n").reset_index().assign(set=setname).to_csv(
            RUN / f"reason_counts_{setname.split()[0].lower()}.csv", index=False)
    R = pd.concat(out, ignore_index=True)
    R.to_csv(RUN / "results_by_label_market.csv", index=False)
    # edge-tier flags (not cuts) within STRONG UNDER, OOS
    tiers = se.table(E[E.label == se.STRONG_UNDER], by=("edge_tier",))
    tiers.to_csv(RUN / "results_strong_under_by_edge_tier_oos.csv", index=False)
    # reconciliation with the 18-5 study row: gated rush-yds unders with study edge >= +5 pts (same rows, same prices)
    rec = E[(E.kind == "main") & (E.market == "rushyds") & (E.side == "Under") & E.label.isin(
        [se.STRONG_UNDER, se.STANDARD])]
    rec5 = rec[rec.edge_study >= 0.05 - 1e-12]
    gate_ok = E[(E.kind == "main") & (E.market == "rushyds") & ~E.reason.isin(
        ["do_not_play_rb_carry_lt_60", "carry_history_unknown"])]
    rows = [dict(view="prior study X=+5 (edge vs no-vig >= 0.05), gated", **se.summarize(rec5)),
            dict(view="Phase 4 STRONG UNDER rushyds (edge >= 0, tiers as flags)",
                 **se.summarize(E[(E.label == se.STRONG_UNDER) & (E.market == "rushyds")])),
            dict(view="all gated rush-yds main unders, no edge filter", **se.summarize(gate_ok))]
    pd.DataFrame(rows).to_csv(RUN / "reconcile_18_5.csv", index=False)
    pr = rec5.groupby(["week", "book"], dropna=False).size().rename("n").reset_index()
    pr.to_csv(RUN / "reconcile_18_5_pricing.csv", index=False)
    grad = {s: se.graduation(E, sources=s) for s in [("backtest_oos",)]}
    for s, g in grad.items():
        g.to_csv(RUN / "graduation_preview_backtest_oos.csv", index=False)
    pd.set_option("display.width", 250)
    c = ["set", "label", "market", "side", "n", "W", "L", "P", "hit", "be", "margin", "margin_lo", "margin_hi", "roi"]
    print(R[c].round(3).to_string(index=False))
    print(tiers.round(3).to_string(index=False))
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print(pr.to_string(index=False))
    print(grad[("backtest_oos",)].round(3).to_string(index=False))


if __name__ == "__main__":
    {"build": build, "fit": fit, "eval": evaluate}[sys.argv[1]]()
