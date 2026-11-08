#!/usr/bin/env python3
"""Reproducible 100,000-draw Bengals-Falcons Week 9 market projection.

Uses only frozen game-specific inputs in this directory. Each player's historical
values are bootstrapped by opportunity games with positive recorded opportunity;
zero production in such games remains in the sample. Outputs are raw empirical
frequencies, not calibrated probabilities. No live source calls are made.
"""
import csv, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
HISTORY=ROOT/'player_game_history_w1_w8.csv'
LINES=ROOT/'book_lines_20261108_0908ET.csv'
DEFENSE=ROOT/'defense_inputs_pre_game_w1_w8.csv'
OUT=ROOT/'simulation_100k_20261108_0908ET.csv'
N=100_000
ALPHA={
 'player_pass_yds':.50,'player_pass_completions':.50,'player_pass_tds':.50,
 'player_reception_yds':.25,'player_receptions':1.0,
 'player_rush_yds':.50,'player_rush_attempts':.50,
}
DEF_METRIC={
 'player_pass_yds':'pass_yards_allowed_per_game',
 'player_pass_completions':'pass_attempts_allowed_per_game',
 'player_pass_tds':'pass_yards_allowed_per_game',
 'player_reception_yds':'pass_yards_allowed_per_game',
 'player_receptions':'receptions_allowed_per_game',
 'player_rush_yds':'rushing_yards_allowed_per_game',
 'player_rush_attempts':'rushing_yards_allowed_per_game',
}
TEAM={'Cincinnati Bengals':'CIN','Atlanta Falcons':'ATL'}

def seed_for(player, market, book, model):
    return int(hashlib.sha256(f'W9-930-20261108|{player}|{market}|{book}|{model}'.encode()).hexdigest()[:8],16)

def main():
    h=pd.read_csv(HISTORY)
    h['value']=pd.to_numeric(h.value,errors='coerce')
    h['opportunities']=pd.to_numeric(h.opportunities,errors='coerce')
    h['week']=pd.to_numeric(h.week,errors='coerce')
    h=h[(h.verified.astype(str).str.lower().isin(['true','1'])) & h.week.between(1,8)].copy()
    d=pd.read_csv(DEFENSE).set_index('defense_team')
    lines=pd.read_csv(LINES).fillna('')
    rows=[]
    for _,line_row in lines.iterrows():
        player=str(line_row.player); team=str(line_row.team); market=str(line_row.market_key)
        base=h[(h.player_name==player)&(h.market_key==market)&(h.team==team)&(h.opportunities>0)]
        base=base.sort_values(['week','game_id'])
        vals=base.value.to_numpy(dtype=float)
        if len(vals)<2:
            for book,prefix in [('DraftKings','dk'),('FanDuel','fd')]:
                raw=line_row.get(prefix+'_line','')
                if str(raw).strip()=='': continue
                rows.append({'player':player,'team':team,'market':line_row.market,'market_key':market,'book':book,'line':float(raw),'prior_games':len(vals),'status':'INSUFFICIENT_HISTORY'})
            continue
        defense_team='ATL' if team=='CIN' else 'CIN'
        metric=DEF_METRIC[market]
        league=pd.to_numeric(d[metric],errors='coerce').mean()
        opponent=float(d.loc[defense_team,metric]) if defense_team in d.index else np.nan
        factor=float(np.clip(opponent/league,.75,1.25)) if pd.notna(league) and league else 1.0
        alpha=ALPHA[market]
        multiplier=1+alpha*(factor-1)
        vecs={'season_empirical':vals,'rolling5_empirical':vals[-5:],
              'opponent_shrunk_rolling5':np.rint(vals[-5:]*multiplier)}
        for book,prefix in [('DraftKings','dk'),('FanDuel','fd')]:
            raw=line_row.get(prefix+'_line','')
            if str(raw).strip()=='': continue
            line=float(raw)
            for model,vec in vecs.items():
                draws=np.random.default_rng(seed_for(player,market,book,model)).choice(vec,size=N,replace=True)
                rows.append({
                    'player':player,'team':team,'market':line_row.market,'market_key':market,'book':book,
                    'line':line,'over_price':line_row.get(prefix+'_over',''),'under_price':line_row.get(prefix+'_under',''),
                    'prior_games':len(vals),'zero_stat_games_with_opportunity':int(np.sum(vals==0)),
                    'historical_hits_at_current_line':int(np.sum(vals>line)),
                    'historical_pushes_at_current_line':int(np.sum(vals==line)),
                    'historical_misses_at_current_line':int(np.sum(vals<line)),
                    'historical_hit_rate_at_current_line':round(float(np.mean(vals>line)),5),
                    'history_min_week':int(base.week.min()),'history_max_week':int(base.week.max()),
                    'simulations':N,'seed':seed_for(player,market,book,model),'model':model,
                    'mean':round(float(draws.mean()),3),'q10':round(float(np.quantile(draws,.10)),3),
                    'median':round(float(np.quantile(draws,.50)),3),'q90':round(float(np.quantile(draws,.90)),3),
                    'p_over':round(float(np.mean(draws>line)),5),'p_push':round(float(np.mean(draws==line)),5),
                    'p_under':round(float(np.mean(draws<line)),5),'opponent_allowed_factor_capped':round(factor,5),
                    'market_alpha':alpha,'opponent_adjustment_multiplier':round(multiplier,5),
                    'status':'RAW_BOOTSTRAP_FREQUENCY_NOT_CALIBRATED; conditional on positive historical opportunity'
                })
    pd.DataFrame(rows).to_csv(OUT,index=False)
    print(f'Wrote {len(rows)} rows ({sum(1 for r in rows if r.get("simulations")==N)} × {N:,} draws) to {OUT.name}')

if __name__=='__main__': main()
