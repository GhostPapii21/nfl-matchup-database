import json,sys
from extract import imp, fmt
g=sys.argv[1]; f=json.load(open(f'/workspace/runs/2026-11-22_W11_FOCUS9/_work/facts_{g}.json'))
print('#',g,'packet',f['packet_utc'],'lines',f['lines_utc'])
for b,d in f['game_lines'].items(): print(' ',b, {k:[(s[:12],l,a) for s,l,a in v] for k,v in d.items()})
for off,s in f['sides'].items():
    print(f'\n== {off} OFFENSE; QB(s):',[(q['player'],q['games'],q['attempts']) for q in s['qbs']], 'off depth',s['off_depth'])
    print(' off_prod',{k:(round(v,3) if isinstance(v,float) else v) for k,v in s['off_prod'].items()})
    for r in s['receivers'][:6]:
        print(f"  R {r['name']} {r['pos']} ts{r['tshare']} adot{r['adot'] and round(r['adot'],1)} snap{r['snap']} wk{r['weeks']} T{r['tlog']} Y{r['ylog']} {r['label']}")
    for r in s['rushers'][:4]:
        cs=[round(c/s['team_carries'].get(str(w),0),2) if s['team_carries'].get(str(w)) else None for c,w in zip(r['clog'],r['weeks'])]
        print(f"  RB {r['name']} {r['pos']} cs{r['cshare']} wk{r['weeks']} C{r['clog']} Y{r['ylog']} share/g{cs}")
    print(' DEF',[k for k in s['def_depth'].items()])
    print(' def_allowed',{k:(round(v,3) if isinstance(v,float) else v) for k,v in s['def_allowed'].items()})
    print(' def_rank',s['def_rank'])
    for d in s['defenders'][:9]: print('   D',d)
    print('  rush',[(p['player'],p.get('pressures'),p.get('sacks')) for p in s['pass_rush']])
    cp=s['cov_profile'] or {}
    print('  cov2025 man',cp.get('man_rate'),'shells',cp.get('shells'),'blitz5+',cp.get('five_plus_rushers_rate'))
    for k,v in s['visual_defs'].items(): print('   VIS',k,v[:3])
    w=s['watch'] or {}
    for e in (w.get('receivers') or [])[:5]+(w.get('rushers') or [])[:2]: print('   W',e['player'],e['p80'],e.get('stars'),e.get('book80'))
    for k,v in s['opp_rush'].items(): print('   OPP-RUSH',k,v.get('yards_median'),v.get('carries_mean'),v.get('status'))
print('\nPROPS')
for n,d in f['props'].items():
    s=[]
    for m in ('receiving_yards','receptions','rushing_yards','rush_rec_yards'):
        for b,v in d[m].items():
            if v: s.append(f"{m[:6]}:{b[:2]} {v['line']} {fmt(v['over'])}/{fmt(v['under'])}")
    print(' ',n,'|',' ; '.join(s))
