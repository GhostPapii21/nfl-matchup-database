"""Phase 15 (inactives + reprice) for 1 PM ET games, run 2026-11-01 11:35-11:45 ET. Appends Phase 15 rows; refreshes odds/injury source stamps."""
import json,csv,os,re
R='/workspace/nfl-database/runs'; S=R+'/2026-11-01_shared_src'; T='2026-11-01 11:37'; TO='2026-11-01 11:35'
inj=json.load(open('/workspace/nfl-database/week8/inactives/espn_inj_20261101_1137.json'))
OUT=set()
for t in inj.get('injuries',[]):
  for i in t.get('injuries',[]):
    if i.get('status') in ('Out','Injured Reserve','Suspension'): OUT.add(i['athlete']['displayName'])
for n in ['Dee Alford','Spencer Brown','Breece Hall','David Bailey','Nahshon Wright','Tim Patrick']: OUT.add(n)
REPORTER_ACTIVE={'George Pickens':'ACTIVE (Q; Rapoport/Schefter on X 11:3x ET)','Calvin Ridley':'ACTIVE (Q; reporters on X)','Kenny Gainwell':'ACTIVE (Q; reporters on X)',
 'Jakobi Meyers':'ACTIVE (Q; reporters on X)','DJ Moore':'ACTIVE (Q; reporters on X)','Dalton Kincaid':'ACTIVE (Q; reporters on X)','Jonathan Taylor':'ACTIVE (reporters on X)'}
r6=json.load(open(S+'/rescore_v6_i1135.json'))
MOVES={'CeeDee Lamb':'FD rec yds 80.5->86.5, 50+ alt -490->-650, 60+ -300->-360; rec 6.5 -106->-118 (moved toward over)',
 'Zay Flowers':'FD rec yds 87.5->89.5, 50+ -600->-670, 60+ -350->-400; BUF nickel CB Dee Alford + S Kilgore INACTIVE (helped)',
 'Tee Higgins':'FD rec yds 70.5->69.5, 50+ -300->-275; CIN spread -12.5->-13.5, total 46.5->45.5 (blowout risk up, slightly hurt)',
 'Parker Washington':'FD rec yds 67.5->69.5, 40+ -440->-470; JAX WR Meyers (Q) ACTIVE takes targets (mild hurt)',
 'Bijan Robinson':'FD rec 3.5 -148->-188 (moved toward over); v6 sim P(4+) only ~0.43, model leans under',
 'Jaylen Warren':'FD rush+rec 91.5 (-113->-115), PP 90.5->92.5; Dowdle snap share rising 0%->27%->44% wk5-7',
 'Brock Bowers':'unchanged 68.5; NYJ CB Nahshon Wright + EDGE David Bailey INACTIVE (helped)',
 'James Cook':'FD rush+rec 97.5->98.5; BUF RT Spencer Brown INACTIVE (Grable starts) slight hurt',
 'Jahmyr Gibbs':'FD rec 4.5 +118->+124 (moved toward under)','Chris Godwin Jr.':'FD rec 4.5 +100->-106, 4+ alt -225->-215; TB WR Egbuka OUT (more volume); v6 MC/bias P(4+) 0.54, GR 0.44 vs -215 (68% implied) weak',
 'George Pickens':'ACTIVE; FD rec 4.5 -110 unchanged, 4+ alt -250->-260','Drake London':'FD rec 6.5 +104 unchanged; ATL +2.5->+1.5',
 'Amon-Ra St. Brown':'unchanged (rec 6.5 -154, yds 77.5)','Denzel Boston':'unchanged FD 47.5 / PP 49.5'}
ONEPM={'BUF','BAL','TEN','CIN','ARI','DAL','MIN','DET','LV','NYJ','CLE','PIT','ATL','TB','IND','JAX'}
def p_of(player,mkt_hint):
  for k,v in r6.items():
    if k.startswith(player.split(' Jr.')[0]) and 'sims' in v and k.endswith(mkt_hint): return v
def status_for(player):
  if player in REPORTER_ACTIVE: return REPORTER_ACTIVE[player]
  return 'INACTIVE' if player in OUT else 'ACTIVE (not on ESPN Out list / not on team inactives)'
for g in ['ARI@DAL','ATL@TB','BAL@BUF','CLE@PIT','IND@JAX','LV@NYJ','MIN@DET','TEN@CIN','DFS_SLIPS','FD7_REPLACEMENTS']:
  d=f'{R}/2026-11-01_{g}'; mp=d+'/run_manifest.json'; m=json.load(open(mp))
  old={}
  for line in open(d+'/checklist.md'):
    c=[x.strip() for x in line.strip().strip('|').split('|')]
    if len(c)>=6 and re.match(r'^15',c[1]): old[c[0]]=c[2]
  rows=[]
  for l in m['legs']:
    pl=l.get('player') or ' '.join(l['name'].split()[:2]); tm=l.get('team','')
    if g in('DFS_SLIPS','FD7_REPLACEMENTS') and tm not in ONEPM: continue
    st=status_for(pl); prev=old.get(l['name'],'PASS').upper()
    new='CUT' if (st=='INACTIVE' and prev=='PASS') else prev
    if new=='CUT': l['status']='CUT'; l.setdefault('cut_reasons',[]).append('P15 11:37 inactive')
    mv=MOVES.get(pl,'no material line move (<0.5 / <20c) at 11:35 Odds API re-pull')
    rows.append(f"| {l['name']} | 15 Inactives | {new} | 11:37 ET: {pl} {st}; {mv} | ESPN injuries API + ESPN game summary + X reporters + The Odds API 11:35 (FanDuel/PrizePicks/Underdog) | {T} |")
  if not rows: continue
  hdr=f"\n\n## Phase 15 re-check — inactives & reprice, 1 PM ET games (run 2026-11-01 11:35–11:45 ET)\nSupersedes the 07:09 pre-inactives Phase 15 rows for the legs below. Read only; no bets placed. Re-sim: {S}/rescore_v6_i1135.json (sim_v6, 100k x3, seed 20261101).\n\n| Leg | Phase | Status | Number | Source | Pulled (ET) |\n|---|---|---|---|---|---|\n"
  open(d+'/checklist.md','a').write(hdr+'\n'.join(rows)+'\n')
  for s in m['sources']:
    if s['category']=='odds_props':
      s['pulled_et']='2026-11-01T11:35'; s['url_or_file']=S+('/lines_i1135.json' if 'spread' in s['name'] else '/odds_i1135.csv'); s['name']=re.sub(r're-pull \d\d:\d\d',"re-pull 11:35",s['name'])
      if 're-pull' not in s['name']: s['name']+=' (re-pull 11:35)'
    if s['category']=='injuries_news' and s['name']=='ESPN injuries API':
      s['pulled_et']='2026-11-01T11:37'; s['url_or_file']='/workspace/nfl-database/week8/inactives/espn_inj_20261101_1137.json'
  m['sources']=[s for s in m['sources'] if not (s['category']=='injuries_news' and s['pulled_et']<'2026-11-01T06:00')]
  if not any(s['name'].startswith('X reporters') for s in m['sources']):
    m['sources'].append(dict(category='injuries_news',name='X reporters/beat writers inactives posts (Rapoport, Schefter, team beats) via x connector',url_or_file='https://x.com/search (x connector search_posts_all)',pulled_et='2026-11-01T11:38',tool='x connector'))
    m['sources'].append(dict(category='injuries_news',name='ESPN game summary injuries (8 x 1 PM games)',url_or_file='/workspace/nfl-database/week8/inactives/',pulled_et='2026-11-01T11:37',tool='urllib'))
  json.dump(m,open(mp,'w'),indent=1)
  print(g,len(rows),'rows')
