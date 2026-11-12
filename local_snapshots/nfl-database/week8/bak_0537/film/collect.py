import sqlite3,json,subprocess,re,os,glob
c=sqlite3.connect('repo/data/nfl_matchups.sqlite')
slate=json.load(open('week8/slate.json'))
teams=set()
for g in slate['games']:
    a,h=g['matchup'].split(' @ '); teams|={a,h}
games={}
for gid,d in c.execute("select game_id,data from games where status='STATUS_FINAL'"):
    d=json.loads(d); w=d['week']['number']
    if w>6: continue
    comp=d['competitions'][0]['competitors']
    ab={x['homeAway']:x for x in comp}
    A,H=ab['away']['team']['abbreviation'],ab['home']['team']['abbreviation']
    if A in teams or H in teams:
        games[gid]=dict(gid=gid,week=w,away=A,home=H,awayName=ab['away']['team']['displayName'],homeName=ab['home']['team']['displayName'],
          score=f"{A} {ab['away']['score']} - {H} {ab['home']['score']}",date=d['date'],tid={A:ab['away']['team']['id'],H:ab['home']['team']['id']})
os.makedirs('week8/film/games',exist_ok=True)
for gid,g in games.items():
    idt={v:k for k,v in g['tid'].items()}
    plays=[]
    for pid,off,pt,yd,dd in c.execute("select play_id,offense_id,play_type,yards,data from plays where game_id=? order by cast(play_id as integer)",(gid,)):
        dd=json.loads(dd)
        if dd.get('scoringPlay') or (yd or 0)>=20 or dd.get('isTurnover'):
            plays.append(f"Q{dd['period']['number']} {dd['clock']['displayValue']} | {idt.get(off,off)} | {pt} | {yd} yds | score {g['away']} {dd.get('awayScore')}-{g['home']} {dd.get('homeScore')} | {dd['text']}")
    g['key_plays']=plays
    json.dump(g,open(f'week8/film/games/{gid}.json','w'),indent=1)
print(len(teams),len(games))
