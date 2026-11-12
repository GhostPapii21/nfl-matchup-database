import sys,json,datetime
sys.argv=['x']
exec(open('/workspace/nfl-database/backtests/ol_dl_gap/bt_gap.py').read().split('def factor')[0])
exec('def factor'+open('/workspace/nfl-database/backtests/ol_dl_gap/bt_gap.py').read().split('def factor')[1].split('\nGS=')[0])
T=['KC','DEN','DET','MIN','TB','ATL','CIN','TEN']
out={}
for W in (8,9):
    a=factor(W); r=R[R.week<W]
    raw=r.groupby('posteam').agg(ypc=('ry','mean'),succ=('success','mean'),stuff=('stuff','mean'),n=('ry','size'))
    rd=r.groupby('defteam').agg(ypc_allowed=('ry','mean'),n=('ry','size'))
    out[f'thru_wk{W-1}']={t:dict(off_run_pct=round(a['off'][t],1),def_run_pct=round(a['def'][t],1),off_rank=int((a['off']>a['off'][t]).sum()+1),
      rb_ypc=round(raw.ypc[t],2),rb_success=round(raw.succ[t],3),rb_stuff=round(raw.stuff[t],3),rb_carries=int(raw.n[t]),def_rb_ypc_allowed=round(rd.ypc_allowed[t],2)) for t in T}
out['source']='own nflverse pbp via backtests/ol_dl_gap factor() (opponent-adjusted composite of success, stuff, YPC on RB carries); no ALY in our data'
out['pulled']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M ET')
json.dump(out,open('own_ol_run_blocking.json','w'),indent=1); print(json.dumps(out['thru_wk8'],indent=0)[:1500])
