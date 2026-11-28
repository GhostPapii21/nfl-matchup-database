"""sim_v7 — three genuinely distinct NFL game/player simulation methods x three game scripts.

THIS IS A NEW ENGINE, NOT THE ORIGINAL sim_v6. The original (blob ab2144f0...) is preserved verbatim in
engines/sim_v6_recovered/ for provenance; its 'bias' mode is the MC sampler with a different multiplier
(identical medians in a 100K re-run), and it has no game-script axis, so it cannot meet the 3x3 contract.

Methods
  mc    Parametric Monte Carlo. Team TD/FG counts ~ Poisson around market-implied points with a shared pace
        factor and a per-team efficiency shock; quarter points by multinomial allocation of scores; team pass/rush
        volume from the simulated margin (league-fitted log-linear script slopes); player opportunity by
        Beta/multinomial shares; efficiency by Beta catch rate and Gamma yards; TDs allocated from team TDs by
        red-zone share. Player production is therefore tied to team scoring and game script.
  bias  Calibrated Bias. MC draws passed through a per-market probabilistic recalibration map fitted on
        chronological walk-forward PIT residuals (calibration.py). The map is applied as a monotone transform of
        each trial's draw, so the joint structure with team scoring is preserved. Status per market comes from
        the holdout scorecard: CALIBRATED_HOLDOUT_VALIDATED or EXPERIMENTAL_UNVALIDATED. No artifact -> REFUSED.
  gr    Game Randomness. Possession-driven empirical resampling: alternating drives on a 60-minute clock, each
        drive resampled from the team's real 2024-26 drives in the same game-state bucket (trailing 8+, within 7,
        leading 8+) and half. A resampled drive carries its real duration, points, and every player's real
        production on that drive, so player outcomes, team score, quarter score and script are jointly sampled.

Scenarios (favorite perspective; H = first-half margin, F = final regulation margin), disjoint, by rejection:
  favorite_controls  H > 0 and F >= 10
  competitive        |H| <= 6 and |F| <= 7
  underdog_chases    H >= 7 and F < 10     (dog trails by a score+ at half and is chasing)
  residual           exhaustive complement of the three primary scripts (reported separately)

Unconditional market probabilities weight each scenario's conditional distribution by its
empirical scenario frequency (acceptance_rate / sum of rates over the exhaustive partition).
"""
from __future__ import annotations

import hashlib
import time

import numpy as np

from . import data as D

METHODS = ("mc", "bias", "gr")
PRIMARY_SCENARIOS = ("favorite_controls", "competitive", "underdog_chases")
RESIDUAL_SCENARIO = "residual"
SCENARIOS = PRIMARY_SCENARIOS  # default run_cells contract: primary cells
ALL_SCENARIOS = PRIMARY_SCENARIOS + (RESIDUAL_SCENARIO,)
PCTS = (5, 10, 15, 20, 25, 50, 75, 90, 95)
QB_STATS = ("att", "cmp", "passyds", "passtd", "car", "rushyds", "rushtd")
SK_STATS = ("tgt", "rec", "recyds", "rectd", "car", "rushyds", "rushtd")
MARKET = {"att": "pass_att", "cmp": "pass_cmp", "passyds": "pass_yds", "passtd": "pass_td", "car": "rush_att",
          "rushyds": "rush_yds", "rushtd": "rush_td", "tgt": "targets", "rec": "receptions", "recyds": "rec_yds",
          "rectd": "rec_td"}
ENGINE_VERSION = "sim_v7.1.0"


def seed_for(base: int, *parts) -> int:
    return (base + int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)) % (2**32)


def classify(H: np.ndarray, F: np.ndarray, include_residual: bool = False) -> dict:
    primary = {"favorite_controls": (H > 0) & (F >= 10),
               "competitive": (np.abs(H) <= 6) & (np.abs(F) <= 7),
               "underdog_chases": (H >= 7) & (F < 10)}
    if include_residual:
        hit = np.zeros(len(H), dtype=bool)
        for m in primary.values():
            hit |= m
        primary[RESIDUAL_SCENARIO] = ~hit
    return primary


def stat_keys(ctx) -> list:
    out = []
    for gs, role in zip(ctx.players.gsis, ctx.players.role):
        out += [(gs, s) for s in (QB_STATS if role == "QB" else SK_STATS)]
    return out


# --------------------------------------------------------------------------------------------- MC
def _beta(rng, m, v, n):
    m = float(np.clip(m, 1e-3, 0.999))
    v = float(max(min(v, m * (1 - m) * 0.9), 1e-5))
    k = m * (1 - m) / v - 1
    return rng.beta(m * k, (1 - m) * k, n)


def _gamma_sum(rng, k, mean, var, shift=0.0):
    """Sum of k iid (Gamma(mean+shift, var) - shift) draws, vectorised: Gamma(k*a, theta) - shift*k."""
    m = mean + shift
    var = max(var, 1.0)
    a, th = m * m / var, var / m
    out = np.zeros(len(k))
    pos = k > 0
    out[pos] = rng.gamma(k[pos] * a, th) - shift * k[pos]
    return out


def _shares(ctx, col, teamcol, ids):
    pg = ctx.pgame
    g = ctx.games.set_index("game_id")
    res = []
    for gs in ids:
        x = pg[pg.gsis == gs].set_index("game_id")[col].reindex(ctx.game_ids).fillna(0)
        s = (x / g[teamcol].reindex(ctx.game_ids).clip(lower=1)).values
        active = (x.values > 0)
        sa = s[active] if active.any() else s
        last3 = s[-3:][active[-3:]] if active[-3:].any() else sa
        m = 0.6 * sa.mean() + 0.4 * last3.mean()
        v = max(np.var(sa, ddof=1) if len(sa) > 1 else (m * 0.3) ** 2, (m * 0.15) ** 2, 1e-4)
        res.append((m, v))
    return res


def mc_team_plan(ctx, opp_ctx, implied_pts: float | None):
    lg = ctx.league
    g = ctx.games
    pts_hist = g.pts.mean()
    if implied_pts is None:   # no market: regress team scoring and opponent allowance to league mean
        implied_pts = 0.5 * (0.6 * pts_hist + 0.4 * lg["pts_mean"]) + 0.5 * (0.6 * opp_ctx.games.opp_pts.mean() + 0.4 * lg["pts_mean"])
    td7, fg3 = 7 * g.td.sum(), 3 * g.fg.sum()
    r = (td7 + 20 * 0.70) / (td7 + fg3 + 20)
    p_pass = (g.pass_td.sum() + 2 * 0.6) / (g.td.sum() + 2)
    qtot = g[["q1", "q2", "q3", "q4"]].sum().values
    qsh = (qtot + 40 * np.array([0.2, 0.3, 0.2, 0.3])) / (qtot.sum() + 40)
    return dict(implied=float(implied_pts), lam_td=r * implied_pts / 6.95, lam_fg=(1 - r) * implied_pts / 3.0,
                p_pass=float(p_pass), qsh=qsh / qsh.sum(), pa=g.pa.mean(), ra=g.ra.mean(),
                exp_margin=0.0)


def _coverage_share_means(ctx, rec_ids, adj) -> list:
    """Historical Beta means tilted by coverage allocation multipliers (inferred/measured mix)."""
    base = _shares(ctx, "tgt", "pa", rec_ids) if rec_ids else []
    alloc = (adj.get("coverage_allocation") or {}).get("receivers") or {}
    out = []
    for i, gs in enumerate(rec_ids):
        m, v = base[i]
        mult = float((alloc.get(gs) or {}).get("target_share_multiplier") or 1.0)
        # Prefer measured board share level when present
        ms = (alloc.get(gs) or {}).get("measured_target_share")
        if ms is not None:
            m = 0.5 * m + 0.5 * float(ms)
        m = float(np.clip(m * mult, 1e-3, 0.85))
        out.append((m, v))
    return out


def _rz_td_weights(ctx, ids, team_rz, share_mean, kind: str, opp_allow: float = 1.0):
    """Red-zone / goal-line TD allocation weights with defensive allowance tilt."""
    # kind: 'pass' uses rz targets; 'rush' uses rz carries; goal-line = yardline<=5 approx via 0.35 of RZ
    w = []
    for i, g in enumerate(ids):
        rz_t, rz_c = ctx.rz.get(g, (0.0, 0.0))
        rz = rz_t if kind == "pass" else rz_c
        sh = float(share_mean[i]) if i < len(share_mean) else 0.0
        gl = 0.35 * rz  # proxy goal-line usage from RZ (measured RZ counts; GL not separately tagged here)
        w.append((rz + 2 * gl + 3 * sh) * float(opp_allow))
    w.append(max(0.03 * (sum(w) + 1), 0.03))  # _other
    w = np.asarray(w, dtype=float)
    return w / w.sum()


def mc_batch(ctxs: dict, plans: dict, n: int, rng) -> dict:
    """One batch of n MC games. ctxs/plans keyed by team. Returns dict of float32 arrays."""
    teams = list(ctxs)
    lg = ctxs[teams[0]].league
    sig_e = 0.5 * lg["sd_log_ypp"]
    pace = rng.lognormal(0, 0.06, n)
    out, pts, qp = {}, {}, {}
    eff = {}
    for t in teams:
        P = plans[t]
        z = rng.standard_normal(n)
        e = np.exp(sig_e * z - sig_e ** 2 / 2)
        eff[t] = e
        # Mild opponent-defense points tilt when available
        opp = [x for x in teams if x != t][0]
        def_pts = float((plans[t].get("defensive") or {}).get("opp_points_factor", 1.0))
        td = rng.poisson(P["lam_td"] * e * pace * def_pts)
        fg = rng.poisson(P["lam_fg"] * pace * def_pts)
        tdq = rng.multinomial(td, P["qsh"])
        fgq = rng.multinomial(fg, P["qsh"])
        xpq = rng.binomial(tdq, 0.95)
        qp[t] = 6 * tdq + xpq + 3 * fgq
        pts[t] = qp[t].sum(1)
        out[f"{t}|td"] = td
    for t in teams:
        o = [x for x in teams if x != t][0]
        ctx, P = ctxs[t], plans[t]
        margin = pts[t] - pts[o]
        exp_m = P["implied"] - plans[o]["implied"]
        noise = rng.lognormal(0, 0.10, n)
        PA0 = rng.poisson(np.clip(P["pa"] * pace * noise * np.exp(lg["bP"] * (margin - exp_m)), 5, 80))
        adj = P.get("defensive", {})
        PA0 = rng.binomial(PA0, min(1., adj.get("attempts", 1.))) + rng.poisson(PA0 * max(0., adj.get("attempts", 1.) - 1.))
        RA = rng.poisson(np.clip(P["ra"] * pace / noise ** 0.5 * np.exp(lg["bR"] * (margin - exp_m)), 5, 60))
        pl = ctx.players
        qb = pl.gsis.iloc[0]
        rec_ids = [g for g, r in zip(pl.gsis, pl.role) if r != "QB" and ctx.pgame[ctx.pgame.gsis == g].tgt.sum() > 0]
        # Designed rushers exclude QB scramble volume; QB designed runs handled via scramble profile
        rush_ids = [g for g in pl.gsis if g != qb and ctx.pgame[ctx.pgame.gsis == g].car.sum() > 0]
        # --- pressure / scramble on dropbacks (PA0 ≈ dropbacks)
        scr_prof = adj.get("scramble") or {}
        if scr_prof.get("status") in ("MEASURED", "EXPERIMENTAL_UNVALIDATED"):
            from . import scramble as SC
            scr = SC.apply_scramble_to_dropbacks(rng, n, PA0, scr_prof)
            PA = scr["thrown"]  # attempts that become throws (targets)
            qb_scr_att = scr["scrambled"]
            qb_scr_yds = scr["scramble_yds"]
            qb_scr_td = scr["scramble_td"]
            designed_mu = scr["designed_qb_att_mean"]
            designed_ypc = scr["designed_ypc"]
        else:
            PA = PA0.astype(np.float32)
            qb_scr_att = qb_scr_yds = qb_scr_td = np.zeros(n, np.float32)
            designed_mu, designed_ypc = 0.0, 2.5
        # --- targets (coverage-tilted shares)
        means = _coverage_share_means(ctx, rec_ids, adj)
        sh = np.column_stack([_beta(rng, m, v, n) for m, v in means]) if rec_ids else np.zeros((n, 0))
        tot = sh.sum(1, keepdims=True)
        sh = np.where(tot > 0.97, sh * 0.97 / np.maximum(tot, 1e-9), sh)
        pv = np.column_stack([sh, 1 - sh.sum(1)]) if rec_ids else np.ones((n, 1))
        PA_i = np.maximum(np.asarray(PA, dtype=int), 0)
        T = rng.multinomial(PA_i, pv)
        # --- carries (skill only; QB designed added below)
        shr = np.column_stack([_beta(rng, m, v, n) for m, v in _shares(ctx, "car", "ra", rush_ids)]) if rush_ids else np.zeros((n, 0))
        tot = shr.sum(1, keepdims=True)
        shr = np.where(tot > 0.98, shr * 0.98 / np.maximum(tot, 1e-9), shr)
        # Reserve a designed-QB slice from RA so scrambles are not double-counted into RA shares
        qb_des = rng.poisson(np.clip(designed_mu * pace, 0, 8)) if designed_mu > 0 else np.zeros(n, dtype=int)
        RA_skill = np.maximum(RA - qb_des, 0)
        C = rng.multinomial(RA_skill, np.column_stack([shr, 1 - shr.sum(1)])) if rush_ids else np.zeros((n, 1), dtype=int)
        # --- TDs with RZ / GL / defense allowances
        td = out[f"{t}|td"]
        # QB pressure response: more sacks/scrambles slightly shift TD mix toward rush
        scr_frac = qb_scr_att / np.maximum(PA0, 1)
        p_pass = np.clip(P["p_pass"] * (1.0 - 0.15 * scr_frac) * float(adj.get("pass_td_factor", 1.0)), 0.25, 0.85)
        ptd = rng.binomial(td, p_pass)
        rtd = td - ptd
        rzt, rzc = ctx.rz["_team"]
        tsh = pv.mean(0) if pv.size else np.array([1.0])
        opp_pass_allow = 1 + 0.5 * (lg["opp_cr"].get((o, "WR"), 1.0) - 1)
        opp_rush_allow = 1 + 0.5 * (lg["opp_ypc"].get(o, 1.0) - 1)
        rz_p = _rz_td_weights(ctx, rec_ids, rzt, tsh, "pass", opp_pass_allow)
        RT = rng.multinomial(ptd, rz_p)
        csh = shr.mean(0) if rush_ids else np.zeros(0)
        # include QB designed+scramble in rush TD pool as final bucket before _other
        rush_td_ids = rush_ids + ([qb] if (designed_mu > 0 or qb_scr_att.mean() > 0) else [])
        csh_qb = list(csh) + ([max(designed_mu, 0.5) / max(P["ra"], 1)] if qb in rush_td_ids else [])
        rz_r = _rz_td_weights(ctx, rush_td_ids, rzc, csh_qb, "rush", opp_rush_allow)
        UT = rng.multinomial(rtd, rz_r)
        e = eff[t]
        opp = o
        tot_rec, tot_ry = np.zeros(n), np.zeros(n)
        for i, g in enumerate(rec_ids + ["_other"]):
            pos = "WR" if g == "_other" else ctx.players.set_index("gsis").pos.get(g, "WR")
            if g == "_other":
                cr_m, cr_n, y_m, y_v = lg["cr_all"], 0, lg["ypr_all"], lg["ypr_var_all"]
            else:
                x = ctx.pgame[ctx.pgame.gsis == g]
                cr_n = x.tgt.sum()
                cr_m = (x.rec.sum() + 20 * lg["cr"].get(pos, lg["cr_all"])) / (cr_n + 20)
                ys = ctx.rec_yards[g]
                k = len(ys)
                lm, lv = lg["ypr"].get(pos, lg["ypr_all"]), lg["ypr_var"].get(pos, lg["ypr_var_all"])
                y_m = (ys.sum() + 30 * lm) / (k + 30) if k else lm
                y_v = ((ys.var() if k > 1 else lv) * k + lv * 30) / (k + 30)
            a_cr = 1 + 0.5 * (lg["opp_cr"].get((opp, pos), 1.0) - 1)
            a_y = 1 + 0.5 * (lg["opp_ypt"].get((opp, pos), 1.0) / lg["opp_cr"].get((opp, pos), 1.0) - 1)
            cr = np.clip(_beta(rng, min(cr_m * a_cr * adj.get("completion", 1.), 0.92), (0.06) ** 2, n), 0, 1)
            R = rng.binomial(T[:, i], cr)
            Y = _gamma_sum(rng, R, y_m * a_y * adj.get("yards_per_completion", 1.), y_v * a_y ** 2) * e
            tot_rec += R
            tot_ry += Y
            if g != "_other":
                out[f"{g}|tgt"], out[f"{g}|rec"], out[f"{g}|recyds"], out[f"{g}|rectd"] = T[:, i], R, Y, RT[:, i]
        # Consistency: pass_td equals sum of allocated receiving TDs (including _other bucket)
        # Modeled receivers get RT[:, :-1]; QB passtd = ptd (= sum RT)
        a_ypc = 1 + 0.5 * (lg["opp_ypc"].get(opp, 1.0) - 1)
        for i, g in enumerate(rush_ids):
            ys = ctx.rush_yards[g]
            k = len(ys)
            y_m = (ys.sum() + 60 * lg["ypc"]) / (k + 60)
            y_v = ((ys.var() if k > 1 else lg["ypc_var"]) * k + lg["ypc_var"] * 60) / (k + 60)
            out[f"{g}|car"] = C[:, i]
            out[f"{g}|rushyds"] = _gamma_sum(rng, C[:, i], y_m * a_ypc, y_v, shift=6.0) * e
            out[f"{g}|rushtd"] = UT[:, i]
        # QB: designed runs + scrambles (no double-count with skill RA)
        qb_des_yds = _gamma_sum(rng, qb_des, designed_ypc * a_ypc, max(lg["ypc_var"], 9.0), shift=3.0) * e
        qb_rush_att = qb_des + qb_scr_att
        qb_rush_yds = qb_des_yds + qb_scr_yds
        # QB rush TDs from scramble TDs + share of rush TD multinomial if qb in rush_td_ids
        if qb in rush_td_ids:
            qi = rush_td_ids.index(qb)
            qb_rush_td = UT[:, qi] + qb_scr_td
            # scramble TDs already part of game; avoid exceeding team rush TDs by capping display
            # Statistical consistency: team rush TDs = sum skill rushtd + QB designed/scramble share
            # Re-assign: skill UT already sums with QB bucket to rtd; scramble TD is pathway into that bucket
            # so use UT qb bucket as authority and keep scramble_td as informational component
            qb_rush_td = UT[:, qi]
        else:
            qb_rush_td = qb_scr_td
        out[f"{qb}|att"] = PA_i.astype(np.float32)
        out[f"{qb}|cmp"] = tot_rec
        out[f"{qb}|passyds"] = tot_ry
        out[f"{qb}|passtd"] = ptd  # == sum(RT) receiving TDs including _other
        out[f"{qb}|car"] = qb_rush_att
        out[f"{qb}|rushyds"] = qb_rush_yds
        out[f"{qb}|rushtd"] = qb_rush_td
        out[f"{t}|pass_td_team"] = ptd.astype(np.float32)
        out[f"{t}|rush_td_team"] = rtd.astype(np.float32)
        for gs, s in stat_keys(ctx):
            out.setdefault(f"{gs}|{s}", np.zeros(n))
        out[f"{t}|pts"] = pts[t]
        for q in range(4):
            out[f"{t}|q{q+1}"] = qp[t][:, q]
    keep = {}
    for k, v in out.items():
        if k.endswith("|td") and k.split("|")[0] in ctxs:
            continue  # drop internal team td counter
        keep[k] = np.asarray(v, dtype=np.float32)
    return keep


# --------------------------------------------------------------------------------------------- GR
class DrivePool:
    def __init__(self, ctx, opp_ctx=None, defensive: dict | None = None, min_n: int = 12):
        d = ctx.drives
        self.keys = stat_keys(ctx)
        cols = [f"{g}|{s}" for g, s in self.keys]
        self.S = d[cols].to_numpy(np.float32)
        self.dur = d.dur.to_numpy(np.float64)
        self.off = d.off_pts.to_numpy(np.float32)
        self.dfp = d.def_pts.to_numpy(np.float32)
        b = np.where(d.state <= -8, 0, np.where(d.state >= 8, 2, 1))
        h = d.half.to_numpy()
        self.pools = {}
        allidx = np.arange(len(d))
        for bb in (0, 1, 2):
            for hh in (1, 2):
                idx = allidx[(b == bb) & (h == hh)]
                if len(idx) < min_n:
                    idx = allidx[b == bb]
                if len(idx) < min_n:
                    idx = allidx
                self.pools[(bb, hh)] = idx
        self.n_drives = len(d)
        # Opponent-defense reweight: upweight historical drives vs similar-allowance defenses
        self.weights = np.ones(len(d), dtype=np.float64)
        self.def_factor_pts = 1.0
        self.def_factor_yards = 1.0
        if defensive:
            od = defensive.get("opponent_defense") or {}
            # points factor from opponent league allowance already in lg; use mild board pressure tilt
            pr = od.get("pressure_rate")
            if pr is not None:
                self.def_factor_pts = float(np.clip(1.0 - 0.15 * (float(pr) - 0.28), 0.85, 1.12))
                self.def_factor_yards = float(np.clip(1.0 - 0.12 * (float(pr) - 0.28), 0.85, 1.12))
            # Reweight drives by historical opponent pass/rush allowance proximity when opp column exists
            if opp_ctx is not None and "opp" in ctx.games.columns:
                # map each drive's game to opponent; weight by how close opp_ypc was to current opponent
                lg = ctx.league
                cur = lg["opp_ypc"].get(opp_ctx.team, 1.0)
                g2opp = ctx.games.set_index("game_id")["opp"].to_dict()
                opps = d.game_id.map(g2opp)
                hist = opps.map(lambda o: lg["opp_ypc"].get(o, 1.0))
                # closer historical opp allowance → higher weight
                self.weights = np.exp(-3.0 * (hist.fillna(1.0).to_numpy() - cur) ** 2)
                self.weights = np.clip(self.weights, 0.25, 2.5)


def _weighted_choice(rng, pool_idx, weights, k):
    w = weights[pool_idx]
    w = w / w.sum()
    return rng.choice(pool_idx, size=k, replace=True, p=w)


def gr_batch(ctxs: dict, n: int, rng, max_iter: int = 60, defenses: dict | None = None) -> dict:
    teams = list(ctxs)
    defenses = defenses or {}
    pools = [DrivePool(ctxs[t], opp_ctx=ctxs[[x for x in teams if x != t][0]],
                       defensive=defenses.get(t)) for t in teams]
    acc = [np.zeros((n, p.S.shape[1]), np.float32) for p in pools]
    elapsed = np.zeros(n)
    first = rng.integers(0, 2, n)
    poss = first.copy()
    score = np.zeros((n, 2), np.float32)
    qpts = np.zeros((n, 2, 4), np.float32)
    for _ in range(max_iter):
        active = elapsed < 3600
        if not active.any():
            break
        for t in (0, 1):
            m = np.flatnonzero(active & (poss == t))
            if len(m) == 0:
                continue
            P = pools[t]
            marg = score[m, t] - score[m, 1 - t]
            b = np.where(marg <= -8, 0, np.where(marg >= 8, 2, 1))
            half = np.where(elapsed[m] < 1800, 1, 2)
            idx = np.empty(len(m), np.int64)
            for (bb, hh), pool in P.pools.items():
                sel = (b == bb) & (half == hh)
                k = int(sel.sum())
                if k:
                    idx[sel] = _weighted_choice(rng, pool, P.weights, k)
            st = elapsed[m]
            end = st + P.dur[idx]
            cross = (st < 1800) & (end >= 1800)
            end = np.where(cross, 1800.0, np.minimum(end, 3600.0))
            q = np.minimum(((end - 1e-6) // 900).astype(int), 3)
            off = P.off[idx] * P.def_factor_pts
            dfp = P.dfp[idx]
            score[m, t] += off
            score[m, 1 - t] += dfp
            qpts[m, t, q] += off
            qpts[m, 1 - t, q] += dfp
            acc[t][m] += P.S[idx] * np.float32(P.def_factor_yards)
            elapsed[m] = end
            poss[m] = np.where(cross, 1 - first[m], 1 - t)
            active = elapsed < 3600
    out = {}
    for ti, t in enumerate(teams):
        for j, (g, s) in enumerate(pools[ti].keys):
            out[f"{g}|{s}"] = acc[ti][:, j]
        out[f"{t}|pts"] = score[:, ti]
        for q in range(4):
            out[f"{t}|q{q+1}"] = qpts[:, ti, q]
    return out


# --------------------------------------------------------------------------------------------- BIAS
def apply_recalibration(x: np.ndarray, ginv: np.ndarray, rng) -> np.ndarray:
    """Monotone transform: x_i -> Q_raw(G^-1(F_raw(x_i))). ginv = G^-1 tabulated on a uniform grid of [0,1]."""
    n = len(x)
    order = np.lexsort((rng.random(n), x))
    u = np.empty(n)
    u[order] = (np.arange(n) + 0.5) / n
    grid = np.linspace(0, 1, len(ginv))
    u2 = np.clip(np.interp(u, grid, ginv), 0, 1 - 1e-9)
    xs = x[order]
    return xs[(u2 * n).astype(int)]


# --------------------------------------------------------------------------------------------- driver
def run_cells(game: dict, methods=METHODS, scenarios=SCENARIOS, n: int = 100_000, seed: int = 20261129,
              batch: int = 100_000, max_raw_mult: int = 40, calib: dict | None = None, log=print,
              include_residual: bool = True) -> dict:
    """Run method x scenario cells for one game. game: game_id, home, away, cutoff, fav, implied{team:pts}, exclude.

    Primary scenarios always collected to `n` accepted trials. When include_residual=True, the exhaustive
    residual complement is collected in parallel (reported separately; not pooled into primary cells).
    """
    home, away = game["home"], game["away"]
    ctxs = {t: D.team_context(t, game["cutoff"], exclude=set(game.get("exclude", ()))) for t in (home, away)}
    fav = game["fav"]
    dog = away if fav == home else home
    imp = game.get("implied") or {}
    plans = {t: mc_team_plan(ctxs[t], ctxs[[x for x in ctxs if x != t][0]], imp.get(t)) for t in ctxs}
    defenses = {}
    for t, plan in plans.items():
        adj = game.get("defensive_profiles", {}).get(t, {})
        if adj.get("qb_id") == ctxs[t].players.gsis.iloc[0]:
            plan["defensive"] = adj
            defenses[t] = adj
        elif adj:
            # still pass opponent-defense / allocation even if qb_id mismatch (injury replacement)
            plan.setdefault("defensive", {}).update({
                k: adj[k] for k in ("coverage_allocation", "opponent_defense", "scramble",
                                    "completion", "yards_per_completion", "attempts") if k in adj
            })
            defenses[t] = adj
    collect = list(scenarios)
    if include_residual and RESIDUAL_SCENARIO not in collect:
        collect = list(collect) + [RESIDUAL_SCENARIO]
    results = {}
    for method in methods:
        base = "mc" if method == "bias" else method
        if method == "bias" and not calib:
            results[method] = {"execution_status": "REFUSED_NO_CALIBRATION_ARTIFACT"}
            continue
        rng = np.random.default_rng(seed_for(seed, game["game_id"], method))
        acc = {s: [] for s in collect}
        have = {s: 0 for s in collect}
        hits = {s: 0 for s in collect}
        raw = 0
        t0 = time.time()
        # Primary cells must reach n; residual also targets n but does not block primary completion beyond max_raw
        while (min(have[s] for s in scenarios) < n or
               (include_residual and have[RESIDUAL_SCENARIO] < n)) and raw < max_raw_mult * n:
            if base == "mc":
                b = mc_batch(ctxs, plans, batch, rng)
            else:
                b = gr_batch(ctxs, batch, rng, defenses=defenses)
            raw += batch
            H = (b[f"{fav}|q1"] + b[f"{fav}|q2"]) - (b[f"{dog}|q1"] + b[f"{dog}|q2"])
            F = b[f"{fav}|pts"] - b[f"{dog}|pts"]
            masks = classify(H, F, include_residual=include_residual)
            for s in collect:
                if s not in masks:
                    continue
                hits[s] += int(masks[s].sum())
                need = n - have[s]
                if need <= 0:
                    continue
                idx = np.flatnonzero(masks[s])[:need]
                if len(idx):
                    acc[s].append({k: v[idx] for k, v in b.items()})
                    have[s] += len(idx)
            # Early exit once primaries are full even if residual lags (residual filled opportunistically)
            if min(have[s] for s in scenarios) >= n and (not include_residual or have[RESIDUAL_SCENARIO] >= n or raw >= 5 * n):
                if min(have[s] for s in scenarios) >= n and (not include_residual or have.get(RESIDUAL_SCENARIO, 0) >= n):
                    break
                if min(have[s] for s in scenarios) >= n and raw >= max_raw_mult * n:
                    break
        cells = {}
        for s in collect:
            parts = acc[s]
            X = {k: np.concatenate([p[k] for p in parts]) for k in parts[0]} if parts else {}
            if method == "bias" and X:
                crng = np.random.default_rng(seed_for(seed, game["game_id"], method, s, "recal"))
                for key in list(X):
                    gs, _, st = key.partition("|")
                    if gs in ctxs or st not in MARKET:
                        continue
                    mk = MARKET[st]
                    if mk in calib["markets"]:
                        # Do NOT inherit prior validated status after defensive change — remap still applied
                        # but status overridden in cli to EXPERIMENTAL_UNVALIDATED_DEFENSE_CHANGED
                        X[key] = apply_recalibration(X[key], np.array(calib["markets"][mk]["ginv"]), crng)
            cells[s] = dict(X=X, trial_count=have[s], acceptance_rate=round(hits[s] / max(raw, 1), 5),
                            execution_status="OK" if have[s] >= n else "PARTIAL_SCENARIO_RARE",
                            is_residual=(s == RESIDUAL_SCENARIO))
        # Exhaustive partition frequencies for unconditional market probabilities
        freq = {s: cells[s]["acceptance_rate"] for s in collect}
        freq_sum = sum(freq.values()) or 1.0
        scenario_frequency = {s: round(freq[s] / freq_sum, 6) for s in collect}
        results[method] = dict(cells=cells, raw_trials=raw, seconds=round(time.time() - t0, 2),
                               seed=seed_for(seed, game["game_id"], method),
                               scenario_frequency=scenario_frequency,
                               primary_scenarios=list(scenarios),
                               residual_scenario=RESIDUAL_SCENARIO if include_residual else None)
        log(f"  {game['game_id']} {method}: raw={raw} accepted={have} freq={scenario_frequency} in {results[method]['seconds']}s")
    return dict(ctxs=ctxs, plans=plans, results=results, fav=fav, dog=dog)


def summarize(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=np.float64)
    q = np.percentile(x, PCTS)
    d = {f"p{p}": round(float(v), 3) for p, v in zip(PCTS, q)}
    d["median"] = d.pop("p50")
    d.update(mean=round(float(x.mean()), 3), sd=round(float(x.std()), 3))
    return d


def line_probs(x: np.ndarray, lines: list) -> list:
    out = []
    for L in lines:
        v = float(L["line"])
        out.append(dict(book=L.get("book"), line=v, p_over=round(float((x > v).mean()), 5),
                        p_under=round(float((x < v).mean()), 5), p_push=round(float((x == v).mean()), 5)))
    return out
