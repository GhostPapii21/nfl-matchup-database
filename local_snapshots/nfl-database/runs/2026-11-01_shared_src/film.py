"""Phase 10 re-verification vs FRESH pbp (07:09 ET). Each 'verified vs DB' caption play in week8/film/*_film.md is re-matched:
same nflverse game (week + teams), player surname in pbp desc, yards == pbp yards_gained. Writes film_verified.json."""
import re,glob,json,pandas as pd,os
SH=os.path.dirname(os.path.abspath(__file__))+'/'
NVC={'LAR':'LA','WSH':'WAS','ARZ':'ARI','JAC':'JAX'}
p=pd.read_parquet(SH+'play_by_play_2026.parquet')
gids=set(p.game_id)
out={}; stats=dict(rows=0,cand=0,matched=0,nogame=0)
for f in sorted(glob.glob('/workspace/nfl-database/week8/film/*_film.md')):
    team=os.path.basename(f).split('_')[0]; wk=None; url=None; gid=None
    for line in open(f,encoding='utf-8'):
        m=re.match(r'## Week (\d+): (\w+) \d+ - (\w+) \d+ \(game (\d+)\)',line)
        if m:
            wk=int(m.group(1)); a,h=NVC.get(m.group(2),m.group(2)),NVC.get(m.group(3),m.group(3)); gid=f'2026_{wk:02d}_{a}_{h}'
            if gid not in gids: gid=None
            url=None; continue
        m=re.search(r'(https://www\.youtube\.com/watch\?v=[\w-]+)',line)
        if line.startswith('Video:') and m: url=m.group(1); continue
        if not line.startswith('|') or line.startswith('|ts') or line.startswith('|-'): continue
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)<10: continue
        stats['rows']+=1
        if 'verified vs DB' not in c[9] or c[9].startswith('unverified'): continue
        stats['cand']+=1
        if gid is None: stats['nogame']+=1; continue
        player=c[2]; sur=player.split()[-1] if player else ''
        if sur in('Jr.','II','III'): sur=player.split()[-2]
        try: yds=int(float(c[4]))
        except: continue
        g=p[(p.game_id==gid)&(p.desc.fillna('').str.contains(re.escape(sur)))&(p.yards_gained==yds)]
        if len(g):
            r=g.iloc[0]; stats['matched']+=1
            out.setdefault(player,[]).append(dict(team=team,week=wk,game_id=gid,url=url,ts=c[0],play=c[3][:90],yds=yds,pbp_play_id=int(r.play_id),qtr=int(r.qtr),clock=r.time,desc=r.desc[:120]))
json.dump(out,open(SH+'film_verified.json','w'),indent=0)
print(stats,len(out)); print({k:len(v) for k,v in list(out.items())[:15]})
