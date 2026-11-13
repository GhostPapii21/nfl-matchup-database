"""NFL-75 sim bug fix (refs NFL-75, Linear comment 6ce79e04): QB rush YPC prior + separate kneel model.

Opt-in only: an engine uses this module only when a leg carries ``qb_rush_prior=True`` AND the rusher's
position_group is QB AND the market is rushyds / rushrec. Without that key every engine path is unchanged (the
Phase 4 W8-9 reproduction tests still hold bit-for-bit / within 1e-12).

The bug (all three vendored engines, sim_v5 / sim_v6 / sim_v6_fix):
  * a rusher's play-level YPC sample includes kneels (qb_kneel == 1, ~-1 yd each) and kneels count as carries;
  * that YPC is shrunk with weight n/(n+100) toward ``ru.rushing_yards.mean()``, the league mean over ALL rushers
    (RB-dominated, 4.18 on 2026 W1-9 incl kneels), not toward a QB mean.
  Scramble QBs get pulled down (Maye A_ypc .913), kneel-heavy QBs get pulled up (Geno A_ypc 1.570).

The fix (touches only the QB rush YPC prior and kneel handling; shrink weight K=100, opponent strength, volume model
and fitted multipliers are unchanged):
  * QB non-kneel carries / YPC: kneels are removed from the player's YPC sample and from his per-game carry counts.
  * The shrink target is the league QB non-kneel YPC (rushers with position_group QB, before the cutoff).
  * The opponent factor is opp-allowed / league YPC over non-kneel rushes (kneels removed from both sides).
  * Kneels are modeled separately: team kneel count per game is resampled from the league's team-game kneel counts
    before the cutoff, split by whether the team won (final margin > 0); the game state is drawn per trial as
    margin ~ N(-spread, SD_MARGIN). Each kneel's yards are resampled from the league's kneel yards. The QB is
    assumed to take all of his team's kneels (starter). Kneel yards are added after the YPC / opponent factor
    (official settlement counts kneels), and before the engine's fitted per-market multiplier, like all rush yards.
Research only; projection_ready stays false."""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

QB = "QB"
SD_MARGIN = 13.5
K_YPC = 100          # unchanged engine shrink weight n/(n+100)


def kneel_mask(ru: pd.DataFrame) -> np.ndarray:
    if "qb_kneel" not in ru:
        return np.zeros(len(ru), dtype=bool)
    return (pd.to_numeric(ru["qb_kneel"], errors="coerce").fillna(0).values == 1)


def qb_rush_inputs(ru: pd.DataFrame, gsis: str, opp: str, game_ids) -> dict:
    """ru: rush_attempt == 1 rows before the cutoff with a ``pg`` (position_group) column.
    Returns the QB's non-kneel YPC sample, non-kneel carries per active game (aligned to game_ids), the league QB
    non-kneel YPC prior and the non-kneel opponent YPC ratio."""
    kn = kneel_mask(ru)
    nk = ru[~kn]
    mine = nk[nk.rusher_player_id == gsis]
    car = mine.groupby("game_id").size().reindex(list(game_ids), fill_value=0).astype(int).values
    lg_all = float(nk.rushing_yards.mean()) if len(nk) else float("nan")
    opp_y = float(nk[nk.defteam == opp].rushing_yards.mean()) if (nk.defteam == opp).any() else float("nan")
    opp_ratio = opp_y / lg_all if lg_all and lg_all == lg_all and opp_y == opp_y else 1.0
    qbr = nk[nk.pg == QB].rushing_yards
    return dict(ypc=mine.rushing_yards.dropna().values, car=car, lg_qb=float(qbr.mean()) if len(qbr) else float("nan"),
                lg_all_nk=lg_all, opp_ratio=float(opp_ratio), n_kneels_player=int(kn[ru.rusher_player_id.values == gsis].sum()))


def ypc_factor(pm: float, n: int, prior: float, opp_mult: float, k: float = K_YPC) -> float:
    """Same algebra as the engines, ((w*pm + (1-w)*prior) / pm) * opp_mult with w = n/(n+k), but prior = QB mean.
    No sample, a non-positive player mean (the multiplicative form cannot move it) or an unknown prior -> opp only."""
    if not n or pm is None or not pm > 0:
        return 1.0 if not n else float(opp_mult)
    if prior != prior:
        return float(opp_mult)
    w = n / (n + k)
    return float(((w * pm + (1 - w) * prior) / pm) * opp_mult)


def kneel_table(ru: pd.DataFrame, tg: pd.DataFrame) -> dict:
    """League team-game kneel counts (split by final margin > 0) and per-kneel yards, before the cutoff.
    tg: the engine's team-game table (game_id, posteam, margin)."""
    kn = kneel_mask(ru)
    k = ru[kn]
    cnt = k.groupby(["game_id", "posteam"]).size().rename("kneels").reset_index()
    t = tg[["game_id", "posteam", "margin"]].merge(cnt, on=["game_id", "posteam"], how="left").fillna({"kneels": 0})
    return dict(lead=t[t.margin > 0].kneels.astype(int).values, other=t[t.margin <= 0].kneels.astype(int).values,
                yards=k.rushing_yards.fillna(0).astype(float).values)


def kneel_rng(seed: int, name: str, mkt: str, mode: str) -> np.random.Generator:
    """Separate stream so the kneel draws never shift the engine's own random stream."""
    return np.random.default_rng(seed + int(hashlib.md5(f"{name}|{mkt}|{mode}|kneel".encode()).hexdigest()[:6], 16))


def sim_kneel_yards(rng: np.random.Generator, spread: float, n: int, table: dict, sd: float = SD_MARGIN) -> np.ndarray:
    """Per-trial kneel yards: game state margin ~ N(-spread, sd); kneel count from the lead / not-lead league counts."""
    lead_c, oth_c, yds = table["lead"], table["other"], table["yards"]
    if not len(yds) or (not len(lead_c) and not len(oth_c)):
        return np.zeros(n)
    lead = rng.normal(-float(spread), sd, n) > 0
    c_l = rng.choice(lead_c, n) if len(lead_c) else np.zeros(n, dtype=int)
    c_o = rng.choice(oth_c, n) if len(oth_c) else np.zeros(n, dtype=int)
    cnt = np.where(lead, c_l, c_o)
    tot = np.zeros(n)
    for i in range(int(cnt.max()) if n else 0):
        tot += np.where(cnt > i, rng.choice(yds, n), 0.0)
    return tot
