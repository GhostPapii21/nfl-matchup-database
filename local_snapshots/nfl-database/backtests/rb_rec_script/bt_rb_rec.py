"""RB receiving game-script backtest (analysis only; no rule/gate/sim changes).
Lead RB (most prior carries, >=2 prior games) per team-game, Wk3-8. Markets rec/recyds/rushrec (+rushyds for the rush+rec vs rush-only test).
Walk-forward: week W uses pbp strictly before week W (Engine cutoff + all trigger features). RAW sim_v6 (calib=None), 100k x 3 models.
Wk3-7 + Wk8 TNF graded from nflverse pbp; Wk8 Sunday graded from playlogs/2026_wk8/*_box.json with spread/total from game_scripts_2026.csv.
Lines: real (run manifests, game files preferred over DFS) else stand-in floor(prior median)+0.5."""
import sys, json, glob
import numpy as np, pandas as pd
sys.path.insert(0,'/workspace/nfl-database/tools'); sys.path.insert(0,'/workspace/nfl-database/backtests/wk8_proposals')
import sim_v6 as S
from harness import load, proxy_line
ROOT='/workspace/nfl-database'; MK=('rec','recyds','rushrec','rushyds'); COL={'rec':'rec','recyds':'recyds','rushrec':'rr','rushyds':'ryds'}
NAME=S._PL.set_index('gsis_id').display_name.to_dict(); POS=S._PL.set_index('gsis_id').position_group.to_dict()
def real_lines():
    r={}
    fs=sorted(glob.glob(f"{ROOT}/runs/2026-11-01_*/run_manifest.json"),key=lambda f:'DFS' in f)
    for f in fs:
        for l in json.load(open(f)).get('legs',[]):
            if l.get('market') not in MK: continue
            pt=next((b['point'] for b in (l.get('fanduel'),l.get('pinnacle'),l.get('draftkings')) if isinstance(b,dict) and b.get('point') is not None), l.get('line'))
            if pt is not None: r.setdefault((l.get('player'),l['market']),float(pt))
    return r
def feats(d,W):
    """pregame team/QB features from pbp before week W"""
    p=d[d.week<W]; att=p[(p.pass_attempt==1)&(p.sack!=1)]
    tg=att.groupby(['game_id','posteam']).agg(pa=('pass_attempt','sum'),wk=('week','first'),sp=('spread_line','first'),tot=('total_line','first'),home=('home_team','first')).reset_index()
    tg['tsp']=np.where(tg.posteam==tg.home,-tg.sp,tg.sp); tg['imp']=tg.tot/2-tg.tsp/2
    tm=tg.groupby('posteam').pa.mean(); tg['dev']=tg.pa-tg.posteam.map(tm)
    X=np.c_[np.ones(len(tg)),tg.tsp,tg.imp-tg.imp.mean()]; b=np.linalg.lstsq(X,tg.dev,rcond=None)[0]
    db=p[(p.qb_dropback==1)]; dEPA=db.groupby('defteam').epa.mean().rank(ascending=False)  # 1 = worst pass D (most EPA allowed)
    att=att.assign(rpos=att.receiver_player_id.map(POS))
    q=att.groupby('passer_player_id').agg(n=('pass_attempt','size'),rb=('rpos',lambda s:(s=='RB').mean()),sh=('air_yards',lambda s:(s<=0).mean()))
    q=q[q.n>=40]; q['ck']=0.5*q.rb.rank(pct=True)+0.5*q.sh.rank(pct=True)
    lastqb={}
    for t,g in att.sort_values('game_date').groupby('posteam'):
        lg=g[g.game_id==g.game_id.iloc[-1]]; lastqb[t]=lg.passer_player_id.value_counts().index[0]
    return dict(tm=tm,b=b,impmean=tg.imp.mean(),dEPA=dEPA,q=q,lastqb=lastqb)
def main():
    d,g,pg=load(); pg['rr']=pg.ryds+pg.recyds; RL=real_lines(); rows=[]
    GS=pd.read_csv(f'{ROOT}/playlogs/game_scripts_2026.csv'); GS=GS[GS.week==8]
    box={}
    for f in sorted(glob.glob(f'{ROOT}/playlogs/2026_wk8/*_box.json')):
        b=json.load(open(f))
        for team,t in b['teams'].items():
            st={}
            for x in t.get('rushing',[]): st.setdefault(x['player'],dict(car=0,ryds=0,tgt=0,rec=0,recyds=0)).update(car=int(x['CAR']),ryds=float(x['YDS']))
            for x in t.get('receiving',[]): st.setdefault(x['player'],dict(car=0,ryds=0,tgt=0,rec=0,recyds=0)).update(tgt=int(x.get('TGTS',0)),rec=int(x['REC']),recyds=float(x['YDS']))
            pa=sum(int(x['C/ATT'].split('/')[1]) for x in t.get('passing',[]))
            box[team]=(st,pa)
    for W in range(3,9):
        cut=d[d.week==W].game_date.min(); E=S.Engine(cutoff=cut,calib=None); F=feats(d,W); prior=pg[pg.week<W]
        games=[]  # (team,opp,tsp,total,actual_getter,team_pa,src)
        for (gid,team),grp in pg[pg.week==W].groupby(['game_id','team']):
            r0=grp.iloc[0]; tot=float(d[d.game_id==gid].total_line.iloc[0]); tpa=int(d[(d.game_id==gid)&(d.posteam==team)&(d.pass_attempt==1)&(d.sack!=1)].shape[0])
            games.append((team,r0.opp,float(r0.team_spread),tot,lambda pid,grp=grp:(grp[grp.pid==pid].iloc[0].to_dict() if (grp.pid==pid).any() else None),tpa,'pbp'))
        if W==8:
            for team,(st,pa) in box.items():
                gs=GS[GS.team==team]
                if gs.empty: print('no spread',team); continue
                games.append((team,gs.opp.iloc[0],float(gs.spread.iloc[0]),float(gs.total.iloc[0]),lambda pid,st=st:st.get(NAME.get(pid,pid)),pa,'box'))
        for team,opp,tsp,tot,get,tpa,src in games:
            s=prior[(prior.team==team)&(prior.pos=='RB')].groupby('pid').agg(car=('car','sum'),gp=('game_id','nunique'))
            s=s[s.gp>=2].sort_values('car',ascending=False)
            if s.empty: continue
            pid=s.index[0]; a=get(pid)
            if a is None or (a['car']+a['tgt'])==0: continue   # inactive
            a=dict(a); a['rr']=a['ryds']+a['recyds']; name=NAME.get(pid,pid)
            imp=tot/2-tsp/2; pa_hat=F['tm'].get(team,np.nan)+F['b'][1]*tsp+F['b'][2]*(imp-F['impmean'])
            qb=F['lastqb'].get(team); ck=F['q'].ck.get(qb,np.nan); dr=F['dEPA'].get(team,np.nan)
            pr=prior[prior.pid==pid].sort_values('week')
            for m in MK:
                line=proxy_line(pr[COL[m]].tolist()); lsrc='standin'
                if W==8 and (name,m) in RL: line,lsrc=RL[(name,m)],'real'
                if line is None: continue
                try: o,_=E.sim(dict(player=name,gsis=pid,team=team,opp=opp,market=m,spread=tsp,rungs=[line]),raw=True)
                except Exception as e: print('skip',name,W,m,e); continue
                p=float(np.mean([o[x]['rungs'][str(line)] for x in S.MODES]))
                rows.append(dict(week=W,src=src,player=name,gsis=pid,team=team,opp=opp,team_spread=tsp,total=tot,implied=imp,pa_hat=pa_hat,team_pa_actual=tpa,
                    qb=NAME.get(qb,qb),qb_checkdown_pct=ck,own_passD_rank=dr,market=m,line=line,line_src=lsrc,p=p,actual=float(a[COL[m]]),hit=int(a[COL[m]]>line)))
            print(W,name,team,tsp,round(pa_hat,1),flush=True)
    pd.DataFrame(rows).to_csv('rb_rec_legs_raw.csv',index=False)
if __name__=='__main__': main()
