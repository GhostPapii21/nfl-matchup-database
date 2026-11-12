"""Normalize FanDuel event-page props -> props.csv/props.json. DraftKings: blocked (see GAPS)."""
import json,glob,re,csv,os
W='/workspace/nfl-database/week8/'
R=W+'props/raw/'
pulled=open(R+'fd_pulled_at.txt').read().split()[1]
EV={36215311:'CAR@GB',36215312:'TEN@CIN',36215313:'BAL@BUF',36215314:'ARI@DAL',36215315:'CLE@PIT',36215316:'LAC@LAR',
    36215317:'IND@JAX',36215318:'MIN@DET',36215319:'ATL@TB',36215320:'LV@NYJ',36215321:'KC@DEN',36215322:'NE@MIA',36215324:'PHI@WSH'}
norm=lambda s:re.sub(r'[^a-z]','',re.sub(r'\b(jr|sr|ii|iii|iv|v)\b\.?','',s.lower()))
def key(n):
    p=[x for x in n.replace('.',' ').split() if x.lower().strip('.') not in('jr','sr','ii','iii','iv','v')]
    return (p[0][0].lower(),norm(p[-1])) if p else None
# roster names (week8/rosters) and full.json names
ROS={}
for f in glob.glob(W+'rosters/*.json'):
    try: r=json.load(open(f))
    except: continue
    if 'players' not in r: continue
    for p in r['players']: ROS.setdefault(key(p['name']),[]).append((p['name'],r['team']))
FULL=json.load(open(W+'breakdown/full/full.json'))
FN={}
for g in FULL['games']:
    for t in g['teams']:
        for p in t['players']: FN[(g['id'],key(p['name']))]=(p['name'],t['team'])
GID={'LAC@LAR':'LAC@LA','PHI@WSH':'PHI@WAS'}
gids={g['id'] for g in FULL['games']}
MK={'Receiving Yds':'rec_yds','Total Receptions':'receptions','Rushing Yds':'rush_yds','Rushing + Receiving Yds':'rush_rec_yds','Passing Yds':'pass_yds',
    'Alt Receiving Yds':'rec_yds_alt','Alt Receptions':'receptions_alt','Alt Rushing Yds':'rush_yds_alt','Alt Passing Yds':'pass_yds_alt'}
odds=lambda r:r.get('winRunnerOdds',{}).get('americanDisplayOdds',{}).get('americanOddsInt')
rows={}; unmatched=set()
def ident(game,name):
    g=GID.get(game,game) if GID.get(game,game) in gids else game
    k=key(name)
    strip=lambda n:norm(n)
    for (gg,kk),(n,t) in FN.items():
        if gg==g and strip(n)==strip(name): return (n,t)
    if (g,k) in FN and sum(1 for (gg,kk) in FN if gg==g and kk==k)==1:
        n,t=FN[(g,k)]
        # same initial+last but different first name -> not the same player
        if norm(n.split()[0])[:3]==norm(name.split()[0])[:3]: return (n,t)
    al={'LAR':'LA','LA':'LAR','WSH':'WAS','WAS':'WSH'}
    teams=set(game.split('@'))|{al.get(x,x) for x in game.split('@')}
    for n,t in ROS.get(k,[]):
        if t in teams and norm(n.split()[0])[:3]==norm(name.split()[0])[:3]: return (n,t)
    unmatched.add((game,name)); return (name,'')
for f in sorted(glob.glob(R+'fd_*_*.json')):
    eid=int(f.split('fd_')[1].split('_')[0]); game=EV.get(eid)
    if not game: continue
    for m in json.load(open(f)).get('attachments',{}).get('markets',{}).values():
        nm=m['marketName']
        if nm=='Any Time Touchdown Scorer':
            for r in m['runners']:
                pl,tm=ident(game,r['runnerName'])
                rows[(game,pl,'anytime_td')]=dict(game=game,player=pl,team=tm,book='FanDuel',market='anytime_td',line='',over_odds=odds(r),under_odds='',alt='',pulled_at_et=pulled,fd_name=r['runnerName'])
            continue
        if ' - ' not in nm: continue
        who,mk=nm.split(' - ',1); mk=MK.get(mk)
        if not mk: continue
        pl,tm=ident(game,who)
        k=(game,pl,mk.replace('_alt',''))
        row=rows.setdefault(k,dict(game=game,player=pl,team=tm,book='FanDuel',market=mk.replace('_alt',''),line='',over_odds='',under_odds='',alt=[],pulled_at_et=pulled,fd_name=who))
        if mk.endswith('_alt'):
            for r in m['runners']:
                mm=re.search(r'(\d+)\+',r['runnerName'])
                if mm: row['alt'].append([int(mm.group(1)),odds(r)])
        else:
            for r in m['runners']:
                if r['runnerName'].endswith('Over'): row['line']=r['handicap']; row['over_odds']=odds(r)
                elif r['runnerName'].endswith('Under'): row['under_odds']=odds(r)
out=[]
for r in rows.values():
    if isinstance(r['alt'],list): r['alt']=sorted(set(map(tuple,r['alt'])))
    out.append(r)
out.sort(key=lambda r:(r['game'],r['team'],r['player'],r['market']))
json.dump(dict(pulled_at_et=pulled,books={'FanDuel':'ok (sbapi.nj.sportsbook.fanduel.com event-page, NJ)','DraftKings':'UNAVAILABLE: DK API 403/blocked from box; Odds API quota 0; balldontlie key rejected'},rows=out),open(W+'props/props.json','w'),indent=1)
with open(W+'props/props.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['game','player','team','book','market','line','over_odds','under_odds','alt','pulled_at_et','fd_name']); w.writeheader()
    for r in out: w.writerow({**r,'alt':' '.join(f"{a}+:{o}" for a,o in r['alt']) if r['alt'] else ''})
print(len(out),'rows; unmatched',len(unmatched)); print(sorted(unmatched)[:40])
