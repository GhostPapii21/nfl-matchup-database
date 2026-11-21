"""Extract per-game facts for the Week 11 focus-9 research run. Reads repo packets, board data and Nov 20 grok lines.
No new pulls. Research only."""
import json, re, statistics as st, sys
from pathlib import Path
R = Path('/tmp/wt-focus9')
GAMES = ['ARI_KC','BAL_CAR','MIA_BUF','NO_CHI','TB_DET','JAX_NYG','LV_DEN','MIN_SF','CIN_WAS']
BOOKS = ['fanduel','draftkings','betmgm','caesars']
def imp(a):
    return abs(a)/(abs(a)+100) if a < 0 else 100/(a+100)
def norm(n):
    n = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", "", (n or '').lower()); return re.sub(r"[^a-z]", "", n)
def short(n):  # 'Travis Kelce' -> 'tkelce'
    parts = (n or '').replace('.', ' ').split()
    parts = [p for p in parts if p.lower().strip('.') not in ('jr','sr','ii','iii','iv')]
    return norm(parts[0][0] + parts[-1]) if parts else ''
def fmt(a):
    return 'n/a' if a is None else (f'+{int(a)}' if a > 0 else f'{int(a)}')

def lines_for(gid):
    g = json.load(open(R/f'pregame/grok_lines/2026_11_{gid}.json'))
    return g

def player_rows(rows, name):
    s = short(name); out = []
    for r in rows:
        if r['market'] in ('moneyline','spread','total'): continue
        if short(r['player']) == s or norm(r['player']) == norm(name): out.append(r)
    return out

def main_two_way(rows, market, book):
    """main line two-way (over/under at same line) for a book"""
    ov = [r for r in rows if r['market']==market and r['book']==book and r['side'].lower()=='over']
    un = [r for r in rows if r['market']==market and r['book']==book and r['side'].lower()=='under']
    for o in ov:
        for u in un:
            if u['line']==o['line']:
                io, iu = imp(o['american']), imp(u['american'])
                return {'line':o['line'],'over':o['american'],'under':u['american'],'nv_over':io/(io+iu),'nv_under':iu/(io+iu),'over_round':io+iu}
    return None

def facts(gid):
    pk = json.load(open(R/f'pregame/packets/2026_11_{gid}/packet.json'))
    bd = json.load(open(R/f'dashboard/data/2026_11_{gid}.json'))
    gl = lines_for(gid); rows = gl['rows']
    away, home = pk['game']['away'], pk['game']['home']
    out = {'gid':gid,'away':away,'home':home,'game':pk['game'],'packet_utc':pk['generated_utc'],'lines_utc':gl['retrieved_utc'],
           'books_utc':{b:v.get('retrieved_utc') for b,v in gl['books'].items()},'missing':gl.get('missing',[]),
           'weather_packet':pk.get('weather',{}).get('at_kickoff'),'implied_board':bd.get('implied_points')}
    gm = {}
    for b in BOOKS:
        d = {}
        for r in rows:
            if r['book']!=b or r['market'] not in ('moneyline','spread','total'): continue
            d.setdefault(r['market'],[]).append((r['side'],r['line'],r['american']))
        gm[b] = d
    out['game_lines'] = gm
    sides = {}
    for off, dfn in ((away,home),(home,away)):
        sd = bd['sides'][f'{off}_vs_{dfn}']
        tdef = pk['teams'][dfn]; toff = pk['teams'][off]
        s = {}
        s['qbs'] = toff['offense']['players']['quarterbacks']
        s['qb_card'] = sd.get('qb')
        rec = []
        for r in sd['roles']['receivers'][:7]:
            log = r.get('log',[])
            rec.append({'name':r.get('full_name') or r['player'],'pos':r['pos'],'g':r['games'],'tgt':r['targets'],'rec':r['receptions'],'yds':r['yards'],
                        'tshare':round(r['target_share'],3),'adot':r.get('avg_depth_of_target'),'ypt':r.get('yards_per_target'),'snap':r.get('snap_share'),
                        'tpg':r.get('targets_pg'),'t_l3':r.get('targets_last3_pg'),'catch':r.get('catch_rate'),'ylog':[x['yards'] for x in log],
                        'tlog':[x['targets'] for x in log],'rlog':[x['receptions'] for x in log],'weeks':[x['week'] for x in log],
                        'label':(r.get('opportunity') or {}).get('label'),'tags':[t['tag'] for t in r.get('tags',[])]})
        s['receivers'] = rec
        rush = []
        for r in sd['roles']['rushers'][:6]:
            log = r.get('log',[])
            rush.append({'name':r.get('full_name') or r['player'],'pos':r['pos'],'g':r['games'],'car':r['carries'],'yds':r['yards'],'cshare':round(r.get('carry_share') or 0,3),
                         'ypc':r.get('yards_per_carry'),'clog':[x['carries'] for x in log],'ylog':[x['yards'] for x in log],'weeks':[x['week'] for x in log],
                         'tags':[t['tag'] for t in r.get('tags',[])]})
        s['rushers'] = rush
        # carry share per game from offense_by_game carries
        s['team_carries'] = {g['week']:g['carries'] for g in sd['offense_by_game']}
        s['team_tgts'] = {g['week']:(g['wr_targets'] or 0)+(g['te_targets'] or 0)+(g['rb_targets'] or 0) for g in sd['offense_by_game']}
        s['def_allowed'] = {k:sd['defense_allowed'].get(k) for k in ('points_pg','pass_yards_pg','yards_per_pass_attempt','completion_rate','rush_yards_pg','rb_yards_per_carry','rb_rush_yards_pg','qb_rush_yards_pg','scrambles_pg','sack_rate','pressure_rate','explosive_pass_pg','explosive_rush_pg','third_down_rate','red_zone_td_rate','wr_rec_yards_pg','te_rec_yards_pg','rb_rec_yards_pg')}
        s['def_rank'] = {k:v.get('rank') for k,v in sd['defense_rank'].items()}
        s['off_prod'] = {k:sd['offense_produced'].get(k) for k in ('points_pg','plays_pg','pass_att_pg','rush_att_pg','rb_carries_pg','qb_rush_yards_pg','scrambles_pg','sack_rate','pressure_rate','neutral_pass_rate','red_zone_td_rate')}
        s['off_rank'] = {k:v.get('rank') for k,v in sd['offense_rank'].items()}
        s['def_by_game'] = sd['defense_by_game']; s['off_by_game']=sd['offense_by_game']
        cov = sd['defenders']['coverage']
        s['defenders'] = [{'name':c['player'],'pos':c.get('position'),'g':c['games'],'tgt':c['targets'],'cmp':c['completions'],'cmp_pct':c.get('completion_pct'),'yds':c['yards'],'ypt':round(c['yards_per_target'],1) if c.get('yards_per_target') is not None else None,'td':c['td_allowed'],'int':c['interceptions'],'grade':c.get('grade')} for c in cov]
        s['pass_rush'] = sd['defenders']['pass_rush'][:5]
        s['cov_profile'] = sd.get('coverage_profile')
        s['def_depth'] = {x['slot']:x['player'] for x in tdef['depth_chart']['starters'] if x['slot'] in ('LCB','RCB','NB','SS','FS','WLB','MLB','SLB','LILB','RILB','LOLB','ROLB','LDE','RDE','LDT','RDT','NT')}
        s['off_depth'] = {x['slot']:x['player'] for x in toff['depth_chart']['starters'] if x['slot'] in ('QB','RB','WR','TE','LT','LG','C','RG','RT')}
        s['opp'] = {'team_pass_attempts':sd['opportunity'].get('team_pass_attempts'),'team_rush_attempts':sd['opportunity'].get('team_rush_attempts'),'implied_margin':sd['opportunity'].get('implied_margin')}
        s['opp_rec'] = {o['player']:{'yards_median':o.get('yards_median'),'yards':o.get('yards'),'receptions':o.get('receptions'),'targets_mean':o.get('targets_mean'),'status':o.get('status')} for o in sd['opportunity'].get('receivers',[])}
        s['opp_rush'] = {o['player']:{'yards_median':o.get('yards_median'),'yards':o.get('yards'),'carries_mean':o.get('carries_mean'),'status':o.get('status')} for o in sd['opportunity'].get('rushers',[])}
        s['watch'] = sd.get('watch')
        s['visual_defs'] = {}
        for pid, v in (sd.get('visual') or {}).get('receivers',{}).items():
            sz = v.get('size') or {}
            if sz.get('player'):
                s['visual_defs'][sz['player']['name']] = [(d['player'],d['position'],d['targets'],d['yards_per_target'],d['grade']) for d in sz.get('defenders',[])]
        sides[off] = s
    out['sides'] = sides
    # props per player for listed receivers/rushers + QBs
    props = {}
    names = set()
    for off in sides:
        for r in sides[off]['receivers'][:5]: names.add(r['name'])
        for r in sides[off]['rushers'][:4]: names.add(r['name'])
    allp = sorted(set(r['player'] for r in rows if r['market'] not in ('moneyline','spread','total')))
    out['all_prop_players'] = allp
    for n in allp:
        pr = [r for r in rows if r['player']==n]
        d = {}
        for m in ('receiving_yards','receptions','rushing_yards','rush_rec_yards'):
            d[m] = {b:main_two_way(pr,m,b) for b in BOOKS}
        for m in ('alt_receiving_yards','alt_rushing_yards','alt_rush_rec_yards'):
            lad = {}
            for r in pr:
                if r['market']==m and r['side'].lower()=='over':
                    lad.setdefault(r['line'],{})[r['book']] = r['american']
            d[m] = {str(k):v for k,v in sorted(lad.items())}
        props[n] = d
    out['props'] = props
    return out

if __name__=='__main__':
    od = Path('/workspace/runs/2026-11-22_W11_FOCUS9/_work')
    for g in GAMES:
        f = facts(g)
        (od/f'facts_{g}.json').write_text(json.dumps(f, indent=1, default=str))
        print(g, len(f['props']), f['packet_utc'], f['lines_utc'])
