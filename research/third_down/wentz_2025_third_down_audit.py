"""Auditable NFL third-down and possession-opportunity research.

Fetches nflverse 2025 REG PBP for Carson Wentz's Minnesota starts and 2026
REG Weeks 1-8 for both teams. Separates:
  * TEAM 3rd-down conversions (run, pass, flags and penalties)
  * QB dropbacks on 3rd down (passes, sacks and scrambles)
  * QB 3rd-down completions/conversions/negative plays
  * Targets and conversion on 3rd-down QB pass attempts
  * Distances and drives (not a direct possession-time forecast)
Pressure NOTE: PBP sacks and QB hits are NOT all charted pressures. Never
call that a clean-pocket/blitz conversion or a pressure-to-sack rate.

Not imported by production, no model parameters, odds, or database writes.
"""
from __future__ import annotations
import collections
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
import time
import urllib.request

BASE = Path("research/third_down")
BASE.mkdir(parents=True, exist_ok=True)
PBP = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{season}.csv.gz"
WENTZ = "00-0032950"
ALLEN = "00-0034857"
WENTZ_WEEKS_2025 = {3, 4, 5, 7, 8}
VALID_2026_WEEKS = {1, 2, 3, 4, 5, 6, 7, 8}
COLUMNS = ("game_id", "week", "season_type", "posteam", "defteam", "down",
           "ydstogo", "third_down_converted", "third_down_failed",
           "qb_dropback", "pass_attempt", "complete_pass",
           "passer_player_id", "passer_player_name", "rusher_player_id",
           "rusher_player_name", "receiver_player_name",
           "qb_scramble", "sack", "qb_hit", "desc",
           "play_type", "first_down", "touchdown",
           "drive", "play_id", "score_differential", "yards_gained")


def n(value, default=0):
    try:
        v=float(value)
        return default if math.isnan(v) else v
    except (ValueError, TypeError):
        return default


def flag(row, name):
    return n(row.get(name)) == 1


def meaningful_third_down(row):
    """nflfastR official-conversion event flags; exclude no-play."""
    return (int(n(row.get("down"))) == 3 and
            (flag(row,"third_down_converted") or flag(row,"third_down_failed")))


def is_wentz_dropback(row):
    if not flag(row,"qb_dropback"):
        return False
    if row.get("passer_player_id") == WENTZ or row.get("rusher_player_id") == WENTZ:
        return True
    # Narrow fallback for QB sacks with absent passer IDs.
    return (flag(row,"sack") and "Wentz" in row.get("desc","") and
            row.get("posteam")=="MIN")


def is_allen_dropback(row):
    if not flag(row,"qb_dropback"):
        return False
    if row.get("passer_player_id") == ALLEN or row.get("rusher_player_id") == ALLEN:
        return True
    return (flag(row,"sack") and "Allen" in row.get("desc","") and
            row.get("posteam")=="BUF")


def get_source(season):
    path=BASE/f"play_by_play_{season}.csv.gz"
    if path.exists() and path.stat().st_size > 100000:
        return path
    url=PBP.format(season=season)
    for attempt in range(3):
        try:
            request=urllib.request.Request(url,headers={"User-Agent":"NFLThirdDownResearch/1.0"})
            with urllib.request.urlopen(request,timeout=90) as response, path.open("wb") as output:
                import shutil
                shutil.copyfileobj(response,output,1<<20)
            if path.stat().st_size < 100000:
                raise ValueError("NFL play-by-play download appears too small")
            return path
        except Exception:
            if path.exists():path.unlink()
            if attempt==2:raise
            time.sleep(attempt+1)
    raise AssertionError("unreachable")


def read_filtered(path,season):
    selected=[]
    with gzip.open(path,"rt",encoding="utf-8",newline="") as stream:
        reader=csv.DictReader(stream)
        missing=set(COLUMNS)-set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{season}: missing required nflverse columns {sorted(missing)}")
        for r in reader:
            if r["season_type"]!="REG":continue
            week=int(n(r["week"]))
            if season==2025:
                if week not in WENTZ_WEEKS_2025:continue
                if r["posteam"]!="MIN":continue
            else:
                if week not in VALID_2026_WEEKS:continue
                if r["posteam"] not in ("BUF","MIN") and r["defteam"] not in ("BUF","MIN"):
                    continue
            selected.append({c:r.get(c,"") for c in COLUMNS})
    return selected


def bucket(ydstogo):
    d=int(n(ydstogo,-1))
    if d<0:return "unknown"
    return ("1-3" if d<=3 else "4-6" if d<=6 else "7-9" if d<=9 else "10+")


def audit_team(rows,team):
    eligible=[r for r in rows if r["posteam"]==team and meaningful_third_down(r)]
    return {
        "third_down_conversions":sum(flag(r,"third_down_converted") for r in eligible),
        "third_down_attempts":len(eligible),
        "third_down_pct":round(100*sum(flag(r,"third_down_converted") for r in eligible)/len(eligible),1) if eligible else None,
        "by_distance":{b:{
            "conversions":sum(flag(r,"third_down_converted") for r in eligible if bucket(r["ydstogo"])==b),
            "attempts":sum(bucket(r["ydstogo"])==b for r in eligible)
        } for b in ("1-3","4-6","7-9","10+","unknown")},
    }


def audit_qb(rows,selected,team):
    if selected=="wentz":selector=is_wentz_dropback
    elif selected=="allen":selector=is_allen_dropback
    else:raise ValueError("unknown QB")
    all_dropbacks=[r for r in rows if r["posteam"]==team and selector(r) and not flag(r,"no_play") and r.get("play_type")!="no_play"]
    third=[r for r in all_dropbacks if int(n(r["down"]))==3]
    eligible=[r for r in third if meaningful_third_down(r)]
    # nflverse flags sacks with pass_attempt=1; exclude them from true throws.
    attempts=[r for r in third if flag(r,"pass_attempt") and not flag(r,"sack") and not flag(r,"qb_scramble")]
    complete=[r for r in attempts if flag(r,"complete_pass")]
    sacks=[r for r in third if flag(r,"sack")]
    scrambles=[r for r in third if flag(r,"qb_scramble")]
    hits=[r for r in third if flag(r,"qb_hit")]
    overlaps = {
        "pass_attempt_and_sack": [r for r in third if flag(r,"pass_attempt") and flag(r,"sack")],
        "pass_attempt_and_scramble": [r for r in third if flag(r,"pass_attempt") and flag(r,"qb_scramble")],
        "scramble_and_sack": [r for r in third if flag(r,"qb_scramble") and flag(r,"sack")],
    }
    cross_flag_examples = [
        {"game_id":r["game_id"],"play_id":r["play_id"],
         "play_type":r["play_type"],"sack":r["sack"],
         "qb_scramble":r["qb_scramble"],"pass_attempt":r["pass_attempt"],
         "desc":r["desc"][:250]}
        for r in (overlaps["pass_attempt_and_sack"] + overlaps["pass_attempt_and_scramble"])[:8]
    ]
    if len(attempts)+len(sacks)+len(scrambles)!=len(third):
        raise ValueError(
            f"{selected} {team}: third-down throws+sacks+scrambles "
            f"do not reconcile to QB dropbacks; refuse publication"
        )
    targets=collections.defaultdict(lambda:{"targets":0,"catches":0,"third_down_conversions":0})
    for r in attempts:
        name=r["receiver_player_name"] or "(unattributed)"
        t=targets[name]
        t["targets"]+=1
        t["catches"]+=int(flag(r,"complete_pass"))
        t["third_down_conversions"]+=int(flag(r,"third_down_converted"))
    attempts_by_distance={}
    for b in ("1-3","4-6","7-9","10+","unknown"):
        sub=[r for r in third if bucket(r["ydstogo"])==b]
        attempts_by_distance[b]={
            "dropbacks":len(sub),
            "successful":sum(flag(r,"third_down_converted") for r in sub),
            "sacks":sum(flag(r,"sack") for r in sub),
            "completions":sum(flag(r,"complete_pass") for r in sub),
        }
    return {
        "qb":selected,
        "total_dropbacks":len(all_dropbacks),
        "total_sacks":sum(flag(r,"sack") for r in all_dropbacks),
        "overall_sacks_per_dropback_pct":round(100*sum(flag(r,"sack") for r in all_dropbacks)/len(all_dropbacks),1) if all_dropbacks else None,
        "third_down_dropbacks":len(third),
        "third_down_eligible":len(eligible),
        "third_down_dropback_conversions":sum(flag(r,"third_down_converted") for r in eligible),
        "third_down_dropback_conversion_pct":round(100*sum(flag(r,"third_down_converted") for r in eligible)/len(eligible),1) if eligible else None,
        "third_down_pass_attempts":len(attempts),
        "third_down_pass_and_sack_are_disjoint":True,
        "third_down_sack_rate_pct":round(100*len(sacks)/len(third),1) if third else None,
        "third_down_pass_completions":len(complete),
        "third_down_pass_completion_pct":round(100*len(complete)/len(attempts),1) if attempts else None,
        "third_down_sacks":len(sacks),
        "third_down_scrambles":len(scrambles),
        "third_down_qb_hit_flags":len(hits),
        "third_down_overlap_flags":{key:len(value) for key,value in overlaps.items()},
        "third_down_overlap_examples":cross_flag_examples,
        "qb_hit_warning":"QB hit flags not full pressure charting; sack not synonymous with blitz",
        "third_down_by_distance":attempts_by_distance,
        "third_down_receivers":dict(sorted(targets.items(),key=lambda z:-z[1]["targets"])),
    }


def drive_opportunities(rows,team):
    # Offensive drives are not equal-duration. This counts distinct drives and plays,
    # and is deliberately not labeled time of possession.
    drives=collections.defaultdict(lambda:{"plays":0,"thirds":0,"thirds_converted":0})
    for r in rows:
        if r["posteam"]!=team or flag(r,"no_play"):continue
        if r["play_type"] not in ("pass","run"):continue
        game=r["game_id"];drive=r["drive"]
        if not drive:continue
        d=drives[(game,drive)]
        d["plays"]+=1
        if meaningful_third_down(r):
            d["thirds"]+=1;d["thirds_converted"]+=int(flag(r,"third_down_converted"))
    vals=list(drives.values())
    return {
        "offensive_drives_with_offensive_plays":len(vals),
        "offensive_pass_run_plays":sum(x["plays"] for x in vals),
        "offensive_plays_per_drive":round(sum(x["plays"] for x in vals)/len(vals),2) if vals else None,
        "third_down_chances_per_drive":round(sum(x["thirds"] for x in vals)/len(vals),2) if vals else None,
        "note":"Play counts exclude penalties/kicks and are NOT time of possession."
    }


def perform(rows_2025,rows_2026):
    games=collections.defaultdict(list)
    for r in rows_2025:
        games[(r["game_id"],int(n(r["week"])))].append(r)
    if len(games)!=5:
        raise ValueError(f"expected Wentz's five 2025 MIN starts, found {len(games)} games")
    game_details=[]
    for (gid,week),g in sorted(games.items(),key=lambda p:p[0][1]):
        qb=audit_qb(g,"wentz","MIN")
        if qb["total_dropbacks"]<12:
            raise ValueError(f"missing Wentz dropbacks in {gid}: {qb['total_dropbacks']}")
        detail={"game_id":gid,"week":week,"team":audit_team(g,"MIN"),"wentz":qb,
                "drive_opportunity":drive_opportunities(g,"MIN")}
        game_details.append(detail)
    wentz_all=audit_qb(rows_2025,"wentz","MIN")
    min_2025_team=audit_team(rows_2025,"MIN")
    team_2026={x:{
        "offense":audit_team(rows_2026,x),
        "defense_allowed":_team_defense(rows_2026,x),
        "drive_opportunities":drive_opportunities(rows_2026,x),
    } for x in ("BUF","MIN")}
    allen_2026=audit_qb(rows_2026,"allen","BUF")
    if allen_2026["total_dropbacks"]<100:
        raise ValueError("Bills Josh Allen W1-8 qb dropbacks insufficient")
    report={
        "status":"RESEARCH_ONLY_VERIFIED_PBP_NO_UNSUPPORTED_PRESSURE_CLAIM",
        "scope":"Carson Wentz MIN Weeks 3,4,5,7,8 2025; BUF/MIN 2026 REG W1-8; no Week9 outcomes",
        "source":"nflverse official release PBP (open-source public data)",
        "pressure_caveat":"No audited charted pressure/blitz flags on every dropback; qb_hit and sacks are observed subsets only. Pressure-to-conversion conditional rate not computed.",
        "third_down_caveat":"Team third_down_converted/failed flags count all play types and penalties. QB third downs count pass/sack/scramble dropbacks only. Different denominators, do not conflate.",
        "game_details_2025_wentz":game_details,
        "wentz_2025_team_3d":min_2025_team,
        "wentz_2025_qb":wentz_all,
        "team_2026":team_2026,
        "allen_2026_qb":allen_2026,
        "we_cannot_infer_actual_possession_from_3d_alone":True,
        "production_parameters_changed":False,
    }
    return report


def _team_defense(rows,team):
    eligible=[r for r in rows if r["defteam"]==team and meaningful_third_down(r)]
    c=sum(flag(r,"third_down_converted") for r in eligible)
    return {"allowed_3rd_down_conversions":c,"faced_3rd_down_attempts":len(eligible),
            "allowed_pct":round(100*c/len(eligible),1) if eligible else None}


def main():
    sources={}
    subsets={}
    for season in (2025,2026):
        path=get_source(season)
        sources[str(season)]={"download_url":PBP.format(season=season),
                             "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                             "bytes":path.stat().st_size}
        subsets[season]=read_filtered(path,season)
        if len(subsets[season])<200:raise ValueError(f"{season} missing PBP subset")
    report=perform(subsets[2025],subsets[2026])
    report["source_files"]=sources
    report["source_counts"]={str(k):len(v) for k,v in subsets.items()}
    # Save explicit game-by-game QB third-down plays as verifiable audit events,
    # but exclude unrelated private player data, and no late Week9 plays.
    out=BASE/"wentz_2025_third_down_audit_20261109.json"
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("WENTZ_2025_SUMMARY=",json.dumps({
        "wentz_2025_qb":{k:v for k,v in report["wentz_2025_qb"].items() if k not in ("third_down_receivers","third_down_by_distance")},
        "min_2025_team":report["wentz_2025_team_3d"],
        "team_2026":report["team_2026"],
        "allen_2026_qb":{k:v for k,v in report["allen_2026_qb"].items() if k not in ("third_down_receivers","third_down_by_distance")},
        "2025_game_ids":[x["game_id"] for x in report["game_details_2025_wentz"]]
    },sort_keys=True))

if __name__=="__main__":
    main()
