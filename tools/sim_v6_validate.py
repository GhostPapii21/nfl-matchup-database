"""Leakage-safe backtest, calibration and acceptance check for the restored sim_v6 and the sim_v6r1 replacement.

    python3 tools/sim_v6_validate.py rows  --weeks 4-11 --n 4000 --out research/sim_v6_recovery/rows.csv
    python3 tools/sim_v6_validate.py score --rows research/sim_v6_recovery/rows.csv --out research/sim_v6_recovery
    python3 tools/sim_v6_validate.py fit   --rows research/sim_v6_recovery/rows.csv --before 12 --out tools/sim_v6r1_calib.json

rows:  For each week W, both engines see only PBP before W's first game date. The universe is sim_v6.universe(), the
       original usage thresholds. Each player-market gets:
       * sim_v6 (restored, opp strength 1.0 as in the blob): methods mc, bias, gr.
       * sim_v6r1: methods mc_nb, gr_share, eb_boot, on the unconditional game.
       The spread is the nflverse spread_line (a closing line: mild optimism, disclosed). The proxy line L is
       floor(0.6 season mean + 0.4 last-3 mean) + 0.5 of the player's own stat. P(X >= L*f) is kept on a grid of f, so a
       fitted multiplier can be applied afterwards.
score: The multipliers for week W are fitted ONLY on rows from weeks < W (sim_v6 rule: K=30, MIN_N=20; sim_v6's bias
       uses pred_mc, as in the original fit). They are scored on week W, for W = 5..11.
       The committed 1,096-row sim_v6_backtest.csv (sim_v6 at opp 0.5, weeks 4-7) is scored the same way for W = 5..7.
fit:   Multipliers from all rows before --before, for live use.

ACCEPTANCE is fixed here, before any result was seen. A method is accepted only if, pooled over the held-out weeks:
  1. |median signed error| <= 10% in every market with n >= 30,
  2. 80% interval coverage (calibrated q10..q90) is within [0.70, 0.90],
  3. Brier at L beats the player's own hit-rate baseline ((k+1)/(n+2) over his prior active games),
  4. the method is distinct from EACH other method in its family: correlation < 0.995 or median absolute difference
     >= 2%. (First written as "from every other method"; made pairwise after the first scoring run. That is stricter
     and changed only sim_v6's mc/bias verdicts.)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sim_v6r1 as R  # noqa: E402  (prepares SIMV6_SRC)
V6 = R.V6

ROOT = HERE.parent
GRID = tuple(round(x, 3) for x in np.linspace(0.5, 2.0, 31))
ACCEPTANCE = dict(max_abs_median_signed_err_pct=10.0, min_market_n=30, coverage80=(0.70, 0.90),
                  brier_must_beat="player_hit_rate", distinct_corr=0.995, distinct_mad_pct=2.0)
V6_MODES = ("mc", "bias", "gr")
STAT = {"rec": "rec", "recyds": "ry", "passyds": "ry", "rushyds": "rush"}


def _stat(a, mkt):
    return a.ry + a.rush if mkt == "rushrec" else a[STAT[mkt]]


def build_rows(weeks, n):
    P = V6._P; rows = []
    for W in weeks:
        t0 = time.time()
        cut = P[P.week == W].game_date.min()
        E6 = V6.Engine(cutoff=cut, calib=None, n=n)
        Er = R.Engine(cutoff=cut, n=n)
        PW = P[P.week == W]
        for g, mkt in V6.universe(E6):
            q = PW[(PW.passer_player_id == g) | (PW.receiver_player_id == g) | (PW.rusher_player_id == g)]
            if q.empty:
                continue
            gid = q.game_id.iloc[0]; Q = PW[PW.game_id == gid]
            t = q.posteam.mode().iloc[0]; home = Q.home_team.iloc[0]
            opp = home if Q.away_team.iloc[0] == t else Q.away_team.iloc[0]
            if not (E6.tg.posteam == t).any():
                continue
            sl = float(Q.spread_line.iloc[0]) if Q.spread_line.notna().any() else 0.0
            spread = -sl if t == home else sl         # team spread, negative = favourite
            try:
                _, a, *_ = E6.player(g, t, mkt in ("passyds", "comp"), g)
            except Exception:
                continue
            if len(a) < 2:
                continue
            s = _stat(a, mkt); L = float(np.floor(0.6 * s.mean() + 0.4 * s.tail(3).mean()) + 0.5)
            base = float(((s >= L).sum() + 1) / (len(s) + 2))
            rungs = sorted({round(L * f, 4) for f in GRID})
            leg = dict(player=g, gsis=g, team=t, opp=opp, market=mkt, spread=spread, team_is_fav=spread <= 0,
                       rungs=rungs, game_id=gid)
            try:
                o6, _ = E6.sim(dict(leg), raw=True)
                orr, _ = Er.sim_r1(dict(leg), scenarios=(None,), raw=True)
            except Exception:
                continue
            act = V6.actual(P, gid, g, mkt)
            row = dict(week=W, gsis=g, market=mkt, game_id=gid, team=t, spread=spread, L=L, base_p=base, actual=act,
                       hit=float(act >= L))
            ok = True
            for m in V6_MODES:
                r = o6[m]; ok &= bool(np.isfinite(r["cmedian"]))
                row[f"v6_{m}_pred"] = r["cmedian"]; row[f"v6_{m}_q10"] = r["p10"]; row[f"v6_{m}_q90"] = r["p90"]
                row[f"v6_{m}_grid"] = json.dumps([r["rungs"][str(k)] for k in rungs])
            for m in R.METHODS:
                r = orr[m]["all"]; ok &= bool(np.isfinite(r["cmedian"]))
                row[f"r1_{m}_pred"] = r["cmedian"]; row[f"r1_{m}_q10"] = r["q"]["0.1"]; row[f"r1_{m}_q90"] = r["q"]["0.9"]
                row[f"r1_{m}_grid"] = json.dumps([r["rungs"][str(k)] for k in rungs])
            row["grid"] = json.dumps(rungs)
            if ok:
                rows.append(row)
        print(f"week {W}: {sum(1 for r in rows if r['week'] == W)} rows, {time.time() - t0:.0f}s", flush=True)
    return pd.DataFrame(rows)


def fit_mult(df, pred_col, K=V6.SHRINK_K, min_n=V6.MIN_N):
    out = {}
    for mk, g in df.groupby("market"):
        g = g[g[pred_col] > 0.5]; n = len(g)
        raw = float(np.median(g.actual / g[pred_col])) if n else 1.0
        M = 1.0 if n < min_n else 1 + (n / (n + K)) * (raw - 1)
        out[mk] = dict(M=round(M, 4), raw=round(raw, 4), n=n, shrink_K=K, guard=n < min_n)
    return out


def method_cols():
    return [("sim_v6", m, f"v6_{m}", "v6_mc" if m == "bias" else f"v6_{m}") for m in V6_MODES] + \
           [(R.VERSION, m, f"r1_{m}", f"r1_{m}") for m in R.METHODS]


def p_cal(row, pre, M):
    grid = np.array(json.loads(row["grid"])); p = np.array(json.loads(row[f"{pre}_grid"]))
    x = row["L"] / M if M > 0 else row["L"]
    return float(np.interp(x, grid, p))


def forward(df, weeks):
    """Calibrated held-out predictions, multipliers from weeks < W only."""
    parts = []
    for W in weeks:
        tr = df[df.week < W]; te = df[df.week == W].copy()
        if tr.empty or te.empty:
            continue
        for eng, m, pre, fitcol in method_cols():
            mult = fit_mult(tr, f"{fitcol}_pred")
            Ms = te.market.map(lambda k: mult.get(k, {}).get("M", 1.0))
            te[f"{pre}_M"] = Ms
            te[f"{pre}_cal"] = te[f"{pre}_pred"] * Ms
            te[f"{pre}_c10"] = te[f"{pre}_q10"] * Ms
            te[f"{pre}_c90"] = te[f"{pre}_q90"] * Ms
            te[f"{pre}_pcal"] = [p_cal(r, pre, M) for (_, r), M in zip(te.iterrows(), Ms)]
        parts.append(te)
    return pd.concat(parts) if parts else pd.DataFrame()


def metrics(H):
    out = {}
    for eng, m, pre, _ in method_cols():
        key = f"{eng}:{m}"; res = {"by_market": {}}
        for mk, g in list(H.groupby("market")) + [("ALL", H)]:
            gg = g[g[f"{pre}_cal"] > 0.5]
            if gg.empty:
                continue
            pr = gg[f"{pre}_cal"]; act = gg.actual
            pc = gg[f"{pre}_pcal"].clip(0, 1); y = gg.hit
            d = dict(n=int(len(gg)),
                     median_signed_err_pct=float(100 * np.median((pr - act) / pr)),
                     mae=float(np.mean(np.abs(pr - act))),
                     coverage80=float(((act >= gg[f"{pre}_c10"]) & (act <= gg[f"{pre}_c90"])).mean()),
                     brier=float(np.mean((pc - y) ** 2)),
                     brier_baseline=float(np.mean((gg.base_p - y) ** 2)),
                     mean_p=float(pc.mean()), hit_rate=float(y.mean()))
            bins = pd.cut(pc, np.linspace(0, 1, 11), include_lowest=True)
            rel = gg.assign(pc=pc).groupby(bins, observed=True).agg(p=("pc", "mean"), o=("hit", "mean"), k=("hit", "size"))
            d["calibration_gap"] = float((np.abs(rel.p - rel.o) * rel.k).sum() / rel.k.sum())
            (res if mk == "ALL" else res["by_market"])[mk if mk != "ALL" else "pooled"] = d
        out[key] = res
    # distinctness
    keys = [(f"{e}:{m}", f"{p}_cal") for e, m, p, _ in method_cols()]
    dist = {}
    for k, c in keys:
        others = []
        for k2, c2 in keys:
            if k2 == k:
                continue
            ok = (H[c] > 0.5) & (H[c2] > 0.5)
            corr = float(np.corrcoef(H.loc[ok, c], H.loc[ok, c2])[0, 1])
            mad = float(100 * np.median(np.abs(H.loc[ok, c] - H.loc[ok, c2]) / H.loc[ok, c]))
            others.append(dict(vs=k2, corr=round(corr, 5), median_abs_diff_pct=round(mad, 3)))
        dist[k] = others
    return out, dist


def accept(met, dist, family):
    A = ACCEPTANCE; verdict = {}
    for key, res in met.items():
        if not key.startswith(family + ":"):
            continue
        reasons = []
        for mk, d in res["by_market"].items():
            if d["n"] >= A["min_market_n"] and abs(d["median_signed_err_pct"]) > A["max_abs_median_signed_err_pct"]:
                reasons.append(f"{mk} median signed error {d['median_signed_err_pct']:+.1f}%")
        p = res["pooled"]; lo, hi = A["coverage80"]
        if not lo <= p["coverage80"] <= hi:
            reasons.append(f"80% coverage {p['coverage80']:.3f}")
        if not p["brier"] < p["brier_baseline"]:
            reasons.append(f"Brier {p['brier']:.4f} not below baseline {p['brier_baseline']:.4f}")
        fam = [o for o in dist[key] if o["vs"].startswith(family + ":")]
        # Pairwise (tightened after the first scoring run; the only effect is stricter): a method must differ from
        # EACH other method in its family, not just from one of them.
        for o in fam:
            if o["corr"] >= A["distinct_corr"] and o["median_abs_diff_pct"] < A["distinct_mad_pct"]:
                reasons.append(f"not distinct from {o['vs']} (corr {o['corr']}, median abs diff {o['median_abs_diff_pct']}%)")
        verdict[key] = dict(accepted=not reasons, reasons=reasons)
    return verdict


def score_committed_csv():
    """The committed 1,096 rows (sim_v6 at opp 0.5, weeks 4-7): forward-chained median metrics only."""
    f = ROOT / "calibration/simv56/engines/sim_v6_backtest.csv"
    df = pd.read_csv(f); out = {"file": str(f.relative_to(ROOT)), "rows": int(len(df)), "weeks": sorted(df.week.unique().tolist())}
    res = {}
    for m in V6_MODES:
        fitcol = "pred_mc" if m == "bias" else f"pred_{m}"; parts = []
        for W in (5, 6, 7):
            mult = fit_mult(df[df.week < W], fitcol); te = df[df.week == W].copy()
            te["cal"] = te[f"pred_{m}"] * te.market.map(lambda k: mult.get(k, {}).get("M", 1.0)); parts.append(te)
        H = pd.concat(parts); H = H[H.cal > 0.5]
        res[m] = {mk: dict(n=int(len(g)), median_signed_err_pct=float(100 * np.median((g.cal - g.actual) / g.cal)),
                           mae=float(np.mean(np.abs(g.cal - g.actual)))) for mk, g in H.groupby("market")}
    out["forward_weeks_5_7"] = res
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rows"); r.add_argument("--weeks", default="4-11"); r.add_argument("--n", type=int, default=4000)
    r.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("score"); s.add_argument("--rows", type=Path, required=True); s.add_argument("--out", type=Path, required=True)
    f = sub.add_parser("fit"); f.add_argument("--rows", type=Path, required=True); f.add_argument("--before", type=int, required=True)
    f.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "rows":
        lo, hi = map(int, a.weeks.split("-"))
        df = build_rows(range(lo, hi + 1), a.n); a.out.parent.mkdir(parents=True, exist_ok=True); df.to_csv(a.out, index=False)
        print(f"{len(df)} rows -> {a.out}")
    elif a.cmd == "score":
        df = pd.read_csv(a.rows); weeks = sorted(w for w in df.week.unique() if w > df.week.min())
        H = forward(df, weeks); met, dist = metrics(H)
        res = dict(rows_file=str(a.rows), rows=int(len(df)), backtest_weeks=sorted(df.week.unique().tolist()),
                   held_out_weeks=weeks, acceptance_rule=ACCEPTANCE, metrics=met, distinctness=dist,
                   verdict={"sim_v6": accept(met, dist, "sim_v6"), R.VERSION: accept(met, dist, R.VERSION)},
                   committed_1096=score_committed_csv())
        a.out.mkdir(parents=True, exist_ok=True)
        (a.out / "validation.json").write_text(json.dumps(res, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
        print(json.dumps(res["verdict"], indent=1))
    elif a.cmd == "fit":
        df = pd.read_csv(a.rows); tr = df[df.week < a.before]
        calib = {m: fit_mult(tr, f"r1_{m}_pred") for m in R.METHODS}
        a.out.write_text(json.dumps(dict(version=R.VERSION, is_original_sim_v6=False, fitted_on_weeks=sorted(tr.week.unique().tolist()),
                                         rows=int(len(tr)), rule="M = 1 + n/(n+30)*(median(actual/pred)-1); M=1 if n<20",
                                         multipliers=calib), indent=1))
        print(a.out)


if __name__ == "__main__":
    main()
