"""Game-line legs through policy (r4). Method: final and halftime scores per game from nflverse pbp (max total_*_score
overall, and at the last play with qtr<=2). Team total: team points. Spread -X: team margin > X (cover). 1H spread: 1H margin.
§7 = 3 of last 4 games clear; last-2 = both last 2 clear (else DOWNGRADE). Any-QB window (Rico decides vs Fagnano-only)."""
import pandas as pd, json
p=pd.read_parquet('../2026-11-05_JAX@BAL_r2/src/play_by_play_2026.parquet',columns=['game_id','game_date','home_team','away_team','qtr','total_home_score','total_away_score'])
def games(t):
    g=p[(p.home_team==t)|(p.away_team==t)]; rows=[]
    for gid,x in g.groupby('game_id'):
        h=x.home_team.iloc[0]==t; f=x.iloc[-1]; hf=x[x.qtr<=2].iloc[-1]
        pf,pa=(f.total_home_score,f.total_away_score) if h else (f.total_away_score,f.total_home_score)
        hp,ha=(hf.total_home_score,hf.total_away_score) if h else (hf.total_away_score,hf.total_home_score)
        rows.append(dict(game_id=gid,date=x.game_date.iloc[0],pts=int(pf),opp=int(pa),margin=int(pf-pa),h1_margin=int(hp-ha)))
    return pd.DataFrame(rows).sort_values('date').tail(4)
B,J=games('BAL'),games('JAX')
O=pd.read_csv('odds/odds_jaxbal_game.csv'); O=O[O.book.isin(['fanduel','draftkings','pinnacle'])]
def best(q):
    if q.empty: return 'NO_QUOTE',None,{}
    d=q.price.map(lambda a:1+(a/100 if a>0 else 100/-a)); b=q.loc[d.idxmax()]; return b.book,int(b.price),dict(zip(q.book+'@'+q.point.astype(str),q.price))
LEGS=[('BAL TT under 14.5',list(B.pts),lambda v:v<14.5,O[(O.market=='team_totals')&(O.player=='Baltimore Ravens')&(O.side=='Under')&(O.point==14.5)],'SECONDARY (BAL TT U)'),
      ('JAX -10',list(J.margin),lambda v:v>10,O[(O.market=='spreads')&(O.side=='Jacksonville Jaguars')&(O.point==-10)],'SECONDARY (JAX spread)'),
      ('JAX -9.5',list(J.margin),lambda v:v>9.5,O[(O.market=='spreads')&(O.side=='Jacksonville Jaguars')&(O.point==-9.5)],'SECONDARY (JAX spread)'),
      ('JAX 1H -6.5',list(J.h1_margin),lambda v:v>6.5,O[(O.market=='spreads_h1')&(O.side=='Jacksonville Jaguars')&(O.point==-6.5)],'SECONDARY (JAX 1H)')]
out=[]
for n,v,f,q,read in LEGS:
    h=sum(map(f,v)); s7=('PASS' if h>=3 else 'FAIL')+f' {h}/4 {v}'; l2='OK' if all(map(f,v[-2:])) else 'DOWNGRADE'
    bk,bp,sh=best(q); st='CUT' if not s7.startswith('PASS') else ('PASS-DOWNGRADE' if l2=='DOWNGRADE' else 'PASS')
    out.append(dict(leg=n,read=read,s7=s7,last2=f'{l2} {v[-2:]}',N1='n/a',status=st,best_book=bk,best_price=bp,shop=sh,clv_open_book=bk,clv_open_price=bp,edge='no game model: FLAG n/a'))
pd.DataFrame(out).to_csv('game_legs.csv',index=False)
print(B.to_string());print(J.to_string());print(pd.DataFrame(out)[['leg','s7','last2','status','best_book','best_price','shop']].to_string())
