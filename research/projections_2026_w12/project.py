"""Adjusted projections for the Week 12 holiday games (owner, Nov 25, 2026): the board's simulation, re-run with

  1. Injuries as the owner rules them: Out / Doubtful / IR do not play (the board already drops them); Questionable
     players play on limited snaps, at the measured 2026 snap share Questionable skill players kept when they played
     (backs 69%, tight ends 89%, receivers 91% of their usual; research/projections_2026_w12, this script's `qfactor`).
     Their lost work goes to teammates at the same position in proportion to share.
  2. Recent role: half the board's share, half the team's last two games, so a role that changed with an injury shows.
  3. Sharp coverage effects that tested real on 2026 Weeks 3-10 (research/blitz_targets_2026-11-24): per 10 points of
     man coverage above the league, the WR1 loses 0.66 points of target share (to backs and tight ends); per 10 points
     of blitz above the league, throws are 0.22 yards shorter (applied to yards per catch through the air part).
  Next Gen Stats public pages have no routes run (NFL Pro only), so separation and air-yard share are shown as context.

Side by side with the board; the board itself is not changed. Research only.

    python3 research/projections_2026_w12/project.py 2026_12_GB_LA
"""
from __future__ import annotations

import json
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from dashboard import opportunity as O  # noqa: E402

C = ROOT / "pregame" / ".cache"
QF = {"RB": 0.69, "TE": 0.89, "WR": 0.91}
MAN_WR1, MAN_RBTE = -0.066, 0.043          # share change per 1.0 of man rate above league (per 10 pts: -0.0066 / +0.0043)
BLITZ_ADOT = -2.17                         # yards of aDOT per 1.0 of blitz rate above league
SHARP = ROOT / "data_packages" / "sharp_advanced_2026_w1_10" / "team_games.jsonl"
CODE = {"LA": "LAR"}
N = 20000


def sharp_def():
    rows = [json.loads(l) for l in open(SHARP)]
    t = pd.DataFrame([{"opp": r["opponent"], **r["metrics"]} for r in rows])
    lg = {"blitz": t.blitz.sum() / t.db.sum(), "man": t.man.sum() / t["cov"].sum()}
    d = t.groupby("opp").agg(blitz=("blitz", "sum"), db=("db", "sum"), man=("man", "sum"), cov=("cov", "sum"))
    return {k: {"blitz": v.blitz / v.db, "man": v.man / v["cov"]} for k, v in d.iterrows()}, lg


def recent(team, ids_pos):
    p = pd.read_parquet(C / "play_by_play_2026.parquet", columns=["week", "season_type", "posteam", "receiver_player_id", "rusher_player_id",
                                                                   "pass_attempt", "rush_attempt", "qb_scramble", "sack", "two_point_attempt"])
    p = p[(p.season_type == "REG") & (p.posteam == team) & (p.two_point_attempt != 1)]
    wks = sorted(p.week.unique())[-2:]
    q = p[p.week.isin(wks)]
    tg = q[(q.pass_attempt == 1) & (q.sack != 1) & q.receiver_player_id.notna()]
    ca = q[(q.rush_attempt == 1) & (q.qb_scramble != 1) & q.rusher_player_id.isin([i for i, pp in ids_pos.items() if pp == "RB"])]
    q3 = p[p.week.isin(sorted(p.week.unique())[-3:])]
    touched = set(q3.receiver_player_id.dropna()) | set(q3.rusher_player_id.dropna())   # anyone with a touch in the last 3 games
    return wks, (tg.receiver_player_id.value_counts() / len(tg)).to_dict(), (ca.rusher_player_id.value_counts() / max(len(ca), 1)).to_dict(), touched


def status_map(gid):
    pk = json.loads((ROOT / "pregame" / "packets" / gid / "packet.json").read_text())
    out = {}
    for t, v in pk["teams"].items():
        for x in (v.get("injuries") or {}).get("espn_live") or []:
            out[x["player"].lower()] = x["status"]
        for x in (v.get("injuries") or {}).get("official_report") or []:
            nm = (x.get("player") or x.get("full_name") or "").lower()
            if nm:
                out[nm] = x.get("game_status") or x.get("status") or out.get(nm)
    return out


def main(gid):
    b = json.loads((ROOT / "dashboard" / "data" / f"{gid}.json").read_text())
    st = status_map(gid)
    sd, lg = sharp_def()
    pp = pd.read_parquet(C / "play_by_play_2025.parquet"); pp = pp[pp.season_type == "REG"]
    pr = pd.read_parquet(C / "roster_weekly_2025.parquet"); pr = pr[pr.game_type == "REG"]
    pools = O.league_pools(pp, pr)
    ngs = pd.read_parquet(C / "ngs_receiving.parquet")
    ngs = ngs[(ngs.season == 2026) & (ngs.week == 0)].set_index("player_gsis_id") if ((ngs.season == 2026) & (ngs.week == 0)).any() else None
    out = {"game_id": gid, "board_built_utc": b.get("board_built_utc"), "teams": {}}
    for s in b["sides"].values():
        off, dfn = s["offense"], s["defense"]
        op = s["opportunity"]
        rec = [e for e in op["receivers"] if not e.get("status") and e.get("sim")]
        rus = [e for e in op["rushers"] if not e.get("status") and e.get("sim")]
        ids = {e["player_id"]: e["pos"] for e in rec + rus}
        wks, rt, rc, touched = recent(off, ids)
        benched = [e["player"] for e in rec + rus if e["player_id"] not in touched]
        rec = [e for e in rec if e["player_id"] in touched]
        rus = [e for e in rus if e["player_id"] in touched]
        dd = sd.get(CODE.get(dfn, dfn), {})
        d_man, d_bl = dd.get("man", lg["man"]) - lg["man"], dd.get("blitz", lg["blitz"]) - lg["blitz"]

        def adjust(entries, key_used, recent_share, group_of):
            old = {e["player_id"]: e["inputs"][key_used] for e in entries}
            new = {i: 0.5 * old[i] + 0.5 * recent_share.get(i, 0.0) for i in old}
            tags = {}
            for e in entries:
                s_ = (st.get(e["player"].lower()) or "")
                if s_.lower().startswith("questionable"):
                    f = QF.get(e["pos"], 0.9)
                    freed = new[e["player_id"]] * (1 - f)
                    new[e["player_id"]] *= f
                    mates = [m for m in entries if group_of(m) == group_of(e) and m is not e]
                    tot = sum(new[m["player_id"]] for m in mates) or 1
                    for m in mates:
                        new[m["player_id"]] += freed * new[m["player_id"]] / tot
                    tags[e["player_id"]] = f"Questionable: {f:.0%} of usual snaps"
            k = min(1.0, sum(old.values())) / (sum(new.values()) or 1)   # the board's total for the group, never above 100%
            return {i: v * k for i, v in new.items()}, tags
        grp = lambda e: "RB" if e["pos"] == "RB" else ("TE" if e["pos"] == "TE" else "WR")
        new_t, tag_t = adjust(rec, "target_share_used", rt, grp)
        new_c, tag_c = adjust(rus, "carry_share_used", rc, lambda e: "RB")
        wr1 = max((e for e in rec if e["pos"] == "WR"), key=lambda e: new_t[e["player_id"]], default=None)
        if wr1 is not None and d_man:
            dlt = MAN_WR1 * d_man
            new_t[wr1["player_id"]] += dlt
            rbte = [e for e in rec if e["pos"] in ("RB", "TE")]
            tot = sum(new_t[e["player_id"]] for e in rbte) or 1
            for e in rbte:
                new_t[e["player_id"]] += -dlt * new_t[e["player_id"]] / tot
        team = {"offense": off, "defense": dfn, "recent_weeks": [int(w) for w in wks], "defense_man_vs_league": round(d_man, 3),
                "defense_blitz_vs_league": round(d_bl, 3), "out_of_rotation": benched, "receivers": [], "rushers": []}
        for e in rec:
            sm, i = e["sim"], e["player_id"]
            ratio = new_t[i] / max(e["inputs"]["target_share_used"], 1e-6)
            ypr = sm["ypr"] + 0.6 * BLITZ_ADOT * d_bl
            tg, rcp, yd = O.simulate_receiver(exp_targets=sm["targets_raw"] * ratio, k=sm["k"], catch_rate=sm["catch_rate"], ypr=max(ypr, 3),
                                              pool=pools["catch"][sm.get("pool", e["pos"])], rain_yards=sm.get("rain_yards", 1.0),
                                              rain_catch=sm.get("rain_catch", 1.0), n=N, seed=zlib.crc32(f"{gid}{i}".encode()))
            row = {"player": e["player"], "pos": e["pos"], "status": st.get(e["player"].lower()), "tag": tag_t.get(i),
                   "share_board": round(e["inputs"]["target_share_used"], 3), "share_adj": round(new_t[i], 3),
                   "targets": [e.get("targets_mean"), round(float(tg.mean()), 1)], "receptions": [e.get("receptions_mean"), round(float(rcp.mean()), 1)],
                   "yards": [e.get("yards_mean"), round(float(yd.mean()), 1)], "yards_median_adj": round(float(np.median(yd)), 1), "lines": {}}
            if ngs is not None and i in ngs.index:
                g = ngs.loc[i]
                row["ngs"] = {"separation": float(g.avg_separation), "air_yard_share": float(g.percent_share_of_intended_air_yards), "yac_over_exp": float(g.avg_yac_above_expectation)}
            for mk, arr, integer in (("receiving_yards", yd, False), ("receptions", rcp, True)):
                L = (e.get("book_lines") or {}).get(mk)
                if L and L.get("fair_line") is not None:
                    pz = float((arr > L["fair_line"]).mean())
                    if mk == "receiving_yards":
                        pz = O.calibrate(pz, "receiving_yards", L["fair_line"])
                    row["lines"][mk] = {"line": L["fair_line"], "p_over_adj": round(pz, 3), "market_over": L.get("fair_over")}
            team["receivers"].append(row)
        for e in rus:
            sm, i = e["sim"], e["player_id"]
            ratio = new_c[i] / max(e["inputs"]["carry_share_used"], 1e-6)
            car, yd = O.simulate_rusher(exp_carries=sm["carries_raw"] * ratio, k=sm["k"], ypc=sm["ypc"], pool=pools["carry"], n=N,
                                        seed=zlib.crc32(f"{gid}{i}r".encode()))
            row = {"player": e["player"], "status": st.get(e["player"].lower()), "tag": tag_c.get(i),
                   "share_board": round(e["inputs"]["carry_share_used"], 3), "share_adj": round(new_c[i], 3),
                   "carries": [e.get("carries_mean"), round(float(car.mean()), 1)], "yards": [e.get("yards_mean"), round(float(yd.mean()), 1)],
                   "yards_median_adj": round(float(np.median(yd)), 1), "lines": {}}
            L = (e.get("book_lines") or {}).get("rushing_yards")
            if L and L.get("fair_line") is not None:
                pz = O.calibrate(float((yd > L["fair_line"]).mean()), "rushing_yards", L["fair_line"])
                row["lines"]["rushing_yards"] = {"line": L["fair_line"], "p_over_adj": round(pz, 3), "market_over": L.get("fair_over")}
            team["rushers"].append(row)
        out["teams"][off] = team
    (Path(__file__).parent / f"{gid}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    return out


def show(o):
    for t in o["teams"].values():
        print(f"\n(out of the rotation, no touch in 3 games: {', '.join(t.get('out_of_rotation') or []) or 'none'})")
        print(f"=== {t['offense']} offense vs {t['defense']} (recent weeks {t['recent_weeks']}; their man {t['defense_man_vs_league']:+.1%}, blitz {t['defense_blitz_vs_league']:+.1%} vs league)")
        for r in sorted(t["receivers"], key=lambda r: -r["yards"][1]):
            ln = "; ".join(f"{k.split('_')[-1]} {v['line']:g}: over {v['p_over_adj']:.0%}" for k, v in r["lines"].items())
            ng = f" | NGS sep {r['ngs']['separation']:.1f}, air share {r['ngs']['air_yard_share']:.0f}%" if r.get("ngs") else ""
            print(f" {r['player'][:22]:22} {r['pos']} share {r['share_board']:.2f}->{r['share_adj']:.2f}  tgt {r['targets'][0]}->{r['targets'][1]}  rec {r['receptions'][0]}->{r['receptions'][1]}  yds {r['yards'][0]}->{r['yards'][1]} (med {r['yards_median_adj']})  {ln} {('['+r['tag']+']') if r['tag'] else ''}{ng}")
        for r in sorted(t["rushers"], key=lambda r: -r["yards"][1]):
            ln = "; ".join(f"line {v['line']:g}: over {v['p_over_adj']:.0%}" for v in r["lines"].values())
            print(f" {r['player'][:22]:22} RB share {r['share_board']:.2f}->{r['share_adj']:.2f}  car {r['carries'][0]}->{r['carries'][1]}  yds {r['yards'][0]}->{r['yards'][1]} (med {r['yards_median_adj']})  {ln} {('['+r['tag']+']') if r['tag'] else ''}")


if __name__ == "__main__":
    show(main(sys.argv[1]))
