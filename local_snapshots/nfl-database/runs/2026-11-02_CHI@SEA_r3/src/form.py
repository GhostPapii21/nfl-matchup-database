"""§7 recent form: last 4 games with the current QB (>=10 dropbacks as passer) from nflverse pbp (r3 src, pulled 16:38 ET)."""
import pandas as pd,json
p=pd.read_parquet('play_by_play_2026.parquet');p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
QB={'CHI':'C.Williams','SEA':'S.Darnold'}
AB={'Caleb Williams':'C.Williams','Sam Darnold':'S.Darnold','Luther Burden III':'L.Burden','Rome Odunze':'R.Odunze','Colston Loveland':'C.Loveland',"D'Andre Swift":'D.Swift','Roschon Johnson':'R.Johnson','Jaxon Smith-Njigba':'J.Smith-Njigba','Cooper Kupp':'C.Kupp','AJ Barner':'A.Barner','Emanuel Wilson':'E.Wilson'}
def qb_games(t):
    q=p[(p.posteam==t)&(p.passer_player_name==QB[t])&(p.pass_attempt==1)].groupby('game_id').size()
    return sorted(q[q>=10].index,key=lambda g:p[p.game_id==g].game_date.iloc[0])
def stat(g,t,n,mk):
    x=p[(p.game_id==g)&(p.posteam==t)]
    if mk=='passyds': return float(x[(x.passer_player_name==n)].passing_yards.fillna(0).sum())
    r=x[(x.receiver_player_name==n)&(x.complete_pass==1)]; u=x[x.rusher_player_name==n]
    if mk=='rec': return float(len(r))
    if mk=='recyds': return float(r.receiving_yards.fillna(0).sum())
    if mk=='rushyds': return float(u.rushing_yards.fillna(0).sum())
    if mk=='rushrec': return float(r.receiving_yards.fillna(0).sum()+u.rushing_yards.fillna(0).sum())
def form(player,team,mk):
    n=AB[player]; gs=qb_games(team)
    act=[g for g in gs if ((p.game_id==g)&((p.receiver_player_name==n)|(p.rusher_player_name==n)|(p.passer_player_name==n))).any()][-4:]
    tg=[int(((p.game_id==g)&(p.receiver_player_name==n)&(p.pass_attempt==1)).sum()) for g in act]
    return dict(values=[stat(g,team,n,mk) for g in act],games=act,qb=QB[team],targets=tg,source='nflverse play_by_play_2026.parquet (runs/2026-11-02_CHI@SEA_r3/src, release 2026-11-02 14:29 ET)',pulled_et='2026-11-02T16:38')
if __name__=='__main__':
    for a in [('Jaxon Smith-Njigba','SEA','recyds'),("D'Andre Swift",'CHI','rec'),('Rome Odunze','CHI','rec'),('Sam Darnold','SEA','passyds')]: print(a,form(*a))
