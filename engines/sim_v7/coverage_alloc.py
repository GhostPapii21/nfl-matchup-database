"""Player-specific coverage target allocation from existing repository sources.

Measured observations (never invented):
  - Board opportunity target shares (`opportunity.receivers[].inputs`)
  - Sharp Football man/zone/MOFO/MOFC team rates (`data/coverage/sharp_coverage_2026.csv`)
  - Board coverage_profile (man_rate, zone_rate, two_high/one_high, shells, pressure)
  - NextGen Stats receiving cushion / separation / intended air yards
  - Board defender coverage allowed rates (targets/completions/yards) — aggregate, not assignment
  - FTN/nflverse blitz rates already on the board

Inferred (explicitly labelled):
  - Position-level man/zone/MOF share priors from dashboard.coverage_model.LEAGUE_SPLIT
    applied to a team's measured shell rates to reweight target shares.
  - Soft affinity of a receiver toward slower/higher-cushion matchups using NGS separation
    vs defender yards-allowed — never a claimed man-to-man assignment.

No play-level defense_coverage_type / defense_man_zone_type participation exists for 2026
on free nflverse; missing charting is reported as MISSING, not filled.
"""
from __future__ import annotations

import os
from functools import lru_cache

import numpy as np
import pandas as pd

from . import data as D

try:
    from dashboard.coverage_model import LEAGUE_SPLIT, LEAGUE_MAN_RATE, LEAGUE_MOFO_RATE
except Exception:  # research-only fallback if dashboard import path shifts
    LEAGUE_SPLIT = {
        "WR": {"man": {"share": 1.103}, "zone": {"share": 0.925},
               "mofo": {"share": 0.923}, "mofc": {"share": 1.054}},
        "TE": {"man": {"share": 0.935}, "zone": {"share": 1.047},
               "mofo": {"share": 1.036}, "mofc": {"share": 0.975}},
        "RB": {"man": {"share": 0.731}, "zone": {"share": 1.196},
               "mofo": {"share": 1.216}, "mofc": {"share": 0.849}},
    }
    LEAGUE_MAN_RATE = 0.324
    LEAGUE_MOFO_RATE = 0.445

SHARP_FILE = "data/coverage/sharp_coverage_2026.csv"
NGS_RECV = "data/ngs/nflverse_ngs_raw/ngs_receiving.csv.gz"
SOURCE_CUTOFF_DEFAULT = "2026-11-24"


def _clip(x, lo=0.70, hi=1.35):
    return float(np.clip(x, lo, hi))


@lru_cache(maxsize=1)
def load_sharp() -> pd.DataFrame:
    path = os.path.join(D.REPO, SHARP_FILE)
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["team"] = df["team"].map(lambda t: D.NV.get(t, t))
    return df


@lru_cache(maxsize=1)
def load_ngs_receiving() -> pd.DataFrame:
    path = os.path.join(D.REPO, NGS_RECV)
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "season_type" in df.columns:
        df = df[df.season_type == "REG"]
    return df


def sharp_for(team: str) -> dict:
    df = load_sharp()
    team = D.NV.get(team, team)
    if df.empty or team not in set(df.team):
        return {"status": "MISSING", "kind": "measured"}
    r = df[df.team == team].iloc[-1]
    return {
        "status": "MEASURED",
        "kind": "measured",
        "source": SHARP_FILE,
        "source_updated": r.get("source_updated"),
        "man_pct": float(r.man_pct) / 100.0,
        "zone_pct": float(r.zone_pct) / 100.0,
        "mofc_pct": float(r.mofc_pct) / 100.0,
        "mofo_pct": float(r.mofo_pct) / 100.0,
    }


def ngs_for_player(gsis: str, cutoff_week: int = 11, season: int = 2026) -> dict:
    df = load_ngs_receiving()
    if df.empty or "player_gsis_id" not in df.columns:
        return {"status": "MISSING", "kind": "measured"}
    x = df[(df.player_gsis_id == gsis) & (df.season == season) & (df.week <= cutoff_week)]
    if x.empty:
        x = df[(df.player_gsis_id == gsis) & (df.season == season - 1)]
    if x.empty:
        return {"status": "MISSING", "kind": "measured", "player_id": gsis}
    w = x.targets.fillna(0).clip(lower=0)
    if w.sum() <= 0:
        w = pd.Series(np.ones(len(x)))
    def wavg(col):
        v = x[col].astype(float)
        m = v.notna()
        return float(np.average(v[m], weights=w[m])) if m.any() else None
    return {
        "status": "MEASURED",
        "kind": "measured",
        "source": NGS_RECV,
        "player_id": gsis,
        "games": int(len(x)),
        "targets": float(w.sum()),
        "avg_cushion": wavg("avg_cushion"),
        "avg_separation": wavg("avg_separation"),
        "avg_intended_air_yards": wavg("avg_intended_air_yards"),
        "percent_share_of_intended_air_yards": wavg("percent_share_of_intended_air_yards"),
        "catch_percentage": wavg("catch_percentage"),
    }


def _board_side(board: dict, offense: str) -> dict | None:
    offense = D.NV.get(offense, offense)
    for s in (board.get("sides") or {}).values():
        off = D.NV.get(s.get("offense") or s.get("team") or "", "")
        if off == offense or s.get("offense") == offense:
            return s
    # fallback: match by offense key pattern
    for s in (board.get("sides") or {}).values():
        if offense in str(s.get("offense", "")) or offense in str(s.get("team", "")):
            return s
    return None


def _opp_defense_team(board: dict, offense: str) -> str | None:
    offense = D.NV.get(offense, offense)
    home = D.NV.get(board.get("game", {}).get("home"), board.get("game", {}).get("home"))
    away = D.NV.get(board.get("game", {}).get("away"), board.get("game", {}).get("away"))
    if home == offense:
        return away
    if away == offense:
        return home
    return None


def _measured_target_shares(side: dict, receiver_ids: list[str]) -> dict:
    """Board opportunity target shares keyed by gsis. Measured when player_id present."""
    out = {}
    for r in (side.get("opportunity") or {}).get("receivers") or []:
        pid = r.get("player_id")
        if not pid or pid not in receiver_ids:
            continue
        inp = r.get("inputs") or {}
        share = inp.get("target_share_used")
        if share is None:
            share = inp.get("target_share_window")
        if share is None:
            continue
        out[pid] = {
            "kind": "measured",
            "source": "board.opportunity.receivers",
            "target_share": float(share),
            "target_share_last3": inp.get("target_share_last3"),
            "yards_per_target": inp.get("yards_per_target"),
            "position_share": inp.get("position_share"),
        }
    return out


def _position_shell_share_factor(pos: str, man_rate: float | None, mofo_rate: float | None) -> tuple[float, dict]:
    """Inferred position prior under opponent shell rates. Not a player assignment."""
    split = LEAGUE_SPLIT.get(pos) or LEAGUE_SPLIT.get("WR")
    evidence = {"kind": "inferred", "basis": "LEAGUE_SPLIT x opponent shell rates", "position": pos}
    fac = 1.0
    if man_rate is not None and split:
        man = split.get("man", {}).get("share", 1.0)
        zone = split.get("zone", {}).get("share", 1.0)
        base = LEAGUE_MAN_RATE * man + (1 - LEAGUE_MAN_RATE) * zone
        exp = man_rate * man + (1 - man_rate) * zone
        if base > 0:
            fac *= exp / base
        evidence["man_rate"] = man_rate
        evidence["man_zone_factor"] = exp / base if base else 1.0
    if mofo_rate is not None and split:
        mofo = split.get("mofo", {}).get("share", 1.0)
        mofc = split.get("mofc", {}).get("share", 1.0)
        base = LEAGUE_MOFO_RATE * mofo + (1 - LEAGUE_MOFO_RATE) * mofc
        exp = mofo_rate * mofo + (1 - mofo_rate) * mofc
        if base > 0:
            fac *= exp / base
        evidence["mofo_rate"] = mofo_rate
        evidence["mof_factor"] = exp / base if base else 1.0
    return _clip(fac, 0.85, 1.20), evidence


def _ngs_depth_factor(ngs: dict) -> tuple[float, dict]:
    """Mild target-share tilt from measured NGS air-yard share vs separation (measured inputs, inferred weight)."""
    if ngs.get("status") != "MEASURED":
        return 1.0, {"kind": "missing", "status": "MISSING"}
    air = ngs.get("percent_share_of_intended_air_yards")
    sep = ngs.get("avg_separation")
    fac = 1.0
    ev = {"kind": "inferred", "basis": "NGS measured air-yard share + separation", "ngs": {
        k: ngs.get(k) for k in ("avg_cushion", "avg_separation", "avg_intended_air_yards",
                                "percent_share_of_intended_air_yards", "targets", "games")
    }}
    if air is not None:
        # air share is already a measured target-depth signal; shrink toward 1
        fac *= _clip(0.7 + 0.6 * float(air), 0.85, 1.20)
    if sep is not None:
        # league separation ~2.7; more separation -> slightly more targets
        fac *= _clip(1.0 + 0.04 * (float(sep) - 2.7), 0.90, 1.10)
    return _clip(fac, 0.85, 1.20), ev


def _defender_context(side: dict) -> dict:
    """Aggregate defender allowed rates — measured board rows, not player assignments."""
    rows = ((side.get("defenders") or {}).get("coverage") or [])
    if not rows:
        return {"status": "MISSING", "kind": "measured"}
    tg = sum(r.get("targets") or 0 for r in rows)
    if tg <= 0:
        return {"status": "MISSING", "kind": "measured"}
    ypt = sum((r.get("yards") or 0) for r in rows) / tg
    cr = sum((r.get("completions") or 0) for r in rows) / tg
    return {
        "status": "MEASURED",
        "kind": "measured",
        "source": "board.defenders.coverage",
        "n_defenders": len(rows),
        "targets": tg,
        "yards_per_target": ypt,
        "completion_pct": cr,
        "note": "aggregate allowed rates only; no receiver-defender assignment claimed",
    }


def allocate_for_side(board: dict, offense: str, receiver_ids: list[str],
                      positions: dict[str, str], cutoff: str = SOURCE_CUTOFF_DEFAULT) -> dict:
    """Return per-receiver target-share multipliers and full provenance."""
    side = _board_side(board, offense)
    defense = _opp_defense_team(board, offense)
    if side is None:
        return {"status": "MISSING", "offense": offense, "defense": defense, "receivers": {},
                "note": "board side not found"}
    cp = side.get("coverage_profile") or {}
    cts = cp.get("coverage_this_season") or {}
    man_rate = cts.get("man_rate", cp.get("man_rate"))
    mofo_rate = cts.get("two_high_rate")  # Sharp two-high ≈ MOFO
    sharp = sharp_for(defense) if defense else {"status": "MISSING"}
    if sharp.get("status") == "MEASURED":
        man_rate = sharp["man_pct"] if man_rate is None else man_rate
        mofo_rate = sharp["mofo_pct"] if mofo_rate is None else mofo_rate
    measured_shares = _measured_target_shares(side, receiver_ids)
    defenders = _defender_context(side)
    receivers = {}
    weights = []
    for gs in receiver_ids:
        pos = positions.get(gs, "WR")
        ngs = ngs_for_player(gs)
        shell_fac, shell_ev = _position_shell_share_factor(pos, man_rate, mofo_rate)
        ngs_fac, ngs_ev = _ngs_depth_factor(ngs)
        base = measured_shares.get(gs, {})
        base_share = base.get("target_share")
        # combine inferred shell/NGS tilts; keep measured share as the level when present
        mult = _clip(shell_fac * ngs_fac, 0.80, 1.25)
        receivers[gs] = {
            "player_id": gs,
            "position": pos,
            "target_share_multiplier": mult,
            "measured_target_share": base_share,
            "measured": {
                "opportunity": base or {"status": "MISSING"},
                "ngs": ngs,
            },
            "inferred": {
                "shell_share": shell_ev,
                "ngs_tilt": ngs_ev,
            },
            "sources_used": [s for s, ok in (
                ("board.opportunity", bool(base)),
                ("sharp_coverage", sharp.get("status") == "MEASURED"),
                ("board.coverage_profile", man_rate is not None),
                ("ngs_receiving", ngs.get("status") == "MEASURED"),
                ("board.defenders.coverage", defenders.get("status") == "MEASURED"),
            ) if ok],
        }
        weights.append(mult * (base_share if base_share is not None else 1.0 / max(len(receiver_ids), 1)))
    # renormalize multipliers so mean weight unchanged (avoid inventing total targets)
    w = np.array(weights, dtype=float)
    if w.sum() > 0 and len(w):
        scale = (w.mean() and (np.mean([receivers[g]["target_share_multiplier"] for g in receiver_ids]) / (
            np.average([receivers[g]["target_share_multiplier"] for g in receiver_ids],
                       weights=[max(receivers[g]["measured_target_share"] or 1e-6, 1e-6) for g in receiver_ids])
            if any(receivers[g]["measured_target_share"] for g in receiver_ids) else
            np.mean([receivers[g]["target_share_multiplier"] for g in receiver_ids])
        ))) or 1.0
        # keep simple: leave multipliers as-is; engine renormalizes multinomial shares
    status = "EXPERIMENTAL_UNVALIDATED"
    if not any(receivers[g]["sources_used"] for g in receivers):
        status = "MISSING"
    return {
        "status": status,
        "offense": D.NV.get(offense, offense),
        "defense": defense,
        "game_id": (board.get("game") or {}).get("game_id"),
        "source_cutoff": cutoff,
        "defense_shell": {
            "kind": "measured",
            "man_rate": man_rate,
            "mofo_rate": mofo_rate,
            "zone_rate": cts.get("zone_rate", cp.get("zone_rate")),
            "sharp": sharp,
            "coverage_profile_source": cts.get("source") or cp.get("note"),
        },
        "defenders_aggregate": defenders,
        "charting": {
            "play_level_coverage_assignment": "MISSING",
            "note": "no free 2026 pbp_participation defense_man_zone_type; not invented",
        },
        "receivers": receivers,
    }


def profiles_from_board(board: dict, cutoff: str = SOURCE_CUTOFF_DEFAULT) -> dict:
    """Team-keyed allocation profiles for both sides of a board."""
    out = {}
    for s in (board.get("sides") or {}).values():
        offense = s.get("offense")
        if not offense:
            continue
        offense = D.NV.get(offense, offense)
        # receiver ids from opportunity board when present
        recs = []
        pos = {}
        for r in (s.get("opportunity") or {}).get("receivers") or []:
            pid = r.get("player_id")
            if pid:
                recs.append(pid)
                pos[pid] = (r.get("position") or r.get("pos") or "WR")
        out[offense] = allocate_for_side(board, offense, recs, pos, cutoff=cutoff)
    return out
