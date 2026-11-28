#!/usr/bin/env python3
"""Reproduces the measurements quoted in docs/audits/nfl_source_coverage_matrix.md.

Read-only. Free public downloads only (nflverse-data GitHub releases). No keys, no paid APIs, no repo writes
except the cache folder you name.

    python3 docs/audits/nfl_source_coverage_verify.py --cache /tmp/nfl_audit_cache > verify_output.md

Needs pandas + pyarrow. About 300 MB of downloads on first run. Every number in the matrix that says "verified"
and is not a web-page/API probe comes from this script. Probes of ESPN, Action Network, Open-Meteo, NWS, NOAA,
Meteostat, NFL.com, Sharp and ESPN win-rate pages are listed in the matrix's methodology section and are one-off
curl requests (not scripted here, so they are not re-run by this file).
"""
from __future__ import annotations

import argparse
import re
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download"
UA = {"User-Agent": "nfl-source-audit/1.0 (research; public data)"}


def fetch(cache: Path, rel: str) -> Path:
    dest = cache / Path(rel).name
    if not dest.exists() or dest.stat().st_size < 1000:
        req = urllib.request.Request(f"{NFLVERSE}/{rel}", headers=UA)
        with urllib.request.urlopen(req, timeout=300) as r:
            dest.write_bytes(r.read())
    return dest


def rd(cache: Path, rel: str, **kw) -> pd.DataFrame:
    return pd.read_parquet(fetch(cache, rel), **kw)


def md(df: pd.DataFrame, title: str, note: str = "") -> None:
    print(f"\n### {title}\n")
    if note:
        print(note + "\n")
    print(df.to_markdown(index=False) if hasattr(df, "to_markdown") else df.to_string(index=False))


def nn(s: pd.Series) -> float:
    """Non-null share, treating '' as null."""
    return float((s.notna() & (s.astype(str) != "")).mean())


def participation(cache: Path) -> None:
    rows, qb_rows = [], []
    for y in range(2016, 2026):
        pbp = rd(cache, f"pbp/play_by_play_{y}.parquet",
                 columns=["game_id", "play_id", "season_type", "qb_dropback", "sack", "qb_hit", "pass_attempt",
                          "receiver_player_id", "qb_scramble", "passer_player_id", "epa"])
        pt = rd(cache, f"pbp_participation/pbp_participation_{y}.parquet")
        m = pbp.merge(pt.drop(columns=["possession_team"]), left_on=["game_id", "play_id"],
                      right_on=["nflverse_game_id", "play_id"], how="left", indicator=True)
        reg = m[m.season_type == "REG"]
        db = reg[reg.qb_dropback == 1].copy()
        db["wp"] = db.was_pressure.map({True: 1.0, False: 0.0, "True": 1.0, "False": 0.0})
        known = db.defense_man_zone_type.isin(["MAN_COVERAGE", "ZONE_COVERAGE"])
        pa = db[(db.pass_attempt == 1) & (db.sack == 0)]
        rows.append({
            "season": y, "pbp_plays": len(pbp), "participation_rows": len(pt),
            "dropbacks": len(db), "route": round(nn(db.route), 3), "man_zone": round(nn(db.defense_man_zone_type), 3),
            "coverage_type": round(nn(db.defense_coverage_type), 3), "was_pressure": round(nn(db.was_pressure), 3),
            "time_to_throw": round(nn(db.time_to_throw), 3), "pass_rushers": round(nn(db.number_of_pass_rushers), 3),
            "man_share": round((db.defense_man_zone_type == "MAN_COVERAGE").sum() / max(known.sum(), 1), 3),
            "pressure_rate": round(db.wp.mean(), 3),
            "P(pressure|sack)": round(db[db.sack == 1].wp.mean(), 3) if db[db.sack == 1].wp.notna().any() else None,
            "route_on_sack": round(nn(db[db.sack == 1].route), 3),
            "route_on_attempt_w_receiver": round(nn(pa[pa.receiver_player_id.notna()].route), 3),
        })
    md(pd.DataFrame(rows), "nflverse pbp_participation joined to pbp (regular season dropbacks)",
       "Non-null share counts '' as null. `route` is documented as the route of the PRIMARY receiver only.")


def ftn(cache: Path) -> None:
    rows = []
    for y in range(2022, 2027):
        f = rd(cache, f"ftn_charting/ftn_charting_{y}.parquet")
        pbp = rd(cache, f"pbp/play_by_play_{y}.parquet", columns=["game_id", "play_id", "qb_dropback", "season_type"])
        m = pbp.merge(f, left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"], how="left", indicator=True)
        db = m[(m.qb_dropback == 1) & (m.season_type == "REG")]
        hit = db[db._merge == "both"]
        rows.append({"season": y, "ftn_rows": len(f), "weeks": f"{f.week.min()}-{f.week.max()}", "dropbacks": len(db),
                     "matched": round((db._merge == "both").mean(), 3),
                     "blitz_share(n_blitzers>0)": round((hit.n_blitzers > 0).mean(), 3),
                     "play_action_share": round(hit.is_play_action.astype(float).mean(), 3),
                     "columns_with_route_or_coverage_or_pressure": ", ".join(c for c in f.columns if re.search("route|cover|press", c)) or "none"})
    md(pd.DataFrame(rows), "nflverse ftn_charting")


def cross_pressure(cache: Path, y: int = 2025) -> None:
    pbp = rd(cache, f"pbp/play_by_play_{y}.parquet", columns=["game_id", "play_id", "posteam", "defteam", "season_type", "qb_dropback", "sack", "qb_hit"])
    pt = rd(cache, f"pbp_participation/pbp_participation_{y}.parquet")
    f = rd(cache, f"ftn_charting/ftn_charting_{y}.parquet")
    m = (pbp.merge(pt[["nflverse_game_id", "play_id", "was_pressure"]], left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"])
         .merge(f[["nflverse_game_id", "nflverse_play_id", "n_blitzers"]], left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"]))
    m = m[(m.season_type == "REG") & (m.qb_dropback == 1)]
    m["wp"] = m.was_pressure.map({True: 1, False: 0, "True": 1, "False": 0})
    m["blitz"] = (m.n_blitzers > 0).astype(int)
    tg = m.groupby(["game_id", "posteam"]).agg(part_pressure=("wp", "sum"), ftn_blitz=("blitz", "sum"), sacks=("sack", "sum"), qb_hit=("qb_hit", "sum")).reset_index()
    pf = rd(cache, f"pfr_advstats/advstats_week_pass_{y}.parquet")
    pf = pf[pf.game_type == "REG"].groupby(["game_id", "team"]).agg(pfr_pressured=("times_pressured", "sum"), pfr_blitzed=("times_blitzed", "sum"),
                                                                    pfr_sacked=("times_sacked", "sum"), pfr_hit=("times_hit", "sum")).reset_index()
    j = tg.merge(pf, left_on=["game_id", "posteam"], right_on=["game_id", "team"])
    out = []
    for a, b in [("part_pressure", "pfr_pressured"), ("ftn_blitz", "pfr_blitzed"), ("sacks", "pfr_sacked"), ("qb_hit", "pfr_hit")]:
        out.append({"nflverse/FTN field": a, "PFR field": b, "team_games": len(j), "sum_a": int(j[a].sum()), "sum_PFR": int(j[b].sum()),
                    "corr": round(float(np.corrcoef(j[a], j[b])[0, 1]), 3), "exact_match_share": round(float((j[a] == j[b]).mean()), 3)})
    md(pd.DataFrame(out), f"Cross-source pressure / blitz agreement, {y} regular season (team-game level)")
    d = rd(cache, f"pfr_advstats/advstats_week_def_{y}.parquet")
    d = d[d.game_type == "REG"].groupby(["game_id", "team"]).agg(def_targets=("def_targets", "sum")).reset_index()
    a = pbp[(pbp.season_type == "REG")].merge(rd(cache, f"pbp/play_by_play_{y}.parquet", columns=["game_id", "play_id", "pass_attempt"]), on=["game_id", "play_id"])
    a = a[(a.pass_attempt == 1) & (a.sack == 0)].groupby(["game_id", "defteam"]).size().rename("pbp_attempts").reset_index()
    k = d.merge(a, left_on=["game_id", "team"], right_on=["game_id", "defteam"])
    print(f"\nPFR def_targets / pbp pass attempts, {y}: {len(k)} team-games, total ratio {k.def_targets.sum() / k.pbp_attempts.sum():.3f}\n")


def pbp_fields(cache: Path) -> None:
    rows = []
    for y in range(2016, 2027):
        p = rd(cache, f"pbp/play_by_play_{y}.parquet", columns=["season_type", "pass_attempt", "sack", "qb_spike", "rush_attempt", "qb_kneel", "qb_scramble",
                                                               "air_yards", "pass_length", "pass_location", "run_location", "run_gap", "receiver_player_id", "down", "ydstogo", "yardline_100", "posteam", "play_type"])
        r = p[p.season_type == "REG"]
        pa = r[(r.pass_attempt == 1) & (r.sack == 0) & (r.qb_spike != 1)]
        ru = r[(r.rush_attempt == 1) & (r.qb_kneel != 1) & (r.qb_scramble != 1)]
        rows.append({"season": y, "pass_att": len(pa), "air_yards": round(pa.air_yards.notna().mean(), 3), "pass_location": round(pa.pass_location.notna().mean(), 3),
                     "receiver_id": round(pa.receiver_player_id.notna().mean(), 3), "rush_att": len(ru), "run_location": round(ru.run_location.notna().mean(), 3),
                     "run_gap": round(ru.run_gap.notna().mean(), 3),
                     "run_gap_blank_when_middle": round(ru[ru.run_location == "middle"].run_gap.isna().mean(), 3),
                     "run_gap_blank_when_left_right": round(ru[ru.run_location.isin(["left", "right"])].run_gap.isna().mean(), 3)})
    md(pd.DataFrame(rows), "nflverse pbp: depth / direction / gap fields (regular season)")


def ngs_pfr(cache: Path) -> None:
    pbp = rd(cache, "pbp/play_by_play_2025.parquet", columns=["season_type", "week", "receiver_player_id", "pass_attempt", "rusher_player_id", "rush_attempt"])
    pbp = pbp[pbp.season_type == "REG"]
    out = []
    nr = rd(cache, "nextgen_stats/ngs_receiving.parquet"); nr = nr[(nr.season == 2025) & (nr.week > 0) & (nr.season_type == "REG")]
    t = pbp[(pbp.pass_attempt == 1) & pbp.receiver_player_id.notna()].groupby(["week", "receiver_player_id"]).size().rename("n").reset_index()
    m = t.merge(nr[["week", "player_gsis_id"]], left_on=["week", "receiver_player_id"], right_on=["week", "player_gsis_id"], how="left")
    out.append({"table": "ngs_receiving 2025", "player_weeks": len(t), "share_of_player_weeks_present": round(m.player_gsis_id.notna().mean(), 3),
                "share_of_volume_present": round(float((m.n * m.player_gsis_id.notna()).sum() / m.n.sum()), 3), "min_volume_in_ngs_rows": int(nr.targets.min())})
    nu = rd(cache, "nextgen_stats/ngs_rushing.parquet"); nu = nu[(nu.season == 2025) & (nu.week > 0) & (nu.season_type == "REG")]
    r = pbp[(pbp.rush_attempt == 1) & pbp.rusher_player_id.notna()].groupby(["week", "rusher_player_id"]).size().rename("n").reset_index()
    m = r.merge(nu[["week", "player_gsis_id"]], left_on=["week", "rusher_player_id"], right_on=["week", "player_gsis_id"], how="left")
    out.append({"table": "ngs_rushing 2025", "player_weeks": len(r), "share_of_player_weeks_present": round(m.player_gsis_id.notna().mean(), 3),
                "share_of_volume_present": round(float((m.n * m.player_gsis_id.notna()).sum() / m.n.sum()), 3), "min_volume_in_ngs_rows": int(nu.rush_attempts.min())})
    md(pd.DataFrame(out), "NGS qualifier coverage (nflverse nextgen_stats weekly rows vs pbp volume)")
    for k in ["pass", "rec", "rush", "def"]:
        d = rd(cache, f"pfr_advstats/advstats_week_{k}_2025.parquet")
        print(f"\nPFR advstats week_{k} 2025 columns: {', '.join(d.columns)}")


def injuries_games(cache: Path) -> None:
    rows = []
    for y in range(2016, 2027):
        d = rd(cache, f"injuries/injuries_{y}.parquet")
        rows.append({"season": y, "rows": len(d), "weeks": f"{d.week.min()}-{d.week.max()}", "has_date_modified_column": "date_modified" in d.columns,
                     "report_status_nonnull": round(d.report_status.notna().mean(), 3), "practice_status_nonnull": round(d.practice_status.notna().mean(), 3)})
    md(pd.DataFrame(rows), "nflverse injuries")
    g = rd(cache, "schedules/games.parquet")
    rows = []
    rx_t = re.compile(r"Temp:\s*(-?\d+)")
    for y in range(2016, 2027):
        x = g[(g.season == y) & (g.game_type == "REG") & g.result.notna()]
        out = x[x.roof.isin(["outdoors", "open"])]
        p = rd(cache, f"pbp/play_by_play_{y}.parquet", columns=["game_id", "season_type", "weather"])
        w = p[p.season_type == "REG"].groupby("game_id").weather.first()
        pt = w.reindex(out.game_id).fillna("").str.extract(rx_t)[0].astype(float).values
        rows.append({"season": y, "finished_games": len(x), "spread_line": round(x.spread_line.notna().mean(), 3), "total_line": round(x.total_line.notna().mean(), 3),
                     "home_moneyline": round(x.home_moneyline.notna().mean(), 3), "outdoor_games": len(out),
                     "games.temp_nonnull_outdoor": round(out.temp.notna().mean(), 3),
                     "pbp.weather_text_temp_parsed_outdoor": round(float(np.mean(~np.isnan(pt))), 3) if len(out) else None})
    md(pd.DataFrame(rows), "nflverse games.csv: lines and weather (finished regular-season games)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True, help="folder for downloaded nflverse files")
    a = ap.parse_args()
    cache = Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
    print("# nfl_source_coverage_verify output\n")
    for fn in (participation, ftn, cross_pressure, pbp_fields, ngs_pfr, injuries_games):
        fn(cache)


if __name__ == "__main__":
    main()
