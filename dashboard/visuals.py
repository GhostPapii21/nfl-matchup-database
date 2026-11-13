"""Data for the board's visual matchup views: size and speed, where a player's targets go, his route tree, how a back
runs by gap against the defenders on that side, the offense's personnel, the defense's shell, and his production
against top and bottom defenses.

Free data limits, stated on the board: per-play routes, man/zone and coverage shells come from NGS participation, which
is published through last season only; where a receiver lines up (slot or wide) is not in any free source.
"""
from __future__ import annotations

import math
import re

import numpy as np
import pandas as pd

MOFO = {"COVER_2", "COVER_4", "COVER_6", "2_MAN"}            # two high safeties: middle of the field open
MOFC = {"COVER_0", "COVER_1", "COVER_3"}                     # one or no high safety: middle of the field closed
DEPTHS = [("behind", -99, -1), ("short", 0, 9), ("intermediate", 10, 19), ("deep", 20, 99)]
LANES = ("left", "middle", "right")


def _f(x, nd=3):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if (math.isnan(x) or math.isinf(x)) else round(x, nd)


def _height_in(h):
    if h is None or (isinstance(h, float) and math.isnan(h)):
        return None
    if isinstance(h, (int, float)):
        return float(h)
    m = re.match(r"(\d+)-(\d+)", str(h))
    return float(m.group(1)) * 12 + float(m.group(2)) if m else None


# ----------------------------------------------------------------------------------------------- size and speed
class Bodies:
    """Height and weight from the current roster; 40-yard dash, vertical and draft slot from the combine."""

    def __init__(self, rosters: pd.DataFrame | None, combine: pd.DataFrame | None):
        self.by_id, self.by_name = {}, {}
        comb = {}
        if combine is not None and len(combine):
            for r in combine.itertuples():
                if isinstance(r.pfr_id, str):
                    comb[r.pfr_id] = r
        if rosters is not None and len(rosters):
            for r in rosters.sort_values("week").itertuples():
                c = comb.get(r.pfr_id)
                d = {"name": r.full_name, "team": r.team, "position": r.position, "height_in": _height_in(r.height),
                     "weight": _f(r.weight, 0), "forty": _f(getattr(c, "forty", None), 2) if c is not None else None,
                     "vertical": _f(getattr(c, "vertical", None), 1) if c is not None else None,
                     "draft": (f"{int(c.draft_round)}.{int(c.draft_ovr)}" if c is not None and pd.notna(getattr(c, "draft_round", None)) else None),
                     "headshot": getattr(r, "headshot_url", None)}
                self.by_id[r.gsis_id] = d
                self.by_name[(str(r.full_name).lower(), r.team)] = d

    def player(self, gsis_id=None, name=None, team=None):
        if gsis_id and gsis_id in self.by_id:
            return self.by_id[gsis_id]
        if name:
            return self.by_name.get((name.lower(), team))
        return None


def size_matchup(receiver: dict, defenders: list[dict], bodies: Bodies, team_def: str) -> dict | None:
    """Receiver against the defenders most likely to cover his position (corners for WRs, safeties and linebackers for TEs/RBs)."""
    me = bodies.player(receiver.get("player_id"))
    if not me:
        return None
    pos = (receiver.get("pos") or "").upper()
    want = ("CB",) if pos == "WR" else ("S", "LB")
    cands = []
    for d in defenders:
        if d.get("position") not in want or (d.get("targets") or 0) < 8:
            continue
        b = bodies.player(name=d["player"], team=team_def)
        if b:
            cands.append({"player": d["player"], "position": d["position"], "targets": d.get("targets"), "yards_per_target": _f(d.get("yards_per_target"), 1),
                          "grade": d.get("grade"), "height_in": b["height_in"], "weight": b["weight"], "forty": b["forty"]})
    cands.sort(key=lambda x: -(x["targets"] or 0))
    cands = cands[:4]
    if not cands:
        return {"player": me, "defenders": [], "edges": []}
    hs = [c["height_in"] for c in cands if c["height_in"]]
    ws = [c["weight"] for c in cands if c["weight"]]
    fs = [c["forty"] for c in cands if c["forty"]]
    edges = []
    if me["height_in"] and hs:
        dh = me["height_in"] - sum(hs) / len(hs)
        if dh >= 3:
            edges.append({"kind": "size", "level": "good", "text": f"Size edge: {dh:.0f} inches taller than the {'corners' if pos == 'WR' else 'defenders'} who see the most targets. Contested catches and red zone."})
        elif dh <= -3:
            edges.append({"kind": "size", "level": "warn", "text": f"Gives up {-dh:.0f} inches: needs separation and route running, not jump balls."})
    if me["weight"] and ws and pos in ("TE", "RB"):
        dw = me["weight"] - sum(ws) / len(ws)
        if dw >= 25:
            edges.append({"kind": "size", "level": "good", "text": f"Outweighs the safeties and linebackers by about {dw:.0f} lb: hard to tackle after the catch."})
    if me["forty"] and fs:
        ds = sum(fs) / len(fs) - me["forty"]
        if ds >= 0.08:
            edges.append({"kind": "speed", "level": "good", "text": f"Speed edge: {me['forty']:.2f} forty against {sum(fs) / len(fs):.2f} for the likely coverage."})
        elif ds <= -0.08:
            edges.append({"kind": "speed", "level": "warn", "text": f"Slower than the likely coverage ({me['forty']:.2f} against {sum(fs) / len(fs):.2f}): wins with routes and size, not speed."})
    return {"player": me, "defenders": cands, "edges": edges}


# ----------------------------------------------------------------------------------------------- where his targets go
def target_map(pbp: pd.DataFrame, receiver_id: str, weeks) -> dict:
    t = pbp[(pbp.receiver_player_id == receiver_id) & pbp.week.isin(list(weeks)) & (pbp.pass_attempt == 1) & (pbp.sack != 1) & (pbp.two_point_attempt != 1)]
    cells = []
    for name, lo, hi in DEPTHS:
        for lane in LANES:
            c = t[(t.pass_location == lane) & t.air_yards.between(lo, hi)]
            cells.append({"depth": name, "lane": lane, "targets": int(len(c)), "catches": int(c.complete_pass.sum()),
                          "yards": int(c.receiving_yards.fillna(0).sum()), "td": int(c.pass_touchdown.sum()),
                          "yards_per_target": _f(c.receiving_yards.fillna(0).sum() / len(c), 1) if len(c) else None})
    return {"targets": int(len(t)), "cells": cells}


def route_tree(pbp_prev: pd.DataFrame | None, part_prev: pd.DataFrame | None, receiver_id: str) -> dict | None:
    """Last season's targeted routes with results, and his splits against man/zone and one-high/two-high shells."""
    if pbp_prev is None or part_prev is None:
        return None
    t = pbp_prev[(pbp_prev.receiver_player_id == receiver_id) & (pbp_prev.pass_attempt == 1) & (pbp_prev.sack != 1) & (pbp_prev.season_type == "REG")]
    if not len(t):
        return None
    j = t.merge(part_prev[["nflverse_game_id", "play_id", "route", "defense_man_zone_type", "defense_coverage_type"]],
                left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"], how="inner")
    j = j[j.route.fillna("") != ""]
    if len(j) < 10:
        return None
    routes = []
    for rname, g in j.groupby("route"):
        routes.append({"route": rname, "targets": int(len(g)), "share": _f(len(g) / len(j)), "catches": int(g.complete_pass.sum()),
                       "yards_per_target": _f(g.receiving_yards.fillna(0).sum() / len(g), 1)})
    routes.sort(key=lambda x: -x["targets"])

    def split(df):
        if not len(df):
            return None
        return {"targets": int(len(df)), "catch_rate": _f(df.complete_pass.mean()), "yards_per_target": _f(df.receiving_yards.fillna(0).sum() / len(df), 2),
                "td": int(df.pass_touchdown.sum())}
    return {"season": int(pbp_prev.season.iloc[0]), "targets": int(len(j)), "routes": routes,
            "vs_man": split(j[j.defense_man_zone_type == "MAN_COVERAGE"]), "vs_zone": split(j[j.defense_man_zone_type == "ZONE_COVERAGE"]),
            "vs_mofo": split(j[j.defense_coverage_type.isin(MOFO)]), "vs_mofc": split(j[j.defense_coverage_type.isin(MOFC)]),
            "teams": sorted(set(t.posteam.dropna()))}


# ----------------------------------------------------------------------------------------------- running backs by gap
def run_map(pbp: pd.DataFrame, rusher_id: str, weeks) -> dict:
    r = pbp[(pbp.rusher_player_id == rusher_id) & pbp.week.isin(list(weeks)) & (pbp.rush_attempt == 1) & (pbp.qb_scramble != 1) & (pbp.two_point_attempt != 1)]
    cells = []
    for loc, gap in (("left", "end"), ("left", "tackle"), ("left", "guard"), ("middle", None), ("right", "guard"), ("right", "tackle"), ("right", "end")):
        c = r[(r.run_location == loc) & ((r.run_gap == gap) if gap else True)]
        cells.append({"direction": f"{loc} {gap}" if gap else "middle", "carries": int(len(c)), "yards": int(c.rushing_yards.fillna(0).sum()),
                      "ypc": _f(c.rushing_yards.fillna(0).sum() / len(c), 2) if len(c) else None,
                      "explosive": int((c.rushing_yards >= 15).sum())})
    return {"carries": int(len(r)), "cells": cells}


def defense_front(depth_chart: dict) -> dict:
    """Starting front by side from the defense's depth chart (the offense's left is the defense's right)."""
    out = {}
    for s in depth_chart.get("starters", []) or []:
        out.setdefault(s["slot"], s["player"])
    return out


# ----------------------------------------------------------------------------------------------- personnel and shell
def personnel(part_prev: pd.DataFrame | None, pbp_prev: pd.DataFrame | None, team: str) -> dict | None:
    if part_prev is None or pbp_prev is None:
        return None
    p = part_prev[part_prev.possession_team == team]
    if not len(p):
        return None

    def code(s):
        s = str(s)
        rb = re.search(r"(\d) RB", s); te = re.search(r"(\d) TE", s)
        return f"{rb.group(1) if rb else 0}{te.group(1) if te else 0}"
    groups = p.offense_personnel.dropna().map(code).value_counts(normalize=True).head(5)
    forms = p.offense_formation.dropna().value_counts(normalize=True).head(4)
    return {"season": int(pbp_prev.season.iloc[0]), "personnel": [{"group": k, "rate": _f(v)} for k, v in groups.items()],
            "formations": [{"formation": k.title(), "rate": _f(v)} for k, v in forms.items()]}


def defense_shell(part_prev: pd.DataFrame | None, pbp_prev: pd.DataFrame | None, team: str) -> dict | None:
    if part_prev is None or pbp_prev is None:
        return None
    d = pbp_prev[(pbp_prev.defteam == team) & (pbp_prev.qb_dropback == 1) & (pbp_prev.season_type == "REG")]
    j = d.merge(part_prev[["nflverse_game_id", "play_id", "defense_man_zone_type", "defense_coverage_type", "was_pressure"]],
                left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"], how="inner")
    j = j[j.defense_coverage_type.notna() & (j.defense_coverage_type != "")]
    if len(j) < 50:
        return None

    def allowed(df):
        if not len(df):
            return None
        att = df[(df.pass_attempt == 1) & (df.sack != 1)]
        return {"dropbacks": int(len(df)), "yards_per_attempt": _f(att.passing_yards.fillna(0).sum() / max(len(att), 1), 2),
                "explosive_rate": _f(((df.pass_attempt == 1) & (df.yards_gained >= 20)).sum() / len(df)),
                "completion_pct": _f(att.complete_pass.mean() if len(att) else None)}
    return {"season": int(pbp_prev.season.iloc[0]), "dropbacks": int(len(j)),
            "mofo_rate": _f(j.defense_coverage_type.isin(MOFO).mean()), "mofc_rate": _f(j.defense_coverage_type.isin(MOFC).mean()),
            "man_rate": _f((j.defense_man_zone_type == "MAN_COVERAGE").mean()), "zone_rate": _f((j.defense_man_zone_type == "ZONE_COVERAGE").mean()),
            "vs_man": allowed(j[j.defense_man_zone_type == "MAN_COVERAGE"]), "vs_zone": allowed(j[j.defense_man_zone_type == "ZONE_COVERAGE"]),
            "vs_mofo": allowed(j[j.defense_coverage_type.isin(MOFO)]), "vs_mofc": allowed(j[j.defense_coverage_type.isin(MOFC)])}


# ----------------------------------------------------------------------------------------------- top and bottom defenses
def position_ranks(pbp: pd.DataFrame, pos_map: dict, through_week: int | None = None) -> dict:
    """Rank of each defense by yards allowed per game to WR / TE / RB receivers and RB rushing (1 = allows the least)."""
    q = pbp[(pbp.season_type == "REG") & (pbp.two_point_attempt != 1)]
    if through_week is not None:
        q = q[q.week < through_week]
    games = q.groupby("defteam").game_id.nunique()
    out = {}
    rec = q[(q.complete_pass == 1)].assign(rpos=lambda x: x.receiver_player_id.map(pos_map))
    for P in ("WR", "TE", "RB"):
        y = rec[rec.rpos == P].groupby("defteam").receiving_yards.sum() / games
        out[P] = {t: int(r) for t, r in y.rank(method="min").items()}
    ru = q[(q.rush_attempt == 1) & (q.qb_scramble != 1)].assign(rpos=lambda x: x.rusher_player_id.map(pos_map))
    y = ru[ru.rpos == "RB"].groupby("defteam").rushing_yards.sum() / games
    out["RB_rush"] = {t: int(r) for t, r in y.rank(method="min").items()}
    return out


def tier_splits(seasons: list[tuple[pd.DataFrame, dict]], player_id: str, pos: str, kind: str = "rec") -> dict | None:
    """His per-game production against top-10, middle and bottom-10 defenses for his position (season ranks)."""
    key = pos if kind == "rec" else "RB_rush"
    rows = []
    for pbp, ranks in seasons:
        q = pbp[(pbp.season_type == "REG") & (pbp.two_point_attempt != 1)]
        if kind == "rec":
            g = q[q.receiver_player_id == player_id].groupby(["game_id", "defteam"]).agg(
                targets=("pass_attempt", "sum"), catches=("complete_pass", "sum"), yards=("receiving_yards", lambda s: float(s.fillna(0).sum()))).reset_index()
        else:
            g = q[(q.rusher_player_id == player_id) & (q.qb_scramble != 1)].groupby(["game_id", "defteam"]).agg(
                carries=("rush_attempt", "sum"), yards=("rushing_yards", lambda s: float(s.fillna(0).sum()))).reset_index()
        rk = ranks.get(key, {})
        g["rank"] = g.defteam.map(rk)
        rows.append(g)
    if not rows:
        return None
    g = pd.concat(rows)
    g = g[g["rank"].notna()]
    if not len(g):
        return None
    n = max(int(g["rank"].max()), 32)

    def tier(r):
        return "top" if r <= 10 else "bottom" if r > n - 10 else "middle"
    g["tier"] = g["rank"].map(tier)
    out = {}
    for t in ("top", "middle", "bottom"):
        x = g[g.tier == t]
        if kind == "rec":
            out[t] = {"games": int(len(x)), "targets": _f(x.targets.mean(), 1), "catches": _f(x.catches.mean(), 1), "yards": _f(x.yards.mean(), 1)} if len(x) else {"games": 0}
        else:
            out[t] = {"games": int(len(x)), "carries": _f(x.carries.mean(), 1), "yards": _f(x.yards.mean(), 1)} if len(x) else {"games": 0}
    return out


def pool_quantiles(pool: np.ndarray, q: int = 200) -> list[float]:
    """A compact copy of a per-catch or per-carry outcome pool for the in-page simulation."""
    if pool is None or not len(pool):
        return []
    return [round(float(x), 1) for x in np.quantile(pool, np.linspace(0, 1, q))]
