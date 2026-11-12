import pandas as pd, csv, re, json
S='/workspace/nfl-database/runs/2026-11-01_shared_src/'
p=pd.read_parquet(S+'play_by_play_2026.parquet',columns=['game_id','week','posteam','receiver_player_name','rusher_player_name','pass_attempt','complete_pass','receiving_yards','rushing_yards','rush_attempt','season_type','receiver_player_id','rusher_player_id'])
p=p[p.season_type=='REG']
pl=pd.read_parquet(S+'players.parquet')
namecol=[c for c in pl.columns if c in('display_name','full_name','football_name')][0]
idcol='gsis_id' if 'gsis_id' in pl.columns else pl.columns[0]
idmap=dict(zip(pl[idcol],pl[namecol]))
rec=p[p.pass_attempt==1].groupby(['receiver_player_id','week','posteam']).agg(tgt=('pass_attempt','sum'),rec=('complete_pass','sum'),ry=('receiving_yards','sum')).reset_index().rename(columns={'receiver_player_id':'pid'})
ru=p[p.rush_attempt==1].groupby(['rusher_player_id','week','posteam']).agg(car=('rush_attempt','sum'),rush=('rushing_yards','sum')).reset_index().rename(columns={'rusher_player_id':'pid'})
g=pd.merge(rec,ru,on=['pid','week','posteam'],how='outer').fillna(0)
g['rr']=g.ry+g.rush; g['name']=g.pid.map(idmap)
team_weeks={t:sorted(p[p.posteam==t].week.unique()) for t in p.posteam.dropna().unique()}
fd=list(csv.DictReader(open('fd_now.csv')))
def imp(a): a=float(a); return 100/(a+100) if a>0 else -a/(-a+100)
# main lines
mains={}
for r in fd:
  m=re.match(r'(.+) - (Receiving Yds|Total Receptions|Rushing Yds|Rush \+ Rec Yds|Rushing \+ Receiving Yds)$',r['market'])
  if m and r['odds']:
    k=(m.group(1),m.group(2)); side='o' if ' Over' in r['runner'] else 'u'
    mains.setdefault(k,{})[side]=(float(r['hcp'] or 0),int(r['odds']),r['game'])
statmap={'Receiving Yds':'ry','Total Receptions':'rec','Rushing Yds':'rush','Rush + Rec Yds':'rr','Rushing + Receiving Yds':'rr'}
altmap={'Alt Receiving Yds':'Receiving Yds','Alt Receptions':'Total Receptions','Alt Rushing Yds':'Rushing Yds','Alt Rush + Rec Yds':'Rush + Rec Yds'}
out=[]
for r in fd:
  m=re.match(r'(.+) - (Alt Receiving Yds|Alt Receptions|Alt Rushing Yds|Alt Rush \+ Rec Yds)$',r['market'])
  if not m or not r['odds']: continue
  pn,mk=m.group(1),m.group(2); o=int(r['odds'])
  if o< -280 or o>150: continue
  n=re.search(r'(\d+)\+',r['runner']); 
  if not n: continue
  line=int(n.group(1))-0.5; base=altmap[mk]; st=statmap[base]
  mn=mains.get((pn,base)) or mains.get((pn,'Rushing + Receiving Yds' if base=='Rush + Rec Yds' else base))
  ov=(imp(mn['o'][1])+imp(mn['u'][1])) if mn and 'o' in mn and 'u' in mn else 1.045
  gp=g[g.name==pn]
  if gp.empty: continue
  t=gp.posteam.iloc[-1]; tw=team_weeks[t]; last4=tw[-4:]
  vals=[float(gp[gp.week==w][st].sum()) if w in set(gp.week) else None for w in last4]
  played=[v for v in vals if v is not None]
  allv=gp.sort_values('week')[st].tolist()
  hits4=sum(v>line for v in played); seas=sum(v>line for v in allv)
  tg=gp.sort_values('week').tgt.tolist()[-4:]
  out.append(dict(player=pn,team=t,game=r['game'],stat=st,line=line,odds=o,nv=round(imp(o)/ov,3),l4=vals,hits4=f'{hits4}/{len(played)}',season=f'{seas}/{len(allv)}',tgt4=tg,med4=(sorted(played)[len(played)//2] if played else None)))
df=pd.DataFrame(out)
df.to_csv('scan_all.csv',index=False)
ex=['Lamb','Bowers','Walker','St. Brown','Higgins','Flowers','Parker Washington']
badteam={'CIN','LV','BAL','JAX','DAL'}
f=df[(~df.player.str.contains('|'.join(ex)))&(~df.team.isin(badteam))]
f=f[f.hits4.str.match(r'^(4/4|3/3)$')]
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
print(f.sort_values(['odds']).to_string())
