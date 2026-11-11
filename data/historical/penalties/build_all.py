import json,re,csv,collections
games=json.load(open('raw/games.json'))
R=re.compile(r'PENALTY on ([A-Z]{2,3})(?:-([^,]+?))?, ([^,]+?), (?:(\d+) yards?|(declined)|(offsetting))',re.I)
KILL=('PUNT','INT','FUMBLE','DOWNS','MISSED FG','BLOCKED')
PRE={'false start','delay of game','illegal formation/shift/motion'}
AUTO={'dpi','defensive holding','illegal contact','roughing','face mask'}
def norm(t):
    l=t.lower()
    for k,v in [('false start','false start'),('offensive holding','offensive holding'),('illegal formation','illegal formation/shift/motion'),('illegal shift','illegal formation/shift/motion'),('illegal motion','illegal formation/shift/motion'),('offensive pass interference','OPI'),('defensive pass interference','DPI'),('roughing','roughing'),('face mask','face mask'),('defensive holding','defensive holding'),('illegal contact','illegal contact'),('delay of game','delay of game')]:
        if k in l: return v
    return 'other'
rows=[];per=collections.Counter()
for w,gid in games:
    per[w]+=1
    d=json.load(open(f'raw/{gid}.json'))
    comp=d['header']['competitions'][0]['competitors']
    ha={c['team']['abbreviation']:c['homeAway'] for c in comp}
    AL={}
    for a in ha:
        for x in {'LAR':['LA'],'WSH':['WAS'],'JAX':['JAC'],'LAC':['SD'],'LV':['OAK']}.get(a,[]): AL[x]=a
    for i,dr in enumerate(d['drives']['previous']):
        off=dr['team']['abbreviation'];r=(dr.get('result') or '').upper()
        killer=r.startswith(KILL) and 'TD' not in r
        for p in dr['plays']:
            tx=p['text'];kick=bool(re.search(r'kicks|punts|field goal|extra point|Punt formation|Field Goal formation',tx,re.I))
            for m in R.finditer(tx):
                tm,pl,ty,yd,dec,offs=m.groups();tm=AL.get(tm,tm);seg=tx[m.end():m.end()+60]
                status='offsetting' if offs else 'declined' if dec else 'no-play' if 'No Play' in seg else 'accepted'
                nt=norm(ty);side='offense' if nt in PRE else 'special teams' if kick else 'offense' if tm==off else 'defense'
                nt=norm(ty);opp=[t for t in ha if t!=tm]
                s=p.get('start') or {}
                rows.append(dict(game_id=gid,week=w,team=tm,opp=opp[0] if opp else '',home_away=ha.get(tm,''),side=side,status=status,type=nt,raw_type=ty.strip(),
                  yards=int(yd) if yd else 0,quarter=p['period']['number'],clock=p['clock']['displayValue'],player=(pl or '').strip(),down=s.get('down'),distance=s.get('distance'),
                  yardline=s.get('yardsToEndzone'),drive_id=dr.get('id',f'{gid}-{i}'),drive_outcome=r,
                  auto_first_down=side=='defense' and status in('accepted','no-play') and (nt in AUTO or 'automatic first down' in tx.lower()),
                  drive_killer=side=='offense' and tm==off and status in('accepted','no-play') and killer,raw_text=tx))
with open('penalties_2026.csv','w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print(len(rows),dict(per),collections.Counter(r['status'] for r in rows),collections.Counter(r['side'] for r in rows))
print('killers',sum(r['drive_killer'] for r in rows))
# box check
mism=0
for w,gid in games:
    d=json.load(open(f'raw/{gid}.json'))
    for t in d['boxscore']['teams']:
        s={x['name']:x['displayValue'] for x in t['statistics']}
        n=int(s['totalPenaltiesYards'].split('-')[0]);a=t['team']['abbreviation']
        m=sum(1 for r in rows if r['game_id']==gid and r['team']==a and r['status'] in('accepted','no-play'))
        mism+=abs(n-m)
print('abs diff vs box accepted',mism)
