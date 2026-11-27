import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pathlib import Path
import coverage_sim as C, attribution as A, pandas as pd, numpy as np
from pathlib import Path
import argparse; _a=argparse.ArgumentParser(); _a.add_argument('--raw',type=Path,required=True); raw=_a.parse_args().raw
filt=lambda l: l[~((l.label=='verified')&(l.week>=9))]
p,t,links,s,names,off=C.prepare(raw)
cover_pos=A.B.id_maps(*[A.B.load(raw,None)[i] for i in (3,2)])[0]
links['grp']=links.def_id.map(cover_pos).map(A.group_of)
ver=links[(links.label=='verified')&links.link.isin(['PBU','INT'])&(links.week>=9)&links.grp.isin(['CB','S','LB'])]
keys=set(zip(ver.game_id,ver.play_id))
only=lambda tt: pd.Series([(g,pl) in keys for g,pl in zip(tt.game_id,tt.play_id)],index=tt.index)
t,_,names,rows,rbg,mix,imp,s2=C.run(raw,filt,only)
# v1 pieces fit without wk9-12 verified labels
fl=filt(links); fl=fl[fl.grp.isin(A.GROUPS)]
rid=t.set_index(['game_id','play_id']).receiver_player_id
fl=fl.assign(rid=[rid.get((g,pl)) for g,pl in zip(fl.game_id,fl.play_id)])
zc,gz=A.zone_counts(fl); rg,rs=A.receiver_link_maps(fl)
pp=A.fit_pos_prior(fl[fl.label=='verified'])
sr=pd.read_csv(raw/'statrankings_team_cov.csv'); sr['team']=sr.team.replace(A.B.SR_CODE); sr=sr.set_index('team')
s1=s.copy(); s1['grp']=s1.grp.map(A.group_of)
sg={k:v for k,v in s1.groupby(['game_id','team'])}
tt=t.set_index(['game_id','play_id'])
out=[]
for g,tm,pl,vc,rc,cell in rows:
    truth=set(ver[(ver.game_id==g)&(ver.play_id==pl)].def_id); roles=rbg[(g,tm)]
    c=sg[(g,tm)].groupby('gsis').agg(grp=('grp','first'),pct=('defense_pct','max')).reset_index()
    row=tt.loc[(g,pl)].copy(); row['game_id']=g; row['play_id']=pl
    pr1=A.score_game(pd.DataFrame([row]),c,zc,gz,pp,rg,rs,{'man':sr.at[tm,'man'],'two_high':sr.at[tm,'two_high']},A.PARAMS)[0]
    ids=c.gsis.tolist()
    v1=pd.Series(pr1,index=ids) if pr1 is not None else pd.Series(1/len(ids),index=ids)
    win=vc.reindex(ids).fillna(0)
    hyb=(win+0.05)*v1; hyb/=hyb.sum()
    cls=rc.groupby(rc.index.map(C.role_class)).sum(); pc=rc.groupby(rc.index.map(C.pos_class)).sum()
    tcls={C.role_class(r) for r,d in roles.items() if d in truth} or {'other'}
    tpc={C.pos_class(r) for r,d in roles.items() if d in truth} or {'other'}
    # hybrid window class: class of hybrid top pick's role(s)
    def cl_of(d,f): return {f(r) for r,x in roles.items() if x==d} or {'other'}
    h1=hyb.idxmax(); o1=v1.idxmax()
    out.append(dict(game_id=g,play_id=pl,
      v2w_top1=vc.index[0] in truth, v2w_top2=bool(truth&set(vc.index[:2])), v2w_p1=vc.iloc[0],
      v2w_window=cls.idxmax() in tcls, v2w_pos=pc.idxmax() in tpc,
      hyb_top1=h1 in truth, hyb_top2=bool(truth&set(hyb.nlargest(2).index)), hyb_p1=hyb.max(),
      hyb_window=bool(cl_of(h1,C.role_class)&tcls), hyb_pos=bool(cl_of(h1,C.pos_class)&tpc),
      v1_top1=o1 in truth, v1_top2=bool(truth&set(v1.nlargest(2).index)), v1_window=bool(cl_of(o1,C.role_class)&tcls), v1_pos=bool(cl_of(o1,C.pos_class)&tpc),
      truth_has_role='other' not in tcls, true_pos='/'.join(sorted(tpc)), true_window='/'.join(sorted(tcls))))
v=pd.DataFrame(out); v.to_csv('attribution_v2_validation_plays.csv',index=False)
print(len(v)); print(v.drop(columns=['game_id','play_id','true_pos','true_window']).mean().round(3).to_string())
v['tier']=np.where(v.hyb_p1>=0.5,'high',np.where(v.hyb_p1>=0.3,'med','low'))
print(v.groupby('tier')[['hyb_top1','hyb_top2','hyb_window','hyb_pos']].agg(['mean','size']).round(3))

rows=[]
for m,k in (("v1_same_holdout","v1"),("v2_window","v2w"),("v2_window_x_v1_hybrid","hyb")):
    rows.append(dict(method=m,n=len(v),top1=v[f"{k}_top1"].mean(),top2=v[f"{k}_top2"].mean(),window=v[f"{k}_window"].mean(),pos=v[f"{k}_pos"].mean()))
maj_w=v.true_window.value_counts(normalize=True).iloc[0]; maj_p=v.true_pos.value_counts(normalize=True).iloc[0]
rows.append(dict(method="baseline_majority_class",n=len(v),top1=None,top2=None,window=maj_w,pos=maj_p))
pd.DataFrame(rows).round(3).to_csv(Path(__file__).resolve().parent/"attribution_v2_validation_summary.csv",index=False)
print(pd.DataFrame(rows).round(3).to_string(index=False))
print("truth in a role slot:",round(v.truth_has_role.mean(),3)); print(v.true_window.value_counts().to_dict())
