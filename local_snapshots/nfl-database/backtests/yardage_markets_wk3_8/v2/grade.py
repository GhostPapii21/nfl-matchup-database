"""STAGE B ONLY: explicitly computes holdout outcomes. Never fits rules."""
import json, math, hashlib
from pathlib import Path
import pandas as pd
import rules
from build import ROOT, profit, summary
HERE=Path(__file__).resolve().parent

def settle(outcomes,odds):
 if 'ungraded' in outcomes:return 'ungraded',0.,0.
 if 'loss' in outcomes:return 'loss',-10.,10.
 return ('push' if all(v=='push' for v in outcomes) else 'win'),10*(math.prod(o for v,o in zip(outcomes,odds) if v=='win')-1),10.

def main():
 frozen={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in ['locked_rules.json','rules.py','slip_method.md']}
 expected=json.loads((HERE/'frozen_sha256.json').read_text())
 assert all(expected[f]==digest for f,digest in frozen.items()), 'Stage A lock changed'
 x=pd.read_csv(HERE/'legs.csv');p=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/play_by_play_2026.parquet')
 p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
 ru=p[(p.rush_attempt==1)&p.rusher_player_id.notna()].groupby(['game_id','rusher_player_id']).rushing_yards.sum()
 re=p[(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()].groupby(['game_id','receiver_player_id']).receiving_yards.sum()
 outcomes=[]
 for r in x.itertuples():
  actual=(float(ru.get((r.game_id,r.gsis),0))*(r.market!='recyds')+float(re.get((r.game_id,r.gsis),0))*(r.market!='rushyds')) if pd.notna(r.gsis) and pd.notna(r.team) else float('nan')
  result='ungraded' if pd.isna(actual) or pd.isna(r.price) else 'push' if actual==r.line else 'win' if ((actual>r.line)==(r.side=='over')) else 'loss'
  outcomes.append((actual,result,profit(r.price) if result=='win' else -10 if result=='loss' else 0,0 if result=='ungraded' else 10))
 x[['result_stat','result','pl','stake']]=pd.DataFrame(outcomes,index=x.index)
 singles=[];slips=[]
 for variant in ['baseline','edgecap']:
  for sharp in [False,True]:
   q=rules.passing(x,sharp,variant);q['variant']=variant;q['sharp']='ON' if sharp else 'OFF';q['split']=q.week.map(lambda w:'train' if w<=6 else 'holdout');singles.append(q)
   for week,number,legs in rules.slips(q):
    odds=[1+(r['price']/100 if r['price']>0 else 100/-r['price']) for r in legs]
    result,pl,stake=settle([r['result'] for r in legs],odds)
    slips.append(dict(variant=variant,sharp='ON' if sharp else 'OFF',week=week,split='train' if week<=6 else 'holdout',slip_id=number,legs=len(legs),candidate_ids=json.dumps([r['candidate_id'] for r in legs]),price=math.prod(odds),result=result,pl=pl,stake=stake))
 s=pd.concat(singles,ignore_index=True);t=pd.DataFrame(slips,columns=['variant','sharp','week','split','slip_id','legs','candidate_ids','price','result','pl','stake'])
 s.to_csv(HERE/'selected_singles.csv',index=False);t.to_csv(HERE/'selected_slips.csv',index=False)
 reports=['# Stage B frozen results','Sharp ON is HINDSIGHT. Singles/slips are separate portfolios; product payouts illustrative.']
 for label,z in [('singles',s),('slips',t)]:
  for keys in [['variant','sharp','split'],['variant','sharp','week']]+([['variant','sharp','split','market','side'],['variant','sharp','week','market','side']] if label=='singles' else []):
   a=summary(z,keys);a.to_csv(HERE/f'{label}_{"_".join(keys)}.csv',index=False);reports.extend([label+' '+str(keys),a.to_string(index=False)])
  for (variant,sharp),z in z.groupby(['variant','sharp']):
   h=z[z.week>=7];a=summary(h.assign(period='holdout'),['period']);weekly=h.groupby('week').pl.sum()
   passed=bool(len(a) and a.n.iloc[0]>=100 and a.hit_pct.iloc[0]>=57 and a.roi.iloc[0]>=3 and all(w in weekly.index and weekly.loc[w]>=0 for w in [7,8]))
   reports.append(f'{label} {variant} Sharp {sharp}: target pass={passed}')
 assert frozen=={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in frozen}
 (HERE/'results.md').write_text('\n\n'.join(reports)+'\n')
 print('\n\n'.join(reports))
if __name__=='__main__':main()
