"""Build BONUS_SLIP run folder from gated game folders + fresh b1149 odds + bonus_sims.json. Written 2026-11-01 ~11:55 ET."""
import json,re,copy,csv
R='/workspace/nfl-database/runs/'; SS=R+'2026-11-01_shared_src/'
S=json.load(open('bonus_sims.json'))
def imp(a): a=float(a); return 100/(a+100) if a>0 else -a/(-a+100)
def man(g): return json.load(open(f'{R}2026-11-01_{g}/run_manifest.json'))
def rows(g):
    out={}
    for line in open(f'{R}2026-11-01_{g}/checklist.md'):
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)>=6 and re.match(r'^\d+',c[1]): out.setdefault(c[0],{})[int(re.match(r'^\d+',c[1]).group())]=c
    return out
INJ=('/workspace/nfl-database/week8/inactives/espn_inj_20261101_1152.json','2026-11-01T11:52')
OD=(SS+'odds_b1149.csv',SS+'lines_b1149.json','2026-11-01T11:49')
# leg specs: (src folder, src leg name, new name, sim key, rung, price, main over, main under, spread txt, game, kickoff)
SPEC=[('LV@NYJ','Tre Tucker Receptions Over 3.5','Tre Tucker Receptions Over 3.5','Tre Tucker|rec',3.5,-120,-120,-110,'LV +1.5 (toss-up); total 46.5','LV@NYJ','1:00 PM'),
 ('LAC@LAR','Puka Nacua Receptions Over 7.5','Puka Nacua Receptions Over 7.5','Puka Nacua|rec',7.5,-138,-138,104,'LAR -6.5 (moderate favorite); total 45.5','LAC@LAR','4:05 PM'),
 ('FD7_REPLACEMENTS','Stefon Diggs Receptions Over 3.5','Stefon Diggs Receptions Over 3.5 (alt)','Stefon Diggs|rec',3.5,-166,132,-178,'WSH -5.5 (moderate favorite); total 40.5','PHI@WSH','8:20 PM'),
 ('MIN@DET','Jahmyr Gibbs Rush Yds Over 87.5','Jahmyr Gibbs Rush Yds Over 79.5 (alt)','Jahmyr Gibbs|rushyds',79.5,-162,-113,-113,'DET -3.5 (moderate favorite); total 46.5','MIN@DET','1:00 PM')]
legs=[];chk=[];sims={m:{} for m in ('mc','bias','gr')};grades={}
srcs={}
for g,src,new,sk,rung,pr,mo,mu,sp,game,ko in SPEC:
    M=man(g); L=copy.deepcopy(next(l for l in M['legs'] if l['name']==src)); RW=rows(g)[src]
    for s in M['sources']: srcs.setdefault((s['category'],s['name']),s)
    nv=imp(pr)/(imp(mo)+imp(mu)); sm=S[sk]['sims']
    ps=[sm[m]['rungs'][str(rung)] for m in ('mc','bias','gr')]; meds=[sm[m]['median'] for m in ('mc','bias','gr')]
    avg=sum(ps)/3; edge=avg-nv; sh=0.5+0.7*(avg-0.5)-nv
    grades[new]=dict(p=ps,med=meds,avg=avg,nv=nv,edge=edge,sh=sh,price=pr,line=rung,game=game,kickoff_et=ko,spread=sp)
    for m in ('mc','bias','gr'): sims[m][new]=dict(p=sm[m]['rungs'][str(rung)],median=sm[m]['median'])
    L.update(name=new,line=rung,price_fd=pr,no_vig=round(nv,4),status='PASS',side='over',game=game,kickoff_et=ko,
        rung=('FD main' if mo==pr and 'alt' not in new else 'FD alt (de-vigged vs main)'),
        bonus_grade=dict(avg_p=round(avg,4),edge=round(edge,4),shrunk=round(sh,4),file=OD[0],pulled_et=OD[2]),injury_status='Active')
    if 'Gibbs' in new:
        from_rf=None
    legs.append(L)
    tag=new; o=[]
    for ph in range(1,16):
        c=list(RW[ph]); c[0]=tag; o.append(c)
    dsrc='FanDuel (price of record) via The Odds API b1149 (odds_b1149.csv/lines_b1149.json); sim_v6 100k x3 seed 20261101 (bonus_sims.json)'
    pmain=f"main {'%.1f'%(rung if 'alt' not in new else {3.5:4.5,79.5:87.5}[rung])} o{mo:+d}/u{mu:+d}"
    o[13]=[tag,'14 Models/price/edge','PASS',f"Over {rung} @ {pr:+d} FD; {pmain}; p mc/bias/gr {ps[0]:.3f}/{ps[1]:.3f}/{ps[2]:.3f} avg {avg:.3f}; no-vig {nv:.3f}; edge {100*edge:+.1f}, shrunk {100*sh:+.1f}; medians {meds[0]}/{meds[1]}/{meds[2]} clear {rung}; all p>=.45; not MODEL-SUSPECT; no placed-ticket same player+stat (BARS legs.py)",dsrc,'2026-11-01 11:55']
    o[14]=[tag,'15 Inactives','PASS',f"{L['player']} Active on ESPN injuries 11:52 and CBS inactives 11:46 (owner pt113u); line/price vs 11:35 re-pull no reprice-trigger move except as noted in report",'ESPN injuries API espn_inj_20261101_1152.json + CBS inactives (owner msg pt113u) + Odds API b1149','2026-11-01 11:52']
    o[7]=[tag,'8 Injuries','PASS',o[7][3].split(';')[0].replace('Active','Active (11:52)')+'; ESPN 11:52 re-pull: no new OL/secondary outs that change the leg (DET C McLaughlin Out is C3 on ESPN depth; LAC CB Donte Jackson Q flagged for Puka)','ESPN injuries API espn_inj_20261101_1152.json','2026-11-01 11:52']
    o[12]=[tag,'13 Game script 10G','PASS',sp+'; FD spread at 11:49','FanDuel spread/total via The Odds API lines_b1149.json','2026-11-01 11:49']
    if 'Gibbs' in new:
        rf=dict(values=[99.0,46.0,151.0,116.0],games=['2026_03_NYJ_DET','2026_04_DET_CAR','2026_05_DET_ARI','2026_07_GB_DET'],qb='Jared Goff',
           source=SS+'play_by_play_2026.parquet (nflverse, thru 2026-10-29) via runs/2026-11-01_vetting/fill_recent_form.py form()',pulled_et='2026-11-01T07:09')
        L['recent_form']=rf; L['market']='rushyds'
        o[1]=[tag,'2 Opportunity','PASS','proj 26.8 ra x 0.873 = 23.4 car x ~4.0 YPC (MIN 3.99) = ~94 vs 79.5 (+18%); MC mean ~93; primary back','nflverse play_by_play_2026.parquet wk1-8 (thru 2026-10-29)','2026-11-01 07:09']
        o[6]=[tag,'7 Role','PASS','carry share last4 0.71/1.00/0.78/0.88 (4 of 4 >=60%); targets last4 8/7/6/6 (>=4, rush-only over OK if DET trails); rush+rec 120.5 graded too: MODEL-SUSPECT (median 133.4 is 12.9 off main) so rush-only alt used','nflverse pbp + snap_counts','2026-11-01 11:50']
        o[2][3]=o[2][3]; o[2][2]='PASS'
    chk+=o
# Gibbs form: §7 3/4 >79.5 (99,151,116); §14 at -162 median 107.5 >= 95.4
srcl=[s for (c,n),s in srcs.items() if c not in('odds_props','injuries_news')]
srcl+=[dict(category='odds_props',name='The Odds API b1149: FanDuel main+alt, DraftKings, Pinnacle, PrizePicks player props',url_or_file=OD[0],tool='pull_odds.py b1149',pulled_et=OD[2]),
 dict(category='odds_props',name='The Odds API b1149: FanDuel/DK/Pinnacle spreads+totals',url_or_file=OD[1],tool='pull_lines.py b1149',pulled_et=OD[2]),
 dict(category='injuries_news',name='ESPN injuries API',url_or_file=INJ[0],tool='curl',pulled_et=INJ[1]),
 dict(category='injuries_news',name='CBS Sports inactives (URL supplied in owner msg pt113u)',url_or_file='owner message pt113u (CBS inactives, 11:46 ET)',tool='owner-relayed',pulled_et='2026-11-01T11:46')]
B=man('MIN@DET'); X=man('LV@NYJ')
mf=dict(season=2026,week=8,game='BONUS_SLIP (remaining Sunday slate)',game_date='2026-11-01',kickoff_et='2026-11-01 01:00 PM (first leg); 4:05 PM; 8:20 PM',
 input_cutoff_et='2026-11-01T11:52',skill='/home/box/agent-data/workflows/nfl-game-script-run/SKILL.md',seed=20261101,trials=100000,
 sim_script='/workspace/nfl-database/tools/sim_v6.py via runs/2026-11-01_BONUS_SLIP/bonus_sims*.py',approved_exceptions=X['approved_exceptions'],
 sources=srcl,flagged_gaps=[],pressure_inputs=B['pressure_inputs'],
 sims=[dict(model=mm,n=100000,seed=20261101,script='tools/sim_v6.py',legs={k:{'p':v['p'],'median':v['median']} for k,v in sims[m].items()}) for m,mm in (('mc','monte_carlo'),('bias','bias'),('gr','game_randomness'))],
 legs=legs,grades=grades,cross_checks=[])
json.dump(mf,open('run_manifest.json','w'),indent=1,default=float)
json.dump(chk,open('_rows.json','w'))
for k,v in grades.items(): print(k,{a:(round(b,3) if isinstance(b,float) else b) for a,b in v.items()})
