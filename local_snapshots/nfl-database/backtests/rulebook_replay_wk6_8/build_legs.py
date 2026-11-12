"""Step 2: point-in-time leg features + per-game run dirs (run_manifest.json, checklist.md, report.md) + team files.
Everything uses pbp weeks < W (the week-W starting QB is the only week-W input, announced pregame). Labels:
PROXY = built from pbp/FTN, not the named vendor stat; HINDSIGHT = Sharp table as of Oct 27 used for Weeks 6-7;
REPLAY STAMP = pulled_et set relative to the replay clock (kickoff-30m); true as-of kept in true_asof."""
import os,sys,re,json,glob,io,collections,numpy as np,pandas as pd
from datetime import datetime,timedelta,timezone
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT='/workspace/nfl-database'; SRC=f'{ROOT}/runs/2026-11-02_shared_src'
os.environ['SIMV6_SRC']=SRC; sys.path.insert(0,f'{ROOT}/tools'); import sim_v6 as S
ET=timezone(timedelta(hours=-4))  # EDT through Nov 1 2026
def et(dt_utc,tz_off=None):
    off=-5 if dt_utc>=datetime(2026,11,1,6,tzinfo=timezone.utc) else -4
    return dt_utc.astimezone(timezone(timedelta(hours=off))).replace(tzinfo=None)
fmt=lambda d:d.strftime('%Y-%m-%dT%H:%M')
P=pd.read_parquet(f'{SRC}/play_by_play_2026.parquet'); P=P[(P.season_type=='REG')&(P.two_point_attempt!=1)]
PLr=pd.read_parquet(f'{SRC}/players.parquet'); PG=PLr.set_index('gsis_id').position_group.to_dict(); POS=PLr.set_index('gsis_id').position.to_dict(); NAME=PLr.set_index('gsis_id').display_name.to_dict()
E2G=PLr.dropna(subset=['espn_id']).assign(e=lambda x:x.espn_id.astype(str).str.replace(r'\.0$','',regex=True)).set_index('e').gsis_id.to_dict()
FTN=pd.read_parquet(f'{ROOT}/runs/2026-11-01_shared_src/ftn_charting_2026.parquet'); NGSP=pd.read_parquet(f'{ROOT}/runs/2026-11-01_shared_src/ngs_passing.parquet')
INJ=pd.read_parquet('/tmp/inj26.parquet'); AB=json.load(open(f'{HERE}/abbr.json')); WX=json.load(open(f'{HERE}/weather_wk6_8.json'))
EA={'LAR':'LA','WSH':'WAS'}; ea=lambda a:EA.get(a,a)
pa=P[(P.pass_attempt==1)&(P.sack!=1)].copy(); pa['pg']=pa.receiver_player_id.map(PG); ru=P[P.rush_attempt==1].copy(); ru['pg']=ru.rusher_player_id.map(PG)
wk=P.drop_duplicates('game_id').set_index('game_id').week
qbg=pa.groupby(['game_id','posteam','passer_player_id']).size().reset_index(name='n').sort_values('n').drop_duplicates(['game_id','posteam'],keep='last').set_index(['game_id','posteam']).passer_player_id
ST={'passyds':pa.groupby(['passer_player_id','game_id']).passing_yards.sum(),'rec':pa.groupby(['receiver_player_id','game_id']).complete_pass.sum(),
    'recyds':pa.groupby(['receiver_player_id','game_id']).receiving_yards.sum(),'rushyds':ru.groupby(['rusher_player_id','game_id']).rushing_yards.sum()}
TGT=pa.groupby(['receiver_player_id','game_id']).size(); TT=pa.groupby(['game_id','posteam']).size()
CAR=ru.groupby(['rusher_player_id','game_id']).size(); RBC=ru[ru.pg=='RB'].groupby(['game_id','posteam']).size()
APP=set(zip(pa.receiver_player_id,pa.game_id))|set(zip(ru.rusher_player_id,ru.game_id))|set(zip(pa.passer_player_id,pa.game_id))
def stat(g,gid,m): return float(ST[m].get((g,gid),0) or 0)
def team_games(t,W): return sorted([g for g in set(P[P.posteam==t].game_id) if wk[g]<W],key=lambda g:wk[g])
# ---------- ESPN (injuries / inactives, MNF box) ----------
EIDX=json.load(open(f'{HERE}/espn/index.json')); ESP={}
for eid,v in EIDX.items(): ESP[(ea(v['away']),ea(v['home']),v['week'])]=eid
def espn(a,h,W): 
    k=ESP.get((a,h,min(W,8))); return json.load(open(f'{HERE}/espn/{k}.json')) if k else None  # MNF CHI@SEA is ESPN week 8
# ---------- lines + sims ----------
V1=pd.read_csv('../current_rules_wk6_8/sims_wk6_8.csv'); SR=pd.read_csv('sims_replay.csv'); ALT=pd.read_csv('alt_candidates.csv'); MN=pd.read_csv('mnf_lines.csv')
SRk={(r.week,r.gsis,r.market,round(r.thr,1)):r for r in SR.itertuples()}
thr=lambda mk,line:line+0.5 if mk=='rec' else line
MOD={'mc':'monte_carlo','bias':'bias','gr':'game_randomness'}
cand=[]
def add(base,side,line,price,nv,rung,simr,kind,nvnote,snap):
    ps={m:getattr(simr,f'p_{m}') for m in MOD}; md={m:getattr(simr,f'med_{m}') for m in MOD}
    if side=='under': ps={m:1-v for m,v in ps.items()}
    d=dict(base); d.update(side=side,line=float(line),price=float(price),no_vig=float(nv),rung=rung,p=ps,med=md,kind=kind,nv_note=nvnote,snap=snap,
        ypc_boost=float(getattr(simr,'ypc_boost',1.0) if hasattr(simr,'ypc_boost') else 1.0),opp_ypc_sim=getattr(simr,'opp_ypc',None))
    cand.append(d)
class R: pass
def v1sim(r):
    o=R(); [setattr(o,f'p_{m}',getattr(r,f'p_{m}')) for m in MOD]; [setattr(o,f'med_{m}',getattr(r,f'med_{m}')) for m in MOD]; o.ypc_boost=1.0; o.opp_ypc=None; return o
for r in V1.itertuples():
    b=dict(week=r.week,game_id=r.game_id,home=r.home_team,away=r.away_team,player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,team_spread=r.team_spread,
           total=r.total_line,main_line=r.line,book=r.book,commence=r.commence,pos=r.pos)
    s=SRk.get((r.week,r.gsis,r.market,round(thr(r.market,r.line),1)),None) if r.market=='rushyds' else None
    s=s if s is not None else v1sim(r)
    add(b,'over',r.line,r.over_price,r.nv_over,'main',s,'main','two-way consensus no-vig (v1 real_lines)',r.snap)
    add(b,'under',r.line,r.under_price,1-r.nv_over,'main',s,'main','two-way consensus no-vig (v1 real_lines)',r.snap)
v1i=V1.set_index(['event','player','market'])
for r in ALT.itertuples():
    s=SRk.get((r.week,r.gsis,r.market,round(thr(r.market,r.point),1)))
    if s is None: continue
    v=v1i.loc[(r.event,r.player,r.market)]; v=v.iloc[0] if isinstance(v,pd.DataFrame) else v
    b=dict(week=r.week,game_id=r.game_id,home=v.home_team,away=v.away_team,player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,team_spread=r.team_spread,
           total=v.total_line,main_line=r.line,book=r.book,commence=v.commence,pos=r.pos)
    add(b,'over',r.point,r.price,min(r.nv_proxy,0.99),'low',s,'alt','PROXY: one-sided alt, same/v1-book main-line margin removed',r.snap)
for r in MN.itertuples():
    s=SRk.get((9,r.gsis,r.market,round(thr(r.market,r.line),1)))
    if s is None: continue
    b=dict(week=9,game_id=r.game_id,home='SEA',away='CHI',player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,market=r.market,team_spread=r.team_spread,total=r.total_line,main_line=r.line,book=r.book,commence=r.commence,pos=None)
    add(b,'over',r.line,r.over_price,r.nv_over,'main',s,'main','two-way consensus no-vig',r.snap); add(b,'under',r.line,r.under_price,1-r.nv_over,'main',s,'main','two-way consensus no-vig',r.snap)
C=pd.DataFrame(cand); C['pos']=C.pos.fillna(C.gsis.map(PG)); C['pos']=C.pos.replace({'DB':'WR'})
print('candidates',len(C),C.groupby(['week','kind']).size().to_dict())
# ---------- per-week defensive tables ----------
DPOS=lambda g:POS.get(g)
def cov_table(W):
    d=pa[pa.game_id.map(wk)<W].copy()
    cr=d.interception_player_id.fillna(d.pass_defense_1_player_id).fillna(d.solo_tackle_1_player_id).fillna(d.tackle_with_assist_1_player_id).fillna(d.assist_tackle_1_player_id)
    d['cred']=cr; d=d.dropna(subset=['cred']); d['dpos']=d.cred.map(DPOS)
    g=d.groupby(['defteam','cred']).agg(targets=('play_id','size'),comp=('complete_pass','sum'),yds=('receiving_yards',lambda x:x.fillna(0).sum())).reset_index()
    g['comp_pct']=g.comp/g.targets; g['ypt']=g.yds/g.targets; g['dpos']=g.cred.map(DPOS); g['name']=g.cred.map(NAME)
    lg=d.groupby(d.dpos.map(lambda p:'CB' if p in('CB',) else 'S' if p in('S','FS','SAF','SS','DB') else 'LB' if p in('LB','ILB','OLB','MLB') else 'X')).apply(lambda x:x.receiving_yards.fillna(0).sum()/len(x)).to_dict()
    return g,lg
def bucket(p): return 'CB' if p=='CB' else 'S' if p in('S','FS','SAF','SS','DB') else 'LB' if p in('LB','ILB','OLB','MLB') else 'X'
SH=pd.read_html(io.StringIO(open('/tmp/sharp.html').read()))[0].drop_duplicates('Team'); SH['ab']=SH.Team.map(AB); SHd=SH.set_index('ab').to_dict('index')
MANMED=float(SH['Man Rate'].median())
def pressure(W):
    f=FTN[FTN.week<W]; f=f[f.n_pass_rushers>0]; mp=P[['game_id','play_id','defteam','posteam']].rename(columns={'game_id':'nflverse_game_id','play_id':'nflverse_play_id'})
    f=f.merge(mp,on=['nflverse_game_id','nflverse_play_id'])
    bl=(f.n_blitzers.astype(float)/f.n_pass_rushers.astype(float)).groupby(f.defteam).mean().round(3).to_dict()
    db=P[(P.week<W)&((P.pass_attempt==1)|(P.sack==1))]; pr=db.groupby('defteam').apply(lambda x:((x.sack==1)|(x.qb_hit==1)).mean()).round(3).to_dict()
    th=f[f.read_thrown.isin(['0','1','2','SD','CHK','DES'])]; ck=(th.read_thrown=='CHK').groupby(th.posteam).mean().round(3).to_dict()
    n=NGSP[(NGSP.week<W)&(NGSP.week>0)]; tt=n.groupby('team_abbr').apply(lambda x:np.average(x.avg_time_to_throw,weights=x.attempts)).round(2).to_dict()
    pp=pa[pa.week<W]; tup=pp.groupby('posteam').apply(lambda x:(x.qb_hit==1).mean()).round(3).to_dict()
    return bl,pr,ck,tt,tup
def box(W):
    f=FTN[FTN.week<W].merge(P[['game_id','play_id','defteam','rush_attempt']].rename(columns={'game_id':'nflverse_game_id','play_id':'nflverse_play_id'}),on=['nflverse_game_id','nflverse_play_id'])
    f=f[f.rush_attempt==1]; return f.groupby('defteam').n_defense_box.mean().to_dict(), float(f.n_defense_box.mean())
def allow(opp,W,m,pg):
    if m=='rushyds': d=ru[(ru.game_id.map(wk)<W)&(ru.pg=='RB')]; return d[d.defteam==opp].rushing_yards.mean()/d.rushing_yards.mean()
    if m=='passyds': d=pa[pa.game_id.map(wk)<W]; return d[d.defteam==opp].passing_yards.fillna(0).mean()/d.passing_yards.fillna(0).mean()
    d=pa[(pa.game_id.map(wk)<W)&(pa.pg==pg)]; o=d[d.defteam==opp]; return (o.receiving_yards.fillna(0).sum()/max(len(o),1))/(d.receiving_yards.fillna(0).sum()/max(len(d),1))
# ---------- injuries ----------
def inj_map(W,a,h):
    m={}
    for r in INJ[(INJ.week==min(W,8))].itertuples(): m[r.gsis_id]=(str(r.report_status).lower(),'nflverse injuries_2026 weekly report (/tmp/inj26.parquet)',r.position,r.team)
    e=espn(a,h,W)
    if e:
        for t in e.get('injuries',[]):
            for x in t.get('injuries',[]):
                g=E2G.get(str(x['athlete']['id']))
                if g: m[g]=(('inactive' if str(x.get('status','')).lower()=='out' else str(x.get('status','')).lower()),'ESPN summary injuries (game status / inactives)',x['athlete'].get('position',{}).get('abbreviation'),ea(t['team']['abbreviation']))
    return m
# ---------- game list ----------
GAMES=C.drop_duplicates('game_id')[['week','game_id','home','away','commence','total']].to_dict('records')
SNAPS={}
for f in glob.glob('raw/game_*.json'):
    j=json.load(open(f))
    for g in j['data']: SNAPS.setdefault((AB[g['away_team']],AB[g['home_team']]),[]).append((j['timestamp'],g))
def gline(a,h,ko):
    L=[x for x in SNAPS.get((a,h),[]) if x[0]<=ko] or SNAPS.get((a,h),[])
    ts,g=sorted(L)[-1]; sp=[o['point'] for b in g['bookmakers'] for m in b['markets'] if m['key']=='spreads' for o in m['outcomes'] if AB.get(o['name'])==h]
    tot=[o['point'] for b in g['bookmakers'] for m in b['markets'] if m['key']=='totals' for o in m['outcomes'] if o['name']=='Over']
    return ts,(float(np.median(sp)) if sp else None),(float(np.median(tot)) if tot else None)
os.makedirs('runs',exist_ok=True); LEGROWS=[]; EN={}
def engine(W):
    if W not in EN: EN[W]=S.Engine(cutoff=(P[P.week==W].game_date.min() if W<9 else '2026-11-02'),calib=None,n=100_000)
    return EN[W]
for G in GAMES:
    W,gid,h,a=G['week'],G['game_id'],G['home'],G['away']; game=f'{a}@{h}'
    ko=datetime.fromisoformat(G['commence'].replace('Z','+00:00')); now=et(ko)-timedelta(minutes=30); stamp=fmt(now-timedelta(minutes=5))
    gl=C[C.game_id==gid]; ts_odds,hsp,tot=gline(a,h,G['commence'])
    covg,lgy=cov_table(W); bl,pr,ck,tt,tup=pressure(W); bx,bxl=box(W); IM=inj_map(W,a,h)
    wkey=game if game in WX else next((k for k in WX if WX[k].get('game_id')==gid),None); w=WX.get(wkey) if wkey else None
    roof=(w or {}).get('roof') or str(P[P.game_id==gid].roof.iloc[0] if (P.game_id==gid).any() else 'outdoors')
    kv=(w or {}).get('kickoff') or {}; dv=(w or {}).get('day_before') or {}
    wxe=dict(roof=roof,precip_pct=kv.get('precip_pct'),gust_mph=kv.get('gust_mph'),wind_mph=kv.get('wind_mph'),source=kv.get('url','open-meteo'),provider='open-meteo',pulled_et=fmt(now-timedelta(hours=1)),
             label='REPLAY STAMP: Open-Meteo historical-forecast archive, kickoff hours; pulled after the fact')
    fc_ok=dv.get('status')=='OK' and dv.get('precip_pct') is not None
    fce=dict(roof=roof,status='OK',kickoff_et=fmt(et(ko)),provider='open-meteo',source=(dv if fc_ok else kv).get('url','open-meteo'),
             precip_pct=(dv if fc_ok else kv).get('precip_pct'),gust_mph=(dv if fc_ok else kv).get('gust_mph'),wind_mph=(dv if fc_ok else kv).get('wind_mph'),
             label='Open-Meteo previous-runs day-1 forecast' if fc_ok else 'NO day-1 precip: KICKOFF-hour value used and labeled')
    wxflag=S.__dict__.get('x',None)
    import run_gate as RG; wxflag=RG.wx_flag_of(wxe)
    # coverage by defense (drop Out/Doubtful/inactive defenders)
    def defenders(dteam):
        g=covg[covg.defteam==dteam].copy(); bad=('out','doubtful','inactive','ir')
        g['st']=g.cred.map(lambda x:IM.get(x,('active',))[0]); g=g[~g.st.isin(bad)]; g['b']=g.dpos.map(bucket)
        return {b:g[g.b==b].sort_values('targets',ascending=False) for b in ('CB','S','LB')}
    DF={t:defenders(t) for t in (h,a)}
    cbs_out={t:sorted({NAME.get(x,x) for x,v in IM.items() if v[3]==t and str(v[2]).upper() in('CB',) and v[0] in('out','doubtful','inactive')}) for t in (h,a)}
    legs=[]; sims={k:dict(model=v,n=100000,seed=S.SEED,script='tools/sim_v6.py',legs={}) for k,v in MOD.items()}
    tsp_pool=[]
    for t in (h,a):
        l4=team_games(t,W)[-4:]; q=pa[(pa.game_id.isin(l4))&(pa.posteam==t)].receiver_player_id.value_counts(); tot_t=sum(TT.get((x,t),0) for x in l4)
        for g,n in q.items():
            if tot_t and n/tot_t>=0.22: tsp_pool.append(dict(name=NAME.get(g,g),team=t,share=round(n/tot_t,3),gsis=g))
    for r in gl.itertuples():
        t,o=r.team,r.opp; qb=qbg.get((gid,t))
        if W==9:
            e=espn(a,h,9) or {}; qb=None  # starting QB from ESPN box (allowed: week-W starter)
            for tm in (e.get('boxscore') or {}).get('players',[]):
                if ea(tm['team']['abbreviation'])==t:
                    for st in tm['statistics']:
                        if st['name']=='passing' and st['athletes']: qb=E2G.get(str(st['athletes'][0]['athlete']['id']))
        pr_g=team_games(t,W); same=[x for x in pr_g if qbg.get((x,t))==qb and (r.gsis,x) in APP][-4:]
        vals=[stat(r.gsis,x,r.market) for x in same]; l4=pr_g[-4:]
        name=f"{r.player} {r.market} {r.side} {r.line:g}"
        pos=str(r.pos); rec=r.market in('rec','recyds')
        tsh=sum(TGT.get((r.gsis,x),0) for x in l4)/max(sum(TT.get((x,t),0) for x in l4),1)
        rk=None
        if pos in('WR','TE'):
            q=pa[(pa.game_id.isin(l4))&(pa.posteam==t)&(pa.pg==pos)].receiver_player_id.value_counts(); rk=list(q.index).index(r.gsis)+1 if r.gsis in q.index else 9
        src_pbp=f'nflverse play_by_play_2026.parquet weeks<{W} ({SRC})'
        L=dict(name=name,player=r.player,gsis=r.gsis,team=t,opp=o,game=game,type=pos,market=r.market,side=r.side,line=r.line,price=r.price,no_vig=round(r.no_vig,4),
               no_vig_note=r.nv_note,book=r.book,rung=r.rung,status='PASS',spread=r.team_spread,receiving=rec,kind=r.kind)
        L['recent_form']=dict(values=vals,games=same,qb=NAME.get(qb,qb),source=src_pbp+' ; appearance = had a target/carry/pass that game (PROXY for active)',pulled_et=stamp,true_asof=f'pbp through week {W-1}')
        inj=IM.get(r.gsis); L['injury_status']=inj[0] if inj else 'active'; L['injury_source']=inj[1] if inj else 'not on nflverse weekly report or ESPN game injuries'
        L['weather_stop']=bool(wxflag and r.side=='over' and RG.wx_sensitive(L))
        if pos=='WR': L['wr_rank']=rk
        if pos=='TE': L['te_rank']=rk
        # coverage
        sh=SHd.get(o,{}); covsrc='sharpfootballanalysis.com coverage-schemes table (/tmp/sharp.html, as of 2026-10-27)'+(' HINDSIGHT for week %d'%W if W<=7 else '')
        mz=dict(value=dict(man=sh.get('Man Rate'),zone=sh.get('Zone Rate')),source=covsrc,pulled_et=stamp,true_asof='2026-10-27',label='REPLAY STAMP')
        mf=dict(value=dict(middle_closed=sh.get('Middle Closed Rate'),middle_open=sh.get('Middle Open Rate')),source=covsrc,pulled_et=stamp,true_asof='2026-10-27',label='REPLAY STAMP')
        cov=dict(man_zone=mz,mof=mf); prim=None
        if rec:
            D=DF[o]; b,idx=('CB',0) if pos=='WR' and (rk or 9)==1 else ('CB',1) if pos=='WR' and rk==2 else ('CB',2) if pos=='WR' else (('S',0) if pos=='TE' else ('LB',0))
            if pos=='TE' and len(D['S'])==0: b='LB'
            tb=D[b]
            if len(tb)>idx:
                x=tb.iloc[idx]; prim=dict(name=x['name'],pos=x.dpos,targets=int(x.targets),comp_pct=round(float(x.comp_pct),3),ypt=round(float(x.ypt),2),primary=True,
                    source=f'PROXY pbp credit (INT/PBU/tackler on targeted plays) weeks<{W}; rule {pos}{rk}->{b}#{idx+1}; nflverse pbp',pulled_et=stamp,true_asof=f'pbp through week {W-1}')
                cov['defenders']=[prim]
            else: cov['defenders']=[]
        L['coverage']=cov
        # RB
        if pos=='RB':
            sh4=[CAR.get((r.gsis,x),0)/max(RBC.get((x,t),1),1) for x in l4]
            cs=sum(CAR.get((r.gsis,x),0) for x in l4)/max(sum(RBC.get((x,t),0) for x in l4),1)
            L['carry_share']=dict(value=round(cs,3),source=src_pbp+' last 4 team games, share of team RB carries')
            L['rb_role']=dict(share60_3of4=sum(s>=0.6 for s in sh4)>=3,shares=[round(s,2) for s in sh4],may_trail=bool(r.team_spread>0),tgt_pg=round(np.mean([TGT.get((r.gsis,x),0) for x in l4]) if l4 else 0,2),source=src_pbp)
        if r.market=='rushyds':
            oy=r.opp_ypc_sim if r.opp_ypc_sim==r.opp_ypc_sim and r.opp_ypc_sim is not None else None
            if oy is None:
                try: oy=S.opp_rb_ypc(engine(W),o)
                except Exception: oy=None
            if oy is not None:
                L['opp_rb_ypc']=round(float(oy),2); sb=S.soft_run_d_boost(oy); L['soft_run_d']=dict(sb,applied=float(sb['applied']),resimmed=bool(sb['soft']),ypc_boost_used=r.ypc_boost)
        # depth
        if (pos=='WR' and rk in(3,4)) or (pos=='TE' and (rk or 1)>=2):
            sp_ok=bool(r.team_spread>=3 or (tot or 0)>=47); dg=(prim and prim['ypt']>lgy.get(bucket(prim['pos']),99)) or allow(o,W,r.market,pos)>=1.05
            L['depth']=dict(script_pass=dict(ok=sp_ok,source=f'odds snapshot {ts_odds}: team spread {r.team_spread:+g}, total {tot}',detail='ok if team is a 3+ pt dog or total >= 47'),
                            target_share=dict(value=round(tsh,3),source=src_pbp+' last 4'),defender_giving=dict(ok=bool(dg),source='pbp credit PROXY ypt vs league bucket avg / opp allowance ratio'))
        if pos=='WR' and rk==3 and r.side=='over' and len(cbs_out[o])>=2:
            tpg=np.mean([TGT.get((r.gsis,x),0) for x in same]) if same else 0; L['tpg_last4_cur_qb']=round(float(tpg),2)
            L['flags']=['WR3_DEPLETED_SECONDARY_EXCEPTION']+(['BORDERLINE'] if 4<=tpg<5 else [])
            l2=np.mean([TGT.get((r.gsis,x),0) for x in same[-2:]]) if same else 0; L['opportunity']='up' if l2>=tpg else 'mixed'
        # SCHEME_EDGE
        over=r.side=='over'
        if rec and prim:
            lb=lgy.get(bucket(prim['pos'])); mt=(prim['ypt']>lb) if over else (prim['ypt']<lb); md=f"primary {prim['name']} {prim['ypt']} ypt vs league {bucket(prim['pos'])} {lb:.2f}"
        else:
            al=allow(o,W,r.market,pos); mt=(al>1) if over else (al<1); md=f'opp allowance ratio {al:.2f} vs league 1.00'
        if pos=='RB' or r.market=='rushyds':
            ob=bx.get(o); sf=(ob<bxl) if over else (ob>=bxl); sfd=f'opp avg box {ob:.2f} vs league {bxl:.2f} (FTN, weeks<{W})'; sfs='FTN charting n_defense_box'
        else:
            hi=set(SH[SH['Man Rate']>=MANMED].ab); vs=[(stat(r.gsis,x,r.market),(P[(P.game_id==x)&(P.posteam==t)].defteam.iloc[0] in hi)) for x in same]
            hv=[v for v,i in vs if i]; lv=[v for v,i in vs if not i]; ohi=o in hi; bv=hv if ohi else lv; allv=[v for v,_ in vs]
            sf=bool(bv) and ((np.mean(bv)>=np.mean(allv)) if over else (np.mean(bv)<=np.mean(allv))); sfd=f"opp {'high' if ohi else 'low'}-man ({sh.get('Man Rate')}%); player avg vs that bucket {np.mean(bv) if bv else 'n/a'} vs all {np.mean(allv) if allv else 'n/a'}"
            sfs=covsrc+' x pbp splits (PROXY)'
        if r.market=='rushyds': sc=(r.team_spread<0) if over else (r.team_spread>0)
        else: sc=(r.team_spread>0 or (tot or 0)>=46) if over else (r.team_spread<0 and (tot or 99)<46)
        scd=f'team spread {r.team_spread:+g}, total {tot}'
        if len(vals)>=2:
            l2,l4m=np.mean(vals[-2:]),np.mean(vals[-4:]); ft=(l2>=l4m and l2>r.line) if over else (l2<=l4m and l2<r.line); ftd=f'last2 {l2:.1f} vs last4 {l4m:.1f} vs line {r.line:g}'
        else: ft=False; ftd='fewer than 2 current-QB games'
        se=dict(matchup=dict(ok=bool(mt),source='nflverse pbp (credit PROXY)' if rec and prim else 'nflverse pbp allowance',detail=md),
                scheme_fit=dict(ok=bool(sf),source=sfs,detail=sfd),script=dict(ok=bool(sc),source=f'The Odds API snapshot {ts_odds}',detail=scd),
                form_trend=dict(ok=bool(ft),source='nflverse pbp',detail=ftd))
        if all(v['ok'] for v in se.values()): se['explanation']=f"AUTO-GENERATED (harness, not analyst): {md}; {sfd}; {scd}; {ftd}."
        L['scheme_edge']=se
        legs.append(L)
        for k in MOD: sims[k]['legs'][name]=dict(p=round(float(r.p[k]),4),median=round(float(r.med[k]),2))
        LEGROWS.append(dict(L,week=W,game_id=gid,now=fmt(now),p_avg=float(np.mean(list(r.p.values()))),meds=list(r.med.values())))
    # target share pool
    names=[l['name'] for l in legs]
    pool=[]
    for p_ in tsp_pool:
        lg=[n for n in names if n.startswith(p_['name'])]; pool.append(dict(name=p_['name'],team=p_['team'],share=p_['share'],**({'leg':lg[0]} if lg else {'skip_reason':'no line posted / not matched at book'})))
    dep=[]
    for t in (h,a):
        if len(cbs_out[t])>=2:
            off=a if t==h else h; c=[]
            for rk in (2,3):
                l4=team_games(off,W)[-4:]; q=pa[(pa.game_id.isin(l4))&(pa.posteam==off)&(pa.pg=='WR')].receiver_player_id.value_counts()
                if len(q)>=rk:
                    nm=NAME.get(q.index[rk-1]); lg=[n for n in names if n.startswith(str(nm)) and ' over ' in n and (' rec ' in n or 'recyds' in n)]
                    c.append(dict(name=nm,wr_rank=rk,**({'leg':lg[0]} if lg else {'skip_reason':'no over line'})))
            dep.append(dict(team=t,cbs_out=cbs_out[t],wr23_over_pool=c,source='ESPN game injuries + nflverse weekly report'))
    # game script RB block
    fav=h if (hsp or 0)<0 else a; fs=-abs(hsp) if hsp is not None else 0.0; E=engine(W)
    try: oy=float(S.opp_rb_ypc(E,a if fav==h else h))
    except Exception: oy=0.0
    trig=bool(wxflag or (fs<=-7 and oy>=4.4))
    gs=dict(fav_spread=fs,opp_ypc=round(oy,3),wx_flag=bool(wxflag),triggered=trig,source=f'odds snapshot {ts_odds} + sim_v6.opp_rb_ypc',pulled_et=stamp,team=fav)
    if trig:
        l4=team_games(fav,W)[-4:]; q=ru[(ru.game_id.isin(l4))&(ru.posteam==fav)&(ru.pg=='RB')].rusher_player_id.value_counts()
        if len(q)>=2:
            try:
                out=S.price_game_script(E,dict(team=fav,opp=(a if fav==h else h),fav_spread=fs,opp_ypc=oy,wx_flag=wxflag,lead=dict(player=q.index[0],market='rushyds',line=None),rb2=dict(player=q.index[1],market='rushyds'),
                    other_legs=[dict(player=l['gsis'],market=l['market']) for l in legs if l['team']==fav]))
                gs.update(boost=dict(lead=out['lead'] if isinstance(out['lead'],float) else out['lead'].get('boost'),rb2=out['rb2'].get('boost'),source=out['source']),lead_rb=NAME.get(q.index[0]),rb2=NAME.get(q.index[1]),
                          rb2_projection=dict(median=out['rb2']['median']),model_order=out['model_order'])
            except Exception as ex: gs['error']=str(ex)
    # manifest
    def src(cat,name,f,dw,kind,true):
        return dict(category=cat,name=name,url_or_file=f,pulled_et=stamp,season=2026,data_week=dw,week_kind=kind,true_asof=true,label='REPLAY STAMP')
    sources=[src('core_stats_pbp','nflverse pbp',f'{SRC}/play_by_play_2026.parquet',W-1,'through',f'through week {W-1}'),
             src('coverage_matchups','pbp defender credit PROXY + Sharp coverage schemes (HINDSIGHT wk6-7)','/tmp/sharp.html',W-1,'through','2026-10-27 (Sharp); pbp through week %d'%(W-1)),
             src('ngs','NFL NGS passing/receiving (nflverse)',f'{ROOT}/runs/2026-11-01_shared_src/ngs_passing.parquet',W-1,'through',f'weeks<{W} used'),
             src('injuries_news','nflverse weekly injury report + ESPN game injuries/inactives',f'/tmp/inj26.parquet ; espn/{ESP.get((a,h,min(W,8)))}.json',W,'label','ESPN summary fetched post-game (inactives published ~90m pre-kick)'),
             src('weather','Open-Meteo',wxe['source'],W,'label','archive pulled after the fact'),
             src('odds_props','The Odds API historical snapshot',f'{HERE}/raw/',W,'label',f'snapshot {ts_odds} UTC')]
    # NOTE: no film source -> real missing data (no film review can be reconstructed for a replay)
    m=dict(season=2026,week=W,game_id=gid,game=game,kickoff_et=fmt(et(ko)),game_date=fmt(et(ko))[:10],input_cutoff_et=stamp,seed=S.SEED,trials=100000,sim_script='tools/sim_v6.py',
           sources=sources,flagged_gaps=[],
           pressure_inputs={k:dict(value={t:v.get(t) for t in (h,a)},label=lab,source=s_,pulled_et=stamp,true_asof=f'weeks<{W}') for k,v,lab,s_ in (
               ('blitz_rate',bl,'FTN n_blitzers/n_pass_rushers (defense)','FTN charting 2026'),('pressure_rate',pr,'PROXY sack|qb_hit per dropback (defense)','nflverse pbp'),
               ('checkdown_share',ck,'FTN read_thrown==CHK share (offense)','FTN charting 2026'),('time_to_throw',tt,'NGS avg_time_to_throw, attempt-weighted (offense)','NGS passing'),
               ('targets_under_pressure',tup,'PROXY share of targets with qb_hit (offense)','nflverse pbp'))},
           weather={game:wxe},weather_forecast=dict(source='open-meteo previous-runs API',provider='open-meteo',pulled_et=fmt(et(ko)-timedelta(hours=23)),label='REPLAY STAMP (day-1 forecast)',games={game:fce}),
           sims=list(sims.values()),legs=legs,target_share_pool=dict(source='nflverse pbp last 4 team games',players=pool),depleted_secondary=dep,game_script_rb={game:gs})
    d=f"runs/wk{W}_{a}_{h}"; os.makedirs(d,exist_ok=True); json.dump(m,open(f'{d}/run_manifest.json','w'),indent=1,default=str)
    with open(f'{d}/checklist.md','w') as f:
        f.write('| leg | phase | status | detail | source | pulled |\n|---|---|---|---|---|---|\n')
        for l in legs:
            for ph in range(1,16): f.write(f"| {l['name']} | {ph} | N/A | analyst attestation not reconstructable in replay; gate-enforced via manifest fields |  |  |\n")
    open(f'{d}/report.md','w').write(f'# Replay {game} week {W}\nTEST ONLY. Built by backtests/rulebook_replay_wk6_8/build_legs.py.\n\n## Risks\n- No film review (film source missing).\n- Sharp coverage HINDSIGHT for weeks 6-7; defender coverage is a pbp credit PROXY.\n- Alt no-vig is a PROXY.\n')
    # team files (as of week W)
    for t in (h,a):
        td=f'door_out/wk{W}/teams'; os.makedirs(td,exist_ok=True)
        json.dump(dict(team=t,as_of=f'pbp weeks<{W}',man_zone=SHd.get(t),blitz_rate=bl.get(t),pressure_rate=pr.get(t),rb_box=bx.get(t),
                       top_defenders={b:DF[t][b].head(3)[['name','targets','ypt']].to_dict('records') for b in DF[t]},source='replay build_legs.py'),open(f'{td}/{t}.json','w'),indent=1,default=str)
    print(game,W,len(legs),flush=True)
pd.DataFrame(LEGROWS).to_pickle('legs_all.pkl')
