"""Formation and pass-zone splits per team, from the play-by-play already loaded.

NFL Savant's season download (pbp-<season>.csv) was checked on 2026-11-11 and is the nflverse play-by-play:
same plays, same columns, same values. So these tables are computed from the nflverse file directly and
no second download is made.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ZONES = [(length, loc) for length in ("short", "deep") for loc in ("left", "middle", "right")]


def _formation(p):
    sg = pd.to_numeric(p.shotgun, errors="coerce").fillna(0) == 1
    nh = pd.to_numeric(p.no_huddle, errors="coerce").fillna(0) == 1
    return np.where(nh, "No huddle", np.where(sg, "Shotgun", "Under center"))


def team_splits(plays, team, game_ids_off, game_ids_def) -> dict:
    """plays: metrics.prepare() output. Offence over game_ids_off, defence over game_ids_def."""
    def formations(x):
        if not len(x):
            return []
        x = x.assign(_f=_formation(x))
        out = []
        for f, g in x.groupby("_f"):
            out.append({"formation": f, "plays": int(len(g)), "share": round(len(g) / len(x), 3),
                        "pass_rate": round(float(g.dropback.mean()), 3), "yards_per_play": round(float(pd.to_numeric(g.yards_gained, errors="coerce").mean()), 2),
                        "epa_per_play": round(float(pd.to_numeric(g.epa, errors="coerce").mean()), 3)})
        return sorted(out, key=lambda r: -r["plays"])

    def zones(x):
        a = x[(x.att == 1) & x.pass_length.notna() & x.pass_location.notna()]
        out = []
        for length, loc in ZONES:
            g = a[(a.pass_length == length) & (a.pass_location == loc)]
            if len(g):
                out.append({"zone": f"{length.title()} {loc}", "attempts": int(len(g)), "share": round(len(g) / len(a), 3),
                            "completion_rate": round(float(g.cmp.mean()), 3), "yards_per_attempt": round(float(g.pass_yds.mean()), 2),
                            "explosive": int(g.xpl_pass.sum())})
        return out

    off = plays[(plays.posteam == team) & plays.game_id.isin(game_ids_off)]
    dfn = plays[(plays.defteam == team) & plays.game_id.isin(game_ids_def)]
    return {"offense_by_formation": formations(off), "offense_pass_zones": zones(off),
            "defense_vs_formation": formations(dfn), "defense_pass_zones_allowed": zones(dfn)}
