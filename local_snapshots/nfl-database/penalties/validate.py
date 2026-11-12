import json,csv,collections,statistics as st
games=json.load(open('raw/games.json'));P=list(csv.DictReader(open('penalties_2026.csv')))
q1=collections.Counter();tot=collections.Counter();dk=collections.Counter()
for r in P:
    k=(r['game_id'],r['team'])
    if r['side']=='offense' and r['status'] in('accepted','no-play'):
        tot[k]+=1; q1[k]+=r['quarter']=='1'
    if r['drive_killer']=='True': dk[k]+=1
T=[]
for w,gid in games:
    d=json.load(open(f'raw/{gid}.json'));sc={c['team']['abbreviation']:int(c['score']) for c in d['header']['competitions'][0]['competitors']}
    for t in d['boxscore']['teams']:
        a=t['team']['abbreviation'];s={x['name']:x['displayValue'] for x in t['statistics']}
        c,att=map(int,s['completionAttempts'].split('/'));o=[v for v in sc if v!=a][0]
        T.append(dict(team=a,c=c,att=att,plays=int(s.get('totalOffensivePlays',0) or 0),m=sc[a]-sc[o],q1=q1[(gid,a)],tot=tot[(gid,a)],dk=dk[(gid,a)]))
for f in('c','att','plays'):
    av=collections.defaultdict(list)
    for x in T: av[x['team']].append(x[f])
    for x in T: x['d'+f]=x[f]-st.mean(av[x['team']])
def res(y,x):
    b,a=st.linear_regression(x,y);return [yi-(a+b*xi) for xi,yi in zip(x,y)]
M=[x['m'] for x in T]
def rep(xn,yn):
    X=[t[xn] for t in T];Y=[t[yn] for t in T]
    print(f"{xn} vs {yn}: r={st.correlation(X,Y):+.3f}  partial|margin={st.correlation(res(X,M),res(Y,M)):+.3f}  n={len(T)}")
print('margin vs dc',round(st.correlation(M,[t['dc'] for t in T]),3),'vs datt',round(st.correlation(M,[t['datt'] for t in T]),3))
for a,b in[('q1','dc'),('tot','dc'),('tot','datt'),('dk','dplays'),('dk','datt')]: rep(a,b)
def bk(xn,yn,cuts):
    for lo,hi in cuts:
        g=[t[yn] for t in T if lo<=t[xn]<=hi]; print(f"  {xn} {lo}-{hi}: n={len(g)} mean {yn}={st.mean(g):+.2f}")
bk('q1','dc',[(0,0),(1,1),(2,9)]);bk('tot','dc',[(0,2),(3,4),(5,6),(7,99)]);bk('tot','datt',[(0,2),(3,4),(5,6),(7,99)]);bk('dk','dplays',[(0,0),(1,1),(2,2),(3,99)]);bk('dk','datt',[(0,0),(1,1),(2,2),(3,99)])
print('LAR',[t for t in T if t['team']=='LAR'][-1])
