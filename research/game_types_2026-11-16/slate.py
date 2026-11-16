"""Receiver tiers, team game types and defense profiles for the current season, and the next week's matchups.

    python3 research/game_types_2026-11-16/slate.py --data DIR --week 11
DIR holds pbp_2026.parquet, games.parquet, adv_rush.parquet, adv_def.parquet (nflverse downloads). Writes slate_week<N>.json.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--week", type=int, required=True); ap.add_argument("--season", type=int, default=2026)
    a = ap.parse_args()
    D = Path(a.data)
    p = pd.read_parquet(D / f"pbp_{a.season}.parquet")
    p = p[(p.season_type == "REG") & (p.two_point_attempt != 1) & (p.week < a.week)]
    ro = pd.read_parquet(ROOT / "pregame" / ".cache" / f"roster_weekly_{a.season}.parquet").dropna(subset=["gsis_id"]).sort_values("week")
    pos, full, team_now = dict(zip(ro.gsis_id, ro.position)), dict(zip(ro.gsis_id, ro.full_name)), dict(zip(ro.gsis_id, ro.team))
    status = dict(zip(ro.gsis_id, ro.status))
    t = p[(p.pass_attempt == 1) & (p.sack != 1) & p.receiver_player_id.notna()].copy()
    t["y"] = t.receiving_yards.fillna(0); t["pos"] = t.receiver_player_id.map(pos)
    t["ex"] = ((t.complete_pass == 1) & (t.y >= 20)).astype(int)
    pg = t.groupby(["receiver_player_id", "posteam", "defteam", "week"]).agg(tgt=("y", "size"), rec=("complete_pass", "sum"), yds=("y", "sum"), ex=("ex", "sum")).reset_index()
    pg["pos"] = pg.receiver_player_id.map(pos)
    team_t = t.groupby(["posteam", "week"]).size().rename("team_tgt")
    pg = pg.join(team_t, on=["posteam", "week"])
    # ---- receiver tiers
    rec = []
    for pid, g in pg[pg.pos.isin(["WR", "TE"])].groupby("receiver_player_id"):
        if len(g) < 3:
            continue
        g = g.sort_values("week"); l3 = g.tail(3)
        r = {"player": full.get(pid, pid), "pos": pos.get(pid), "team": team_now.get(pid, g.posteam.iloc[-1]), "status": status.get(pid), "games": int(len(g)),
             "tgt_pg": round(g.tgt.mean(), 1), "rec_pg": round(g.rec.mean(), 1), "yds_pg": round(g.yds.mean(), 1), "ex_pg": round(g.ex.mean(), 2),
             "share": round(g.tgt.sum() / g.team_tgt.sum(), 3), "share_l3": round(l3.tgt.sum() / l3.team_tgt.sum(), 3),
             "yds_l3": round(l3.yds.mean(), 1), "g80": int((g.yds >= 80).sum()), "g100": int((g.yds >= 100).sum()),
             "ex_share": round(float(t[(t.receiver_player_id == pid) & (t.ex == 1)].y.sum() / max(g.yds.sum(), 1)), 2)}
        r["tier"] = "alpha" if r["tgt_pg"] >= 8 and r["yds_pg"] >= 70 else "tier B" if r["tgt_pg"] >= 7 and r["yds_pg"] >= 55 else None
        r["style"] = "explosive" if r["ex_pg"] >= 1.2 and r["ex_share"] >= 0.5 else "volume" if r["tgt_pg"] >= 9 and r["ex_share"] < 0.45 else "both" if r["ex_pg"] >= 1.0 else "volume"
        if r["tier"]:
            rec.append(r)
    rec.sort(key=lambda r: (r["tier"] != "alpha", -r["yds_pg"]))
    # ---- defense profiles
    games_d = t.groupby("defteam").week.nunique()
    lead = pg[pg.pos.isin(["WR", "TE"])].sort_values("tgt", ascending=False).groupby(["defteam", "week"]).head(1)
    lead = lead[lead.tgt >= 8]
    ru = p[(p.rush_attempt == 1) & (p.qb_kneel != 1) & (p.rusher_player_id.map(pos) == "RB")]
    comp = t[t.complete_pass == 1]
    rb_rec = comp[comp.pos == "RB"]
    adv_r = pd.read_parquet(D / "adv_rush.parquet"); adv_d = pd.read_parquet(D / "adv_def.parquet")
    bt = adv_r.groupby("opponent").agg(bt=("rushing_broken_tackles", "sum"), yac=("rushing_yards_after_contact", "sum"), car=("carries", "sum"), g=("week", "nunique"))
    mt = adv_d.groupby("team").agg(mt=("def_missed_tackles", "sum"), g=("week", "nunique"))
    dfn = {}
    for d in games_d.index:
        n = games_d[d]
        x = pg[(pg.defteam == d) & pg.pos.isin(["WR", "TE"])]
        ld = lead[lead.defteam == d]
        r = ru[ru.defteam == d]
        dfn[d] = {"games": int(n), "ex_pg": round(t[t.defteam == d].ex.sum() / n, 2), "ex_wr_pg": round(t[(t.defteam == d) & (t.pos == "WR")].ex.sum() / n, 2),
                  "g80": int((x.yds >= 80).sum()), "g80_pg": round((x.yds >= 80).sum() / n, 2), "g100": int((x.yds >= 100).sum()),
                  "lead_games": int(len(ld)), "lead_yds": round(ld.yds.mean(), 1) if len(ld) else None, "lead_ex": round(ld.ex.mean(), 2) if len(ld) else None,
                  "lead_g80": int((ld.yds >= 80).sum()),
                  "pass_yds_pg": round(t[t.defteam == d].y.sum() / n, 1),
                  "rb_rush_pg": round(r.rushing_yards.sum() / n, 1), "rb_ypc": round(r.rushing_yards.sum() / max(len(r), 1), 2),
                  "rb_runs_10_pg": round((r.rushing_yards >= 10).sum() / n, 2), "rb_rec_yac_pg": round(rb_rec[rb_rec.defteam == d].yards_after_catch.sum() / n, 1),
                  "missed_tackles_pg": round(mt.loc[d].mt / mt.loc[d].g, 1) if d in mt.index else None,
                  "broken_tackles_by_backs_pg": round(bt.loc[d].bt / bt.loc[d].g, 1) if d in bt.index else None,
                  "yards_after_contact_per_carry": round(bt.loc[d].yac / max(bt.loc[d].car, 1), 2) if d in bt.index else None}
    for k, hi in (("ex_pg", True), ("g80_pg", True), ("lead_yds", True), ("rb_rush_pg", True), ("missed_tackles_pg", True), ("broken_tackles_by_backs_pg", True),
                  ("yards_after_contact_per_carry", True), ("rb_runs_10_pg", True)):
        order = sorted([d for d in dfn if dfn[d][k] is not None], key=lambda d: -dfn[d][k])
        for i, d in enumerate(order, 1):
            dfn[d][k + "_rank"] = i
    # ---- team game types (last five games)
    off = {}
    sc = p.groupby(["game_id", "posteam"]).agg(pass_yds=("passing_yards", "sum"), att=("pass_attempt", "sum"), rush=("rush_attempt", "sum"), week=("week", "first"),
                                                defteam=("defteam", "first")).reset_index()
    neutral = p[(p.qtr <= 3) & ((p.posteam_score - p.defteam_score).abs() <= 8) & ((p.pass_attempt == 1) | (p.rush_attempt == 1))]
    npr = neutral.groupby("posteam").pass_attempt.mean()
    lg_npr = neutral.pass_attempt.mean()
    for tm, g in sc.groupby("posteam"):
        g = g.sort_values("week").tail(5)
        opp = sc.set_index(["game_id", "posteam"]).pass_yds
        out_threw = sum(1 for x in g.itertuples() if x.pass_yds > opp.get((x.game_id, x.defteam), 0))
        off[tm] = {"pass_yds_l5": round(g.pass_yds.mean(), 1), "att_l5": round(g.att.mean(), 1), "out_threw_l5": int(out_threw), "games_l5": int(len(g)),
                   "neutral_pass_rate": round(float(npr.get(tm, lg_npr)), 3), "pass_first": bool(npr.get(tm, lg_npr) >= lg_npr + 0.03)}
    order = sorted(off, key=lambda k: -off[k]["pass_yds_l5"])
    for i, k in enumerate(order, 1):
        off[k]["pass_yds_l5_rank"] = i
    # ---- next week's matchups
    gm = pd.read_parquet(D / "games.parquet"); gm = gm[(gm.season == a.season) & (gm.week == a.week)]
    games = []
    for g in gm.itertuples():
        hi, ai = g.total_line / 2 + g.spread_line / 2, g.total_line / 2 - g.spread_line / 2
        kind = "shootout" if g.total_line >= 47 else "low scoring" if g.total_line <= 41 else "average"
        lop = abs(g.spread_line) >= 7
        games.append({"game_id": g.game_id, "day": g.weekday, "kickoff_et": g.gametime, "away": g.away_team, "home": g.home_team, "total": float(g.total_line),
                      "spread_home": float(g.spread_line), "implied": {g.home_team: round(hi, 2), g.away_team: round(ai, 2)}, "type": kind, "lopsided": bool(lop)})
    spots = []
    for g in games:
        for tm, op in ((g["home"], g["away"]), (g["away"], g["home"])):
            for r in rec:
                if r["team"] != tm:
                    continue
                d, imp = dfn.get(op, {}), g["implied"][tm]
                base = {"alpha": 0.41, "tier B": 0.30}[r["tier"]]
                # measured on 2022-2026: implied total thirds for alphas 31.5 / 41.7 / 50.0; for tier B 25.9 / 31.3 / 32.4
                env = ({"alpha": (0.315, 0.417, 0.50), "tier B": (0.26, 0.31, 0.325)}[r["tier"]])[0 if imp < 21.8 else 1 if imp < 25.7 else 2]
                head = d.get("g80_pg") is not None and d["g80_pg_rank"] >= 23        # rarely allows 80+ games: lowest third
                est = env - (0.07 if head else 0.0)
                flags = []
                if imp >= 25.7: flags.append("high team total")
                if imp < 21.8: flags.append("low team total")
                if off[tm]["pass_first"]: flags.append("pass-first offense")
                if head: flags.append("defense rarely allows 80+")
                if d.get("g80_pg_rank", 99) <= 8: flags.append("defense often allows 80+")
                if d.get("ex_pg_rank", 99) <= 8: flags.append("defense gives up big plays")
                if r["status"] not in (None, "ACT"): flags.append(f"roster status {r['status']}")
                spots.append({"game": g["game_id"], "player": r["player"], "pos": r["pos"], "team": tm, "opp": op, "tier": r["tier"], "style": r["style"],
                              "tgt_pg": r["tgt_pg"], "yds_pg": r["yds_pg"], "ex_pg": r["ex_pg"], "share_l3": r["share_l3"], "g80": r["g80"], "games": r["games"],
                              "implied": imp, "total": g["total"], "game_type": g["type"], "opp_g80": d.get("g80"), "opp_games": d.get("games"),
                              "opp_g80_rank": d.get("g80_pg_rank"), "opp_ex_pg": d.get("ex_pg"), "opp_ex_rank": d.get("ex_pg_rank"),
                              "tier_base": base, "estimate_80": round(est, 2), "flags": flags})
    spots.sort(key=lambda s: -s["estimate_80"])
    out = {"season": a.season, "week": a.week, "through_week": int(p.week.max()), "receivers": rec, "defenses": dfn, "offenses": off, "games": games, "spots": spots}
    f = HERE / f"slate_week{a.week}.json"
    f.write_text(json.dumps(out, indent=1, default=str))
    print(f, len(rec), "tiered receivers;", len(spots), "spots")


if __name__ == "__main__":
    main()
