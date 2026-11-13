#!/usr/bin/env python3
"""Grade FanDuel alt over rungs (Wk8-9 2026) vs nflverse actuals. Rules: ../PREREG_BACKTEST.md.
Usage: grade_alt_ladders.py --nflverse DIR --wk9-pr41-raw DIR --out DIR
Research only. No engine changes. projection_ready stays false.

Review fixes (PR #42, refs NFL-75): Joshua/Josh first-name alias is a name-matching
bug fix only (pre-registered grading rules unchanged). Tables report player-game
(and game) cluster-bootstrap CIs for margin and ROI; independent-rung Wilson CIs
are labeled as too narrow. nflverse inputs are sha256-pinned in meta.json.
"""
from __future__ import annotations
import argparse, glob, hashlib, json, math, re, unicodedata
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw"
MK = {"player_rush_yds_alternate": "rush", "player_reception_yds_alternate": "rec"}

# Cluster bootstrap (fixed; reported in meta.json / tables.md / REPORT.md).
BOOT_SEED = 20261113
BOOT_REPS = 10_000

NFLVERSE_FILES = [
    ("play_by_play_2026.parquet",
     "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet"),
    ("roster_weekly_2026.parquet",
     "https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/roster_weekly_2026.parquet"),
    ("snap_counts_2026.parquet",
     "https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_2026.parquet"),
]

# Joshua <-> Josh only; applied when the exact name match is empty. Not a grading-rule change.
FIRST_NAME_ALIASES = {"joshua": "josh", "josh": "joshua"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`\-]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def query_keys(player, exact_only=False):
    k = norm(player)
    keys = {k}
    if exact_only:
        return keys
    parts = k.split()
    if parts and parts[0] in FIRST_NAME_ALIASES:
        keys.add(" ".join([FIRST_NAME_ALIASES[parts[0]], *parts[1:]]).strip())
    return keys


def dec(am):
    am = float(am)
    return 1 + am / 100 if am > 0 else 1 + 100 / -am


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def pin_nflverse(nv: Path):
    rows = []
    for name, url in NFLVERSE_FILES:
        p = nv / name
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        ts_path = nv / f"{name}.retrieved_utc"
        pull_time = None
        if ts_path.exists():
            raw = ts_path.read_text().strip()
            pull_time = raw.replace("+00:00", "Z")
            if pull_time.endswith("UTC"):
                pull_time = pull_time[:-3].strip() + "Z"
        rows.append({
            "path": name,
            "url": url,
            "source": "nflverse public release (github.com/nflverse/nflverse-data)",
            "pull_time": pull_time,
            "sha256": sha,
        })
    return rows


def cluster_boot_ci(g, cluster_cols, seed=BOOT_SEED, reps=BOOT_REPS):
    """Percentile 95% CIs for (hit-avg_be, ROI) by resampling clusters with replacement.

    Each cluster's rungs travel together. Quantiles use numpy's default linear method.
    Returns None bounds when there are fewer than 2 clusters.
    """
    nan = {"margin_lo": None, "margin_hi": None, "roi_lo": None, "roi_hi": None, "n_clusters": 0}
    if g is None or g.empty:
        return nan
    cl = g.groupby(cluster_cols, sort=False).agg(
        n=("win", "size"), wins=("win", "sum"), profit=("profit", "sum"), be_sum=("be", "sum"),
    )
    n_cl = len(cl)
    if n_cl < 2:
        return {**nan, "n_clusters": int(n_cl)}
    n = cl.n.to_numpy(dtype=float)
    wins = cl.wins.to_numpy(dtype=float)
    profit = cl.profit.to_numpy(dtype=float)
    be_sum = cl.be_sum.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n_cl, size=(reps, n_cl))
    n_b = n[idx].sum(axis=1)
    ok = n_b > 0
    margin_b = np.full(reps, np.nan)
    roi_b = np.full(reps, np.nan)
    margin_b[ok] = wins[idx][ok].sum(axis=1) / n_b[ok] - be_sum[idx][ok].sum(axis=1) / n_b[ok]
    roi_b[ok] = profit[idx][ok].sum(axis=1) / n_b[ok]
    lo_m, hi_m = np.nanquantile(margin_b, [0.025, 0.975])
    lo_r, hi_r = np.nanquantile(roi_b, [0.025, 0.975])
    return {
        "margin_lo": float(lo_m), "margin_hi": float(hi_m),
        "roi_lo": float(lo_r), "roi_hi": float(hi_r),
        "n_clusters": int(n_cl),
    }


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


def roster_mask(rw, keys):
    return (rw.full_name.map(norm).isin(keys)) | (
        (rw.football_name.fillna("") + " " + rw.last_name.fillna("")).map(norm).isin(keys)
    )


def match_player(rw, player):
    """Exact full_name or football_name+last_name first; Joshua/Josh alias only if exact is empty."""
    exact = rw[roster_mask(rw, query_keys(player, exact_only=True))]
    n_exact = exact.gsis_id.nunique()
    if n_exact == 1:
        return exact, False
    if n_exact > 1:
        return exact, False
    aliased = rw[roster_mask(rw, query_keys(player, exact_only=False))]
    return aliased, aliased.gsis_id.nunique() == 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nflverse", required=True); ap.add_argument("--wk9-pr41-raw", required=True)
    ap.add_argument("--out", default=str(HERE))
    a = ap.parse_args(); nv = Path(a.nflverse); out = Path(a.out)
    R, hashes = load_rungs(a.wk9_pr41_raw)
    nflverse_inputs = pin_nflverse(nv)
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
    out_rows, unmatched, voids, alias_matches = [], set(), set(), []
    cache = {}
    for (gid, wk, player), grp in R.groupby(["game_id", "week", "player"]):
        _, _, away, home = gid.split("_")
        rw = ros[(ros.week == wk) & (ros.team.isin([away, home]))]
        cand, used_alias = match_player(rw, player)
        if cand.gsis_id.nunique() != 1:
            unmatched.add((gid, player, int(cand.gsis_id.nunique()))); continue
        pid = cand.gsis_id.iloc[0]; team = cand.team.iloc[0]; pos = cand.position.iloc[0]
        if used_alias:
            roster_name = cand.full_name.iloc[0]
            alias_matches.append({
                "game_id": gid, "listed_name": player, "roster_name": roster_name,
                "gsis_id": pid, "note": "Joshua/Josh first-name alias (name-matching bug fix)",
            })
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
            pg = cluster_boot_ci(g, ["game_id", "player"])
            gm = cluster_boot_ci(g, ["game_id"])
            rows.append({**dict(zip(by if isinstance(by, list) else [by], k if isinstance(k, tuple) else [k])),
                         "n_rungs": n, "n_player_games": g[["game_id", "player"]].drop_duplicates().shape[0],
                         "n_games": g.game_id.nunique(), "wins": w, "hit": w / n,
                         "wilson_indep_rung_ci_lo": lo, "wilson_indep_rung_ci_hi": hi,
                         "avg_be": g.be.mean(), "margin": w / n - g.be.mean(), "roi": g.profit.sum() / n,
                         "margin_pg_ci_lo": pg["margin_lo"], "margin_pg_ci_hi": pg["margin_hi"],
                         "roi_pg_ci_lo": pg["roi_lo"], "roi_pg_ci_hi": pg["roi_hi"],
                         "margin_game_ci_lo": gm["margin_lo"], "margin_game_ci_hi": gm["margin_hi"],
                         "roi_game_ci_lo": gm["roi_lo"], "roi_game_ci_hi": gm["roi_hi"]})
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
    ci_note = (
        f"CI notes: `wilson_indep_rung_ci_*` treats every rung as independent and is too narrow "
        f"(one game settles a whole ladder), except on `rico_floor_one_rung_per_player_game` where "
        f"n_rungs = n_player_games. `*_pg_ci_*` = cluster bootstrap over player-games; "
        f"`*_game_ci_*` = cluster bootstrap over games. Both are percentile 95% intervals on "
        f"margin (hit − mean break-even) and flat 1u ROI. seed={BOOT_SEED}, reps={BOOT_REPS}, "
        f"numpy default_rng + nanquantile (linear).\n\n"
    )
    with open(out / "tables.md", "w") as f:
        f.write(ci_note)
        for name, t in tabs.items():
            f.write(f"## {name}\n\n")
            f.write(t.to_markdown(index=False, floatfmt=".3f") if not t.empty else "(empty)\n")
            f.write("\n\n")
    meta = {"n_rungs_raw": len(R), "n_graded": len(G), "n_player_games_graded": G[["game_id", "player"]].drop_duplicates().shape[0],
            "games": int(G.game_id.nunique()), "unmatched_player_names": sorted([list(u) for u in unmatched]),
            "void_no_offense_snaps": sorted([list(v) for v in voids]),
            "rungs_unmatched": int(R.merge(pd.DataFrame([(u[0], u[1]) for u in unmatched], columns=["game_id", "player"])).shape[0]) if unmatched else 0,
            "rungs_void": int(R.merge(pd.DataFrame(list(voids), columns=["game_id", "player"])).shape[0]) if voids else 0,
            "name_match_bugfix": {
                "description": "Joshua/Josh first-name alias applied only when the exact full_name or football_name+last_name match is empty. Pre-registered grading rules unchanged.",
                "alias_matches": alias_matches,
            },
            "cluster_bootstrap": {"seed": BOOT_SEED, "reps": BOOT_REPS, "method": "resample clusters with replacement; percentile 95% CI (numpy nanquantile, linear) on margin=hit-mean(BE) and ROI=profit/n; clusters = player-game (game_id, player) and game (game_id)"},
            "nflverse_inputs": nflverse_inputs,
            "input_sha256": hashes}
    json.dump(meta, open(out / "meta.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in meta.items() if k != "input_sha256"}, indent=1))
    print(open(out / "tables.md").read())

if __name__ == "__main__":
    main()
