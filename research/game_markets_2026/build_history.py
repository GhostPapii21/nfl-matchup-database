"""History table for the game-market model: every regular-season game 2022-2026 with the closing spread/total (nflverse
schedules), each team's implied points, and points by quarter from play-by-play. Writes dashboard/game_history.csv."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "pregame" / ".cache"


def main():
    g = pd.read_parquet(C / "games.parquet")
    g = g[(g.game_type == "REG") & g.season.between(2022, 2026) & g.home_score.notna() & g.spread_line.notna() & g.total_line.notna()]
    rows = []
    for y in sorted(g.season.unique()):
        p = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["game_id", "qtr", "total_home_score", "total_away_score"])
        for gid, x in p.groupby("game_id"):
            end = x.groupby("qtr")[["total_home_score", "total_away_score"]].max().sort_index()
            ph = pa = 0
            q = {}
            for qt, r in end.iterrows():
                h, a = int(r.total_home_score), int(r.total_away_score)
                q[int(qt)] = (h - ph, a - pa)
                ph, pa = max(ph, h), max(pa, a)
            row = {"game_id": gid}
            for k in (1, 2, 3, 4):
                row[f"h_q{k}"], row[f"a_q{k}"] = q.get(k, (0, 0))
            row["h_ot"], row["a_ot"] = q.get(5, (0, 0))
            rows.append(row)
    q = pd.DataFrame(rows)
    out = g[["game_id", "season", "week", "home_team", "away_team", "spread_line", "total_line", "home_score", "away_score"]].merge(q, on="game_id")
    out["home_imp"] = (out.total_line + out.spread_line) / 2          # nflverse spread_line > 0 = home favored
    out["away_imp"] = (out.total_line - out.spread_line) / 2
    ok = (out[[f"h_q{k}" for k in (1, 2, 3, 4)]].sum(axis=1) + out.h_ot == out.home_score) & (out[[f"a_q{k}" for k in (1, 2, 3, 4)]].sum(axis=1) + out.a_ot == out.away_score)
    out = out[ok]
    out.to_csv(ROOT / "dashboard" / "game_history.csv", index=False)
    print(len(out), "games;", (~ok).sum(), "dropped (quarters did not add up)")


if __name__ == "__main__":
    main()
