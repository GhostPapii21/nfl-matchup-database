"""BUG-2026-11-01-FORM: fill legs[].recent_form (last 4 games with current QB) from nflverse pbp + snap counts.
Real data only: play_by_play_2026.parquet (thru 2026-10-29) + snap_counts_2026.parquet (activity). Unsupported markets
are left without recent_form (gate fails closed if such a leg is live)."""
import json, re, sys, glob, os, pandas as pd, numpy as np
S='/workspace/nfl-database/runs/2026-11-01_shared_src/'; NOW=sys.argv[1] if len(sys.argv)>1 else None
P=pd.read_parquet(S+'play_by_play_2026.parquet'); P=P[(P.season_type=='REG')&(P.two_point_attempt!=1)]
PL=pd.read_parquet(S+'players.parquet'); SN=pd.read_parquet(S+'snap_counts_2026.parquet')
NV={'LAR':'LA','WSH':'WAS'}
norm=lambda s:re.sub(r'\b(jr|sr|ii|iii|iv)\b','',re.sub(r'[^a-z ]','',str(s).lower())).split()
norm2=lambda s:' '.join(norm(s))
def pid(name,team):
    c=PL[PL.display_name==name]
    if len(c)>1 and (c.latest_team==team).any(): c=c[c.latest_team==team]
    if c.empty:
        c=PL[PL.display_name.map(lambda x:norm(x)==norm(name))]
    return c.gsis_id.iloc[0] if len(c) else None
db=P[(P.pass_attempt==1)|(P.sack==1)|(P.qb_scramble==1)]
starter=db.groupby(['game_id','posteam','passer_player_id']).size().reset_index(name='n').sort_values('n').groupby(['game_id','posteam']).tail(1)
starter=starter.merge(P.groupby('game_id').game_date.first().reset_index(),on='game_id').sort_values('game_date')
nm=PL.set_index('gsis_id').display_name.to_dict()
def val(q,g,mkt):
    pa=q[(q.passer_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)]
    rr=q[(q.receiver_player_id==g)&(q.pass_attempt==1)&(q.sack!=1)]; uu=q[(q.rusher_player_id==g)&(q.rush_attempt==1)]
    return {'passyds':lambda:pa.passing_yards.fillna(0).sum(),'comp':lambda:pa.complete_pass.sum(),
            'rec':lambda:rr.complete_pass.sum(),'recyds':lambda:rr.receiving_yards.fillna(0).sum(),
            'rushyds':lambda:uu.rushing_yards.fillna(0).sum(),'rushrec':lambda:rr.receiving_yards.fillna(0).sum()+uu.rushing_yards.fillna(0).sum(),
            'targets':lambda:len(rr)}[mkt]()
def form(player,team,mkt):
    t=NV.get(team,team); g=pid(player,team) or pid(player,t)
    if g is None: return None,'player id not found'
    st=starter[starter.posteam==t]
    if st.empty: return None,'no team games'
    qb=st.passer_player_id.iloc[-1]; qgames=st[st.passer_player_id==qb].game_id.tolist()
    sn=SN[(SN.team.isin([t,team]))&(SN.player.map(norm2)==norm2(player))]
    out=[]
    for gid in reversed(qgames):
        q=P[P.game_id==gid]
        snaps=sn[sn.game_id==gid].offense_snaps
        active=(len(snaps) and snaps.iloc[0]>0) or ((q.passer_player_id==g)|(q.receiver_player_id==g)|(q.rusher_player_id==g)).any()
        if not active: continue
        out.append((gid,float(val(q,g,mkt))))
        if len(out)==4: break
    out=out[::-1]
    return dict(values=[v for _,v in out],games=[x for x,_ in out],qb=nm.get(qb,qb),qb_gsis=qb,player_gsis=g,
                source=S+'play_by_play_2026.parquet (nflverse, thru 2026-10-29) + snap_counts_2026.parquet for activity',
                pulled_et='2026-11-01T07:09',note='last 4 games player was active (snaps>0 or pbp involvement) in which current QB (starter of team\'s latest game, most dropbacks) started'),None
MK={'passyds':'passyds','comp':'comp','rec':'rec','recyds':'recyds','rushyds':'rushyds','rushrec':'rushrec','Rec Targets 8.5':'targets'}
if __name__=='__main__':
    log=[]
    for mp in sorted(glob.glob('/workspace/nfl-database/runs/2026-11-01_*/run_manifest.json')):
        m=json.load(open(mp)); 
        for L in m['legs']:
            mk=MK.get(L.get('market'))
            if not mk or not L.get('player'): log.append((mp,L['name'],'SKIP unsupported market',None)); continue
            rf,err=form(L['player'],L['team'],mk)
            if err: log.append((mp,L['name'],'SKIP '+err,None)); continue
            L['recent_form']=rf; log.append((mp,L['name'],'OK',rf['values']))
        # PFF props: pick-side cross-check only (Ghost6-approved), real capture time 07:34
        cc=m.setdefault('cross_checks',[]); keep=[]
        for s in m['sources']:
            if 'PFF player props' in s.get('name',''):
                s=dict(s,pulled_et='2026-11-01T07:34',use='pick-side cross-check only (moved out of gated sources per Ghost6, BUG-2026-11-01-FORM)')
                if not any(c.get('name')==s['name'] for c in cc): cc.append(s)
            else: keep.append(s)
        m['sources']=keep
        json.dump(m,open(mp,'w'),indent=2)
    json.dump(log,open('/workspace/nfl-database/runs/2026-11-01_vetting/recent_form_fill_log.json','w'),indent=1)
    for r in log: print(os.path.basename(os.path.dirname(r[0])),'|',r[1],'|',r[2],r[3] or '')
