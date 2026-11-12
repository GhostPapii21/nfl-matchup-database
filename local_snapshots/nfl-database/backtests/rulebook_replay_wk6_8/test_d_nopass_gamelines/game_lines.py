"""Test D step 1: inventory of SAVED pre-kickoff game-line prices (no network) + game-line legs where a pre-kickoff
team-level model exists. Gate logic applied where it applies: one leg per game-market, all 3 model p >= .45,
model medians clear the line, raw edge (avg p - no-vig) >= +3 (NOSHRINK), N3 for half/quarter spreads."""
import json,glob,os,datetime as dt,collections,pandas as pd
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT='/workspace/nfl-database'
EV=json.load(open('../current_rules_wk6_8/raw/events.json'))
ev={e['id']:e for e in EV.values() if '2026-10-15'<=e['commence_time']<='2026-11-03T06'}
inv=[]
seen=collections.defaultdict(collections.Counter)
for f in glob.glob('raw/game_*.json'):
    d=json.load(open(f))
    for e in d['data']:
        if e['id'] not in ev: continue
        for b in e['bookmakers']:
            for m in b['markets']: seen[e['id']][m['key']]+=1
# MNF saved Nov 2 7:43 AM pull (pre-kickoff)
mnf=pd.read_csv(f'{ROOT}/runs/2026-11-02_CHI@SEA_r2/total/odds_t0743.csv')
HALFQ=['spreads_h1','totals_h1','h2h_h1','spreads_h2','totals_h2','spreads_q1','totals_q1','spreads_q2','totals_q2','spreads_q3','totals_q3','spreads_q4','totals_q4']
for i,e in sorted(ev.items(),key=lambda x:x[1]['commence_time']):
    mn=e['commence_time'].startswith('2026-11-03')
    keys=set(seen[i])|(set(mnf.market) if mn else set())
    inv.append(dict(event=i,game=f"{e['away_team']}@{e['home_team']}",commence_utc=e['commence_time'],
        h2h='h2h' in keys,spreads='spreads' in keys,totals='totals' in keys,n_books_spreads=seen[i]['spreads'],
        alt_spreads_totals='alternate_spreads' in keys,team_totals='team_totals' in keys,
        half_quarter_saved=any(k in keys for k in HALFQ),
        team_model=('MNF total_sim.py (game total + team totals, pre-kick 7:45 AM ET Nov 2)' if mn else 'NONE')))
I=pd.DataFrame(inv); I.to_csv('test_d_nopass_gamelines/gameline_inventory.csv',index=False)
print(I[['h2h','spreads','totals','half_quarter_saved']].sum().to_dict(),len(I))
# game-line candidates: only MNF has a team-level model
T=json.load(open(f'{ROOT}/runs/2026-11-02_CHI@SEA_r2/total/raw_total_sims.json'))['totals']
E=json.load(open('espn/401873036.json')); sc={c['team']['abbreviation']:int(c['score']) for c in E['header']['competitions'][0]['competitors']}
tot=sum(sc.values())
RUN9='/workspace/nfl-database/backtests/rulebook_replay_wk6_8/runs/wk9_CHI_SEA'
dec=lambda a:1+(a/100 if a>0 else 100/-a)
C=[]
for r in T:
    if r['market']!='Game total': continue
    p=[r['mc'],r['bias'],r['gr']]; edge=round((sum(p)/3-r['nv'])*100,1)
    passed=bool(r['clears']) and min(p)>=.45 and edge>=3
    res='push' if tot==r['line'] else ('win' if (tot>r['line'])==(r['side']=='Over') else 'loss')
    C.append(dict(week=9,game='CHI@SEA',run=RUN9,
        leg=f"CHI@SEA total {r['side'].lower()} {r['line']}",player='GAME CHI@SEA',gsis='GAME_CHI_SEA_total',market='game_total',side=r['side'].lower(),
        line=r['line'],price=r['fd'],no_vig=r['nv'],p_mc=r['mc'],p_bias=r['bias'],p_gr=r['gr'],raw_edge=edge/100,medians=r['med'],
        model_clears=r['clears'],gate_like_pass=passed,actual=tot,result=res,profit_single=(10*(dec(r['fd'])-1) if res=='win' else -10 if res=='loss' else 0.0)))
C=pd.DataFrame(C)
# one leg per game-market: highest raw edge among passers (same tie rule as player pool)
C['passed']=False
ps=C[C.gate_like_pass].sort_values(['raw_edge','price'],ascending=[False,True])
if len(ps): C.loc[ps.index[0],'passed']=True
C.to_csv('test_d_nopass_gamelines/game_candidates.csv',index=False)
print(C[['leg','price','raw_edge','gate_like_pass','passed','result']].to_string())
C[C.passed].assign(type='GAME',rung='main',scheme_edge_flag=False,depth=False,door_block='').to_csv('test_d_nopass_gamelines/game_legs.csv',index=False)
