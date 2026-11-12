"""Game-total / team-total / anytime-TD sim. 'fixed-model, copies only': reads the frozen pbp copy in tools/sim_v6_fix/sim_v6_src,
imports nothing from nfl-sim/, sb-fix/, sb-grades. sim_v6 has no points/TD market, so this is a points extension built on the
same 3-model design (MC season+L3 regressed / Bias = last-4 current-QB only, 2x regression / GR = shared game shock + team
shock + spread tilt). N=100k each, seed 20261101."""
import pandas as pd,numpy as np,json
N=100_000;SEED=20261101
p=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/play_by_play_2026.parquet');p=p[p.season_type=='REG']
qbm=p[p.pass_attempt==1].groupby(['game_id','posteam']).passer_player_name.agg(lambda s:s.mode().iat[0])
off=p[(p.touchdown==1)&(p.td_team==p.posteam)&((p.rush==1)|(p.pass_attempt==1))]
nonoff=p[(p.touchdown==1)&(p.td_team==p.defteam)]
fg=p[(p.field_goal_attempt==1)&(p.field_goal_result=='made')]
games=p.groupby(['game_id','posteam']).week.first().reset_index(); games['qb']=[qbm.get((g,t)) for g,t in zip(games.game_id,games.posteam)]
games['td']=[((off.game_id==g)&(off.posteam==t)).sum() for g,t in zip(games.game_id,games.posteam)]
games['fg']=[((fg.game_id==g)&(fg.posteam==t)).sum() for g,t in zip(games.game_id,games.posteam)]
import os
if os.environ.get('EXCL_CHI_W1'): games=games[~((games.week==1)&games.game_id.str.contains('CHI'))]
dfn=games.merge(games[['game_id','posteam','td','fg']].rename(columns={'posteam':'opp','td':'td_a','fg':'fg_a'}),on='game_id');dfn=dfn[dfn.posteam!=dfn.opp]
LTD,LFG=games.td.mean(),games.fg.mean(); NONOFF=len(nonoff)/len(games)
def rates(t,o,qb,window=None,k=3):
    a=dfn[(dfn.posteam==t)&(dfn.qb==qb)].sort_values('week'); d=dfn[dfn.opp==o].sort_values('week')
    if window: a=a.tail(window); d=d.tail(window)
    reg=lambda x,n,L:(x*n+L*k)/(n+k)
    otd,ofg=reg(a.td.mean(),len(a),LTD),reg(a.fg.mean(),len(a),LFG)
    dtd,dfg=reg(d.td_a.mean(),len(d),LTD),reg(d.fg_a.mean(),len(d),LFG)
    return otd*dtd/LTD, ofg*dfg/LFG
SIDE={'CHI':('SEA','C.Williams'),'SEA':('CHI','S.Darnold')}
lam={'mc':{t:rates(t,o,q) for t,(o,q) in SIDE.items()},'bias':{t:rates(t,o,q,window=4,k=6) for t,(o,q) in SIDE.items()}}
lam['gr']=lam['mc']
SPREAD=-3.0 # SEA fav (FD -3)
def sim(mode):
    rng=np.random.default_rng(SEED+hash(mode)%1000 if False else SEED+{'mc':1,'bias':2,'gr':3}[mode])
    out={}
    g=rng.lognormal(-0.02,0.20,N) if mode=='gr' else np.ones(N)
    for t in ('CHI','SEA'):
        ltd,lfg=lam[mode][t]
        if mode=='gr':
            tilt=np.exp((0.5 if t=='SEA' else -0.5)*(-SPREAD)/2/23.0*2)  # ~+/-6.5% toward the spread
            sh=rng.lognormal(-0.011,0.15,N); ltd=ltd*g*sh*tilt; lfg=lfg*g**0.5*sh*tilt
        else:
            ltd=ltd*rng.gamma(12,1/12,N)  # overdispersion
        td=rng.poisson(ltd); f=rng.poisson(lfg,N); nd=rng.poisson(NONOFF,N)
        xp=rng.binomial(td+nd,0.95)
        out[t]=dict(td=td,pts=6*(td+nd)+xp+3*f)
    out['tot']=out['CHI']['pts']+out['SEA']['pts']; return out
S={m:sim(m) for m in ('mc','bias','gr')}
d=pd.read_csv('odds_t0743.csv');fd=d[d.book=='fanduel']
imp=lambda a:100/(a+100) if a>0 else -a/(-a+100)
def nv(mkt,line,player=None):
    x=fd[(fd.market==mkt)&(fd.point==line)]; x=x[x.player==player] if player else x
    o=imp(x[x.side=='Over'].price.iat[0]);u=imp(x[x.side=='Under'].price.iat[0]); return o/(o+u),u/(o+u),int(x[x.side=='Over'].price.iat[0]),int(x[x.side=='Under'].price.iat[0])
R=[]
def row(label,key,line,mkt,player):
    po,pu,ao,au=nv(mkt,line,player)
    for side,nvp,am in (('Over',po,ao),('Under',pu,au)):
        ps={m:float(((S[m][key] if key=='tot' else S[m][key]['pts'])>line).mean()) if side=='Over' else float(((S[m][key] if key=='tot' else S[m][key]['pts'])<line).mean()) for m in S}
        med={m:float(np.median(S[m][key] if key=='tot' else S[m][key]['pts'])) for m in S}
        avg=np.mean(list(ps.values())); sh=0.5+0.7*(avg-0.5)
        R.append(dict(market=label,line=line,side=side,fd=am,nv=round(nvp,3),mc=round(ps['mc'],3),bias=round(ps['bias'],3),gr=round(ps['gr'],3),avg=round(avg,3),
          raw_edge=round(100*(avg-nvp),1),g6_shrunk_edge=round(100*(sh-nvp),1),edge_x07=round(70*(avg-nvp),1),med=f"{med['mc']:.0f}/{med['bias']:.0f}/{med['gr']:.0f}",
          clears=bool(avg-nvp>=.03 and sh-nvp>0 and min(ps.values())>=.45 and all((m>line) if side=='Over' else (m<line) for m in med.values()))))
for L in (42.5,43.5,44.5,45.5,46.5,47.5,48.5,50.5): row('Game total',"tot",L,'alternate_totals' if L!=46.5 else 'totals',None)
for L in (17.5,18.5,19.5,20.5,21.5,22.5,23.5): row('CHI TT','CHI',L,'alternate_team_totals' if L!=21.5 else 'team_totals','Chicago Bears')
for L in (20.5,21.5,22.5,23.5,24.5,25.5,26.5): row('SEA TT','SEA',L,'alternate_team_totals' if L!=24.5 else 'team_totals','Seattle Seahawks')
T=pd.DataFrame(R); open('sim_totals'+('_exW1' if os.environ.get('EXCL_CHI_W1') else '')+'.md','w').write("fixed-model, copies only | seed 20261101 | 100k x3 | FD odds_t0743 (7:43 AM ET)\n\n"+T.to_markdown(index=False))
summ={m:dict(mean_tot=float(S[m]['tot'].mean()),CHI=float(S[m]['CHI']['pts'].mean()),SEA=float(S[m]['SEA']['pts'].mean()),CHI_td=float(S[m]['CHI']['td'].mean()),SEA_td=float(S[m]['SEA']['td'].mean())) for m in S}
print(json.dumps(dict(lam={m:{t:[round(v,2) for v in lam[m][t]] for t in lam[m]} for m in lam},summ=summ),indent=0)); print(T.to_string())
# ---------- anytime TD ----------
# ---------- anytime TD: share = .4 td_sh + .3 rz_sh + .3 i10_sh over current-QB games, then 25% shrink toward equal-weight 1/8 ----------
p['gqb']=[qbm.get((g,t)) for g,t in zip(p.game_id,p.posteam)]
pin=d[(d.book=='pinnacle')&(d.market=='player_anytime_td')].pivot_table(index='player',columns='side',values='price',aggfunc='first').dropna()
pin_nv={k:imp(r.Yes)/(imp(r.Yes)+imp(r.No)) for k,r in pin.iterrows()}
fdy={r.player:int(r.price) for r in fd[fd.market=='player_anytime_td'].itertuples()}
k_fd=np.median([imp(fdy[k])/v for k,v in pin_nv.items() if k in fdy])  # FD ATD overround vs Pinnacle two-way no-vig
NAME={'D.Swift':"D'Andre Swift",'C.Loveland':'Colston Loveland','L.Burden':'Luther Burden III','R.Odunze':'Rome Odunze','R.Johnson':'Roschon Johnson','C.Williams':'Caleb Williams','K.Monangai':None,
      'J.Smith-Njigba':'Jaxon Smith-Njigba','A.Barner':'AJ Barner','C.Kupp':'Cooper Kupp','E.Wilson':'Emanuel Wilson','G.Holani':'George Holani','R.Shaheed':None}
AT=[]
for t,(o,qb) in SIDE.items():
    s=p[(p.posteam==t)&(p.gqb==qb)&((p.rush==1)|(p.pass_attempt==1))].copy(); s['who']=s.rusher_player_name.where(s.rush==1,s.receiver_player_name)
    s['tdp']=(s.touchdown==1)&(s.td_team==t)
    a=s.groupby('who').agg(td=('tdp','sum'),rz=('yardline_100',lambda y:(y<=20).sum()),i10=('yardline_100',lambda y:(y<=10).sum()))
    sh=.4*a.td/a.td.sum()+.3*a.rz/a.rz.sum()+.3*a.i10/a.i10.sum(); sh=.75*sh+.25*sh.mean()*(sh>0); sh=sh/sh.sum()
    for who,nm in NAME.items():
        if nm is None or who not in sh.index: continue
        if (t=='CHI')!=(who in ('D.Swift','C.Loveland','L.Burden','R.Odunze','R.Johnson','C.Williams')): continue
        ps={m:float(1-np.mean((1-sh[who])**S[m][t]['td'])) for m in S}
        avg=np.mean(list(ps.values())); nvp=imp(fdy[nm])/k_fd if nm in fdy else np.nan
        AT.append(dict(team=t,player=nm,share=round(sh[who],3),fd=fdy.get(nm),pin_nv=round(pin_nv.get(nm,np.nan),3),fd_nv=round(nvp,3),mc=round(ps['mc'],3),bias=round(ps['bias'],3),gr=round(ps['gr'],3),
            raw_edge=round(100*(avg-nvp),1),g6_shrunk=round(100*(0.5+.7*(avg-.5)-nvp),1),x07=round(70*(avg-nvp),1)))
A=pd.DataFrame(AT); print('FD ATD overround k',round(k_fd,3)); print(A.to_string())
open('sim_atd.md','w').write(f"fixed-model, copies only | seed 20261101 | FD ATD de-vig: FD implied / {k_fd:.3f} (median FD vs Pinnacle two-way no-vig)\n\n"+A.to_markdown(index=False))
json.dump(dict(totals=R,atd=AT,summ=summ),open('raw_total_sims.json','w'),indent=1,default=float)
# SEA RB pool (Charbonnet returns with 0 2026 games -> individual RB split MISSING; pool only)
s=p[(p.posteam=='SEA')&(p.gqb=='S.Darnold')&((p.rush==1)|(p.pass_attempt==1))].copy(); s['who']=s.rusher_player_name.where(s.rush==1,s.receiver_player_name)
pos=pd.read_parquet('/workspace/nfl-database/tools/sim_v6_fix/sim_v6_src/players.parquet')
rbids=set(pos[pos.position=='RB'].gsis_id); s['rb']=np.where(s.rush==1,s.rusher_player_id.isin(rbids),s.receiver_player_id.isin(rbids))
s['tdp']=(s.touchdown==1)&(s.td_team=='SEA')
rb_sh=.4*s[s.tdp].rb.mean()+.3*s[s.yardline_100<=20].rb.mean()+.3*s[s.yardline_100<=10].rb.mean()
pool={m:float(1-np.mean((1-rb_sh)**S[m]['SEA']['td'])) for m in S}
rbn=[n for n in ('Zach Charbonnet','Emanuel Wilson','Jadarian Price','George Holani') if n in fdy]
# P(at least one of those RBs) from book: assume TDs mostly exclusive -> 1-prod(1-nv) as upper-ish proxy
book_pool=1-np.prod([1-imp(fdy[n])/k_fd for n in rbn])
print('SEA RB pool share',round(rb_sh,3),'P(any SEA RB TD)',{k:round(v,3) for k,v in pool.items()},'book proxy (indep. 1-prod)',round(book_pool,3),rbn)
json.dump(dict(rb_sh=rb_sh,pool=pool,book_pool=book_pool),open('sea_rb_pool.json','w'))
