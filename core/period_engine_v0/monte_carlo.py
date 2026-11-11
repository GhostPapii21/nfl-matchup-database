"""Monte Carlo period engine v0 (research).
MC: joint empirical bootstrap of opponent-adjusted? No — honest as-of:
  sample each team's quarter scoring vector from its as-of empirical games
  (home/away pooled), then assemble Q1-Q4 into one trajectory so H1=Q1+Q2.

Bias: UNIMPLEMENTED (no fitted residual calib).
GR: shared game-level multiplicative shock on both teams' quarter points,
    scale = empirical CV of team FG points as-of (data-driven, not hand edge coeffs).

No invented fitted coefficients. Production FAIL / research only.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import numpy as np
import pandas as pd
from reconstruct import as_of_mask
import hashlib

def stable_seed(base: int, week: int, game_id: str) -> int:
    """Deterministic seed independent of PYTHONHASHSEED / process hash randomization."""
    digest = hashlib.sha256(f"{base}|{week}|{game_id}".encode()).hexdigest()
    return (base + week * 1000 + int(digest[:8], 16)) % (2**31 - 1)

from settlement import (
    PeriodScore, settle_spread_2way, settle_winner_3way,
    settle_total_2way, settle_team_total_2way,
)

QUARTERS = ("q1", "q2", "q3", "q4")


@dataclass
class ModelStatus:
    monte_carlo: str = "IMPLEMENTED_EMPIRICAL_BOOTSTRAP"
    bias: str = "UNIMPLEMENTED_NO_FITTED_CALIB"
    game_randomness: str = "IMPLEMENTED_SHARED_GAME_SHOCK_UNFITTED_SCALE"


STATUS = ModelStatus()


def _sample_team_quarters(rng: np.random.Generator, hist: np.ndarray, n: int, replace_ok: bool = True) -> np.ndarray:
    """hist shape (n_games, 4) -> samples (n, 4)."""
    if hist.size == 0:
        return np.full((n, 4), np.nan)
    idx = rng.integers(0, len(hist), size=n)
    return hist[idx]


def team_game_matrix(periods: pd.DataFrame, team: str) -> np.ndarray:
    """Rows = games involving team; cols = q1..q4 scored by team, then q1..q4 allowed (same game)."""
    H = [f"q{i}_home" for i in range(1, 5)]
    A = [f"q{i}_away" for i in range(1, 5)]
    home = periods.home_team.to_numpy() == team
    away = periods.away_team.to_numpy() == team
    rows = np.zeros((int(home.sum() + away.sum()), 8))
    if len(rows) == 0:
        return rows
    ph, pa = periods[H].to_numpy(float), periods[A].to_numpy(float)
    # keep the original row order of `periods` (matches the legacy iterrows order)
    order = np.flatnonzero(home | away)
    is_home = home[order]
    rows[:, :4] = np.where(is_home[:, None], ph[order], pa[order])
    rows[:, 4:] = np.where(is_home[:, None], pa[order], ph[order])
    return rows


def team_quarter_matrix(periods: pd.DataFrame, team: str) -> np.ndarray:
    """Rows = games involving team; cols = q1..q4 points scored by team."""
    return team_game_matrix(periods, team)[:, :4]


SAMPLING_MODES = ("independent", "matchup_pair")
GR_SCALES = ("within_game_covariance", "legacy_total_cv")


def simulate_game(
    periods_asof: pd.DataFrame,
    home: str,
    away: str,
    *,
    n: int = 100_000,
    seed: int = 20261105,
    apply_gr: bool = False,
    sampling: str = "independent",
    gr_scale: str = "within_game_covariance",
) -> dict:
    """Return joint trajectories and summaries. Bias always absent.

    sampling:
      "independent"  (default, legacy) each team's quarter vector is drawn from its own
                     as-of games, independently of the other team.
      "matchup_pair" each trial draws ONE real as-of game, with probability 1/2 from the
                     home team's games (home = what it scored, away = what it allowed) and
                     otherwise from the away team's games (away = scored, home = allowed).
                     The opponent's defence enters (home mean = average of home offence and
                     away defence allowed), and real within-game structure is kept: the
                     negative quarter-level score correlation, key numbers and tie rates.
    gr_scale (only when apply_gr):
      "within_game_covariance" (default) shared shock variance = max(0, Cov(scored, allowed))
                     / (mean scored * mean allowed) over the two teams' as-of games, so the
                     shock adds exactly the observed same-game covariance.
      "legacy_total_cv" the original rule: sigma from the total CV of team points. The bootstrap
                     already carries that variance, so this roughly doubles Var(team points)
                     (factor 2 + CV^2) and forces corr(home, away) = 1 / (2 + CV^2) ~ 0.47,
                     while observed NFL corr is ~0. Kept for reproducing old runs.
    """
    if sampling not in SAMPLING_MODES:
        raise ValueError(f"sampling must be one of {SAMPLING_MODES}")
    if gr_scale not in GR_SCALES:
        raise ValueError(f"gr_scale must be one of {GR_SCALES}")
    rng = np.random.default_rng(seed)
    Gh = team_game_matrix(periods_asof, home)
    Ga = team_game_matrix(periods_asof, away)
    Hh, Ha = Gh[:, :4], Ga[:, :4]
    status = {
        "monte_carlo": STATUS.monte_carlo,
        "bias": STATUS.bias,
        "game_randomness": STATUS.game_randomness if apply_gr else "NOT_APPLIED_THIS_CALL",
        "home_games_asof": int(len(Hh)),
        "away_games_asof": int(len(Ha)),
        "asof_insufficient": bool(len(Hh) < 1 or len(Ha) < 1),
        "sampling": sampling,
    }
    if status["asof_insufficient"]:
        return {"status": status, "n": 0, "error": "ASOF_INSUFFICIENT_HISTORY"}

    if sampling == "independent":
        hq = _sample_team_quarters(rng, Hh, n)
        aq = _sample_team_quarters(rng, Ha, n)
    else:
        use_home = rng.random(n) < 0.5
        gi = Gh[rng.integers(0, len(Gh), size=n)]
        gj = Ga[rng.integers(0, len(Ga), size=n)]
        hq = np.where(use_home[:, None], gi[:, :4], gj[:, 4:])
        aq = np.where(use_home[:, None], gi[:, 4:], gj[:, :4])
        status["matchup_pair_home_team_share"] = float(use_home.mean())

    if apply_gr:
        # Shared multiplicative shock S (E[S]=1) on both teams' points.
        fg_h = Hh.sum(axis=1)
        fg_a = Ha.sum(axis=1)
        pool = np.concatenate([fg_h, fg_a])
        mu = pool.mean()
        cv = float(pool.std(ddof=1) / mu) if mu > 0 else 0.0
        if gr_scale == "legacy_total_cv":
            shock_var = cv**2
        else:
            # Cov(h*S, a*S) = E[h]E[a]Var(S) for independent h, a: match the observed same-game covariance.
            scored = np.concatenate([Gh[:, :4].sum(axis=1), Ga[:, :4].sum(axis=1)])
            allowed = np.concatenate([Gh[:, 4:].sum(axis=1), Ga[:, 4:].sum(axis=1)])
            cov = float(np.cov(scored, allowed)[0, 1]) if len(scored) > 1 else 0.0
            denom = float(scored.mean() * allowed.mean())
            shock_var = max(0.0, cov) / denom if denom > 0 else 0.0
            status["gr_within_game_cov"] = cov
            if cov <= 0:
                status["gr_note"] = "OBSERVED_SAME_GAME_COVARIANCE_NONPOSITIVE_SHOCK_OFF"
        status["gr_scale"] = gr_scale
        sigma = float(np.sqrt(np.log(1 + shock_var))) if shock_var > 0 else 0.0
        shock = rng.lognormal(mean=-0.5 * sigma**2, sigma=sigma, size=n)
        hq = hq * shock[:, None]
        aq = aq * shock[:, None]
        status["gr_sigma_empirical"] = sigma
        status["gr_cv_empirical"] = cv
        status["game_randomness"] = STATUS.game_randomness

    # discrete football-ish rounding to nearest int >=0
    hq = np.maximum(np.rint(hq), 0).astype(int)
    aq = np.maximum(np.rint(aq), 0).astype(int)

    q = {f"q{i+1}": (hq[:, i], aq[:, i]) for i in range(4)}
    h1_h = hq[:, 0] + hq[:, 1]
    h1_a = aq[:, 0] + aq[:, 1]
    reg_h = hq.sum(axis=1)
    reg_a = aq.sum(axis=1)

    # Coherent FG path: start from regulation; OT only if reg tied.
    # OT increments sampled jointly from as-of games that went_ot (observed fg-reg >=0).
    ot_games = periods_asof[periods_asof["went_ot"].astype(bool)] if "went_ot" in periods_asof.columns else periods_asof.iloc[0:0]
    ot_inc = []
    for _, r in ot_games.iterrows():
        dh = int(r.fg_home) - int(r.reg_home)
        da = int(r.fg_away) - int(r.reg_away)
        if dh >= 0 and da >= 0 and (dh + da) > 0:
            ot_inc.append((dh, da))
    ot_inc = np.asarray(ot_inc, dtype=int) if ot_inc else np.zeros((0, 2), dtype=int)

    fg_h = reg_h.copy()
    fg_a = reg_a.copy()
    reg_tie = reg_h == reg_a
    n_ot = int(reg_tie.sum())
    if n_ot and len(ot_inc):
        idx = rng.integers(0, len(ot_inc), size=n_ot)
        fg_h[reg_tie] = reg_h[reg_tie] + ot_inc[idx, 0]
        fg_a[reg_tie] = reg_a[reg_tie] + ot_inc[idx, 1]
    elif n_ot and not len(ot_inc):
        # No as-of OT observations: leave fg=reg; declare limitation
        status["ot_limitation"] = "REG_TIE_BUT_NO_ASOF_OT_GAMES_FG_EQUALS_REG"
    status["fg_sampling"] = "joint_reg_then_ot_if_tied"
    status["reg_sampling"] = "q1_q4_bootstrap_regulation_only"
    status["source_composition"] = "league_team_quarter_bootstrap_not_possession_engine"

    def summ(h, a):
        return {
            "home_mean": float(h.mean()), "away_mean": float(a.mean()),
            "home_median": float(np.median(h)), "away_median": float(np.median(a)),
            "margin_home_mean": float((h - a).mean()),
            "margin_home_median": float(np.median(h - a)),
            "total_mean": float((h + a).mean()),
            "total_median": float(np.median(h + a)),
        }

    outcome_meta = {
        "reg_scope": "regulation_only",
        "fg_scope": "includes_ot_if_reg_tied",
        "ot_rule": "OT increments only when reg_home==reg_away; else fg=reg",
        "ot_increment_source": "asof_went_ot_games_fg_minus_reg",
        "n_reg_ties": n_ot,
        "n_asof_ot_templates": int(len(ot_inc)),
        "source_composition": status["source_composition"],
    }

    out = {
        "status": status,
        "n": n,
        "seed": seed,
        "outcome_meta": outcome_meta,
        "settlement_paths": outcome_meta,
        "summaries": {
            "q1": summ(*q["q1"]), "q2": summ(*q["q2"]), "q3": summ(*q["q3"]), "q4": summ(*q["q4"]),
            "h1": summ(h1_h, h1_a),
            "reg": summ(reg_h, reg_a),
            "fg": summ(fg_h, fg_a),
        },
        "arrays": {
            "q1_home": q["q1"][0], "q1_away": q["q1"][1],
            "q2_home": q["q2"][0], "q2_away": q["q2"][1],
            "q3_home": q["q3"][0], "q3_away": q["q3"][1],
            "q4_home": q["q4"][0], "q4_away": q["q4"][1],
            "h1_home": h1_h, "h1_away": h1_a,
            "reg_home": reg_h, "reg_away": reg_a,
            "fg_home": fg_h, "fg_away": fg_a,
            "reg_tied": reg_tie,
            "ot_played": (fg_h > reg_h) | (fg_a > reg_a),
        },
    }
    return out


def raw_probs_from_sim(sim: dict, *, period: str, market: str, line: float, side: str) -> dict:
    """Raw model probabilities with push mass retained.

    For two-way markets:
      p_win / p_push / p_lose unconditional (sum to 1)
      p_win_decisive = P(win | not push) for comparison to two-way no-vig when pushes refunded
      monte_carlo = p_win (unconditional; preserved legacy key — NOT decisive)
    For winner_3way: p_side / p_opp / p_tie (sum to 1); monte_carlo = p_side
    """
    if sim.get("error"):
        return {"monte_carlo": None, "bias": "UNIMPLEMENTED", "game_randomness": None, "error": sim["error"]}
    A = sim["arrays"]
    # period fg uses final-including-OT vectors when present
    h, a = A[f"{period}_home"], A[f"{period}_away"]
    out = {"bias": "UNIMPLEMENTED", "game_randomness": None}
    def wpl(adj):
        # same rule as settlement.settle_*_2way: push iff |adj| < 1e-12, win iff adj > 0
        adj = np.asarray(adj, dtype=float)
        push = np.abs(adj) < 1e-12
        win = (adj > 0) & ~push
        p_win, p_push = float(win.mean()), float(push.mean())
        p_lose = float(1.0 - p_win - p_push) if len(adj) else 0.0
        decisive = 1.0 - p_push
        return dict(p_win=p_win, p_push=p_push, p_lose=p_lose,
                    p_win_decisive=(p_win / decisive if decisive > 0 else None), monte_carlo=p_win)

    if market == "spread_2way":
        margin = h - a if side == "home" else a - h
        out.update(wpl(margin + line))
        out["settlement_note"] = "unconditional W/P/L; compare p_win_decisive to two-way no-vig when pushes refunded"
    elif market == "winner_3way":
        margin = h - a if side == "home" else a - h
        p_side = float((margin > 0).mean())
        p_opp = float((margin < 0).mean())
        p_tie = float((margin == 0).mean())
        out.update(p_side=p_side, p_opp=p_opp, p_tie=p_tie, monte_carlo=p_side, monte_carlo_tie=p_tie)
    elif market == "total_2way":
        tot = (h + a).astype(float)
        if side not in ("over", "under"):
            raise ValueError(side)
        out.update(wpl(tot - line if side == "over" else line - tot))
    elif market == "team_total_2way":
        pts = (h if side.startswith("home") else a).astype(float)
        ou = "over" if side.endswith("over") else "under"
        out.update(wpl(pts - line if ou == "over" else line - pts))
    else:
        raise ValueError(market)
    return out


def raw_probs_mc_and_gr(periods_asof, home, away, **market_kw) -> dict:
    """Run MC and GR as distinct structures; Bias remains unimplemented.

    Propagates full push/decisive fields from raw_probs_from_sim for both branches.
    monte_carlo / game_randomness remain unconditional win rates; decisive is separate.
    """
    seed = market_kw.pop("seed", 20261105)
    n = market_kw.pop("n", 50_000)
    sampling = market_kw.pop("sampling", "independent")
    gr_scale = market_kw.pop("gr_scale", "within_game_covariance")
    base = simulate_game(periods_asof, home, away, n=n, seed=seed, apply_gr=False, sampling=sampling)
    gr = simulate_game(periods_asof, home, away, n=n, seed=seed + 1, apply_gr=True, sampling=sampling, gr_scale=gr_scale)
    rb = raw_probs_from_sim(base, **market_kw)
    rg = raw_probs_from_sim(gr, **market_kw)
    out = {
        "monte_carlo": rb.get("monte_carlo"),
        "bias": "UNIMPLEMENTED",
        "game_randomness": rg.get("monte_carlo"),
        "mc_status": base.get("status"),
        "gr_status": gr.get("status"),
        "mc_error": base.get("error"),
        "gr_error": gr.get("error"),
        "tie_mc": rb.get("monte_carlo_tie") or rb.get("p_tie"),
        "tie_gr": rg.get("monte_carlo_tie") or rg.get("p_tie"),
        "comparison_basis_recommended": "p_win_decisive_vs_two_way_novig",
        "outcome_meta": base.get("outcome_meta"),
    }
    # propagate MC push/decisive / 3-way
    for k in ("p_win", "p_push", "p_lose", "p_win_decisive", "p_side", "p_opp", "p_tie", "settlement_note"):
        if k in rb:
            out[k] = rb[k]
    # GR decisive fields under explicit names
    if "p_win_decisive" in rg:
        out["p_win_decisive_gr"] = rg["p_win_decisive"]
        out["gr_detail"] = {k: rg[k] for k in ("p_win", "p_push", "p_lose", "p_win_decisive") if k in rg}
    elif "p_side" in rg:
        out["gr_detail"] = {k: rg[k] for k in ("p_side", "p_opp", "p_tie") if k in rg}
    return out
