#!/usr/bin/env python3
"""Import, reconcile, export and audit the authorized Sharp 2026 W1-10 package.

This script starts from the current public SQLite archive, adds only missing
schedule/game rows and new Sharp supplemental records, preserves legacy source
observations, rebuilds the public snapshot, and emits a machine-readable audit.
It is designed to be idempotent and fail closed.
"""
import argparse
import concurrent.futures
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
import time
import urllib.request

SHARP_PAGE = "https://www.sharpfootballanalysis.com/stats-nfl/nfl-advanced-box-scores/"
SHARP_TEAM_URL = "https://rmsummerlin.github.io/SFAStatsPages/data/boxscore_2026.json"
SHARP_QUARTER_URL = "https://rmsummerlin.github.io/SFAStatsPages/data/boxscore_q_2026.json"
NFLVERSE_SCHEDULE_URL = "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv"
ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates="
DATASETS = {
    "team": "sharp_advanced_boxscore_team_game_2026",
    "quarter": "sharp_advanced_boxscore_quarter_2026",
    "catalog": "sharp_advanced_boxscore_metric_catalog_2026",
}
TEAM_ALIAS = {"LA": "LAR", "LAR": "LAR"}

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def fetch_bytes(url, timeout=90, attempts=4):
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NFL-Matchup-Database/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Could not retrieve {url}: {last}")

def fetch_json(url):
    return json.loads(fetch_bytes(url).decode("utf-8"))

def normalize_team(team):
    return TEAM_ALIAS.get(team, team)

def schedule_rows():
    raw = fetch_bytes(NFLVERSE_SCHEDULE_URL, timeout=120)
    parsed = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    selected = [r for r in parsed
                if r.get("season") == "2026" and r.get("game_type") == "REG"
                and r.get("week") in {str(i) for i in range(1, 11)}]
    by_id = {r["game_id"]: r for r in selected}
    if len(selected) != 150 or len(by_id) != 150:
        raise RuntimeError(f"NFLverse schedule coverage mismatch: {len(selected)} rows, {len(by_id)} unique IDs")
    if any(not r.get("espn") or not r.get("away_score") or not r.get("home_score") for r in selected):
        raise RuntimeError("Schedule contains missing ESPN IDs or final scores")
    if len({r["espn"] for r in selected}) != 150:
        raise RuntimeError("NFLverse schedule contains duplicate ESPN game IDs")
    return raw, by_id

def espn_scoreboards(schedule):
    dates = sorted({r["gameday"].replace("-", "") for r in schedule.values()})
    def one(date):
        data = fetch_json(ESPN_SCOREBOARD_URL + date)
        events = data.get("events", [])
        return date, {str(e.get("id")): e for e in events}
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for date, events in pool.map(one, dates):
            for event_id, event in events.items():
                if event_id in out:
                    raise RuntimeError(f"Duplicate ESPN event returned across scoreboard dates: {event_id}")
                out[event_id] = event
    return dates, out

def event_teams(event):
    comps = event.get("competitions") or []
    if not comps:
        raise RuntimeError(f"ESPN event {event.get('id')} has no competition")
    result = {}
    for competitor in comps[0].get("competitors", []):
        side = competitor.get("homeAway")
        team = competitor.get("team") or {}
        abbr = team.get("abbreviation")
        team_id = str(team.get("id") or competitor.get("id") or "")
        if side not in ("home", "away") or not abbr or not team_id or side in result:
            raise RuntimeError(f"Malformed ESPN team identity in event {event.get('id')}")
        result[side] = {"abbr": abbr, "team_id": team_id,
                        "score": str(competitor.get("score", ""))}
    if set(result) != {"home", "away"}:
        raise RuntimeError(f"ESPN event {event.get('id')} missing home/away team")
    return result

def check_event_against_schedule(event, sched):
    if str(event.get("id")) != str(sched["espn"]):
        raise RuntimeError("ESPN ID does not match NFLverse schedule ID")
    status = (event.get("status") or {}).get("type") or {}
    if status.get("name") != "STATUS_FINAL" or status.get("completed") is not True:
        raise RuntimeError(f"ESPN event {event.get('id')} is not final")
    teams = event_teams(event)
    expected = {
        "home": normalize_team(sched["home_team"]),
        "away": normalize_team(sched["away_team"]),
    }
    for side in ("home", "away"):
        if normalize_team(teams[side]["abbr"]) != expected[side]:
            raise RuntimeError(f"ESPN/NFLverse {side} team mismatch for game {sched['game_id']}")
        if int(float(teams[side]["score"])) != int(float(sched[side + "_score"])):
            raise RuntimeError(f"ESPN/NFLverse {side} score mismatch for game {sched['game_id']}")
    return teams

def parse_existing_event(raw, game_id):
    try:
        return json.loads(raw)
    except Exception as exc:
        raise RuntimeError(f"Existing games.data is invalid JSON for {game_id}: {exc}")

def legacy_hash(db, where_sql, params=()):
    rows = db.execute("SELECT * FROM external_observations WHERE " + where_sql + " ORDER BY observation_id", params).fetchall()
    serial = json.dumps(rows, separators=(",", ":"), ensure_ascii=False)
    return len(rows), sha256_bytes(serial.encode("utf-8"))

def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def source_comparison(team_rows, quarter_rows):
    source_team = fetch_json(SHARP_TEAM_URL)
    source_quarter = fetch_json(SHARP_QUARTER_URL)
    source_games = {g["id"]: g for g in source_team["schedule"] if 1 <= int(g["w"]) <= 10}
    source_quarter_games = source_quarter["games"]
    expected_team = {}
    for game_id, game in source_team["games"].items():
        sched = source_games.get(game_id)
        if not sched:
            continue
        for team in (sched["away"], sched["home"]):
            if team in game:
                expected_team[(game_id, team)] = (sched["date"], int(sched["w"]), game[team])
    actual_team = {(r["source_game_id"], r["team"]): r for r in team_rows}
    if set(expected_team) != set(actual_team):
        raise RuntimeError("Sharp team-game package keys do not match fresh source JSON")
    for key, (date, week, metrics) in expected_team.items():
        row = actual_team[key]
        if row["date"] != date or int(row["week"]) != week or row["metrics"] != metrics:
            raise RuntimeError(f"Sharp team-game source mismatch: {key}")
    expected_quarter = {}
    for game_id, game in source_quarter_games.items():
        sched = source_games.get(game_id)
        if not sched:
            continue
        for team in (sched["away"], sched["home"]):
            for period, metrics in (game.get(team) or {}).items():
                expected_quarter[(game_id, team, int(period))] = (sched["date"], int(sched["w"]), metrics)
    actual_quarter = {(r["source_game_id"], r["team"], int(r["quarter"])): r for r in quarter_rows}
    if set(expected_quarter) != set(actual_quarter):
        raise RuntimeError("Sharp quarter package keys do not match fresh source JSON")
    for key, (date, week, metrics) in expected_quarter.items():
        row = actual_quarter[key]
        if row["date"] != date or int(row["week"]) != week or row["metrics"] != metrics:
            raise RuntimeError(f"Sharp quarter source mismatch: {key}")
    if len(source_team["stats"]) != 43:
        raise RuntimeError(f"Sharp metric catalog expected 43 definitions, got {len(source_team['stats'])}")
    return {
        "team_game_source_exact_matches": len(expected_team),
        "quarter_source_exact_matches": len(expected_quarter),
        "source_metric_definitions": len(source_team["stats"]),
        "source_generated_utc": source_team.get("generated_utc"),
        "quarter_source_generated_utc": source_quarter.get("generated_utc"),
    }

def import_into_db(db_path, package_dir):
    package_dir = Path(package_dir)
    team_rows = load_jsonl(package_dir / "team_games.jsonl")
    quarter_rows = load_jsonl(package_dir / "team_quarters.jsonl")
    package_manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
    if len(team_rows) != 300 or len(quarter_rows) != 1224 or len(package_manifest["metric_catalog"]) != 43:
        raise RuntimeError("Sharp package row/catalog totals do not match expected 300/1224/43")
    source_check = source_comparison(team_rows, quarter_rows)

    schedule_raw, schedule = schedule_rows()
    if set(schedule) != {r["source_game_id"] for r in team_rows}:
        raise RuntimeError("NFLverse schedule and Sharp team-game source IDs do not match exactly")
    for row in team_rows:
        s = schedule[row["source_game_id"]]
        if row["date"] != s["gameday"] or int(row["week"]) != int(s["week"]):
            raise RuntimeError(f"Schedule date/week mismatch for {row['source_game_id']}")
        if {normalize_team(row["team"]), normalize_team(row["opponent"])} != {
            normalize_team(s["home_team"]), normalize_team(s["away_team"])
        }:
            raise RuntimeError(f"Schedule team matchup mismatch for {row['source_game_id']}")
        expected_team = s["home_team"] if row["venue_role"] == "home" else s["away_team"]
        expected_opp = s["away_team"] if row["venue_role"] == "home" else s["home_team"]
        if normalize_team(row["team"]) != normalize_team(expected_team) or normalize_team(row["opponent"]) != normalize_team(expected_opp):
            raise RuntimeError(f"Home/away assignment mismatch for {row['source_game_id']} {row['team']}")

    dates, scoreboard = espn_scoreboards(schedule)
    mapped_events = {}
    for source_game_id, s in schedule.items():
        event = scoreboard.get(str(s["espn"]))
        if event is None:
            raise RuntimeError(f"ESPN scoreboard missing game {s['espn']} ({source_game_id})")
        teams = check_event_against_schedule(event, s)
        mapped_events[source_game_id] = (s, event, teams)
    if len(mapped_events) != 150:
        raise RuntimeError("Not all 150 Sharp games mapped to unique ESPN final results")

    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA foreign_keys=ON")
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise RuntimeError("Input SQLite integrity check failed")
        required_tables = {"games", "supplemental_records", "external_observations"}
        existing_tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not required_tables.issubset(existing_tables):
            raise RuntimeError("Input database missing required tables")
        before84 = legacy_hash(db, "source_id='sharp_advanced' AND json_extract(data,'$.week')=7")
        before_sharp = legacy_hash(db, "source_id='sharp_advanced'")
        if before84[0] != 84:
            raise RuntimeError(f"Expected 84 legacy Week 7 Sharp observations, found {before84[0]}")

        current_games = {r["game_id"]: r for r in db.execute("SELECT game_id,date,status,data FROM games")}
        team_id_by_abbr = {}
        for source_game_id, (s, event, teams) in mapped_events.items():
            espn_id = str(s["espn"])
            for side in ("home", "away"):
                abbr = teams[side]["abbr"]
                team_id = teams[side]["team_id"]
                if abbr in team_id_by_abbr and team_id_by_abbr[abbr] != team_id:
                    raise RuntimeError(f"Ambiguous ESPN team ID for {abbr}")
                team_id_by_abbr[abbr] = team_id
            if espn_id in current_games:
                existing = current_games[espn_id]
                if existing["date"] != s["gameday"]:
                    raise RuntimeError(f"Existing games.date mismatch for ESPN game {espn_id}")
                stored_event = parse_existing_event(existing["data"], espn_id)
                stored_teams = event_teams(stored_event)
                for side in ("home", "away"):
                    if normalize_team(stored_teams[side]["abbr"]) != normalize_team(teams[side]["abbr"]):
                        raise RuntimeError(f"Existing game team identity mismatch for {espn_id}")
                    if str(stored_teams[side]["score"]) != str(teams[side]["score"]):
                        raise RuntimeError(f"Existing game score mismatch against ESPN for {espn_id}")
            else:
                db.execute(
                    "INSERT INTO games(game_id,date,status,data) VALUES(?,?,?,?)",
                    (espn_id, s["gameday"], "STATUS_FINAL",
                     json.dumps(event, separators=(",", ":"), sort_keys=True))
                )
        db.commit()

        # Verify all 32 NFL teams resolve to stable ESPN team IDs.
        if len(team_id_by_abbr) != 32:
            raise RuntimeError(f"Expected 32 ESPN team identities, found {len(team_id_by_abbr)}")
        def team_id_for(abbr):
            target = normalize_team(abbr)
            matches = [tid for name, tid in team_id_by_abbr.items() if normalize_team(name) == target]
            if len(set(matches)) != 1:
                raise RuntimeError(f"Unmatched or ambiguous ESPN team ID for {abbr}: {matches}")
            return matches[0]

        # A complete one-to-one source game -> ESPN event crosswalk.
        crosswalk = {gid: str(s["espn"]) for gid, (s, _, _) in mapped_events.items()}
        if len(crosswalk) != 150 or len(set(crosswalk.values())) != 150:
            raise RuntimeError("Ambiguous or duplicate game-ID crosswalk")

        now = dt.datetime.now(dt.timezone.utc).isoformat()
        new_records = []
        for row in team_rows:
            s = schedule[row["source_game_id"]]
            espn_id = crosswalk[row["source_game_id"]]
            payload = dict(row)
            payload.update({
                "linked_game_id": espn_id,
                "espn_team_id": team_id_for(row["team"]),
                "game_link_status": "matched_unique",
                "source_page": SHARP_PAGE,
                "schedule_source": NFLVERSE_SCHEDULE_URL,
                "score_source": "ESPN scoreboard cross-checked against NFLverse schedule",
                "metric_values_are_publisher_supplied": True,
            })
            dataset = DATASETS["team"]
            rid = sha256_bytes((dataset + "|" + row["source_game_id"] + "|" + row["team"]).encode())
            new_records.append((rid, dataset, espn_id, team_id_for(row["team"]), None,
                                int(row["week"]), SHARP_PAGE, now,
                                package_manifest["source_generated_utc"],
                                json.dumps(payload, separators=(",", ":"), sort_keys=True)))
        for row in quarter_rows:
            espn_id = crosswalk[row["source_game_id"]]
            payload = dict(row)
            payload.update({
                "linked_game_id": espn_id,
                "espn_team_id": team_id_for(row["team"]),
                "game_link_status": "matched_unique",
                "source_page": SHARP_PAGE,
                "schedule_source": NFLVERSE_SCHEDULE_URL,
                "score_source": "ESPN scoreboard cross-checked against NFLverse schedule",
                "metric_values_are_publisher_supplied": True,
            })
            dataset = DATASETS["quarter"]
            rid = sha256_bytes((dataset + "|" + row["source_game_id"] + "|" + row["team"] + "|" + str(row["quarter"])).encode())
            new_records.append((rid, dataset, espn_id, team_id_for(row["team"]), None,
                                int(row["week"]), SHARP_PAGE, now,
                                package_manifest["quarter_source_generated_utc"],
                                json.dumps(payload, separators=(",", ":"), sort_keys=True)))
        for definition in package_manifest["metric_catalog"]:
            key = definition["key"]
            dataset = DATASETS["catalog"]
            rid = sha256_bytes((dataset + "|" + key).encode())
            payload = {
                "source": "Sharp Football Analysis",
                "source_page": SHARP_PAGE,
                "metric_key": key,
                "group": definition["group"],
                "label": definition["label"],
                "kind": definition["kind"],
                "numerator": definition.get("num"),
                "denominator": definition.get("den"),
                "higher_is_better": definition.get("hi_good"),
                "definition": definition,
            }
            new_records.append((rid, dataset, None, None, None, None, SHARP_PAGE, now,
                                package_manifest["source_generated_utc"],
                                json.dumps(payload, separators=(",", ":"), sort_keys=True)))
        if len(new_records) != 1567 or len({r[0] for r in new_records}) != 1567:
            raise RuntimeError("New record total or deterministic ID uniqueness failed")

        # Idempotent insert: a pre-existing deterministic ID must match the same record.
        existing_ids = {r[0]: r for r in db.execute(
            "SELECT record_id,dataset,game_id,team_id,week,source_url,asset_updated_at,data "
            "FROM supplemental_records WHERE record_id IN (" + ",".join("?" for _ in new_records) + ")",
            [r[0] for r in new_records]
        )} if new_records else {}
        for r in new_records:
            old = existing_ids.get(r[0])
            if old:
                expected = (r[0], r[1], r[2], r[3], r[5], r[6], r[8], r[9])
                if tuple(old) != expected:
                    raise RuntimeError(f"Existing Sharp package record conflicts with deterministic ID {r[0]}")
        to_insert = [r for r in new_records if r[0] not in existing_ids]
        db.executemany(
            "INSERT INTO supplemental_records(record_id,dataset,game_id,team_id,player_id,week,source_url,retrieved_at,asset_updated_at,data) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)", to_insert
        )
        db.commit()

        after84 = legacy_hash(db, "source_id='sharp_advanced' AND json_extract(data,'$.week')=7")
        after_sharp = legacy_hash(db, "source_id='sharp_advanced'")
        if after84 != before84:
            raise RuntimeError("Legacy 84 Week 7 Sharp observations changed during import")
        if after_sharp != before_sharp:
            raise RuntimeError("Existing Sharp advanced observation history changed during import")

        counts = {
            "team_game": db.execute("SELECT count(*) FROM supplemental_records WHERE dataset=?", (DATASETS["team"],)).fetchone()[0],
            "quarter": db.execute("SELECT count(*) FROM supplemental_records WHERE dataset=?", (DATASETS["quarter"],)).fetchone()[0],
            "catalog": db.execute("SELECT count(*) FROM supplemental_records WHERE dataset=?", (DATASETS["catalog"],)).fetchone()[0],
        }
        if counts != {"team_game": 300, "quarter": 1224, "catalog": 43}:
            raise RuntimeError(f"Post-import dataset counts incorrect: {counts}")
        bad_team = db.execute("SELECT count(*) FROM supplemental_records WHERE dataset=? AND (game_id IS NULL OR team_id IS NULL)", (DATASETS["team"],)).fetchone()[0]
        bad_quarter = db.execute("SELECT count(*) FROM supplemental_records WHERE dataset=? AND (game_id IS NULL OR team_id IS NULL)", (DATASETS["quarter"],)).fetchone()[0]
        if bad_team or bad_quarter:
            raise RuntimeError(f"Unmatched imported observations: team={bad_team}, quarter={bad_quarter}")
        mapped_games = db.execute(
            "SELECT count(*) FROM games WHERE game_id IN (" + ",".join("?" for _ in crosswalk.values()) + ")",
            list(crosswalk.values())
        ).fetchone()[0]
        if mapped_games != 150:
            raise RuntimeError(f"Only {mapped_games}/150 ESPN games exist after import")
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise RuntimeError("SQLite integrity_check failed after import")
        if db.execute("PRAGMA foreign_key_check").fetchone():
            raise RuntimeError("SQLite foreign_key_check failed after import")

        return {
            "status": "PASS",
            "source_comparison": source_check,
            "schedule_games": 150,
            "espn_final_scoreboard_games_verified": len(mapped_events),
            "unique_game_id_crosswalks": len(crosswalk),
            "ambiguous_game_ids": 0,
            "unmatched_game_ids": 0,
            "new_games_added": sum(1 for gid, (s, _, _) in mapped_events.items() if str(s["espn"]) not in current_games),
            "team_identities": len(team_id_by_abbr),
            "team_game_records": counts["team_game"],
            "quarter_records": counts["quarter"],
            "metric_catalog_records": counts["catalog"],
            "new_supplemental_records": len(to_insert),
            "existing_supplemental_records_reused": len(existing_ids),
            "legacy_week7_sharp_observations": after84[0],
            "legacy_week7_sharp_sha256_before": before84[1],
            "legacy_week7_sharp_sha256_after": after84[1],
            "all_existing_sharp_advanced_observations": before_sharp[0],
            "all_existing_sharp_advanced_sha256_before": before_sharp[1],
            "all_existing_sharp_advanced_sha256_after": after_sharp[1],
            "scoreboard_dates_checked": len(dates),
            "database_integrity": "ok",
            "foreign_key_check": "ok",
            "source_game_ids": 150,
            "source_schedule_sha256": sha256_bytes(schedule_raw),
            "espn_scoreboard_crosswalk": "all 150 games final; team identities and home/away scores match NFLverse schedule",
        }
    finally:
        db.close()

def publish(repo_root, audit_path):
    repo_root = Path(repo_root).resolve()
    package_dir = repo_root / "data_packages/sharp_advanced_2026_w1_10"
    archive = repo_root / "nfl_matchups.sqlite.gz"
    if not archive.exists():
        raise RuntimeError("Current public SQLite archive is missing")
    with tempfile.TemporaryDirectory(prefix="sharp-publication-") as scratch:
        scratch = Path(scratch)
        source_db = scratch / "nfl_matchups.sqlite"
        with gzip.open(archive, "rb") as src, source_db.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        import_audit = import_into_db(source_db, package_dir)
        # Append a durable data-gap/provenance note without rewriting old audit history.
        gap_path = repo_root / "DATA_GAPS.md"
        old_gaps = gap_path.read_text(encoding="utf-8")
        note = f"""

## Sharp advanced box-score public integration — {dt.datetime.now(dt.timezone.utc).date().isoformat()}

- Imported 300 team-game observations, 1,224 team-quarter/OT observations and 43 metric-catalog definitions (1,567 supplemental records total) for 2026 regular-season Weeks 1–10.
- The package's 300 team-game and 1,224 quarter records were compared field-for-field with fresh Sharp source JSON; all matched exactly.
- All 150 Sharp source games mapped one-to-one to unique ESPN game IDs. ESPN final scores and home/away team identities were independently checked against the NFLverse schedule for all 150 games. No unmatched or ambiguous game IDs remain.
- The public game index was extended with {import_audit['new_games_added']} previously absent completed ESPN game records so all Sharp observations have a canonical game link. Other play-by-play/player-stat layers are not implied complete for those added games.
- The pre-existing 84 Week 7 Sharp observations were preserved byte-for-byte at the row level (SHA-256: {import_audit['legacy_week7_sharp_sha256_after']}). All {import_audit['all_existing_sharp_advanced_observations']} pre-existing Sharp advanced observations were also preserved unchanged.
- All four publisher metric groups are present in the database catalog: box, efficiency, passing, and rushing/personnel. No model weights or projection-readiness settings were changed.
"""
        gap_path.write_text(old_gaps.rstrip() + note, encoding="utf-8")
        # Export from the imported copy. The private/public input archive is not overwritten in place.
        from export_snapshot import build
        result = build(source_db, repo_root, gaps=gap_path, force=True)
        if result.get("status") != "READY_TO_PUBLISH":
            raise RuntimeError(f"Public snapshot exporter did not build a new package: {result}")
        manifest_path = repo_root / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        package_manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
        manifest["sharp_advanced"] = {
            "source": "Sharp Football Analysis",
            "season": 2026,
            "weeks": list(range(1, 11)),
            "completed_games": 150,
            "team_game_records": 300,
            "team_quarter_records": 1224,
            "metric_catalog_records": 43,
            "database_records": 1567,
            "metric_groups": {"box": 15, "eff": 10, "pass": 11, "run": 7},
            "legacy_week7_observations_preserved": 84,
            "legacy_week7_sha256": import_audit["legacy_week7_sharp_sha256_after"],
            "unmatched_game_ids": 0,
            "ambiguous_game_ids": 0,
            "espn_final_results_verified": 150,
            "source_generated_utc": package_manifest["source_generated_utc"],
            "quarter_source_generated_utc": package_manifest["quarter_source_generated_utc"],
            "source_schedule_sha256": import_audit["source_schedule_sha256"],
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        audit = {
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "import": import_audit,
            "export": {
                "status": result["status"],
                "games": manifest["coverage"]["games"],
                "tables": manifest["tables"],
                "sqlite_sha256": manifest["sqlite_sha256"],
                "gzip_sha256": manifest["gzip_sha256"],
                "gzip_bytes": manifest["gzip_bytes"],
            },
        }
        Path(audit_path).write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
        return audit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--audit-output", default="/tmp/sharp_advanced_publication_audit.json")
    args = parser.parse_args()
    print(json.dumps(publish(args.repo_root, args.audit_output), indent=2))
