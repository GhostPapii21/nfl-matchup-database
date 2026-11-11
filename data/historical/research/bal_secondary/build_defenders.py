import pandas as pd
pf=pd.read_csv('pfr_bal_defense_advanced.csv')
s=pd.read_parquet('raw/snap_counts_2026.parquet'); s=s[s.team=='BAL']
sn=s.groupby('player').agg(games=('week','nunique'),def_snaps=('defense_snaps','sum'),last2_pct=('defense_pct',lambda x:list(x.round(2))[-2:]))
pff=pd.read_csv('../pff_jax_bal/defenders.csv').set_index('defender')
x=pd.read_csv('explosives_bal_wk1_9.csv'); xp=x[x.kind=='pass20+']
tk=xp.tackler.value_counts()
alias={'Kyle Hamilton':'K.Hamilton','Malaki Starks':'M.Starks','Jaylinn Hawkins':'J.Hawkins','Marlon Humphrey':'M.Humphrey','Nate Wiggins':'N.Wiggins','Chandler Rivers':'C.Rivers',"K'Von Wallace":'K.Wallace','Chidobe Awuzie':'C.Awuzie','Keondre Jackson':'K.Jackson','Keyon Martin':'K.Martin','T.J. Tampa':'T.Tampa','Roquan Smith':'R.Smith','Trenton Simpson':'T.Simpson','Teddye Buchanan':'T.Buchanan'}
rows=[]
for _,r in pf.iterrows():
  if r.Pos not in ('CB','S','LB'): continue
  n=r.Player; a=alias.get(n,'')
  rows.append(dict(defender=n,pos=r.Pos,G=r.G,GS=r.GS,def_snaps=sn.def_snaps.get(n,''),last2_snap_pct=sn.last2_pct.get(n,''),
    pff_alignment=pff.alignment_snaps_2026.get(n,'not in free PFF pull'),tgt=r.Tgt,cmp=r.Cmp,cmp_pct=r['Cmp%'],yds=r.Yds,y_per_tgt=r['Yds/Tgt'],y_per_cmp=r['Yds/Cmp'],TD=r.TD,INT=r.Int,rating=r.Rat,dadot=r.DADOT,yac=r.YAC,
    explosive_pass_coverage='unattributed (no public per-play coverage source)',explosive_pass_tackler_proxy=int(tk.get(a,0))))
d=pd.DataFrame(rows).sort_values(['pos','tgt'],ascending=[True,False])
d['source']='PFR /years/2026/defense_advanced.htm (fetched 2026-11-04 ~07:05 ET, BAL G=8); snaps nflverse snap_counts; alignment free PFF player pages (../pff_jax_bal/defenders.csv)'
d.to_csv('defender_table.csv',index=False); print(d.drop(columns=['source']).to_string())
# league CB/S benchmark
import json,io
h=open('raw/pfr_2026_defense_advanced.html').read().replace('<!--','').replace('-->','')
t=[t for t in pd.read_html(io.StringIO(h)) if 'Tgt' in [c[-1] if isinstance(c,tuple) else c for c in t.columns]][0]
t.columns=[c[-1] if isinstance(c,tuple) else c for c in t.columns]
for pos in ['CB','S','LB']:
  q=t[(t.Pos==pos)]; q=q[pd.to_numeric(q.Tgt,errors='coerce')>=15]
  Y=pd.to_numeric(q.Yds).sum()/pd.to_numeric(q.Tgt).sum(); C=pd.to_numeric(q.Cmp).sum()/pd.to_numeric(q.Tgt).sum()
  print(pos,'league (>=15 tgt) Y/T',round(Y,2),'cmp%',round(C,3),'n',len(q))
