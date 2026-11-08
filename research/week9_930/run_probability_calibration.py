#!/usr/bin/env python3
"""Threshold-specific forward diagnostic and equation decomposition for CIN-ATL.

All-team-game rows and positive-opportunity-only rows are carried separately.
The all-row case includes recorded zero-opportunity rows; the conditional case
estimates production given a positive market opportunity. Historical thresholds
are today's fixed lines, not historical sportsbook lines.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit
from scipy.stats import beta
ROOT=Path(__file__).resolve().parent
HIST=ROOT/'equation_player_history_w1_w8.csv'
LINES=ROOT/'book_lines_20261108_0908ET.csv'
CALOUT=ROOT/'PROBABILITY_CALIBRATION_20261108_0924ET.csv'
EQOUT=ROOT/'EQUATION_COMPONENTS_20261108_0924ET.csv'
REPORT=ROOT/'CALIBRATION_EQUATION_AUDIT.md'

def smooth(h,n): return (h+.5)/(n+1.0)
def fit_platt(p,y):
    z=logit(np.clip(np.asarray(p,float),1e-5,1-1e-5)); y=np.asarray(y,float)
    if len(y)<10 or len(np.unique(y))<2:return (0.0,1.0,'IDENTITY_TOO_FEW_OR_SINGLE_CLASS')
    def objective(ab):
        a,b=ab;q=np.clip(expit(a+b*z),1e-8,1-1e-8)
        return -np.mean(y*np.log(q)+(1-y)*np.log(1-q))+.01*(a*a+(b-1)*(b-1))
    res=minimize(objective,[0.,1.],method='L-BFGS-B',bounds=[(None,None),(0.0,5.0)])
    return float(res.x[0]),float(res.x[1]),'MONOTONE_PLATT_TRAINED_W5_W6' if res.success else 'PLATT_OPTIMIZER_WARNING'
def brier(y,p):return float(np.mean((np.asarray(y)-np.asarray(p))**2)) if len(y) else float('nan')
def ll(y,p):
    if not len(y):return float('nan')
    p=np.clip(p,1e-8,1-1e-8);y=np.asarray(y)
    return float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p))))
def interval(h,n):return beta.ppf([.05,.95],h+.5,n-h+.5)
def build_equations(h,lines):
    rows=[]
    for _,lr in lines.iterrows():
        p,team=lr.player,lr.team;g=h[(h.player_name==p)&(h.team==team)]
        recgames=g[g.market_key=='player_receptions']
        pgames=int(recgames.game_id.nunique())
        def total(key):
            q=g[g.market_key==key]
            return (float(q.value.sum()) if len(q) else np.nan,
                    float(q.opportunities.sum()) if len(q) else np.nan,
                    int(q.opportunities.gt(0).sum()) if len(q) else 0)
        attempts,_,pass_pos=total('player_pass_attempts');comps,_,_=total('player_pass_completions');passyds,_,_=total('player_pass_yds');td,_,_=total('player_pass_tds')
        carries,_,rush_pos=total('player_rush_attempts');rushyds,_,_=total('player_rush_yds')
        catches,targets,_=total('player_receptions');recvyds,_,_=total('player_reception_yds')
        apg=attempts/pgames if pgames and np.isfinite(attempts) else np.nan
        cr=comps/attempts if attempts and np.isfinite(comps) else np.nan
        ypc=passyds/comps if comps and np.isfinite(passyds) else np.nan
        tdpa=td/attempts if attempts and np.isfinite(td) else np.nan
        cpg=carries/pgames if pgames and np.isfinite(carries) else np.nan
        ypcarry=rushyds/carries if carries and np.isfinite(rushyds) else np.nan
        tpg=targets/pgames if pgames and np.isfinite(targets) else np.nan
        catch=(catches+.5)/(targets+1) if targets and np.isfinite(catches) else np.nan
        ypcatch=recvyds/catches if catches and np.isfinite(recvyds) else np.nan
        rows.append({'player':p,'team':team,'recorded_player_games':pgames,
          'pass_attempts_per_recorded_game':apg,'completion_rate_given_attempt':cr,'yards_per_completion':ypc,
          'equation_pass_yards_mean':apg*cr*ypc if all(np.isfinite(v) for v in [apg,cr,ypc]) else np.nan,
          'pass_td_rate_per_attempt':tdpa,'equation_pass_td_mean':apg*tdpa if np.isfinite(apg) and np.isfinite(tdpa) else np.nan,
          'rush_attempts_per_recorded_game':cpg,'yards_per_rush_attempt':ypcarry,
          'equation_rush_yards_mean':cpg*ypcarry if np.isfinite(cpg) and np.isfinite(ypcarry) else np.nan,
          'targets_per_recorded_game':tpg,'catch_rate_Jeffreys':catch,
          'equation_receptions_mean':tpg*catch if np.isfinite(tpg) and np.isfinite(catch) else np.nan,
          'yards_per_reception':ypcatch,
          'equation_receiving_yards_mean':tpg*catch*ypcatch if all(np.isfinite(v) for v in [tpg,catch,ypcatch]) else np.nan,
          'pass_attempt_denominator':attempts,'completion_denominator':comps,'target_denominator':targets,
          'catch_denominator':catches,'carry_denominator':carries,
          'positive_target_games':int(recgames.opportunities.gt(0).sum()),'positive_rush_games':rush_pos,'positive_pass_games':pass_pos})
    return pd.DataFrame(rows).drop_duplicates(['player','team'])
def main():
    h=pd.read_csv(HIST);h['value']=pd.to_numeric(h.value,errors='coerce');h['opportunities']=pd.to_numeric(h.opportunities,errors='coerce');h['week']=pd.to_numeric(h.week,errors='coerce')
    h=h[h.week.between(1,8)].copy(); lines=pd.read_csv(LINES).fillna('')
    events=[]
    for _,lr in lines.iterrows():
        if str(lr.dk_line).strip()=='':continue
        p,team,mk=lr.player,lr.team,lr.market_key;line=float(lr.dk_line)
        allseries=h[(h.player_name==p)&(h.team==team)&(h.market_key==mk)].sort_values(['week','game_id'])
        for scope,series in [('all_recorded_games',allseries),('positive_opportunity_only',allseries[allseries.opportunities>0])]:
            for _,test in series[series.week.between(5,8)].iterrows():
                past=series[series.week<test.week]
                if len(past)<2:continue
                vals=past.value.to_numpy(float);n=len(vals)
                events.append({'player':p,'market':lr.market,'market_key':mk,'line':line,'scope':scope,'test_week':int(test.week),'opportunity_in_test':bool(test.opportunities>0),'actual_value':float(test.value),'actual_over_today_line':int(test.value>line),'train_games':n,'season_p_raw':smooth(int(np.sum(vals>line)),n),'recent5_p_raw':smooth(int(np.sum(vals[-5:]>line)),min(5,n))})
    ev=pd.DataFrame(events);score=[];params={};apply={}
    for scope in ['all_recorded_games','positive_opportunity_only']:
      e=ev[ev.scope==scope]
      for model in ['season','recent5']:
        col=f'{model}_p_raw';tr=e[e.test_week.isin([5,6])];te=e[e.test_week.isin([7,8])]
        a,b,status=fit_platt(tr[col],tr.actual_over_today_line);params[(scope,model)]=(a,b,status)
        q=expit(a+b*logit(np.clip(te[col].to_numpy(float),1e-5,1-1e-5))) if len(te) else np.array([])
        raw=te[col].to_numpy(float);y=te.actual_over_today_line.to_numpy(float)
        improved=(b>.05 and brier(y,q)<brier(y,raw) and ll(y,q)<ll(y,raw))
        apply[(scope,model)]=improved
        score.append({'scope':scope,'model':model,'W5_W6_fit_events':len(tr),'W7_W8_test_events':len(te),'W7_W8_test_active_opportunity_events':int(te.opportunity_in_test.sum()),'intercept':a,'slope':b,'fit_status':status,'raw_Brier_W7_W8':brier(y,raw),'Platt_Brier_W7_W8':brier(y,q),'raw_logloss_W7_W8':ll(y,raw),'Platt_logloss_W7_W8':ll(y,q),'test_over_rate_W7_W8':float(np.mean(y)) if len(y) else np.nan,'correction_applied':improved})
    current=[]
    for _,lr in lines.iterrows():
        p,team,mk=lr.player,lr.team,lr.market_key
        allseries=h[(h.player_name==p)&(h.team==team)&(h.market_key==mk)].sort_values(['week','game_id'])
        for book,prefix in [('DraftKings','dk'),('FanDuel','fd')]:
          if str(lr.get(prefix+'_line','')).strip()=='':continue
          line=float(lr[f'{prefix}_line'])
          for scope,series in [('all_recorded_games',allseries),('positive_opportunity_only',allseries[allseries.opportunities>0])]:
            vals=series.value.to_numpy(float);n_all=len(vals);hits_all=int(np.sum(vals>line))
            for model in ['season','recent5']:
              sample=vals if model=='season' else vals[-5:]
              n=len(sample);hits=int(np.sum(sample>line))
              rawp=smooth(hits,n) if n else np.nan;lo,hi=interval(hits,n) if n else (np.nan,np.nan)
              a,b,status=params.get((scope,model),(0.,1.,'NO_CALIBRATOR'))
              pc=float(expit(a+b*logit(np.clip(rawp,1e-5,1-1e-5)))) if apply.get((scope,model),False) else rawp
              current.append({'player':p,'team':team,'market':lr.market,'market_key':mk,'book':book,'line':line,'scope':scope,'model':model,'games':n,'all_history_games':n_all,'positive_opportunity_games':int(series.opportunities.gt(0).sum()),'historical_over_count':hits,'historical_over_rate':hits/n if n else np.nan,'all_history_over_count':hits_all,'Jeffreys_p':rawp,'Jeffreys_90_low':float(lo),'Jeffreys_90_high':float(hi),'holdout_calibration_applied':bool(apply.get((scope,model),False)),'probability_after_holdout_rule':pc,'calibrator_intercept':a,'calibrator_slope':b,'status':'THRESHOLD_SPECIFIC_SMALL_SAMPLE; NOT HISTORICAL_MARKET_LINE_CALIBRATION'})
    pd.DataFrame(current).to_csv(CALOUT,index=False);ev.to_csv(ROOT/'walk_forward_threshold_events_W5_W8.csv',index=False)
    pd.DataFrame(score).to_csv(ROOT/'walk_forward_calibration_scores_W7_W8.csv',index=False)
    eq=build_equations(h,lines);eq.to_csv(EQOUT,index=False)
    report=['# Week 9 probability calibration and equation audit','', '**As of:** 2026-11-08 09:24 ET. The 09:08 pregame forecast and its 100k simulation are unchanged. This separate update uses the same pregame Weeks 1–8 source extract and all recorded zero-opportunity rows as a sensitivity.','', '## What was calibrated','', 'Historical prop lines are not in the repository. I therefore used each current DK line as a fixed threshold on earlier Weeks 5–8 outcomes, generating strictly prior-only probabilities for every test week. The correction was fitted on Weeks 5–6 and evaluated on untouched Weeks 7–8. It is pooled across the 31 DK player-market lines because per-market samples are too small. A correction is applied to the Week 9 estimate only if its slope remains positive and it improves both Brier score and log loss on W7–8.','', 'This is a threshold-specific forward diagnostic, not a backtest of the historical sportsbook market. Today’s lines are being applied to past games. Player/week observations overlap, the evaluation spans only four weeks, and the current line does not reflect each past game’s true market line.','', '## Walk-forward scores (Week 7–8 untouched)','', '| Sample definition | Probability model | W5–6 fit n | W7–8 test n | Active-opportunity test n | Raw Brier | Calibrated Brier | Raw log loss | Calibrated log loss | Platt slope | Applied? |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for r in score:
      report.append(f"| {r['scope']} | {r['model']} | {r['W5_W6_fit_events']} | {r['W7_W8_test_events']} | {r['W7_W8_test_active_opportunity_events']} | {r['raw_Brier_W7_W8']:.3f} | {r['Platt_Brier_W7_W8']:.3f} | {r['raw_logloss_W7_W8']:.3f} | {r['Platt_logloss_W7_W8']:.3f} | {r['slope']:.3f} | {'Yes' if r['correction_applied'] else 'No'} |")
    report += ['', 'If the fitted slope is zero, the calibrator collapses to a single pool-level rate and cannot distinguish player props; the procedure refuses to apply it as a player-specific probability. See the score table and CSV rather than treating such a constant as a pick signal.','', '## Equations used','', 'For receivers, the available marginal form is `E[receptions/game] = E[targets/game] × P(catch | target)` and `E[receiving yards/game] = E[targets/game] × P(catch | target) × E[yards | catch]`. The expected target count uses all recorded team-game rows, including zero-target rows; catch rate uses the Jeffreys Beta(0.5, 0.5) estimate. For quarterbacks, `E[completions] = E[attempts] × completion rate`, `E[passing yards] = E[attempts] × completion rate × yards/completion`, and `E[pass TD] = E[attempts] × TD/attempt`. For backs, `E[rush yards] = E[carries] × yards/carry`. Per-player factors and denominators are in `EQUATION_COMPONENTS_20261108_0924ET.csv`.','', 'These are marginal accounting decompositions; the current data has no exhaustive coverage context c, routes per dropback, charted defender assignment, target depth, play-level explosive catches, pressure-at-decision label, or designed-run/scramble split. Therefore it cannot fit the full explosive-completion equation, coverage adjustment, or scramble-trigger equation. Yardage probabilities still use observed player-game joint outcomes; no catch-level explosiveness is fabricated.','', '## Probability files','', '`PROBABILITY_CALIBRATION_20261108_0924ET.csv` reports DK and FD line-specific Jeffreys-smoothed rates, 90% intervals, and both scopes: all recorded games (zero opportunities included) and positive-opportunity-only (conditional role sample). Today’s inactives were checked, but the historical input does not distinguish inactive games from an active player receiving zero opportunities. The two scopes bracket that uncertainty. Re-run with `python run_probability_calibration.py`.','']
    REPORT.write_text('\n'.join(report),encoding='utf-8')
    print('Events',len(ev),'current probability rows',len(current),'equation players',len(eq))
    for r in score:print(r)
if __name__=='__main__':main()
