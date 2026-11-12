"""RB rush+rec at FD mains (P7: rush-receive backs graded on rush+rec). sim_v6 100k x3 seed 20261101."""
import sys,json; sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as V
E=V.Engine(); R=json.load(open('bonus_sims.json'))
for n,t,o,sp,l in [('Jahmyr Gibbs','DET','MIN',-3.5,120.5),('Bucky Irving','TB','ATL',-1.5,91.5),('Javonte Williams','DAL','ARI',-7,92.5),
 ('Kyren Williams','LAR','LAC',-6.5,86.5),('Chase Brown','CIN','TEN',-13.5,80.5),('Braelon Allen','NYJ','LV',-1.5,97.5)]:
    out,info=E.sim(dict(player=n,team=t,opp=o,market='rushrec',spread=sp,rungs=[l]))
    R[f'{n}|rushrec']=dict(sims=out,info=info,spread=sp,team=t,opp=o)
    print(n,l,{k:(round(v['median'],1),round(v['rungs'][str(l)],3)) for k,v in out.items()},flush=True)
json.dump(R,open('bonus_sims.json','w'),default=float)
