import json
from extract import norm
W='/workspace/runs/2026-11-22_W11_FOCUS9/_work/'
DSTAT={'Marlon Humphrey':'OUT','Jaylinn Hawkins':'OUT','Nnamdi Madubuike':'OUT','Bobby Okereke':'OUT','Isaiah Simmons':'OUT','Mike Jackson':'Q','Jaylin Simpson':'DOUBTFUL','Dante Trader Jr.':'DOUBTFUL','Marcellas Dial Jr.':'Q','Christian Benford':'OUT','Dorian Williams':'OUT','Damar Hamlin':'Q','Ed Oliver':'Q (added Sat)','Martin Emerson Jr.':'OUT','Martin Emerson':'OUT','Justin Reid':'OUT (waived)','Decamerion Richardson':'Q','Pete Werner':'Q','Kyler Gordon':'OUT','Antoine Winfield Jr.':'OUT','Antoine Winfield':'OUT','Josh Hayes':'OUT','YaYa Diaby':'Q','D.J. Reed':'Q','DJ Reed':'Q','Ennis Rakestraw Jr.':'Q','Ennis Rakestraw':'Q','Khalil Dorsey':'Q','Joe Bachie':'Q','Tonka Hemingway':'OUT','Brandon Jones':'Q','Isaiah Rodgers':'Q','Jay Ward':'Q','Dre Greenlaw':'Q','Upton Stout':'Q','Nate Hobbs':'Q (IR)','Kyle Dugger':'Q','Oren Burks':'OUT (IR Sat)','Dax Hill':'DNP Thu/Fri; coach: expected to play','Quan Martin':'Q (secondary source)','B.J. Green II':'OUT'}
def st(n): return DSTAT.get(n) or next((v for k,v in DSTAT.items() if norm(k)==norm(n)),'')
def dline(defs,name):
    d=next((x for x in defs if norm(x['name'])==norm(name)),None)
    s=st(name)
    if not d: return f"{name} (PFR coverage line not in packet){' ['+s+']' if s else ''}"
    cp=f"{d['cmp_pct']*100:.0f}%" if d.get('cmp_pct') is not None else 'n/a'
    return f"{name} {d['pos']}: {d['tgt']} tgt, {d['cmp']} cmp ({cp}), {d['yds']} yds, {d['ypt']} YPT, {d['td']} TD, {d['int']} INT{' ['+s+']' if s else ''}"
def build(gid):
    f=json.load(open(W+f'facts_{gid}.json'))
    out={}
    for off,s in f['sides'].items():
        dfn=[t for t in f['sides'] if t!=off][0]
        ds=f['sides'][off]['def_depth']; defs=s['defenders']
        rows=[]
        recs=[r for r in s['receivers'] if r['pos'] in ('WR','TE')][:3]
        for r in recs:
            if r['pos']=='WR':
                cands=[ds.get('LCB'),ds.get('RCB'),ds.get('NB')]
                cands=[c for c in cands if c]
                why='WR: depth-chart LCB/RCB/NB (side and alignment not charted publicly; ESTIMATE)'
            else:
                cands=[x[0] for x in s['visual_defs'].get(r['name'],[])][:3] or [ds.get(k) for k in ('SS','FS','WLB','MLB') if ds.get(k)]
                why='TE: defenders who see the most targets at the position (board), ESTIMATE'
            rows.append({'player':r['name'],'pos':r['pos'],'tshare':r['tshare'],'why':why,'defs':[dline(defs,c) for c in cands]})
        # defenders listed but not in depth (worth noting)
        cp=s['cov_profile'] or {}
        out[off]={'opp':dfn,'rows':rows,'def_depth':ds,'top_defs':[dline(defs,d['name']) for d in defs[:8]],
                  'cov':f"2025 (last free season, STALE as current fact): man {cp.get('man_rate',0)*100:.0f}% / zone {cp.get('zone_rate',0)*100:.0f}%, shells {', '.join(x['shell']+' '+str(round(x['rate']*100))+'%' for x in (cp.get('shells') or [])[:4])}; 5+ rushers {round((cp.get('five_plus_rushers_rate') or 0)*100)}%" if cp else 'MISSING',
                  'rush':[(p['player'],p.get('pressures'),p.get('sacks')) for p in s['pass_rush'][:4]]}
    json.dump(out,open(W+f'match_{gid}.json','w'),indent=1)
    return out
if __name__=='__main__':
    import sys
    for g in ['ARI_KC','BAL_CAR','MIA_BUF','NO_CHI','TB_DET','JAX_NYG','LV_DEN','MIN_SF','CIN_WAS']:
        o=build(g)
        print('###',g)
        for off,v in o.items():
            print(off,'vs',v['opp'],'|',v['cov'],'| rush',v['rush'])
            for r in v['rows']:
                print('  ',r['player'],r['pos'],r['tshare'],'->',' || '.join(r['defs']))
