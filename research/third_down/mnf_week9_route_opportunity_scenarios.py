"""Pregame NFL Week 9 BUF@MIN receiver-route and injury opportunity scenarios.

Research-only, deterministic stress test. Historical route charting differs from
official play-by-play, so its route counts are explicit sourced inputs. No
2026 W9 result, no trained model/production weights, no calibrated probability.
Pass attempts, sack and scramble scenarios are illustrative, not outcomes.
"""
from __future__ import annotations
import json
from datetime import datetime,timezone
from pathlib import Path

OUT=Path("research/third_down/mnf_week9_route_opportunity_scenarios_20261109.json")
# 2026 weeks where Hockenson and Jefferson were available; exclude W4
# Jefferson INACTIVE and W5 Hockenson injured early. Route sources:
# PlayerProfiler weekly routes W1-3, RotoWire weekly team-dropbacks W7-8.
ROUTES=[
    {"week":1,"routes":23,"dropbacks":31,"targets":5,"source":"PlayerProfiler"},
    {"week":2,"routes":18,"dropbacks":24,"targets":4,"source":"PlayerProfiler"},
    {"week":3,"routes":20,"dropbacks":34,"targets":4,"source":"PlayerProfiler"},
    {"week":7,"routes":19,"dropbacks":29,"targets":5,"source":"RotoWire"},
    {"week":8,"routes":22,"dropbacks":33,"targets":5,"source":"RotoWire"},
]
# From source-verified NFL gamebooks / 2025-2026 Wentz-only target audit.
WENTZ_HOCK_TARGETS=37
WENTZ_PASS_ATTEMPTS=208
WENTZ_HOCK_CATCHES=29
WENTZ_HOCK_RECEIVING_YARDS=253
# Jefferson Wentz 2026-only partial sample: 12 targets / 39 attempts and 8
# catches on those 12; use conservative SHRUNK scenario shares (not fitted).
# Addison Wentz 2025-26: 37 targets / 188 attempts, 23 catches / 37.
JEFFERSON_CATCH_SCENARIO=.70
JEFFERSON_TARGET_SHARE_SCENARIOS={"low":.27,"base":.29,"high":.31}
JEFFERSON_YARDS_PER_CATCH_SCENARIO=12.5
ADDISON_TARGET_SHARE=37/188
ADDISON_CATCH_RATE=23/37
ADDISON_YARDS_PER_CATCH_SCENARIO=12.5
# Explicitly separate official completion passes, sacks and scrambling.
SCENARIOS={
    "vikings_low_volume":dict(pass_attempts=24,sacks=3,scrambles=1,hockenson_route_rate=.66,jefferson_share=.27),
    "competitive_base":dict(pass_attempts=30,sacks=5,scrambles=1,hockenson_route_rate=.69,jefferson_share=.29),
    "vikings_trailing_pass_heavy":dict(pass_attempts=38,sacks=6,scrambles=2,hockenson_route_rate=.70,jefferson_share=.31),
    "hockenson_protection_increase":dict(pass_attempts=30,sacks=5,scrambles=1,hockenson_route_rate=.55,jefferson_share=.29),
}
LINES={
    "hockenson_receptions":4.5,
    "hockenson_receiving_yards":41.5,
    "jefferson_receptions":6.5,
    "jefferson_receiving_yards":77.5,
    "addison_receptions":3.5,
    "addison_receiving_yards":39.5,
    "wentz_pass_attempts":30.5,
}
SOURCES={
    "Hockenson routes weeks 1-3":"https://www.playerprofiler.com/nfl/tj-hockenson/",
    "Hockenson routes week 7":"https://www.rotowire.com/football/article/nfl-box-score-breakdown-week-7-recap-usage-stats-144024",
    "Hockenson routes week 8":"https://aws-prod-web9.rotowire.com/football/article/nfl-box-score-breakdown-week-8-recap-usage-stats-145045",
    "Vikings official injuries":"https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season",
    "Bills official injuries":"https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-vikings-week-9",
    "Book line capture":"https://edgelabs.bet/nfl/props?market=player_receptions",
}
# No injury is given a guessed numerical weight: each impacts specific
# scenario and should be treated as unresolved until inactives are published.
INJURIES={
 "MIN_Kyler_Murray":{"status":"OUT","impact":"Wentz starts; historic targets/pass attempts must be QB-specific"},
 "MIN_Jauan_Jennings":{"status":"OUT","impact":"Receiving routes available for redistribution; not necessarily all to Hockenson"},
 "MIN_Demond_Claiborne":{"status":"OUT","impact":"RB snaps may concentrate toward Jones/Mason/Dallas"},
 "MIN_Theo_Jackson":{"status":"QUESTIONABLE","impact":"Safety depth/coverage disguise uncertainty vs Buffalo"},
 "MIN_Jay_Ward":{"status":"QUESTIONABLE","impact":"Safety depth/coverage disguise uncertainty vs Buffalo"},
 "MIN_Isaiah_Rodgers":{"status":"NO_DESIGNATION","impact":"Full practice and expected available; avoid claiming weak injured CB matchup"},
 "MIN_Andrew_Van_Ginkel":{"status":"NO_DESIGNATION","impact":"Full Saturday practice; expected to maintain rush capability"},
 "MIN_Christian_Darrisaw":{"status":"NO_DESIGNATION","impact":"Expected availability at tackle, monitor if limited"},
 "BUF_Joshua_Palmer":{"status":"OUT","impact":"Buffalo receiver routes redistributed toward Moore/Shakir/Coleman"},
 "BUF_Dion_Dawkins":{"status":"QUESTIONABLE","impact":"Left tackle may be absent; alters Cook lane/Allen pocket/scramble and deep throws"},
 "BUF_Alec_Anderson":{"status":"QUESTIONABLE","impact":"Guard may be absent; pocket/inside-zone and edge stress"},
 "BUF_Greg_Gaines":{"status":"QUESTIONABLE","impact":"Run front depth may decrease if OUT; affects Mason/Jones ground efficiency"},
 "BUF_Jordan_Hancock":{"status":"QUESTIONABLE","impact":"Depth DB uncertain, activation required"},
 "BUF_Spencer_Brown":{"status":"NO_DESIGNATION","impact":"Right tackle back after injury and full practice"},
 "BUF_Dee_Alford":{"status":"NO_DESIGNATION","impact":"Slot CB full practice; don't invent Addison slot edge"},
 "BUF_Khalil_Shakir":{"status":"NO_DESIGNATION","impact":"Full Saturday practice after excused personal Friday absence"},
}
def derive(route_rows=ROUTES,scenarios=SCENARIOS):
    if {r["week"] for r in route_rows}!={1,2,3,7,8}:
        raise ValueError("healthy Jefferson/Hockenson route-week selection drift")
    if any(r["routes"]>r["dropbacks"] or r["targets"]>r["routes"] or
           min(r["routes"],r["targets"],r["dropbacks"])<0 for r in route_rows):
        raise ValueError("invalid route/target/dropback denominators")
    total_routes=sum(r["routes"] for r in route_rows)
    total_dropbacks=sum(r["dropbacks"] for r in route_rows)
    total_targets=sum(r["targets"] for r in route_rows)
    if (total_routes,total_dropbacks,total_targets)!=(102,151,23):
        raise ValueError("charting samples changed; do not silently refit")
    tpr=total_targets/total_routes
    catch_rate=WENTZ_HOCK_CATCHES/WENTZ_HOCK_TARGETS
    ypc=WENTZ_HOCK_RECEIVING_YARDS/WENTZ_HOCK_CATCHES
    result={}
    for name,s in scenarios.items():
        throws=s["pass_attempts"];sacks=s["sacks"];scrambles=s["scrambles"]
        route_rate=s["hockenson_route_rate"]
        if min(throws,sacks,scrambles)<0 or not 0<=route_rate<=1:
            raise ValueError("invalid scenario")
        db=throws+sacks+scrambles
        h_routes=db*route_rate
        h_targets=h_routes*tpr
        h_catches=h_targets*catch_rate
        h_yards=h_catches*ypc
        jj_targets=throws*s["jefferson_share"]
        jj_catches=jj_targets*JEFFERSON_CATCH_SCENARIO
        jj_yards=jj_catches*JEFFERSON_YARDS_PER_CATCH_SCENARIO
        add_targets=throws*ADDISON_TARGET_SHARE
        add_catches=add_targets*ADDISON_CATCH_RATE
        add_yards=add_catches*ADDISON_YARDS_PER_CATCH_SCENARIO
        if h_targets+jj_targets+add_targets>throws:
            raise ValueError("receiver target scenarios exceed all QB throws")
        row={
          "wentz_official_pass_attempts":throws,
          "wentz_sacks":sacks,
          "wentz_scrambles":scrambles,
          "estimated_dropbacks":db,
          "hockenson_route_participation":route_rate,
          "hockenson_expected_routes":h_routes,
          "hockenson_expected_targets":h_targets,
          "hockenson_expected_receptions":h_catches,
          "hockenson_expected_receiving_yards":h_yards,
          "hockenson_wentz_share_crosscheck_targets":throws*WENTZ_HOCK_TARGETS/WENTZ_PASS_ATTEMPTS,
          "jefferson_expected_targets":jj_targets,
          "jefferson_expected_receptions":jj_catches,
          "jefferson_expected_receiving_yards":jj_yards,
          "addison_expected_targets":add_targets,
          "addison_expected_receptions":add_catches,
          "addison_expected_receiving_yards":add_yards,
          "remaining_other_receivers_targets":throws-(h_targets+jj_targets+add_targets),
        }
        for market,line in LINES.items():
            # Wentz passes threshold includes strict > comparisons on numeric
            # means; no empirical hit probability supplied.
            value=throws if market=="wentz_pass_attempts" else row.get(market.replace("receptions","expected_receptions").replace("receiving_yards","expected_receiving_yards"))
            if value is None: raise ValueError(f"missing forecast for {market}")
            row[f"{market}_delta_vs_book"]=round(value-line,2)
        result[name]={k:round(v,3) if isinstance(v,float) else v for k,v in row.items()}
    if not (result["vikings_low_volume"]["hockenson_expected_receptions"]
            <result["competitive_base"]["hockenson_expected_receptions"]
            <result["vikings_trailing_pass_heavy"]["hockenson_expected_receptions"]):
        raise ValueError("non-monotonic Hockenson volume scenarios")
    if result["hockenson_protection_increase"]["hockenson_expected_receptions"] >= result["competitive_base"]["hockenson_expected_receptions"]:
        raise ValueError("protection route risk not reflected")
    return {
      "status":"RESEARCH_ONLY_DETERMINISTIC_SENSITIVITY_NOT_CALIBRATED_PROBABILITIES",
      "sport":"NFL","game":"BUF@MIN","kickoff_local":"2026-11-09T20:15:00-05:00",
      "pregame_cutoff":"2026-11-09 morning ET before kickoff",
      "observed_route_evidence":{"routes":total_routes,"team_dropbacks":total_dropbacks,
        "routes_per_dropback":round(total_routes/total_dropbacks,4),
        "hockenson_targets":total_targets,"targets_per_route":round(tpr,4),
        "exclusions":"2026 Week4 Jefferson absent (Hockenson 13 catches); Week5 Hockenson early exited after 1 route"},
      "hockenson_wentz_target_history":{"targets":37,"pass_attempts":208,"catches":29,
        "receiving_yards":253,"targets_per_attempt":round(37/208,4),
        "catch_rate":round(catch_rate,4),"yards_per_reception":round(ypc,3)},
      "market_reference":{"captured_2026_11_09_0408_ET":True,
        "values":LINES,
        "source_note":"Multi-book publicly captured lines; not personal wager or proof lines remain unchanged"},
      "injuries_known_before_game":INJURIES,
      "scenarios":result,
      "sources":SOURCES,
      "warning_flags":[
        "Wentz pressure/completion split by blitz is not source-verified. Sack counts are not charted pressure.",
        "Routes are vendor-charted and may differ by 1-2 routes between vendors; not official NFL route stats.",
        "Recent healthy route sample mixes Murray and Wentz; Wentz-specific targets come from two seasons.",
        "Wentz/Jefferson 2026-only share =12/39; Jefferson scenario shrinks to 27–31%, a SUBJECTIVE assumption.",
        "Receiving yards/catch 12.5 for Jefferson/Addison is a stress-test assumption, not a trained matchup estimate.",
        "Opponent team-level TE allowances cannot establish Hockenson-specific defender assignments.",
        "No individual cornerback shadow / zone responsibility derived without charted data.",
        "Pass attempts and game-script scenarios have NO fitted probabilities; threshold deltas are NOT expected value or betting edge.",
        "Final inactives must be rechecked before kickoff and 4AM quotes may move.",
        "Protection-heavy route rate 55% is a hypothetical scenario, not a documented coaching decision.",
        "Model projection parameters and production baseline unchanged.",
      ]
    }
def main():
    report=derive()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("W9_ROUTE_OPPORTUNITY_AUDIT=",json.dumps({
     "routes":report["observed_route_evidence"],
     "scenarios":report["scenarios"],"status":report["status"]
    },sort_keys=True))
if __name__=="__main__":main()
