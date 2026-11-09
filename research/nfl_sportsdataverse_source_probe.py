"""Optional public SportsDataverse NFL 2026 player-stat live source audit.

Source update may lag games. Query public nflverse release through SportsDataverse,
validate league/game IDs, reconcile any matching Sunday 2026 final player stats
to gamebook/ESPN archive, and emit an allow/deny ingestion manifest.
Never writes production tables or uses postgame stats as pregame features.
"""
from __future__ import annotations
import csv,json,re,unicodedata
from collections import defaultdict,Counter
from datetime import datetime,timezone
from pathlib import Path

DEST=Path("research/NFL_SPORTSDATAVERSE_SOURCE_STATUS_20261109.json")
BASE=Path("research/WEEK9_SUNDAY_FINAL_PLAYER_STATS_20261108.csv")
EXPECTED={
 "CIN@ATL","DAL@IND","NYJ@KC","DET@MIA","CLE@NO","NYG@PHI",
 "LAR@WAS","DEN@CAR","HOU@LAC","GB@NE","LV@SF","ARI@SEA","TB@CHI"
}
STAT_FIELDS={
 "receptions":"receptions",
 "receiving_yards":"receiving_yards",
 "targets":"targets",
 "rushing_attempts":"carries",
 "rushing_yards":"rushing_yards",
 "passing_yards":"passing_yards",
}
ALIASES={"LA":"LAR","WSH":"WAS"}

def normalize_name(name):
    return re.sub(r"[^a-z0-9]","",unicodedata.normalize("NFKD",str(name)).casefold())

def football_game_id(game_id):
    parts=str(game_id).split("_")
    if len(parts)!=4 or parts[0]!="2026" or parts[1]!="09":
        return None
    away=ALIASES.get(parts[2],parts[2]);home=ALIASES.get(parts[3],parts[3])
    val=f"{away}@{home}"
    return val if val in EXPECTED else None

def week9_game_from_teams(row):
    # nflverse's stable load_nfl_player_stats schema lacks a game_id.
    # Reconstruct only using a verified, unique team/opponent pair in 2026 W9.
    if str(row.get("season"))!="2026" or str(row.get("week"))!="9":
        return None
    if str(row.get("season_type",""))!="REG":
        return None
    team_raw=str(row.get("recent_team") or row.get("team") or "")
    opponent_raw=str(row.get("opponent_team") or row.get("opponent") or "")
    team=ALIASES.get(team_raw,team_raw)
    opponent=ALIASES.get(opponent_raw,opponent_raw)
    candidates=[]
    for g in EXPECTED:
        away,home=g.split("@")
        if {team,opponent}=={away,home} and team and opponent and team!=opponent:
            candidates.append(g)
    if len(candidates)>1:
        raise ValueError("ambiguous team-opponent week9 game identity")
    return candidates[0] if candidates else None

def summarize(rows, official):
    unique={};games=set();duplicates=0
    for record in rows:
        game=(football_game_id(record.get("game_id"))
              if record.get("game_id") else week9_game_from_teams(record))
        if not game:continue
        player_id=record.get("player_id") or record.get("gsis_id")
        pname=record.get("player_display_name") or record.get("player_name")
        team=record.get("recent_team") or record.get("team")
        if not all((player_id,pname,team)):continue
        team=ALIASES.get(str(team),str(team))
        key=(game,team,normalize_name(pname))
        if key in unique:
            duplicates+=1
            continue
        games.add(game);unique[key]=record
    matched=0;missing=0;mismatches=[]
    for entry in official:
        if entry["market"] not in STAT_FIELDS:continue
        key=(entry["game"],entry["team"],normalize_name(entry["player"]))
        src=unique.get(key)
        if src is None:
            missing+=1;continue
        field=STAT_FIELDS[entry["market"]]
        observed=src.get(field)
        if observed is None or observed=="":
            missing+=1;continue
        matched+=1
        try:
            if abs(float(observed)-float(entry["final"]))>0.001:
                mismatches.append({"game":entry["game"],"player":entry["player"],
                    "market":entry["market"],"archived_final":entry["final"],
                    "sportsdataverse_value":str(observed)})
        except (TypeError,ValueError):
            mismatches.append({"game":entry["game"],"player":entry["player"],
                "market":entry["market"],"error":"non_numeric_provider_stat"})
    complete=(games==EXPECTED and duplicates==0 and matched>=100 and not mismatches)
    return {
        "status":"RESEARCH_VERIFIED_MATCHED_PARTIAL_FIELDS" if complete else "BLOCKED_SOURCE_FRESHNESS_OR_PARITY",
        "source":"SportsDataverse NFL load_nfl_player_stats seasons=[2026]; public nflverse stats_player asset",
        "game_id_source":"reconstructed from 2026 W9 unique verified team/opponent pair where original weekly stats lack game_id",
        "source_as_of_utc":None,
        "retrieved_utc":datetime.now(timezone.utc).isoformat(),
        "sdk_sunday_games":sorted(games),
        "missing_games":sorted(EXPECTED-games),
        "sdk_unique_player_game_records":len(unique),
        "duplicate_player_game_records":duplicates,
        "official_metric_matches":matched,
        "official_metric_missing":missing,
        "official_metric_mismatch_count":len(mismatches),
        "mismatch_examples":mismatches[:10],
        "result_eligible_for_automated_model_ingest":False,
        "source_verified_for_research":complete,
        "note":"This is a source parity snapshot, not a timestamped pregame feed or a complete player prop model.",
    }

def main():
    with BASE.open(newline="",encoding="utf-8") as f:official=list(csv.DictReader(f))
    from sportsdataverse.nfl import load_nfl_player_stats
    frame=load_nfl_player_stats(seasons=[2026])
    rows=frame.to_dicts()
    report=summarize(rows,official)
    weeks=sorted({int(x["week"]) for x in rows
                  if x.get("week") is not None and str(x.get("week")).isdigit()})
    report["provider_shape"]={
        "total_rows":len(rows),
        "available_columns":list(frame.columns),
        "weeks_present":weeks,
        "max_week":max(weeks) if weeks else None,
        "week9_rows":sum(str(x.get("week"))=="9" for x in rows),
        "week9_game_ids_sample":sorted({str(x.get("game_id",""))
             for x in rows if str(x.get("week"))=="9"})[:20],
    }
    DEST.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("SPORTSDATAVERSE_2026_W9_SOURCE_STATUS=",json.dumps({k:v for k,v in report.items() if k not in ("provider_shape",)},sort_keys=True))

if __name__=="__main__":main()
