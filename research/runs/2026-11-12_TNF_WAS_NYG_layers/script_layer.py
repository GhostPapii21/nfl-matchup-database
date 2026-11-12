# Script-based (scenario-weighted) projection. NOT a simulation: closed-form normal approximations only.
import math, json
from scipy.stats import norm, lognorm
S = {  # name: (weight, NYG, WAS, quarters NYG, quarters WAS)
 'base_rain_grind':  (0.50, 21, 18, [4,7,3,7],[3,7,4,4]),
 'nyg_early_lead':   (0.25, 27, 14, [7,10,7,3],[0,7,0,7]),
 'was_leads_upset':  (0.25, 17, 23, [3,7,0,7],[7,3,7,6]),
}
W=lambda i: sum(v[0]*v[i] for v in S.values())
nyg, was = W(1), W(2)
q_n=[sum(v[0]*v[3][k] for v in S.values()) for k in range(4)]
q_w=[sum(v[0]*v[4][k] for v in S.values()) for k in range(4)]
m, t = nyg-was, nyg+was
SDm, SDt = 13.5, 13.0  # NFL-typical margin/total SDs (structural, not fitted)
p = {
 'NYG -1.5': 1-norm.cdf(1.5, m, SDm), 'NYG -2.5': 1-norm.cdf(2.5, m, SDm),
 'NYG ML': (1-norm.cdf(0.5, m, SDm)) + 0.5*(norm.cdf(0.5,m,SDm)-norm.cdf(-0.5,m,SDm)),
 'Under 40.5': norm.cdf(40.5, t, SDt),
 'NYG 1H 3-way': 1-norm.cdf(0.5, q_n[0]+q_n[1]-q_w[0]-q_w[1], 9.0),
}
print(f"NYG {nyg:.2f} WAS {was:.2f} margin {m:+.2f} total {t:.2f}")
print("quarters NYG",q_n,"WAS",q_w, "1H",sum(q_n[:2]),sum(q_w[:2]),"2H",sum(q_n[2:]),sum(q_w[2:]))
for k,v in p.items(): print(k, round(v,3))
# Screenshot slip legs (closed-form; gamma/lognormal around market or log medians)
legs = {
 'Skattebo 50+ rush+rec': 1-lognorm.cdf(49.5, 0.45, scale=72),
 'Fields 2+ rec': 0.72,   # Poisson(2.2)=0.64, log 8/8 -> blend
 'White 25+ rush': 1-lognorm.cdf(24.5, 0.55, scale=36),  # FD 38.5 line, log median 28; JCM on IR
 'Daniels 25+ rush': 0.47,  # log 3/6 (31,69,103 | 10,23,16); elbow, rain
 'Diggs 30+ rec yds': 0.97*(1-lognorm.cdf(29.5, 0.60, scale=36.5)),
 'Likely 40+ rec yds': 0.56,
 'Nabers 50+ rec yds': 0.98*(1-lognorm.cdf(49.5, 0.70, scale=64.5)),
}
pj=math.prod(legs.values())
for k,v in legs.items(): print(f"  {k}: {v:.3f}")
print("screenshot joint indep", round(pj,4), "eff decimal", 711/65, "EV$", round(pj*711-65,1))
json.dump(dict(nyg=nyg,was=was,q_n=q_n,q_w=q_w,p=p,legs=legs,joint=pj),open('script_layer.json','w'),indent=1)
