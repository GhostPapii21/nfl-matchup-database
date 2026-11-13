"""NFL-75 item 5: chronological walk-forward backtest of fixed vs fitted dispersion, 2026 weeks 4-9. Research only.

    python3 -m market_calibration.backtest_dispersion_wk04_09 --pbp-dir <nflverse pbp folder> --players <players.parquet>

For each test week w in 4..9 the fit uses 2018..2025 + 2026 weeks 1..w-1 only, is frozen, and is scored on week w.
Weeks >= 10 are refused (reserved live holdout).

Game level (88 games): centres are (a) the engine's walk-forward mean margin/total from
calibration/outputs/backtest_after_wp12_n2000_per_game.csv (main engine, adjustments off) and (b) the close.
Only the SD changes between arms, so margin/total MAE are identical by construction (reported anyway).
Probabilities: P(home win)=P(N(m,sd)>0); P(over close total); P(home covers close spread). Pushes/ties excluded.
Player level: 2026 week-w player-games with a trailing mean (proxy line). Thresholds 0.5x / 0.75x / 1.0x trailing mean
(rounded down to x.5). Both arms use the same fitted p0 and median ratio; only sigma differs (isolates the sigma).
Metrics: Brier, ECE (10 equal-width bins), n, bootstrap 95% CI (2,000 resamples by game / by player-game, seed fixed).
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm, lognorm

from market_calibration import fit_dispersion_nflverse as F
from market_calibration import fitted_dispersion as D

ROOT = Path(__file__).resolve().parents[1]
ENGINE_CSV = ROOT / "calibration/outputs/backtest_after_wp12_n2000_per_game.csv"
OUT = Path(__file__).parent / "fitted/backtest_dispersion_wk04_09.json"
WEEKS = range(4, 10)
B, SEED = 2000, 20261113


def brier(p, y):
    return float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))


def ece(p, y, bins=10):
    p, y = np.asarray(p, float), np.asarray(y, float)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    return float(sum(abs(p[idx == b].mean() - y[idx == b].mean()) * (idx == b).sum() for b in range(bins) if (idx == b).any()) / len(p))


def boot(p0, p1, y, rng):
    p0, p1, y = map(lambda a: np.asarray(a, float), (p0, p1, y))
    n = len(y); i = rng.integers(0, n, size=(B, n))
    b0 = ((p0[i] - y[i]) ** 2).mean(1); b1 = ((p1[i] - y[i]) ** 2).mean(1)
    q = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    return {"before_ci95": q(b0), "after_ci95": q(b1), "diff_after_minus_before": float(brier(p1, y) - brier(p0, y)),
            "diff_ci95": q(b1 - b0)}


def score(name, p0, p1, y, rng):
    return {"market": name, "n": int(len(y)), "brier_before": brier(p0, y), "brier_after": brier(p1, y),
            "ece_before": ece(p0, y), "ece_after": ece(p1, y), **boot(p0, p1, y, rng)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pbp-dir", required=True)
    ap.add_argument("--players", required=True)
    a = ap.parse_args(argv)
    pbp, meta = F.load_pbp(Path(a.pbp_dir))
    players = pd.read_parquet(a.players, columns=["gsis_id", "position"])
    games, pg = F.game_table(pbp), F.player_games(pbp, players)
    from calibration.backtest import load_lines, close_for_games
    lines, lines_meta = load_lines()
    close = close_for_games(lines)
    eng = pd.read_csv(ENGINE_CSV)
    eng = eng[eng.arm == "new_off"].set_index("game_id")
    rows, prow, fits = [], [], {}
    for w in WEEKS:
        fit = F.fit(games, pg, 2026, w - 1)          # frozen before week w
        fits[w] = {"margin": {k: round(v["sd"], 3) for k, v in fit["margin_sd_by_abs_spread"]["values"].items()},
                   "total": {k: round(v["sd"], 3) for k, v in fit["total_sd_by_total_line"]["values"].items()}}
        for gid, e in eng[eng.week == w].iterrows():
            c = close.get(gid) or {}
            if c.get("home_spread") is None or c.get("total") is None:
                continue
            cm, ct = -c["home_spread"], c["total"]
            r = {"game_id": gid, "week": w, "act_margin": e.act_margin, "act_total": e.act_total,
                 "sim_margin": e.sim_margin, "sim_total": e.sim_total, "close_margin": cm, "close_total": ct,
                 "close_p_home": c.get("p_home_devig"), "engine_p_home": e.p_home_win}
            for arm, mode in (("before", D.FIXED), ("after", D.FITTED)):
                sm, stt = D.margin_sd(abs(cm), mode, fit), D.total_sd(ct, mode, fit)
                r[f"sd_m_{arm}"], r[f"sd_t_{arm}"] = sm, stt
                r[f"pwin_eng_{arm}"] = 1 - norm.cdf(0, e.sim_margin, sm)
                r[f"pover_eng_{arm}"] = 1 - norm.cdf(ct, e.sim_total, stt)
                r[f"pcov_eng_{arm}"] = 1 - norm.cdf(cm, e.sim_margin, sm)  # P(margin > close margin)
                r[f"pwin_close_{arm}"] = 1 - norm.cdf(0, cm, sm)
            rows.append(r)
        test = pg[(pg.season == 2026) & (pg.week == w) & pg.trail_mean.notna() & (pg.trail_mean > 0)]
        for t in test.itertuples():
            key = f"{t.stat}:{t.pos}"
            if key not in D.FIXED_VALUES["yard_sigma"]:
                continue
            cell = D.yard_cell(t.stat, t.pos, t.trail_mean, fit)
            if cell["sigma"] is None:
                continue
            med = t.trail_mean * cell["med_ratio"]
            for mult in (0.5, 0.75, 1.0):
                thr = math.floor(t.trail_mean * mult) + 0.5
                pr = {"key": key, "week": w, "mult": mult, "y": float(t.yards >= thr), "pid": t.pid}
                for arm, sig in (("before", D.FIXED_VALUES["yard_sigma"][key]), ("after", cell["sigma"])):
                    pr[arm] = (1 - cell["p0"]) * (1 - lognorm.cdf(thr, sig, scale=med))
                prow.append(pr)
    g = pd.DataFrame(rows); p = pd.DataFrame(prow)
    rng = np.random.default_rng(SEED)
    dec = g[g.act_margin != 0]
    ov = g[g.act_total != g.close_total]
    cv = g[g.act_margin != g.close_margin]
    game = [score("home_win | engine centre", dec.pwin_eng_before, dec.pwin_eng_after, (dec.act_margin > 0).astype(float), rng),
            score("over close total | engine centre", ov.pover_eng_before, ov.pover_eng_after, (ov.act_total > ov.close_total).astype(float), rng),
            score("home cover close spread | engine centre", cv.pcov_eng_before, cv.pcov_eng_after, (cv.act_margin > cv.close_margin).astype(float), rng),
            score("home_win | close centre", dec.pwin_close_before, dec.pwin_close_after, (dec.act_margin > 0).astype(float), rng)]
    ref = {"brier_close_devig_moneyline": brier(dec.close_p_home, (dec.act_margin > 0).astype(float)),
           "ece_close_devig_moneyline": ece(dec.close_p_home, (dec.act_margin > 0).astype(float)),
           "brier_engine_sim_p_home": brier(dec.engine_p_home, (dec.act_margin > 0).astype(float)),
           "n_decided": int(len(dec)),
           "mae_margin_engine": float((g.sim_margin - g.act_margin).abs().mean()),
           "mae_total_engine": float((g.sim_total - g.act_total).abs().mean()),
           "mae_margin_close": float((g.close_margin - g.act_margin).abs().mean()),
           "mae_total_close": float((g.close_total - g.act_total).abs().mean()),
           "note": "MAE does not depend on the SD; identical before/after by construction"}
    props = []
    for (key, mult), s in p.groupby(["key", "mult"]):
        props.append({**score(f"{key} >= {mult}x trailing mean", s.before, s.after, s.y, rng), "key": key, "mult": mult})
    for key, s in p.groupby("key"):
        props.append({**score(f"{key} all thresholds", s.before, s.after, s.y, rng), "key": key, "mult": "all"})
    doc = {"label": "research only, not validated; BACKTEST on already-seen 2026 weeks 4-9 (walk-forward fit, frozen per week)",
           "generated_by": "market_calibration/backtest_dispersion_wk04_09.py", "weeks": list(WEEKS),
           "fit_rule": "fit on 2018..2025 + 2026 weeks 1..w-1, frozen, scored on week w", "bootstrap": {"B": B, "seed": SEED},
           "engine_centres": {"path": str(ENGINE_CSV.relative_to(ROOT)), "sha256": F.sha256(ENGINE_CSV)},
           "lines": lines_meta, "sources": meta, "games_scored": int(len(g)),
           "fits_by_test_week": fits, "game_level": game, "game_reference": ref, "player_level": props}
    OUT.write_text(json.dumps(doc, indent=1, default=float) + "\n")
    for s in game + props:
        print(f"{s['market']:<45} n={s['n']:<5} brier {s['brier_before']:.4f} -> {s['brier_after']:.4f} "
              f"(diff {s['diff_after_minus_before']:+.4f} CI {s['diff_ci95'][0]:+.4f},{s['diff_ci95'][1]:+.4f}) "
              f"ECE {s['ece_before']:.3f} -> {s['ece_after']:.3f}")
    print(json.dumps(ref, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
