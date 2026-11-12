"""Turn fresh grok_picks.csv into v5_reads schema (no outcomes) for the locked v5_1.py selector."""
import pandas as pd
g=pd.read_csv('grok_picks.csv'); l=pd.read_csv('../data/lines_noact.csv')
ids=l[['week','player','market','side','gsis','game_id']].drop_duplicates(['week','player','market','side'])
g=g.merge(ids,on=['week','player','market','side'],how='left'); g['tag']='RECONSTRUCTED'
v5=pd.read_csv('../data/v5_reads.csv'); sv=v5[v5.tag=='SAVED_READ']
done={(r.week,r.game) for r in g.itertuples()}
sv=sv[[ (r.week,r.game) in done for r in sv.itertuples()]]  # only games with a completed fresh read
out=pd.concat([g,sv],ignore_index=True); out['split']=out.week.map(lambda w:'train(3-6)' if w<=6 else 'holdout(7-8)')
assert out.gsis.notna().all(), out[out.gsis.isna()]
out=out.drop_duplicates(['week','game_id','gsis','market','side','line'])
out.to_csv('data/fresh_reads.csv',index=False); print(out.tag.value_counts(), out.confidence.value_counts(), out.verdict.value_counts())
