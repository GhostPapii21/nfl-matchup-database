"""CHI@SEA 2026-11-02 MNF: write checklist.md, run_manifest.json, report.md from sims_m0505.json/legs_m0505.json + hand-applied phase rulings
(assemble.py evaluate logic replicated by hand; Nov 2 approved rules applied manually). Does not touch gate/pipeline/sim code."""
import json,os
R='/workspace/nfl-database/runs/2026-11-02_CHI@SEA/'; S=R+'src/'
SM=json.load(open(S+'sims_m0505.json')); LG={f"{l['player']}|{l['market']}":l for l in json.load(open(S+'legs_m0505.json'))}
imp=lambda a:(100/(a+100)) if a>0 else (-a/(-a+100))
PB=S+'play_by_play_2026.parquet'; T='2026-11-02 05:05'; TI='2026-11-02T05:05'
SRC={'pbp':(PB+' (nflverse, data thru 2026-11-01)','2026-11-02 05:03'),'ftn':(S+'ftn_charting_2026.parquet + features.json','2026-11-02 05:03'),
 'pfr':('https://www.pro-football-reference.com/teams/chi/2026_advanced.htm (PFR adv defense, thru Wk7)','2026-11-02 05:10'),
 'wrcb':('/workspace/nfl-database/week8/sources/espn_wrcb_wk8.json (ESPN WR/CB cheatsheet Wk8)','2026-10-29 13:24'),
 'cov':('Sharp coverage schemes (Upd Oct 27) + StatRankings CoverageIQ, src/coverage_profile.json','2026-11-02 05:09'),
 'inj':(S+'espn_injuries.json (ESPN)','2026-11-02 05:04'),'ngs':(S+'ngs_*.parquet (nflverse NGS)','2026-11-02 05:03'),
 'film':(S+'film/ (NFL YouTube IDs; captions HTTP 429)','2026-11-02 05:09'),'wx':(S+'forecast_2026-11-02_0504.json (tools/weather_forecast.py NWS+Open-Meteo)','2026-11-02 05:04'),
 'odds':(S+'odds_m0505.csv (The Odds API FanDuel/DK/Pinnacle, pregame only)','2026-11-02 05:05'),'sim':(S+'sims_m0505.json (tools/sim_v6.py 3x100k seed 20261101)','2026-11-02 05:12'),
 'slips':('/workspace/nfl-database/week8/slips/*.md','2026-11-02 05:11')}
PH=['1 sample','2 opportunity','3 defense profile','4 defender','5 blitz/pressure','6 QB','7 role/snaps','8 injuries','9 NGS','10 film','11 weather','12 market/price','13 game script','14 edge/sims','15 correlation/placed']
DS=['pbp','pbp','pbp','pfr','ftn','ftn','pbp','inj','ngs','film','wx','odds','odds','sim','slips']
FILM=('UNVERIFIED','no caption re-match: YouTube auto-captions HTTP 429 on all 4 CHI/SEA Wk6-7 videos (yt-dlp + transcript API, 05:05-05:10)')
WX=('PASS','Lumen Field open-air; precip 3%, wind 4.1 mph, gust 4.7; no flag')
def leg(player,team,mk,pos,side,rung=None,rows=None,status='CUT',cut=None,press=None,note=None):
    l=LG[f'{player}|{mk}']; sm=SM['sims'][f'{player}|{mk}']; s=sm['sims']; fd=l['fd']
    if rung is None: line=fd['point']; price=fd['over'] if side=='over' else fd['under']; nv=fd['nv_over'] if side=='over' else fd['nv_under']; rl='FD main'
    else: line=rung; price=l['alts'][str(float(rung))]; nv=imp(price)/fd['overround']; rl='FD alt (de-vigged vs main overround %.3f)'%fd['overround']
    po={m:s[m]['rungs'][str(float(line))] for m in s}; p={m:(po[m] if side=='over' else 1-po[m]) for m in po}
    av=sum(p.values())/3; av2=(p['mc']+p['gr'])/2
    mkn={'passyds':'Pass Yds','recyds':'Rec Yds','rec':'Receptions','rushyds':'Rush Yds','rushrec':'Rush+Rec Yds'}[mk]
    name=f"{player} {mkn} {side.title()} {line}"
    e=dict(name=name,player=player,team=team,opp='SEA' if team=='CHI' else 'CHI',type=pos,market=mk,receiving=mk in('recyds','rec','rushrec'),side=side,line=line,price_fd=price,no_vig=round(nv,4),
      rung=rl,status=status,cut_reasons=cut or [],press=press,note=note,p={k:round(v,4) for k,v in p.items()},median={m:round(s[m]['median'],1) for m in s},
      edge_3=round(av-nv,4),edge_mc_gr=round(av2-nv,4),shrunk_mc_gr=round(0.5+0.7*(av2-0.5)-nv,4),gaps=[])
    e['rows']=rows; return e
def rows(over,film=True):
    out=[]
    for i in range(15):
        st,num=over.get(i+1,('PASS','see report'))
        if i+1==10 and film and (i+1) not in over: st,num=FILM
        if i+1==11 and (i+1) not in over: st,num=WX
        out.append((st,num))
    return out
L=[]
U='UNDERDOG CHI +3'
# ---- CHI
L.append(leg('Caleb Williams','CHI','passyds','QB','over',rows=rows({1:('PASS','4 Williams games: 269,138,305,308'),2:('PASS','starter; QB-RETURN flag (missed wk3-5) -> Williams-only games used'),3:('FAIL','SEA 158 pass yds/g allowed (#32 best), WR YPT 5.84'),5:('PASS','SEA blitz 22.1% (#30); Williams vs-blitz C, no-blitz A, protection D'),6:('PASS','card: money downs A, clutch A, CPOE +5.8'),7:('PASS','starter'),8:('PASS','Active'),12:('PASS','FD 227.5 -113/-113, nv .500'),13:('FAIL','10G: underdog over BLOCKED (no written exception)'),14:('FAIL','p mc/bias/gr .510/.510/.502; edge +.007 < .03')}),cut=['P3 SEA elite pass D','P13 10G underdog over','P14 edge +.007']))
L.append(leg('Luther Burden III','CHI','recyds','WR','under',rows=rows({1:('FAIL','§7 QB-RETURN: Williams-only L4 63,32,95,130 -> under 51.5 hits 1 of 4'),2:('PASS','tgt share .195 (CHI #1)'),3:('PASS','SEA WR YPT 5.84 (not soft)'),4:('PASS','ESPN WRCB: Nick Emmanwori (slot 50%); under side'),7:('PASS','slot 50%'),8:('PASS','Active'),12:('PASS','FD 51.5 -113/-113'),13:('PASS','spread 3 < 6.5'),14:('PASS','under p .543/.541/.551 (MC/GR avg .547), edge +.047 (model includes Keenum/Bagent games)')}),cut=['§7 Williams-only form: 1/4 unders hit (QB-RETURN; model contaminated by backup-QB games)']))
L.append(leg('Luther Burden III','CHI','rec','WR','under',rows=rows({1:('FAIL','Williams-only rec 5,3,8,4 -> under 4.5 hits 2/4'),14:('FAIL','under p .553/.553/.547 vs nv_under .572 -> edge -.02')}),cut=['P14 negative edge','§7 2/4']))
L.append(leg('Rome Odunze','CHI','recyds','WR','under',rows=rows({1:('FAIL','Williams-only 52,43,39,69 -> under 38.5 hits 0/4'),4:('PASS','ESPN WRCB: Devon Witherspoon'),14:('FAIL','under p .516/.519/.521 edge +.019 < .03')}),cut=['P14 edge < .03','§7 0/4']))
L.append(leg('Rome Odunze','CHI','rec','WR','under',rows=rows({1:('FAIL','Williams-only rec 2,3,3,4 -> under 3.5 hits 3/4'),14:('FAIL','under p .587/.586/.568 vs nv_under .601: edge -.02')}),cut=['P14 negative edge']))
L.append(leg('Colston Loveland','CHI','recyds','TE','under',rows=rows({1:('FAIL','Williams-only 0,3,65,69 (wk6-7 = post-Kmet role) -> under 42.5 hits 2/4'),2:('PASS','Kmet IR Oct 23: wk7 12 tgt 7-69; model mixes pre-Kmet/backup-QB games'),3:('PASS','SEA TE YPT 5.24'),4:('UNVERIFIED','TE defender mapping not ruled (ISS-05)'),13:('FAIL','could trail (CHI +3): check-down TE rec-yds under BLOCKED'),14:('UNVERIFIED','MODEL-SUSPECT: MC median 30.1 vs FD 42.5 (12.4 >= 12); under edge +.20 > .15')}),cut=['§7 2/4 Williams-only','P4 ISS-05','P13 could-trail TE under','P14 MODEL-SUSPECT (Kmet/backup-QB contamination)']))
L.append(leg('Colston Loveland','CHI','rec','TE','under',rows=rows({1:('FAIL','Williams-only rec 0,1,6,7 -> under 4.5 hits 2/4'),4:('UNVERIFIED','ISS-05'),14:('PASS','under p .620/.620/.603 vs nv_under .567: edge +.05')}),cut=['§7 2/4','P4 ISS-05 TE defender']))
L.append(leg("D'Andre Swift",'CHI','rushyds','RB','under',rows=rows({1:('FAIL','§7 QB-RETURN (Williams-only L4): 124,45,44,78 -> under 59.5 hits 2/4 (any-QB L4 58,43,44,78 = 3/4)'),2:('PASS','RB1; proj 16.2 carries (w_car); 15.7/g w/o Monangai wk5-7 (9,16,22)'),3:('PASS','SEA RB YPC allowed 3.40; opp YPC by game 3.52,4.12,2.80,4.59,4.36,2.78,3.12 (4 of 7 < 4.0)'),4:('N/A','rush yds'),7:('PASS','carry share lead back'),8:('PASS','Swift Active; Monangai OUT'),9:('PASS','RYOE/att -0.44'),12:('PASS','FD 59.5 -113/-113; DK 59.5'),13:('PASS','rush-only under not 10G-blocked; star-under allowed w/ data reason (Rico Oct 14): SEA 3.40 YPC + RYOE -0.44'),14:('PASS','under p .656/.658/.624, edge +.14/+.140 (MC,GR), medians 51.4/51.4/50.0 < 59.5; proj YPC vs SEA ~3.45 (4.10 x A_ypc .84)')}),cut=['§7 HARD: 2 of 4 with Williams (QB-RETURN)','P10 film unverified']))
L.append(leg("D'Andre Swift",'CHI','rushrec','RB','under',rows=rows({4:('UNVERIFIED','RB rush+rec: no LB/S alignment source'),13:('FAIL','underdog rush+rec under BLOCKED (10G)'),14:('PASS','under p .555/.558/.552 edge +.055')}),cut=['P13 10G','P4 unverified']))
L.append(leg("D'Andre Swift",'CHI','recyds','RB','over',rows=rows({4:('UNVERIFIED','RB receiving defender'),13:('FAIL','10G underdog over BLOCKED'),14:('FAIL','p .533/.537/.510 edge +.027 < .03')}),cut=['P13 10G','P14']))
L.append(leg("D'Andre Swift",'CHI','rec','RB','over',rows=rows({4:('UNVERIFIED','RB receiving defender'),13:('FAIL','10G underdog over BLOCKED'),14:('PASS','p .463/.465/.470 vs nv .390')}),cut=['P13 10G underdog over','P4']))
L.append(leg('Roschon Johnson','CHI','rushyds','RB','over',rows=rows({1:('PASS','4 games; fix A applied (Monangai OUT)'),3:('FAIL','SEA RB YPC 3.40 <= 3.8 run suppression'),7:('FAIL','RB2, no 60% carry share'),13:('FAIL','10G underdog over'),14:('UNVERIFIED','MODEL-SUSPECT: fixA p .80/.80/.74 vs nv .50 (edge > .15)')}),cut=['P3','P7','P13','P14 MODEL-SUSPECT']))
# ---- SEA
L.append(leg('Sam Darnold','SEA','passyds','QB','over',rows=rows({1:('FAIL','Darnold L4 168,195,278,257 -> over 238.5 hits 2/4'),3:('PASS','CHI 241 pass yds/g, WR YPT 9.51'),5:('FAIL','CHI blitz 41.1% (#4; StatRankings 43.2%) + LT Cross OUT -> Panthers rule CAUTION; exp sacks 2.9 (39 db x (.411x.099+.589x.056)) < 3'),6:('PASS','vs blitz C, protection D'),8:('FAIL','backup LT (Josh Jones) for Cross OUT -> no QB yardage overs'),14:('PASS','p .523/.522/.570 edge +.038, shrunk +.026')}),cut=['P8 backup OT -> no QB yardage over','§7 2/4']))
JSN=leg('Jaxon Smith-Njigba','SEA','recyds','WR','over',rung=89.5,rows=rows({1:('PASS','§7 Darnold-only L4 76,102,134,150 -> 3/4 >= 89.5; §14 (-166): L4 median 118 >= 1.20x89.5 = 107.4'),2:('PASS','tgt share .345 (#1), 12 tgt/g w/ Darnold L4 avg 10.5; Shaheed OUT (.133 share freed)'),3:('PASS','CHI WR YPT 9.51 (soft), middle 14.70'),4:('PASS','ESPN WRCB: Malik Muhammad (Q toe) - PFR thru Wk7: 31 tgt, 54.8% cmp, 8.4 YPT, 79.9 rtg; if out -> J. Johnson 31 tgt 77.4% 14.4 YPT 129.4 rtg / Stevenson 20 tgt 11.5 YPT; slot Gordon 2 tgt'),5:('PASS','CHI blitz 41.1%; JSN tgt share vs blitz lower but yds over not blitz-cut (Darnold vs-blitz C, not D/F)'),6:('PASS','Darnold starter (Lock games excluded from form); CAUTION: LT Cross OUT'),7:('PASS','WR1, snaps >= 85%'),8:('PASS','JSN Active; Shaheed OUT; CHI CB Muhammad Q'),9:('PASS','NGS row present; no separation flag used'),12:('PASS','FD alt 89.5 -166 (nv .588); main 99.5 -113/-113; Pinnacle 99.5 nv .504'),13:('PASS','SEA fav -3, could-trail rules N/A to WR over'),14:('UNVERIFIED','MODEL-SUSPECT: MC median 119.1 vs FD main 99.5 (+19.6 >= 12). p mc/bias/gr .711/.715/.647; MC+GR edge +.091; rung dropped one (margin >= 8.5)')}),
  cut=['P10 film UNVERIFIED (captions 429)','P14 MODEL-SUSPECT (press -> MANUAL REVIEW)'],press='PRESS candidate: matchup (Muhammad/Johnson), coverage (CHI 30-39% man, single-high 54%), script (SEA fav), QB (Darnold-only §7 3/4), MC .711 & GR .647 clear (2 independent votes; Bias=MC BUG-2026-11-02-BIASDUP) -> MANUAL REVIEW on numbers; gate status CUT only because Phase 10 film unverified')
L.append(JSN)
L.append(leg('Jaxon Smith-Njigba','SEA','rec','WR','over',rows=rows({1:('FAIL','Darnold L4 rec 5,5,12,9 -> 7.5 hits 2/4'),4:('FAIL','Muhammad cmp% 54.8 < 55 and margin (8 vs 7.5) < 20%'),14:('PASS','p .562/.563/.525 edge +.09')}),cut=['§7 2/4','P4 comp% rule']))
L.append(leg('Cooper Kupp','SEA','recyds','WR','over',rows=rows({1:('FAIL','Darnold L4 13,15,50,20 -> 1/4'),4:('PASS','ESPN WRCB: Kyler Gordon (slot)'),14:('FAIL','p .498/.502/.515 edge +.005')}),cut=['P14 no edge','§7']))
L.append(leg('Cooper Kupp','SEA','rec','WR','over',rows=rows({14:('FAIL','p .468/.470/.479 vs nv .575')}),cut=['P14 negative edge']))
L.append(leg('AJ Barner','SEA','recyds','TE','under',rows=rows({3:('FAIL','CHI TE YPT 8.61 >= 8 soft -> under cut'),4:('UNVERIFIED','ISS-05'),14:('PASS','under p .587/.587/.588')}),cut=['P3 soft TE D','P4 ISS-05']))
L.append(leg('AJ Barner','SEA','rec','TE','under',rows=rows({3:('FAIL','CHI TE YPT 8.61 soft'),4:('UNVERIFIED','ISS-05'),14:('PASS','under p .687 vs nv .586')}),cut=['P3','P4']))
L.append(leg('Emanuel Wilson','SEA','rushyds','RB','over',rows=rows({2:('FAIL','Charbonnet returns (no designation); FD 19.5 prices Wilson as RB2'),7:('FAIL','role change: split fix E carries-based only; Charbonnet 0 2026 games'),14:('UNVERIFIED','MODEL-SUSPECT: median 63.2 vs FD 19.5')}),cut=['P2/P7 role change','P14 MODEL-SUSPECT']))
# 15 placed check
for l in L:
    l['rows'][14]=('PASS','no CHI/SEA legs on week8/slips (slips_2026-11-01.md, sgp8_2026-10-30.md)')
    if l['player']=='Jaxon Smith-Njigba' and l['market']=='recyds': pass
# checklist
ck=['| Leg | Phase | Status | Number | Source | Pulled (ET) |','|---|---|---|---|---|---|']
for l in L:
    for i,(st,num) in enumerate(l['rows']):
        s,t=SRC[DS[i]]; ck.append(f"| {l['name']} | {PH[i]} | {st} | {num.replace('|','/')} | {s} | {t} |")
    l['gaps']=[f"P{i+1} {st}" for i,(st,_) in enumerate(l['rows']) if st in('FAIL','UNVERIFIED','MISSING','STALE')]
open(R+'checklist.md','w').write('\n'.join(ck)+'\n')
cov=json.load(open(S+'coverage_profile.json'))
def covblk(l):
    d=cov['teams'][l['opp']]; src='https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/'
    c=dict(man_zone=dict(man=d['man']/100,zone=d['zone']/100,source=src,pulled_et='2026-11-02T05:09',second_source=cov['second_source']),mof=dict(open=d['mof_open']/100,closed=d['mof_closed']/100,source=src,pulled_et='2026-11-02T05:09'))
    if l['player']=='Jaxon Smith-Njigba': c['defenders']=[dict(name='Malik Muhammad',targets=31,comp_pct=.548,ypt=8.4,rating=79.9,status='Questionable',source=SRC['pfr'][0],pulled_et='2026-11-02T05:10'),dict(name='Jaylon Johnson',targets=31,comp_pct=.774,ypt=14.4,rating=129.4,source=SRC['pfr'][0],pulled_et='2026-11-02T05:10'),dict(name='Tyrique Stevenson',targets=20,comp_pct=.60,ypt=11.5,rating=139.4,source=SRC['pfr'][0],pulled_et='2026-11-02T05:10')]
    return c
for l in L:
    if l['receiving'] or l['type']=='QB': l['coverage']=covblk(l)
    l.pop('rows')
src=lambda c,n,u,t,tool:dict(category=c,name=n,url_or_file=u,pulled_et=t,tool=tool,season=2026,data_week=8)
M=dict(game='CHI@SEA',season=2026,week=8,kickoff_et='2026-11-02T20:15',game_date='2026-11-02',venue='Lumen Field, Seattle WA',roof='open',
 skill='nfl-game-script-run',seed=20261101,trials=100000,sim_script='tools/sim_v6.py',
 sources=[src('core_stats_pbp','nflverse pbp 2026 (thru 2026-11-01; CHI last game Wk7 Thu, SEA Wk7 Sun; no Wk8 games yet)',PB,'2026-11-02T05:03','curl'),
  src('coverage_matchups','Sharp coverage schemes + StatRankings CoverageIQ',S+'coverage_profile.json','2026-11-02T05:09','web'),
  src('coverage_matchups','PFR Bears advanced defense (thru Wk7)','https://www.pro-football-reference.com/teams/chi/2026_advanced.htm','2026-11-02T05:10','web search'),
  src('coverage_matchups','FTN charting',S+'ftn_charting_2026.parquet','2026-11-02T05:03','curl'),
  src('ngs','nflverse NGS',S+'ngs_receiving.parquet','2026-11-02T05:03','curl'),
  src('film','NFL YouTube Wk6-7 CHI/SEA (captions 429 - UNVERIFIED)',S+'film/','2026-11-02T05:09','yt-dlp'),
  src('injuries_news','ESPN injuries API',S+'espn_injuries.json','2026-11-02T05:04','urllib'),
  src('weather','tools/weather_forecast.py (NWS + Open-Meteo)',S+'forecast_2026-11-02_0504.json','2026-11-02T05:04','tools/weather_forecast.py'),
  src('odds_props','The Odds API FanDuel/DK/Pinnacle pregame',S+'odds_m0505.csv','2026-11-02T05:05','pull_odds.py')],
 flagged_gaps=[dict(category='film',reason='YouTube captions HTTP 429 (05:05-05:10 ET); Phase 10 UNVERIFIED on every leg')],
 weather=dict(venue='Lumen Field',roof='open',precip_pct=3,wind_mph=4.1,gust_mph=4.7,flag=False,source=SRC['wx'][0],pulled_et='2026-11-02T05:04'),
 weather_forecast=[dict(game='CHI@SEA',roof='open',status='OK',precip_pct=3,wind_mph=4.1,gust_mph=4.7,flag=False,provider='NWS/Open-Meteo',pulled_et='2026-11-02T05:04')],
 pressure_inputs=dict(blitz_rate=dict(value=dict(CHI=.411,SEA=.221),source=S+'features.json (FTN)',pulled_et='2026-11-02T05:03',label='FTN charting'),
   pressure_rate=dict(value=dict(CHI=.223,SEA=.289),source=S+'features.json (pbp)',pulled_et='2026-11-02T05:03',label='PROXY'),
   checkdown_share=dict(value=dict(CHI=.306,SEA=.303),source=S+'features.json',pulled_et='2026-11-02T05:03'),
   time_to_throw=dict(value={'Caleb Williams':3.22,'Sam Darnold':3.00},source=S+'ngs_passing.parquet',pulled_et='2026-11-02T05:03')),
 sims=[dict(model=m,n=100000,seed=20261101,script='tools/sim_v6.py',legs={l['name']:dict(p=l['p'][k],median=l['median'][k]) for l in L}) for m,k in (('monte_carlo','mc'),('bias','bias'),('game_randomness','gr'))],
 model_note='BUG-2026-11-02-BIASDUP: bias model == MC (K_BIAS=SHRINK_K=30, same calib multipliers); only MC and GR are independent votes',
 placed_legs=[],inactives_watch_650pm=['Malik Muhammad II (CB, Q toe) - if out, JSN defender -> Jaylon Johnson/Stevenson; rerun P4','Zach Charbonnet (RB, returning) - SEA split','Drew Lock (QB, Q) - backup only'],
 legs=L)
json.dump(M,open(R+'run_manifest.json','w'),indent=1,default=float)
print(len(L),'legs',sum(1 for l in L if l['status']!='CUT'),'live')
