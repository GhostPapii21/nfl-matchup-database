import json,pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parent;V5=ROOT.parent/'yardage_markets_wk3_8'/'v5'
d=pd.read_csv(V5/'graded_picks.csv');H=d[(d.week>=7)&d.tag.isin(['RECONSTRUCTED','SAVED_READ'])]
st=pd.read_csv(ROOT/'probe_stats.csv');L=st[st.kind=='leg']
out=[]
# test 3
H2=H.merge(L[['week','game','player_id','known','f_recall','forced_result']],left_on=['week','game','player'],right_on=['week','game','player_id'],how='left')
H2['recalled']=H2.known.fillna(False)|H2.f_recall.fillna(False)|H2.forced_result.isin(['exact'])
for k,g in H2.groupby('recalled'):out.append(f"T3 recalled={k}: {(g.result=='WIN').sum()}-{(g.result=='LOSS').sum()}")
# test 4
m=pd.read_csv(ROOT/'masked_picks_LOCKED.csv');sample=[tuple(x) for x in json.load(open(ROOT/'masked_sample.json'))]
import sys;sys.path.insert(0,str(ROOT.parent/'yardage_markets_wk3_8'/'v4'));import grade as g4
pb=pd.read_parquet(ROOT.parents[1]/'runs/2026-11-02_shared_src/play_by_play_2026.parquet');pb=pb[(pb.season_type=='REG')&(pb.two_point_attempt!=1)&pb.play_type.isin(['run','pass'])]
q=pd.concat([pd.read_csv(ROOT.parent/'yardage_markets_wk3_8'/'v4'/'packs'/f'w{w}'/'props_main.csv') for w in (7,8)]).sort_values(['snap','book','candidate_id']).drop_duplicates(['week','game','player','market','side'],keep='last')
m=m.merge(q[['week','game','player','market','side','gsis','game_id']],on=['week','game','player','market','side'],how='left')
all_g=pd.concat([d[['player','gsis']],q[['player','gsis']]]).dropna().drop_duplicates('player').set_index('player').gsis
m['gsis']=m.gsis.fillna(m.player.map(all_g))
m=g4.grade(m,pb)
m.to_csv(ROOT/'masked_picks_graded.csv',index=False)
O=H[[ (w,g) in set(sample) for w,g in zip(H.week,H.game)]]
key=lambda x:set(zip(x.player,x.market,x.side))
same=sum(len(key(O[(O.week==w)&(O.game==g)])&key(m[(m.week==w)&(m.game==g)])) for w,g in sample)
sameplayer=sum(len(set(O[(O.week==w)&(O.game==g)].player)&set(m[(m.week==w)&(m.game==g)].player)) for w,g in sample)
out.append(f"T4 sample games {len(sample)}; original legs {len(O)}: {(O.result=='WIN').sum()}-{(O.result=='LOSS').sum()}; masked legs {len(m)}: {(m.result=='WIN').sum()}-{(m.result=='LOSS').sum()} (unresolved {(m.result=='UNRESOLVED').sum()}); identical leg {same}, same player {sameplayer}")
out.append('masked by side: '+str(m.groupby(['side','result']).size().to_dict()))
out.append('original by side: '+str(O.groupby(['side','result']).size().to_dict()))
c=0
for l in open(ROOT/'usage_log.jsonl'):c+=json.loads(l).get('cost_in_usd_ticks',0)
out.append(f"COST ${c/1e10:.2f}")
open(ROOT/'grade_summary.txt','w').write('\n'.join(out));print('\n'.join(out))
