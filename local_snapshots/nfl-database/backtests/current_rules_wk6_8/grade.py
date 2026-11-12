"""Replay Weeks 6-8 through the rulebook (rules/rulebook.py params + tools/depth_rule.evaluate) on real pre-kickoff prices.
Rules that cannot be replayed from history are listed as OFF in the report. TEAM_FILES is OFF (team files not built yet)."""
import sys,json,numpy as np,pandas as pd
sys.path.insert(0,'/workspace/nfl-database'); sys.path.insert(0,'/workspace/nfl-database/tools')
from rules import rulebook as rb; import depth_rule; from feats import feats
S=pd.read_csv(sys.argv[1] if len(sys.argv)>1 else 'sims_wk6_8.csv')
ME,MP=rb.param('NOSHRINK','min_edge'),rb.param('NOSHRINK','min_model_p'); NEED=rb.param('FORM_3OF4','need')
N1S=rb.param('N1','min_share'); SH=rb.param('SHORT_PRICE','price'); WND=rb.param('WEATHER','wind')
def pay(pr): return 100/-pr if pr<0 else pr/100
out=[]
for _,r in S.iterrows():
    f=feats(r); pm=np.mean([r.p_mc,r.p_bias,r.p_gr]); meds=[r.med_mc,r.med_bias,r.med_gr]
    passing=(r.team_spread>=0) or (r.total_line>=46)
    for side in('over','under'):
        o=side=='over'; p=pm if o else 1-pm; nv=r.nv_over if o else 1-r.nv_over; price=r.over_price if o else r.under_price
        act=f['actual']; hit=None if act==r.line else int((act>r.line)==o)
        v=f['vals']; s7=sum((x>r.line)==o and x!=r.line for x in v)
        matchup=(f['allow']>1)==o; form=len(v)>=2 and (np.mean(v)>r.line)==o
        script=((r.team_spread<=-3) if o else (r.team_spread>=3)) if r.market=='rushyds' else (passing==o)
        scheme=matchup and script and form   # scheme_fit proxy = position-group matchup (no historical coverage file)
        B=[]; FL=[]
        if p-nv<ME or p<MP:
            if scheme and p-nv>0: FL.append('SCHEME_EDGE(+0 to +3)')
            B.append('NOSHRINK(edge<+3)')
        if not(len(v)>=4 and s7>=NEED):
            (FL if scheme else B).append('FORM_3OF4')
        if r.pos=='RB' and r.market=='rushyds' and o:
            sh=f['rb_sh']
            if np.mean(sh)<N1S: B.append('N1(<60% RB carries)')
            elif sum(x>=N1S for x in sh)<3 or (r.team_spread>=3 and f['tgt_pg']<4): B.append('RB_TRAIL')
        leg=dict(type=r.pos,wr_rank=f['rank'] if r.pos=='WR' else None,te_rank=f['rank'] if r.pos=='TE' else None,side=side,rung='low',price=price,no_vig=nv,
                 depth=dict(script_pass=dict(ok=passing,source='spread/total'),target_share=dict(value=f['tsh'],source='pbp last4'),defender_giving=dict(ok=f['allow']>1,source='pbp pos-group allowed')))
        ok,why=depth_rule.evaluate(leg)
        if not ok: B.append('DEPTH_RECEIVER')
        if o and r.market!='rushyds' and f['outdoor'] and f['wind']>=WND: B.append('WEATHER')
        if price<=SH: FL.append('SHORT_PRICE')
        out.append(dict(week=r.week,game=r.game_id,player=r.player,team=r.team,pos=r.pos,rank=f['rank'],market=r.market,side=side,line=r.line,price=price,
            nv=round(nv,3),p=round(p,3),edge=round(p-nv,3),meds=[round(m,1) for m in meds],last4=v,depth=depth_rule.is_depth(leg),scheme_edge=scheme,
            blocks='|'.join(B),flg='|'.join(FL),actual=act,hit=hit,usd=0 if hit is None else (10*pay(price) if hit else -10)))
D=pd.DataFrame(out); D['blocks']=D['blocks'].fillna('');D['flg']=D['flg'].fillna('');D['passed']=D['blocks']==''; D.to_csv('graded_all_sides.csv',index=False)
def s(x,lab):
    x=x[x.hit.notna()]; n=len(x); k=int(x.hit.sum())
    return f"| {lab} | {n} | {k}-{n-k} | {k/n:.1%} | ${x.usd.sum():+,.0f} |" if n else f"| {lab} | 0 | | | |"
best=lambda x:x.sort_values('edge',ascending=False).drop_duplicates(['week','player'])
L=['| bucket | legs | W-L | hit | $10 flat |','|---|---|---|---|---|']
P_=best(D[D.passed]); L.append(s(P_,'PASSED (best leg per player)'))
for W in(6,7,8): L.append(s(P_[P_.week==W],f'  Week {W}'))
for m in('recyds','rec','rushyds','passyds'): L.append(s(P_[P_.market==m],f'  {m}'))
for sd in('over','under'): L.append(s(P_[P_.side==sd],f'  {sd}s'))
L.append(s(P_[P_['flg'].str.contains('FORM_3OF4')],'  SCHEME_EDGE overriding 3-of-4'))
L.append(s(P_[P_.depth],'  depth receivers (WR3/4, TE2)'))
L.append(s(P_[P_['flg'].str.contains('SHORT')],'  -250 or shorter (flag)'))
L.append(s(best(D[D.passed & (D.edge<0.03/0.7)]) if False else P_[(0.5+0.7*(P_.p-0.5))-P_.nv<0.03],'  alive only because the shrink is gone'))
E=D[~D.passed & ~D['blocks'].str.contains('NOSHRINK')]
L.append(s(best(E),'BLOCKED by a rule (had +3 edge)'))
for rl in('FORM_3OF4','N1','RB_TRAIL','DEPTH_RECEIVER','WEATHER'):
    L.append(s(best(E[E.blocks.str.contains(rl)]),f'  {rl}'))
FLG=D[D['flg'].str.contains('SCHEME_EDGE')]; L.append(s(best(FLG),'SCHEME_EDGE FLAGS (+0 to +3, for Ghost6 at real price)'))
L.append(s(best(D[D['blocks'].str.contains('NOSHRINK')&(D.edge>0)&~D['flg'].str.contains('SCHEME')]),'Positive edge under +3 (cut)'))
L.append(s(D[D.edge<=0],'No model edge (all sides)'))
open('summary.md','w').write('\n'.join(L)); print('\n'.join(L))
P_.to_csv('passed_legs.csv',index=False)
