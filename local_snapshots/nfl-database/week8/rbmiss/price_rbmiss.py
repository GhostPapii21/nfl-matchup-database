import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
E_=S.Engine(cutoff='2026-11-01',n=100000); out={}
y=lambda o:S.opp_rb_ypc(E_,o)
out['allen']=S.promote_rb(E_,dict(team='NYJ',opp='LV',spread=-1.5,injured='Breece Hall',rb2='Braelon Allen',market='rushyds',line=78.5,no_vig=0.5,opp_ypc=y('LV')))
out['allen_alt']={str(L):S.promote_rb(E_,dict(team='NYJ',opp='LV',spread=-1.5,injured='Breece Hall',rb2='Braelon Allen',market='rushyds',line=L,no_vig=None,opp_ypc=y('LV')))['p'] for L in (59.5,69.5)}
out['pollard']=S.promote_rb(E_,dict(team='TEN',opp='CIN',spread=12.5,injured='Tyjae Spears',rb2='Tony Pollard',market='rushyds',line=65.5,no_vig=0.5,opp_ypc=y('CIN')))
out['split']=S.split_reprice(E_,dict(team='PIT',opp='CLE',spread=-3.5,opp_ypc=y('CLE'),backs=[dict(player='Jaylen Warren',line=64.5,no_vig=0.5),dict(player='Rico Dowdle',line=31.5,no_vig=0.5)]))
out['opp_ypc']={o:y(o) for o in ('LV','CIN','CLE','WSH','PHI','LAR','LAC','DEN','KC','MIA','NE')}
json.dump(out,open('/workspace/nfl-database/week8/rbmiss/rbmiss_prices.json','w'),indent=1,default=float); print('ok')
