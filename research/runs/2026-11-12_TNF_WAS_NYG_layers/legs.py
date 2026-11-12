import numpy as np, json
from scipy import stats
# Analytic leg probabilities (closed-form; NOT a Monte Carlo). Yards: zero-inflated lognormal.
# Market-anchored: lognormal median = FD main line (no-vig ~50%), sigma by position.
# Model-anchored: median = rain-adjusted forecast mean * med/mean ratio from game log.
logs = {
 'Nabers':[69,1,26,112,121,165,111,43],'Likely':[78,33,13,66,94,99,12,53],
 'Fields':[25,30,19,52,20,19,83,40],'Diggs':[55,47,33,35,44,38,51],
 'AWilliams':[64,24,15,21,31,50,54,25],'Okonkwo':[16,5,60,69,32,57],
 'SkatRush':[81,36,60,58,59,124],'SkatRR':[81+0,36+19,60+40,58+8,59+12,124-3]}
rec_logs={'Nabers':[6,1,5,6,11,12,7,5],'Likely':[8,5,2,7,11,6,2,5],'Diggs':[4,5,4,5,6,3,3],'AWilliams':[4,3,2,3,3,3,5,3]}
def p_yds(line_main, thr, sigma, p0=0.0, median=None):
    med = median if median else line_main
    return (1-p0)*(1-stats.lognorm.cdf(thr-0.5, sigma, scale=med))
def p_rec_pois(lam, k):  # P(X>=k), slight overdispersion via negbin r=12
    r=12; p=r/(r+lam); return 1-stats.nbinom.cdf(k-1, r, p)
def emp(l,thr): return sum(x>=thr for x in l)/len(l)
legs = [
 # name, kind, threshold, market main line, model median, sigma, p0, lam(rec)
 ('Nabers 40+ yds','yds','Nabers',40,66.5,62.0,0.70,0.02),
 ('Nabers 60+ yds','yds','Nabers',60,66.5,62.0,0.70,0.02),
 ('Nabers O67.5 yds','yds','Nabers',68,66.5,62.0,0.70,0.02),
 ('Nabers 5+ rec','rec','Nabers',5,None,None,None,None,6.1),
 ('Likely 20+ yds','yds','Likely',20,46.5,44.0,0.75,0.03),
 ('Likely 30+ yds','yds','Likely',30,46.5,44.0,0.75,0.03),
 ('Likely 40+ yds','yds','Likely',40,46.5,44.0,0.75,0.03),
 ('Likely 3+ rec','rec','Likely',3,None,None,None,None,5.3),
 ('Likely 4+ rec','rec','Likely',4,None,None,None,None,5.3),
 ('Fields 10+ yds','yds','Fields',10,25.5,26.0,0.80,0.10),
 ('Fields 15+ yds','yds','Fields',15,25.5,26.0,0.80,0.10),
 ('Diggs 25+ yds','yds','Diggs',25,36.5,35.5,0.60,0.03),
 ('Diggs 3+ rec','rec','Diggs',3,None,None,None,None,3.9),
 ('A.Williams 15+ yds','yds','AWilliams',15,37.5,27.0,0.75,0.06),
 ('A.Williams 20+ yds','yds','AWilliams',20,37.5,27.0,0.75,0.06),
 ('A.Williams 3+ rec','rec','AWilliams',3,None,None,None,None,3.0),
 ('Okonkwo 15+ yds','yds','Okonkwo',15,35.5,32.0,0.85,0.06),
 ('Okonkwo 25+ yds','yds','Okonkwo',25,35.5,32.0,0.85,0.06),
 ('Skattebo 25+ rush','yds','SkatRush',25,63.5,58.0,0.45,0.02),
 ('Skattebo 30+ R+R','yds','SkatRR',30,74.5,70.0,0.45,0.02),
 ('Skattebo 40+ R+R','yds','SkatRR',40,74.5,70.0,0.45,0.02),
]
out={}
for L in legs:
    name,kind,key,thr=L[:4]
    if kind=='yds':
        mkt,med,sig,p0=L[4:8]
        pm=p_yds(mkt,thr,sig,p0); pmod=p_yds(mkt,thr,sig,p0,median=med); e=emp(logs[key],thr)
    else:
        lam=L[8]; pmod=p_rec_pois(lam,thr); e=emp(rec_logs[key],thr)
        pm=None
    out[name]=dict(market=pm,model=pmod,empirical=e)
    print(f"{name:22s} mkt={pm if pm is None else round(pm,3)} model={pmod:.3f} emp={e:.2f}")
json.dump(out,open('legs.json','w'),indent=1)
