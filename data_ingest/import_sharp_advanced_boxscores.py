#!/usr/bin/env python3
"""Idempotently import authorized Sharp NFL advanced box-score records.

Default is a read-only dry run. Pass --apply to write to the private source SQLite DB.
The public snapshot is published separately through export_snapshot.py.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sqlite3
from pathlib import Path

SOURCE_PAGE = "https://www.sharpfootballanalysis.com/analysis/nfl-advanced-box-scores/"
DATASETS = {
    "team": "sharp_advanced_boxscore_team_game",
    "quarter": "sharp_advanced_boxscore_quarter",
    "catalog": "sharp_advanced_boxscore_metric_catalog",
}

def load_jsonl(path):
    with Path(path).open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def _team_tokens(payload):
    text = json.dumps(payload, sort_keys=True).upper()
    return text

def map_game_id(db, row):
    """Map Sharp source key to an existing game only when date + both teams are unique."""
    candidates = db.execute("SELECT game_id,data FROM games WHERE date=?", (row["date"],)).fetchall()
    hits = []
    for game_id, raw in candidates:
        try:
            payload = json.loads(raw) if isinstance(raw, str) else raw
        except (TypeError, json.JSONDecodeError):
            payload = raw or ""
        haystack = _team_tokens(payload)
        a = re.search(r"(?<![A-Z0-9])" + re.escape(row["team"]) + r"(?![A-Z0-9])", haystack)
        b = re.search(r"(?<![A-Z0-9])" + re.escape(row["opponent"]) + r"(?![A-Z0-9])", haystack)
        if a and b:
            hits.append(game_id)
    return hits[0] if len(hits) == 1 else None

def record_id(dataset, row):
    key = "|".join(str(row.get(k, "")) for k in
                   ("source_game_id", "season", "week", "team", "quarter"))
    return hashlib.sha256((dataset + "|" + key).encode()).hexdigest()

def prepare_rows(db, data_dir):
    out = []
    retrieved = dt.datetime.now(dt.timezone.utc).isoformat()
    for kind, filename in (("team", "team_games.jsonl"), ("quarter", "team_quarters.jsonl")):
        dataset = DATASETS[kind]
        for row in load_jsonl(Path(data_dir) / filename):
            gid = map_game_id(db, row)
            payload = dict(row)
            payload["linked_game_id"] = gid
            payload["game_link_status"] = "matched" if gid else "unmatched_or_ambiguous"
            payload["source_page"] = SOURCE_PAGE
            payload["metric_values_are_publisher_supplied"] = True
            out.append((record_id(dataset, row), dataset, gid, row["team"], row["week"],
                        SOURCE_PAGE, retrieved, row.get("source_generated_utc"),
                        json.dumps(payload, separators=(",", ":"), sort_keys=True)))
    # Store the publisher's metric dictionary in the database too, so consumers
    # can interpret raw numerator/denominator fields without reading a repo file.
    manifest = json.loads((Path(data_dir) / "manifest.json").read_text(encoding="utf-8"))
    dataset = DATASETS["catalog"]
    for definition in manifest["metric_catalog"]:
        key = definition["key"]
        rid = hashlib.sha256((dataset + "|" + key).encode()).hexdigest()
        payload = {
            "source": "Sharp Football Analysis",
            "source_page": SOURCE_PAGE,
            "metric_key": key,
            "group": definition["group"],
            "label": definition["label"],
            "kind": definition["kind"],
            "numerator": definition.get("num"),
            "denominator": definition.get("den"),
            "higher_is_better": definition.get("hi_good"),
            "definition": definition,
        }
        out.append((rid, dataset, None, None, None, SOURCE_PAGE, retrieved,
                    manifest.get("source_generated_utc"),
                    json.dumps(payload, separators=(",", ":"), sort_keys=True)))
    return out

def run(db_path, data_dir, apply=False):
    db = sqlite3.connect(str(db_path))
    try:
        cols = {r[1] for r in db.execute('PRAGMA table_info("supplemental_records")')}
        required = {"record_id","dataset","game_id","team_id","week","source_url",
                    "retrieved_at","asset_updated_at","data"}
        if not required.issubset(cols):
            raise RuntimeError("supplemental_records schema mismatch; missing " + repr(sorted(required-cols)))
        rows = prepare_rows(db, data_dir)
        unique = len({r[0] for r in rows})
        matched = sum(r[2] is not None for r in rows)
        if unique != len(rows):
            raise RuntimeError("Duplicate deterministic record IDs in source package")
        existing = {r[0] for r in db.execute("SELECT record_id FROM supplemental_records WHERE dataset IN (?,?)", tuple(DATASETS.values()))}
        if apply:
            db.execute("BEGIN IMMEDIATE")
            db.executemany("""INSERT INTO supplemental_records
                (record_id,dataset,game_id,team_id,week,source_url,retrieved_at,asset_updated_at,data)
                VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT(record_id) DO UPDATE SET
                  game_id=excluded.game_id, team_id=excluded.team_id, week=excluded.week,
                  source_url=excluded.source_url, retrieved_at=excluded.retrieved_at,
                  asset_updated_at=excluded.asset_updated_at, data=excluded.data""", rows)
            db.commit()
            integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        else:
            integrity = "not_run_dry_run"
        return {"status":"IMPORTED" if apply else "DRY_RUN",
                "source_rows":len(rows),"unique_rows":unique,
                "team_game_rows":sum(r[1]==DATASETS["team"] for r in rows),
                "quarter_rows":sum(r[1]==DATASETS["quarter"] for r in rows),
                "metric_catalog_rows":sum(r[1]==DATASETS["catalog"] for r in rows),
                "existing_source_rows":len(existing),"new_or_updated_rows":len(rows),
                "game_id_matches":matched,"unmatched_or_ambiguous":len(rows)-matched,
                "sqlite_integrity":integrity,"model_weights_changed":False}
    finally:
        db.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db",required=True,help="private source SQLite database path")
    p.add_argument("--data-dir",default=str(Path(__file__).resolve().parents[1] / "data_packages/sharp_advanced_2026_w1_10"))
    p.add_argument("--apply",action="store_true",help="write records; without this flag the command is a dry run")
    a=p.parse_args()
    print(json.dumps(run(a.db,a.data_dir,a.apply),indent=2))

if __name__=="__main__":
    main()
