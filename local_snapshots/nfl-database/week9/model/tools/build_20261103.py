import pandas as pd, numpy as np, glob, json
S='/workspace/nfl-database/runs/2026-11-03_shared_src/'
p=pd.read_parquet(S+'play_by_play_2026.parquet'); p=p[p.season_type=='REG'] if 'season_type' in p else p
f=pd.read_parquet(S+'ftn_charting_2026.parquet')[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers']]
p=p.merge(f,left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
pl=pd.read_parquet(S+'players.parquet') if __import__('os').path.exists(S+'players.parquet') else None
rush=p[(p.rush_attempt==1)&(p.qb_scramble!=1)&p.rusher_player_id.notna()].copy()
if pl is not None:
    pos=dict(zip(pl.gsis_id,pl.position)); rush['pos']=rush.rusher_player_id.map(pos)
    rush=rush[rush.pos=='RB']
# wk8 Sunday supplement (ESPN play text CSVs)
sup=[]
for c in glob.glob('/workspace/nfl-database/playlogs/2026_wk8/*.csv'):
    d=pd.read_csv(c)
    if 'pos' not in d: continue
    d=d[(d.kind=='rush')&(d.pos=='RB')]
    sup.append(pd.DataFrame({'posteam':d.off,'defteam':d.defn,'yards_gained':pd.to_numeric(d.yds,errors='coerce'),'game_id':d.game,'week':8}))
sup=pd.concat(sup); have=set(rush[rush.week==8].posteam)
sup=sup[~sup.posteam.isin(have)]
R=pd.concat([rush[['posteam','defteam','yards_gained','game_id','week']],sup])
off=R.groupby('posteam').yards_gained.agg(['sum','count']); off['ypc']=off['sum']/off['count']
lg=R.yards_gained.mean()
R['opp_off_ypc']=R.posteam.map(off.ypc)
D=R.groupby('defteam').agg(car=('yards_gained','size'),yds=('yards_gained','sum'),g=('game_id','nunique'),exp=('yards_gained',lambda x:(x>=15).sum()),oppypc=('opp_off_ypc','mean'))
D['ypc']=D.yds/D.car; D['rb_rush_ypg']=D.yds/D.g; D['exp15_pg']=D.exp/D.g; D['exp_rate%']=100*D.exp/D.car
D['adj_ypc']=D.ypc-(D.oppypc-lg)  # opponent-adjusted (offenses faced)
QE67=D['exp_rate%'].quantile(.67); QE33=D['exp_rate%'].quantile(.33)
QY67=D.rb_rush_ypg.quantile(.67); QY33=D.rb_rush_ypg.quantile(.33)
def tier(r):
    s=0
    s+= int(r.adj_ypc>4.4)+int(r.ypc>4.4)+int(r.exp_rate_>QE67)+int(r.rb_rush_ypg>QY67)  # int(): numpy-2 bool+bool is logical OR
    t=int(r.adj_ypc<=3.9)+int(r.ypc<=3.8)+int(r.exp_rate_<QE33)+int(r.rb_rush_ypg<QY33)
    return 'SOFT' if s>=3 else ('STOUT' if t>=3 else 'MIDDLE')
D=D.rename(columns={'exp_rate%':'exp_rate_'}); D['tier']=D.apply(tier,axis=1); D=D.rename(columns={'exp_rate_':'exp_rate%'})
D=D.round(2).sort_values('adj_ypc',ascending=False)
D.to_csv('run_defense_tiers_2026-11-03.csv')
# team volume: pass att/g, plays, pass rate neutral (wp .2-.8, q1-3)
sc=p[(p.pass_attempt==1)|(p.rush_attempt==1)]
T=sc.groupby('posteam').agg(g=('game_id','nunique'),pa=('pass_attempt','sum'),ru=('rush_attempt','sum'))
T['pa_pg']=T.pa/T.g; T['ru_pg']=T.ru/T.g
n=sc[(sc.wp.between(.2,.8))&(sc.qtr<=3)&(sc.down<=2)]
T['neutral_ed_pass%']=100*n.groupby('posteam').pass_attempt.mean()
T['rb_ypc_off']=off.ypc
T.round(2).to_csv('team_volume_2026-11-03.csv')
# blitz / pressure (proxy) by defense; CIN focus
db=p[(p.qb_dropback==1)]
B=db.groupby('defteam').agg(db=('play_id','size'),blitz=('n_blitzers',lambda x:(x>0).mean()),rush5=('n_pass_rushers',lambda x:(x>=5).mean()),sack=('sack','mean'),hit=('qb_hit','mean'))
B['press_proxy']=db.assign(pp=((db.sack==1)|(db.qb_hit==1)|(db.qb_scramble==1)).astype(int)).groupby('defteam').pp.mean()
B['blitz_rk']=B.blitz.rank(ascending=False); B['press_rk']=B.press_proxy.rank(ascending=False)
B.round(3).to_csv('defense_blitz_pressure_2026-11-03.csv')
# QB splits Penix
q=db[db.passer_player_name.fillna('').str.contains('Penix')]
def sp(x): 
    a=x[x.pass_attempt==1]; return dict(n=len(x),att=len(a),cmp=round(a.complete_pass.mean(),3),ypa=round(a.passing_yards.fillna(0).sum()/max(len(a),1),2),int_=int(a.interception.sum()),sack=round(x.sack.mean(),3),epa=round(x.epa.mean(),3))
pen={'all':sp(q),'blitz':sp(q[q.n_blitzers>0]),'no_blitz':sp(q[q.n_blitzers==0]),'pressured_proxy':sp(q[(q.qb_hit==1)|(q.sack==1)|(q.qb_scramble==1)]),'clean_proxy':sp(q[(q.qb_hit!=1)&(q.sack!=1)&(q.qb_scramble!=1)])}
pen['blitz_rate_faced']=round((q.n_blitzers>0).mean(),3); pen['press_rate_faced_proxy']=round(((q.qb_hit==1)|(q.sack==1)|(q.qb_scramble==1)).mean(),3)
ints=q[q.interception==1][['week','qtr','air_yards','n_blitzers','qb_hit','pass_location','defteam']]
pen['ints']=ints.to_dict('records')
lgq=db[db.pass_attempt==1]; pen['league_int_rate']=round(lgq.interception.mean(),4)
pen['league_blitz_rate']=round((db.n_blitzers>0).mean(),3)
json.dump(pen,open('penix_splits_2026-11-03.json','w'),indent=1,default=str)
# RB logs
def log(name):
    r=p[(p.rusher_player_name==name)&(p.rush_attempt==1)]; t=p[p.receiver_player_name==name]
    g=r.groupby(['week','defteam']).agg(car=('play_id','size'),yds=('rushing_yards','sum'))
    g['tgt']=t.groupby(['week','defteam']).size(); g['rec_yds']=t.groupby(['week','defteam']).receiving_yards.sum()
    team=p[(p.rush_attempt==1)&(p.qb_scramble!=1)].groupby(['week','posteam']).size()
    return g.fillna(0)
out={}
for nm in ['J.Gibbs','B.Robinson','K.Walker','B.Tuten']:
    out[nm]=log(nm).reset_index().to_dict('records')
json.dump(out,open('rb_logs_2026-11-03.json','w'),indent=1,default=str)
print(D.to_string()); print(B.loc[['CIN','ATL','BAL','DET','MIA','KC','SEA','IND']].round(3).to_string())
print(json.dumps({k:v for k,v in pen.items()},indent=0,default=str)[:3000])
for k,v in out.items(): print(k,v)
print(T.round(1).to_string())
