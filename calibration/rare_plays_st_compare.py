"""NFL-75: special-teams scoring / event frequencies, simulated vs actual, weeks 4-9 backtest games.

    python3 -m calibration.rare_plays_st_compare --per-game calibration/outputs/backtest_rare_plays_n2000_per_game.csv

Actual counts come from the committed nflverse W1-9 PBP (pulled 2026-11-12 11:16 AM ET) with the same class
definitions as core/possession_engine_v0/rare_plays.py. Sim counts are the per-game means the backtest records
(st_* columns, simulate.special_teams_counts). Diagnostic only; nothing is fitted. Research only, not validated.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

import numpy as np
import pandas as pd

from calibration.common import PBP, PBP_PULLED_ET, ROOT, engine_path, sha256

KEYS = ("fg_made", "pat_good", "pat_blocked", "def_two_point", "kick_return_td", "punt_return_td", "safety",
        "punt_blocked", "fg_blocked", "blocked_kick_td", "fake", "fake_kicking_td", "fake_def_td", "kick_foul_presnap",
        "kick_foul_flagged", "flagged_kick_return_td", "onside_attempt", "onside_recovered", "punt_plays", "fg_plays")
ST_POINTS = {"fg_made": 3, "pat_good": 1, "def_two_point": 2, "kick_return_td": 6, "punt_return_td": 6,
             "blocked_kick_td": 6, "fake_kicking_td": 6, "fake_def_td": 6, "flagged_kick_return_td": 6}


def actual_counts(game_ids) -> pd.DataFrame:
    engine_path()
    import rare_plays as rp
    cols = list(dict.fromkeys(rp._COLS + ["safety"]))
    import pyarrow.parquet as pq
    have = set(pq.ParquetFile(PBP).schema_arrow.names)
    d = pd.read_parquet(PBP, columns=[c for c in cols if c in have])
    d = d[d["game_id"].isin(set(game_ids))].sort_values(["game_id", "play_id"]).reset_index(drop=True)
    d = rp.classify(d)
    n = lambda s: pd.to_numeric(s, errors="coerce").fillna(0)
    recv6 = (n(d["defteam_score_post"]) - n(d["defteam_score"])) == 6
    kick6 = (n(d["posteam_score_post"]) - n(d["posteam_score"])) == 6
    ko = n(d["kickoff_attempt"]) == 1
    out = pd.DataFrame(index=sorted(set(game_ids)))
    def add(name, mask):
        out[name] = d[mask].groupby("game_id").size().reindex(out.index).fillna(0).astype(int)
    add("fg_made", d["field_goal_result"] == "made")
    add("pat_good", d["extra_point_result"] == "good")
    add("pat_blocked", d["extra_point_result"] == "blocked")
    add("def_two_point", n(d["defensive_extra_point_conv"]) == 1)
    add("kick_return_td", ko & (n(d["return_touchdown"]) == 1))
    add("punt_return_td", (d["_cls"] == "clean") & (d["_form"] == "punt") & (n(d["return_touchdown"]) == 1))
    add("safety", n(d["safety"]) == 1)
    add("punt_blocked", (d["_cls"] == "blocked") & (d["_form"] == "punt"))
    add("fg_blocked", (d["_cls"] == "blocked") & (d["_form"] == "field_goal"))
    add("blocked_kick_td", (d["_cls"] == "blocked") & recv6)
    add("fake", d["_cls"] == "fake")
    add("fake_kicking_td", (d["_cls"] == "fake") & kick6)
    add("fake_def_td", (d["_cls"] == "fake") & recv6)
    add("kick_foul_presnap", d["_cls"] == "presnap")
    add("kick_foul_flagged", d["_cls"] == "flagged")
    add("flagged_kick_return_td", (d["_cls"] == "flagged") & recv6)
    add("onside_attempt", d["_onside"])
    add("onside_recovered", d["_onside"] & (n(d["own_kickoff_recovery"]) == 1))
    add("punt_plays", (d["_form"] == "punt") & d["_cls"].isin(["clean", "fake", "blocked", "flagged"]))
    add("fg_plays", (d["_form"] == "field_goal") & d["_cls"].isin(["clean", "fake", "blocked", "flagged"]))
    return out


def compare(per_game_paths: list[str]) -> dict:
    frames = [pd.read_csv(p) for p in per_game_paths]
    per = pd.concat(frames, ignore_index=True)
    games = sorted(per["game_id"].unique())
    act = actual_counts(games)
    res = {"games": len(games), "actual": {}, "arms": {}}
    res["actual"] = {k: float(act[k].mean()) for k in KEYS}
    res["actual"]["st_points"] = float(sum(act[k].mean() * v for k, v in ST_POINTS.items()))
    for arm, g in per.groupby("arm"):
        r = {}
        for k in KEYS:
            c = f"st_{k}"
            r[k] = float(g[c].mean()) if c in g.columns else None
        r["st_points"] = float(sum((r[k] or 0) * v for k, v in ST_POINTS.items()))
        res["arms"][arm] = r
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-game", nargs="+", required=True)
    ap.add_argument("--out", default=str(ROOT / "calibration/outputs/rare_plays_st_compare.json"))
    a = ap.parse_args(argv)
    res = compare(a.per_game)
    res.update({"label": "research only, not validated; diagnostic, nothing fitted",
                "pbp": {"path": str(PBP.relative_to(ROOT)), "sha256": sha256(PBP), "pulled_et": PBP_PULLED_ET},
                "per_game_inputs": a.per_game, "st_points_weights": ST_POINTS,
                "note": "per-game means, both teams; sim = mean of n sims per game, actual = the real game"})
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
