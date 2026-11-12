import sqlite3,json
c=sqlite3.connect('repo/data/nfl_matchups.sqlite'); f=sqlite3.connect('fixes/fixes.sqlite')
G={'401872929':('PHI','WSH'),'401872931':('KC','DEN'),'401872964':('CLE','PIT')}
out={}
for gid in G:
    d=json.loads(c.execute('select data from games where game_id=?',(gid,)).fetchone()[0])
    comp=d['competitions'][0]['competitors']; tid={x['team']['id']:x['team']['abbreviation'] for x in comp}
    lines={}
    for team,pid,name,cat,dd in c.execute('select team,player_id,player,category,data from player_stats where game_id=? and category in ("passing","rushing","receiving")',(gid,)):
        lines.setdefault((tid.get(team,team),name,pid),{})[cat]=json.loads(dd)
    snaps={r[0]:(r[1],r[2],r[3]) for r in f.execute('select espn_id,position,offense_snaps,offense_pct from fix_participation where espn_game_id=?',(gid,))}
    big=[]
    for off,yd,dd in c.execute('select offense_id,yards,data from plays where game_id=? order by cast(play_id as integer)',(gid,)):
        dd=json.loads(dd)
        if dd.get('scoringPlay') or (yd or 0)>=20 or dd.get('isTurnover'):
            big.append(f"Q{dd['period']['number']} {dd['clock']['displayValue']} {tid.get(off,off)} ({yd} yds; {dd.get('awayScore')}-{dd.get('homeScore')} away-home): {dd['text']}")
    qs=[f"Q{l['period']}: away {l['displayValue']}" for x in comp for l in x.get('linescores',[]) if x['homeAway']=='away']
    qh=[l['displayValue'] for x in comp for l in x.get('linescores',[]) if x['homeAway']=='home']
    out[gid]=dict(date=d['date'],score=' '.join(f"{x['team']['abbreviation']} {x['score']}" for x in comp),linescore_away=qs,linescore_home=qh,
      players=[dict(team=k[0],name=k[1],snap=snaps.get(k[2]),**v) for k,v in lines.items()],key_plays=big,
      recap=[h.get('shortLinkText','')+' — '+h.get('description','') for h in d['competitions'][0].get('headlines',[])])
json.dump(out,open('week8/rematches/first_meetings.json','w'),indent=1)
for g,v in out.items(): print(g,v['score'],len(v['players']),sum(1 for p in v['players'] if p['snap']))
