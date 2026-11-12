"""Stage B. Run only after lock commit. Reuses v4 grade()/summary() (import, unchanged)."""
import sys,math,pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parent/'v4'))
import grade as g4
pb=pd.read_parquet(ROOT.parents[2]/'runs/2026-11-02_shared_src/play_by_play_2026.parquet')
pb=pb[(pb.season_type=='REG')&(pb.two_point_attempt!=1)&pb.play_type.isin(['run','pass'])]
P=pd.read_csv(ROOT/'locked_picks.csv')
q=pd.concat([pd.read_csv(ROOT.parent/'v4'/'packs'/f'w{w}'/'props_main.csv') for w in range(3,9)])
q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['week','game','player','market','side'],keep='last')
P=P.merge(q[['week','game','player','market','side','gsis','game_id']],on=['week','game','player','market','side'],how='left')
G=g4.grade(P,pb);G['split']=G.week.map(lambda w:'train(3-6)' if w<=6 else 'holdout(7-8)')
B=g4.grade(q[(q.market=='rushyds')&(q.side=='under')&(q.tier=='main')],pb);B['split']=B.week.map(lambda w:'train(3-6)' if w<=6 else 'holdout(7-8)')
prim=G[G.tag.isin(['SAVED_READ','RECONSTRUCTED'])].copy();prim['set']='PRIMARY'
z=prim[prim.zone_mof_keep==1].copy();z['set']='ZONE_MOF'
pe=prim[prim.pe_pass==1].copy()
G.to_csv(ROOT/'graded_picks.csv',index=False);B.to_csv(ROOT/'graded_baseline.csv',index=False)
def slips(df,per=5):
    out=[]
    for w,g in df.groupby('week'):
        pool=g[g.result.isin(['WIN','LOSS','PUSH'])&g.decimal.notna()].sort_values(['game','player']).drop_duplicates('player').to_dict('records');n=0
        while len(pool)>=3 and n<per:
            sel=[];c={}
            for r in pool:
                if c.get(r['game'],0)<1:sel.append(r);c[r['game']]=1
                if len(sel)==4:break
            if len(sel)<3:break
            names={r['player'] for r in sel};pool=[r for r in pool if r['player'] not in names]
            lost=any(r['result']=='LOSS' for r in sel);odds=math.prod(r['decimal'] for r in sel if r['result']!='PUSH')
            out.append(dict(week=w,legs=len(sel),players=';'.join(r['player']+' '+r['market']+' '+r['side'] for r in sel),product_decimal=round(odds,2),won=int(not lost),pl=-10 if lost else round(10*(odds-1),2)));n+=1
    return pd.DataFrame(out)
S={k:slips(v) for k,v in [('PRIMARY',prim),('ZONE_MOF',z),('PRO_EDGE',pe)]}
for k,v in S.items():v.to_csv(ROOT/f'graded_slips_{k}.csv',index=False)
o=pd.read_csv(ROOT.parent/'v4'/'saved_reads'/'outcomes.csv')
o['hit']=o.leg_result.astype(str).str.lower().map({'hit':1,'miss':0})
sec=['# v5 graded results','$10 flat/leg at saved main-line prices. UNRESOLVED = no PBP participation (excluded). Slips: ≤5/week, 3–4 legs, 1 leg/game/slip, 1 leg/player, independent product price (estimate).']
for t,d,k in [('By tag',G,['tag']),('By tag x split',G,['tag','split']),('By tag x week',G,['tag','week']),('By tag x market',G,['tag','market','side']),('PRIMARY by split',prim,['split']),('PRIMARY by week',prim,['week']),('PRIMARY by market',prim,['market','side']),('ZONE_MOF by split',z,['split']),('PRO_EDGE-pass subset by split',pe,['split']),('PRO_EDGE-pass by week',pe,['week']),('ZONE_MOF by week',z,['week']),('Baseline rush-under by split',B,['split']),('Baseline by week',B,['week'])]:
    sec+=['## '+t,'```\n'+g4.summary(d,k)+'\n```']
for k,v in S.items():
    sec+=[f'## Slips {k} by week','```\n'+(v.groupby('week').agg(slips=('pl','size'),won=('won','sum'),pl=('pl','sum')).to_string() if len(v) else 'none')+f'\ntotal pl {v.pl.sum() if len(v) else 0:.2f}\n```']
r=o[o.hit.notna()]
sec+=['## Rico placed legs (outcomes.csv, leg hit rate; leg prices mostly unknown)','```\n'+r.groupby(['week','market']).hit.agg(['count','sum','mean']).round(3).to_string()+'\n\nBy market:\n'+r.groupby('market').hit.agg(['count','sum','mean']).round(3).to_string()+'\n\nTickets: '+o.drop_duplicates('ticket').groupby('week').ticket_cash_pnl.agg(['count','sum']).to_string()+'\n```']
(ROOT/'results.md').write_text('\n\n'.join(sec)+'\n');print('\n\n'.join(sec))
