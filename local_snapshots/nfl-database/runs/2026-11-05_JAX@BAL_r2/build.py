"""TNF JAX@BAL (2026-11-05 20:15 ET, M&T Bank Stadium, week 9) leg build + pre-gate screen. Built 2026-11-03 ET by Blitz.
Inputs (all in src/ or odds/, stamped in feed_stamps.json): nflverse pbp thru 2026-11-02 (fresh pull), players, FTN charting (thru wk8),
FanDuel/DK/Pinnacle props (The Odds API, one event-odds call), ESPN scoreboard spread/total, ESPN injuries, weather_forecast.py week9.
Sims: tools/sim_v6.py, 3 models x 100,000, seed 20261101, SIMV6_SRC=src/. NO_PASS_YDS: passing-yards legs are not built.
This is NOT a full run_gate run: wk9 WR/CB chart, film, NGS, coverage man/zone are MISSING (see report.md)."""
import os,sys,json,re,numpy as np,pandas as pd
R=os.path.dirname(os.path.abspath(__file__)); S=R+'/src'; os.environ['SIMV6_SRC']=S
sys.path.insert(0,'/workspace/nfl-database/tools'); import sim_v6 as SV, depth_wiring as DW
p=pd.read_parquet(S+'/play_by_play_2026.parquet'); p=p[(p.season_type=='REG')&(p.two_point_attempt!=1)]
pl=pd.read_parquet(S+'/players.parquet',columns=['gsis_id','position','display_name']); POS=dict(zip(pl.gsis_id,pl.position))
POS['00-0040718']='WR'   # Travis Hunter: two-way, listed CB in nflverse players; all his props are receiving (ESPN depth lists him at WR)
O=pd.read_csv(R+'/odds/odds_jaxbal.csv'); PULL=O.pulled_utc.iloc[0]
SB=json.load(open(S+'/espn_scoreboard.json'))['events'][0]['competitions'][0]['odds'][0]
SPR={'JAX':-10.0,'BAL':10.0}; TOT=float(SB['overUnder'])   # ESPN/DraftKings "JAX -9.5", O/U 41.5
QB={'JAX':'T.Lawrence','BAL':'J.Fagnano'}  # BAL: Jackson OUT, Huntley 'probably' out (ESPN injuries 2026-11-03), Fagnano Q (ankle)
qid={t:p[(p.posteam==t)&(p.passer_player_name==n)].passer_player_id.iloc[0] for t,n in QB.items()}
MK={'player_receptions':'rec','player_reception_yds':'recyds','player_rush_yds':'rushyds','player_rush_reception_yds':'rushrec'}
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
team_of=lambda n:'JAX' if n in set(O[O.game.str.len()>0].player) and False else None
def pid(name):
    ids=set(p.receiver_player_id.dropna())|set(p.rusher_player_id.dropna())
    for i in pl[pl.display_name.str.replace('.','',regex=False).str.replace(' Jr','',regex=False)==name.replace('.','').replace(' Jr','')].gsis_id:
        if i in ids: return i
def team(i):
    x=p[(p.receiver_player_id==i)|(p.rusher_player_id==i)].sort_values('game_date'); return x.posteam.iloc[-1]
pp=p[(p.pass_attempt==1)&(p.sack!=1)&p.receiver_player_id.notna()].assign(pg=lambda x:x.receiver_player_id.map(POS),
    loc=lambda x:np.where(x.air_yards>=15,'deep','short')+'_'+x.pass_location.fillna('middle').astype(str))
def ypt(d): return float(d.yards_gained.fillna(0).sum()/len(d)) if len(d) else None
def scheme(L,i,t,o,gp):
    """scheme_edge four checks (Rico Nov 2 21:13 ET) for an over; every check has a source."""
    pos=POS.get(i); me=pp[(pp.receiver_player_id==i)&(pp.posteam==t)]
    lgp=ypt(pp[pp.pg==pos]); op=ypt(pp[(pp.pg==pos)&(pp.defteam==o)]); npos=len(pp[(pp.pg==pos)&(pp.defteam==o)])
    m=dict(ok=bool(op and lgp and op>=lgp),detail=f"{o} allows {op:.2f} YPT to {pos} on {npos} tgt vs league {lgp:.2f}" if op else 'no sample',source='nflverse pbp 2026 wk1-8 (fresh pull 2026-11-03 19:13 ET)')
    if len(me)>=5:
        top=me['loc'].value_counts(); z=top.index[0]; share=top.iloc[0]/len(me)
        oz=ypt(pp[(pp['loc']==z)&(pp.defteam==o)]); lz=ypt(pp[pp['loc']==z])
        f=dict(ok=bool(oz and oz>=lz),detail=f"his top zone {z} ({share:.0%} of {len(me)} tgt); {o} allows {oz:.2f} YPT there vs league {lz:.2f}",source='nflverse pbp air_yards/pass_location')
    else: f=dict(ok=False,detail=f'only {len(me)} targets - no zone profile',source='nflverse pbp')
    dog=SPR[t]>=3; s=dict(ok=bool(dog if L['market'] in('rec','recyds') else not dog),detail=f"{t} {SPR[t]:+g}, total {TOT:g}: "+('trailing script -> pass volume' if dog else 'favored script -> run-lean'),source=f"ESPN scoreboard (DraftKings) pulled 2026-11-03 19:13 ET")
    v=[x for x in gp]; l2=np.mean(v[-2:]) if len(v)>=2 else None; l4=np.mean(v[-4:]) if v else None
    ft=dict(ok=bool(l2 is not None and l2>=l4 and l2>L['line']),detail=(f"current-QB games {v}: last2 {l2:.1f} vs last4 {l4:.1f} vs line {L['line']:g}" if l2 is not None else f'{len(v)} current-QB game(s): {v} - fewer than 2'),source='nflverse pbp, games with '+QB[t])
    return dict(matchup=m,scheme_fit=f,script=s,form_trend=ft,status='SCHEME_EDGE' if all(c['ok'] for c in (m,f,s,ft)) else 'no')
def gamelog(i,t,mk):
    gs=DW._last_qb_games(p,t,qid[t],n=4); out=[]
    for g in gs:
        x=p[(p.game_date.astype(str).str[:10]==g)&((p.posteam==t)|(p.defteam==t))]; r=x[(x.receiver_player_id==i)&(x.pass_attempt==1)&(x.sack!=1)]; u=x[(x.rusher_player_id==i)&(x.rush_attempt==1)]
        out.append({'rec':int(r.complete_pass.sum()),'recyds':float(r.receiving_yards.fillna(0).sum()),'rushyds':float(u.rushing_yards.fillna(0).sum())}[mk] if mk!='rushrec' else float(r.receiving_yards.fillna(0).sum()+u.rushing_yards.fillna(0).sum()))
    return gs,out
E_=SV.Engine(); legs=[]
FD=O[(O.book=='fanduel')]; PN=O[O.book=='pinnacle']
for (pn,mk),g in FD[FD.market.isin(MK)].groupby(['player','market']):
    i=pid(pn); m=MK[mk]
    if not i: legs.append(dict(player=pn,market=m,status='CUT',why='no pbp id')); continue
    t=team(i); o='BAL' if t=='JAX' else 'JAX'
    ov,un=g[g.side=='Over'].iloc[0],g[g.side=='Under'].iloc[0]; main=float(ov.point); oround=imp(ov.price)+imp(un.price); nvo=imp(ov.price)/oround
    alts=O[(O.book=='fanduel')&(O.market==mk+'_alternate')&(O.player==pn)&(O.side=='Over')&(O.point<main)].sort_values('point',ascending=False).head(2)
    rungs=[main]+list(alts.point.astype(float))
    try: sims,info=E_.sim(dict(player=pl.set_index('gsis_id').display_name[i],market=m,spread=SPR[t],team=t,opp=o,gsis=i,rungs=rungs))
    except Exception as ex: legs.append(dict(player=pn,market=m,team=t,status='CUT',why=f'SIMULATION NOT RUN: {ex}')); continue
    gs,gp=gamelog(i,t,m)
    def mk_leg(side,line,price,nv,rung):
        ps={k:(v['rungs'][str(line)] if side=='over' else 1-v['rungs'][str(line)]) for k,v in sims.items()}; med={k:v['median'] for k,v in sims.items()}
        e=float(np.mean(list(ps.values()))-nv); why=[]
        if e<0.03: why.append(f'edge {e*100:+.1f} < +3')
        if min(ps.values())<0.45: why.append(f'min model p {min(ps.values()):.3f} < .45')
        if any((md<=line if side=='over' else md>=line) for md in med.values()): why.append('sim median does not clear')
        hit=sum((x>line if side=='over' else x<line) for x in gp)
        if len(gp)<4: why.append(f'§7 MISSING: only {len(gp)} current-QB game(s) ({QB[t]})')
        elif hit<3: why.append(f'§7 FAIL {hit}/4 {gp}')
        L=dict(player=pn,team=t,opp=o,market=m,side=side,line=line,rung=rung,price=int(price),no_vig=round(nv,4),p={k:round(v,4) for k,v in ps.items()},median={k:round(v,1) for k,v in med.items()},edge=round(e,4),last4_cur_qb=gp,games=gs)
        if m in('rec','recyds') and POS.get(i) in('WR','TE'):
            ts=DW.target_share(p,t,i,qid[t]); L['target_share']=ts and ts['value']
            if POS[i]=='TE': L['te_rank']=DW.te_rank(p,POS,t,i,qid[t])
        if m in('rushyds','rushrec') or POS.get(i)=='RB':
            cs=DW.rb_carry_share(p,POS,t,i,qid[t]); L['carry_share']=cs and cs['value']
        if side=='over' and POS.get(i) in('WR','TE','RB'): L['scheme_edge']=scheme(L,i,t,o,gp)
        L['status']='SCREEN_PASS' if not why else 'CUT'; L['why']=why; return L
    legs.append(mk_leg('over',main,ov.price,nvo,'main')); legs.append(mk_leg('under',main,un.price,1-nvo,'main'))
    for a in alts.itertuples(): legs.append(mk_leg('over',float(a.point),a.price,min(imp(a.price)/oround,0.99),'low'))
import depth_rule as DR
# wr_rank: target share with the current QB (last 4), WRs per team; depth_rule (fail closed) on every WR/TE over
RK={}
for t in ('JAX','BAL'):
    w=sorted({(L['player'],L.get('target_share') or 0) for L in legs if L.get('team')==t and 'target_share' in L and 'te_rank' not in L},key=lambda x:-x[1])
    RK.update({n:k+1 for k,(n,_) in enumerate(w)})
for L in legs:
    if 'target_share' not in L or L.get('side')!='over': continue
    typ='TE' if 'te_rank' in L else 'WR'
    leg=dict(type=typ,side='over',wr_rank=RK.get(L['player']) if typ=='WR' else None,te_rank=L.get('te_rank'),rung=L['rung'],price=L['price'],no_vig=L['no_vig'],
             depth=dict(script_pass=DW.script_pass(SPR[L['team']],TOT,'ESPN scoreboard (DraftKings) 2026-11-03 19:13 ET'),
                        target_share=dict(value=L['target_share'],source='nflverse pbp last 4 current-QB'),
                        defender_giving=DW.defender_giving(None,None,zone_pct=None,coverage_allow=None,league_cov=None)))
    if typ=='WR': L['wr_rank']=RK.get(L['player'])
    if DR.is_depth(leg):
        ok,why=DR.evaluate(leg)
        if not ok: L['status']='CUT'; L['why']=L['why']+['DEPTH_RECEIVER: '+'; '.join(why)]
    if typ=='WR' and (RK.get(L['player']) or 9)>=3 and L['status']!='CUT': L['status']='CUT'; L['why'].append('#3/#4 WR over ban')
    if L['price']<=-250: L['flag_m250']=True
json.dump(dict(game='JAX@BAL',kickoff_et='2026-11-05 20:15',odds_pulled_utc=PULL,spread=SPR,total=TOT,qb=QB,seed=SV.SEED,n=SV.N,sim='tools/sim_v6.py',legs=legs),open(R+'/legs.json','w'),indent=1,default=str)
for L in legs: print(L.get('status'),L.get('wr_rank') or L.get('te_rank') or '','flag-250' if L.get('flag_m250') else '',L['player'],L['market'],L.get('side',''),L.get('line',''),L.get('price',''),'edge',L.get('edge'),'|',L.get('why'),'| SE:',L.get('scheme_edge',{}).get('status',''))
