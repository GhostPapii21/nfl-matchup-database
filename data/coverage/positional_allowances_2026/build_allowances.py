"""Positional defensive allowances for 2026: WR1/WR2/WR3, TE, RB (rush + receiving), QB, by window, with
opponent adjustment, depth and field-location splits, situational splits, and Sharp per-game man/blitz/pressure windows.

Research only. projection_ready stays false. Changes no betting rule, gate, weight, skill or pregame/*.py file.
Reads only free inputs already pulled: nflverse play-by-play, weekly rosters, snap counts, FTN charting (via nflverse),
and the committed Sharp advanced box-score package (data_packages/sharp_advanced_2026_w1_10).

    python3 data/coverage/positional_allowances_2026/build_allowances.py --raw /path/to/raw [--through-week N]

`--raw` must hold play_by_play_2026.parquet, roster_weekly_2026.parquet, snap_counts_2026.parquet and
ftn_charting_2026.parquet. Each file's sha256 is checked against EXPECTED_SHA (the pull recorded in
data/coverage/defender_profiles_2026/MANIFEST.json on PR #143, pulled 2026-11-27T12:26Z). A mismatch stops the build
unless --allow-new-inputs is passed, in which case the new hashes are written to MANIFEST.json.

Definitions (also in README.md):
  * Target = pass attempt, not a sack, with a receiver id. Yards = the receiver's receiving_yards on completions
    (lateral yards excluded, box-score basis). Explosive reception = 20+ receiving yards.
  * Depth from air_yards: short < 10 (includes behind the line), intermediate 10-19, deep 20+. Missing air_yards = unknown.
  * Location from pass_location (offense's view): middle vs outside (left or right). This is NOT slot vs outside.
  * WR1/WR2/WR3 for an offense in a game: WRs who took an offensive snap in that game (snap counts) or were targeted,
    ranked by that player's targets for that team in EARLIER games of the season; ties broken by this game's offensive
    snaps. Week-1 ranks are therefore snap-based. Anything past WR3 is WR_other.
  * Opponent adjustment (leave-one-out): for a defense-game, allowed minus the offense's own per-game average for that
    group in its other games inside the build window. Window value = mean over the window's games.
  * Windows: a defense's last 3 / 5 / 10 games played and the full season, through --through-week.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SHARP_PKG = REPO / "data_packages" / "sharp_advanced_2026_w1_10"

EXPECTED_SHA = {
    "play_by_play_2026.parquet": "e0f532a73338bbd4cd68723bf6136daed8ec517455d93e51a1f939fe7880fb97",
    "roster_weekly_2026.parquet": "42ad550d2948b27c4ef03676c58e1a2c75336ea5f023d96f75a34966b49c9806",
    "snap_counts_2026.parquet": "a671bbfca0a9079abfd71e2a35f0d062ec7c2e1d13b7b6e1a6f6f9c653e10c23",
    "ftn_charting_2026.parquet": "ee09d5f28f5fe1637267cf5588ab9135d3706af834b83d2814ba0ba97ee1cac0",
}
SOURCE_URLS = {
    "play_by_play_2026.parquet": "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet",
    "roster_weekly_2026.parquet": "https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/roster_weekly_2026.parquet",
    "snap_counts_2026.parquet": "https://github.com/nflverse/nflverse-data/releases/download/snap_counts/snap_counts_2026.parquet",
    "ftn_charting_2026.parquet": "https://github.com/nflverse/nflverse-data/releases/download/ftn_charting/ftn_charting_2026.parquet",
}
PULLED_UTC = "2026-11-27T12:26:11Z"
SHARP_TEAM_FIX = {"LAR": "LA"}

WINDOWS = {"season": None, "L10": 10, "L5": 5, "L3": 3}
GROUPS = ["WR1", "WR2", "WR3", "WR_other", "TE", "RB", "other"]
REC_METRICS = ["tgt", "rec", "yds", "td", "int", "explo20", "rz_tgt",
               "short_tgt", "short_rec", "short_yds", "inter_tgt", "inter_rec", "inter_yds",
               "deep_tgt", "deep_rec", "deep_yds", "depth_unknown_tgt",
               "middle_tgt", "middle_yds", "outside_tgt", "outside_yds", "loc_unknown_tgt"]
RUSH_METRICS = ["rb_rush_att", "rb_rush_yds", "rb_rush_td", "rb_rush_explo10", "rb_rush_explo20", "rb_rush_succ",
                "rb_screen_tgt", "rb_screen_rec", "rb_screen_yds", "rb_behind_los_tgt", "rb_behind_los_yds"]
QB_METRICS = ["dropbacks", "pass_att", "cmp", "pass_yds", "pass_td", "pass_int", "sacks",
              "scrambles", "scramble_yds", "qb_designed_runs", "qb_designed_yds"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_inputs(raw: Path, allow_new: bool) -> dict:
    got = {}
    for name, exp in EXPECTED_SHA.items():
        p = raw / name
        if not p.exists():
            raise SystemExit(f"missing input {p}")
        got[name] = sha256(p)
        if got[name] != exp and not allow_new:
            raise SystemExit(f"sha256 mismatch for {name}: {got[name]} != {exp}. Pass --allow-new-inputs to rebuild "
                             "from a newer pull; the new hash is then recorded in MANIFEST.json.")
    return got


# ----------------------------------------------------------------------------------------------- play selection
def scrimmage(p: pd.DataFrame) -> pd.DataFrame:
    """Regular-season pass and run plays. Kneels, spikes, two-point tries, kicks and no-plays are excluded."""
    m = (p["season_type"] == "REG") & p["play_type"].isin(["pass", "run"])
    for c in ("qb_kneel", "qb_spike", "two_point_attempt"):
        if c in p:
            m &= p[c].fillna(0) == 0
    return p[m].copy()


def depth_bucket(air) -> str:
    if air is None or (isinstance(air, float) and math.isnan(air)):
        return "unknown"
    if air < 10:
        return "short"
    if air < 20:
        return "inter"
    return "deep"


def loc_bucket(loc) -> str:
    if loc == "middle":
        return "middle"
    if loc in ("left", "right"):
        return "outside"
    return "unknown"


# ----------------------------------------------------------------------------------------------- positions / ranks
def position_lookup(rosters: pd.DataFrame) -> tuple[dict, dict]:
    r = rosters[["gsis_id", "week", "team", "position"]].dropna(subset=["gsis_id"])
    by_week = {(g, int(w)): pos for g, w, pos in zip(r.gsis_id, r.week, r.position)}
    season = r.groupby("gsis_id")["position"].agg(lambda s: s.mode().iat[0]).to_dict()
    return by_week, season


def pos_of(pid, week, by_week, season) -> str:
    pos = by_week.get((pid, int(week))) or season.get(pid)
    if pos == "FB":
        return "RB"
    return pos if pos in ("WR", "TE", "RB", "QB") else "other"


def active_wrs(snaps: pd.DataFrame, rosters: pd.DataFrame) -> pd.DataFrame:
    """WRs with an offensive snap per (game_id, team), mapped to gsis ids by pfr id, then by name within team-week."""
    s = snaps[(snaps["position"] == "WR") & (snaps["offense_snaps"].fillna(0) > 0)][
        ["game_id", "week", "team", "player", "pfr_player_id", "offense_snaps"]].copy()
    r = rosters.dropna(subset=["gsis_id"])
    by_pfr = r.dropna(subset=["pfr_id"]).drop_duplicates("pfr_id").set_index("pfr_id")["gsis_id"].to_dict()
    by_name = {(t, int(w), n): g for t, w, n, g in zip(r.team, r.week, r.full_name, r.gsis_id)}
    s["gsis_id"] = [by_pfr.get(pf) or by_name.get((t, int(w), n)) for pf, t, w, n in
                    zip(s.pfr_player_id, s.team, s.week, s.player)]
    return s


def wr_ranks(targets: pd.DataFrame, act: pd.DataFrame, games: pd.DataFrame) -> tuple[dict, dict]:
    """(game_id, team, gsis_id) -> 'WR1'|'WR2'|'WR3'|'WR_other'. Rank by prior-game targets for that team, then snaps.

    targets: rows with game_id, week, posteam, receiver_player_id, rpos (only WR rows used).
    act: active WR snap rows (game_id, team, gsis_id, offense_snaps).
    games: game_id, week, posteam (one row per offense-game).
    """
    wt = targets[targets["rpos"] == "WR"]
    tg = wt.groupby(["posteam", "week", "receiver_player_id"]).size().rename("t").reset_index()
    out, stats = {}, {"offense_games": 0, "unmapped_active_wr": 0, "week1_snap_ranked": 0}
    for gid, week, team in games[["game_id", "week", "posteam"]].itertuples(index=False):
        stats["offense_games"] += 1
        a = act[(act["game_id"] == gid) & (act["team"] == team)]
        stats["unmapped_active_wr"] += int(a["gsis_id"].isna().sum())
        snaps = {g: s for g, s in zip(a["gsis_id"], a["offense_snaps"]) if isinstance(g, str)}
        cand = set(snaps) | set(wt[(wt["game_id"] == gid) & (wt["posteam"] == team)]["receiver_player_id"])
        prior = tg[(tg["posteam"] == team) & (tg["week"] < week)].groupby("receiver_player_id")["t"].sum().to_dict()
        if not prior:
            stats["week1_snap_ranked"] += 1
        order = sorted(cand, key=lambda g: (-prior.get(g, 0), -snaps.get(g, 0), g))
        for i, g in enumerate(order):
            out[(gid, team, g)] = ["WR1", "WR2", "WR3"][i] if i < 3 else "WR_other"
    return out, stats


# ----------------------------------------------------------------------------------------------- team-game table
def team_game_table(plays: pd.DataFrame, rosters: pd.DataFrame, snaps: pd.DataFrame, ftn: pd.DataFrame | None):
    """One row per (game, defense, group). Allowed by the defense = produced by the offense in that game."""
    by_week, season = position_lookup(rosters)
    p = plays.copy()
    p["week"] = p["week"].astype(int)
    if ftn is not None and len(ftn):
        f = ftn[["nflverse_game_id", "nflverse_play_id", "is_screen_pass", "is_play_action", "n_blitzers"]].copy()
        f["nflverse_play_id"] = f["nflverse_play_id"].astype(float)
        p = p.merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"], how="left")
        p["ftn_charted"] = p["nflverse_play_id"].notna()
    else:
        p["is_screen_pass"] = np.nan
        p["is_play_action"] = np.nan
        p["n_blitzers"] = np.nan
        p["ftn_charted"] = False

    games = p[["game_id", "week", "posteam", "defteam"]].drop_duplicates().dropna()
    is_tgt = (p["play_type"] == "pass") & (p["sack"].fillna(0) == 0) & p["receiver_player_id"].notna()
    t = p[is_tgt].copy()
    t["rpos"] = [pos_of(r, w, by_week, season) for r, w in zip(t.receiver_player_id, t.week)]
    act = active_wrs(snaps, rosters)
    ranks, rank_stats = wr_ranks(t, act, games)
    t["group"] = [ranks.get((g, tm, r), "WR_other") if rp == "WR" else rp
                  for g, tm, r, rp in zip(t.game_id, t.posteam, t.receiver_player_id, t.rpos)]
    t["group"] = t["group"].where(t["group"].isin(GROUPS), "other")
    cmp_ = t["complete_pass"].fillna(0) == 1
    # receiver's own yards (box-score basis): lateral yards after the catch are not credited to the receiver
    yds = t["receiving_yards"].fillna(t["yards_gained"]).fillna(0).where(cmp_, 0.0)
    t["tgt"] = 1
    t["rec"] = cmp_.astype(int)
    t["yds"] = yds
    t["td"] = t["pass_touchdown"].fillna(0).astype(int)
    t["int"] = t["interception"].fillna(0).astype(int)
    t["explo20"] = (cmp_ & (yds >= 20)).astype(int)
    t["rz_tgt"] = (t["yardline_100"] <= 20).astype(int)
    d = t["air_yards"].map(depth_bucket)
    for b, name in (("short", "short"), ("inter", "inter"), ("deep", "deep")):
        t[f"{name}_tgt"] = (d == b).astype(int)
        t[f"{name}_rec"] = ((d == b) & cmp_).astype(int)
        t[f"{name}_yds"] = yds.where(d == b, 0.0)
    t["depth_unknown_tgt"] = (d == "unknown").astype(int)
    loc = t["pass_location"].map(loc_bucket)
    for b in ("middle", "outside"):
        t[f"{b}_tgt"] = (loc == b).astype(int)
        t[f"{b}_yds"] = yds.where(loc == b, 0.0)
    t["loc_unknown_tgt"] = (loc == "unknown").astype(int)
    rec = t.groupby(["game_id", "week", "posteam", "defteam", "group"])[REC_METRICS].sum().reset_index()

    # grid so a group with zero targets in a game is a 0 row, not missing
    grid = games.assign(_k=1).merge(pd.DataFrame({"group": GROUPS, "_k": 1}), on="_k").drop(columns="_k")
    tg = grid.merge(rec, on=["game_id", "week", "posteam", "defteam", "group"], how="left")
    tg[REC_METRICS] = tg[REC_METRICS].fillna(0)

    # RB rushing + RB screen / behind-LOS targets, attached to the RB row
    runs = p[(p["play_type"] == "run") & p["rusher_player_id"].notna()].copy()
    runs["rpos"] = [pos_of(r, w, by_week, season) for r, w in zip(runs.rusher_player_id, runs.week)]
    rb = runs[runs["rpos"] == "RB"].copy()
    rb["rb_rush_att"] = 1
    rb["rb_rush_yds"] = rb["rushing_yards"].fillna(rb["yards_gained"]).fillna(0)
    rb["rb_rush_td"] = rb["rush_touchdown"].fillna(0).astype(int)
    rb["rb_rush_explo10"] = (rb["rb_rush_yds"] >= 10).astype(int)
    rb["rb_rush_explo20"] = (rb["rb_rush_yds"] >= 20).astype(int)
    rb["rb_rush_succ"] = rb["success"].fillna(0).astype(int)
    rbs = rb.groupby(["game_id", "posteam"])[RUSH_METRICS[:6]].sum()
    rbt = t[t["group"] == "RB"].copy()
    scr = rbt["is_screen_pass"].fillna(0).astype(bool) if "is_screen_pass" in rbt else pd.Series(False, index=rbt.index)
    rbt["rb_screen_tgt"] = scr.astype(int)
    rbt["rb_screen_rec"] = (scr & (rbt["rec"] == 1)).astype(int)
    rbt["rb_screen_yds"] = rbt["yds"].where(scr, 0.0)
    blos = rbt["air_yards"].fillna(99) <= 0
    rbt["rb_behind_los_tgt"] = blos.astype(int)
    rbt["rb_behind_los_yds"] = rbt["yds"].where(blos, 0.0)
    rbr = rbt.groupby(["game_id", "posteam"])[RUSH_METRICS[6:]].sum()
    rbx = rbs.join(rbr, how="outer").fillna(0).reset_index()
    tg = tg.merge(rbx.assign(group="RB"), on=["game_id", "posteam", "group"], how="left")
    tg[RUSH_METRICS] = tg[RUSH_METRICS].fillna(0).where(tg["group"] == "RB", np.nan)

    # QB row
    db = p[p["qb_dropback"].fillna(0) == 1].copy()
    db["dropbacks"] = 1
    db["pass_att"] = ((db["pass_attempt"].fillna(0) == 1) & (db["sack"].fillna(0) == 0)).astype(int)
    db["cmp"] = db["complete_pass"].fillna(0).astype(int)
    db["pass_yds"] = db["passing_yards"].fillna(db["yards_gained"]).fillna(0).where(db["cmp"] == 1, 0.0)
    db["pass_td"] = db["pass_touchdown"].fillna(0).astype(int)
    db["pass_int"] = db["interception"].fillna(0).astype(int)
    db["sacks"] = db["sack"].fillna(0).astype(int)
    db["scrambles"] = db["qb_scramble"].fillna(0).astype(int)
    db["scramble_yds"] = db["rushing_yards"].fillna(db["yards_gained"]).fillna(0).where(db["scrambles"] == 1, 0.0)
    qbs = db.groupby(["game_id", "posteam"])[QB_METRICS[:9]].sum()
    qr = runs[(runs["rpos"] == "QB") & (runs["qb_scramble"].fillna(0) == 0)].copy()
    qr["qb_designed_runs"] = 1
    qr["qb_designed_yds"] = qr["rushing_yards"].fillna(qr["yards_gained"]).fillna(0)
    qbr = qr.groupby(["game_id", "posteam"])[QB_METRICS[9:]].sum()
    qbx = qbs.join(qbr, how="outer").fillna(0).reset_index()
    qrow = games.merge(qbx, on=["game_id", "posteam"], how="left").assign(group="QB")
    qrow[QB_METRICS] = qrow[QB_METRICS].fillna(0)
    tg = pd.concat([tg, qrow], ignore_index=True, sort=False)

    ftn_cov = p.groupby("game_id")["ftn_charted"].mean().rename("ftn_charted_share")
    tg = tg.merge(ftn_cov, on="game_id", how="left")
    tg = tg.sort_values(["defteam", "week", "group"]).reset_index(drop=True)
    return tg, p, rank_stats


# ----------------------------------------------------------------------------------------------- windows
def window_games(team_weeks: list[int], n: int | None) -> list[int]:
    w = sorted(set(team_weeks))
    return w if n is None else w[-n:]


def opp_adjusted(tg: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    """Leave-one-out: allowed minus the offense's mean for that group in its OTHER games in the table."""
    rows = []
    for (off, grp), g in tg.groupby(["posteam", "group"]):
        tot = g[metrics].sum()
        n = len(g)
        for idx, r in g.iterrows():
            if n < 2:
                base = pd.Series(np.nan, index=metrics)
            else:
                base = (tot - r[metrics]) / (n - 1)
            rows.append((idx, *(r[metrics] - base).tolist(), *base.tolist(), n - 1))
    cols = [f"{m}_oa" for m in metrics] + [f"{m}_offbase" for m in metrics] + ["offbase_games"]
    oa = pd.DataFrame([r[1:] for r in rows], index=[r[0] for r in rows], columns=cols)
    return tg.join(oa)


KEY_METRICS = {
    "WR1": ["tgt", "rec", "yds", "td", "explo20", "short_yds", "inter_yds", "deep_yds", "middle_yds", "outside_yds"],
    "WR2": ["tgt", "rec", "yds", "td", "explo20", "short_yds", "inter_yds", "deep_yds", "middle_yds", "outside_yds"],
    "WR3": ["tgt", "rec", "yds", "td", "explo20", "short_yds", "inter_yds", "deep_yds", "middle_yds", "outside_yds"],
    "WR_other": ["tgt", "rec", "yds", "td"],
    "TE": ["tgt", "rec", "yds", "td", "explo20", "rz_tgt", "short_yds", "inter_yds", "deep_yds"],
    "RB": ["tgt", "rec", "yds", "td", "rb_rush_att", "rb_rush_yds", "rb_rush_td", "rb_rush_explo10",
           "rb_rush_explo20", "rb_rush_succ", "rb_screen_tgt", "rb_screen_yds", "rb_behind_los_tgt", "rb_behind_los_yds"],
    "QB": QB_METRICS,
    "other": ["tgt", "rec", "yds"],
}


def windows_table(tg: pd.DataFrame) -> pd.DataFrame:
    out = []
    for grp, metrics in KEY_METRICS.items():
        g = tg[tg["group"] == grp]
        g = opp_adjusted(g, metrics)
        for team, gt in g.groupby("defteam"):
            for wname, n in WINDOWS.items():
                weeks = window_games(gt["week"].tolist(), n)
                gw = gt[gt["week"].isin(weeks)]
                row = {"defteam": team, "group": grp, "window": wname, "games": len(gw),
                       "weeks": " ".join(str(w) for w in sorted(weeks)), "partial_window": n is not None and len(gw) < n}
                for m in metrics:
                    row[f"{m}_pg"] = round(gw[m].mean(), 3)
                    row[f"{m}_oa_pg"] = round(gw[f"{m}_oa"].mean(), 3) if gw[f"{m}_oa"].notna().any() else np.nan
                    row[f"{m}_total"] = float(gw[m].sum())
                if "tgt" in metrics:
                    tt = gw["tgt"].sum()
                    row["catch_rate"] = round(gw["rec"].sum() / tt, 3) if tt else np.nan
                    row["yds_per_tgt"] = round(gw["yds"].sum() / tt, 2) if tt else np.nan
                    rr = gw["rec"].sum()
                    row["yds_per_rec"] = round(gw["yds"].sum() / rr, 2) if rr else np.nan
                if grp == "RB":
                    a = gw["rb_rush_att"].sum()
                    row["rb_ypc"] = round(gw["rb_rush_yds"].sum() / a, 2) if a else np.nan
                    row["rb_rush_succ_rate"] = round(gw["rb_rush_succ"].sum() / a, 3) if a else np.nan
                    row["rb_explo10_rate"] = round(gw["rb_rush_explo10"].sum() / a, 3) if a else np.nan
                if grp == "QB":
                    att = gw["pass_att"].sum()
                    row["cmp_pct"] = round(gw["cmp"].sum() / att, 3) if att else np.nan
                    row["sack_rate"] = round(gw["sacks"].sum() / gw["dropbacks"].sum(), 3) if gw["dropbacks"].sum() else np.nan
                out.append(row)
    w = pd.DataFrame(out)
    # league rank inside each group x window (1 = most allowed); opponent-adjusted rank too
    for c in [c for c in w.columns if c.endswith("_pg")]:
        w[c.replace("_pg", "_rank")] = w.groupby(["group", "window"])[c].rank(ascending=False, method="min")
    return w


def trend_table(w: pd.DataFrame, tg: pd.DataFrame) -> pd.DataFrame:
    """L3 and L5 minus season for the headline per-game metrics, with a rough z from game-level spread.

    Descriptive only. The L3 games are inside the season sample, so z overstates independence; |z| >= 2 is flagged
    as a possible shift, anything else as noise. Not validated.
    """
    head = {"WR1": "yds", "WR2": "yds", "WR3": "yds", "TE": "yds", "RB": "rb_rush_yds", "QB": "pass_yds"}
    rows = []
    for grp, m in head.items():
        for team in sorted(w["defteam"].unique()):
            g = tg[(tg["group"] == grp) & (tg["defteam"] == team)].sort_values("week")
            if g.empty:
                continue
            sd = g[m].std(ddof=1)
            season = g[m].mean()
            r = {"defteam": team, "group": grp, "metric": f"{m}_pg", "season": round(season, 1), "season_games": len(g)}
            for lab, n in (("L5", 5), ("L3", 3)):
                tail = g.tail(n)
                r[lab] = round(tail[m].mean(), 1)
                r[f"{lab}_minus_season"] = round(tail[m].mean() - season, 1)
                z = (tail[m].mean() - season) / (sd / math.sqrt(len(tail))) if sd and len(tail) else np.nan
                r[f"{lab}_z"] = round(z, 2) if z == z else np.nan
            z3 = r["L3_z"]
            r["L3_flag"] = ("UP" if z3 >= 2 else "DOWN" if z3 <= -2 else "noise") if z3 == z3 else "unknown"
            rows.append(r)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------- situational
def situational_table(p: pd.DataFrame) -> pd.DataFrame:
    """Defense performance by split and window: plays, pass rate faced, yards/play, EPA/play, success.

    These are results allowed in each situation. They are NOT coverage-call frequencies by situation (not in any free
    source we hold; see GAPS.md).
    """
    p = p.copy()
    p["is_pass"] = (p["qb_dropback"].fillna(0) == 1).astype(int)
    splits = {
        "all": pd.Series(True, index=p.index),
        "early_down": p["down"].isin([1, 2]),
        "third_down": p["down"] == 3,
        "third_long_7plus": (p["down"] == 3) & (p["ydstogo"] >= 7),
        "red_zone": p["yardline_100"] <= 20,
        "shotgun": p["shotgun"].fillna(0) == 1,
        "under_center": p["shotgun"].fillna(0) == 0,
        "ftn_play_action": p["is_play_action"] == True,  # noqa: E712  (NaN = not charted, excluded)
        "ftn_no_play_action_dropback": (p["is_play_action"] == False) & (p["is_pass"] == 1),  # noqa: E712
        "ftn_blitz_dropback": (p["n_blitzers"] > 0) & (p["is_pass"] == 1),
        "ftn_no_blitz_dropback": (p["n_blitzers"] == 0) & (p["is_pass"] == 1),
    }
    rows = []
    for team, gt in p.groupby("defteam"):
        weeks_all = sorted(gt["week"].unique())
        for wname, n in WINDOWS.items():
            weeks = weeks_all if n is None else weeks_all[-n:]
            gw = gt[gt["week"].isin(weeks)]
            for sname, mask in splits.items():
                s = gw[mask.loc[gw.index]]
                plays = len(s)
                row = {"defteam": team, "window": wname, "games": len(weeks), "split": sname, "plays": plays}
                if plays:
                    row.update(pass_rate_faced=round(s["is_pass"].mean(), 3),
                               yds_per_play=round(s["yards_gained"].fillna(0).mean(), 2),
                               epa_per_play=round(s["epa"].mean(), 3),
                               success_rate=round(s["success"].mean(), 3))
                    dbs = s[s["is_pass"] == 1]
                    row["epa_per_dropback"] = round(dbs["epa"].mean(), 3) if len(dbs) else np.nan
                    if sname.startswith("third"):
                        row["conv_rate"] = round((s["first_down"].fillna(0) == 1).mean(), 3) if "first_down" in s else np.nan
                rows.append(row)
    s = pd.DataFrame(rows)
    s["low_sample"] = s["plays"] < 30
    return s


# ----------------------------------------------------------------------------------------------- Sharp windows
def sharp_defense_windows(pkg: Path = SHARP_PKG) -> pd.DataFrame:
    """Per-defense windows from Sharp advanced box scores. The offense rows carry what it faced, so a defense's numbers
    come from its opponents' rows: man / cov, blitz / db, prsr / db, air / att (aDOT allowed), deep / att.
    Pooled ratios (sum over sum). Sharp weeks 1-10 only (source generated 2026-11-24 02:15 UTC)."""
    rows = [json.loads(l) for l in open(pkg / "team_games.jsonl")]
    df = pd.DataFrame([{"week": r["week"], "game_id": r["source_game_id"], "defteam": r["opponent"], "offense": r["team"],
                        **r["metrics"]} for r in rows])
    # Sharp writes the Rams as LAR; nflverse and the rest of the repo use LA
    df["defteam"] = df["defteam"].replace(SHARP_TEAM_FIX)
    df["offense"] = df["offense"].replace(SHARP_TEAM_FIX)
    ratio = {"man_rate": ("man", "cov"), "blitz_rate": ("blitz", "db"), "pressure_rate": ("prsr", "db"),
             "adot_allowed": ("air", "att"), "deep_tgt_rate_allowed": ("deep", "att"), "pa_rate_faced": ("pa", "db"),
             "epa_per_db_allowed": ("db_epa", "db"), "explosive_rate_allowed": ("explo", "plays")}
    out = []
    for team, g in df.groupby("defteam"):
        weeks_all = sorted(g["week"].unique())
        for wname, n in WINDOWS.items():
            weeks = weeks_all if n is None else weeks_all[-n:]
            gw = g[g["week"].isin(weeks)]
            r = {"defteam": team, "window": wname, "games": len(gw), "weeks": " ".join(map(str, weeks)),
                 "cov_snaps": int(gw["cov"].sum()), "dropbacks": int(gw["db"].sum())}
            for k, (a, b) in ratio.items():
                den = gw[b].sum()
                r[k] = round(gw[a].sum() / den, 3) if den else np.nan
            out.append(r)
    w = pd.DataFrame(out)
    s = w[w.window == "season"].set_index("defteam")
    for k in ("man_rate", "blitz_rate", "pressure_rate", "adot_allowed"):
        w[f"{k}_minus_season"] = (w[k] - w["defteam"].map(s[k])).round(3)
    w["source"] = "Sharp Football Analysis advanced box scores, weeks 1-10, generated 2026-11-24 02:15 UTC"
    return w


# ----------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--through-week", type=int, default=None)
    ap.add_argument("--out", type=Path, default=HERE)
    ap.add_argument("--allow-new-inputs", action="store_true")
    a = ap.parse_args(argv)
    shas = check_inputs(a.raw, a.allow_new_inputs)
    pbp = pd.read_parquet(a.raw / "play_by_play_2026.parquet")
    rosters = pd.read_parquet(a.raw / "roster_weekly_2026.parquet")
    snaps = pd.read_parquet(a.raw / "snap_counts_2026.parquet")
    ftn = pd.read_parquet(a.raw / "ftn_charting_2026.parquet")
    if a.through_week:
        pbp = pbp[pbp["week"] <= a.through_week]
        rosters = rosters[rosters["week"] <= a.through_week]
        snaps = snaps[snaps["week"] <= a.through_week]
        ftn = ftn[ftn["week"] <= a.through_week]
    plays = scrimmage(pbp)
    tg, p, rank_stats = team_game_table(plays, rosters, snaps, ftn)
    w = windows_table(tg)
    tr = trend_table(w, tg)
    sit = situational_table(p)
    sh = sharp_defense_windows()
    a.out.mkdir(parents=True, exist_ok=True)
    tg.to_csv(a.out / "team_game_allowed.csv", index=False)
    w.to_csv(a.out / "allowances_windows.csv", index=False)
    tr.to_csv(a.out / "allowance_trends.csv", index=False)
    sit.to_csv(a.out / "situational_allowed.csv", index=False)
    sh.to_csv(a.out / "sharp_defense_windows.csv", index=False)
    man = {
        "projection_ready": False, "research_only": True,
        "built_from": {k: {"sha256": v, "url": SOURCE_URLS[k], "pulled_utc": PULLED_UTC} for k, v in shas.items()},
        "sharp_package": {"path": "data_packages/sharp_advanced_2026_w1_10", "weeks": "1-10",
                          "source_generated_utc": "2026-11-24 02:15:25"},
        "through_week": a.through_week or int(plays["week"].max()),
        "games": int(plays["game_id"].nunique()),
        "last_game_date": str(plays["game_date"].max()),
        "ftn_last_week": int(ftn["week"].max()),
        "wr_rank_stats": rank_stats,
        "rows": {"team_game_allowed": len(tg), "allowances_windows": len(w), "allowance_trends": len(tr),
                 "situational_allowed": len(sit), "sharp_defense_windows": len(sh)},
    }
    (a.out / "MANIFEST.json").write_text(json.dumps(man, indent=1, default=int) + "\n")
    print(json.dumps(man["rows"]), json.dumps(rank_stats))


if __name__ == "__main__":
    main()
