"""Season-level public team coverage rates: StatRankings CoverageIQ (primary) and Sharp Football Analysis (cross-check), side by side.
Never mixed or averaged. refs NFL-56, NFL-49."""
import csv, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f'{OUT}/sources/team_coverage_rates.csv'
NAME2AB = {'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN',
           'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB', 'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND',
           'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC', 'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LAR', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN',
           'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG', 'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
           'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WSH'}
CORE = [('man_pct', 'Man'), ('zone_pct', 'Zone'), ('mofc_pct', 'MOF closed (single-high)'), ('mofo_pct', 'MOF open (two-high)'), ('blitz_pct', 'Blitz')]
SHELL = [('cover0_pct', 'Cover 0'), ('cover1_pct', 'Cover 1'), ('cover2_pct', 'Cover 2'), ('cover2m_pct', 'Cover 2-Man'), ('cover3_pct', 'Cover 3'), ('cover4_pct', 'Cover 4'), ('cover6_pct', 'Cover 6'), ('cover9_pct', 'Cover 9')]
FLAG_PP = 7.0
SR_TAG = 'StatRankings CoverageIQ, thru games of 2026-11-20 (pages updated 2026-11-21 7:32 PM AST), pulled 2026-11-22 5:03 PM AST'
SH_TAG = 'Sharp Football Analysis, thru Week 10 (updated 2026-11-17), pulled 2026-11-22 5:04 PM AST'
def load():
    d = {}
    for r in csv.DictReader(open(SRC)):
        ab = NAME2AB.get(r['team']);
        if not ab: raise SystemExit('unmapped team ' + r['team'])
        k = 'SR' if 'statrankings' in r['source_url'] else 'SH' if 'sharpfootball' in r['source_url'] else None
        d.setdefault(ab, {})[k] = r
    return d
def v(r, k):
    x = (r or {}).get(k, '')
    return f'{x}%' if x not in ('', None) else 'unknown'
import statistics as _st
_STATS = {}
def stats(d):
    if _STATS: return _STATS
    for k, lab in CORE:
        ok = [a for a in d if d[a].get('SR', {}).get(k) and d[a].get('SH', {}).get(k)]
        gaps = {a: float(d[a]['SR'][k]) - float(d[a]['SH'][k]) for a in ok}
        rsr = {a: i + 1 for i, a in enumerate(sorted(ok, key=lambda a: -float(d[a]['SR'][k])))}
        rsh = {a: i + 1 for i, a in enumerate(sorted(ok, key=lambda a: -float(d[a]['SH'][k])))}
        _STATS[k] = {'median': _st.median(gaps.values()), 'sd': _st.pstdev(gaps.values()), 'n_sr_higher': sum(g > 0 for g in gaps.values()), 'n': len(gaps), 'gaps': gaps, 'rsr': rsr, 'rsh': rsh}
    return _STATS
def outliers(ab, d):
    out = []
    for k, lab in CORE:
        S = stats(d)[k]
        if ab not in S['gaps']: continue
        g = S['gaps'][ab]; rel = g - S['median']; rg = S['rsr'][ab] - S['rsh'][ab]
        if abs(rel) >= 2 * S['sd'] or abs(rg) >= 10: out.append((lab, round(g, 1), round(rel, 1), S['rsr'][ab], S['rsh'][ab]))
    return out
def flags(ab, d):
    out = []
    sr, sh = d.get(ab, {}).get('SR'), d.get(ab, {}).get('SH')
    for k, lab in CORE:
        try: a, b = float(sr[k]), float(sh[k])
        except Exception: continue
        if abs(a - b) >= FLAG_PP: out.append((lab, a, b, round(a - b, 1)))
    return out
def block(ab, d, hlevel='###'):
    sr, sh = d.get(ab, {}).get('SR'), d.get(ab, {}).get('SH')
    L = [f'{hlevel} {ab} season coverage rates (public, season-level; NOT game-level)', '',
         '| Rate | StatRankings CoverageIQ (primary) | Sharp Football Analysis (cross-check) |', '|---|---|---|']
    for k, lab in CORE: L.append(f'| {lab} | {v(sr, k)} | {v(sh, k)} |')
    for k, lab in SHELL: L.append(f'| {lab} | {v(sr, k)} | {v(sh, k) if (sh or {}).get(k) else "not published"} |')
    L.append(f"| Coverage snaps | {(sr or {}).get('coverage_snaps') or 'unknown'} | {(sh or {}).get('coverage_snaps') or 'not published'} |")
    L += ['', f'Sources: StatRankings = {SR_TAG} ({(sr or {}).get("source_url","")}). Sharp = {SH_TAG} ({(sh or {}).get("source_url","")}; blitz from the Sharp defensive-tendencies page, same update day).',
          'The two sources use different charting definitions: never mix or average them. StatRankings shell rates (Cover 0-9) are filled only where the public ranking articles list the team (top 25); blank = unknown, not zero. Week 11 Sunday games are in neither source.']
    f = flags(ab, d)
    L.append('**Source disagreement (7+ pts):** ' + ('; '.join(f'{lab}: StatRankings {a}% vs Sharp {b}% ({dd:+} pts)' for lab, a, b, dd in f) if f else 'none at 7+ pts'))
    o = outliers(ab, d)
    L.append('**Outlier vs the usual source gap** (gap 2+ SD away from the league-median gap, or ranks 10+ apart): ' + ('; '.join(f'{lab}: gap {g:+} pts is {rel:+} vs the median gap; rank {a} StatRankings vs {b} Sharp' for lab, g, rel, a, b in o) if o else 'none'))
    L.append('Game-level shells/coverage for Week 11: unknown unless video names them (see VIDEO_EVIDENCE.md).')
    return '\n'.join(L)
def offsets_md(d):
    S = stats(d); L = ['| Rate | Median gap (StatRankings - Sharp) | SD of gap | Teams where StatRankings is higher |', '|---|---|---|---|']
    for k, lab in CORE: L.append(f"| {lab} | {S[k]['median']:+.1f} pts | {S[k]['sd']:.1f} | {S[k]['n_sr_higher']}/{S[k]['n']} |")
    return '\n'.join(L)
def all_outliers(d):
    return [(ab, *x) for ab in sorted(d) for x in outliers(ab, d)]
def all_flags(d):
    return sorted(((ab, *x) for ab in d for x in flags(ab, d)), key=lambda t: -abs(t[4]))
if __name__ == '__main__':
    d = load(); print(len(d), 'teams')
    print(offsets_md(d))
    for t in all_outliers(d): print(t)
