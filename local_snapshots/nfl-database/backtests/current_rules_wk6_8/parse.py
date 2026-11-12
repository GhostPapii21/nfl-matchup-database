import json,glob,collections,pandas as pd,numpy as np
MK={'player_reception_yds':'recyds','player_receptions':'rec','player_rush_yds':'rushyds','player_pass_yds':'passyds'}
def imp(o): return 100/(o+100) if o>0 else -o/(-o+100)
rows=[]
for f in glob.glob('raw/*.json'):
    if f.endswith('events.json'): continue
    j=json.load(open(f)); d=j['data']; snap=j['timestamp']
    q=collections.defaultdict(dict)
    for bk in d.get('bookmakers',[]):
        for m in bk['markets']:
            if m['key'] not in MK: continue
            for o in m['outcomes']:
                q[(o['description'],MK[m['key']],o.get('point'),bk['key'])][o['name']]=o['price']
    agg=collections.defaultdict(list)
    for (pl,mk,pt,bk),v in q.items():
        if 'Over' in v and 'Under' in v: agg[(pl,mk)].append((pt,bk,v['Over'],v['Under']))
    for (pl,mk),L in agg.items():
        pts=collections.Counter(x[0] for x in L); main=max(pts,key=lambda p:(pts[p],-abs(p)))
        M=[x for x in L if x[0]==main]
        nv=np.mean([imp(o)/(imp(o)+imp(u)) for _,_,o,u in M])
        fd=[x for x in M if x[1]=='fanduel']; pick=fd[0] if fd else M[0]
        rows.append(dict(event=d['id'],home=d['home_team'],away=d['away_team'],commence=d['commence_time'],snap=snap,player=pl,market=mk,line=main,
            nv_over=nv,book=pick[1],over_price=pick[2],under_price=pick[3],n_books=len(M)))
df=pd.DataFrame(rows); df.to_csv('real_lines_wk6_8.csv',index=False)
print(len(df), df.groupby('market').size().to_dict(), df.event.nunique(), (df.book=='fanduel').mean())
