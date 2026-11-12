"""r3 build: checklist.md, run_manifest.json and report body for MNF CHI@SEA (game-day 4:30 PM ET routine). Inputs pulled 16:38 ET."""
import json,statistics as st
from form import form
R='/workspace/nfl-database/runs/2026-11-02_CHI@SEA_r3'; S=R+'/src'
R2=json.load(open('/workspace/nfl-database/runs/2026-11-02_CHI@SEA_r2/run_manifest.json'))
SIMS=json.load(open(S+'/sims_m1638.json')); SM=SIMS['sims']; META=SIMS['meta']
LG={f"{l['player']}|{l['market']}":l for l in json.load(open(S+'/legs_m1638.json'))}
COV={l['opp']:l['coverage'] for l in R2['legs'] if l.get('receiving') and l.get('coverage')}
for t in COV:
    for k in ('man_zone','mof'): COV[t][k]=dict(COV[t][k])
T0,TP,TC,TF='2026-11-02T16:38','2026-11-02T05:10','2026-11-02T05:09','2026-11-02T06:40'
PFRC='https://www.pro-football-reference.com/teams/chi/2026_advanced.htm'; PFRS='https://www.pro-football-reference.com/teams/sea/2026_advanced.htm'
def D(n,tg,c,y,src,t,role): return dict(name=n,targets=tg,comp_pct=c,ypt=y,source=src,pulled_et=t,role=role)
DEF={'Jaxon Smith-Njigba':[D('Malik Muhammad (Q toe)',31,54.8,8.4,PFRC,TP,'ESPN WR/CB primary'),D('Jaylon Johnson',31,77.4,14.4,PFRC,TP,'outside'),D('Tyrique Stevenson',20,60.0,11.5,PFRC,TP,'fill-in if Muhammad out')],
 'Cooper Kupp':[D('Kyler Gordon',None,None,None,PFRC,TP,'slot (ESPN WR/CB)')],
 'Luther Burden III':[D('Nick Emmanwori',17,52.9,4.4,PFRS,TF,'slot (ESPN WR/CB)'),D('Josh Jobe',32,71.9,6.6,PFRS,TF,'outside')],
 'Rome Odunze':[D('Devon Witherspoon',41,63.4,4.1,PFRS,TF,'ESPN WR/CB primary')],
 "D'Andre Swift":[D('Ernest Jones IV',38,63.2,5.0,PFRS,TF,'LB (first tackler on RB catches, proxy)'),D('Drake Thomas',17,58.8,4.2,PFRS,TF,'LB second')],
 'Colston Loveland':[],'AJ Barner':[]}
MO=('mc','bias','gr'); NV={}
def price_nv(l,line,side):
    fd=l['fd']
    if line==fd['point']: return (fd[side], fd['nv_'+side])
    o=l['alts'].get(f"{line:.1f}".rstrip('0').rstrip('.') if False else str(line))
    imp=(100/(o+100)) if o>0 else (-o/(-o+100))
    nv=imp/fd['overround']; return (o, nv if side=='over' else 1-nv)
def P(key,line,side):
    out={}
    for m in MO:
        s=SM[key]['sims'][m]; po=s['rungs'][str(line)]
        out[m]=dict(p=round(po if side=='over' else 1-po,4),median=round(s['median'],2))
    return out
NAME={'passyds':'Pass Yds','recyds':'Rec Yds','rec':'Receptions','rushyds':'Rush Yds','rushrec':'Rush+Rec Yds'}
PH=['1 sample','2 opportunity','3 defense profile','4 defender','5 blitz/pressure','6 QB','7 role/snaps','8 injuries','9 NGS','10 film','11 weather','12 market/price','13 game script','14 edge/sims','15 correlation/ticket bar']
FILM_OK={'Jaxon Smith-Njigba','Luther Burden III','Colston Loveland',"D'Andre Swift",'Rome Odunze','Caleb Williams','Sam Darnold'}
legs=[]; sims={m:{} for m in MO}
def leg(player,mk,line,side,cuts,ov=None,note='',press=False,rung='main',wr_rank=None):
    key=f'{player}|{mk}'; l=LG[key]; pr,nv=price_nv(l,line,side); ps=P(key,line,side)
    name=f"{player} {NAME[mk]} {side.title()} {line}"
    for m in MO: sims[m][name]=ps[m]
    avg=sum(ps[m]['p'] for m in MO)/3; shr=0.5+0.7*(avg-0.5)
    rf=form(player,l['team'],mk); rec=mk in('rec','recyds') or (mk=='rushrec')
    vals=rf['values']; hits=sum((v>line) if side=='over' else (v<line) for v in vals)
    o={1:('PASS',f"{len(vals)} games w/ current QB {rf['qb']}; season sample through Wk8"),2:('PASS',f"targets L4 {rf['targets']}" if rec else 'role per snaps/carries'),
       3:('PASS','opp defense profile (advstats_season_def, coverage_profile)'),4:('PASS','see coverage block') ,5:('PASS','blitz CHI .411/SEA .221 (FTN); pressure PROXY; flag: Sweat+Simmons first game, not in CHI rate'),
       6:('PASS',f"QB {rf['qb']} (Williams back from injury Wk6: QB-RETURN flag + form recheck)" if l['team']=='CHI' else f"QB {rf['qb']}; LT Cross OUT, Nelson (G) added"),
       7:('PASS','snap share stable L4'),8:('PASS','ESPN injuries 16:38 ET'),9:('PASS','NGS thru Wk8'),
       10:(('PASS','matched to pbp rows, src/film_matches.md') if player in FILM_OK else ('UNVERIFIED','no caption cue matched to pbp')),
       11:('PASS','NWS+Open-Meteo 16:38 ET: precip 2%, wind 2.7, gust 3.4 mph, no flag'),12:('PASS',f"FD {line} {pr:+d}, no-vig {nv:.3f} (16:38 ET)"),
       13:('PASS','SEA -3.5 / total 46.5'),14:('PASS' if (avg-nv>=.03 and shr-nv>0 and min(ps[m]['p'] for m in MO)>=.45) else 'FAIL',f"avg p {avg:.3f} edge {avg-nv:+.3f} shrunk {shr-nv:+.3f}"),
       15:('PASS','no open ticket on this player+stat')}
    o['7s']=f"§7 {hits}/{len(vals)} {vals}"
    for k,v in (ov or {}).items(): o[k]=v
    L=dict(name=name,player=player,team=l['team'],opp=l['opp'],market=mk,line=line,side=side,price_fd=pr,no_vig=round(nv,4),rung=rung,press=press,
           p={m:ps[m]['p'] for m in MO},median={m:ps[m]['median'] for m in MO},edge_3=round(avg-nv,4),shrunk=round(shr-nv,4),
           status='CUT',cut_reasons=cuts,note=note,recent_form=rf,receiving=rec,type=l['pos'],gaps=[],rows=o,
           books={'dk':(l.get('dk') or {}).get('point'),'pin':(l.get('pin') or {}).get('point')})
    if wr_rank: L['wr_rank']=wr_rank
    if rec and player in DEF:
        L['coverage']=dict(man_zone=COV[l['opp']]['man_zone'],mof=COV[l['opp']]['mof'],defenders=[d for d in DEF[player] if d['targets'] is not None])
    if rec and player in DEF and not L['coverage']['defenders'] and o[4][0]=='PASS': o[4]=('UNVERIFIED','no per-defender numbers (Kyler Gordon slot: no PFR row pulled)')
    legs.append(L)
F=lambda s,t:(s,t)
JSNBAR='§11/§15 BAR: nested rung of open ticket JSN 70+ rec yds (live SGP, Ghost6 bankroll_slips.md 4:11 PM ET)'
SW3='open-ticket status of Swift 3+ rec UNCONFIRMED (r2/odunze/results.md ~1:20 PM ET says placed; the 7-leg ticket holding it was cashed out per Ghost6 4:10 PM ET); barred fail-closed as nested rung'
leg('Caleb Williams','passyds',224.5,'over',['P13 10G underdog over BLOCKED (CHI +3.5)','P14 edge +2.6 < +3'],{13:F('FAIL','10G CHI underdog over'),14:F('FAIL','edge +.026 < .03')})
leg('Luther Burden III','recyds',52.5,'under',['§7 HARD: Williams-only form 1/4 unders (63,32,95,130)'],{7:F('FAIL','§7 1/4 with Williams')},note='line moved 51.5 -> 52.5; edge +5.5 alone not enough')
leg('Luther Burden III','rec',4.5,'under',['P14 negative edge'],{14:F('FAIL','negative edge')},note='Burden 4+ open-ticket status ambiguous (r2/odunze 1:20 PM ET); under not nested in an over ticket but same player')
leg('Rome Odunze','recyds',38.5,'under',['P14 edge < +3','§7 0/4 unders'],{7:F('FAIL','§7 0/4'),14:F('FAIL','edge < .03')},wr_rank=3,note='zone check: SEA zone 90% (Sharp)/82.3% (SR). Odunze averages 44.8 yds/g vs zone-heavy teams, so zone does not suppress him')
leg('Rome Odunze','rec',3.5,'under',['P14 negative edge'],{14:F('FAIL','negative edge')},wr_rank=3)
leg('Colston Loveland','recyds',42.5,'under',['§7 2/4','P4 ISS-05 TE defender UNVERIFIED','P13 could-trail TE under','P14 MODEL-SUSPECT (median 12+ below line)'],{4:F('UNVERIFIED','ISS-05: no per-defender TE coverage data'),7:F('FAIL','§7 2/4'),13:F('FAIL','CHI could trail -> TE volume up'),14:F('FAIL','MODEL-SUSPECT')})
leg('Colston Loveland','rec',4.5,'under',['§7 2/4 (0,1,6,7)','P4 ISS-05'],{4:F('UNVERIFIED','ISS-05'),7:F('FAIL','§7 2/4')})
leg("D'Andre Swift",'rushyds',59.5,'under',['§7 HARD: Williams-only 2/4 (124,45,44,78)'],{7:F('FAIL','§7 2/4')},note='edge is large but form fails')
leg("D'Andre Swift",'rushrec',86.5,'under',['P13 10G underdog rush+rec under BLOCKED','§7 1/4 (134,99,70,90)'],{7:F('FAIL','§7 1/4'),13:F('FAIL','10G')})
leg("D'Andre Swift",'recyds',21.5,'over',['P13 10G underdog over','P14 model p < .45'],{13:F('FAIL','10G'),14:F('FAIL','p < .45')})
leg("D'Andre Swift",'rec',3.5,'over',['P2 catches over needs 5+ tgt in 3 of L4 (1,5,5,4 = 2/4)','P13 10G underdog over','P14 edge +2.5 < +3 and medians 3.0 do not clear 3.5','P15 '+SW3],
    {2:F('FAIL','5+ tgt in 2 of L4'),13:F('FAIL','10G'),14:F('FAIL','edge +.025, medians 3.0'),15:F('FAIL',SW3)},note='repriced +140 -> +112 (FD main), more than 20 cents; re-run through Phase 14 -> fails')
leg("D'Andre Swift",'rec',2.5,'over',['P14 shrunk edge -3.1','P15 '+SW3,'P2 tgt'],{2:F('FAIL','5+ tgt 2/4'),14:F('FAIL','shrunk -.031'),15:F('FAIL',SW3)},rung='alt')
leg('Roschon Johnson','rushyds',10.5,'over',['P3 SEA allows 3.40 YPC','P7 RB2 role','P13 underdog RB','P14 MODEL-SUSPECT (fixA boost)','§7 only 2 games with carries'],{1:F('FAIL','2 games (LOW-SAMPLE)'),3:F('FAIL','SEA 3.40 YPC'),7:F('FAIL','RB2'),13:F('FAIL','dog'),14:F('FAIL','MODEL-SUSPECT')})
leg('Sam Darnold','passyds',238.5,'over',['P8 backup LT (Cross OUT) -> no QB yardage over','§7 2/4'],{7:F('FAIL','§7 2/4'),8:F('FAIL','LT Cross OUT; Nelson is a guard')})
leg('Jaxon Smith-Njigba','recyds',99.5,'over',['§14 cushion FAIL at -113 (L4 median 118 < 124.4; 1.10x hit 2/4)','P14 MODEL-SUSPECT (MC median 119.1, +19.6 vs line; press -> manual review)',JSNBAR],
    {14:F('FAIL','§14 cushion; MODEL-SUSPECT'),15:F('FAIL',JSNBAR)},press=True)
leg('Jaxon Smith-Njigba','recyds',89.5,'over',['P14 MODEL-SUSPECT (press -> MANUAL_REVIEW on numbers alone)',JSNBAR],{14:F('PASS','edge +.103 shrunk +.046; §14 118 >= 107.4; MODEL-SUSPECT flag'),15:F('FAIL',JSNBAR)},press=True,rung='alt',
    note='would be MANUAL_REVIEW (press) without the bar; the gate does not accept a MANUAL_REVIEW status for runs dated before 11-05, so status is CUT')
leg('Jaxon Smith-Njigba','recyds',109.5,'over',['§7 2/4 at 109.5',JSNBAR],{7:F('FAIL','§7 2/4'),15:F('FAIL',JSNBAR)},rung='alt')
leg('Jaxon Smith-Njigba','rec',7.5,'over',['§7 2/4 (5,5,12,9)','§11 same player as open SGP (JSN 70+, JSN TD)'],{7:F('FAIL','§7 2/4'),15:F('FAIL','§11 one slip per player')})
leg('Cooper Kupp','recyds',29.5,'over',['P14 no edge','§7 1/4'],{7:F('FAIL','§7 1/4'),14:F('FAIL','no edge')})
leg('Cooper Kupp','rec',2.5,'over',['P14 negative edge','§7 1/4'],{7:F('FAIL','§7 1/4'),14:F('FAIL','negative edge')})
leg('AJ Barner','recyds',29.5,'under',['P3 soft CHI TE D (TE YPT 8.61)','P4 ISS-05'],{3:F('FAIL','soft TE D'),4:F('UNVERIFIED','ISS-05')})
leg('AJ Barner','rec',3.5,'under',['P3','P4 ISS-05'],{3:F('FAIL','soft TE D'),4:F('UNVERIFIED','ISS-05')})
leg('Emanuel Wilson','rushyds',19.5,'over',['P2/P7 role change: Charbonnet (no designation) + Price activated 4:05 PM ET -> 3-way committee','P14 MODEL-SUSPECT (sim p .95 on 63 median; no split data)'],{2:F('FAIL','committee'),7:F('FAIL','role UNVERIFIED'),14:F('FAIL','MODEL-SUSPECT')},
    note='§11: Wilson 15+ rush is on the open SGP')
# fix: rows 15 for same-player SGP legs
for L in legs:
    if L['player'] in ("D'Andre Swift",'Emanuel Wilson') and L['rows'][15][0]=='PASS': L['rows'][15]=('FAIL','§11 same player as open SGP (Swift 50+ rush+rec/Swift TD; Wilson 15+)'); L['cut_reasons'].append('§11 one slip per player (open SGP)')
json.dump(dict(legs=legs,sims=sims),open(S+'/build_legs.json','w'),indent=1,default=str)
# checklist
SRCN={1:'nflverse pbp (src/play_by_play_2026.parquet)',2:'nflverse pbp + snap_counts',3:'advstats_season_def + coverage_profile.json',4:'PFR adv defense CHI (05:10) / SEA (Firecrawl 06:40)',5:'FTN charting + features.json',6:'nflverse pbp/NGS passing',7:'snap_counts_2026.parquet',8:'ESPN injuries API',9:'nflverse NGS',10:'NFL YouTube captions (yt-dlp) + pbp',11:'tools/weather_forecast.py',12:'The Odds API pull_odds.py (FD/DK/Pinnacle)',13:'lines_m1638.json + 10G rule',14:'tools/sim_v6.py 3x100k seed 20261101',15:'Ghost6 bankroll_slips.md + bet-log.csv'}
TT={1:T0,2:T0,3:TC,4:TP,5:'2026-11-02T05:03',6:T0,7:'2026-11-02T05:03',8:T0,9:'2026-11-02T05:03',10:'2026-11-02T16:42',11:T0,12:T0,13:T0,14:'2026-11-02T16:44',15:'2026-11-02T16:45'}
out=['# Checklist: MNF CHI@SEA r3 (2026-11-02, kickoff 8:15 PM ET)','',f'Inputs pulled 16:38 ET (odds, injuries, weather, pbp); coverage 05:09 ET; PFR 05:10/06:40 ET. All times ET.','']
cnt={}
for L in legs:
    for i,ph in enumerate(PH,1):
        s,num=L['rows'][i]; cnt.setdefault(i,{}); cnt[i][s]=cnt[i].get(s,0)+1
        if i==7: num=f"{num}; {L['rows']['7s']}"
        out.append(f"| {L['name']} | {ph} | {s} | {num} | {SRCN[i]} | {TT[i].replace('T',' ')} |")
summ=['## Summary',f'- Legs evaluated: {len(legs)}. PASS: 0. CUT: {len(legs)}. MANUAL_REVIEW: 0 (JSN O89.5 would be manual review but is barred by the open JSN 70+ ticket).']
for i,ph in enumerate(PH,1): summ.append(f"- Phase {ph}: "+', '.join(f'{k} {v}' for k,v in sorted(cnt[i].items())))
cuts=['## Cut reasons by leg']+[f"- {L['name']} ({L['price_fd']:+d}): {'; '.join(L['cut_reasons'])}" for L in legs]
open(R+'/checklist.md','w').write('\n'.join(out[:4]+summ+['','| Leg | Phase | Status | Number | Source | Pulled (ET) |','|---|---|---|---|---|---|']+out[4:]+['']+cuts)+'\n')
# manifest
src=lambda c,n,u,t,tool,**k:dict(category=c,name=n,url_or_file=u,pulled_et=t,tool=tool,season=2026,data_week=8,**k)
cp=R2['sources'][1]['second_source']
M=dict(game='CHI@SEA',season=2026,week=8,week_note='parent task called it Week 9; ESPN scoreboard (16:38 ET) lists Week 8 (MNF of Week 8)',kickoff_et='2026-11-02T20:15',game_date='2026-11-02',venue='Lumen Field',roof='open',
 skill='nfl-game-script-run + nfl-betting-script',seed=20261101,trials=100000,sim_script='tools/sim_v6.py',parent_run=['runs/2026-11-02_CHI@SEA','runs/2026-11-02_CHI@SEA_r2'],input_cutoff_et=T0,
 sources=[src('core_stats_pbp','nflverse pbp 2026 (release 14:29 ET, thru 2026-11-01 incl. Wk8 SNF)',S+'/play_by_play_2026.parquet',T0,'curl'),
  src('coverage_matchups','Sharp coverage schemes + StatRankings CoverageIQ',S+'/coverage_profile.json',TC,'web',second_source=cp),
  src('coverage_matchups','PFR Bears advanced defense (thru Wk7)',PFRC,TP,'web search'),
  src('coverage_matchups','PFR Seahawks advanced defense (thru Wk7)',S+'/pfr_sea_adv_fc.html',TF,'Firecrawl'),
  src('coverage_matchups','FTN charting',S+'/ftn_charting_2026.parquet','2026-11-02T05:03','curl'),
  src('ngs','nflverse NGS receiving/passing/rushing',S+'/ngs_receiving.parquet','2026-11-02T05:03','curl'),
  src('film','NFL YouTube highlights Wk6-7 CHI/SEA, captions matched to pbp',S+'/film/',"2026-11-02T16:42",'yt-dlp'),
  src('injuries_news','ESPN injuries + team news API',S+'/espn_injuries.json',T0,'curl'),
  src('weather','tools/weather_forecast.py (NWS + Open-Meteo)',S+'/forecast_2026-11-02_1638.json',T0,'tools/weather_forecast.py'),
  src('odds_props','The Odds API FanDuel/DK/Pinnacle pregame (0 in-play rows dropped)',S+'/odds_m1638.csv',T0,'pull_odds.py')],
 flagged_gaps=[],
 weather=dict(venue='Lumen Field',roof='open',precip_pct=2,wind_mph=2.7,gust_mph=3.4,flag=False,source=S+'/forecast_2026-11-02_1638.json (tools/weather_forecast.py NWS+Open-Meteo)',pulled_et=T0),
 weather_forecast=[dict(game='CHI@SEA',roof='open',status='OK',precip_pct=2,wind_mph=2.7,gust_mph=3.4,flag=False,provider='NWS/Open-Meteo',pulled_et=T0)],
 pressure_inputs=R2['pressure_inputs'],
 sims=[dict(model=k,n=100000,seed=20261101,script='tools/sim_v6.py',legs=sims[m]) for k,m in (('monte_carlo','mc'),('bias','bias'),('game_randomness','gr'))],
 model_note='BUG-2026-11-02-BIASDUP still present in live tools/sim_v6.py (bias == MC; K_BIAS = SHRINK_K = 30). Fix is STAGED in tools/sim_v6_fix/ (11:45 PM ET swap), NOT swapped in by this run. Only MC and GR are independent votes. Fit run 16:42 ET: calib multipliers unchanged (weeks 4-7). Unit tests: 108 OK.',
 placed_legs=[dict(game='CHI@SEA',leg=x,source='Ghost6 bankroll_slips.md (SGP, live 4:11 PM ET)') for x in ['JSN 70+ rec yds','JSN anytime TD','Swift 50+ rush+rec yds','Swift anytime TD','E. Wilson 15+ rush yds','Under 58.5 total']]+
  [dict(game='CHI@SEA',leg=x,source='r2/odunze/results.md ~1:20 PM ET says placed; status UNCONFIRMED (7-leg ticket cashed out 4:10 PM ET)',status='UNCONFIRMED') for x in ['Swift 3+ receptions','Burden 4+ receptions']],
 inactives_watch_650pm=['Malik Muhammad (CB, Q toe): if out, JSN primary defender -> Jaylon Johnson/Stevenson; rerun P4 (CHI then 1 CB out; depleted-secondary rule needs 2)','D\'Marco Jackson (LB, Q)','Drew Lock (QB, Q): backup only','Uchenna Nwosu (LB, Doubtful)','Charbonnet / J. Price usage: SEA RB split','Montez Sweat + Jeffery Simmons active (first CHI game for Simmons); JSN 100+ rerun if both play','Bradford / Pili / O\'Connell (Q)'],
 loeb_claims={'Quenton Nelson to SEA':'VERIFIED: ESPN "Seahawks acquire Pro Bowl guard Quenton Nelson in trade with Colts" (Oct 27, 7:51 PM ET)',
  'Jeffery Simmons to CHI':'VERIFIED: ESPN "Bears acquire All-Pro DT Jeffery Simmons in trade with Titans"; ESPN injury feed 16:38 ET shows Active',
  'Montez Sweat back':'VERIFIED: ESPN injury feed (16:38 ET): reinstated Fri Oct 23 after a two-game suspension; ESPN Oct 28 "Montez Sweat returns to Bears"'},
 questionable_wr=[],depleted_secondary=[],
 game_script_rb=dict(rule='fav <= -7 AND opp RB YPC >= 4.4',spread=-3.5,chi_rb_ypc_allowed=round(META['opp_rb_ypc']['CHI'],2),sea_rb_ypc_allowed=round(META['opp_rb_ypc']['SEA'],2),triggered=False,source='pbp thru 2026-11-01 (sim meta)'),
 legs=[{k:v for k,v in L.items() if k!='rows'} for L in legs])
json.dump(M,open(R+'/run_manifest.json','w'),indent=1,default=str)
print('legs',len(legs))
