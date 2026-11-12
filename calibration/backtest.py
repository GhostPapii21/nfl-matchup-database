"""NFL-49 task C: point-in-time walk-forward BACKTEST, weeks 4-9 of 2026.

    python3 -m calibration.backtest                     # weeks 4-9, n=2000/game, arms new_off + legacy_old
    python3 -m calibration.backtest --arms new_off --n 500 --weeks 9 --tag quick

Single command, reruns cleanly on any later engine: every output records git head, the engine tree hash and a
sha256 over core/possession_engine_v0/*.py (calibration.common.engine_version).

LABEL: BACKTEST on already-seen data (weeks 4-9 were used while building the model and its review), NOT a clean
holdout. Weeks >= 10 are the reserved live holdout and are refused here.

Point in time: each game is simulated with history weeks 1..(week-1) only (cfg history + as-of penalty/return
models), from the committed nflverse W1-9 PBP (pulled 2026-11-12 11:16 AM ET). n <= 20,000 per game, never 100k.
Market: Blitz's data/lines/lines_wk04_09_2026.csv read with `git show <ref>:<path>` (never merged); graded vs CLOSE.
Close used per game: book=consensus close (nflverse games.csv, pulled 2026-11-09 22:25:18Z); 2026_09_BUF_MIN has no
consensus close, so the mean of its DraftKings/FanDuel/Pinnacle closes (pulled 2026-11-10T01:14:01Z) is used.
Win probability from the close moneylines, de-vigged proportionally. Missing = unknown, never filled.
Research only, not validated. Zero Odds API credits (no network).
"""
from __future__ import annotations
import argparse, csv, io, json, math, subprocess, time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from calibration.common import (PBP, PBP_PULLED_ET, MAX_N, LABEL, ROOT, engine_path, engine_version, make_cfg, sha256)

OUT = ROOT / "calibration/outputs"
LINES_REF = "ba83615"
LINES_PATH = "data/lines/lines_wk04_09_2026.csv"
LINES_SHA256 = "6e330ca155e285e919716ecc3d53dce0d0c74c4cc3d83c927fbdcba872a85212"  # data/lines/README.md
HOLDOUT_FIRST_WEEK = 10
ARMS = {
    # new engine defaults: h2h off, NFL-49 B accounting
    "new_off": {"h2h": "off", "accounting": None},
    "new_shrunk": {"h2h": {"mode": "shrunk"}, "accounting": None},
    # the engine as it was for the TNF / BUF@NYJ locks: h2h always on, legacy accounting
    "legacy_old": {"h2h": "legacy_always", "accounting": "legacy"},
}


def load_lines(ref: str = LINES_REF, path: str = LINES_PATH) -> tuple[pd.DataFrame, dict]:
    raw = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, check=True).stdout
    import hashlib
    h = hashlib.sha256(raw).hexdigest()
    df = pd.read_csv(io.BytesIO(raw), dtype={"game_id": str, "book": str, "line_type": str})
    return df, {"ref": ref, "path": path, "sha256": h, "sha256_matches_readme": h == LINES_SHA256}


def american_to_prob(ml) -> float:
    ml = float(ml)
    return 100.0 / (ml + 100.0) if ml > 0 else -ml / (-ml + 100.0)


def close_for_games(lines: pd.DataFrame) -> dict:
    """game_id -> {home_spread, total, p_home_devig, source, pulled_utc}. Blank stays None."""
    c = lines[lines["line_type"] == "close"]
    out = {}
    for gid, g in c.groupby("game_id"):
        cons = g[g["book"] == "consensus"]
        if len(cons):
            r = cons.iloc[0]
            sp = None if pd.isna(r.home_spread) else float(r.home_spread)
            tot = None if pd.isna(r.total) else float(r.total)
            ph = None
            if pd.notna(r.home_ml) and pd.notna(r.away_ml):
                a, b = american_to_prob(r.home_ml), american_to_prob(r.away_ml)
                ph = a / (a + b)
            out[gid] = {"home_spread": sp, "total": tot, "p_home_devig": ph, "source": f"consensus close: {r.source}",
                        "pulled_utc": r.pulled_utc}
        else:
            sub = g[g["book"].isin(["draftkings", "fanduel", "pinnacle"])]
            if not len(sub):
                continue
            sp = sub["home_spread"].dropna(); tot = sub["total"].dropna()
            ps = [american_to_prob(h) / (american_to_prob(h) + american_to_prob(a))
                  for h, a in zip(sub["home_ml"], sub["away_ml"]) if pd.notna(h) and pd.notna(a)]
            out[gid] = {"home_spread": float(sp.mean()) if len(sp) else None, "total": float(tot.mean()) if len(tot) else None,
                        "p_home_devig": float(np.mean(ps)) if ps else None,
                        "source": "mean of DK/FD/Pinnacle closes (no consensus close): " + ";".join(sorted(set(sub["source"]))),
                        "pulled_utc": ",".join(sorted(set(sub["pulled_utc"])))}
    return out


def _sim_game(job):
    gid, home, away, week, arm, n, seed = job
    engine_path()
    import simulate
    cfg = make_cfg(home, away, week, h2h=ARMS[arm]["h2h"])
    if ARMS[arm]["accounting"] is not None:
        cfg["accounting"] = ARMS[arm]["accounting"]
    t0 = time.time()
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=simulate.stable_seed(seed, week, gid))
    ev = o["history_evidence"]
    if max(ev["weeks"]) >= week:
        raise RuntimeError(f"{gid}: history leaks week >= {week}")
    A = o["arrays"]
    hp, ap = A["fg_home"].astype(float), A["fg_away"].astype(float)
    m = hp - ap
    return {"game_id": gid, "arm": arm, "week": week, "home": home, "away": away, "n": n, "status": o["status"],
            "sim_home": float(hp.mean()), "sim_away": float(ap.mean()), "sim_total": float((hp + ap).mean()),
            "sim_margin": float(m.mean()), "sim_total_sd": float((hp + ap).std(ddof=1)), "sim_margin_sd": float(m.std(ddof=1)),
            "p_home_win": float((m > 0).mean() + 0.5 * (m == 0).mean()),
            "history_weeks": ev["weeks"], "history_plays": ev["n_plays"], "secs": round(time.time() - t0, 1),
            "h2h": o["effects_provenance"]["defense_interaction"]["h2h"],
            "accounting": o["effects_provenance"].get("accounting", "absent (pre-NFL-49 engine)"),
            "def_cond_snaps_per_game": o["evidence_summary"]["defense_cond_flag_events"] / n,
            "_totals": (hp + ap), "_margins": m}


def _brier(p, y):
    return float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))


def _logloss(p, y):
    p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6); y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def grade(rows: list[dict], actual: dict, close: dict) -> dict:
    df = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in rows])
    df["act_home"] = df.game_id.map(lambda g: actual[g]["home"])
    df["act_away"] = df.game_id.map(lambda g: actual[g]["away"])
    df["act_total"] = df.act_home + df.act_away
    df["act_margin"] = df.act_home - df.act_away
    df["close_total"] = df.game_id.map(lambda g: (close.get(g) or {}).get("total"))
    df["close_home_spread"] = df.game_id.map(lambda g: (close.get(g) or {}).get("home_spread"))
    df["close_p_home"] = df.game_id.map(lambda g: (close.get(g) or {}).get("p_home_devig"))
    df["close_source"] = df.game_id.map(lambda g: (close.get(g) or {}).get("source"))
    df["close_pulled_utc"] = df.game_id.map(lambda g: (close.get(g) or {}).get("pulled_utc"))
    # P(sim total > actual) percentile = PIT, filled by caller
    out = {}
    for arm, g in df.groupby("arm"):
        dec = g[g.act_margin != 0]
        y = (dec.act_margin > 0).astype(float)
        r = {"games": int(len(g)), "weeks": sorted(int(w) for w in g.week.unique()),
             "decided_games": int(len(dec)), "ties": int((g.act_margin == 0).sum()),
             "mae_home_pts": float((g.sim_home - g.act_home).abs().mean()),
             "mae_away_pts": float((g.sim_away - g.act_away).abs().mean()),
             "mae_total": float((g.sim_total - g.act_total).abs().mean()),
             "mae_margin": float((g.sim_margin - g.act_margin).abs().mean()),
             "total_bias_sim_minus_actual": float((g.sim_total - g.act_total).mean()),
             "margin_bias_sim_minus_actual": float((g.sim_margin - g.act_margin).mean()),
             "mean_sim_total": float(g.sim_total.mean()), "mean_actual_total": float(g.act_total.mean()),
             "brier_model": _brier(dec.p_home_win, y), "logloss_model": _logloss(dec.p_home_win, y),
             "brier_coinflip": 0.25, "logloss_coinflip": math.log(2)}
        mk = g[g.close_total.notna()]
        r["market_games_with_close_total"] = int(len(mk))
        if len(mk):
            r["mae_total_close"] = float((mk.close_total - mk.act_total).abs().mean())
            r["mae_total_model_same_games"] = float((mk.sim_total - mk.act_total).abs().mean())
            r["total_bias_close_minus_actual"] = float((mk.close_total - mk.act_total).mean())
            r["mean_model_minus_close_total"] = float((mk.sim_total - mk.close_total).mean())
            r["corr_model_total_vs_close"] = float(np.corrcoef(mk.sim_total, mk.close_total)[0, 1])
        ms = g[g.close_home_spread.notna()]
        if len(ms):
            close_margin = -ms.close_home_spread
            r["mae_margin_close"] = float((close_margin - ms.act_margin).abs().mean())
            r["mae_margin_model_same_games"] = float((ms.sim_margin - ms.act_margin).abs().mean())
            r["mean_abs_model_margin_minus_close"] = float((ms.sim_margin - close_margin).abs().mean())
            r["corr_model_margin_vs_close"] = float(np.corrcoef(ms.sim_margin, close_margin)[0, 1])
        mp = dec[dec.close_p_home.notna()]
        if len(mp):
            yy = (mp.act_margin > 0).astype(float)
            r["market_wp_games"] = int(len(mp))
            r["brier_close_devig"] = _brier(mp.close_p_home, yy)
            r["logloss_close_devig"] = _logloss(mp.close_p_home, yy)
            r["brier_model_same_games"] = _brier(mp.p_home_win, yy)
            r["logloss_model_same_games"] = _logloss(mp.p_home_win, yy)
        bins = [0, .2, .35, .5, .65, .8, 1.0001]
        cal = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            b = dec[(dec.p_home_win >= lo) & (dec.p_home_win < hi)]
            if len(b):
                cal.append({"bin": f"[{lo:.2f},{min(hi,1):.2f})", "n": int(len(b)), "mean_p_home": round(float(b.p_home_win.mean()), 3),
                            "home_win_rate": round(float((b.act_margin > 0).mean()), 3)})
        r["calibration_table_p_home_win"] = cal
        r["pit_total_quartiles"] = None
        out[arm] = r
    return {"by_arm": out, "per_game": df}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", default="4-9")
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261112)
    ap.add_argument("--arms", default="new_off,legacy_old")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--lines-ref", default=LINES_REF)
    ap.add_argument("--tag", default="wk04_09")
    a = ap.parse_args(argv)
    if a.n > MAX_N:
        print(f"refused: n={a.n} > {MAX_N} (never 100k)"); return 2
    lo, _, hi = a.weeks.partition("-")
    weeks = list(range(int(lo), int(hi or lo) + 1))
    if max(weeks) >= HOLDOUT_FIRST_WEEK:
        print(f"refused: week >= {HOLDOUT_FIRST_WEEK} is the reserved live holdout"); return 2
    arms = a.arms.split(",")
    for arm in arms:
        if arm not in ARMS:
            print(f"unknown arm {arm}"); return 2
    pbp = pd.read_parquet(PBP, columns=["game_id", "week", "season", "home_team", "away_team", "home_score", "away_score"])
    sched = pbp.drop_duplicates("game_id")
    sched = sched[sched.week.isin(weeks) & (sched.season == 2026)]
    actual = {r.game_id: {"home": int(r.home_score), "away": int(r.away_score)} for r in sched.itertuples()}
    try:
        lines, lines_meta = load_lines(a.lines_ref)
        close = close_for_games(lines)
    except subprocess.CalledProcessError as e:
        lines_meta, close = {"status": "UNAVAILABLE", "error": str(e)}, {}
    jobs = [(r.game_id, r.home_team, r.away_team, int(r.week), arm, a.n, a.seed) for arm in arms for r in sched.itertuples()]
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for res in ex.map(_sim_game, jobs):
            rows.append(res)
            print(f"{res['arm']:<11} {res['game_id']:<17} sim {res['sim_away']:.1f}-{res['sim_home']:.1f} "
                  f"act {actual[res['game_id']]['away']}-{actual[res['game_id']]['home']} ({res['secs']}s)", flush=True)
    # PIT of actual total within each game's simulated distribution
    pit = {}
    for r in rows:
        act_t = actual[r["game_id"]]["home"] + actual[r["game_id"]]["away"]
        t = r["_totals"]
        pit[(r["arm"], r["game_id"])] = float((t < act_t).mean() + 0.5 * (t == act_t).mean())
    g = grade(rows, actual, close)
    per = g["per_game"]
    per["pit_total"] = [pit[(r.arm, r.game_id)] for r in per.itertuples()]
    for arm, r in g["by_arm"].items():
        p = per[per.arm == arm]["pit_total"]
        r["pit_total_quartiles"] = {"q1_share(<.25)": round(float((p < .25).mean()), 3), "q2": round(float(((p >= .25) & (p < .5)).mean()), 3),
                                    "q3": round(float(((p >= .5) & (p < .75)).mean()), 3), "q4_share(>=.75)": round(float((p >= .75).mean()), 3),
                                    "note": "uniform 0.25 each if the simulated total distribution is calibrated"}
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"backtest_{a.tag}_n{a.n}"
    per.to_csv(OUT / f"{stem}_per_game.csv", index=False, float_format="%.4f")
    doc = {"label": LABEL, "set_label": "BACKTEST on already-seen weeks 4-9 (NOT a clean holdout; weeks >= 10 reserved as live holdout)",
           "generated_by": "calibration/backtest.py", "command": "python3 -m calibration.backtest " + " ".join(argv or []),
           "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "runtime_sec": round(time.time() - t0, 1),
           "engine": engine_version(), "arms": {k: ARMS[k] for k in arms}, "n_per_game": a.n, "seed_base": a.seed,
           "pbp": {"path": str(PBP.relative_to(ROOT)), "sha256": sha256(PBP), "pulled_et": PBP_PULLED_ET,
                   "use": "history weeks 1..week-1 only per game (point in time); actual final scores from the same file"},
           "lines": {**lines_meta, "graded_against": "close", "close_rule": "consensus close; 2026_09_BUF_MIN = mean DK/FD/Pinnacle closes",
                     "games_with_close": len([gid for gid in actual if gid in close]),
                     "known_limits": "wk4-5 consensus closes only; consensus pulled_utc is the games.csv fetch time (after kickoff by design), the quote time itself is unknown"},
           "results": g["by_arm"]}
    (OUT / f"{stem}.json").write_text(json.dumps(doc, indent=1, default=float) + "\n")
    print(json.dumps(doc["results"], indent=1, default=float))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
