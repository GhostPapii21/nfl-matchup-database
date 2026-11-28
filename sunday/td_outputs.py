"""Copy passing and rushing touchdown distributions off the script branch files.

The numbers are the branch artifacts' own means. They are not a 100k sim_v6
probability and they are not pooled across branches.
"""
from __future__ import annotations

import json
from pathlib import Path


def collect(script_dir: Path) -> dict:
    rows = []
    if script_dir.is_dir():
        for path in sorted(script_dir.glob("branches/**/*.json")):
            body = json.loads(path.read_text())
            players = body.get("players") or []
            for player in players:
                td = player.get("td_opportunity") or {}
                rows.append({
                    "path": str(path.relative_to(script_dir)),
                    "engine_id": body.get("engine_id"),
                    "branch": body.get("branch"),
                    "trials": body.get("n_trials"),
                    "team": player.get("team"),
                    "player": player.get("player"),
                    "pass_td_mean": (td.get("pass_td") or {}).get("mean"),
                    "rush_td_mean": (td.get("rush_td") or {}).get("mean"),
                    "acceptance_100k": False,
                })
    return {
        "schema": "sunday-td-outputs/1",
        "projection_ready": False,
        "certification": False,
        "pooled": False,
        "rows": rows,
        "players_with_pass_td": sum(1 for row in rows if row["pass_td_mean"] is not None),
        "players_with_rush_td": sum(1 for row in rows if row["rush_td_mean"] is not None),
        "note": "Means come from the script branch file. A 24-trial possession run is not the 100k gate.",
    }
