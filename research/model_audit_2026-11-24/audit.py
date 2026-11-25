"""Five audits of the prop model (owner, Nov 24, 2026, from a thread of model-audit prompts). Read-only: nothing in the
model, the board or any saved record is changed. Every prediction used was made from earlier weeks only.

  1. Edge auditor        the opportunity simulation (with the board's calibration layer) vs FanDuel alt-ladder prices
                         saved at T-90 for 2026 Weeks 8-9 (data/odds_history/alt_ladders_wk8_9): 20 biggest gaps, their
                         inputs, data checks, and whether bigger gaps did better.
  2. Feature eliminator  switch off one part of the simulation at a time and re-run 2026 Weeks 5-11 (2026 was never
                         used to fit anything in the simulation); and drop one group of the 80-yard star model's inputs,
                         fitting on earlier seasons only and testing on each later season (2024, 2025, 2026).
  3. Confidence checker  the simulation's favoured side grouped 50-60 / 60-70 / 70-80 / 80-90 / 90+, vs a baseline.
  5. Change tester       one proposed change (rising role, now in the side-by-side run), fit on earlier seasons only,
                         per season with a bootstrap interval.
  (4. the backtest-process review is written by hand in REPORT.md, with file references.)

    python3 research/model_audit_2026-11-24/audit.py          # writes results.json (about 4 minutes)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from dashboard import backtest_opportunity as B  # noqa: E402
from dashboard import opportunity as O  # noqa: E402

B.NS = 3000
RUNGS = ROOT / "data" / "odds_history" / "alt_ladders_wk8_9" / "backtest" / "graded_rungs.csv"
HOLD = {"rec": 0.06443, "rush": 0.06453}     # FanDuel main-line average hold (research/edge_2026), to de-vig one-sided rungs
STAT = {"rec": "receiving_yards", "rush": "rushing_yards"}


# ------------------------------------------------------------------ simulation runs that keep each player's draws
def run(season=2026, prev=2025, patch=None):
    saved, keep = [], {}
    orig = {"simulate_receiver": O.simulate_receiver, "simulate_rusher": O.simulate_rusher}

    def rec(**kw):
        out = orig["simulate_receiver"](**kw)
        saved.append((kw, out[2], out[1]))
        return out

    def rush(**kw):
        out = orig["simulate_rusher"](**kw)
        saved.append((kw, out[1], out[0]))
        return out
    O.simulate_receiver, O.simulate_rusher = rec, rush
    for k, v in (patch or {}).items():
        keep[k] = getattr(O, k)
        setattr(O, k, v)
    try:
        rows = B.run_season(season, prev)
    finally:
        O.simulate_receiver, O.simulate_rusher = orig["simulate_receiver"], orig["simulate_rusher"]
        for k, v in keep.items():
            setattr(O, k, v)
    assert len(rows) == len(saved)
    for r, (kw, yd, cnt) in zip(rows, saved):
        r["_yd"], r["_cnt"] = yd, cnt
        r["catch_rate"] = kw.get("catch_rate")
        r["ypr"] = kw.get("ypr")
        r["ypc"] = kw.get("ypc")
    return rows


def p_cal(yd, kind, t):
    return O.calibrate(float((yd >= t).mean()), STAT[kind], t)


# ------------------------------------------------------------------ 1. edge auditor
def edge_audit(rows):
    g = pd.read_csv(RUNGS)
    idx = {(r["week"], r["player"], r["kind"]): r for r in rows if r["week"] in (8, 9)}
    out = []
    for x in g.itertuples():
        r = idx.get((x.week, x.gsis_id, x.market))
        if r is None:
            continue
        pm = p_cal(r["_yd"], x.market, x.rung)
        pf = x.be / (1 + HOLD[x.market])
        out.append({"game_id": x.game_id, "week": x.week, "player": x.player, "team": x.team, "pos": x.pos, "market": x.market,
                    "rung": x.rung, "price": x.price, "p_model": pm, "p_market": pf, "edge": pm - pf, "actual": x.actual, "win": x.win,
                    "profit": x.profit, "trail_mean": x.trail_mean, "games_prior": r["games_prior"], "sim_mean": r["pred_yards_mean"],
                    "exp_volume": r.get("exp_targets") or r.get("exp_carries"), "share": r["share"], "catch_rate": r["catch_rate"],
                    "ypr": r["ypr"], "ypc": r["ypc"], "pg": f"{x.game_id}|{x.gsis_id}|{x.market}"})
    d = pd.DataFrame(out)
    res = {"rungs_matched": int(len(d)), "rungs_total": int(len(g)), "player_games": int(d.pg.nunique()),
           "unmatched_note": "rungs for players the simulation does not project (under 8 earlier targets / 15 carries, or not active)"}
    res["brier"] = {"model": round(float(((d.p_model - d.win) ** 2).mean()), 4), "market_devig": round(float(((d.p_market - d.win) ** 2).mean()), 4),
                    "blend": round(float(((((d.p_model + d.p_market) / 2) - d.win) ** 2).mean()), 4)}
    top = d.reindex(d.edge.abs().sort_values(ascending=False).index).drop_duplicates("pg").head(20)
    res["top20"] = [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k != "pg"} for r in top.to_dict("records")]
    # bigger edges, better results? one-sided: only overs can be bet at FanDuel
    bins = [-1, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 1]
    d["band"] = pd.cut(d.edge, bins)
    rng = np.random.default_rng(7)
    tab = []
    for b, x in d.groupby("band", observed=True):
        pgs = x.pg.unique()
        # cluster bootstrap of ROI by player-game
        grp = x.groupby("pg").profit.agg(["sum", "size"])
        arr = grp.values
        bs = []
        for _ in range(2000):
            i = rng.integers(0, len(arr), len(arr))
            bs.append(arr[i, 0].sum() / arr[i, 1].sum())
        tab.append({"edge_band": str(b), "rungs": int(len(x)), "player_games": int(len(pgs)), "model": round(float(x.p_model.mean()), 3),
                    "market": round(float(x.p_market.mean()), 3), "hit": round(float(x.win.mean()), 3),
                    "over_roi": round(float(x.profit.mean()), 3), "roi_95": [round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)]})
    res["by_edge"] = tab
    # checks
    res["checks"] = {
        "few_earlier_games(<=4)": int((d.drop_duplicates("pg").games_prior <= 4).sum()),
        "extreme_prices(<= -500 or >= +500)": int(((d.price <= -500) | (d.price >= 500)).sum()),
        "edges_over_15pts": int((d.edge.abs() > 0.15).sum()),
        "edges_over_15pts_on_rungs_below_half_or_above_double_trailing_mean": int(((d.edge.abs() > 0.15) & ((d.rung < 0.5 * d.trail_mean) | (d.rung > 2 * d.trail_mean))).sum()),
        "model_minus_market_mean": round(float(d.edge.mean()), 3),
    }
    return res, d


# ------------------------------------------------------------------ 2. feature eliminator (simulation parts)
THR = {"rec": [("y", 40), ("y", 60), ("y", 80), ("r", 4), ("r", 6)], "rush": [("y", 50), ("y", 70), ("c", 12), ("c", 15)]}


def score_rows(rows, rungs=None, calibrated=True):
    ps, ys = [], []
    for r in rows:
        for kind_t, t in THR[r["kind"]]:
            arr = r["_yd"] if kind_t == "y" else r["_cnt"]
            p = float((arr >= t).mean())
            if calibrated:
                st = STAT[r["kind"]] if kind_t == "y" else ("receptions" if kind_t == "r" else "carries")
                p = O.calibrate(p, st, t)
            a = r[f"a_{kind_t}{t}"]
            ps.append(p); ys.append(a)
    p, y = np.clip(np.array(ps), 1e-4, 1 - 1e-4), np.array(ys)
    bins = np.minimum((p * 10).astype(int), 9)
    ece = sum(abs(p[bins == b].mean() - y[bins == b].mean()) * (bins == b).sum() for b in set(bins)) / len(p)
    out = {"n": int(len(p)), "brier": round(float(((p - y) ** 2).mean()), 5), "logloss": round(float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()), 5),
           "calibration_gap": round(float(ece), 4), "yards_mae": round(float(np.mean([abs(r["pred_yards_mean"] - r["actual_yards"]) for r in rows])), 2)}
    if rungs is not None:
        idx = {(r["week"], r["player"], r["kind"]): r for r in rows if r["week"] in (8, 9)}
        e = []
        for x in rungs.itertuples():
            r = idx.get((x.week, x.gsis_id, x.market))
            if r is not None:
                pm = p_cal(r["_yd"], x.market, x.rung) if calibrated else float((r["_yd"] >= x.rung).mean())
                e.append((pm - x.be / (1 + HOLD[x.market]), x.profit, pm, x.win))
        e = np.array(e)
        sel = e[e[:, 0] >= 0.05]
        out["fanduel_overs_model_edge_5plus"] = {"bets": int(len(sel)), "roi": round(float(sel[:, 1].mean()), 3) if len(sel) else None}
        out["fanduel_rungs_brier"] = round(float(((e[:, 2] - e[:, 3]) ** 2).mean()), 4)
    return out


def ablations():
    rungs = pd.read_csv(RUNGS)
    variants = {
        "full simulation (as the board runs it)": ({}, True),
        "without the defense adjustment": ({"def_factor": lambda a, b: 1.0}, True),
        "without the game-script adjustment": ({"script_multipliers": lambda m: (1.0, 1.0)}, True),
        "without the volume correction": ({"VOLUME_CAL": {"rec": (0.0, 1.0), "rush": (0.0, 1.0)}}, True),
        "without shrinking to league rates": ({"PRIOR_TARGETS": 1e-9, "PRIOR_CATCHES": 1e-9, "PRIOR_CARRIES": 1e-9}, True),
        "without role uncertainty": ({"SHARE_CV": {"rec": 0.0, "rush": 0.0}}, True),
        "without the output calibration layer": ({}, False),
    }
    res, base_rows = {}, None
    for name, (patch, cal) in variants.items():
        rows = base_rows if (not patch and base_rows is not None) else run(2026, 2025, patch)
        if not patch:
            base_rows = rows
        res[name] = score_rows(rows, rungs, calibrated=cal)
        print(name, res[name], flush=True)
    return res, base_rows


# ------------------------------------------------------------------ 2b. star-model ablation, chronological
def star_ablation():
    sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
    import fit as F
    r = F.receivers()
    groups = {"volume (targets)": ["l_tgt"], "his production (yards a game)": ["l_yds"], "game environment (team total, team pass volume)": ["implied", "team_pass"],
              "defense (big plays allowed, 80+ games allowed)": ["l_ex", "g80_pg"]}
    full = ["l_tgt", "l_yds", "implied", "team_pass", "l_ex", "g80_pg"]
    out = {}
    for yr in (2024, 2025, 2026):
        tr, te = r[r.season < yr], r[r.season == yr]
        row = {}
        for name, drop in [("all inputs", [])] + list(groups.items()):
            cols = [c for c in full if c not in drop]
            m = sm.GLM(tr.hit80, sm.add_constant(tr[cols]), family=sm.families.Binomial()).fit()
            p = m.predict(sm.add_constant(te[cols], has_constant="add")).clip(1e-4, 1 - 1e-4).values
            y = te.hit80.values
            st = p >= 0.30
            row[name] = {"logloss": round(float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()), 5), "brier": round(float(((p - y) ** 2).mean()), 5),
                         "stars": int(st.sum()), "stars_hit": round(float(y[st].mean()), 3) if st.any() else None}
        out[str(yr)] = {"fit_on": f"2022-{yr - 1}", "rows": int(len(te)), "results": row}
    return out


# ------------------------------------------------------------------ 3. confidence checker
def confidence(rows):
    recs = []
    for r in rows:
        for kind_t, t in THR[r["kind"]]:
            arr = r["_yd"] if kind_t == "y" else r["_cnt"]
            st = STAT[r["kind"]] if kind_t == "y" else ("receptions" if kind_t == "r" else "carries")
            p = O.calibrate(float((arr >= t).mean()), st, t)
            recs.append({"p": p, "a": r[f"a_{kind_t}{t}"], "b": r[f"b_{kind_t}{t}"], "market": f"{st} {t}+"})
    d = pd.DataFrame(recs)
    d["conf"] = np.where(d.p >= 0.5, d.p, 1 - d.p)
    d["right"] = np.where(d.p >= 0.5, d.a, 1 - d.a)
    d["band"] = pd.cut(d.conf, [0.5, 0.6, 0.7, 0.8, 0.9, 1.0001], right=False, labels=["50-60%", "60-70%", "70-80%", "80-90%", "90%+"])
    tab = []
    for b, x in d.groupby("band", observed=False):
        n = len(x)
        if not n:
            tab.append({"band": str(b), "n": 0}); continue
        pr, ac = float(x.conf.mean()), float(x.right.mean())
        se = (pr * (1 - pr) / n) ** 0.5
        flag = "small sample" if n < 30 else ("overconfident" if ac < pr - 2 * se else ("underconfident" if ac > pr + 2 * se else "ok"))
        tab.append({"band": str(b), "n": n, "said": round(pr, 3), "happened": round(ac, 3), "flag": flag})
    # base rates for a naive baseline: each market's hit rate in 2024-25 backtest rows
    old = pd.read_parquet(ROOT / "pregame" / ".cache" / "opportunity_backtest_rows.parquet") if (ROOT / "pregame" / ".cache" / "opportunity_backtest_rows.parquet").exists() else None
    base = {}
    if old is not None and "season" in old:
        o = old[old.season < 2026]
        for kind, ts in THR.items():
            for k, t in ts:
                c = f"a_{k}{t}"
                if c in o:
                    st = STAT[kind] if k == "y" else ("receptions" if k == "r" else "carries")
                    base[f"{st} {t}+"] = float(o[o.kind == kind][c].mean())
    d["base"] = d.market.map(base)
    brier = {"model": round(float(((d.p - d.a) ** 2).mean()), 5), "own_history_baseline": round(float(((d.b - d.a) ** 2).mean()), 5)}
    if d.base.notna().all():
        brier["league_base_rate_baseline"] = round(float(((d.base - d.a) ** 2).mean()), 5)
    per = []
    for mk, x in d.groupby("market"):
        per.append({"market": mk, "n": int(len(x)), "model": round(float(((x.p - x.a) ** 2).mean()), 4), "own_history": round(float(((x.b - x.a) ** 2).mean()), 4),
                    "said": round(float(x.p.mean()), 3), "happened": round(float(x.a.mean()), 3)})
    return {"predictions": int(len(d)), "bands": tab, "brier": brier, "by_market": per}


# ------------------------------------------------------------------ 5. change tester: rising role
def change_test():
    sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
    sys.path.insert(0, str(ROOT / "research" / "star_review_2026-11-23"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("shadow_study", ROOT / "research" / "shadow_2026-11-23" / "study.py")
    S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
    import fit as F
    r = S.add_streak_role(F.receivers()).dropna(subset=["last1"])
    full = S.RX
    out, rng = {}, np.random.default_rng(11)
    for yr in (2024, 2025, 2026):
        tr, te = r[r.season < yr], r[r.season == yr]
        res = {}
        for name, cols in (("current", full), ("with rising role", full + ["last1"])):
            m = sm.GLM(tr.hit80, sm.add_constant(tr[cols]), family=sm.families.Binomial()).fit()
            res[name] = m.predict(sm.add_constant(te[cols], has_constant="add")).clip(1e-4, 1 - 1e-4).values
        y = te.hit80.values
        ll = lambda p: -(y * np.log(p) + (1 - y) * np.log(1 - p))
        diff = ll(res["with rising role"]) - ll(res["current"])
        bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
        subs = {}
        for lab, mask in (("WR", te.pos.values == "WR"), ("TE", te.pos.values == "TE"), ("starred (30%+)", res["current"] >= 0.30),
                          ("role up last game", te.last1.values > 0.2), ("role down last game", te.last1.values < -0.2)):
            if mask.sum() >= 30:
                subs[lab] = {"n": int(mask.sum()), "logloss_change": round(float(diff[mask].mean()), 5)}
        out[str(yr)] = {"fit_on": f"2022-{yr - 1}", "rows": int(len(te)), "logloss_change": round(float(diff.mean()), 5),
                        "ci95": [round(float(np.percentile(bs, 2.5)), 5), round(float(np.percentile(bs, 97.5)), 5)],
                        "brier": [round(float(((res["current"] - y) ** 2).mean()), 5), round(float(((res["with rising role"] - y) ** 2).mean()), 5)],
                        "subgroups": subs}
    return out


def main():
    res = {}
    abl, rows = ablations()
    res["2_feature_eliminator_simulation_2026"] = abl
    e, _ = edge_audit(rows)
    res["1_edge_auditor"] = e
    res["2b_feature_eliminator_star_model"] = star_ablation()
    res["3_confidence_checker_2026"] = confidence(rows)
    res["5_change_tester_rising_role"] = change_test()
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "1_edge_auditor"}, indent=1, default=str))
    print(json.dumps({k: v for k, v in e.items() if k != "top20"}, indent=1, default=str))


if __name__ == "__main__":
    main()
