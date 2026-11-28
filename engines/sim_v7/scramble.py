"""Pressure-induced QB scrambling, separated from designed QB runs.

All rates are measured from nflverse play-by-play before `source_cutoff`:
  - qb_dropback, qb_scramble, sack, pass_attempt, rush_attempt, qb_kneel
  - Designed QB runs = rush_attempt by a QB where qb_scramble != 1 and qb_kneel != 1
  - Scrambles are never double-counted into designed rush volume

Board pressure_rate (coverage_profile) supplies the matchup pressure probability when present;
otherwise the QB's own historical pressure/sack proxy is used.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from . import data as D

SCRAMBLE_COLS = [
    "game_id", "game_date", "season", "week", "posteam",
    "passer_player_id", "rusher_player_id",
    "qb_dropback", "qb_scramble", "qb_kneel", "qb_spike", "sack", "qb_hit",
    "pass_attempt", "rush_attempt", "complete_pass", "rushing_yards",
    "pass_touchdown", "rush_touchdown", "yardline_100",
]


@lru_cache(maxsize=2)
def _pbp_scramble(cutoff: str) -> pd.DataFrame:
    """Load pbp columns needed for scramble modeling (cached per cutoff)."""
    import pyarrow.parquet as pq
    frames = []
    for season, rel in D.PBP_FILES.items():
        path = f"{D.REPO}/{rel}"
        try:
            names = set(pq.read_schema(path).names)
            cols = [c for c in SCRAMBLE_COLS if c in names]
            extra = [c for c in ("season_type",) if c in names and c not in cols]
            p = pd.read_parquet(path, columns=cols + extra)
        except Exception:
            continue
        if "season_type" in p.columns:
            p = p[p.season_type == "REG"].drop(columns=["season_type"])
        p = p[p.game_date.astype(str) < cutoff]
        frames.append(p)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _qb_ids() -> set[str]:
    pl = D.load_players()
    return set(pl[pl.position_group == "QB"].gsis_id.astype(str))


def qb_scramble_profile(qb_id: str, cutoff: str, board_pressure_rate: float | None = None,
                        min_dropbacks: int = 40) -> dict:
    """Measured scramble / sack / throw rates for one QB before cutoff."""
    p = _pbp_scramble(cutoff)
    if p.empty or not qb_id:
        return {"status": "MISSING", "qb_id": qb_id, "kind": "measured"}
    db = p[(p.qb_dropback == 1) & (p.passer_player_id == qb_id)]
    if len(db) < min_dropbacks:
        # league prior from all QBs
        league = p[p.qb_dropback == 1]
        use = league
        sample = "league_prior"
    else:
        use = db
        sample = "qb"
    n = len(use)
    sack = float((use.sack == 1).mean()) if n else 0.07
    # nflverse: scrambles are tagged on dropbacks and are mutually exclusive with sack/hit
    scramble = float((use.qb_scramble == 1).mean()) if n else 0.05
    throw = max(0.0, 1.0 - sack - scramble)
    complete_given_throw = float(use[(use.sack != 1) & (use.qb_scramble != 1)].complete_pass.mean()) if n else 0.65
    scr_rows = use[use.qb_scramble == 1]
    scr_ypc = float(scr_rows.rushing_yards.mean()) if len(scr_rows) else 6.5
    scr_ypc_var = float(scr_rows.rushing_yards.var()) if len(scr_rows) > 1 else 25.0
    scr_td_rate = float(scr_rows.rush_touchdown.mean()) if len(scr_rows) else 0.02

    # Designed QB runs (exclude kneels and scrambles)
    qbs = _qb_ids()
    designed = p[(p.rush_attempt == 1) & (p.qb_scramble != 1) & (p.qb_kneel != 1) &
                 (p.rusher_player_id == qb_id)]
    if len(designed) < 5:
        designed_all = p[(p.rush_attempt == 1) & (p.qb_scramble != 1) & (p.qb_kneel != 1) &
                         (p.rusher_player_id.isin(qbs))]
        des_ypc = float(designed_all.rushing_yards.mean()) if len(designed_all) else 2.5
        des_rate_per_game = float(designed_all.groupby("game_id").size().mean()) if len(designed_all) else 1.0
        des_n = len(designed_all)
        des_sample = "league_prior"
    else:
        des_ypc = float(designed.rushing_yards.mean())
        des_rate_per_game = float(designed.groupby("game_id").size().mean())
        des_n = len(designed)
        des_sample = "qb"

    # Pressure probability: board matchup rate preferred; else sack+historical proxy
    # Historical: treat sack as realized pressure endpoint; board pressure_rate is pre-snap look
    if board_pressure_rate is not None and 0 <= board_pressure_rate <= 1:
        p_pressure = float(board_pressure_rate)
        pressure_source = "board.coverage_profile.pressure_rate"
    else:
        p_pressure = float(np.clip(sack / 0.25, 0.10, 0.50))  # crude map from sack rate
        pressure_source = "inferred_from_sack_rate"

    # Scramble probability conditional on pressure.
    # PBP tags scramble exclusive of qb_hit, so estimate via: P(scramble) / P(pressure_proxy)
    # Use sack rate as lower bound of pressure; board pressure as the matchup rate.
    # Assume scrambles occur under pressure: P(scramble|pressure) = P(scramble)/P(pressure)
    p_scr_given_pressure = float(np.clip(scramble / max(p_pressure, 0.05), 0.02, 0.55))
    # Residual scramble when "clean" kept near 0 (most scrambles are pressure responses)
    p_scr_given_clean = float(np.clip(0.15 * scramble, 0.0, 0.05))
    p_sack_given_pressure = float(np.clip(sack / max(p_pressure, 0.05), 0.05, 0.60))
    p_throwaway_given_pressure = float(np.clip(0.08, 0.02, 0.20))  # league-ish; not play-tagged in free pbp

    return {
        "status": "MEASURED" if sample == "qb" else "EXPERIMENTAL_UNVALIDATED",
        "kind": "measured",
        "qb_id": qb_id,
        "source_cutoff": cutoff,
        "dropbacks": int(len(db)),
        "sample": sample,
        "p_sack": sack,
        "p_scramble": scramble,
        "p_throw": throw,
        "completion_given_throw": complete_given_throw,
        "scramble_ypc": scr_ypc,
        "scramble_ypc_var": max(scr_ypc_var, 9.0),
        "scramble_td_rate": scr_td_rate,
        "designed": {
            "sample": des_sample,
            "n": des_n,
            "ypc": des_ypc,
            "attempts_per_game": des_rate_per_game,
            "kind": "measured" if des_sample == "qb" else "league_prior",
        },
        "pressure": {
            "p_pressure": p_pressure,
            "source": pressure_source,
            "p_scramble_given_pressure": p_scr_given_pressure,
            "p_scramble_given_clean": p_scr_given_clean,
            "p_sack_given_pressure": p_sack_given_pressure,
            "p_throwaway_given_pressure": p_throwaway_given_pressure,
        },
        "note": "designed runs and scrambles separated; scramble yards not added to designed RA share",
    }


def apply_scramble_to_dropbacks(rng, n: int, dropbacks: np.ndarray, profile: dict) -> dict:
    """Vectorized dropback outcomes: throw / sack / scramble / throwaway.

    dropbacks: intended pass attempts (PA) as a proxy for dropbacks.
    Returns arrays: thrown, sacked, scrambled, throwaway, scramble_yds, scramble_td,
    and effective pass attempts after removing sack/scramble/throwaway.
    """
    pr = profile.get("pressure") or {}
    p_press = float(pr.get("p_pressure", 0.28))
    p_scr_p = float(pr.get("p_scramble_given_pressure", 0.15))
    p_scr_c = float(pr.get("p_scramble_given_clean", 0.01))
    p_sack_p = float(pr.get("p_sack_given_pressure", 0.25))
    p_ta_p = float(pr.get("p_throwaway_given_pressure", 0.08))
    ypc = float(profile.get("scramble_ypc", 6.5))
    ypv = float(profile.get("scramble_ypc_var", 25.0))
    td_r = float(profile.get("scramble_td_rate", 0.02))

    PA = np.asarray(dropbacks, dtype=np.int64)
    press = rng.binomial(PA, p_press)
    clean = PA - press
    scrambled_p = rng.binomial(press, p_scr_p)
    sacked = rng.binomial(press - scrambled_p, min(p_sack_p, 0.95))
    rem_p = press - scrambled_p - sacked
    throwaway = rng.binomial(np.maximum(rem_p, 0), min(p_ta_p, 0.95))
    thrown_p = rem_p - throwaway
    scrambled_c = rng.binomial(clean, p_scr_c)
    thrown_c = clean - scrambled_c
    scrambled = scrambled_p + scrambled_c
    thrown = np.maximum(thrown_p, 0) + thrown_c

    # scramble yards ~ gamma
    a = max(ypc, 0.5) ** 2 / max(ypv, 1.0)
    th = max(ypv, 1.0) / max(ypc, 0.5)
    scramble_yds = np.zeros(n)
    pos = scrambled > 0
    scramble_yds[pos] = rng.gamma(scrambled[pos] * a, th)
    scramble_td = rng.binomial(scrambled, td_r)

    return {
        "thrown": thrown.astype(np.float32),
        "sacked": sacked.astype(np.float32),
        "scrambled": scrambled.astype(np.float32),
        "throwaway": throwaway.astype(np.float32),
        "scramble_yds": scramble_yds.astype(np.float32),
        "scramble_td": scramble_td.astype(np.float32),
        "designed_qb_att_mean": float((profile.get("designed") or {}).get("attempts_per_game") or 0.0),
        "designed_ypc": float((profile.get("designed") or {}).get("ypc") or 2.5),
    }
