"""Fail-closed *research-only* quarantine for unsafe 2026 Week9 projection rows.

Does not change original frozen forecasts or the production model.
"""
import csv,json
from collections import Counter
from pathlib import Path
ROOT=Path("research")
F=ROOT/"week9_1pm_live/WEEK9_1PM_100K_SIMULATIONS.csv"
M=ROOT/"WEEK9_DAY1_MODEL_SIMULATION_20261108.csv"
G=ROOT/"WEEK9_SUNDAY_FINAL_FORECAST_GRADES_20261108.csv"

def rows(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def scan():
    early=rows(F);morning=rows(M);grade=rows(G)
    if len(early)!=1299 or len(morning)!=471 or len(grade)!=1599:
        raise ValueError("frozen archive changed; do not release")
    status=Counter(x["status"] for x in early)
    low_history=[x for x in early if int(x["prior_games"])<3]
    uncalibrated=[x for x in morning if "UNCALIBRATED" in x["status"]]
    sample=[x for x in early if x["player"]=="Shedeur Sanders" and x["market"]=="passing_yards"]
    if not sample or any(float(x["mean_projection"])>2 or int(x["prior_games"])>2 for x in sample):
        raise ValueError("known low-sample passing anomaly changed")
    player_dnp=[x for x in grade if x["reg_grade"]=="DNP_UNGRADED"]
    late=[x for x in grade if x["window"] in ("Late/SNF frozen overlay","Late/SNF range only","SNF pregame chat")]
    report={
        "status":"RELEASE_BLOCKED_RESEARCH_ONLY",
        "production_model_modified":False,
        "fatal_model_calibration":{"raw_not_bet_gradeable":status.get("RAW_EMPIRICAL_BOOTSTRAP_NOT_BET_GRADEABLE",0),
            "uncalibrated_morning_rows":len(uncalibrated)},
        "history_quality":{"frozen_1pm_simulation_rows":len(early),
                           "below_three_prior_games":len(low_history)},
        "known_issue":{
            "player":"Shedeur Sanders",
            "market":"passing_yards",
            "line":191.5,
            "frozen_projection_means":sorted({float(x["mean_projection"]) for x in sample}),
            "prior_games":2,
            "severity":"BLOCK_FROM_PROP_DISPLAY_AND_AUTOMATED_RECOMMENDATIONS",
            "reason":"2-game empirical history includes zero-stat outing; extreme sample mismatch"},
        "source_notes":{
            "DNP_ungraded_rows":len(player_dnp),
            "late_heterogeneous_rows":len(late),
            "run_uses_verified_regulation_outcomes":True,
            "draws_are_not_calibrated_probabilities":True,
        },
        "action_required":[
            "Enforce source status NOT_BET_GRADEABLE before any prediction or slip publishing.",
            "Add true pregame starter/role and availability gate before forecasting low-sample QBs.",
            "Require a later untouched multi-slate Brier and calibration audit.",
            "Keep missed coverage, defender responsibilities, and routes NULL rather than made up.",
            "Do not mingle late mean-only overlays with probabilistic simulations or mark them as Lightning.",
        ]}
    return report

def main():
    report=scan()
    path=ROOT/"WEEK9_20261108_PUBLICATION_GUARD.json"
    path.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("PUBLICATION_GUARD=",json.dumps({k:report[k] for k in ("status","fatal_model_calibration","history_quality","known_issue")},sort_keys=True))
if __name__=="__main__":main()
