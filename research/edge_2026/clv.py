"""Build a point-in-time CLV ledger from committed direct-line snapshots."""
from __future__ import annotations

import csv
import json
import subprocess
from collections import defaultdict
from datetime import datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

from fair_price import devig, implied, norm_name

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
LINE_DIR = "pregame/direct_lines"
SCHEDULE = ROOT / "data" / "historical" / "nflverse" / "games.csv"
EASTERN = ZoneInfo("America/New_York")
BOOT_REPS = 5000
BOOT_SEED = 20261119


def _write_json(payload: dict, path: Path, compact_arrays: set[str]) -> None:
    """Write ledger rows compactly while keeping the summary easy to scan."""
    lines = ["{"]
    items = list(payload.items())
    for index, (key, value) in enumerate(items):
        comma = "," if index < len(items) - 1 else ""
        if key in compact_arrays and isinstance(value, list):
            lines.append(f" {json.dumps(key)}: [")
            for row_index, row in enumerate(value):
                row_comma = "," if row_index < len(value) - 1 else ""
                lines.append("  " + json.dumps(row, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + row_comma)
            lines.append(" ]" + comma)
        else:
            encoded = json.dumps(value, indent=1, ensure_ascii=False, allow_nan=False).replace("\n", "\n ")
            lines.append(f" {json.dumps(key)}: {encoded}{comma}")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


def _parse_kickoff(row: dict[str, str]) -> datetime | None:
    day, clock = row.get("gameday"), row.get("gametime")
    if not day or not clock:
        return None
    try:
        local = datetime.combine(datetime.strptime(day, "%Y-%m-%d").date(), time.fromisoformat(clock))
        return local.replace(tzinfo=EASTERN).astimezone(timezone.utc)
    except ValueError:
        return None


def load_schedule() -> dict[str, datetime]:
    schedule = {}
    with SCHEDULE.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("season") != "2026" or row.get("game_id") is None:
                continue
            kickoff = _parse_kickoff(row)
            if kickoff:
                schedule[row["game_id"]] = kickoff
    return schedule


def git_snapshots() -> tuple[list[dict], datetime | None, int]:
    commits = subprocess.run(
        ["git", "log", "--format=%H%x09%cI", "--", LINE_DIR],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / LINE_DIR).glob("20*.json"))
    snapshots: list[dict] = []
    times: list[datetime] = []
    unavailable_blobs = 0
    for line in commits:
        sha, timestamp = line.split("\t", 1)
        committed = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)
        times.append(committed)
        for path in paths:
            blob = subprocess.run(
                ["git", "show", f"{sha}:{path}"], cwd=ROOT,
                text=True, capture_output=True, check=False,
            )
            if blob.returncode:
                if "could not fetch" in blob.stderr:
                    unavailable_blobs += 1
                continue
            try:
                doc = json.loads(blob.stdout)
            except json.JSONDecodeError:
                continue
            gid = str(doc.get("game_id") or Path(path).stem)
            snapshots.append({"time": committed, "game_id": gid, "rows": doc.get("rows", [])})
    return snapshots, max(times) if times else None, unavailable_blobs


def select_open_last(observations: list[dict], kickoff: datetime, as_of: datetime) -> dict:
    eligible = sorted(
        (o for o in observations if o["time"] <= as_of and o["time"] < kickoff),
        key=lambda o: o["time"],
    )
    if not eligible:
        return {"status": "no_pregame_snapshot", "open": None, "last": None, "clv": None}
    opening, last = eligible[0], eligible[-1]
    pending = kickoff > as_of
    distinct_times = len({o["time"] for o in eligible})
    if pending:
        status = "pending_kickoff"
        clv = None
    elif distinct_times < 2:
        status = "single_snapshot"
        clv = None
    else:
        status = "closed"
        clv = implied(last["american"]) - implied(opening["american"])
    return {
        "status": status,
        "open": opening,
        "last": last,
        "clv": clv,
        "distinct_snapshots": distinct_times,
        "provisional_move": implied(last["american"]) - implied(opening["american"]),
    }


def _summary_ci(rows: list[dict]) -> dict:
    if not rows:
        return {"n_clusters": 0, "ci95": [None, None], "method": "cluster bootstrap by game-player-market"}
    clusters: dict[tuple, list[float]] = defaultdict(list)
    for row in rows:
        clusters[(row["game_id"], row["player"], row["market"])].append(float(row["clv"]))
    keys = list(clusters)
    if len(keys) < 2:
        return {"n_clusters": len(keys), "ci95": [None, None], "method": "cluster bootstrap by game-player-market"}
    values = [np.asarray(clusters[key], dtype=float) for key in keys]
    rng = np.random.default_rng(BOOT_SEED)
    idx = rng.integers(0, len(values), size=(BOOT_REPS, len(values)))
    boot = np.empty(BOOT_REPS, dtype=float)
    for i, sample in enumerate(idx):
        selected = [values[j] for j in sample]
        boot[i] = np.concatenate(selected).mean()
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return {
        "n_clusters": len(keys), "ci95": [float(lo), float(hi)],
        "method": "percentile bootstrap resampling game-player-market clusters",
        "reps": BOOT_REPS, "seed": BOOT_SEED,
    }


def _edge_close_grades(edges: list[dict], snapshots: list[dict], schedule: dict[str, datetime], as_of: datetime) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for snapshot in snapshots:
        gid = snapshot["game_id"]
        kickoff = schedule.get(gid)
        if kickoff is None:
            continue
        for row in snapshot["rows"]:
            if row.get("book") != "pinnacle" or row.get("side") not in {"Over", "Under"}:
                continue
            if row.get("line") is None or row.get("american") is None:
                continue
            key = (gid, norm_name(row.get("player", "")), row.get("market"), float(row["line"]))
            groups[key].append({"time": snapshot["time"], "side": row["side"], "american": float(row["american"]), "kickoff": kickoff})
    results = []
    for edge in edges:
        gid = str(edge.get("game_id", ""))
        kickoff = schedule.get(gid)
        pin_line = edge.get("pinnacle_line", edge.get("line"))
        if kickoff is None or pin_line is None:
            results.append({**edge, "close_status": "schedule_or_reference_missing", "moved_toward_us": None})
            continue
        key = (gid, norm_name(edge.get("player", "")), edge.get("market"), float(pin_line))
        candidates = groups.get(key, [])
        by_time: dict[datetime, dict[str, float]] = defaultdict(dict)
        for item in candidates:
            if item["time"] <= as_of and item["time"] < kickoff:
                by_time[item["time"]][item["side"]] = item["american"]
        paired = [(ts, sides) for ts, sides in sorted(by_time.items()) if "Over" in sides and "Under" in sides]
        if kickoff > as_of:
            results.append({**edge, "close_status": "pending_kickoff", "pinnacle_open_fair": None, "pinnacle_close_fair": None, "moved_toward_us": None})
            continue
        if len(paired) < 2:
            results.append({**edge, "close_status": "insufficient_pinnacle_history", "pinnacle_open_fair": None, "pinnacle_close_fair": None, "moved_toward_us": None})
            continue
        open_time, open_sides = paired[0]
        close_time, close_sides = paired[-1]
        open_pair = devig(open_sides["Over"], open_sides["Under"])
        close_pair = devig(close_sides["Over"], close_sides["Under"])
        side_index = 0 if edge.get("side") == "Over" else 1
        p_open, p_close = open_pair[side_index], close_pair[side_index]
        results.append({
            **edge, "close_status": "graded", "pinnacle_open_timestamp": open_time.isoformat(),
            "pinnacle_close_timestamp": close_time.isoformat(),
            "pinnacle_open_fair": round(p_open, 6), "pinnacle_close_fair": round(p_close, 6),
            "pinnacle_fair_move": round(p_close - p_open, 6),
            "moved_toward_us": bool(p_close > p_open),
        })
    return results


def main() -> dict:
    snapshots, as_of, unavailable_blobs = git_snapshots()
    schedule = load_schedule()
    if as_of is None:
        as_of = datetime.now(timezone.utc)
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for snapshot in snapshots:
        kickoff = schedule.get(snapshot["game_id"])
        if kickoff is None:
            continue
        for row in snapshot["rows"]:
            if not row.get("book") or row.get("side") not in {"Over", "Under", "Yes", "No", "Home", "Away"}:
                continue
            if row.get("line") is None or row.get("american") is None or row.get("player") is None:
                continue
            key = (
                snapshot["game_id"], norm_name(row["player"]), str(row.get("market", "")),
                str(row["book"]), str(row["side"]), float(row["line"]),
            )
            grouped[key].append({"time": snapshot["time"], "american": float(row["american"]), "kickoff": kickoff})

    ledger = []
    for (gid, player, market, book, side, line), observations in sorted(grouped.items()):
        kickoff = schedule.get(gid)
        if kickoff is None:
            continue
        selection = select_open_last(observations, kickoff, as_of)
        opening, last = selection["open"], selection["last"]
        row = {
            "game_id": gid, "player": player, "market": market, "book": book,
            "side": side, "line": line, "status": selection["status"],
            "observations": selection.get("distinct_snapshots", 0),
            "kickoff_utc": kickoff.isoformat(),
            "open_timestamp": opening["time"].isoformat() if opening else None,
            "open_american": opening["american"] if opening else None,
            "open_break_even": round(implied(opening["american"]), 6) if opening else None,
            "last_pre_kickoff_timestamp": last["time"].isoformat() if last else None,
            "last_pre_kickoff_american": last["american"] if last else None,
            "last_pre_kickoff_break_even": round(implied(last["american"]), 6) if last else None,
            "clv": round(float(selection["clv"]), 6) if selection["clv"] is not None else None,
            "provisional_open_to_latest_move": round(float(selection["provisional_move"]), 6) if selection.get("provisional_move") is not None else None,
        }
        if last:
            row["last_quote_age_hours"] = round((kickoff - last["time"]).total_seconds() / 3600, 3)
        ledger.append(row)

    complete = [row for row in ledger if row["status"] == "closed" and row["clv"] is not None]
    provisional = [
        row for row in ledger
        if row["status"] == "pending_kickoff" and row["observations"] >= 2
        and row["provisional_open_to_latest_move"] is not None
    ]
    ci = _summary_ci(complete)
    summary = {
        "n": len(complete),
        "mean_clv": round(float(np.mean([r["clv"] for r in complete])), 6) if complete else None,
        "share_positive": round(float(np.mean([r["clv"] > 0 for r in complete])), 6) if complete else None,
        "ci95": [round(float(x), 6) for x in ci["ci95"]] if ci["ci95"][0] is not None else [None, None],
        "ci_method": ci["method"], "independent_clusters": ci["n_clusters"],
        "pending_rows": sum(r["status"] == "pending_kickoff" for r in ledger),
        "single_snapshot_rows": sum(r["status"] == "single_snapshot" for r in ledger),
        "no_pregame_snapshot_rows": sum(r["status"] == "no_pregame_snapshot" for r in ledger),
        "provisional_rows": len(provisional),
        "mean_provisional_open_to_latest_move": round(float(np.mean([r["provisional_open_to_latest_move"] for r in provisional])), 6) if provisional else None,
        "status": "no finalized open-to-close comparisons" if not complete else "complete",
    }
    edge_path = OUT / "edges_latest.json"
    edge_payload = json.loads(edge_path.read_text()) if edge_path.exists() else {"edges": []}
    edge_grades = _edge_close_grades(edge_payload.get("edges", []), snapshots, schedule, as_of)
    result = {
        "schema_version": 1,
        "as_of_utc": as_of.isoformat(),
        "snapshot_commits": len({item["time"] for item in snapshots}),
        "unavailable_historical_blobs": unavailable_blobs,
        "schedule_games": len(schedule),
        "summary": summary,
        "rows": ledger,
        "task1_edge_close_grades": edge_grades,
        "limitations": [
            "A pending game's latest quote is not a closing line; it is reported only as a provisional move.",
            "A single snapshot does not identify open-to-close movement, even if its price is known.",
            "CLV is computed only for games whose kickoff had passed by the latest direct-lines commit and which have at least two distinct pregame observations.",
        ],
    }
    _write_json(result, OUT / "clv.json", {"rows", "task1_edge_close_grades"})
    print(json.dumps({"as_of_utc": result["as_of_utc"], "summary": summary, "ledger_rows": len(ledger), "edge_grades": len(edge_grades)}, indent=1))
    return result


if __name__ == "__main__":
    main()
