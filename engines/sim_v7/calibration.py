"""Chronological walk-forward backtest + Calibrated Bias fitting for sim_v7.

Phases (by kickoff date, never shuffled):
  train       2025 weeks 5-18     rows only ever used to fit
  validation  2026 weeks 3-7      walk-forward; selects the shrink constant K
  test        2026 weeks 8-11     walk-forward with the chosen K; this scorecard decides calibration_status
For week W every model input is built from plays with game_date < first kickoff of week W (no leakage), and the
recalibration map used to score week W is fitted only on rows from earlier weeks.
Games named in any *LOCK*.json file (frozen evaluation locks) are excluded from every phase.

Usage:
  python3 -m engines.sim_v7.calibration backtest --season 2025 --weeks 5-18 --out runs/.../bt_2025.csv
  python3 -m engines.sim_v7.calibration fit --rows a.csv b.csv --out engines/sim_v7/calibration_v7.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import data as D
from . import engine as E

GRID = np.linspace(0, 1, 101)
U_EVAL = np.arange(0.05, 0.951, 0.05)
KS = (10, 50, 200, 1000)
PHASES = {"train": (2025, range(5, 19)), "validation": (2026, range(3, 8)), "test": (2026, range(8, 12))}


def implied_from_schedule(row) -> dict | None:
    sl, tl = row.get("spread_line"), row.get("total_line")
    if sl != sl or tl != tl or sl is None or tl is None:
        return None
    # nflverse spread_line: positive = home favoured by that many points
    return {row["home_team"]: (tl + sl) / 2, row["away_team"]: (tl - sl) / 2}


def _pit(x, a, rng):
    lo, eq = float((x < a).mean()), float((x == a).mean())
    return lo + rng.random() * eq


def backtest(season: int, weeks, n: int = 2000, seed: int = 7, log=print) -> pd.DataFrame:
    P = D.load_pbp()
    sched = pd.read_csv(f"{D.REPO}/{D.GAMES_FILE}")
    locks = D.lock_game_ids()
    rows = []
    rng = np.random.default_rng(seed)
    for W in weeks:
        wk = P[(P.season == season) & (P.week == W)]
        if wk.empty:
            continue
        cutoff = wk.game_date.min()
        t0 = time.time()
        for gid in sorted(wk.game_id.unique()):
            if gid in locks:
                continue
            g = wk[wk.game_id == gid]
            home, away = g.home_team.iloc[0], g.away_team.iloc[0]
            s = sched[sched.game_id == gid]
            imp = implied_from_schedule(s.iloc[0].to_dict()) if len(s) else None
            try:
                ctxs = {t: D.team_context(t, cutoff) for t in (home, away)}
            except Exception as ex:
                log(f"skip {gid}: {ex}")
                continue
            plans = {t: E.mc_team_plan(ctxs[t], ctxs[[x for x in ctxs if x != t][0]], (imp or {}).get(t)) for t in ctxs}
            mc = E.mc_batch(ctxs, plans, n, np.random.default_rng(E.seed_for(seed, gid, "mc")))
            gr = E.gr_batch(ctxs, n, np.random.default_rng(E.seed_for(seed, gid, "gr")))
            act = D.actual_player_stats(gid)
            ag = D.actual_game(gid)
            fav = home if (imp and imp[home] >= imp[away]) or (not imp and plans[home]["implied"] >= plans[away]["implied"]) else away
            base = dict(season=season, week=W, game_id=gid, cutoff=cutoff, market_source="schedule" if imp else "derived")
            for t in (home, away):
                ctx = ctxs[t]
                for gs, st in E.stat_keys(ctx):
                    if gs not in act.index:
                        continue   # inactive / DNP: not settled
                    a = float(act.loc[gs, st])
                    x_mc, x_gr = mc[f"{gs}|{st}"].astype(float), gr[f"{gs}|{st}"].astype(float)
                    hist = ctx.pgame[ctx.pgame.gsis == gs]
                    hist = hist[(hist.tgt + hist.car + hist.att) > 0][st]
                    proxy = float(np.floor(hist.median()) + 0.5) if len(hist) else 0.5
                    rows.append(dict(base, team=t, player_id=gs, market=E.MARKET[st], actual=a, proxy_line=proxy,
                                     mc_pit=_pit(x_mc, a, rng), gr_pit=_pit(x_gr, a, rng),
                                     mc_q=json.dumps(np.round(np.quantile(x_mc, GRID), 2).tolist()),
                                     gr_q=json.dumps(np.round(np.quantile(x_gr, GRID), 2).tolist())))
                a = ag["home_pts"] if t == home else ag["away_pts"]
                x_mc, x_gr = mc[f"{t}|pts"].astype(float), gr[f"{t}|pts"].astype(float)
                rows.append(dict(base, team=t, player_id=t, market="team_points", actual=a,
                                 proxy_line=float(np.floor(ctx.games.pts.median()) + 0.5),
                                 mc_pit=_pit(x_mc, a, rng), gr_pit=_pit(x_gr, a, rng),
                                 mc_q=json.dumps(np.round(np.quantile(x_mc, GRID), 2).tolist()),
                                 gr_q=json.dumps(np.round(np.quantile(x_gr, GRID), 2).tolist())))
            dog = away if fav == home else home
            fm = ag["home_pts"] - ag["away_pts"] if fav == home else ag["away_pts"] - ag["home_pts"]
            for meth, b in (("mc", mc), ("gr", gr)):
                F = b[f"{fav}|pts"] - b[f"{dog}|pts"]
                rows.append(dict(base, team=fav, player_id=fav, market=f"fav_win_{meth}", actual=float(fm > 0) + 0.5 * (fm == 0),
                                 p_model=float((F > 0).mean() + 0.5 * (F == 0).mean())))
        log(f"{season} wk{W}: cutoff {cutoff}, rows {len(rows)}, {time.time()-t0:.1f}s")
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------- recalibration + scoring
def fit_ginv(pits: np.ndarray, K: float) -> np.ndarray:
    if len(pits) == 0:
        return GRID.copy()
    lam = len(pits) / (len(pits) + K)
    return np.clip(lam * np.quantile(pits, GRID) + (1 - lam) * GRID, 0, 1)


def _qf(qgrid, u):
    return np.interp(u, GRID, qgrid)


def _cdf(qgrid, x):
    q = np.asarray(qgrid)
    if x < q[0]:
        return 0.0
    if x >= q[-1]:
        return 1.0
    i = np.searchsorted(q, x, side="right")
    lo = np.searchsorted(q, x, side="left")
    return float(GRID[min(i, 100)] if i == lo else (GRID[lo] + GRID[min(i, 100)]) / 2)


def score_rows(df: pd.DataFrame, col: str, ginv: np.ndarray | None) -> dict:
    """MAE/bias of median, pinball-CRPS, Brier at proxy line, 80% coverage. ginv None = raw."""
    if df.empty:
        return {}
    mae, bias, crps, brier, cov, pover = [], [], [], [], [], []
    for qj, a, L in zip(df[col], df.actual, df.proxy_line):
        q = np.asarray(json.loads(qj))
        u = U_EVAL if ginv is None else np.interp(U_EVAL, GRID, ginv)
        qs = _qf(q, u)
        med = _qf(q, 0.5 if ginv is None else np.interp(0.5, GRID, ginv))
        mae.append(abs(med - a))
        bias.append(med - a)
        crps.append(np.mean([max(uu * (a - v), (uu - 1) * (a - v)) for uu, v in zip(U_EVAL, qs)]) * 2)
        Fr = _cdf(q, L)
        Fc = Fr if ginv is None else float(np.interp(Fr, ginv, GRID))
        p = 1 - Fc
        pover.append(p)
        brier.append((p - float(a > L)) ** 2)
        lo, hi = (_qf(q, 0.1), _qf(q, 0.9)) if ginv is None else (_qf(q, np.interp(0.1, GRID, ginv)), _qf(q, np.interp(0.9, GRID, ginv)))
        cov.append(float(lo <= a <= hi))
    pover, y = np.array(pover), (df.actual.values > df.proxy_line.values).astype(float)
    bins = np.clip((pover * 5).astype(int), 0, 4)
    rel = [dict(bin=f"{b/5:.1f}-{(b+1)/5:.1f}", n=int((bins == b).sum()), mean_p=round(float(pover[bins == b].mean()), 3),
                obs=round(float(y[bins == b].mean()), 3)) for b in range(5) if (bins == b).any()]
    return dict(n=len(df), mae=round(float(np.mean(mae)), 3), bias=round(float(np.mean(bias)), 3),
                crps=round(float(np.mean(crps)), 4), brier_proxy_line=round(float(np.mean(brier)), 4),
                coverage_80=round(float(np.mean(cov)), 3), reliability=rel)


def walk_forward(rows: pd.DataFrame, phase: str, K: float) -> dict:
    season, weeks = PHASES[phase]
    out = {}
    pr = rows[rows.mc_q.notna()]
    for mk in sorted(pr.market.unique()):
        m = pr[pr.market == mk]
        parts_raw, parts_cal, parts_gr = [], [], []
        for W in weeks:
            ev = m[(m.season == season) & (m.week == W)]
            if ev.empty:
                continue
            tr = m[m.cutoff < ev.cutoff.min()]
            g = fit_ginv(tr.mc_pit.values, K)
            parts_cal.append((ev, g))
        ev_all = pd.concat([e for e, _ in parts_cal]) if parts_cal else m.iloc[:0]
        raw = score_rows(ev_all, "mc_q", None)
        gr = score_rows(ev_all, "gr_q", None)
        # calibrated: score each week with its own walk-forward map, then pool
        cal_parts = [score_rows(e, "mc_q", g) for e, g in parts_cal]
        cal = {}
        if cal_parts:
            nn = sum(c["n"] for c in cal_parts)
            for k in ("mae", "bias", "crps", "brier_proxy_line", "coverage_80"):
                cal[k] = round(sum(c[k] * c["n"] for c in cal_parts) / nn, 4)
            cal["n"] = nn
        out[mk] = dict(mc_raw=raw, bias_calibrated=cal, gr=gr)
    return out


def game_brier(rows: pd.DataFrame, phase: str) -> dict:
    season, weeks = PHASES[phase]
    g = rows[rows.market.str.startswith("fav_win_") & (rows.season == season) & rows.week.isin(list(weeks))]
    return {mk: dict(n=int(len(x)), brier=round(float(((x.p_model - x.actual) ** 2).mean()), 4),
                     mean_p=round(float(x.p_model.mean()), 3), obs=round(float(x.actual.mean()), 3))
            for mk, x in g.groupby("market")}


def fit(rows: pd.DataFrame, final_cutoff: str) -> dict:
    pr = rows[rows.mc_q.notna()]
    # 1) validation: choose K by pooled walk-forward CRPS
    val = {K: walk_forward(rows, "validation", K) for K in KS}
    tot = {K: sum(v["bias_calibrated"].get("crps", 0) * v["bias_calibrated"].get("n", 0) for v in val[K].values()) for K in KS}
    K = min(tot, key=tot.get)
    test = walk_forward(rows, "test", K)
    markets = {}
    for mk in sorted(pr.market.unique()):
        tr = pr[(pr.market == mk) & (pr.cutoff < final_cutoff)]
        t = test.get(mk, {})
        raw, cal = t.get("mc_raw", {}), t.get("bias_calibrated", {})
        ok = bool(cal and raw and cal.get("n", 0) >= 50 and cal["crps"] < raw["crps"] and cal["brier_proxy_line"] <= raw["brier_proxy_line"])
        markets[mk] = dict(ginv=np.round(fit_ginv(tr.mc_pit.values, K), 5).tolist(), n_fit=int(len(tr)), K=K,
                           status="CALIBRATED_HOLDOUT_VALIDATED" if ok else "EXPERIMENTAL_UNVALIDATED",
                           test_scorecard=t)
    counts = {ph: int(((rows.season == s) & rows.week.isin(list(w)) & rows.mc_q.notna()).sum()) for ph, (s, w) in PHASES.items()}
    return dict(engine=E.ENGINE_VERSION, method="probabilistic recalibration of MC predictive (PIT quantile map), "
                "shrunk toward identity by n/(n+K)", as_of=datetime.now(timezone.utc).isoformat(),
                fit_cutoff=final_cutoff, phases={k: dict(season=s, weeks=[min(w), max(w)], rows=counts[k]) for k, (s, w) in PHASES.items()},
                excluded_lock_games=sorted(D.lock_game_ids()), K_selected=K, K_validation_crps=tot,
                holdout_scorecard=dict(as_of=final_cutoff, phase="test", markets=test,
                                       game_winner_brier=dict(validation=game_brier(rows, "validation"), test=game_brier(rows, "test"))),
                provenance=D.provenance(), markets=markets)


def relevant(rows: pd.DataFrame) -> pd.DataFrame:
    """Drop structural zeros using pre-game information only: rows whose MC P90 is 0 (e.g. carries for a WR
    with no rushing role). Selection never looks at the actual outcome."""
    q90 = rows.mc_q.map(lambda q: json.loads(q)[90] if isinstance(q, str) else np.nan)
    return rows[rows.mc_q.isna() | (q90 > 0)].reset_index(drop=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("backtest")
    b.add_argument("--season", type=int, required=True)
    b.add_argument("--weeks", required=True)
    b.add_argument("--n", type=int, default=2000)
    b.add_argument("--out", required=True)
    f = sp.add_parser("fit")
    f.add_argument("--rows", nargs="+", required=True)
    f.add_argument("--cutoff", default="2026-11-24")
    f.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "backtest":
        lo, hi = map(int, a.weeks.split("-"))
        df = backtest(a.season, range(lo, hi + 1), n=a.n, log=lambda m: print(m, flush=True))
        df.to_csv(a.out, index=False)
        print(f"wrote {len(df)} rows -> {a.out}")
    else:
        rows = pd.concat([pd.read_csv(r) for r in a.rows], ignore_index=True)
        rows = relevant(rows)
        art = fit(rows, a.cutoff)
        json.dump(art, open(a.out, "w"), indent=1, default=float)
        print(json.dumps({k: v["status"] for k, v in art["markets"].items()}, indent=1))
        print("K", art["K_selected"], "phases", art["phases"])


if __name__ == "__main__":
    sys.exit(main())
