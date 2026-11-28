"""sim_v6r1: an explicitly versioned REPLACEMENT triad built from the restored sim_v6. It is NOT sim_v6.

Why a replacement is needed (tools/sim_v6.py is restored unchanged, blob ab2144f0):
  * sim_v6's 'bias' method is the MC draw again with its own seed. Its multipliers are fitted on pred_mc with
    K_BIAS == SHRINK_K == 30, so 'bias' and 'mc' get the same multipliers. It is not a distinct simulation.
  * sim_v6 'mc' ignores the spread. Only 'gr' reacts to game script, so sim_v6 cannot give three distinct methods per
    game-script scenario.

Three methods. Each runs n trials (100,000 by default) per scenario:
  mc_nb     sim_v6 'mc' unchanged. The player's negative-binomial volume, binomial catches and resampled per-catch yards.
            The volume mean is scaled by E[exp(b*(M-mu)) | M in scenario] / E[exp(b*(M-mu))], with M ~ N(mu, 13.5) and
            mu = -spread. The pass and rush slopes b are fitted on pre-cutoff team games, as in sim_v6.
  gr_share  sim_v6 'gr' unchanged (beta target/carry share x lognormal team pace x margin slope), except the margin is
            drawn from N(mu, 13.5) truncated to the scenario. The volume normalisation uses the unconditional margin, so
            the scenario effect is kept.
  eb_boot   New and nonparametric. Each trial draws one prior active game of the player (recency weights 0.6 season /
            0.4 last 3, as sim_v6's w()). It takes that game's per-team-play target and carry rates. Team volume is the
            team's mean plays x the volume index of a league team-game (pre-cutoff) whose own margin falls in the
            scenario. Outcomes come from a joint per-target bootstrap (catch and yards together) and a per-carry
            bootstrap, with sim_v6's opponent factors.

Scenarios are on the realized favorite margin f, using the edges of sunday/script_models.py (PR #159):
  favorite_controls f >= 10 | underdog_chases 3 <= f < 10 | competitive -3 <= f < 3 | residual f < -3 (upset)
The residual bin is simulated too, so the four bins add up to the unconditional game. Scenario probabilities come from
the same N(mu, 13.5) margin model.

Calibration: per (method, market) multipliers M = 1 + n/(n+K)*(median(actual/pred) - 1). They use sim_v6's rule
(K=30, MIN_N=20), fitted only on backtest weeks before the week being projected (calib_r1.json; see
tools/sim_v6_validate.py). Counts are rescaled with sim_v6.scale_count, yards are multiplied.

Research only. projection_ready stays false. No betting rule reads this.
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
if "SIMV6_SRC" not in os.environ:
    import simsrc
    simsrc.prepare()
import sim_v6_ab2144f0 as V6  # noqa: E402  (restored original, byte-identical blob; reads $SIMV6_SRC at import)

VERSION = "sim_v6r1"
IS_ORIGINAL_SIM_V6 = False
METHODS = ("mc_nb", "gr_share", "eb_boot")
SCENARIOS = {  # favorite-margin bins [lo, hi)
    "favorite_controls": (10.0, np.inf),
    "underdog_chases": (3.0, 10.0),
    "competitive": (-3.0, 3.0),
    "residual": (-np.inf, -3.0),
}
NAMED = ("favorite_controls", "underdog_chases", "competitive")
SD = V6.SD_MARGIN
MARKETS = ("passyds", "rec", "recyds", "rushyds", "rushrec")
QUANTS = tuple(round(q, 2) for q in np.arange(0.05, 0.96, 0.05))


def team_bin(lo: float, hi: float, team_is_fav: bool) -> tuple[float, float]:
    """Favorite-margin bin -> bin on this team's own margin."""
    return (lo, hi) if team_is_fav else (-hi, -lo)


def scenario_probs(spread: float, team_is_fav: bool) -> dict:
    mu = -float(spread)
    out = {}
    for s, (lo, hi) in SCENARIOS.items():
        a, b = team_bin(lo, hi, team_is_fav)
        out[s] = float(norm.cdf(b, mu, SD) - norm.cdf(a, mu, SD))
    return out


def trunc_normal(rng, mu, sd, a, b, n):
    """Inverse-CDF draws from N(mu, sd) truncated to [a, b)."""
    ca, cb = norm.cdf(a, mu, sd), norm.cdf(b, mu, sd)
    if cb - ca < 1e-9:  # bin has no mass under the normal: put draws at the nearest edge
        return np.full(n, a if np.isfinite(a) else b, dtype=float)
    u = rng.uniform(ca, cb, n)
    return norm.ppf(np.clip(u, 1e-12, 1 - 1e-12), mu, sd)


def _seed(base: int, *parts) -> int:
    return base + int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def summarize(x: np.ndarray, rungs, count: bool, rng) -> dict:
    x = np.asarray(x, dtype=float)
    jit = x + rng.uniform(-.5, .5, len(x)) if count else x
    return dict(mean=float(x.mean()), median=float(np.median(x)), cmedian=float(np.median(jit)),
                q={str(q): float(np.quantile(jit, q)) for q in QUANTS},
                rungs={str(k): float((x >= k).mean()) for k in rungs})


class Engine(V6.Engine):
    """sim_v6 data preparation (cutoff, team games, slopes, opponent factors) plus the three r1 methods."""

    def __init__(self, cutoff=None, n=100_000, seed=V6.SEED, calib=None, opp_shrink=1.0):
        super().__init__(cutoff=cutoff, calib=None, n=n, seed=seed)
        self.r1_calib = calib or {}
        self.opp_shrink = opp_shrink
        tg = self.tg.copy()
        lmean_pa = tg.groupby("posteam").pa.transform("mean")
        lmean_ra = tg.groupby("posteam").ra.transform("mean")
        tg["vi_pa"] = tg.pa / lmean_pa
        tg["vi_ra"] = tg.ra / lmean_ra
        self.vi = tg[["margin", "vi_pa", "vi_ra"]].reset_index(drop=True)
        p = self.p
        self.pass_rows = p[(p.pass_attempt == 1) & (p.sack != 1)]

    # ---------------------------------------------------------------- shared inputs (sim_v6 logic, unchanged)
    def _inputs(self, leg):
        name, mkt = leg["player"], leg["market"]
        team = V6.NV.get(leg["team"], leg["team"]); opp = V6.NV.get(leg["opp"], leg["opp"])
        qb = mkt in ("passyds", "comp")
        d, a, yc, ypc_rush, g = self.player(name, team, qb, leg.get("gsis"))
        PG = self.pos.get(g, "WR")
        if len(a) == 0:
            raise ValueError("no active games before cutoff")
        l3 = a.tail(3)
        cr = (a.rec.sum() + 1) / (a.tgt.sum() + 2); pgk = None if qb else PG
        sh = self.opp_shrink
        A_ypt, _ = self.oppadj(opp, pgk, "ypt", shrink=sh); A_cr, _ = self.oppadj(opp, pgk, "cr", shrink=sh)
        cr = min(cr * A_cr, 0.95); A_rec_y = A_ypt / A_cr
        pp, ru = self.pp, self.ru
        if len(yc):
            lg = (pp[pp.complete_pass == 1].receiving_yards.mean() if qb
                  else pp[(pp.pg == PG) & (pp.complete_pass == 1)].receiving_yards.mean())
            K = 100 if qb else 30; wv = len(yc) / (len(yc) + K); A_rec_y *= (wv * yc.mean() + (1 - wv) * lg) / yc.mean()
        A_ypc = 1.0
        if len(ypc_rush):
            lgA = ru.rushing_yards.mean(); pm = ypc_rush.mean(); wv = len(ypc_rush) / (len(ypc_rush) + 100)
            oppY = ru[ru.defteam == opp].rushing_yards.mean()
            A_ypc = ((wv * pm + (1 - wv) * lgA) / pm) * (oppY / lgA) if pm and lgA and oppY == oppY else 1.0
        # per-target joint outcomes for eb_boot
        col = "passer_player_id" if qb else "receiver_player_id"
        tr = self.pass_rows[self.pass_rows[col] == g]
        ycol = "passing_yards" if qb else "receiving_yards"
        tgt_pool = np.c_[tr.complete_pass.fillna(0).values, tr[ycol].fillna(0).values]
        return dict(name=name, mkt=mkt, team=team, opp=opp, qb=qb, a=a, l3=l3, yc=yc, ypc=ypc_rush, g=g, PG=PG,
                    cr=cr, A_cr=A_cr, A_rec_y=A_rec_y, A_ypc=A_ypc, tgt_pool=tgt_pool)

    # ---------------------------------------------------------------- the three methods
    def _w(self, I, col):
        a, l3 = I["a"], I["l3"]
        return 0.6 * a[col].mean() + 0.4 * l3[col].mean()

    def _mc_nb(self, rng, I, leg, scen, N):
        mu = -float(leg["spread"]); fav = bool(leg.get("team_is_fav", mu >= 0))
        lo, hi = SCENARIOS[scen] if scen else (-np.inf, np.inf)
        a_, b_ = team_bin(lo, hi, fav)
        Mg = trunc_normal(rng, mu, SD, a_, b_, N)
        M0 = rng.normal(mu, SD, N)

        def vol(col, b):
            F = float(np.exp(b * (Mg - mu)).mean() / np.exp(b * (M0 - mu)).mean()) if scen else 1.0
            mean = self._w(I, col) * F; var = I["a"][col].var(ddof=1)
            var = var * F if var == var else var
            return V6.nb(rng, mean, var, N)
        return self._outcomes(rng, I, leg, N, vol, kind="param")

    def _gr_share(self, rng, I, leg, scen, N):
        mu = -float(leg["spread"]); fav = bool(leg.get("team_is_fav", mu >= 0))
        lo, hi = SCENARIOS[scen] if scen else (-np.inf, np.inf)
        a_, b_ = team_bin(lo, hi, fav)
        a, l3, tg, team = I["a"], I["l3"], self.tg, I["team"]

        def vol(col, b):
            teamcol = "pa" if col == "tgt" else "ra"
            mean = self._w(I, col)
            share = (a[col] / a[teamcol]).clip(0, 0.999)
            m_s = share.mean(); v_s = max(share.var(ddof=1) if len(share) > 1 else 1e-3, 1e-4)
            if len(l3):
                m_s = min(0.6 * m_s + 0.4 * (l3[col] / l3[teamcol]).clip(0, 0.999).mean(), 0.995)
            kk = max(m_s * (1 - m_s) / v_s - 1, 2); sh = rng.beta(m_s * kk, (1 - m_s) * kk, N)
            tm = tg[tg.posteam == team][teamcol]; sig = np.std(np.log(tm), ddof=1)
            sig = sig if sig == sig else 0.15
            Mg = trunc_normal(rng, mu, SD, a_, b_, N) if scen else rng.normal(mu, SD, N)
            M0 = rng.normal(mu, SD, N)
            pace = rng.lognormal(0, sig, N)
            base = tm.mean() * np.exp(b * mu)
            TV = base * pace * np.exp(b * (Mg - mu))
            TV0 = base * rng.lognormal(0, sig, N) * np.exp(b * (M0 - mu))
            TV = TV * (mean / (m_s * TV0.mean()))   # unconditional normalisation keeps the script effect
            return rng.binomial(np.maximum(np.round(TV).astype(int), 0), np.clip(sh, 0, 1))
        return self._outcomes(rng, I, leg, N, vol, kind="param")

    def _eb_boot(self, rng, I, leg, scen, N):
        mu = -float(leg["spread"]); fav = bool(leg.get("team_is_fav", mu >= 0))
        a = I["a"].reset_index(drop=True); n_a = len(a)
        wts = np.full(n_a, 0.6 / n_a)
        k3 = min(3, n_a); wts[-k3:] += 0.4 / k3
        gi = rng.choice(n_a, N, p=wts / wts.sum())
        tm = self.tg[self.tg.posteam == I["team"]]
        vi = self.vi
        if scen:
            lo, hi = SCENARIOS[scen]; a_, b_ = team_bin(lo, hi, fav)
            pool = vi[(vi.margin >= a_) & (vi.margin < b_)]
            if len(pool) < 10:
                pool = vi
            vrow = rng.integers(0, len(pool), N); pool = pool.iloc[vrow]
        else:  # unconditional: draw a scenario by its probability, then a pool row
            probs = scenario_probs(leg["spread"], fav); names = list(SCENARIOS)
            pick = rng.choice(len(names), N, p=np.array([probs[s] for s in names]) / sum(probs.values()))
            idx = np.empty(N, dtype=int)
            for j, s in enumerate(names):
                lo, hi = SCENARIOS[s]; a_, b_ = team_bin(lo, hi, fav)
                cand = np.flatnonzero(((vi.margin >= a_) & (vi.margin < b_)).values)
                if len(cand) < 10:
                    cand = np.arange(len(vi))
                m = pick == j; idx[m] = rng.choice(cand, int(m.sum()))
            pool = vi.iloc[idx]

        def vol(col, b):
            teamcol, vcol = ("pa", "vi_pa") if col == "tgt" else ("ra", "vi_ra")
            rate = (a[col] / a[teamcol]).clip(0, 0.999).values[gi]
            plays = np.maximum(np.round(tm[teamcol].mean() * pool[vcol].values), 0).astype(int)
            return rng.binomial(plays, rate)
        return self._outcomes(rng, I, leg, N, vol, kind="boot")

    # ---------------------------------------------------------------- outcomes
    def _outcomes(self, rng, I, leg, N, vol, kind):
        mkt = I["mkt"]; x = np.zeros(N)
        if mkt in ("rec", "recyds", "rushrec", "passyds", "comp"):
            T = vol("tgt", self.bP)
            if kind == "boot" and len(I["tgt_pool"]):
                pool = I["tgt_pool"]; C = np.zeros(N); Y = np.zeros(N)
                for i in range(int(T.max())):
                    j = rng.integers(0, len(pool), N); on = T > i
                    C += np.where(on, pool[j, 0], 0); Y += np.where(on, pool[j, 1], 0)
                C = V6.scale_count(rng, C.astype(int), I["A_cr"]) if mkt in ("rec", "comp") else C
                # A_rec_y is per catch; boot yards are per target (incompletions are 0), so scale by A_ypt = A_rec_y*A_cr
                x = C.astype(float) if mkt in ("rec", "comp") else Y * I["A_rec_y"] * I["A_cr"]
            else:
                C = rng.binomial(T, np.clip(I["cr"], 0, 1))
                if mkt in ("rec", "comp"):
                    x = C.astype(float)
                else:
                    tot = np.zeros(N)
                    if len(I["yc"]):
                        for i in range(int(C.max())):
                            tot += np.where(C > i, rng.choice(I["yc"], N), 0)
                    x = tot * I["A_rec_y"]
        if mkt in ("rushyds", "rushrec"):
            Cr = vol("car", self.bR)
            cb = float(leg.get("carry_boost", 1.0))
            if cb != 1.0:
                Cr = V6.scale_count(rng, Cr, cb)
            tot = np.zeros(N)
            if len(I["ypc"]):
                for i in range(int(Cr.max())):
                    tot += np.where(Cr > i, rng.choice(I["ypc"], N), 0)
            x = x + tot * I["A_ypc"] * float(leg.get("ypc_boost", 1.0))
        return np.asarray(x, dtype=float)

    def mult(self, method, mkt):
        return float(self.r1_calib.get(method, {}).get(mkt, {}).get("M", 1.0))

    def sim_r1(self, leg, scenarios=(None,), raw=False, methods=METHODS, n=None):
        """Return {method: {scenario or 'all': summary}}. scenario None = unconditional game."""
        N = n or self.n
        I = self._inputs(leg); count = I["mkt"] in ("rec", "comp"); out = {}
        fn = {"mc_nb": self._mc_nb, "gr_share": self._gr_share, "eb_boot": self._eb_boot}
        for m in methods:
            M = 1.0 if raw else self.mult(m, I["mkt"]); out[m] = {}
            for s in scenarios:
                rng = np.random.default_rng(_seed(self.seed, VERSION, leg.get("game_id", ""), I["name"], I["mkt"], m, s))
                x = fn[m](rng, I, leg, s, N)
                x = V6.scale_count(rng, x.astype(int), M).astype(float) if count else x * M
                r = summarize(x, leg.get("rungs", []), count, rng); r["M"] = M; r["trials"] = int(N)
                out[m][s or "all"] = r
        info = dict(n_games=int(len(I["a"])), w_tgt=float(self._w(I, "tgt")), w_car=float(self._w(I, "car")),
                    cr=float(I["cr"]), A_ypc=float(I["A_ypc"]), A_rec_y=float(I["A_rec_y"]), pos=I["PG"], gsis=I["g"])
        return out, info
