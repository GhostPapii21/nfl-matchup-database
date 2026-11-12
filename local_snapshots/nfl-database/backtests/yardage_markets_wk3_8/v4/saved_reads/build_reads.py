"""Build reads_by_game.jsonl from saved BetGuru transcript pages (ReadTranscript dumps).
Only quotes real text; keeps a message for a game only if its timestamp is before that game's kickoff
and inside that game's week window (TNF-2d .. kickoff)."""
import json,re,glob,sys,datetime as dt
import pandas as pd
TX=sys.argv[1]; OUT=sys.argv[2]
g=pd.read_csv('/workspace/games.csv',low_memory=False)
g=g[(g.season==2026)&(g.week.between(3,8))]
ros=pd.read_parquet('/workspace/ros_2026.parquet')
ros=ros.sort_values('week').drop_duplicates('full_name',keep='last')
TEAMN={'ARI':['Cardinals','Arizona'],'ATL':['Falcons','Atlanta'],'BAL':['Ravens','Baltimore'],'BUF':['Bills','Buffalo'],'CAR':['Panthers','Carolina'],'CHI':['Bears','Chicago'],'CIN':['Bengals','Cincinnati'],'CLE':['Browns','Cleveland'],'DAL':['Cowboys','Dallas'],'DEN':['Broncos','Denver'],'DET':['Lions','Detroit'],'GB':['Packers','Green Bay'],'HOU':['Texans','Houston'],'IND':['Colts','Indianapolis'],'JAX':['Jaguars','Jacksonville'],'KC':['Chiefs','Kansas City'],'LV':['Raiders','Las Vegas'],'LAC':['Chargers'],'LA':['Rams'],'MIA':['Dolphins','Miami'],'MIN':['Vikings','Minnesota'],'NE':['Patriots','New England'],'NO':['Saints','New Orleans'],'NYG':['Giants'],'NYJ':['Jets'],'PHI':['Eagles','Philadelphia'],'PIT':['Steelers','Pittsburgh'],'SEA':['Seahawks','Seattle'],'SF':['49ers','Niners','San Francisco'],'TB':['Buccaneers','Bucs','Tampa'],'TEN':['Titans','Tennessee'],'WAS':['Commanders','Washington']}
# skill-position players only, full names (avoid last-name false positives)
sk=ros[ros.position.isin(['QB','RB','WR','TE','FB'])]
PL={r.full_name:r.team for r in sk.itertuples() if isinstance(r.full_name,str)}
def ts_parse(s):
    m=re.match(r'\w+, (\w+ \d+, \d{4}), (\d+:\d+ [AP]M) \(UTC([+-]\d+)\)',s)
    d=dt.datetime.strptime(m.group(1)+' '+m.group(2),'%b %d, %Y %I:%M %p')
    off=int(m.group(3));  # convert to ET (UTC-4 in Oct before Nov 1 DST end, UTC-5 after)
    return d,off
msgs=[];seen=set()
for f in sorted(glob.glob(TX+'/*.txt')):
    ts=None
    for line in open(f):
        line=line.strip()
        if not line.startswith('{'): continue
        try: m=json.loads(line)
        except: continue
        for c in m.get('message',{}).get('content',[]):
            if c.get('type')=='text' and m['role']=='user':
                t=c['text']; mt=re.search(r'<timestamp>([^<]*)',t)
                if mt: ts=mt.group(1)
                q=re.search(r'<user_query>(.*?)</user_query>',t,re.S)
                if not q: continue
                q=q.group(1)
                if 'GROK_BOT_HIDDEN_PROMPT' in q:
                    gm=re.search(r'\[Group chat: "([^"]+)"',q)
                    if not gm or 'New messages in the room' not in q: continue
                    body=q.split('New messages in the room (oldest first):',1)[1].split("It's your turn",1)[0]
                    parts=re.split(r'\n(?=(?:User \(user\)|Smoke|Ghost6[^:\n]*|Blitz[^:\n]*|TopShotta[^:\n]*|BetGuru[^:\n]*): )',"\n"+body.strip())
                    for p in parts:
                        p=p.strip()
                        if not p or ':' not in p: continue
                        who,txt=p.split(': ',1)
                        who='Rico' if who.startswith('User') else who.strip()
                        msgs.append(dict(ts=ts,who=who,room=gm.group(1),text=txt.strip(),src=f))
                else:
                    msgs.append(dict(ts=ts,who='Rico',room='BetGuru 1:1',text=re.sub(r'^\[t\w+\]\s*','',q.strip()),src=f))
            if c.get('type')=='tool_use' and c.get('name')=='SendToUser':
                msgs.append(dict(ts=ts,who='BetGuru',room='(BetGuru send)',text=c['input'].get('content',''),src=f))
rows=[]
for mm in msgs:
    if not mm['ts'] or len(mm['text'])<25: continue
    key=(mm['who'],mm['text'][:200])
    if key in seen: continue
    seen.add(key)
    d,off=ts_parse(mm['ts']); d_et=d+dt.timedelta(hours=(-5 if d>=dt.datetime(2026,11,1,2) else -4)-off)
    t=mm['text']
    teams=set(a for a,ns in TEAMN.items() if any(re.search(r'\b'+re.escape(n)+r'\b',t) for n in ns))
    players={n:tm for n,tm in PL.items() if n in t}
    teams|=set(players.values())
    for r in g.itertuples():
        if not ({r.away_team,r.home_team}&teams): continue
        ko=dt.datetime.strptime(f'{r.gameday} {r.gametime}','%Y-%m-%d %H:%M')
        wk_start=dt.datetime.strptime(g[g.week==r.week].gameday.min(),'%Y-%m-%d')-dt.timedelta(days=3)
        if not (wk_start<=d_et<ko): continue
        mk=sorted(set(x.lower() for x in re.findall(r'(rec(?:eiving)? yards|rush(?:ing)? yards|receptions|rush\+rec|passing yards|pass yards|anytime TD|ATD|longest|targets|carries)',t,re.I)))
        rows.append(dict(week=int(r.week),game=f'{r.away_team}@{r.home_team}',kickoff_et=ko.strftime('%Y-%m-%d %H:%M ET'),
          read_ts_et=d_et.strftime('%Y-%m-%d %H:%M ET'),author=mm['who'],source_session=('BetGuru transcript ff79913d-8e37-4af9-b035-11a26727df67; room: '+mm['room']),
          source_page=mm['src'].split('/')[-1],quoted_text=t,players_named=sorted(n for n,tm in players.items() if tm in (r.away_team,r.home_team)),markets_named=mk))
with open(OUT,'w') as fo:
    for x in sorted(rows,key=lambda x:(x['week'],x['kickoff_et'],x['game'],x['read_ts_et'])): fo.write(json.dumps(x)+'\n')
print(len(msgs),'msgs',len(rows),'rows')
