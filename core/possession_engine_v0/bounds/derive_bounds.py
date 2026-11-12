"""NFL-43 review D1/D3/D4/D5: reproduce every descriptive figure in SEMANTICS_BOUNDS.md section 3 from files in the repo.

    python3 core/possession_engine_v0/bounds/derive_bounds.py            # writes bounds/bounds_figures.json
    python3 core/possession_engine_v0/bounds/derive_bounds.py --check    # exit 1 if the committed JSON differs

Every figure carries its source file, the file's sha256 and the source's pull time. Weeks with no data are reported
as "unknown", never as zero. No network, no API credits, no model run. Research only, not validated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from semantics import KICK_PLAY_TYPES, PENALTY_LOG_PULLED_ET, penalty_log_unknowns  # noqa: E402

PEN_LOG = REPO / "data/redistributable/teams/penalty_plays_2026.csv"
PEN_GAMES = REPO / "data/redistributable/teams/penalties_2026.csv"
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PBP_PROV = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.provenance.json"
OUT = HERE / "bounds_figures.json"
LABEL = "research only, not validated"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _truthy(s):
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def derive() -> dict:
    pbp_pull = json.loads(PBP_PROV.read_text())["pulled_et"]
    pen_src = {"files": [str(PEN_LOG.relative_to(REPO)), str(PEN_GAMES.relative_to(REPO))],
               "sha256": {PEN_LOG.name: sha(PEN_LOG), PEN_GAMES.name: sha(PEN_GAMES)},
               "pulled_et": PENALTY_LOG_PULLED_ET}
    pbp_src = {"files": [str(PBP.relative_to(REPO))], "sha256": {PBP.name: sha(PBP)}, "pulled_et": pbp_pull}

    log = pd.read_csv(PEN_LOG)
    games = pd.read_csv(PEN_GAMES)
    log = log[log["season"] == 2026]
    pen_weeks = sorted(int(w) for w in log["week"].unique())
    n_games = int(games["game_id"].nunique())
    n_tg = int(len(games))
    acc = log[log["status"] == "accepted"].copy()
    acc["yards"] = acc["yards"].fillna(0).astype(int)
    kick = acc["play_type"].isin(KICK_PLAY_TYPES)
    scr = acc[~kick]
    tg_yds = games[["game_id", "team"]].merge(
        acc.groupby(["game_id", "team_penalized"])["yards"].sum().rename("y").reset_index()
        .rename(columns={"team_penalized": "team"}), on=["game_id", "team"], how="left")["y"].fillna(0)
    pen = {
        "weeks_with_data": pen_weeks,
        "games": n_games, "team_games": n_tg,
        "accepted_flags": int(len(acc)), "accepted_yards": int(acc["yards"].sum()),
        "accepted_flags_per_team_game": round(len(acc) / n_tg, 2),
        "accepted_yards_per_team_game": round(acc["yards"].sum() / n_tg, 1),
        "team_game_yards_p10_p50_p90": [int(np.percentile(tg_yds, q)) for q in (10, 50, 90)],
        "share_no_play": round(float(_truthy(acc["no_play"]).mean()), 3),
        "share_auto_first_down": round(float(_truthy(acc["auto_first_down"]).mean()), 3),
        "flags_drive_extended": int(_truthy(acc["drive_extended"]).sum()),
        "flags_drive_killer": int(_truthy(acc["drive_killer"]).sum()),
        "kick_play_flags": int(kick.sum()), "kick_play_yards": int(acc.loc[kick, "yards"].sum()),
        "kick_play_flag_share": round(float(kick.mean()), 3),
        "kick_play_yard_share": round(float(acc.loc[kick, "yards"].sum() / acc["yards"].sum()), 3),
        "scrimmage_flags": int(len(scr)), "scrimmage_yards": int(scr["yards"].sum()),
        "scrimmage_flags_per_team_game": round(len(scr) / n_tg, 2),
        "scrimmage_yards_per_team_game": round(scr["yards"].sum() / n_tg, 1),
        "declined_or_offsetting_rows": int(log["status"].isin(["declined", "offsetting"]).sum()),
        # Like-for-like comparator for the WAS@NYG sim (review D5): scrimmage-only accepted fouls BY each team, per
        # team-game, from the same two teams' W1-8 games. The sim draws from exactly these teams' rates.
        "scrimmage_by_team_per_team_game": {
            t: {"team_games": int((games["team"] == t).sum()),
                "flags": int((scr["team_penalized"] == t).sum()),
                "yards": int(scr.loc[scr["team_penalized"] == t, "yards"].sum()),
                "flags_per_team_game": round(float((scr["team_penalized"] == t).sum() / max(1, (games["team"] == t).sum())), 2),
                "yards_per_team_game": round(float(scr.loc[scr["team_penalized"] == t, "yards"].sum() / max(1, (games["team"] == t).sum())), 1)}
            for t in ("NYG", "WSH")},
        "boxscore_match_team_games": "228 of 238 (PENALTY_NOTES.md; not re-derived here)",
    }

    d = pd.read_parquet(PBP)
    d = d[d["season"] == 2026]
    pbp_weeks = sorted(int(w) for w in d["week"].unique())
    g = d.groupby("game_id")
    n_pbp_games = int(d["game_id"].nunique())
    ko, pu = d[d["kickoff_attempt"] == 1], d[d["punt_attempt"] == 1]
    ints, fl = d[d["interception"] == 1], d[d["fumble_lost"] == 1]
    ot_games = int((g["qtr"].max() >= 5).sum())
    pbp = {
        "weeks_with_data": pbp_weeks, "games": n_pbp_games, "rows": int(len(d)),
        "rows_with_penalty": int((d["penalty"] == 1).sum()),
        "share_rows_with_penalty": round(float((d["penalty"] == 1).mean()), 3),
        "kickoffs": int(len(ko)), "kick_return_tds": int(ko["return_touchdown"].fillna(0).sum()),
        "punts": int(len(pu)), "punt_return_tds": int(pu["return_touchdown"].fillna(0).sum()),
        "mean_kick_return_yards": round(float(ko["return_yards"].mean()), 1),
        "mean_punt_return_yards": round(float(pu["return_yards"].mean()), 1),
        "interceptions": int(len(ints)), "interception_return_tds": int(ints["return_touchdown"].fillna(0).sum()),
        "fumbles_lost": int(len(fl)), "fumble_return_tds": int(fl["return_touchdown"].fillna(0).sum()),
        "mean_interception_return_yards": round(float(ints["return_yards"].mean()), 1),
        "mean_fumble_lost_return_yards": round(float(fl["return_yards"].mean()), 1),
        "ot_games": ot_games, "ot_game_rate": round(ot_games / n_pbp_games, 3),
    }
    # R1: W9 is an unknown week; two W8 games are also missing from PEN (not a complete W1-8 log).
    asof = (max(pbp_weeks) + 1) if pbp_weeks else 10
    cov = penalty_log_unknowns(games, season=2026, week_asof_exclusive=asof, pbp_df=d)
    # attach per-team unknown-game labels onto the NYG/WAS (WSH) comparators
    by_team = cov["unknown_games_by_team"]
    for t, row in pen["scrimmage_by_team_per_team_game"].items():
        nfl = "WAS" if t == "WSH" else t
        row["unknown_games"] = by_team.get(nfl, [])
        row["unknown_games_policy"] = "UNKNOWN, not zero" if row["unknown_games"] else None
    unknown = {
        "penalty_log_weeks_unknown": cov["unknown_weeks"],
        "penalty_log_games_unknown": cov["unknown_games"],
        "penalty_log_games_unknown_by_team": cov["unknown_games_by_team"],
        "pbp_games_in_pen_weeks": cov["pbp_games_in_pen_weeks"],
        "pen_games_in_log": n_games,
        "policy": cov["policy"],
        "note": ("The canonical penalty log is not a complete W1-8 file: it has "
                 f"{n_games} of {cov['pbp_games_in_pen_weeks']} PBP games in weeks {pen_weeks}. "
                 "Unknown (not zero): " + ", ".join(cov["unknown_games"] or ["(none)"])
                 + ("; weeks " + ", ".join(str(w) for w in cov["unknown_weeks"]) if cov["unknown_weeks"] else "")
                 + ". PENALTY_NOTES.md: Week 8 SNF/MNF were not final when PEN was pulled (2026-11-01 ~9 PM ET). "
                 "Sims use rates from games that exist in PEN only."),
    }
    return {"label": LABEL, "generated_by": "core/possession_engine_v0/bounds/derive_bounds.py",
            "penalty_log": {"source": pen_src, "figures": pen},
            "pbp": {"source": pbp_src, "figures": pbp},
            "unknown": unknown}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if bounds_figures.json is stale")
    a = ap.parse_args(argv)
    out = derive()
    text = json.dumps(out, indent=1, sort_keys=False) + "\n"
    if a.check:
        if not OUT.exists() or OUT.read_text() != text:
            print("bounds_figures.json is stale or missing; rerun derive_bounds.py")
            return 1
        print("bounds_figures.json matches the source files")
        return 0
    OUT.write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
