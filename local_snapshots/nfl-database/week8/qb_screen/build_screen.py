from pathlib import Path
import json,re,sqlite3,csv,datetime
import pandas as pd
ROOT=Path('/workspace/nfl-database'); OUT=ROOT/'week8/qb_screen'
def load(p):return json.loads((ROOT/p).read_text())
def nt(t):return {'WSH':'WAS','LAR':'LA'}.get(t,t)
def fmt(x,n=1):return 'n/a' if x is None or pd.isna(x) else f'{x:.{n}f}'
p=pd.read_parquet(ROOT/'fixes/src/play_by_play_2026.parquet')
p=p[(p.season==2026)&(p.week<=7)&(p.two_point_attempt!=1)&p.play_type.isin(['pass','run','qb_spike'])].copy()
f=pd.read_parquet(ROOT/'week8/defense/raw/ftn_charting_2026.parquet')
assert not f.duplicated(['nflverse_game_id','nflverse_play_id']).any()
p=p.merge(f[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left',validate='one_to_one')
s=pd.read_parquet(ROOT/'fixes/src/stats_player_week_2026.parquet')
s=s[(s.season==2026)&(s.week<=7)]
dp=load('week8/defense/defense_profiles.json');D=dp['teams'];games=dp['games']
e=load('week8/qb_screen/monday_scoreboard.json')['events'][0];o=e['competitions'][0]['odds'][0]
games.append(dict(id=e['id'],away='CHI',home='SEA',odds=[o['details'],o['overUnder']],date=e['date']))
depth={}
for t,b in re.findall(r'### (\w+)\n(.*?)(?=\n### |\n## |\Z)',(ROOT/'week8/depth_charts_offense.md').read_text(),re.S):
 depth[t]={l.split('|')[1]:dict(name=l.split('|')[2],status=l.split('|')[3],role=l.split('|')[4]) for l in b.splitlines() if l.startswith('|') and len(l.split('|'))>=6 and l.split('|')[1] not in ['Slot','-']}
# ESPN repo box scores and PBP are accessed strictly read-only.
c=sqlite3.connect('file:'+str(ROOT/'repo/data/nfl_matchups.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
teamid={};gamemap={}
for row in c.execute('select game_id,data from games'):
 g=json.loads(row['data']);gamemap[row['game_id']]=g
 for co in g['competitions'][0]['competitors']:teamid[co['team']['id']]=co['team']['abbreviation']
box={}
for row in c.execute("select * from player_stats where category='passing'"):
 if row['game_id'] not in gamemap or gamemap[row['game_id']].get('week',{}).get('number',99)>7:continue
 key=(teamid.get(row['team'],row['team']),row['player']);x=json.loads(row['data']);ca=x.get('completions/passingAttempts','').split('/')
 if len(ca)!=2:continue
 box.setdefault(key,[]).append(dict(game=row['game_id'],c=int(ca[0]),a=int(ca[1]),s=int(x.get('sacks-sackYardsLost','0-0').split('-')[0])))
repo_plays=[]
for row in c.execute('select * from plays'):
 if row['game_id'] not in gamemap or gamemap[row['game_id']].get('week',{}).get('number',99)>7:continue
 d=json.loads(row['data']);text=d.get('text','');repo_plays.append(dict(game=row['game_id'],team=teamid.get(row['offense_id']),down=row['down'],distance=row['distance'],text=text))
inj=load('week8/qb_screen/injuries_current.json');inj_by={}
for team in inj['injuries']:
 for r in team['injuries']:
  a=r['athlete'];inj_by[a['displayName']]=r
# Current feed team IDs map through scoreboard/game records.
inj_team={teamid.get(t['id'],t['displayName']):t['injuries'] for t in inj['injuries']}
props=[]
for source in ['fanduel','prizepicks']:
 with (ROOT/f'week8/lines/props_2026-10-30_{source}.csv').open() as h:props+=list(csv.DictReader(h))
outlier=ROOT/'outlier/qb_completions_2026-10-31.csv'
if outlier.exists():
 with outlier.open() as h:props+=list(csv.DictReader(h))
def split(q):
 a=q[(q.pass_attempt==1)&(q.sack!=1)];n=len(a)
 return dict(attempts=n,completions=int(a.complete_pass.sum()),comp_pct=100*a.complete_pass.sum()/n if n else None,ypa=a.passing_yards.fillna(0).sum()/n if n else None,sacks=int(q.sack.sum()),ints=int(a.interception.sum()),dropbacks=len(q))
def targets(q):
 x=q[q.receiver_player_id.notna()];counts=x.receiver_player_name.fillna('unknown').value_counts();total=len(x)
 return '; '.join(f'{k} {v}/{total} ({100*v/total:.0f}%)' for k,v in counts.head(5).items()) if total else 'n/a (no named targets in sample)'
metrics={}
for game in games:
 for team,opp in [(game['away'],game['home']),(game['home'],game['away'])]:
  name=depth[team]['QB1']['name'];ss=s[(s.player_display_name==name)&(s.team==nt(team))];ids=ss.player_id.unique();q=p[(p.posteam==nt(team))&(p.passer_player_id.isin(ids)|((p.qb_scramble==1)&p.rusher_player_id.isin(ids)))];q=q[(q.qb_dropback==1)|(q.qb_spike==1)].copy();a=q[(q.pass_attempt==1)&(q.sack!=1)];g=len(ss)
  bb=box.get((team,name),[]);bc=sum(x['c'] for x in bb);ba=sum(x['a'] for x in bb);bs=sum(x['s'] for x in bb)
  ca=ss.completions.sum();aa=ss.attempts.sum();sa=ss.sacks_suffered.sum()
  audit=f'ESPN repo box {bc}/{ba}, {bs} sacks, {len(bb)} appearances; nflverse weekly {int(ca)}/{int(aa)}, {int(sa)} sacks, {g} appearances.'
  # Prefer official stored box scores; retain explicit cross-source discrepancy.
  if bb:g=len(bb);ca=bc;aa=ba;sa=bs
  chart=q[q.n_blitzers.notna()&(q.qb_dropback==1)];bl=split(chart[chart.n_blitzers>0]);pr=split(q[(q.sack==1)|(q.qb_hit==1)|(q.qb_scramble==1)])
  third=q[q.down==3];ta=third[(third.pass_attempt==1)&(third.sack!=1)];conv=int(ta.third_down_converted.sum());tcount=len(ta)
  teamplays=p[p.posteam==nt(team)];den=teamplays.third_down_converted.sum()+teamplays.third_down_failed.sum();num=teamplays.third_down_converted.sum()
  prs=q[(q.qb_hit==1)&(q.sack!=1)];long=q[(q.down==3)&(q.ydstogo>=7)]
  # Same-play hit targets and 3rd-and-long are separate, never next-play pressure labels.
  ol=[]
  for r in inj_team.get(team,[]):
   pos=r['athlete'].get('position',{}).get('abbreviation','')
   if pos in ['OT','OG','G','C','OL','T'] and r['status']!='Active':ol.append(f"{r['athlete']['displayName']} ({pos}) {r['status']}")
  lines={}
  for r in props:
   if r.get('player')==name and r.get('team',team)==team and any(k in r.get('market','').lower() for k in ['pass','completion']):
    key=r.get('source','Outlier')+' '+r.get('market','');lines.setdefault(key,set()).add(str(r.get('line','n/a')))
  lt='; '.join(k+': '+', '.join(sorted(v,key=lambda z:float(re.sub('[^0-9.]','',z) or 0))) for k,v in lines.items()) or 'n/a'
  comp_lines='; '.join(k+': '+', '.join(sorted(v)) for k,v in lines.items() if 'comp' in k.lower()) or 'n/a'
  attempt_lines='; '.join(k+': '+', '.join(sorted(v)) for k,v in lines.items() if 'att' in k.lower()) or 'n/a'
  # Repo text-only target audit, QB restricted and no nullified plays.
  qbshort=ss.player_name.iloc[0] if len(ss) else ''
  rp=[r for r in repo_plays if r['team']==team and qbshort and re.search(r'(?<!\w)'+re.escape(qbshort)+r' (?:pass|sacked|scrambles)',r['text']) and not re.search(r'No Play|NULLIFIED|TWO-POINT',r['text'],re.I)]
  def rt(rows):
   from collections import Counter
   ts=[]
   for r in rows:
    m=re.search(r'(?:intended for|to) (.*)',r['text'])
    if m:
     candidates=sorted(p.receiver_player_name.dropna().unique(),key=len,reverse=True)
     match=next((name for name in candidates if m.group(1).startswith(name) and (len(m.group(1))==len(name) or not m.group(1)[len(name)].isalpha())),None)
     if match:ts.append(match)
   co=Counter(ts);n=len(ts)
   return '; '.join(f'{k} {v}/{n}' for k,v in co.most_common(5)) if n else 'n/a'
  rlong=rt([r for r in rp if r['down']==3 and r['distance']>=7]);rhit=rt([r for r in rp if re.search(r'\[[A-Z]',r['text']) and ' pass ' in r['text']])
  metrics[team]=dict(team=team,opp=opp,qb=name,opposing_qb=depth[opp]['QB1']['name'],game_id=game['id'],spread=game['odds'][0],total=game['odds'][1],games=g,completions_pg=ca/g if g else None,attempts_pg=aa/g if g else None,comp_pct=100*ca/aa if aa else None,sacks_taken_pg=sa/g if g else None,box_audit=audit,blitz=bl,pressure_proxy=pr,chart_db=len(chart),third_conv=conv,third_att=tcount,third_pct=100*conv/tcount if tcount else None,third_sacks=int(third.sack.sum()),team_third_conv=int(num),team_third_att=int(den),team_third_pct=100*num/den if den else None,hit_targets=targets(prs),long_targets=targets(long),repo_long_targets=rlong,repo_hit_targets=rhit,repo_qb_plays=len(rp),ol='; '.join(ol) or 'No non-Active OL designation in current ESPN feed; full OL health not established.',lines=lt,completion_lines=comp_lines,attempt_lines=attempt_lines,box_game_ids=[x['game'] for x in bb])
(OUT/'computed_metrics.json').write_text(json.dumps(metrics,indent=2,default=lambda v:int(v) if hasattr(v,'item') else str(v)))
for t,m in metrics.items():
 print(t,m['qb'],'blitz',fmt(m['blitz']['comp_pct']),fmt(m['blitz']['ypa']),'s',m['blitz']['sacks'],'INT',m['blitz']['ints'],'n',m['blitz']['attempts'],'3rd',fmt(m['third_pct']),'long:',m['long_targets'],'lines',m['completion_lines'],m['attempt_lines'])
# Hand-reviewed football judgments, deliberately separate from descriptive calculations.
judgments={
'BAL':('CARE-OVER',['Zay Flowers','Mark Andrews'],'Return of Jackson restores efficient passing, but use concentrated Flowers/Andrews volume rather than assuming a high-completion game. Buffalo allows TE production and suppresses rushing efficiency.','Allen has the stronger current team passing environment; BAL may trail narrowly, but Jackson’s own strong blitz split keeps this side relevant.','Andrews is the long-yardage outlet; hit throws lean TE/RB. Flowers is the current volume role, not a proven pressure lock-on in Jackson’s small hit sample. Jackson returns from a three-game absence; Huntley’s team-level results are not his baseline.'),
'BUF':('CARE-OVER',['Khalil Shakir','Keon Coleman'],'Highest-total environment plus Baltimore’s soft WR allowance supports concentrated receiver volume. Do not treat Allen’s rushing or a favorite script as guaranteed completions.','Allen’s offense has the better season EPA/play than BAL and is favored; Jackson makes this competitive rather than an automatic blowout.','Coleman and DJ Moore lead long-yardage targets; Coleman also leads hit throws. Shakir is the current safety-valve role. Moore and Kincaid remain Questionable, so do not assign their targets away in advance.'),
'TEN':('IGNORE',["Wan'Dale Robinson",'Elic Ayomanor'],'Burrow/Cincinnati should outplay this offense; trailing alone does not repair a weak passing game, with Tate and Spears out. No receiver-volume build from Ward’s side.','Burrow has the clear efficiency and sustained-passing-volume edge; TEN is a double-digit underdog.','Tate leads historical long-yardage targets but is OUT; Spears is OUT too. Robinson/Ayomanor are the remaining receivers to monitor, without inventing redistribution. Helm/Pollard appear as short outlets; no verified new lock-on.'),
'CIN':('CARE-OVER',["Ja'Marr Chase",'Tee Higgins'],'Strong completion baseline and two established target leaders make the passing tree useful. The ten-point favorite script can shut volume down early, so avoid demanding multiple ceiling games.','Burrow’s passing baseline and team EPA/play exceed Ward’s; Cincinnati is likely to lead and outplay TEN.','Higgins and Chase are current volume roles. Chase Brown leads named hit targets and ties Higgins on long-yardage targets, so pressure does not automatically funnel every throw to the WRs.'),
'ARI':('CARE-OVER',['Trey McBride','Michael Wilson'],'Heavy attempts and completions support McBride/Wilson even while trailing. Dallas’ relatively modest blitz rate is less threatening than Brissett’s poor historical blitz efficiency suggests.','Prescott/Dallas have the stronger offense and are favored by seven; ARI can be outplayed while still sustaining concentrated receiver volume.','McBride leads long-yardage targets; Wilson leads hit throws. Those are distinct forms of opportunity. Gaines OUT/Froholdt Questionable add protection risk; cap ambitious yardage assumptions.'),
'DAL':('CARE-OVER',['CeeDee Lamb','George Pickens'],'High passing baseline and a high-total game against soft Arizona outside coverage keep the receivers central. Pickens’ status and a seven-point lead script limit confidence in aggressive volume.','Prescott has the better team offensive EPA/play than Brissett and Dallas is favored; Arizona’s passing volume can keep the game active.','Pickens/Lamb dominate long-yardage targets; Pickens leads hit targets. Pickens is Questionable; Ferguson is a contingency to review, with no assumed target transfer.'),
'MIN':('IGNORE',['Justin Jefferson','T.J. Hockenson'],'Murray’s completion volume is too small to build broad receiver overs around, and DET has the stronger passing offense. This is not enough evidence for a blanket receiver fade either.','Goff’s passing volume and Detroit’s offensive EPA/play are stronger; MIN’s unbeaten record alone does not establish passing-game superiority.','Addison leads long-yardage and ties the hit-target lead; Jefferson/Hockenson have established current roles but their opportunities must clear a volume gate. Do not presume blitz means automatic TE targets.'),
'DET':('CARE-OVER',['Amon-Ra St. Brown','Jahmyr Gibbs'],'Goff has handled blitzes efficiently despite Minnesota’s extreme blitz/pressure profile. Concentrate on St. Brown and Gibbs receiving; pressure is a risk, not sufficient evidence of a collapse.','Goff has the larger passing baseline and better team offensive EPA/play than Murray; DET is narrowly favored.','St. Brown dominates long-yardage targets and leads hit throws. LaPorta is a secondary outlet, but the phase script flags his prior two-target game despite heavy snaps; Gibbs receiving is a separate path.'),
'LV':('CARE-UNDER',['Brock Bowers','Tre Tucker'],'Jets blitz volume meets Cousins’ reduced completion rate against blitz, with an interior-OL question. Review WR efficiency fades; Bowers/Jeanty outlets can retain catches.','Geno’s completion efficiency is higher, though his sacks make the matchup close; the slight NYJ favorite does not prove a decisive QB mismatch.','Bowers/Tucker tie for the long-yardage lead; Bowers, Tucker and Jeanty split hit throws. A blitz narrative cannot justify fading every Bowers reception.'),
'NYJ':('CARE-OVER',['Garrett Wilson','Mason Taylor'],'Geno’s completion efficiency and Wilson’s target concentration support selective receiving volume against LV’s moderate rush profile. Three sacks per game and current OL issues argue against broad overs.','Geno has better completion efficiency than Cousins; teams are close in offensive EPA/play and NYJ is only a slight favorite.','Wilson leads long-yardage looks; historical hit targets are dispersed and include Sadiq. Taylor is a current TE outlet candidate, not a proven pressure lock-on; use his role/line rather than inheriting Sadiq’s targets.'),
'CLE':('CARE-UNDER',['Harold Fannin Jr.','Denzel Boston'],'Watson’s sack burden and weak third-down passing conversion meet Pittsburgh pressure in the slate’s lowest total. WR yardage/secondary volume are more vulnerable than short Fannin catches.','Rodgers has more completion volume but both teams’ offensive EPA/play are weak; PIT’s favorite status is a team/script edge, not clear QB dominance.','Fannin leads both hit and long-yardage targets. The behavior log’s single rematch sample instead shows Boston after pressure and Judkins short; preserve that distinction rather than treating every sack as a check-down.'),
'PIT':('CARE-UNDER',['DK Metcalf','Germie Bernard'],'Low-total game, repeated sacks and poor YPA against blitz limit receiver-yardage support. Cleveland pressure can end drives before trailing volume becomes productive.','Rodgers has the larger passing baseline than Watson but similar weak team offensive EPA/play; neither QB has a compelling sustained-drive advantage.','Metcalf leads hit and long-yardage throws. The behavior log’s rematch sample finds Roman Wilson/Warren after pressure; Bernard’s current role takes precedence over automatically reusing historical personnel.'),
'ATL':('CARE-UNDER',['Drake London','Kyle Pitts Sr.'],'Tampa’s heavy blitz profile meets Penix’s documented pressure problems and narrow target tree. Fade broad receiver efficiency; London can retain targets and trailing yardage, so his receptions are not an automatic under.','Mayfield has a weaker recent team EPA baseline, but TB is favored; Penix’s pressure response is the concern rather than a claim that Mayfield clearly dominates him.','Behavior log: London is the lock-on, Pitts second; Bijan had zero third-and-long targets in the examined pressure-game sample. Current season long-yardage distribution agrees on London; do not label Bijan an automatic blitz outlet.'),
'TB':('CARE-UNDER',['Chris Godwin Jr.','Cade Otton'],'Mayfield’s sacks and low blitz YPA leave a fragile passing floor; Egbuka OUT, thumb protection and Goedeke Questionable compound it. Otton/Irving catches can survive while WR yardage suffers.','Mayfield’s own completion baseline is below Penix’s; TB being narrowly favored does not establish a passing edge. Both passing games warrant pressure scrutiny.','Behavior log identifies Otton/Irving after pressure; same-play hit targets support those outlets. Egbuka led historical pressure-adjacent usage but is OUT. Godwin’s current role is relevant without assuming all vacated targets move to him.'),
'IND':('IGNORE',['Josh Downs','Tyler Warren'],'Jones’ inefficient completions and double-digit underdog script make broad receiving builds unreliable. Jacksonville has the stronger offense; extra trailing attempts are not enough.','Lawrence/JAX have the stronger team offensive EPA/play and completion efficiency; IND is likely to be outplayed.','Downs leads hit throws; Keenan Allen leads long-yardage looks. Warren has a current TE volume role, but is not the observed long-yardage leader; no automatic receiver boost from the deficit.'),
'JAX':('CARE-OVER',['Parker Washington','Brenton Strange'],'Washington’s target concentration and a better offense than IND justify selective receiving attention. Ten-point favorite script can compress attempts, so volume thresholds still matter.','Lawrence/JAX should outplay Jones/IND; a sustained lead creates second-half passing reduction risk.','Washington leads long-yardage targets; Meyers leads hit throws and is Questionable. Strange is a current TE option and tied near the long-yardage lead, not an assumed beneficiary of a Meyers absence. Harrison on IR weakens protection.'),
'LAC':('CARE-UNDER',['Ladd McConkey','Quentin Johnston'],'Herbert’s low completion baseline, heavy sacks and poor team offense create an explicit passing-collapse concern. Rams pressure plus Awosika OUT can erase receiver efficiency despite trailing attempts.','Stafford has a substantially stronger completion/attempt baseline and better team offensive EPA/play; LAC is likely to trail and be outplayed.','Historical hit/long-yardage trees involve Gadsden, Harris and Vidal; do not transfer those targets blindly to current starters. McConkey/Johnston are present-day WR review candidates, with no verified pressure concentration.'),
'LAR':('CARE-OVER',['Puka Nacua','Konata Mumpfield'],'Stafford’s substantial completion volume and a soft Chargers receiving defense support Nacua and a second receiver review. Favorite-script compression and Shelton Questionable remain constraints.','Stafford’s passing baseline and LAR offensive EPA/play clearly exceed Herbert/LAC; Rams likely lead.','Nacua leads long-yardage targets; hit throws previously split Nacua/Adams. Adams is not a current depth-chart receiver here; Mumpfield’s current slot and long-yardage usage require his own volume check. Kyren is a receiving alternative.'),
'KC':('CARE-OVER',['Travis Kelce','Rashee Rice'],'Mahomes’ strong blitz completion/YPA split provides a route through Denver pressure. Use concentrated short receiving volume; the low total limits explosive-yard expectations.','Mahomes has stronger completion efficiency and better team offensive EPA/play than Nix; KC is only narrowly favored, so a competitive game remains plausible.','Kelce/Walker tie for the long-yardage lead and Rice remains a current safety-valve role. Hit throws are dispersed; no single proven pressure lock-on. Worthy yardage needs a separate opportunity check.'),
'DEN':('CARE-UNDER',['Jaylen Waddle','Courtland Sutton'],'Nix’s very poor blitz completion/YPA split and weak third-down passing create a receiver-efficiency fade against KC’s blitz packages. Bolles Questionable adds protection downside.','Mahomes has the stronger passing efficiency and team offense; DEN can be outplayed despite a competitive spread.','Sutton leads long-yardage targets; Waddle/Engram share the small hit-target lead. Waddle is Questionable; pressure does not establish that Sutton or Engram will inherit all his usage.'),
'NE':('CARE-OVER',['A.J. Brown','Hunter Henry'],'Maye’s passing efficiency can support receivers against Miami’s modest pressure profile. Seven-point favorite script and Brown’s ankle status keep this selective.','Maye has substantially better completion efficiency than Willis and NE is favored by seven; NE likely leads.','Henry/Stevenson tie for long-yardage lead; hit targets are spread, with historical Doubs usage. Brown is a current role candidate and Questionable, not a historical pressure lock-on inferred from an old receiver tree.'),
'MIA':('IGNORE',['Malik Washington','Greg Dulcich'],'Willis has a small completion pool and a weaker passing environment than Maye; Proctor OUT adds risk. Trailing volume is insufficient to support a broad receiver build.','Maye’s completion efficiency and NE’s team offense are stronger; MIA is likely to be outplayed as a seven-point underdog.','Washington leads the small hit-target sample, while Caleb Douglas leads long-yardage targets. Dulcich is a current short option, not a verified pressure lock-on; historical Achane targets are not reassigned.'),
'PHI':('CARE-UNDER',['Makai Lemon','Dallas Goedert'],'Washington blitz volume meets McKee’s poor blitz split and a depleted WR room. Forty attempts per appearance are not enough to validate overs with Smith and Wicks OUT.','Daniels/WSH have better team offensive EPA/play; McKee’s two-appearance sample is small and PHI is a six-point underdog.','Lemon ties Smith in long-yardage targets; Smith and Wicks are OUT. Goedert is the current TE candidate but the tiny hit-target sample does not establish a new pressure funnel.'),
'WSH':('IGNORE',['Stefon Diggs','Chig Okonkwo'],'Daniels’ low completion baseline, low total and likely leading script do not support a broad receiving build. This is a volume pass, with Tunsil on IR, rather than a proven blitz-collapse fade.','Daniels/WSH have a better team offense than McKee/PHI and are favored by six, but that can reduce pass volume rather than lift receiver totals.','Diggs ties the small hit-target lead; Brown/Antonio Williams lead long-yardage throws. Okonkwo is a current TE candidate without a demonstrated pressure lock-on.'),
'CHI':('CARE-OVER',['Rome Odunze','Luther Burden III'],'Williams’ completion efficiency and strong third-down passing warrant receiver attention despite Seattle’s strong rush. Keep protection risk visible; this is a concentrated volume screen.','Williams has better current completion efficiency and CHI team offensive EPA/play than Darnold/SEA; Seattle’s home-favorite line alone does not mean CHI gets outplayed.','Odunze leads long-yardage targets; Burden leads the small hit sample. Loveland is Questionable, so his targets are not preassigned. Four Williams appearances make the baseline less stable.'),
'SEA':('CARE-UNDER',['Jaxon Smith-Njigba','AJ Barner'],'Chicago blitz volume plus Cross Doubtful/Bradford Questionable threaten a middling Darnold passing baseline. Review secondary receiver yardage fades; JSN targets and Barner outlets can survive.','Williams’ completion efficiency and CHI team offensive EPA/play are stronger; SEA is favored at home, but its passing side can be outplayed.','JSN leads long-yardage usage; Barner leads hit targets. Shaheed is Questionable, and historical Lock games are excluded from Darnold’s own splits. A pressure fade does not mean a blanket JSN reception under.')}
behavior={
'CLE':'Behavior log W4 rematch: Boston 3/8 pressure-adjacent targets; Judkins 6 catches for 42, all short. These are one-game/next-throw observations, not a season true-pressure split.',
'PIT':'Behavior log W4 rematch: Metcalf 3/9 third/fourth-down targets; Roman Wilson and Warren 3/12 each on hit throws or the next throw after pressure. Sample differs from same-play hits below.',
'ATL':'Behavior log cites a reported 22.7% completion rate under pressure (The Rundown), but its raw charting/denominator is absent: unverified contextual report, not a verified current split. Its verified PBP review identifies London/Pitts and no automatic Bijan check-down.',
'TB':'Behavior log cites reported 2026 pressure 45.8%/4.3 YPA and blitz 62.5%/7.1 YPA; raw charting is absent and the four-game reported split differs from the reproducible W1–7 blitz split here. Do not blend them; 2025 NGS numbers are historical only.'}
# Print report and a flat, analysis-ready CSV with n/a for unavailable observations.
rows=[];sections=[]
for team,m in metrics.items():
 t=nt(team);opp=nt(m['opp']);d=D[t];de=D[opp];sh=de['sharp'];v,rec,reason,comparison,tree=judgments[team]
 fav,margin=m['spread'].rsplit(' -',1);margin=float(margin);lead=fav==team
 risk='high' if margin>=10 else 'elevated' if margin>=6 else 'limited by the spread'
 script=f"{'Likely leading' if lead else 'Likely trailing'}; blowout risk {risk}. " + ('A lead can cut late attempts.' if lead else 'A deficit can add attempts but sacks/failed drives can prevent usable completions.')
 shell=('MOF open' if sh['Middle Open Rate']>sh['Middle Closed Rate'] else 'MOF closed')
 qbp=m['pressure_proxy'];bl=m['blitz']
 # Pressure proxy is computed separately; official pressure unavailable.
 qbname=m['qb'];r=inj_by.get(qbname);status=(r['status']+' — '+r.get('shortComment','')) if r else 'No current QB injury row in feed; starter per saved Friday depth chart.'
 rstatus=[]
 for receiver in rec:
  rr=next((z for k,z in inj_by.items() if k==receiver),None)
  if not rr:
   rr=next((z for k,z in inj_by.items() if k.replace(' Jr.','').replace(' Sr.','')==receiver.replace(' Jr.','').replace(' Sr.','')),None)
  rstatus.append(receiver+(' ['+rr['status']+']' if rr and rr['status']!='Active' else ''))
 df=p[p.defteam==opp];dgp=df.game_id.nunique();dspg=df.sack.sum()/dgp if dgp else None
 passing='; '.join(f'{k}: {val}' for k,val in [('completions',m['completion_lines']),('attempts',m['attempt_lines'])])
 table_rec='; '.join(rstatus)
 row=dict(qb=qbname,team=team,opponent=m['opp'],verdict=v,key_reason=reason,receiver_1=rstatus[0],receiver_2=rstatus[1],spread=m['spread'],total=m['total'],game_script=script,opposing_qb=m['opposing_qb'],opposing_qb_comparison=comparison,games=m['games'],completions_pg=fmt(m['completions_pg']),attempts_pg=fmt(m['attempts_pg']),comp_pct=fmt(m['comp_pct']),completion_lines=m['completion_lines'],attempt_lines=m['attempt_lines'],all_passing_lines=m['lines'],sacks_taken_pg=fmt(m['sacks_taken_pg']),pressure_allowed_pct=fmt(d['sharp_off_pressure_allowed_avg']),pressure_allowed_method='Sharp mean of per-game rates; team, not QB-specific',ol_injuries=m['ol'],opponent_blitz_pct=fmt(sh['Blitz Rate']),opponent_ftn_blitz_pct=fmt(de['ftn_blitz_rate']),opponent_pressure_pct='n/a',opponent_pressure_proxy_pct=fmt(de['sharp_def_pressure_rate_proxy']),opponent_sacks_pg=fmt(dspg),coverage_shell=shell,mof_open_pct=sh['Middle Open Rate'],mof_closed_pct=sh['Middle Closed Rate'],qb_blitz_comp_pct=fmt(bl['comp_pct']),qb_blitz_ypa=fmt(bl['ypa']),qb_blitz_sacks=bl['sacks'],qb_blitz_ints=bl['ints'],qb_blitz_attempts=bl['attempts'],qb_blitz_charted_dropbacks=m['chart_db'],qb_pressure_comp_pct='n/a',qb_pressure_ypa='n/a',qb_pressure_sacks='n/a',qb_pressure_ints='n/a',qb_hit_sack_scramble_proxy_comp_pct=fmt(qbp['comp_pct']),qb_hit_sack_scramble_proxy_ypa=fmt(qbp['ypa']),qb_hit_sack_scramble_proxy_sacks=qbp['sacks'],qb_hit_sack_scramble_proxy_ints=qbp['ints'],qb_hit_sack_scramble_proxy_attempts=qbp['attempts'],team_third_down_pct=fmt(m['team_third_pct']),team_third_down_conversions=m['team_third_conv'],team_third_down_opportunities=m['team_third_att'],qb_third_down_pass_conversion_pct=fmt(m['third_pct']),qb_third_down_pass_conversions=m['third_conv'],qb_third_down_pass_attempts=m['third_att'],qb_third_down_sacks=m['third_sacks'],same_play_hit_targets=m['hit_targets'],third_and_long_targets=m['long_targets'],repo_same_play_hit_targets=m['repo_hit_targets'],repo_third_and_long_targets=m['repo_long_targets'],target_interpretation=tree,behavior_log_note=behavior.get(team,'n/a — no QB-specific entry in supplied behavior log.'),qb_status=status,box_audit=m['box_audit'],sources='week8/slate.json; week8/depth_charts_offense.md; week8/qb_screen/injuries_current.json; week8/defense/defense_profiles.json; fixes/src/play_by_play_2026.parquet; fixes/src/stats_player_week_2026.parquet; week8/defense/raw/ftn_charting_2026.parquet; repo/data/nfl_matchups.sqlite (read-only); week8/lines/props_2026-10-30_*.csv; qb_behavior_log.md')
 rows.append(row)
 matchup=next(g['away']+'_at_'+g['home'] for g in games if g['id']==m['game_id'])
 links=f'[depth chart](../depth_charts_offense.md), [current injuries](injuries_current.json), [defense profiles](../defense/defense_profiles.json), [derived inputs](computed_metrics.json), [behavior log](../../qb_behavior_log.md)'
 if team not in ['CHI','SEA']:links+=f', [matchup/checklist](../checklist/{matchup}_checklist.md), [team baseline](../team_baselines/{team}.md), [player roles](../player_types/{t}.md)'
 else:links+=', [Monday scoreboard](monday_scoreboard.json)'
 pbplinks=', '.join(f'[W1–7 box/PBP {gid}](https://www.espn.com/nfl/playbyplay/_/gameId/{gid})' for gid in m['box_game_ids'])
 text=f'''## {qbname} — {team} vs {m['opp']} — {v}

**{reason}** Top receiving candidates to examine: {table_rec}. For CARE-UNDER these are fade/exception review targets; for IGNORE they are a watch list only.

- **Environment:** {m['spread']}; total {m['total']}. {script}
- **Opposing QB ({m['opposing_qb']}):** {comparison} Team offensive EPA/play: {team} {d['off_epa_play']:+.3f}, {m['opp']} {de['off_epa_play']:+.3f} (team context, includes other QBs).
- **Passing baseline:** {fmt(m['completions_pg'])} completions / {fmt(m['attempts_pg'])} attempts per appearance; {fmt(m['comp_pct'])}% completions; {m['games']} QB appearances in W1–7, including partial games. QB status: {status}
- **Known completion line(s):** {m['completion_lines']}. **Attempt line(s):** {m['attempt_lines']}. These are saved Oct 30 snapshots; goblin/demon variants are labeled, not main lines.
- **Protection:** {fmt(m['sacks_taken_pg'])} sacks taken/game by this QB; team pressure allowed {fmt(d['sharp_off_pressure_allowed_avg'])}% (Sharp average of game rates, not weighted/charted QB pressure). This week’s OL flags: {m['ol']}
- **Defense:** blitz {fmt(sh['Blitz Rate'])}% Sharp / {fmt(de['ftn_blitz_rate'])}% FTN (different charting); true pressure rate **n/a**, saved opponent-pressure proxy {fmt(de['sharp_def_pressure_rate_proxy'])}%; sacks {fmt(dspg)}/game ({dgp} games). Predominant shell **{shell}**: open {fmt(sh['Middle Open Rate'])}%, closed {fmt(sh['Middle Closed Rate'])}%; man {fmt(sh['Man Rate'])}%, zone {fmt(sh['Zone Rate'])}%. Mixed shells remain possible. Sharp WR/TE/RB YPT allowed {fmt(sh['YPT Allowed WR'])}/{fmt(sh['YPT Allowed TE'])}/{fmt(sh['YPT Allowed RB'])}.
- **QB vs blitz (W1–7, QB-specific FTN join):** {fmt(bl['comp_pct'])}% completions ({bl['completions']}/{bl['attempts']}), {fmt(bl['ypa'])} YPA; {bl['sacks']} sacks, {bl['ints']} INTs. {bl['dropbacks']} blitzed dropbacks out of {m['chart_db']} charted QB dropbacks. Blitz means FTN n_blitzers > 0.
- **QB vs true pressure:** comp% **n/a**, YPA **n/a**, sacks **n/a**, INTs **n/a** (no true hurry/pressure flag). Separately, **sack/hit/scramble proxy**: {fmt(qbp['comp_pct'])}% ({qbp['completions']}/{qbp['attempts']}), {fmt(qbp['ypa'])} YPA; {qbp['sacks']} sacks and {qbp['ints']} INTs across {qbp['dropbacks']} proxy dropbacks. This selection omits unh it hurries and is not a true pressure split.
- **Third down:** team {fmt(m['team_third_pct'])}% ({m['team_third_conv']}/{m['team_third_att']}); this QB’s passing attempts converted {fmt(m['third_pct'])}% ({m['third_conv']}/{m['third_att']}); {m['third_sacks']} additional third-down sacks excluded from that attempt denominator. This is conversion rate, not third-down completion percentage.
- **Same-play QB-hit named targets (nflverse PBP, top five):** {m['hit_targets']}. **Third-and-7+ named targets:** {m['long_targets']}. Shares use all named targets in each subset; unlisted targets form the remainder.
- **Independent stored ESPN PBP text check:** same-play bracketed-hit targets {m['repo_hit_targets']}; third-and-7+ targets {m['repo_long_targets']}. Parsed {m['repo_qb_plays']} QB pass/sack/scramble plays; ESPN naming/annotations and nflverse flags can differ.
- **Check-down / lock-on interpretation:** {tree} {behavior.get(team,'Behavior log: n/a — no entry for this QB; do not invent a tendency.')}
- **Baseline reconciliation:** {m['box_audit']}

Sources: {links}. Primary per-game evidence: {pbplinks}.
'''.replace('unh it','unhit')
 sections.append(text)
summary=['# Week 8 2026 QB screen — Sunday Nov 1 / Monday Nov 2','', '| QB | Opp | Verdict | Key reason | Top 2 receiving candidates |','|---|---|---|---|---|']
for r in rows:summary.append(f"| {r['qb']} ({r['team']}) | {r['opponent']} | {r['verdict']} | {r['key_reason']} | {r['receiver_1']}; {r['receiver_2']} |")
method='''
Scope: all **26 projected starting QBs**, 12 Sunday games plus CHI@SEA Monday; CAR@GB excluded. Built Oct 31, 2026. The saved Sunday slate has 24 QBs; Monday was added from the [ESPN Nov 2 scoreboard](https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261102), saved [here](monday_scoreboard.json). [NFL Monday schedule](https://www.nfl.com/schedules/2026/prime-time/monday-night-football) independently confirms the matchup. Starter identities come from the [Friday offensive depth chart](../depth_charts_offense.md), with current ESPN injuries superseding early-week injury labels. This is a receiver opportunity/fade screen, not a pass-completions bet or a priced receiver recommendation.

**Reading the verdicts.** CARE-OVER means investigate concentrated receiver receptions/yards volume; it does not endorse every receiver over. CARE-UNDER means investigate passing failure and receiver efficiency fades, preserving primary-target/check-down exceptions. IGNORE means no compelling receiver build/fade from the available passing evidence. Outplayed is a football judgment supported by the opponent QB baseline, team EPA and spread; it is not mechanically assigned to every underdog. Leading/trailing and blowout reads are descriptive, not simulated probabilities. No model percentiles or fabricated projections are supplied.

**Data and denominators.** Baselines cover 2026 regular-season W1–7. QB per-game averages divide totals by passing appearances, including injury-shortened/relief games; they are not full-start forecasts. Stored ESPN box totals reconcile with nflverse weekly totals for every starter. Team pressure allowed, team EPA, shell and defensive rates include all QBs/opponents in the team sample. Blitz splits use QB identity, valid pass/run dropbacks, FTN n_blitzers > 0; attempts exclude sacks, sacks/INTs are total counts, and YPA uses gross passing yards. No-play penalties and two-point tries are excluded by the valid-play filter. Official QB attempts include spikes; charted blitz dropbacks exclude spikes. Third-and-long means third-and-7+; team third-down denominator uses converted + failed flags, while QB passing conversion uses official pass attempts and reports sacks separately. Historical targets include players no longer in the current role/depth chart and are never silently reassigned.

**Pressure limits.** No loaded source charts every hurry/pressure. True pressure splits/rates are n/a. Sack/hit/scramble and same-play hit targets are explicitly labeled proxies; sack plays cannot themselves identify a target, and hit throws cannot prove a check-down/progression. The behavior log sometimes includes the next throw after pressure, a different denominator. Its externally reported Penix/Mayfield pressure percentages lack underlying charting, so remain contextual, unverified reports. The saved defensive pressure proxy is an unweighted average of opponents’ Sharp pressure-allowed game rates, not a measured hurry rate. Coverage percentages do not necessarily sum to 100; the higher MOFO/MOFC rate is a tendency, not a prediction of every snap.

**Lines.** The requested `outlier/qb_completions_2026-10-31.csv` is absent. Known completions/attempts come from saved [PrizePicks](../lines/props_2026-10-30_prizepicks.csv) and [FanDuel](../lines/props_2026-10-30_fanduel.csv) CSVs (Oct 30 01:26 ET). Only six QBs have completion/attempt lines in those files; others are n/a. A goblin/demon threshold is not a standard main line. Other known passing markets are retained in CSV `all_passing_lines`; no yardage line is relabeled as completions. No live prop availability is asserted.

**Source hierarchy and freshness.**

- [Sunday slate](../slate.json), [defensive profiles](../defense/defense_profiles.json), [defense source timestamps/methods](../defense/SOURCES.md), [checklists](../checklist/summary.json), [team baselines](../team_baselines/), [player types](../player_types/player_types.json), [early-week injuries](../injuries.md), [Friday depth charts](../depth_charts_offense.md), [QB behavior](../../qb_behavior_log.md), and [opportunity/pressure rules](../../PHASE_SCRIPT.md). Team baselines are W1–6 contextual notes; calculated baselines here extend through W7. Sunday spreads/totals retain the saved Oct 29 snapshot; Monday odds are from the current scoreboard.
- Current [ESPN injury API](https://site.api.espn.com/apis/site/v2/sports/football/nfl/injuries), feed timestamp 2026-10-31T11:21:50Z, saved in [injuries_current.json](injuries_current.json). Active rows are not treated as absences; no listed OL flag does not prove a healthy starting five. Monday is still before final Saturday designations. [CHI depth](https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/CHI/depthcharts) and [SEA depth](https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/SEA/depthcharts) were also fetched and saved here.
- Read-only [ESPN repo PBP/boxes](../../repo/data/nfl_matchups.sqlite); per-game public ESPN links appear in each section. Reproducible W1–7 PBP/weekly aggregation uses [nflverse PBP](../../fixes/src/play_by_play_2026.parquet), [weekly player stats](../../fixes/src/stats_player_week_2026.parquet), and [FTN charting](../defense/raw/ftn_charting_2026.parquet). Primary public releases: [PBP](https://github.com/nflverse/nflverse-data/releases/tag/pbp), [player stats](https://github.com/nflverse/nflverse-data/releases/tag/player_stats), [FTN](https://github.com/nflverse/nflverse-data/releases/tag/ftn_charting). Stored ESPN target counts cross-check the independent nflverse subsets rather than replacing missing true-pressure charting.
- Sharp saved coverage/tendency pages dated Oct 20: [schemes](https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/), [defensive tendencies](https://www.sharpfootballanalysis.com/stats-nfl/nfl-defensive-tendencies/), [position allowances](https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-stats-by-position/). These are saved snapshots, not freshly charted Week 8 rates. Sharp advanced pressure observations in the repo were updated through Oct 27. No PFF data used. [Saved NGS passing](../defense/raw/ngs_passing.parquet) supplies context in defense reports but does not supply true-pressure splits.

Reproduce with `python3 week8/qb_screen/build_screen.py` from the workspace. Computed underlying counts are in [computed_metrics.json](computed_metrics.json). All source databases/files were read-only; output is confined to this directory.
'''
(OUT/'QB_SCREEN.md').write_text('\n'.join(summary)+'\n'+method+'\n'+'\n'.join(sections))
with (OUT/'qb_screen.csv').open('w',newline='') as h:
 writer=csv.DictWriter(h,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print('Wrote',len(rows),'QB sections and CSV rows')
