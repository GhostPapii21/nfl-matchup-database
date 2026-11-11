# Inferred route/zone matchup estimate, NYG pass catchers vs WAS defenders. Research only.
import pandas as pd, numpy as np, json, os
OUT='/workspace/nyg_was_route_matchups_2026-11-10'; RAW=OUT+'/raw'
PBP='/tmp/nflverse_2026/play_by_play_2026.parquet'
p=pd.read_parquet(PBP)
NAMES={'M.Nabers':'Malik Nabers','I.Likely':'Isaiah Likely','M.Fields':'Malachi Fields'}
CAVEAT='ESTIMATE from routes+alignment+scheme+snaps; not charted coverage'

# ---------- 1. NGS routes / receiving ----------
ngs=pd.read_parquet(RAW+'/ngs_receiving.parquet')
n=ngs[(ngs.season==2026)&(ngs.season_type=='REG')&ngs.player_display_name.isin(NAMES.values())].copy()
charts=json.load(open(RAW+'/ngs_charts_nyg_route.json'))['charts']
chart_idx={(c['playerName'],c['week']):c for c in charts}
rows=[]
for _,r in n.sort_values(['player_display_name','week']).iterrows():
    c=chart_idx.get((r.player_display_name,r.week))
    rows.append(dict(player=r.player_display_name,scope='season W1-9' if r.week==0 else f'week {r.week}',week=r.week,
        targets=r.targets,receptions=r.receptions,yards=r.yards,rec_td=r.rec_touchdowns,
        ngs_avg_separation_yds=round(r.avg_separation,2),ngs_avg_cushion_yds=round(r.avg_cushion,2),
        ngs_avg_intended_air_yds=round(r.avg_intended_air_yards,2),ngs_share_team_intended_air_yds_pct=round(r.percent_share_of_intended_air_yards,1),
        ngs_avg_yac=round(r.avg_yac,2),ngs_yac_over_expected=round(r.avg_yac_above_expectation,2),
        ngs_route_chart_available=bool(c), ngs_route_chart_image=(f"raw/ngs_chart_images/{c['imageName']}" if c else ''),
        route_types_labeled=False,
        source='nflverse nextgen_stats/ngs_receiving.parquet (NGS weekly receiving; week 0 = season). Route chart = nextgenstats.nfl.com /api/content/microsite/chart type=route (JPEG image of TARGETED routes only, no route-type labels)'))
ngs_df=pd.DataFrame(rows)
# Week 5 rows not in NGS weekly for Fields (below threshold): note
ngs_df.to_csv(OUT+'/ngs_routes.csv',index=False)

# ---------- target zones (nflverse pbp) ----------
t=p[(p.posteam=='NYG')&p.receiver_player_name.isin(NAMES)&(p.play_type=='pass')&p.air_yards.notna()].copy()
t['player']=t.receiver_player_name.map(NAMES)
def depth(a): return 'short (<=9 air yds)' if a<10 else ('intermediate (10-19)' if a<20 else 'deep (20+)')
t['depth_band']=t.air_yards.apply(depth); t['side']=t.pass_location
zone_rows=[]
for scope,sub in [('season W1-9',t),('week 5 vs WAS',t[t.week==5])]:
    for pl,g in sub.groupby('player'):
        tot=len(g)
        for (sd,db),gg in g.groupby(['side','depth_band']):
            zone_rows.append(dict(player=pl,scope=scope,side_offense_view=sd,depth_band=db,targets=len(gg),share_of_player_targets_pct=round(100*len(gg)/tot,1),
              receptions=int(gg.complete_pass.sum()),rec_yards=int(gg.loc[gg.complete_pass==1,'yards_gained'].sum()),avg_air_yards=round(gg.air_yards.mean(),1),
              source='nflverse play_by_play_2026.parquet (pass_location, air_yards); W8 NYG bye'))
zones=pd.DataFrame(zone_rows); zones.to_csv(OUT+'/target_zone_profile.csv',index=False)

# ---------- 3. scheme + personnel models ----------
P_TWO_HIGH=0.618; P_MAN=0.179; P_ONE_HIGH_ZONE=round(1-P_TWO_HIGH-P_MAN,3)  # StatRankings CoverageIQ season, Nov 10
# role pools: who fills each zone role (probabilities), by personnel era. Basis documented in alignment_sources.csv
POOLS={
 'wk5':{
  'OUT_R':{'Rasul Douglas':.70,'Fabian Moreau':.20,'Amik Robertson':.10},           # SR right-coverage: Douglas 61.3%, Moreau 64.0% (offense's right)
  'OUT_L':{'Amik Robertson':.65,'Rasul Douglas':.20,'Fabian Moreau':.10,'Mike Sainristil':.05},
  'NICKEL':{'Mike Sainristil':.50,'Amik Robertson':.30,'Quan Martin':.20},
  'DEEP_L':{'Jeremy Reaves':.45,'Quan Martin':.45,'Mike Sainristil':.10},
  'DEEP_R':{'Jeremy Reaves':.45,'Quan Martin':.45,'Mike Sainristil':.10},
  'FS_MOFC':{'Jeremy Reaves':.55,'Quan Martin':.35,'Mike Sainristil':.10},
  'ROBBER':{'Quan Martin':.55,'Jeremy Reaves':.30,'Mike Sainristil':.15},
  'HOOK_L':{'Sonny Styles':.70,'Frankie Luvu':.30},   # RILB Styles stationed on defense's right = offense's left
  'HOOK_R':{'Frankie Luvu':.70,'Sonny Styles':.30},   # LILB Luvu = offense's right
  'HOOK_M':{'Sonny Styles':.45,'Frankie Luvu':.45,'Dorance Armstrong':.05,"K'Lavon Chaisson":.05},
  'NABERS_MAN':{'Rasul Douglas':.60,'Amik Robertson':.25,'Fabian Moreau':.15},  # Athletic (via Heavy): Douglas shadowed Nabers on perimeter for parts
  'TE_MAN':{'Quan Martin':.30,'Sonny Styles':.25,'Frankie Luvu':.15,'Mike Sainristil':.20,'Jeremy Reaves':.10},
 },
 'thu':{
  'OUT_L':{'Trey Amos':.85,'Rasul Douglas':.15},                                  # Amos RCB (stationed defense's right = offense's left), 97% W9
  'OUT_R':{'Amik Robertson':.60,'Rasul Douglas':.40},                             # Douglas LCB/right-coverage skew; Robertson outside when 3 safeties
  'NICKEL':{'Quan Martin':.50,'Amik Robertson':.35,'Rasul Douglas':.10,'Mike Sainristil':.05},
  'DEEP_L':{'Nick Cross':.40,'Jeremy Reaves':.40,'Quan Martin':.20},
  'DEEP_R':{'Nick Cross':.40,'Jeremy Reaves':.40,'Quan Martin':.20},
  'FS_MOFC':{'Jeremy Reaves':.55,'Quan Martin':.30,'Nick Cross':.15},
  'ROBBER':{'Nick Cross':.65,'Quan Martin':.25,'Jeremy Reaves':.10},
  'HOOK_L':{'Sonny Styles':.70,'Frankie Luvu':.30},
  'HOOK_R':{'Frankie Luvu':.70,'Sonny Styles':.30},
  'HOOK_M':{'Sonny Styles':.45,'Frankie Luvu':.45,'Dorance Armstrong':.05,"K'Lavon Chaisson":.05},
  'NABERS_MAN':{'Trey Amos':.45,'Amik Robertson':.35,'Rasul Douglas':.20},
  'TE_MAN':{'Nick Cross':.35,'Sonny Styles':.20,'Frankie Luvu':.15,'Quan Martin':.20,'Amik Robertson':.10},
 }}
# zone-role responsibility by target area (shell -> role weights). Generic Cover 2/6 vs Cover 3 rules.
def roles_for(side,db,shell,player):
    S='L' if side=='left' else 'R'
    slotty = player=='Isaiah Likely'
    if side in('left','right'):
        if db.startswith('short'):
            r={'two':{f'OUT_{S}':.55,f'HOOK_{S}':.25,'NICKEL':.20},'one':{f'OUT_{S}':.30,'NICKEL':.30,f'HOOK_{S}':.25,'ROBBER':.15}}[shell]
            if slotty: r={k:(v*.4 if k.startswith('OUT') else v) for k,v in r.items()}; r['NICKEL']=r.get('NICKEL',0)+.15; r[f'HOOK_{S}']+=.15
        elif db.startswith('inter'):
            r={'two':{f'OUT_{S}':.30,f'DEEP_{S}':.45,f'HOOK_{S}':.15,'NICKEL':.10},'one':{f'OUT_{S}':.50,'FS_MOFC':.20,f'HOOK_{S}':.15,'ROBBER':.15}}[shell]
            if slotty: r={k:(v*.5 if k.startswith('OUT') else v) for k,v in r.items()}; r['NICKEL']=r.get('NICKEL',0)+.10; r[f'HOOK_{S}']+=.05
        else:
            r={'two':{f'DEEP_{S}':.65,f'OUT_{S}':.35},'one':{f'OUT_{S}':.60,'FS_MOFC':.40}}[shell]
    else:
        if db.startswith('short'):
            r={'two':{'HOOK_M':.60,'NICKEL':.20,'DEEP_L':.10,'DEEP_R':.10},'one':{'HOOK_M':.50,'ROBBER':.30,'NICKEL':.20}}[shell]
        elif db.startswith('inter'):
            r={'two':{'DEEP_L':.25,'DEEP_R':.25,'HOOK_M':.40,'NICKEL':.10},'one':{'FS_MOFC':.35,'HOOK_M':.35,'ROBBER':.30}}[shell]
        else:
            r={'two':{'DEEP_L':.40,'DEEP_R':.40,'NICKEL':.20},'one':{'FS_MOFC':.70,'ROBBER':.30}}[shell]
    s=sum(r.values()); return {k:v/s for k,v in r.items()}
def man_roles(side,player):
    if player=='Isaiah Likely': return {'TE_MAN':1.0}
    if player=='Malik Nabers': return {'NICKEL':1.0} if side=='middle' else {'NABERS_MAN':1.0}
    return {('OUT_L' if side=='left' else 'OUT_R'):1.0} if side!='middle' else {'NICKEL':1.0}
def prior(side,db,player,era):
    pools=POOLS[era]; out={}
    for shell,ps in [('two',P_TWO_HIGH),('one',P_ONE_HIGH_ZONE)]:
        for role,w in roles_for(side,db,shell,player).items():
            for d,q in pools[role].items(): out[d]=out.get(d,0)+ps*w*q
    for role,w in man_roles(side,player).items():
        for d,q in pools[role].items(): out[d]=out.get(d,0)+P_MAN*w*q
    s=sum(out.values()); return {k:v/s for k,v in out.items()}
def top_roles(side,db,player):
    r=roles_for(side,db,'two',player); return ', '.join(f'{k} {v:.0%}' for k,v in sorted(r.items(),key=lambda x:-x[1])[:3])

# ---------- 4. Week 5 target map ----------
ABBR={'R.Douglas':'Rasul Douglas','A.Robertson':'Amik Robertson','S.Styles':'Sonny Styles','Q.Martin':'Quan Martin','F.Moreau':'Fabian Moreau',
      'J.Reaves':'Jeremy Reaves','F.Luvu':'Frankie Luvu','D.Armstrong':'Dorance Armstrong','M.Sainristil':'Mike Sainristil','K.Chaisson':"K'Lavon Chaisson"}
gb=pd.read_csv('/workspace/was_pass_def_2026-11-10/week5_nabers_likely_targets_gamebook.csv')
cw=pd.read_csv('/workspace/was_pass_def_2026-11-10/week5_nabers_likely_targets_crosswalk.csv')
gb=gb.merge(cw[['quarter','clock','target','pbp_play_id']],on=['quarter','clock','target'],how='left')
w5=p[p.game_id=='2026_05_NYG_WAS'].set_index('play_id')
fld=p[(p.game_id=='2026_05_NYG_WAS')&(p.receiver_player_name=='M.Fields')]
recs=[]
for _,r in gb.iterrows():
    pr=w5.loc[r.pbp_play_id] if pd.notna(r.pbp_play_id) and r.pbp_play_id in w5.index else None
    recs.append(dict(quarter=r.quarter,clock=r.clock,down=r.down,distance=r.distance,spot=r.spot,passer=r.passer,receiver=r.target,
        pass_location_gamebook=r.pass_location,air_yards_pbp=(pr.air_yards if pr is not None else np.nan),result=r.result,official_target=r.official_target,
        yards=r.yards,touchdown=r.touchdown,credits=r.named_tackler_or_pass_defender if isinstance(r.named_tackler_or_pass_defender,str) else '',
        interceptor=r.named_interception if isinstance(r.named_interception,str) else '',play_text=r.play_text,pbp_play_id=r.pbp_play_id))
for _,r in fld.iterrows():
    import re
    cr=re.findall(r'\d+-([A-Z]\.[A-Za-z\'-]+)\)?',r.desc.split(' for ')[-1]) if '(' in r.desc else []
    cr=[c for c in re.findall(r'\(([^)]*)\)',r.desc)[-1].split('; ')] if '(' in r.desc else []
    cr=[c.split('-',1)[1] for c in cr if '-' in c]
    recs.append(dict(quarter=r.qtr,clock=r.time,down=r.down,distance=r.ydstogo,spot=f"yardline_100={r.yardline_100}",passer=r.passer_player_name,receiver='Malachi Fields',
        pass_location_gamebook=f"{r.pass_length} {r.pass_location}",air_yards_pbp=r.air_yards,result='complete' if r.complete_pass==1 else 'incomplete',official_target=True,
        yards=r.yards_gained,touchdown=bool(r.touchdown),credits='; '.join(cr),interceptor='',play_text=r.desc,pbp_play_id=r.play_id))
m=pd.DataFrame(recs)
def side_of(s): return 'left' if 'left' in s else ('right' if 'right' in s else 'middle')
m['side']=m.pass_location_gamebook.apply(side_of)
def dband(r):
    a=r.air_yards_pbp
    if pd.isna(a): a=25 if 'deep' in r.pass_location_gamebook else 5
    return depth(a)
m['depth_band']=m.apply(dband,axis=1)
MEDIA={('Malik Nabers','4','1:48'):'Mike Sainristil',('Malik Nabers','OT','4:40'):'Mike Sainristil'}  # The Athletic (Duggan) via Heavy, Oct 15
out=[]
for _,r in m.iterrows():
    pri=prior(r.side,r.depth_band,r.receiver,'wk5')
    cred=[ABBR.get(c.strip(),c.strip()) for c in r.credits.split(';') if c.strip()]
    if r.interceptor: cred.append(ABBR.get(r.interceptor,r.interceptor))
    q='OT' if int(float(r.quarter))==5 else str(int(float(r.quarter)))
    media=MEDIA.get((r.receiver,q,r.clock))
    if media: fin={k:.5*v for k,v in pri.items()}; fin[media]=fin.get(media,0)+.5; basis='prior 50% + media attribution 50% (The Athletic via Heavy)'
    elif cred: fin={k:.6*v for k,v in pri.items()}; [fin.__setitem__(c,fin.get(c,0)+.4/len(cred)) for c in cred]; basis='prior 60% + official credit 40%'
    else: fin=pri; basis='prior only (no defender named)'
    top=sorted(fin.items(),key=lambda x:-x[1])[:3]
    zone_rank=sorted(pri.items(),key=lambda x:-x[1])
    agree= bool(cred) and any(c in [d for d,_ in zone_rank[:3]] for c in cred)
    out.append({**r.to_dict(),'zone_roles_two_high':top_roles(r.side,r.depth_band,r.receiver),
        'prior_top3':'; '.join(f'{d} {v:.0%}' for d,v in zone_rank[:3]),'official_credit_full':'; '.join(cred),'media_attribution':media or '',
        'credit_in_prior_top3':agree if cred else '', 'est_top1':top[0][0],'est_top1_p':round(top[0][1],3),'est_top2':top[1][0],'est_top2_p':round(top[1][1],3),
        'est_top3':top[2][0],'est_top3_p':round(top[2][1],3),'weights_json':json.dumps({k:round(v,4) for k,v in fin.items()}),'basis':basis,'label':CAVEAT})
wk5=pd.DataFrame(out); wk5.to_csv(OUT+'/wk5_target_zone_map.csv',index=False)

# crossing estimate
off=wk5[wk5.official_target==True]
cr=[]
for rc,g in off.groupby('receiver'):
    agg={};pri_agg={};credn={}
    for _,r in g.iterrows():
        for d,v in json.loads(r.weights_json).items(): agg[d]=agg.get(d,0)+v
        for d,v in prior(r.side,r.depth_band,rc,'wk5').items(): pri_agg[d]=pri_agg.get(d,0)+v
        for c in [x for x in r.official_credit_full.split('; ') if x]: credn[c]=credn.get(c,0)+1
        if r.media_attribution: credn[r.media_attribution+' (media)']=credn.get(r.media_attribution+' (media)',0)+1
    N=len(g)
    for d,v in sorted(agg.items(),key=lambda x:-x[1]):
        sh=v/N; ps=pri_agg.get(d,0)/N; c=credn.get(d,0); md=credn.get(d+' (media)',0)
        if sh>=.15 and (c+md)>=2 and ps>=.10: conf='high'
        elif sh>=.08 and ((c+md)>=1 or ps>=.12): conf='medium'
        else: conf='low'
        why=f"zone-prior share {ps:.0%} from {N} target locations; named on {c} official target(s)"+(f"; media-attributed on {md}" if md else '')
        cr.append(dict(receiver=rc,defender=d,official_targets=N,est_target_crossings=round(v,2),est_share_pct=round(100*sh,1),zone_prior_share_pct=round(100*ps,1),
            official_credit_targets=c,media_attributions=md,confidence=conf,reasoning=why,label=CAVEAT))
cx=pd.DataFrame(cr); cx=cx[cx.est_share_pct>=1].sort_values(['receiver','est_share_pct'],ascending=[True,False]); cx.to_csv(OUT+'/crossing_estimate.csv',index=False)

# ---------- Thursday projection ----------
AVAIL={'Trey Amos':'every-down RCB W8-9 (87%,97%); not in Week 5','Amik Robertson':'every-down 96-99%; NB on PFM/ESPN depth','Rasul Douglas':'active, reduced 46%/24% W8-9',
 'Nick Cross':'every-down SS W8-9; not in Week 5','Jeremy Reaves':'starting FS, 93%/60%','Quan Martin':'rotational 46%/56% (3rd safety)','Sonny Styles':'every-down ILB',
 'Frankie Luvu':'every-down ILB','Mike Sainristil':'0%/1% W8-9','Dorance Armstrong':'rotational OLB 53-58%',"K'Lavon Chaisson":'starting OLB 61-71%','Fabian Moreau':'UNCERTAIN: no W8 snaps, inactive W9'}
tp=[]
def proj(scope,g,rc):
    agg={}
    for _,r in g.iterrows():
        for d,v in prior(r.side,r.depth_band,rc,'thu').items(): agg[d]=agg.get(d,0)+v
    N=len(g)
    for d,v in sorted(agg.items(),key=lambda x:-x[1]):
        sh=v/N
        if sh<.01: continue
        conf='medium' if sh>=.18 else 'low'
        tp.append(dict(receiver=rc,scope=scope,targets_used=N,defender=d,est_share_pct=round(100*sh,1),confidence=conf,thursday_status=AVAIL.get(d,''),
             label=CAVEAT+'; projected personnel from W8-9 snaps + Nov 9-10 depth charts; inactives not posted'))
tt=t.copy()
for rc in NAMES.values():
    proj('season W1-9 target locations (nflverse pbp)',tt[tt.player==rc],rc)
    g=wk5[(wk5.receiver==rc)&(wk5.official_target==True)]
    proj('Week 5 target locations re-mapped to current WAS personnel',g,rc)
th=pd.DataFrame(tp); th.to_csv(OUT+'/thursday_projection.csv',index=False)
json.dump({'P_TWO_HIGH':P_TWO_HIGH,'P_MAN':P_MAN,'P_ONE_HIGH_ZONE':P_ONE_HIGH_ZONE,'POOLS':POOLS},open(OUT+'/model_assumptions.json','w'),indent=1)
v=wk5[(wk5.official_target==True)&(wk5.official_credit_full!='')]
print('VALIDATION credited official targets',len(v),'credit in prior top3',int((v.credit_in_prior_top3==True).sum()))
print(cx.groupby('receiver').head(6).to_string()); print(th.groupby(['receiver','scope']).head(4).to_string())
print(wk5[['receiver','quarter','clock','pass_location_gamebook','air_yards_pbp','result','official_credit_full','est_top1','est_top1_p','credit_in_prior_top3']].to_string())
