import sys; sys.path.insert(0,'/workspace/nfl-database/tools'); sys.path.insert(0,'/tmp')
import pandas as pd, scan_data, slate_scan as new, slate_scan_old as old
data=scan_data.load(); pg=data[0]; out=[]
for w in range(3,9):
    a=old.scan_week(w,data); b=new.scan_week(w,data)
    ka=set(a[a.market=='ryds'].pid); nb=b[(b.market=='ryds')&~b.pid.isin(ka)]
    for _,r in nb.iterrows():
        act=pg[(pg.week==w)&(pg.pid==r.pid)]; ry=act.ryds.sum()
        out.append(dict(week=w,team=r.team,name=r['name'],role=r.role,trigger=r.trigger,line=r.line,car=act.car.sum(),ryds=ry,hit=ry>r.line,rank=r['rank'],n=len(b)))
    if w==8:
        print(b[b.pid=='00-0040878'][['market','role','trigger','line','rank','score']].to_string(),'new n',len(b),'old n',len(a))
        print(a[a.pid=='00-0040878'][['market','rank']].to_string())
d=pd.DataFrame(out);d.to_csv('/workspace/nfl-database/backtests/scan_press/rb_rush_missing_wk3_8.csv',index=False)
print(len(d),'missing; hits',int(d.hit.sum()));print(d.trigger.value_counts().to_string());print(d.groupby('week').size().to_string());print(d.sort_values('ryds',ascending=False).head(10).to_string())
