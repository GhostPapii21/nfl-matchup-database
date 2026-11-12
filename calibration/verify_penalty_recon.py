"""NFL-49 task D: independently re-check PENALTY_NOTES.md's "228 of 238 team-games match ESPN box totals".

    python3 -m calibration.verify_penalty_recon --espn-raw /workspace/nfl-database/teams/espn_raw

Compares, per (ESPN game id, team): accepted flags (status == accepted, incl. no-play) and their yards from
data/redistributable/teams/penalty_plays_2026.csv against ESPN box `totalPenaltiesYards` ("count-yards") read
directly from the raw ESPN summary JSONs (sum_<id>.json). Does not use penalties_2026.csv's box columns, so the
check is independent of the earlier build. Writes calibration/outputs/penalty_recon_check.{csv,json}.
ESPN raw JSON is NOT redistributed here; its sha256 + file mtime are recorded. Research only, not validated.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYS = ROOT / "data/redistributable/teams/penalty_plays_2026.csv"
OUT = ROOT / "calibration/outputs"
ALIAS = {"WAS": "WSH"}  # ESPN box uses WSH


def box_totals(espn_raw: Path) -> tuple[dict, list]:
    box, files = {}, []
    for p in sorted(espn_raw.glob("sum_*.json")):
        gid = p.stem.split("_", 1)[1]
        d = json.loads(p.read_bytes())
        for t in d["boxscore"]["teams"]:
            st = {s["name"]: s.get("displayValue") for s in t.get("statistics", [])}
            v = st.get("totalPenaltiesYards")
            if v is None:
                continue
            c, y = v.split("-")
            box[(gid, t["team"]["abbreviation"])] = (int(c), int(y))
        files.append({"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                      "mtime_et": datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(timespec="seconds")})
    return box, files


def parsed_totals(plays_csv: Path) -> dict:
    agg = defaultdict(lambda: [0, 0])
    with open(plays_csv, newline="") as f:
        for r in csv.DictReader(f):
            if r["status"] != "accepted":
                continue
            k = (r["game_id"], ALIAS.get(r["team_penalized"], r["team_penalized"]))
            agg[k][0] += 1
            agg[k][1] += int(float(r["yards"] or 0))
    return {k: tuple(v) for k, v in agg.items()}


def compare(box: dict, parsed: dict) -> dict:
    rows = []
    for k in sorted(box):
        bc, by = box[k]
        pc, py = parsed.get(k, (0, 0))
        rows.append({"game_id": k[0], "team": k[1], "box_count": bc, "box_yards": by, "parsed_count": pc,
                     "parsed_yards": py, "match": bc == pc and by == py})
    n = len(rows)
    return {"rows": rows, "team_games": n, "exact_matches": sum(r["match"] for r in rows),
            "box_flags": sum(r["box_count"] for r in rows), "parsed_flags": sum(r["parsed_count"] for r in rows),
            "unmatched_parsed_keys": sorted(f"{a}|{b}" for a, b in set(parsed) - set(box))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--espn-raw", required=True)
    a = ap.parse_args(argv)
    box, files = box_totals(Path(a.espn_raw))
    res = compare(box, parsed_totals(PLAYS))
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "penalty_recon_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(res["rows"][0]))
        w.writeheader(); w.writerows(res["rows"])
    summary = {k: v for k, v in res.items() if k != "rows"}
    summary["mismatches"] = [f"{r['game_id']}|{r['team']}: box {r['box_count']}-{r['box_yards']} vs parsed "
                             f"{r['parsed_count']}-{r['parsed_yards']}" for r in res["rows"] if not r["match"]]
    summary["claim_checked"] = "PENALTY_NOTES.md: 228 of 238 team-games match exactly on count and yards (1,736 vs 1,739 flags)"
    summary["sources"] = {"parsed": {"file": str(PLAYS.relative_to(ROOT)), "sha256": hashlib.sha256(PLAYS.read_bytes()).hexdigest(),
                                     "built": "2026-11-01 ~9 PM ET per PENALTY_NOTES.md (exact minute unknown)"},
                          "espn_box": {"dir": str(a.espn_raw), "n_files": len(files),
                                       "pull_time": "unknown (ESPN responses carry no pull stamp; file mtimes recorded below are the box copy times)",
                                       "files": files}}
    summary["label"] = "research only, not validated"
    (OUT / "penalty_recon_check.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("team_games", "exact_matches", "box_flags", "parsed_flags", "mismatches", "unmatched_parsed_keys")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
