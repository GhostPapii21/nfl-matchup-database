"""Historical validation of same-game slip probability: sim joint hit rate vs independent product (Rico item 8 /
Phase 6). Research only, not validated. BACKTEST on already-seen weeks 4-9 (NOT a clean holdout).

For every week 4-9 game the engine (new_off arm, point-in-time history weeks 1..w-1) is simulated n times. A fixed,
deterministic family of same-game slips is built per game from (a) the real consensus close total/spread
(ba83615:data/lines/lines_wk04_09_2026.csv) and (b) thresholds at the sim's own per-player medians. No prices, no alt
lines, no hand-typed numbers. Each slip gets p_joint (share of trials where every leg hits) and p_indep (product of
marginals from the same trials), and is graded against the realized game from the same nflverse PBP file.
A slip is VOID (dropped) if a leg pushes exactly on its line or a player leg's player recorded no credited play.

  python3 -m calibration.slip_joint_validation --n 1000 --workers 6 --tag wk04_09
"""
from __future__ import annotations
import argparse, json, math, sys, time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from calibration.common import PBP, PBP_PULLED_ET, MAX_N, LABEL, ROOT, engine_path, engine_version, make_cfg, sha256
from calibration import backtest as bt
from slips.joint import Leg, leg_hits, joint_from_hits, OPS, game_values

OUT = ROOT / "calibration/outputs"
FAMILIES = {
    "G2_total_x_side": "game total vs close total x home/away vs close spread (4 slips/game)",
    "S2_qb_wr1": "same team: QB1 pass yds >= sim median and WR1 rec yds >= sim median",
    "S2_qb_teampts": "same team: QB1 pass yds >= sim median and team points >= sim median",
    "S2_rb_win": "same team: RB1 rush yds >= sim median and team wins",
    "S2_rb_qb": "same team: RB1 rush yds >= sim median and QB1 pass yds >= sim median",
    "X2_qb_qb": "both QB1s pass yds >= their sim medians",
    "S3_qb_wr1_over": "same team: QB1, WR1 at sim medians and game total over the close total",
}


def _top(player_samples, kind, team):
    tot = {}
    for t in player_samples:
        for k, v in t.items():
            kd, tm, pl = k.split("|", 2)
            if kd == kind and tm == team:
                tot[pl] = tot.get(pl, 0.0) + v
    return max(tot, key=tot.get) if tot else None


def build_slips(sim, home, away, close):
    """Deterministic slip family for one game. Thresholds: close lines, or medians of the sim's own player values
    (x.5 offset avoids pushes on integer yards)."""
    from slips.joint import player_values
    slips = []
    ps = sim["player_samples"]
    if close and close.get("total") is not None and close.get("home_spread") is not None:
        tot, sp = close["total"], close["home_spread"]
        for o_name, o_op in (("over", ">"), ("under", "<")):
            for side, key_op in (("home", ">"), ("away", "<")):
                # home covers: home_margin > -home_spread ; away covers: home_margin < -home_spread
                slips.append(("G2_total_x_side", f"{o_name}_{side}",
                              [Leg("game", "total", o_op, tot), Leg("game", "home_margin", key_op, -sp)]))
    for team, opp in ((home, away), (away, home)):
        side_pts = "home_pts" if team == home else "away_pts"
        qb, wr, rb = _top(ps, "pass_yards", team), _top(ps, "rec_yards", team), _top(ps, "rush_yards", team)
        med = lambda kind, pl: math.floor(float(np.median(player_values(ps, kind, f"{team}|{pl}")))) + 0.5
        tp = math.floor(float(np.median(game_values(sim["arrays"], side_pts)))) + 0.5
        win = Leg("game", "home_margin", ">" if team == home else "<", 0)
        if qb and wr:
            slips.append(("S2_qb_wr1", team, [Leg("pass_yards", f"{team}|{qb}", ">=", med("pass_yards", qb)),
                                              Leg("rec_yards", f"{team}|{wr}", ">=", med("rec_yards", wr))]))
            if close and close.get("total") is not None:
                slips.append(("S3_qb_wr1_over", team, [Leg("pass_yards", f"{team}|{qb}", ">=", med("pass_yards", qb)),
                                                       Leg("rec_yards", f"{team}|{wr}", ">=", med("rec_yards", wr)),
                                                       Leg("game", "total", ">", close["total"])]))
        if qb:
            slips.append(("S2_qb_teampts", team, [Leg("pass_yards", f"{team}|{qb}", ">=", med("pass_yards", qb)),
                                                  Leg("game", side_pts, ">=", tp)]))
        if rb:
            slips.append(("S2_rb_win", team, [Leg("rush_yards", f"{team}|{rb}", ">=", med("rush_yards", rb)), win]))
        if rb and qb:
            slips.append(("S2_rb_qb", team, [Leg("rush_yards", f"{team}|{rb}", ">=", med("rush_yards", rb)),
                                             Leg("pass_yards", f"{team}|{qb}", ">=", med("pass_yards", qb))]))
    qh, qa = _top(ps, "pass_yards", home), _top(ps, "pass_yards", away)
    if qh and qa:
        mh = math.floor(float(np.median(player_values(ps, "pass_yards", f"{home}|{qh}")))) + 0.5
        ma = math.floor(float(np.median(player_values(ps, "pass_yards", f"{away}|{qa}")))) + 0.5
        slips.append(("X2_qb_qb", "both", [Leg("pass_yards", f"{home}|{qh}", ">=", mh), Leg("pass_yards", f"{away}|{qa}", ">=", ma)]))
    return slips


def _sim_job(job):
    gid, home, away, week, n, seed, close = job
    engine_path()
    import simulate
    cfg = make_cfg(home, away, week, h2h=bt.ARMS["new_off"]["h2h"])
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=simulate.stable_seed(seed, week, gid))
    if max(o["history_evidence"]["weeks"]) >= week:
        raise RuntimeError(f"{gid}: history leaks week >= {week}")
    out = []
    for fam, tag, legs in build_slips(o, home, away, close):
        r = joint_from_hits(leg_hits(o, legs))
        out.append({"game_id": gid, "week": week, "family": fam, "tag": tag,
                    "legs": [(l.kind, l.key, l.op, l.line) for l in legs],
                    "p_joint": r["p_joint"], "p_indep": r["p_independent"], "marginals": r["marginals"], "n": n})
    return out


def actual_game(pbp: pd.DataFrame, gid: str) -> dict:
    g = pbp[pbp.game_id == gid]
    r0 = g.iloc[0]
    players, played = {}, set()
    def add(kind, team, name, y):
        if isinstance(name, str) and name:
            k = f"{kind}|{team}|{name}"; players[k] = players.get(k, 0.0) + float(y)
    for r in g.itertuples():
        for c in ("passer_player_name", "receiver_player_name", "rusher_player_name"):
            v = getattr(r, c)
            if isinstance(v, str) and v:
                played.add(f"{r.posteam}|{v}")
        y = 0.0 if pd.isna(r.yards_gained) else float(r.yards_gained)
        if r.play_type == "pass" and (r.complete_pass == 1) and not (r.sack == 1):
            add("pass_yards", r.posteam, r.passer_player_name, y); add("rec_yards", r.posteam, r.receiver_player_name, y)
        elif r.play_type == "run":
            add("rush_yards", r.posteam, r.rusher_player_name, y)
    return {"home_pts": int(r0.home_score), "away_pts": int(r0.away_score), "players": players, "played": played}


def grade_leg(actual, leg):
    kind, key, op, line = leg
    if kind == "game":
        v = {"home_pts": actual["home_pts"], "away_pts": actual["away_pts"], "total": actual["home_pts"] + actual["away_pts"],
             "home_margin": actual["home_pts"] - actual["away_pts"]}[key]
    else:
        if key not in actual["played"]:
            return None
        v = actual["players"].get(f"{kind}|{key}", 0.0)
    if v == line:
        return None  # push -> void
    return bool(OPS[op](np.float64(v), line))


def metrics(df: pd.DataFrame, rng_seed=20261113, B=2000) -> dict:
    eps = 1e-4
    y = df.hit.values.astype(float)
    out = {"slips": int(len(df)), "games": int(df.game_id.nunique()), "hit_rate": float(y.mean())}
    for m in ("p_joint", "p_indep"):
        p = df[m].values
        pc = np.clip(p, eps, 1 - eps)
        out[f"mean_{m}"] = float(p.mean())
        out[f"brier_{m}"] = float(((p - y) ** 2).mean())
        out[f"logloss_{m}"] = float(-(y * np.log(pc) + (1 - y) * np.log(1 - pc)).mean())
    # game-clustered bootstrap of brier(indep) - brier(joint): > 0 means the joint method is better
    d = ((df.p_indep - df.hit) ** 2 - (df.p_joint - df.hit) ** 2).values
    games = df.game_id.values
    ug = np.unique(games); idx = {g: np.where(games == g)[0] for g in ug}
    rng = np.random.default_rng(rng_seed); bs = []
    for _ in range(B):
        pick = rng.choice(ug, size=len(ug), replace=True)
        ii = np.concatenate([idx[g] for g in pick]); bs.append(d[ii].mean())
    out["brier_improvement_joint_vs_indep"] = float(d.mean())
    out["brier_improvement_ci95_game_bootstrap"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    out["mean_lift_joint_over_indep"] = float((df.p_joint / df.p_indep.replace(0, np.nan)).mean())
    return out


def calib_bins(df, col, edges=(0, .1, .2, .3, .4, .5, .6, 1.0001)):
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = df[(df[col] >= lo) & (df[col] < hi)]
        if len(s):
            rows.append({"bin": f"[{lo:.1f},{min(hi,1):.1f})", "n": int(len(s)), "mean_pred": float(s[col].mean()), "hit_rate": float(s.hit.mean())})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", default="4-9")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261112)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--tag", default="wk04_09")
    a = ap.parse_args(argv)
    if a.n > MAX_N:
        print(f"refused: n={a.n} > {MAX_N}"); return 2
    lo, _, hi = a.weeks.partition("-")
    weeks = list(range(int(lo), int(hi or lo) + 1))
    if max(weeks) >= bt.HOLDOUT_FIRST_WEEK:
        print("refused: weeks >= 10 are the reserved holdout"); return 2
    pbp = pd.read_parquet(PBP)
    sched = pbp.drop_duplicates("game_id")
    sched = sched[sched.week.isin(weeks) & (sched.season == 2026)]
    lines, lines_meta = bt.load_lines()
    close = bt.close_for_games(lines)
    jobs = [(r.game_id, r.home_team, r.away_team, int(r.week), a.n, a.seed, close.get(r.game_id)) for r in sched.itertuples()]
    t0 = time.time(); rows = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for res in ex.map(_sim_job, jobs):
            rows.extend(res); print(f"{res[0]['game_id'] if res else '?'}: {len(res)} slips", flush=True)
    actual = {gid: actual_game(pbp, gid) for gid in sched.game_id}
    graded = []
    for r in rows:
        hs = [grade_leg(actual[r["game_id"]], l) for l in r["legs"]]
        if any(h is None for h in hs):
            continue
        graded.append({**{k: r[k] for k in ("game_id", "week", "family", "tag", "p_joint", "p_indep", "n")},
                       "legs": json.dumps(r["legs"]), "hit": int(all(hs)), "leg_hits": json.dumps(hs)})
    df = pd.DataFrame(graded)
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"slip_joint_validation_{a.tag}_n{a.n}"
    df.to_csv(OUT / f"{stem}_slips.csv", index=False, float_format="%.5f")
    res = {"ALL": metrics(df), **{f: metrics(df[df.family == f]) for f in FAMILIES if (df.family == f).any()}}
    doc = {"label": LABEL, "set_label": "BACKTEST on already-seen weeks 4-9 (NOT a clean holdout)",
           "command": "python3 -m calibration.slip_joint_validation " + " ".join(sys.argv[1:] if argv is None else argv),
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "runtime_sec": round(time.time() - t0, 1),
           "engine": engine_version(), "arm": "new_off", "n_per_game": a.n, "seed_base": a.seed,
           "pbp": {"path": str(PBP.relative_to(ROOT)), "sha256": sha256(PBP), "pulled_et": PBP_PULLED_ET},
           "lines": lines_meta, "families": FAMILIES, "slips_built": len(rows), "slips_graded": len(df),
           "slips_void": len(rows) - len(df),
           "results": res, "calibration_bins": {"p_joint": calib_bins(df, "p_joint"), "p_indep": calib_bins(df, "p_indep")},
           "notes": ["p_joint = share of sim trials where every leg hits; p_indep = product of the same trials' marginals",
                     "brier_improvement_joint_vs_indep > 0 means joint beats independence; CI is a game-clustered bootstrap",
                     "thresholds are close lines or sim medians; no prices, no alt lines"]}
    (OUT / f"{stem}.json").write_text(json.dumps(doc, indent=1, default=float) + "\n")
    print(json.dumps(res, indent=1, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
