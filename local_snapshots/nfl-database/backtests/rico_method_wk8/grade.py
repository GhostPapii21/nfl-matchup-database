import pandas as pd, json, ast
c=pd.read_csv('picks_locked.csv'); cand=pd.read_csv('candidates.csv')
mn={'recyds':20,'rushyds':25,'rec':2.5,'passyds':150}
cand=cand[(cand.line>=cand.market.map(mn))&(cand.edge>=0.10)&(cand.h>=3)&(cand.price>-250)]
cand['score']=cand.edge*cand.h/cand.n
wx={'ATL@TB':'precip 80% / gust 30.6 mph','IND@JAX':'gust 20.6 mph','NE@MIA':'precip 65%'}
def stopped(r): return r.game in wx and r.side=='over' and r.market in('recyds','rec','passyds')
log=[];keep=[]
for g,grp in c.groupby('game'):
    used=set(grp.gsis)
    for _,r in grp.iterrows():
        if stopped(r):
            alt=cand[(cand.game==g)&~cand.gsis.isin(used)].sort_values('score',ascending=False)
            alt=alt[~alt.apply(stopped,axis=1)]
            rep=alt.iloc[0] if len(alt) else None
            log.append(f"- {g}: CUT {r.player} {r.market} {r.side} {r.line} (weather: {wx[g]}) -> "+(f"REPLACED by {rep.player} {rep.market} {rep.side} {rep.line} @ {int(rep.price)}" if rep is not None else "no replacement passing filters"))
            if rep is not None: used.add(rep.gsis); rr=rep.copy(); rr['src']='RECONSTRUCTED(repl)'; keep.append(rr)
        else: r=r.copy(); r['src']='RECONSTRUCTED'; keep.append(r)
k=pd.DataFrame(keep)
# actuals
p=pd.read_parquet('../../runs/2026-11-02_shared_src/play_by_play_2026.parquet'); p=p[p.week==8]
act={}
for col,idc,m in [('receiving_yards','receiver_player_id','recyds'),('complete_pass','receiver_player_id','rec'),('rushing_yards','rusher_player_id','rushyds'),('passing_yards','passer_player_id','passyds')]:
    s=p[p[idc].notna()].groupby(idc)[col].sum()
    for i,v in s.items(): act[(i,m)]=v
played=set(pd.concat([p.receiver_player_id,p.rusher_player_id,p.passer_player_id]).dropna())
# MNF from ESPN box
mnfbox={}
import glob
for f in glob.glob('../rulebook_replay_wk6_8/espn/*.json'):
    d=json.load(open(f))
    if 'header' not in d: continue
    comp=d['header']['competitions'][0]
    if not comp['date'].startswith('2026-11-03'): continue
    for t in d['boxscore'].get('players',[]):
        for st in t['statistics']:
            keys=st['keys']
            for a in st['athletes']:
                n=a['athlete']['displayName']; vals=dict(zip(keys,a['stats']))
                if st['name']=='receiving': mnfbox[(n,'rec')]=float(vals['receptions']); mnfbox[(n,'recyds')]=float(vals['receivingYards'])
                if st['name']=='rushing': mnfbox[(n,'rushyds')]=float(vals['rushingYards'])
                if st['name']=='passing': mnfbox[(n,'passyds')]=float(vals['passingYards'])
def actual(r):
    if r.game=='CHI@SEA': return mnfbox.get((r.player,r.market), 0.0 if any(x[0]==r.player for x in mnfbox) else None)
    if r.gsis not in played: return None
    return act.get((r.gsis,r.market),0.0)
k['actual']=k.apply(actual,axis=1)
def res(r):
    if pd.isna(r.actual): return 'VOID'
    if r.actual==r.line: return 'PUSH'
    return 'HIT' if (r.actual>r.line)==(r.side=='over') else 'MISS'
k['result']=k.apply(res,axis=1)
dec=lambda a: 1+a/100 if a>0 else 1+100/abs(a)
k['dec']=k.price.map(dec); k['pl10']=k.apply(lambda r: 10*(r.dec-1) if r.result=='HIT' else (-10 if r.result=='MISS' else 0),axis=1)
k.to_csv('graded_legs.csv',index=False)
open('hardstop_log.md','w').write("# Hard-stop log\n"+"\n".join(log)+"\n- Injuries: report_status Q for Kincaid, Ridley (both unders, kept; active per pbp/box). No pick listed Out/Doubtful. Inactive => VOID.\n")
print("\n".join(log)); print(k[['game','player','market','side','line','price','actual','result','pl10','src']].to_string())
