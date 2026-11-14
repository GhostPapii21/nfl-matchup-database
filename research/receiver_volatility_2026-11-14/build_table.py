"""Receiver-game table 2022-2026 with only pre-game information, for the explosive / seesaw / QB-change / target-tree studies."""
from __future__ import annotations
import numpy as np, pandas as pd
from pathlib import Path
C = Path(__file__).resolve().parents[2] / "pregame" / ".cache"
OUT = Path(__file__).resolve().parent / "rows.parquet"

def season(y):
    p = pd.read_parquet(C / f"play_by_play_{y}.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1)]
    r = pd.read_parquet(C / f"roster_weekly_{y}.parquet")
    pos = dict(zip(r.gsis_id, r.position))
    act = set(zip(r[r.status == "ACT"].week, r[r.status == "ACT"].team, r[r.status == "ACT"].gsis_id))
    t = p[(p.pass_attempt == 1) & (p.sack != 1)].copy()
    t["is_tgt"] = t.receiver_player_id.notna()
    tg = t[t.is_tgt].copy()
    tg["pos"] = tg.receiver_player_id.map(pos)
    tg["y"] = tg.receiving_yards.fillna(0)
    tg["ex20"] = ((tg.complete_pass == 1) & (tg.y >= 20)).astype(int)
    tg["ex30"] = ((tg.complete_pass == 1) & (tg.y >= 30)).astype(int)
    tg["deep"] = (tg.air_yards.fillna(0) >= 20).astype(int)
    # per player-game
    pg = tg.groupby(["game_id", "week", "posteam", "defteam", "receiver_player_id"]).agg(
        pos=("pos", "first"), targets=("is_tgt", "size"), rec=("complete_pass", "sum"), yds=("y", "sum"), td=("pass_touchdown", "sum"),
        ex20=("ex20", "sum"), ex30=("ex30", "sum"), deep=("deep", "sum"), air=("air_yards", lambda s: float(s.fillna(0).sum())),
        long=("y", "max")).reset_index()
    # passer per team-game (most dropbacks)
    db = p[p.qb_dropback == 1]
    qb = db.groupby(["game_id", "posteam"]).passer_player_id.agg(lambda s: s.mode().iloc[0] if len(s.dropna()) else None).rename("qb").reset_index()
    team = t.groupby(["game_id", "week", "posteam"]).agg(att=("is_tgt", "size"), team_tgts=("is_tgt", "sum"), team_air=("air_yards", lambda s: float(s.fillna(0).sum()))).reset_index().merge(qb, on=["game_id", "posteam"], how="left")
    # defense allowed per game
    dg = t.groupby(["game_id", "week", "defteam"]).agg(d_att=("is_tgt", "size"), d_yds=("passing_yards", lambda s: float(s.fillna(0).sum())),
        d_ex20=("yards_gained", lambda s: int((s >= 20).sum())), d_deep=("air_yards", lambda s: int((s.fillna(0) >= 20).sum()))).reset_index()
    dpos = tg.groupby(["game_id", "week", "defteam", "pos"]).agg(dp_tgt=("is_tgt", "size"), dp_yds=("y", "sum")).reset_index()
    return p, pos, act, pg, team, dg, dpos

def build():
    games = pd.read_parquet(C / "games.parquet")
    rows = []
    for y in (2022, 2023, 2024, 2025, 2026):
        p, pos, act, pg, team, dg, dpos = season(y)
        pg = pg.merge(team, on=["game_id", "week", "posteam"], how="left")
        sched = games[(games.season == y) & (games.game_type == "REG")].set_index("game_id")
        weeks = sorted(pg.week.unique())
        for w in weeks:
            if w < 4:
                continue
            prior, now = pg[pg.week < w], pg[pg.week == w]
            tprior = team[team.week < w]
            dprior = dg[dg.week < w]
            dposp = dpos[dpos.week < w]
            lg_ex = dprior.d_ex20.sum() / max(dprior.d_att.sum(), 1)
            lg_ypa = dprior.d_yds.sum() / max(dprior.d_att.sum(), 1)
            for gid, g in sched[sched.week == w].iterrows():
                for team_, opp, home in ((g.home_team, g.away_team, True), (g.away_team, g.home_team, False)):
                    tp = tprior[tprior.posteam == team_]
                    if len(tp) < 3:
                        continue
                    cur_qb = team[(team.game_id == gid) & (team.posteam == team_)].qb
                    cur_qb = cur_qb.iloc[0] if len(cur_qb) else None
                    main_qb = tp.qb.mode().iloc[0] if tp.qb.notna().any() else None
                    od = dprior[dprior.defteam == opp]
                    spread = g.spread_line if home else -g.spread_line
                    implied = (g.total_line / 2 + spread / 2) if pd.notna(g.total_line) and pd.notna(g.spread_line) else np.nan
                    pp = prior[prior.posteam == team_]
                    for pid, h in pp.groupby("receiver_player_id"):
                        P = pos.get(pid)
                        if P not in ("WR", "TE", "RB") or h.targets.sum() < 8 or (w, team_, pid) not in act:
                            continue
                        h = h.sort_values("week")
                        tt = tp.set_index("game_id").team_tgts
                        share = h.targets.sum() / tt.loc[h.game_id].sum()
                        l3 = h.tail(3)
                        same_qb = h[h.qb == cur_qb] if cur_qb else h.iloc[0:0]
                        o = now[(now.receiver_player_id == pid) & (now.game_id == gid)]
                        odp = dposp[(dposp.defteam == opp) & (dposp.pos == P)]
                        rows.append({
                            "season": y, "week": w, "game_id": gid, "team": team_, "opp": opp, "player": pid, "pos": P,
                            "games_prior": len(h), "tgt_pg": h.targets.mean(), "share": share,
                            "share_l3": l3.targets.sum() / tt.loc[l3.game_id].sum(),
                            "share_same_qb": (same_qb.targets.sum() / tt.loc[same_qb.game_id].sum()) if len(same_qb) else np.nan, "games_same_qb": len(same_qb),
                            "qb_changed": int(cur_qb is not None and main_qb is not None and cur_qb != main_qb),
                            "ypt": h.yds.sum() / h.targets.sum(), "adot": h.air.sum() / h.targets.sum(),
                            "air_share": h.air.sum() / max(tp.set_index("game_id").team_air.loc[h.game_id].sum(), 1),
                            "deep_rate": h.deep.sum() / h.targets.sum(), "ex20_rate": h.ex20.sum() / h.targets.sum(), "ex30_rate": h.ex30.sum() / h.targets.sum(),
                            "ex20_l2": h.tail(2).ex20.sum(), "ex20_l3": l3.ex20.sum(), "yds_l3": l3.yds.mean(), "yds_avg": h.yds.mean(),
                            "big100_prior": int((h.yds >= 100).sum()),
                            "opp_ex_rate": (od.d_ex20.sum() / max(od.d_att.sum(), 1)) / max(lg_ex, 1e-6) if len(od) else 1.0,
                            "opp_ypa": (od.d_yds.sum() / max(od.d_att.sum(), 1)) / max(lg_ypa, 1e-6) if len(od) else 1.0,
                            "opp_pos_ypg": odp.dp_yds.sum() / max(len(od), 1) if len(od) else np.nan, "opp_pos_tpg": odp.dp_tgt.sum() / max(len(od), 1) if len(od) else np.nan,
                            "implied": implied, "spread": spread, "wind": g.wind, "temp": g.temp, "roof": g.roof,
                            "y_tgt": int(o.targets.iloc[0]) if len(o) else 0, "y_rec": int(o.rec.iloc[0]) if len(o) else 0,
                            "y_yds": float(o.yds.iloc[0]) if len(o) else 0.0, "y_ex20": int(o.ex20.iloc[0]) if len(o) else 0,
                            "y_ex30": int(o.ex30.iloc[0]) if len(o) else 0, "y_long": float(o.long.iloc[0]) if len(o) else 0.0,
                            "y_team_tgts": int(team[(team.game_id == gid) & (team.posteam == team_)].team_tgts.iloc[0]) if len(team[(team.game_id == gid) & (team.posteam == team_)]) else np.nan})
        print(y, len(rows), flush=True)
    df = pd.DataFrame(rows)
    df.to_parquet(OUT)
    return df

if __name__ == "__main__":
    d = build(); print(d.shape); print(d.describe().T[["mean"]].head(40))
