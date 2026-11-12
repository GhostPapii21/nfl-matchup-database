import json, glob, numpy as np, pandas as pd, common as C, features as Fx, sys
sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as S
R='/workspace/nfl-database'; d,g,pg=C.load()
NAME=S._PL.set_index('gsis_id').display_name.to_dict(); BYN={v:k for k,v in NAME.items()}; POS=S._PL.set_index('gsis_id').position_group.to_dict()
def prior_feats(W):
    p=d[d.week<W]; pa=p[(p.pass_attempt==1)&(p.sack!=1)]
    tsh=pa.groupby(['posteam','receiver_player_id']).size()/pa.groupby('posteam').size()
    ng=p.groupby('defteam').game_id.nunique()
    exp=pa[pa.yards_gained>=20].groupby('defteam').size()/ng
    pos_ypt={}
    pa2=pa.assign(pos=pa.receiver_player_id.map(POS))
    for pos in ('WR','TE','RB'):
        x=pa2[pa2.pos==pos]; pos_ypt[pos]=(x.groupby('defteam').yards_gained.sum()/x.groupby('defteam').size())/(x.yards_gained.sum()/len(x))
    F=Fx.week_feats(d,W); return dict(tsh=tsh,exp=exp,exp_hi=exp.quantile(2/3),pos_ypt=pos_ypt,F=F)
PF={W:prior_feats(W) for W in range(3,9)}
def signals(W,team,opp,pid,pos,tsp):
    P=PF[W]; F=P['F']; s={}
    s['target_share>=22%']=P['tsh'].get((team,pid),0)>=0.22
    s['explosives_allowed_top3rd']=P['exp'].get(opp,0)>=P['exp_hi']
    s['coverage_vs_type(ypt>=1.10x lg)']=P['pos_ypt'].get(pos,pd.Series()).get(opp,1)>=1.10
    gap=F['def_press'].get(opp,np.nan)+F['off_press'].get(team,np.nan)-2*F['lg_press']
    s['passrush_vs_OL_mismatch']=bool(gap>=0.011)
    s['script_dog']=tsp>0
    return s
# ---- pool: Wk8 run manifests ----
pool={}
for f in glob.glob(f'{R}/runs/2026-11-01_*/run_manifest.json'):
    for l in json.load(open(f)).get('legs',[]):
        pool.setdefault(l.get('player'),[]).append(dict(run=f.split('/')[-2],leg=l.get('name'),status=l.get('status'),market=l.get('market'),why=l.get('cut_reasons') or l.get('notes')))
# ---- 100+ receivers ----
rows=[]
for _,x in pg[(pg.week.isin([7,8]))&(pg.recyds>=100)].iterrows():
    rows.append(dict(week=int(x.week),player=NAME.get(x.pid,x.pid),pid=x.pid,pos=x.pos,team=x.team,opp=x.opp,recyds=x.recyds,tgt=x.tgt,tsp=float(x.team_spread),src='pbp'))
GS=pd.read_csv(f'{R}/playlogs/game_scripts_2026.csv'); GS=GS[GS.week==8]; seen={(r['player'],r['week']) for r in rows}
for f in sorted(glob.glob(f'{R}/playlogs/2026_wk8/*_box.json')):
    b=json.load(open(f)); teams=list(b['teams'])
    for t in teams:
        o=[z for z in teams if z!=t][0]; sp=GS[GS.team==t].spread
        for x in b['teams'][t].get('receiving',[]):
            if float(x['YDS'])>=100 and (x['player'],8) not in seen:
                pid=BYN.get(x['player']); rows.append(dict(week=8,player=x['player'],pid=pid,pos=POS.get(pid,'?'),team=t,opp=o,recyds=float(x['YDS']),tgt=int(x.get('TGTS',0)),tsp=float(sp.iloc[0]) if len(sp) else np.nan,src='box'))
M=pd.DataFrame(rows)
NV={'LA':'LAR','WAS':'WSH'}; RV={'LAR':'LA','WSH':'WAS'}
lines=[]
for _,r in M.iterrows():
    pl=pool.get(r.player) if r.week==8 else None
    t=RV.get(r.team,r.team); o=RV.get(r.opp,r.opp)
    s=signals(int(r.week),t,o,r.pid,r.pos,r.tsp if r.tsp==r.tsp else 0) if r.pid else {}
    lit=[k for k,v in s.items() if v]
    if r.week==7: inpool='n/a (no Wk7 run records on the box)'
    elif not pl: inpool='NOT in candidate pool (no leg in any 11-01 run manifest)'
    else: inpool='; '.join(f"{p['leg']} [{p['status']}] {('cut: '+'; '.join(p['why'][:2])) if p['status']=='CUT' and p['why'] else ''}" for p in pl[:3])
    lines.append(f"| Wk{r.week} | {r.player} ({r.pos}, {r.team} vs {r.opp}) | {int(r.recyds)} on {r.tgt} tgt | {inpool} | {', '.join(lit) or 'none'} |")
# ---- walk-forward signal test Wk3-8 (pbp) : does each signal raise P(100+) and recyds-over hit rate ----
T=[]
for _,x in pg[(pg.week>=3)&pg.pos.isin(['WR','TE','RB'])&(pg.tgt>0)].iterrows():
    pr=pg[(pg.pid==x.pid)&(pg.week<x.week)]
    if len(pr)<2: continue
    s=signals(int(x.week),x.team,x.opp,x.pid,x.pos,float(x.team_spread)); line=C.proxy_line(pr.recyds.tolist())
    T.append(dict(week=x.week,pos=x.pos,c100=int(x.recyds>=100),hit=int(x.recyds>line),**s))
T=pd.DataFrame(T); sig=[c for c in T.columns if c not in ('week','pos','c100','hit')]
tt=["| Signal | n on | 100+ rate on | 100+ rate off | lift | recyds-over hit on (stand-in) | p (hit on vs off) |","|---|---|---|---|---|---|---|"]
for c in sig:
    on=T[T[c]];off=T[~T[c]]
    tt.append(f"| {c} | {len(on)} | {on.c100.mean():.1%} | {off.c100.mean():.1%} | {on.c100.mean()/max(off.c100.mean(),1e-9):.2f}x | {on.hit.mean():.1%} | {C.diff_p(on.hit,off.hit):.2f} |")
T['n_sig']=T[sig].sum(axis=1)
tt.append(""); tt.append("| # signals lit | n | 100+ rate | recyds-over hit | ROI −110 |"); tt.append("|---|---|---|---|---|")
for k,gp in T.groupby(T.n_sig.clip(upper=4)): st=C.stats(gp.hit); tt.append(f"| {k}{'+' if k==4 else ''} | {len(gp)} | {gp.c100.mean():.1%} | {st['hit']:.1%} | {st['roi']:+.1%} |")
T.to_csv('b5_signal_rows.csv',index=False); M.to_csv('b5_100plus.csv',index=False)
open('/tmp/b5.md','w').write("\n".join(["| Wk | Player | Rec yds | Candidate pool / what cut him | Signals lit (pregame, weeks < W) |","|---|---|---|---|---|"]+lines)+"\n\n"+"\n".join(tt))
print(open('/tmp/b5.md').read())
