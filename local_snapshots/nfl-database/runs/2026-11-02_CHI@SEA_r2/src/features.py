# COPY of runs/2026-11-01_shared_src/features.py (unchanged logic) for the CHI@SEA Nov 2 run; inputs = this src folder (pulled 05:03 ET)
"""Shared features for Nov 1 2026 game-day run (Phases 1-9 inputs). Writes features.json. All from files pulled 07:09-07:14 ET today
(plus ESPN box Oct 31 19:19 ET, PFR cache Oct 29 06:02 ET under Rico's exception)."""
import pandas as pd, numpy as np, json, re, os
SH=os.path.dirname(os.path.abspath(__file__))+'/'
W8='/workspace/nfl-database/week8/'
NV={'LAR':'LA','WSH':'WAS'}; EV={v:k for k,v in NV.items()}
p=pd.read_parquet(SH+'play_by_play_2026.parquet'); p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)].copy()
pl=pd.read_parquet(SH+'players.parquet'); pos=pl.set_index('gsis_id').position_group.to_dict()
ftn=pd.read_parquet(SH+'ftn_charting_2026.parquet')[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers']]
p=p.merge(ftn,left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
p['rpg']=p.receiver_player_id.map(pos)
db=p[p.qb_dropback==1].copy(); db['qbid']=db.passer_player_id.fillna(db.rusher_player_id)
db['blitz5']=(db.n_pass_rushers>=5); db['blitzN']=(db.n_blitzers>0); db['has_ftn']=db.n_pass_rushers.notna()
db['press']=((db.sack==1)|(db.qb_hit==1)|(db.qb_scramble==1))
att=p[(p.pass_attempt==1)&(p.sack!=1)].copy(); att['blitz5']=att.n_pass_rushers>=5; att['has_ftn']=att.n_pass_rushers.notna()
att['press']=(att.qb_hit==1)
F={'teams':{},'qbs':{},'recv':{},'meta':{}}
L4={}
for t in sorted(set(p.posteam.dropna())):
    gids=p[(p.posteam==t)|(p.defteam==t)].drop_duplicates('game_id').sort_values('game_date').game_id.tolist(); L4[t]=gids[-4:]
lg_bl=db[db.has_ftn].blitz5.mean()
for t in sorted(L4):
    d=db[db.defteam==t]; df=d[d.has_ftn]; d4=d[d.game_id.isin(L4[t])]; df4=d4[d4.has_ftn]
    a=att[att.defteam==t]; ng=a.game_id.nunique()
    rr=p[(p.defteam==t)&(p.rush_attempt==1)]
    pg=lambda g:a[a.rpg==g]
    def ypt(x): return float(x.receiving_yards.fillna(0).sum()/max(len(x),1))
    # QB-adjusted RB YPT allowed: residual vs each passer's RB-target YPT against all OTHER defenses
    rb=att[att.rpg=='RB']; res=[]
    for qb,xx in rb[rb.defteam==t].groupby('passer_player_id'):
        oth=rb[(rb.passer_player_id==qb)&(rb.defteam!=t)]
        base=ypt(oth) if len(oth)>=8 else ypt(rb[rb.defteam!=t])
        res.append((ypt(xx)-base)*len(xx))
    rbn=len(rb[rb.defteam==t])
    outside=a[(a.rpg=='WR')&a.pass_location.isin(['left','right'])]; mid=a[(a.rpg=='WR')&(a.pass_location=='middle')]
    F['teams'][EV.get(t,t)]=dict(games=ng,
        blitz5=float(df.blitz5.mean()),blitz5_l4=float(df4.blitz5.mean()) if len(df4) else None,blitzN=float(df.blitzN.mean()),blitzN_l4=float(df4.blitzN.mean()) if len(df4) else None,
        n_db=int(len(df)),pressure_proxy=float(d.press.mean()),pressure_proxy_l4=float(d4.press.mean()),
        pass_yds_pg=float(a.passing_yards.fillna(0).sum()/ng),comp_pg=float(a.complete_pass.sum()/ng),att_pg=float(len(a)/ng),
        rush_yds_pg=float(rr.rushing_yards.fillna(0).sum()/ng),rb_ypc=float(rr[rr.rusher_player_id.map(pos)=='RB'].rushing_yards.mean()),
        pts_pg=float(p[p.defteam==t].groupby('game_id').posteam_score_post.max().mean()),
        ypt_WR=ypt(pg('WR')),n_WR=len(pg('WR')),ypt_TE=ypt(pg('TE')),n_TE=len(pg('TE')),ypt_RB=ypt(pg('RB')),n_RB=len(pg('RB')),
        cr_WR=float(pg('WR').complete_pass.mean()),cr_TE=float(pg('TE').complete_pass.mean()),
        rb_ypt_qbadj=float(sum(res)/max(rbn,1)),wr_outside_ypt_proxy=ypt(outside),wr_middle_ypt_proxy=ypt(mid),
        expl_rec20_WR_pg=float(((pg('WR').receiving_yards>=20).sum())/ng),expl_rec20_RB_pg=float(((pg('RB').receiving_yards>=20).sum())/ng),
        expl_rush15_pg=float(((rr.rushing_yards>=15).sum())/ng),
        third_down_conv_allowed=float(p[(p.defteam==t)&(p.down==3)&p.play_type.isin(['pass','run'])].first_down.mean()))
for k in ['blitz5','pressure_proxy','pass_yds_pg','ypt_WR','ypt_TE','rb_ypc']:
    s=pd.Series({t:v[k] for t,v in F['teams'].items()}); r=s.rank(ascending=False,method='min')
    for t in s.index: F['teams'][t][k+'_rank']=int(r[t])
# QB card (nfl-betting-script §15)
q=db[db.qbid.notna()]
cards={}
for qid,d in q.groupby('qbid'):
    if len(d)<40: continue
    a_=d[(d.pass_attempt==1)&(d.sack!=1)]; f=d[d.has_ftn]; bl=f[f.blitz5]; nb_=f[~f.blitz5]
    ab=bl[(bl.pass_attempt==1)&(bl.sack!=1)]; an=nb_[(nb_.pass_attempt==1)&(nb_.sack!=1)]
    md=d[d.down.isin([3,4])]; cl=d[(d.qtr==4)|(d.score_differential<0)]; acl=cl[(cl.pass_attempt==1)&(cl.sack!=1)]
    ypa=lambda x:float(x.passing_yards.fillna(0).sum()/max(len(x),1))
    name=pl.set_index('gsis_id').display_name.get(qid,qid)
    tm=d.posteam.mode().iloc[0]
    cards[qid]=dict(name=name,team=EV.get(tm,tm),db=len(d),n_blitz_db=len(bl),
        vb_cmp=float(ab.complete_pass.mean()) if len(ab) else None,vb_ypa=ypa(ab),vb_sack=float(bl.sack.mean()) if len(bl) else None,
        nb_cmp=float(an.complete_pass.mean()) if len(an) else None,nb_ypa=ypa(an),nb_sack=float(nb_.sack.mean()) if len(nb_) else None,
        sack_rate=float(d.sack.mean()),sack_hit=float(((d.sack==1)|(d.qb_hit==1)).mean()),
        md_conv=float(((md.first_down==1)|(md.touchdown==1)).mean()) if len(md) else None,
        cl_cmp=float(acl.complete_pass.mean()) if len(acl) else None,cl_ypa=ypa(acl),cl_epa=float(cl.epa.mean()) if len(cl) else None,
        epa_db=float(d.epa.mean()),adot=float(a_.air_yards.mean()),adot_blitz=float(ab.air_yards.mean()) if len(ab) else None,
        behind_los=float((a_.air_yards<=0).mean()),checkdown=float(((a_.air_yards<=0)|(a_.rpg=='RB')).mean()),last_game=d.game_date.max())
C=pd.DataFrame(cards).T
def pct(col,asc=True):
    s=pd.to_numeric(C[col]); return s.rank(pct=True,ascending=asc)
comp={'vs_blitz':(pct('vb_cmp')+pct('vb_ypa')+pct('vb_sack',False))/3,'no_blitz':(pct('nb_cmp')+pct('nb_ypa'))/2,
      'protection':(pct('sack_rate',False)+pct('sack_hit',False))/2,'money_downs':pct('md_conv'),'clutch':(pct('cl_cmp')+pct('cl_ypa')+pct('cl_epa'))/3}
g=lambda x:'A' if x>=.8 else 'B' if x>=.6 else 'C' if x>=.4 else 'D' if x>=.2 else 'F'
for qid in C.index:
    cards[qid]['grades']={k:g(float(v[qid])) for k,v in comp.items()}; cards[qid]['pctl']={k:round(float(v[qid]),2) for k,v in comp.items()}
F['qbs']=cards
# NGS (nflverse release; nextgenstats.nfl.com on hold)
ng={}
for typ in ['passing','receiving','rushing']:
    n=pd.read_parquet(SH+f'ngs_{typ}.parquet'); n=n[(n.season==2026)&(n.season_type=='REG')]
    s=n[n.week==0] if (n.week==0).any() else n
    for _,r in s.iterrows():
        key=r.player_display_name
        if typ=='passing': ng.setdefault(key,{}).update(ttt=r.avg_time_to_throw,cpoe=r.completion_percentage_above_expectation,aggr=r.aggressiveness,ngs_iay=r.avg_intended_air_yards)
        if typ=='receiving': ng.setdefault(key,{}).update(sep=r.avg_separation,cushion=r.avg_cushion,yacoe=r.avg_yac_above_expectation,iay=r.avg_intended_air_yards)
        if typ=='rushing': ng.setdefault(key,{}).update(ryoe_att=r.rush_yards_over_expected_per_att,box8=r.percent_attempts_gte_eight_defenders,eff=r.efficiency)
    F['meta']['ngs_'+typ+'_week0']=bool((n.week==0).any())
F['ngs']={k:{a:(None if v!=v else float(v)) for a,v in d.items()} for k,d in ng.items()}
# receivers: target share all vs blitzed vs pressured(hit), and team ranks last-3
for (tm,rid),d in att[att.receiver_player_id.notna()].groupby(['posteam','receiver_player_id']):
    T=att[att.posteam==tm]; Tf=T[T.has_ftn]; df=d[d.has_ftn]
    name=pl.set_index('gsis_id').display_name.get(rid,rid)
    F['recv'][name+'|'+EV.get(tm,tm)]=dict(share=len(d)/len(T),n_t=len(d),share_bl=(df.blitz5.sum()/max(Tf.blitz5.sum(),1)),n_bl=int(df.blitz5.sum()),
        share_nobl=((~df.blitz5).sum()/max((~Tf.blitz5).sum(),1)),share_press=(d.press.sum()/max(T.press.sum(),1)),n_press=int(d.press.sum()),
        share_clean=((~d.press).sum()/max((~T.press).sum(),1)),pos=pos.get(rid))
F['meta']['lg_blitz5']=float(lg_bl); F['meta']['pbp_through']=str(p.game_date.max()); F['meta']['L4']=L4
json.dump(F,open(SH+'features.json','w'),indent=0,default=lambda o: o.item() if hasattr(o,'item') else str(o))
print('teams',len(F['teams']),'qbs',len(cards),'ngs',len(F['ngs']),'recv',len(F['recv']))
for t in ['MIN','TB','ATL','BAL','CLE','JAX','DET']: print(t,{k:round(v,3) if isinstance(v,float) else v for k,v in F['teams'][t].items() if k in('blitz5','blitz5_rank','pressure_proxy','ypt_WR','ypt_TE','rb_ypc','rb_ypt_qbadj')})
