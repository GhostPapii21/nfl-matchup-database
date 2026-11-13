"""NFL-75 Phase 2b metrics: research/runs/2026-11-13_opportunity_phase2b/backtest_raw.json vs the Phase 2 run.
    python3 -m calibration.opportunity_report_2b

Same games, same seed, same n, same scoring as calibration/opportunity_report.py (game-cluster bootstrap, 2,000
resamples, seed 75). Comparisons:
  A. main (Phase 2 run's name-locked recorder, engine without INT pooling) vs Phase 2b opportunity model
     (depth signal + INT pooling): the headline vs current main.
  B. Phase 2 opportunity model vs Phase 2b opportunity model: what Phase 2b adds.
  D. Phase 2 opportunity model vs Phase 2b WITHOUT INT pooling (noint/backtest_raw_noint.json: same params, engine
     without int_pool): the depth signal + grid changes alone. Without pooling the engine stream is identical to the
     Phase 2 run, so the name-locked lines must match it exactly (checked).
  C. QB interceptions (QBs with >= 10 actual attempts): main, Phase 2 opp, Phase 2b name-locked (INT pooling only),
     Phase 2b opp; Brier with a 95% CI on the difference vs main.
Weeks 4-9 only (backtest on already-seen weeks; the Phase 2b parameters are walk-forward). Research only."""
from __future__ import annotations
import json

import numpy as np

from calibration import opportunity_fit as F
from calibration import opportunity_report as R

RUN2 = F.ROOT / "research/runs/2026-11-13_opportunity_phase2"
RUN2B = F.ROOT / "research/runs/2026-11-13_opportunity_phase2b"


def _pair(r2, r2b, base_src, opp_src, rn=None):
    by2 = {g["game_id"]: g for g in r2["games"]}
    byn = {g["game_id"]: g for g in rn["games"]} if rn else {}
    games = []
    for g in r2b["games"]:
        a = by2[g["game_id"]]
        nn = byn.get(g["game_id"], {"opportunity": {}, "recon": {"opportunity_failures": 0}})
        src = {"main": a["name_locked"], "p2opp": a["opportunity"], "p2b_nl": g["name_locked"], "p2b": g["opportunity"],
               "p2b_noint": nn["opportunity"]}
        rec = {"main": a["recon"]["name_locked_failures"], "p2opp": a["recon"]["opportunity_failures"],
               "p2b_nl": g["recon"]["name_locked_failures"], "p2b": g["recon"]["opportunity_failures"],
               "p2b_noint": nn["recon"]["opportunity_failures"]}
        games.append({"game_id": g["game_id"], "week": g["week"], "home": g["home"], "away": g["away"],
                      "name_locked": src[base_src], "opportunity": src[opp_src],
                      "recon": {"name_locked_failures": rec[base_src], "opportunity_failures": rec[opp_src]}})
    if r2["n"] != r2b["n"] or r2["seed"] != r2b["seed"] or sorted(r2["weeks"]) != sorted(r2b["weeks"]):
        raise RuntimeError("Phase 2 and Phase 2b runs differ in n / seed / weeks")
    return {**r2b, "games": games, "actual": r2b["actual"]}


def int_table(r2, r2b, min_att=10, rn=None) -> dict:
    rng = np.random.default_rng(75)
    srcs = ("main", "p2opp", "p2b_nl", "p2b") + (("p2b_noint",) if rn else ())
    raws = {s: _pair(r2, r2b, "main", s, rn) for s in srcs}
    rows = {s: R.build_rows(raws[s]) for s in srcs}
    key = lambda r: (r["game"], r["team"], r["name"])
    base = {key(r): r for r in rows["main"]}
    q = [r for r in rows["main"] if r["grp"] == "QB" and r["act"].get("pass_att", 0) >= min_att]
    ks = [key(r) for r in q]
    gidx = np.array([k[0] for k in ks])
    y = np.array([float(base[k]["act"].get("int_thrown", 0) >= 1) for k in ks])
    lookup = {s: {key(r): r for r in rows[s]} for s in srcs}
    out = {"qb_games": len(q), "min_actual_attempts": min_att, "actual_rate": round(float(y.mean()), 4), "models": {}}
    pm = None
    for s in srcs:
        p = np.array([float(lookup[s].get(k, {}).get("opp", {}).get("int_thrown", {}).get("p_ge1", 0.0)) for k in ks])
        if s == "main":
            p = np.array([float(base[k]["base"].get("int_thrown", {}).get("p_ge1", 0.0)) for k in ks])
            pm = p
        v = {"b": (pm - y) ** 2, "o": (p - y) ** 2}
        z = p == 0
        out["models"][s] = {"p_zero_games": int(z.sum()), "p_zero_with_actual_int": int(y[z].sum()),
                            "mean_p": round(float(p.mean()), 4),
                            "brier": R._boot(gidx, v, lambda d: d["o"].mean(), rng),
                            "minus_main": R._boot(gidx, v, lambda d: (d["o"] - d["b"]).mean(), rng)}
        if s == "p2b":
            out["p2b_zero_games"] = [{"game": k[0], "team": k[1], "qb": k[2],
                                      "actual_att": int(base[k]["act"].get("pass_att", 0)),
                                      "opp_mean_att": round(float(lookup[s].get(k, {}).get("opp", {}).get("pass_att", {}).get("mean", 0.0)), 1)}
                                     for k, zz in zip(ks, z) if zz]
    return out


LAB = {"main": "main (name-locked, no INT pooling)", "p2opp": "Phase 2 opportunity (PR #38)",
       "p2b_nl": "Phase 2b name-locked + INT pooling", "p2b": "Phase 2b opportunity (depth + INT pooling)",
       "p2b_noint": "Phase 2b opportunity WITHOUT INT pooling (depth only)"}


def markdown(mA, mB, it, r2b, mD=None, nl_identical=None, rn=None) -> str:
    def body(m, raw, a_lab, b_lab):
        s = R.markdown(m, raw).split("## History-capped events")[0]
        s = s.split("\n", 2)[2]  # drop the Phase 2 title line
        return s.replace("ME main", f"ME {a_lab}").replace("MAE main", f"MAE {a_lab}").replace(
            "cov main", f"cov {a_lab}").replace("Brier main", f"Brier {a_lab}").replace("opp-main", f"opp-{a_lab}").replace(
            "ME opp", f"ME {b_lab}").replace("MAE opp", f"MAE {b_lab}").replace("cov opp", f"cov {b_lab}").replace(
            "Brier opp", f"Brier {b_lab}")
    ip = [g.get("int_pool", {}) for g in r2b["games"]]
    conv_int = sum(x.get("counts", {}).get("to_int", 0) for x in ip)
    conv_inc = sum(x.get("counts", {}).get("to_incomplete", 0) for x in ip)
    seen = sum(x.get("counts", {}).get("attempts_seen", 0) for x in ip)
    L = ["# Phase 2b: depth signal + opt-in INT pooling, walk-forward Weeks 4-9 (2026)", "",
         "Backtest on weeks already seen while the engine was built; the Phase 2b parameters (depth weights, M grid, "
         "INT pooling m and league rate) are walk-forward: fit on data before each eval week, frozen, then scored. "
         "Research only, not validated; projection_ready=false.", "",
         f"INT pooling over the 88 games: {seen} sampled pass attempts saw a draw, {conv_int} became interceptions, "
         f"{conv_inc} interceptions became incompletions (summed over trials).", "",
         "## A. main vs Phase 2b opportunity model", "", body(mA, r2b, "main", "2b"),
         "## B. Phase 2 opportunity model (PR #38) vs Phase 2b", "", body(mB, r2b, "p2", "2b"),
         *((["## D. Phase 2 opportunity model (PR #38) vs Phase 2b WITHOUT INT pooling (depth signal + grids only)", "",
              f"Same params as 2b, engine without int_pool, same games / n / seed. Name-locked lines identical to the "
              f"Phase 2 run: {nl_identical} (the engine stream is unchanged without pooling).", "",
              body(mD, rn or r2b, "p2", "2b-noint")]) if mD is not None else []),
         f"## C. QB interceptions (QB-games with >= {it['min_actual_attempts']} actual attempts: {it['qb_games']}; "
         f"actual INT rate {it['actual_rate']:.3f})", "",
         "| model | games with P(INT>=1)=0 | of those, actual INT | mean P(INT>=1) | Brier [95% CI] | minus main [95% CI] |",
         "|---|---|---|---|---|---|"]
    for s, v in it["models"].items():
        L.append(f"| {LAB[s]} | {v['p_zero_games']} | {v['p_zero_with_actual_int']} | {v['mean_p']:.3f} | "
                 f"{R.fmtp(v['brier'])} | {R.fmt(v['minus_main'])} |")
    L += ["", "Remaining Phase 2b zero-probability QB-games: QBs the model did not list as candidates (not all backups; "
          "some started, see actual attempts):", "",
          "| game | team | QB | 2b mean att | actual att |", "|---|---|---|---|---|"]
    L += [f"| {z['game']} | {z['team']} | {z['qb']} | {z['opp_mean_att']} | {z['actual_att']} |"
          for z in it.get("p2b_zero_games", [])]
    L.append("")
    return "\n".join(L)


def main():
    r2 = json.loads((RUN2 / "backtest_raw.json").read_text())
    r2b = json.loads((RUN2B / "backtest_raw.json").read_text())
    npath = RUN2B / "noint/backtest_raw_noint.json"
    rn = json.loads(npath.read_text()) if npath.exists() else None
    mA = R.metrics(_pair(r2, r2b, "main", "p2b"))
    mB = R.metrics(_pair(r2, r2b, "p2opp", "p2b"))
    mD, same = None, None
    if rn is not None:
        if (rn["n"], rn["seed"], sorted(rn["weeks"])) != (r2["n"], r2["seed"], sorted(r2["weeks"])):
            raise RuntimeError("no-INT-pool run differs from Phase 2 in n / seed / weeks")
        by2 = {g["game_id"]: g["name_locked"] for g in r2["games"]}
        same = all(by2[g["game_id"]] == g["name_locked"] for g in rn["games"]) and len(rn["games"]) == len(r2["games"])
        mD = R.metrics(_pair(r2, r2b, "p2opp", "p2b_noint", rn))
    it = int_table(r2, r2b, rn=rn)
    md = markdown(mA, mB, it, r2b, mD, same, rn)
    for m in (mA, mB, mD):
        if m is not None:
            m.pop("int_zero", None)  # superseded by C_int (the Phase 2 reason labels assume an unpooled engine)
    (RUN2B / "metrics.json").write_text(json.dumps({"A_main_vs_2b": mA, "B_phase2_vs_2b": mB,
                                                    "D_phase2_vs_2b_noint": mD, "noint_name_locked_identical_to_phase2": same,
                                                    "C_int": it}, indent=1) + "\n")
    (RUN2B / "metrics.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
