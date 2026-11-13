"""NFL-75 Phase 2: walk-forward backtest of the player opportunity model vs the name-locked recorder, 2026 Weeks 4-9.

    python3 -m calibration.opportunity_backtest --weeks 4 5 6 7 8 9 --n 2000 --workers 7

For each eval week w: fit the opportunity parameters on data before w (calibration.opportunity_fit.fit_week), FREEZE
them to params_w{w}.json, build each game's model, then run the engine once per game (calibration.common.make_cfg,
h2h off, history weeks 1..w-1) with BOTH recorders on the same snaps: the name-locked player_box (main) and the
opportunity recorder. Score every player-game against the week-w nflverse play-by-play (committed 2026 W1-9 file).
Weeks >= 10 are refused. LABEL: BACKTEST on already-seen data (weeks 4-9 were used while building the engine), the
opportunity model's own parameters are walk-forward (fit before w, frozen, scored on w).
Research only. projection_ready stays false. Zero Odds API credits, no network."""
from __future__ import annotations
import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from calibration.common import PBP, engine_path, engine_version, make_cfg
from calibration import opportunity_fit as F

OUT = F.ROOT / "research/runs/2026-11-13_opportunity_phase2"
STATS = ("pass_att", "targets", "rec", "rec_yds", "carries", "rush_yds", "int_thrown", "pass_td", "rec_td", "rush_td")
THRESH = {"rec": (3, 5), "rec_yds": (25, 50, 75), "rush_yds": (25, 50, 75)}
OPP_BY_GROUP = {"QB": ("pass_att", "carries"), "RB": ("carries", "targets"), "WR": ("targets",), "TE": ("targets",)}


def actual_lines(week: int) -> dict:
    """{(team, name): {stat: value}} from the committed 2026 PBP, same row rules as player_box."""
    df = F.load_pbp(2026)
    df = df[df["week"] == week]
    out: dict = {}
    def add(t, n, s, v=1):
        if not isinstance(n, str):
            return
        d = out.setdefault((t, n), {})
        d[s] = d.get(s, 0) + v
    for r in df.itertuples(index=False):
        y = r.yards_gained if r.yards_gained == r.yards_gained else 0
        if r.play_type == "pass" and r.sack != 1:
            add(r.posteam, r.passer_player_name, "pass_att")
            if isinstance(r.receiver_player_name, str) or r.complete_pass == 1:
                add(r.posteam, r.receiver_player_name, "targets")
            if r.complete_pass == 1:
                add(r.posteam, r.receiver_player_name, "rec")
                add(r.posteam, r.receiver_player_name, "rec_yds", y)
            if r.interception == 1:
                add(r.posteam, r.passer_player_name, "int_thrown")
        elif r.play_type == "run":
            add(r.posteam, r.rusher_player_name, "carries")
            add(r.posteam, r.rusher_player_name, "rush_yds", y)
    return out


def _summ(box, n):
    cols, vals = box["columns"], box["values"]
    res: dict = {}
    for j, (t, p, s) in enumerate(cols):
        if s not in STATS:
            continue
        v = vals[:, j]
        d = {"mean": float(v.mean()), "p10": float(np.percentile(v, 10)), "p90": float(np.percentile(v, 90)),
             "p_ge1": float((v >= 1).mean())}
        for thr in THRESH.get(s, ()):
            d[f"p_ge{thr}"] = float((v >= thr).mean())
        res.setdefault(f"{t}|{p}", {})[s] = d
    return res


def _job(args):
    gid, home, away, week, n, seed, model_path = args[:7]
    ip = args[7] if len(args) > 7 else None
    engine_path()
    import simulate
    model = json.loads(Path(model_path).read_text())
    cfg = make_cfg(home, away, week, h2h="off")
    t0 = time.time()
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=simulate.stable_seed(seed, week, gid),
                                opportunity_model=model, **({"int_pool": ip} if ip is not None else {}))
    if max(o["history_evidence"]["weeks"]) >= week:
        raise RuntimeError(f"{gid}: history leaks week >= {week}")
    ob = o["player_box_opportunity"]
    return {"game_id": gid, "week": week, "home": home, "away": away, "n": n,
            "name_locked": _summ(o["player_box"], n), "opportunity": _summ(ob, n),
            "recon": {"name_locked_failures": o["player_box"]["reconciliation"]["failures"],
                      "opportunity_failures": ob["reconciliation"]["failures"]},
            "secs": round(time.time() - t0, 1),
            **({"int_pool": {"spec": o["int_pool"]["spec"], "counts": o["int_pool"]["counts"],
                             "teams": {t: o["int_pool"]["teams"].get(t) for t in (home, away)}}} if ip is not None else {})}


def games_for_week(week: int) -> list:
    df = pd.read_parquet(PBP, columns=["game_id", "week", "home_team", "away_team", "season_type"])
    df = df[(df["week"] == week) & (df["season_type"] == "REG")].drop_duplicates("game_id")
    return [(r.game_id, r.home_team, r.away_team) for r in df.sort_values("game_id").itertuples()]


def _fit(week):
    return week, F.fit_week(2026, week)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", type=int, nargs="+", default=[4, 5, 6, 7, 8, 9])
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261113)
    ap.add_argument("--workers", type=int, default=7)
    ap.add_argument("--refit", action="store_true")
    ap.add_argument("--variant", choices=("phase2", "phase2b", "phase2b_noint"), default="phase2",
                    help="phase2b: depth-signal params from research/runs/2026-11-13_opportunity_phase2b/params "
                         "(fitted by fit2b, frozen before scoring) + opt-in engine INT pooling fitted walk-forward")
    a = ap.parse_args(argv)
    global OUT
    if a.variant in ("phase2b", "phase2b_noint"):
        OUT = F.ROOT / "research/runs/2026-11-13_opportunity_phase2b"
        missing = [w for w in a.weeks if not (OUT / f"params/params_2026_w{w:02d}.json").exists()]
        if missing or a.refit:
            raise SystemExit(f"phase2b params must be fitted and frozen first by calibration/opportunity_fit2b.py "
                             f"(missing weeks {missing}); --refit is not allowed here")
    if any(w >= F.HOLDOUT_FIRST_WEEK for w in a.weeks):
        raise SystemExit("weeks >= 10 are the reserved live holdout; refused")
    if a.n > 20_000:
        raise SystemExit("n <= 20,000 per game")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "params").mkdir(exist_ok=True)
    mdir = Path("/tmp/p2work/models"); mdir.mkdir(parents=True, exist_ok=True)
    src = F.verify_sources()
    todo = [w for w in a.weeks if a.refit or not (OUT / f"params/params_2026_w{w:02d}.json").exists()]
    with ProcessPoolExecutor(max_workers=min(len(todo) or 1, a.workers)) as ex:
        for w, p in ex.map(_fit, todo):
            (OUT / f"params/params_2026_w{w:02d}.json").write_text(json.dumps(p, indent=1, default=str) + "\n")
            print(f"froze params week {w}", flush=True)
    raw_out = OUT / "backtest_raw.json"
    if a.variant == "phase2b_noint":  # depth effect alone: Phase 2b params, engine WITHOUT INT pooling
        raw_out = OUT / "noint/backtest_raw_noint.json"
        raw_out.parent.mkdir(exist_ok=True)
    jobs = []
    ipspec = {}
    if a.variant == "phase2b":
        for w in a.weeks:  # frozen by calibration/opportunity_intcap.py before scoring
            ipspec[w] = json.loads((OUT / f"int_pool/int_pool_2026_w{w:02d}.json").read_text())
    for w in a.weeks:
        params = json.loads((OUT / f"params/params_2026_w{w:02d}.json").read_text())  # frozen before scoring
        for gid, home, away in games_for_week(w):
            m = F.build_model(2026, w, [home, away], params)
            mp = mdir / f"model_{a.variant}_2026_w{w:02d}_{away}_{home}.json"
            mp.write_text(json.dumps(m, default=float))
            jobs.append((gid, home, away, w, a.n, a.seed, str(mp)) + ((ipspec[w],) if ipspec else ()))
    print(f"{len(jobs)} games", flush=True)
    res = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(_job, jobs):
            print(f"{r['game_id']} {r['secs']}s recon {r['recon']}", flush=True)
            res.append(r)
    acts = {w: {f"{t}|{nm}": v for (t, nm), v in actual_lines(w).items()} for w in a.weeks}
    raw_out.write_text(json.dumps({"games": res, "actual": {str(k): v for k, v in acts.items()},
                                                        "n": a.n, "seed": a.seed, "weeks": a.weeks,
                                                        "variant": a.variant,
                                                        "engine": engine_version(), "sources": src},
                                                       default=float) + "\n")
    print("wrote", raw_out)


if __name__ == "__main__":
    main()
