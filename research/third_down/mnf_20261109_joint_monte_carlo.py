"""Research-only joint MNF BUF@MIN Week9 Monte Carlo.

N = 100,000 draws for EACH of three game scripts x three explicitly named
sensitivity methods (900,000 total game draws). Seed fixed for reproducibility.
NOT the production sportsbook-odds-bridge main model or actual trained Lightning
network. Their current Week9 files do not contain future BUF@MIN forecasts.
Do not call simulated clearance percentages calibrated true hit probabilities.

All pregame DK/FD lines come from separately frozen BetSharp quote record.
No late game-day inactives or outcome leakage. No production config/weights writes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np

ROOT=Path("research/third_down")
INPUT=ROOT/"BUF_MIN_W9_THREE_SCENARIO_PROP_RESEARCH_20261109.json"
QUOTES=ROOT/"BUF_MIN_DK_FD_QUOTES_20261109_1001ET.json"
OUT=ROOT/"BUF_MIN_W9_MC_100K_X_3_SCENARIOS_X_3_METHODS_20261109_1001ET.json"

N=100000
SEED=20261109
SCENARIOS=("A","B","C")
METHODS=("historical_shares","route_drive_opportunity","injury_protection_downside")
# Official Week1-8 Q scores from 7 games for BUF and MIN, plus opponents'
# defensive quarter allowances. Blend with 25% uniform quarter shape to
# moderate Minnesota's 7/7 Q4 record and the +22 point Week1 outlier.
BUF_Q_SCORED=np.array([5.142857,12.0,4.714286,11.0])
BUF_Q_ALLOWED=np.array([5.428571,6.285714,3.857143,10.285714])
MIN_Q_SCORED=np.array([3.142857,5.571429,2.428571,8.857143])
MIN_Q_ALLOWED=np.array([4.142857,3.714286,4.0,1.428571])
# The historical-v-opponent matchup fraction has a shrink to 25% per quarter.
def quarter_shares(team,method,scenario):
    if team=="BUF":
        q=(BUF_Q_SCORED+MIN_Q_ALLOWED)*.5
    else:
        q=(MIN_Q_SCORED+BUF_Q_ALLOWED)*.5
    q=q/q.sum()
    shrink={"historical_shares":.45,"route_drive_opportunity":.55,
            "injury_protection_downside":.65}[method]
    q=(1-shrink)*q+shrink*np.full(4,.25)
    if scenario=="C" and team=="MIN":
        q[3]+=0.02
        q=q/q.sum()
    if scenario=="A" and team=="MIN":
        # Fourth-quarter comeback possibility; allow modest extra late share
        # in trailing script, but no unverified defensive collapse.
        q[3]+=.015;q=q/q.sum()
    return q

def clip_int(x,low,high):
    return np.rint(np.clip(x,low,high)).astype(np.int32)

def lognormal_multiplier(rng,n,sd):
    return rng.lognormal(-sd**2/2,sd,size=n)

def draw_receptions(rng,attempts,targets_spec,sd=.03,concentration=40):
    """Joint per-attempt Dirichlet target competition; every target assigned once."""
    keys=list(targets_spec)
    weights=np.array([targets_spec[k][0] for k in keys],dtype=float)
    if (weights<0).any() or weights.sum()>=.96:
        raise ValueError("target shares must leave 4%+ others")
    weights=np.append(weights,1-weights.sum())
    group=rng.gamma(np.maximum(weights*concentration,.01),1,size=(len(attempts),len(weights)))
    group=group/group.sum(axis=1,keepdims=True)
    remain=attempts.copy()
    out={}
    rs=group.sum(axis=1)
    team_eff=rng.normal(0,sd,len(attempts))
    for i,k in enumerate(keys):
        if i==len(keys)-1:
            picks=rng.binomial(remain,np.clip(group[:,i]/np.maximum(rs,1.e-9),0,1))
        else:
            picks=rng.binomial(remain,np.clip(group[:,i]/np.maximum(rs,1.e-9),0,1))
        remain-=picks
        rs-=group[:,i]
        catch_rate=targets_spec[k][1]
        catch_prob=np.clip(catch_rate+team_eff+rng.normal(0,.027,len(attempts)),.13,.95)
        catches=rng.binomial(picks,catch_prob)
        mean_ypc,shape=targets_spec[k][2],targets_spec[k][3]
        # Gamma conditional on exact catch count; additive nonnegative yardage.
        yards=np.rint(rng.gamma(np.maximum(catches*shape,1.e-7),mean_ypc/shape)).astype(np.int32)
        yards[catches==0]=0
        out[k]={"targets":picks,"receptions":catches,"receiving_yards":yards}
    other_catches=rng.binomial(remain,.67)
    other_yards=np.rint(rng.gamma(np.maximum(other_catches*1.45,1.e-7),9.5/1.45)).astype(np.int32)
    other_yards[other_catches==0]=0
    return out,other_yards,remain

def run_rusher(rng,mean_att,ypc,n,sd=3.2,stochastic_factor=None):
    if stochastic_factor is None:
        stochastic_factor=np.ones(n)
    att=clip_int(rng.normal(mean_att,sd,n)*stochastic_factor,0,40)
    # YPC has explosive-play tail; negative rush plays approximated by 0
    # (causes upward bias, hence treat as noncalibrated sensitivity).
    yards=np.rint(rng.gamma(np.maximum(att*1.6,1.e-7),max(.5,ypc)/1.6)).astype(np.int32)
    yards[att==0]=0
    return att,yards

def draw_qscores(rng,meanpoints,shares,pace):
    """NFL-ish TD/FG event process: 7-point TD & 3-point FG, excluding safeties."""
    td=[];fg=[];scores=[]
    for q in range(4):
        exppts=meanpoints*shares[q]*pace
        ntd=rng.poisson(np.maximum(0,exppts*.72/7))
        nfg=rng.poisson(np.maximum(0,exppts*.28/3))
        td.append(ntd);fg.append(nfg);scores.append(ntd*7+nfg*3)
    return np.array(scores),np.sum(np.array(td),axis=0)

def give_tds(rng,tdcounts,players,probabilities):
    if abs(sum(probabilities)-1)>1e-6:
        raise ValueError("TD weights not normalized")
    n=len(tdcounts);count={p:np.zeros(n,dtype=np.int16) for p in players}
    cumulative=np.cumsum(probabilities)
    for j in range(int(np.max(tdcounts))):
        active=tdcounts>j
        draw=rng.random(n)
        for i,p in enumerate(players):
            sel=active & (draw<cumulative[i]) & (draw >= (cumulative[i-1] if i else 0))
            count[p]+=sel.astype(np.int16)
    return {p:count[p]>0 for p in players}

def american_to_prob(price):
    return (-price)/((-price)+100) if price<0 else 100/(price+100)

def summary(values):
    return {"median":float(np.median(values)),"mean":float(np.mean(values)),
            "p10":float(np.quantile(values,.1)),"p90":float(np.quantile(values,.9))}

def simulate_one(rng,script,method,config,quotes,n=N):
    base=config["scenarios"][[x["key"] for x in config["scenarios"]].index(script)]
    mi,bi=base["min"],base["buf"]
    i=SCENARIOS.index(script)
    # Shared pace and shared "Minnesota trailing more" latent affect both teams.
    pace=lognormal_multiplier(rng,n,.08)
    chase=rng.standard_normal(n)
    Wmean=mi["wentz"]["att"]
    Amean=bi["allen"]["att"]
    winjury=1 if method=="injury_protection_downside" else 0
    Wattempt=clip_int(rng.normal(Wmean+chase*2.8,4.5,n)*pace*(.965 if winjury else 1),8,62)
    Aattempt=clip_int(rng.normal(Amean-chase*.9,4.2,n)*pace,8,56)
    # Wentz's 3D sack/scramble stress is folded into variance and TE role.
    # No unsupported "pressure success rate" is inferred from QB-hit flags.
    hrate={"historical_shares":.178,"route_drive_opportunity":None,
           "injury_protection_downside":None}[method]
    if hrate is None:
        # Routes ~= dropbacks × route participation, targets ~= routes × .2255
        routes_rate={"A":.66,"B":.69,"C":.70}[script]
        if method=="injury_protection_downside":routes_rate=.55
        sacks={"A":3,"B":5,"C":6}[script]
        scrambles={"A":1,"B":1,"C":2}[script]
        hrate=np.clip((Wattempt+sacks+scrambles)*routes_rate*.2255/np.maximum(Wattempt,1),.06,.30)
    jshare={"A":.27,"B":.29,"C":.31}[script]
    addshare=.197
    jones_share={"A":.062,"B":.071,"C":.074}[script]
    if winjury:jones_share*=.77
    # NumPy scalar vs vector hock share normalized by per-row sum.
    # Avoid collective target shares >95% even under unusually low attempts.
    if isinstance(hrate,np.ndarray):
        hrate=np.minimum(hrate,.255)
        h_base=float(np.mean(hrate))
    else:h_base=hrate
    shares={"jefferson":(jshare,.70,12.5,1.3),
            "addison":(addshare,.622,12.5,1.02),
            "hockenson":(h_base,.784,8.724,2.0),
            "jones":(jones_share,.73,7.0,2.3)}
    # Conditional Hockenson share per QB dropbacks may vary with attempts;
    # approximate with scalar mean within method; actual draw includes Dirichlet
    # per-game variation, avoid an invented per-blitz QB/TE assignment.
    minreceivers,MINother,_=draw_receptions(rng,Wattempt,shares,concentration=38)
    minPass=sum(x["receiving_yards"] for x in minreceivers.values())+MINother
    # BUF roles: explicitly inferred from each game script's prior projections.
    br={}
    probs={"shakir":.80,"moore":.65,"coleman":.67,"kincaid":.76,"cook":.74}
    ypcs={"shakir":10.3,"moore":13.5,"coleman":12.5,"kincaid":10.4,"cook":8.0}
    shapes={"shakir":1.8,"moore":1.12,"coleman":1.08,"kincaid":1.65,"cook":2.0}
    for name in probs:
        expected=bi[name]["rec"]
        share=(expected/probs[name])/Amean
        if winjury and name in ("moore","coleman","kincaid"):
            share*= {"moore":.82,"coleman":.88,"kincaid":.90}[name]
        br[name]=(share,probs[name],ypcs[name],shapes[name])
    bufrec,BUFother,_=draw_receptions(rng,Aattempt,br,concentration=38)
    bufPass=sum(x["receiving_yards"] for x in bufrec.values())+BUFother
    # Rushing attempts in Minnesota are correlated by role; any Jones
    # participation cap shifts some early carries to Mason, not guaranteed.
    jMean={"A":7,"B":8,"C":5}[script]
    mMean={"A":12,"B":12.5,"C":8.3}[script]
    jbackfac=np.ones(n)
    if method=="injury_protection_downside":
        jbackfac*=.80
        mMean+=1.3
    JonesAtt,JonesRush=run_rusher(rng,jMean,3.7,n,sd=2.6,stochastic_factor=jbackfac)
    MasonAtt,MasonRush=run_rusher(rng,mMean,3.7,n,sd=3.4)
    # Wentz sacks + passing stats are game-level rates, not just third downs.
    # No new probability is derived from his 2025 20%-of-3D sack sample.
    CookAtt,CookRush=run_rusher(rng,bi["cook"]["rushAtt"],
                               bi["cook"]["rushYds"]/bi["cook"]["rushAtt"]-(.30 if winjury else 0),
                               n,sd=3.5,stochastic_factor=np.clip(1+.04*chase,.85,1.15))
    AllenRatt,AllenRush=run_rusher(rng,{"A":6.4,"B":7.0,"C":6.2}[script],
                                  {"A":4.2,"B":4.7,"C":4.2}[script],
                                  n,sd=2.6)
    # Team score simulation based on dated seven-game Q distributions,
    # shrunk toward equal quarter shape, with scenario mean score.
    bufq,bufTD=draw_qscores(rng,base["score"]["BUF"],quarter_shares("BUF",method,script),pace)
    minq,minTD=draw_qscores(rng,base["score"]["MIN"],quarter_shares("MIN",method,script),pace)
    BUFscore=bufq.sum(axis=0);MINscore=minq.sum(axis=0)
    # Assign touchdowns to actual scoring players only. A passing TD is NOT
    # an anytime-TD win for the passer. These weights are SUBJECIVE and not
    # learned or derived from book prices.
    bp=["allen","cook","shakir","moore","coleman","kincaid","other"]
    bweights=[.25,.30,.075,.10,.06,.10,.115]
    mp=["jefferson","hockenson","addison","jones","mason","wentz","other"]
    mweights=[.29,.17,.13,.13,.23,.015,.035]
    if script=="C":
        mweights=[.31,.19,.15,.09,.19,.015,.055]
    if script=="A":
        bweights=[.24,.33,.075,.09,.05,.095,.12]
    bufTDs=give_tds(rng,bufTD,bp,bweights)
    minTDs=give_tds(rng,minTD,mp,mweights)
    # Retain conditional player-outcome identity & grade bookmaker lines.
    player={
        ("MIN","Carson Wentz","passing_yards"):minPass,
        ("MIN","Carson Wentz","pass_attempts"):Wattempt,
        ("MIN","Justin Jefferson","receptions"):minreceivers["jefferson"]["receptions"],
        ("MIN","Justin Jefferson","receiving_yards"):minreceivers["jefferson"]["receiving_yards"],
        ("MIN","T.J. Hockenson","receptions"):minreceivers["hockenson"]["receptions"],
        ("MIN","T.J. Hockenson","receiving_yards"):minreceivers["hockenson"]["receiving_yards"],
        ("MIN","Jordan Addison","receptions"):minreceivers["addison"]["receptions"],
        ("MIN","Jordan Addison","receiving_yards"):minreceivers["addison"]["receiving_yards"],
        ("MIN","Aaron Jones","receptions"):minreceivers["jones"]["receptions"],
        ("MIN","Aaron Jones","receiving_yards"):minreceivers["jones"]["receiving_yards"],
        ("MIN","Aaron Jones","rushing_yards"):JonesRush,
        ("MIN","Aaron Jones","rush_receiving_yards"):JonesRush+minreceivers["jones"]["receiving_yards"],
        ("MIN","Jordan Mason","rushing_yards"):MasonRush,
        ("BUF","Josh Allen","passing_yards"):bufPass,
        ("BUF","Josh Allen","rushing_yards"):AllenRush,
        ("BUF","Khalil Shakir","receptions"):bufrec["shakir"]["receptions"],
        ("BUF","Khalil Shakir","receiving_yards"):bufrec["shakir"]["receiving_yards"],
        ("BUF","Keon Coleman","receptions"):bufrec["coleman"]["receptions"],
        ("BUF","Keon Coleman","receiving_yards"):bufrec["coleman"]["receiving_yards"],
        ("BUF","James Cook","rush_attempts"):CookAtt,
        ("BUF","James Cook","rushing_yards"):CookRush,
        ("BUF","James Cook","receptions"):bufrec["cook"]["receptions"],
        ("BUF","James Cook","receiving_yards"):bufrec["cook"]["receiving_yards"],
        ("BUF","James Cook","rush_receiving_yards"):CookRush+bufrec["cook"]["receiving_yards"],
        ("BUF","D.J. Moore","receptions"):bufrec["moore"]["receptions"],
        ("BUF","D.J. Moore","receiving_yards"):bufrec["moore"]["receiving_yards"],
        ("BUF","Dalton Kincaid","receptions"):bufrec["kincaid"]["receptions"],
        ("BUF","Dalton Kincaid","receiving_yards"):bufrec["kincaid"]["receiving_yards"],
    }
    if len(player)!=len(quotes["markets"]):
        raise ValueError("some market prop lacks a 100k simulated outcome")
    if np.any(minPass<minreceivers["jefferson"]["receiving_yards"]):
        raise ValueError("QB passing yard total less than Jefferson receiving yard")
    if np.any(bufPass<bufrec["shakir"]["receiving_yards"]):
        raise ValueError("QB passing yard total less than Shakir receiving yard")
    outprops=[]
    for record in quotes["markets"]:
        team,name,market=record["team"],record["player"],record["market"]
        arr=player[(team,name,market)]
        datum={"team":team,"player":name,"market":market,"outcome":summary(arr)}
        for book in ("DK","FD"):
            line=record[book]
            if line is None:
                datum[book]=None
                continue
            threshold=line["line"]
            over=(arr>threshold);under=(arr<threshold);push=(arr==threshold)
            pim=american_to_prob(line["over"]);uim=american_to_prob(line["under"])
            novig=pim/(pim+uim)
            datum[book]={"line":threshold,"over_odds":line["over"],
                "under_odds":line["under"],
                "sim_over_pct":round(100*float(over.mean()),2),
                "sim_under_pct":round(100*float(under.mean()),2),
                "sim_push_pct":round(100*float(push.mean()),2),
                "market_novig_over_pct":round(100*novig,2),
                "uncalibrated_disagreement_pp":round(100*(float(over.mean())-novig),2)}
        outprops.append(datum)
    qstats={}
    for qi in range(4):
        b=bufq[qi];m=minq[qi];winning=b>m;losing=b<m;tie=b==m
        # Market quarter ML settlement for tie is not verified.
        qstats[f"Q{qi+1}"]={"BUF_win_pct":round(float(winning.mean())*100,2),
                "MIN_win_pct":round(float(losing.mean())*100,2),
                "tie_pct":round(float(tie.mean())*100,2),
                "BUF_win_if_not_tied_pct":round(float(winning.sum()/(winning.sum()+losing.sum()))*100,2),
                "BUF_points":summary(b),"MIN_points":summary(m)}
    total={
        "BUF_score":summary(BUFscore),
        "MIN_score":summary(MINscore),
        "total_points":summary(BUFscore+MINscore),
        "BUF_win_pct":round(100*float(np.mean(BUFscore>MINscore)),2),
        "MIN_win_pct":round(100*float(np.mean(BUFscore<MINscore)),2),
        "tie_after_regulation_pct":round(100*float(np.mean(BUFscore==MINscore)),2),
        "over_44_5_pct":round(100*float(np.mean(BUFscore+MINscore>44.5)),2),
        "first_half_BUF_win_pct":round(100*float(np.mean(bufq[:2].sum(axis=0)>minq[:2].sum(axis=0))),2),
        "first_half_MIN_win_pct":round(100*float(np.mean(bufq[:2].sum(axis=0)<minq[:2].sum(axis=0))),2),
        "second_half_BUF_win_pct":round(100*float(np.mean(bufq[2:].sum(axis=0)>minq[2:].sum(axis=0))),2),
        "second_half_MIN_win_pct":round(100*float(np.mean(bufq[2:].sum(axis=0)<minq[2:].sum(axis=0))),2),
    }
    atd=[]
    for rec in quotes["anytimeTD"]:
        key=rec["player"]
        mapn={
          "Josh Allen":"allen","James Cook":"cook","D.J. Moore":"moore",
          "Khalil Shakir":"shakir","Keon Coleman":"coleman",
          "Dalton Kincaid":"kincaid","Dawson Knox":"other",
          "Justin Jefferson":"jefferson","T.J. Hockenson":"hockenson",
          "Jordan Addison":"addison","Aaron Jones":"jones",
          "Jordan Mason":"mason","Carson Wentz":"wentz"
        }
        k=mapn[key]
        # Dawson Knox is grouped into 'other' with other BUF scorers;
        # DO NOT misstate combined group as his individual probability.
        simtd=None if key=="Dawson Knox" else (bufTDs if rec["team"]=="BUF" else minTDs)[k]
        atd.append({"player":key,"team":rec["team"],"DK_price":rec["DK"],"FD_price":rec["FD"],
                    "sim_anytime_td_pct":None if simtd is None else round(100*float(simtd.mean()),2),
                    "status":"other receiver share not Knox individually" if key=="Dawson Knox" else "assumed scoring share, uncalibrated"})
    # "Jones 25+" alternate result has NO verified DK/FD price.
    j25=JonesRush+minreceivers["jones"]["receiving_yards"]
    result={"scenario":script,"method":method,"trials":n,
            "scenario_assumptions":{"MIN_Wentz_expected_attempts":Wmean,
                "BUF_Allen_expected_attempts":Amean,
                "BUF_Cook_expected_carries":bi["cook"]["rushAtt"],
                "illustrative_score":base["score"]},
            "player_props":outprops,"quarters":qstats,"game":total,"anytime_td":atd,
            "unquoted_alt":{"Aaron_Jones_25plus_rush_receive_pct":round(float(np.mean(j25>=25))*100,2),
                "quoted_at_DK_FD":False}}
    return result

def run(seed=SEED,n=N):
    config=json.loads(INPUT.read_text(encoding="utf-8"))
    quotes=json.loads(QUOTES.read_text(encoding="utf-8"))
    if len(quotes["markets"])!=28:
        raise ValueError("quote snapshot length changed; explicitly re-audit it")
    rng=np.random.default_rng(seed)
    rows=[]
    for scenario in SCENARIOS:
        for method in METHODS:
            rows.append(simulate_one(rng,scenario,method,config,quotes,n))
    report={"status":"COMPLETED_RESEARCH_ONLY_NO_VALIDATED_PROBABILITIES",
            "game":"BUF at MIN 2026-11-09 pregame",
            "quote_snapshot":str(QUOTES),"source_display_updated_ET":"2026-11-09 10:01 ET",
            "trials_per_scenario_method":n,"total_trials":len(rows)*n,"seed":seed,
            "methods":{
              "historical_shares":"Current Wentz historic target-share and original opportunity scenarios; not trained sportsbook main model",
              "route_drive_opportunity":"Hockenson route × targets-per-route and correlated drives/targets plus recent quarter tendencies; not trained Lightning model",
              "injury_protection_downside":"Explicit non-fitted workload haircuts for recent injuries and extra TE blocking; pessimistic sensitivity, not medical prognosis",
            },
            "game_scripts":{
              "A":"Buffalo controls clock; Wentz 24 attempts baseline",
              "B":"One-score competitive; Wentz 30 attempts baseline",
              "C":"Minnesota chasing while Buffalo uses Cook more; Wentz 38 attempts baseline",
            },
            "not_run_actual_main_or_lightning":True,
            "warnings":[
              "The 3 methods are transparent independently parameterized research sensitivities, NOT the existing production main or trained Lightning models.",
              "Conditional hit rates are from assumed distributions; they are not out-of-sample-calibrated win probabilities, profitable edges or fair bet prices.",
              "No weights assigned among the three game scripts, so don't average scenario percentages into a betting recommendation.",
              "Team score simulation uses a coarse Poisson touchdown/field-goal process; does not model exact drive PBP, safeties, two-points, OT or quarterback/team-scoring correlation.",
              "Quarter ML tie settlement unverified. All period results report three-way win/tie/loss separately.",
              "Receiving target shares in the same game compete and Wentz/Allen passing yards reconcile to their simulated catches; TD scoring process is not calibrated to player receptions.",
              "Touchdown scorer allocation uses explicitly assumed positional shares, not opponent charted goal-line play-by-play, so avoid confident TD bets.",
              "J. Mason and Jones share role opportunity but carry volume is only partially correlated; Dallas competition remains a risk.",
              "Player rushing simulation approximates positive aggregate gains and ignores negative runs/kneels, which may bias yardage slightly upward.",
              "Book odds are from a 10:01 ET third-party aggregator snapshot, not directly authenticated live DK/FD prices; re-verify before wagering.",
              "Official final game-day inactives are not known at 10 AM ET; no medical probabilities estimated.",
              "No production model, NFL-13 assessment, baseline, DB or config changes.",
            ],"runs":rows}
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--trials",type=int,default=N)
    ap.add_argument("--seed",type=int,default=SEED)
    args=ap.parse_args()
    if args.trials<1 or args.trials>1000000:
        raise ValueError("1 to 1,000,000 trials per scenario-method")
    result=run(args.seed,args.trials)
    OUT.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    for row in result["runs"]:
        k={(p["player"],p["market"]):p for p in row["player_props"]}
        q=row["quarters"]
        print(f"{row['scenario']} {row['method']} trials={row['trials']} BUF_game={row['game']['BUF_win_pct']}% "
              f"Jeff_rec_med={k[('Justin Jefferson','receptions')]['outcome']['median']} "
              f"Hock_rec_med={k[('T.J. Hockenson','receptions')]['outcome']['median']} "
              f"Cook_rush_med={k[('James Cook','rushing_yards')]['outcome']['median']} "
              f"Q2_BUF={q['Q2']['BUF_win_pct']}% Q4_MIN={q['Q4']['MIN_win_pct']}%")
    print(f"FINISHED_REPORT={OUT} total_trials={result['total_trials']}")
if __name__=="__main__":
    main()
