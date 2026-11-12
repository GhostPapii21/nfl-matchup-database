"""STAGE B ONLY. Never run during Stage A; no fitting here."""
import hashlib,json,math
import pandas as pd
from build import OUT,ROOT,settle,summary
import rules

def main():
 expected=json.loads((OUT/'frozen_sha256.json').read_text())
 assert all(hashlib.sha256((OUT/f).read_bytes()).hexdigest()==v for f,v in expected.items()),'Frozen Stage A changed'
 x=pd.read_csv(OUT/'features.csv')
 p=pd.read_parquet(ROOT/'runs/2026-11-02_shared_src/play_by_play_2026.parquet');p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)&p.week.between(3,8)]
 x=settle(x,p);x['split']=x.week.map(lambda w:'train' if w<=6 else 'holdout')
 s=rules.passing(x);s.to_csv(OUT/'selected_singles.csv',index=False)
 rows=[]
 for week,number,legs in rules.slips(s):
  outcomes=[r['result'] for r in legs];odds=[1+(r['price']/100 if r['price']>0 else 100/-r['price']) for r in legs]
  if 'ungraded' in outcomes:result,pl,stake='ungraded',0,0
  elif 'loss' in outcomes:result,pl,stake='loss',-10,10
  else:result,pl,stake=('push' if all(v=='push' for v in outcomes) else 'win'),10*(math.prod(o for o,v in zip(odds,outcomes) if v=='win')-1),10
  rows.append(dict(week=week,split='train' if week<=6 else 'holdout',slip_id=number,market_side=';'.join(sorted({r['market']+' '+r['side'] for r in legs})),candidate_ids=';'.join(r['candidate_id'] for r in legs),result=result,pl=pl,stake=stake))
 t=pd.DataFrame(rows,columns=['week','split','slip_id','market_side','candidate_ids','result','pl','stake']);t.to_csv(OUT/'selected_slips.csv',index=False)
 report=['# Stage B results','Singles and slips are separate $10 portfolios. Mixed slips are grouped by their market-side composition; constituent singles provide individual market × side results. Slip payouts are illustrative.']
 for label,z in [('singles',s),('slips',t)]:
  groups=[['split'],['week']]+([['split','market','side'],['week','market','side']] if label=='singles' else [['split','market_side'],['week','market_side']])
  for keys in groups:
   a=summary(z,keys);a.to_csv(OUT/(label+'_'+'_'.join(keys)+'.csv'),index=False);report.extend([label+' '+str(keys),a.to_string(index=False)])
  h=z[z.week>=7];a=summary(h.assign(period='holdout'),['period']);weekly=h.groupby('week').pl.sum()
  passed=bool(len(a) and a.n.iloc[0]>=100 and a.hit_pct.iloc[0]>=57 and a.roi.iloc[0]>=3 and all(w in weekly.index and weekly[w]>=0 for w in [7,8]))
  report.append(f'{label} target: {passed}. Requires holdout n>=100, hit>=57%, ROI>=3%, each holdout week P/L>=0.')
 base=x[(x.market=='rushyds')&(x.side=='under')];baselines=[]
 for label,z in [('all',base),('one_player',rules.one_player(base))]:
  a=summary(z,['week']);a['baseline']=label;baselines.append(a)
 b=pd.concat(baselines);b.to_csv(OUT/'baseline_by_week.csv',index=False);report.extend(['Rush unders baselines',b.to_string(index=False)])
 comparisons=[]
 for r in json.loads((OUT/'locked_rules.json').read_text())['rules']:
  q=rules.one_player(x[rules.mask(x,r)])
  for period,weeks in [('train',[3,4,5,6]),('holdout',[7,8])]+[(str(w),[w]) for w in range(3,9)]:
   a=summary(q[q.week.isin(weeks)].assign(period=period),['period'])
   for label,z in [('all',base),('one_player',rules.one_player(base))]:
    bb=summary(z[z.week.isin(weeks)].assign(period=period),['period'])
    comparisons.append(dict(market=r['market'],side=r['side'],period=period,baseline=label,rule_n=int(a.n.iloc[0]) if len(a) else 0,rule_roi=float(a.roi.iloc[0]) if len(a) else None,baseline_roi=float(bb.roi.iloc[0]) if len(bb) else None,beats_baseline=bool(len(a) and len(bb) and a.roi.iloc[0]>bb.roi.iloc[0])))
 c=pd.DataFrame(comparisons);c.to_csv(OUT/'rule_baseline_comparison.csv',index=False);report.extend(['Per-rule ROI versus baseline (each rule independently deduplicated)',c.to_string(index=False)])
 (OUT/'results.md').write_text('\n\n'.join(report)+'\n')
 assert all(hashlib.sha256((OUT/f).read_bytes()).hexdigest()==v for f,v in expected.items())
if __name__=='__main__':main()
