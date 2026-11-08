#!/usr/bin/env python3
"""Collect Bengals-Falcons live play-by-play, box score, quarter scores and optional odds."""
from __future__ import annotations
import csv, datetime as dt, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/week9_930/live'
EVENT_ID = '401873038'
GAME_DATE = '2026-11-08'
ET = ZoneInfo('America/New_York')
BASE = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary'


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {'User-Agent':'week9-live-tracker/1.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def num(x):
    try:
        value=float(x)
        return int(value) if value.is_integer() else value
    except (TypeError, ValueError): return None


def player_rows(boxscore):
    out=[]
    for side in boxscore.get('players',[]):
        team=side.get('team',{}).get('abbreviation','')
        for category in side.get('statistics',[]):
            cat=category.get('name','')
            if cat not in ('passing','rushing','receiving'):
                continue
            labels=category.get('labels',[])
            for athlete in category.get('athletes',[]):
                vals=athlete.get('stats',[])
                stats={labels[i]: vals[i] for i in range(min(len(labels),len(vals)))}
                out.append({'team':team,'name':athlete.get('athlete',{}).get('displayName',''),
                            'category':cat,'stats':stats})
    return out


def add_projected_zeros(rows, locked_lines):
    """Keep every player on the locked prop board visible before first production."""
    seen={(r['name'],r['team'],r['category']) for r in rows}
    cats={'player_pass_yds':'passing','player_pass_tds':'passing',
          'player_rush_yds':'rushing','player_rush_attempts':'rushing',
          'player_reception_yds':'receiving','player_receptions':'receiving'}
    defaults={'passing':{'C/ATT':'0/0','YDS':'0','TD':'0','INT':'0'},
              'rushing':{'CAR':'0','YDS':'0','TD':'0'},
              'receiving':{'REC':'0','YDS':'0','TD':'0','TGTS':'0'}}
    for line in locked_lines:
        name=line.get('player',''); team=line.get('team',''); cat=cats.get(line.get('market_key',''))
        if name and cat and (name,team,cat) not in seen:
            rows.append({'team':team,'name':name,'category':cat,'stats':defaults[cat].copy()})
            seen.add((name,team,cat))
    return rows


def all_plays(drives):
    plays=[]
    for drive in drives.get('previous',[]): plays.extend(drive.get('plays',[]))
    current=drives.get('current')
    if isinstance(current,dict): plays.extend(current.get('plays',[]))
    unique={str(p.get('id')):p for p in plays if p.get('id')}
    return sorted(unique.values(),key=lambda p:int(p.get('sequenceNumber',0) or 0))


def event_player_splits(plays, players):
    """Derive per-quarter rush/receiving splits from ESPN's play labels and text."""
    aliases={}
    for p in players:
        bits=p['name'].replace('-', ' ').split()
        if len(bits)>=2:
            last=bits[-2] if bits[-1].lower() in {'jr.','jr','sr.','sr','iii','ii','iv'} else bits[-1]
            aliases[f'{bits[0][0]}.{last}'.lower()]=p['name']
    stats={}
    for play in plays:
        period=(play.get('period') or {}).get('number')
        if not period: continue
        typ=(play.get('type') or {}).get('text','').lower()
        text=play.get('text',''); yard=num(play.get('statYardage'))
        if yard is None: continue
        if typ in ('rush','rushing'):
            match=re.match(r'^\s*(?:\([^)]*\)\s*)?([A-Z]\.[A-Za-z\'’-]+)',text)
            key='rush'
        elif typ in ('pass reception','reception'):
            match=re.search(r'\bto\s+([A-Z]\.[A-Za-z\'’-]+)\s+(?:to|for|at)\b',text)
            key='receiving'
        else: continue
        if not match: continue
        name=aliases.get(match.group(1).lower(),match.group(1))
        row=stats.setdefault((name,period),{'rush_attempts':0,'rush_yards':0,'receptions':0,'receiving_yards':0})
        if key=='rush': row['rush_attempts']+=1; row['rush_yards']+=yard
        else: row['receptions']+=1; row['receiving_yards']+=yard
    out=[{'player':name,'period':period,**row} for (name,period),row in sorted(stats.items(),key=lambda x:(x[0][0],x[0][1]))]
    halves={}
    for row in out:
        if row['period']>2: continue
        h=halves.setdefault(row['player'],{'player':row['player'],'rush_attempts':0,'rush_yards':0,'receptions':0,'receiving_yards':0})
        for key in ('rush_attempts','rush_yards','receptions','receiving_yards'): h[key]+=row[key]
    return {'by_quarter':out,'first_half':list(halves.values()),
            'method':'Play-text/statYardage reconstruction; cross-check with official cumulative box score. Unmatched player abbreviations are retained.'}


def quarter_scores(header, scoring):
    c=(header.get('competitions') or [{}])[0]
    result={x.get('team',{}).get('abbreviation',''):{} for x in c.get('competitors',[])}
    # Prefer official linescores when present.
    for x in c.get('competitors',[]):
        team=x.get('team',{}).get('abbreviation','')
        for i,line in enumerate(x.get('linescores',[]),1):
            result.setdefault(team,{})[f'Q{i}']=line.get('displayValue') or line.get('value')
    # Score-by-play fallback, assigning scoring increments to the scoring play's quarter.
    prior={t:0 for t in result}
    increments={t:{} for t in result}
    for p in scoring or []:
        period=(p.get('period') or {}).get('number')
        if not period: continue
        for team, key in ((p.get('homeTeam',{}).get('abbreviation'), 'homeScore'),(p.get('awayTeam',{}).get('abbreviation'),'awayScore')):
            if team not in increments: continue
            score=num(p.get(key))
            if score is None: continue
            delta=score-prior[team]
            if delta>0:
                q=f'Q{period}'; increments[team][q]=increments[team].get(q,0)+delta
            prior[team]=score
    for team, qs in increments.items():
        for q,val in qs.items(): result.setdefault(team,{}).setdefault(q,val)
    for team, qs in result.items():
        for q in ('Q1','Q2','Q3','Q4','OT'): qs.setdefault(q,None)
    return result


def quarter_results(qscores, teams):
    if len(teams)<2: return []
    home=next((t for t in teams if t.get('home_away')=='home'),teams[0])
    away=next((t for t in teams if t.get('home_away')=='away'),teams[1])
    h=qscores.get(home['team'],{}); a=qscores.get(away['team'],{})
    out=[]; cum_h=cum_a=0
    for q in ('Q1','Q2','Q3','Q4','OT'):
        hv=num(h.get(q)); av=num(a.get(q))
        if hv is None or av is None: out.append({'period':q,'home_points':hv,'away_points':av,'winner':'pending','margin':None,'cumulative_margin':None}); continue
        margin=hv-av; cum_h+=hv; cum_a+=av
        out.append({'period':q,'home_points':hv,'away_points':av,
                    'winner':home['team'] if margin>0 else away['team'] if margin<0 else 'tie',
                    'margin':margin,'cumulative_margin':cum_h-cum_a})
    return out


def model_scores(evaluation):
    by_model={}
    for row in evaluation:
        y=1 if row['outcome']=='over' else 0 if row['outcome']=='under' else None
        if y is None: continue
        for model in row.get('models',[]):
            try: p=float(model['p_over'])
            except (TypeError,ValueError): continue
            p=min(max(p,1e-12),1-1e-12)
            item=by_model.setdefault(model['model'],{'n':0,'brier_sum':0.0,'logloss_sum':0.0})
            item['n']+=1; item['brier_sum']+=(p-y)**2
            item['logloss_sum']+=-(y*__import__('math').log(p)+(1-y)*__import__('math').log(1-p))
    return {name:{'n':v['n'],'brier':v['brier_sum']/v['n'],'logloss':v['logloss_sum']/v['n']}
            for name,v in by_model.items() if v['n']}


def odds_rows(odds):
    result=[]
    for event in odds.get('events',[]):
        for book in event.get('bookmakers',[]):
            if book.get('key') not in {'draftkings','fanduel'}: continue
            for market in book.get('markets',[]):
                for outcome in market.get('outcomes',[]):
                    result.append({'book':book.get('title') or book.get('key'),'market':market.get('key'),
                                   'outcome':outcome.get('name'),'point':outcome.get('point'),
                                   'price':outcome.get('price'),'last_update':market.get('last_update')})
    return result


def parse_odds_api():
    key=os.environ.get('ODDS_API_KEY','').strip()
    if not key:
        return {'status':'UNAVAILABLE: ODDS_API_KEY GitHub secret is not configured'}
    try:
        event_query=urllib.parse.urlencode({'apiKey':key,'dateFormat':'iso'})
        events=get_json(f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/?{event_query}')
        for event in events if isinstance(events,list) else []:
            names=' '.join([event.get('home_team',''),event.get('away_team','')]).lower()
            if 'atlanta falcons' in names and 'cincinnati bengals' in names:
                event_id=event.get('id')
                market_q=urllib.parse.urlencode({'apiKey':key,'regions':'us','dateFormat':'iso'})
                available=get_json(f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/markets/?{market_q}')
                wanted={'h2h','spreads','totals','h2h_h1','spreads_h1','totals_h1'}
                for qtr in range(1,5): wanted.update({f'h2h_q{qtr}',f'spreads_q{qtr}',f'totals_q{qtr}'})
                wanted.update({'player_pass_yds','player_pass_tds','player_rush_yds','player_rush_attempts','player_reception_yds','player_receptions'})
                available_keys=set()
                for book in available.get('bookmakers',[]) if isinstance(available,dict) else []:
                    for market in book.get('markets',[]):
                        if market.get('key') in wanted: available_keys.add(market['key'])
                if not available_keys: return {'status':'NO_SUPPORTED_MARKETS','event_id':event_id,'events':[]}
                oq=urllib.parse.urlencode({'apiKey':key,'regions':'us','markets':','.join(sorted(available_keys)),
                                           'oddsFormat':'american','dateFormat':'iso'})
                odds=get_json(f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/events/{event_id}/odds/?{oq}')
                return {'status':'OK','event_id':event_id,'markets_requested':sorted(available_keys),'events':[odds]}
        return {'status':'NO_MATCHING_EVENT','events':[]}
    except Exception as exc:
        return {'status':f'ERROR: {type(exc).__name__}: {exc}'}


def load_locked_lines():
    candidates=[ROOT/'research/week9_930/book_lines_20261108_0908ET.csv',ROOT/'research/week9_930/book_lines_20261108_0908ET.csv']
    for path in candidates:
        if path.exists():
            with path.open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
    return []


def final_evaluation(players):
    actual={}
    context={}
    for p in players:
        name=p['name']; cat=p['category']; stats=p['stats']
        context.setdefault(name,{})[cat]=stats
        if cat=='passing':
            actual[(name,'player_pass_yds')]=num(stats.get('YDS'))
            actual[(name,'player_pass_tds')]=num(stats.get('TD'))
        elif cat=='rushing':
            actual[(name,'player_rush_yds')]=num(stats.get('YDS'))
            actual[(name,'player_rush_attempts')]=num(stats.get('CAR'))
        elif cat=='receiving':
            actual[(name,'player_reception_yds')]=num(stats.get('YDS'))
            actual[(name,'player_receptions')]=num(stats.get('REC'))
    sims=ROOT/'research/week9_930/simulation_100k_20261108_0908ET.csv'
    sim_rows=[]
    if sims.exists():
        with sims.open(newline='',encoding='utf-8') as f: sim_rows=list(csv.DictReader(f))
    result=[]
    for line in load_locked_lines():
        name=line.get('player',''); key=line.get('market_key',''); val=actual.get((name,key))
        if val is None: continue
        try: threshold=float(line.get('dk_line',''))
        except (TypeError,ValueError): continue
        outcome='push' if val==threshold else ('over' if val>threshold else 'under')
        matched=[s for s in sim_rows if s.get('player')==name and s.get('market_key')==key and s.get('book')=='DraftKings']
        cats=context.get(name,{})
        if key.startswith('player_pass_'):
            st=cats.get('passing',{}); completed,attempted=(st.get('C/ATT','0/0').split('/')+['0'])[:2]
            comp=num(completed) or 0; att=num(attempted) or 0; yards=num(st.get('YDS')) or 0
            why=f"{int(comp)}/{int(att)} completions, {yards:g} pass yards ({yards/att:.1f} yards/attempt)" if att else 'No pass attempts recorded'
        elif key in ('player_rush_yds','player_rush_attempts'):
            st=cats.get('rushing',{}); carries=num(st.get('CAR')) or 0; yards=num(st.get('YDS')) or 0
            why=f"{carries:g} carries, {yards:g} rush yards ({yards/carries:.1f} yards/carry)" if carries else 'No carries recorded'
        else:
            st=cats.get('receiving',{}); rec=num(st.get('REC')) or 0; targets=num(st.get('TGTS')) or 0; yards=num(st.get('YDS')) or 0
            why=f"{rec:g}/{targets:g} targets caught for {yards:g} receiving yards" + (f" ({yards/rec:.1f} yards/catch)" if rec else '')
        result.append({'player':name,'team':line.get('team'),'market_key':key,'line':threshold,
                       'actual':val,'outcome':outcome,'usage_note':why,
                       'models':[{'model':s.get('model'),'mean':s.get('mean'),'p_over':s.get('p_over'),'p_under':s.get('p_under'),'status':s.get('status')} for s in matched]})
    return result


def main():
    now=dt.datetime.now(dt.timezone.utc)
    if now.astimezone(ET).date().isoformat()!=GAME_DATE:
        print('Guard: tracker is scoped to 2026-11-08; no collection today.'); return 0
    package=get_json(f'{BASE}?event={EVENT_ID}')
    header=package.get('header',{})
    comp=(header.get('competitions') or [{}])[0]
    status=(comp.get('status') or {}).get('type',{}).get('description','Unknown')
    latest=OUT/'latest.json'
    if status.lower()=='final' and latest.exists():
        try:
            if json.loads(latest.read_text(encoding='utf-8')).get('status','').lower()=='final':
                print('Game already finalized in the latest snapshot; no duplicate collection.'); return 0
        except Exception: pass
    teams=[]
    for t in comp.get('competitors',[]):
        teams.append({'team':t.get('team',{}).get('abbreviation'), 'name':t.get('team',{}).get('displayName'),
                      'home_away':t.get('homeAway'),'score':num(t.get('score')),
                      'quarter_scores':[x.get('displayValue') or x.get('value') for x in t.get('linescores',[])]})
    plays=all_plays(package.get('drives',{}))
    players=add_projected_zeros(player_rows(package.get('boxscore',{})),load_locked_lines())
    event_splits=event_player_splits(plays,players)
    snapshot={'captured_at_utc':now.isoformat(),'captured_at_et':now.astimezone(ET).isoformat(),
        'source':'ESPN NFL summary API','source_url':f'{BASE}?event={EVENT_ID}','event_id':EVENT_ID,
        'game':'Cincinnati Bengals at Atlanta Falcons','status':status,
        'period':(comp.get('status') or {}).get('period'),'clock':(comp.get('status') or {}).get('displayClock'),
        'teams':teams,'quarter_scores':quarter_scores(header,package.get('scoringPlays',[])),
        'player_boxscore_cumulative':players,'player_period_splits':event_splits,
        'play_by_play':plays,'live_odds':parse_odds_api()}
    if status.lower()=='final': snapshot['projection_evaluation']=final_evaluation(players)
    snapshot['model_score_summary']=model_scores(snapshot.get('projection_evaluation',[]))
    snapshot['quarter_results']=quarter_results(snapshot['quarter_scores'],teams)
    snapshot['tracked_odds_rows']=odds_rows(snapshot['live_odds'])
    OUT.mkdir(parents=True,exist_ok=True)
    stamp=now.strftime('%Y%m%dT%H%M%SZ')
    (OUT/f'{stamp}.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
    (OUT/'latest.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
    q=snapshot['quarter_scores']
    rows=['# Bengals–Falcons live tracker','',f"**Last update:** {snapshot['captured_at_et']} ET  |  **State:** {status} — Q{snapshot['period']} {snapshot['clock']}",'',
          f"**Score:** {teams[0]['team']} {teams[0]['score']} – {teams[1]['team']} {teams[1]['score']}",'',
          '## Quarter score and spread tracking','', '| Team | Q1 | Q2 | Q3 | Q4 | OT | Final |','|---|---:|---:|---:|---:|---:|---:|']
    for t in teams:
        qs=q.get(t['team'],{})
        rows.append('| '+t['team']+' | '+' | '.join(str(qs.get(k,'—') if qs.get(k) is not None else '—') for k in ('Q1','Q2','Q3','Q4','OT'))+' | '+str(t['score'])+' |')
    rows += ['', 'Quarter scoring margin = home points minus away points. Cumulative margin is the score difference at each quarter end.', '', '| Period | ATL points | CIN points | Quarter winner | Quarter margin (ATL−CIN) | Cumulative margin (ATL−CIN) |','|---|---:|---:|---|---:|---:|']
    for qr in snapshot['quarter_results']:
        # Keep the teams explicit so home/away presentation cannot be mistaken for the margin sign.
        atl=num(q.get('ATL',{}).get(qr['period'])); cin=num(q.get('CIN',{}).get(qr['period']))
        if atl is None or cin is None: continue
        winner='ATL' if atl>cin else 'CIN' if cin>atl else 'tie'
        rows.append(f"| {qr['period']} | {atl} | {cin} | {winner} | {atl-cin:+g} | {qr['cumulative_margin'] if qr['cumulative_margin'] is not None else '—'} |")
    rows += ['', 'Quarter winners, margins, and cover results will be finalized from completed quarter scores. Cover results require an actual captured quarter spread line.', '', '## Player production (official cumulative box score)', '', '| Player | Team | Category | Stats |','|---|---|---|---|']
    for p in players:
        rows.append(f"| {p['name']} | {p['team']} | {p['category']} | "+', '.join(f'{k}: {v}' for k,v in p['stats'].items())+' |')
    rows += ['', '## Player rush and receiving splits by quarter', '', 'Derived from play events; official cumulative box-score totals remain the authority.', '', '| Player | Quarter | Carries | Rush yards | Receptions | Receiving yards |','|---|---:|---:|---:|---:|---:|']
    for p in event_splits['by_quarter']:
        rows.append(f"| {p['player']} | Q{p['period']} | {p['rush_attempts']} | {p['rush_yards']:g} | {p['receptions']} | {p['receiving_yards']:g} |")
    rows += ['', '### First-half rollup','', '| Player | Carries | Rush yards | Receptions | Receiving yards |','|---|---:|---:|---:|---:|']
    for p in event_splits['first_half']:
        rows.append(f"| {p['player']} | {p['rush_attempts']} | {p['rush_yards']:g} | {p['receptions']} | {p['receiving_yards']:g} |")
    rows += ['', '## Lines and projection evaluation','', f"- Live sportsbook odds: **{snapshot['live_odds']['status']}**.", '- Pregame prop lines and three frozen simulation runs are in the 09:08 ET locked artifacts. They are not relabeled as live prices.', '- Official box-score outcomes are used to evaluate the frozen DraftKings thresholds at game end; simulation frequencies remain labeled raw, uncalibrated model outputs.', '- Quarter-score cover results require a captured sportsbook spread. Odds rows are saved only when the feed returns them.', '']
    if snapshot['tracked_odds_rows']:
        rows += ['| Book | Market | Selection | Line | Price | Updated |','|---|---|---|---:|---:|---|']
        for r in snapshot['tracked_odds_rows']:
            rows.append(f"| {r['book']} | {r['market']} | {r['outcome']} | {r['point'] if r['point'] is not None else '—'} | {r['price']} | {r['last_update'] or '—'} |")
    if status.lower()=='final':
        rows += ['', '## Frozen projection hit/miss audit', '', '| Player | Market | DK line | Actual | Threshold result | Usage / production note | Model | Mean | Raw P(over) |','|---|---|---:|---:|---|---|---|---:|---:|']
        for entry in snapshot.get('projection_evaluation',[]):
            models=entry.get('models') or [{'model':'no matching frozen row','mean':'—','p_over':'—'}]
            for model in models:
                rows.append(f"| {entry['player']} | {entry['market_key']} | {entry['line']:g} | {entry['actual']:g} | {entry['outcome']} | {entry['usage_note']} | {model['model']} | {model['mean']} | {model['p_over']} |")
        rows += ['', 'Probability score on this single game (pushes excluded; smaller is better):', '']
        rows += [f"- `{name}`: n={score['n']}, Brier={score['brier']:.4f}, log loss={score['logloss']:.4f}." for name,score in snapshot['model_score_summary'].items()]
        rows += ['', 'These are one-game holdout scores, not a recalibration fit. The separate historical calibration audit remains the evidence for calibration; this game adds an untouched result to that record.']
    rows += ['', f"Raw play-by-play and snapshot: `{stamp}.json`."]
    (OUT/'LIVE_TRACKER.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    journal=OUT/'updates.jsonl'
    with journal.open('a',encoding='utf-8') as f: f.write(json.dumps({'captured_at_utc':snapshot['captured_at_utc'],'status':status,'period':snapshot['period'],'clock':snapshot['clock'],'teams':teams,'quarter_scores':q,'player_boxscore_cumulative':players,'live_odds_status':snapshot['live_odds']['status']},separators=(',',':'))+'\n')
    print(json.dumps({'captured_at_et':snapshot['captured_at_et'],'status':status,'period':snapshot['period'],'clock':snapshot['clock'],'teams':teams,'players':len(players),'plays':len(plays),'live_odds':snapshot['live_odds']['status']}))
    return 0

if __name__=='__main__': sys.exit(main())
