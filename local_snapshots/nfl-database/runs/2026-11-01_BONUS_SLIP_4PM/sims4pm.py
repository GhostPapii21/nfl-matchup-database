"""4 PM BONUS slip candidates (no §11 conflicts). sim_v6 100k x3 seed 20261101; FD prices odds_b1149.csv; auto-grade edge rule."""
import sys,json,csv; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
TAG=sys.argv[1] if len(sys.argv)>1 else 'b1149'
O=[x for x in csv.DictReader(open(f'/workspace/nfl-database/runs/2026-11-01_shared_src/odds_{TAG}.csv')) if x['book']=='fanduel']
def imp(a): a=float(a); return 100/(a+100) if a>0 else -a/(-a+100)
MK={'rec':'player_receptions','recyds':'player_reception_yds','rushyds':'player_rush_yds','rushrec':'player_rush_reception_yds'}
C=[('Tyler Higbee','LAR','LAC',-6.5,['rec','recyds']),('Rashee Rice','KC','DEN',-1.5,['rec','recyds']),('Xavier Worthy','KC','DEN',-1.5,['rec','recyds']),
 ('Travis Kelce','KC','DEN',-1.5,['rec','recyds']),('J.K. Dobbins','DEN','KC',1.5,['rushyds']),('Courtland Sutton','DEN','KC',1.5,['rec','recyds']),
 ('Evan Engram','DEN','KC',1.5,['rec','recyds']),('Jaylen Waddle','DEN','KC',1.5,['rec','recyds']),('Rhamondre Stevenson','NE','MIA',-7.5,['rec','recyds','rushyds','rushrec']),
 ('DeMario Douglas','NE','MIA',-7.5,['rec','recyds']),('Hunter Henry','NE','MIA',-7.5,['rec','recyds']),('Stefon Diggs','WSH','PHI',-5.5,['rec'])]
E_=V.Engine(); R={}; G=[]
for n,t,o,sp,mks in C:
  for m in mks:
    rows=[x for x in O if x['player']==n and x['market'] in (MK[m],MK[m]+'_alternate')]
    mo=[x for x in rows if x['market']==MK[m] and x['side']=='Over']; mu=[x for x in rows if x['market']==MK[m] and x['side']=='Under']
    if not mo or not mu: print(n,m,'no FD main'); continue
    main=float(mo[0]['point']); ovr=imp(mo[0]['price'])+imp(mu[0]['price'])
    lad={float(x['point']):int(x['price']) for x in rows if x['side']=='Over' and int(x['price'])>-700 and float(x['point'])<=main}
    lad[main]=int(mo[0]['price'])
    try: out,info=E_.sim(dict(player=n,team=t,opp=o,market=m,spread=sp,rungs=sorted(lad)))
    except Exception as e: print(n,m,'ERR',e); continue
    R[f'{n}|{m}']=dict(sims=out,spread=sp,team=t,opp=o,main=main,ladder=lad,overround=ovr)
    for r,pr in sorted(lad.items()):
      ps=[out[k]['rungs'][str(r)] for k in ('mc','bias','gr')]; md=[out[k]['median'] for k in ('mc','bias','gr')]
      nv=imp(pr)/ovr; a=sum(ps)/3; e=a-nv; s=0.5+0.7*(a-0.5)-nv
      ok=e>=.03 and s>0 and min(ps)>=.45 and all(x>r for x in md) and abs(md[0]-main)<12
      G.append(dict(player=n,market=m,rung=r,price=pr,nv=nv,avg=a,edge=e,sh=s,minp=min(ps),med=md,main=main,ok=ok,spread=sp))
      print(('PASS ' if ok else '     ')+f"{n:20s} {m:7s} o{r:<5} {pr:+5d} nv {nv:.3f} avg {a:.3f} e {100*e:+.1f} s {100*s:+.1f} minp {min(ps):.2f} med {[round(x,1) for x in md]} main {main}")
json.dump(dict(sims=R,grades=G,odds_tag=TAG,N=V.N,seed=V.SEED),open(f'sims4pm_{TAG}.json','w'),default=float)
