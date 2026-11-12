import json,re,math
from scipy.stats import norm
# median projections (pre-bias), built from opportunity gate: team volume x share x efficiency x matchup
P={ # name: dict(stat:(median), q flag)
 'Tetairoa McMillan':dict(team='CAR',tgt=9.0,rec=5.9,recyds=76),
 'Jalen Coker':dict(team='CAR',tgt=7.3,rec=4.7,recyds=61),
 'John Metchie III':dict(team='CAR',tgt=4.0,rec=2.1,recyds=21),
 'Darren Waller':dict(team='CAR',tgt=3.2,rec=2.0,recyds=22),
 'Tommy Tremble':dict(team='CAR',tgt=3.0,rec=2.2,recyds=15),
 'Mitchell Evans':dict(team='CAR',tgt=1.4,rec=1.0,recyds=10),
 'Brycen Tremayne':dict(team='CAR',tgt=1.6,rec=0.9,recyds=9),
 'Chuba Hubbard':dict(team='CAR',tgt=3.0,rec=2.4,recyds=17,car=16,rushyds=66,rr=83),
 'Trevor Etienne':dict(team='CAR',car=4,rushyds=12),
 'Matthew Golden':dict(team='GB',q=1,tgt=8.8,rec=4.6,recyds=68),
 'Christian Watson':dict(team='GB',tgt=7.0,rec=4.3,recyds=72),
 'Tucker Kraft':dict(team='GB',tgt=5.6,rec=3.8,recyds=41),
 'Savion Williams':dict(team='GB',tgt=3.2,rec=2.4,recyds=25,rushyds=5,rr=30),
 'Bo Melton':dict(team='GB',tgt=1.5,rec=0.8,recyds=7),
 'Jonnu Smith':dict(team='GB',tgt=1.0,rec=0.7,recyds=6),
 'Josh Jacobs':dict(team='GB',tgt=3.6,rec=2.9,recyds=21,car=16.5,rushyds=66,rr=87),
 'MarShawn Lloyd':dict(team='GB',tgt=1.2,rec=0.9,recyds=5,car=6,rushyds=18,rr=23),
}
SIG=dict(rec=0.40,recyds=0.55,rushyds=0.40,rr=0.40)
BIAS=dict(rec=0.92,recyds=0.88,rushyds=0.90,rr=0.90)  # partial correction of ~22% (+28.7% rec yds) historical high bias
def pover(med,line,s): return 1-norm.cdf((math.log(line)-math.log(med))/s)
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
lines=open('raw/fd_lines.txt').read().splitlines()
MAP={'Total Receptions':'rec','Receiving Yds':'recyds','Rushing Yds':'rushyds','Rushing + Receiving Yds':'rr'}
ALTMAP={'Alt Receptions':'rec','Alt Receiving Yds':'recyds','Alt Rushing Yds':'rushyds'}
pin={}
for l in open('raw/statshawk_props.txt'):
  m=re.match(r"(.+?) (receiving\.rec|receiving\.yards|rushing\.yards) (\{.*\})",l)
  if m:
    d=eval(m.group(3)).get('pinnacle')
    if d: pin[(m.group(1),{'receiving.rec':'rec','receiving.yards':'recyds','rushing.yards':'rushyds'}[m.group(2)])]=d
out=[];alts=[]
for l in lines:
  tag,name,rs=l.split(' | ',2); rs=eval(rs)
  if tag=='MAIN' and ' - ' in name:
    pl,mk=name.split(' - ',1)
    if pl in P and mk in MAP and MAP[mk] in P[pl]:
      st=MAP[mk];med=P[pl][st];ln=rs[0][1];oo,uo=rs[0][2],rs[1][2]
      fv=imp(oo)/(imp(oo)+imp(uo))
      pv=pin.get((pl,st));pnv=None
      if pv:
        po=int(pv[0].split(':')[1]);pu=int(pv[1].split(':')[1]);pl_=float(pv[0][1:].split(':')[0]);pnv=(imp(po)/(imp(po)+imp(pu)),pl_)
      p=pover(med,ln,SIG[st]);pa=pover(med*BIAS[st],ln,SIG[st])
      out.append(dict(player=pl,team=P[pl]['team'],stat=st,line=ln,over=oo,under=uo,median=med,adj_median=round(med*BIAS[st],1),lo=round(med*math.exp(-1.2816*SIG[st]),1),hi=round(med*math.exp(1.2816*SIG[st]),1),edge=round((med/ln-1)*100,1),p_over=round(p,3),p_over_adj=round(pa,3),fd_novig_over=round(fv,3),pin=pnv,q=P[pl].get('q',0)))
  if tag=='ALT' and ' - ' in name:
    pl,mk=name.split(' - ',1)
    if pl in P and mk in ALTMAP and ALTMAP[mk] in P[pl]:
      st=ALTMAP[mk];med=P[pl][st]
      for r,_,o in rs:
        k=float(re.search(r'(\d+)\+',r).group(1));pa=pover(med*BIAS[st],k-0.5,SIG[st])
        alts.append(dict(player=pl,stat=st,rung=k,odds=o,p_adj=round(pa,3),imp=round(imp(o),3),ev=round(pa*(100/(-o) if o<0 else o/100)-(1-pa),3)))
json.dump(dict(main=out,alts=alts),open('tnf_compare.json','w'),indent=1)
for r in sorted(out,key=lambda r:-abs(r['p_over_adj']-.5)):
  print(f"{r['player']:18s}{r['stat']:8s} L{r['line']:>6} ({r['over']}/{r['under']}) med {r['median']:>5} adj {r['adj_median']:>5} [{r['lo']}-{r['hi']}] edge {r['edge']:+5.1f}% P {r['p_over']:.2f} Padj {r['p_over_adj']:.2f} FDnv {r['fd_novig_over']:.2f} pin {r['pin']} {'Q' if r['q'] else ''}")
print('\nALT rungs passing gate (Padj>=0.68 or 0.80 if Q, odds>=-250, EV>0):')
for a in alts:
  thr=0.80 if P[a['player']].get('q') else 0.68
  if a['p_adj']>=thr and a['odds']>=-250 and a['ev']>0: print(a)
