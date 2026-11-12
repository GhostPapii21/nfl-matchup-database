# Builds week8/team_baselines/<TEAM>.md from user DB (read-only) + fixes overlay. Weeks 1-6 plays; usage from overlay.
import sqlite3,json,ast,re,collections,datetime
R=sqlite3.connect('file:repo/data/nfl_matchups.sqlite?mode=ro',uri=True);F=sqlite3.connect('file:fixes/fixes.sqlite?mode=ro',uri=True)
slate=json.load(open('week8/slate.json'))['games']
teams=[a for g in slate for a in g['matchup'].split(' @ ')]
L=lambda s: ast.literal_eval(s) if isinstance(s,str) and s[:1] in '{[' else s
games={};tid={}
for gid,data in R.execute('select game_id,data from games'):
  d=json.loads(data);wk=d['week']['number']
  if d['season']['type']!=2 or wk>6: continue
  comp=d['competitions'][0];ab={x['team']['id']:x['team']['abbreviation'] for x in comp['competitors']}
  for k,v in ab.items(): tid[v]=k
  hl=(comp.get('headlines') or [{}])[0]
  games[gid]=dict(week=wk,name=d['shortName'],ab=ab,score={ab[x['team']['id']]:x.get('score') for x in comp['competitors']},recap=hl.get('shortLinkText'),recapd=hl.get('description'),url=f"https://www.espn.com/nfl/recap?gameId={gid}")
plays=collections.defaultdict(list)
for gid,pid,off,pt,yds,data in R.execute('select game_id,play_id,offense_id,play_type,yards,data from plays'):
  if gid in games: plays[gid].append((off,pt,yds,json.loads(data)))
def opp(g,t): return [a for a in g['ab'].values() if a!=t][0]
for T in teams:
  t=tid.get(T);gl=sorted([g for g,v in games.items() if T in v['ab'].values()],key=lambda g:games[g]['week'])
  o=[f"# {T} — Weeks 1–6 baseline (Phase 8 text substitute; no video watched)\n",f"Built {datetime.datetime.now().isoformat(timespec='minutes')} ET from user DB plays (ESPN PBP, read-only) + fixes overlay. Sources: ESPN recap/PBP URLs per game below; nflverse pbp/participation via overlay.\n",
     "Gaps (whole file): personnel groupings (11/12/21) and coverage/scheme from film not in any loaded source; snap counts from nflverse participation only; defender 'beaten' attribution = only where PBP names a defender on a big play allowed (tackler ≠ coverage defender) — treat as weak signal.\n","## Games\n"]
  for g in gl:
    v=games[g];o.append(f"- W{v['week']} {v['name']} {v['score']} — {v['recap'] or 'recap headline gap'} ({v['url']}; PBP https://www.espn.com/nfl/playbyplay/_/gameId/{g})\n")
  sc=[];big=[];bigA=[];rz=collections.Counter();rzt=collections.Counter();conc=collections.Counter();defn=collections.Counter()
  for g in gl:
    wk=games[g]['week']
    for off,pt,yds,d in plays[g]:
      txt=re.sub(r"^\S+ reported in as eligible\.\s*",'',d.get('text',''));st=L(d.get('start','{}')) or {}
      if off==t:
        if str(d.get('scoringPlay'))=='True' and pt not in('Kickoff',): sc.append(f"W{wk} {pt}: {txt[:160]}")
        if pt in('Pass Reception','Passing Touchdown') and yds and yds>=20: big.append(f"W{wk} PASS {int(yds)}: {txt[:150]}")
        if pt in('Rush','Rushing Touchdown') and yds and yds>=15: big.append(f"W{wk} RUSH {int(yds)}: {txt[:150]}")
        m=re.search(r'pass (?:short|deep|incomplete short|incomplete deep|incomplete)?\s*(left|middle|right)?',txt)
        dm=re.search(r'pass (?:incomplete )?(short|deep) (left|middle|right)',txt)
        if dm and pt in('Pass Reception','Passing Touchdown'): conc[f"pass {dm.group(1)} {dm.group(2)} (completed)"]+=1
        rm=re.search(r'(left end|left tackle|left guard|up the middle|right guard|right tackle|right end)',txt)
        if rm and pt in('Rush','Rushing Touchdown') and yds and yds>=4: conc[f"run {rm.group(1)} (4+ yds)"]+=1
        ytz=st.get('yardsToEndzone') if isinstance(st,dict) else None
        if ytz and ytz<=20 and pt in('Rush','Rushing Touchdown','Pass Reception','Pass Incompletion','Passing Touchdown'):
          who=re.search(r'(?:to|^)\s*([A-Z]\.[A-Za-z\'\-]+(?:\.\s?[A-Z][a-z]+)?)',txt[ txt.find(' to ') if ' pass ' in txt else 0:]) if ' pass ' in txt else re.match(r'(?:\(.*?\)\s*)?(?:\S+\s+)?([A-Z]\.[A-Za-z\'\-]+(?:\.\s?[A-Z][a-z]+)?)',re.sub(r'^\(.*?\)\s*','',txt))
          k=('tgt ' if ' pass ' in txt else 'carry ')+(who.group(1) if who else '?');rz[k]+=1
          if 'TOUCHDOWN' in txt: rzt[k]+=1
      elif off and off!=t and pt in('Pass Reception','Passing Touchdown','Rush','Rushing Touchdown') and yds and yds>=20:
        bigA.append(f"W{wk} {pt} {int(yds)}: {txt[:150]}")
        for n in re.findall(r'\(([^)]*)\)',txt)[-1:]:
          for x in n.split(';'): defn[x.strip()]+=1
  o.append(f"\n## Scoring plays ({len(sc)})\n"+''.join(f"- {x}\n" for x in sc))
  o.append(f"\n## Big plays — pass 20+ / rush 15+ ({len(big)})\n"+''.join(f"- {x}\n" for x in big))
  o.append("\n## Successful concepts (PBP direction proxies, W1–6 count)\n"+''.join(f"- {k}: {n}\n" for k,n in conc.most_common(10)))
  o.append("\n## Red-zone usage (inside 20, W1–6; parsed from PBP text — verify)\n"+''.join(f"- {k}: {n} opps, {rzt[k]} TD\n" for k,n in rz.most_common(12)))
  o.append("\n## Who gets the work (overlay fix_player_role: season vs L3 played games; through latest synced week)\n|Player|Pos|GP|Tgt sh season|Tgt sh L3|Carry sh season|Carry sh L3|Snap% L3|Tgt/g|Car/g|Last wk|\n|-|-|-|-|-|-|-|-|-|-|-|\n")
  for r in F.execute("select player,position,games_played,season_target_share,current_target_share_l3,season_carry_share,current_carry_share_l3,current_snap_pct_l3,targets_per_game,carries_per_game,last_played_week from fix_player_role where team=? and position in('WR','TE','RB','FB','QB') and (season_target_share>0.03 or season_carry_share>0.05) order by position,season_target_share+season_carry_share desc",(T if T!='WSH' else 'WAS',)):
    P=lambda x:'gap' if x is None else f"{x*100:.0f}%"
    N=lambda x:'gap' if x is None else f"{x:.1f}"
    o.append('|'+'|'.join([r[0],r[1],str(r[2]),P(r[3]),P(r[4]),P(r[5]),P(r[6]),P(r[7]),N(r[8]),N(r[9]),str(r[10])])+'|\n')
  o.append(f"\n## Defense — opponent plays of 20+ allowed W1–6 ({len(bigA)})\n"+''.join(f"- {x}\n" for x in bigA))
  o.append("\nDefenders most often named as tackler on those plays (NOT proof of coverage responsibility):\n"+''.join(f"- {k}: {n}\n" for k,n in defn.most_common(6)))
  o.append("\n## Gaps\n- Personnel tendencies, coverage shells, players 'beaten' in coverage: not in text sources loaded (needs film/charting — PFF paid, marked missing).\n- Recap narratives limited to ESPN headline blurbs stored in DB; full recap text not fetched.\n")
  open(f'week8/team_baselines/{T}.md','w').write(''.join(o))
  print(T,len(gl),len(sc),len(big))
