import pandas as pd, json
ab=json.load(open('abbr.json'))
inv=pd.read_csv('test_d_nopass_gamelines/gameline_inventory.csv')
def code(full):
    a,h=full.split('@'); return f"{ab[a]}@{ab[h]}"
inv['g']=inv.game.map(code)
inv['day']=pd.to_datetime(inv.commence_utc).dt.tz_convert('America/New_York').dt.date
g2d=dict(zip(inv.g,inv.day))
L=pd.read_csv('graded_legs.csv')
L['g']=L.game
key={}
for r in L.itertuples(): key[(r.week,r.player)]=r.g
s=pd.read_csv('test_d_nopass_gamelines/slips_graded.csv')
s=s[s.pool=='combined'].copy()
s['order']=range(len(s))
def sday(r):
    ds=[]
    for leg in r.legs.split(' | '):
        if leg.startswith('CHI@SEA') or leg.startswith('GAME'): ds.append(g2d.get('CHI@SEA')); continue
        best=None
        for (w,p),gm in key.items():
            if w==r.week and leg.startswith(p+' '):
                if best is None or len(p)>len(best[0]): best=(p,gm)
        ds.append(g2d.get(best[1]) if best else None)
    ds=[d for d in ds if d is not None]
    return max(ds) if ds else None
s['day']=s.apply(sday,axis=1)
print('unmapped',s.day.isna().sum())
out=[]
for (t,m),grp in s.groupby(['test','method']):
    cap=grp.sort_values('order').groupby('day').head(5)
    for w,gw in cap.groupby('week'):
        out.append(dict(test=t,method=m,week=w,days=gw.day.nunique(),slips=len(gw),won=(gw.outcome=='win').sum(),lost=(gw.outcome=='loss').sum(),pl=round(gw.profit.sum(),2)))
    out.append(dict(test=t,method=m,week='ALL',days=cap.day.nunique(),slips=len(cap),won=(cap.outcome=='win').sum(),lost=(cap.outcome=='loss').sum(),pl=round(cap.profit.sum(),2)))
o=pd.DataFrame(out); print(o.to_string()); o.to_csv('test_d_nopass_gamelines/cap5_per_day.csv',index=False)
print(s.outcome.value_counts())
