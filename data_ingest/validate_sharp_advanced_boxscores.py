#!/usr/bin/env python3
"""Fail-closed completeness audit for the Sharp 2026 Weeks 1-10 package."""
import json
from collections import Counter, defaultdict
from pathlib import Path
import argparse

EXPECTED_GROUPS = {"box", "eff", "pass", "run"}

def audit(root):
    root = Path(root)
    package = root / "data_packages/sharp_advanced_2026_w1_10"
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    def read(name):
        return [json.loads(line) for line in (package / name).read_text(encoding="utf-8").splitlines() if line.strip()]
    team = read("team_games.jsonl")
    quarter = read("team_quarters.jsonl")
    catalog = manifest["metric_catalog"]
    errors = []
    if manifest["season"] != 2026 or manifest["weeks"] != list(range(1, 11)):
        errors.append("season/week scope mismatch")
    if len(team) != manifest["team_game_rows"] or len(quarter) != manifest["quarter_team_rows"]:
        errors.append("manifest row totals do not match JSONL")
    if len(catalog) != manifest["metric_count"] or len(catalog) != 43:
        errors.append("metric catalog count mismatch")
    groups = Counter(x["group"] for x in catalog)
    if set(groups) != EXPECTED_GROUPS:
        errors.append("expected four catalog groups box/eff/pass/run")
    team_keys = [(x["source_game_id"], x["team"]) for x in team]
    quarter_keys = [(x["source_game_id"], x["team"], x["quarter"]) for x in quarter]
    if len(set(team_keys)) != len(team):
        errors.append("duplicate team-game identity")
    if len(set(quarter_keys)) != len(quarter):
        errors.append("duplicate team-quarter identity")
    games = defaultdict(list)
    for row in team:
        games[row["source_game_id"]].append(row)
        if row["season"] != 2026 or row["week"] not in range(1, 11):
            errors.append("out-of-scope team-game row")
        if not row.get("metrics"):
            errors.append("empty team-game metrics")
    if len(games) != manifest["completed_games"]:
        errors.append("unique game count mismatch")
    for game_id, rows in games.items():
        if len(rows) != 2:
            errors.append("game does not have exactly two team rows: " + game_id)
        elif rows[0]["team"] != rows[1]["opponent"] or rows[1]["team"] != rows[0]["opponent"]:
            errors.append("team/opponent pair is not reciprocal: " + game_id)
    for row in quarter:
        if row["season"] != 2026 or row["week"] not in range(1, 11):
            errors.append("out-of-scope quarter row")
        if not row.get("metrics"):
            errors.append("empty quarter metrics")
        if row["quarter"] < 1:
            errors.append("invalid quarter/OT index")
    raw_fields = set()
    for row in team + quarter:
        raw_fields.update(row.get("metrics", {}).keys())
    for metric in catalog:
        if metric.get("num") not in raw_fields:
            errors.append("catalog numerator missing from raw payload: " + metric["key"])
        if metric.get("den") and metric["den"] not in raw_fields:
            errors.append("catalog denominator missing from raw payload: " + metric["key"])
    weeks_team = Counter(str(x["week"]) for x in team)
    weeks_quarter = Counter(str(x["week"]) for x in quarter)
    if dict(weeks_team) != manifest["team_game_rows_by_week"]:
        errors.append("team-game week distribution mismatch")
    if dict(weeks_quarter) != manifest["quarter_rows_by_week"]:
        errors.append("quarter week distribution mismatch")
    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "completed_games": len(games),
        "team_game_rows": len(team),
        "quarter_rows": len(quarter),
        "metric_catalog_rows": len(catalog),
        "total_database_records_expected": len(team) + len(quarter) + len(catalog),
        "catalog_groups": dict(groups),
        "distinct_raw_metric_fields": len(raw_fields),
        "duplicate_team_game_keys": len(team) - len(set(team_keys)),
        "duplicate_team_quarter_keys": len(quarter) - len(set(quarter_keys)),
        "team_game_rows_by_week": dict(weeks_team),
        "quarter_rows_by_week": dict(weeks_quarter),
    }
    if errors:
        raise ValueError(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = p.parse_args()
    print(json.dumps(audit(args.root), indent=2))
