"""Zone matchup profile (owner, Nov 25, 2026): where each defense gives up catches and yards, by depth and side of the
field, who was around the ball there, and where each receiver's targets come from.

Play-by-play per target: depth = air yards (behind/at the line <=0, short 1-9, intermediate 10-19, deep 20+), side =
pass_location (left / middle / right), the defender named on the play: the one who broke up the pass, else the
tackler. That is who finished the play, usually but not always the man in coverage (no free source has assignments).
NGS route charts (images of each targeted route) can add route shape on top of this; they are not machine-readable.

    python3 research/projections_2026_w12/zones.py GB LA         # offense-vs-defense pairs both ways
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "pregame" / ".cache"
BANDS = [(-99, 0, "behind/at line"), (1, 9, "short 1-9"), (10, 19, "intermediate 10-19"), (20, 99, "deep 20+")]


def load():
    p = pd.read_parquet(C / "play_by_play_2026.parquet")
    p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna() & p.air_yards.notna() & p.pass_location.notna()]
    p = p.copy()
    p["band"] = pd.cut(p.air_yards, [-99, 0.5, 9.5, 19.5, 99], labels=[b[2] for b in BANDS])
    p["side"] = p.pass_location
    p["yds"] = p.receiving_yards.fillna(0)
    p["defender"] = p.pass_defense_1_player_name.fillna(p.solo_tackle_1_player_name).fillna(p.assist_tackle_1_player_name)
    return p


def profile(p, dfn):
    lg = p.groupby(["band", "side"], observed=True).agg(lg_tgt=("yds", "size"), lg_cmp=("complete_pass", "mean"), lg_ypt=("yds", "mean"))
    d = p[p.defteam == dfn]
    z = d.groupby(["band", "side"], observed=True).agg(tgt=("yds", "size"), cmp=("complete_pass", "mean"), ypt=("yds", "mean")).join(lg)
    z["ypt_vs_lg"] = z.ypt - z.lg_ypt
    top = d.dropna(subset=["defender"]).groupby(["band", "side", "defender"], observed=True).agg(n=("yds", "size"), y=("yds", "sum")).reset_index()
    top = top.sort_values(["band", "side", "n", "y"], ascending=[True, True, False, False]).groupby(["band", "side"], observed=True).head(2)
    names = top.groupby(["band", "side"], observed=True).apply(lambda x: ", ".join(f"{r.defender} {int(r.n)}/{int(r.y)}y" for r in x.itertuples()), include_groups=False)
    z["around_the_ball"] = names
    return z


def receivers(p, off):
    o = p[p.posteam == off]
    tot = o.groupby("receiver_player_name").size()
    keep = tot[tot >= 15].index
    o = o[o.receiver_player_name.isin(keep)]
    c = o.groupby(["receiver_player_name", "band", "side"], observed=True).size()
    return c / c.groupby(level=0).transform("sum")


def matchup(p, off, dfn):
    z = profile(p, dfn)
    mix = receivers(p, off)
    print(f"\n##### {dfn} DEFENSE: catch rate and yards per target by zone vs league (2026, through week {int(p.week.max())})")
    show = z[z.tgt >= 4][["tgt", "cmp", "lg_cmp", "ypt", "ypt_vs_lg", "around_the_ball"]].copy()
    show["cmp"] = (show.cmp * 100).round(0); show["lg_cmp"] = (show.lg_cmp * 100).round(0)
    print(show.round(1).to_string())
    print(f"\n##### {off} RECEIVERS: where their targets come from, and what {dfn} allows there (expected yards per target vs league)")
    for name, s in mix.groupby(level=0):
        s = s.droplevel(0)
        zz = z.reindex(s.index)
        exp = float(np.nansum(s.values * zz.ypt_vs_lg.fillna(0).values))
        topz = ", ".join(f"{b} {sd} {v:.0%}" for (b, sd), v in s.sort_values(ascending=False).head(3).items())
        print(f"  {name:18} {exp:+.2f} yds/target vs league in his zones | his top zones: {topz}")


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    p = load()
    matchup(p, a, b)
    matchup(p, b, a)
