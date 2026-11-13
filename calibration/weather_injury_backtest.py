"""NFL-75 item 6: backtest opt-in weather and injury adjustments, each separately, 2026 weeks 4-9 vs the close.

    python3 -m calibration.weather_injury_backtest --pbp-dir <folder of nflverse play_by_play_2018..2025.parquet>
        [--n 2000 --workers 8]

Walk-forward / no leakage:
  * Weather coefficients are REFIT on 2018-2025 only (research/weather/fit_rain_effects.py functions, written to
    research/weather/rain_effects_train_2018_2025.json) and frozen before any 2026 game is simulated. The committed
    rain_effects.json includes 2026 weeks 4-9 and is NOT used here.
  * Injury adjustment has no fitted parameters (it only removes rows of players listed Out).
  * Engine history per game = 2026 weeks 1..w-1 (calibration.common.make_cfg). Weeks >= 10 refused.
Point-in-time evidence:
  * Weather: the nflverse play-by-play `weather` / `roof` / `wind` fields of the game itself (kickoff observation
    recorded by the home team; wind parsed from the text when the numeric field is blank). This is a kickoff
    observation, not a pregame forecast, so it is an optimistic (upper-bound) test of a forecast-driven adjustment.
  * Injuries: nflverse injuries_2026 (final game-status report, published before kickoff), report_status == "Out",
    skill positions QB/RB/WR/TE/FB. Doubtful/Questionable are not used.
Arms: baseline = main engine defaults (adjustments off, h2h off) -- re-simulated for the games each arm touches and
checked against calibration/outputs/backtest_after_wp12_n2000_per_game.csv; weather; injury. Same seed per game.
Research only, not validated. n <= 20,000, never 100k.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

from calibration.common import PBP, ROOT, engine_path, engine_version, make_cfg, sha256
from calibration.backtest import load_lines, close_for_games

OUT = ROOT / "calibration/outputs"
INJ = ROOT / "data/historical/nflverse/injuries_2026_pulled_20261113T0526Z.parquet"
INJ_PULLED_UTC = "2026-11-13T05:26:36Z"  # https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_2026.parquet
TRAIN_EFFECTS = "research/weather/rain_effects_train_2018_2025.json"
BASE_CSV = OUT / "backtest_after_wp12_n2000_per_game.csv"
SKILL = ("QB", "RB", "WR", "TE", "FB")
B, BOOT_SEED = 2000, 20261113


def fit_train_effects(pbp_dir: Path) -> dict:
    sys.path.insert(0, str(ROOT / "research/weather"))
    import fit_rain_effects as fre
    import pyarrow.parquet as pq
    files = [Path(pbp_dir) / f"play_by_play_{y}.parquet" for y in range(2018, 2026)]
    parts = []
    for f in files:
        names = set(pq.read_schema(f).names)
        parts.append(pd.read_parquet(f, columns=[c for c in fre.COLS if c in names]))
    pbp = pd.concat(parts, ignore_index=True)
    assert int(pbp.season.max()) <= 2025
    players = pd.read_parquet(ROOT / "fixtures/players.parquet")
    pos = players.drop_duplicates("gsis_id").set_index("gsis_id").position
    res = fre.fit(fre.team_games(pbp, pos))
    res.update(seasons=sorted(int(s) for s in pbp.season.unique()),
               method="research/weather/fit_rain_effects.py fit(), TRAIN ONLY 2018-2025 (no 2026 rows)",
               sources={f.name: {"sha256": sha256(f)} for f in files})
    (ROOT / TRAIN_EFFECTS).write_text(json.dumps(res, indent=1) + "\n")
    return res


def wind_mph(text, wind) -> float | None:
    if wind is not None and not pd.isna(wind):
        return float(wind)
    m = re.search(r"Wind:\s*(?:[NSEW]{1,3}\s*)?(\d+)\s*mph", str(text or ""), re.I)
    if m:
        return float(m.group(1))
    if re.search(r"Wind:\s*calm", str(text or ""), re.I):
        return 0.0
    return None


def weather_specs(games: pd.DataFrame) -> dict:
    sys.path.insert(0, str(ROOT / "research/weather"))
    from fit_rain_effects import rain_tier
    out = {}
    for r in games.itertuples():
        outdoor = r.roof in ("outdoors", "open")
        w = wind_mph(r.weather, r.wind) if outdoor else 0.0
        tier = rain_tier(r.weather, w) if outdoor else "indoor"
        R = 1.0 if tier in ("light", "rain", "heavy") else 0.0
        on = outdoor and tier != "snow" and (R > 0 or (w or 0) > 10)
        out[r.game_id] = {"outdoor": outdoor, "tier": tier, "rain": R, "wind_mph": w, "on": bool(on),
                          "text": r.weather, "roof": r.roof}
    return out


def injury_specs(games: pd.DataFrame) -> dict:
    inj = pd.read_parquet(INJ)
    inj = inj[(inj.report_status == "Out") & inj.position.isin(SKILL) & (inj.season_type == "REG")]
    out = {}
    for r in games.itertuples():
        d = {}
        for t in (r.home_team, r.away_team):
            ids = sorted(inj[(inj.week == r.week) & (inj.team == t)].gsis_id.dropna().unique().tolist())
            if ids:
                d[t] = ids
        out[r.game_id] = d
    return out


def _sim(job):
    gid, home, away, week, arm, n, seed, extra = job
    engine_path()
    import simulate
    cfg = make_cfg(home, away, week, h2h="off")
    research = ()
    if arm == "weather":
        cfg["environment"] = {"weather": {"mode": "rain_wind_v1", "rain": extra["rain"], "wind_mph": extra["wind_mph"] or 0.0,
                                          "effects_path": TRAIN_EFFECTS,
                                          "evidence": {"source": "nflverse pbp weather/roof/wind (kickoff observation)",
                                                       "asof": "kickoff", "text": extra["text"]}}}
        research = ("weather_rain_wind_v1",)
    elif arm == "injury":
        cfg["availability"] = {"mode": "injury_report_out_v1", "out_player_ids": extra,
                               "evidence": {"source": f"nflverse injuries_2026 report_status=Out (pulled {INJ_PULLED_UTC})",
                                            "asof": "final game-status report, before kickoff"}}
        research = ("injury_report_out_v1",)
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=n, seed=simulate.stable_seed(seed, week, gid),
                                research_unaccepted=research)
    A = o["arrays"]; hp, ap = A["fg_home"].astype(float), A["fg_away"].astype(float); m = hp - ap
    env = o.get("environment_adjustments") or {}
    av = (env.get("availability") or {}).get("teams") or {}
    return {"game_id": gid, "arm": arm, "week": week, "sim_home": float(hp.mean()), "sim_away": float(ap.mean()),
            "sim_total": float((hp + ap).mean()), "sim_margin": float(m.mean()),
            "p_home_win": float((m > 0).mean() + 0.5 * (m == 0).mean()),
            "rows_removed": int(sum(v["rows_removed"] for v in av.values())),
            "qb_kept_sparse": [t for t, v in av.items() if v["passer_rows_kept_sparse"]],
            "keep_completion": (env.get("weather") or {}).get("keep_completion"),
            "ypc_factor": (env.get("weather") or {}).get("ypc_factor")}


def _brier(p, y): return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


def _ece(p, y, bins=10):
    p, y = np.asarray(p, float), np.asarray(y, float)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    return float(sum(abs(p[idx == b].mean() - y[idx == b].mean()) * (idx == b).sum() for b in range(bins) if (idx == b).any()) / len(p))


def compare(df: pd.DataFrame, arm: str, rng) -> dict:
    """df has base_* and arm_* columns plus act_*, close_*; one row per game the arm touched."""
    dec = df[df.act_margin != 0]; y = (dec.act_margin > 0).astype(float).values
    pb, pa = dec.base_p.values, dec.arm_p.values
    eb = np.abs(df.base_margin - df.act_margin).values; ea = np.abs(df.arm_margin - df.act_margin).values
    tb = np.abs(df.base_total - df.act_total).values; ta = np.abs(df.arm_total - df.act_total).values
    n, nd = len(df), len(dec)
    q = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    i = rng.integers(0, nd, size=(B, nd)); j = rng.integers(0, n, size=(B, n))
    d_brier = ((pa[i] - y[i]) ** 2).mean(1) - ((pb[i] - y[i]) ** 2).mean(1)
    d_mm = ea[j].mean(1) - eb[j].mean(1); d_tm = ta[j].mean(1) - tb[j].mean(1)
    cm = df.close_margin.values; ct = df.close_total.values
    return {"arm": arm, "n_games": int(n), "n_decided": int(nd),
            "brier_base": _brier(pb, y), "brier_arm": _brier(pa, y), "brier_diff": _brier(pa, y) - _brier(pb, y),
            "brier_diff_ci95": q(d_brier), "ece_base": _ece(pb, y), "ece_arm": _ece(pa, y),
            "brier_close": _brier(dec.close_p.values, y),
            "mae_margin_base": float(eb.mean()), "mae_margin_arm": float(ea.mean()), "mae_margin_diff_ci95": q(d_mm),
            "mae_total_base": float(tb.mean()), "mae_total_arm": float(ta.mean()), "mae_total_diff_ci95": q(d_tm),
            "mae_margin_close": float(np.abs(cm - df.act_margin.values).mean()),
            "mae_total_close": float(np.abs(ct - df.act_total.values).mean()),
            "mean_shift_total_arm_minus_base": float((df.arm_total - df.base_total).mean()),
            "mean_shift_margin_arm_minus_base": float((df.arm_margin - df.base_margin).mean())}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pbp-dir", required=True)
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261112)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)
    t0 = time.time()
    eff = fit_train_effects(Path(a.pbp_dir))
    pbp = pd.read_parquet(PBP, columns=["game_id", "week", "season", "home_team", "away_team", "home_score",
                                         "away_score", "weather", "roof", "wind"])
    games = pbp.drop_duplicates("game_id")
    games = games[(games.season == 2026) & games.week.between(4, 9)].reset_index(drop=True)
    wx, inj = weather_specs(games), injury_specs(games)
    lines, lines_meta = load_lines(); close = close_for_games(lines)
    jobs = []
    for r in games.itertuples():
        w = wx[r.game_id]
        if w["on"]:
            jobs.append((r.game_id, r.home_team, r.away_team, int(r.week), "weather", a.n, a.seed, w))
        if inj[r.game_id]:
            jobs.append((r.game_id, r.home_team, r.away_team, int(r.week), "injury", a.n, a.seed, inj[r.game_id]))
    touched = sorted({j[0] for j in jobs})
    g_by = games.set_index("game_id")
    jobs += [(gid, g_by.loc[gid].home_team, g_by.loc[gid].away_team, int(g_by.loc[gid].week), "baseline", a.n, a.seed, None)
             for gid in touched]
    rows = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for res in ex.map(_sim, jobs):
            rows.append(res); print(res["arm"], res["game_id"], round(res["sim_total"], 2), round(res["p_home_win"], 3), flush=True)
    R = pd.DataFrame(rows)
    base = R[R.arm == "baseline"].set_index("game_id")
    ref = pd.read_csv(BASE_CSV); ref = ref[ref.arm == "new_off"].set_index("game_id")
    repro = {gid: bool(abs(base.loc[gid].sim_total - ref.loc[gid].sim_total) < 1e-3 and abs(base.loc[gid].p_home_win - ref.loc[gid].p_home_win) < 1e-3)
             for gid in base.index if gid in ref.index}
    act = {r.game_id: (int(r.home_score), int(r.away_score)) for r in games.itertuples()}
    rng = np.random.default_rng(BOOT_SEED)
    results = {}
    for arm in ("weather", "injury"):
        s = R[R.arm == arm].set_index("game_id")
        recs = []
        for gid, x in s.iterrows():
            c = close.get(gid) or {}
            if c.get("home_spread") is None or c.get("total") is None:
                continue
            h, aw = act[gid]
            recs.append({"game_id": gid, "act_margin": h - aw, "act_total": h + aw, "close_margin": -c["home_spread"],
                         "close_total": c["total"], "close_p": c.get("p_home_devig"),
                         "base_p": base.loc[gid].p_home_win, "arm_p": x.p_home_win, "base_margin": base.loc[gid].sim_margin,
                         "arm_margin": x.sim_margin, "base_total": base.loc[gid].sim_total, "arm_total": x.sim_total})
        df = pd.DataFrame(recs)
        results[arm] = compare(df, arm, rng)
        if arm == "injury":
            results[arm]["games_with_qb_out_kept_sparse"] = sorted(s[s.qb_kept_sparse.map(len) > 0].index.tolist())
            results[arm]["rows_removed_total"] = int(s.rows_removed.sum())
        else:
            results[arm]["per_game"] = {gid: {k: wx[gid][k] for k in ("tier", "rain", "wind_mph", "text")} |
                                        {"keep_completion": s.loc[gid].keep_completion, "ypc_factor": s.loc[gid].ypc_factor,
                                         "total_shift": float(s.loc[gid].sim_total - base.loc[gid].sim_total)} for gid in s.index}
    stem = f"weather_injury_backtest_wk04_09_n{a.n}"
    R.to_csv(OUT / f"{stem}_per_game.csv", index=False, float_format="%.4f")
    doc = {"label": "research only, not validated; BACKTEST on already-seen 2026 weeks 4-9 (not a clean holdout)",
           "generated_by": "calibration/weather_injury_backtest.py", "n_per_game": a.n, "seed_base": a.seed,
           "engine": engine_version(), "runtime_sec": round(time.time() - t0, 1),
           "weather_effects": {"path": TRAIN_EFFECTS, "seasons": eff["seasons"], "sha256": sha256(ROOT / TRAIN_EFFECTS),
                               "pooled_used": {m: eff["pooled"][m] for m in ("completion_pct", "yards_per_completion")}},
           "injuries": {"path": str(INJ.relative_to(ROOT)), "sha256": sha256(INJ), "pulled_utc": INJ_PULLED_UTC},
           "pbp": {"path": str(PBP.relative_to(ROOT)), "sha256": sha256(PBP)}, "lines": lines_meta,
           "baseline_reproduces_committed_csv": {"all": all(repro.values()), "n": len(repro),
                                                 "mismatches": [k for k, v in repro.items() if not v]},
           "bootstrap": {"B": B, "seed": BOOT_SEED}, "results": results}
    (OUT / f"{stem}.json").write_text(json.dumps(doc, indent=1, default=float) + "\n")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "per_game"} for k, v in results.items()}, indent=1, default=float))
    print("baseline reproduces committed csv:", doc["baseline_reproduces_committed_csv"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
