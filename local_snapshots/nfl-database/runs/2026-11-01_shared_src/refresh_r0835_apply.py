"""08:25 routine: re-price at 08:36 ET pull (odds_r0835.csv) + re-score on sim_v6, update manifests/checklists, keep v5 alongside."""
import json,shutil,os,math,pandas as pd
R='/workspace/nfl-database/runs/'; S=R+'2026-11-01_shared_src/'
V6=json.load(open(S+'rescore_v6_r0835.json')); OD=pd.read_csv(S+'odds_r0835.csv')
TI='2026-11-01T08:36'; T='2026-11-01 08:36'
MK={'recyds':('player_reception_yds','player_reception_yds_alternate'),'rec':('player_receptions','player_receptions_alternate'),'comp':('player_pass_completions',None)}
def imp(a): return 100/(a+100) if a>0 else -a/(-a+100)
def price(book,pl,mkt,pt,side):
    q=OD[(OD.book==book)&(OD.player==pl)&(OD.market==mkt)&(OD.point==pt)&(OD.side==side.capitalize())]
    return int(q.price.iloc[0]) if len(q) else None
def main_pair(book,pl,mkey):
    q=OD[(OD.book==book)&(OD.player==pl)&(OD.market==mkey)]
    if not len(q): return None
    pt=q.point.iloc[0]; return pt,price(book,pl,mkey,pt,'over'),price(book,pl,mkey,pt,'under')
def mkt_of(name):
    return 'recyds' if 'Rec Yds' in name else 'rec' if 'Receptions' in name else 'comp' if 'Completions' in name else None
FOLD=['ATL@TB','KC@DEN','LAC@LAR','LV@NYJ','MIN@DET','PHI@WSH','DFS_SLIPS','FD7_REPLACEMENTS']
OUT={}
for f in FOLD:
    d=R+'2026-11-01_'+f+'/'
    for fn in ('checklist.md','report.md','run_manifest.json','gate_output.txt'):
        b=d+fn.replace('.','.pre0825.',1)
        if not os.path.exists(b): shutil.copy(d+fn,b)
    m=json.load(open(d+'run_manifest.json')); old={s['model']:s for s in m['sims']}
    m['sims_v5']=m['sims']; new={mo:dict(model=mo,n=100000,seed=20261101,engine='/workspace/nfl-database/tools/sim_v6.py',calib='/workspace/nfl-database/tools/sim_v6_calib.json',run_et=TI,legs={}) for mo in ('monte_carlo','bias','game_randomness')}
    for l in m['legs']:
        n=l['name']; mk=mkt_of(n); pl=l.get('player') or ('Matthew Stafford' if 'Stafford' in n else None)
        key=f'{pl}|{mk}'
        if key not in V6: continue
        if l.get('status')=='CUT' and f!='FD7_REPLACEMENTS': continue
        line=float(l['line']); side=l['side']; sims=V6[key]['sims']; rk=str(line)
        pm={mo:(sims[k]['rungs'][rk] if side=='over' else 1-sims[k]['rungs'][rk]) for mo,k in (('monte_carlo','mc'),('bias','bias'),('game_randomness','gr'))}
        md={mo:sims[k]['median'] for mo,k in (('monte_carlo','mc'),('bias','bias'),('game_randomness','gr'))}
        mainm,altm=MK[mk]
        # price of record
        fdm=main_pair('fanduel',pl,mainm); pin=main_pair('pinnacle',pl,mainm)
        if mk=='comp':
            pt,o,u=pin; ov=imp(o)+imp(u); nv=(imp(o) if side=='over' else imp(u))/ov; pr=o if side=='over' else u; src='Pinnacle no-vig (no FD line)'; onl=(pt==line)
        else:
            pt,o,u=fdm; ov=imp(o)+imp(u)
            if pt==line: pr=o if side=='over' else u; nv=imp(pr)/ov; src='FD main'
            else: pr=price('fanduel',pl,altm,line,'over'); nv=imp(pr)/ov; src=f'FD alt (de-vigged vs main {pt} two-way)'
            onl=True
        v5={mo:old[mo]['legs'].get(n) for mo in old}
        v5p=[v5[mo]['p'] for mo in ('monte_carlo','bias','game_randomness')] if all(v5.values()) else None
        rec=dict(folder=f,leg=n,status_before=l['status'],old_price=l.get('price_fd'),old_nv=l.get('no_vig'),new_price=pr,new_nv=nv,price_src=src,on_line=onl,
                 pin=pin,fd_main=fdm,v6_p=pm,v6_med=md,split=V6[key]['split'])
        if v5p:
            a5=sum(v5p)/3; rec.update(v5_p=v5p,v5_med=[v5[mo]['median'] for mo in ('monte_carlo','bias','game_randomness')],
              v5_gate=a5-l['no_vig'],v5_shr=0.5+0.7*(a5-0.5)-l['no_vig'],v5_mcgr=(v5p[0]+v5p[2])/2-l['no_vig'])
        a=sum(pm.values())/3; rec.update(v6_gate=a-nv,v6_shr=0.5+0.7*(a-0.5)-nv,v6_mcgr=(pm['monte_carlo']+pm['game_randomness'])/2-nv,
            v6_ok=(a-nv>=0.03 and 0.5+0.7*(a-0.5)-nv>0 and min(pm.values())>=0.45 and all((x>line) if side=='over' else (x<line) for x in md.values())))
        OUT[f+'::'+n]=rec
        for mo in new: new[mo]['legs'][n]=dict(p=round(pm[mo],5),median=md[mo])
        l['price_fd']=pr if mk!='comp' else l.get('price_fd'); l['no_vig']=round(nv,4)
        if pin: l['pinnacle']=dict(point=pin[0],over=pin[1],under=pin[2],nv_over=imp(pin[1])/(imp(pin[1])+imp(pin[2])),nv_under=imp(pin[2])/(imp(pin[1])+imp(pin[2])),pulled_et=TI)
        l['reprice_0836']=dict(price=pr,no_vig=round(nv,4),src=src,v6_avg_p=round(a,4),v6_edge=round(a-nv,4),v6_shrunk=round(0.5+0.7*(a-0.5)-nv,4),file=S+'odds_r0835.csv',pulled_et=TI)
        if l['status']=='PASS' and not rec['v6_ok']: l['status']='CUT'; l.setdefault('cut_reasons',[]).append('08:36 v6 re-score fails edge rule')
    m['sims']=list(new.values()); m['sim_script']='/workspace/nfl-database/tools/sim_v6.py (08:36 re-score; v5 kept in sims_v5)'
    m['edge_decision']='08:36: gate rule on avg of all 3 models (sim_v6 calibrated bias model, BUG-2026-11-01-BIAS fixed); v5 MC+GR numbers kept for comparison'
    keep=[]; sup=m.setdefault('superseded_sources',[])
    for s in m['sources']:
        if s['category']=='odds_props':
            if 'pff_props' in s['url_or_file']: m.setdefault('cross_checks',[]).append(dict(s,note='PFF pick-side cross-check only, not a price of record; captured 07:40 ET and now >1h old, so moved out of sources at 08:36 rather than re-stamped'))
            else: sup.append(dict(s,superseded_by=S+'odds_r0835.csv',superseded_et=TI))
        else: keep.append(s)
    keep+= [dict(category='odds_props',name='The Odds API re-pull 08:36: FanDuel main+alt, DraftKings, Pinnacle player props (12 events)',url_or_file=S+'odds_r0835.csv',pulled_et=TI,tool='The Odds API via pull_odds.py (urllib)'),
            dict(category='odds_props',name='The Odds API re-pull 08:36: FanDuel/DK/Pinnacle spreads+totals (28 games)',url_or_file=S+'lines_r0835.json',pulled_et=TI,tool='The Odds API via pull_lines.py (urllib)')]
    m['sources']=keep
    json.dump(m,open(d+'run_manifest.json','w'),indent=1,default=float)
    # checklist phase 14 rows
    ck=open(d+'checklist.md').read().splitlines()
    for i,r in enumerate(ck):
        c=[x.strip() for x in r.strip().strip('|').split('|')]
        if len(c)>=6 and c[1].startswith('14') and (f+'::'+c[0]) in OUT:
            o=OUT[f+'::'+c[0]]; c[3]+=(f"; REPRICED 08:36 {o['price_src']} {o['new_price']:+d} nv {o['new_nv']:.3f}; sim_v6 p {o['v6_p']['monte_carlo']:.3f}/{o['v6_p']['bias']:.3f}/{o['v6_p']['game_randomness']:.3f} "
                  f"edge {o['v6_gate']*100:+.1f} shrunk {o['v6_shr']*100:+.1f} medians {o['v6_med']['monte_carlo']}/{o['v6_med']['bias']}/{o['v6_med']['game_randomness']}")
            if o['status_before']=='PASS' and not o['v6_ok']: c[2]='FAIL'
            c[4]+=' + odds_r0835.csv (The Odds API) + tools/sim_v6.py seed 20261101 N=100000 x3'; c[5]=T; ck[i]='| '+' | '.join(c)+' |'
    open(d+'checklist.md','w').write('\n'.join(ck)+'\n')
json.dump(OUT,open(S+'refresh_r0835_results.json','w'),indent=1,default=float)
for k,o in OUT.items():
    v5=f"v5 gate {o['v5_gate']*100:+.1f}/{o['v5_shr']*100:+.1f} MCGR {o['v5_mcgr']*100:+.1f}" if 'v5_gate' in o else 'v5 n/a'
    print(k,'|',o['old_price'],'->',o['new_price'],f"nv {o['old_nv']}->{o['new_nv']:.4f}",'|',v5,f"| v6 gate {o['v6_gate']*100:+.1f}/{o['v6_shr']*100:+.1f} MCGR {o['v6_mcgr']*100:+.1f}",'OK' if o['v6_ok'] else 'FAILS',o['status_before'])
