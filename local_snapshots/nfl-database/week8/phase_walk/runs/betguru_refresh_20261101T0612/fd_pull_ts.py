import json,urllib.request,csv,datetime
U="https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=%d&tab=%s"
ev=json.load(open('../slate.json')) if False else None
ids=[36215311,36215312,36215313,36215314,36215315,36215316,36215317,36215318,36215319,36215320,36215321,36215322,36215324]
rows=[]
for E in ids:
  seen=set();name=''
  for tab in ['receiving-props','rushing-props','passing-props','popular','player-props','game-lines','touchdown-scorers']:
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(U%(E,tab),headers={'User-Agent':'Mozilla/5.0'}),timeout=20))
    except Exception as e: print(E,tab,e); continue
    evs=d.get('attachments',{}).get('events',{})
    if evs: name=list(evs.values())[0].get('name','')
    for m in d.get('attachments',{}).get('markets',{}).values():
      if m['marketId'] in seen: continue
      seen.add(m['marketId'])
      for r in m.get('runners',[]):
        o=r.get('winRunnerOdds',{}).get('americanDisplayOdds',{}).get('americanOdds')
        rows.append([name,E,m['marketName'],r.get('runnerName'),r.get('handicap'),o])
w=csv.writer(open('fd_refresh.csv','w'));w.writerow(['game','event','market','runner','hcp','odds']);w.writerows(rows)
open('fd_refresh_pulled_at.txt','w').write(datetime.datetime.now().isoformat())
print(len(rows))
