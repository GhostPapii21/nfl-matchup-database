"""FD7 receptions re-grade 07:50 ET. Rice-active split for KC (Rice/Worthy): games where Rice had >=1 target and was not hurt early (wk1-3)."""
import json, sim_v5 as S
orig=S.player
KC_GAMES=None
def kc_split(name,team,qb=False):
    d,a,yc,yr,g=orig(name,team,qb)
    keep=set(KC_GAMES); a2=a[a.game_id.isin(keep)]
    return d,a2,yc,yr,g
r_d,r_a,_,_,_=orig('Rashee Rice','KC')
print('Rice log',r_a[['game_id','tgt','rec','pa']].to_string())
w_d,w_a,_,_,_=orig('Xavier Worthy','KC'); print('Worthy log',w_a[['game_id','tgt','rec','pa']].to_string())
KC_GAMES=list(r_a[r_a.tgt>=2].game_id)  # wk1-3 (exclude wk4 early-exit)
legs=[('Rashee Rice','KC','DEN',-1.5,[2.5,3.5,4.5,5.5,6.5],True),('Xavier Worthy','KC','DEN',-1.5,[2.5,3.5,4.5],True),
 ('Stefon Diggs','WSH','PHI',-5.5,[2.5,3.5,4.5,5.5],False),('Tre Tucker','LV','NYJ',1.5,[2.5,3.5,4.5],False),
 ('Puka Nacua','LAR','LAC',-6.5,[6.5,7.5,8.5],False),('Jordan Addison','MIN','DET',3.5,[2.5,3.5,4.5],False)]
out={'kc_games':KC_GAMES}
for n,t,o,sp,r,split in legs:
    S.player=kc_split if split else orig
    s,i=S.sim(dict(player=n,team=t,opp=o,market='rec',spread=sp,rungs=r))
    out[n]=dict(sims=s,info={k:v for k,v in i.items() if k!='log'},split=split)
    print(n,{m:(round(s[m]['median'],1),{k:round(v,3) for k,v in s[m]['rungs'].items()}) for m in s}, 'w_tgt',round(i['w_tgt'],2),'cr',round(i['cr'],3),'n',i['n_games'])
json.dump(out,open('rec_r0750.json','w'),default=float)
