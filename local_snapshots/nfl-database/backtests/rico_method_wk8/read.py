# Pre-kick "Rico method" read for Week 8. Uses ONLY pbp weeks<8, FTN weeks<8, pre-kick lines.
import pandas as pd, numpy as np
S='../../runs/2026-11-02_shared_src/'
p=pd.read_parquet(S+'play_by_play_2026.parquet'); pl=pd.read_parquet(S+'players.parquet')
f=pd.read_parquet(S+'ftn_charting_2026.parquet')
g8=p[p.week==8].groupby('game_id').agg(home=('home_team','first'),away=('away_team','first'),spread=('spread_line','first'),total=('total_line','first')).reset_index()
p=p[p.week<8]  # LEAK GUARD
pos=pl.set_index('gsis_id').position
# defense allowed per game by receiver position, vs league
r=p[p.pass_attempt==1].copy(); r['pos']=r.receiver_player_id.map(pos)
dg=r.groupby(['defteam','game_id','pos']).agg(y=('receiving_yards','sum'),c=('complete_pass','sum')).reset_index()
da=dg.groupby(['defteam','pos'])[['y','c']].mean(); lg=dg.groupby('pos')[['y','c']].mean()
ru=p[p.rush_attempt==1].groupby(['defteam','game_id']).rushing_yards.sum().groupby('defteam').mean(); lgr=ru.mean()
pa=p[p.pass_attempt==1].groupby(['defteam','game_id']).passing_yards.sum().groupby('defteam').mean(); lgp=pa.mean()
# FTN blitz rate allowed by defense (weeks<8)
fm=f[f.week<8].merge(p[['game_id','play_id','defteam','pass_attempt']],left_on=['nflverse_game_id','nflverse_play_id'],right_on=['game_id','play_id'])
bl=fm[fm.pass_attempt==1].groupby('defteam').n_blitzers.apply(lambda s:(s>0).mean())
# player per-game logs
def logs(col,idc,m):
    x=p.groupby([idc,'game_id','week','posteam'])[col].sum().reset_index().rename(columns={idc:'id',col:'v'}); x['market']=m; return x
rec=p[p.pass_attempt==1]
L=pd.concat([rec.groupby(['receiver_player_id','game_id','week','posteam']).receiving_yards.sum().reset_index().rename(columns={'receiver_player_id':'id','receiving_yards':'v'}).assign(market='recyds'),
 rec.groupby(['receiver_player_id','game_id','week','posteam']).complete_pass.sum().reset_index().rename(columns={'receiver_player_id':'id','complete_pass':'v'}).assign(market='rec'),
 p[p.rush_attempt==1].groupby(['rusher_player_id','game_id','week','posteam']).rushing_yards.sum().reset_index().rename(columns={'rusher_player_id':'id','rushing_yards':'v'}).assign(market='rushyds'),
 p[p.pass_attempt==1].groupby(['passer_player_id','game_id','week','posteam']).passing_yards.sum().reset_index().rename(columns={'passer_player_id':'id','passing_yards':'v'}).assign(market='passyds')])
# current QB per team = passer with most attempts in team's last game <8
qa=p[p.pass_attempt==1].groupby(['posteam','week','passer_player_id']).size().reset_index(name='n').sort_values('n').drop_duplicates(['posteam','week'],keep='last')
lastqb=qa.sort_values('week').drop_duplicates('posteam',keep='last').set_index('posteam').passer_player_id
qbw=qa.set_index(['posteam','week']).passer_player_id
lines=pd.read_csv('../current_rules_wk6_8/real_lines_wk6_8.csv'); lines=lines[lines.commence>='2026-10-29']
mnf=pd.read_csv('../rulebook_replay_wk6_8/mnf_lines.csv'); lines=pd.concat([lines,mnf[lines.columns]])
nm=pl.assign(k=pl.display_name.str.lower().str.replace(r'[^a-z ]','',regex=True).str.replace(r' (jr|sr|ii|iii|iv)$','',regex=True))
lines['k']=lines.player.str.lower().str.replace(r'[^a-z ]','',regex=True).str.replace(r' (jr|sr|ii|iii|iv)$','',regex=True)
act=set(pd.concat([p.receiver_player_id,p.rusher_player_id,p.passer_player_id]).dropna())
nm=nm[nm.gsis_id.isin(act)].drop_duplicates('k')
lines=lines.merge(nm[['k','gsis_id']],on='k',how='left')
out=[]
for _,l in lines.iterrows():
    if pd.isna(l.gsis_id): continue
    x=L[(L.id==l.gsis_id)&(L.market==l.market)].sort_values('week')
    if len(x)<3: continue
    tm=x.posteam.iloc[-1]; q=lastqb.get(tm)
    xq=x[[qbw.get((tm,w))==q for w in x.week]] if l.market!='passyds' else x
    if len(xq)<3: xq=x
    l4=xq.tail(4); hits=(l4.v>l.line).sum(); m4=l4.v.mean(); med=l4.v.median()
    opp=[g for g in [l.home,l.away]]; 
    ps=pos.get(l.gsis_id)
    # opponent
    row=g8[(g8.home==tm)|(g8.away==tm)]
    if l.home.startswith('Seattle'): opp_t='SEA' if tm=='CHI' else 'CHI'; spread=3.25; total=46.5; home='SEA'
    else:
        if row.empty: continue
        rr=row.iloc[0]; opp_t=rr.away if rr.home==tm else rr.home; spread=rr.spread; total=rr.total; home=rr.home
    if l.market in('recyds','rec'):
        k='y' if l.market=='recyds' else 'c'
        try: df=da.loc[(opp_t,ps),k]/lg.loc[ps,k]
        except KeyError: df=1.0
    elif l.market=='rushyds': df=ru.get(opp_t,lgr)/lgr
    else: df=pa.get(opp_t,lgp)/lgp
    tspread = spread if tm==home else -spread  # nflverse spread_line: + = home favored
    proj=0.6*m4*df+0.4*med
    for side in ['over','under']:
        e=(proj-l.line)/max(l.line,1) if side=='over' else (l.line-proj)/max(l.line,1)
        h=hits if side=='over' else (l4.v<l.line).sum()
        price=l.over_price if side=='over' else l.under_price
        nv=l.nv_over if side=='over' else 1-l.nv_over
        out.append(dict(game=f"{rr.away if not l.home.startswith('Seattle') else 'CHI'}@{home}",team=tm,opp=opp_t,player=l.player,gsis=l.gsis_id,pos=ps,market=l.market,side=side,line=l.line,price=price,nv=round(nv,3),book=l.book,
          last4=list(l4.v.astype(int)),hits4=f"{h}/{len(l4)}",m4=round(m4,1),def_factor=round(df,2),opp_blitz=round(bl.get(opp_t,np.nan),3),team_spread=tspread,total=total,proj=round(proj,1),edge=round(e,3),h=h,n=len(l4)))
o=pd.DataFrame(out)
o.to_csv('candidates.csv',index=False)
# Selection: edge>=0.12, hits>=3 of last4 w/ current QB, price not shorter than -250, no TDs; script filter: rush overs need team_spread>=-3 (not big dog), pass/rec overs penalised if fav by 7+.
mn={'recyds':20,'rushyds':25,'rec':2.5,'passyds':150}
o=o[o.line>=o.market.map(mn)]
c=o[(o.edge>=0.10)&(o.h>=3)&(o.price>-250)&(o.price.notna())].copy()
c=c[~((c.market=='rushyds')&(c.side=='over')&(c.team_spread>=7))]  # big dog RB over -> skip (nflverse: team_spread>0 means this team favored?)
c['score']=c.edge*(c.h/c.n)
c=c.sort_values('score',ascending=False).drop_duplicates('gsis')
picks=c.groupby('game').head(2)
picks.to_csv('picks_locked.csv',index=False); print(len(o),len(c),len(picks)); print(picks[['game','player','market','side','line','price','last4','def_factor','edge']].to_string())
