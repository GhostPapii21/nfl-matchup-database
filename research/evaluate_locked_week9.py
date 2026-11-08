#!/usr/bin/env python3
"""Score exact, frozen Week 9 prop probabilities after verified outcomes arrive.

Outcomes CSV columns: player,market,book,line,actual,availability,game_id,source,source_time,source_sha256.
Availability must be ACTIVE, INACTIVE, QUESTIONABLE_ACTIVE, or UNKNOWN. Unknown and inactive
rows are reported separately; only verified active outcome rows are scored here.
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "research" else SCRIPT_DIR
RESEARCH = ROOT / "research"
SIM = RESEARCH / "WEEK9_DAY1_MODEL_SIMULATION_20261108.csv"
LOCK = RESEARCH / "WEEK9_PROSPECTIVE_EVAL_LOCK_20261108_0856ET.json"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outcomes", required=True, help="verified official outcome CSV")
    parser.add_argument("--out", default="research/WEEK9_PROSPECTIVE_SCORE_20261108.csv")
    args = parser.parse_args()
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    if lock["calibration_claim"] is not False or lock["status"] != "FROZEN_PENDING_OUTCOMES":
        raise SystemExit("refusing to score: lock status or calibration claim was altered")
    outcomes = read_csv(Path(args.outcomes))
    forecast_rows = read_csv(SIM)
    overlay = read_csv(RESEARCH / "WEEK9_DAY1_REFRESHED_PROJECTION_OVERLAY_20261108_0823ET.csv")
    exact_keys = {
        (r["player"].strip().casefold(), r["market"], r["book"], float(r["line"]))
        for r in overlay if str(r.get("exact_threshold", "")).lower() == "true"
    }
    actuals = {}
    availability_counts = defaultdict(int)
    for row in outcomes:
        key = (row["player"].strip().casefold(), row["market"], row["book"], float(row["line"]))
        availability = row["availability"].upper()
        availability_counts[availability] += 1
        if availability not in {"ACTIVE", "INACTIVE", "QUESTIONABLE_ACTIVE", "UNKNOWN"}:
            raise SystemExit(f"invalid availability value {availability!r}")
        if key in actuals:
            raise SystemExit(f"duplicate outcome key: {key}")
        actuals[key] = row

    score = []
    for forecast in forecast_rows:
        key = (forecast["player"].strip().casefold(), forecast["market"], forecast["book"], float(forecast["line"]))
        if key not in exact_keys or key not in actuals:
            continue
        outcome = actuals[key]
        if outcome["availability"].upper() not in {"ACTIVE", "QUESTIONABLE_ACTIVE"}:
            continue
        actual = float(outcome["actual"])
        line = float(forecast["line"])
        y = "over" if actual > line else "under" if actual < line else "push"
        p = {name: float(forecast[f"p_{name}"]) for name in ("over", "push", "under")}
        if any(x < 0 or x > 1 for x in p.values()) or abs(sum(p.values()) - 1) > 0.002:
            raise SystemExit(f"invalid three-way probabilities for {key}: {p}")
        brier = sum((p[k] - (1.0 if k == y else 0.0)) ** 2 for k in p)
        logloss = -math.log(max(p[y], 1e-15))
        score.append({
            "game_id": outcome["game_id"], "player": outcome["player"], "market": outcome["market"],
            "book": outcome["book"], "line": line, "model": forecast["model"], "actual": actual,
            "settlement": y.upper(), "p_over": p["over"], "p_push": p["push"], "p_under": p["under"],
            "brier_3way": round(brier, 8), "logloss_3way": round(logloss, 8),
            "outcome_source": outcome["source"], "outcome_source_time": outcome["source_time"],
            "outcome_source_sha256": outcome["source_sha256"],
        })

    counts = defaultdict(list)
    for row in score:
        counts[(row["market"], row["model"])].append(row)
    outpath = ROOT / args.out
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fields = list(score[0]) if score else ["game_id", "player", "market", "book", "line", "model", "actual", "settlement", "p_over", "p_push", "p_under", "brier_3way", "logloss_3way", "outcome_source", "outcome_source_time", "outcome_source_sha256"]
    with outpath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(score)
    print("Availability counts:", dict(availability_counts))
    print("Scored exact-line active forecasts:", len(score))
    for (market, model), rows in sorted(counts.items()):
        print(f"{market} | {model} | n={len(rows)} | Brier={sum(r['brier_3way'] for r in rows)/len(rows):.5f} | logloss={sum(r['logloss_3way'] for r in rows)/len(rows):.5f}")
    print("This is one-slate prospective evidence, not independent-calibration certification.")
    print("Output:", outpath)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
