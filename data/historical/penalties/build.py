import json,re,csv,collections,statistics as st
games=json.load(open('raw/games.json'))
res=collections.Counter()
R=re.compile(r'PENALTY on ([A-Z]{2,3})(?:-([A-Za-z.\'\- ]+?))?, ([^,]+), (\d+) yards?',re.I)
KILL=('PUNT','INT','FUMBLE','DOWNS','MISSED FG','BLOCKED','FG MISSED','BLOCKED PUNT','BLOCKED FG','INTERCEPTION','FUMBLE RETURN TD','INT TD','PUNT RETURN TD','DOWNS ')
rows=[];q1=collections.Counter();comp={}
for w,gid in games:
    d=json.load(open(f'raw/{gid}.json'))
    for t in d['boxscore']['teams']:
        s={x['name']:x['displayValue'] for x in t['statistics']}
        c=s.get('completionAttempts','').split('/')
        if len(c)==2: comp[(w,gid,t['team']['abbreviation'])]=int(c[0])
    for i,dr in enumerate(d['drives']['previous']):
        off=dr['team']['abbreviation']; r=(dr.get('result') or '').upper(); res[r]+=1
        killer=any(r.startswith(k) for k in KILL) and 'TD' not in r
        for p in dr['plays']:
            tx=p['text']
            if re.search(r'kicks|punts|field goal|extra point|two-point',tx,re.I) and not tx.upper().startswith('(SHOTGUN) PENALTY'): 
                if 'enforced between downs' in tx or re.search(r'kicks|punts|field goal',tx,re.I): continue
            for m in R.finditer(tx):
                tm,pl,ty,yd=m.groups()
                seg=tx[m.end():m.end()+80]
                if 'Offsetting' in tx or 'offsetting' in seg: continue
                if tm!=off: continue
                if p['period']['number']==1: q1[(w,gid,off)]+=1
                if killer:
                    rows.append(dict(week=w,game_id=gid,team=off,drive_id=dr.get('id',f'{gid}-{i}'),drive_result=r,quarter=p['period']['number'],
                      clock=p['clock']['displayValue'],player=(pl or '').strip(),type=ty.strip(),yards=int(yd),ten_plus=int(yd)>=10,
                      no_play='No Play' in seg,yards_to_endzone=(p.get('start') or {}).get('yardsToEndzone'),raw_text=tx))
with open('drive_killers_2026.csv','w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print(res.most_common())
print('rows',len(rows),'games',len(games))
tc=collections.Counter(r['team'] for r in rows);t10=collections.Counter(r['team'] for r in rows if r['ten_plus'])
gp=collections.Counter(k[2] for k in comp)
print('top teams',[(t,n,round(n/gp[t],2),t10[t]) for t,n in tc.most_common(8)])
print('types',collections.Counter(r['type'] for r in rows).most_common(6))
print('players',collections.Counter((r['team'],r['player'],r['type']) for r in rows if r['player']).most_common(6))
print('players any',collections.Counter((r['team'],r['player']) for r in rows if r['player']).most_common(6))
# validation
avg=collections.defaultdict(list)
for k,v in comp.items(): avg[k[2]].append(v)
xs=[];ys=[]
for k,v in comp.items():
    xs.append(q1[k]); ys.append(v-st.mean(avg[k[2]]))
print('n',len(xs),'r',round(st.correlation(xs,ys),3))
for b in (0,1,2):
    g=[y for x,y in zip(xs,ys) if (x>=2 if b==2 else x==b)]; print('q1 off pen',b,len(g),round(st.mean(g),2))
print('LAR w8',[(k,v,q1[k]) for k,v in comp.items() if k[0]==8 and k[2]=='LAR'])
