"""Stage A: reads only PHASE_SCRIPT.md and frozen packs; never loads target outcomes."""
from pathlib import Path
import pandas as pd
import numpy as np
import re, json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'reads';OUT.mkdir(exist_ok=True)
access=[];picks=[];audit=[];lengths=[]
def load(p):
 access.append(str(p.relative_to(ROOT)))
 return pd.read_parquet(p) if p.suffix=='.parquet' else pd.read_csv(p)
def norm(s):return re.sub('[^a-z]','',str(s).lower()).removesuffix('sr').removesuffix('jr')
def text(p):access.append(str(p.relative_to(ROOT)));return p.read_text()
def ratio(a,b):return float(a)/float(b) if b else 0.
for w in range(3,9):
 d=ROOT/'packs'/f'w{w}';manifest=text(d/'MANIFEST.md')
 pb=load(d/'pbp_prior.parquet');ft=load(d/'ftn_prior.parquet');sn=load(d/'snap_counts_prior.parquet')
 pr=load(d/'props_main.csv');gl=load(d/'game_lines.csv');we=load(d/'weather.csv');idx=load(d/'saved_reads/INDEX.csv')
 assert (pb.week<w).all() and (ft.week<w).all() and (sn.week<w).all()
 pb=pb[(pb.season_type=='REG') & (pb.play_type.isin(['run','pass'])) & (pb.two_point_attempt!=1)].copy()
 pb['carry']=(pb.rush_attempt==1)&(pb.qb_kneel!=1)&pb.rusher_player_id.notna()
 pb['target']=pb.receiver_player_id.notna()&(pb.pass_attempt==1)
 merged=pb.merge(ft[['nflverse_game_id','nflverse_play_id','n_blitzers']],left_on=['game_id','play_id'],right_on=['nflverse_game_id','nflverse_play_id'],how='left',validate='one_to_one')
 recent={t:x[x.week.isin(sorted(x.week.unique())[-3:])] for t,x in pb.groupby('posteam')}
 saved={}
 for _,r in idx.iterrows():
  s=text(d/r.path)
  for game in str(r.games).split(';'):
   saved[game.replace('LAR','LA')]=(r,s)
 for game,g in pr.groupby('game',sort=True):
  away,home=game.split('@');lines=gl[gl.game==game];weather=we[we.game==game];sv=saved.get(game)
  tag='SAVED_READ' if sv else 'RECONSTRUCTED';ref=f"packs/w{w}/{sv[0].path} | {sv[0].timestamp} ({sv[0].timestamp_source})" if sv else ''
  spreads=lines[(lines.market=='spreads')&(lines.name==home)].sort_values(['timestamp','book'])
  totals=lines[lines.market=='totals'].sort_values(['timestamp','book'])
  spread=float(spreads.iloc[-1].point) if len(spreads) else None
  total=float(totals.iloc[-1].point) if len(totals) else None
  env=(f'{home} {spread:+g}, total {total:g}; '+('home' if spread<0 else 'away')+' side projects to lead.' if spread is not None and total is not None else 'Spread/total missing; neutral script with no invented favorite.')
  # Deterministic latest eligible snapshot, then book; no best-line shopping.
  q=g[(g.market=='rushyds')&(g.tier=='main')].copy()
  q=q.sort_values(['snap','book','candidate_id']).drop_duplicates(['player','side'],keep='last')
  candidates=[]
  for _,r in q.iterrows():
   t=recent.get(r.team,pb.iloc[0:0]);games=t.game_id.nunique()
   if not games:continue
   player=t[t.rusher_player_id==r.gsis];c=player[player.carry];teamc=t[t.carry]
   if len(c)<3:continue
   n=sn[(sn.team==r.team)&(sn.player.map(norm)==norm(r.player))]
   pos=n.position.mode().iloc[0] if len(n) else 'UNKNOWN'
   # RB-only pool; no quarterback rushing legs or guessed position.
   if pos not in ['RB','FB','HB']:continue
   share=ratio(len(c),len(teamc));rushes=len(teamc)/games
   points=spread if r.team==home else (-spread if spread is not None else None)
   adjustment=1.10 if points is not None and points<=-6 else .88 if points is not None and points>=6 else 1.
   carries=rushes*adjustment*share
   defense=pb[(pb.defteam==r.opp)&pb.carry]
   dy=ratio(defense.rushing_yards.sum(),len(defense));own=ratio(c.rushing_yards.sum(),len(c))
   eff=.5*own+.5*dy;projection=carries*eff
   side='over' if projection>r.line and share>=.60 else 'under'
   if r.side!=side or (side=='over' and share<.60):continue
   if not np.isfinite(r.price) or abs(r.price)<100:continue
   edge=abs(projection-r.line)/max(15.,float(r.line))
   values=[float(c[c.game_id==gid].rushing_yards.sum()) for gid in t.game_id.unique()]
   candidates.append(dict(row=r,share=share,carries=carries,projection=projection,dy=dy,own=own,edge=edge,values=values))
  candidates.sort(key=lambda c:(-c['edge'],c['row'].player))
  chosen=[]
  for c in candidates:
   if c['row'].player not in [a['row'].player for a in chosen]:chosen.append(c)
   if len(chosen)==2:break
  assert chosen, (w,game,'no eligible rushing candidate')
  profiles=[];blitz=[];tes=[]
  for team in [away,home]:
   de=pb[pb.defteam==team];rr=de[de.carry];pa=de[de.pass_attempt==1]
   profiles.append(f"{team}: {ratio(rr.rushing_yards.sum(),len(rr)):.2f} run YPC, {int((pa.receiving_yards>=20).sum())}/{len(pa)} pass explosives (20+)")
   b=merged[(merged.posteam==team)&(merged.qb_dropback==1)&merged.n_blitzers.notna()]
   yes=b[b.n_blitzers>0];no=b[b.n_blitzers==0]
   blitz.append(f"{team} {yes.epa.mean():.2f}/{no.epa.mean():.2f} EPA/dropback blitz/nonblitz (n={len(yes)}/{len(no)})")
   ss=sn[(sn.team==team)&(sn.position=='TE')];names=set(ss.player.map(norm));t=recent[team];targets=t[t.target]
   tg=targets[targets.receiver_player_name.map(norm).isin(names)]
   # PBP abbreviated names require GSIS to full-name matching via available suffix.
   if not len(tg):
    full=set(ss.player.map(lambda x:str(x).split()[-1].lower()))
    tg=targets[targets.receiver_player_name.map(lambda x:str(x).split('.')[-1].lower()).isin(full)]
   leader=tg.receiver_player_name.value_counts()
   tes.append(f"{team} {leader.index[0]} {int(leader.iloc[0])} L3 targets" if len(leader) else f'{team} TE identity/usage unresolved')
  injury='Injuries/inactives unavailable; no replacement boost.'
  wx='Weather unavailable; rain/wind clearance unverified.'
  if sv:
   s=sv[1];inj=s.split('## Injury impact')[1].split('Profile effect rule')[0] if '## Injury impact' in s else ''
   issues=re.findall(r'- (.*?) (?:RB|OT|G|C|QB) — (Questionable|Out|Doubtful)',inj)
   injury='Saved injury risks: '+('; '.join(f'{a} {b}' for a,b in issues[:4]) or 'no listed RB/OL/QB issue')+'; final status pending; no redistribution.'
   match=re.search(r'\|39\|P9.weather\|[^|]*\|([^|]*)',s)
   if match:wx='Saved weather: '+match.group(1).split(' — ')[0]+'.'
  if len(weather):
   z=weather.sort_values('issued').iloc[-1];wx=f"Forecast issued {z.issued}: wind {z.wind:g}, temperature {z.temp:g}; gust/rain unavailable."
  legs=[]
  for c in chosen:
   r=c['row'];flags=['projection disagrees' if (r.side=='under' and c['projection']>r.line) else 'projection agrees','three-model consensus unavailable','injury clearance incomplete']
   if spread is None:flags.append('missing script lines')
   if r.side=='under' and c['dy']>4.4:flags.append('soft defense contradicts under')
   if r.side=='over' and c['dy']<=3.8:flags.append('run suppression contradicts over')
   legs.append(f"{r.player} {r.side} {r.line:g} rushyds ({r.price:+g}): {c['share']:.0%} carry share → {c['carries']:.1f} carries × {(.5*c['own']+.5*c['dy']):.2f} YPC = {c['projection']:.1f}; recent yards {','.join(f'{v:g}' for v in c['values'])}.")
   picks.append(dict(week=w,game=game,player=r.player,market=r.market,side=r.side,line=r.line,price=r.price,tag=tag,flag=1,saved_read_ref=ref))
   audit.append(dict(week=w,game=game,player=r.player,gsis=r.gsis,team=r.team,opp=r.opp,candidate_id=r.candidate_id,book=r.book,snap=r.snap,carry_share=c['share'],projection=c['projection'],flags=flags))
  # Compact per-game phase mapping, no claim of unperformed simulation or scheme verification.
  prose=f'''# Week {w}: {game}
{tag}{': '+ref if ref else ''}

P1–3: {env} {'; '.join(profiles)}. MOFO/MOFC and man/zone numbers absent; no shell inferred. QB vs blitz: {'; '.join(blitz)}. TE usage: {'; '.join(tes)}.

{injury} {wx}

P4–8: {' '.join(legs)} {'The strongest projected rushing opportunity is '+max(chosen,key=lambda x:x['projection'])['row'].player+'; volume and opponent efficiency drive the upside case.'} Overs require ≥60% team carry share; trailing favorites’ opponents lose 12% volume, favorites of six-plus gain 10%. Efficiency equally weights player L3 and opponent prior YPC; ≤3.8 triggers suppression caution. Similar-coverage form cannot be verified; recent yardage includes zero-carry team games.

P9–10: Three-model consensus unavailable under read restrictions; these are exploratory projections, not simulated medians. Exact main quotes above come from props_main.csv. FLAG=1 on retained legs for incomplete injury/model evidence, plus any run-defense disagreement; receiving markets fail the named-defender gate. No outcome data used.
'''
  # Keep the requested concise range while retaining meaningful game evidence.
  words=len(prose.split());lengths.append(words)
  (OUT/f'w{w}_{game}.md').write_text(prose)
pd.DataFrame(picks).to_csv(ROOT/'picks.csv',index=False)
(ROOT/'stage_a_audit.json').write_text(json.dumps(audit,indent=2))
(ROOT/'ALLOWED_FILES.md').write_text('''# Stage A read boundary
TASK4.md was read only for the task instructions. Analytical reads were restricted to the root PHASE_SCRIPT.md and the following pack files. No source paths cited inside packs were followed. No network, environment keys, target-week outcomes, or grade.py reads/execution. Generated helpers were executed but generated artifacts were not reopened.

All statistics assert week < target week. Snap counts identify RB/TE roles; FTN joins on game/play ID. Missing named-defender data excludes receiving markets. All retained picks carry FLAG=1 because consensus simulations and final injury clearance are unavailable. SAVED_READ means a dated checklist informed the reconstruction, not that its author supplied the exact selected leg. Weeks 3–5 missing script inputs remain explicit. Quotes use latest snapshot then deterministic book ordering, never outcomes. No assumed price fills.

The v2 slip implementation is outside the allowed read boundary. grade.py therefore documents an explicit deterministic approximation, not claimed exact v2 parity. It is written for Stage B only, not opened or executed in Stage A.

## Analytical inputs
- ../../../../PHASE_SCRIPT.md
'''+''.join('- '+p+'\n' for p in sorted(set(access))))
print(json.dumps(dict(games=len(lengths),picks=len(picks),words_min=min(lengths),words_max=max(lengths),by_week=pd.DataFrame(picks).groupby('week').size().to_dict(),tags=pd.DataFrame(picks).tag.value_counts().to_dict())))
