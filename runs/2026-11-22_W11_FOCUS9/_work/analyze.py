"""Candidate builder (research only; no sims). Uses facts_*.json. Status per Rico rules."""
import json, statistics as st, sys, math
from pathlib import Path
from extract import imp, fmt, short, norm
W = Path('/workspace/runs/2026-11-22_W11_FOCUS9/_work')
BOOKS = ['fanduel','draftkings','betmgm','caesars']
BK = {'fanduel':'FD','draftkings':'DK','betmgm':'MGM','caesars':'CZR'}
# Status from Friday official reports + Saturday web checks (see SUMMARY sources)
OUT = {'Kenneth Walker III','Carson Beck','Kyler Murray','Jordan Addison','Jared Wayne','Jake Ferguson','Jonathan Mingo','Caleb Lohner','Oren Burks','Dalton Risner'}
DOUBTFUL = {'Dalton Kincaid'}
QUEST = {'Brock Bowers','Darren Waller','Tommy Tremble','Mike Evans','Baker Mayfield','Jackson Hawes','Zavion Thomas','Sione Vaki','Jonathon Brooks','Jordan James','Rachaad White','Mac Jones'}
def p_at(log, rung, over=True):
    if not log: return None
    return sum(1 for y in log if (y > rung if over else y < rung)) / len(log)
def cushion_check(log, rung, price):
    l4 = log[-4:]
    if len(l4) < 3: return ('MISSING', 'under 3 recent games')
    med = st.median(l4)
    need = 0.20 if price is not None and price <= -150 else 0.25
    c = (med - rung) / rung if rung > 0 else 9
    clear10 = sum(1 for y in l4 if y >= rung * 1.10)
    ok = c >= need and (price is None or price <= -150 or clear10 >= 3)
    return ('PASS' if ok else 'FAIL', f'last-4 median {med:g} vs rung {rung:g} = {c*100:.0f}% cushion (need {need*100:.0f}%); cleared by 10%+ in {clear10} of {len(l4)}')
def best(lad):
    b = max(lad.items(), key=lambda kv: kv[1]) if lad else None
    return b
def devig_alt(price, mains, book):
    m = mains.get(book) or mains.get('fanduel') or next((v for v in mains.values() if v), None)
    if not m: return None, 'NO_VIG_UNAVAILABLE'
    return imp(price) / m['over_round'], f"alt de-vigged by {BK.get(book,book)} main {m['line']} overround {m['over_round']:.3f}"
def ladder_rows(lad, mains, log, sim):
    out = []
    for rung_s, bk in lad.items():
        rung = float(rung_s)
        if not bk: continue
        bb, bp = max(bk.items(), key=lambda kv: kv[1])
        fdp = bk.get('fanduel')
        fair, how = devig_alt(bp, mains, bb)
        simp = (sim or {}).get(str(int(rung + 0.5)))
        out.append({'rung': rung, 'books': {BK[k]: v for k, v in bk.items()}, 'best_book': BK[bb], 'best': bp, 'be_best': imp(bp), 'fd': fdp,
                    'nv_best': fair, 'nv_how': how, 'hit_all': p_at(log, rung), 'hit_l4': p_at(log[-4:], rung), 'n': len(log), 'board_sim': simp})
    return out
def pick_floor(rows, log):
    """Rico style alt floor: highest rung that cleared in >=7 of 8 (or all but one) and passes the cushion check."""
    good = []
    for r in rows:
        if r['hit_all'] is None or r['n'] < 4: continue
        if r['hit_all'] >= (r['n'] - 1) / r['n'] and r['hit_l4'] == 1.0 and 0.55 <= r['be_best'] <= 0.80:
            cc = cushion_check(log, r['rung'], r['best'])
            r = dict(r, cushion=cc)
            good.append(r)
    good = [g for g in good if g['cushion'][0] == 'PASS'] or good
    return max(good, key=lambda r: r['rung']) if good else None
def analyze(gid):
    f = json.load(open(W / f'facts_{gid}.json'))
    res = {'gid': gid, 'receiving': [], 'rushing': [], 'rush_unders': [], 'dnp': [], 'watch80': []}
    props = f['props']
    pmap = {short(n): n for n in props}
    for off, s in f['sides'].items():
        dfn = [t for t in f['sides'] if t != off][0]
        recs = [r for r in s['receivers'] if r['pos'] in ('WR', 'TE')]
        recs = sorted(recs, key=lambda r: -r['tshare'])[:3]
        rbrec = sorted([r for r in s['receivers'] if r['pos'] == 'RB'], key=lambda r: -r['tshare'])[:1]
        for rank, r in enumerate(recs + rbrec, 1):
            nm = pmap.get(short(r['name']))
            status = 'OUT' if r['name'] in OUT else 'DOUBTFUL' if r['name'] in DOUBTFUL else 'Q' if r['name'] in QUEST else ''
            item = {'team': off, 'opp': dfn, 'player': r['name'], 'pos': r['pos'], 'rank': rank if r['pos'] != 'RB' else 'RB', 'tshare': r['tshare'], 'tlog': r['tlog'], 'ylog': r['ylog'], 'rlog': r['rlog'], 'weeks': r['weeks'], 'status': status, 'prop_name': nm}
            if nm:
                d = props[nm]
                item['main_rec'] = {BK[b]: v for b, v in d['receiving_yards'].items() if v}
                item['main_recp'] = {BK[b]: v for b, v in d['receptions'].items() if v}
                sim = (s['opp_rec'].get(r['name']) or {}).get('yards')
                rows = ladder_rows(d['alt_receiving_yards'], d['receiving_yards'], r['ylog'], sim)
                item['ladder'] = rows
                item['floor'] = pick_floor(rows, r['ylog'])
            res['receiving'].append(item)
        team_car = s['team_carries']
        for r in s['rushers']:
            if r['pos'] != 'RB': continue
            shares = [c / team_car[str(w)] for c, w in zip(r['clog'], r['weeks']) if team_car.get(str(w))]
            l4 = shares[-4:]
            n60 = sum(1 for x in l4 if x >= 0.60)
            status = 'OUT' if r['name'] in OUT else 'Q' if r['name'] in QUEST else ''
            item = {'team': off, 'opp': dfn, 'player': r['name'], 'clog': r['clog'], 'ylog': r['ylog'], 'weeks': r['weeks'], 'shares': [round(x, 2) for x in shares], 'n60_l4': n60, 'status': status, 'gate60': 'PASS' if n60 >= 3 else 'FAIL'}
            nm = pmap.get(short(r['name']))
            if nm:
                d = props[nm]
                item['main_rush'] = {BK[b]: v for b, v in d['rushing_yards'].items() if v}
                sim = (s['opp_rush'].get(r['name']) or {}).get('yards')
                rows = ladder_rows(d['alt_rushing_yards'], d['rushing_yards'], r['ylog'], sim)
                item['ladder'] = rows
                item['floor'] = pick_floor(rows, r['ylog'])
            res['rushing'].append(item)
            if item['gate60'] == 'FAIL' or status == 'OUT':
                res['dnp'].append(f"{r['name']} ({off} RB) rushing: carry share {item['shares'][-4:]} last 4, {n60} of 4 at 60%+" + (' [OUT]' if status == 'OUT' else ''))
        # QB/RB rush unders: any player with a rushing_yards main line on this team
        names_team = {short(x['name']) for x in s['rushers']} | {short(q['player']) for q in s['qbs']}
        for nm, d in props.items():
            mr = {BK[b]: v for b, v in d['rushing_yards'].items() if v}
            if not mr: continue
            rr = next((x for x in s['rushers'] if short(x['name']) == short(nm)), None)
            qb = next((q for q in s['qbs'] if short(q['player']) == short(nm)), None)
            QBL0 = json.load(open(W/'qb_rush_logs.json'))
            if not rr and not qb and not (nm in QBL0 and QBL0[nm]['game']==gid and QBL0[nm]['log'][-1]['team']==off): continue
            QBL = json.load(open(W/'qb_rush_logs.json'))
            log = [x['yds'] for x in QBL[nm]['log']] if (not rr or rr['pos']=='QB') and nm in QBL else (rr['ylog'] if rr else None)
            if rr and rr['pos']=='QB' and nm not in QBL: log = None
            fdm = mr.get('FD') or next(iter(mr.values()))
            bu = max(mr.items(), key=lambda kv: kv[1]['under'])
            res['rush_unders'].append({'team': off, 'player': nm, 'pos': rr['pos'] if rr else 'QB', 'mains': mr, 'log': log, 'weeks': ([x['week'] for x in QBL[nm]['log']] if nm in QBL else (rr['weeks'] if rr else None)), 'qb_pbp': nm in QBL,
                                       'under_hits': (sum(1 for y in log if y < fdm['line']), len(log)) if log else None,
                                       'best_under': (bu[0], bu[1]['line'], bu[1]['under'], bu[1]['nv_under']), 'status': 'OUT' if nm in OUT else ''})
        # 80+ side list
        w = s.get('watch') or {}
        for e in (w.get('receivers') or []) + (w.get('rushers') or []):
            nm = pmap.get(short(e['player']))
            mk = 'alt_receiving_yards' if e in (w.get('receivers') or []) else 'alt_rushing_yards'
            bk = props[nm][mk].get('79.5', {}) if nm else {}
            if not bk: continue
            bb, bp = max(bk.items(), key=lambda kv: kv[1])
            be = imp(bp)
            lg = lambda p: math.log(p / (1 - p))
            blend = 1 / (1 + math.exp(-(0.5 * lg(e['p80']) + 0.5 * lg(be))))
            res['watch80'].append({'team': off, 'player': e['player'], 'p80_model': e['p80'], 'books': {BK[k]: v for k, v in bk.items()}, 'best': (BK[bb], bp), 'be_best': be,
                                   'blend': blend, 'edge_vs_best': blend - be, 'outliers': [BK[k] for k, v in bk.items() if abs(imp(v) - be) >= 0.05],
                                   'status': 'OUT' if e['player'] in OUT else 'Q' if e['player'] in QUEST else 'DOUBTFUL' if e['player'] in DOUBTFUL else ''})
    (W / f'cand_{gid}.json').write_text(json.dumps(res, indent=1, default=str))
    return res
def brief(res):
    L = [f"### {res['gid']}"]
    for it in res['receiving']:
        fl = it.get('floor')
        mr = it.get('main_rec', {})
        fdm = mr.get('FD')
        L.append(f"REC {it['team']} {it['player']} {it['pos']}#{it['rank']} ts{it['tshare']} {it['status']} wk{it['weeks']} Y{it['ylog']} T{it['tlog']} | main FD {fdm and (fdm['line'], fdm['over'], fdm['under'])} | floor " +
                 (f"{fl['rung']} best {fl['best_book']} {fmt(fl['best'])} (BE {fl['be_best']:.2f}, nv {fl['nv_best'] and round(fl['nv_best'],3)}) FD {fmt(fl['fd'])} hit {fl['hit_all']:.2f}/{fl['n']} l4 {fl['hit_l4']:.2f} sim {fl['board_sim']} {fl['cushion']}" if fl else 'none'))
    for it in res['rushing']:
        fl = it.get('floor'); mr = it.get('main_rush', {}); fdm = mr.get('FD') or (next(iter(mr.values())) if mr else None)
        L.append(f"RUSH {it['team']} {it['player']} {it['status']} share{it['shares']} gate{it['gate60']} C{it['clog']} Y{it['ylog']} | main {fdm and (fdm['line'], fdm['over'], fdm['under'])} | floor " +
                 (f"{fl['rung']} {fl['best_book']} {fmt(fl['best'])} BE {fl['be_best']:.2f} hit {fl['hit_all']:.2f}/{fl['n']} sim {fl['board_sim']} {fl['cushion']}" if fl else 'none'))
    for it in res['rush_unders']:
        L.append(f"RU {it['team']} {it['player']} {it['pos']} {it['status']} mains {[(k, v['line'], v['over'], v['under']) for k, v in it['mains'].items()]} log {it['log']} under_hits {it['under_hits']} best_under {it['best_under'][:3]} nv {it['best_under'][3]:.3f}")
    for it in sorted(res['watch80'], key=lambda x: -x['edge_vs_best']):
        L.append(f"W80 {it['team']} {it['player']} {it['status']} model {it['p80_model']} books {it['books']} best {it['best']} BE {it['be_best']:.3f} blend {it['blend']:.3f} edge {it['edge_vs_best']*100:+.1f} outliers {it['outliers']}")
    L.append('DNP: ' + '; '.join(res['dnp']))
    return '\n'.join(L)
if __name__ == '__main__':
    for g in ['ARI_KC','BAL_CAR','MIA_BUF','NO_CHI','TB_DET','JAX_NYG','LV_DEN','MIN_SF','CIN_WAS']:
        r = analyze(g)
        (W / f'brief_{g}.txt').write_text(brief(r))
    print('ok')
