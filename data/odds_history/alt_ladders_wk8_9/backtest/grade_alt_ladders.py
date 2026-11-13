#!/usr/bin/env python3
"""Grade FanDuel alt over rungs (Wk8-9 2026) vs nflverse actuals. Rules: ../PREREG_BACKTEST.md.
Usage: grade_alt_ladders.py --nflverse DIR --wk9-pr41-raw DIR --out DIR
Research only. No engine changes. projection_ready stays false.
"""
from __future__ import annotations
import argparse, glob, hashlib, json, math, re, unicodedata
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw"
MK = {"player_rush_yds_alternate": "rush", "player_reception_yds_alternate": "rec"}

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`\-]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()

def dec(am):
    am = float(am)
    return 1 + am / 100 if am > 0 else 1 + 100 / -am

def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)

def load_rungs(wk9_dir):
    files = sorted(glob.glob(str(RAW / "2026_*__*.json"))) + sorted(glob.glob(str(Path(wk9_dir) / "2026_09_*.json")))
    rows, hashes = [], {}
    for f in files:
        hashes[Path(f).name] = hashlib.sha256(Path(f).read_bytes()).hexdigest()
        blob = json.load(open(f)); gid = blob["meta"]["game_id"]
        for b in blob["response"]["data"]["bookmakers"]:
            if b["key"] != "fanduel":
                continue
            for m in b["markets"]:
                if m["key"] not in MK:
                    continue
                for o in m["outcomes"]:
                    if o["name"] != "Over":
                        continue
                    rows.append({"game_id": gid, "week": int(gid[5:7]), "market": MK[m["key"]], "player": o["description"],
                                 "rung": float(o["point"]), "price": int(o["price"])})
    return pd.DataFrame(rows), hashes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nflverse", required=True); ap.add_argument("--wk9-pr41-raw", required=True)
    ap.add_argument("--out", default=str(HERE))
    a = ap.parse_args(); nv = Path(a.nflverse); out = Path(a.out)
    R, hashes = load_rungs(a.wk9_pr41_raw)
    pbp = pd.read_parquet(nv / "play_by_play_2026.parquet")
    pbp = pbp[(pbp.season_type == "REG") & (pbp.week <= 9) & (pbp.two_point_attempt.fillna(0) == 0)]
    ros = pd.read_parquet(nv / "roster_weekly_2026.parquet")
    snaps = pd.read_parquet(nv / "snap_counts_2026.parquet")
    snaps = snaps[snaps.week <= 9]

    # per player-game stats keyed by gsis id
    ru = pbp[pbp.rusher_player_id.notna()].groupby(["game_id", "week", "posteam", "rusher_player_id"]).agg(
        ry=("rushing_yards", lambda s: s.fillna(0).sum()), car=("rush_attempt", "sum")).reset_index().rename(columns={"rusher_player_id": "pid"})
    lr = pbp[pbp.lateral_rusher_player_id.notna()].groupby(["game_id", "lateral_rusher_player_id"]).lateral_rushing_yards.sum()
    rc = pbp[pbp.receiver_player_id.notna()].groupby(["game_id", "week", "posteam", "receiver_player_id"]).agg(
        recy=("receiving_yards", lambda s: s.fillna(0).sum()), tgt=("pass_attempt", "size")).reset_index().rename(columns={"receiver_player_id": "pid"})
    lc = pbp[pbp.lateral_receiver_player_id.notna()].groupby(["game_id", "lateral_receiver_player_id"]).lateral_receiving_yards.sum()
    team_car = pbp[(pbp.rush_attempt == 1) & (pbp.qb_kneel.fillna(0) == 0)].groupby(["game_id", "posteam"]).size().rename("team_car")
    team_tgt = pbp[pbp.receiver_player_id.notna()].groupby(["game_id", "posteam"]).size().rename("team_tgt")
    car_k = pbp[(pbp.rush_attempt == 1) & (pbp.qb_kneel.fillna(0) == 0) & pbp.rusher_player_id.notna()].groupby(
        ["game_id", "posteam", "rusher_player_id"]).size()

    # games played = offense snaps > 0 (pfr id via roster)
    pfr2gsis = ros.dropna(subset=["pfr_id", "gsis_id"]).drop_duplicates("pfr_id").set_index("pfr_id").gsis_id
    snaps = snaps.assign(pid=snaps.pfr_player_id.map(pfr2gsis))
    played = snaps[snaps.offense_snaps.fillna(0) > 0][["game_id", "week", "team", "pid", "offense_snaps"]].dropna(subset=["pid"])

    def stat(gid, pid, team):
        r = ru[(ru.game_id == gid) & (ru.pid == pid)]; c = rc[(rc.game_id == gid) & (rc.pid == pid)]
        ry = float(r.ry.sum()) + float(lr.get((gid, pid), 0) or 0)
        recy = float(c.recy.sum()) + float(lc.get((gid, pid), 0) or 0)
        tc = team_car.get((gid, team), 0); tt = team_tgt.get((gid, team), 0)
        cs = car_k.get((gid, team, pid), 0) / tc if tc else None
        ts = float(c.tgt.sum()) / tt if tt else None
        return ry, recy, cs, ts

    # roster lookup for matching names per game
    out_rows, unmatched, voids = [], set(), set()
    cache = {}
    for (gid, wk, player), grp in R.groupby(["game_id", "week", "player"]):
        _, _, away, home = gid.split("_")
        rw = ros[(ros.week == wk) & (ros.team.isin([away, home]))]
        key = norm(player)
        cand = rw[(rw.full_name.map(norm) == key) | ((rw.football_name.fillna("") + " " + rw.last_name.fillna("")).map(norm) == key)]
        if cand.gsis_id.nunique() != 1:
            unmatched.add((gid, player, int(cand.gsis_id.nunique()))); continue
        pid = cand.gsis_id.iloc[0]; team = cand.team.iloc[0]; pos = cand.position.iloc[0]
        pg = played[(played.game_id == gid) & (played.pid == pid)]
        if pg.empty:
            voids.add((gid, player)); continue
        if pid not in cache:
            hist = played[played.pid == pid].sort_values("week")
            cache[pid] = [(int(h.week), h.game_id, h.team, *stat(h.game_id, pid, h.team)) for h in hist.itertuples()]
        hist = cache[pid]
        prior = [h for h in hist if h[0] < wk]
        cur = [h for h in hist if h[1] == gid][0]
        last4 = prior[-4:]
        rb_gate = pos == "RB" and len(last4) >= 3 and sum((h[5] or 0) >= 0.60 for h in last4) >= 3
        ts_gate = pos in ("WR", "TE") and len(last4) >= 3 and sum((h[6] or 0) >= 0.15 for h in last4) >= 3
        for r in grp.itertuples():
            actual = cur[3] if r.market == "rush" else cur[4]
            tm = (sum(h[3] for h in prior) / len(prior) if r.market == "rush" else sum(h[4] for h in prior) / len(prior)) if prior else None
            d = dec(r.price)
            win = actual >= r.rung
            out_rows.append({"game_id": gid, "week": wk, "player": player, "gsis_id": pid, "team": team, "pos": pos,
                             "market": r.market, "rung": r.rung, "price": r.price, "dec": d, "be": 1 / d,
                             "actual": actual, "win": int(win), "profit": (d - 1) if win else -1.0,
                             "trail_mean": tm, "n_prior": len(prior), "rb60_gate": rb_gate, "tshare15_gate": ts_gate})
    G = pd.DataFrame(out_rows)

    def relband(r):
        if r.trail_mean is None or pd.isna(r.trail_mean) or r.n_prior == 0:
            return "no prior games"
        if r.trail_mean <= 0:
            return ">100%"
        x = r.rung / r.trail_mean
        return "<=50%" if x <= .5 else "50-75%" if x <= .75 else "75-100%" if x <= 1 else ">100%"
    def absband(r):
        e = [9.5, 24.5, 49.5, 74.5, 99.5] if r.market == "rush" else [19.5, 39.5, 59.5, 79.5, 99.5]
        lab = (["<=9.5", "10-24.5", "25-49.5", "50-74.5", "75-99.5", ">=100"] if r.market == "rush"
               else ["<=19.5", "20-39.5", "40-59.5", "60-79.5", "80-99.5", ">=100"])
        for i, edge in enumerate(e):
            if r.rung <= edge:
                return lab[i]
        return lab[-1]
    G["rel_band"] = G.apply(relband, axis=1); G["abs_band"] = G.apply(absband, axis=1)
    G["rico_floor"] = (((G.market == "rush") & G.rb60_gate) | ((G.market == "rec") & G.tshare15_gate)) & \
        G.trail_mean.notna() & (G.rung <= G.trail_mean)

    def summ(df, by):
        rows = []
        for k, g in df.groupby(by, sort=False):
            n = len(g); w = int(g.win.sum()); lo, hi = wilson(w, n)
            rows.append({**dict(zip(by if isinstance(by, list) else [by], k if isinstance(k, tuple) else [k])),
                         "n_rungs": n, "n_player_games": g[["game_id", "player"]].drop_duplicates().shape[0],
                         "n_games": g.game_id.nunique(), "wins": w, "hit": w / n, "ci_lo": lo, "ci_hi": hi,
                         "avg_be": g.be.mean(), "margin": w / n - g.be.mean(), "roi": g.profit.sum() / n})
        return pd.DataFrame(rows)
    relorder = ["<=50%", "50-75%", "75-100%", ">100%", "no prior games"]
    G["rel_band"] = pd.Categorical(G.rel_band, relorder, ordered=True)
    tabs = {
        "overall": summ(G, ["market"]),
        "by_rel_band": summ(G.sort_values("rel_band"), ["market", "rel_band"]),
        "by_abs_band": summ(G, ["market", "abs_band"]),
        "by_week": summ(G, ["market", "week"]),
        "rico_floor": summ(G[G.rico_floor], ["market"]),
        "rico_floor_by_rel_band": summ(G[G.rico_floor].sort_values("rel_band"), ["market", "rel_band"]),
        "rico_floor_by_week": summ(G[G.rico_floor], ["market", "week"]),
        "gated_all_rungs_by_rel_band": summ(G[((G.market == "rush") & G.rb60_gate) | ((G.market == "rec") & G.tshare15_gate)].sort_values("rel_band"), ["market", "rel_band"]),
    }
    # one rung per player-game (lowest rung >= ... ): decorrelated sensitivity = the single rung closest to 75% of trailing mean in rico_floor
    rf = G[G.rico_floor].copy()
    if not rf.empty:
        rf["dist"] = (rf.rung / rf.trail_mean - 0.75).abs()
        one = rf.sort_values("dist").groupby(["game_id", "player", "market"]).head(1)
        tabs["rico_floor_one_rung_per_player_game"] = summ(one, ["market"])
    out.mkdir(parents=True, exist_ok=True)
    G.to_csv(out / "graded_rungs.csv", index=False)
    with open(out / "tables.md", "w") as f:
        for name, t in tabs.items():
            f.write(f"## {name}\n\n")
            f.write(t.to_markdown(index=False, floatfmt=".3f") if not t.empty else "(empty)\n")
            f.write("\n\n")
    meta = {"n_rungs_raw": len(R), "n_graded": len(G), "n_player_games_graded": G[["game_id", "player"]].drop_duplicates().shape[0],
            "games": int(G.game_id.nunique()), "unmatched_player_names": sorted([list(u) for u in unmatched]),
            "void_no_offense_snaps": sorted([list(v) for v in voids]),
            "rungs_unmatched": int(R.merge(pd.DataFrame([(u[0], u[1]) for u in unmatched], columns=["game_id", "player"])).shape[0]) if unmatched else 0,
            "rungs_void": int(R.merge(pd.DataFrame(list(voids), columns=["game_id", "player"])).shape[0]) if voids else 0,
            "input_sha256": hashes}
    json.dump(meta, open(out / "meta.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in meta.items() if k != "input_sha256"}, indent=1))
    print(open(out / "tables.md").read())

if __name__ == "__main__":
    main()
