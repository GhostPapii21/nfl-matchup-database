"""NFL-only Week 9 research rescan: frozen inputs, grades, and live ESPN finals."""
import csv,hashlib,json,math,re
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import urlopen,Request

R=Path("research")
EXPECTED={
"CIN@ATL":(34,17),"DAL@IND":(27,23),"NYJ@KC":(12,35),
"DET@MIA":(19,9),"CLE@NO":(22,23),"NYG@PHI":(19,11),
"LAR@WAS":(20,13),"DEN@CAR":(26,21),"HOU@LAC":(44,22),
"GB@NE":(45,27),"LV@SF":(17,38),"ARI@SEA":(3,17),"TB@CHI":(24,27)}
URL="https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261108&limit=100"
F=R/"WEEK9_SUNDAY_FINAL_FORECAST_GRADES_20261108.csv"
A=R/"WEEK9_SUNDAY_FINAL_PLAYER_STATS_20261108.csv"
L=R/"WEEK9_PROSPECTIVE_EVAL_LOCK_20261108_0856ET.json"

def records(path):
    with Path(path).open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def timestamp(s):return datetime.fromisoformat(s.replace("Z","+00:00"))

def audit():
    lock=json.loads(L.read_text())
    assert timestamp(lock["locked_at_utc"])<timestamp("2026-11-08T14:30:00Z")
    for obj in lock["artifacts"]:
        if digest(obj["path"])!=obj["sha256"]:
            raise ValueError("pregame snapshot modified: "+obj["path"])
    rows,actual=records(F),records(A)
    if len(rows)!=1599 or len(actual)!=1315:raise ValueError("archive count drift")
    if {r["game"] for r in rows}!={*EXPECTED} or {r["game"] for r in actual}!={*EXPECTED}:
        raise ValueError("Sunday game coverage incomplete")
    if any(float(r["regulation"])+float(r["ot"])!=float(r["final"]) for r in actual):
        raise ValueError("regulation/OT totals do not reconcile")
    if any(r["game"]!="CLE@NO" and float(r["ot"])!=0 for r in actual):
        raise ValueError("spurious overtime stats")
    seen=set();counts=Counter();agg=defaultdict(lambda:{"hit":0,"miss":0,"n":0,"sum_abs_error":0.0,"brier":0.0,"brier_n":0})
    featured={}
    for r in rows:
        key=tuple(r[x] for x in ("game","team","player","market","book","line","model","window"))
        if key in seen:raise ValueError("duplicate forecast row")
        seen.add(key)
        if r["book"] not in ("DraftKings","FanDuel"):raise ValueError("unexpected book")
        if r["window"]=="1PM":
            m=re.fullmatch(r"W9_1PM_LIVE_(\d{8})_(\d{6})\.\d+Z",r["forecast_lock"])
            if m is None or m[1]!="20261108" or m[2]>="180000":
                raise ValueError("1PM forecast not locked before kickoff")
        if r["window"]=="Madrid" and r["forecast_lock"]!="2026-11-08 09:08 ET":
            raise ValueError("Madrid lock mismatch")
        if r["window"]=="Late/SNF frozen overlay" and r["forecast_lock"]!="2026-11-08 08:23 ET":
            raise ValueError("late overlay lock mismatch")
        group=(r["window"],r["book"],r["model"],r["market"])
        stats=agg[group];counts[r["reg_grade"]]+=1
        if r["reg_grade"] in ("HIT","MISS"):
            a=float(r["reg_actual"]);line=float(r["line"])
            if a==line:raise ValueError("push labeled hit/miss")
            expected="HIT" if (r["call"]=="OVER" and a>line) or (r["call"]=="UNDER" and a<line) else "MISS"
            if expected!=r["reg_grade"]:raise ValueError("bad settlement: "+str(key))
            stats["hit" if expected=="HIT" else "miss"]+=1
        elif r["reg_grade"] not in ("DNP_UNGRADED","NO_CALL"):
            raise ValueError("unrecognized settlement")
        if r["mean"]!="" and r["reg_actual"]!="":
            err=float(r["reg_actual"])-float(r["mean"])
            if r["reg_error"]=="" or abs(err-float(r["reg_error"]))>0.055:
                raise ValueError("wrong signed forecast error: "+str(key))
            stats["n"]+=1;stats["sum_abs_error"]+=abs(err)
            if r["book"]=="DraftKings" and r["market"] in ("receiving_yards","passing_yards","rushing_yards") and r["model"] in ("season_empirical","frozen mean overlay"):
                k=r["game"];cand={"game":k,"player":r["player"],"market":r["market"],"line":r["line"],"mean":r["mean"],"reg_actual":r["reg_actual"],"error":round(err,2),"call":r["call"],"grade":r["reg_grade"]}
                if k not in featured or abs(cand["error"])>abs(featured[k]["error"]):featured[k]=cand
        if r["p_over"]!="" and r["p_under"]!="":
            p=float(r["p_over"]);q=float(r["p_under"])
            if not 0<=p<=1 or abs(p+q-1)>0.002:raise ValueError("invalid probability")
            if r["reg_grade"] in ("HIT","MISS"):
                y=int(float(r["reg_actual"])>float(r["line"]))
                stats["brier"]+=(p-y)**2;stats["brier_n"]+=1
    groups=[]
    for (window,book,model,market),v in sorted(agg.items()):
        n=v["hit"]+v["miss"]
        groups.append(dict(window=window,book=book,model=model,market=market,
            calls=n,hits=v["hit"],misses=v["miss"],
            hit_rate=round(v["hit"]/n,4) if n else None,
            mae=round(v["sum_abs_error"]/v["n"],3) if v["n"] else None,
            brier=round(v["brier"]/v["brier_n"],4) if v["brier_n"] else None))
    return dict(status="AUDIT_ARCHIVE_PASSED_RESEARCH_ONLY",games=sorted(EXPECTED),
        archived_forecast_rows=len(rows),archived_actual_rows=len(actual),
        locked_file_hashes_verified=len(lock["artifacts"]),
        grade_counts=dict(counts),market_level_metrics=groups,
        illustrative_largest_absolute_yardage_error_by_game=featured,
        caveats=["Mixed market MAE incomparable; score within market.",
        "Late/SNF mean overlay is NOT a trained main probability model.",
        "Cleveland at New Orleans OT excluded from regulation grading.",
        "Historical outputs do not establish bet returns or Lightning score.",
        "Pregame estimates are uncalibrated; do not promote."])

def check_live(fetch=None):
    if fetch is None:
        with urlopen(Request(URL,headers={"Accept":"application/json","User-Agent":"ResearchScoreboardAudit/1.0"}),timeout=20) as f:
            payload=json.load(f)
    else:payload=fetch()
    found={}
    for e in payload.get("events",[]):
        if not e.get("status",{}).get("type",{}).get("completed"):continue
        opponents={x.get("homeAway"):x for x in e.get("competitions",[{}])[0].get("competitors",[])}
        if "away" not in opponents or "home" not in opponents:continue
        away=opponents["away"]["team"]["abbreviation"];home=opponents["home"]["team"]["abbreviation"]
        game=f"{away}@{home}"
        if game=="LA@WAS":game="LAR@WAS"
        if game not in EXPECTED:continue
        if game in found:raise ValueError("duplicate game in live scoreboard")
        found[game]=dict(espn_id=e.get("id"),away=int(opponents["away"]["score"]),home=int(opponents["home"]["score"]))
    if set(found)!=set(EXPECTED):raise ValueError(f"live source incomplete: {len(found)}/13")
    for g,x in found.items():
        if (x["away"],x["home"])!=EXPECTED[g]:raise ValueError("live scoreboard conflicts with gamebook: "+g)
    return found

def main():
    result=audit()
    result["live_source_url"]=URL
    result["live_checked_utc"]=datetime.now(timezone.utc).isoformat()
    result["live_scoreboard"]=check_live()
    result["live_source_status"]="PASS_13_FINAL_SCORES"
    out=R/"WEEK9_20261108_RESCAN_20261109.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("AUDIT_RESULT=",json.dumps({k:result[k] for k in ("status","archived_forecast_rows","archived_actual_rows","locked_file_hashes_verified","live_source_status","grade_counts")},sort_keys=True))

if __name__=="__main__":main()
