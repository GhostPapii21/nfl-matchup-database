"""NFL-49 task B: why is the sim total low? Compare simulated per-team-game accounting with the SAME teams'
actual W1..(week-1) per-game rates from the nflverse PBP the sim samples from.

    python3 -m calibration.diagnose_total --week 9 --n 400            # every week-9 game, h2h off
    python3 -m calibration.diagnose_total --games 2026_10_WAS_NYG --n 1000

Instrumentation is diagnostic-only: _apply_snap is wrapped IN MEMORY to tag each snap with the offense, field
position and play type; the engine's logic is not changed. n <= 20,000. Output: calibration/outputs/diag_total_*.json
Research only, not validated.
"""
from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from calibration.common import (PBP, PBP_PULLED_ET, MAX_N, LABEL, ROOT, engine_path, engine_version, make_cfg, sha256)

DRIVE_END = {"kickoff", "punt", "turnover", "turnover_on_downs", "field_goal", "touchdown", "def_return",
             "def_return_td", "safety", "halftime", "fg_sparse_miss_default", "end_q1", "end_q3", "ot_start"}


DEPTH = [(20, "le20"), (35, "21_35"), (50, "36_50"), (100, "gt50")]
LAB = {"Touchdown": "td", "Field goal": "fga", "Missed field goal": "fga", "Punt": "punt", "Turnover": "turnover",
       "Opp touchdown": "turnover", "Turnover on downs": "downs", "End of half": "end_period", "Safety": "safety"}


def depth_bucket(y) -> str:
    for hi, name in DEPTH:
        if y <= hi:
            return name
    return "gt50"


def actual_depth_counts(pbp, teams, weeks) -> dict:
    x = pbp[pbp["week"].isin(weeks) & pbp["posteam"].isin(teams) & pbp["play_type"].isin(["pass", "run"]) & pbp["down"].notna()]
    g = x.groupby(["game_id", "drive"]).agg(miny=("yardline_100", "min"), res=("fixed_drive_result", "first"))
    c = Counter((depth_bucket(r.miny), LAB.get(r.res, "other")) for r in g.itertuples())
    return {f"{k[0]}|{k[1]}": v for k, v in c.items()}


def depth_table(counts: dict) -> dict:
    tot = sum(counts.values()) or 1
    out = {}
    for _, b in DEPTH:
        n = sum(v for k, v in counts.items() if k.startswith(b + "|"))
        out[b] = {"share_of_drives": round(n / tot, 4),
                  "td_rate": round(counts.get(f"{b}|td", 0) / n, 4) if n else None,
                  "fga_rate": round(counts.get(f"{b}|fga", 0) / n, 4) if n else None,
                  "punt_rate": round(counts.get(f"{b}|punt", 0) / n, 4) if n else None}
    return out


def actual_team_rates(pbp: pd.DataFrame, teams, weeks) -> dict:
    d = pbp[(pbp["week"].isin(weeks)) & (pbp["posteam"].isin(teams))]
    out = {}
    for t in teams:
        x = d[d["posteam"] == t]
        g = x["game_id"].nunique()
        if not g:
            continue
        snaps = x[x["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"]) & x["down"].notna()]
        dr = x[x["drive"].notna()].drop_duplicates(["game_id", "drive"])
        dr = dr[dr["fixed_drive_result"].notna()]
        res = dr["fixed_drive_result"].value_counts()
        rz = dr[dr["drive_inside20"] == 1]
        gx = pbp[pbp["game_id"].isin(x["game_id"].unique())].drop_duplicates("game_id")
        pts = np.where(gx["home_team"] == t, gx["home_score"], gx["away_score"]).astype(float)
        out[t] = {"games": int(g), "points_pg": float(pts.mean()),
                  "snaps_pg": len(snaps) / g, "no_play_rows_pg": int((x["play_type"] == "no_play").sum()) / g,
                  "kneels_pg": int((x["play_type"] == "qb_kneel").sum()) / g,
                  "yards_per_snap": float(snaps["yards_gained"].mean()),
                  "drives_pg": len(dr) / g,
                  "td_per_drive": float(res.get("Touchdown", 0)) / len(dr),
                  "fga_per_drive": float(res.get("Field goal", 0) + res.get("Missed field goal", 0)) / len(dr),
                  "punt_per_drive": float(res.get("Punt", 0)) / len(dr),
                  "turnover_per_drive": float(res.get("Turnover", 0) + res.get("Opp touchdown", 0)) / len(dr),
                  "downs_per_drive": float(res.get("Turnover on downs", 0)) / len(dr),
                  "end_half_per_drive": float(res.get("End of half", 0)) / len(dr),
                  "rz_trips_pg": len(rz) / g,
                  "rz_td_rate": float((rz["fixed_drive_result"] == "Touchdown").mean()) if len(rz) else None,
                  "points_per_drive": float(pts.sum()) / len(dr)}
    return out


def sim_team_rates(cfg: dict, n: int, seed: int) -> dict:
    engine_path()
    import simulate
    from pbp_filter import load_team_history
    orig = simulate._apply_snap

    def tagged(rng, catalog, st, allow_pool):
        st.events.append({"type": "diag_snap", "team": st.possession, "yl": st.yardline_100})
        orig(rng, catalog, st, allow_pool)
    simulate._apply_snap = tagged
    try:
        h = load_team_history(str(PBP), teams=cfg["history"]["teams"], season=cfg["history"]["season"],
                              weeks=(cfg["history"]["weeks_inclusive"][0], cfg["history"]["weeks_inclusive"][-1]))
        cat, prov = simulate.build_catalog(h["df"], cfg, games_df=h.get("games_df"))
        simulate.attach_semantics(cat, cfg, str(PBP))
        rng = np.random.default_rng(seed)
        agg = {t: Counter() for t in (cfg["game"]["home"], cfg["game"]["away"])}
        totals, maxsteps, clocks = [], 0, []
        depth = Counter()
        miny = 100
        for _ in range(n):
            st = simulate.simulate_one(h["df"], cat, cfg, rng)
            totals.append(st.score_home + st.score_away)
            maxsteps += any(e.get("type") == "final_max_steps" for e in st.events)
            cur, rz, drive_open = None, False, False
            ev = st.events
            for i, e in enumerate(ev):
                ty = e.get("type")
                if ty == "diag_snap":
                    if not drive_open or e["team"] != cur:
                        if drive_open and cur in agg:
                            agg[cur]["drive_end_unlabelled"] += 1
                        cur, drive_open, rz = e["team"], True, False
                        agg[cur]["drives"] += 1
                        miny = 100
                    miny = min(miny, e["yl"])
                    if e["yl"] <= 20 and not rz:
                        rz = True; agg[cur]["rz_trips"] += 1
                    nxt = ev[i + 1] if i + 1 < len(ev) else {}
                    if nxt.get("type") == "snap":
                        agg[cur]["snaps"] += 1
                        agg[cur]["yards"] += nxt.get("yards", 0)
                        agg[cur][f"pt_{nxt.get('play_type')}"] += 1
                elif drive_open and ty in DRIVE_END:
                    lab = {"touchdown": "td", "punt": "punt", "turnover": "turnover", "turnover_on_downs": "downs",
                           "def_return": None, "def_return_td": None, "safety": "safety", "kickoff": None,
                           "fg_sparse_miss_default": "fga", "field_goal": "fga"}.get(ty, "end_period")
                    if ty == "field_goal" and e.get("team") != cur:
                        continue
                    if lab is None or ty in ("end_q1", "end_q3"):
                        continue  # follows the labelled event that ended the drive / drive continues across Q1, Q3
                    agg[cur][lab] += 1
                    depth[(depth_bucket(miny), lab)] += 1
                    if lab == "td":
                        agg[cur]["td_from_rz" if rz else "td_outside_rz"] += 1
                    drive_open = False
            for t in agg:
                agg[t]["points"] += st.score_home if t == st.home else st.score_away
    finally:
        simulate._apply_snap = orig
    out = {}
    for t, c in agg.items():
        d = max(c["drives"], 1)
        out[t] = {"points_pg": c["points"] / n, "snaps_pg": c["snaps"] / n, "kneels_pg": c["pt_qb_kneel"] / n,
                  "yards_per_snap": c["yards"] / max(c["snaps"], 1), "drives_pg": c["drives"] / n,
                  "td_per_drive": c["td"] / d, "fga_per_drive": c["fga"] / d, "punt_per_drive": c["punt"] / d,
                  "turnover_per_drive": c["turnover"] / d, "downs_per_drive": c["downs"] / d,
                  "end_half_per_drive": c["end_period"] / d, "rz_trips_pg": c["rz_trips"] / n,
                  "rz_td_rate": c["td_from_rz"] / max(c["rz_trips"], 1), "points_per_drive": c["points"] / d}
    return {"teams": out, "depth_counts": {f"{k[0]}|{k[1]}": v for k, v in depth.items()}, "total_mean": float(np.mean(totals)), "max_steps_rate": maxsteps / n,
            "h2h": prov["defense_interaction"]["h2h"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int)
    ap.add_argument("--games", default="")
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=4949)
    ap.add_argument("--h2h", default="off", choices=["off", "shrunk", "legacy_always"])
    ap.add_argument("--accounting", default="default", choices=["default", "legacy"])
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    if a.n > MAX_N:
        print(f"refused: n={a.n} > {MAX_N}"); return 2
    pbp = pd.read_parquet(PBP)
    sched = pbp.drop_duplicates("game_id")[["game_id", "week", "home_team", "away_team"]]
    if a.games:
        rows = [(g.split("_")[3], g.split("_")[2], int(g.split("_")[1])) for g in a.games.split(",")]
    else:
        s = sched[sched["week"] == a.week]
        rows = [(r.home_team, r.away_team, a.week) for r in s.itertuples()]
    h2h = {"mode": "shrunk"} if a.h2h == "shrunk" else a.h2h
    games, keys = [], ["points_pg", "snaps_pg", "kneels_pg", "yards_per_snap", "drives_pg", "td_per_drive",
                       "fga_per_drive", "punt_per_drive", "turnover_per_drive", "downs_per_drive",
                       "end_half_per_drive", "rz_trips_pg", "rz_td_rate", "points_per_drive"]
    for home, away, wk in rows:
        cfg = make_cfg(home, away, wk, h2h=h2h)
        if a.accounting == "legacy":
            cfg["accounting"] = "legacy"
        sim = sim_team_rates(cfg, a.n, a.seed)
        act = actual_team_rates(pbp, [home, away], list(range(1, wk)))
        games.append({"game": cfg["game"]["game_id"], "sim": sim, "actual_prior_weeks": act,
                      "actual_depth_counts": actual_depth_counts(pbp, [home, away], list(range(1, wk)))})
        print(cfg["game"]["game_id"], "sim total", round(sim["total_mean"], 1),
              "actual prior ppg sum", round(sum(v["points_pg"] for v in act.values()), 1), flush=True)
    # pooled per-team comparison (mean over team-games)
    pooled = {}
    for k in keys:
        s = [g["sim"]["teams"][t][k] for g in games for t in g["sim"]["teams"]]
        r = [g["actual_prior_weeks"][t][k] for g in games for t in g["actual_prior_weeks"] if g["actual_prior_weeks"][t][k] is not None]
        pooled[k] = {"sim": round(float(np.mean(s)), 4), "actual_same_teams_prior_weeks": round(float(np.mean(r)), 4),
                     "sim_minus_actual": round(float(np.mean(s) - np.mean(r)), 4)}
    doc = {"label": LABEL, "generated_by": "calibration/diagnose_total.py",
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "engine": engine_version(),
           "pbp": str(PBP.relative_to(ROOT)), "pbp_sha256": sha256(PBP), "pbp_pulled_et": PBP_PULLED_ET,
           "n_per_game": a.n, "seed": a.seed, "h2h": h2h, "accounting": a.accounting,
           "actual_definitions": ("nflverse W1..week-1, offense rows of the same two teams: snaps = pass/run/kneel/spike "
                                  "with a down; drives = distinct (game, drive) with fixed_drive_result; rz = drive_inside20"),
           "sim_definitions": ("drive = run of snaps by one offense ended by a score, punt, FG try, turnover, downs or "
                               "half end; rz trip = a snap taken at yardline_100 <= 20"),
           "pooled_per_team_game": pooled, "games": games}
    sd, ad = Counter(), Counter()
    for g in games:
        sd.update(g["sim"]["depth_counts"]); ad.update(g["actual_depth_counts"])
    doc["drive_depth_table"] = {"definition": "deepest snap yardline_100 of the drive (le20 = reached the red zone)",
                                "sim": depth_table(sd), "actual_same_teams_prior_weeks": depth_table(ad)}
    # Goal-line censoring evidence: share of sampled-pool rows (pass/run, prior weeks) whose gain was capped by the
    # goal line (offensive TD with yards_gained >= yardline_100), per engine yardline bucket.
    engine_path()
    from empirical import yl_bucket
    wk_max = max(r[2] for r in rows)
    pr = pbp[(pbp["week"] < wk_max) & pbp["play_type"].isin(["pass", "run"]) & pbp["down"].notna()].copy()
    pr["_yl"] = pr["yardline_100"].map(yl_bucket)
    pr["_cens"] = (pr["touchdown"] == 1) & (pr["td_team"] == pr["posteam"]) & (pr["yards_gained"] >= pr["yardline_100"])
    doc["goal_line_censoring"] = {"definition": "league pass/run rows before the latest target week; share whose gain was capped at the goal line",
                                  "by_yl_bucket": {b: {"rows": int(len(g)), "censored_share": round(float(g["_cens"].mean()), 4),
                                                       "yardline_range": [int(g["yardline_100"].min()), int(g["yardline_100"].max())]}
                                                   for b, g in pr.groupby("_yl")}}
    out = a.out or str(ROOT / f"calibration/outputs/diag_total_{'w%02d' % a.week if a.week else 'games'}_{a.h2h}_{a.accounting}.json")
    open(out, "w").write(json.dumps(doc, indent=1, default=float) + "\n")
    print(json.dumps({"pooled": pooled, "depth": doc["drive_depth_table"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
