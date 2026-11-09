"""NFL Week 9 fail-closed model publication quality gate.

The history is research-only and includes uncalibrated raw bootstraps, so
successful source/CI checks MUST NOT imply production projection readiness.
Audits existing frozen output, marks publishable only after *all* gates pass.
No change to model predictions or original archived prop lines.
"""
import csv,json
from collections import Counter
from pathlib import Path

SOURCE=Path("research/week9_1pm_live/WEEK9_1PM_100K_SIMULATIONS.csv")
OUT=Path("research/NFL_WEEK9_FORECAST_RELEASE_GATE_20261109.json")
KNOWN_ISSUES=[
    "Uncalibrated empirical frequencies cannot be advertised as calibrated win probabilities.",
    "Insufficient historical player opportunity counts and zero-stat participation must trigger abstentions.",
    "Full defensive coverage/pressure assignments and position-level availability remain unavailable.",
    "No verified current API-SPORTS or BALLDONTLIE NFL key for authenticated ingestion.",
    "Lightning opportunity model and derived efficiency bridge have no prospectively locked prop probabilities.",
    "Single Sunday slate, with duplicated DK/FD prop outcomes, is insufficient for promotion."
]


def evaluate(rows):
    model_names={"season_empirical","rolling5_empirical","opponent_shrunk_rolling5"}
    seen=set()
    counts=Counter()
    for row in rows:
        if row.get("model") not in model_names:
            raise ValueError("unknown model in frozen 1pm research")
        key=tuple(row[k] for k in ("snapshot_id","player","team","opponent","market","book","line","model"))
        if key in seen:raise ValueError("duplicate player prop forecast")
        seen.add(key)
        counts["rows"]+=1
        if row.get("status")=="RAW_EMPIRICAL_BOOTSTRAP_NOT_BET_GRADEABLE":
            counts["not_bet_gradeable"]+=1
        else:counts["unexpected_status"]+=1
        if int(row["prior_games"])<3:counts["under_three_prior_games"]+=1
        if row.get("calibration_status")!="THRESHOLD_DIAGNOSTIC_CORRECTION_APPLIED":
            counts["calibration_not_applied"]+=1
        p=float(row["p_over_raw"])
        if not 0<=p<=1:
            raise ValueError("invalid raw forecast probability")
        if p in (0,1):counts["extreme_raw_probability"]+=1
        if row["player"]=="Shedeur Sanders" and row["market"]=="passing_yards":
            counts["shedeur_passing_yards_rows"]+=1
            if float(row["mean_projection"])<=2:
                counts["shedeur_unrealistic_mean"]+=1
    if counts["rows"]!=1299:
        raise ValueError("1PM archived forecast population unexpectedly changed")
    if counts["not_bet_gradeable"]!=counts["rows"]:
        raise ValueError("some frozen output lost research-only status unexpectedly")
    return {
       "sport":"NFL","date":"2026-11-08",
       "source_scope":"saved 1PM frozen simulation, not live current prop feed",
       "source_rows":counts["rows"],"counts":dict(counts),
       "publish_to_production":False,
       "allow_bet_graded_confidence":False,
       "gate_status":"BLOCKED_RESEARCH_ONLY_EXPECTED",
       "blockers":KNOWN_ISSUES,
       "next_acceptance":"Require original pregame data-as-of, verified role/coverage/snap labels, model recalibration on new slates, keys/entitlement and multi-week blind grading.",
    }

def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:
        report=evaluate(list(csv.DictReader(f)))
    OUT.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("NFL_WEEK9_PUBLISH_GATE=",json.dumps(report,sort_keys=True))

if __name__=="__main__":main()
