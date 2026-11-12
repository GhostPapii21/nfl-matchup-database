"""[COPIED FORWARD 2026-11-01 21:51 ET for runs dated 2026-11-05+; writes the PRESS block per leg via tools/press_inputs.py]
Assemble per-game run folders for the game-day run (nfl-game-script-run skill, 15 phases).
Usage: python3 assemble.py <odds_tag> --date 2026-11-05 [--suffix _r2]   Never overwrites an existing run folder."""
import json, os, sys, re, math, datetime, subprocess, urllib.request, collections
import pandas as pd, numpy as np
SH=os.path.dirname(os.path.abspath(__file__))+'/'; DB='/workspace/nfl-database/'
TAG=sys.argv[1]; GAME_DATE=sys.argv[sys.argv.index('--date')+1]; WEEK=int(sys.argv[sys.argv.index('--week')+1]) if '--week' in sys.argv else 9; assert GAME_DATE>='2026-11-05', 'this copy is for runs dated 2026-11-05 onward'; SUF=sys.argv[sys.argv.index('--suffix')+1] if '--suffix' in sys.argv else ''
WK=DB+f'week{WEEK}/'   # BUG-2026-11-01-ASM9: was hard-wired to the Week 8 input folder
# --- PREFLIGHT (fail closed before anything loads): every input must be this week's pull; no silent Week 8 fallback
REQ=[SH+f'legs_{TAG}.json',SH+f'sims_{TAG}.json',SH+'features.json',SH+'film_verified.json',SH+'espn_depth_all.json',SH+'weather.json',
     SH+'injuries_parsed.csv',SH+'snap_counts_2026.parquet',SH+'espn_scoreboard.json',SH+'sharp_cov_schemes.md',SH+'pull_times.json',
     SH+'inactives.json',SH+'placed_slips.json',WK+f'sources/espn_wrcb_wk{WEEK}.json',WK+'phase_walk/src/espn_box.json',WK+'phase_walk/src/pbp25.parquet',SH+'qb_pressure.json']  # qb_pressure.json: {team:{time_to_throw,targets_under_pressure}, source, pulled_et} (lesson 5)
REQ+=[SH+'feed_stamps.json']   # SRC-5: per-feed season/data_week/pulled_et (tools/feed_week_check.py)
REQ+=[SH+'feed_stamps.json']   # SRC-5 srclist: per-feed stamps (tools/feed_week_check.py)
_miss=[f for f in REQ if not os.path.exists(f)]
# BUG-2026-11-01-WXDAYS (Rico): multi-day forecast from tools/weather_forecast.py must exist; run_gate fails it if > 24h old
sys.path.insert(0,DB+'tools'); import weather_forecast as WFC
FCP=WFC.latest(WK+'weather_forecast/')
if not FCP: sys.exit('PREFLIGHT FAIL: no weather forecast in '+WK+'weather_forecast/ (run: python3 tools/weather_forecast.py --week '+str(WEEK)+')')
FC=json.load(open(FCP))
if _miss: sys.exit('PREFLIGHT FAIL (no run folders written). Missing inputs:\n  '+'\n  '.join(_miss))
sys.path.insert(0,DB+'tools'); import feed_week_check as _FW
_fw=_FW.check(SH,season=2026,week=WEEK)
if not _fw['ok']: sys.exit('PREFLIGHT FAIL (SRC-5 feed weeks; no run folders written):\n  '+'\n  '.join(f"{k}: {'; '.join(v['problems'])}" for k,v in _fw['feeds'].items() if v['status']=='FAIL'))
sys.path.insert(0,DB+'tools'); import feed_week_check as _FW   # SRC-5 srclist
_fw=_FW.check(SH,season=2026,week=WEEK)
if not _fw['ok']: sys.exit('PREFLIGHT FAIL (SRC-5 feed weeks; no run folders written):\n  '+'\n  '.join(f"{k}: {'; '.join(v['problems'])}" for k,v in _fw['feeds'].items() if v['status']=='FAIL'))
_sm=json.load(open(SH+f'sims_{TAG}.json'))['meta']; SIMP=str(_sm.get('script',''))
if not SIMP.endswith('sim_v6.py'): sys.exit(f'PREFLIGHT FAIL: sims_{TAG}.json meta.script={SIMP!r}; runs dated >= 2026-11-05 must be priced by tools/sim_v6.py (BUG-2026-11-01-SIMV6)')
sys.path.insert(0,SH); import sim_v5 as S   # feature helpers only (pbp frames, pid); pricing comes from sims_{TAG}.json (sim_v6)
sys.path.insert(0,DB+'tools'); import press_inputs as PRI
import depth_wiring as DW   # Ghost6 audit 2026-11-03: N1 RB-only/current-QB, depth fields, zone coverage allowance, slot/primary
import rico4_rules as R4   # Rico 2026-11-02 05:01 ET R1-R4 (runs >= 2026-11-05)
def _roster_pos():
    try: x=pd.read_parquet(SH+'players.parquet',columns=['gsis_id','position']); return dict(zip(x.gsis_id,x.position))
    except Exception: return {}   # pool then lists nobody as WR/TE; gate still needs the block (fail-visible)
_ld=lambda f:json.load(open(SH+f)) if os.path.exists(SH+f) else None
INACTIVES=_ld('inactives.json')   # list of player names from the posted inactives (required by PREFLIGHT)
PLACED=_ld('placed_slips.json')   # players already on placed slips/tickets (§11) (required by PREFLIGHT)
D=json.load(open(SH+f'legs_{TAG}.json')); SM=json.load(open(SH+f'sims_{TAG}.json')); F=json.load(open(SH+'features.json'))
FILM=json.load(open(SH+'film_verified.json')); DEP=json.load(open(SH+'espn_depth_all.json')); WR=json.load(open(WK+f'sources/espn_wrcb_wk{WEEK}.json'))
BOX=json.load(open(WK+'phase_walk/src/espn_box.json')); WX=json.load(open(SH+'weather.json'))
INJ=pd.read_csv(SH+'injuries_parsed.csv'); SNP=pd.read_parquet(SH+'snap_counts_2026.parquet')
PFR=pd.read_html('/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html')[0]; PFR.columns=[c[1] for c in PFR.columns]; PFR=PFR[PFR.Player!='Player']
NV={'LAR':'LA','WSH':'WAS'}; nv=lambda t:NV.get(t,t)
PFRT={'LAR':'LAR','WSH':'WAS','LAC':'LAC','JAX':'JAX','ARI':'ARI'}
T=dict(json.load(open(SH+'pull_times.json')),odds=D['odds_pulled'],lines=D['lines_pulled'])   # was hard-coded 2026-11-01 times
PFR_SRC='/workspace/nfl-sim/mnf12/pfr_def_adv_2026.html'
EXC={"input":"coverage.defenders","source":PFR_SRC,"approved_by":"Rico","approved_on":"2026-11-01","valid_for_date":"2026-11-01","scope":"receiving legs","reason":"misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only"}
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
# --- Sharp coverage schemes (Updated: October 27)
SHARP={}; FULL2AB={}
sb=json.load(open(SH+'espn_scoreboard.json'))
for e in sb['events']:
    for c in e['competitions'][0]['competitors']: FULL2AB[c['team']['displayName']]=c['team']['abbreviation']
for l in open(SH+'sharp_cov_schemes.md'):
    m=re.match(r'\| ([A-Z][\w .]+?) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|',l)
    if m and m.group(1) in FULL2AB: SHARP[FULL2AB[m.group(1)]]=dict(man=float(m.group(2)),zone=float(m.group(3)),mof_closed=float(m.group(4)),mof_open=float(m.group(5)))
SHARP_URL='https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/'
def inj(team,name):
    x=INJ[(INJ.ab==team)&(INJ.name==name)]
    return (x.status.iloc[0],str(x.det.iloc[0]) if x.det.iloc[0]==x.det.iloc[0] else '') if len(x) else ('Active','')
BADST={'Out','Doubtful','Injured Reserve','IR','Suspension'}
def pfr(name,team):
    x=PFR[PFR.Player==name]
    if len(x)>1: x=x[x.Team==PFRT.get(team,team)]
    if not len(x): return None
    r=x.iloc[0]; f=lambda k:(None if pd.isna(pd.to_numeric(r[k],errors='coerce')) else float(r[k]))
    return dict(name=name,team=r.Team,pos=r.Pos,targets=f('Tgt'),completions=f('Cmp'),comp_pct=f('Cmp%'),yds=f('Yds'),ypt=f('Yds/Tgt'),rating=f('Rat'),source=PFR_SRC,pulled_et=T['pfr'])
def remap(def_team,name):
    for posk in ['nb','lcb','rcb','ss','fs']:
        lst=DEP.get(def_team,{}).get(posk,[])
        if name in lst:
            for n in lst[lst.index(name)+1:]:
                if inj(def_team,n)[0] not in BADST: return n,posk
    return None,None
OEMB=json.load(open(SH+'oembed.json')) if os.path.exists(SH+'oembed.json') else {}
def oembed(url):
    if url in OEMB: return OEMB[url]
    try: c=urllib.request.urlopen('https://www.youtube.com/oembed?format=json&url='+url,timeout=15).getcode(); t=json.loads(urllib.request.urlopen('https://www.youtube.com/oembed?format=json&url='+url,timeout=15).read()).get('title','')
    except Exception as ex: c,t=str(ex)[:40],''
    OEMB[url]=dict(code=c,title=t,checked=f'{datetime.datetime.now():%Y-%m-%dT%H:%M}'); json.dump(OEMB,open(SH+'oembed.json','w'),indent=0); return OEMB[url]
FILMTEAM={'LAR':'LAR','WSH':'WSH'}
def film_for(name,team):
    first,last=name.replace(' Jr.','').replace(' III','').replace(' II','').split()[0],name.replace(' Jr.','').replace(' III','').replace(' II','').split()[-1]
    keys=[name,f'{first[0]}.{last}',f'{first[0]}. {last}',name.replace(' Jr.','').replace(' III','').replace(' II','')]
    out=[]
    for k,v in FILM.items():
        parts=[x.strip() for x in re.split(r';| to ',k)]
        if any(p in keys for p in parts):
            for r in v:
                if r['team'] in (team,nv(team),{'ARI':'ARZ'}.get(team,team)) and f'{first[0]}.{last}' in r['desc'].replace(' ',''): out.append(r)
    return out
# --- team-level helpers
p=S.p; tg=S.tg
def team_games(team): return tg[tg.posteam==nv(team)].sort_values('date')
def qb_dates(team,qid):
    db=p[(p.posteam==nv(team))&(p.qb_dropback==1)].copy(); db['q']=db.passer_player_id.fillna(db.rusher_player_id)
    top=db.groupby('game_date').q.agg(lambda x:x.value_counts().index[0]); return [str(d)[:10] for d,q in top.items() if q==qid]
def last_qb(team):
    db=p[(p.posteam==nv(team))&(p.qb_dropback==1)]; lg=db.game_date.max(); x=db[db.game_date==lg]
    pid=x.passer_player_id.fillna(x.rusher_player_id).value_counts().index[0]; return pid
QBCARD=F['qbs']
def snaps(name,team):
    x=SNP[(SNP.player==name.replace(' Jr.','').replace(' III','').replace(' II',''))|(SNP.player==name)]; x=x[x.team==nv(team)].sort_values('week')
    return x.tail(2)[['week','offense_pct']].values.tolist()
pbp25=pd.read_parquet(WK+'phase_walk/src/pbp25.parquet',columns=['season','receiver_player_id','receiver_player_name','posteam','game_id','pass_attempt','sack','receiving_yards','season_type'])
TEAM_OL={}
for t in set(INJ.ab):
    x=INJ[(INJ.ab==t)&INJ.pos.isin(['OT','T','G','C','OL'])&INJ.status.isin(['Out','Doubtful'])]; TEAM_OL[t]=x[['name','pos','status']].values.tolist()
def kickhour(ko): h,m=map(int,ko.split()[0].split(':')); return h+12 if 'PM' in ko and h!=12 else h
def wind(home,ko):
    w=WX[home]; kh=kickhour(ko); hrs=[r for r in w['nws'] if kh<=int(r['t'][11:13])<kh+4]
    ws=[int(re.findall(r'\d+',r['wind'])[-1]) for r in hrs] if hrs else []
    om=[r for r in w['om']]; return w['roof'],ws,hrs,w['nws_url'],w['om_url']
RECHECK=lambda ko:'11:30 AM' if ko.startswith('01:00') else ('2:35 PM' if ko.startswith('04') else '6:50 PM')
def fmt(x,n=1): return 'NA' if x is None or (isinstance(x,float) and x!=x) else f'{x:.{n}f}'
# --- main per-leg evaluation
def evaluate(L):
    sm=SM['sims'][f"{L['player']}|{L['market']}"]; sims=sm['sims']; info=sm['info']
    fd=L['fd']; main=fd['point']; mk=L['market']; pos=L['pos']; team,opp=L['team'],L['opp']; spread=L['spread']
    st,stn=inj(team,L['player'])
    def P(side,line): 
        ps=[sims[m]['rungs'][str(float(line))] for m in ('mc','bias','gr')]
        return ps if side=='Over' else [1-x for x in ps]
    # side choice at main
    if L['explicit']: side='Over'
    else:
        eo=np.mean(P('Over',main))-fd['nv_over']; eu=np.mean(P('Under',main))-fd['nv_under']; side='Over' if eo>=eu else 'Under'
    line,price,nvp,rung_note=main,(fd['over'] if side=='Over' else fd['under']),(fd['nv_over'] if side=='Over' else fd['nv_under']),'FD main'
    if L.get('fdbook','fanduel')!='fanduel': rung_note=f"{L['fdbook']} main (no FanDuel line posted: FD price MISSING)"
    lower_reason=[]
    FORCE=L.get('force')
    if FORCE is not None:
        side='Over'; line=float(FORCE); fb=L.get('fdbook','fanduel')
        if line==main: price=fd['over']; nvp=fd['nv_over']; rung_note=f"{fb} main at the slip line"
        elif str(line) in L['alts']: price=int(L['alts'][str(line)]); nvp=imp(price)/fd['overround']; rung_note=f"FD alt {line:g} (no-vig via main-market overround)"
        else:
            alt=[(b,x) for b,x in (('Pinnacle',L.get('pin')),('DK',L.get('dk'))) if x and x['point']==line]
            if alt: price=alt[0][1]['over']; nvp=alt[0][1]['nv_over']; rung_note=f"no FD price at {line:g}; {alt[0][0]} two-way no-vig used"
            else: price=0; nvp=float('nan'); rung_note=f'no FD/Pinnacle/DK price at the slip line {line:g} (DFS-only line): no-vig MISSING'

    _qc=QBCARD.get(last_qb(team),{})
    if side=='Over' and _qc.get('grades',{}).get('money_downs')=='F' and (mk=='passyds' or (pos=='TE' and mk=='rec')): lower_reason.append('QB money-down grade F (§15: drop one rung)')
    if side=='Over' and spread<=-8.5: lower_reason.append(f'projected margin {-spread:+.1f} >= 8.5 (Phase 13 lower alt rung)')
    if side=='Over' and st=='Questionable': lower_reason.append('player Questionable (Phase 8 lower rung)')
    if lower_reason and FORCE is None:
        below=sorted([float(a) for a in L['alts'] if float(a)<main])
        if below: line=below[-1]; price=int(L['alts'][str(line)]); nvp=imp(price)/fd['overround']; rung_note=f'FD alt {line} (one rung below main {main}): '+'; '.join(lower_reason)
        else: rung_note='no lower FD alt rung available: '+'; '.join(lower_reason)
    _wr_rank=None
    ps=P(side,line); meds=[sims[m]['median'] for m in ('mc','bias','gr')]; avg=float(np.mean(ps)); shr=avg  # NOSHRINK Rico 2026-11-02 21:13 ET: raw model p, no 30% shrink
    name=f"{L['player']} {L['label']} {side} {line:g}"
    R={}; src_pbp='nflverse play_by_play_2026.parquet wk1-8 (thru 2026-10-29)'
    log=info['log']; l3=log[-3:]; l4=log[-4:]
    # Phase 1
    lg=', '.join(f"{g['date'][5:]} {g['tgt']}t/{g['rec']}r/{g['ry']:.0f}y/{g['car']}c/{g['rush']:.0f}ry" for g in l3)
    R[1]=('PASS' if info['n_games']>=3 else 'FAIL',f"{info['n_games']} games; last3 {lg}",src_pbp+' + nflverse snap_counts + ESPN depth API',T['pbp'])
    # Phase 2 opportunity
    tgm=team_games(team); mm=float(tgm.margin.mean()); pa_proj=float(tgm.pa.mean()*math.exp(S.bP*(-spread-mm))); ra_proj=float(tgm.ra.mean()*math.exp(S.bR*(-spread-mm)))
    sh3=sum(g['tgt'] for g in l3)/max(sum(g['pa'] for g in l3),1); csh3=sum(g['car'] for g in l3)/max(sum(g['ra'] for g in l3),1)
    ptg=pa_proj*sh3; prec=ptg*info['cr']; pcar=ra_proj*csh3; mc_mean=sims['mc']['mean']
    if pos in('WR','TE'):
        T3=p[(p.posteam==nv(team))&(p.game_id.isin(tgm.game_id.tail(3)))&(p.pass_attempt==1)&(p.sack!=1)]
        rk=T3.receiver_player_id.value_counts(); rank=list(rk.index).index(S.pid(L['player'],nv(team)))+1 if S.pid(L['player'],nv(team)) in rk.index else 99
        if pos=='WR' and rank!=99: _wr_rank=rank   # target rank among ALL team receivers last 3 (>= WR-only rank, so conservative); 99 = not found -> MISSING
        dmap=dict(zip(tgm.date.astype(str),tgm.game_id)); wk=[int(dmap[g['date'][:10]][5:7]) for g in l3]; pbpt=[g['tgt'] for g in l3]
        esp=[BOX.get(f"{L['player'].replace(' Jr.','') if L['player']=='Chris Godwin Jr.' else L['player']}|{w}",{}).get('tg') for w in wk]
        two=all(e is not None for e in esp) and all(abs(int(e)-int(a))<=1 for e,a in zip(esp,pbpt))
        mates=[(k.split('|')[0],v['share']) for k,v in F['recv'].items() if k.endswith('|'+team) and v['pos']==pos and k.split('|')[0]!=L['player'] and v['share']>=0.28]
        num=f"rank {rank} by tgt last3 (pbp {pbpt}; ESPN box {esp}); proj {pa_proj:.1f} pa x {sh3:.3f} = {ptg:.1f} tgt x cr {info['cr']:.2f} = {prec:.1f} rec; MC mean {mc_mean:.1f}"
        if side=='Under': stt='PASS'; num+=' (under: volume recorded)'
        else:
            fails=[]
            if rank>2: fails.append(f'not top-2 target earner (#{rank})')
            if mk=='rec':
                if sum(g['tgt']>=5 for g in l4)<3: fails.append('5+ tgt in <3 of last 4')
                if mates: fails.append(f'same-role teammate >=28%: {mates}')
                if prec<line: fails.append(f'proj rec {prec:.1f} < {line}')
            else:
                if not all(g['tgt']>=4 for g in l3): fails.append('not 4+ tgt in each of last 3')
                if mc_mean<line: fails.append(f'proj yds {mc_mean:.1f} < {line}')
            stt='FAIL' if fails else 'PASS'
            if not fails and L['explicit'] and not two: stt='UNVERIFIED'; fails.append('ESPN box does not confirm pbp targets (two-source rule for regrade legs)')
            if fails: num+=' | '+'; '.join(fails)
        R[2]=(stt,num,src_pbp+(' + ESPN box scores (espn_box.json)' if True else ''),T['pbp'] if not L['explicit'] else T['box'])
    elif pos=='RB':
        T3=p[(p.posteam==nv(team))&(p.game_id.isin(tgm.game_id.tail(2)))&(p.rush_attempt==1)]; top=T3.rusher_player_id.value_counts().index[0]
        prim=top==S.pid(L['player'],nv(team))
        num=f"proj {ra_proj:.1f} ra x {csh3:.3f} = {pcar:.1f} car; {ptg:.1f} tgt; MC mean {mc_mean:.1f}; primary back last2: {prim}"
        stt='PASS' if (side=='Under' or (prim and mc_mean>=line)) else 'FAIL'
        R[2]=(stt,num+('' if stt=='PASS' else ' | not primary back or proj < line'),src_pbp,T['pbp'])
    else:
        qb=last_qb(team)==S.pid(L['player'],nv(team)); num=f"starter by dropbacks last game: {qb}; proj {pa_proj:.1f} pa; MC mean {mc_mean:.1f}"
        R[2]=('PASS' if qb and (side=='Under' or mc_mean>=line) else 'FAIL',num,src_pbp,T['pbp'])
    # Phase 3 defense
    dt=F['teams'][opp]; num=(f"{opp}: pass {dt['pass_yds_pg']:.0f} y/g ({dt['comp_pg']:.1f}/{dt['att_pg']:.1f}), rush {dt['rush_yds_pg']:.0f} y/g, RB YPC {dt['rb_ypc']:.2f}; YPT WR {dt['ypt_WR']:.2f} (n{dt['n_WR']}) TE {dt['ypt_TE']:.2f} (n{dt['n_TE']}) RB {dt['ypt_RB']:.2f}, RB YPT QB-adj {dt['rb_ypt_qbadj']:+.2f}; "
         f"WR outside/middle YPT PROXY {dt['wr_outside_ypt_proxy']:.2f}/{dt['wr_middle_ypt_proxy']:.2f}; expl rec20 WR {dt['expl_rec20_WR_pg']:.2f}/g RB {dt['expl_rec20_RB_pg']:.2f}/g, rush15 {dt['expl_rush15_pg']:.2f}/g; pts {dt['pts_pg']:.1f}/g; 3D conv allowed {dt['third_down_conv_allowed']:.3f}")
    f3=[]
    if side=='Over' and pos=='TE' and dt['ypt_TE']<=5.5: f3.append('TE YPT allowed <=5.5 hard')
    if side=='Over' and mk=='rushyds' and dt['rb_ypc']<=3.8: f3.append('RB YPC allowed <=3.8 suppression')
    if side=='Under' and pos=='WR' and dt['ypt_WR']>=9.0: f3.append('under vs soft WR D (YPT>=9.0)')
    if side=='Under' and pos=='TE' and dt['ypt_TE']>=8.0: f3.append('under vs soft TE D (YPT>=8.0)')
    if side=='Under' and mk in('rushyds','rushrec') and dt['rb_ypc']>4.4: f3.append('under vs soft run D (YPC>4.4)')
    if side=='Under' and mk in('passyds','comp') and dt['pass_yds_pg_rank']<=8: f3.append(f"under vs top-8 pass yds allowed (rank {dt['pass_yds_pg_rank']})")
    R[3]=('FAIL' if f3 else 'PASS',num+(' | '+'; '.join(f3) if f3 else ''),src_pbp,T['pbp'])
    # Phase 4 defender coverage
    sc=SHARP.get(opp); mz=dict(value=f"man {sc['man']}% / zone {sc['zone']}%",source=SHARP_URL+' (Firecrawl; data Updated Oct 27)',pulled_et=T['sharp']); mof=dict(value=f"MOF closed {sc['mof_closed']}% / open {sc['mof_open']}%",source=SHARP_URL+' (Firecrawl; data Updated Oct 27)',pulled_et=T['sharp'])
    cov=None; defs=[]
    if pos=='WR':
        key=L['player'].replace(' Jr.','') if L['player']=='Chris Godwin Jr.' else L['player']
        w=WR.get(key) or WR.get(L['player'])
        if not w: R[4]=('MISSING',f'no ESPN WR/CB cheatsheet mapping for {L["player"]}; no stand-in allowed',f'ESPN NFL26_CS_WRCB (wk{WEEK})',T['wrcb'])
        else:
            _sp=DW.slot_primary(w,DEP.get(opp,{}),healthy=lambda n:inj(opp,n)[0] not in BADST)   # (e) slot/primary chart, not WR rank -> CB rank
            d0=_sp['name']; s0=inj(opp,d0)[0]; d1=d0; note=f"cheatsheet: {L['player']} ({w['pos']}: L{w['lwr']}/S{w['slot']}/R{w['rwr']}%) vs {d0} [{_sp['basis']}]"
            if s0 in BADST:
                d1,pk=remap(opp,d0); note+=f" [{d0} {s0} -> remapped via ESPN depth {pk}: {d1}]"
            elif s0=='Questionable': note+=f' [{d0} Questionable: re-check Phase 15]'
            pr=pfr(d1,opp) if d1 else None
            if not pr: R[4]=('MISSING',note+' | defender not in PFR cache','PFR advanced defense cache '+PFR_SRC,T['pfr'])
            else:
                defs=[pr]; cov=dict(defenders=defs,man_zone=mz,mof=mof)
                note+=f" | PFR {pr['name']}: {pr['targets']:.0f} tgt, {pr['comp_pct']}% cmp, {pr['ypt']} YPT, rtg {pr['rating']} | {mz['value']}, {mof['value']}"
                margin=(prec/line-1) if mk=='rec' else (mc_mean/line-1)
                f4=[]
                if pr['targets']<8: R[4]=('UNVERIFIED',note+f" | defender sample {pr['targets']:.0f} tgt < 8: too thin to grade",'PFR cache '+PFR_SRC+' + ESPN WRCB + Sharp',T['pfr'])
                else:
                    if side=='Over' and mk=='rec' and pr['comp_pct']<55 and margin<0.2: f4.append(f'rec over vs {pr["comp_pct"]}% cmp allowed, volume margin {margin:+.0%} < 20%')
                    if side=='Over' and mk=='recyds' and pr['ypt']<6.0 and margin<0.2: f4.append(f'yds over vs {pr["ypt"]} YPT allowed, margin {margin:+.0%} < 20%')
                    if side=='Under' and mk=='recyds' and pr['ypt']>10: f4.append('yds under vs YPT>10 defender')
                    if side=='Under' and mk=='rec' and pr['comp_pct']>75: f4.append('rec under vs cmp%>75 defender')
                    R[4]=('FAIL' if f4 else 'PASS',note+(' | '+'; '.join(f4) if f4 else f' | volume margin {margin:+.0%}'),'PFR cache '+PFR_SRC+' (Rico exception) + ESPN WRCB cheatsheet + ESPN depth + Sharp coverage schemes',T['pfr'])
    elif pos=='TE': R[4]=('UNVERIFIED',f"TE defender mapping not ruled (ISS-05); {mz['value']}, {mof['value']}; no stand-in allowed",'Sharp coverage schemes; PFR cache',T['sharp'])
    elif mk=='rushrec': R[4]=('UNVERIFIED',f"RB receiving defender mapping: no LB/S alignment source; {mz['value']}, {mof['value']}; awaiting ruling","Sharp coverage schemes",T['sharp'])
    elif mk=='rushyds': R[4]=('N/A','pure rushing leg: no coverage defender','n/a','')
    else:
        cbs=[pfr(n,opp) for k in ('lcb','rcb','nb') for n in DEP.get(opp,{}).get(k,[])[:1]]
        txt='; '.join(f"{c['name']} {c['targets']:.0f}t {c['comp_pct']}% {c['ypt']} YPT" for c in cbs if c)
        R[4]=('PASS',f"QB leg vs {opp} secondary: {txt} | {mz['value']}, {mof['value']}",'PFR cache '+PFR_SRC+' + ESPN depth + Sharp',T['sharp'])
        defs=[c for c in cbs if c]; cov=dict(defenders=defs,man_zone=mz,mof=mof)
    # Phase 5 pressure
    qid=last_qb(team); qc=QBCARD.get(qid,{}); ng=F['ngs'].get(qc.get('name',''),{})
    rv=F['recv'].get(f"{L['player']}|{team}",{})
    pnum=(f"{opp} blitz(5+ rushers) {dt['blitz5']:.1%} (rank {dt['blitz5_rank']}, L4 {fmt(dt['blitz5_l4'] and dt['blitz5_l4']*100)}%), n_blitzers>0 {dt['blitzN']:.1%}; pressure PROXY (sack|hit|scramble)/db {dt['pressure_proxy']:.1%} (rank {dt['pressure_proxy_rank']}); "
          f"QB {qc.get('name')} TTT {fmt(ng.get('ttt'),2)}s (NGS backup), aDOT {fmt(qc.get('adot'))} vs blitz {fmt(qc.get('adot_blitz'))}, behind-LOS {fmt(qc.get('behind_los') and qc['behind_los']*100)}%, checkdown share {fmt(qc.get('checkdown') and qc['checkdown']*100)}%")
    f5=[]; s5='PASS'
    if pos in('WR','TE') or mk=='rushrec':
        if rv:
            pnum+=f"; {L['player']} tgt share all {rv['share']:.1%}, blitzed {rv['share_bl']:.1%} (n{rv['n_bl']}{' LOW-SAMPLE' if rv['n_bl']<15 else ''}) vs not {rv['share_nobl']:.1%}, hit {rv['share_press']:.1%} (n{rv['n_press']}) vs clean {rv['share_clean']:.1%}"
            if side=='Over' and dt['blitz5_rank']<=10 and rv['share_bl']-rv['share_nobl']<-0.04: f5.append('top-10 blitz D and player blitzed share drops >4 pts')
        else: pnum+='; player target-share split unavailable'
    ol=TEAM_OL.get(team,[]); oln=[x for x in ol if x[1] in('OT','T','C')]
    c1,c2,c3=dt['blitz5_rank']<=10,dt['pressure_proxy_rank']<=10,bool(oln); c4=qc.get('grades',{}).get('vs_blitz') in('D','F')
    pan=(c1 or c2 or c3) and c4
    pnum+=f"; Panthers rule: top10 blitz {c1}, top10 pressure PROXY (PRWR not public) {c2}, OL out {oln or 'none'}, QB vs-blitz grade {qc.get('grades',{}).get('vs_blitz')}"
    if mk=='rushyds': s5='N/A'; pnum='pure rushing leg: pressure layer n/a; '+pnum
    elif pan and side=='Over': s5='UNVERIFIED'; f5.append('Panthers rule CAUTION: user decides')
    if mk!='rushyds' and any('blitzed share' in x for x in f5): s5='FAIL'
    R[5]=(s5,pnum+(' | '+'; '.join(f5) if f5 else ''),'nflverse pbp + FTN charting (n_pass_rushers, n_blitzers) + nflverse NGS backup',T['pbp'])
    # Phase 6 QB card
    gr=qc.get('grades',{}); f6=[]
    exp_s=(qc['db']/max(len(team_games(team)),1))*(dt['blitz5']*(qc['vb_sack'] or 0)+(1-dt['blitz5'])*(qc['nb_sack'] or 0)) if qc else 0
    if side=='Over' and mk in('passyds','recyds','rushrec') and gr.get('vs_blitz') in('D','F') and dt['blitz5']>=0.35: f6.append('vs-blitz D/F vs 35%+ blitz D')
    if side=='Over' and mk in('passyds','recyds','rushrec') and gr.get('no_blitz') in('D','F') and dt['blitz5']<0.25: f6.append('no-blitz D/F vs <25% blitz D')
    if side=='Over' and mk=='passyds' and gr.get('protection') in('D','F') and exp_s>=3: f6.append(f'protection D/F with {exp_s:.1f} exp sacks')
    if side=='Over' and spread>0 and gr.get('clutch') in('D','F'): f6.append('clutch D/F: no trailing-script overs')
    if side=='Over' and gr.get('money_downs')=='F' and (mk=='passyds' or (pos=='TE' and mk=='rec')) and line==main: f6.append('money-down F: one rung lower required but no lower FD alt')
    R[6]=('FAIL' if f6 else 'PASS',f"{qc.get('name')} card: vs blitz {gr.get('vs_blitz')} ({fmt(qc.get('vb_cmp') and qc['vb_cmp']*100)}% / {fmt(qc.get('vb_ypa'))} YPA / sack {fmt(qc.get('vb_sack') and qc['vb_sack']*100)}%), no blitz {gr.get('no_blitz')}, protection {gr.get('protection')} (sack {fmt(qc.get('sack_rate') and qc['sack_rate']*100)}%), money downs {gr.get('money_downs')} ({fmt(qc.get('md_conv') and qc['md_conv']*100)}%), clutch {gr.get('clutch')}; exp sacks {exp_s:.1f}"+(' | '+'; '.join(f6) if f6 else ''),'nflverse pbp + FTN charting (§15 card, 40+ db QBs)',T['pbp'])
    # Phase 7 role
    f7=[]; s7='PASS'
    if pos=='RB':
        cs=[g['car']/max(g['ra'],1) for g in l4]; num=f"carry share last4 {[round(x,2) for x in cs]}; tgt/g {np.mean([g['tgt'] for g in log]):.1f}"
        if side=='Over' and mk=='rushyds' and sum(x>=0.6 for x in cs)<3: f7.append('rush over needs 60%+ carry share in 3 of last 4')
        if side=='Over' and mk=='rushyds' and spread>0 and np.mean([g['tgt'] for g in log])<4: f7.append('rush-only over on possible trailer needs 4+ tgt/g')
    elif pos in('WR','TE'):
        sn=snaps(L['player'],team); num=f"offense snap% last2 {sn}"
        if len(sn)<2: s7='UNVERIFIED'; num+=' (snap rows missing)'
        elif side=='Over' and not all(x[1]>=0.6 for x in sn): f7.append('snap share <60% in last 2')
        if L['player']=='DJ Moore':
            pid25=S.pid('DJ Moore',nv(team)); x=pbp25[(pbp25.season_type=='REG')&(pbp25.pass_attempt==1)&(pbp25.sack!=1)]
            me=x[x.receiver_player_id==pid25]; tm=me.posteam.mode().iloc[0]; rk=x[x.posteam==tm].receiver_player_id.value_counts(); r25=list(rk.index).index(pid25)+1
            g25=me.groupby('game_id').receiving_yards.sum(); hit=(g25>=54).mean()
            num+=f"; 2025 ({tm}): target rank {r25}, share {len(me)/len(x[x.posteam==tm]):.1%}, 54+ yds in {hit:.0%} of {len(g25)} games; 2026 share {rv.get('share',0):.1%}"
            if r25>2: f7.append('2-season role support fails (2025 not top-2)')
    else: num=f"QB1 by dropbacks; {qc.get('db')} db"
    if f7: s7='FAIL'
    R[7]=(s7,num+(' | '+'; '.join(f7) if f7 else ''),'nflverse snap_counts + pbp'+(' + 2025 pbp' if L['player']=='DJ Moore' else ''),T['pbp'])
    # Phase 8 injuries
    f8=[]; s8='PASS'; num=f"{L['player']}: {st}{' ('+stn+')' if stn else ''}; {team} OL out/doubtful {ol or 'none'}; {opp} secondary/DL out: "+str(INJ[(INJ.ab==opp)&INJ.pos.isin(['CB','S','DE','DT','LB','DL','EDGE'])&INJ.status.isin(['Out','Doubtful'])][['name','pos','status']].values.tolist())
    if st in BADST: f8.append(f'player {st}')
    if st=='Questionable': num+=f' | Q: lower rung ({rung_note}); Phase 15 recheck MANDATORY'
    if side=='Over' and mk=='passyds' and any(x[1] in('OT','T') for x in ol): f8.append('backup OT: no QB yardage over')
    if side=='Over' and mk=='rushyds' and (any(x[1]=='C' for x in ol) or sum(x[1]=='G' for x in ol)>=2): f8.append('C or 2 interior OL out: cap lead-RB rush over')
    if f8: s8='FAIL'
    R[8]=(s8,num+(' | '+'; '.join(f8) if f8 else ''),'ESPN injuries API (site.api.espn.com)',T['inj'])
    # Phase 9 NGS
    pn=F['ngs'].get(L['player'],{})
    if pos in('WR','TE'): num=f"sep {fmt(pn.get('sep'),2)}, cushion {fmt(pn.get('cushion'),2)}, YAC+ {fmt(pn.get('yacoe'),2)}, iAY {fmt(pn.get('iay'),1)}" if pn else f"player below NGS qualifier; QB TTT {fmt(ng.get('ttt'),2)}s"
    elif pos=='RB': num=f"RYOE/att {fmt(pn.get('ryoe_att'),2)}, 8+ box {fmt(pn.get('box8'),1)}%" if pn else 'below NGS rushing qualifier (logged)'
    else: num=f"TTT {fmt(pn.get('ttt'),2)}s, CPOE {fmt(pn.get('cpoe'),2)}, aggr {fmt(pn.get('aggr'),1)}%"
    R[9]=('PASS','BACKUP (nextgenstats.nfl.com on hold per Ghost6): '+num,'nflverse nextgen_stats release ngs_{passing,receiving,rushing}.parquet (season wk0)',T['ngs'])
    # Phase 10 film
    fm=film_for(L['player'],team)
    if fm:
        fm=sorted(fm,key=lambda r:-r['week'])[:2]; oks=[oembed(r['url']) for r in fm]
        good=all(o['code']==200 for o in oks)
        num='; '.join(f"wk{r['week']} {r['url']} @{r['ts']} Q{r['qtr']} {r['clock']} {r['yds']}y = pbp play {r['pbp_play_id']}" for r in fm)
        R[10]=('PASS' if good else 'UNVERIFIED',num+('' if good else ' | YouTube oEmbed check failed'),'Official NFL YouTube highlights (oEmbed-checked) + week'+str(WEEK)+'/film captions re-matched to fresh pbp',oks[0]['checked'])
    else: R[10]=('UNVERIFIED','no cited caption play re-matched a fresh pbp row for this player',f'week{WEEK}/film/*_film.md vs nflverse pbp',T['pbp'])
    # Phase 11 environment
    roof,ws,hrs,nu,ou=wind(L['game'].split('@')[1],L['ko'])
    mx=max(ws) if ws else None; num=f"roof {roof}; NWS game-hour wind {ws} mph, pop {[h['pop'] for h in hrs]}%, {hrs[0]['sf'] if hrs else ''}"
    f11=[]
    if not any(x in roof for x in ('dome','closed','indoor')) and mx is not None and min(ws)>=15 and side=='Over' and mk in('recyds','passyds'): f11.append('sustained wind 15+ mph: cut passing/receiving yardage overs')
    R[11]=('FAIL' if f11 else 'PASS',num+(' | '+'; '.join(f11) if f11 else ''),'api.weather.gov hourly + api.open-meteo.com',T['wx'])
    # Phase 12 source audit
    R[12]=('PASS','all 7 categories logged in run_manifest sources; pull times (ET) from pull_times.json: '+', '.join(f'{k} {v}' for k,v in sorted(T.items()))+' (staleness enforced by run_gate.py)','run_manifest.json sources[]',T['pbp'])
    # Phase 13 game script
    f13=[]; cls='blowout favorite' if spread<=-8.5 else 'moderate favorite' if spread<=-3 else 'toss-up' if abs(spread)<=2.5 else 'underdog'
    if spread>2.5 and side=='Over': f13.append('10G: underdog over BLOCKED (no written trap/elimination exception)')
    if spread>2.5 and side=='Under' and mk not in('rushyds',) and spread>=6.5: f13.append('trailing-team passing/receiving under BLOCKED')
    if spread>2.5 and side=='Under' and mk=='rushrec': f13.append('underdog leg BLOCKED (10G)')
    if spread<=-6.5 and side=='Under' and mk in('rushyds','rushrec'): f13.append('6.5+ favorite rush under vs clock-killing script')
    if spread<=-8.5 and side=='Over' and line==main: f13.append('margin 8.5+: lower alt rung required but none available')
    R[13]=('FAIL' if f13 else 'PASS',f"{team} {spread:+g} ({cls}); total {L['total']}; {rung_note}"+(' | '+'; '.join(f13) if f13 else ''),'FanDuel spread/total via The Odds API',T['lines'])
    # Phase 14 edge
    f14=[]
    if L['bar']: f14.append(f"placed-ticket bar: {L['bar']}")
    if avg-nvp<0.03: f14.append(f'edge {100*(avg-nvp):+.1f} < +3')
    if min(ps)<0.45: f14.append(f'model p {min(ps):.3f} < .45')
    if any((side=='Over' and m<=line) or (side=='Under' and m>=line) for m in meds): f14.append('a model median does not clear the line')
    pin=L.get('pin'); dk=L.get('dk')
    cons=float(np.mean([main]+[x['point'] for x in (pin,dk) if x]))
    ms=mk in('recyds','rushyds','rushrec','passyds') and max(abs(sims['mc']['median']-main),abs(sims['mc']['median']-cons))>=12
    if ms: f14.append(f"MODEL-SUSPECT: MC median {sims['mc']['median']:.1f} vs FD main {main} / book consensus {cons:.1f} (>=12 yds) -> Debugging")
    elif avg-nvp>0.15: ms=True; f14.append(f"MODEL-SUSPECT: edge {100*(avg-nvp):+.1f} pts > +15 implausible vs market (FD {main}, consensus {cons:.1f}; possible role change the history-based sim cannot see) -> Debugging")
    cmpb='; '.join(f"{b} {x['point']} nv {(x['nv_over'] if side=='Over' else x['nv_under']):.3f}" for b,x in (('Pinnacle',pin),('DK',dk)) if x)
    num=f"{side} {line:g} @ {price:+d} ({rung_note}); p mc/bias/gr {ps[0]:.3f}/{ps[1]:.3f}/{ps[2]:.3f} avg {avg:.3f}; FD no-vig {nvp:.3f}; raw edge {100*(avg-nvp):+.1f}; medians {meds[0]:.1f}/{meds[1]:.1f}/{meds[2]:.1f}; {cmpb}; PP {L['pp']} UD {L['ud']}"
    if not L['stack']:
        oth=sorted(set(b for (pl_,m_),b in BARS_ALL.items() if pl_==L['player'] and m_!=mk))
        if oth and not L['bar']: L['stack']='placed ticket on a different stat: '+'; '.join(oth)
    if L['explicit'] and float(L['explicit']['line'])!=line:
        rq=float(L['explicit']['line']); pr=[sims[m]['rungs'].get(str(rq)) for m in ('mc','bias','gr')]
        if None not in pr:
            nvr=L['fd']['nv_over'] if L['fd']['point']==rq else None
            num+=f" | BetGuru requested Over {rq:g}: p mc/bias/gr {pr[0]:.3f}/{pr[1]:.3f}/{pr[2]:.3f} avg {np.mean(pr):.3f}"+(f", FD nv {nvr:.3f}, edge {100*(np.mean(pr)-nvr):+.1f}" if nvr else '')
    if L['stack']: num+=f" | FLAG same-player different-stat stack (user decides): {L['stack']}"+('; DAL game correlation (ARI@DAL tickets)' if L['team'] in ('DAL','ARI') else '')
    _hold=None
    if nvp!=nvp:  # BUGLOG 2026-11-01: re-pull/derive, else HOLD (was: MISSING -> silent CUT)
        import sys as _s; _s.path.insert(0,'/workspace/nfl-database/tools'); from price_hold import resolve_price
        _r=[dict(point=float(k),nv_over=imp(int(v))/fd['overround']) for k,v in (L.get('alts') or {}).items()]+[dict(point=x['point'],nv_over=x['nv_over']) for x in (L.get('pin'),L.get('dk'),fd) if x]
        _hold=resolve_price('over',line,dict(rungs=_r),repull=L.get('repull'))
        if _hold['status']=='DERIVED': num+=f" | conservative derived no-vig {_hold['nv']:.3f} ({_hold['note']}); edge not re-run here so leg stays HOLD"
        if True: f14=['no book price at this rung after re-pull: HOLD (fail-closed)']+[x for x in f14 if 'edge' not in x]
    s14='HOLD' if nvp!=nvp else ('UNVERIFIED' if ms and len(f14)==1 else ('FAIL' if f14 else 'PASS'))
    R[14]=(s14,num+(' | '+'; '.join(f14) if f14 else ''),'FanDuel (price of record) + Pinnacle + DraftKings + PrizePicks + Underdog via The Odds API; sim_v6.py seed 20261101 N=100000 x3',T['odds'])
    # Phase 15
    R[15]=('PASS',f"pre-inactives: {L['player']} {st} at 07:09 ET; inactives/defender/weather/price recheck at {RECHECK(L['ko'])} ET"+(' (MANDATORY: Q)' if st=='Questionable' else ''),'ESPN injuries API + The Odds API',T['inj'])
    bad=[(k,v[0],v[1].split(' | ')[-1]) for k,v in R.items() if v[0] in('FAIL','MISSING','STALE','UNVERIFIED')]
    status='CUT' if bad else ('HOLD' if s14=='HOLD' else 'PASS')
    _key={'recyds':'ry','passyds':'ry','rushyds':'rush','rec':'rec'}.get(mk)
    _cq=last_qb(team); _qd=set(qb_dates(team,_cq))
    _form=[g[_key] for g in log if g['date'][:10] in _qd][-4:] if _key else None
    _press=PRI.build_press(player=L['player'],pos=pos,market=mk,side=side,line=line,meds=meds,phases={k:R[k][0] for k in (3,4,6,11,13) if k in R},
        recent_form=_form,injury_status=st,inactives=INACTIVES,placed_players=PLACED,wr_rank=_wr_rank)
    # R1 (Rico 2026-11-02): PRESS leg cut ONLY by P14 (MODEL-SUSPECT / edge-shrink) -> MANUAL_REVIEW, never live
    _mr=None
    if status=='CUT' and bad and all(k==14 for k,_,_ in bad) and f14 and all(R4.MR_RX.search(x) for x in f14):
        _mr=R4.press_manual_review(dict(press=_press,price_fd=price,no_vig=nvp),[f"P14 {x}" for x in f14],[round(float(x),4) for x in ps])
        if _mr: status='MANUAL_REVIEW'
    # R4 (Rico 2026-11-02): QB back from missing 2+ games, or model built on the backup -> QB-RETURN flag + current-QB recheck; NO rung drop
    _qbr=None
    if pos in ('WR','TE'):
        _td=[str(d)[:10] for d in team_games(team).date]; _has=[d in _qd for d in _td]; _i=len(_has)
        while _i>0 and _has[_i-1]: _i-=1
        _missed=0
        while _i>0 and not _has[_i-1]: _missed+=1; _i-=1
        _missed=_missed if _i>0 or _missed<len(_has) else 0
        _mq=_cq if sum(g['date'][:10] in _qd for g in l4)*2>=len(l4) else 'backup'
        if R4.qb_return(dict(type=pos),current_qb=_cq,qb_missed_before=_missed,model_qb=_mq):
            _qg=[g for g in log if g['date'][:10] in _qd][-4:]
            _qbr=dict(current_qb=str(_cq),qb_missed_before=_missed,model_qb=str(_mq),games=[g['date'][:10] for g in _qg],form_values=_form,
                      sec7=R[7][0] if 7 in R else 'MISSING',note='§7 + recent form rechecked on current-QB games only; no automatic rung drop')
    # ---- Locked Door fields (rules/rulebook.py). Missing data -> field None -> gate/door fail the leg closed with 'missing data'.
    _rf=dict(values=_form,games=[g['date'][:10] for g in log if g['date'][:10] in _qd][-4:],qb=str(_cq),source=src_pbp,pulled_et=T['pbp']) if _form else None
    _POS=_roster_pos(); _cqi=_cq
    _cs=DW.rb_carry_share(p,_POS,nv(team),S.pid(L['player'],nv(team)),_cqi,source=src_pbp) if pos=='RB' else None   # N1 fix: RB carries only, last 4 current-QB games (was csh3 = all rush att, last 3 team games)
    if _cs: _cs['pulled_et']=T['pbp']
    _rbr=None
    if pos=='RB':
        _c4=[x for x in (_cs or {}).get('shares',[]) if x is not None]   # same RB-only / current-QB basis as N1
        _rbr=dict(share60_3of4=sum(x>=0.6 for x in _c4)>=3 if len(_c4)>=3 else None,shares=[round(x,3) for x in _c4],tgt_pg=round(float(np.mean([g['tgt'] for g in log])),2),may_trail=spread>0,source=src_pbp)
    if cov and cov.get('defenders') and R.get(4,('',))[0]=='PASS':   # N2: verified primary = cheatsheet defender, PFR-graded
        cov['defenders'][0]['primary']=True; cov['defenders'][0].setdefault('source',f'ESPN NFL26_CS_WRCB (wk{WEEK}) + PFR '+PFR_SRC)
    _fav=team if spread<0 else (opp if spread>0 else None)
    _sr=dict(expected_winner=_fav,spread=spread,script=cls,source='FanDuel spread/total via The Odds API (Phase 13)',pulled_et=T['lines']) if _fav else None
    _ok=lambda k:R.get(k,('MISSING',))[0]=='PASS'
    _ft=None
    if _form and len(_form)>=2: _ft=all((v>line) if side=='Over' else (v<line) for v in _form[-2:])
    _se=dict(matchup=dict(ok=_ok(3),source=R[3][2] if 3 in R else None,detail=R[3][1][:240] if 3 in R else 'MISSING'),
             scheme_fit=dict(ok=_ok(4),source=R[4][2] if 4 in R else None,detail=R[4][1][:240] if 4 in R else 'MISSING'),
             script=dict(ok=_ok(13),source=R[13][2] if 13 in R else None,detail=R[13][1][:240] if 13 in R else 'MISSING'),
             form_trend=dict(ok=bool(_ft),source=src_pbp,detail=f'last 2 with current QB {(_form or [])[-2:]} vs {line:g}'),
             explanation='')   # REQUIRED plain words: Ghost6 writes it before a SCHEME_EDGE waiver can apply (gate fails closed when empty)
    # (a) depth fields for DEPTH_RECEIVER (Rico 2026-11-02 23:59); missing -> None -> depth_rule fails closed
    _depth=None; _te_rank=None; _pid=S.pid(L['player'],nv(team))
    if pos in ('WR','TE'):
        _ts=DW.target_share(p,nv(team),_pid,_cq,source=src_pbp)
        if pos=='TE': _te_rank=DW.te_rank(p,_roster_pos(),nv(team),_pid,_cq)
        _df=None
        if cov and cov.get('defenders'):
            _c=cov['defenders'][0]; _lg=pd.to_numeric(PFR[PFR.Pos.isin(['CB','DB','LCB','RCB'])&(pd.to_numeric(PFR.Tgt,errors='coerce')>=8)]['Yds/Tgt'],errors='coerce').mean()
            _df=dict(name=_c.get('name'),ypt=_c.get('ypt'),targets=_c.get('targets'),source=_c.get('source') or PFR_SRC); _lgy=float(_lg)
        else: _lgy=None
        _bk='wr_outside_ypt_proxy' if (pos=='WR' and WR.get(L['player']) and float(WR[L['player']].get('slot') or 0)<max(float(WR[L['player']].get('lwr') or 0),float(WR[L['player']].get('rwr') or 0))) else 'wr_middle_ypt_proxy'
        _tv=[v.get(_bk) for v in F['teams'].values() if isinstance(v,dict) and v.get(_bk) is not None]
        _ca=dict(value=F['teams'].get(opp,{}).get(_bk),bucket=_bk,source='features.json teams.'+_bk+' (nflverse pbp)') if F['teams'].get(opp,{}).get(_bk) is not None else None
        _dg=DW.defender_giving(_df,_lgy,zone_pct=(SHARP.get(opp) or {}).get('zone'),coverage_allow=_ca,league_cov=(float(np.mean(_tv)) if _tv else None))
        _depth=dict(script_pass=DW.script_pass(spread,L.get('total'),'FanDuel spread/total via The Odds API (Phase 13)'),target_share=_ts,defender_giving=_dg)
    return dict(depth=_depth,te_rank=_te_rank,rung_label=DW.rung(line,main),recent_form=_rf,carry_share=_cs,rb_role=_rbr,script_read=_sr,scheme_edge=_se,manual_review=_mr,qb_return=_qbr,press=_press,name=name,L=L,side=side,line=line,price=price,nv=nvp,ps=ps,meds=meds,avg=avg,shr=shr,R=R,bad=bad,status=status,cov=cov,sims=sims,info=info,rung_note=rung_note,pin=pin,dk=dk,inj=st)
def clean(s): return str(s).replace('|','/').replace('\n',' ')
def mirrors(E):
    """R2 (Rico 2026-11-02): under cut for soft-D / missing defender / no-unders-on-stars -> mirror over at the lowest alt
    rung that clears the edge rules, then the full phase walk (evaluate with force=rung). Else a logged no_rung_reason."""
    out=[]
    for r in E:
        if r['side']!='Under' or r['status']!='CUT' or not any(R4.mirror_eligible(f"P{k} {m}") for k,s_,m in r['bad']): continue
        L=r['L']; fd=L['fd']; sims=r['sims']; rungs=[]
        for ln in sorted({float(fd['point'])}|{float(a) for a in L['alts']}):
            k=str(float(ln))
            if not all(k in sims[m]['rungs'] for m in ('mc','bias','gr')): continue
            pr=fd['over'] if ln==float(fd['point']) else int(L['alts'].get(str(ln),L['alts'].get(f"{ln:g}",0)) or 0)
            if not pr: continue
            nvp=fd['nv_over'] if ln==float(fd['point']) else imp(pr)/fd['overround']
            rungs.append(dict(line=ln,price=pr,no_vig=nvp,p=[sims[m]['rungs'][k] for m in ('mc','bias','gr')],medians=r['meds']))
        c=R4.mirror_over(dict(name=r['name'],side='under',line=r['line']),rungs)
        if c.get('line') is None: r['mirror']=dict(no_rung_reason=c['no_rung_reason']); continue
        m2=evaluate(dict(L,force=c['line'],explicit=L.get('explicit') or {})); m2['mirror_of']=r['name']; r['mirror']=dict(candidate=m2['name'],line=c['line'])
        out.append(m2)
    return out
def pool_block(TMS,legs):
    """R3: WR/TE >= 22% target share (season or last 3 with current QB), nflverse pbp; #3/#4 WRs flagged depth_receiver (DEPTH_RECEIVER rule)."""
    pls=[]; ex=[]
    for t in TMS:
        x=p[(p.posteam==nv(t))&(p.pass_attempt==1)&p.receiver_player_name.notna()]
        rows=[dict(week=int(w),posteam=t,passer_player_name=q,receiver_player_name=rn) for w,q,rn in zip(x.week,x.passer_player_id,x.receiver_player_name)]
        pos={}; ROSTER_POS=_roster_pos()
        for rn,pid in zip(x.receiver_player_name,x.receiver_player_id): pos.setdefault(rn,ROSTER_POS.get(pid))
        l3=sorted(x.week.unique())[-3:]; tc=x[x.week.isin(l3)].groupby('receiver_player_name').size().sort_values(ascending=False)
        wrk={n:i+1 for i,n in enumerate([n for n in tc.index if pos.get(n)=='WR'])}
        P=R4.target_share_pool(rows,t,last_qb(t),pos,wrk,source=SH+'play_by_play_2026.parquet (nflverse)')
        for pl in P['players']:
            lg=[l['name'] for l in legs if pl['name'].split('.')[-1] in l['player']]
            pl['leg']=lg[0] if lg else None
            if not lg: pl['skip_reason']='added to candidate pool (R3); no FD line in legs file - add leg or log skip before publish'
        pls+=P['players']; ex+=P.get('depth_receivers',[])
    return dict(source='nflverse play_by_play_2026.parquet',pulled_et=T['pbp'],threshold=R4.SHARE_MIN,players=pls,excluded_wr34=[],depth_receivers=ex)
BARS_ALL={(a,b):c for a,b,c in json.load(open(SH+'bars.json'))}
PH={1:'Data pull',2:'Opportunity',3:'Defense profile',4:'Defender coverage',5:'Pressure/blitz/checkdown',6:'QB card',7:'Role',8:'Injuries',9:'NGS',10:'Film',11:'Environment',12:'Source audit',13:'Game script 10G',14:'Models/price/edge',15:'Inactives'}
def sources(oemb_t):
    S_=[dict(category='core_stats_pbp',name='nflverse play_by_play_2026 (thru 2026-10-29)',url_or_file=SH+'play_by_play_2026.parquet',tool='curl (github nflverse release)',pulled_et=T['pbp']),
        dict(category='core_stats_pbp',name='nflverse snap_counts_2026 + players',url_or_file=SH+'snap_counts_2026.parquet',tool='curl',pulled_et=T['pbp']),
        dict(category='core_stats_pbp',name='ESPN depth charts API (24 teams)',url_or_file=SH+'espn_depth_all.json',tool='python urllib',pulled_et=T['depth']),
        dict(category='core_stats_pbp',name='ESPN box scores (season to date) (two-source target check)',url_or_file=WK+'phase_walk/src/espn_box.json',tool='earlier urllib pull (Oct 31)',pulled_et=T['box']),
        dict(category='coverage_matchups',name='FTN charting via nflverse (blitzers, rushers)',url_or_file=SH+'ftn_charting_2026.parquet',tool='curl',pulled_et=T['pbp']),
        dict(category='coverage_matchups',name='Sharp Football coverage schemes (man/zone, MOF; data Updated Oct 27)',url_or_file=SHARP_URL,tool='Firecrawl scrape',pulled_et=T['sharp']),
        dict(category='coverage_matchups',name=f'ESPN WR/CB matchup cheatsheet wk{WEEK}',url_or_file='https://g.espncdn.com/s/ffldraftkit/26/NFL26_CS_WRCB.pdf',tool='curl',pulled_et=T['wrcb']),
        dict(category='ngs',name='BACKUP nflverse nextgen_stats release (nextgenstats.nfl.com on hold)',url_or_file=SH+'ngs_passing.parquet',tool='curl',pulled_et=T['ngs']),
        dict(category='film',name='Official NFL YouTube highlights (oEmbed-checked) + caption plays re-matched to fresh pbp',url_or_file='https://www.youtube.com/@NFL',tool='python urllib oEmbed',pulled_et=oemb_t),
        dict(category='injuries_news',name='ESPN injuries API',url_or_file='https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries',tool='curl',pulled_et=T['inj']),
        dict(category='weather',name='NWS hourly + Open-Meteo',url_or_file='https://api.weather.gov ; https://api.open-meteo.com',tool='python urllib',pulled_et=T['wx']),
        dict(category='odds_props',name='The Odds API: FanDuel main+alt, DraftKings, Pinnacle, PrizePicks, Underdog player props',url_or_file=SH+f'odds_{TAG}.csv',tool='python urllib (The Odds API)',pulled_et=T['odds']),
        dict(category='odds_props',name='The Odds API: FanDuel/DK/Pinnacle spreads+totals',url_or_file=SH+f"lines_{D['lines_tag']}.json",tool='python urllib (The Odds API)',pulled_et=T['lines'])]
    # SRC-5 (Rico 2026-11-01 22:47 ET): stamp every source with season/data_week/week_kind from feed_stamps.json (gate fails closed if absent)
    KEYS=['pbp','snap_counts','espn_depth','espn_box','ftn','sharp','espn_wrcb','ngs','film','injuries','weather','odds_props','odds_props']
    for s,k in zip(S_,KEYS): s.update(_FW.stamp_for(SH,k))
    # SRC-3: Sharp counts only with an agreeing second source (sharp_second_source.json: {name,url_or_file,pulled_et,agrees})
    if os.path.exists(SH+'sharp_second_source.json'): S_[5]['second_source']=json.load(open(SH+'sharp_second_source.json'))
    # SRC-5 srclist (Rico 2026-11-01 22:47 ET): stamp every source with season/data_week/week_kind from feed_stamps.json
    KEYS=['pbp','snap_counts','espn_depth','espn_box','ftn','sharp','espn_wrcb','ngs','film','injuries','weather','odds_props','odds_props']
    for s,k in zip(S_,KEYS): s.update(_FW.stamp_for(SH,k))
    # SRC-3 srclist: Sharp counts only with an agreeing second source (sharp_second_source.json)
    if os.path.exists(SH+'sharp_second_source.json'): S_[5]['second_source']=json.load(open(SH+'sharp_second_source.json'))
    return S_
GAPS=[dict(category='coverage_matchups',item='PFR advanced defense live pull',status='MISSING (HTTP 403, not routed around)',backup='PFR cache pfr_def_adv_2026.html 2026-10-29 06:02 under Rico exception'),
      dict(category='coverage_matchups',item='Sharp pressure page / SumerSports',status='ON HOLD (Ghost6)',backup='pressure PROXY (sack|hit|scramble)/dropbacks from nflverse pbp'),
      dict(category='ngs',item='nextgenstats.nfl.com public pages',status='ON HOLD (Ghost6)',backup='nflverse nextgen_stats release parquet (labelled BACKUP)'),
      dict(category='coverage_matchups',item='PFF per-defender/props',status='NOT PULLED (logged-out preview only; needs signed-in box browser, read-only)',backup='none used as numbers'),
      dict(category='core_stats_pbp',item='nflverse pbp_participation_2026',status='MISSING (HTTP 404 not published; corrupt 9-byte file kept out)',backup='ESPN WR/CB cheatsheet alignment + ESPN depth')]
def write_game(g,E,out_dir):
    os.makedirs(out_dir)
    oemb_t=max([r['R'][10][3] for r in E if r['R'][10][0]=='PASS'] or [f'{datetime.datetime.now():%Y-%m-%dT%H:%M}'])
    # checklist
    ck=['| Leg | Phase | Status (PASS/FAIL/MISSING/STALE/UNVERIFIED/N/A) | Number | Source | Pulled (ET) |','|-----|-------|------|--------|--------|-------------|']
    for r in E:
        for ph in range(1,16):
            st,num,src,t=r['R'][ph]; ck.append(f"| {clean(r['name'])} | {ph} {PH[ph]} | {st} | {clean(num)} | {clean(src) if st!='N/A' else clean(src or 'n/a')} | {t.replace('T',' ') if t else ''} |")
    live=[r for r in E if r['status']=='PASS']; cut=[r for r in E if r['status']=='CUT']
    ck+=['','## Summary',f"- Legs passed: {len(live)}"]+[f"  - {r['name']} @ {r['price']:+d}: avg p {r['avg']:.3f}, no-vig {r['nv']:.3f}, raw edge {100*(r['avg']-r['nv']):+.1f}" for r in live]
    ck+=[f"- Legs cut: {len(cut)}"]+[f"  - {r['name']}: "+'; '.join(f"P{k} {s}: {clean(m)[:150]}" for k,s,m in r['bad'][:3]) for r in cut]
    ck+=[f"- Seeds: sim_v6.py seed {SM['meta']['seed']} (per-leg md5 offset), N={SM['meta']['N']} x 3 models; code sha {SM['meta']['code_sha']}, pbp sha {SM['meta']['pbp_sha']}",
         f"- Scripts: {SIMP}, features.py, film.py, legs.py, sims_run.py, assemble.py",
         "- Data gaps: "+'; '.join(f"{x['item']}: {x['status']} -> {x['backup']}" for x in GAPS)]
    open(out_dir+'/checklist.md','w').write('\n'.join(ck)+'\n')
    # manifest
    gt=F['teams']; a,h=g['away'],g['home']; TMS=g.get('teams',[a,h]); EM=[r for r in E if r.get('ps')]
    lab='PROXY' 
    _QP=json.load(open(SH+'qb_pressure.json'))
    PI=dict(time_to_throw=dict(value={t:_QP['teams'][t]['time_to_throw'] for t in TMS if t in _QP['teams']},source=_QP['source'],pulled_et=_QP['pulled_et'],label='QB time to throw'),
            targets_under_pressure=dict(value={t:_QP['teams'][t]['targets_under_pressure'] for t in TMS if t in _QP['teams']},source=_QP['source'],pulled_et=_QP['pulled_et'],label='targets under pressure'),
            blitz_rate=dict(value={t:round(gt[t]['blitz5'],3) for t in TMS},definition='defense FTN n_pass_rushers>=5 / charted dropbacks, season',l4={t:gt[t]['blitz5_l4'] for t in TMS},source=SH+'ftn_charting_2026.parquet + play_by_play_2026.parquet',pulled_et=T['pbp'],label='FTN charting'),
            pressure_rate=dict(value={t:round(gt[t]['pressure_proxy'],3) for t in TMS},definition='defense (sack|qb_hit|scramble)/dropbacks',source=SH+'play_by_play_2026.parquet',pulled_et=T['pbp'],label='PROXY'),
            checkdown_share=dict(value={t:round(F['qbs'][last_qb(t)]['checkdown'],3) for t in TMS if last_qb(t) in F['qbs']},definition='QB attempts with air_yards<=0 or RB target / attempts',source=SH+'play_by_play_2026.parquet',pulled_et=T['pbp'],label='nflverse pbp'))
    legs=[]
    for r in E:
        L=r['L']; d=dict(name=r['name'],player=L['player'],team=L['team'],opp=L['opp'],type=L['pos'],market=L['market'],receiving=(L['pos'] in('WR','TE') or L['market']=='rushrec'),
            side=r['side'].lower(),line=r['line'],price_fd=r['price'],no_vig=round(r['nv'],4),status=r['status'],rung=r['rung_label'],rung_note=r['rung_note'],injury_status=r['inj'],
            pinnacle=r['pin'],draftkings=r['dk'],prizepicks_lines=L['pp'],underdog_lines=L['ud'],bar=L['bar'],stack_flag=L['stack'],explicit=L['explicit'],
            cut_reasons=[f"P{k} {s}: {m}" for k,s,m in r['bad']])
        if r['cov']: d['coverage']=r['cov']
        for _k in ('recent_form','carry_share','rb_role','script_read','scheme_edge','depth','te_rank'):   # Locked Door fields
            if r.get(_k) is not None: d[_k]=r[_k]
        if r['L']['pos']=='WR' and isinstance(r['press'].get('wr_rank'),int): d['wr_rank']=r['press']['wr_rank']
        d['press']=r['press']
        if r.get('manual_review'): d['manual_review']=r['manual_review']
        if r.get('qb_return'): d['flags']=['QB-RETURN']; d['qb_return_recheck']=r['qb_return']
        if r.get('mirror_of'): d['mirror_of']=r['mirror_of']
        if r.get('mirror'): d['mirror']=r['mirror']
        legs.append(d)
    M=dict(season=2026,week=WEEK,game_id=g['id'],game=f"{a}@{h}",kickoff_et=f"{GAME_DATE} {g['ko']}",game_date=GAME_DATE,venue=g.get('venue'),input_cutoff_et=T['odds'],
           skill='/home/box/agent-data/workflows/nfl-game-script-run/SKILL.md',seed=SM['meta']['seed'],trials=SM['meta']['N'],sim_script=SIMP,
           approved_exceptions=[EXC],sources=sources(oemb_t),weather_forecast=dict(file=FCP,source=FC['source'],pulled_et=FC['pulled_et'],games=FC['games']),flagged_gaps=GAPS,pressure_inputs=PI,
           sims=[dict(model=mo,n=SM['meta']['N'],seed=SM['meta']['seed'],script=SIMP,legs={r['name']:dict(p=round(r['ps'][i],4),median=round(r['meds'][i],2)) for r in EM}) for i,mo in enumerate(['monte_carlo','bias','game_randomness'])],
           legs=legs)
    if GAME_DATE>=R4.RICO4_FROM: M['target_share_pool']=pool_block(TMS,legs)   # R3
    json.dump(M,open(out_dir+'/run_manifest.json','w'),indent=1,default=str)
    # report
    def report(gate_txt):
        cnt={ph:collections.Counter(r['R'][ph][0] for r in E) for ph in range(1,16)}
        o=['```',gate_txt.rstrip(),'```','',(g.get('title') or f"# {a} @ {h} — Week 8 game-script run (Sunday Nov 1, 2026)"),'',
           f"**For Ghost6 vetting only — not for Rico until VETTED.**",'','## 1. Header',f"- Game: {a} @ {h}, game ID {g['id']}, kickoff {g['ko']} ET.",
           f"- Data pulled 07:09–{T['odds'][11:]} ET Nov 1 (odds {T['odds'][11:]} ET, spreads {T['lines'][11:]} ET). pbp through Oct 29 (Week 8 TNF).",f"- Checklist: {out_dir}/checklist.md",
           f"- Candidate legs: {len(E)} (key players × FD main market); passed {len(live)}, cut {len(cut)}.",'','## 2. Phases run']
        for ph in range(1,16): o.append(f"- {ph} {PH[ph]}: "+', '.join(f"{k} {v}" for k,v in sorted(cnt[ph].items())))
        o+=['- Gaps: Phase 4 has no ruled mapping for TE and RB-receiving legs (UNVERIFIED → cut); Phase 9 uses the NGS backup; Phase 5 pressure is a PROXY.','','## 3. Sources used, by category']
        o+=['- Core stats and play-by-play: nflverse pbp, snaps and players (curl, 07:09 ET); ESPN depth-chart API (07:14 ET); ESPN box scores (Oct 31, 7:19 PM ET) as the second source for targets. The PFR live pull returned HTTP 403, so the PFR cache from Oct 29 was used (Rico exception).',
            '- Coverage schemes and matchups: FTN charting via nflverse (blitz rate); Sharp coverage-schemes page via Firecrawl (man/zone and MOF; data updated Oct 27); ESPN WR/CB cheatsheet (07:12 ET); PFR per-defender cache. The Sharp pressure page and SumerSports are on hold, so pressure uses the labelled PROXY. PFF was not pulled (logged-out preview only).',
            '- Next Gen Stats: BACKUP only, the nflverse nextgen_stats release (TTT, separation, cushion, YAC+, RYOE). nextgenstats.nfl.com is on hold per Ghost6.',
            '- Film: official NFL YouTube highlights (oEmbed-checked); only caption plays that re-matched a fresh pbp row are cited.',
            '- Injuries and news: ESPN injuries API (07:09 ET).','- Weather: NWS hourly + Open-Meteo (07:10 ET).',
            f"- Odds and props: The Odds API, FanDuel main and alt ladders (price of record), Pinnacle and DraftKings no-vig comparison, PrizePicks and Underdog lines (props {T['odds'][11:]} ET; spreads/totals {T['lines'][11:]} ET).",'',
            '## 4. Simulations',f"- Monte Carlo, Bias and Game Randomness each ran 100,000 sims per leg. Seed {SM['meta']['seed']} (md5 per-leg offset). Script {SIMP} (sha {SM['meta']['code_sha']}).",'',
            '| Leg | MC p / median | Bias p / median | GR p / median |','|---|---|---|---|']
        for r in EM: o.append(f"| {clean(r['name'])} | {r['ps'][0]:.3f} / {r['meds'][0]:.1f} | {r['ps'][1]:.3f} / {r['meds'][1]:.1f} | {r['ps'][2]:.3f} / {r['meds'][2]:.1f} |")
        o+=['','## 5. Projections and picks']
        if not live: o.append('**No card.** No leg passed every phase for this game.')
        for r in live:
            R=r['R']; o.append(f"- **{r['name']} @ {r['price']:+d} (FanDuel)**: projection MC mean {r['sims']['mc']['mean']:.1f}, median {r['meds'][0]:.1f}. No-vig {r['nv']:.3f}; avg p {r['avg']:.3f}; raw edge {100*(r['avg']-r['nv']):+.1f} pts (no shrink). {r['rung_note']}.")
            o.append(f"  - Opportunity: {R[2][1][:220]}"); o.append(f"  - Matchup/coverage: {R[4][1][:260]}"); o.append(f"  - Script: {R[13][1][:160]}")
        o+=['','### Cut legs']
        for r in cut: o.append(f"- {r['name']}: "+'; '.join(f"Phase {k} {s} ({clean(m)[:140]})" for k,s,m in r['bad'][:3]))
        o+=g.get('extra',[])
        qs=[r for r in E if r.get('inj')=='Questionable']
        o+=['','## 6. Risks and checks still to come',
            f"- Approved exception: per-defender numbers come from the PFR cache pfr_def_adv_2026.html (pulled Oct 29, 6:02 AM ET). It misses roughly the last 2 games per team; approved by Rico for Nov 1 receiving legs only, and it expires after today.",
            '- Sharp coverage-schemes data is dated Oct 27 (through Week 7), so the man/zone and MOF figures miss Week 8.',
            '- Pressure is a PROXY ((sack | QB hit | scramble) / dropbacks), not charted pressure. NGS is the nflverse BACKUP. Blitzed-target samples under 15 are labelled LOW-SAMPLE in Phase 5.',
            f"- Inactives recheck at {RECHECK(g['ko'])} ET: every leg, the Phase 4 defenders, weather and prices; a line move of more than 0.5 or 20 cents means a reprice.",
            f"- Questionable players among the candidates: {', '.join(sorted(set(r['L']['player'] for r in qs))) or 'none'}.",
            f"- UNVERIFIED film: {sum(r['R'][10][0]=='UNVERIFIED' for r in E)} leg(s) had no re-matched film play (cut).",
            '- PFF read-only cross-check is not done; it needs a signed-in browser session (read-only).']
        return '\n'.join(o)+'\n'
    open(out_dir+'/report.md','w').write(report('GATE: PENDING'))
    gate=lambda:subprocess.run(['python3',DB+'tools/run_gate.py',out_dir],capture_output=True,text=True).stdout
    g1=gate(); open(out_dir+'/report.md','w').write(report(g1)); g2=gate(); open(out_dir+'/report.md','w').write(report(g2))
    g3=gate()
    return g3   # first line 'GATE: PASS|FAIL'
if __name__=='__main__':
    res={}; ALL=[]
    for g in D['slate']:
        E=[evaluate(L) for L in D['legs'] if L['game']==f"{g['away']}@{g['home']}" and not L.get('dfs_only')]
        if GAME_DATE>=R4.RICO4_FROM: E+=mirrors(E)   # R2: mirror overs run every phase via evaluate(force=rung)
        out=(('/tmp/dry/' if '--dry' in sys.argv else DB+'runs/')+f"{GAME_DATE}_{g['away']}@{g['home']}{SUF}")
        if os.path.exists(out): print('EXISTS, not overwriting:',out); continue
        gt=write_game(g,E,out); res[out]=gt.splitlines()[0]; ALL+=E
        print(gt.splitlines()[0], '| live', sum(r['status']=='PASS' for r in E),'/',len(E),flush=True)
    json.dump([dict(name=r['name'],game=r['L']['game'],status=r['status'],avg=r['avg'],nv=r['nv'],price=r['price'],bad=r['bad']) for r in ALL],open(SH+f'eval_{TAG}{SUF}.json','w'),indent=0,default=str)
    _bad=[o for o,t in res.items() if not t.startswith('GATE: PASS')]
    if _bad:   # Locked Door: a gate FAIL stops assemble (exit 1). Slips are made only by tools/door.py build.
        print('ASSEMBLE: GATE FAIL ->',', '.join(_bad),file=sys.stderr); sys.exit(1)
    print('ASSEMBLE: all runs passed run_gate. Next: python3 tools/door.py build <slip.json> (the only way to make a slip).')
