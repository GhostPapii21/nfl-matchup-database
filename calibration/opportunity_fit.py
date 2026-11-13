"""NFL-75 Phase 2: fit the player OPPORTUNITY model (core/possession_engine_v0/opportunity.py) point in time.

Everything here is fitted on data strictly BEFORE the eval week and frozen before scoring:
  * share model (per slot: dropback / carry / target), per team-game:
        r_p  = sum_g lam^age_g * c_pg / sum_g lam^age_g * T_g      over the games g the player played this season
        base = r_p^gamma normalised to (1 - u), UNLISTED gets u
        candidates: players with >= 1 slot row for the team this season, last seen <= K team games ago (unless every
        missed game since was an injury-report Out/Doubtful); Out players stay in the list with avail 0 so their share
        is redistributed by opportunity.redistribute(alpha) inside the sim; Questionable / Doubtful play with the
        fitted probability for their status.
    (lam, gamma, K, alpha) by grid search on multinomial log loss, then the Dirichlet concentration kappa by
    Dirichlet-multinomial likelihood, on team-games of 2024, 2025 and 2026 weeks < eval week.
  * per-player feature distributions with empirical-Bayes shrinkage toward the position prior (prior strength m by
    held-out log likelihood of the last pre-eval week), from 2024-2025 + 2026 weeks < eval week.
"played" in a history game = the player had any offensive opportunity in it, or he was not Out/Doubtful that week and
had opportunities for the team both before and after it (bracketed). No snap counts are used (nflverse snap counts in
the repo stop at 2026 Week 7, so snaps are unknown for the model).
Point in time: injury status is the nflverse weekly report status for the eval week (a pregame publication); game-day
inactives are NOT used (not available point in time in the data we hold). No week >= the eval week is ever read for
fitting. Weeks >= 10 are refused for scoring.
Research only. projection_ready stays false."""
from __future__ import annotations
import hashlib
import json
import math
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "core/possession_engine_v0"
NFLV = ROOT / "data/historical/nflverse"
PBP_2026 = NFLV / "pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PBP_DIR = Path(os.environ.get("NFLVERSE_PBP_DIR", "/tmp/nflverse_pbp"))
SOURCES = {
    "pbp_2024": {"path": NFLV / "play_by_play_2024.parquet",
                 "sha256": "3fd2896bc0b911b615142d2f1fabae54a4bbba5ab7b73b28187b118ef8af6a3b"},
    "pbp_2025": {"path": PBP_DIR / "play_by_play_2025.parquet",
                 "sha256": "c6ecedd6d678cc37ed316b23ef84ee1ec6abb69c514bb11868a7ebd5a367df29",
                 "url": "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2025.parquet",
                 "retrieved_utc": "2026-11-13T05:25:07Z", "committed": False},
    "pbp_2026": {"path": PBP_2026, "sha256": "1028614beb746bea596633bb2215948d19ddcc34f8928e74a3338635122ec5b8"},
    "inj_2024": {"path": NFLV / "injuries/injuries_2024_pulled_20261113T0717Z.parquet",
                 "sha256": "7ebabbba930a70bc7e4d257c7c41ca8708f147a4cdd4100956abcfbaf70f7fc1"},
    "inj_2025": {"path": NFLV / "injuries_2025.parquet",
                 "sha256": "c7637c2f6347194426a8582a984aac82a6bf8ab06af72cdd96666a2e0733ab24"},
    "inj_2026": {"path": NFLV / "injuries/injuries_2026_pulled_20261113T0526Z.parquet",
                 "sha256": "a72cc1afc7224baf6cafdc81950d807fd603ee9c02e7348b38151fcc1af8fa36",
                 "retrieved_utc": "2026-11-13T05:26:36Z (00:26 AM ET Nov 13, AFTER the Nov 12 TNF kickoff)",
                 "publication_time": "UNKNOWN (the nflverse file carries no per-row publication timestamp)",
                 "provenance_gap": "its Week 10 rows feed the WAS@NYG sanity model (e.g. C.Yankoff Out); pregame "
                                   "publication of those statuses is assumed, not proven"},
    "depth_qb1": {"path": NFLV / "derived_pit/depth_qb1_snapshots_2025_2026.csv",
                  "sha256": "c1ab52498fad542f62677e02977494a9283e4e3d78e6d2eb08a3344b0068d5d2",
                  "use": "point-in-time QB1 (latest snapshot before 04:00 UTC of game day); see derived_pit/README.md"},
    "games": {"path": NFLV / "games.csv", "sha256": "c606cb6cdf94d6a1c1e939e23ed524223dc7aeaa01a4e2982b0cb5db42bae017",
              "use": "game day per (season, week, team) only", "committed": "d9779a1 (2026-11-11 10:07 AM ET)"},
    "players": {"path": PBP_DIR / "players.parquet",
                "sha256": "4f885ccfeb4853f3cde70b1507c3349fb843bd8a54047dc940e89050ee313342",
                "url": "https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet",
                "retrieved_utc": "2026-11-13T05:26:36Z", "committed": False,
                "use": "position only (gsis_id -> position); latest_team/status are NOT read (post-date info)",
                "provenance_gap": "position is the CURRENT snapshot (retrieved 2026-11-13), not point in time"},
}
SLOTS = ("dropback", "carry", "target")
HOLDOUT_FIRST_WEEK = 10
GRID = {"lam": (0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 1.0), "gamma": (0.75, 1.0, 1.5, 2.0, 3.0, 5.0), "K": (0, 1, 2, 3, 99),
        "alpha": (0.0, 0.5, 0.8, 1.0)}
KAPPA_GRID = (0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 80.0, 160.0, 400.0, 1000.0)
M_GRID = (2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0, 5000.0)
STATUS_OUT = "Out"
COLS = ["season", "season_type", "week", "game_id", "play_id", "posteam", "play_type", "yardline_100", "yards_gained",
        "air_yards", "complete_pass", "interception", "fumble_lost", "sack", "qb_scramble", "two_point_attempt",
        "pass_touchdown", "rush_touchdown", "passer_player_id", "passer_player_name", "receiver_player_id",
        "receiver_player_name", "rusher_player_id", "rusher_player_name"]


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verify_sources(keys=None) -> dict:
    out = {}
    for k, v in SOURCES.items():
        if keys is not None and k not in keys:
            continue
        p = Path(v["path"])
        h = sha256(p) if p.exists() else None
        if h != v["sha256"]:
            raise RuntimeError(f"{k}: sha256 mismatch or missing ({p}): {h}")
        out[k] = {kk: (str(vv) if isinstance(vv, Path) else vv) for kk, vv in v.items()}
        out[k]["path"] = str(p.relative_to(ROOT)) if str(p).startswith(str(ROOT)) else str(p)
    return out


@lru_cache(maxsize=1)
def positions() -> dict:
    pl = pd.read_parquet(SOURCES["players"]["path"], columns=["gsis_id", "position"])
    return {r.gsis_id: (r.position or "UNK") for r in pl.itertuples() if isinstance(r.gsis_id, str)}


def group(pos) -> str:
    return {"QB": "QB", "RB": "RB", "FB": "RB", "HB": "RB", "WR": "WR", "TE": "TE"}.get(str(pos), "OTH")


def _feat_mod():
    import sys
    if str(ENGINE) not in sys.path:
        sys.path.insert(0, str(ENGINE))
    import opportunity
    return opportunity


@lru_cache(maxsize=4)
def load_pbp(season: int) -> pd.DataFrame:
    p = SOURCES[f"pbp_{season}"]["path"]
    import pyarrow.parquet as pq
    have = set(pq.ParquetFile(p).schema_arrow.names)
    df = pd.read_parquet(p, columns=[c for c in COLS if c in have])
    df = df[(df["season_type"] == "REG") & df["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])]
    df = df[df["two_point_attempt"].fillna(0) != 1].copy()
    df["season"] = int(season)
    return df


@lru_cache(maxsize=4)
def opp_rows(season: int) -> pd.DataFrame:
    """One row per (play, slot) with player id/name and feature cell (historical zone/yards/result)."""
    om = _feat_mod()
    df = load_pbp(season)
    pos = positions()
    out = []
    for r in df.itertuples(index=False):
        y0 = r.yardline_100 if r.yardline_100 == r.yardline_100 else 50
        yds = r.yards_gained if r.yards_gained == r.yards_gained else 0.0
        is_int = r.interception == 1
        base = (r.season, r.week, r.game_id, r.posteam)
        if r.play_type == "pass":
            comp = r.complete_pass == 1
            td = r.pass_touchdown == 1
            if r.sack == 1:
                kind = "sack"
            else:
                kind = "int" if is_int else ("td" if td else ("comp" if comp else "inc"))
            out.append(base + ("dropback", r.passer_player_id, r.passer_player_name, om.feat_dropback(y0, kind)))
            if r.sack != 1 and (isinstance(r.receiver_player_id, str) or comp):
                out.append(base + ("target", r.receiver_player_id, r.receiver_player_name,
                                   om.feat_target(y0, r.air_yards, comp, td, is_int)))
        elif r.play_type == "run":
            qb_run = r.qb_scramble == 1 or pos.get(r.rusher_player_id) == "QB"
            if qb_run:
                out.append(base + ("dropback", r.rusher_player_id, r.rusher_player_name, om.feat_dropback(y0, "run")))
            else:
                out.append(base + ("carry", r.rusher_player_id, r.rusher_player_name,
                                   om.feat_carry(y0, yds, r.rush_touchdown == 1)))
        elif r.play_type == "qb_kneel":
            out.append(base + ("dropback", r.rusher_player_id, r.rusher_player_name, None))
        elif r.play_type == "qb_spike":
            out.append(base + ("dropback", r.passer_player_id, r.passer_player_name, None))
    o = pd.DataFrame(out, columns=["season", "week", "game_id", "team", "slot", "pid", "name", "feat"])
    o["pid"] = o["pid"].where(o["pid"].map(lambda x: isinstance(x, str)), None)
    return o


@lru_cache(maxsize=4)
def injuries(season: int) -> pd.DataFrame:
    i = pd.read_parquet(SOURCES[f"inj_{season}"]["path"])
    i = i[i["game_type"] == "REG"] if "game_type" in i.columns else i
    return i[["season", "week", "team", "gsis_id", "report_status"]].copy()


def status_map(season: int, week: int) -> dict:
    """(team, gsis_id) -> report_status for that week's (pregame) report."""
    i = injuries(season)
    i = i[(i["week"] == week) & i["report_status"].notna()]
    return {(r.team, r.gsis_id): r.report_status for r in i.itertuples()}


# ------------------------------------------------------------------ share model
@lru_cache(maxsize=8)
def _season_tables(season: int):
    """counts[(team, slot)] -> (weeks list, {pid: np.array per week}), totals, any-opp presence, names."""
    o = opp_rows(season)
    tables = {}
    for (team, slot), g in o.groupby(["team", "slot"]):
        tables[(team, slot)] = g
    weeks_by_team = {t: sorted(g["week"].unique().tolist()) for t, g in o.groupby("team")}
    presence = {t: {w: set(gw["pid"].dropna()) for w, gw in g.groupby("week")} for t, g in o.groupby("team")}
    names = {}
    for (t, pid), g in o.dropna(subset=["pid"]).groupby(["team", "pid"]):
        names[(t, pid)] = g["name"].mode().iat[0]
    return tables, weeks_by_team, presence, names


@lru_cache(maxsize=None)
def team_game_inputs(season: int, team: str, week: int, slot: str) -> dict | None:
    """Raw point-in-time inputs for one team-game and slot (weeks < week only) + actual counts at week (or None)."""
    tables, wbt, presence, names = _season_tables(season)
    weeks = [w for w in wbt.get(team, []) if w < week]
    if not weeks:
        return None
    g = tables.get((team, slot))
    if g is None:
        return None
    hist = g[g["week"] < week]
    pids = sorted(set(hist["pid"].dropna()))
    W = len(weeks)
    widx = {w: j for j, w in enumerate(weeks)}
    C = np.zeros((len(pids), W))
    T = np.zeros(W)
    for w, gw in hist.groupby("week"):
        T[widx[w]] = len(gw)
        vc = gw["pid"].value_counts()
        for j, pid in enumerate(pids):
            C[j, widx[w]] = vc.get(pid, 0)
    pres = np.zeros((len(pids), W), dtype=bool)
    st_hist = np.zeros((len(pids), W), dtype=bool)  # Out/Doubtful that week
    for w in weeks:
        sm = status_map(season, w)
        for j, pid in enumerate(pids):
            pres[j, widx[w]] = pid in presence[team].get(w, set())
            st_hist[j, widx[w]] = sm.get((team, pid)) in ("Out", "Doubtful")
    sm_now = status_map(season, week)
    status = [sm_now.get((team, pid)) for pid in pids]
    pos = positions()
    actual = None
    cur = g[g["week"] == week]
    if week in wbt.get(team, []):
        vc = cur["pid"].value_counts()
        actual = {"by_pid": {pid: int(vc.get(pid, 0)) for pid in pids}, "total": int(len(cur)),
                  "unlisted": int(len(cur) - sum(vc.get(pid, 0) for pid in pids))}
    return {"season": season, "team": team, "week": week, "slot": slot, "weeks": weeks, "pids": pids,
            "names": [names.get((team, p), p) for p in pids], "pos": [pos.get(p, "UNK") for p in pids],
            "C": C, "T": T, "pres": pres, "st_hist": st_hist, "status": status, "actual": actual}


def played_matrix(inp) -> np.ndarray:
    if "_played" in inp:
        return inp["_played"]
    pres, st = inp["pres"], inp["st_hist"]
    W = pres.shape[1]
    out = pres.copy()
    for j in range(pres.shape[0]):
        idx = np.where(pres[j])[0]
        if len(idx):
            lo, hi = idx.min(), idx.max()
            for k in range(lo, hi + 1):
                if not pres[j, k] and not st[j, k]:
                    out[j, k] = True
    inp["_played"] = out
    return out


def base_shares(inp, lam: float, gamma: float, K: int, u: float):
    """-> (keep mask, base share vector over kept candidates + UNLISTED at the end)."""
    C, T = inp["C"], inp["T"]
    W = len(inp["weeks"])
    age = np.arange(W)[::-1].astype(float)  # most recent game age 0
    w = lam ** age
    pl = played_matrix(inp)
    num = (C * w).sum(1)
    den = (pl * (T * w)).sum(1)
    r = np.where(den > 0, num / np.maximum(den, 1e-12), 0.0)
    pres = inp["pres"]
    keep = np.zeros(len(r), dtype=bool)
    for j in range(len(r)):
        idx = np.where(pres[j])[0]
        if not len(idx):
            continue
        gap = W - 1 - idx.max()  # team games since last seen
        if gap <= K or all(inp["st_hist"][j, idx.max() + 1:]):
            keep[j] = r[j] > 0
    s = np.where(keep, r, 0.0) ** gamma
    s = np.where(keep, s, 0.0)
    if s.sum() > 0:
        s = s / s.sum() * (1 - u)
        return keep, np.append(s[keep], u)
    return keep, np.array([1.0])


def predict(inp, lam, gamma, K, alpha, u, p_q=1.0, p_d=0.0, expected=True):
    """Expected share vector after availability (Out removed; Q/D at their fitted play probability in expectation is
    approximated by Q=in, D=out for fitting; the sim draws them)."""
    om = _feat_mod()
    keep, s = base_shares(inp, lam, gamma, K, u)
    st = [inp["status"][j] for j in np.where(keep)[0]] + [None]
    pos = [inp["pos"][j] for j in np.where(keep)[0]] + [om.UNLISTED]
    out = np.array([x in ("Out", "Doubtful") for x in st])
    return keep, om.redistribute(s, pos, out, alpha)


def _ll(inp, keep, pred):
    a = inp["actual"]
    cnt = np.array([a["by_pid"][p] for j, p in enumerate(inp["pids"]) if keep[j]] + [a["total"] - sum(
        a["by_pid"][p] for j, p in enumerate(inp["pids"]) if keep[j])], dtype=float)
    pr = np.clip(pred, 1e-4, 1)
    pr = pr / pr.sum()
    return float((cnt * np.log(pr)).sum()), cnt


def train_set(eval_season: int, eval_week: int, slot: str, seasons=(2024, 2025)) -> list:
    out = []
    for s in seasons:
        if s >= eval_season:
            continue
        for team in sorted(_season_tables(s)[1]):
            for w in _season_tables(s)[1][team]:
                if w >= 3:
                    x = team_game_inputs(s, team, w, slot)
                    if x is not None and x["actual"] and x["actual"]["total"] > 0:
                        out.append(x)
    tb = _season_tables(eval_season)[1]
    for team in sorted(tb):
        for w in tb[team]:
            if 3 <= w < eval_week:
                x = team_game_inputs(eval_season, team, w, slot)
                if x is not None and x["actual"] and x["actual"]["total"] > 0:
                    out.append(x)
    for x in out:  # leakage guard
        if x["season"] == eval_season and (x["week"] >= eval_week or max(x["weeks"]) >= eval_week):
            raise RuntimeError("train set reads the eval week or later")
    return out


def _u_for(train, lam, gamma, K):
    num = den = 0.0
    for x in train:
        keep, _ = base_shares(x, lam, gamma, K, 0.0)
        a = x["actual"]
        listed = sum(a["by_pid"][p] for j, p in enumerate(x["pids"]) if keep[j])
        num += a["total"] - listed
        den += a["total"]
    return min(max(num / den, 1e-3), 0.5) if den else 0.05


def _dm_ll(preds, kappas) -> np.ndarray:
    """Dirichlet-multinomial log likelihood (up to the multinomial coefficient) for each kappa."""
    from scipy.special import gammaln
    pr = np.concatenate([p for p, _ in preds])
    c = np.concatenate([q for _, q in preds])
    seg = np.repeat(np.arange(len(preds)), [len(p) for p, _ in preds])
    n = np.array([q.sum() for _, q in preds])
    out = []
    for k in kappas:
        a = k * pr
        per = np.bincount(seg, weights=gammaln(c + a) - gammaln(a), minlength=len(preds))
        out.append(float((gammaln(k) - gammaln(n + k) + per).sum()))
    return np.array(out)


def _preds(train, lam, gamma, K, alpha, u):
    out = []
    for x in train:
        keep, pr = predict(x, lam, gamma, K, alpha, u)
        _, cnt = _ll(x, keep, pr)
        pr = np.clip(pr, 1e-4, 1)
        out.append((pr / pr.sum(), cnt))
    return out


def fit_slot(train: list) -> dict:
    """Joint fit of (lam, gamma, K, alpha, kappa) by Dirichlet-multinomial likelihood of each team-game's actual
    counts (kappa profiled over KAPPA_GRID). The DM accounts for within-game correlation (e.g. a QB change moves a
    whole game's dropbacks at once), which a plain multinomial log loss would treat as independent snaps."""
    kap = np.array(KAPPA_GRID)
    best = None
    a0 = 0.5
    for lam in GRID["lam"]:
        for K in GRID["K"]:
            for gamma in GRID["gamma"]:
                u = _u_for(train, lam, gamma, K)
                ll = _dm_ll(_preds(train, lam, gamma, K, a0, u), kap)
                j = int(np.argmax(ll))
                if best is None or ll[j] > best[0]:
                    best = (float(ll[j]), lam, gamma, K, u)
    _, lam, gamma, K, u = best
    lla = {a: _dm_ll(_preds(train, lam, gamma, K, a, u), kap) for a in GRID["alpha"]}
    best_a = max(lla, key=lambda a: lla[a].max())
    ll = lla[best_a]
    kappa = float(kap[int(np.argmax(ll))])
    edges = {"lam": lam in (GRID["lam"][0], GRID["lam"][-1]), "gamma": gamma in (GRID["gamma"][0], GRID["gamma"][-1]),
             "K": K in (GRID["K"][0], GRID["K"][-1]), "kappa": kappa in (KAPPA_GRID[0], KAPPA_GRID[-1])}
    return {"lam": lam, "gamma": gamma, "K": int(K), "alpha": best_a, "u": u, "kappa": kappa,
            "objective": "dirichlet_multinomial", "train_team_games": len(train), "train_dm_ll": float(ll.max()),
            "at_grid_edge": edges}


STARTER_GRID = {"lam": (0.2, 0.35, 0.5, 0.65, 0.8, 1.0), "K": (0, 1, 2, 99), "start_gamma": (0.5, 1.0, 2.0, 3.0),
                "rho": (0.9, 0.95, 0.975, 0.99),
                "beta_last": (0.0, 1.0, 2.0, 3.0), "beta_dc": (0.0, 1.0, 2.0, 3.0, 4.0, 6.0)}


@lru_cache(maxsize=1)
def _depth():
    d = pd.read_csv(SOURCES["depth_qb1"]["path"], dtype={"gsis_id": str})
    return {k: g.sort_values("dt") for k, g in d.groupby(["season", "team"])}


@lru_cache(maxsize=1)
def _gamedays():
    g = pd.read_csv(SOURCES["games"]["path"], usecols=["season", "week", "gameday", "home_team", "away_team"])
    out = {}
    for r in g.itertuples():
        out[(int(r.season), int(r.week), r.home_team)] = r.gameday
        out[(int(r.season), int(r.week), r.away_team)] = r.gameday
    return out


def depth_qb1(season: int, team: str, week: int):
    """gsis_id of the depth-chart QB1 in the latest snapshot with dt < 04:00 UTC on game day (None = unknown)."""
    gd = _gamedays().get((season, week, team))
    d = _depth().get((season, team))
    if gd is None or d is None:
        return None
    cut = f"{gd}T04:00:00Z"
    d = d[d["dt"] < cut]
    if not len(d):
        return None
    v = d.iloc[-1]["gsis_id"]
    return v if isinstance(v, str) else None


def last_top(inp, keep) -> int | None:
    """Index (into pids) of the kept candidate with the most slot rows in the team's most recent game."""
    idx = np.where(keep)[0]
    if not len(idx):
        return None
    c = inp["C"][idx, -1]
    return int(idx[int(np.argmax(c))]) if c.max() > 0 else None


def starter_parts(inp, lam, K, start_gamma, u_start, beta_last=0.0, beta_dc=0.0):
    """Depth signal: the point-in-time depth-chart QB1 (depth_qb1) is kept as a candidate even if stale (unless Out)
    and his start weight is multiplied by exp(beta_dc); if he has no rows for the team, UNLISTED gets the boost. Dropback slot, starter mixture: P(start) over kept candidates + UNLISTED and the spread vector used for the
    non-starter remainder. Out / Doubtful players cannot start (fitting; the sim draws Q/D availability)."""
    keep, s = _starter_base(inp, lam, K)
    idx = np.where(keep)[0]
    r = s[:-1] if len(s) > 1 else np.array([])
    out = np.array([inp["status"][j] in ("Out", "Doubtful") for j in idx], dtype=bool)
    w = np.where(out, 0.0, r ** start_gamma) if len(r) else r
    lt = last_top(inp, keep)
    if lt is not None and len(w):
        w = w * np.where(idx == lt, math.exp(beta_last), 1.0)
    dc = inp.get("_dc_idx", "none")
    u_w = u_start
    if dc == "unlisted":
        u_w = u_start * math.exp(beta_dc)
    elif dc not in ("none", None) and len(w):
        w = w * np.where(idx == dc, math.exp(beta_dc), 1.0)
    if len(w) and w.sum() > 0:
        p_start = np.append((1 - u_start) * w / w.sum(), u_w)
        p_start = p_start / p_start.sum()
    else:
        p_start = np.append(np.zeros(len(r)), 1.0)
    spread = np.append(np.where(out, 0.0, r), max(u_start, 1e-3)) if len(r) else np.array([1.0])
    return keep, p_start, spread


def _starter_base(inp, lam, K):
    """base_shares with the depth-chart QB1 force-kept (if he has rows for the team and is not Out)."""
    keep, s = base_shares(inp, lam, 1.0, K, 0.0)
    q = inp.get("_dc_pid", "unset")
    if q == "unset":
        q = depth_qb1(inp["season"], inp["team"], inp["week"])
        inp["_dc_pid"] = q
    inp["_dc_idx"] = "none"
    if q is None:
        return keep, s
    if q in inp["pids"]:
        j = inp["pids"].index(q)
        if not keep[j] and inp["status"][j] != "Out":
            keep2, s2 = base_shares(inp, lam, 1.0, 99, 0.0)
            if keep2[j]:
                keep = keep.copy(); keep[j] = True
                r = np.zeros(len(keep))
                r[keep2] = s2[:-1]
                rr = r[keep]
                s = np.append(rr / rr.sum(), 0.0) if rr.sum() > 0 else s
        if keep[j]:
            inp["_dc_idx"] = j
    else:
        inp["_dc_idx"] = "unlisted"
    return keep, s


def _starter_ll(inp, lam, K, start_gamma, rho, u_start, beta_last=0.0, beta_dc=0.0) -> float:
    keep, p_start, spread = starter_parts(inp, lam, K, start_gamma, u_start, beta_last, beta_dc)
    a = inp["actual"]
    ids = [p for j, p in enumerate(inp["pids"]) if keep[j]]
    c = np.array([a["by_pid"][p] for p in ids] + [a["total"] - sum(a["by_pid"][p] for p in ids)], dtype=float)
    terms = []
    for i in range(len(p_start)):
        if p_start[i] <= 0:
            continue
        rest = spread.copy(); rest[i] = 0.0
        pi = np.full(len(c), 0.0)
        if rest.sum() > 0:
            pi = (1 - rho) * rest / rest.sum()
            pi[i] = rho
        else:
            pi[i] = 1.0
        pi = np.clip(pi, 1e-6, 1)
        terms.append(math.log(p_start[i]) + float((c * np.log(pi)).sum()))
    m = max(terms)
    return m + math.log(sum(math.exp(t - m) for t in terms))


def fit_starter(train: list) -> dict:
    """Dropback slot: per game one starter drawn from P(start_p) ~ r_p^start_gamma (r = recency-weighted dropback
    share over games played, lam / K as for the other slots) times exp(beta_last) for the player with the most
    dropbacks in the team's most recent game; Out/Doubtful cannot start; u_start = P(starter is
    someone outside the list) = train frequency of games whose top dropback player was unlisted); the starter takes
    rho of the dropbacks, the rest is spread over the others in proportion to r. Fit by maximum likelihood."""
    G = STARTER_GRID
    u_cache = {}

    def u_for(lam, K):
        if (lam, K) not in u_cache:
            n_unl = 0
            for x in train:
                keep, _ = _starter_base(x, lam, K)
                a = x["actual"]
                ids = [p for j, p in enumerate(x["pids"]) if keep[j]]
                top = max([a["by_pid"][p] for p in ids] or [0])
                n_unl += int(a["total"] - sum(a["by_pid"][p] for p in ids) > top)
            u_cache[(lam, K)] = min(max(n_unl / len(train), 1e-3), 0.5)
        return u_cache[(lam, K)]

    def ll(lam, K, g, rho, b, bd):
        return sum(_starter_ll(x, lam, K, g, rho, u_for(lam, K), b, bd) for x in train)

    # staged (coordinate) grid search: (lam, K, gamma) | (beta_last, beta_dc, rho) | (lam, K, gamma) again
    cur = {"lam": 0.5, "K": 1, "g": 1.0, "rho": 0.975, "b": 0.0, "bd": 2.0}
    trace = []
    for stage in ("share", "boosts", "share"):
        cands = ([{"lam": l, "K": k, "g": g} for l in G["lam"] for k in G["K"] for g in G["start_gamma"]]
                 if stage == "share" else
                 [{"b": b, "bd": bd, "rho": r} for b in G["beta_last"] for bd in G["beta_dc"] for r in G["rho"]])
        scored = [(ll(**{**cur, **c}), c) for c in cands]
        v, c = max(scored, key=lambda t: t[0])
        cur.update(c)
        trace.append({"stage": stage, "ll": v, **c})
    best = (trace[-1]["ll"], cur["lam"], cur["K"], cur["g"], cur["rho"], u_for(cur["lam"], cur["K"]), cur["b"], cur["bd"])
    ll, lam, K, g, rho, u, b, bd = best
    n_dc = sum(1 for x in train if x.get("_dc_pid") not in (None, "unset"))
    return {"mode": "starter", "lam": lam, "K": int(K), "start_gamma": g, "rho": rho, "u_start": u, "beta_last": b,
            "beta_dc": bd, "train_games_with_depth_signal": n_dc, "search": "staged grid", "search_trace": trace,
            "gamma": 1.0, "alpha": 0.0, "u": u, "kappa": None, "objective": "starter_mixture_multinomial",
            "train_team_games": len(train), "train_ll": ll,
            "at_grid_edge": {k: v in (G[k][0], G[k][-1]) for k, v in (("lam", lam), ("K", K), ("start_gamma", g),
                                                                      ("rho", rho), ("beta_last", b), ("beta_dc", bd))}}


def fit_availability(eval_season: int, eval_week: int, seasons=(2024, 2025), min_r: float = 0.10) -> dict:
    """P(plays | Questionable) and P(plays | Doubtful) among candidates with prior share >= min_r in any slot
    ("plays" = >= 1 opportunity of any kind that week; low-usage players excluded because 0 opps is ambiguous)."""
    cnt = {"Questionable": [0, 0], "Doubtful": [0, 0]}
    def scan(s, wmax):
        tb = _season_tables(s)
        for team, weeks in tb[1].items():
            for w in weeks:
                if w < 3 or w >= wmax:
                    continue
                seen = set()
                for slot in SLOTS:
                    x = team_game_inputs(s, team, w, slot)
                    if x is None:
                        continue
                    keep, sh = base_shares(x, 0.8, 1.0, 3, 0.0)
                    for j, pid in enumerate(x["pids"]):
                        stt = x["status"][j]
                        if stt in cnt and pid not in seen and keep[j]:
                            r = sh[list(np.where(keep)[0]).index(j)]
                            if r >= min_r:
                                seen.add(pid)
                                cnt[stt][1] += 1
                                cnt[stt][0] += int(pid in tb[2][team].get(w, set()))
    for s in seasons:
        if s < eval_season:
            scan(s, 99)
    scan(eval_season, eval_week)
    return {k: {"p_play": (v[0] + 1) / (v[1] + 2), "n": v[1], "played": v[0], "prior": "Beta(1,1)"} for k, v in cnt.items()}


# ------------------------------------------------------------------ feature likelihoods (empirical Bayes)
def feature_cells(slot: str) -> list:
    zones = ("i5", "rz", "op")
    if slot == "target":
        return [f"{z}|{d}|{r}" for z in zones for d in ("bl", "s", "m", "d", "u") for r in ("inc", "comp", "td", "int")]
    if slot == "carry":
        return [f"{z}|{y}|{t}" for z in zones for y in ("le0", "1_3", "4_9", "10p") for t in ("no", "td")]
    return [f"{z}|{k}" for z in zones for k in ("comp", "inc", "int", "sack", "td", "run")]


def lik_rows(eval_season: int, eval_week: int, seasons=(2024, 2025)) -> pd.DataFrame:
    parts = [opp_rows(s) for s in seasons if s < eval_season]
    cur = opp_rows(eval_season)
    parts.append(cur[cur["week"] < eval_week])
    o = pd.concat(parts, ignore_index=True)
    o = o[o["feat"].notna() & o["pid"].notna()]
    if ((o["season"] == eval_season) & (o["week"] >= eval_week)).any():
        raise RuntimeError("likelihood rows read the eval week or later")
    return o


def fit_priors(rows: pd.DataFrame, slot: str) -> dict:
    pos = positions()
    cells = feature_cells(slot)
    g = rows[rows["slot"] == slot]
    out = {}
    grp = g["pid"].map(lambda p: group(pos.get(p, "UNK")))
    for key, sub in list(g.groupby(grp)) + [("ALL", g)]:
        vc = sub["feat"].value_counts()
        tot = len(sub) + 0.5 * len(cells)
        out[key] = {c: (vc.get(c, 0) + 0.5) / tot for c in cells}
    out["UNLISTED"] = out["ALL"]
    return out


def fit_m(rows: pd.DataFrame, slot: str, eval_season: int, eval_week: int) -> dict:
    """Prior strength m by held-out log likelihood: counts from rows before the last pre-eval week, scored on it."""
    pos = positions()
    g = rows[rows["slot"] == slot]
    last = eval_week - 1
    ho = g[(g["season"] == eval_season) & (g["week"] == last)]
    tr = g[~((g["season"] == eval_season) & (g["week"] >= last))]
    pri = fit_priors(tr, slot)
    counts = {pid: sub["feat"].value_counts().to_dict() for pid, sub in tr.groupby("pid")}
    res = {}
    for m in M_GRID:
        ll = 0.0
        for r in ho.itertuples():
            pr = pri.get(group(pos.get(r.pid, "UNK")), pri["ALL"])
            c = counts.get(r.pid, {})
            n = sum(c.values())
            ll += math.log((c.get(r.feat, 0) + m * pr[r.feat]) / (n + m))
        res[m] = ll
    m = max(res, key=res.get)
    return {"m": m, "heldout_week": [eval_season, last], "heldout_rows": int(len(ho)),
            "ll_by_m": {str(k): round(v, 2) for k, v in res.items()}, "m_at_grid_edge": m in (M_GRID[0], M_GRID[-1])}


# ------------------------------------------------------------------ freeze one week's parameters
def fit_week(eval_season: int, eval_week: int) -> dict:
    if eval_season == 2026 and eval_week >= HOLDOUT_FIRST_WEEK:
        pass  # fitting with weeks < 10 is allowed (a pregame model for a week-10 game); SCORING weeks >= 10 is refused
    params = {"eval_season": eval_season, "eval_week": eval_week, "slots": {}, "lik": {}}
    for slot in SLOTS:
        tr = train_set(eval_season, eval_week, slot)
        params["slots"][slot] = fit_starter(tr) if slot == "dropback" else fit_slot(tr)
    params["availability"] = fit_availability(eval_season, eval_week)
    rows = lik_rows(eval_season, eval_week)
    for slot in SLOTS:
        params["lik"][slot] = fit_m(rows, slot, eval_season, eval_week)
    params["data_max_week_used"] = {"season": eval_season, "week": eval_week - 1}
    return params


def build_model(eval_season: int, eval_week: int, teams, params: dict, *, name_source: str = "pbp_2026") -> dict:
    """Frozen JSON model for opportunity.OpportunityRecorder (teams' candidate lists for the eval week)."""
    om = _feat_mod()
    rows = lik_rows(eval_season, eval_week)
    pos = positions()
    avail = params["availability"]
    model = {"schema": om.SCHEMA, "teams": {}, "qb_ids": sorted({p for p in rows["pid"].unique() if pos.get(p) == "QB"}),
             "meta": {"eval_season": eval_season, "eval_week": eval_week, "params": params,
                      "fitted_on": f"2024-2025 REG + {eval_season} weeks < {eval_week}",
                      "research_only": True, "projection_ready": False}}
    for team in teams:
        tm = {"slots": {}, "lik": {}, "candidates": {}}
        for slot in SLOTS:
            p = params["slots"][slot]
            x = team_game_inputs(eval_season, team, eval_week, slot)
            if x is None:
                raise RuntimeError(f"no history for {team} before week {eval_week}")
            if p.get("mode") == "starter":
                keep, s0 = _starter_base(x, p["lam"], p["K"])
                s = np.append(s0[:-1] * (1 - p["u"]), p["u"]) if len(s0) > 1 else np.array([1.0])
            else:
                keep, s = base_shares(x, p["lam"], p["gamma"], p["K"], p["u"])
            idx = list(np.where(keep)[0])
            names, poss, av, pids, stat = [], [], [], [], []
            shares = []
            for k, j in enumerate(idx):
                st = x["status"][j]
                a = 0.0 if st == "Out" else (avail["Doubtful"]["p_play"] if st == "Doubtful" else (
                    avail["Questionable"]["p_play"] if st == "Questionable" else 1.0))
                nm = x["names"][j]
                if nm in names:  # same engine name for two ids on one team: merge (rows cannot tell them apart)
                    i = names.index(nm)
                    shares[i] += s[k]
                    av[i] = max(av[i], a)
                    continue
                names.append(nm); poss.append(x["pos"][j]); av.append(a); pids.append(x["pids"][j]); stat.append(st)
                shares.append(float(s[k]))
            names.append(om.UNLISTED); poss.append(om.UNLISTED); av.append(1.0); pids.append(None); stat.append(None)
            shares.append(float(s[-1]))
            tm["slots"][slot] = {"players": names, "pos": poss, "share": shares, "avail": av,
                                 "alpha": p["alpha"], "kappa": p["kappa"]}
            if p.get("mode") == "starter":
                lt = last_top(x, keep)
                tm["slots"][slot].update({"mode": "starter", "start_gamma": p["start_gamma"], "rho": p["rho"],
                                          "u_start": p["u_start"], "beta_last": p.get("beta_last", 0.0),
                                          "last_top": x["names"][lt] if lt is not None else None,
                                          "beta_dc": p.get("beta_dc", 0.0),
                                          "depth_qb1": (x["names"][x["_dc_idx"]] if isinstance(x.get("_dc_idx"), int)
                                                        else ("UNLISTED" if x.get("_dc_idx") == "unlisted" else None)),
                                          "depth_qb1_gsis": x.get("_dc_pid") if x.get("_dc_pid") != "unset" else None})
            tm["candidates"][slot] = [{"name": n, "gsis_id": i, "pos": q, "status": t, "base_share": round(v, 4),
                                       "avail": a} for n, i, q, t, v, a in zip(names, pids, poss, stat, shares, av)]
            pri = fit_priors(rows, slot)
            m = params["lik"][slot]["m"]
            g = rows[rows["slot"] == slot]
            pl = {}
            for n, i, q in zip(names, pids, poss):
                if i is None:
                    continue
                c = g[g["pid"] == i]["feat"].value_counts().to_dict()
                pl[n] = om.eb_lik(c, pri.get(group(q), pri["ALL"]), m)
            tm["lik"][slot] = {"players": pl, "prior": pri, "floor": 1e-6, "m": m}
        model["teams"][team] = tm
    return model
