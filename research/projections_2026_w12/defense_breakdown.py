"""Where a defense leaks, by receiver role and the run game (owner, Nov 25, 2026; same breakdown as the MNF debrief).

Roles come from the OFFENSE's own season: WR1 / WR2 / WR3+ = its wide receivers ranked by targets; TE; RB (receiving);
RB rushing. For every game a defense played: what each role got vs that same player's (or group's) average in his
other games, so a defense isn't penalised for facing good offenses. Ranks are among 32 defenses (1 = allows the most
above usual). Season and last 5 games. Screens from FTN charting.

    python3 research/projections_2026_w12/defense_breakdown.py LA GB
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "pregame" / ".cache"


def load():
    p = pd.read_parquet(C / "play_by_play_2026.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    ro = pd.read_parquet(C / "roster_weekly_2026.parquet", columns=["gsis_id", "position"]).drop_duplicates("gsis_id")
    pos = dict(zip(ro.gsis_id, ro.position))
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].copy()
    t["pos"] = t.receiver_player_id.map(pos)
    wr = t[t.pos == "WR"].groupby(["posteam", "receiver_player_id"]).size().rename("n").reset_index()
    wr["rk"] = wr.groupby("posteam").n.rank(ascending=False, method="first")
    rk = {(r.posteam, r.receiver_player_id): r.rk for r in wr.itertuples()}
    def role(r):
        if r.pos == "WR":
            k = rk.get((r.posteam, r.receiver_player_id), 9)
            return "WR1" if k == 1 else ("WR2" if k == 2 else "WR3+")
        return {"TE": "TE", "RB": "RB rec", "FB": "RB rec"}.get(r.pos, "other")
    t["role"] = t.apply(role, axis=1)
    t["yds"] = t.receiving_yards.fillna(0)
    rec = t.groupby(["game_id", "week", "posteam", "defteam", "role"]).agg(tg=("yds", "size"), rec=("complete_pass", "sum"), yds=("yds", "sum"), td=("pass_touchdown", "sum")).reset_index()
    r = p[(p.rush_attempt == 1) & (p.qb_scramble != 1) & (p.rusher_player_id.map(pos) == "RB")]
    ru = r.groupby(["game_id", "week", "posteam", "defteam"]).agg(tg=("rushing_yards", "size"), rec=("rushing_yards", lambda s: (s >= 10).sum()), yds=("rushing_yards", "sum"), td=("rush_touchdown", "sum")).reset_index()
    ru["role"] = "RB rush"
    g = pd.concat([rec, ru])
    # each offense-role's usual (its other games)
    tot = g.groupby(["posteam", "role"])[["tg", "rec", "yds", "td"]].transform("sum")
    n = g.groupby(["posteam", "role"]).yds.transform("size")
    for c in ("tg", "rec", "yds", "td"):
        g[c + "_usual"] = (tot[c] - g[c]) / (n - 1).clip(lower=1)
    g["yds_vs_usual"] = g.yds - g.yds_usual
    g["rec_vs_usual"] = g.rec - g.rec_usual
    g["tg_vs_usual"] = g.tg - g.tg_usual
    return g, t


def table(g, last=None):
    if last:
        g = g[g.groupby("defteam").week.rank(ascending=False, method="dense") <= last]
    d = g.groupby(["defteam", "role"]).agg(games=("week", "nunique"), yds_pg=("yds", "mean"), yds_vs_usual=("yds_vs_usual", "mean"),
                                           rec_vs_usual=("rec_vs_usual", "mean"), tg_vs_usual=("tg_vs_usual", "mean"), td_pg=("td", "mean")).reset_index()
    d["rank"] = d.groupby("role").yds_vs_usual.rank(ascending=False, method="min").astype(int)
    return d


def screens(t, team=None, defense=None):
    f = pd.read_parquet(C / "ftn_charting_2026.parquet", columns=["nflverse_game_id", "nflverse_play_id", "is_screen_pass"])
    x = t.merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"])
    out = {}
    if team:
        o = x[x.posteam == team]
        s = o[o.is_screen_pass == True]  # noqa: E712
        out["team_screen_rate"] = round(len(s) / max(len(o), 1), 3)
        out["screen_targets_by_player"] = s.receiver_player_name.value_counts().head(5).to_dict()
    if defense:
        d = x[(x.defteam == defense) & (x.is_screen_pass == True)]  # noqa: E712
        lg = x[x.is_screen_pass == True]  # noqa: E712
        out["screen_yds_per_target_allowed"] = round(float(d.yds.mean()), 2) if len(d) else None
        out["league_screen_ypt"] = round(float(lg.yds.mean()), 2)
    return out


if __name__ == "__main__":
    g, t = load()
    for dfn in sys.argv[1:]:
        for lab, last in (("season", None), ("last 5", 5)):
            d = table(g, last)
            d = d[d.defteam == dfn].set_index("role").loc[["WR1", "WR2", "WR3+", "TE", "RB rec", "RB rush"]]
            print(f"\n##### {dfn} DEFENSE, {lab}: yards a game by role, vs those players' usual (rank of 32: 1 = gives up the most over usual)")
            print(d[["games", "yds_pg", "yds_vs_usual", "rec_vs_usual", "tg_vs_usual", "td_pg", "rank"]].round(1).to_string())
        print(f"{dfn} vs screens: {screens(t, defense=dfn)}")
    for off in sys.argv[1:]:
        print(f"{off} offense screens: {screens(t, team=off)}")
