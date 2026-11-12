import pandas as pd, numpy as np, json, sqlite3, re, os
W8='/workspace/nfl-database/week8'
pbp=pd.read_parquet('/tmp/pbp26.parquet'); pbp=pbp[(pbp.season_type=='REG')&(pbp.week<=7)]
ftn=pd.read_parquet('/tmp/ftn_charting_2026.parquet')[['nflverse_game_id','nflverse_play_id','n_blitzers','n_pass_rushers','n_defense_box','is_play_action','is_screen_pass']]
pbp=pbp.merge(ftn,left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left')
pfr=pd.read_parquet('/tmp/pfr_def_2026.parquet'); pfr=pfr[pfr.week<=7]
ros=pd.read_parquet('/tmp/rost.parquet'); pos=ros.sort_values('week').drop_duplicates('gsis_id',keep='last').set_index('gsis_id')
posmap=pos.position.to_dict(); pfrpos=pos.dropna(subset=['pfr_id']).set_index('pfr_id').position.to_dict()
inj=json.load(open(f'{W8}/injuries.json'))['teams']; dp=json.load(open(f'{W8}/defense/defense_profiles.json'))['teams']
pt=json.load(open(f'{W8}/player_types/player_types.json'))['teams']
con=sqlite3.connect('/workspace/nfl-database/fixes/fixes.sqlite')
part=pd.read_sql('select gsis_id,full_name,team,position,week,offense_snaps,offense_pct from fix_participation',con)
T=lambda t:{'LAR':'LA','WSH':'WAS'}.get(t,t)
games=[(T(g['away']),T(g['home']),g['odds']) for g in json.load(open(f'{W8}/defense/defense_profiles.json'))['games']]
games.append(('CAR','GB',['TNF','']))
gp=pbp.groupby('posteam').game_id.nunique()
def r1(x,n=1):
    try: return None if x is None or (isinstance(x,float) and np.isnan(x)) else round(float(x),n)
    except: return x
# ---- runs
ru=pbp[(pbp.play_type=='run')&(pbp.qb_kneel==0)&pbp.rusher_player_id.notna()].copy()
ru['pos']=ru.rusher_player_id.map(posmap)
def dirn(r):
    if r.run_location=='middle' or pd.isna(r.run_location): return 'middle' if r.run_location=='middle' else None
    return f"{r.run_location} {r.run_gap or ''}".strip()
ru['dir']=ru.apply(dirn,axis=1); rb=ru[ru.pos=='RB']
lg_ypc=rb.yards_gained.mean(); lg_dir=rb.groupby('dir').yards_gained.mean()
pas=pbp[(pbp.play_type=='pass')&pbp.passer_player_id.notna()].copy()
pas['blitz']=pas.n_blitzers>0; pas['tpos']=pas.receiver_player_id.map(posmap)
tg=pas[pas.receiver_player_id.notna()]
# league defense RB receiving ranks
rbrec=tg[tg.tpos=='RB'].groupby('defteam').agg(t=('play_id','size'),r=('complete_pass','sum'),y=('receiving_yards','sum'))
gpd=pbp.groupby('defteam').game_id.nunique(); rbrec=rbrec.div(gpd,axis=0); rbrec['rank_most']=rbrec.y.rank(ascending=False).astype(int)
def defense(d):
    g=gpd[d]; dr=rb[rb.defteam==d]; o={}
    o['rb_car_pg']=r1(len(dr)/g); o['rb_ypc_allowed']=r1(dr.yards_gained.mean(),2); o['rb_rush_yds_pg']=r1(dr.yards_gained.sum()/g)
    o['rb_rush_td_pg']=r1(dr.rush_touchdown.sum()/g,2); o['rb_rush_td_total']=int(dr.rush_touchdown.sum())
    x=rbrec.loc[d]; o['rb_tgt_pg'],o['rb_rec_pg'],o['rb_recyds_pg']=r1(x.t),r1(x.r),r1(x.y); o['rb_recyds_rank_most_allowed']=int(x.rank_most)
    bd=dr.groupby('dir').yards_gained.agg(['size','mean']); bd=bd[bd['size']>=8]
    o['by_dir']={k:{'car':int(v['size']),'ypc':r1(v['mean'],2),'lg':r1(lg_dir.get(k),2)} for k,v in bd.iterrows()}
    if len(bd): w=(bd['mean']-lg_dir.reindex(bd.index)).idxmax(); o['weak_dir']=w
    a=pbp[pbp.defteam==d]
    o['pass_yds_pg']=r1(a[a.play_type=='pass'].passing_yards.fillna(0).sum()/g); o['rush_yds_pg']=r1(a[a.play_type=='run'].yards_gained.sum()/g)
    o['pass_td']=int(a.pass_touchdown.sum()); o['rush_td']=int(a.rush_touchdown.sum())
    pts=pbp[pbp.defteam==d].groupby('game_id').apply(lambda z: z.total_away_score.max() if (z.home_team.iloc[0]==d) else z.total_home_score.max(),include_groups=False)
    o['pts_allowed_pg']=r1(pts.mean())
    dd=a[a.play_type=='pass']; o['ftn_blitz_pct']=r1(100*dd.blitz.mean() if 'blitz' in dd else None)
    dd=pas[pas.defteam==d]; o['ftn_blitz_pct']=r1(100*dd.blitz.mean()); o['sacks']=int(a.sack.sum()); o['sack_rate']=r1(100*dd.sack.mean())
    t3=dd[dd.down==3]; o['3rd_blitz_pct']=r1(100*t3.blitz.mean()); o['3rd_avg_box']=r1(t3.n_defense_box.mean())
    o['3rd_box7plus_pct']=r1(100*(t3.n_defense_box>=7).mean()); o['3rd_5plus_rushers_pct']=r1(100*(t3.n_pass_rushers>=5).mean())
    pr=pfr[pfr.team==d].groupby('pfr_player_name').agg(p=('def_pressures','sum'),s=('def_sacks','sum'))
    o['pfr_pressures_pg']=r1(pr.p.sum()/g); o['top_rushers']=[{'name':n,'pressures':int(v.p),'sacks':r1(v.s)} for n,v in pr.sort_values('p',ascending=False).head(3).iterrows()]
    cb=pfr[pfr.team==d].copy(); cb['pos']=cb.pfr_player_id.map(pfrpos)
    c=cb[cb.pos.isin(['CB','S','DB','SS','FS'])].groupby(['pfr_player_name','pos']).agg(gp=('week','nunique'),t=('def_targets','sum'),r=('def_completions_allowed','sum'),y=('def_yards_allowed','sum'),td=('def_receiving_td_allowed','sum')).reset_index()
    c=c.sort_values('t',ascending=False)
    o['cover']=[{'name':v.pfr_player_name,'pos':v.pos,'gp':int(v.gp),'tgt_pg':r1(v.t/v.gp),'rec_pg':r1(v.r/v.gp),'yds_pg':r1(v.y/v.gp),'td':int(v.td or 0)} for v in c.head(5).itertuples()]
    # 3rd/4th/RZ allowed
    o['3rd_conv_allowed']=r1(100*a[a.down==3].third_down_converted.sum()/max(1,(a[a.down==3].play_type.isin(['run','pass'])).sum()))
    rz=drv(a); o['rz_td_pct_allowed']=rz
    dpi=inj.get({'LA':'LAR','WAS':'WSH'}.get(d,d),[])
    o['front_injuries']=[f"{i['name']} ({i['pos']}, {i['designation']})" for i in dpi if i['pos'] in('DE','DT','NT','DL','LB','OLB','EDGE','ILB')]
    o['db_injuries']=[f"{i['name']} ({i['pos']}, {i['designation']})" for i in dpi if i['pos'] in('CB','S','DB','SS','FS')]
    sh=dp.get(d,{}).get('sharp',{}) or {}; o['sharp']=sh
    o['sharp_pressure_proxy']=dp.get(d,{}).get('sharp_def_pressure_rate_proxy'); o['pass_rush_win_rate']=dp.get(d,{}).get('defense.pass_rush_win_rate_pct')
    for k,v in (dp.get(d,{}) or {}).items():
        if k in('WR','TE'): o[k+'_allowed_pg']={'tgt':r1(v['tgt_pg']),'rec':r1(v['rec_pg']),'yds':r1(v['yds_pg'])}
    return o
def drv(a):
    dv=a[a.fixed_drive.notna()].groupby(['game_id','fixed_drive']).agg(m=('yardline_100','min'),res=('fixed_drive_result','first'))
    z=dv[dv.m<=20]; return r1(100*(z.res=='Touchdown').mean()) if len(z) else None
def offense(t):
    g=gp[t]; o={}; a=pbp[pbp.posteam==t]
    tr=rb[rb.posteam==t]; tc=len(ru[(ru.posteam==t)]); wk=sorted(a.week.unique()); l3=wk[-3:]
    rbs=[]
    for pid,z in tr.groupby('rusher_player_id'):
        if len(z)<15: continue
        n=z.rusher_player_name.iloc[0]; gpp=z.game_id.nunique(); zl=z[z.week.isin(l3)]
        bd=z.groupby('dir').yards_gained.agg(['size','mean'])
        tt=tg[(tg.posteam==t)&(tg.receiver_player_id==pid)]; tl=tt[tt.week.isin(l3)]; gl=max(1,zl.game_id.nunique())
        rbs.append({'name':n,'gp':gpp,'car_pg':r1(len(z)/gpp),'car_pg_l3':r1(len(zl)/gl),'car_share':r1(100*len(z)/tc),'ypc':r1(z.yards_gained.mean(),2),'rush_td':int(z.rush_touchdown.sum()),
            'dir_share':{k:r1(100*v['size']/len(z)) for k,v in bd.iterrows()},'dir_ypc':{k:r1(v['mean'],2) for k,v in bd.iterrows() if v['size']>=5},
            'tgt_pg':r1(len(tt)/gpp),'rec_pg':r1(tt.complete_pass.sum()/gpp),'recyds_pg':r1(tt.receiving_yards.sum()/gpp),'tgt_pg_l3':r1(len(tl)/gl),'rec_pg_l3':r1(tl.complete_pass.sum()/gl),'recyds_pg_l3':r1(tl.receiving_yards.sum()/gl)})
    o['rbs']=sorted(rbs,key=lambda x:-x['car_pg'])
    p=pas[pas.posteam==t]; qb=p.passer_player_name.value_counts().index[0]; o['qb']=qb; q=p
    def sp(z):
        att=z[z.pass_attempt==1&(z.sack==0)] ; at=z[(z.sack==0)]
        return {'dropbacks':len(z),'comp_pct':r1(100*at.complete_pass.sum()/max(1,at.pass_attempt.sum()-0)),'ypa':r1(at.passing_yards.fillna(0).sum()/max(1,len(at))),'sacks':int(z.sack.sum()),'int':int(z.interception.sum()),'epa':r1(z.epa.mean(),3)}
    ch=q[q.n_blitzers.notna()]
    o['qb_blitz']=sp(ch[ch.blitz]); o['qb_noblitz']=sp(ch[~ch.blitz]); o['blitz_faced_pct']=r1(100*ch.blitz.mean())
    bt=tg[(tg.posteam==t)&(tg.blitz)]
    def tree(z):
        n=len(z); 
        if not n: return []
        v=z.groupby(['receiver_player_name','tpos']).size().sort_values(ascending=False).head(4)
        return [f"{a} ({b}) {r1(100*c/n,0):.0f}%" for (a,b),c in v.items()]
    o['blitz_tree_0_5']=tree(bt[bt.air_yards<=5]); o['blitz_tree_5_15']=tree(bt[(bt.air_yards>5)&(bt.air_yards<=15)]); o['blitz_n']=len(bt)
    o['blitz_pos_share']={k:r1(100*v,0) for k,v in bt.tpos.value_counts(normalize=True).items()}
    # RZ
    rzp=a[(a.yardline_100<=20)&a.play_type.isin(['run','pass'])]
    def rzu(z,col):
        return z.groupby(col).size().sort_values(ascending=False).head(4).to_dict()
    o['rz20_tgts']=rzu(rzp[rzp.receiver_player_name.notna()],'receiver_player_name'); o['rz20_car']=rzu(rzp[rzp.rusher_player_name.notna()],'rusher_player_name')
    r10=rzp[rzp.yardline_100<=10]; o['rz10_tgts']=rzu(r10[r10.receiver_player_name.notna()],'receiver_player_name'); o['rz10_car']=rzu(r10[r10.rusher_player_name.notna()],'rusher_player_name')
    o['rz_td_pct']=drv(a)
    d3=a[(a.down==3)&a.play_type.isin(['run','pass'])]; o['3rd_pass_pct']=r1(100*(d3.play_type=='pass').mean()); o['3rd_conv']=r1(100*d3.third_down_converted.mean())
    d4=a[a.down==4]; go=d4[d4.play_type.isin(['run','pass'])]; o['4th_go']=len(go); o['4th_att_total']=len(d4[d4.play_type.isin(['run','pass','punt','field_goal'])]); o['4th_conv_pct']=r1(100*go.fourth_down_converted.mean()) if len(go) else None
    o['pass_rate_neutral']=r1(100*(a[(a.play_type.isin(['run','pass']))&(a.wp.between(.2,.8))&(a.down<=2)].play_type=='pass').mean())
    # TE usage
    te=part[(part.team==t)&(part.position=='TE')].groupby('full_name').agg(sn=('offense_snaps','sum'),pct=('offense_pct','mean')).sort_values('sn',ascending=False).head(3)
    tes=[]
    for n,v in te.iterrows():
        z=tg[(tg.posteam==t)&(tg.tpos=='TE')]
        ids=pos[(pos.full_name==n)].index; tt=z[z.receiver_player_id.isin(ids)]
        tes.append({'name':n,'snap_pct':r1(v.pct),'tgts':len(tt),'tgt_per_100snaps':r1(100*len(tt)/max(1,v.sn))})
    o['tes']=tes
    if len(tes)>=2: o['te_roles']=f"Receiving TE: {max(tes,key=lambda x:x['tgt_per_100snaps'])['name']} | Blocking/in-line: {min(tes,key=lambda x:x['tgt_per_100snaps'])['name']} (by targets per snap; 12/13 rates = GAP)"
    # seesaw
    tt=tg[tg.posteam==t]; top=tt.receiver_player_name.value_counts().head(3).index.tolist()
    pg=tt.groupby(['week','receiver_player_name']).agg(tg=('play_id','size'),y=('receiving_yards','sum')).reset_index()
    tot=tt.groupby('week').size(); pg['ts']=pg.apply(lambda r:r.tg/tot[r.week],axis=1)
    ss=[]
    for i in range(len(top)):
        for j in range(i+1,len(top)):
            A=pg[pg.receiver_player_name==top[i]].set_index('week'); B=pg[pg.receiver_player_name==top[j]].set_index('week')
            w=A.index.intersection(B.index); n=len(w)
            if n<4: continue
            ry=np.corrcoef(A.y[w],B.y[w])[0,1]; rs=np.corrcoef(A.ts[w],B.ts[w])[0,1]
            flips=[f"Wk{k}: {top[i]} {int(A.y[k])} / {top[j]} {int(B.y[k])}" for k in w if (A.y[k]<0.6*A.y.mean() and B.y[k]>1.4*B.y.mean()) or (B.y[k]<0.6*B.y.mean() and A.y[k]>1.4*A.y.mean())]
            lab='strong inverse' if ry<=-0.6 and n>=6 else 'weak inverse' if ry<=-0.3 else 'no inverse pattern'
            ss.append({'pair':f"{top[i]} vs {top[j]}",'n':n,'r_yds':r1(ry,2),'r_tgt_share':r1(rs,2),'label':lab,'flip_games':flips,'games':{f"Wk{k}":f"{int(A.y[k])}/{int(B.y[k])}" for k in w}})
    o['seesaw']=ss
    fp=f'{W8}/film/{ {"LA":"LA"}.get(t,t)}_film.md'
    notes=[]
    if os.path.exists(fp):
        txt=open(fp).read().splitlines()
        for nm in top:
            ln=nm.split('.')[-1]
            hit=[l.strip()[:220] for l in txt if ln in l and len(l)>30][:2]; notes+=hit
    o['film_receiver_notes']=notes
    # receivers by type
    plist=pt.get(t,[]); o['receivers']=[{k:p.get(k) for k in('player','pos','primary','tgt_share_season','tgt_share_l3','tgt_pg','rec','rec_yds','gp','adot','rz_tgts','injury')} for p in sorted(plist,key=lambda p:-(p.get('tgt_pg') or 0)) if p['pos'] in('WR','TE') and (p.get('tgt_pg') or 0)>=3][:5]
    o['inj']=[f"{i['name']} ({i['pos']}, {i['designation']})" for i in inj.get({'LA':'LAR','WAS':'WSH'}.get(t,t),[]) if i['designation'] not in('Active',)][:12]
    return o
OFF={};DEF={}
for a,h,_ in games:
    for t in(a,h): OFF[t]=offense(t); DEF[t]=defense(t)
lgp=pas.groupby('defteam').blitz.mean()*100
def bottom(o,d,opp):
    e=[];tr=[]
    for r in o['rbs'][:2]:
        diff=d['rb_ypc_allowed']-lg_ypc
        gate=r['car_pg_l3']>=12
        wd=d.get('weak_dir'); wds=r['dir_share'].get(wd,0) if wd else 0
        if diff>=0.3 and gate: e.append(f"RUN EDGE {r['name']}: {r['ypc']} YPC vs D allowing {d['rb_ypc_allowed']} (lg {lg_ypc:.2f}); {r['car_pg_l3']} car/g L3 passes gate; weak side {wd} ({wds}% of his runs)")
        elif diff<=-0.3 and r['car_pg']>=10: tr.append(f"RUN TRAP {r['name']}: D allows {d['rb_ypc_allowed']} YPC (lg {lg_ypc:.2f}), {d['rb_rush_td_pg']} RB rush TD/g")
        if r['tgt_pg_l3']>=3.5 and d['rb_recyds_rank_most_allowed']<=10: e.append(f"RB REC EDGE {r['name']}: {r['tgt_pg_l3']} tgt/g L3 vs D ranked #{d['rb_recyds_rank_most_allowed']} most RB rec yds ({d['rb_recyds_pg']}/g)")
    bb=o['qb_blitz']; 
    if bb['epa'] is not None and bb['epa']<-0.1 and (d['ftn_blitz_pct'] or 0)>=30: tr.append(f"BLITZ FLAG {o['qb']}: EPA {bb['epa']} vs blitz ({bb['sacks']} sk, {bb['int']} INT in {bb['dropbacks']}) and {opp} blitzes {d['ftn_blitz_pct']}% -> downgrade WR yardage/receptions legs; lean check-down tree")
    sh=d['sharp']
    for p in o['receivers'][:3]:
        ts=p.get('tgt_share_l3') or 0
        soft=sh.get('YPT Allowed TE') if p['pos']=='TE' else sh.get('YPT Allowed WR')
        if ts>=20 and soft and soft>=9.0: e.append(f"PASS EDGE {p['player']} ({p['primary']}): {ts}% tgt share L3 vs {p['pos']} YPT allowed {soft}")
        elif soft and soft<7.5 and ts>=18: tr.append(f"COVERAGE TRAP {p['player']}: {p['pos']} YPT allowed only {soft}")
    return e,tr
out=[]
for a,h,odds in games:
    G={'game':f'{a}@{h}','odds':odds,'sides':{}}
    for t,opp in((a,h),(h,a)):
        e,tr=bottom(OFF[t],DEF[opp],opp)
        G['sides'][t]={'offense':OFF[t],'opp_defense':DEF[opp],'edges':e,'traps':tr}
    out.append(G)
json.dump({'built':'2026-10-29','data_through_week':7,'league_rb_ypc':round(lg_ypc,2),'league_dir_ypc':{k:r1(v,2) for k,v in lg_dir.items()},'games':out},open('breakdown.json','w'),indent=1,default=str)
print('ok',len(out))
