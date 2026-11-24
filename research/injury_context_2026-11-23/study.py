"""Injury context for the 80-yard stars (asked after Week 11, 2026-11-23).

1. Defense missing starters: does a defense without its starting corners/safeties (for WRs) or linebackers too (for TEs
   and backs) give up more 80-yard games than the star model expects? A starter = played 70%+ of defensive snaps in his
   team's earlier games that season (3+ games) and played one of the last two; "missing" = no defensive snaps this game.
2. The player himself: first game back after missing 1-2 or 3+ games (no offensive snaps), listed Questionable that week,
   or back from a concussion listing in the previous three weeks' reports.

Base: the board's star models (fit 2022-24). Snap counts 2024-26, injury reports 2025-26. Defense terms: one weight fit on
2024, held out on 2025-26 (log loss, Brier). Player flags: on 2025-26 (never seen by the base), hit rate vs the model's
prediction with a 95% interval -- does the model over-rate players in that spot?

    python3 research/injury_context_2026-11-23/study.py --data DIR     # DIR as for research/game_types_2026-11-16/test_rb.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C, H = ROOT / "pregame" / ".cache", ROOT / "data" / "historical" / "nflverse"
sys.path.insert(0, str(ROOT / "research" / "star_review_2026-11-23"))
sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
sys.path.insert(0, str(ROOT / "research" / "game_types_2026-11-16"))
import study as SR  # noqa: E402

DB = {"CB", "S", "FS", "SS", "DB"}
LB = {"LB", "ILB", "OLB", "MLB"}


def snaps():
    fr = [pd.read_parquet(H / "snap_counts_2024.parquet"), pd.read_parquet(H / "snaps_2025.parquet"), pd.read_parquet(C / "snap_counts_2026.parquet")]
    s = pd.concat(fr)
    s = s[s.game_type == "REG"]
    ids = pd.concat([pd.read_parquet(C / f"roster_weekly_{y}.parquet", columns=["pfr_id", "gsis_id"]) for y in (2024, 2025, 2026)]).dropna().drop_duplicates("pfr_id")
    return s.merge(ids, left_on="pfr_player_id", right_on="pfr_id", how="left")


def defense_missing(s):
    d = s[s.position.isin(DB | LB)]
    out = []
    for (yr, tm), g in s.groupby(["season", "team"]):
        weeks = sorted(g.week.unique())
        dd = d[(d.season == yr) & (d.team == tm)]
        for i, w in enumerate(weeks):
            if i < 3:
                continue
            prior = dd[dd.week < w]
            av = prior.groupby(["pfr_player_id", "position"]).agg(pct=("defense_pct", "mean"), n=("week", "nunique"), last=("week", "max")).reset_index()
            starters = av[(av.pct >= 0.70) & (av.n >= 3) & (av.last >= weeks[i - 2])]
            here = set(dd[(dd.week == w) & (dd.defense_snaps > 0)].pfr_player_id)
            miss = starters[~starters.pfr_player_id.isin(here)]
            out.append({"season": yr, "week": w, "opp": tm, "miss_db": int(miss.position.isin(DB).sum()), "miss_lb": int(miss.position.isin(LB).sum())})
    return pd.DataFrame(out)


def player_flags(s):
    """missed-games streak before each game the player played, per gsis id."""
    o = s[s.offense_snaps > 0][["season", "week", "team", "gsis_id"]].dropna()
    team_weeks = s.groupby(["season", "team"]).week.apply(lambda x: sorted(set(x))).to_dict()
    rows = []
    for (yr, pid), g in o.groupby(["season", "gsis_id"]):
        played = sorted(set(g.week))
        tm = g.team.iloc[-1]
        tw = team_weeks.get((yr, tm), [])
        for w in played[1:]:
            before = [x for x in tw if x < w]
            streak = 0
            for x in reversed(before):
                if x in played:
                    break
                streak += 1
            rows.append({"season": yr, "week": w, "player": pid, "missed_before": streak})
    f = pd.DataFrame(rows)
    inj = pd.concat([pd.read_parquet(H / "injuries_2025.parquet"), pd.read_parquet(C / "injuries_2026.parquet")])
    inj = inj[inj.game_type == "REG"] if "game_type" in inj else inj
    q = inj[inj.report_status == "Questionable"][["season", "week", "gsis_id"]].drop_duplicates().assign(questionable=1)
    con = inj[inj.report_primary_injury.fillna("").str.contains("Concussion")][["season", "week", "gsis_id"]].drop_duplicates()
    f = f.merge(q.rename(columns={"gsis_id": "player"}), on=["season", "week", "player"], how="left").fillna({"questionable": 0})
    cset = set(map(tuple, con[["season", "week", "gsis_id"]].to_numpy()))
    f["back_concussion"] = [int(any((s_, w - k, p) in cset for k in (1, 2, 3))) for s_, w, p in zip(f.season, f.week, f.player)]
    return f


def check(d, flag, label):
    x = d[d[flag] > 0]
    if len(x) < 15:
        return {"label": label, "games": int(len(x)), "note": "too few"}
    se = float(np.sqrt(x.hit80.mean() * (1 - x.hit80.mean()) / len(x)))
    st = x[x.p >= 0.30]
    return {"label": label, "games": int(len(x)), "predicted": round(float(x.p.mean()), 3), "hit80": round(float(x.hit80.mean()), 3),
            "hit80_ci95": [round(float(x.hit80.mean() - 1.96 * se), 3), round(float(x.hit80.mean() + 1.96 * se), 3)],
            "ratio": round(float(x.hit80.mean() / x.p.mean()), 2),
            "starred": {"n": int(len(st)), "predicted": round(float(st.p.mean()), 3) if len(st) else None, "hit80": round(float(st.hit80.mean()), 3) if len(st) else None}}


def with_base(d, X):
    tr = d[d.season <= 2024]
    m = sm.GLM(tr.hit80, sm.add_constant(tr[X].astype(float)), family=sm.families.Binomial()).fit()
    d = d.copy()
    d["z"] = m.predict(sm.add_constant(d[X].astype(float), has_constant="add"), which="linear") if hasattr(m, "predict") else None
    d["p"] = 1 / (1 + np.exp(-d.z))
    return d


def def_term(d, col):
    tr, te = d[d.season == 2024], d[d.season >= 2025]
    m = sm.GLM(tr.hit80, sm.add_constant(tr[[col]].astype(float)), family=sm.families.Binomial(), offset=tr.z).fit()
    p0 = te.p.clip(1e-4, 1 - 1e-4)
    p1 = (1 / (1 + np.exp(-(te.z + m.params["const"] + m.params[col] * te[col])))).clip(1e-4, 1 - 1e-4)
    ll = lambda p: round(float(-(te.hit80 * np.log(p) + (1 - te.hit80) * np.log(1 - p)).mean()), 5)
    br = lambda p: round(float(((p - te.hit80) ** 2).mean()), 5)
    g = te.groupby(te[col].clip(upper=2))
    return {"coef_per_missing": round(float(m.params[col]), 4), "z": round(float(m.params[col] / m.bse[col]), 2),
            "heldout_logloss": [ll(p0), ll(p1)], "heldout_brier": [br(p0), br(p1)],
            "by_missing_2025_26": [{"missing": int(k), "games": int(len(x)), "predicted": round(float(x.p.mean()), 3), "hit80": round(float(x.hit80.mean()), 3)} for k, x in g]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    import fit as F
    import test_rb as T
    s = snaps()
    dm, pf = defense_missing(s), player_flags(s)
    res = {}
    r = with_base(F.receivers(), SR.RX)
    r = r[r.season >= 2024].merge(dm, on=["season", "week", "opp"], how="left").fillna({"miss_db": 0, "miss_lb": 0})
    r["miss_cover"] = np.where(r.pos == "TE", r.miss_db + r.miss_lb, r.miss_db)
    r = r.merge(pf, on=["season", "week", "player"], how="left").fillna({"missed_before": 0, "questionable": 0, "back_concussion": 0})
    r["back_1_2"] = r.missed_before.between(1, 2).astype(int)
    r["back_3plus"] = (r.missed_before >= 3).astype(int)
    res["receivers_defense_missing_coverage_starters"] = def_term(r, "miss_cover")
    h = r[r.season >= 2025]
    res["receivers_player_flags_2025_26"] = [check(h, "back_1_2", "first game back after missing 1-2 games"), check(h, "back_3plus", "first game back after missing 3+ games"),
                                             check(h, "questionable", "listed Questionable that week"), check(h, "back_concussion", "concussion listing in the previous 3 weeks")]
    D = Path(a.data)
    b = pd.concat([T.season(y, D) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied"]).reset_index(drop=True)
    b["l_car"], b["l_ypc"], b["l_d"] = np.log(0.6 * b.car_pg + 0.4 * b.car_l3), np.log(b.ypc), np.log(b.d_yds_pg)
    b["hit80"] = (b.y_yds >= 80).astype(int)
    mates = b.groupby(["season", "week", "team"]).car_pg.agg(list).rename("cars").reset_index()
    b = b.merge(mates, on=["season", "week", "team"])
    b["mate_car"] = [max([c for c in cs if c != me] or [0]) if cs.count(me) == 1 else max(cs) for cs, me in zip(b.cars, b.car_pg)]
    b = with_base(b, SR.BX + ["mate_car"])
    b = b[b.season >= 2024].merge(dm, on=["season", "week", "opp"], how="left").fillna({"miss_db": 0, "miss_lb": 0})
    b["miss_front"] = b.miss_lb + b.miss_db
    b = b.merge(pf, on=["season", "week", "player"], how="left").fillna({"missed_before": 0, "questionable": 0, "back_concussion": 0})
    b["back_1_2"] = b.missed_before.between(1, 2).astype(int)
    b["back_3plus"] = (b.missed_before >= 3).astype(int)
    res["backs_defense_missing_lb_db_starters"] = def_term(b, "miss_front")
    hb = b[b.season >= 2025]
    res["backs_player_flags_2025_26"] = [check(hb, "back_1_2", "first game back after missing 1-2 games"), check(hb, "back_3plus", "first game back after missing 3+ games"),
                                         check(hb, "questionable", "listed Questionable that week"), check(hb, "back_concussion", "concussion listing in the previous 3 weeks")]
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
