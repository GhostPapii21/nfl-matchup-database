import json, glob, csv, re
import pandas as pd
from penparse import parse_penalties
AF = {"DPI", "Roughing the Passer", "Face Mask", "Defensive Holding", "Illegal Contact"}
rows, box = [], []
for w in range(1, 9):
    for e in json.load(open(f"espn_raw/sb_{w}.json"))["events"]:
        if not e["status"]["type"]["completed"]: continue
        d = json.load(open(f"espn_raw/sum_{e['id']}.json"))
        tid = {c["team"]["id"]: c["team"]["abbreviation"] for c in e["competitions"][0]["competitors"]}
        for t in d["boxscore"]["teams"]:
            st = {s["name"]: s["displayValue"] for s in t["statistics"]}
            n, y = st.get("totalPenaltiesYards", "0-0").split("-")
            box.append(dict(week=w, game_id=e["id"], team=t["team"]["abbreviation"], box_pen=int(n), box_pen_yds=int(y), off_plays=int(st.get("totalOffensivePlays", 0))))
        for dr in d.get("drives", {}).get("previous", []):
            off = dr["team"]["abbreviation"]
            for p in dr["plays"]:
                if "penalty" not in p.get("text", "").lower(): continue
                s, en = p.get("start", {}), p.get("end", {})
                for x in parse_penalties(p["text"]):
                    side = "offense" if x["team"] == off else "defense"
                    acc = x["status"] == "accepted"
                    auto = acc and side == "defense" and x["type_norm"] in AF
                    ext = acc and side == "defense" and s.get("down") in (3, 4) and en.get("down") == 1
                    q = p["period"]["number"]
                    rows.append(dict(season=2026, week=w, game_id=e["id"], date=e["date"][:10], team_penalized=x["team"], side=side,
                        play_type=p.get("type", {}).get("text", ""), quarter=("OT" if q > 4 else f"Q{q}"), clock=p["clock"]["displayValue"],
                        penalty_type=x["type"], penalty_type_norm=x["type_norm"], yards=x["yards"], status=x["status"], no_play=x["no_play"],
                        player=x["player"], down=s.get("down"), distance=s.get("distance"), drive_id=dr["id"], drive_team=off,
                        drive_outcome=dr.get("displayResult", dr.get("result")), auto_first_down=auto, drive_extended=ext or auto,
                        text=re.sub(r"\s+", " ", p["text"])))
pp = pd.DataFrame(rows).drop_duplicates(["game_id","drive_id","quarter","clock","text","penalty_type","player"]); pp.to_csv("penalty_plays_2026.csv", index=False)
bx = pd.DataFrame(box)
a = pp[pp.status == "accepted"]
o = a[a.side == "offense"]
def cnt(df, name, cond=None):
    df = df if cond is None else df[cond(df)]
    return df.groupby(["game_id", "team_penalized"]).size().rename(name)
parts = [cnt(o, "off_pen"), cnt(o, "off_pen_10plus", lambda d: d.yards >= 10)]
for q in ["Q1", "Q2", "Q3", "Q4", "OT"]: parts.append(cnt(o, f"off_pen_{q}", lambda d, q=q: d.quarter == q))
for nm, t in [("false_start", "False Start/Offside"), ("off_holding", "Offensive Holding"), ("illegal_form_shift_motion", "Illegal Formation/Shift/Motion"), ("opi", "OPI")]:
    parts.append(cnt(o, nm, lambda d, t=t: d.penalty_type_norm == t))
dd = a[(a.side == "defense") & a.drive_extended]
for nm, t in [("def_dpi", "DPI"), ("def_rtp", "Roughing the Passer"), ("def_facemask", "Face Mask"), ("def_holding", "Defensive Holding"), ("def_illegal_contact", "Illegal Contact")]:
    parts.append(cnt(dd, nm, lambda d, t=t: d.penalty_type_norm == t))
parts.append(cnt(dd, "def_other_auto_first", lambda d: ~d.penalty_type_norm.isin(AF)))
parts.append(cnt(dd, "def_drive_extending_total"))
parts.append(cnt(a, "pbp_accepted_pen")); parts.append(a.groupby(["game_id", "team_penalized"]).yards.sum().rename("pbp_accepted_yds"))
tg = pd.concat(parts, axis=1).fillna(0).astype(int).reset_index().rename(columns={"team_penalized": "team"})
tg = bx.merge(tg, on=["game_id", "team"], how="left").fillna(0)
tg["snaps_source"] = "ESPN box totalOffensivePlays (plays run; excludes no-play penalties)"
tg["recon_count_diff"] = tg.pbp_accepted_pen - tg.box_pen; tg["recon_yds_diff"] = tg.pbp_accepted_yds - tg.box_pen_yds
tg.to_csv("penalties_2026.csv", index=False)
g = tg.groupby("team").agg(games=("game_id", "nunique"), off_pen=("off_pen", "sum"), off_plays=("off_plays", "sum"), false_start=("false_start", "sum"),
    off_holding=("off_holding", "sum"), def_ext=("def_drive_extending_total", "sum"), tot_pen=("box_pen", "sum"), tot_yds=("box_pen_yds", "sum")).reset_index()
for c in ["off_pen", "false_start", "off_holding", "def_ext", "tot_pen", "tot_yds"]: g[f"{c}_pg"] = g[c] / g.games
g["off_pen_per60"] = g.off_pen / g.off_plays * 60; g["def_ext_per60_opp"] = None
g.sort_values("off_pen_per60", ascending=False).to_csv("penalty_rates_2026.csv", index=False)
print(len(pp), len(tg)); print("recon mismatches:", (tg.recon_count_diff != 0).sum(), "yds:", (tg.recon_yds_diff != 0).sum())
print(tg[tg.week == 8][tg.team.isin(["KC", "LAR"])][["team", "box_pen", "box_pen_yds", "pbp_accepted_pen", "pbp_accepted_yds", "false_start"]])
