import sqlite3,json,subprocess,csv,os
c=sqlite3.connect('/workspace/nfl-database/fixes/fixes.sqlite')
P={'Tee Higgins':'CIN','Ryan Flournoy':'DAL','DK Metcalf':'PIT','Puka Nacua':'LAR','Josh Downs':'IND','Laquon Treadwell':'IND','Antonio Williams':'WSH','Brock Bowers':'LV','CeeDee Lamb':'DAL','Jahmyr Gibbs':'DET','Trey McBride':'ARI'}
games=[]
for gid,d,data in c.execute("select game_id,date,data from games where status='STATUS_FINAL' order by date desc"):
  j=json.loads(data);cs=j['competitions'][0]['competitors']
  games.append((d,j['week']['number'],j['season']['year'],{x['team']['abbreviation']:x['team']['displayName'] for x in cs},j['name']))
def official(ch,teams):
  return ch=='NFL' or ch in teams
rows=[];cache={}
def find(g):
  if g[4] in cache: return cache[g[4]]
  away,home=g[4].split(' at ')
  q=f"ytsearch10:{away} vs. {home} Game Highlights NFL {g[2]} Week {g[1]}"
  r=subprocess.run(['yt-dlp','--flat-playlist','-J',q],capture_output=True,text=True,timeout=120)
  res=None
  try:
    for e in json.loads(r.stdout)['entries']:
      ch=e.get('channel') or e.get('uploader') or ''
      if official(ch,[away,home]) and (e.get('duration') or 0)<=960 and 'highlight' in (e.get('title') or '').lower() and str(g[2]) in (e.get('title') or '')+str(g[2]):
        if home.split()[-1] in e['title'] and away.split()[-1] in e['title']:
          res=(e['url'] if e['url'].startswith('http') else 'https://www.youtube.com/watch?v='+e['id'],ch,e.get('title'),e.get('duration'));break
  except Exception as ex: res=('ERR',str(ex)[:100] or r.stderr[-200:],'','')
  cache[g[4]]=res;return res
for p,t in P.items():
  mine=[g for g in games if t in g[3]][:3]
  if p=='DK Metcalf': mine+= [g for g in games if 'CLE' in g[3] and 'PIT' in g[3]][:2]
  d=f"{p.replace(' ','_')}";os.makedirs(d,exist_ok=True)
  for g in mine:
    f=find(g);gname=f"{g[0]} wk{g[1]} {g[4]}"
    if not f or f[0]=='ERR':
      rows.append([p,gname,'','', '', 'FAILED: '+('no official NFL/team upload found in search' if not f else f[1])]);continue
    out=f"{d}/{g[0]}_{g[4].replace(' ','_')}.%(ext)s"
    r=subprocess.run(['yt-dlp','-f','b[height<=480]/bv*[height<=480]+ba/w','-o',out,f[0]],capture_output=True,text=True,timeout=600)
    path=[x for x in os.listdir(d) if x.startswith(f"{g[0]}_{g[4].replace(' ','_')}")]
    rows.append([p,gname,f[0],f[1],os.path.abspath(d+'/'+path[0]) if path else '', 'ok' if path and r.returncode==0 else 'FAILED: '+r.stderr.strip().splitlines()[-1][:200] if r.stderr.strip() else 'FAILED'])
    print(rows[-1],flush=True)
w=csv.writer(open('manifest.csv','w'));w.writerow(['player','game','video_url','channel','local_path','status']);w.writerows(rows)
