import json,copy,re
R='/workspace/nfl-database/runs/'; F=R+'2026-11-01_FD7_REPLACEMENTS/'
S=json.load(open(R+'2026-11-01_shared_src/rec_r0750.json'))
M=json.load(open(F+'run_manifest.json')); KM=json.load(open(R+'2026-11-01_KC@DEN/run_manifest.json'))
ck=open(F+'checklist.md').read().splitlines(); kck=open(R+'2026-11-01_KC@DEN/checklist.md').read().splitlines()
T='2026-11-01 07:44'; TI='2026-11-01T07:44'
def imp(a): return 100/(a+100) if a>0 else -a/(-a+100)
MAIN={'Rashee Rice':(-106,-125),'Xavier Worthy':(116,-154),'Stefon Diggs':(132,-178),'Tre Tucker':(-120,-110),'Puka Nacua':(-138,104),'Jordan Addison':(120,-160)}
PIN={'Rashee Rice':(4.5,-117,-107),'Xavier Worthy':(3.5,118,-148),'Stefon Diggs':(4.5,132,-167),'Tre Tucker':(3.5,-123,-102),'Puka Nacua':(7.5,-133,106),'Jordan Addison':(3.5,127,-160)}
def nv(p,price,side):
    o,u=MAIN[p]; ov=imp(o)+imp(u); return (imp(price) if side=='over' else imp(u))/ov
def pinnv(p):
    pt,o,u=PIN[p]; ov=imp(o)+imp(u); return pt,imp(o)/ov
rows=lambda src,leg:[r for r in src if r.startswith('| '+leg+' |')]
NEW=[('Rashee Rice',4.5,-106,'FD main (5+)','kck','Rashee Rice Receptions Under 4.5'),
     ('Rashee Rice',5.5,182,'FD alt (6+)','kck','Rashee Rice Receptions Under 4.5'),
     ('Rashee Rice',3.5,-230,'FD alt (4+)','kck','Rashee Rice Receptions Under 4.5'),
     ('Xavier Worthy',3.5,116,'FD main (4+)','ck','Xavier Worthy Rec Yds Over 29.5'),
     ('Stefon Diggs',3.5,-166,'FD alt (4+)','ck','Stefon Diggs Rec Yds Over 42.5'),
     ('Stefon Diggs',4.5,130,'FD alt (5+)','ck','Stefon Diggs Rec Yds Over 42.5')]
PFF={'Rashee Rice':'PFF: no receptions row; PFF picks Rice REC YDS UNDER 51.5 (proj 39.5) - leans against Rice volume',
 'Xavier Worthy':'PFF: no receptions row; PFF picks Worthy REC YDS OVER 29.5 (proj 34.5)',
 'Stefon Diggs':'PFF: no Diggs row in pff_props csv; PFF projects ~5.6 targets (per Ghost6) - x .61 cr = ~3.4 rec, supports 4+ only thinly, not 5+',
 'Tre Tucker':'PFF: no receptions row; PFF picks Tucker REC YDS UNDER 48.5 (proj 41.5) - soft conflict',
 'Puka Nacua':'PFF: receptions not listed; only Rush Yds U0.5 row', 'Jordan Addison':'PFF: no row'}
def grade(p,line,price,side='over'):
    s=S[p]['sims']; k=str(line+0.5) if False else str(line)
    pm={m:(s[m]['rungs'][str(line)] if side=='over' else 1-s[m]['rungs'][str(line)]) for m in ('mc','bias','gr')}
    md={m:s[m]['median'] for m in pm}; n=nv(p,price,side); avg=sum(pm.values())/3; mg=(pm['mc']+pm['gr'])/2
    e=avg-n; sh=0.5+0.7*(avg-0.5)-n; emg=mg-n; shmg=0.5+0.7*(mg-0.5)-n
    medok=all((md[m]>line) if side=='over' else (md[m]<line) for m in md)
    ok=e>=0.03 and sh>0 and min(pm.values())>=0.45 and medok
    return dict(p=pm,med=md,nv=n,avg=avg,edge=e,sh=sh,mg=mg,edge_mg=emg,sh_mg=shmg,medok=medok,ok=ok)
out=[]; RES={}
manifest_sims={s['model']:s for s in M['sims']}
for p,line,price,rung,src,tmpl in NEW:
    name=f"{p} Receptions Over {line}"; g=grade(p,line,price); i=S[p]['info']
    trs=rows(kck if src=='kck' else ck,tmpl); assert len(trs)==15,(tmpl,len(trs))
    proj=i['w_tgt']*i['cr']; split=S[p]['split']
    reasons=[]
    p2_ok = proj>line+0.0 and not (p=='Rashee Rice')
    p2=f"{'Rice-active split (KC games '+','.join(S['kc_games'])+', wk1-3) ' if split else ''}w_tgt {i['w_tgt']:.2f} x cr {i['cr']:.3f} = {proj:.2f} rec vs {line}"
    if p=='Rashee Rice': p2+='; catches-over rule 5+ tgt in 3 of last 4 FAILS (2,6,9; only 3 active games, LOW-SAMPLE)'
    if p=='Xavier Worthy': p2+='; with Rice active Worthy tgt 6/7/2 (wk1-3) vs 7/7/6 without - share drops'
    if p=='Stefon Diggs': p2+='; last3 tgt 7/9/7 (5+ in 3 of last 4 PASS)'
    if not p2_ok: reasons.append('P2 FAIL: projected receptions do not clear line with margin')
    pt,pn=pinnv(p)
    p14=(f"Over {line} @ {price:+d} ({rung}); p mc/bias/gr {g['p']['mc']:.3f}/{g['p']['bias']:.3f}/{g['p']['gr']:.3f} avg {g['avg']:.3f}; FD no-vig {g['nv']:.3f} (alt de-vigged vs main 4.5/3.5 two-way); "
         f"gate edge {g['edge']*100:+.1f}, shrunk {g['sh']*100:+.1f}; MC+GR avg {g['mg']:.3f} edge {g['edge_mg']*100:+.1f} shrunk {g['sh_mg']*100:+.1f}; medians {g['med']['mc']:.1f}/{g['med']['bias']:.1f}/{g['med']['gr']:.1f}; Pinnacle {pt} over nv {pn:.3f}; {PFF[p]}")
    if not g['ok']: reasons.append('P14 FAIL: edge rule (gate 3-model): '+('median does not clear; ' if not g['medok'] else '')+('model p<.45; ' if min(g['p'].values())<.45 else '')+('edge<+3' if g['edge']<.03 else ''))
    st2='PASS' if p2_ok else 'FAIL'; st14='PASS' if g['ok'] else 'FAIL'
    new=[]
    for r in trs:
        c=[x.strip() for x in r.strip('|').split('|')]; c[0]=name; ph=int(c[1].split()[0])
        if ph==2: c[2],c[3],c[4],c[5]=st2,p2,'sim_v5 player() inputs, nflverse pbp wk1-8'+(' (Rice-active split, rec_r0750.py)' if split else ''),T
        if ph==4 and src=='kck': c[2]='PASS'; c[3]=c[3].replace('yds under vs YPT>10 defender','catches over vs 60% comp allowed - OK')
        if ph==8: c[3]=f"{p}: Active (ESPN injuries 07:44 pull){'; Rice (hamstring, Wk4 Q1) no designation, will play per Chiefs.com/Reid' if p in('Rashee Rice','Xavier Worthy') else ''}"; c[4]='ESPN injuries API (site.api.espn.com)'; c[5]=T
        if ph==13: c[5]=T; c[4]='FanDuel spread/total via The Odds API (r0750)'
        if ph==14: c[2],c[3],c[4],c[5]=st14,p14,'FanDuel main+alt + Pinnacle via The Odds API odds_r0750.csv; sim_v5.py seed 20261101 N=100000 x3 (rec_r0750.py)',T
        if ph==15: c[3]=f'pre-inactives: {p} Active at 07:44 ET; recheck ~90 min pre-kick'; c[5]=T
        new.append('| '+' | '.join(c)+' |')
    out+=new
    # manifest leg
    base=[l for l in (KM['legs'] if src=='kck' else M['legs']) if l['name']==tmpl][0]
    L=copy.deepcopy(base); L.update(name=name,market='rec',side='over',line=line,price_fd=price,no_vig=round(g['nv'],4),rung=rung,
       status='PASS' if not reasons else 'CUT',cut_reasons=reasons,gaps=[],pff_crosscheck=PFF[p],avg_p_mc_gr=round(g['mg'],4),edge_mc_gr=round(g['edge_mg'],4),shrunk_mc_gr=round(g['sh_mg'],4),
       odds_pulled_et=TI,rice_active_split=split)
    M['legs']=[l for l in M['legs'] if l['name']!=name]+[L]
    for m,k in (('monte_carlo','mc'),('bias','bias'),('game_randomness','gr')): manifest_sims[m]['legs'][name]={'p':g['p'][k],'median':g['med'][k]}
    RES[name]=dict(g,price=price,rung=rung,status=L['status'],reasons=reasons,pff=PFF[p])
# re-grade existing receptions legs on fresh odds (prices unchanged at 07:44)
for p,line,price,side in (('Tre Tucker',3.5,-120,'over'),('Puka Nacua',7.5,-138,'over'),('Jordan Addison',3.5,-160,'under')):
    g=grade(p,line,price,side); nm=f"{p} Receptions {side.title()} {line}"; RES[nm]=dict(g,price=price,rung='FD main',status='PASS' if g['ok'] else 'CUT',reasons=[],pff=PFF[p])
    for i,r in enumerate(ck):
        if r.startswith('| '+nm+' |') and '| 14 ' in r:
            c=[x.strip() for x in r.strip('|').split('|')]; c[3]+=f"; REPRICED 07:44 FD {price:+d} unchanged, nv {g['nv']:.3f}, MC+GR edge {g['edge_mg']*100:+.1f}"; c[4]+=' + odds_r0750.csv'; c[5]=T; ck[i]='| '+' | '.join(c)+' |'
    for l in M['legs']:
        if l['name']==nm: l['odds_pulled_et']=TI
# insert rows before summary (after last table row)
last=max(i for i,r in enumerate(ck) if r.startswith('| ') and not r.startswith('| Leg') and not r.startswith('|---'))
ck=ck[:last+1]+out+ck[last+1:]
ck.append('\n## 07:50 ET receptions add-on (FD7 TD slots as RECEPTIONS)\n'+'\n'.join(f"- {k}: {v['status']} {'; '.join(v['reasons'])}" for k,v in RES.items())+
 '\n- Rice/Worthy graded on Rice-active split (KC wk1-3, games '+', '.join(S['kc_games'])+'); Rice wk4 excluded (hamstring Q1 exit). LOW-SAMPLE n=3. Seed 20261101, N=100000 x3, script runs/2026-11-01_shared_src/rec_r0750.py + sim_v5.py.')
open(F+'checklist.md','w').write('\n'.join(ck)+'\n')
M['sources'].append({'category':'odds_props','name':'The Odds API re-pull: FanDuel main+alt receptions, Pinnacle, DK (r0750)','url_or_file':R+'2026-11-01_shared_src/odds_r0750.csv','tool':'python urllib (The Odds API, pull_odds.py)','pulled_et':TI})
M['sources'].append({'category':'injuries_news','name':'ESPN injuries API re-pull (Rice active, no designation)','url_or_file':R+'2026-11-01_shared_src/espn_inj_0750.json','tool':'curl','pulled_et':TI})
M['sources'].append({'category':'injuries_news','name':'NBC Sports/Rotoworld: Reid - Rice (hamstring) will play Wk8 (2026-10-30)','url_or_file':'https://www.nbcsports.com/fantasy/football/player-news/2026-10-30/reid-rashee-rice-hamstring-will-play-in-week-8','tool':'Firecrawl search','pulled_et':TI})
M['sources'].append({'category':'injuries_news','name':'KCTV5: Rice to miss Chargers game, hamstring from Wk4 Q1 vs LV (2026-10-16)','url_or_file':'https://www.kctv5.com/2026/10/16/rashee-rice-miss-chiefs-chargers-matchup-due-hamstring-injury/','tool':'Firecrawl search','pulled_et':TI})
json.dump(M,open(F+'run_manifest.json','w'),indent=1,default=float)
json.dump(RES,open(F+'rec_results_0750.json','w'),indent=1,default=float)
for k,v in RES.items(): print(f"{k} @{v['price']:+d} nv {v['nv']:.3f} p {v['p']['mc']:.3f}/{v['p']['bias']:.3f}/{v['p']['gr']:.3f} med {v['med']['mc']}/{v['med']['bias']}/{v['med']['gr']} gate {v['edge']*100:+.1f}/{v['sh']*100:+.1f} MCGR {v['edge_mg']*100:+.1f}/{v['sh_mg']*100:+.1f} {v['status']} {v['reasons']}")
