#!/usr/bin/env python3
"""Refresh 1 PM ET Week 9 DK/FD lines, empirical projections and 100k trials.

The 08:56 prospective lock is read-only. This writes a separately timestamped
research snapshot. Historical prop lines are not available, so calibration is
tested as a fixed-current-threshold walk-forward diagnostic and only applied
when predeclared minimum/evaluation rules pass.
"""
from __future__ import annotations
import csv, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
API = "https://fieldworklines.com/api/board?week=9&season=2026"
SOURCE = "https://fieldworklines.com/nfl/2026/week-9"
API_SOURCE = "https://fieldworklines.com/api/board?week=9&season=2026"
INACTIVE_SOURCE = "https://www.nfl.com/news/nfl-week-9-inactives-players-ruled-out-sunday-2026-season"
N_SIM = 100_000
MARKETS = {
    "player_pass_yds": ("passing_yards", "pass_yards_allowed_per_game", .50),
    "player_rush_yds": ("rushing_yards", "rushing_yards_allowed_per_game", .50),
    "player_reception_yds": ("receiving_yards", "pass_yards_allowed_per_game", .25),
    "player_receptions": ("receptions", "receptions_allowed_per_game", 1.00),
}
BOOKS = {"draftkings": "DraftKings", "fanduel": "FanDuel"}
INACTIVE_OFFENSE = {
    "Lil’Jordan Humphrey", "AJ Dillon", "George Pickens", "KaVontae Turpin",
    "Pharaoh Brown", "Will Mallory", "Tim Patrick", "Garrett Wilson",
    "Jacob Saylors", "Jordan Meeks", "Jalen Tolbert", "Jaylen Wright", "Justin Joly",
    "Deshaun Watson", "Taylen Green", "Zach Wilson", "CJ Donaldson",
    "Cam Skattebo", "Thomas Fidone II", "DeVonta Smith", "Dontayvion Wicks", "Britain Covey",
    "Ty Simpson", "Treylon Burks", "Athan Kaliakmanis",
}

def get_board():
    req = Request(API, headers={"User-Agent": "Mozilla/5.0 (research snapshot)"})
    with urlopen(req, timeout=25) as f:
        return json.loads(f.read().decode("utf-8"))

def week_num(game_id):
    m = re.search(r"_(\d{2})_", str(game_id))
    return int(m.group(1)) if m else 0

def brier(y,p):
    return float(np.mean((np.asarray(y,float)-np.asarray(p,float))**2)) if len(y) else float("nan")

def logloss(y,p):
    if not len(y): return float("nan")
    p=np.clip(np.asarray(p,float),1e-8,1-1e-8); y=np.asarray(y,float)
    return float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p))))

def fit_platt(p,y):
    p=np.clip(np.asarray(p,float),1e-5,1-1e-5); y=np.asarray(y,float)
    if len(y)<30 or len(np.unique(y))<2: return 0.,1.,"NOT_FIT_N_LT_30_OR_SINGLE_CLASS"
    z=logit(p)
    def obj(ab):
        q=np.clip(expit(ab[0]+ab[1]*z),1e-8,1-1e-8)
        return -np.mean(y*np.log(q)+(1-y)*np.log(1-q))+.01*(ab[0]**2+(ab[1]-1)**2)
    r=minimize(obj,[0.,1.],method="L-BFGS-B",bounds=[(None,None),(0.,5.)])
    return float(r.x[0]),float(r.x[1]),"FIT" if r.success else "FIT_WARNING"

board = get_board()
captured = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
asof = board.get("asOf")
if board.get("mode") != "live":
    raise RuntimeError(f"Board is not live mode: {board.get('mode')}")
players = [p for p in board["players"] if str(p.get("kickoff", "")).startswith("2026-11-08T18:00:")]
games = sorted({p.get("gameId") for p in players})

lines=[]
for p in players:
    for market_key,(market,_,_) in MARKETS.items():
        cell=p.get("cells",{}).get(market_key,{})
        for q in cell.get("quotes",[]):
            if q.get("book") not in BOOKS or q.get("line") is None or q.get("state")!="CURRENT":
                continue
            lines.append({
                "snapshot_id":"W9_1PM_LIVE_"+asof.replace(":","").replace("-","").replace("T","_").replace("Z","Z"),
                "retrieved_at_local":captured,"board_as_of_utc":asof,"quote_source_at_utc":q.get("sourceAt"),
                "quote_received_at_utc":q.get("receivedAt"),"quote_valid_until_utc":q.get("validUntil"),
                "player":p["name"],"team":p["team"],"opponent":p["opponent"],"game_id":p["gameId"],
                "kickoff_utc":p.get("kickoff"),"position":p.get("position"),"market":market,"market_key":market_key,
                "book":BOOKS[q["book"]],"line":float(q["line"]),"over_price":q.get("over"),"under_price":q.get("under"),
                "opening_line":q.get("opening"),"consensus_line":cell.get("value"),"book_coverage":cell.get("coverage"),
                "movement":cell.get("movement"),"source_url":SOURCE,"api_url":API_SOURCE,
            })
if not lines: raise RuntimeError("No current 1 PM DK/FD lines returned")
lines_df=pd.DataFrame(lines)
lines_path=OUT/f"WEEK9_1PM_DK_FD_LINES_{asof.replace(':','').replace('-','').replace('T','_').replace('Z','Z')}.csv"
lines_df.to_csv(lines_path,index=False)

hist=pd.read_csv(ROOT/"nfl_player_games.gz",compression="gzip")
hist=hist[(hist.sport=="nfl")&(hist.season==2026)&(hist.verified==True)].copy()
hist["week"]=hist.game_id.map(week_num)
hist["value"]=pd.to_numeric(hist.value,errors="coerce")
hist["opportunities"]=pd.to_numeric(hist.opportunities,errors="coerce")
hist=hist[hist.week.between(1,8)]
defense=pd.read_csv(ROOT/"w9_defense.csv").set_index("defense_team")

# Calibration diagnostic: use current line as a fixed threshold on W1-8 prior-only
# forecasts; current DK and FD quotes are deduplicated at the player/market/line level.
events=[]
for _,lr in lines_df.drop_duplicates(["player","team","market_key","line"]).iterrows():
    g=hist[(hist.player_name.str.casefold()==lr.player.casefold())&(hist.team==lr.team)&(hist.market_key==lr.market_key)].sort_values(["week","game_id"])
    for idx,test in g[g.week.between(5,8)].iterrows():
        past=g[g.week<test.week]
        if len(past)<2: continue
        v=past.value.to_numpy(float); y=int(float(test.value)>float(lr.line))
        for model, sample in [("season_empirical",v),("rolling5_empirical",v[-5:])]:
            p=(int(np.sum(sample>lr.line))+.5)/(len(sample)+1.)
            events.append({"player":lr.player,"team":lr.team,"market":lr.market,"line":lr.line,"model":model,
                           "test_week":int(test.week),"raw_probability":p,"actual_over":y})
ev=pd.DataFrame(events)
cal_rows=[];params={}
if not ev.empty:
    for market in sorted(ev.market.unique()):
        for model in ["season_empirical","rolling5_empirical"]:
            e=ev[(ev.market==market)&(ev.model==model)]
            tr=e[e.test_week.isin([5,6])]; te=e[e.test_week.isin([7,8])]
            a,b,status=fit_platt(tr.raw_probability,tr.actual_over)
            raw=te.raw_probability.to_numpy(float); y=te.actual_over.to_numpy(float)
            adj=expit(a+b*logit(np.clip(raw,1e-5,1-1e-5))) if len(te) else np.array([])
            passed=(len(tr)>=30 and len(te)>=30 and b>.05 and brier(y,adj)<brier(y,raw) and logloss(y,adj)<logloss(y,raw))
            params[(market,model)]=(a,b,bool(passed))
            cal_rows.append({"market":market,"model":model,"fit_n_W5_W6":len(tr),"test_n_W7_W8":len(te),
                "intercept":a,"slope":b,"raw_brier_W7_W8":brier(y,raw),"platt_brier_W7_W8":brier(y,adj),
                "raw_logloss_W7_W8":logloss(y,raw),"platt_logloss_W7_W8":logloss(y,adj),
                "correction_applied":passed,"status":"THRESHOLD_DIAGNOSTIC_NOT_HISTORICAL_PROP_LINE_BACKTEST" if not passed else "DIAGNOSTIC_CORRECTION_PASSED"})
cal=pd.DataFrame(cal_rows)
cal_path=OUT/"WEEK9_1PM_CALIBRATION_DIAGNOSTIC.csv"; cal.to_csv(cal_path,index=False)
ev.to_csv(OUT/"WEEK9_1PM_WALK_FORWARD_EVENTS.csv",index=False)

# Simulate three empirical candidate distributions using 100k draws for every quote.
team_names={"New York Giants":"NYG","Philadelphia Eagles":"PHI"}
market_to_hist={k:k for k in MARKETS}
alpha={k:v[2] for k,v in MARKETS.items()}
def metric(mk):return MARKETS[mk][1]
game_def=hist[hist.market_key.isin({v[1] for v in MARKETS.values()})&(hist.opportunities>0)].groupby(["game_id","week","opponent","market_key"],dropna=False).value.sum().reset_index()
sim=[]; skipped=[]
for _,lr in lines_df.iterrows():
    if lr.player in INACTIVE_OFFENSE:
        skipped.append({"player":lr.player,"market":lr.market,"book":lr.book,"line":lr.line,"reason":"OFFICIAL_INACTIVE"})
        continue
    g=hist[(hist.player_name.str.casefold()==lr.player.casefold())&(hist.team==lr.team)&(hist.market_key==lr.market_key)].sort_values(["week","game_id"])
    g=g[g.opportunities>0]
    vals=g.value.to_numpy(float)
    if len(vals)<2:
        skipped.append({"player":lr.player,"market":lr.market,"book":lr.book,"line":lr.line,"reason":"FEWER_THAN_TWO_POSITIVE_OPPORTUNITY_GAMES"});continue
    opp=str(lr.opponent); fac=1.
    if opp in defense.index:
        den=float(defense[metric(lr.market_key)].mean()); num=float(defense.loc[opp,metric(lr.market_key)])
        if den>0: fac=float(np.clip(num/den,.75,1.25))
    mult=1+alpha[lr.market_key]*(fac-1)
    distributions={"season_empirical":vals,"rolling5_empirical":vals[-5:],"opponent_shrunk_rolling5":np.rint(vals[-5:]*mult)}
    for model,vec in distributions.items():
        seed=int(hashlib.sha256(f"{lr.player}|{lr.market_key}|{lr.book}|{lr.line}|{model}|{asof}".encode()).hexdigest()[:8],16)
        sims=np.random.default_rng(seed).choice(vec,size=N_SIM,replace=True)
        rawp=float(np.mean(sims>lr.line))
        a,b,apply=params.get((lr.market,model),(0.,1.,False))
        cp=float(expit(a+b*logit(np.clip(rawp,1e-5,1-1e-5)))) if apply else rawp
        sim.append({
            "snapshot_id":lr.snapshot_id,"player":lr.player,"team":lr.team,"opponent":lr.opponent,"position":lr.position,
            "kickoff_utc":lr.kickoff_utc,"market":lr.market,"book":lr.book,"line":lr.line,"over_price":lr.over_price,"under_price":lr.under_price,
            "model":model,"prior_games":len(vals),"zero_stat_games":int(np.sum(vals==0)),"history_weeks":f"{int(g.week.min())}-{int(g.week.max())}",
            "draws":N_SIM,"mean_projection":round(float(np.mean(sims)),2),"q10":round(float(np.quantile(sims,.1)),2),
            "median":round(float(np.quantile(sims,.5)),2),"q90":round(float(np.quantile(sims,.9)),2),
            "p_over_raw":round(float(np.mean(sims>lr.line)),5),"p_push":round(float(np.mean(sims==lr.line)),5),
            "p_under_raw":round(float(np.mean(sims<lr.line)),5),
            "calibration_status":"THRESHOLD_DIAGNOSTIC_CORRECTION_APPLIED" if apply else "NOT_APPLIED_DIAGNOSTIC_FAILED_OR_INSUFFICIENT",
            "calibration_probability":round(cp if apply else rawp,5),"opponent_factor":round(fac,4),"adjustment_multiplier":round(mult,4),
            "status":"RAW_EMPIRICAL_BOOTSTRAP_NOT_BET_GRADEABLE",
        })
sim_df=pd.DataFrame(sim)
sim_path=OUT/"WEEK9_1PM_100K_SIMULATIONS.csv";sim_df.to_csv(sim_path,index=False)
pd.DataFrame(skipped).to_csv(OUT/"WEEK9_1PM_SIMULATION_SKIPS.csv",index=False)

lines_sha=hashlib.sha256(lines_path.read_bytes()).hexdigest()
sim_sha=hashlib.sha256(sim_path.read_bytes()).hexdigest()
metadata={"as_of_local":captured,"board_as_of_utc":asof,"mode":board.get("mode"),"scheduled_collection_utc":board.get("scheduleAt"),
 "games":games,"game_count":len(games),"players_with_1pm_kickoff":len(players),"DK_FD_quote_rows":len(lines_df),"sim_rows":len(sim_df),
 "simulations_per_row":N_SIM,"calibration_claim":False,"production_ready":False,
 "calibration_method":"W5-W6 fit / W7-W8 untouched diagnostic using today's line as threshold; not historical market line validation; correction applied only with >=30 fit and test rows, positive slope, and lower Brier plus log loss.",
 "calibration_pass_rows":int(cal.correction_applied.sum()) if not cal.empty else 0,
 "source_api":API_SOURCE,"source_page":SOURCE,"inactive_source":INACTIVE_SOURCE,"line_csv":lines_path.name,"line_csv_sha256":lines_sha,
 "simulation_csv":sim_path.name,"simulation_csv_sha256":sim_sha,"calibration_csv":cal_path.name,
 "limitations":["Only 1 PM ET games included.","Player-game export cannot distinguish a healthy active zero-opportunity game from an inactive game; positive-opportunity conditioning retains zero stat outcomes when opportunity exists.","Opponent adjustment is exploratory and capped at 0.75-1.25; no coverage/assignment/route/pressure decision-time data enter these draws.","These are empirical bootstrap frequencies, not independently calibrated prop-hit probabilities.","Quote times are per-book source and receipt timestamps; quotes expire at validUntil and must be rechecked after that time."]}
(OUT/"WEEK9_1PM_RUN_METADATA.json").write_text(json.dumps(metadata,indent=2)+"\n")

# Concise projection summary: one consensus threshold per player/market, all three model views.
cons=sim_df.merge(lines_df[["player","team","market","book","line","consensus_line","book_coverage"]],on=["player","team","market","book","line"],how="left")
summary=(cons.groupby(["player","team","opponent","position","market","model"],as_index=False)
         .agg(line=("line","median"),mean=("mean_projection","mean"),p_over=("p_over_raw","mean"),
              p_under=("p_under_raw","mean"),p_cal_diag=("calibration_probability","mean"),
              sample=("prior_games","min"),books=("book","nunique"),
              calibration_status=("calibration_status",lambda s:"APPLIED" if (s=="THRESHOLD_DIAGNOSTIC_CORRECTION_APPLIED").all() else "NOT_APPLIED")))
core_names={"Dak Prescott","CeeDee Lamb","George Pickens","Jake Ferguson","Jonathan Taylor","Javonte Williams",
"Jahmyr Gibbs","Amon-Ra St. Brown","Sam LaPorta","Jared Goff","Travis Kelce","Kenneth Walker III",
"Rashee Rice","Joe Milton III","Malik Nabers","Saquon Barkley","Dallas Goedert","Puka Nacua","Kyren Williams",
"Matthew Stafford","Chuba Hubbard","Jonah Coleman","Tetairoa McMillan","Chris Olave","Harold Fannin Jr."}
shown=summary[summary.player.isin(core_names)]
md=["# NFL Week 9 1 PM ET refreshed projections and simulations","",f"Captured {captured} (board as-of {asof}). Scope: the seven 1 PM ET games.",
"",f"Source lines: current DraftKings and FanDuel quotes from Fieldwork's market API, with per-book source/receipt/expiry timestamps. The page states it aggregates DK, FD, BetMGM and BetRivers; it uses the median of eligible standard lines. It is not a direct sportsbook connection.",
"",f"Quotes: {len(lines_df)}; simulation rows: {len(sim_df)}; 100,000 draws per quote/model. Input SHA-256: `{lines_sha}`; simulation SHA-256: `{sim_sha}`.",
"","## Calibration status","","Calibration remains **false**. This run tests a pooled Platt correction on Weeks 5-6 and holds out Weeks 7-8, using today's prices as fixed thresholds because historical book lines are unavailable. It applies only to market/model pairs with at least 30 fit and 30 test events, positive slope, and improved Brier and log loss. Passing pairs receive a separate `calibration_probability`; other pairs retain the raw probability. These tests are diagnostics, not a true historical-line calibration backtest.",
"","## Model definitions","","- Season empirical: bootstrap verified same-team Week 1-8 outcomes with positive opportunities, retaining zero-stat outcomes.","- Rolling five: same using the latest five eligible games.","- Opponent-shrunk rolling five: last-five outcomes multiplied by a capped opponent allowed-rate factor using existing team-level data; experimental only.","","The chance columns are raw bootstrap frequencies. Diagnostic-adjusted values are sensitivity outputs only, not accepted calibrated hit probabilities.","","## Current lines and projections","","Values below summarize current DK/FD quotes by median line. These projections come from Weeks 1-8 recorded player-game outcomes; use the downloadable CSV for each book and the three separate model distributions.","","| Player | Opp | Market | Current median line | Model | Mean | Raw over | Diagnostic-adjusted over* | Raw under | Eligible games |","|---|---|---|---:|---|---:|---:|---:|---:|---:|"]
for _,r in shown.sort_values(["player","market","model"]).iterrows():
    diag=f"{r.p_cal_diag:.1%}" if r.calibration_status=="APPLIED" else "—"
    md.append(f"| {r.player} | {r.opponent} | {r.market} | {r.line:g} | {r.model} | {r['mean']:.1f} | {r.p_over:.1%} | {diag} | {r.p_under:.1%} | {int(r['sample'])} |")
md += ["","## Official inactive impact to apply","","The NFL Week 9 official inactive report is the availability source. Material 1 PM names include DAL WR George Pickens and KaVontae Turpin; NYJ WR Garrett Wilson; DET RB Jacob Saylors; PHI WR DeVonta Smith and Dontayvion Wicks; NYG RB Cam Skattebo; CAR RB AJ Dillon; plus the other listed inactives. Offensive inactives are excluded from the simulation while their captured quotes remain in the line archive. Defensive inactives are matchup context and do not receive player offensive prop projections.",
"","## Limits and gates","","- Exact quote timestamps are per book and expire at the stored `validUntil`; recheck before any later decision.","- Historical input does not distinguish active zero opportunity from inactive or unavailable. A zero stat with positive opportunity remains in history; no-opportunity rows are omitted.","- Coverage, route participation, player assignment, pressure-at-decision, snap limits and weather are not included in these empirical distributions.","- `calibration=false` and `production_ready=false`; this new run does not change the 08:56 prospective lock or its baseline.","","## Files","",f"- Lines: `{lines_path.relative_to(ROOT)}`",f"- 100k simulation: `{sim_path.relative_to(ROOT)}`",f"- Calibration diagnostic: `{cal_path.relative_to(ROOT)}`",f"- Historical walk-forward events: `{(OUT/'WEEK9_1PM_WALK_FORWARD_EVENTS.csv').relative_to(ROOT)}`",f"- Metadata: `{(OUT/'WEEK9_1PM_RUN_METADATA.json').relative_to(ROOT)}`",""]
(OUT/"WEEK9_1PM_PROJECTIONS.md").write_text("\n".join(md),encoding="utf-8")
print(json.dumps({"captured":captured,"asof":asof,"players":len(players),"quotes":len(lines_df),"sim_rows":len(sim_df),
 "calibration_rows":len(cal),"calibration_pass_rows":metadata["calibration_pass_rows"],"skips":len(skipped),
 "line_file":str(lines_path),"simulation_file":str(sim_path),"report":str(OUT/"WEEK9_1PM_PROJECTIONS.md")},indent=2))
