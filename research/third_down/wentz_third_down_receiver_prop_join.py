"""Join independent official 2025 Minnesota receiver game logs to audited
Wentz-era third-down dropbacks. Research only, no live projection changes.

Receiver receptions/yards are FULL GAME team outcomes. The 2025 Week 3 and
Week 8 games had brief Max Brosmer relief snaps, so these cannot ALL be
attributed to Wentz individually. Third-down sacks, by contrast, are Wentz's
personally verified dropbacks.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path("research/third_down")
AUDIT=ROOT/"wentz_2025_third_down_audit_20261109.json"
OUT=ROOT/"wentz_third_down_jefferson_hockenson_props_20261109.json"
# Frozen full-game box-score outcomes manually transcribed from Vikings official
# box scores and independently matched to player game logs. Each record is
# documented with a source URL to make revisions auditable.
OFFICIAL={
    3:{"opponent":"CIN","jefferson_rec":5,"jefferson_yds":75,
       "hockenson_rec":5,"hockenson_yds":49,
       "source":"https://www.vikings.com/game-day/2025/bengals-reg-week3/box-score"},
    4:{"opponent":"PIT","jefferson_rec":10,"jefferson_yds":126,
       "hockenson_rec":4,"hockenson_yds":39,
       "source":"https://www.vikings.com/game-day/2025/steelers-reg-week4/box-score"},
    5:{"opponent":"CLE","jefferson_rec":7,"jefferson_yds":123,
       "hockenson_rec":6,"hockenson_yds":38,
       "source":"https://www.vikings.com/game-day/2025/browns-reg-week5/box-score"},
    7:{"opponent":"PHI","jefferson_rec":5,"jefferson_yds":79,
       "hockenson_rec":6,"hockenson_yds":43,
       "source":"https://www.vikings.com/game-day/2025/eagles-reg-week7/box-score"},
    8:{"opponent":"LAC","jefferson_rec":7,"jefferson_yds":74,
       "hockenson_rec":2,"hockenson_yds":26,
       "source":"https://www.vikings.com/game-day/2025/chargers-reg-week8/box-score"},
}
THRESHOLDS={
    "jefferson_over_70_5_yds":lambda x:x["jefferson_yds"]>70.5,
    "jefferson_over_77_5_yds":lambda x:x["jefferson_yds"]>77.5,
    "jefferson_7plus_rec":lambda x:x["jefferson_rec"]>=7,
    "jefferson_8plus_rec":lambda x:x["jefferson_rec"]>=8,
    "hockenson_over_4_5_rec":lambda x:x["hockenson_rec"]>4.5,
}

def generate(audit=AUDIT):
    data=json.loads(Path(audit).read_text())
    if data.get("status")!="RESEARCH_ONLY_VERIFIED_PBP_NO_UNSUPPORTED_PRESSURE_CLAIM":
        raise ValueError("third-down PBP audit is not source verified")
    games=data["game_details_2025_wentz"]
    if len(games)!=5 or {g["week"] for g in games}!={*OFFICIAL}:
        raise ValueError("2025 Wentz start list changed: update separately")
    details=[]
    for game in sorted(games,key=lambda x:x["week"]):
        week=game["week"]
        o=OFFICIAL[week]
        team=game["team"];qb=game["wentz"]
        if qb["third_down_sacks"]<0 or qb["third_down_sacks"]>qb["third_down_dropbacks"]:
            raise ValueError("implausible QB sack count")
        if not 0<=team["third_down_conversions"]<=team["third_down_attempts"]:
            raise ValueError("invalid team 3rd-down conversions")
        conversion=team["third_down_conversions"]/team["third_down_attempts"]
        row={
            "week":week,"opponent":o["opponent"],"game_id":game["game_id"],
            "wentz_third_down_sacks":qb["third_down_sacks"],
            "wentz_total_sacks":qb["total_sacks"],
            "wentz_third_down_dropbacks":qb["third_down_dropbacks"],
            "vikings_third_down_conversions":team["third_down_conversions"],
            "vikings_third_down_attempts":team["third_down_attempts"],
            "vikings_third_down_pct":round(conversion*100,2),
            "high_3d_sack_exposure":qb["third_down_sacks"]>=2,
            "below_35pct_3d_conversion":conversion<0.35,
            **o
        }
        row["prop_clears"]={name:fn(row) for name,fn in THRESHOLDS.items()}
        details.append(row)
    def summary(rows):
        return {
            "games":len(rows),
            "thresholds":{
                key:{"clears":sum(row["prop_clears"][key] for row in rows),
                     "sample":len(rows)}
                for key in THRESHOLDS},
        }
    return {
        "status":"VERIFIED_HISTORICAL_MATCHUP_2025_ONLY_RESEARCH",
        "asof_cutoff":"before 2026-11-09 Bills at Vikings kickoff",
        "pregame_market_lines_2026_11_09":"reference thresholds only, no live book odds",
        "threshold_explanation":"70.5 yards needs 71; 77.5 needs 78; 7+ catches differs from over 7 catches needing 8; Hockenson 4.5 needs 5.",
        "all_five_wentz_starts":summary(details),
        "third_down_sacks_2plus":summary([x for x in details if x["high_3d_sack_exposure"]]),
        "team_third_down_conversion_below_35pct":summary([x for x in details if x["below_35pct_3d_conversion"]]),
        "per_game":details,
        "warnings":[
            "Small selected five-game sample; high 3rd-down sack group four games. Historical clearance != forecast hit probability.",
            "Official receiving boxscore is entire team/game, including brief backup QB action in W3 and W8.",
            "Observed sacks/failed third downs are NOT separately sourced charted pressures or blitz rates.",
            "Pass attempts, score script, QB substitutions and missed plays affect receiving opportunity independently.",
            "The same games appear in all groups; do not infer independent samples or causal effects.",
            "The 2026 W1 Packers relief outing cannot be treated as Wentz full start and is excluded from this five-start comparison.",
        ],
    }

def main():
    summary=generate()
    OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print("WENTZ_RECEIVER_MATCHUP=",json.dumps({
        "all_5":summary["all_five_wentz_starts"],
        "high_sacks":summary["third_down_sacks_2plus"],
        "stalled_3d":summary["team_third_down_conversion_below_35pct"]
    },sort_keys=True))

if __name__=="__main__":
    main()
